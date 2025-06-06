#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration et paramètres de l'application
"""

import json
import os

class AppSettings:
    """Gestionnaire de configuration de l'application"""
    
    def __init__(self):
        # Fichiers de configuration
        self.fichier_donnees = "donnees_encheres.json"
        self.fichier_parametres = "parametres_encheres.json"
        
        # Paramètres par défaut (MODIFIÉS : ajout paramètres d'interface)
        self.parametres_defaut = {
            'tarif_horaire': 45.0,
            'commission_vente': 8.5,  # Commission lors de la vente (%)
            'marge_securite': 200.0,  # Marge de sécurité en euros
            'mode_edition': 'double_clic',
            
            # NOUVEAUX PARAMÈTRES D'INTERFACE
            'hauteur_lignes_tableau': 30,  # Hauteur des lignes des tableaux (pixels)
            'taille_police_tableau': 14,  # Taille de police dans les tableaux
            'taille_police_entetes': 16,  # Taille de police des en-têtes de tableaux
            'taille_police_titres': 20,  # Taille de police des titres principales
            'taille_police_boutons': 12,  # Taille de police des boutons
            'taille_police_labels': 12,  # Taille de police des labels normaux
            'taille_police_champs': 12,  # Taille de police des champs de saisie
            'largeur_colonnes_auto': True,  # Ajustement automatique des colonnes
        }
        
        # Couleurs du thème
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72', 
            'success': '#F18F01',
            'danger': '#C73E1D',
            'dark': '#1A1A2E',
            'light': '#F5F7FA',
            'accent': '#FFD23F',
            'white': '#FFFFFF',
            'gray_light': '#E8E8E8',
            'gray_medium': '#CCCCCC',
            'text_dark': '#2C3E50'
        }
        
        # Configuration interface
        self.window_config = {
            'title': "🚗 Gestionnaire d'Enchères Véhicules PRO v4",
            'geometry': "1600x1000",
            'state': 'zoomed'
        }
        
        # Configuration colonnes tableau (MODIFIÉE : ajout colonne Prix Max)
        self.colonnes_reperage = [
            "Lot", "Marque", "Modèle", "Année", "Km", "À Faire", 
            "Coût R.", "Temps R.", "Prix Rev.", "Prix Max", "Prix Achat", "Statut"
        ]
        
        self.largeurs_colonnes = [60, 100, 120, 60, 80, 180, 70, 65, 85, 90, 85, 80]
        
        self.colonnes_achetes = [
            "Lot", "Marque", "Modèle", "Année", 
            "Prix Achat", "Prix Max", "Marge", "Date Achat"
        ]
        
        # Charger paramètres utilisateur
        self.parametres = self.parametres_defaut.copy()
        self.charger_parametres()
    
    def charger_parametres(self):
        """Charge les paramètres depuis le fichier"""
        if os.path.exists(self.fichier_parametres):
            try:
                with open(self.fichier_parametres, 'r', encoding='utf-8') as f:
                    parametres_fichier = json.load(f)
                    self.parametres.update(parametres_fichier)
            except Exception as e:
                print(f"⚠️ Erreur chargement paramètres: {e}")
    
    def sauvegarder_parametres(self):
        """Sauvegarde les paramètres dans le fichier"""
        try:
            with open(self.fichier_parametres, 'w', encoding='utf-8') as f:
                json.dump(self.parametres, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Erreur sauvegarde paramètres: {e}")
            return False
    
    def reinitialiser_parametres(self):
        """Remet les paramètres aux valeurs par défaut"""
        self.parametres = self.parametres_defaut.copy()
        return self.sauvegarder_parametres()
    
    def calculer_prix_max(self, prix_revente: float, cout_reparations: float, temps_reparations: float) -> float:
        """
        Calcule le prix maximum d'achat selon la formule :
        Prix Max = Prix Revente - (Coût Réparations + Main d'Œuvre) - Commission Vente - Marge Sécurité
        """
        try:
            # Main d'œuvre = Temps × Tarif horaire
            main_oeuvre = temps_reparations * self.parametres.get('tarif_horaire', 45.0)
            
            # Commission vente = pourcentage du prix de revente
            commission_vente = prix_revente * (self.parametres.get('commission_vente', 8.5) / 100)
            
            # Marge de sécurité
            marge_securite = self.parametres.get('marge_securite', 200.0)
            
            # Calcul final
            prix_max = prix_revente - (cout_reparations + main_oeuvre) - commission_vente - marge_securite
            
            # Ne pas retourner de valeur négative
            return max(0, prix_max)
            
        except Exception as e:
            print(f"⚠️ Erreur calcul prix max: {e}")
            return 0.0
    
    def get_font_config(self, element_type):
        """
        Retourne la configuration de police pour un type d'élément donné
        
        Args:
            element_type (str): Type d'élément ('tableau', 'entetes', 'titres', 'boutons', 'labels', 'champs')
        
        Returns:
            dict: Configuration de police avec 'family', 'size' et optionnellement 'weight'
        """
        base_size = self.parametres.get(f'taille_police_{element_type}', 12)
        
        configs = {
            'tableau': {'family': 'Segoe UI', 'size': base_size},
            'entetes': {'family': 'Segoe UI', 'size': base_size, 'weight': 'bold'},
            'titres': {'family': 'Segoe UI', 'size': base_size, 'weight': 'bold'},
            'boutons': {'family': 'Segoe UI', 'size': base_size, 'weight': 'bold'},
            'labels': {'family': 'Segoe UI', 'size': base_size, 'weight': 'bold'},
            'champs': {'family': 'Segoe UI', 'size': base_size}
        }
        
        return configs.get(element_type, {'family': 'Segoe UI', 'size': 12})
    
    def get_ctk_font(self, element_type, weight=None):
        """
        Retourne un objet CTkFont configuré pour l'élément demandé
        
        Args:
            element_type (str): Type d'élément
            weight (str, optional): Poids de la police ('normal', 'bold')
        
        Returns:
            CTkFont: Police configurée
        """
        try:
            import customtkinter as ctk
            config = self.get_font_config(element_type)
            
            font_weight = weight or config.get('weight', 'normal')
            return ctk.CTkFont(
                family=config['family'],
                size=config['size'],
                weight=font_weight
            )
        except ImportError:
            # Fallback si CustomTkinter n'est pas disponible
            return None
    
    def get_tableau_height(self):
        """Retourne la hauteur des lignes de tableau configurée"""
        return self.parametres.get('hauteur_lignes_tableau', 30) 