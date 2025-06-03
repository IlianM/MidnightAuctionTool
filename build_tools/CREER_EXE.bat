@echo off
chcp 65001 > nul
title 🏗️ Création EXE - Gestionnaire d'Enchères

echo.
echo ============================================================
echo 🚗 GESTIONNAIRE D'ENCHÈRES - CRÉATEUR D'EXE
echo ============================================================
echo.

echo 🔍 Vérification de l'environnement...

:: Vérifier Python
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou non accessible
    echo.
    echo 📥 Téléchargez Python depuis: https://python.org
    echo    Cochez "Add to PATH" lors de l'installation
    pause
    exit /b 1
)
echo ✅ Python trouvé

:: Vérifier pip
pip --version > nul 2>&1
if errorlevel 1 (
    echo ❌ pip non trouvé
    pause
    exit /b 1
)
echo ✅ pip trouvé

:: Vérifier main.py
if not exist "main.py" (
    echo ❌ Fichier main.py non trouvé
    echo    Assurez-vous d'être dans le bon dossier
    pause
    exit /b 1
)
echo ✅ main.py trouvé

echo.
echo 📦 Installation de PyInstaller (si nécessaire)...
pip install pyinstaller --quiet
if errorlevel 1 (
    echo ⚠️ Problème avec l'installation, mais on continue...
)
echo ✅ PyInstaller prêt

echo.
echo 🏗️ Lancement de la construction automatique...
python build_exe.py

echo.
if exist "exe_build\Gestionnaire_Encheres.exe" (
    echo ✅ SUCCESS! L'EXE a été créé avec succès!
    echo.
    echo 📁 Fichiers générés:
    echo    - exe_build\Gestionnaire_Encheres.exe
    echo    - Gestionnaire_Encheres_Distribution\
    echo.
    echo 🎯 Vous pouvez maintenant:
    echo    1. Tester l'EXE en double-cliquant dessus
    echo    2. Compresser le dossier Distribution en ZIP
    echo    3. Partager avec vos utilisateurs
    echo.
    
    set /p test="🧪 Voulez-vous tester l'EXE maintenant? (o/n): "
    if /i "%test%"=="o" (
        echo 🚀 Lancement du test...
        start "" "exe_build\Gestionnaire_Encheres.exe"
    )
    
    set /p explorer="📁 Ouvrir le dossier de distribution? (o/n): "
    if /i "%explorer%"=="o" (
        explorer "Gestionnaire_Encheres_Distribution"
    )
    
) else (
    echo ❌ ERREUR: L'EXE n'a pas été créé
    echo.
    echo 🔧 Solutions possibles:
    echo    1. Réessayez en tant qu'administrateur
    echo    2. Désactivez temporairement l'antivirus
    echo    3. Vérifiez les erreurs dans la console
)

echo.
echo 🎉 Processus terminé!
pause 