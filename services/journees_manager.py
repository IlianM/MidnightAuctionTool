#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire des journées d'enchères - Version fichiers séparés
"""

import json
import os
import glob
from typing import List, Dict, Any, Optional
from datetime import datetime
from models.journee_enchere import JourneeEnchere


class JourneesManager:
    """Gestionnaire pour journées d'enchères avec fichiers séparés"""
    
    def __init__(self):
        self.dossier_journees = "journees_data"
        self.journee_active: Optional[JourneeEnchere] = None
        self.fichier_actif = ""
        
        # Créer le dossier s'il n'existe pas
        if not os.path.exists(self.dossier_journees):
            os.makedirs(self.dossier_journees)
        
        # Migrer les anciennes données si nécessaire
        self.migrer_anciennes_donnees()
    
    def migrer_anciennes_donnees(self):
        """Migre les anciennes données vers une première journée"""
        try:
            # Vérifier si l'ancien fichier unique existe
            ancien_fichier = "journees_encheres.json"
            if os.path.exists(ancien_fichier):
                print("🔄 Migration de l'ancien système...")
                with open(ancien_fichier, 'r', encoding='utf-8') as f:
                    anciennes_donnees = json.load(f)
                
                # Si on a des journées dans l'ancien format
                if 'journees' in anciennes_donnees:
                    for i, journee_data in enumerate(anciennes_donnees['journees']):
                        journee = JourneeEnchere(journee_data)
                        nom_fichier = f"migration_{i+1}_{journee.id}.json"
                        self.sauvegarder_journee_fichier(journee, nom_fichier)
                        print(f"✅ Journée migrée: {journee.nom}")
                
                # Renommer l'ancien fichier
                os.rename(ancien_fichier, f"{ancien_fichier}.backup")
                print("✅ Migration terminée, ancien fichier sauvegardé")
            
            # Vérifier l'ancien système de données uniques
            ancien_donnees = "donnees_encheres.json"
            if os.path.exists(ancien_donnees) and not self.get_journees_disponibles():
                print("🔄 Migration des données uniques...")
                with open(ancien_donnees, 'r', encoding='utf-8') as f:
                    anciennes_donnees = json.load(f)
                
                # Créer une journée avec les anciennes données
                journee = JourneeEnchere()
                journee.nom = "Migration - Données existantes"
                journee.description = "Journée créée automatiquement lors de la migration"
                
                # Migrer les véhicules
                if 'vehicules_reperage' in anciennes_donnees:
                    from models.vehicule import Vehicule
                    journee.vehicules_reperage = [Vehicule(v) for v in anciennes_donnees['vehicules_reperage']]
                
                if 'vehicules_achetes' in anciennes_donnees:
                    from models.vehicule import Vehicule
                    journee.vehicules_achetes = [Vehicule(v) for v in anciennes_donnees['vehicules_achetes']]
                
                # Migrer les paramètres si ils existent
                if os.path.exists("parametres_encheres.json"):
                    with open("parametres_encheres.json", 'r', encoding='utf-8') as f:
                        anciens_parametres = json.load(f)
                        journee.parametres.update(anciens_parametres)
                
                nom_fichier = f"migration_{journee.id}.json"
                self.sauvegarder_journee_fichier(journee, nom_fichier)
                
                # Renommer l'ancien fichier
                os.rename(ancien_donnees, f"{ancien_donnees}.backup")
                print(f"✅ Données migrées: {len(journee.vehicules_reperage)} repérage, {len(journee.vehicules_achetes)} achetés")
                
        except Exception as e:
            print(f"⚠️ Erreur migration: {e}")
    
    def get_journees_disponibles(self) -> List[Dict[str, Any]]:
        """Retourne la liste des journées disponibles"""
        journees = []
        
        # Chercher tous les fichiers JSON dans le dossier
        pattern = os.path.join(self.dossier_journees, "*.json")
        fichiers = glob.glob(pattern)
        
        for fichier in fichiers:
            try:
                with open(fichier, 'r', encoding='utf-8') as f:
                    donnees = json.load(f)
                
                # Récupérer les infos de base
                info = {
                    'fichier': os.path.basename(fichier),
                    'chemin_complet': fichier,
                    'nom': donnees.get('nom', 'Journée sans nom'),
                    'date': donnees.get('date', ''),
                    'lieu': donnees.get('lieu', ''),
                    'description': donnees.get('description', ''),
                    'nb_reperage': len(donnees.get('vehicules_reperage', [])),
                    'nb_achetes': len(donnees.get('vehicules_achetes', [])),
                    'date_creation': donnees.get('date_creation', '')
                }
                
                # Calculer l'investissement
                investissement = 0.0
                for vehicule in donnees.get('vehicules_achetes', []):
                    try:
                        prix = float(vehicule.get('prix_achat', '0').replace(',', '.').replace('€', ''))
                        investissement += prix
                    except:
                        pass
                
                info['investissement'] = investissement
                journees.append(info)
                
            except Exception as e:
                print(f"⚠️ Erreur lecture fichier {fichier}: {e}")
        
        # Trier par date de création (plus récent en premier)
        journees.sort(key=lambda x: x.get('date_creation', ''), reverse=True)
        
        return journees
    
    def creer_nouvelle_journee(self, nom: str, date: str = "", lieu: str = "", description: str = "") -> str:
        """Crée une nouvelle journée et retourne le nom du fichier"""
        journee = JourneeEnchere()
        journee.nom = nom
        if date:
            journee.date = date
        if lieu:
            journee.lieu = lieu
        if description:
            journee.description = description
        
        # Générer un nom de fichier unique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nom_securise = "".join(c for c in nom if c.isalnum() or c in (' ', '-', '_')).rstrip()
        nom_securise = nom_securise.replace(' ', '_')[:20]  # Limiter la taille
        
        nom_fichier = f"{timestamp}_{nom_securise}.json"
        
        self.sauvegarder_journee_fichier(journee, nom_fichier)
        
        print(f"✅ Nouvelle journée créée: {nom_fichier}")
        return nom_fichier
    
    def sauvegarder_journee_fichier(self, journee: JourneeEnchere, nom_fichier: str) -> bool:
        """Sauvegarde une journée dans son fichier"""
        try:
            chemin = os.path.join(self.dossier_journees, nom_fichier)
            
            with open(chemin, 'w', encoding='utf-8') as f:
                json.dump(journee.to_dict(), f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur sauvegarde {nom_fichier}: {e}")
            return False
    
    def charger_journee_fichier(self, nom_fichier: str) -> Optional[JourneeEnchere]:
        """Charge une journée depuis son fichier"""
        try:
            chemin = os.path.join(self.dossier_journees, nom_fichier)
            
            if not os.path.exists(chemin):
                print(f"❌ Fichier non trouvé: {nom_fichier}")
                return None
            
            with open(chemin, 'r', encoding='utf-8') as f:
                donnees = json.load(f)
            
            journee = JourneeEnchere(donnees)
            self.journee_active = journee
            self.fichier_actif = nom_fichier
            
            print(f"✅ Journée chargée: {journee.nom} ({nom_fichier})")
            return journee
            
        except Exception as e:
            print(f"❌ Erreur chargement {nom_fichier}: {e}")
            return None
    
    def supprimer_journee(self, nom_fichier: str) -> bool:
        """Supprime une journée (son fichier)"""
        try:
            chemin = os.path.join(self.dossier_journees, nom_fichier)
            
            if os.path.exists(chemin):
                os.remove(chemin)
                print(f"✅ Journée supprimée: {nom_fichier}")
                return True
            else:
                print(f"❌ Fichier non trouvé: {nom_fichier}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur suppression {nom_fichier}: {e}")
            return False
    
    def modifier_journee(self, nom_fichier: str, nom: str = None, date: str = None, 
                        lieu: str = None, description: str = None) -> bool:
        """Modifie les informations d'une journée"""
        journee = self.charger_journee_fichier(nom_fichier)
        if not journee:
            return False
        
        if nom is not None:
            journee.nom = nom
        if date is not None:
            journee.date = date
        if lieu is not None:
            journee.lieu = lieu
        if description is not None:
            journee.description = description
        
        return self.sauvegarder_journee_fichier(journee, nom_fichier)
    
    def sauvegarder_journee_active(self) -> bool:
        """Sauvegarde la journée actuellement active"""
        if self.journee_active and self.fichier_actif:
            return self.sauvegarder_journee_fichier(self.journee_active, self.fichier_actif)
        return False 