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
- **Finanzen (`finanzen`)**: 10 Artikel zu Aktienmärkten, Anleihen, Rohstoffen, Leitzinsen (Fed, EZB …), Börsengängen und Devisen, dazu die Kurstafel. Krypto nur, wenn es den Gesamtmarkt bewegt. Alles andere zu Krypto gehört in die Rubrik Krypto.
- **Krypto (`krypto`)**: 5 Artikel zu Bitcoin, Ether und Altcoins, Kryptobörsen, Hacks, ETFs/ETPs, Stablecoins, DeFi, On-Chain-Daten und Regulierung (MiCA, DAC8, SEC, BaFin …). Fachlich genau, der Leser kennt sich aus.
- **Vermögen & Beteiligungen (`vermoegen`)**: 5 Artikel zu Wealth Management, Family Offices und Private Equity: Deals, Fundraising, Exits, Fusionen von Vermögensverwaltern und Privatbanken, neue Family Offices, Regulierung, WealthTech, Studien (z. B. UBS Global Wealth Report). Gern mit Bezug zum deutschsprachigen Raum.
- **Köpfe des Tages (`koepfe`)**: 5 kurze Porträt-Meldungen darüber, was eine wichtige Person gerade tut: Konzernchefs, Notenbanker, Investoren, Gründer, Politiker, Prominente aus Sport und Kultur. Jeder Artikel dreht sich um eine Person (Titel mit Namen, Kicker z. B. „Köpfe · Notenbank“). Personalwechsel, Aussagen, Deals, Auftritte. Auch Privatleben gehört dazu (Hochzeit, Trennung, Familienzuwachs, Umzug, Rückzug aus der Öffentlichkeit), wenn es breit berichtet wird und Gesprächsthema ist. Dann gilt Klatsch ausdrücklich als erlaubt. Bedingungen: Die Sache ist von mindestens einem seriösen Medium berichtet oder von der Person selbst bestätigt, nicht nur Spekulation. Keine Mutmaßungen über Gesundheit. Kinder und Privatpersonen im Umfeld werden nicht namentlich in den Mittelpunkt gestellt.
- **München (`muenchen`)**: 5 Artikel zu Konzerten, Kultur, Theater, Festen (Wiesn, Frühlingsfest, Starkbierfest, Tollwood, Christkindlmärkte …) und Sport (FC Bayern, NFL, EHC, Basketball …) in München. Schwerpunkt ist der **Kartenvorverkauf**: Wann gehen Tickets live (Datum, Uhrzeit, Presales und wer Zugang hat), wo gibt es sie offiziell, was kosten sie, ist etwas ausverkauft. Neue Vorverkaufsstarts der nächsten Tage haben Vorrang vor allgemeinen Kulturmeldungen. Jeder Artikel bekommt, wenn es um Karten geht, den Kasten `karten`. Dazu gehören zwei Listen:
  - **Vorverkaufskalender (`vorverkauf`)**: alle gefundenen Vorverkaufsstarts für München in den nächsten rund 14 Tagen, je Phase ein Eintrag (Presale und allgemeiner Verkauf getrennt). Nur mit belegtem Datum; Uhrzeit nur, wenn sie in der Quelle steht.
  - **Aktionen & Frühbucher (`aktionen`)**: aktuelle Angebote, damit Moritz rechtzeitig buchen und Frühbucherrabatte nutzen kann. Bereiche (Feld `kategorie`, einheitlich halten): „Restaurants & Bars“ (Restaurant Week, Menü-Aktionen, Weihnachtsfeier-Frühbucher, Happy Hours), „Kino“, „Mode & Designerläden“ (Pop-ups, Sales, Events), „Trachten“, „Sport“ (FC Bayern, TSV 1860, FC Bayern Basketball, EHC Red Bull München: Ticketaktionen, Familientage, Probe-Dauerkarten), „Freizeit & Erlebnis“ (Jochen Schweizer Arena, o2 Surftown MUC, Therme Erding …), „Theater & Konzerte“ (Frühbucherpreise, Abos, Last-Minute) und „Museen“ (Gratisabende, 1-Euro-Sonntag mit nächstem Termin). Anbieter ist der Betrieb selbst oder eine offizielle Stelle (muenchen.de, Verein, Veranstalter); keine Gutschein-Sammelportale und keine Deal-Seiten als Quelle. Konkrete Daten haben Vorrang vor Daueraktionen; ist ein Datum aus einer älteren Übersicht abgeleitet, steht das im `hinweis`. Abgelaufene Angebote fliegen raus. Bis zu etwa 15 Einträge.
  - **Gewinnspiele & Rabatte (`gewinnspiele`)**: aktuelle Verlosungen und Vergünstigungen zu Münchner Veranstaltungen, gern lukrativ (begehrte oder teure Karten, VIP, Reise). **Keine Scams.** Aufgenommen wird nur, was alle Bedingungen erfüllt: Anbieter ist der Veranstalter, ein offizieller Partner/Sponsor, ein Verkehrsunternehmen oder ein etabliertes Medium (z. B. SZ, AZ, tz, Merkur, BR, Antenne Bayern, Radio Arabella, IN München, muenchen.de) und die Aktion steht auf dessen eigener Website oder offiziellem Kanal; Teilnahme kostenlos und ohne Kaufpflicht, kein Bezahl-Abo, keine Mehrwertnummer oder Premium-SMS; Teilnahmebedingungen oder Impressum vorhanden; keine Abfrage von Bank- oder Kartendaten. Ausgeschlossen sind Glücksspiel- und Wettanbieter, Kettenbriefe, „Teilen & Liken“-Seiten unbekannter Profile, Gutschein-Sammelportale und Ticket-Zweitmärkte. Abgelaufene Fristen fliegen raus. Im Feld `pruefung` steht kurz, warum die Aktion seriös ist. Findet sich nichts Passendes, bleibt die Liste leer.
