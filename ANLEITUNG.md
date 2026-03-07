# Hobby-App: Schnellstart für Windows (2–3 Minuten)

Diese Anleitung ist für dich, wenn du **kein Entwickler** bist und die App einfach starten möchtest.

---

## 1) Schnellster Weg (empfohlen)

1. Öffne den Projektordner `Hobby-App-` im Explorer.
2. **Doppelklicke auf `start_windows.bat`**.
3. Warte kurz, bis das Fenster meldet, dass die App läuft.

Fertig – das ist der Standardweg.

---

## 2) Erster Aufruf im Browser

Öffne deinen Browser und gehe auf:

`http://localhost:5000`

Beispielseiten:

- `http://localhost:5000/hobbies`
- `http://localhost:5000/attributes`

---

## 3) Wenn etwas nicht klappt (Notlösung per Kommandozeile)

Nur falls der Doppelklick nicht funktioniert:

1. Öffne PowerShell im Projektordner.
2. Führe nacheinander aus:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

3. Danach im Browser öffnen:

`http://localhost:5000`

---

## 4) Linux/macOS

Linux/macOS-Anleitung ist hier bewusst **nicht** der Hauptweg und wird bei Bedarf später ergänzt.
