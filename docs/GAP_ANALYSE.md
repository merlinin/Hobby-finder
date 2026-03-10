# Gap-Analyse: Ist-Zustand vs. Project Compass

## 1. Ist-Zustand

### Aktuelle Module/Dateien und Verantwortung

- `app.py`
  - Flask-App-Factory und HTTP-Routen (`/`, `/hobbies`, `/attributes`, `/wordcloud.png`).
  - Orchestriert Datenbank-Setup und Seed-Aufruf beim Start.
  - Rendert Template und liefert JSON/PNG aus.
- `models.py`
  - SQLAlchemy-Datenmodell (`Hobby`, `Attribute`, `HobbyAttribute`).
  - Seed-Logik mit Beispiel-Attributen/Hobbys.
- `wordcloud_service.py`
  - Textnormalisierung, Stopword-Filter, Frequenzzählung.
  - Wordcloud-Erzeugung inkl. Farbklassifikation nach Wortkategorien.
- `analysis/analyze_definitions.py`
  - CLI-Analyse von `data/definitions.json`.
  - Tokenisierung/Frequenzen, optionaler Wordcloud-Export.
- `templates/index.html`
  - UI für Landingpage mit Wordcloud und Top-Wörtern.
- `tests/test_app.py`
  - Testet Landingpage und PNG-Endpoint.
- `tests/test_wordcloud_service.py`
  - Testet Normalisierung/Top-Wörter/Farbzuordnung.

## 2. Abgleich mit dem Project Compass

### Bereits teilweise vorhanden

