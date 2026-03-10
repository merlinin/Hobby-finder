# Phase-1-Umsetzungsplan: Architektur-Schablone + Adapter ohne Verhaltensänderung

## 1) Ziel von Phase 1

### Was nach Phase 1 besser sein soll
- Die Zielarchitektur aus dem Project Compass ist **sichtbar im Repository vorbereitet** (als Paket-/Modulstruktur).
- Verantwortlichkeiten sind klarer getrennt: App-Layer, Research, Knowledge-Base, Matching und Qualification haben jeweils einen definierten Ort.
- Bestehender Code wird über dünne Adapter in die neue Struktur eingebunden, sodass spätere Migrationen inkrementell erfolgen können.
- Die nächsten Phasen (Matching MVP, Qualification MVP) erhalten stabile Anschlussstellen (Interfaces/Ports), ohne sofortige Logikänderung.

### Was ausdrücklich unverändert bleiben soll
- Verhalten und Signaturen bestehender Endpoints (`/`, `/hobbies`, `/attributes`, `/wordcloud.png`).
- Ergebnislogik der Wordcloud-Generierung.
- Aktuelles Datenmodell und Seed-Verhalten inhaltlich.
- Bestehende Tests und ihr erwartetes Verhalten.

---

## 2) Geplante Modulstruktur

Zielstruktur gemäß Compass:
- `research/`
- `knowledge_base/`
- `matching/`
- `qualification/`
- `app/`

### Scope in Phase 1
In Phase 1 werden **alle fünf Bereiche strukturell vorbereitet**, aber nur mit Platzhaltern/Adaptern:

- `research/`: Adapter zu bestehender Analyse-/Wordcloud-Logik, noch keine inhaltliche Konsolidierung.
- `knowledge_base/`: Adapter zu `models.py` (read-orientierte Schnittstellen), keine Datenmodelländerung.
- `matching/`: Interface/Stub (noch keine produktive Matching-Logik).
- `qualification/`: Interface/Stub (noch keine produktive Statuslogik).
- `app/`: dünne Orchestrierungsschicht, die zunächst bestehende Funktionen delegiert.

---

## 3) Umgang mit bestehendem Code

### Dateien, die zunächst bestehen bleiben
- `app.py`
- `models.py`
- `wordcloud_service.py`
- `analysis/` (insb. `analysis/analyze_definitions.py`)
- `templates/index.html`
- `tests/`

### Spätere Zielbewegung (nicht in Phase 1 umsetzen)
- `app.py` später aufteilen in `app/routes.py`, `app/factory.py`, ggf. `app/controllers.py`.
- `models.py` später trennen in Domänenmodell (`knowledge_base/models.py`) und Seed/Bootstrap (`knowledge_base/bootstrap.py`).
- `wordcloud_service.py` später fachlich in `research/` überführen (z. B. `research/text_processing.py`, `research/wordcloud.py`).
- `analysis/analyze_definitions.py` später auf gemeinsame Utilities aus `research/` umstellen.

Phase 1 nutzt hier ausschließlich **Adapter-Anbindung**, keine funktionale Verlagerung.

---

## 4) Adapter- / Übergangsschicht

Sinnvolle Adapter ohne Verhaltensänderung:

1. **ResearchAdapter**
   - Kapselt Aufrufe aus `wordcloud_service.py` und optional Analyse-Helfer.
   - Exponiert dieselben semantischen Outputs (Top-Wörter, Bilddaten, Farblogik).

2. **KnowledgeBaseAdapter**
   - Kapselt ORM-Zugriffe aus `models.py` hinter klaren Methoden (z. B. `list_hobbies()`, `list_attributes()`).
   - Keine Änderung an SQLAlchemy-Modellen oder Seed-Strategie.

3. **AppOrchestrationAdapter**
   - Zentraler Delegationspunkt zwischen Flask-Routen und Adaptern.
   - Dient als späterer Hook für Matching + Qualification, aktuell pass-through.

4. **MatchingPort (Stub)**
   - Interface + No-op/Dummy-Implementierung mit klarer Rückgabeform.
   - Noch nicht in produktive Route-Antworten integriert.

