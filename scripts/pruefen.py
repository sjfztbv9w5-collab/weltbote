#!/usr/bin/env python3
"""Prüft eine Ausgabe des Weltboten, bevor sie veröffentlicht wird.

Aufruf:  python3 scripts/pruefen.py ausgaben/2026-11-03.json
Endet mit Exit-Code 1 und einer Fehlerliste, wenn etwas nicht stimmt.
"""
import json
import re
import sys
from pathlib import Path

RUBRIKEN_BASIS = {"welt": 10, "wirtschaft": 10, "finanzen": 10}
# Seit der Ausgabe vom 4. November 2026 zusätzlich:
RUBRIKEN_NEU = {"krypto": 5, "vermoegen": 5, "koepfe": 5}
NEU_AB = "2026-11-04"
# Seit der Ausgabe vom 3. November 2026: München mit Vorverkaufskalender und Gewinnspielen
RUBRIK_MUENCHEN = {"muenchen": 5}
MUENCHEN_AB = "2026-11-03"
# Seit der Ausgabe vom 5. November 2026: München-Schlagzeilen („Kurz notiert“)
MUC_KURZ_AB = "2026-11-05"
# Seit der Ausgabe vom 5. November 2026: Künstliche Intelligenz
RUBRIK_KI = {"ki": 5}
KI_AB = "2026-11-05"
# Seit der Ausgabe vom 6. November 2026: Gute Nachrichten
RUBRIK_GUT = {"gut": 10}
GUT_AB = "2026-11-06"
# Seit der Ausgabe vom 14. November 2026: Wissenschaft (mit Vortrag des Tages) und Transfermarkt
RUBRIK_WISS = {"wissenschaft": 5}
WISS_AB = "2026-11-14"
FUSS_AB = "2026-11-14"
FUSS_MIN, FUSS_MAX = 1, 20
FUSS_STATUS = ("fix", "verhandlung", "geruecht")
ALLE_RUBRIKEN = {**RUBRIKEN_BASIS, **RUBRIKEN_NEU, **RUBRIK_MUENCHEN, **RUBRIK_KI, **RUBRIK_GUT, **RUBRIK_WISS, "fussball": None}
ISO_START = re.compile(r"\d{4}-\d{2}-\d{2}(T\d{2}:\d{2})?$")
MAX_WOERTER = 500


def _finde(domain: str, medien: dict):
    d = domain.lower().split("//")[-1].split("/")[0].removeprefix("www.")
    while "." in d:
        if d in medien:
            return medien[d]["name"]
        d = d.split(".", 1)[1]
    return None


HINWEISE: list[str] = []


