#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'installation des dépendances pour le scraping LeBonCoin
"""

import subprocess
import sys
import os

def installer_dependances():
    """Installe les dépendances nécessaires pour le scraping"""
    
    print("🔧 Installation des dépendances pour le scraping LeBonCoin...")
    
    # Liste des packages nécessaires
    packages = [
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0", 
        "lxml>=4.9.0"
    ]
    
    for package in packages:
        try:
            print(f"📦 Installation de {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installé avec succès")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'installation de {package}: {e}")
            return False
    
    print("\n🎉 Toutes les dépendances ont été installées avec succès !")
    print("🔍 L'onglet Recherche LeBonCoin est maintenant fonctionnel.")
    
    return True

def verifier_dependances():
    """Vérifie si les dépendances sont déjà installées"""
    print("🔍 Vérification des dépendances...")
    
    dependances_manquantes = []
    
    try:
        import requests
        print("✅ requests trouvé")
    except ImportError:
        dependances_manquantes.append("requests")
    
    try:
        import bs4
        print("✅ beautifulsoup4 trouvé")
    except ImportError:
        dependances_manquantes.append("beautifulsoup4")
    
    try:
        import lxml
        print("✅ lxml trouvé")
    except ImportError:
        dependances_manquantes.append("lxml")
    
    return dependances_manquantes

if __name__ == "__main__":
    print("🚗 Installation des dépendances pour le scraping LeBonCoin")
    print("=" * 60)
    
    # Vérifier les dépendances manquantes
    manquantes = verifier_dependances()
    
    if not manquantes:
        print("\n🎉 Toutes les dépendances sont déjà installées !")
    else:
        print(f"\n⚠️ Dépendances manquantes : {', '.join(manquantes)}")
        
        response = input("\n📥 Voulez-vous installer les dépendances manquantes ? (o/n): ")
        if response.lower() in ['o', 'oui', 'y', 'yes']:
            if installer_dependances():
                print("\n✅ Installation terminée. Vous pouvez maintenant utiliser l'onglet Recherche.")
            else:
                print("\n❌ L'installation a échoué. Veuillez installer manuellement avec:")
                print("pip install requests beautifulsoup4 lxml")
        else:
            print("\n⚠️ Sans les dépendances, l'onglet Recherche ne fonctionnera pas.")
    
    input("\nAppuyez sur Entrée pour fermer...") 