#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de construction d'EXE pour le Gestionnaire d'Enchères Véhicules - CustomTkinter
"""

import subprocess
import sys
import os
import shutil
import time
from pathlib import Path

def installer_pyinstaller():
    """Installe PyInstaller si nécessaire"""
    try:
        import PyInstaller
        print("✅ PyInstaller déjà installé")
        return True
    except ImportError:
        print("📦 Installation de PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller installé avec succès")
            return True
        except subprocess.CalledProcessError:
            print("❌ Erreur lors de l'installation de PyInstaller")
            return False

def installer_customtkinter():
    """Installe CustomTkinter si nécessaire"""
    try:
        import customtkinter
        print("✅ CustomTkinter déjà installé")
        return True
    except ImportError:
        print("📦 Installation de CustomTkinter...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
            print("✅ CustomTkinter installé avec succès")
            return True
        except subprocess.CalledProcessError:
            print("❌ Erreur lors de l'installation de CustomTkinter")
            return False

def construire_exe():
    """Construit l'EXE avec PyInstaller"""
    print("🔨 Construction de l'EXE...")
    
    # Commande PyInstaller simplifiée pour CustomTkinter
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=Gestionnaire_Encheres',
        '--hidden-import=customtkinter',
        '--hidden-import=PIL',
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter.simpledialog',
        '--collect-all=customtkinter',
        '--optimize=2',
        '--distpath=exe_build',
        '--workpath=exe_build/temp',
        '--specpath=exe_build',
        'main.py'
    ]
    
    print("📝 Configuration PyInstaller simplifiée pour CustomTkinter")
    
    try:
        # Supprimer les anciens fichiers de build
        build_dirs = ['exe_build', 'build', 'dist']
        for dir_name in build_dirs:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
                print(f"🗑️ Ancien dossier {dir_name} supprimé")
        
        # Créer le dossier de build
        os.makedirs('exe_build', exist_ok=True)
        
        # Exécuter PyInstaller
        print("⚙️ Exécution de PyInstaller...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ EXE créé avec succès !")
            return True
        else:
            print("❌ Erreur lors de la création de l'EXE:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def creer_package_distribution():
    """Crée un package de distribution complet"""
    print("📦 Création du package de distribution...")
    
    # Créer le dossier de distribution
    dist_folder = "Gestionnaire_Encheres_Distribution"
    if os.path.exists(dist_folder):
        shutil.rmtree(dist_folder)
    
    os.makedirs(dist_folder)
    
    try:
        # Copier l'EXE
        exe_source = "exe_build/Gestionnaire_Encheres.exe"
        if os.path.exists(exe_source):
            shutil.copy2(exe_source, dist_folder)
            print("✅ EXE copié")
        else:
            print("❌ EXE introuvable")
            return False
        
        # Copier les fichiers de données
        data_files = [
            "donnees_encheres.json",
            "parametres_encheres.json"
        ]
        
        for file in data_files:
            if os.path.exists(file):
                shutil.copy2(file, dist_folder)
                print(f"✅ {file} copié")
        
        # Créer un README pour les utilisateurs finaux
        readme_content = """🚗 GESTIONNAIRE D'ENCHÈRES VÉHICULES
==================================

📋 INSTALLATION:
1. Aucune installation requise !
2. Double-cliquez sur "Gestionnaire_Encheres.exe"

🎯 PREMIÈRE UTILISATION:
1. Lancez l'application
2. Allez dans l'onglet "⚙️ Paramètres" 
3. Configurez vos tarifs et marges
4. Commencez à saisir vos véhicules !

💡 CONSEILS:
• Sauvegardez régulièrement (bouton "💾 Sauvegarder")
• Exportez vos données avec le bouton "📊 Exporter CSV"
• Vos données sont dans les fichiers .json

🆘 PROBLÈMES:
• Si l'antivirus bloque: ajoutez une exception
• Si l'app ne démarre pas: vérifiez Windows Defender
• Les données sont sauvegardées automatiquement

Version: CustomTkinter 2024
"""
        
        with open(f"{dist_folder}/README.txt", "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        # Copier la documentation
        docs_folder = f"{dist_folder}/Documentation"
        if os.path.exists("docs"):
            shutil.copytree("docs", docs_folder)
            print("✅ Documentation copiée")
        
        print(f"🎉 Package de distribution créé: {dist_folder}/")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du package: {e}")
        return False

def nettoyer_fichiers_temporaires():
    """Nettoie les fichiers temporaires"""
    print("🧹 Nettoyage des fichiers temporaires...")
    
    temp_dirs = ['exe_build/temp', 'build', '__pycache__']
    temp_files = ['*.spec']
    
    for dir_name in temp_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🗑️ {dir_name} supprimé")
    
    # Supprimer les fichiers .spec
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"🗑️ {spec_file} supprimé")

def afficher_taille_exe():
    """Affiche la taille de l'EXE créé"""
    exe_path = "exe_build/Gestionnaire_Encheres.exe"
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"📏 Taille de l'EXE: {size_mb:.1f} MB")

def main():
    """Fonction principale"""
    print("🚀 CONSTRUCTION EXE - GESTIONNAIRE D'ENCHÈRES VÉHICULES")
    print("=" * 60)
    print("🎨 Version: CustomTkinter")
    print()
    
    start_time = time.time()
    
    # Étape 1: Installer les dépendances
    if not installer_pyinstaller():
        return
    
    if not installer_customtkinter():
        return
    
    # Étape 2: Construire l'EXE
    if not construire_exe():
        return
    
    # Étape 3: Afficher la taille
    afficher_taille_exe()
    
    # Étape 4: Créer le package de distribution
    if not creer_package_distribution():
        return
    
    # Étape 5: Nettoyer
    nettoyer_fichiers_temporaires()
    
    end_time = time.time()
    duration = end_time - start_time
    
    print()
    print("🎉 CONSTRUCTION TERMINÉE AVEC SUCCÈS !")
    print(f"⏱️ Temps total: {duration:.1f} secondes")
    print()
    print("📂 Fichiers créés:")
    print("  • exe_build/Gestionnaire_Encheres.exe")
    print("  • Gestionnaire_Encheres_Distribution/ (package complet)")
    print()
    print("✅ PRÊT À DISTRIBUER !")

if __name__ == "__main__":
    main() 