- **research/** (teilweise vorhanden, aber nicht als Modulstruktur)
  - Funktional vorhanden in `analysis/analyze_definitions.py`, `wordcloud_service.py`, `data/definitions.json`, `Hobby-Definitionen.txt`.
- **app/** (teilweise vorhanden)
  - Funktional vorhanden in `app.py` + `templates/index.html`.
- **knowledge_base/** (rudimentär vorhanden)
  - In relationaler Form in `models.py` (Hobby/Attribute), jedoch nicht als eigenständige, kuratierte Knowledge-Base-Schicht mit Management-Skripten.

### Fehlt komplett

- **matching/**
  - Keine dedizierte Normalisierung/Alias-Lookup/Fuzzy-Matching-Pipeline für Nutzereingaben.
  - Keine Confidence-Mechanik.
- **qualification/**
  - Keine Statuslogik (active/dormant/former/interest/no hobby) basierend auf Nutzerkontext.
  - Keine Explainability-Ausgabe für Klassifikationsentscheidungen.

### Aktuell vermischte Verantwortlichkeiten

- In `app.py` sind App-Layer und Teile der Pipeline-Orchestrierung vermischt (direkter Zugriff auf Daten/Service).
- In `models.py` sind Domänenmodell und Seed-/Initialisierungslogik gekoppelt.
- Research-bezogene Textlogik ist auf `analysis/analyze_definitions.py` und `wordcloud_service.py` verteilt, mit teilweiser Duplikation (Stopwords/Normalisierung).

## 3. Architektur-Lücken (Trennschärfe)

### research
- Vorhanden, aber ohne klare Paketgrenzen/öffentliche API.
- Teilweise doppelte Logik in Analyse-Skript und Wordcloud-Service.

### knowledge base
- Datenmodell vorhanden, aber keine klare KB-Abstraktion:
  - kein dedizierter Datenzugriffsservice,
  - keine Alias-/Synonymstruktur je Aktivität,
  - keine Trennung zwischen kuratiertem Stammdatenbestand und Laufzeitdaten.

### matching
- Fehlt als Schicht vollständig.
- Derzeit keine Eingabetext-Normalisierung zu kanonischen Aktivitäten.

### qualification
- Fehlt als Schicht vollständig.
- Keine formalisierte Bewertungs-/Schwellwertlogik und keine Begründungsausgabe.

### app layer
- Vorhanden, aber zu nah an Persistenz/Analysefunktionen.
- Noch keine klare Übergabe an Matching + Qualification Pipeline.

## 4. Migrationsvorschlag (ohne Umsetzung)

### Sinnvolle Umbauten
1. Zielstruktur als Pakete vorbereiten: `research/`, `knowledge_base/`, `matching/`, `qualification/`, `app/`.
2. Gemeinsame Textnormalisierung aus Research-Teilen extrahieren (ein gemeinsamer Ort).
3. Knowledge-Base-Schicht einführen (Repository/Service), um App vom ORM zu entkoppeln.
4. Matching-Minimum (exakte + Alias-Treffer) als eigenes Modul.
5. Qualification-Minimum mit klaren Statusregeln + Rationale.
6. App-Routen auf Pipeline-Aufrufe umstellen.

### Empfohlene Reihenfolge
1. **Strukturell vorbereiten** (Pakete + Schnittstellen, noch ohne Verhaltensänderung).
2. **Research konsolidieren** (duplizierte Normalisierung/Stopwords zusammenführen).
3. **Knowledge-Base-Abstraktion** einziehen und bestehende Zugriffe darüber leiten.
4. **Matching MVP** ergänzen.
5. **Qualification MVP** ergänzen.
6. **End-to-End API/UX** um neue Pipeline erweitern.

### Was kann bleiben / sollte später aufgeteilt werden
- **Kann bleiben**
  - `templates/index.html` (als UI-Basis),
  - `data/definitions.json`, `Hobby-Definitionen.txt` (als Research-Input),
  - bestehende Testdateien als Ausgangspunkt.
- **Sollte aufgeteilt/verschoben werden**
  - `app.py` -> in `app/` (Routen, Factory, Controller-Orchestrierung getrennt),
  - `models.py` -> in `knowledge_base/` (Modelle vs. Seed/Bootstrapping trennen),
  - `wordcloud_service.py` -> research-spezifische Komponenten modularisieren,
  - `analysis/analyze_definitions.py` -> auf gemeinsame Research-Utilities aufsetzen.

## 5. Risikoeinschätzung

### Kleine Änderungen (geringes Risiko)
- Neue Paketstruktur anlegen, ohne externe Imports zu brechen.
- Reine Dokumentations- und Architekturartefakte.
- Zusätzliche Tests für neue Modulgrenzen (ohne Logikänderung).

### Mittelgroße Änderungen
- Verschieben/Umbenennen von Dateien mit Importanpassungen.
- Herauslösen gemeinsamer Text-Utilities aus bestehenden Modulen.
- Einführung einer KB-Service-Schicht zwischen App und ORM.

### Hohe Risiken / potenziell testbrechend
- Einführung von Matching/Qualification in bestehende API-Responses.
- Änderung des Datenmodells (Alias-/Synonymtabellen, neue Entitäten).
- Anpassung der Initialisierungsreihenfolge (Seed/DB-Bootstrap), da aktuelle Tests auf existierendes Verhalten bauen.

## 6. Konkreter Vorschlag für Phase 1 (kleinster sinnvoller Schritt)

**Phase 1: Architektur-Schablone + Adapter ohne Verhaltensänderung**

- Neue Zielpakete anlegen (`research`, `knowledge_base`, `matching`, `qualification`, `app`) mit klaren Interfaces/Stubs.
- Bestehende Implementierung zunächst als Adapter weiterverwenden (z. B. App ruft weiterhin existierende Funktionen auf, aber über dünne Schicht).
- Bestehende Endpunkte und Testverhalten unverändert lassen.
- Ziel: sichtbare Trennung der Verantwortlichkeiten herstellen, ohne Produktionslogik und API-Verträge zu destabilisieren.

Ergebnis von Phase 1:
- Struktur ist Compass-konform vorbereitet.
- Risiko minimal, weil Verhalten identisch bleibt.
- Danach können Matching und Qualification inkrementell und testgetrieben ergänzt werden.