- **Feuilleton**: Weisheit/Zitat des Tages (echtes, korrekt zugeordnetes Zitat, gemeinfrei bzw. vor 1929 veröffentlicht), Witz des Tages (eigener, harmloser Witz) und Rätsel des Tages mit Auflösung. Jeden Tag ein neues Stück, keine Wiederholungen aus früheren Ausgaben.

## Regeln für Artikel

- Sprache Deutsch, sachlich, Stil einer seriösen Tageszeitung. Eigene Zusammenfassungen, keine kopierten Passagen.
- **Höchstens 500 Wörter**, üblich sind 180 bis 350, in 3 bis 4 Absätzen.
- Jeder Artikel nennt 2 bis 3 **echte Quellen-URLs**, die bei der Recherche tatsächlich gefunden wurden. Keine erfundenen Links.
- Jede Zahl und jeder Name muss aus den Quellen stammen. Was unsicher ist, wird weggelassen.
- Politische Themen werden neutral dargestellt, ohne eigene Wertung.
- Keine Meldung doppelt, auch nicht über die Rubriken hinweg. Ein Thema darf in einer zweiten Rubrik nur mit klar anderem Blickwinkel auftauchen (z. B. Weltgeschehen: Hack, Finanzen: Kursfolgen).
- Neue Themen vor Fortsetzungen: Eine Geschichte aus der Vorausgabe kommt nur wieder, wenn es echte Neuigkeiten gibt.

## „Wer berichtet?“: politisches Spektrum

Unter jedem Artikel zeigt die Seite, wie sich die Medien, die über das Thema berichtet haben, auf links, Mitte und rechts verteilen. Die Prozente rechnet die Seite selbst aus `medien.json` aus. Die Redaktion schreibt **keine Prozentzahlen**, sondern nur das Feld `berichterstattung`: eine Liste der Domains, die über das Thema berichtet haben.

