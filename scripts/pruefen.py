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
ALLE_RUBRIKEN = {**RUBRIKEN_BASIS, **RUBRIKEN_NEU}
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
            if w > MAX_WOERTER:
                fehler.append(f"{aid}: {w} Wörter (max. {MAX_WOERTER})")
            if w < 80:
                fehler.append(f"{aid}: nur {w} Wörter, zu dünn")
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
