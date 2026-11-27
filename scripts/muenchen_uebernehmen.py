#!/usr/bin/env python3
"""Übernimmt den München-Teil aus muenchen/aktuell.json in eine Tagesausgabe.

Der München-Teil wird nur alle 3 Tage neu recherchiert (eigene geplante Aufgabe).
Die Tagesausgabe übernimmt ihn mit diesem Skript und wirft dabei Abgelaufenes heraus.

Aufruf:  python3 scripts/muenchen_uebernehmen.py ausgaben/2026-11-28.json
Die Ausgabe-Datei muss schon existieren (mit 'datum'); sie wird ergänzt.
"""
import json
import sys
from datetime import date
from pathlib import Path

QUELLE = Path(__file__).resolve().parent.parent / "muenchen" / "aktuell.json"


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    ziel = Path(sys.argv[1])
    d = json.loads(ziel.read_text(encoding="utf-8"))
    heute = d["datum"]
    m = json.loads(QUELLE.read_text(encoding="utf-8"))

    d["artikel"] = [a for a in d.get("artikel", []) if a.get("rubrik") != "muenchen"] + m["artikel"]
    d["muenchen_schlagzeilen"] = m["muenchen_schlagzeilen"]
    d["vorverkauf"] = [v for v in m["vorverkauf"] if v["start"][:10] >= heute]
    d["aktionen"] = [a for a in m["aktionen"] if not a.get("buchen_bis") or a["buchen_bis"] >= heute]
    d["gewinnspiele"] = [g for g in m["gewinnspiele"] if not g.get("bis") or g["bis"] >= heute]
    d["muenchen_stand"] = m["stand"]

    ziel.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    alter = (date.fromisoformat(heute) - date.fromisoformat(m["stand"])).days
    print(f"München-Teil vom {m['stand']} übernommen ({alter} Tage alt): "
          f"{len(m['artikel'])} Artikel, {len(d['vorverkauf'])} Vorverkauf, "
          f"{len(d['aktionen'])} Aktionen, {len(d['gewinnspiele'])} Gewinnspiele")
    if alter > 3:
        print(f"WARNUNG: München-Teil ist {alter} Tage alt – die München-Aufgabe ist offenbar ausgefallen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
