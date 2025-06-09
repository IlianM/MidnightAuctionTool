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
        
        # NOUVELLE SECTION INTERFACE
        self.creer_section_interface(params_frame)
        
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
            'mode_sombre': ctk.BooleanVar(),
            
            # NOUVELLES VARIABLES POUR L'INTERFACE
            'hauteur_lignes_tableau': ctk.StringVar(),
            'taille_police_tableau': ctk.StringVar(),
            'taille_police_entetes': ctk.StringVar(),
            'taille_police_titres': ctk.StringVar(),
            'taille_police_boutons': ctk.StringVar(),
            'taille_police_labels': ctk.StringVar(),
            'taille_police_champs': ctk.StringVar(),
            'taille_police_tooltips': ctk.StringVar(),
            'largeur_colonnes_auto': ctk.BooleanVar()
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
    
    def creer_section_interface(self, parent):
        """Crée la section de personnalisation de l'interface"""
        section_frame = ctk.CTkFrame(parent)
        section_frame.pack(fill="x", padx=20, pady=10)
        
        # Titre section
        titre_section = ctk.CTkLabel(
            section_frame,
            text="🖥️ PERSONNALISATION DE L'INTERFACE",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        titre_section.pack(pady=(15, 20))
        
        # Sous-titre explicatif
        info_label = ctk.CTkLabel(
            section_frame,
            text="Personnalisez la taille des polices et l'espacement pour votre confort visuel",
            font=ctk.CTkFont(size=11),
            text_color="#666666"
        )
        info_label.pack(pady=(0, 15))
        
        # Container principal avec deux colonnes
        container_frame = ctk.CTkFrame(section_frame)
        container_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Colonne de gauche - Tailles de police
        left_column = ctk.CTkFrame(container_frame)
        left_column.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Titre colonne gauche
        titre_polices = ctk.CTkLabel(
            left_column,
            text="📝 TAILLES DE POLICE",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        titre_polices.pack(pady=(10, 15))
        
        # Taille police tableau
        tableau_frame = ctk.CTkFrame(left_column)
        tableau_frame.pack(fill="x", pady=3, padx=10)
        
        tableau_label = ctk.CTkLabel(
            tableau_frame,
            text="Contenu tableaux:",
            font=ctk.CTkFont(size=11),
            width=140
        )
        tableau_label.pack(side="left", padx=5, pady=5)
        
        tableau_entry = ctk.CTkEntry(
            tableau_frame,
            textvariable=self.vars_parametres['taille_police_tableau'],
            width=60,
            placeholder_text="14"
        )
        tableau_entry.pack(side="right", padx=5, pady=5)
        
        ajouter_tooltip(tableau_label, TOOLTIPS['param_taille_police_tableau'])
        ajouter_tooltip(tableau_entry, TOOLTIPS['param_taille_police_tableau'])
        
        # Taille police en-têtes
        entetes_frame = ctk.CTkFrame(left_column)
        entetes_frame.pack(fill="x", pady=3, padx=10)
        
        entetes_label = ctk.CTkLabel(
            entetes_frame,
            text="En-têtes tableaux:",
            font=ctk.CTkFont(size=11),
            width=140
        )
        entetes_label.pack(side="left", padx=5, pady=5)
        
        entetes_entry = ctk.CTkEntry(
            entetes_frame,
            textvariable=self.vars_parametres['taille_police_entetes'],
            width=60,
            placeholder_text="16"
        )
        entetes_entry.pack(side="right", padx=5, pady=5)
        
        ajouter_tooltip(entetes_label, TOOLTIPS['param_taille_police_entetes'])
        ajouter_tooltip(entetes_entry, TOOLTIPS['param_taille_police_entetes'])
        
        # Taille police titres
        titres_frame = ctk.CTkFrame(left_column)
        titres_frame.pack(fill="x", pady=3, padx=10)
        
        titres_label = ctk.CTkLabel(
            titres_frame,
            text="Titres principaux:",
            font=ctk.CTkFont(size=11),
            width=140
        )
        titres_label.pack(side="left", padx=5, pady=5)
        
        titres_entry = ctk.CTkEntry(
            titres_frame,
            textvariable=self.vars_parametres['taille_police_titres'],
            width=60,
            placeholder_text="20"
        )
        titres_entry.pack(side="right", padx=5, pady=5)
        
        ajouter_tooltip(titres_label, TOOLTIPS['param_taille_police_titres'])
        ajouter_tooltip(titres_entry, TOOLTIPS['param_taille_police_titres'])
        
        # Taille police boutons
        boutons_frame = ctk.CTkFrame(left_column)
        boutons_frame.pack(fill="x", pady=3, padx=10)
        
        boutons_label = ctk.CTkLabel(
            boutons_frame,
            text="Boutons:",
            font=ctk.CTkFont(size=11),
            width=140
        )
        boutons_label.pack(side="left", padx=5, pady=5)
        
        boutons_entry = ctk.CTkEntry(
            boutons_frame,
            textvariable=self.vars_parametres['taille_police_boutons'],
            width=60,
            placeholder_text="12"
        )
        boutons_entry.pack(side="right", padx=5, pady=5)
        
        ajouter_tooltip(boutons_label, TOOLTIPS['param_taille_police_boutons'])
        ajouter_tooltip(boutons_entry, TOOLTIPS['param_taille_police_boutons'])
        
        # Colonne de droite - Autres paramètres
        right_column = ctk.CTkFrame(container_frame)
        right_column.pack(side="right", fill="x", expand=True, padx=(10, 0))
        
        # Titre colonne droite
        titre_autres = ctk.CTkLabel(
            right_column,
            text="⚙️ AUTRES PARAMÈTRES",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        titre_autres.pack(pady=(10, 15))
        
        # Taille police labels
        labels_frame = ctk.CTkFrame(right_column)
        labels_frame.pack(fill="x", pady=3, padx=10)
        
        labels_label = ctk.CTkLabel(
            labels_frame,
            text="Étiquettes:",
            font=ctk.CTkFont(size=11),
            width=140
        )
        labels_label.pack(side="left", padx=5, pady=5)
        
        labels_entry = ctk.CTkEntry(
            labels_frame,
            textvariable=self.vars_parametres['taille_police_labels'],
            width=60,
            placeholder_text="12"
        )
        labels_entry.pack(side="right", padx=5, pady=5)
        
        ajouter_tooltip(labels_label, TOOLTIPS['param_taille_police_labels'])
        ajouter_tooltip(labels_entry, TOOLTIPS['param_taille_police_labels'])
        
        # Taille police champs
        champs_frame = ctk.CTkFrame(right_column)
        champs_frame.pack(fill="x", pady=3, padx=10)
        
        champs_label = ctk.CTkLabel(
            champs_frame,
            text="Champs de saisie:",
            font=ctk.CTkFont(size=11),
            width=140
        )
        champs_label.pack(side="left", padx=5, pady=5)
        
        champs_entry = ctk.CTkEntry(
            champs_frame,
            textvariable=self.vars_parametres['taille_police_champs'],
            width=60,
            placeholder_text="12"
        )
        champs_entry.pack(side="right", padx=5, pady=5)
        
        ajouter_tooltip(champs_label, TOOLTIPS['param_taille_police_champs'])
        ajouter_tooltip(champs_entry, TOOLTIPS['param_taille_police_champs'])
        
        # NOUVEAU : Taille police tooltips
        tooltips_frame = ctk.CTkFrame(right_column)
        tooltips_frame.pack(fill="x", pady=3, padx=10)
        
        tooltips_label = ctk.CTkLabel(
            tooltips_frame,
            text="Tooltips:",
            font=ctk.CTkFont(size=11),
            width=140
        )
        tooltips_label.pack(side="left", padx=5, pady=5)
        
        tooltips_entry = ctk.CTkEntry(
            tooltips_frame,
            textvariable=self.vars_parametres['taille_police_tooltips'],
            width=60,
            placeholder_text="11"
        )
        tooltips_entry.pack(side="right", padx=5, pady=5)
        
        ajouter_tooltip(tooltips_label, "Taille de la police des infobulles d'aide (recommandé: 9-14)")
        ajouter_tooltip(tooltips_entry, "Taille de la police des infobulles d'aide (recommandé: 9-14)")
        
        # Hauteur lignes tableau
        hauteur_frame = ctk.CTkFrame(right_column)
        hauteur_frame.pack(fill="x", pady=3, padx=10)
        
        hauteur_label = ctk.CTkLabel(
            hauteur_frame,
            text="Hauteur lignes (px):",
            font=ctk.CTkFont(size=11),
            width=140
        )
        hauteur_label.pack(side="left", padx=5, pady=5)
        
        hauteur_entry = ctk.CTkEntry(
            hauteur_frame,
            textvariable=self.vars_parametres['hauteur_lignes_tableau'],
            width=60,
            placeholder_text="30"
        )
        hauteur_entry.pack(side="right", padx=5, pady=5)
        
        ajouter_tooltip(hauteur_label, TOOLTIPS['param_hauteur_lignes_tableau'])
        ajouter_tooltip(hauteur_entry, TOOLTIPS['param_hauteur_lignes_tableau'])
        
        # Largeur colonnes auto
        auto_width_frame = ctk.CTkFrame(right_column)
        auto_width_frame.pack(fill="x", pady=3, padx=10)
        
        auto_width_label = ctk.CTkLabel(
            auto_width_frame,
            text="Colonnes auto:",
            font=ctk.CTkFont(size=11),
            width=140
        )
        auto_width_label.pack(side="left", padx=5, pady=5)
        
        auto_width_switch = ctk.CTkSwitch(
            auto_width_frame,
            text="",
            variable=self.vars_parametres['largeur_colonnes_auto'],
            width=50
        )
        auto_width_switch.pack(side="right", padx=5, pady=5)
        
        ajouter_tooltip(auto_width_label, TOOLTIPS['param_largeur_colonnes_auto'])
        ajouter_tooltip(auto_width_switch, TOOLTIPS['param_largeur_colonnes_auto'])
        
        # Bouton test/aperçu
        test_button = ctk.CTkButton(
            section_frame,
            text="👁️ Aperçu des modifications",
            command=self.apercu_modifications,
            font=ctk.CTkFont(size=11),
            width=200,
            height=30
        )
        test_button.pack(pady=(15, 10))
        
        ajouter_tooltip(test_button, "Applique temporairement les modifications pour voir le résultat avant de sauvegarder")
    
    def charger_valeurs(self):
        """Charge les valeurs des paramètres de la journée"""
        parametres = self.journee.parametres
        
        self.vars_parametres['tarif_horaire'].set(str(parametres.get('tarif_horaire', 45.0)))
        self.vars_parametres['commission_vente'].set(str(parametres.get('commission_vente', 8.5)))
        self.vars_parametres['marge_securite'].set(str(parametres.get('marge_securite', 200.0)))
        self.vars_parametres['mode_sombre'].set(parametres.get('mode_sombre', False))
        
        # CHARGER LES NOUVEAUX PARAMÈTRES D'INTERFACE
        self.vars_parametres['hauteur_lignes_tableau'].set(str(parametres.get('hauteur_lignes_tableau', 30)))
        self.vars_parametres['taille_police_tableau'].set(str(parametres.get('taille_police_tableau', 14)))
        self.vars_parametres['taille_police_entetes'].set(str(parametres.get('taille_police_entetes', 16)))
        self.vars_parametres['taille_police_titres'].set(str(parametres.get('taille_police_titres', 20)))
        self.vars_parametres['taille_police_boutons'].set(str(parametres.get('taille_police_boutons', 12)))
        self.vars_parametres['taille_police_labels'].set(str(parametres.get('taille_police_labels', 12)))
        self.vars_parametres['taille_police_champs'].set(str(parametres.get('taille_police_champs', 12)))
        self.vars_parametres['taille_police_tooltips'].set(str(parametres.get('taille_police_tooltips', 12)))
        self.vars_parametres['largeur_colonnes_auto'].set(parametres.get('largeur_colonnes_auto', True))
    
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
            
            # RÉCUPÉRER LES NOUVEAUX PARAMÈTRES D'INTERFACE
            hauteur_lignes_tableau = int(self.vars_parametres['hauteur_lignes_tableau'].get())
            taille_police_tableau = int(self.vars_parametres['taille_police_tableau'].get())
            taille_police_entetes = int(self.vars_parametres['taille_police_entetes'].get())
            taille_police_titres = int(self.vars_parametres['taille_police_titres'].get())
            taille_police_boutons = int(self.vars_parametres['taille_police_boutons'].get())
            taille_police_labels = int(self.vars_parametres['taille_police_labels'].get())
            taille_police_champs = int(self.vars_parametres['taille_police_champs'].get())
            taille_police_tooltips = int(self.vars_parametres['taille_police_tooltips'].get())
            largeur_colonnes_auto = self.vars_parametres['largeur_colonnes_auto'].get()
            
            # Validation
            if tarif_horaire < 0 or commission_vente < 0 or marge_securite < 0:
                messagebox.showerror("❌ Erreur", "Les valeurs ne peuvent pas être négatives")
                return
            
            if commission_vente > 100:
                messagebox.showerror("❌ Erreur", "La commission ne peut pas dépasser 100%")
                return
                
            # VALIDATION DES NOUVEAUX PARAMÈTRES
            if not (15 <= hauteur_lignes_tableau <= 60):
                messagebox.showerror("❌ Erreur", "La hauteur des lignes doit être entre 15 et 60 pixels")
                return
                
            if not (8 <= taille_police_tableau <= 24):
                messagebox.showerror("❌ Erreur", "La taille de police des tableaux doit être entre 8 et 24")
                return
                
            if not (8 <= taille_police_entetes <= 28):
                messagebox.showerror("❌ Erreur", "La taille de police des en-têtes doit être entre 8 et 28")
                return
                
            if not (12 <= taille_police_titres <= 32):
                messagebox.showerror("❌ Erreur", "La taille de police des titres doit être entre 12 et 32")
                return
                
            if not (8 <= taille_police_boutons <= 20):
                messagebox.showerror("❌ Erreur", "La taille de police des boutons doit être entre 8 et 20")
                return
                
            if not (8 <= taille_police_labels <= 20):
                messagebox.showerror("❌ Erreur", "La taille de police des étiquettes doit être entre 8 et 20")
                return
                
            if not (8 <= taille_police_champs <= 20):
                messagebox.showerror("❌ Erreur", "La taille de police des champs doit être entre 8 et 20")
                return
            
            if not (8 <= taille_police_tooltips <= 20):
                messagebox.showerror("❌ Erreur", "La taille de police des tooltips doit être entre 8 et 20")
                return
            
            # Mettre à jour les paramètres de la journée
            self.journee.parametres['tarif_horaire'] = tarif_horaire
            self.journee.parametres['commission_vente'] = commission_vente
            self.journee.parametres['marge_securite'] = marge_securite
            self.journee.parametres['mode_sombre'] = mode_sombre
            
            # SAUVEGARDER LES NOUVEAUX PARAMÈTRES D'INTERFACE
            self.journee.parametres['hauteur_lignes_tableau'] = hauteur_lignes_tableau
            self.journee.parametres['taille_police_tableau'] = taille_police_tableau
            self.journee.parametres['taille_police_entetes'] = taille_police_entetes
            self.journee.parametres['taille_police_titres'] = taille_police_titres
            self.journee.parametres['taille_police_boutons'] = taille_police_boutons
            self.journee.parametres['taille_police_labels'] = taille_police_labels
            self.journee.parametres['taille_police_champs'] = taille_police_champs
            self.journee.parametres['taille_police_tooltips'] = taille_police_tooltips
            self.journee.parametres['largeur_colonnes_auto'] = largeur_colonnes_auto
            
            # Notifier le changement pour recalculer les prix max ET appliquer le style
            if self.on_parametres_changed:
                self.on_parametres_changed()
            
            messagebox.showinfo("✅ Succès", "Paramètres sauvegardés ! Interface mise à jour et prix maximums recalculés.")
            
        except ValueError:
            messagebox.showerror("❌ Erreur", "Veuillez entrer des valeurs numériques valides")
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de la sauvegarde: {e}")
    
    def apercu_modifications(self):
        """Applique temporairement les modifications pour aperçu"""
        try:
            # Récupérer les valeurs sans les sauvegarder
            hauteur_lignes_tableau = int(self.vars_parametres['hauteur_lignes_tableau'].get())
            taille_police_tableau = int(self.vars_parametres['taille_police_tableau'].get())
            taille_police_entetes = int(self.vars_parametres['taille_police_entetes'].get())
            taille_police_titres = int(self.vars_parametres['taille_police_titres'].get())
            taille_police_boutons = int(self.vars_parametres['taille_police_boutons'].get())
            taille_police_labels = int(self.vars_parametres['taille_police_labels'].get())
            taille_police_champs = int(self.vars_parametres['taille_police_champs'].get())
            taille_police_tooltips = int(self.vars_parametres['taille_police_tooltips'].get())
            
            # Validation rapide
            if not (15 <= hauteur_lignes_tableau <= 60) or \
               not (8 <= taille_police_tableau <= 24) or \
               not (8 <= taille_police_entetes <= 28) or \
               not (12 <= taille_police_titres <= 32) or \
               not (8 <= taille_police_boutons <= 20) or \
               not (8 <= taille_police_labels <= 20) or \
               not (8 <= taille_police_champs <= 20) or \
               not (8 <= taille_police_tooltips <= 20):
                messagebox.showerror("❌ Erreur", "Une ou plusieurs valeurs sont hors limites")
                return
            
            # Appliquer temporairement
            parametres_temp = self.journee.parametres.copy()
            parametres_temp['hauteur_lignes_tableau'] = hauteur_lignes_tableau
            parametres_temp['taille_police_tableau'] = taille_police_tableau
            parametres_temp['taille_police_entetes'] = taille_police_entetes
            parametres_temp['taille_police_titres'] = taille_police_titres
            parametres_temp['taille_police_boutons'] = taille_police_boutons
            parametres_temp['taille_police_labels'] = taille_police_labels
            parametres_temp['taille_police_champs'] = taille_police_champs
            parametres_temp['taille_police_tooltips'] = taille_police_tooltips
            
            # Faire appliquer temporairement via le callback
            if self.on_parametres_changed:
                self.on_parametres_changed(parametres_temp)
            
            messagebox.showinfo("👁️ Aperçu", "Modifications appliquées temporairement.\nUtilisez 'Sauvegarder' pour conserver les changements.")
            
        except ValueError:
            messagebox.showerror("❌ Erreur", "Veuillez entrer des valeurs numériques valides")
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de l'aperçu: {e}")
    
    def reinitialiser_parametres(self):
        """Remet les paramètres aux valeurs par défaut"""
        if messagebox.askyesno("Confirmation", "Remettre tous les paramètres aux valeurs par défaut ?"):
            # Valeurs par défaut
            self.journee.parametres = {
                'tarif_horaire': 45.0,
                'commission_vente': 8.5,
                'marge_securite': 200.0,
                'mode_sombre': False,
                
                # VALEURS PAR DÉFAUT POUR L'INTERFACE
                'hauteur_lignes_tableau': 30,
                'taille_police_tableau': 14,
                'taille_police_entetes': 16,
                'taille_police_titres': 20,
                'taille_police_boutons': 12,
                'taille_police_labels': 12,
                'taille_police_champs': 12,
                'taille_police_tooltips': 11,
                'largeur_colonnes_auto': True
            }
            
            # Recharger l'affichage
            self.charger_valeurs()
            
            # Notifier le changement
            if self.on_parametres_changed:
                self.on_parametres_changed()
            
            messagebox.showinfo("✅ Succès", "Paramètres réinitialisés !")
    
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
    
    def afficher_aide(self):
        """Affiche l'aide détaillée"""
        aide_text = """🔧 AIDE - PARAMÈTRES DE L'ENCHÈRE

💰 TARIF HORAIRE
Votre tarif horaire pour calculer le coût de la main d'œuvre.
Utilisé dans le calcul : Main d'Œuvre = Temps × Tarif Horaire

💸 COMMISSION D'ENCHÈRE
Pourcentage prélevé par la maison d'enchères lors de l'ACHAT.
• Dans Prix Max : calculée sur Prix Revente (estimation)
• Dans Marge Finale : calculée sur Prix d'Achat (réel)

🛡️ MARGE DE SÉCURITÉ  
Marge fixe déduite UNIQUEMENT du prix maximum pour éviter les pertes.
Elle N'EST PAS déduite de la marge finale (car c'est juste une sécurité).

🎨 MODE SOMBRE
Active/désactive le thème sombre de l'interface.

📊 CALCULS DÉTAILLÉS

🔍 PRIX MAXIMUM (Phase repérage) :
Prix Max = Prix Revente - (Coût Réparations + Main d'Œuvre) - Commission% × Prix Revente - Marge Sécurité

💰 MARGE FINALE (Véhicules vendus) :
Marge = Prix Vente Final - (Prix Achat + Coût Réparations + Main d'Œuvre + Commission% × Prix Achat)

⚠️ CES PARAMÈTRES SONT SPÉCIFIQUES À CETTE JOURNÉE D'ENCHÈRE
Chaque journée a ses propres paramètres et ne sont pas partagés."""
        
        messagebox.showinfo("🔧 Aide - Paramètres", aide_text)
    
    def actualiser(self):
        """Met à jour l'affichage (si nécessaire)"""
        self.charger_valeurs() 