5. **QualificationPort (Stub)**
   - Interface + No-op/Dummy-Implementierung für künftige Hobby-Statuslogik.
   - Liefert in Phase 1 keine verhaltensrelevante Entscheidung.

---

## 5) Risiken

### Testbruch-Risiken
- Import-Pfade brechen beim frühen Verschieben/Umbenennen bestehender Dateien.
- Versehentliche Änderung der Flask-App-Initialisierung (`create_app`) oder Seed-Reihenfolge.

### Endpoint-Risiken
- Response-Formate (JSON-Felder, Reihenfolge, Datentypen) könnten unabsichtlich verändert werden.
- Content-Type oder Statuscodes könnten bei Adapter-Einzug ungewollt abweichen.

### Funktionsrisiken
- Wordcloud kann sich ändern, wenn Tokenisierung/Stopwords/Farbklassifikation unabsichtlich berührt werden.
- ORM-Session-/Query-Verhalten kann abweichen, wenn Adapter nicht exakt delegieren.

---

## 6) Stabilitätsstrategie

1. **Striktes No-Behavior-Change-Prinzip in Phase 1**
   - Adapter dürfen nur weiterreichen, nicht transformieren.

2. **Kompatibilitäts-Tests als Gate**
   - Bestehende Tests müssen unverändert grün bleiben.
   - Ergänzend: Snapshot-/Golden-Master-Checks für kritische Endpoint-Responses (falls eingeführt: rein additiv).

3. **Schrittweise Aktivierung**
   - Erst Modulstruktur + Stubs.
   - Dann einzelne Route intern über Adapter verdrahten.
   - Nach jedem Schritt Testsuite laufen lassen.

4. **Wordcloud-Schutz**
   - Keine Änderung an Normalisierung, Frequenzzählung und Farbzuordnung.
   - PNG-Endpoint mit bestehendem Test plus optionalem Byte-Length-Sanity-Check absichern.

5. **Rollback-freundliche Commits**
   - Kleine, thematisch saubere Commits (Struktur, dann Adapter), um Risiken schnell revertieren zu können.

---

## 7) Konkrete Deliverables für Phase 1

Nach Phase 1 sollen mindestens folgende Artefakte existieren:

### Neue Ordner/Pakete
- `research/`
- `knowledge_base/`
- `matching/`
- `qualification/`
- `app/`

Jeweils mit `__init__.py` und kurzen Modul-README/Docstring zur Verantwortung.

### Schnittstellen / Platzhalter
- `research/adapter.py` (Wrapper auf bestehende Wordcloud-/Analysefunktionen)
- `knowledge_base/adapter.py` (Wrapper auf bestehende ORM-Zugriffe)
- `matching/port.py` + `matching/stub.py`
- `qualification/port.py` + `qualification/stub.py`
- `app/orchestration.py` (zentraler Delegationspunkt)

### Integrationspunkt ohne Verhaltensänderung
- Bestehende Flask-Routen delegieren intern an `app/orchestration.py`, das wiederum bestehende Implementierung via Adapter aufruft.

### Test-/Qualitätsziel
- Bestehende Tests laufen unverändert grün.
- Keine Änderung an öffentlichen API-Verträgen und Wordcloud-Ausgabe.

---

## Definition of Done für Phase 1

- Compass-Zielstruktur ist sichtbar im Repo vorhanden.
- Adapter/Ports/Stubs sind implementiert, aber ohne fachliche Verhaltensänderung.
- Alle bestehenden Tests sind grün.
- Endpoints und Wordcloud verhalten sich für Nutzer unverändert.
- Die Codebasis ist bereit für Phase 2 (Research-Konsolidierung + KB-Abstraktion vertiefen).


---

## 8) Konkrete Umsetzungssequenz (PR-Slices)

Zur operativen Umsetzung wird Phase 1 in kleine, reviewbare PR-Slices aufgeteilt. Jeder Slice muss die bestehenden Tests grün halten und darf kein API-Verhalten ändern.

