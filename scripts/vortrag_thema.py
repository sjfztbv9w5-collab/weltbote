#!/usr/bin/env python3
"""Würfelt das Fachgebiet für den „Vortrag des Tages“ aus.

Aufruf:  python3 scripts/vortrag_thema.py
Lässt die Fachgebiete der letzten 10 Ausgaben aus und zeigt die bisherigen
Vortragstitel, damit sich kein Thema wiederholt.
"""
import json
import random
from pathlib import Path

FACHGEBIETE = [
    "Astronomie", "Kosmologie", "Raumfahrt", "Teilchenphysik", "Quantenphysik",
    "Thermodynamik", "Optik", "Chemie", "Materialwissenschaft", "Biochemie",
    "Genetik", "Evolutionsbiologie", "Zoologie", "Botanik", "Mikrobiologie",
    "Ökologie", "Meeresforschung", "Neurowissenschaft", "Medizin", "Immunologie",
    "Psychologie", "Geologie", "Vulkanologie", "Meteorologie", "Klimaforschung",
    "Mathematik", "Informatik", "Ingenieurwesen", "Energietechnik",
    "Archäologie", "Paläontologie", "Anthropologie", "Sprachwissenschaft",
    "Wirtschaftswissenschaft", "Wissenschaftsgeschichte",
]


def main() -> None:
    ordner = Path(__file__).resolve().parent.parent / "ausgaben"
    vortraege = []
    for p in sorted(ordner.glob("????-??-??.json")):
        try:
            v = json.loads(p.read_text(encoding="utf-8")).get("vortrag")
        except Exception:  # noqa: BLE001
            continue
        if v:
            vortraege.append((p.stem, v.get("fachgebiet", ""), v.get("titel", "")))
    zuletzt = {f for _, f, _ in vortraege[-10:]}
    auswahl = [f for f in FACHGEBIETE if f not in zuletzt] or FACHGEBIETE
    print("Fachgebiet heute:", random.SystemRandom().choice(auswahl))
    if vortraege:
        print("\nBisherige Vorträge (nicht wiederholen):")
        for datum, fach, titel in vortraege:
            print(f" - {datum} [{fach}] {titel}")


if __name__ == "__main__":
    main()
