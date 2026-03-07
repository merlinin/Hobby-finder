@echo off
setlocal

echo.
echo ==========================================
echo   Hobby-App Aufraeumen (Windows)
echo ==========================================
echo.
echo Dieses Skript entfernt lokale Laufzeitdateien:
echo - .venv
echo - venv
echo - instance\hobbies.db
echo - analysis\artifacts
echo - __pycache__ Ordner
echo.
set /p CONFIRM=Weiter mit Aufraeumen? (j/n): 
if /I not "%CONFIRM%"=="j" (
  echo Abgebrochen.
  exit /b 0
)

if exist ".venv" (
  rmdir /s /q ".venv"
  echo [OK] .venv entfernt
) else (
  echo [Info] .venv nicht gefunden
)


if exist "venv" (
  rmdir /s /q "venv"
  echo [OK] venv entfernt
) else (
  echo [Info] venv nicht gefunden
)

if exist "instance\hobbies.db" (
  del /f /q "instance\hobbies.db"
  echo [OK] instance\hobbies.db entfernt
) else (
  echo [Info] instance\hobbies.db nicht gefunden
)

if exist "analysis\artifacts" (
  rmdir /s /q "analysis\artifacts"
  echo [OK] analysis\artifacts entfernt
) else (
  echo [Info] analysis\artifacts nicht gefunden
)

for /d /r %%D in (__pycache__) do (
  if exist "%%D" rmdir /s /q "%%D"
)
echo [OK] __pycache__-Ordner entfernt (falls vorhanden)

echo.
echo Fertig. Um alles zu loeschen, kannst du danach den Projektordner entfernen.
echo.
endlocal