def pruefe(pfad: Path) -> list[str]:
    fehler = []
    try:
        d = json.loads(pfad.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return [f"JSON nicht lesbar: {e}"]

    datum = d.get("datum", "")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", datum):
        fehler.append("'datum' fehlt oder ist nicht im Format JJJJ-MM-TT")
    elif pfad.stem != datum:
        fehler.append(f"Dateiname {pfad.name} passt nicht zu datum {datum}")

    for feld in ("datumszeile", "kolophon", "kurse_stand"):
        if not isinstance(d.get(feld), str) or not d[feld].strip():
            fehler.append(f"Feld '{feld}' fehlt oder ist leer")

    kurse = d.get("kurse", [])
    if not isinstance(kurse, list) or len(kurse) < 6:
        fehler.append("'kurse' braucht mindestens 6 Einträge")
    for k in kurse if isinstance(kurse, list) else []:
        for f in ("name", "wert", "veraenderung", "richtung"):
            if f not in k:
                fehler.append(f"Kurs {k.get('name', '?')}: Feld '{f}' fehlt")
        if k.get("richtung") not in ("up", "down", "flat", ""):
            fehler.append(f"Kurs {k.get('name', '?')}: richtung muss up/down/flat/'' sein")

    artikel = d.get("artikel", [])
    ids = set()
    RUBRIKEN = dict(RUBRIKEN_BASIS)
    if datum >= NEU_AB:
        RUBRIKEN.update(RUBRIKEN_NEU)
    if datum >= MUENCHEN_AB:
        RUBRIKEN.update(RUBRIK_MUENCHEN)
    if datum >= KI_AB:
        RUBRIKEN.update(RUBRIK_KI)
    if datum >= GUT_AB:
        RUBRIKEN.update(RUBRIK_GUT)
    if datum >= WISS_AB:
        RUBRIKEN.update(RUBRIK_WISS)
    zaehler = {r: 0 for r in ALLE_RUBRIKEN}
    for a in artikel:
        aid = a.get("id", "?")
        if aid in ids:
            fehler.append(f"Doppelte id {aid}")
        ids.add(aid)
        r = a.get("rubrik")
        if r not in ALLE_RUBRIKEN:
            fehler.append(f"{aid}: unbekannte rubrik {r!r}")
        else:
            zaehler[r] += 1
        for f in ("kicker", "titel", "deck"):
            if not isinstance(a.get(f), str) or not a[f].strip():
                fehler.append(f"{aid}: Feld '{f}' fehlt")
        if not isinstance(a.get("tags"), list) or not a["tags"]:
            fehler.append(f"{aid}: 'tags' fehlt")
        text = a.get("text")
        if not isinstance(text, list) or not text or not all(isinstance(p, str) for p in text):
            fehler.append(f"{aid}: 'text' muss eine Liste von Absätzen sein")
        else:
            w = len(" ".join(text).split())
            if r == "fussball":
                if len(text) != 1:
                    fehler.append(f"{aid}: Transfer-Artikel haben genau einen Absatz (3 bis 5 Sätze)")
                if not 35 <= w <= 140:
                    fehler.append(f"{aid}: {w} Wörter, Transfer-Artikel brauchen 35 bis 140 (3 bis 5 Sätze)")
            else:
                if w > MAX_WOERTER:
                    fehler.append(f"{aid}: {w} Wörter (max. {MAX_WOERTER})")
                if w < 80:
                    fehler.append(f"{aid}: nur {w} Wörter, zu dünn")
        if r == "fussball":
            if a.get("status") not in FUSS_STATUS:
                fehler.append(f"{aid}: 'status' muss fix, verhandlung oder geruecht sein")
            t = a.get("transfer")
            if not isinstance(t, dict) or not t.get("spieler"):
                fehler.append(f"{aid}: 'transfer' mit mindestens 'spieler' fehlt")
        quellen = a.get("quellen")
        if not isinstance(quellen, list) or not quellen:
            fehler.append(f"{aid}: keine Quellen")
        else:
            for q in quellen:
                if not (isinstance(q, list) and len(q) == 2 and str(q[1]).startswith("https://")):
                    fehler.append(f"{aid}: Quelle {q!r} muss [Name, https-URL] sein")
    if datum >= NEU_AB:
        medien = json.loads((pfad.parent.parent / "medien.json").read_text(encoding="utf-8")).get("medien", {}) \
            if (pfad.parent.parent / "medien.json").exists() else {}
        for a in artikel:
            aid = a.get("id", "?")
            if a.get("rubrik") == "fussball":
                continue
            b = a.get("berichterstattung")
            if not isinstance(b, list) or not all(isinstance(x, str) and "." in x and " " not in x for x in b):
                fehler.append(f"{aid}: 'berichterstattung' muss eine Liste von Domains sein")
                continue
            bekannt = {_finde(x, medien) for x in b} - {None}
            if a.get("rubrik") == "welt" and len(bekannt) < 3:
                HINWEISE.append(f"{aid}: nur {len(bekannt)} eingeordnete Medien, die Seite zeigt keine Verteilung")
    for r, soll in RUBRIKEN.items():
        if zaehler[r] != soll:
            fehler.append(f"Rubrik {r}: {zaehler[r]} Artikel statt {soll}")
    if datum >= FUSS_AB:
        n = zaehler["fussball"]
        if not FUSS_MIN <= n <= FUSS_MAX:
            fehler.append(f"Rubrik fussball: {n} Artikel, erlaubt sind {FUSS_MIN} bis {FUSS_MAX}")
        elif n < 3:
            HINWEISE.append(f"Transfermarkt: nur {n} Meldung(en), wirklich nicht mehr los?")
    if datum >= WISS_AB:
        fehler += pruefe_vortrag(d.get("vortrag"), pfad, datum)

    fehler += pruefe_muenchen(d, artikel, datum)

    feuil = {f.get("art"): f for f in d.get("feuilleton", [])}
    for art in ("weisheit", "witz", "raetsel"):
        if art not in feuil:
            fehler.append(f"Feuilleton: '{art}' fehlt")
    if "weisheit" in feuil and not all(feuil["weisheit"].get(k) for k in ("zitat", "urheber", "text")):
        fehler.append("Weisheit braucht zitat, urheber und text")
    if "raetsel" in feuil and not feuil["raetsel"].get("loesung"):
        fehler.append("Rätsel braucht eine loesung")
    for f in d.get("feuilleton", []):
        for k in ("id", "kicker", "titel", "tags"):
            if not f.get(k):
                fehler.append(f"Feuilleton {f.get('art', '?')}: Feld '{k}' fehlt")

    return fehler


def pruefe_vortrag(v, pfad: Path, datum: str) -> list[str]:
    if not isinstance(v, dict):
        return ["'vortrag' (Vortrag des Tages) fehlt"]
    fehler = []
    for f in ("id", "fachgebiet", "titel", "einstieg"):
        if not isinstance(v.get(f), str) or not v[f].strip():
            fehler.append(f"Vortrag: Feld '{f}' fehlt")
    if not isinstance(v.get("tags"), list) or not v["tags"]:
        fehler.append("Vortrag: 'tags' fehlt")
    text = v.get("text")
    if not isinstance(text, list) or not 3 <= len(text) <= 5 or not all(isinstance(p, str) for p in text):
        fehler.append("Vortrag: 'text' braucht 3 bis 5 Absätze")
    else:
        w = len(" ".join(text).split())
        if not 250 <= w <= 450:
            fehler.append(f"Vortrag: {w} Wörter, erlaubt sind 250 bis 450")
    m = v.get("merksaetze")
    if not isinstance(m, list) or len(m) != 3:
        fehler.append("Vortrag: genau 3 'merksaetze'")
    else:
        for i, s in enumerate(m, 1):
            if len(str(s).split()) > 20:
                fehler.append(f"Vortrag: Merksatz {i} zu lang (max. 20 Wörter)")
    b = v.get("begriffe")
    if not isinstance(b, list) or not 2 <= len(b) <= 4 or not all(isinstance(x, list) and len(x) == 2 for x in b):
        fehler.append("Vortrag: 'begriffe' braucht 2 bis 4 Paare [Begriff, Erklärung]")
    q = v.get("quellen")
    if not isinstance(q, list) or not q or not all(isinstance(x, list) and len(x) == 2 and _https(x[1]) for x in q):
        fehler.append("Vortrag: 'quellen' als Liste von [Name, https-URL]")
    titel = str(v.get("titel", "")).strip().lower()
    for p in pfad.parent.glob("????-??-??.json"):
        if p.stem >= datum:
            continue
        try:
            alt = json.loads(p.read_text(encoding="utf-8")).get("vortrag") or {}
        except Exception:  # noqa: BLE001
            continue
        if str(alt.get("titel", "")).strip().lower() == titel:
            fehler.append(f"Vortrag: Thema „{v.get('titel')}“ gab es schon am {p.stem}")
    return fehler


def _https(u) -> bool:
    return isinstance(u, str) and u.startswith("https://")


def pruefe_muenchen(d: dict, artikel: list, datum: str) -> list[str]:
    fehler = []
    for a in artikel:
        if a.get("rubrik") != "muenchen" or "karten" not in a:
            continue
        k = a["karten"]
        aid = a.get("id", "?")
        if not isinstance(k, dict) or not k.get("vorverkauf"):
            fehler.append(f"{aid}: 'karten' braucht mindestens 'vorverkauf'")
        elif "link" in k and not _https(k["link"]):
            fehler.append(f"{aid}: karten.link muss eine https-URL sein")
    vvk = d.get("vorverkauf", [])
    if not isinstance(vvk, list):
        return fehler + ["'vorverkauf' muss eine Liste sein"]
    for i, v in enumerate(vvk, 1):
        if not ISO_START.match(str(v.get("start", ""))):
            fehler.append(f"vorverkauf {i}: 'start' muss JJJJ-MM-TT oder JJJJ-MM-TTTHH:MM sein")
        if not v.get("veranstaltung"):
            fehler.append(f"vorverkauf {i}: 'veranstaltung' fehlt")
        if not _https(v.get("url")):
            fehler.append(f"vorverkauf {i}: 'url' (https) fehlt")
    if datum >= MUC_KURZ_AB:
        kurz = d.get("muenchen_schlagzeilen")
        if not isinstance(kurz, list) or len(kurz) != 5:
            fehler.append("'muenchen_schlagzeilen' braucht genau 5 Einträge")
        else:
            for i, s in enumerate(kurz, 1):
                if not s.get("titel"):
                    fehler.append(f"München-Schlagzeile {i}: 'titel' fehlt")
                elif len(s["titel"]) > 110:
                    fehler.append(f"München-Schlagzeile {i}: Titel zu lang (max. 110 Zeichen)")
                if s.get("satz") and len(s["satz"].split()) > 30:
                    fehler.append(f"München-Schlagzeile {i}: 'satz' zu lang (max. 30 Wörter)")
                if not _https(s.get("url")):
                    fehler.append(f"München-Schlagzeile {i}: 'url' (https) fehlt")
    for liste in ("aktionen", "gewinnspiele"):
        for x in d.get(liste, []) if isinstance(d.get(liste), list) else []:
            if "regelmaessig" in x and not isinstance(x["regelmaessig"], bool):
                fehler.append(f"{liste} {x.get('titel', '?')}: 'regelmaessig' muss true oder false sein")
            if x.get("regelmaessig") and len(str(x.get("angebot") or x.get("gewinn") or "").split()) > 15:
                fehler.append(f"{liste} {x.get('titel', '?')}: regelmäßiges Angebot in höchstens 15 Wörtern beschreiben")
    gw = d.get("gewinnspiele", [])
    if not isinstance(gw, list):
        return fehler + ["'gewinnspiele' muss eine Liste sein"]
    for i, g in enumerate(gw, 1):
        name = g.get("titel", f"Nr. {i}")
        if g.get("art") not in ("gewinnspiel", "rabatt"):
            fehler.append(f"gewinnspiel {name}: 'art' muss gewinnspiel oder rabatt sein")
        for f in ("titel", "anbieter", "pruefung"):
            if not g.get(f):
                fehler.append(f"gewinnspiel {name}: Feld '{f}' fehlt")
        if not _https(g.get("url")):
            fehler.append(f"gewinnspiel {name}: 'url' (https) fehlt")
        bis = g.get("bis")
        if bis:
            if not ISO_START.match(str(bis)):
                fehler.append(f"gewinnspiel {name}: 'bis' muss JJJJ-MM-TT sein")
            elif str(bis)[:10] < datum:
                fehler.append(f"gewinnspiel {name}: Frist {bis} ist schon abgelaufen, herausnehmen")
    ak = d.get("aktionen", [])
    if not isinstance(ak, list):
        return fehler + ["'aktionen' muss eine Liste sein"]
    for i, x in enumerate(ak, 1):
        name = x.get("titel", f"Nr. {i}")
        for f in ("kategorie", "titel", "anbieter", "angebot"):
            if not x.get(f):
                fehler.append(f"aktion {name}: Feld '{f}' fehlt")
        if not _https(x.get("url")):
            fehler.append(f"aktion {name}: 'url' (https) fehlt")
        bis = x.get("buchen_bis")
        if bis:
            if not ISO_START.match(str(bis)):
                fehler.append(f"aktion {name}: 'buchen_bis' muss JJJJ-MM-TT sein")
            elif str(bis)[:10] < datum:
                fehler.append(f"aktion {name}: {bis} ist schon vorbei, herausnehmen")
    return fehler


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    pfad = Path(sys.argv[1])
    fehler = pruefe(pfad)
    idx = pfad.parent / "index.json"
    if idx.exists():
        liste = json.loads(idx.read_text(encoding="utf-8")).get("ausgaben", [])
        if pfad.stem not in liste:
            fehler.append(f"{pfad.stem} fehlt in ausgaben/index.json")
    if HINWEISE:
        print("Hinweise (kein Fehler, wenn wirklich nicht mehr Berichterstattung zu finden ist):")
        for h in HINWEISE:
            print(" -", h)
    if fehler:
        print("NICHT in Ordnung:")
        for f in fehler:
            print(" -", f)
        return 1
    print(f"In Ordnung: {pfad.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
