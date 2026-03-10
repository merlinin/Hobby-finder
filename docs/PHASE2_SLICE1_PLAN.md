# Phase 2 – Umsetzungsplan für den ersten produktiven Vertical Slice

## Ausgangslage (nach Phase 1)

Nach Phase 1 ist die Zielstruktur aus dem Project Compass sichtbar und bereits als technische Schablone angelegt (`app`, `matching`, `knowledge_base`, `qualification`, `research`). Die bestehenden Endpunkte und das bisherige Verhalten bleiben stabil. 

Phase 2 Slice 1 soll diese Architektur **erstmals produktiv nutzen**, aber bewusst nur in einem kleinen, kontrollierten Umfang.

---

## 1) Ziel von Phase 2 Slice 1

## Was Slice 1 fachlich erstmals können soll

Slice 1 liefert einen **vorläufigen, erklärbaren Architektur-Flow** für eine einzelne Aktivität:

1. Aktivitätstext erkennen und matchen.
2. Attribute der erkannten Aktivität aus der bestehenden Knowledge Base laden.
3. Eine **preliminary qualification** erzeugen (nicht final), z. B.:
   - `known_activity`
   - `unknown_activity`
   - `potential_hobby_candidate`

Wichtig: Das Ergebnis ist **explizit vorläufig und explainable** – ein Nachweis der Pipeline, keine endgültige Hobby-Entscheidung.

## Was Slice 1 bewusst noch **nicht** leisten soll

Slice 1 bestimmt **nicht**:

- ob eine Person tatsächlich ein Hobby hat,
- aktive/dormante/ehemalige Hobby-Zustände,
- frequenzbasierte persönliche Hobby-Klassifikation.

---

## 2) Empfohlener erster Vertical Slice

## Vorschlag: additiver Endpunkt `POST /qualify`

Der Endpunkt wird neu hinzugefügt und ersetzt keine bestehende Route.

### Minimales Request-Contract (MVP)

```json
{
  "activity": "bouldern"
}
```

### Minimales Response-Contract (MVP)

```json
{
  "input": {
    "activity": "bouldern"
  },
  "match": {
    "matched": true,
    "activity_name": "Bouldern",
    "match_type": "exact_name",
    "confidence": 1.0
  },
  "attributes": {
    "physical": 4,
    "social": 2
  },
  "qualification": {
    "label": "potential_hobby_candidate",
    "preliminary": true
  },
  "explanation": "Aktivität wurde in der Knowledge Base erkannt und Attribute geladen. Ergebnis ist eine vorläufige Einordnung, keine finale Hobby-Bewertung."
}
```

### Warum dieser Slice?

- Er zeigt den Zielpfad der Architektur erstmals produktiv.
- Er ist klein, testbar und additiv.
- Er minimiert Regressionsrisiken für bestehende Endpunkte (`/`, `/hobbies`, `/attributes`, `/wordcloud.png`).

---

## 3) Architektur-Check und Verantwortlichkeiten

Die Datenfluss-Reihenfolge bleibt strikt:

**app → matching → knowledge_base → qualification**

### Rollen je Modul

- **app**
  - Nimmt Request an.
  - Orchestriert Aufrufe in der festgelegten Reihenfolge.
  - Liefert Response mit klarer Vorläufigkeitskennzeichnung (`preliminary: true`).

- **matching**
  - Normalisiert Eingabe (`activity`).
  - Prüft exakten Treffer auf kanonischen Namen oder kleine Alias-Mapping-Liste.
  - Liefert Match-Metadaten (`matched`, `match_type`, `confidence`).

- **knowledge_base**
  - Lädt Aktivität und vorhandene Attribute aus der **bestehenden** KB/ORM-Schicht.
  - Keine neue Datenhaltung für Slice 1.

- **qualification**
  - Nutzt Match + Attribute für eine **vorläufige** Einstufung.
  - Liefert Label + kurze Erklärung.
  - Keine finale Hobby-Qualifikation und keine personenbezogene Zeitmodellierung.

`research` bleibt in Slice 1 unverändert außerhalb dieses Flows.

---

## 4) Datenmodell / Verträge (minimal)

## Input DTO

- `QualificationInput`
  - `activity: str`

## Matching DTO

- `MatchResult`
  - `matched: bool`
  - `activity_id: int | None`
  - `activity_name: str | None`
  - `match_type: Literal["exact_name", "exact_alias", "none"]`
  - `confidence: float`

## Attribute DTO

- `ActivityAttributes`
  - Schlüssel/Wert-Paare aus bestehender KB-Attributstruktur (z. B. `physical`, `creative`, `social`)

