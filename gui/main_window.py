#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenêtre principale de l'application avec CustomTkinter
"""

import customtkinter as ctk
from tkinter import ttk, messagebox

from config.settings import AppSettings
from services.data_manager import DataManager
from utils.styles import StyleManager

from gui.dashboard_tab import DashboardTab
from gui.reperage_tab import ReperageTab
from gui.achetes_tab import AchetesTab  
from gui.parametres_tab import ParametresTab

class MainWindow:
    """Fenêtre principale de l'application (CustomTkinter)"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🚗 Gestionnaire d'Enchères Véhicules")
        
        # Initialiser les composants
        self.settings = AppSettings()
        self.data_manager = DataManager(self.settings)
        self.style_manager = StyleManager(self.settings)
        
        # Variables d'interface
        self.notebook = None
        self.tab_dashboard = None
        self.tab_reperage = None
        self.tab_achetes = None
        self.tab_parametres = None
        
        # Charger les données
        self.data_manager.charger_donnees()
        
        self.creer_interface()
        self.initialiser()
    
    def creer_interface(self):
        """Crée l'interface principale avec CustomTkinter"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Titre principal
        title_label = ctk.CTkLabel(
            main_frame,
            text="🚗 GESTIONNAIRE D'ENCHÈRES VÉHICULES",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(10, 20))
        
        # Notebook pour les onglets (utilisation du ttk.Notebook standard avec CustomTkinter)
        notebook_frame = ctk.CTkFrame(main_frame)
        notebook_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Configuration du style des onglets pour les agrandir
        style = ttk.Style()
        style.configure("TNotebook.Tab", padding=[60, 25], font=('Segoe UI', 16, 'bold'))
        style.configure("TNotebook", tabposition='n')
        
        # Créer les onglets
        self.tab_dashboard = DashboardTab(
            self.notebook,
            self.settings,
            self.data_manager,
            self.style_manager
        )
        
        self.tab_reperage = ReperageTab(
            self.notebook,
            self.settings,
            self.data_manager,
            self.style_manager,
            self.actualiser_tous_onglets
        )
        
        self.tab_achetes = AchetesTab(
            self.notebook,
            self.settings,
            self.data_manager,
            self.style_manager,
            self.actualiser_tous_onglets
        )
        
        self.tab_parametres = ParametresTab(
            self.notebook,
            self.settings,
            self.data_manager,
            self.style_manager,
            self.actualiser_tous_onglets
        )
        
        # Ajouter les onglets au notebook
        self.notebook.add(self.tab_dashboard.frame, text="📊 Dashboard")
        self.notebook.add(self.tab_reperage.frame, text="🔍 Repérage")
        self.notebook.add(self.tab_achetes.frame, text="🏆 Véhicules Achetés")
        self.notebook.add(self.tab_parametres.frame, text="⚙️ Paramètres")
        
        # Frame pour les boutons de contrôle
        control_frame = ctk.CTkFrame(main_frame)
        control_frame.pack(fill="x", pady=(20, 10), padx=10)
        
        # Bouton de sauvegarde
        save_button = ctk.CTkButton(
            control_frame,
            text="💾 Sauvegarder",
            command=self.sauvegarder_donnees,
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            height=40
        )
        save_button.pack(side="left", padx=15, pady=15)
        
        # Bouton d'actualisation
        refresh_button = ctk.CTkButton(
            control_frame,
            text="🔄 Actualiser",
            command=self.actualiser_tous_onglets,
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            height=40
        )
        refresh_button.pack(side="left", padx=15, pady=15)
        
        # Bouton de mode sombre/clair
        theme_button = ctk.CTkButton(
            control_frame,
            text="🌙 Mode Sombre",
            command=self.basculer_theme,
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            height=40
        )
        theme_button.pack(side="right", padx=15, pady=15)
        
        # Stocker la référence du bouton pour pouvoir le modifier
        self.theme_button = theme_button
    
    def basculer_theme(self):
        """Bascule entre le mode clair et sombre"""
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Light":
            ctk.set_appearance_mode("dark")
            self.theme_button.configure(text="☀️ Mode Clair")
        else:
            ctk.set_appearance_mode("light")
            self.theme_button.configure(text="🌙 Mode Sombre")
    
    def initialiser(self):
        """Initialise l'application après création de l'interface"""
        # Actualiser tous les onglets avec les données
        self.actualiser_tous_onglets()
        
        # Sélectionner le dashboard par défaut
        self.notebook.select(0)
        
        print(f"🚀 Application initialisée avec {len(self.data_manager.vehicules_reperage) + len(self.data_manager.vehicules_achetes)} véhicules")
    
    def actualiser_tous_onglets(self):
        """Met à jour tous les onglets"""
        if self.tab_dashboard:
            self.tab_dashboard.actualiser()
        if self.tab_reperage:
            self.tab_reperage.actualiser()
        if self.tab_achetes:
            self.tab_achetes.actualiser()
        if self.tab_parametres:
            self.tab_parametres.actualiser()
    
    def sauvegarder_donnees(self):
        """Sauvegarde les données"""
        try:
            self.data_manager.sauvegarder_donnees()
            self.settings.sauvegarder()
            messagebox.showinfo("✅ Succès", "Données sauvegardées avec succès !")
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de la sauvegarde: {e}")
    
    def on_closing(self):
        """Gère la fermeture de l'application"""
        self.sauvegarder_donnees()
        self.root.destroy() 