So wird die Liste erstellt:
- Für jeden Artikel eigens nach dem Thema suchen, z. B. mit Stichworten aus der Überschrift plus Datum, auf Englisch und auf Deutsch.
- Aufnehmen werden alle Medien aus `medien.json`, die in den Ergebnissen mit einem Bericht zum Thema auftauchen. Nicht gezielt nach einer Seite suchen und nichts weglassen, damit die Verteilung nicht verzerrt wird.
- Die eigenen Quellen-Links zählen mit, wenn sie in `medien.json` stehen. Fachmedien ohne Einordnung (z. B. CoinDesk) dürfen in der Liste stehen, sie werden nur nicht mitgezählt.
- Ziel sind mindestens 3 eingeordnete Medien pro Artikel. Bei Weltgeschehen lohnt sich eine zweite Suche (andere Sprache, andere Stichworte), wenn es weniger sind. Wirtschafts-, Finanz-, Krypto- und Vermögensthemen stehen oft nur in Fachmedien ohne Einordnung. Dann bleibt die Liste kurz, die Seite zeigt „zu wenige Medien“. Niemals Medien eintragen, die nicht tatsächlich berichtet haben, nur um die Zahl zu erreichen. Das Prüfskript meldet zu kurze Listen nur als Hinweis, nicht als Fehler.
- Nur Domains, ohne `https://` und `www.`, z. B. `["reuters.com", "foxnews.com", "spiegel.de"]`.
- `medien.json` wird nicht von der Redaktion geändert. Neue Medien nimmt nur Moritz auf.

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
   "quellen": [["Reuters", "https://…"], ["Tagesschau", "https://…"]],
   "berichterstattung": ["reuters.com", "tagesschau.de", "foxnews.com", "nytimes.com", "faz.net"]
  }
 ],
 "feuilleton": [
  {"id": "feuil-weisheit", "art": "weisheit", "tags": ["Weisheit"], "kicker": "Weisheit des Tages", "titel": "…", "zitat": "„…“", "urheber": "…", "text": "Kurze Einordnung."},
  {"id": "feuil-witz", "art": "witz", "tags": ["Humor"], "kicker": "Witz des Tages", "titel": "…", "text": "…"},
  {"id": "feuil-raetsel", "art": "raetsel", "tags": ["Rätsel"], "kicker": "Rätsel des Tages", "titel": "…", "text": "…", "loesung": "…"}
 ]
}
```

- IDs: `welt-01` … `welt-10`, `wirt-01` … `wirt-10`, `fin-01` … `fin-10`, `krypto-01` … `krypto-05`, `verm-01` … `verm-05`, `koepfe-01` … `koepfe-05`, `muc-01` … `muc-05`, innerhalb der Rubrik nach Wichtigkeit geordnet.
- München gibt es seit der Ausgabe vom 3. November 2026. Zusätzliche Felder (alle Angaben aus den Quellen, sonst weglassen). Im München-Artikel:

```json
"karten": {"vorverkauf": "Presale Mi, 4.11.2026, 11 Uhr · allgemein Fr, 6.11.2026, 11 Uhr", "termin": "Sa, 22.5.2027, 20 Uhr", "ort": "Olympiahalle", "preise": "ab 59 €", "stelle": "Eventim", "link": "https://…"}
```

Auf oberster Ebene der Ausgabe:

```json
"vorverkauf": [
 {"start": "2026-11-04T11:00", "veranstaltung": "Scorpions", "termin": "22.5.2027", "ort": "Olympiahalle", "stelle": "Eventim", "url": "https://…", "hinweis": "Presale"}
],
"gewinnspiele": [
 {"art": "gewinnspiel", "titel": "…", "anbieter": "IN München", "gewinn": "5 × 2 Karten für den 20.11.", "bis": "2026-11-12", "teilnahme": "Formular ausfüllen", "pruefung": "etabliertes Stadtmagazin, Teilnahmebedingungen verlinkt, kostenlos", "url": "https://…"}
]
```

Ebenfalls auf oberster Ebene:

```json
"aktionen": [
 {"kategorie": "Restaurants & Bars", "titel": "…", "anbieter": "…", "angebot": "Was es gibt und was es kostet", "wann": "läuft bis 22.11.2026", "buchen_bis": "2026-11-22", "hinweis": "Bedingungen, Einschränkungen", "frueh": false, "url": "https://…"}
]
```

`frueh: true` markiert Frühbucher-Angebote. `start` ist `JJJJ-MM-TT` oder `JJJJ-MM-TTTHH:MM` (Berliner Zeit), `art` ist `gewinnspiel` oder `rabatt`, `bis` ist optional (`JJJJ-MM-TT`). Die Seite sortiert beide Listen selbst und ist unter `#muenchen`, `#vorverkauf` und `#gewinnspiele` direkt erreichbar, die Aktionen unter `#aktionen`.
- Die drei neuen Rubriken gibt es seit der Ausgabe vom 4. November 2026. Ältere Ausgaben haben sie nicht, die Seite blendet sie dort aus.
- Kurstafel (8 Werte): DAX, S&P 500, Nasdaq, Brent, Gold, Bitcoin, EUR/USD, Rendite 10-jähriger US-Anleihen. `richtung` ist `up`, `down` oder `flat`.
- `tags`: 1 bis 4 kurze Themen-Schlagworte. Sie speisen das Leserbarometer, also einheitlich halten (z. B. immer „Krypto“, nicht mal „Kryptowährungen“).
