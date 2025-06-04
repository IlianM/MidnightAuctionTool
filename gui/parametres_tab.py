#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Onglet paramètres - CustomTkinter - Version par journée
"""

import customtkinter as ctk
from tkinter import messagebox

from config.settings import AppSettings
from utils.tooltips import ajouter_tooltip, TOOLTIPS

class ParametresTab:
    """Onglet paramètres avec CustomTkinter - Version par journée d'enchère"""
    
    def __init__(self, parent, settings: AppSettings, data_adapter,
                 style_manager, journee, on_parametres_changed=None):
        self.parent = parent
        self.settings = settings
        self.data_adapter = data_adapter
        self.style_manager = style_manager
        self.journee = journee  # Journée d'enchère spécifique
        self.on_parametres_changed = on_parametres_changed
        
        # Variables d'interface
        self.vars_parametres = {}
        
        # Créer l'interface directement dans le parent (qui est un onglet du TabView)
        self.creer_interface()
    
    def creer_interface(self):
        """Crée l'interface de l'onglet paramètres avec CustomTkinter"""
        main_frame = ctk.CTkScrollableFrame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre avec nom de la journée
        titre = ctk.CTkLabel(
            main_frame,
            text=f"⚙️ PARAMÈTRES DE L'ENCHÈRE\n{self.journee.nom}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titre.pack(pady=(0, 30))
        
        # Information importante
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", pady=(0, 20))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="💡 Ces paramètres sont spécifiques à cette journée d'enchère\net n'affectent que les véhicules de cette journée.",
            font=ctk.CTkFont(size=12),
            text_color="#2E86AB"
        )
        info_label.pack(pady=15)
        
        # Frame pour les paramètres
        params_frame = ctk.CTkFrame(main_frame)
        params_frame.pack(fill="x", pady=(0, 20))
        
        # Initialiser les variables
        self.initialiser_variables()
        
        # Section tarifs
        self.creer_section_tarifs(params_frame)
        
        # Section marges
        self.creer_section_marges(params_frame)
        
        # Section apparence (mode sombre)
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
        
        tarif_label = ctk.CTkLabel(
            tarif_frame,
            text="Tarif horaire (€/h):",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=200
        )
        tarif_label.pack(side="left", padx=10)
        
        tarif_entry = ctk.CTkEntry(
            tarif_frame,
            textvariable=self.vars_parametres['tarif_horaire'],
            width=100,
            placeholder_text="45"
        )
        tarif_entry.pack(side="right", padx=10)
        
        # Ajouter tooltip
        ajouter_tooltip(tarif_label, TOOLTIPS['param_tarif_horaire'])
        ajouter_tooltip(tarif_entry, TOOLTIPS['param_tarif_horaire'])
        
        # Commission vente
        comm_vente_frame = ctk.CTkFrame(grid_frame)
        comm_vente_frame.pack(fill="x", pady=5)
        
        comm_vente_label = ctk.CTkLabel(
            comm_vente_frame,
            text="Commission vente (%):",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=200
        )
        comm_vente_label.pack(side="left", padx=10)
        
        comm_vente_entry = ctk.CTkEntry(
            comm_vente_frame,
            textvariable=self.vars_parametres['commission_vente'],
            width=100,
            placeholder_text="8.5"
        )
        comm_vente_entry.pack(side="right", padx=10)
        
        # Ajouter tooltip
        ajouter_tooltip(comm_vente_label, TOOLTIPS['param_commission_vente'])
        ajouter_tooltip(comm_vente_entry, TOOLTIPS['param_commission_vente'])
    
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
        
        marge_label = ctk.CTkLabel(
            marge_frame,
            text="Marge de sécurité (€):",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=200
        )
        marge_label.pack(side="left", padx=10)
        
        marge_entry = ctk.CTkEntry(
            marge_frame,
            textvariable=self.vars_parametres['marge_securite'],
            width=100,
            placeholder_text="200"
        )
        marge_entry.pack(side="right", padx=10)
        
        # Ajouter tooltip
        ajouter_tooltip(marge_label, TOOLTIPS['param_marge_securite'])
        ajouter_tooltip(marge_entry, TOOLTIPS['param_marge_securite'])
        
        # Explication du calcul
        explication_frame = ctk.CTkFrame(grid_frame)
        explication_frame.pack(fill="x", pady=(10, 0))
        
        explication_text = """💡 FORMULE DU PRIX MAXIMUM :
Prix Max = Prix Revente - (Coût Réparations + Main d'Œuvre) - Commission Vente - Marge Sécurité

Où Main d'Œuvre = Temps Réparations × Tarif Horaire"""
        
        explication_label = ctk.CTkLabel(
            explication_frame,
            text=explication_text,
            font=ctk.CTkFont(size=11),
            text_color="#666666",
            justify="left"
        )
        explication_label.pack(padx=20, pady=15)
    
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
        
        mode_sombre_label = ctk.CTkLabel(
            mode_frame,
            text="Mode sombre:",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=200
        )
        mode_sombre_label.pack(side="left", padx=10, pady=10)
        
        mode_sombre_switch = ctk.CTkSwitch(
            mode_frame,
            text="",
            variable=self.vars_parametres['mode_sombre'],
            command=self.toggle_mode_sombre
        )
        mode_sombre_switch.pack(side="right", padx=10, pady=10)
        
        # Ajouter tooltip
        ajouter_tooltip(mode_sombre_label, TOOLTIPS['param_mode_sombre'])
        ajouter_tooltip(mode_sombre_switch, TOOLTIPS['param_mode_sombre'])
    
    def creer_boutons(self, parent):
        """Crée les boutons d'action"""
        buttons_frame = ctk.CTkFrame(parent)
        buttons_frame.pack(fill="x", pady=20)
        
        # Bouton sauvegarder
        save_button = ctk.CTkButton(
            buttons_frame,
            text="💾 Sauvegarder les paramètres",
            command=self.sauvegarder_parametres,
            font=ctk.CTkFont(size=12, weight="bold"),
            width=200,
            height=40
        )
        save_button.pack(side="left", padx=20, pady=15)
        
        # Bouton réinitialiser
        reset_button = ctk.CTkButton(
            buttons_frame,
            text="🔄 Réinitialiser",
            command=self.reinitialiser_parametres,
            font=ctk.CTkFont(size=12, weight="bold"),
            width=150,
            height=40
        )
        reset_button.pack(side="left", padx=10, pady=15)
        
        # Bouton aide
        help_button = ctk.CTkButton(
            buttons_frame,
            text="❓ Aide",
            command=self.afficher_aide,
            font=ctk.CTkFont(size=12, weight="bold"),
            width=100,
            height=40
        )
        help_button.pack(side="right", padx=20, pady=15)
        
        # Ajouter tooltips
        ajouter_tooltip(save_button, TOOLTIPS['btn_sauvegarder_param'])
        ajouter_tooltip(reset_button, TOOLTIPS['btn_reinitialiser_param'])
        ajouter_tooltip(help_button, TOOLTIPS['btn_aide_param'])
    
    def charger_valeurs(self):
        """Charge les valeurs des paramètres de la journée"""
        parametres = self.journee.parametres
        
        self.vars_parametres['tarif_horaire'].set(str(parametres.get('tarif_horaire', 45.0)))
        self.vars_parametres['commission_vente'].set(str(parametres.get('commission_vente', 8.5)))
        self.vars_parametres['marge_securite'].set(str(parametres.get('marge_securite', 200.0)))
        self.vars_parametres['mode_sombre'].set(parametres.get('mode_sombre', False))
    
    def toggle_mode_sombre(self):
        """Bascule le mode sombre"""
        mode_sombre = self.vars_parametres['mode_sombre'].get()
        mode = "dark" if mode_sombre else "light"
        ctk.set_appearance_mode(mode)
    
    def sauvegarder_parametres(self):
        """Sauvegarde les paramètres de la journée"""
        try:
            # Récupérer et valider les valeurs
            tarif_horaire = float(self.vars_parametres['tarif_horaire'].get().replace(',', '.'))
            commission_vente = float(self.vars_parametres['commission_vente'].get().replace(',', '.'))
            marge_securite = float(self.vars_parametres['marge_securite'].get().replace(',', '.'))
            mode_sombre = self.vars_parametres['mode_sombre'].get()
            
            # Validation
            if tarif_horaire < 0 or commission_vente < 0 or marge_securite < 0:
                messagebox.showerror("❌ Erreur", "Les valeurs ne peuvent pas être négatives")
                return
            
            if commission_vente > 100:
                messagebox.showerror("❌ Erreur", "La commission ne peut pas dépasser 100%")
                return
            
            # Mettre à jour les paramètres de la journée
            self.journee.parametres['tarif_horaire'] = tarif_horaire
            self.journee.parametres['commission_vente'] = commission_vente
            self.journee.parametres['marge_securite'] = marge_securite
            self.journee.parametres['mode_sombre'] = mode_sombre
            
            # Notifier le changement pour recalculer les prix max
            if self.on_parametres_changed:
                self.on_parametres_changed()
            
            messagebox.showinfo("✅ Succès", "Paramètres sauvegardés et prix maximums recalculés !")
            
        except ValueError:
            messagebox.showerror("❌ Erreur", "Veuillez entrer des valeurs numériques valides")
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de la sauvegarde: {e}")
    
    def reinitialiser_parametres(self):
        """Remet les paramètres aux valeurs par défaut"""
        if messagebox.askyesno("Confirmation", "Remettre tous les paramètres aux valeurs par défaut ?"):
            # Valeurs par défaut
            self.journee.parametres = {
                'tarif_horaire': 45.0,
                'commission_vente': 8.5,
                'marge_securite': 200.0,
                'mode_sombre': False
            }
            
            # Recharger l'affichage
            self.charger_valeurs()
            
            # Notifier le changement
            if self.on_parametres_changed:
                self.on_parametres_changed()
            
            messagebox.showinfo("✅ Succès", "Paramètres réinitialisés !")
    
    def afficher_aide(self):
        """Affiche l'aide détaillée"""
        aide_text = """🔧 AIDE - PARAMÈTRES DE L'ENCHÈRE

💰 TARIF HORAIRE
Votre tarif horaire pour calculer le coût de la main d'œuvre.
Utilisé dans le calcul : Main d'Œuvre = Temps × Tarif Horaire

💸 COMMISSION VENTE
Pourcentage prélevé lors de la vente du véhicule réparé.
Utilisé dans le calcul : Commission = Prix Revente × (% / 100)

🛡️ MARGE DE SÉCURITÉ  
Marge fixe déduite pour couvrir les imprévus et garantir la rentabilité.
Montant fixe en euros décompté du prix maximum.

🎨 MODE SOMBRE
Active/désactive le thème sombre de l'interface.

📊 CALCUL DU PRIX MAXIMUM
Prix Max = Prix Revente - (Coût Réparations + Main d'Œuvre) - Commission Vente - Marge Sécurité

⚠️ CES PARAMÈTRES SONT SPÉCIFIQUES À CETTE JOURNÉE D'ENCHÈRE
Chaque journée a ses propres paramètres et ne sont pas partagés."""
        
        messagebox.showinfo("🔧 Aide - Paramètres", aide_text)
    
    def actualiser(self):
        """Met à jour l'affichage (si nécessaire)"""
        self.charger_valeurs() 