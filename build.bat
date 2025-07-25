@echo off
setlocal

REM === Activer l'environnement virtuel ===
if exist .venv\Scripts\activate.bat (
    echo Activation de l'environnement virtuel...
    call .venv\Scripts\activate.bat
) else (
    echo [ERREUR] Environnement virtuel non trouvé. Abandon.
    pause
    exit /b
)

REM === Configuration ===
set SCRIPT=ppp/main.py
set ICON=poups.ico

REM === Nettoyage des anciens builds ===
echo Nettoyage des anciens fichiers...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del /q *.spec 2>nul

REM === Création de l'exécutable ===
echo Création de l'exécutable...
pyinstaller --clean --onefile ^
  --icon=%ICON% ^
  --add-data "ppp;ppp" ^
  --add-data "ppp/utils;ppp/utils" ^
  --add-data "ppp/defaultImages;ppp/defaultImages" ^
  --add-data "ppp/playlistGeneration;ppp/playlistGeneration" ^
  --add-data "ppp/CSVGeneration;ppp/CSVGeneration" ^
  %SCRIPT%

if %ERRORLEVEL% neq 0 (
    echo [ERREUR] La compilation a échoué.
    pause
    exit /b
)

echo.
echo Build terminé. Le fichier EXE est dans le dossier dist\

REM === Copier les dossiers externes ===
echo Copie des dossiers externes...

xcopy config.json  dist\ /Y
xcopy LICENCE dist\ /Y
xcopy PlaylistsSpecs.json  dist\ /Y
xcopy README.MD dist\ /Y
xcopy requirements.txt dist\ /Y
xcopy EXAMPLE_PlaylistsSpecs.txt dist\ /Y
mkdir dist\Images
mkdir dist\.poupetteData
attrib +h dist\.poupetteData


ren dist\main.exe PoupettePlaylistPacker.exe


echo.
echo === BUILD COMPLET ===
pause
