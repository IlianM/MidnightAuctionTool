#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Onglet de repérage des véhicules - CustomTkinter
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os

# Imports pour l'export PDF
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from config.settings import AppSettings
from utils.tooltips import ajouter_tooltip, TOOLTIPS, set_tooltip_font_size, ajouter_tooltips_colonnes_tableau
from utils.dialogs import demander_prix_achat, afficher_info_vehicule
from models.vehicule import Vehicule

class ReperageTab:
    """Onglet principal de repérage des véhicules avec CustomTkinter"""
    
    def __init__(self, parent, settings: AppSettings, data_adapter, 
                 style_manager, on_data_changed=None):
        self.parent = parent
        self.settings = settings
        self.data_adapter = data_adapter  # Nouveau nom pour le gestionnaire de données
        self.style_manager = style_manager
        self.on_data_changed = on_data_changed
        
        # Variables d'interface
        self.vars_saisie = {}
        self.tree_reperage = None
        self.edit_entry = None  # Widget d'édition temporaire
        self.editing_item = None
        self.editing_column = None
        self.column_tooltips = None  # NOUVEAU : Gestionnaire de tooltips contextuels
        
        # Variables pour le tri
        self.tri_actuel = {'colonne': None, 'sens': 'asc'}  # 'asc' ou 'desc'
        
        # Variables pour l'actualisation automatique
        self.auto_refresh_enabled = True
        self.auto_refresh_interval = 500
        self.last_data_hash = None
        
        # Créer l'interface directement dans le parent (onglet du TabView)
        self.creer_interface()
        
        # Démarrer l'actualisation automatique
        self.demarrer_auto_refresh()
    
    def creer_interface(self):
        """Crée l'interface complète de l'onglet repérage avec CustomTkinter"""
        # Créer un scrollable frame directement dans le parent
        self.scrollable_frame = ctk.CTkScrollableFrame(self.parent)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre
        titre = ctk.CTkLabel(
            self.scrollable_frame,
            text="🔍 REPÉRAGE DE VÉHICULES",
            font=self.get_font_from_settings('titres')
        )
        titre.pack(pady=(0, 20))
        
        # Saisie rapide
        self.creer_section_saisie(self.scrollable_frame)
        
        # Barre de recherche (juste au-dessus du tableau)
        self.creer_barre_recherche(self.scrollable_frame)
        
        # Tableau véhicules
        self.creer_section_tableau(self.scrollable_frame)
        
        # Boutons actions
        self.creer_section_actions(self.scrollable_frame)
        
        # Charger les données initiales
        self.actualiser()
    
    def creer_barre_recherche(self, parent):
        """Crée la barre de recherche"""
        search_frame = ctk.CTkFrame(parent)
        search_frame.pack(fill="x", pady=(0, 20))
        
        # Titre de la section
        search_title = ctk.CTkLabel(
            search_frame,
            text="🔎 RECHERCHE",
            font=self.get_font_from_settings('titres')
        )
        search_title.pack(pady=(15, 10))
        
        # Frame pour la barre de recherche
        search_input_frame = ctk.CTkFrame(search_frame)
        search_input_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Label
        search_label = ctk.CTkLabel(
            search_input_frame,
            text="Rechercher:",
            font=self.get_font_from_settings('labels'),
            width=100
        )
        search_label.pack(side="left", padx=10, pady=10)
        
        # Variable de recherche
        self.var_recherche = ctk.StringVar()
        self.var_recherche.trace('w', self.on_recherche_change)
        
        # Champ de recherche
        self.entry_recherche = ctk.CTkEntry(
            search_input_frame,
            textvariable=self.var_recherche,
            placeholder_text="N° lot, marque ou modèle...",
            font=self.get_font_from_settings('champs'),
            width=300
        )
        self.entry_recherche.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        
        # Bouton effacer
        clear_button = ctk.CTkButton(
            search_input_frame,
            text="🗑️ Effacer",
            command=self.effacer_recherche,
            font=self.get_font_from_settings('boutons'),
            width=100
        )
        clear_button.pack(side="right", padx=10, pady=10)
        
        # Ajouter tooltips
        ajouter_tooltip(self.entry_recherche, TOOLTIPS['recherche'])
        ajouter_tooltip(clear_button, TOOLTIPS['btn_effacer_recherche'])
    
    def creer_section_saisie(self, parent):
        """Crée la section de saisie rapide avec les nouveaux champs"""
        frame_saisie = ctk.CTkFrame(parent)
        frame_saisie.pack(fill="x", pady=(0, 20))
        
        # Titre section
        titre_saisie = ctk.CTkLabel(
            frame_saisie,
            text="⚡ SAISIE RAPIDE VÉHICULE",
            font=self.get_font_from_settings('titres')
        )
        titre_saisie.pack(pady=(15, 20))
        
        # Initialiser les variables (MISES À JOUR avec nouveaux champs)
        self.vars_saisie = {
            'lot': ctk.StringVar(),
            'marque': ctk.StringVar(),
            'modele': ctk.StringVar(),
            'annee': ctk.StringVar(),
            'kilometrage': ctk.StringVar(),
            'motorisation': ctk.StringVar(),  # NOUVEAU
            'prix_revente': ctk.StringVar(),
            'cout_reparations': ctk.StringVar(),
            'temps_reparations': ctk.StringVar(),
            'chose_a_faire': ctk.StringVar(),
            'champ_libre': ctk.StringVar(),  # NOUVEAU
            'reserve_professionnels': ctk.BooleanVar(),  # NOUVEAU
            'couleur': ctk.StringVar(value='turquoise')  # NOUVEAU
        }
        
        # Grille de saisie avec 4 lignes maintenant
        grid_frame = ctk.CTkFrame(frame_saisie)
        grid_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Ligne 1: Infos de base
        row1 = ctk.CTkFrame(grid_frame)
        row1.pack(fill="x", pady=5)
        
        # Lot
        lot_label = ctk.CTkLabel(row1, text="N° LOT:", width=80, font=self.get_font_from_settings('labels'))
        lot_label.pack(side="left", padx=5)
        lot_entry = ctk.CTkEntry(row1, textvariable=self.vars_saisie['lot'], width=100, font=self.get_font_from_settings('champs'))
        lot_entry.pack(side="left", padx=5)
        ajouter_tooltip(lot_label, TOOLTIPS['lot'])
        ajouter_tooltip(lot_entry, TOOLTIPS['lot'])
        
        # Marque
        marque_label = ctk.CTkLabel(row1, text="MARQUE:", width=80, font=self.get_font_from_settings('labels'))
        marque_label.pack(side="left", padx=5)
        marque_entry = ctk.CTkEntry(row1, textvariable=self.vars_saisie['marque'], width=120, font=self.get_font_from_settings('champs'))
        marque_entry.pack(side="left", padx=5)
        ajouter_tooltip(marque_label, TOOLTIPS['marque'])
        ajouter_tooltip(marque_entry, TOOLTIPS['marque'])
        
        # Modèle
        modele_label = ctk.CTkLabel(row1, text="MODÈLE:", width=80, font=self.get_font_from_settings('labels'))
        modele_label.pack(side="left", padx=5)
        modele_entry = ctk.CTkEntry(row1, textvariable=self.vars_saisie['modele'], width=120, font=self.get_font_from_settings('champs'))
        modele_entry.pack(side="left", padx=5)
        ajouter_tooltip(modele_label, TOOLTIPS['modele'])
        ajouter_tooltip(modele_entry, TOOLTIPS['modele'])
        
        # Année
        annee_label = ctk.CTkLabel(row1, text="ANNÉE:", width=80, font=self.get_font_from_settings('labels'))
        annee_label.pack(side="left", padx=5)
        annee_entry = ctk.CTkEntry(row1, textvariable=self.vars_saisie['annee'], width=80, font=self.get_font_from_settings('champs'))
        annee_entry.pack(side="left", padx=5)
        ajouter_tooltip(annee_label, TOOLTIPS['annee'])
        ajouter_tooltip(annee_entry, TOOLTIPS['annee'])
        
        # Ligne 2: Kilométrage et motorisation
        row2 = ctk.CTkFrame(grid_frame)
        row2.pack(fill="x", pady=5)
        
        # Kilométrage avec formatage automatique en temps réel
        km_label = ctk.CTkLabel(row2, text="KM:", width=80, font=self.get_font_from_settings('labels'))
        km_label.pack(side="left", padx=5)
        km_entry = ctk.CTkEntry(row2, textvariable=self.vars_saisie['kilometrage'], width=100, font=self.get_font_from_settings('champs'))
        km_entry.pack(side="left", padx=5)
        
        # Bind pour formatage automatique du kilométrage
        def formater_kilometrage_temps_reel(*args):
            """Formate le kilométrage en temps réel pendant la saisie"""
            valeur = self.vars_saisie['kilometrage'].get()
            
            # Éviter les boucles infinies
            if hasattr(formater_kilometrage_temps_reel, 'en_cours'):
                return
            formater_kilometrage_temps_reel.en_cours = True
            
            try:
                # Garder la position du curseur
                position_curseur = km_entry.index(tk.INSERT)
                
                # Enlever tout ce qui n'est pas un chiffre pour le calcul
                chiffres_seulement = ''.join(filter(str.isdigit, valeur))
                
                if chiffres_seulement and not valeur.endswith('km'):
                    km = int(chiffres_seulement)
                    ancienne_valeur = valeur
                    
                    # Appliquer le formatage selon la taille
                    if 1 <= km <= 999:  # Probablement en milliers
                        nouvelle_valeur = f"{km},000km"
                    elif km >= 1000:  # Valeur exacte
                        if km >= 100000:
                            # Formater avec espaces pour les gros nombres
                            nouvelle_valeur = f"{km:,}km".replace(',', ' ')
                        else:
                            nouvelle_valeur = f"{km}km"
                    else:
                        nouvelle_valeur = valeur
                    
                    # Mettre à jour seulement si différent pour éviter boucles
                    if nouvelle_valeur != ancienne_valeur:
                        self.vars_saisie['kilometrage'].set(nouvelle_valeur)
                        # Restaurer la position du curseur si possible
                        try:
                            km_entry.icursor(min(position_curseur, len(nouvelle_valeur)))
                        except:
                            pass
            except:
                pass
            finally:
                if hasattr(formater_kilometrage_temps_reel, 'en_cours'):
                    del formater_kilometrage_temps_reel.en_cours
        
        # Bind pour formatage en temps réel
        self.vars_saisie['kilometrage'].trace('w', formater_kilometrage_temps_reel)
        
        ajouter_tooltip(km_label, TOOLTIPS['kilometrage'])
        ajouter_tooltip(km_entry, "Kilométrage du véhicule. Tapez juste le nombre (ex: 330 devient automatiquement 330,000km en temps réel)")
        
        # NOUVEAU : Motorisation
        motorisation_label = ctk.CTkLabel(row2, text="MOTORISATION:", width=120, font=self.get_font_from_settings('labels'))
        motorisation_label.pack(side="left", padx=5)
        motorisation_entry = ctk.CTkEntry(row2, textvariable=self.vars_saisie['motorisation'], width=150, font=self.get_font_from_settings('champs'))
        motorisation_entry.pack(side="left", padx=5)
        ajouter_tooltip(motorisation_label, "Type de motorisation du véhicule (ex: Diesel, Essence, Hybride)")
        ajouter_tooltip(motorisation_entry, "Type de motorisation du véhicule (ex: Diesel, Essence, Hybride)")
        
        # NOUVEAU : Couleur
        couleur_label = ctk.CTkLabel(row2, text="COULEUR:", width=80, font=self.get_font_from_settings('labels'))
        couleur_label.pack(side="left", padx=5)
        couleur_combo = ctk.CTkComboBox(
            row2, 
            variable=self.vars_saisie['couleur'],
            values=['turquoise', 'vert', 'orange', 'rouge'],
            width=120,
            font=self.get_font_from_settings('champs'),
            state="readonly"
        )
        couleur_combo.pack(side="left", padx=5)
        ajouter_tooltip(couleur_label, "Couleur d'affichage de la ligne dans le tableau")
        ajouter_tooltip(couleur_combo, "Couleur d'affichage de la ligne dans le tableau")
        
        # Ligne 3: Prix et coûts
        row3 = ctk.CTkFrame(grid_frame)
        row3.pack(fill="x", pady=5)
        
        # Prix revente
        prix_rev_label = ctk.CTkLabel(row3, text="PRIX REVENTE:", width=100, font=self.get_font_from_settings('labels'))
        prix_rev_label.pack(side="left", padx=5)
        prix_rev_entry = ctk.CTkEntry(row3, textvariable=self.vars_saisie['prix_revente'], width=100, font=self.get_font_from_settings('champs'))
        prix_rev_entry.pack(side="left", padx=5)
        ajouter_tooltip(prix_rev_label, TOOLTIPS['prix_revente'])
        ajouter_tooltip(prix_rev_entry, TOOLTIPS['prix_revente'])
        
        # Coût réparations
        cout_rep_label = ctk.CTkLabel(row3, text="COÛT RÉPAR:", width=100, font=self.get_font_from_settings('labels'))
        cout_rep_label.pack(side="left", padx=5)
        cout_rep_entry = ctk.CTkEntry(row3, textvariable=self.vars_saisie['cout_reparations'], width=100, font=self.get_font_from_settings('champs'))
        cout_rep_entry.pack(side="left", padx=5)
        ajouter_tooltip(cout_rep_label, TOOLTIPS['cout_reparations'])
        ajouter_tooltip(cout_rep_entry, TOOLTIPS['cout_reparations'])
        
        # Temps réparations
        temps_rep_label = ctk.CTkLabel(row3, text="TEMPS (h):", width=80, font=self.get_font_from_settings('labels'))
        temps_rep_label.pack(side="left", padx=5)
        temps_rep_entry = ctk.CTkEntry(row3, textvariable=self.vars_saisie['temps_reparations'], width=80, font=self.get_font_from_settings('champs'))
        temps_rep_entry.pack(side="left", padx=5)
        ajouter_tooltip(temps_rep_label, TOOLTIPS['temps_reparations'])
        ajouter_tooltip(temps_rep_entry, TOOLTIPS['temps_reparations'])
        
        # NOUVEAU : Réservé aux professionnels
        pro_check = ctk.CTkCheckBox(
            row3,
            text="Réservé aux pros",
            variable=self.vars_saisie['reserve_professionnels'],
            font=self.get_font_from_settings('labels')
        )
        pro_check.pack(side="left", padx=15)
        ajouter_tooltip(pro_check, "Cochez si ce véhicule est réservé aux professionnels uniquement")
        
        # Ligne 4: Descriptions
        row4 = ctk.CTkFrame(grid_frame)
        row4.pack(fill="x", pady=5)
        
        # Description des réparations
        desc_label = ctk.CTkLabel(row4, text="DESCRIPTION RÉPAR:", width=140, font=self.get_font_from_settings('labels'))
        desc_label.pack(side="left", padx=5)
        desc_entry = ctk.CTkEntry(row4, textvariable=self.vars_saisie['chose_a_faire'], width=300, font=self.get_font_from_settings('champs'))
        desc_entry.pack(side="left", padx=5, fill="x", expand=True)
        ajouter_tooltip(desc_label, "Description détaillée des réparations à effectuer sur le véhicule")
        ajouter_tooltip(desc_entry, "Description détaillée des réparations à effectuer sur le véhicule")
        
        # Ligne 5: Champ libre
        row5 = ctk.CTkFrame(grid_frame)
        row5.pack(fill="x", pady=5)
        
        # NOUVEAU : Champ libre
        libre_label = ctk.CTkLabel(row5, text="CHAMP LIBRE:", width=140, font=self.get_font_from_settings('labels'))
        libre_label.pack(side="left", padx=5)
        libre_entry = ctk.CTkEntry(row5, textvariable=self.vars_saisie['champ_libre'], width=400, font=self.get_font_from_settings('champs'))
        libre_entry.pack(side="left", padx=5, fill="x", expand=True)
        ajouter_tooltip(libre_label, "Champ libre pour noter des informations supplémentaires")
        ajouter_tooltip(libre_entry, "Champ libre pour noter des informations supplémentaires")
        
        # Boutons de saisie
        buttons_frame = ctk.CTkFrame(frame_saisie)
        buttons_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        add_button = ctk.CTkButton(
            buttons_frame,
            text="➕ AJOUTER VÉHICULE",
            command=self.ajouter_vehicule,
            font=self.get_font_from_settings('boutons')
        )
        add_button.pack(side="left", padx=10, pady=10)
        ajouter_tooltip(add_button, TOOLTIPS['btn_ajouter'])
        
        clear_button = ctk.CTkButton(
            buttons_frame,
            text="🗑️ VIDER",
            command=self.vider_champs,
            font=self.get_font_from_settings('boutons')
        )
        clear_button.pack(side="left", padx=10, pady=10)
        ajouter_tooltip(clear_button, TOOLTIPS['btn_vider'])
        
        # NOUVEAU : Boutons de couleur
        color_label = ctk.CTkLabel(
            buttons_frame,
            text="🎨 COULEURS:",
            font=self.get_font_from_settings('labels')
        )
        color_label.pack(side="left", padx=(30, 5), pady=10)
        
        # Bouton turquoise
        btn_turquoise = ctk.CTkButton(
            buttons_frame,
            text="🟢",
            command=lambda: self.changer_couleur_selection("turquoise"),
            font=ctk.CTkFont(size=16),
            width=40,
            height=30,
            fg_color="#1ABC9C",
            hover_color="#16A085"
        )
        btn_turquoise.pack(side="left", padx=2, pady=10)
        ajouter_tooltip(btn_turquoise, "Changer la couleur du véhicule sélectionné en turquoise")
        
        # Bouton vert
        btn_vert = ctk.CTkButton(
            buttons_frame,
            text="🟢",
            command=lambda: self.changer_couleur_selection("vert"),
            font=ctk.CTkFont(size=16),
            width=40,
            height=30,
            fg_color="#2ECC71",
            hover_color="#27AE60"
        )
        btn_vert.pack(side="left", padx=2, pady=10)
        ajouter_tooltip(btn_vert, "Changer la couleur du véhicule sélectionné en vert")
        
        # Bouton orange
        btn_orange = ctk.CTkButton(
            buttons_frame,
            text="🟠",
            command=lambda: self.changer_couleur_selection("orange"),
            font=ctk.CTkFont(size=16),
            width=40,
            height=30,
            fg_color="#F39C12",
            hover_color="#E67E22"
        )
        btn_orange.pack(side="left", padx=2, pady=10)
        ajouter_tooltip(btn_orange, "Changer la couleur du véhicule sélectionné en orange")
        
        # Bouton rouge
        btn_rouge = ctk.CTkButton(
            buttons_frame,
            text="🔴",
            command=lambda: self.changer_couleur_selection("rouge"),
            font=ctk.CTkFont(size=16),
            width=40,
            height=30,
            fg_color="#E74C3C",
            hover_color="#C0392B"
        )
        btn_rouge.pack(side="left", padx=2, pady=10)
        ajouter_tooltip(btn_rouge, "Changer la couleur du véhicule sélectionné en rouge")
    
    def creer_section_tableau(self, parent):
        """Crée la section tableau avec les nouvelles colonnes et tri"""
        tableau_frame = ctk.CTkFrame(parent)
        tableau_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Titre tableau
        titre_tableau = ctk.CTkLabel(
            tableau_frame,
            text="📋 VÉHICULES EN REPÉRAGE",
            font=self.get_font_from_settings('titres')
        )
        titre_tableau.pack(pady=(15, 20))
        
        # Container pour le tableau avec hauteur minimale
        container = ctk.CTkFrame(tableau_frame)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        container.configure(height=250)  # Hauteur minimale de 250px
        
        # Tableau (MODIFIÉ : ajout nouvelles colonnes)
        columns = ("lot", "marque", "modele", "annee", "kilometrage", "motorisation", "prix_revente", "cout_reparations", "temps_reparations", "description_reparations", "prix_max", "prix_achat", "marge", "statut", "champ_libre", "reserve_pro", "couleur")
        self.tree_reperage = ttk.Treeview(container, columns=columns, show="headings", height=8)
        
        # Configuration du style pour utiliser les paramètres de la journée
        self.configurer_style_tableau()
        
        # Configuration des colonnes (MODIFIÉE avec nouvelles colonnes)
        headings = {
            "lot": "LOT ↕",
            "marque": "MARQUE ↕",
            "modele": "MODÈLE ↕", 
            "annee": "ANNÉE ↕",
            "kilometrage": "KM ↕",
            "motorisation": "MOTORISATION ↕",  # NOUVEAU
            "prix_revente": "PRIX REVENTE ↕",
            "cout_reparations": "COÛT RÉPAR ↕",
            "temps_reparations": "TEMPS (h) ↕",
            "description_reparations": "DESCRIPTION RÉPAR ↕",
            "prix_max": "PRIX MAX",  # Pas de tri (calculé)
            "prix_achat": "PRIX ACHAT ↕",
            "marge": "ÉCART BUDGET",  # MODIFIÉ - Pas de tri (calculé)
            "statut": "STATUT",  # Pas de tri (automatique)
            "champ_libre": "CHAMP LIBRE ↕",  # NOUVEAU
            "reserve_pro": "RÉSERVÉ PRO ↕",  # NOUVEAU
            "couleur": "COULEUR ↕"  # NOUVEAU
        }
        
        for col, heading in headings.items():
            self.tree_reperage.heading(col, text=heading)
            
            # Ajouter le callback de tri pour les colonnes avec ↕
            if "↕" in heading:
                self.tree_reperage.heading(col, command=lambda c=col: self.trier_par_colonne(c))
            
            # Ajuster les largeurs selon le contenu
            if self.get_param_from_journee('largeur_colonnes_auto', True):
                if col in ["lot", "annee", "temps_reparations"]:
                    self.tree_reperage.column(col, width=80, anchor="center", minwidth=60)
                elif col in ["kilometrage", "reserve_pro", "couleur"]:
                    self.tree_reperage.column(col, width=100, anchor="center", minwidth=80)
                elif col in ["prix_revente", "cout_reparations", "prix_max", "prix_achat"]:
                    self.tree_reperage.column(col, width=110, anchor="center", minwidth=90)
                elif col == "marge":  # NOUVEAU
                    self.tree_reperage.column(col, width=130, anchor="center", minwidth=100)
                elif col == "statut":
                    self.tree_reperage.column(col, width=100, anchor="center", minwidth=80)
                elif col in ["description_reparations", "champ_libre"]:
                    self.tree_reperage.column(col, width=180, anchor="w", minwidth=120)
                elif col == "motorisation":
                    self.tree_reperage.column(col, width=120, anchor="center", minwidth=100)
                else:
                    self.tree_reperage.column(col, width=130, anchor="w", minwidth=100)
            else:
                # Tailles fixes traditionnelles
                if col in ["lot", "annee", "temps_reparations"]:
                    self.tree_reperage.column(col, width=80, anchor="center")
                elif col in ["kilometrage", "reserve_pro", "couleur"]:
                    self.tree_reperage.column(col, width=100, anchor="center")
                elif col in ["prix_revente", "cout_reparations", "prix_max", "prix_achat"]:
                    self.tree_reperage.column(col, width=100, anchor="center")
                elif col == "marge":  # NOUVEAU
                    self.tree_reperage.column(col, width=120, anchor="center")
                elif col == "statut":
                    self.tree_reperage.column(col, width=100, anchor="center")
                elif col in ["description_reparations", "champ_libre"]:
                    self.tree_reperage.column(col, width=160, anchor="w")
                elif col == "motorisation":
                    self.tree_reperage.column(col, width=120, anchor="center")
                else:
                    self.tree_reperage.column(col, width=120, anchor="w")
        
        # Configuration des tags de couleur (MODIFIÉS selon nouvelles couleurs utilisateur)
        self.tree_reperage.tag_configure('couleur_turquoise', background='#1ABC9C', foreground='white')
        self.tree_reperage.tag_configure('couleur_vert', background='#2ECC71', foreground='white')
        self.tree_reperage.tag_configure('couleur_orange', background='#F39C12', foreground='white')
        self.tree_reperage.tag_configure('couleur_rouge', background='#E74C3C', foreground='white')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree_reperage.yview)
        h_scrollbar = ttk.Scrollbar(container, orient="horizontal", command=self.tree_reperage.xview)
        
        self.tree_reperage.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Placement
        self.tree_reperage.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configuration du grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # Bind pour édition au double-clic (MODIFIÉ pour gestion spéciale du lot)
        self.tree_reperage.bind("<Double-1>", self.on_double_click)
        
        # Initialiser les indicateurs visuels de tri
        self.mettre_a_jour_indicateurs_tri()
        
        # NOUVEAU : Initialiser les tooltips contextuels par colonne avec formules
        self.column_tooltips = ajouter_tooltips_colonnes_tableau(self.tree_reperage, self.data_adapter)
    
    def trier_par_colonne(self, colonne):
        """Trie le tableau par la colonne sélectionnée"""
        # Déterminer le sens du tri
        if self.tri_actuel['colonne'] == colonne:
            # Inverser le sens si on clique sur la même colonne
            self.tri_actuel['sens'] = 'desc' if self.tri_actuel['sens'] == 'asc' else 'asc'
        else:
            # Nouveau tri par défaut en ascendant
            self.tri_actuel['colonne'] = colonne
            self.tri_actuel['sens'] = 'asc'
        
        # Mettre à jour les indicateurs visuels dans les en-têtes
        self.mettre_a_jour_indicateurs_tri()
        
        # Actualiser l'affichage avec le tri
        self.actualiser()
    
    def mettre_a_jour_indicateurs_tri(self):
        """Met à jour les indicateurs visuels de tri dans les en-têtes"""
        # Mapping des en-têtes avec leurs indicateurs
        headings_base = {
            "lot": "LOT",
            "marque": "MARQUE",
            "modele": "MODÈLE", 
            "annee": "ANNÉE",
            "kilometrage": "KM",
            "motorisation": "MOTORISATION",
            "prix_revente": "PRIX REVENTE",
            "cout_reparations": "COÛT RÉPAR",
            "temps_reparations": "TEMPS (h)",
            "description_reparations": "DESCRIPTION RÉPAR",
            "prix_max": "PRIX MAX",  # Pas de tri
            "prix_achat": "PRIX ACHAT",
            "marge": "ÉCART BUDGET",  # Pas de tri
            "statut": "STATUT",  # Pas de tri
            "champ_libre": "CHAMP LIBRE",
            "reserve_pro": "RÉSERVÉ PRO"
        }
        
        # Colonnes non triables
        colonnes_non_triables = ["prix_max", "marge", "statut"]
        
        for col, heading_base in headings_base.items():
            if col in colonnes_non_triables:
                # Pas d'indicateur pour ces colonnes
                self.tree_reperage.heading(col, text=heading_base)
            else:
                # Ajouter l'indicateur approprié
                if self.tri_actuel['colonne'] == col:
                    if self.tri_actuel['sens'] == 'asc':
                        indicateur = " ↑"
                    else:
                        indicateur = " ↓"
                else:
                    indicateur = " ↕"
                
                self.tree_reperage.heading(col, text=heading_base + indicateur)
    
    def appliquer_tri(self, vehicules):
        """Applique le tri sur la liste de véhicules"""
        if not self.tri_actuel['colonne']:
            return vehicules
        
        colonne = self.tri_actuel['colonne']
        sens_inverse = self.tri_actuel['sens'] == 'desc'
        
        # Mapper les noms de colonnes vers les attributs du véhicule
        attribut_map = {
            'lot': 'lot',
            'marque': 'marque',
            'modele': 'modele',
            'annee': 'annee',
            'kilometrage': 'kilometrage',
            'motorisation': 'motorisation',
            'prix_revente': 'prix_revente',
            'cout_reparations': 'cout_reparations',
            'temps_reparations': 'temps_reparations',
            'description_reparations': 'chose_a_faire',
            'prix_achat': 'prix_achat',
            'champ_libre': 'champ_libre',
            'reserve_pro': 'reserve_professionnels',
            'couleur': 'couleur'
        }
        
        attribut = attribut_map.get(colonne)
        if not attribut:
            return vehicules
        
        def get_sort_key(vehicule):
            """Fonction pour récupérer la clé de tri améliorée"""
            try:
                valeur = getattr(vehicule, attribut, '')
                
                # Traitement spécial selon le type de donnée
                if colonne in ['prix_revente', 'cout_reparations', 'temps_reparations', 'prix_achat']:
                    # Valeurs numériques - nettoyage amélioré
                    if not valeur or str(valeur).strip() == '':
                        return 0.0
                    try:
                        # Nettoyer les caractères non numériques
                        valeur_nettoyee = str(valeur).replace('€', '').replace(' ', '').replace(',', '.')
                        # Garder seulement les chiffres et le point décimal
                        valeur_numerique = ''
                        point_trouve = False
                        for char in valeur_nettoyee:
                            if char.isdigit():
                                valeur_numerique += char
                            elif char == '.' and not point_trouve:
                                valeur_numerique += char
                                point_trouve = True
                        
                        return float(valeur_numerique) if valeur_numerique else 0.0
                    except (ValueError, TypeError):
                        return 0.0
                        
                elif colonne == 'annee':
                    # Années - gestion améliorée
                    if not valeur or str(valeur).strip() == '':
                        return 0
                    try:
                        # Extraire seulement les chiffres
                        annee_str = ''.join(c for c in str(valeur) if c.isdigit())
                        return int(annee_str) if annee_str else 0
                    except (ValueError, TypeError):
                        return 0
                        
                elif colonne == 'kilometrage':
                    # Kilométrage - traitement spécial
                    if not valeur or str(valeur).strip() == '':
                        return 0
                    try:
                        # Nettoyer et extraire le nombre
                        km_str = str(valeur).replace(' ', '').replace(',', '').replace('.', '')
                        km_str = ''.join(c for c in km_str if c.isdigit())
                        return int(km_str) if km_str else 0
                    except (ValueError, TypeError):
                        return 0
                        
                elif colonne == 'reserve_pro':
                    # Booléen - conversion explicite
                    try:
                        return bool(vehicule.reserve_professionnels)
                    except:
                        return False
                        
                elif colonne == 'lot':
                    # Numéro de lot - tri intelligent
                    if not valeur or str(valeur).strip() == '':
                        return ('', 0)  # Tuple pour tri : chaîne vide + nombre 0
                    
                    lot_str = str(valeur).strip()
                    
                    # Essayer d'extraire un nombre du lot
                    import re
                    match = re.search(r'(\d+)', lot_str)
                    if match:
                        numero = int(match.group(1))
                        # Retourner un tuple (partie alphabétique, numéro) pour tri naturel
                        partie_alpha = lot_str[:match.start()].lower()
                        return (partie_alpha, numero)
                    else:
                        # Pas de nombre trouvé, tri alphabétique
                        return (lot_str.lower(), 0)
                        
                else:
                    # Texte standard (marque, modèle, etc.) - insensible à la casse
                    if not valeur:
                        return ''
                    return str(valeur).lower().strip()
                    
            except Exception as e:
                # En cas d'erreur, retourner une valeur neutre selon le type
                print(f"⚠️ Erreur tri colonne {colonne}: {e}")
                if colonne in ['prix_revente', 'cout_reparations', 'temps_reparations', 'prix_achat']:
                    return 0.0
                elif colonne in ['annee', 'kilometrage']:
                    return 0
                elif colonne == 'reserve_pro':
                    return False
                elif colonne == 'lot':
                    return ('', 0)
                else:
                    return ''
        
        try:
            return sorted(vehicules, key=get_sort_key, reverse=sens_inverse)
        except Exception as e:
            print(f"❌ Erreur lors du tri: {e}")
            return vehicules  # Retourner la liste originale en cas d'erreur
    
    def configurer_style_tableau(self):
        """Configure le style du tableau selon les paramètres de la journée"""
        style = ttk.Style()
        
        # Récupérer les tailles depuis les paramètres de la journée
        taille_contenu = self.get_param_from_journee('taille_police_tableau', 14)
        taille_entetes = self.get_param_from_journee('taille_police_entetes', 16) 
        hauteur_lignes = self.get_param_from_journee('hauteur_lignes_tableau', 30)
        
        # Configurer les styles
        style.configure("Treeview", 
                       font=('Segoe UI', taille_contenu), 
                       rowheight=hauteur_lignes)
        style.configure("Treeview.Heading", 
                       font=('Segoe UI', taille_entetes, 'bold'))
    
    def get_param_from_journee(self, param_name, default_value):
        """Récupère un paramètre depuis la journée ou fallback vers les settings puis valeur par défaut"""
        if hasattr(self.data_adapter, 'journee') and self.data_adapter.journee:
            return self.data_adapter.journee.parametres.get(param_name, default_value)
        return self.settings.parametres.get(param_name, default_value)
    
    def get_font_from_settings(self, element_type):
        """Retourne une police CTkFont configurée selon les paramètres de la journée"""
        if hasattr(self.data_adapter, 'journee') and self.data_adapter.journee:
            # Utiliser les paramètres de la journée
            taille = self.data_adapter.journee.parametres.get(f'taille_police_{element_type}', 12)
        else:
            # Fallback vers les settings
            taille = self.settings.parametres.get(f'taille_police_{element_type}', 12)
        
        if element_type in ['titres', 'entetes', 'boutons', 'labels']:
            return ctk.CTkFont(size=taille, weight="bold")
        else:
            return ctk.CTkFont(size=taille)
    
    def appliquer_parametres_interface(self, parametres_temp=None):
        """Applique les paramètres d'interface (pour aperçu ou sauvegarde définitive)"""
        # Utiliser les paramètres temporaires ou ceux de la journée
        if parametres_temp:
            params = parametres_temp
        elif hasattr(self.data_adapter, 'journee') and self.data_adapter.journee:
            params = self.data_adapter.journee.parametres
        else:
            return  # Pas de paramètres disponibles
        
        # Appliquer la taille de police des tooltips
        taille_tooltips = params.get('taille_police_tooltips', 11)
        set_tooltip_font_size(taille_tooltips)
        
        # Mettre à jour les tooltips contextuels avec les nouveaux paramètres
        self.mettre_a_jour_tooltips_contextuels()
        
        # Reconfigurer le style du tableau
        if hasattr(self, 'tree_reperage') and self.tree_reperage.winfo_exists():
            self.configurer_style_tableau()
        
        # Mettre à jour les titres et boutons si possible
        try:
            # Parcourir tous les widgets pour mettre à jour les polices
            self.mettre_a_jour_polices_recursive(self.scrollable_frame, params)
        except Exception as e:
            print(f"⚠️ Erreur lors de la mise à jour des polices: {e}")
    
    def mettre_a_jour_tooltips_contextuels(self):
        """Met à jour les tooltips contextuels avec les paramètres actuels"""
        if self.column_tooltips and hasattr(self, 'tree_reperage'):
            # Nettoyer l'ancien gestionnaire de tooltips
            try:
                self.column_tooltips.cleanup()
            except:
                pass
            
            # Forcer un petit délai avant de recréer pour éviter les conflits
            self.tree_reperage.after(100, lambda: self._recreer_tooltips_contextuels())
    
    def _recreer_tooltips_contextuels(self):
        """Recrée les tooltips contextuels après nettoyage"""
        try:
            # Recréer les tooltips avec les paramètres mis à jour
            self.column_tooltips = ajouter_tooltips_colonnes_tableau(self.tree_reperage, self.data_adapter)
        except Exception as e:
            print(f"Erreur recréation tooltips: {e}")
            self.column_tooltips = None
    
    def mettre_a_jour_polices_recursive(self, widget, params):
        """Met à jour récursivement les polices des widgets selon les paramètres"""
        try:
            # Mettre à jour les CTkLabel (titres, labels)
            if isinstance(widget, ctk.CTkLabel):
                text = widget.cget("text")
                if "📋" in text or "🔍" in text or "⚡" in text or "🔎" in text:  # Titres principaux
                    nouvelle_taille = params.get('taille_police_titres', 20)
                    widget.configure(font=ctk.CTkFont(size=nouvelle_taille, weight="bold"))
                else:  # Labels normaux
                    nouvelle_taille = params.get('taille_police_labels', 12)
                    widget.configure(font=ctk.CTkFont(size=nouvelle_taille, weight="bold"))
            
            # Mettre à jour les CTkButton
            elif isinstance(widget, ctk.CTkButton):
                nouvelle_taille = params.get('taille_police_boutons', 12)
                widget.configure(font=ctk.CTkFont(size=nouvelle_taille, weight="bold"))
            
            # Mettre à jour les CTkEntry
            elif isinstance(widget, ctk.CTkEntry):
                nouvelle_taille = params.get('taille_police_champs', 12)
                widget.configure(font=ctk.CTkFont(size=nouvelle_taille))
            
            # Parcourir récursivement les enfants
            for child in widget.winfo_children():
                self.mettre_a_jour_polices_recursive(child, params)
                
        except Exception as e:
            # Ignorer les erreurs pour les widgets qui n'existent plus
            pass
    
    def ajouter_tooltips_colonnes(self):
        """Ajoute des tooltips aux en-têtes des colonnes"""
        try:
            # Note: Les tooltips sur les headers de treeview sont complexes
            # On peut essayer d'ajouter un tooltip global au tableau
            tooltip_text = """Double-clic pour modifier les cellules (sauf Prix Max et Statut qui sont automatiques)
• Prix Max = calculé automatiquement selon vos paramètres
• Statut = géré automatiquement selon le prix d'achat"""
            ajouter_tooltip(self.tree_reperage, tooltip_text)
        except:
            pass  # En cas d'erreur, pas grave
    
    def creer_section_actions(self, parent):
        """Crée la section des boutons d'action"""
        actions_frame = ctk.CTkFrame(parent)
        actions_frame.pack(fill="x")
        
        # Boutons d'action
        delete_button = ctk.CTkButton(
            actions_frame,
            text="🗑️ Supprimer",
            command=self.supprimer_vehicule,
            font=self.get_font_from_settings('boutons')
        )
        delete_button.pack(side="left", padx=20, pady=15)
        ajouter_tooltip(delete_button, TOOLTIPS['btn_supprimer'])
        
        buy_button = ctk.CTkButton(
            actions_frame,
            text="🏆 Marquer Acheté",
            command=self.marquer_achete,
            font=self.get_font_from_settings('boutons')
        )
        buy_button.pack(side="left", padx=10, pady=15)
        ajouter_tooltip(buy_button, TOOLTIPS['btn_marquer_achete'])
        
        # Bouton export PDF
        export_pdf_button = ctk.CTkButton(
            actions_frame,
            text="📄 Exporter PDF",
            command=self.exporter_pdf,
            font=self.get_font_from_settings('boutons')
        )
        export_pdf_button.pack(side="left", padx=10, pady=15)
        ajouter_tooltip(export_pdf_button, "Exporter les véhicules en repérage vers un document PDF professionnel")
        
        refresh_button = ctk.CTkButton(
            actions_frame,
            text="🔄 Actualiser",
            command=self.actualiser,
            font=self.get_font_from_settings('boutons')
        )
        refresh_button.pack(side="right", padx=20, pady=15)
        ajouter_tooltip(refresh_button, TOOLTIPS['btn_actualiser'])
    
    def demarrer_auto_refresh(self):
        """Démarre l'actualisation automatique périodique"""
        if self.auto_refresh_enabled:
            self.auto_refresh()
    
    def auto_refresh(self):
        """Actualise automatiquement si les données ont changé"""
        try:
            # Créer un hash des données pour détecter les changements
            current_hash = self.calculer_hash_donnees()
            
            if current_hash != self.last_data_hash:
                # Les données ont changé, actualiser silencieusement
                self.actualiser_silencieux()
                self.last_data_hash = current_hash
            
            # Programmer la prochaine actualisation
            if self.auto_refresh_enabled and hasattr(self.parent, 'winfo_exists') and self.parent.winfo_exists():
                self.parent.after(self.auto_refresh_interval, self.auto_refresh)
                
        except Exception as e:
            # En cas d'erreur, continuer sans planter
            print(f"⚠️ Erreur auto-refresh repérage: {e}")
            if self.auto_refresh_enabled and hasattr(self.parent, 'winfo_exists') and self.parent.winfo_exists():
                self.parent.after(self.auto_refresh_interval, self.auto_refresh)
    
    def calculer_hash_donnees(self):
        """Calcule un hash des données pour détecter les changements"""
        try:
            # Créer une représentation des données importantes
            data_repr = []
            
            # Ajouter les véhicules de repérage
            for v in self.data_adapter.vehicules_reperage:
                data_repr.append(f"{v.lot}|{v.marque}|{v.modele}|{v.prix_revente}|{v.cout_reparations}|{v.temps_reparations}")
            
            # Ajouter les paramètres de la journée
            if hasattr(self.data_adapter, 'journee') and self.data_adapter.journee:
                parametres = self.data_adapter.journee.parametres
                data_repr.append(f"params:{parametres.get('tarif_horaire', 0)}|{parametres.get('commission_vente', 0)}|{parametres.get('marge_securite', 0)}")
            
            # Retourner un hash simple
            return hash('|'.join(data_repr))
            
        except Exception:
            return None
    
    def actualiser_silencieux(self):
        """Actualise sans messages d'erreur visibles"""
        try:
            self.actualiser_tableaux_seulement()
        except Exception:
            pass  # Ignorer les erreurs pour éviter les popups
    
    def actualiser_tableaux_seulement(self):
        """Met à jour uniquement les tableaux sans messages"""
        # Effacer le tableau
        if self.tree_reperage and self.tree_reperage.winfo_exists():
            for item in self.tree_reperage.get_children():
                self.tree_reperage.delete(item)
        
        # Recalculer les prix max avec les paramètres de la journée
        for vehicule in self.data_adapter.vehicules_reperage:
            if hasattr(self.data_adapter, 'journee') and self.data_adapter.journee:
                # Utiliser les paramètres de la journée
                vehicule.mettre_a_jour_prix_max_avec_parametres(self.data_adapter.journee.parametres)
            else:
                # Fallback vers settings
                vehicule.mettre_a_jour_prix_max(self.settings)
        
        # Remplir avec les véhicules en repérage
        vehicules_reperage = self.filtrer_vehicules(self.data_adapter.vehicules_reperage)
        for vehicule in vehicules_reperage:
            tags = ("reperage",)
            statut = "Repérage"
            
            if self.tree_reperage and self.tree_reperage.winfo_exists():
                self.tree_reperage.insert("", "end", values=(
                    vehicule.lot,
                    vehicule.marque,
                    vehicule.modele,
                    vehicule.annee,
                    vehicule.kilometrage,
                    vehicule.motorisation,
                    vehicule.prix_revente,
                    vehicule.cout_reparations,
                    vehicule.temps_reparations,
                    vehicule.chose_a_faire,  # Description des réparations
                    vehicule.prix_max_achat,  # Prix Max calculé avec les paramètres de la journée
                    vehicule.prix_achat,
                    vehicule.get_ecart_budget_str(),
                    statut,
                    vehicule.champ_libre,
                    vehicule.reserve_professionnels,
                    vehicule.get_tag_couleur()
                ), tags=tags)
    
    def arreter_auto_refresh(self):
        """Arrête l'actualisation automatique"""
        self.auto_refresh_enabled = False
    
    def cleanup(self):
        """Nettoie complètement l'onglet et ses ressources"""
        # Arrêter l'auto-refresh
        self.arreter_auto_refresh()
        
        # Nettoyer les tooltips contextuels
        if self.column_tooltips:
            try:
                self.column_tooltips.cleanup()
                self.column_tooltips = None
            except:
                pass
        
        # Nettoyer l'édition en cours
        try:
            self.finish_edit()
        except:
            pass
    
    def changer_couleur_selection(self, nouvelle_couleur: str):
        """Change la couleur du véhicule sélectionné"""
        selection = self.tree_reperage.selection()
        if not selection:
            messagebox.showwarning("Attention", "Sélectionnez d'abord un véhicule dans le tableau pour changer sa couleur")
            return
        
        try:
            # Récupérer l'index du véhicule sélectionné
            index_affiche = self.tree_reperage.index(selection[0])
            
            # Obtenir le véhicule correspondant dans la liste filtrée/triée
            vehicules_affiches = self.filtrer_vehicules(self.data_adapter.vehicules_reperage)
            vehicules_tries = self.appliquer_tri(vehicules_affiches)
            
            if 0 <= index_affiche < len(vehicules_tries):
                vehicule = vehicules_tries[index_affiche]
                
                # Trouver l'index réel dans la liste complète
                index_reel = None
                for i, vehicule_original in enumerate(self.data_adapter.vehicules_reperage):
                    if vehicule_original.lot == vehicule.lot:  # Identifier par le lot unique
                        index_reel = i
                        break
                
                if index_reel is not None:
                    # Mettre à jour la couleur
                    vehicule_final = self.data_adapter.vehicules_reperage[index_reel]
                    vehicule_final.couleur = nouvelle_couleur
                    
                    # Sauvegarder et actualiser
                    self.data_adapter.sauvegarder_donnees()
                    self.actualiser()
                    
                    if self.on_data_changed:
                        self.on_data_changed()
                    
                    # Message de confirmation
                    couleurs_noms = {
                        'turquoise': '🟢 Turquoise',
                        'vert': '🟢 Vert', 
                        'orange': '🟠 Orange',
                        'rouge': '🔴 Rouge'
                    }
                    couleur_nom = couleurs_noms.get(nouvelle_couleur, nouvelle_couleur)
                    messagebox.showinfo("✅ Succès", f"Couleur du véhicule {vehicule.lot} changée en {couleur_nom}")
                else:
                    messagebox.showerror("❌ Erreur", "Véhicule non trouvé dans la liste")
            else:
                messagebox.showerror("❌ Erreur", "Index invalide")
            
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors du changement de couleur: {e}")
            print(f"Erreur détaillée: {e}")  # Pour debug
    
    def ajouter_vehicule(self):
        """Ajoute un véhicule au repérage avec calcul automatique du prix max"""
        # Validation basique
        if not self.vars_saisie['lot'].get() or not self.vars_saisie['marque'].get():
            messagebox.showwarning("Attention", "Le n° de lot et la marque sont obligatoires")
            return
        
        try:
            # Créer le véhicule
            vehicule = Vehicule({
                'lot': self.vars_saisie['lot'].get(),
                'marque': self.vars_saisie['marque'].get(),
                'modele': self.vars_saisie['modele'].get(),
                'annee': self.vars_saisie['annee'].get(),
                'kilometrage': self.vars_saisie['kilometrage'].get(),
                'motorisation': self.vars_saisie['motorisation'].get(),
                'prix_revente': self.vars_saisie['prix_revente'].get(),
                'chose_a_faire': self.vars_saisie['chose_a_faire'].get(),
                'cout_reparations': self.vars_saisie['cout_reparations'].get(),
                'temps_reparations': self.vars_saisie['temps_reparations'].get(),
                'champ_libre': self.vars_saisie['champ_libre'].get(),
                'reserve_professionnels': self.vars_saisie['reserve_professionnels'].get(),
                'couleur': self.vars_saisie['couleur'].get()
            })
            
            # Calculer automatiquement le prix max avec les paramètres de la journée
            if hasattr(self.data_adapter, 'journee') and self.data_adapter.journee:
                vehicule.mettre_a_jour_prix_max_avec_parametres(self.data_adapter.journee.parametres)
            else:
                vehicule.mettre_a_jour_prix_max(self.settings)
            
            # Ajouter au data manager
            self.data_adapter.ajouter_vehicule(vehicule)
            
            # Actualiser l'affichage
            self.actualiser()
            
            # Vider les champs
            self.vider_champs()
            
            # Notifier le changement
            if self.on_data_changed:
                self.on_data_changed()
            
            messagebox.showinfo("✅ Succès", "Véhicule ajouté avec succès !")
            
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de l'ajout: {e}")
    
    def vider_champs(self):
        """Vide tous les champs de saisie"""
        try:
            for var in self.vars_saisie.values():
                if isinstance(var, ctk.BooleanVar):
                    var.set(False)  # Remettre les cases à cocher à False
                else:
                    var.set("")  # Vider les champs texte
            
            # Remettre la couleur par défaut
            self.vars_saisie['couleur'].set('turquoise')
            
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors du vidage des champs: {e}")
    
    def supprimer_vehicule(self):
        """Supprime le véhicule sélectionné"""
        selection = self.tree_reperage.selection()
        if not selection:
            messagebox.showwarning("Attention", "Sélectionnez un véhicule à supprimer")
            return
        
        if messagebox.askyesno("Confirmation", "Supprimer ce véhicule ?"):
            try:
                index = self.tree_reperage.index(selection[0])
                self.data_adapter.supprimer_vehicule(index)
                self.actualiser()
                
                if self.on_data_changed:
                    self.on_data_changed()
                
                messagebox.showinfo("✅ Succès", "Véhicule supprimé !")
                
            except Exception as e:
                messagebox.showerror("❌ Erreur", f"Erreur lors de la suppression: {e}")
    
    def marquer_achete(self):
        """Marque le véhicule comme acheté avec dialog personnalisée à police agrandie"""
        selection = self.tree_reperage.selection()
        if not selection:
            messagebox.showwarning("Attention", "Sélectionnez un véhicule à marquer comme acheté")
            return
        
        # Utiliser la nouvelle dialog personnalisée avec police agrandie
        prix_achat = demander_prix_achat(
            self.parent.winfo_toplevel(), 
            "Prix d'achat du véhicule", 
            "Entrez le prix d'achat réel du véhicule (€):"
        )
        
        if prix_achat:
            try:
                # Récupérer l'index dans le tableau affiché (filtré/trié)
                index_affiche = self.tree_reperage.index(selection[0])
                
                # Obtenir le véhicule correspondant dans la liste filtrée/triée
                vehicules_affiches = self.filtrer_vehicules(self.data_adapter.vehicules_reperage)
                vehicules_tries = self.appliquer_tri(vehicules_affiches)
                
                if 0 <= index_affiche < len(vehicules_tries):
                    vehicule = vehicules_tries[index_affiche]
                    
                    # Trouver l'index réel dans la liste complète
                    index_reel = None
                    for i, vehicule_original in enumerate(self.data_adapter.vehicules_reperage):
                        if vehicule_original.lot == vehicule.lot:  # Identifier par le lot unique
                            index_reel = i
                            break
                    
                    if index_reel is not None:
                        # Mettre à jour le véhicule avec le prix d'achat
                        vehicule_final = self.data_adapter.vehicules_reperage[index_reel]
                        vehicule_final.prix_achat = prix_achat
                        vehicule_final.statut = "Acheté"
                        
                        # Utiliser la date actuelle au format correct
                        from datetime import datetime
                        vehicule_final.date_achat = datetime.now().strftime("%d/%m/%Y")
                        
                        # Transférer vers les achetés
                        if self.data_adapter.marquer_achete(index_reel):
                            self.actualiser()
                            
                            if self.on_data_changed:
                                self.on_data_changed()
                            
                            messagebox.showinfo("✅ Succès", "Véhicule marqué comme acheté et transféré !")
                        else:
                            messagebox.showerror("❌ Erreur", "Erreur lors du transfert du véhicule")
                    else:
                        messagebox.showerror("❌ Erreur", "Véhicule non trouvé dans la liste")
                else:
                    messagebox.showerror("❌ Erreur", "Index invalide")
                
            except Exception as e:
                messagebox.showerror("❌ Erreur", f"Erreur lors du marquage: {e}")
                print(f"Erreur détaillée: {e}")  # Pour debug
    
    def actualiser(self):
        """Met à jour l'affichage du tableau avec tri et nouvelles couleurs"""
        # Effacer le tableau
        for item in self.tree_reperage.get_children():
            self.tree_reperage.delete(item)
        
        # Recalculer les prix max pour tous les véhicules avec les paramètres de la journée
        for vehicule in self.data_adapter.vehicules_reperage:
            if hasattr(self.data_adapter, 'journee') and self.data_adapter.journee:
                # Utiliser les paramètres spécifiques de la journée
                vehicule.mettre_a_jour_prix_max_avec_parametres(self.data_adapter.journee.parametres)
            else:
                # Fallback vers settings globaux
                vehicule.mettre_a_jour_prix_max(self.settings)
        
        # SUPPRIMÉ : Le transfert automatique des véhicules avec prix d'achat
        # Désormais, seul le bouton "Marquer acheté" peut transférer un véhicule
        
        # Remplir avec les véhicules en repérage (filtrés et triés)
        vehicules_reperage = self.filtrer_vehicules(self.data_adapter.vehicules_reperage)
        vehicules_reperage = self.appliquer_tri(vehicules_reperage)
        
        for vehicule in vehicules_reperage:
            # Utiliser la couleur choisie par l'utilisateur
            tags = (vehicule.get_tag_couleur(),)
            statut = "Repérage"
            
            self.tree_reperage.insert("", "end", values=(
                vehicule.lot,
                vehicule.marque,
                vehicule.modele,
                vehicule.annee,
                vehicule.kilometrage,
                vehicule.motorisation,  # NOUVEAU
                vehicule.prix_revente,
                vehicule.cout_reparations,
                vehicule.temps_reparations,
                vehicule.chose_a_faire,  # Description des réparations
                vehicule.prix_max_achat,  # Prix Max calculé avec paramètres spécifiques
                vehicule.prix_achat,
                vehicule.get_ecart_budget_str(),
                statut,
                vehicule.champ_libre,  # NOUVEAU
                "Oui" if vehicule.reserve_professionnels else "Non",  # NOUVEAU
                vehicule.get_tag_couleur()  # NOUVEAU
            ), tags=tags)
        
        # Sauvegarder les changements (seulement si pas de recherche)
        if not hasattr(self, 'var_recherche') or not self.var_recherche.get().strip():
            self.data_adapter.sauvegarder_donnees()
        
        # Mettre à jour le hash pour l'auto-refresh
        self.last_data_hash = self.calculer_hash_donnees()
    
    def exporter_pdf(self):
        """Exporte les données de repérage vers un fichier PDF professionnel"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Fichiers PDF", "*.pdf")],
                title="Exporter les véhicules en repérage en PDF"
            )
            
            if filename:
                # Créer le document PDF avec marges
                doc = SimpleDocTemplate(
                    filename, 
                    pagesize=A4,
                    rightMargin=50,
                    leftMargin=50,
                    topMargin=50,
                    bottomMargin=50
                )
                elements = []
                styles = getSampleStyleSheet()
                
                # Style personnalisé pour le titre
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=18,
                    textColor=colors.HexColor('#2196F3'),
                    spaceAfter=30,
                    alignment=1  # Centré
                )
                
                # Récupérer le nom de la journée
                journee_nom = "Enchère"
                if hasattr(self.data_adapter, 'journee') and self.data_adapter.journee:
                    journee_nom = self.data_adapter.journee.nom
                
                # Titre principal
                titre = f"🔍 RAPPORT VÉHICULES EN REPÉRAGE - {journee_nom.upper()}"
                elements.append(Paragraph(titre, title_style))
                
                # Date du rapport
                date_rapport = datetime.now().strftime("%d/%m/%Y à %H:%M")
                date_style = ParagraphStyle(
                    'DateStyle',
                    parent=styles['Normal'],
                    fontSize=10,
                    textColor=colors.grey,
                    alignment=1,
                    spaceAfter=20
                )
                elements.append(Paragraph(f"Rapport généré le {date_rapport}", date_style))
                
                # Récupérer la marge de sécurité
                marge_securite = 200.0  # Valeur par défaut
                if hasattr(self.data_adapter, 'journee') and self.data_adapter.journee:
                    marge_securite = self.data_adapter.journee.parametres.get('marge_securite', 200.0)
                elif hasattr(self, 'settings') and self.settings:
                    marge_securite = self.settings.parametres.get('marge_securite', 200.0)
                
                # Statistiques avec marge de sécurité en rouge
                nb_reperage = len(self.data_adapter.vehicules_reperage)
                prix_max_total = sum(v.get_prix_numerique('prix_max_achat') for v in self.data_adapter.vehicules_reperage)
                prix_revente_total = sum(v.get_prix_numerique('prix_revente') for v in self.data_adapter.vehicules_reperage if v.prix_revente and v.prix_revente.strip())
                marge_potentielle_total = sum(
                    v.get_prix_numerique('prix_revente') - v.get_prix_numerique('prix_max_achat') 
                    for v in self.data_adapter.vehicules_reperage 
                    if v.prix_revente and v.prix_revente.strip() and v.prix_max_achat and v.prix_max_achat.strip()
                )
                
                stats_text = f"""
                <b>📊 STATISTIQUES DE REPÉRAGE</b><br/>
                • Nombre de véhicules en repérage : <b>{nb_reperage}</b><br/>
                • Budget maximum total : <b>{prix_max_total:,.0f}€</b><br/>
                • Potentiel de revente total : <b>{prix_revente_total:,.0f}€</b><br/>
                • Marge potentielle totale : <b>{marge_potentielle_total:+,.0f}€</b><br/>
                <br/>
                <font color="red" size="14"><b>🛡️ MARGE DE SÉCURITÉ : {marge_securite:,.0f}€</b></font>
                """
                
                stats_style = ParagraphStyle(
                    'StatsStyle',
                    parent=styles['Normal'],
                    fontSize=12,
                    spaceAfter=30,
                    backColor=colors.HexColor('#F5F5F5'),
                    borderColor=colors.HexColor('#2196F3'),
                    borderWidth=1,
                    borderPadding=10
                )
                elements.append(Paragraph(stats_text, stats_style))
                elements.append(Spacer(1, 20))
                
                # Titre du tableau
                table_title = Paragraph("<b>📋 DÉTAIL DES VÉHICULES EN REPÉRAGE</b>", styles['Heading2'])
                elements.append(table_title)
                elements.append(Spacer(1, 10))
                
                # Trier les véhicules par numéro de lot (du plus petit au plus grand)
                vehicules_tries = sorted(
                    self.data_adapter.vehicules_reperage, 
                    key=lambda v: self._extraire_numero_lot(v.lot)
                )
                
                # Données du tableau avec nouvelle colonne couleur et réservé pro
                data = [
                    ["LOT", "COULEUR", "MARQUE", "MODÈLE", "ANNÉE", "KM", "MOTORISATION", "PRIX REV", "COÛT RÉP", "TEMPS (h)", "PRIX MAX", "PRO"]
                ]
                
                for vehicule in vehicules_tries:
                    prix_revente = vehicule.get_prix_numerique('prix_revente')
                    prix_max = vehicule.get_prix_numerique('prix_max_achat')
                    cout_reparations = vehicule.get_prix_numerique('cout_reparations')
                    temps_reparations = vehicule.get_prix_numerique('temps_reparations')
                    
                    # Formater les données avec retour à la ligne si nécessaire
                    def formater_cellule(texte, max_chars=15):
                        """Formate une cellule en ajoutant des retours à la ligne"""
                        if not texte or len(str(texte)) <= max_chars:
                            return str(texte)
                        
                        mots = str(texte).split()
                        lignes = []
                        ligne_actuelle = ""
                        
                        for mot in mots:
                            if len(ligne_actuelle + " " + mot) <= max_chars:
                                ligne_actuelle = ligne_actuelle + " " + mot if ligne_actuelle else mot
                            else:
                                if ligne_actuelle:
                                    lignes.append(ligne_actuelle)
                                ligne_actuelle = mot
                        
                        if ligne_actuelle:
                            lignes.append(ligne_actuelle)
                        
                        return "\n".join(lignes)
                    
                    # Créer case couleur (carré unicode coloré)
                    couleur_symbole = self._get_couleur_symbole(vehicule.couleur)
                    
                    # Réservé aux pros
                    reserve_pro = "OUI" if vehicule.reserve_professionnels else "NON"
                    
                    data.append([
                        vehicule.lot,
                        couleur_symbole,
                        formater_cellule(vehicule.marque, 10),
                        formater_cellule(vehicule.modele, 10),
                        vehicule.annee,
                        formater_cellule(vehicule.kilometrage, 8),
                        formater_cellule(vehicule.motorisation, 10),
                        f"{prix_revente:.0f}€" if prix_revente > 0 else "-",
                        f"{cout_reparations:.0f}€" if cout_reparations > 0 else "-",
                        f"{temps_reparations:.0f}h" if temps_reparations > 0 else "-",
                        f"{prix_max:.0f}€" if prix_max > 0 else "-",
                        reserve_pro
                    ])
                
                # Créer le tableau avec largeurs adaptées
                table = Table(data, colWidths=[
                    0.5*inch,  # LOT
                    0.4*inch,  # COULEUR
                    0.7*inch,  # MARQUE  
                    0.7*inch,  # MODÈLE
                    0.4*inch,  # ANNÉE
                    0.6*inch,  # KM
                    0.7*inch,  # MOTORISATION
                    0.6*inch,  # PRIX REV
                    0.6*inch,  # COÛT RÉP
                    0.5*inch,  # TEMPS
                    0.6*inch,  # PRIX MAX
                    0.4*inch   # PRO
                ])
                
                # Style du tableau
                table_style = [
                    # En-tête
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2196F3')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 7),  # Police plus petite pour en-têtes
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    
                    # Corps du tableau
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 6),  # Police plus petite pour contenu
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Grille plus fine
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Alignement vertical en haut
                    
                    # Alternance de couleurs pour les lignes
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')])
                ]
                
                # Ajouter les couleurs de fond pour les cases couleur
                for i, vehicule in enumerate(vehicules_tries):
                    row_idx = i + 1  # +1 car la première ligne est l'en-tête
                    couleur_bg = self._get_couleur_bg(vehicule.couleur)
                    table_style.append(('BACKGROUND', (1, row_idx), (1, row_idx), couleur_bg))
                
                table.setStyle(TableStyle(table_style))
                elements.append(table)
                
                # Section descriptions si présentes
                descriptions_avec_vehicules = [
                    (v, v.chose_a_faire) for v in vehicules_tries  # Utiliser la liste triée
                    if v.chose_a_faire and v.chose_a_faire.strip()
                ]
                
                if descriptions_avec_vehicules:
                    elements.append(Spacer(1, 30))
                    desc_title = Paragraph("<b>🔧 DESCRIPTIONS DES RÉPARATIONS</b>", styles['Heading2'])
                    elements.append(desc_title)
                    elements.append(Spacer(1, 10))
                    
                    for vehicule, description in descriptions_avec_vehicules:
                        desc_text = f"<b>Lot {vehicule.lot} ({vehicule.marque} {vehicule.modele}):</b> {description}"
                        desc_para = Paragraph(desc_text, styles['Normal'])
                        elements.append(desc_para)
                        elements.append(Spacer(1, 5))
                
                # Pied de page
                elements.append(Spacer(1, 30))
                footer_style = ParagraphStyle(
                    'FooterStyle',
                    parent=styles['Normal'],
                    fontSize=8,
                    textColor=colors.grey,
                    alignment=1
                )
                footer_text = f"Gestionnaire d'Enchères - Rapport de repérage généré automatiquement - {date_rapport}"
                elements.append(Paragraph(footer_text, footer_style))
                
                # Construire le document
                doc.build(elements)
                
                messagebox.showinfo("✅ Succès", f"Export PDF réussi vers:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de l'export PDF: {e}")
    
    def _extraire_numero_lot(self, lot: str) -> int:
        """Extrait le numéro du lot pour le tri (gère les lots numériques et alphanumériques)"""
        import re
        # Chercher un nombre dans le lot
        match = re.search(r'\d+', str(lot))
        if match:
            return int(match.group())
        # Si pas de nombre, retourner 0 pour les lots sans numéro
        return 0
    
    def _get_couleur_symbole(self, couleur: str) -> str:
        """Retourne un symbole coloré pour la colonne couleur"""
        symboles = {
            'turquoise': '●',
            'vert': '●', 
            'orange': '●',
            'rouge': '●'
        }
        return symboles.get(couleur, '●')
    
    def _get_couleur_bg(self, couleur: str) -> colors.Color:
        """Retourne la couleur de fond correspondante pour le PDF"""
        couleurs_bg = {
            'turquoise': colors.HexColor('#1ABC9C'),
            'vert': colors.HexColor('#2ECC71'),
            'orange': colors.HexColor('#F39C12'), 
            'rouge': colors.HexColor('#E74C3C')
        }
        return couleurs_bg.get(couleur, colors.HexColor('#1ABC9C'))
    
    def on_double_click(self, event):
        """Gestion du double-clic : popup info pour le lot, édition pour les autres colonnes"""
        try:
            # Fermer l'édition précédente si elle existe
            self.finish_edit()
            
            # Identifier l'élément et la colonne cliqués
            item = self.tree_reperage.identify_row(event.y)
            column = self.tree_reperage.identify_column(event.x)
            
            if not item or column == "#0":
                return
            
            # Vérifier si c'est la colonne du lot (première colonne)
            col_index = int(column.replace('#', '')) - 1
            if col_index == 0:  # Colonne lot
                # Afficher la popup d'informations
                index = self.tree_reperage.index(item)
                vehicules_affiches = self.filtrer_vehicules(self.data_adapter.vehicules_reperage)
                vehicules_tries = self.appliquer_tri(vehicules_affiches)
                
                if 0 <= index < len(vehicules_tries):
                    vehicule = vehicules_tries[index]
                    afficher_info_vehicule(self.parent.winfo_toplevel(), vehicule)
                return
            
            # Pour les autres colonnes, procéder à l'édition normale
            columns_names = ["lot", "marque", "modele", "annee", "kilometrage", "motorisation", "prix_revente", "cout_reparations", "temps_reparations", "description_reparations", "prix_max", "prix_achat", "marge", "statut", "champ_libre", "reserve_pro", "couleur"]
            
            if 0 <= col_index < len(columns_names):
                col_name = columns_names[col_index]
                
                # INTERDIRE l'édition des colonnes prix_max, marge et statut
                if col_name in ["prix_max", "marge", "statut"]:
                    if col_name == "prix_max":
                        messagebox.showinfo("Information", "Le prix maximum est calculé automatiquement selon vos paramètres.\nModifiez le prix de revente, les coûts ou les paramètres pour le changer.")
                    elif col_name == "marge":
                        messagebox.showinfo("Information", "L'écart budget est calculé automatiquement (Prix Max - Prix Achat).\nIl indique si vous respectez votre budget prévu.")
                    else:
                        messagebox.showinfo("Information", "Le statut est géré automatiquement.\nUtilisez le bouton 'Marquer Acheté' pour changer le statut.")
                    return
            
            # Récupérer les coordonnées de la cellule
            bbox = self.tree_reperage.bbox(item, column)
            if not bbox:
                return
            
            # Stocker les informations d'édition
            self.editing_item = item
            self.editing_column = column
            
            # Récupérer la valeur actuelle
            values = self.tree_reperage.item(item)['values']
            current_value = values[col_index] if col_index < len(values) else ""
            
            # Traitement spécial pour la couleur (ComboBox)
            if col_name == "couleur":
                # Créer un ComboBox pour la couleur
                import tkinter.ttk as ttk_native
                self.edit_entry = ttk_native.Combobox(
                    self.tree_reperage, 
                    values=['couleur_turquoise', 'couleur_vert', 'couleur_orange', 'couleur_rouge'],
                    font=('Segoe UI', 16),
                    state="readonly"
                )
                self.edit_entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
                
                # Sélectionner la valeur actuelle
                try:
                    self.edit_entry.current(self.edit_entry['values'].index(str(current_value)))
                except (ValueError, tk.TclError):
                    # Si la valeur actuelle n'est pas dans la liste, prendre la première
                    self.edit_entry.current(0)
            else:
                # Créer le widget d'édition classique avec police normale
                self.edit_entry = tk.Entry(self.tree_reperage, font=('Segoe UI', 20))
                self.edit_entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
                self.edit_entry.insert(0, str(current_value))
                self.edit_entry.select_range(0, tk.END)
            
            self.edit_entry.focus()
            
            # Bind des événements
            self.edit_entry.bind('<Return>', self.on_edit_enter)
            self.edit_entry.bind('<Escape>', self.on_edit_escape)
            self.edit_entry.bind('<FocusOut>', self.on_edit_focusout)
            
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de l'édition: {e}")

    def on_edit_enter(self, event):
        """Valide l'édition avec Entrée"""
        self.save_edit()

    def on_edit_escape(self, event):
        """Annule l'édition avec Échap"""
        self.finish_edit()

    def on_edit_focusout(self, event):
        """Sauvegarde quand on perd le focus"""
        self.save_edit()

    def save_edit(self):
        """Sauvegarde la modification avec recalcul automatique du prix max"""
        if not self.edit_entry or not self.editing_item:
            return
        
        try:
            # Récupérer la nouvelle valeur
            new_value = self.edit_entry.get()
            
            # Récupérer l'index de la ligne dans les données triées/filtrées
            index_affiche = self.tree_reperage.index(self.editing_item)
            
            # Obtenir les véhicules dans l'ordre affiché (filtré et trié)
            vehicules_affiches = self.filtrer_vehicules(self.data_adapter.vehicules_reperage)
            vehicules_tries = self.appliquer_tri(vehicules_affiches)
            
            if 0 <= index_affiche < len(vehicules_tries):
                vehicule = vehicules_tries[index_affiche]
                
                # Récupérer le nom de la colonne
                columns_names = ["lot", "marque", "modele", "annee", "kilometrage", "motorisation", "prix_revente", "cout_reparations", "temps_reparations", "description_reparations", "prix_max", "prix_achat", "marge", "statut", "champ_libre", "reserve_pro", "couleur"]
                col_index = int(self.editing_column.replace('#', '')) - 1
                
                if 0 <= col_index < len(columns_names):
                    col_name = columns_names[col_index]
                    
                    # Mapper les noms de colonnes vers les attributs
                    if col_name == "description_reparations":
                        setattr(vehicule, "chose_a_faire", new_value)
                    elif col_name == "reserve_pro":
                        # Conversion booléenne
                        setattr(vehicule, "reserve_professionnels", new_value.lower() in ['oui', 'true', '1', 'yes'])
                    elif col_name == "couleur":
                        # Conversion couleur
                        setattr(vehicule, "couleur", new_value)
                    else:
                        setattr(vehicule, col_name, new_value)
                
                # Cas spécial pour prix_achat : SUPPRIMÉ le transfert automatique
                # Désormais, seul le bouton "Marquer acheté" peut transférer un véhicule
                if col_name == "prix_achat":
                    # Modification normale du prix d'achat - pas de transfert automatique
                    # Recalculer le prix max si nécessaire
                    if hasattr(self.data_adapter, 'journee') and self.data_adapter.journee:
                        vehicule.mettre_a_jour_prix_max_avec_parametres(self.data_adapter.journee.parametres)
                    else:
                        vehicule.mettre_a_jour_prix_max(self.settings)
                    
                    # Sauvegarder et actualiser normalement
                    self.data_adapter.sauvegarder_donnees()
                    self.actualiser()
                    
                    if self.on_data_changed:
                        self.on_data_changed()
                
                else:
                    # Modification normale - recalculer le prix max si nécessaire
                    if col_name in ["prix_revente", "cout_reparations", "temps_reparations"]:
                        if hasattr(self.data_adapter, 'journee') and self.data_adapter.journee:
                            vehicule.mettre_a_jour_prix_max_avec_parametres(self.data_adapter.journee.parametres)
                        else:
                            vehicule.mettre_a_jour_prix_max(self.settings)
                    
                    # Sauvegarder et actualiser normalement
                    self.data_adapter.sauvegarder_donnees()
                    self.actualiser()
                    
                    if self.on_data_changed:
                        self.on_data_changed()
                
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de la sauvegarde: {e}")
        finally:
            self.finish_edit()

    def finish_edit(self):
        """Termine l'édition et nettoie"""
        if self.edit_entry:
            self.edit_entry.destroy()
            self.edit_entry = None
        self.editing_item = None
        self.editing_column = None

    def on_recherche_change(self, *args):
        """Déclenché quand le texte de recherche change"""
        self.actualiser()

    def effacer_recherche(self):
        """Efface la recherche"""
        self.var_recherche.set("")

    def filtrer_vehicules(self, vehicules):
        """Filtre les véhicules selon le terme de recherche"""
        terme = self.var_recherche.get().lower().strip()
        if not terme:
            return vehicules
        
        vehicules_filtres = []
        for vehicule in vehicules:
            # Recherche dans lot, marque et modèle
            if (terme in vehicule.lot.lower() or 
                terme in vehicule.marque.lower() or 
                terme in vehicule.modele.lower()):
                vehicules_filtres.append(vehicule)
        
        return vehicules_filtres 