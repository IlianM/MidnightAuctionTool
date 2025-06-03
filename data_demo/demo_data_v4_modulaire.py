#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de données de démonstration pour le Gestionnaire d'Enchères V4
Compatible avec la structure modulaire
"""

import json
import random
from datetime import datetime, timedelta

def generer_donnees_demo():
    """Génère des données de démonstration réalistes"""
    
    # Marques et modèles de véhicules populaires
    vehicules_templates = [
        {"marque": "Peugeot", "modele": "308", "annee_min": 2015, "annee_max": 2022, "prix_min": 8000, "prix_max": 18000},
        {"marque": "Renault", "modele": "Clio", "annee_min": 2016, "annee_max": 2023, "prix_min": 7000, "prix_max": 16000},
        {"marque": "Citroën", "modele": "C3", "annee_min": 2014, "annee_max": 2022, "prix_min": 6000, "prix_max": 14000},
        {"marque": "Volkswagen", "modele": "Golf", "annee_min": 2016, "annee_max": 2023, "prix_min": 12000, "prix_max": 25000},
        {"marque": "BMW", "modele": "Série 3", "annee_min": 2015, "annee_max": 2022, "prix_min": 15000, "prix_max": 35000},
        {"marque": "Audi", "modele": "A3", "annee_min": 2016, "annee_max": 2023, "prix_min": 16000, "prix_max": 30000},
        {"marque": "Mercedes", "modele": "Classe A", "annee_min": 2017, "annee_max": 2023, "prix_min": 18000, "prix_max": 32000},
        {"marque": "Ford", "modele": "Focus", "annee_min": 2015, "annee_max": 2022, "prix_min": 8000, "prix_max": 18000},
        {"marque": "Toyota", "modele": "Yaris", "annee_min": 2016, "annee_max": 2023, "prix_min": 9000, "prix_max": 19000},
        {"marque": "Nissan", "modele": "Micra", "annee_min": 2015, "annee_max": 2022, "prix_min": 6000, "prix_max": 14000},
        {"marque": "Opel", "modele": "Corsa", "annee_min": 2016, "annee_max": 2023, "prix_min": 7000, "prix_max": 15000},
        {"marque": "Fiat", "modele": "500", "annee_min": 2014, "annee_max": 2022, "prix_min": 5000, "prix_max": 12000},
    ]
    
    # Descriptions de réparations réalistes
    reparations_courantes = [
        "Révision complète + vidange",
        "Changement plaquettes de frein",
        "Réparation climatisation",
        "Remplacement pneus",
        "Carrosserie rayures + retouche peinture",
        "Changement échappement",
        "Réparation système électrique",
        "Changement amortisseurs",
        "Révision distribution",
        "Nettoyage complet intérieur/extérieur",
        "Changement batterie + alternateur",
        "Réparation boîte de vitesse",
        "Changement embrayage",
        "Réparation direction assistée",
        "Polissage carrosserie",
    ]
    
    # Générer véhicules de repérage
    vehicules_reperage = []
    vehicules_achetes = []
    
    # 15 véhicules en repérage
    for i in range(15):
        template = random.choice(vehicules_templates)
        
        lot = f"LOT{100 + i:03d}"
        annee = random.randint(template["annee_min"], template["annee_max"])
        kilometrage = f"{random.randint(15, 180)},000 km"
        
        # Calculs réalistes
        prix_revente = random.randint(template["prix_min"], template["prix_max"])
        cout_reparations = random.randint(200, 2500)
        temps_reparations = random.randint(2, 20)
        
        # Prix max calculé (formule réaliste)
        prix_max_achat = prix_revente - cout_reparations - (temps_reparations * 25) - (prix_revente * 0.08) - 200 - 1000
        prix_max_achat = max(prix_max_achat, 1000)  # Minimum 1000€
        
        vehicule = {
            "lot": lot,
            "marque": template["marque"],
            "modele": template["modele"],
            "annee": str(annee),
            "kilometrage": kilometrage,
            "chose_a_faire": random.choice(reparations_courantes),
            "cout_reparations": str(cout_reparations),
            "temps_reparations": str(temps_reparations),
            "prix_revente": str(prix_revente),
            "prix_max_achat": f"{prix_max_achat:.0f}",
            "prix_achat": "",
            "statut": "Repérage",
            "date_ajout": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
        }
        
        vehicules_reperage.append(vehicule)
    
    # 8 véhicules achetés
    for i in range(8):
        template = random.choice(vehicules_templates)
        
        lot = f"ACH{200 + i:03d}"
        annee = random.randint(template["annee_min"], template["annee_max"])
        kilometrage = f"{random.randint(25, 160)},000 km"
        
        # Calculs pour véhicules achetés
        prix_revente = random.randint(template["prix_min"], template["prix_max"])
        cout_reparations = random.randint(300, 2000)
        temps_reparations = random.randint(3, 15)
        
        prix_max_achat = prix_revente - cout_reparations - (temps_reparations * 25) - (prix_revente * 0.08) - 200 - 1000
        prix_max_achat = max(prix_max_achat, 1000)
        
        # Prix d'achat réel (parfois au-dessus du max pour simulation réaliste)
        if random.random() < 0.8:  # 80% de bons achats
            prix_achat = random.randint(int(prix_max_achat * 0.7), int(prix_max_achat))
        else:  # 20% d'achats au-dessus du prix max
            prix_achat = random.randint(int(prix_max_achat), int(prix_max_achat * 1.3))
        
        date_achat = datetime.now() - timedelta(days=random.randint(1, 60))
        
        vehicule = {
            "lot": lot,
            "marque": template["marque"],
            "modele": template["modele"],
            "annee": str(annee),
            "kilometrage": kilometrage,
            "chose_a_faire": random.choice(reparations_courantes),
            "cout_reparations": str(cout_reparations),
            "temps_reparations": str(temps_reparations),
            "prix_revente": str(prix_revente),
            "prix_max_achat": f"{prix_max_achat:.0f}",
            "prix_achat": str(prix_achat),
            "statut": "Acheté",
            "date_ajout": (date_achat - timedelta(days=random.randint(1, 10))).isoformat(),
            "date_achat": date_achat.isoformat()
        }
        
        vehicules_achetes.append(vehicule)
    
    return vehicules_reperage, vehicules_achetes

def generer_parametres_demo():
    """Génère des paramètres de démonstration"""
    return {
        "tarif_horaire": 25.0,
        "type_marge": "pourcentage",
        "marge_minimum": 15.0,
        "commission_encheres": 8.0,
        "frais_fixes": 200.0,
        "mode_edition": "double_clic"
    }

def sauvegarder_donnees_demo():
    """Sauvegarde les données de démonstration"""
    print("🎯 Génération des données de démonstration...")
    
    # Générer les données
    vehicules_reperage, vehicules_achetes = generer_donnees_demo()
    parametres = generer_parametres_demo()
    
    # Structure de données conforme au DataManager
    donnees = {
        "vehicules_reperage": vehicules_reperage,
        "vehicules_achetes": vehicules_achetes,
        "version": "4.0"
    }
    
    # Sauvegarder les véhicules
    try:
        with open("donnees_encheres.json", "w", encoding="utf-8") as f:
            json.dump(donnees, f, indent=2, ensure_ascii=False)
        print(f"✅ {len(vehicules_reperage)} véhicules de repérage générés")
        print(f"✅ {len(vehicules_achetes)} véhicules achetés générés")
    except Exception as e:
        print(f"❌ Erreur sauvegarde véhicules: {e}")
        return False
    
    # Sauvegarder les paramètres
    try:
        with open("parametres_encheres.json", "w", encoding="utf-8") as f:
            json.dump(parametres, f, indent=2, ensure_ascii=False)
        print("✅ Paramètres générés")
    except Exception as e:
        print(f"❌ Erreur sauvegarde paramètres: {e}")
        return False
    
    # Calculer quelques statistiques pour info
    total_invest = sum(int(v.get("prix_achat", 0)) for v in vehicules_achetes if v.get("prix_achat"))
    marges = []
    for v in vehicules_achetes:
        if v.get("prix_achat"):
            prix_revente = int(v["prix_revente"])
            prix_achat = int(v["prix_achat"])
            cout_rep = int(v["cout_reparations"])
            temps_rep = int(v["temps_reparations"])
            
            marge = prix_revente - prix_achat - cout_rep - (temps_rep * 25) - (prix_revente * 0.08) - 200
            marges.append(marge)
    
    marge_totale = sum(marges)
    marge_moyenne = marge_totale / len(marges) if marges else 0
    
    print(f"\n📊 STATISTIQUES DE DÉMONSTRATION:")
    print(f"   💰 Budget investi: {total_invest:,}€")
    print(f"   📈 Marge totale: {marge_totale:,.0f}€")
    print(f"   📊 Marge moyenne: {marge_moyenne:.0f}€")
    print(f"   ✅ Achats rentables: {len([m for m in marges if m > 0])}/{len(marges)}")
    
    return True

def main():
    """Fonction principale"""
    print("=" * 60)
    print("🎯 GÉNÉRATEUR DE DONNÉES DE DÉMONSTRATION V4")
    print("=" * 60)
    
    if sauvegarder_donnees_demo():
        print("\n🎉 Données de démonstration créées avec succès!")
        print("\n🚀 Vous pouvez maintenant:")
        print("   1. Lancer l'application: python main.py")
        print("   2. Ou créer l'EXE: python build_exe.py")
        print("\n✨ Profitez de l'application avec des données réalistes!")
    else:
        print("\n❌ Erreur lors de la génération des données")

if __name__ == "__main__":
    main() 