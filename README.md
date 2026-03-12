# Hobby Attribution App

Dieses Verzeichnis enthält einen einfachen Prototypen einer Web‑App zum
Verwalten und Bewerten von Hobbys anhand von Attributen. Die App eignet
sich als Ausgangspunkt für weitere Entwicklungen mit ChatGPT Codex.

## Einfache Schritt-für-Schritt-Anleitung

Für normale Nutzer:innen ohne Entwickler-Erfahrung gibt es eine separate
Anleitung:

**[`ANLEITUNG.md`](ANLEITUNG.md)**

## Installieren

Erstellen Sie eine virtuelle Umgebung und installieren Sie die
Abhängigkeiten aus `requirements.txt`:

Für die Word-Cloud-Analyse enthält das Projekt zusätzlich `wordcloud` und `matplotlib`.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Nutzung

Starten Sie die Flask‑Anwendung:

```bash
python app.py
```

Die API ist anschließend unter `http://localhost:5000/` erreichbar.

- `GET /` – Startseite für die persönliche Selbstreflexion inkl. Wordcloud.
- `GET /wordcloud.png` – Generiert die Wordcloud aus `Hobby-Definitionen.txt`.
- `GET /hobbies` – Listet alle Hobbys auf. Optionaler Query‑Parameter `q`
  filtert nach Name, `attribute` filtert nach Attributname.
- `GET /attributes` – Gibt alle definierten Attribute zurück.

- `POST /qualify` – Zweistufige Bewertung: allgemeine Aktivitäts-Qualification plus persönlicher Hobby-Status.

### `/qualify` Request (neu in Phase 2 Slice 2)

Pflichtfeld:

```json
{
  "activity": "bouldern"
}
```

Optionale Nutzerkontext-Felder:

- `currently_active` (`bool`)
- `previously_active` (`bool`)
- `frequency` (`"rarely" | "occasionally" | "regularly"`)
- `personal_importance` (`"low" | "medium" | "high"`)
- `intends_to_resume` (`bool`)

Response enthält zusätzlich:

- `general_explanation` (allgemeine Einordnung der Tätigkeit; bevorzugtes Feld für neue Clients)
- `personal_status` (`active_hobby | dormant_hobby | former_hobby | emerging_interest | not_a_hobby | insufficient_personal_context`)
- `personal_explanation` (kurze Begründung der persönlichen Einstufung)
- `matching_hint` (kurzer Hinweis, ob exact/alias/normalized/no_match)

Kompatibilität: `explanation` bleibt vorerst als Legacy-Feld erhalten und ist inhaltlich identisch zu `general_explanation`, damit bestehende Clients nicht brechen.

Hinweis: Bei fehlenden oder zu dünnen persönlichen Angaben liefert das System `insufficient_personal_context` statt vorschnell `not_a_hobby`.

Die Datenbank wird beim ersten Start automatisch erstellt und mit
Beispieldaten befüllt. Sie können die Seed‑Werte in
`models.py` anpassen.

## Analyse der Definitionen

Im Unterordner `analysis` befindet sich das Skript `analyze_definitions.py`.
Es lädt `data/definitions.json`, normalisiert den Text (Lowercase, URL- und Satzzeichen-Entfernung), verwendet eine deduplizierte DE+EN-Stopwortliste, akzeptiert optionale Bereichs-Stopwörter per `--domain-stopwords` und berechnet Wortfrequenzen.

Aufruf:

```bash
python analysis/analyze_definitions.py
```

Erwartete Textausgabe (Top-Wörter, Beispiel):

```text
Word cloud saved to: analysis/artifacts/wordcloud.png
Top 10 most frequent words in definitions:
tätigkeit: 6
man: 3
regelmäßige: 3
...
```

Artefaktpfad der Word-Cloud:
`analysis/artifacts/wordcloud.png`.

Hinweis: Diese Top-Wörter bilden die Grundlage für das Attribut-Design
in der App (Definition und Gewichtung von Attributen).

Optional können Sie bereichsspezifische Stopwörter ergänzen (z. B.
`hobby`, wenn der Begriff zu dominant ist):

```bash
python analysis/analyze_definitions.py --domain-stopwords hobby,freizeit --top-n 20
```

Bei fehlender `wordcloud`-Abhängigkeit kann die Analyse ohne PNG erfolgen:

```bash
python analysis/analyze_definitions.py --skip-wordcloud
```

## Datenbasis

Im Ordner `data` liegt `definitions.json`. Diese Datei enthält einige
Begriffsdefinitionen für den Begriff „Hobby“ aus verschiedenen Quellen.
Sie dient als Ausgangspunkt für die Wortfrequenzanalyse und kann
erweitert oder ersetzt werden.

## Weiterführende Entwicklung

Das Projekt bildet einen Grundstein. Mögliche Erweiterungen umfassen:

- Ein Front‑End (HTML/React) zum bequemen Durchsuchen und Bewerten von
  Hobbys.
- Ein Persistenzlayer mit Benutzerauthentifizierung, um persönliche
  Hobbylisten zu speichern.
- Komplexere Matching‑Algorithmen zur Empfehlung von Hobbys basierend
  auf Benutzerpräferenzen.

Viel Erfolg beim weiteren Ausbau mit Codex!
