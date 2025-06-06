#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Outil de migration pour convertir les anciennes données vers le nouveau système de journées
Usage: python tools_migration_ami.py [chemin_vers_donnees_encheres.json]
"""

import json
import os
import sys
from datetime import datetime

def convertir_ancien_format_vers_journee(ancien_fichier_json, nom_journee=None):
    """
    Convertit un fichier donnees_encheres.json de l'ancienne version 
    vers le nouveau format de journée
    
    Args:
        ancien_fichier_json (str): Chemin vers l'ancien fichier JSON
        nom_journee (str): Nom optionnel pour la journée
    
    Returns:
        str: Nom du fichier créé ou None si erreur
    """
    try:
        # Vérifier que le fichier existe
        if not os.path.exists(ancien_fichier_json):
            print(f"❌ ERREUR: Le fichier {ancien_fichier_json} n'existe pas.")
            return None
        
        # Charger les anciennes données
        print(f"📂 Chargement de {ancien_fichier_json}...")
        with open(ancien_fichier_json, 'r', encoding='utf-8') as f:
            anciennes_donnees = json.load(f)
        
        # Vérifier la structure des anciennes données
        if 'vehicules_reperage' not in anciennes_donnees and 'vehicules_achetes' not in anciennes_donnees:
            print("❌ ERREUR: Structure de données non reconnue. Ce fichier ne semble pas être un ancien fichier de données.")
            return None
        
        # Créer l'ID unique basé sur timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        journee_id = timestamp
        
        # Nom par défaut si pas spécifié
        if not nom_journee:
            nom_journee = f"Migration - {os.path.basename(ancien_fichier_json).replace('.json', '')}"
        
        print(f"🔄 Conversion vers la journée: {nom_journee}")
        
        # Convertir chaque véhicule vers le nouveau format
        def convertir_vehicule(vehicule_ancien):
            """Convertit un véhicule de l'ancien format vers le nouveau"""
            vehicule_nouveau = vehicule_ancien.copy()
            
            # Ajouter les nouveaux champs avec valeurs par défaut
            vehicule_nouveau.setdefault('prix_vente_final', '')
            vehicule_nouveau.setdefault('motorisation', '')
            vehicule_nouveau.setdefault('champ_libre', '')
            vehicule_nouveau.setdefault('reserve_professionnels', False)
            vehicule_nouveau.setdefault('couleur', 'turquoise')
            
            return vehicule_nouveau
        
        # Convertir les véhicules
        vehicules_reperage_nouveaux = []
        vehicules_achetes_nouveaux = []
        
        # Convertir véhicules en repérage
        if 'vehicules_reperage' in anciennes_donnees:
            for vehicule in anciennes_donnees['vehicules_reperage']:
                vehicules_reperage_nouveaux.append(convertir_vehicule(vehicule))
            print(f"✅ {len(vehicules_reperage_nouveaux)} véhicules en repérage convertis")
        
        # Convertir véhicules achetés
        if 'vehicules_achetes' in anciennes_donnees:
            for vehicule in anciennes_donnees['vehicules_achetes']:
                vehicules_achetes_nouveaux.append(convertir_vehicule(vehicule))
            print(f"✅ {len(vehicules_achetes_nouveaux)} véhicules achetés convertis")
        
        # Créer la nouvelle structure de journée
        nouvelle_journee = {
            "id": journee_id,
            "nom": nom_journee,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "lieu": "",
            "description": f"Journée migrée automatiquement depuis {os.path.basename(ancien_fichier_json)}",
            "date_creation": datetime.now().isoformat(),
            "parametres": {
                "tarif_horaire": 45.0,
                "commission_vente": 8.5,
                "marge_securite": 200.0,
                "type_marge": "pourcentage",
                "marge_minimum": 15.0,
                "commission_encheres": 8.0,
                "frais_fixes": 200.0,
                "mode_edition": "double_clic",
                "mode_sombre": False,
                "hauteur_lignes_tableau": 30,
                "taille_police_tableau": 14,
                "taille_police_entetes": 16,
                "taille_police_titres": 20,
                "taille_police_boutons": 12,
                "taille_police_labels": 12,
                "taille_police_champs": 12,
                "largeur_colonnes_auto": True
            },
            "vehicules_reperage": vehicules_reperage_nouveaux,
            "vehicules_achetes": vehicules_achetes_nouveaux
        }
        
        # Créer le dossier journees_data s'il n'existe pas
        if not os.path.exists('journees_data'):
            os.makedirs('journees_data')
            print("📁 Dossier journees_data créé")
        
        # Sauvegarder la nouvelle journée
        nom_fichier = f"migration_{journee_id}_{nom_journee.replace(' ', '_').replace('-', '_')}.json"
        # Nettoyer le nom de fichier des caractères spéciaux
        nom_fichier = "".join(c for c in nom_fichier if c.isalnum() or c in "._-")
        chemin_fichier = os.path.join('journees_data', nom_fichier)
        
        with open(chemin_fichier, 'w', encoding='utf-8') as f:
            json.dump(nouvelle_journee, f, indent=2, ensure_ascii=False)
        
        print(f"✅ MIGRATION TERMINÉE AVEC SUCCÈS !")
        print(f"📄 Fichier créé: {chemin_fichier}")
        print(f"📊 Résumé:")
        print(f"   • {len(vehicules_reperage_nouveaux)} véhicules en repérage")
        print(f"   • {len(vehicules_achetes_nouveaux)} véhicules achetés")
        print(f"   • Journée: {nom_journee}")
        print(f"")
        print(f"🎯 INSTRUCTIONS POUR VOTRE AMI:")
        print(f"   1. Copiez le fichier {nom_fichier}")
        print(f"   2. Placez-le dans le dossier 'journees_data' de la nouvelle version")
        print(f"   3. Lancez l'application, la journée apparaîtra dans la liste")
        
        return chemin_fichier
        
    except Exception as e:
        print(f"❌ ERREUR lors de la migration: {e}")
        return None

