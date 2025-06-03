#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Onglet paramètres - CustomTkinter
"""

import customtkinter as ctk
from tkinter import messagebox

from config.settings import AppSettings
from services.data_manager import DataManager
from utils.styles import StyleManager

class ParametresTab:
    """Onglet paramètres avec CustomTkinter"""
    
    def __init__(self, parent, settings: AppSettings, data_manager: DataManager,
                 style_manager: StyleManager, on_data_changed=None):
        self.parent = parent
        self.settings = settings
        self.data_manager = data_manager
        self.style_manager = style_manager
        self.on_data_changed = on_data_changed
        
        # Variables d'interface
        self.vars_parametres = {}
        
        # Créer le frame principal
        self.frame = ctk.CTkFrame(parent)
        
        self.creer_interface()
    
    def creer_interface(self):
        """Crée l'interface de l'onglet paramètres avec CustomTkinter"""
        main_frame = ctk.CTkFrame(self.frame)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre
        titre = ctk.CTkLabel(
            main_frame,
            text="⚙️ PARAMÈTRES DE L'APPLICATION",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titre.pack(pady=(0, 30))
        
        # Frame pour les paramètres
        params_frame = ctk.CTkFrame(main_frame)
        params_frame.pack(fill="both", expand=True)
        
        # Initialiser les variables
        self.initialiser_variables()
        
        # Section tarifs
        self.creer_section_tarifs(params_frame)
        
        # Section marges
        self.creer_section_marges(params_frame)
        
        # Section apparence
        self.creer_section_apparence(params_frame)
        
        # Boutons
        self.creer_boutons(main_frame)
        
        # Charger les valeurs actuelles
        self.charger_valeurs()
    
    def initialiser_variables(self):
        """Initialise les variables d'interface"""
        self.vars_parametres = {
            'tarif_horaire': ctk.StringVar(),
            'commission_vente': ctk.StringVar(),
            'commission_achat': ctk.StringVar(),
            'marge_securite': ctk.StringVar(),
            'mode_sombre': ctk.BooleanVar()
        }
    
    def creer_section_tarifs(self, parent):
        """Crée la section des tarifs"""
        section_frame = ctk.CTkFrame(parent)
        section_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Titre section
        titre_section = ctk.CTkLabel(
            section_frame,
            text="💰 TARIFS ET COMMISSIONS",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        titre_section.pack(pady=(15, 20))
        
        # Grid pour les champs
        grid_frame = ctk.CTkFrame(section_frame)
        grid_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Tarif horaire
        tarif_frame = ctk.CTkFrame(grid_frame)
        tarif_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            tarif_frame,
            text="Tarif horaire (€/h):",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=200
        ).pack(side="left", padx=10)
        
        ctk.CTkEntry(
            tarif_frame,
            textvariable=self.vars_parametres['tarif_horaire'],
            width=100,
            placeholder_text="25"
        ).pack(side="right", padx=10)
        
        # Commission vente
        comm_vente_frame = ctk.CTkFrame(grid_frame)
        comm_vente_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            comm_vente_frame,
            text="Commission vente (%):",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=200
        ).pack(side="left", padx=10)
        
        ctk.CTkEntry(
            comm_vente_frame,
            textvariable=self.vars_parametres['commission_vente'],
            width=100,
            placeholder_text="8.5"
        ).pack(side="right", padx=10)
        
        # Commission achat
        comm_achat_frame = ctk.CTkFrame(grid_frame)
        comm_achat_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            comm_achat_frame,
            text="Commission achat (%):",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=200
        ).pack(side="left", padx=10)
        
        ctk.CTkEntry(
            comm_achat_frame,
            textvariable=self.vars_parametres['commission_achat'],
            width=100,
            placeholder_text="1.2"
        ).pack(side="right", padx=10)
    
    def creer_section_marges(self, parent):
        """Crée la section des marges"""
        section_frame = ctk.CTkFrame(parent)
        section_frame.pack(fill="x", padx=20, pady=10)
        
        # Titre section
        titre_section = ctk.CTkLabel(
            section_frame,
            text="📊 MARGES ET SÉCURITÉ",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        titre_section.pack(pady=(15, 20))
        
        # Grid pour les champs
        grid_frame = ctk.CTkFrame(section_frame)
        grid_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Marge de sécurité
        marge_frame = ctk.CTkFrame(grid_frame)
        marge_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            marge_frame,
            text="Marge de sécurité (€):",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=200
        ).pack(side="left", padx=10)
        
        ctk.CTkEntry(
            marge_frame,
            textvariable=self.vars_parametres['marge_securite'],
            width=100,
            placeholder_text="200"
        ).pack(side="right", padx=10)
    
    def creer_section_apparence(self, parent):
        """Crée la section apparence"""
        section_frame = ctk.CTkFrame(parent)
        section_frame.pack(fill="x", padx=20, pady=10)
        
        # Titre section
        titre_section = ctk.CTkLabel(
            section_frame,
            text="🎨 APPARENCE",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        titre_section.pack(pady=(15, 20))
        
        # Mode sombre
        mode_frame = ctk.CTkFrame(section_frame)
        mode_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(
            mode_frame,
            text="Mode sombre:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left", padx=10)
        
        ctk.CTkCheckBox(
            mode_frame,
            text="Activer le mode sombre",
            variable=self.vars_parametres['mode_sombre'],
            command=self.toggle_mode_sombre
        ).pack(side="right", padx=10)
    
    def creer_boutons(self, parent):
        """Crée les boutons d'action"""
        buttons_frame = ctk.CTkFrame(parent)
        buttons_frame.pack(fill="x", pady=(20, 0))
        
        # Bouton Sauvegarder
        sauvegarder_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Sauvegarder",
            command=self.sauvegarder_parametres,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        sauvegarder_btn.pack(side="left", padx=20, pady=15)
        
        # Bouton Réinitialiser
        reset_btn = ctk.CTkButton(
            buttons_frame,
            text="🔄 Réinitialiser",
            command=self.reinitialiser_parametres,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        reset_btn.pack(side="left", padx=10, pady=15)
        
        # Bouton Aide
        aide_btn = ctk.CTkButton(
            buttons_frame,
            text="❓ Aide",
            command=self.afficher_aide,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        aide_btn.pack(side="right", padx=20, pady=15)
    
    def charger_valeurs(self):
        """Charge les valeurs actuelles des paramètres"""
        # Valeurs par défaut ou depuis les settings
        self.vars_parametres['tarif_horaire'].set(str(getattr(self.settings, 'tarif_horaire', 25)))
        self.vars_parametres['commission_vente'].set(str(getattr(self.settings, 'commission_vente', 8.5)))
        self.vars_parametres['commission_achat'].set(str(getattr(self.settings, 'commission_achat', 1.2)))
        self.vars_parametres['marge_securite'].set(str(getattr(self.settings, 'marge_securite', 200)))
        
        # Mode sombre
        current_mode = ctk.get_appearance_mode()
        self.vars_parametres['mode_sombre'].set(current_mode == "Dark")
    
    def toggle_mode_sombre(self):
        """Bascule le mode sombre"""
        if self.vars_parametres['mode_sombre'].get():
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
    
    def sauvegarder_parametres(self):
        """Sauvegarde les paramètres"""
        try:
            # Validation des valeurs
            tarif = float(self.vars_parametres['tarif_horaire'].get() or 25)
            comm_vente = float(self.vars_parametres['commission_vente'].get() or 8.5)
            comm_achat = float(self.vars_parametres['commission_achat'].get() or 1.2)
            marge_sec = float(self.vars_parametres['marge_securite'].get() or 200)
            
            if tarif <= 0 or comm_vente < 0 or comm_achat < 0 or marge_sec < 0:
                raise ValueError("Les valeurs doivent être positives")
            
            # Sauvegarder (si les attributs existent dans settings)
            if hasattr(self.settings, 'tarif_horaire'):
                self.settings.tarif_horaire = tarif
            if hasattr(self.settings, 'commission_vente'):
                self.settings.commission_vente = comm_vente
            if hasattr(self.settings, 'commission_achat'):
                self.settings.commission_achat = comm_achat
            if hasattr(self.settings, 'marge_securite'):
                self.settings.marge_securite = marge_sec
            
            # Sauvegarder le fichier de configuration
            self.settings.sauvegarder()
            
            messagebox.showinfo("✅ Succès", "Paramètres sauvegardés avec succès !")
            
            # Notifier les changements
            if self.on_data_changed:
                self.on_data_changed()
                
        except ValueError as e:
            messagebox.showerror("❌ Erreur", f"Valeurs invalides: {e}")
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de la sauvegarde: {e}")
    
    def reinitialiser_parametres(self):
        """Réinitialise les paramètres aux valeurs par défaut"""
        if messagebox.askyesno("Confirmation", "Réinitialiser tous les paramètres ?"):
            self.vars_parametres['tarif_horaire'].set("25")
            self.vars_parametres['commission_vente'].set("8.5")
            self.vars_parametres['commission_achat'].set("1.2")
            self.vars_parametres['marge_securite'].set("200")
            self.vars_parametres['mode_sombre'].set(False)
            ctk.set_appearance_mode("light")
    
    def afficher_aide(self):
        """Affiche l'aide des paramètres"""
        aide_text = """
🔧 AIDE PARAMÈTRES

💰 TARIFS:
• Tarif horaire: Coût de votre temps de travail
• Commission vente: Frais de vente (ex: 8.5%)
• Commission achat: Frais d'achat (ex: 1.2%)

📊 MARGES:
• Marge de sécurité: Montant à déduire pour les imprévus

🎨 APPARENCE:
• Mode sombre: Interface sombre pour réduire la fatigue oculaire

💡 Les paramètres sont automatiquement utilisés pour calculer le prix maximum d'achat.
        """
        
        messagebox.showinfo("❓ Aide", aide_text)
    
    def actualiser(self):
        """Met à jour l'affichage (si nécessaire)"""
        self.charger_valeurs() 