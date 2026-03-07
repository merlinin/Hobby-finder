@echo off
setlocal

REM 1) Prüfen, ob python verfügbar ist
where python >nul 2>nul
if errorlevel 1 (
    echo [FEHLER] Python wurde nicht gefunden. Bitte installiere Python und fuege es zum PATH hinzu.
    pause
    exit /b 1
)

REM 2) Falls .venv nicht existiert: python -m venv .venv
if not exist ".venv" (
    echo [INFO] Virtuelle Umgebung wird erstellt ...
    python -m venv .venv
    if errorlevel 1 (
        echo [FEHLER] Die virtuelle Umgebung konnte nicht erstellt werden.
        pause
        exit /b 1
    )
)

REM 3) .venv\Scripts\activate ausführen
if not exist ".venv\Scripts\activate.bat" (
    echo [FEHLER] Aktivierungsskript nicht gefunden: .venv\Scripts\activate.bat
    pause
    exit /b 1
)
call ".venv\Scripts\activate.bat"
if errorlevel 1 (
    echo [FEHLER] Virtuelle Umgebung konnte nicht aktiviert werden.
    pause
    exit /b 1
)

REM 4) pip install -r requirements.txt
if exist "requirements.txt" (
    echo [INFO] Abhaengigkeiten werden installiert ...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [FEHLER] Installation der Abhaengigkeiten fehlgeschlagen.
        pause
        exit /b 1
    )
) else (
    echo [WARNUNG] requirements.txt nicht gefunden. Ueberspringe Installation.
)

REM 6) Hinweis ausgeben

echo App laeuft unter http://localhost:5000

REM 5) python app.py starten
python app.py

endlocal
