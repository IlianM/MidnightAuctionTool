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
    
    def importer_journee_json(self, chemin_fichier: str) -> tuple[bool, str]:
        """
        Importe une journée depuis un fichier JSON externe
        
        Args:
            chemin_fichier: Chemin vers le fichier JSON à importer
            
        Returns:
            tuple[bool, str]: (succès, message)
        """
        try:
            # Vérifier que le fichier existe
            if not os.path.exists(chemin_fichier):
                return False, f"Fichier non trouvé : {chemin_fichier}"
            
            # Lire le fichier JSON
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                donnees = json.load(f)
            
            # Valider la structure de base
            champs_requis = ['nom', 'vehicules_reperage', 'vehicules_achetes']
            for champ in champs_requis:
                if champ not in donnees:
                    return False, f"Structure JSON invalide : champ '{champ}' manquant"
            
            # Créer une nouvelle journée avec les données importées
            journee = JourneeEnchere()
            
            # Récupérer les informations ou générer des valeurs par défaut
            journee.nom = donnees.get('nom', 'Journée importée')
            journee.date = donnees.get('date', datetime.now().strftime("%Y-%m-%d"))
            journee.lieu = donnees.get('lieu', '')
            journee.description = donnees.get('description', 'Importée depuis JSON')
            journee.parametres = donnees.get('parametres', {
                'tarif_horaire': 45.0,
                'commission_vente': 8.5,
                'marge_securite': 200.0
            })
            
            # Importer les véhicules
            from models.vehicule import Vehicule
            
            journee.vehicules_reperage = []
            for v_data in donnees.get('vehicules_reperage', []):
                vehicule = Vehicule(v_data)
                journee.vehicules_reperage.append(vehicule)
            
            journee.vehicules_achetes = []
            for v_data in donnees.get('vehicules_achetes', []):
                vehicule = Vehicule(v_data)
                journee.vehicules_achetes.append(vehicule)
            
            # Générer un nom de fichier unique
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nom_securise = "".join(c for c in journee.nom if c.isalnum() or c in (' ', '-', '_')).rstrip()
            nom_securise = nom_securise.replace(' ', '_')[:20]
            nom_fichier = f"import_{timestamp}_{nom_securise}.json"
            
            # Sauvegarder la journée importée
            if self.sauvegarder_journee_fichier(journee, nom_fichier):
                return True, f"Journée importée avec succès !\nFichier créé : {nom_fichier}\nVéhicules importés : {len(journee.vehicules_reperage)} en repérage, {len(journee.vehicules_achetes)} achetés"
            else:
                return False, "Erreur lors de la sauvegarde de la journée importée"
                
        except json.JSONDecodeError as e:
            return False, f"Erreur de format JSON : {e}"
        except Exception as e:
            return False, f"Erreur lors de l'import : {e}"
    
    def exporter_journee_json(self, nom_fichier: str, chemin_export: str) -> tuple[bool, str]:
        """
        Exporte une journée vers un fichier JSON externe
        
        Args:
            nom_fichier: Nom du fichier de la journée à exporter
            chemin_export: Chemin de destination pour l'export
            
        Returns:
            tuple[bool, str]: (succès, message)
        """
        try:
            # Charger la journée
            journee = self.charger_journee_fichier(nom_fichier)
            if not journee:
                return False, f"Impossible de charger la journée : {nom_fichier}"
            
            # Exporter vers le fichier de destination
            with open(chemin_export, 'w', encoding='utf-8') as f:
                json.dump(journee.to_dict(), f, indent=2, ensure_ascii=False)
            
            return True, f"Journée exportée avec succès vers :\n{chemin_export}"
            
        except Exception as e:
            return False, f"Erreur lors de l'export : {e}"
    
    def exporter_toutes_journees_json(self, chemin_dossier: str) -> tuple[bool, str]:
        """
        Exporte toutes les journées vers un dossier
        
        Args:
            chemin_dossier: Dossier de destination
            
        Returns:
            tuple[bool, str]: (succès, message)
        """
        try:
            # Créer le dossier si nécessaire
            if not os.path.exists(chemin_dossier):
                os.makedirs(chemin_dossier)
            
            journees = self.get_journees_disponibles()
            if not journees:
                return False, "Aucune journée à exporter"
            
            exports_reussis = 0
            
            for info_journee in journees:
                nom_fichier = info_journee['fichier']
                
                # Générer un nom de fichier d'export sécurisé
                nom_export = nom_fichier.replace('.json', '_export.json')
                chemin_export = os.path.join(chemin_dossier, nom_export)
                
                # Exporter la journée
                succes, _ = self.exporter_journee_json(nom_fichier, chemin_export)
                if succes:
                    exports_reussis += 1
            
            return True, f"Export terminé : {exports_reussis}/{len(journees)} journées exportées vers :\n{chemin_dossier}"
            
        except Exception as e:
            return False, f"Erreur lors de l'export de toutes les journées : {e}"
    
    def importer_donnees_csv(self, chemin_fichier: str, nom_journee: str = None, mapping_colonnes: dict = None) -> tuple[bool, str]:
        """
        Importe des données depuis un fichier CSV et crée une nouvelle journée
        
        Args:
            chemin_fichier: Chemin vers le fichier CSV
            nom_journee: Nom pour la nouvelle journée
            mapping_colonnes: Dictionnaire de mapping des colonnes CSV vers les champs
            
        Returns:
            tuple[bool, str]: (succès, message)
        """
        try:
            import csv
            
            # Vérifier que le fichier existe
            if not os.path.exists(chemin_fichier):
                return False, f"Fichier non trouvé : {chemin_fichier}"
            
            # Nom par défaut
            if not nom_journee:
                nom_journee = f"Import CSV - {os.path.basename(chemin_fichier).replace('.csv', '')}"
            
            # Mapping par défaut des colonnes
            if not mapping_colonnes:
                mapping_colonnes = {
                    'lot': ['lot', 'n°lot', 'numero lot', 'LOT', 'N° LOT'],
                    'marque': ['marque', 'MARQUE', 'Marque'],
                    'modele': ['modele', 'modèle', 'MODELE', 'MODÈLE', 'Modèle'],
                    'annee': ['annee', 'année', 'ANNEE', 'ANNÉE', 'Année'],
                    'kilometrage': ['kilometrage', 'kilométrage', 'km', 'KM', 'Kilométrage'],
                    'motorisation': ['motorisation', 'MOTORISATION', 'Motorisation', 'moteur'],
                    'prix_revente': ['prix_revente', 'prix revente', 'PRIX REVENTE', 'prix de revente'],
                    'cout_reparations': ['cout_reparations', 'coût réparations', 'COUT REPARATIONS', 'cout reparations'],
                    'temps_reparations': ['temps_reparations', 'temps réparations', 'TEMPS REPARATIONS', 'temps (h)'],
                    'prix_max_achat': ['prix_max_achat', 'prix max', 'PRIX MAX', 'prix maximum'],
                    'prix_achat': ['prix_achat', 'prix achat', 'PRIX ACHAT', 'prix d\'achat'],
                    'chose_a_faire': ['chose_a_faire', 'description', 'DESCRIPTION', 'travaux', 'réparations'],
                    'champ_libre': ['champ_libre', 'notes', 'NOTES', 'commentaires'],
                    'statut': ['statut', 'STATUT', 'Statut'],
                    'date_achat': ['date_achat', 'date achat', 'DATE ACHAT']
                }
            
            # Lire le fichier CSV
            lignes = []
            with open(chemin_fichier, 'r', encoding='utf-8-sig', newline='') as csvfile:
                # Détecter le délimiteur
                sample = csvfile.read(1024)
                csvfile.seek(0)
                
                delimiter = ';' if ';' in sample else ','
                reader = csv.DictReader(csvfile, delimiter=delimiter)
                
                # Récupérer les en-têtes
                headers = reader.fieldnames
                if not headers:
                    return False, "Le fichier CSV ne contient pas d'en-têtes valides"
                
                # Lire toutes les lignes
                for ligne in reader:
                    lignes.append(ligne)
            
            if not lignes:
                return False, "Le fichier CSV est vide ou ne contient aucune donnée"
            
            # Créer la fonction de mapping des colonnes
            def trouver_colonne(champ, headers):
                """Trouve la colonne correspondant au champ dans les headers"""
                if champ in mapping_colonnes:
                    for possible in mapping_colonnes[champ]:
                        for header in headers:
                            if header.lower().strip() == possible.lower().strip():
                                return header
                # Fallback : correspondance partielle
                for header in headers:
                    if champ.lower() in header.lower() or header.lower() in champ.lower():
                        return header
                return None
            
            # Créer la nouvelle journée
            from models.journee_enchere import JourneeEnchere
            from models.vehicule import Vehicule
            
            journee = JourneeEnchere()
            journee.nom = nom_journee
            journee.date = datetime.now().strftime("%Y-%m-%d")
            journee.description = f"Journée créée depuis import CSV : {os.path.basename(chemin_fichier)}"
            
            # Convertir chaque ligne en véhicule
            vehicules_reperage = []
            vehicules_achetes = []
            
            for i, ligne in enumerate(lignes):
                try:
                    # Extraire les données selon le mapping
                    donnees_vehicule = {}
                    
                    for champ in ['lot', 'marque', 'modele', 'annee', 'kilometrage', 'motorisation',
                                'prix_revente', 'cout_reparations', 'temps_reparations', 'prix_max_achat',
                                'prix_achat', 'chose_a_faire', 'champ_libre', 'statut', 'date_achat']:
                        
                        colonne = trouver_colonne(champ, headers)
                        if colonne and colonne in ligne:
                            valeur = ligne[colonne].strip()
                            
                            # Nettoyage des valeurs numériques
                            if champ in ['prix_revente', 'cout_reparations', 'temps_reparations', 'prix_achat']:
                                valeur = valeur.replace('€', '').replace(',', '.').replace(' ', '')
                                # Garder seulement les chiffres et le point décimal
                                valeur = ''.join(c for c in valeur if c.isdigit() or c == '.')
                            
                            donnees_vehicule[champ] = valeur
                    
                    # Valeurs par défaut
                    donnees_vehicule.setdefault('couleur', 'turquoise')
                    donnees_vehicule.setdefault('reserve_professionnels', False)
                    donnees_vehicule.setdefault('prix_vente_final', '')
                    
                    # Créer le véhicule
                    vehicule = Vehicule(donnees_vehicule)
                    
                    # Déterminer s'il est acheté ou en repérage
                    statut = donnees_vehicule.get('statut', '').lower()
                    prix_achat = donnees_vehicule.get('prix_achat', '').strip()
                    
                    if (statut == 'acheté' or statut == 'achete') or (prix_achat and prix_achat != '0'):
                        vehicule.statut = "Acheté"
                        if not vehicule.date_achat:
                            vehicule.date_achat = datetime.now().strftime("%d/%m/%Y")
                        vehicules_achetes.append(vehicule)
                    else:
                        vehicule.statut = "Repérage"
                        vehicules_reperage.append(vehicule)
                        
                except Exception as e:
                    print(f"⚠️ Erreur ligne {i+1}: {e}")
                    continue
            
            # Assigner les véhicules à la journée
            journee.vehicules_reperage = vehicules_reperage
            journee.vehicules_achetes = vehicules_achetes
            
            # Générer un nom de fichier unique
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nom_securise = "".join(c for c in nom_journee if c.isalnum() or c in (' ', '-', '_')).rstrip()
            nom_securise = nom_securise.replace(' ', '_')[:20]
            nom_fichier = f"csv_import_{timestamp}_{nom_securise}.json"
            
            # Sauvegarder la journée
            if self.sauvegarder_journee_fichier(journee, nom_fichier):
                message = f"✅ Import CSV réussi !\n"
                message += f"📄 Fichier créé : {nom_fichier}\n"
                message += f"📊 Données importées :\n"
                message += f"   • {len(vehicules_reperage)} véhicules en repérage\n"
                message += f"   • {len(vehicules_achetes)} véhicules achetés\n"
                message += f"   • Total : {len(lignes)} lignes traitées"
                return True, message
            else:
                return False, "Erreur lors de la sauvegarde de la journée"
                
        except UnicodeDecodeError:
            return False, "Erreur d'encodage du fichier CSV. Assurez-vous qu'il est encodé en UTF-8."
        except Exception as e:
            return False, f"Erreur lors de l'import CSV : {e}"
    
    def importer_donnees_pdf(self, chemin_fichier: str, nom_journee: str = None) -> tuple[bool, str]:
        """
        Importe des données depuis un fichier PDF et crée une nouvelle journée
        
        Args:
            chemin_fichier: Chemin vers le fichier PDF
            nom_journee: Nom pour la nouvelle journée
            
        Returns:
            tuple[bool, str]: (succès, message)
        """
        try:
            # Vérifier que le fichier existe
            if not os.path.exists(chemin_fichier):
                return False, f"Fichier non trouvé : {chemin_fichier}"
            
            # Nom par défaut
            if not nom_journee:
                nom_journee = f"Import PDF - {os.path.basename(chemin_fichier).replace('.pdf', '')}"
            
            # Importer pdfplumber
            try:
                import pdfplumber
            except ImportError:
                return False, "La bibliothèque 'pdfplumber' n'est pas installée.\nInstallez-la avec: pip install pdfplumber"
            
            # Ouvrir le PDF
            with pdfplumber.open(chemin_fichier) as pdf:
                # Extraire le texte et les tableaux de toutes les pages
                vehicules_data = []
                texte_complet = ""
                
                for page_num, page in enumerate(pdf.pages):
                    # Extraire le texte de la page
                    texte_page = page.extract_text()
                    if texte_page:
                        texte_complet += texte_page + "\n"
                    
                    # Essayer d'extraire des tableaux
                    tableaux = page.extract_tables()
                    
                    for table_num, tableau in enumerate(tableaux):
                        if tableau and len(tableau) > 1:  # Au moins une ligne d'en-tête + données
                            vehicules_tableau = self._analyser_tableau_pdf(tableau, page_num, table_num)
                            vehicules_data.extend(vehicules_tableau)
                
                # Si aucun tableau trouvé, essayer d'analyser le texte brut
                if not vehicules_data:
                    vehicules_data = self._analyser_texte_pdf(texte_complet)
                
                # Si toujours aucune donnée, retourner une erreur
                if not vehicules_data:
                    return False, f"Aucune donnée de véhicule détectée dans le PDF.\nTexte extrait ({len(texte_complet)} caractères):\n{texte_complet[:500]}..."
                
                # Créer la nouvelle journée
                from models.journee_enchere import JourneeEnchere
                from models.vehicule import Vehicule
                
                journee = JourneeEnchere()
                journee.nom = nom_journee
                journee.date = datetime.now().strftime("%Y-%m-%d")
                journee.description = f"Journée créée depuis import PDF : {os.path.basename(chemin_fichier)}"
                
                # Convertir les données en véhicules
                vehicules_reperage = []
                vehicules_achetes = []
                
                for donnees in vehicules_data:
                    try:
                        # Valeurs par défaut
                        donnees.setdefault('couleur', 'turquoise')
                        donnees.setdefault('reserve_professionnels', False)
                        donnees.setdefault('prix_vente_final', '')
                        
                        # Créer le véhicule
                        vehicule = Vehicule(donnees)
                        
                        # Déterminer s'il est acheté ou en repérage
                        prix_achat = donnees.get('prix_achat', '').strip()
                        if prix_achat and prix_achat != '0':
                            vehicule.statut = "Acheté"
                            if not vehicule.date_achat:
                                vehicule.date_achat = datetime.now().strftime("%d/%m/%Y")
                            vehicules_achetes.append(vehicule)
                        else:
                            vehicule.statut = "Repérage"
                            vehicules_reperage.append(vehicule)
                            
                    except Exception as e:
                        print(f"⚠️ Erreur véhicule: {e}")
                        continue
                
                # Assigner les véhicules à la journée
                journee.vehicules_reperage = vehicules_reperage
                journee.vehicules_achetes = vehicules_achetes
                
                # Générer un nom de fichier unique
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nom_securise = "".join(c for c in nom_journee if c.isalnum() or c in (' ', '-', '_')).rstrip()
                nom_securise = nom_securise.replace(' ', '_')[:20]
                nom_fichier = f"pdf_import_{timestamp}_{nom_securise}.json"
                
                # Sauvegarder la journée
                if self.sauvegarder_journee_fichier(journee, nom_fichier):
                    message = f"✅ Import PDF réussi !\n"
                    message += f"📄 Fichier créé : {nom_fichier}\n"
                    message += f"📊 Données importées :\n"
                    message += f"   • {len(vehicules_reperage)} véhicules en repérage\n"
                    message += f"   • {len(vehicules_achetes)} véhicules achetés\n"
                    message += f"   • Total : {len(vehicules_data)} véhicules traités"
                    return True, message
                else:
                    return False, "Erreur lors de la sauvegarde de la journée"
                    
        except Exception as e:
            return False, f"Erreur lors de l'import PDF : {e}"
    
    def _analyser_tableau_pdf(self, tableau: list, page_num: int, table_num: int) -> list:
        """
        Analyse un tableau extrait du PDF et convertit en données de véhicules
        
        Args:
            tableau: Tableau extrait par pdfplumber
            page_num: Numéro de page
            table_num: Numéro de tableau dans la page
            
        Returns:
            list: Liste de dictionnaires représentant des véhicules
        """
        vehicules = []
        
        if not tableau or len(tableau) < 2:
            return vehicules
        
        # Première ligne = en-têtes
        headers = [str(cell).lower().strip() if cell else '' for cell in tableau[0]]
        
        # Mapping des colonnes vers les champs véhicule
        mapping_colonnes = {
            'lot': ['lot', 'n°lot', 'numero', 'n°', 'num'],
            'marque': ['marque', 'brand', 'constructeur'],
            'modele': ['modele', 'modèle', 'model', 'nom'],
            'annee': ['annee', 'année', 'year', 'an'],
            'kilometrage': ['kilometrage', 'kilométrage', 'km', 'mileage'],
            'motorisation': ['motorisation', 'moteur', 'engine', 'carburant'],
            'prix_revente': ['prix', 'prix_revente', 'revente', 'vente', 'price'],
            'cout_reparations': ['reparation', 'réparation', 'cout', 'coût', 'repair'],
            'temps_reparations': ['temps', 'heure', 'h', 'time'],
            'prix_max_achat': ['max', 'maximum', 'budget'],
            'prix_achat': ['achat', 'achete', 'acheté', 'purchase'],
            'chose_a_faire': ['description', 'travaux', 'todo', 'a_faire'],
            'champ_libre': ['notes', 'commentaire', 'libre', 'comment']
        }
        
        # Créer un mapping des index de colonnes
        index_mapping = {}
        for champ, possibles in mapping_colonnes.items():
            for i, header in enumerate(headers):
                if any(possible in header for possible in possibles):
                    index_mapping[champ] = i
                    break
        
        # Traiter chaque ligne de données
        for ligne_num, ligne in enumerate(tableau[1:], 1):
            try:
                donnees_vehicule = {}
                
                # Extraire les données selon le mapping
                for champ, index in index_mapping.items():
                    if index < len(ligne) and ligne[index]:
                        valeur = str(ligne[index]).strip()
                        
                        # Nettoyage des valeurs numériques
                        if champ in ['prix_revente', 'cout_reparations', 'temps_reparations', 'prix_achat', 'prix_max_achat']:
                            valeur = valeur.replace('€', '').replace(',', '.').replace(' ', '')
                            valeur = ''.join(c for c in valeur if c.isdigit() or c == '.')
                        
                        donnees_vehicule[champ] = valeur
                
                # Ajouter des valeurs par défaut si pas de lot
                if 'lot' not in donnees_vehicule:
                    donnees_vehicule['lot'] = f"P{page_num}T{table_num}L{ligne_num}"
                
                # Ne garder que les lignes avec au moins marque OU modèle
                if donnees_vehicule.get('marque') or donnees_vehicule.get('modele'):
                    vehicules.append(donnees_vehicule)
                    
            except Exception as e:
                print(f"⚠️ Erreur ligne {ligne_num}: {e}")
                continue
        
        return vehicules
    
    def _analyser_texte_pdf(self, texte: str) -> list:
        """
        Analyse le texte brut du PDF pour extraire des données de véhicules
        
        Args:
            texte: Texte complet extrait du PDF
            
        Returns:
            list: Liste de dictionnaires représentant des véhicules
        """
        vehicules = []
        
        # Mots-clés pour identifier les lignes de véhicules
        marques_auto = [
            'peugeot', 'renault', 'citroen', 'citroën', 'volkswagen', 'vw', 'audi', 'bmw', 'mercedes',
            'ford', 'opel', 'nissan', 'toyota', 'honda', 'hyundai', 'kia', 'seat', 'skoda',
            'fiat', 'alfa', 'volvo', 'mazda', 'mitsubishi', 'suzuki', 'dacia', 'mini', 'smart'
        ]
        
        # Patterns regex pour extraire des informations
        import re
        
        # Pattern pour les prix (€, euros)
        prix_pattern = r'(\d+(?:\s?\d{3})*(?:[.,]\d{2})?)\s*€?'
        
        # Pattern pour les années
        annee_pattern = r'\b(19|20)\d{2}\b'
        
        # Pattern pour les kilomètres
        km_pattern = r'(\d+(?:\s?\d{3})*)\s*(?:km|kilomètres?)'
        
        lignes = texte.split('\n')
        
        for i, ligne in enumerate(lignes):
            ligne_lower = ligne.lower().strip()
            
            # Ignorer les lignes vides ou trop courtes
            if not ligne_lower or len(ligne_lower) < 10:
                continue
            
            # Chercher des marques de voiture dans la ligne
            marque_trouvee = None
            for marque in marques_auto:
                if marque in ligne_lower:
                    marque_trouvee = marque.capitalize()
                    break
            
            if marque_trouvee:
                # Extraire les informations de cette ligne
                donnees_vehicule = {
                    'marque': marque_trouvee,
                    'lot': f"L{i+1}"
                }
                
                # Extraire le modèle (tout après la marque jusqu'au premier nombre)
                reste_ligne = ligne[ligne_lower.find(marque_trouvee.lower()) + len(marque_trouvee):].strip()
                modele_match = re.match(r'^([a-zA-Z\s\-]+)', reste_ligne)
                if modele_match:
                    donnees_vehicule['modele'] = modele_match.group(1).strip()
                
                # Chercher l'année
                annees = re.findall(annee_pattern, ligne)
                if annees:
                    donnees_vehicule['annee'] = annees[0] + annees[1] if len(annees) >= 2 else '20' + annees[0]
                
                # Chercher les kilomètres
                km_matches = re.findall(km_pattern, ligne_lower)
                if km_matches:
                    donnees_vehicule['kilometrage'] = km_matches[0].replace(' ', '')
                
                # Chercher les prix
                prix_matches = re.findall(prix_pattern, ligne)
                if prix_matches:
                    # Premier prix = prix de revente, deuxième = prix d'achat
                    donnees_vehicule['prix_revente'] = prix_matches[0].replace(' ', '')
                    if len(prix_matches) > 1:
                        donnees_vehicule['prix_achat'] = prix_matches[1].replace(' ', '')
                
                # Chercher dans les lignes suivantes pour plus d'infos
                for j in range(1, min(3, len(lignes) - i)):
                    ligne_suivante = lignes[i + j].strip()
                    if ligne_suivante and not any(m in ligne_suivante.lower() for m in marques_auto):
                        # Chercher des prix supplémentaires
                        prix_supp = re.findall(prix_pattern, ligne_suivante)
                        if prix_supp and 'prix_achat' not in donnees_vehicule:
                            donnees_vehicule['prix_achat'] = prix_supp[0].replace(' ', '')
                        
                        # Si c'est une description
                        if len(ligne_suivante) > 20 and not re.search(r'\d+', ligne_suivante):
                            donnees_vehicule['chose_a_faire'] = ligne_suivante[:100]
                
                vehicules.append(donnees_vehicule)
        
        return vehicules 