### Slice 1 — Paketstruktur + Verantwortungstexte
**Ziel:** Nur Struktur sichtbar machen, ohne Laufzeitintegration.

**Änderungen:**
- Ordner anlegen: `research/`, `knowledge_base/`, `matching/`, `qualification/`, `app/`
- Je Paket: `__init__.py`
- Je Paket: kurze `README.md` oder Modul-Docstring mit Scope und „No-Behavior-Change“-Hinweis

**Akzeptanzkriterien:**
- Keine Änderung an `app.py`, `models.py`, `wordcloud_service.py`.
- Tests unverändert grün.

### Slice 2 — Research-Adapter (read-only Delegation)
**Ziel:** Bestehende Wordcloud-/Analysefunktion über stabilen Adapter verfügbar machen.

**Änderungen:**
- `research/adapter.py` mit dünnen Wrappern auf bestehende Funktionen aus `wordcloud_service.py`.
- Optional: kleine Dataclass/TypedDict für klaren Rückgabevertrag (ohne Transformationslogik).

**Akzeptanzkriterien:**
- Byte-identisches PNG-Verhalten am Endpoint `/wordcloud.png`.
- Keine Änderung der Top-Wort-Logik.

### Slice 3 — Knowledge-Base-Adapter
**Ziel:** ORM-Zugriffe hinter stabile Schnittstelle ziehen.

**Änderungen:**
- `knowledge_base/adapter.py` mit Methoden wie `list_hobbies()`, `list_attributes()`.
- Adapter ruft intern direkt die bestehenden SQLAlchemy-Modelle/Queries auf.

**Akzeptanzkriterien:**
- JSON-Antworten von `/hobbies` und `/attributes` bleiben in Struktur und Inhalt gleich.
- Seed/Bootstrap-Ablauf bleibt unverändert.

### Slice 4 — App-Orchestrierung als Pass-through
**Ziel:** App-Layer auf zentrale Delegation vorbereiten.

**Änderungen:**
- `app/orchestration.py` als dünne Fassade über Research-/KB-Adapter.
- `app.py` ruft intern Orchestrierung auf (Signaturen und Endpoint-Verhalten bleiben gleich).

**Akzeptanzkriterien:**
- Alle bestehenden Endpoint-Tests grün.
- Keine Änderung an Templates oder HTTP-Verträgen.

### Slice 5 — Matching/Qualification Ports + Stubs
**Ziel:** spätere Fachlogik formal andockbar machen.

**Änderungen:**
- `matching/port.py`, `matching/stub.py`
- `qualification/port.py`, `qualification/stub.py`
- Noch keine produktive Nutzung in bestehenden Endpoints.

**Akzeptanzkriterien:**
- Keine Verhaltensänderung zur Laufzeit.
- Type-/Import-Konsistenz gegeben.

---

## 9) Test- und Abnahmeraster für Phase 1

### Pflichtchecks pro Slice
1. Unit-Tests: bestehende Suite muss vollständig grün sein.
2. Endpoint-Kompatibilität:
   - `/` liefert weiterhin HTML-Response.
   - `/wordcloud.png` liefert weiterhin `image/png`.
   - `/hobbies` und `/attributes` liefern unveränderte JSON-Struktur.
3. Import-Kompatibilität: bestehende Imports in Tests bleiben gültig.

### Empfohlene additive Sicherungen
- JSON-Snapshot-Tests für `/hobbies` und `/attributes`.
- Header-/Statuscode-Assertions für alle bestehenden Endpoints.
- Sanity-Check auf PNG-Response-Größe (`len(response.data) > 0`) zusätzlich zu Content-Type.

---

## 10) Arbeitsmodus und Guardrails

- **Keine Datenmodellmigrationen** in Phase 1.
- **Keine Umbenennung öffentlicher Endpoints** in Phase 1.
- **Keine inhaltliche Logikänderung** in Wordcloud/Normalisierung in Phase 1.
- Änderungen erfolgen nur als **kompatible Schablone** (Struktur + Adapter + Stubs).
- Bei jeder Abweichung gilt: erst dokumentieren, dann separat als Proposal abstimmen.
