# Redaktionsanleitung „Der Weltbote“

Diese Datei beschreibt, wie jeden Morgen eine neue Ausgabe entsteht. Die geplante Aufgabe hält sich genau daran.

## Aufbau des Repos

- `index.html`: die Seite (Layout um 1910). Sie lädt `ausgaben/index.json` und zeigt die neueste Ausgabe. Ältere Ausgaben lassen sich über die Auswahl im Kopf öffnen. **Nicht anfassen**, außer Moritz wünscht Layout-Änderungen.
- `ausgaben/JJJJ-MM-TT.json`: eine Ausgabe pro Tag.
- `ausgaben/index.json`: `{"ausgaben": ["2026-11-02", "2026-11-03", …]}`, die Liste aller Ausgaben.
- `scripts/pruefen.py`: prüft eine Ausgabe vor der Veröffentlichung.

## Inhalt einer Ausgabe

- **Weltgeschehen (`welt`)**: die 10 wichtigsten Meldungen der letzten 24 Stunden weltweit, unabhängig vom Ressort, geordnet nach ihrem Gewicht auf den Titelseiten großer internationaler Medien (Reuters, AP, BBC, NYT, FT, Al Jazeera, Tagesschau, Spiegel, FAZ …). Platz 1 wird als großer Aufmacher gesetzt.
- **Wirtschaft (`wirtschaft`)**: 10 Artikel zu Unternehmen, Übernahmen, Quartalszahlen und Welthandel.
- **Finanzen (`finanzen`)**: 10 Artikel zu Aktienmärkten, Anleihen, Rohstoffen, Leitzinsen (Fed, EZB …), Börsengängen, Devisen und Krypto, dazu die Kurstafel.
- **Feuilleton**: Weisheit/Zitat des Tages (echtes, korrekt zugeordnetes Zitat, gemeinfrei bzw. vor 1929 veröffentlicht), Witz des Tages (eigener, harmloser Witz) und Rätsel des Tages mit Auflösung. Jeden Tag ein neues Stück, keine Wiederholungen aus früheren Ausgaben.

## Regeln für Artikel

- Sprache Deutsch, sachlich, Stil einer seriösen Tageszeitung. Eigene Zusammenfassungen, keine kopierten Passagen.
- **Höchstens 500 Wörter**, üblich sind 180 bis 350, in 3 bis 4 Absätzen.
- Jeder Artikel nennt 2 bis 3 **echte Quellen-URLs**, die bei der Recherche tatsächlich gefunden wurden. Keine erfundenen Links.
- Jede Zahl und jeder Name muss aus den Quellen stammen. Was unsicher ist, wird weggelassen.
- Politische Themen werden neutral dargestellt, ohne eigene Wertung.
- Keine Meldung doppelt, auch nicht über die Rubriken hinweg. Ein Thema darf in einer zweiten Rubrik nur mit klar anderem Blickwinkel auftauchen (z. B. Weltgeschehen: Hack, Finanzen: Kursfolgen).
- Neue Themen vor Fortsetzungen: Eine Geschichte aus der Vorausgabe kommt nur wieder, wenn es echte Neuigkeiten gibt.

## Bewertungen

Die Sterne werden in Moritz' Browser gespeichert (localStorage) und sind für die Redaktion nicht einsehbar. Wenn Moritz Vorlieben nennt, gehören sie in den Abschnitt unten.

### Vorlieben des Lesers

- (noch keine)

## JSON-Format

```json
{
 "datum": "2026-11-03",
 "datumszeile": "Dienstag, den 3. November 2026",
 "redaktionsschluss": "6 Uhr",
 "kurse_stand": "Stand: Schlusskurse vom Vortag, Krypto 6 Uhr MEZ",
 "kolophon": "Auswahl der Weltnachrichten nach ihrem Gewicht auf den Titelseiten großer internationaler Medien am 3. November 2026. Alle Texte sind eigene Zusammenfassungen, die Originalquelle ist jeweils verlinkt.",
 "kurse": [
  {"name": "DAX", "wert": "24.120", "veraenderung": "+0,4 %", "richtung": "up"}
 ],
 "artikel": [
  {
   "id": "welt-01",
   "rubrik": "welt",
   "tags": ["USA", "Wahlen"],
   "kicker": "Vereinigte Staaten · Zwischenwahl",
   "titel": "Überschrift",
   "deck": "Unterzeile in einem Satz.",
   "text": ["Absatz 1", "Absatz 2", "Absatz 3"],
   "quellen": [["Reuters", "https://…"], ["Tagesschau", "https://…"]]
  }
 ],
 "feuilleton": [
  {"id": "feuil-weisheit", "art": "weisheit", "tags": ["Weisheit"], "kicker": "Weisheit des Tages", "titel": "…", "zitat": "„…“", "urheber": "…", "text": "Kurze Einordnung."},
  {"id": "feuil-witz", "art": "witz", "tags": ["Humor"], "kicker": "Witz des Tages", "titel": "…", "text": "…"},
  {"id": "feuil-raetsel", "art": "raetsel", "tags": ["Rätsel"], "kicker": "Rätsel des Tages", "titel": "…", "text": "…", "loesung": "…"}
 ]
}
```

- IDs: `welt-01` … `welt-10`, `wirt-01` … `wirt-10`, `fin-01` … `fin-10`, innerhalb der Rubrik nach Wichtigkeit geordnet.
- Kurstafel (8 Werte): DAX, S&P 500, Nasdaq, Brent, Gold, Bitcoin, EUR/USD, Rendite 10-jähriger US-Anleihen. `richtung` ist `up`, `down` oder `flat`.
- `tags`: 1 bis 4 kurze Themen-Schlagworte. Sie speisen das Leserbarometer, also einheitlich halten (z. B. immer „Krypto“, nicht mal „Kryptowährungen“).