def main():
    """Fonction principale de l'outil de migration"""
    print("=" * 60)
    print("🔄 OUTIL DE MIGRATION - DONNÉES ANCIENNES VERS NOUVELLES")
    print("=" * 60)
    
    # Vérifier les arguments
    if len(sys.argv) < 2:
        print("📋 Usage: python tools_migration_ami.py [chemin_vers_donnees_encheres.json] [nom_journee_optionnel]")
        print("")
        
        # Chercher automatiquement un fichier donnees_encheres.json
        fichiers_possibles = [
            'donnees_encheres.json',
            '../donnees_encheres.json',
            'data/donnees_encheres.json'
        ]
        
        fichier_trouve = None
        for fichier in fichiers_possibles:
            if os.path.exists(fichier):
                fichier_trouve = fichier
                break
        
        if fichier_trouve:
            print(f"📂 Fichier trouvé automatiquement: {fichier_trouve}")
            reponse = input("Voulez-vous migrer ce fichier ? (oui/non): ").lower().strip()
            if reponse in ['oui', 'o', 'yes', 'y']:
                nom_journee = input("Nom de la journée (optionnel, Entrée pour défaut): ").strip()
                if not nom_journee:
                    nom_journee = None
                convertir_ancien_format_vers_journee(fichier_trouve, nom_journee)
            else:
                print("❌ Migration annulée.")
        else:
            print("❌ Aucun fichier donnees_encheres.json trouvé automatiquement.")
            print("   Spécifiez le chemin vers votre fichier en paramètre.")
        return
    
    # Paramètres fournis
    ancien_fichier = sys.argv[1]
    nom_journee = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Lancer la migration
    resultat = convertir_ancien_format_vers_journee(ancien_fichier, nom_journee)
    
    if resultat:
        print("\n🎉 MIGRATION RÉUSSIE ! Votre ami peut maintenant utiliser ses données avec la nouvelle version.")
    else:
        print("\n❌ ÉCHEC DE LA MIGRATION. Vérifiez le fichier source.")

if __name__ == "__main__":
    main() 