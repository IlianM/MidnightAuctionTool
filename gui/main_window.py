#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenêtre principale de l'application avec CustomTkinter
"""

import customtkinter as ctk
from tkinter import messagebox

from config.settings import AppSettings
from gui.reperage_tab import ReperageTab
from gui.achetes_tab import AchetesTab  
from gui.parametres_tab import ParametresTab
from models.journee_enchere import JourneeEnchere
from services.journees_manager import JourneesManager

class MainWindow:
    """Fenêtre principale avec onglets CustomTkinter - Version par journée d'enchère"""
    
    def __init__(self, root, journee: JourneeEnchere, journees_manager: JourneesManager, on_retour_journees: callable):
        self.root = root
        self.journee = journee
        self.journees_manager = journees_manager
        self.on_retour_journees = on_retour_journees
        
        # Configuration de la fenêtre avec le nom de la journée
        self.root.title(f"🚗 Gestionnaire d'Enchères - {journee.nom}")
        self.root.geometry("1400x900")
        
        # Gestionnaire de données adaptatif pour la journée
        self.data_adapter = JourneeDataAdapter(journee, journees_manager)
        
        # Paramètres
        self.settings = AppSettings()
        
        # Configuration du mode sombre/clair depuis les paramètres de la journée
        mode = "dark" if journee.parametres.get('mode_sombre', False) else "light"
        ctk.set_appearance_mode(mode)
        
        # Initialisation de l'interface
        self.creer_interface()
        
        print(f"🚀 Application initialisée avec la journée: {journee.nom}")
    
    def creer_interface(self):
        """Crée l'interface principale avec onglets et barre de navigation"""
        # Barre de navigation supérieure
        self.creer_barre_navigation()
        
        # Frame principal pour les onglets
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Création du TabView
        self.tabview = ctk.CTkTabview(main_frame)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Créer les onglets
        self.tab_reperage = self.tabview.add("🔍 Repérage")
        self.tab_achetes = self.tabview.add("🏆 Véhicules Achetés") 
        self.tab_parametres = self.tabview.add("⚙️ Paramètres")
        
        # Initialiser les composants des onglets
        self.reperage_tab = ReperageTab(
            self.tab_reperage, 
            self.settings, 
            self.data_adapter,
            None,  # style_manager
            self.on_data_changed
        )
        
        self.achetes_tab = AchetesTab(
            self.tab_achetes,
            self.settings,
            self.data_adapter,
            None,  # style_manager
            self.on_data_changed
        )
        
        self.parametres_tab = ParametresTab(
            self.tab_parametres,
            self.settings,
            self.data_adapter,
            None,  # style_manager
            self.journee,  # Passer la journée pour les paramètres spécifiques
            self.on_parametres_changed
        )
        
        # Démarrer sur l'onglet repérage
        self.tabview.set("🔍 Repérage")
    
    def creer_barre_navigation(self):
        """Crée la barre de navigation avec infos de la journée et bouton retour"""
        nav_frame = ctk.CTkFrame(self.root, height=80)
        nav_frame.pack(fill="x", padx=10, pady=10)
        nav_frame.pack_propagate(False)
        
        # Bouton retour
        retour_btn = ctk.CTkButton(
            nav_frame,
            text="🔙 Retour aux journées",
            command=self.retour_journees,
            font=ctk.CTkFont(size=12, weight="bold"),
            width=180,
            height=35
        )
        retour_btn.pack(side="left", padx=15, pady=22)
        
        # Informations de la journée au centre
        info_frame = ctk.CTkFrame(nav_frame)
        info_frame.pack(side="left", expand=True, fill="both", padx=10, pady=15)
        
        # Titre de la journée
        titre_journee = ctk.CTkLabel(
            info_frame,
            text=f"🏆 {self.journee.nom}",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        titre_journee.pack(pady=(10, 2))
        
        # Détails de la journée
        details = []
        if self.journee.date:
            details.append(f"📅 {self.format_date(self.journee.date)}")
        if self.journee.lieu:
            details.append(f"📍 {self.journee.lieu}")
        
        if details:
            details_text = " • ".join(details)
            details_label = ctk.CTkLabel(
                info_frame,
                text=details_text,
                font=ctk.CTkFont(size=12),
                text_color="gray60"
            )
            details_label.pack(pady=(0, 10))
        
        # Statistiques rapides à droite
        stats_frame = ctk.CTkFrame(nav_frame)
        stats_frame.pack(side="right", padx=15, pady=15)
        
        nb_reperage = len(self.journee.vehicules_reperage)
        nb_achetes = len(self.journee.vehicules_achetes)
        
        stats_label = ctk.CTkLabel(
            stats_frame,
            text=f"🔍 {nb_reperage} repérage • ✅ {nb_achetes} achetés",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        stats_label.pack(padx=15, pady=10)
    
    def format_date(self, date_str: str) -> str:
        """Formate une date pour affichage"""
        try:
            if date_str:
                from datetime import datetime
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                return date_obj.strftime("%d/%m/%Y")
            return "Date non définie"
        except:
            return date_str or "Date non définie"
    
    def retour_journees(self):
        """Retourne à la sélection des journées"""
        # Sauvegarder avant de partir
        self.journees_manager.sauvegarder_journee_active()
        
        # Appeler le callback de retour
        if self.on_retour_journees:
            self.on_retour_journees()
    
    def on_data_changed(self):
        """Callback appelé quand les données changent"""
        # Sauvegarder la journée active
        self.journees_manager.sauvegarder_journee_active()
        
        # Mettre à jour la barre de navigation
        self.actualiser_barre_navigation()
    
    def on_parametres_changed(self):
        """Callback appelé quand les paramètres changent"""
        # Recalculer tous les prix max des véhicules avec les nouveaux paramètres
        for vehicule in self.journee.vehicules_reperage:
            vehicule.mettre_a_jour_prix_max_avec_parametres(self.journee.parametres)
        
        # Sauvegarder
        self.journees_manager.sauvegarder_journee_active()
        
        # Actualiser les onglets
        if hasattr(self, 'reperage_tab'):
            self.reperage_tab.actualiser()
        if hasattr(self, 'achetes_tab'):
            self.achetes_tab.actualiser()
    
    def actualiser_barre_navigation(self):
        """Met à jour les statistiques de la barre de navigation"""
        # Cette méthode peut être appelée pour actualiser les stats
        # Pour l'instant, on recrée simplement la barre
        pass


class JourneeDataAdapter:
    """Adaptateur pour faire fonctionner les onglets existants avec une journée spécifique"""
    
    def __init__(self, journee: JourneeEnchere, journees_manager: JourneesManager):
        self.journee = journee
        self.journees_manager = journees_manager
    
    @property
    def vehicules_reperage(self):
        """Accès aux véhicules de repérage de la journée"""
        return self.journee.vehicules_reperage
    
    @property
    def vehicules_achetes(self):
        """Accès aux véhicules achetés de la journée"""
        return self.journee.vehicules_achetes
    
    def ajouter_vehicule(self, vehicule):
        """Ajoute un véhicule à la journée"""
        self.journee.ajouter_vehicule_reperage(vehicule)
        return True
    
    def supprimer_vehicule(self, index):
        """Supprime un véhicule du repérage"""
        if 0 <= index < len(self.journee.vehicules_reperage):
            del self.journee.vehicules_reperage[index]
            return True
        return False
    
    def marquer_achete(self, index):
        """Marque un véhicule comme acheté"""
        # Cette méthode sera appelée depuis l'interface
        # La logique de transfert est déjà dans l'interface
        return True
    
    def sauvegarder_donnees(self):
        """Sauvegarde les données de la journée"""
        return self.journees_manager.sauvegarder_journee_active()
    
    def get_statistiques(self):
        """Retourne les statistiques de la journée"""
        return {
            'nb_reperage': len(self.journee.vehicules_reperage),
            'nb_achetes': len(self.journee.vehicules_achetes),
            'total_investissement': self.journee.get_total_investissement()
        } 