## Preliminary Qualification DTO

- `PreliminaryQualificationResult`
  - `label: Literal["known_activity", "unknown_activity", "potential_hobby_candidate"]`
  - `preliminary: bool` (immer `true` in Slice 1)
  - `explanation: str`

### Vorläufige Klassifikationslogik (Slice 1)

- Kein Match → `unknown_activity`.
- Match ohne verfügbare Attribute → `known_activity`.
- Match mit verfügbaren Attributen → `potential_hobby_candidate`.

Diese Logik ist absichtlich einfach, transparent und stabil.

---

## 5) Knowledge-Base-Nutzung (Scope-Grenzen)

Slice 1 nutzt die vorhandene Knowledge-Base-Infrastruktur (Modelle + Adapter) und führt **keine** strukturellen Datenänderungen ein.

Explizit nicht Teil von Slice 1:

- keine DB-Migrationen,
- keine großen Alias-Tabellen,
- keine Schemaerweiterung.

Wenn Aliase benötigt werden, nur als kleine, lokale In-Code-Mapping-Liste im Matching-Adapter.

---

## 6) Risiken, Nicht-Ziele, Stabilitätsstrategie

## Hauptrisiken

- Ungenaue Normalisierung kann zu False-Negatives bei bekannten Aktivitäten führen.
- Unklare Response-Semantik könnte als finale Bewertung missverstanden werden.
- Unbeabsichtigte Nebenwirkungen auf bestehende Endpunkte bei falscher Verdrahtung.

## Explizite Nicht-Ziele (Out of Scope für Slice 1)

- Fuzzy Matching.
- Externe NLP-Abhängigkeiten.
- Große Datenbank-Refactors oder Migrationen.
- UI-Redesign.
- Vollständige Hobby-Status-Evaluierung.
- Persönliches Aktivitäts-/Frequenzmodell.

## Stabilitätsstrategie

- Rein additiver Endpunkt (`POST /qualify`).
- Bestehende Endpunkte unverändert lassen.
- Deterministische, kleine Regeln statt komplexer Scoring-Engine.
- Contract-first-Tests + Regressionstests auf bestehende API.

---

## 7) Konkrete Deliverables für Phase 2 – Slice 1

## Dateien (Planungsziel, keine Implementierung in diesem Schritt)

### Neu

- `app/contracts.py`
  - Minimale Request/Response-Contracts für `POST /qualify`.
- `matching/adapter.py`
  - Produktiver Minimal-Adapter (exact name + kleine Alias-Mapping-Liste).
- `qualification/adapter.py`
  - Produktiver Minimal-Adapter für vorläufige Klassifikation.
- `tests/test_matching_adapter.py`
- `tests/test_preliminary_qualification_adapter.py`
- `tests/test_qualify_endpoint.py`

### Anzupassen

- `matching/port.py` (präziser Match-Contract).
- `qualification/port.py` (vorläufigen Ergebnis-Contract abbilden).
- `knowledge_base/adapter.py` (gezielte Lookup-Methoden für Aktivität + Attribute).
- `app/orchestration.py` (neue Orchestrierungsfunktion für den Slice-Flow).
- `app.py` (neuer additiver Endpunkt `POST /qualify`).

## Tests (zu ergänzen)

1. **Matching Unit Tests**
   - exact name hit,
   - alias hit,
   - no match,
   - Groß-/Kleinschreibung.

2. **Knowledge Base Adapter Tests**
   - Attribute-Lookup für bekannte Aktivität,
   - kein Treffer für unbekannte Aktivität.

3. **Preliminary Qualification Unit Tests**
   - `unknown_activity` bei no match,
   - `known_activity` bei Match ohne Attribute,
   - `potential_hobby_candidate` bei Match mit Attributen.

4. **Endpoint/Integration Tests**
   - `POST /qualify` happy path,
   - invalid payload (`400`),
   - Response enthält `input`, `match`, `qualification`, `attributes`, `explanation`,
   - bestehende Tests bleiben unverändert grün.

---

## Erwartetes Ergebnis nach Slice 1

Nach Phase 2 Slice 1 ist die Zielarchitektur erstmals fachlich und produktiv nachgewiesen – als **kleiner, sicherer, vorläufiger Vertical Slice**.

Der Slice liefert eine erklärbare Vorab-Einordnung von Aktivitäten und zeigt die Modultrennung in der Praxis, ohne bereits den vollständigen Hobby-Entscheidungsraum zu beanspruchen.
