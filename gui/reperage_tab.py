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
from utils.tooltips import ajouter_tooltip, TOOLTIPS
from utils.dialogs import demander_prix_achat
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
            font=ctk.CTkFont(size=20, weight="bold")
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
            font=ctk.CTkFont(size=16, weight="bold")
        )
        search_title.pack(pady=(15, 10))
        
        # Frame pour la barre de recherche
        search_input_frame = ctk.CTkFrame(search_frame)
        search_input_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Label
        search_label = ctk.CTkLabel(
            search_input_frame,
            text="Rechercher:",
            font=ctk.CTkFont(size=12, weight="bold"),
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
            font=ctk.CTkFont(size=12),
            width=300
        )
        self.entry_recherche.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        
        # Bouton effacer
        clear_button = ctk.CTkButton(
            search_input_frame,
            text="🗑️ Effacer",
            command=self.effacer_recherche,
            font=ctk.CTkFont(size=12),
            width=100
        )
        clear_button.pack(side="right", padx=10, pady=10)
        
        # Ajouter tooltips
        ajouter_tooltip(self.entry_recherche, TOOLTIPS['recherche'])
        ajouter_tooltip(clear_button, TOOLTIPS['btn_effacer_recherche'])
    
    def creer_section_saisie(self, parent):
        """Crée la section de saisie rapide simplifiée"""
        frame_saisie = ctk.CTkFrame(parent)
        frame_saisie.pack(fill="x", pady=(0, 20))
        
        # Titre section
        titre_saisie = ctk.CTkLabel(
            frame_saisie,
            text="⚡ SAISIE RAPIDE VÉHICULE",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        titre_saisie.pack(pady=(15, 20))
        
        # Initialiser les variables
        self.vars_saisie = {
            'lot': ctk.StringVar(),
            'marque': ctk.StringVar(),
            'modele': ctk.StringVar(),
            'annee': ctk.StringVar(),
            'kilometrage': ctk.StringVar(),
            'prix_revente': ctk.StringVar(),
            'cout_reparations': ctk.StringVar(),
            'temps_reparations': ctk.StringVar(),
            'chose_a_faire': ctk.StringVar()
        }
        
        # Grille de saisie
        grid_frame = ctk.CTkFrame(frame_saisie)
        grid_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Ligne 1: Infos de base
        row1 = ctk.CTkFrame(grid_frame)
        row1.pack(fill="x", pady=5)
        
        # Lot
        lot_label = ctk.CTkLabel(row1, text="N° LOT:", width=80)
        lot_label.pack(side="left", padx=5)
        lot_entry = ctk.CTkEntry(row1, textvariable=self.vars_saisie['lot'], width=100)
        lot_entry.pack(side="left", padx=5)
        ajouter_tooltip(lot_label, TOOLTIPS['lot'])
        ajouter_tooltip(lot_entry, TOOLTIPS['lot'])
        
        # Marque
        marque_label = ctk.CTkLabel(row1, text="MARQUE:", width=80)
        marque_label.pack(side="left", padx=5)
        marque_entry = ctk.CTkEntry(row1, textvariable=self.vars_saisie['marque'], width=120)
        marque_entry.pack(side="left", padx=5)
        ajouter_tooltip(marque_label, TOOLTIPS['marque'])
        ajouter_tooltip(marque_entry, TOOLTIPS['marque'])
        
        # Modèle
        modele_label = ctk.CTkLabel(row1, text="MODÈLE:", width=80)
        modele_label.pack(side="left", padx=5)
        modele_entry = ctk.CTkEntry(row1, textvariable=self.vars_saisie['modele'], width=120)
        modele_entry.pack(side="left", padx=5)
        ajouter_tooltip(modele_label, TOOLTIPS['modele'])
        ajouter_tooltip(modele_entry, TOOLTIPS['modele'])
        
        # Année
        annee_label = ctk.CTkLabel(row1, text="ANNÉE:", width=80)
        annee_label.pack(side="left", padx=5)
        annee_entry = ctk.CTkEntry(row1, textvariable=self.vars_saisie['annee'], width=80)
        annee_entry.pack(side="left", padx=5)
        ajouter_tooltip(annee_label, TOOLTIPS['annee'])
        ajouter_tooltip(annee_entry, TOOLTIPS['annee'])
        
        # Ligne 2: Prix et coûts
        row2 = ctk.CTkFrame(grid_frame)
        row2.pack(fill="x", pady=5)
        
        # Kilométrage avec formatage automatique en temps réel
        km_label = ctk.CTkLabel(row2, text="KM:", width=80)
        km_label.pack(side="left", padx=5)
        km_entry = ctk.CTkEntry(row2, textvariable=self.vars_saisie['kilometrage'], width=100)
        km_entry.pack(side="left", padx=5)
        
        # Bind pour formatage automatique en temps réel
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
        
        # Bind traditionnel pour la sortie de focus (sécurité)
        def formater_kilometrage_focus(event):
            """Formatage de sécurité au focus"""
            valeur = self.vars_saisie['kilometrage'].get().strip()
            if valeur and not valeur.endswith('km'):
                try:
                    chiffres_seulement = ''.join(filter(str.isdigit, valeur))
                    if chiffres_seulement:
                        km = int(chiffres_seulement)
                        if 1 <= km <= 999:
                            valeur_formatee = f"{km},000km"
                            self.vars_saisie['kilometrage'].set(valeur_formatee)
                        elif km >= 1000:
                            if km >= 100000:
                                valeur_formatee = f"{km:,}km".replace(',', ' ')
                            else:
                                valeur_formatee = f"{km}km"
                            self.vars_saisie['kilometrage'].set(valeur_formatee)
                except:
                    pass
        
        km_entry.bind('<FocusOut>', formater_kilometrage_focus)
        
        ajouter_tooltip(km_label, TOOLTIPS['kilometrage'])
        ajouter_tooltip(km_entry, "Kilométrage du véhicule. Tapez juste le nombre (ex: 330 devient automatiquement 330,000km en temps réel)")
        
        # Prix revente
        prix_rev_label = ctk.CTkLabel(row2, text="PRIX REVENTE:", width=100)
        prix_rev_label.pack(side="left", padx=5)
        prix_rev_entry = ctk.CTkEntry(row2, textvariable=self.vars_saisie['prix_revente'], width=100)
        prix_rev_entry.pack(side="left", padx=5)
        ajouter_tooltip(prix_rev_label, TOOLTIPS['prix_revente'])
        ajouter_tooltip(prix_rev_entry, TOOLTIPS['prix_revente'])
        
        # Coût réparations
        cout_rep_label = ctk.CTkLabel(row2, text="COÛT RÉPAR:", width=100)
        cout_rep_label.pack(side="left", padx=5)
        cout_rep_entry = ctk.CTkEntry(row2, textvariable=self.vars_saisie['cout_reparations'], width=100)
        cout_rep_entry.pack(side="left", padx=5)
        ajouter_tooltip(cout_rep_label, TOOLTIPS['cout_reparations'])
        ajouter_tooltip(cout_rep_entry, TOOLTIPS['cout_reparations'])
        
        # Temps réparations
        temps_rep_label = ctk.CTkLabel(row2, text="TEMPS (h):", width=80)
        temps_rep_label.pack(side="left", padx=5)
        temps_rep_entry = ctk.CTkEntry(row2, textvariable=self.vars_saisie['temps_reparations'], width=80)
        temps_rep_entry.pack(side="left", padx=5)
        ajouter_tooltip(temps_rep_label, TOOLTIPS['temps_reparations'])
        ajouter_tooltip(temps_rep_entry, TOOLTIPS['temps_reparations'])
        
        # Ligne 3: Description des réparations
        row3 = ctk.CTkFrame(grid_frame)
        row3.pack(fill="x", pady=5)
        
        desc_label = ctk.CTkLabel(row3, text="DESCRIPTION RÉPARATIONS:", width=180)
        desc_entry = ctk.CTkEntry(row3, textvariable=self.vars_saisie['chose_a_faire'], width=400)
        desc_entry.pack(side="left", padx=5, fill="x", expand=True)
        ajouter_tooltip(desc_label, "Description détaillée des réparations à effectuer sur le véhicule")
        ajouter_tooltip(desc_entry, "Description détaillée des réparations à effectuer sur le véhicule")
        
        # Boutons de saisie
        buttons_frame = ctk.CTkFrame(frame_saisie)
        buttons_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        add_button = ctk.CTkButton(
            buttons_frame,
            text="➕ AJOUTER VÉHICULE",
            command=self.ajouter_vehicule,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        add_button.pack(side="left", padx=10, pady=10)
        ajouter_tooltip(add_button, TOOLTIPS['btn_ajouter'])
        
        clear_button = ctk.CTkButton(
            buttons_frame,
            text="🗑️ VIDER",
            command=self.vider_champs,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        clear_button.pack(side="left", padx=10, pady=10)
        ajouter_tooltip(clear_button, TOOLTIPS['btn_vider'])
    
    def creer_section_tableau(self, parent):
        """Crée la section tableau avec la nouvelle colonne Prix Max"""
        tableau_frame = ctk.CTkFrame(parent)
        tableau_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Titre tableau
        titre_tableau = ctk.CTkLabel(
            tableau_frame,
            text="📋 VÉHICULES EN REPÉRAGE",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        titre_tableau.pack(pady=(15, 20))
        
        # Container pour le tableau avec hauteur minimale
        container = ctk.CTkFrame(tableau_frame)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        container.configure(height=250)  # Hauteur minimale de 250px
        
        # Tableau (MODIFIÉ : ajout colonne description_reparations)
        columns = ("lot", "marque", "modele", "annee", "kilometrage", "prix_revente", "cout_reparations", "temps_reparations", "description_reparations", "prix_max", "prix_achat", "statut")
        self.tree_reperage = ttk.Treeview(container, columns=columns, show="headings", height=8)  # Hauteur optimisée
        
        # Configuration du style pour agrandir la police
        style = ttk.Style()
        style.configure("Treeview", font=('Segoe UI', 14), rowheight=30)
        style.configure("Treeview.Heading", font=('Segoe UI', 16, 'bold'))  # Police plus petite pour les en-têtes
        
        # Configuration des colonnes (MODIFIÉE avec Description et Prix Max)
        headings = {
            "lot": "LOT",
            "marque": "MARQUE",
            "modele": "MODÈLE", 
            "annee": "ANNÉE",
            "kilometrage": "KM",
            "prix_revente": "PRIX REVENTE",
            "cout_reparations": "COÛT RÉPAR",
            "temps_reparations": "TEMPS (h)",
            "description_reparations": "DESCRIPTION RÉPAR",  # NOUVEAU
            "prix_max": "PRIX MAX",
            "prix_achat": "PRIX ACHAT",
            "statut": "STATUT"
        }
        
        for col, heading in headings.items():
            self.tree_reperage.heading(col, text=heading)
            if col in ["lot", "annee", "kilometrage", "temps_reparations"]:
                self.tree_reperage.column(col, width=80, anchor="center")
            elif col in ["prix_revente", "cout_reparations", "prix_max", "prix_achat"]:
                self.tree_reperage.column(col, width=100, anchor="center")
            elif col == "statut":
                self.tree_reperage.column(col, width=100, anchor="center")
            elif col == "description_reparations":
                self.tree_reperage.column(col, width=200, anchor="w")  # Plus large pour la description
            else:
                self.tree_reperage.column(col, width=120, anchor="w")
        
        # Configuration des tags de couleur
        self.tree_reperage.tag_configure('reperage', background='#2196F3', foreground='white')  # Bleu avec texte blanc
        self.tree_reperage.tag_configure('achete', background='#4CAF50', foreground='white')    # Vert avec texte blanc
        self.tree_reperage.tag_configure('perte', background='#F44336', foreground='white')     # Rouge avec texte blanc
        
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
        
        # Bind pour édition au double-clic
        self.tree_reperage.bind("<Double-1>", self.on_double_click)
        
        # Ajouter tooltips aux en-têtes
        self.ajouter_tooltips_colonnes()
    
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
            font=ctk.CTkFont(size=12, weight="bold")
        )
        delete_button.pack(side="left", padx=20, pady=15)
        ajouter_tooltip(delete_button, TOOLTIPS['btn_supprimer'])
        
        buy_button = ctk.CTkButton(
            actions_frame,
            text="🏆 Marquer Acheté",
            command=self.marquer_achete,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        buy_button.pack(side="left", padx=10, pady=15)
        ajouter_tooltip(buy_button, TOOLTIPS['btn_marquer_achete'])
        
        # Bouton export PDF
        export_pdf_button = ctk.CTkButton(
            actions_frame,
            text="📄 Exporter PDF",
            command=self.exporter_pdf,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        export_pdf_button.pack(side="left", padx=10, pady=15)
        ajouter_tooltip(export_pdf_button, "Exporter les véhicules en repérage vers un document PDF professionnel")
        
        refresh_button = ctk.CTkButton(
            actions_frame,
            text="🔄 Actualiser",
            command=self.actualiser,
            font=ctk.CTkFont(size=12, weight="bold")
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
                    vehicule.prix_revente,
                    vehicule.cout_reparations,
                    vehicule.temps_reparations,
                    vehicule.chose_a_faire,  # Description des réparations
                    vehicule.prix_max_achat,  # Prix Max calculé avec les paramètres de la journée
                    vehicule.prix_achat,
                    statut
                ), tags=tags)
    
    def arreter_auto_refresh(self):
        """Arrête l'actualisation automatique"""
        self.auto_refresh_enabled = False

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
                'prix_revente': self.vars_saisie['prix_revente'].get(),
                'chose_a_faire': self.vars_saisie['chose_a_faire'].get(),
                'cout_reparations': self.vars_saisie['cout_reparations'].get(),
                'temps_reparations': self.vars_saisie['temps_reparations'].get()
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
        for var in self.vars_saisie.values():
            var.set("")
    
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
                index = self.tree_reperage.index(selection[0])
                vehicule = self.data_adapter.vehicules_reperage[index]
                vehicule.prix_achat = prix_achat
                vehicule.statut = "Acheté"
                vehicule.date_achat = "2024-12-20"  # Date actuelle simplifiée
                
                # Déplacer vers les achetés
                self.data_adapter.marquer_achete(index)
                self.actualiser()
                
                if self.on_data_changed:
                    self.on_data_changed()
                
                messagebox.showinfo("✅ Succès", "Véhicule marqué comme acheté !")
                
            except Exception as e:
                messagebox.showerror("❌ Erreur", f"Erreur: {e}")
    
    def actualiser(self):
        """Met à jour l'affichage du tableau avec recalcul des prix max"""
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
        
        # Transférer les véhicules avec prix d'achat vers les achetés (seulement si pas de recherche)
        if not hasattr(self, 'var_recherche') or not self.var_recherche.get().strip():
            vehicules_a_transferer = []
            for i, vehicule in enumerate(self.data_adapter.vehicules_reperage):
                if vehicule.prix_achat and vehicule.prix_achat.strip() and vehicule.prix_achat != "0":
                    vehicules_a_transferer.append(i)
            
            # Transférer (en commençant par la fin pour ne pas décaler les indices)
            for i in reversed(vehicules_a_transferer):
                vehicule = self.data_adapter.vehicules_reperage[i]
                
                # Marquer comme acheté avec date
                vehicule.marquer_achete()
                
                # Ajouter aux achetés s'il n'y est pas déjà
                if not any(v.lot == vehicule.lot for v in self.data_adapter.vehicules_achetes):
                    self.data_adapter.vehicules_achetes.append(vehicule)
                
                # Retirer du repérage
                del self.data_adapter.vehicules_reperage[i]
            
            # Sauvegarder immédiatement après transfert
            if vehicules_a_transferer:
                self.data_adapter.sauvegarder_donnees()
                
                # Notifier les changements pour actualiser l'onglet achetés
                if self.on_data_changed:
                    self.on_data_changed()
        
        # Remplir avec les véhicules en repérage (qui n'ont pas de prix d'achat)
        vehicules_reperage = self.filtrer_vehicules(self.data_adapter.vehicules_reperage)
        for vehicule in vehicules_reperage:
            # Seuls les véhicules sans prix d'achat restent ici = bleu
            tags = ("reperage",)
            statut = "Repérage"
            
            self.tree_reperage.insert("", "end", values=(
                vehicule.lot,
                vehicule.marque,
                vehicule.modele,
                vehicule.annee,
                vehicule.kilometrage,
                vehicule.prix_revente,
                vehicule.cout_reparations,
                vehicule.temps_reparations,
                vehicule.chose_a_faire,  # Description des réparations
                vehicule.prix_max_achat,  # Prix Max calculé avec paramètres spécifiques
                vehicule.prix_achat,
                statut
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
                
                # Statistiques
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
                • Marge potentielle totale : <b>{marge_potentielle_total:+,.0f}€</b>
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
                
                # Données du tableau
                data = [
                    ["LOT", "MARQUE", "MODÈLE", "ANNÉE", "KM", "PRIX REVENTE", "PRIX MAX", "COÛT RÉPAR", "TEMPS (h)"]
                ]
                
                for vehicule in self.data_adapter.vehicules_reperage:
                    prix_revente = vehicule.get_prix_numerique('prix_revente')
                    prix_max = vehicule.get_prix_numerique('prix_max_achat')
                    cout_reparations = vehicule.get_prix_numerique('cout_reparations')
                    temps_reparations = vehicule.get_prix_numerique('temps_reparations')
                    
                    data.append([
                        vehicule.lot,
                        vehicule.marque,
                        vehicule.modele,
                        vehicule.annee,
                        vehicule.kilometrage,
                        f"{prix_revente:.0f}€" if prix_revente > 0 else "-",
                        f"{prix_max:.0f}€" if prix_max > 0 else "-",
                        f"{cout_reparations:.0f}€" if cout_reparations > 0 else "-",
                        f"{temps_reparations:.0f}h" if temps_reparations > 0 else "-"
                    ])
                
                # Créer le tableau
                table = Table(data, colWidths=[0.8*inch, 1.2*inch, 1.2*inch, 0.8*inch, 1*inch, 1*inch, 1*inch, 1*inch, 0.8*inch])
                
                # Style du tableau
                table.setStyle(TableStyle([
                    # En-tête
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2196F3')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    
                    # Corps du tableau
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    
                    # Alternance de couleurs pour les lignes
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')])
                ]))
                
                elements.append(table)
                
                # Section descriptions si présentes
                descriptions_avec_vehicules = [
                    (v, v.chose_a_faire) for v in self.data_adapter.vehicules_reperage 
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
    
    def on_double_click(self, event):
        """Démarre l'édition inline sur double-clic (MODIFIÉE : interdiction statut et prix_max)"""
        try:
            # Fermer l'édition précédente si elle existe
            self.finish_edit()
            
            # Identifier l'élément et la colonne cliqués
            item = self.tree_reperage.identify_row(event.y)
            column = self.tree_reperage.identify_column(event.x)
            
            if not item or column == "#0":
                return
            
            # Vérifier si la colonne peut être éditée
            col_index = int(column.replace('#', '')) - 1
            columns_names = ["lot", "marque", "modele", "annee", "kilometrage", "prix_revente", "cout_reparations", "temps_reparations", "description_reparations", "prix_max", "prix_achat", "statut"]
            
            if 0 <= col_index < len(columns_names):
                col_name = columns_names[col_index]
                
                # INTERDIRE l'édition des colonnes prix_max et statut
                if col_name in ["prix_max", "statut"]:
                    if col_name == "prix_max":
                        messagebox.showinfo("Information", "Le prix maximum est calculé automatiquement selon vos paramètres.\nModifiez le prix de revente, les coûts ou les paramètres pour le changer.")
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
            
            # Créer le widget d'édition avec police normale
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
            
            # Récupérer l'index de la ligne et le véhicule
            index = self.tree_reperage.index(self.editing_item)
            vehicule = self.data_adapter.vehicules_reperage[index]
            
            # Récupérer le nom de la colonne
            columns_names = ["lot", "marque", "modele", "annee", "kilometrage", "prix_revente", "cout_reparations", "temps_reparations", "description_reparations", "prix_max", "prix_achat", "statut"]
            col_index = int(self.editing_column.replace('#', '')) - 1
            
            if 0 <= col_index < len(columns_names):
                col_name = columns_names[col_index]
                
                # Mapper description_reparations vers chose_a_faire dans le modèle
                if col_name == "description_reparations":
                    setattr(vehicule, "chose_a_faire", new_value)
                else:
                    # Mettre à jour le véhicule
                    setattr(vehicule, col_name, new_value)
                
                # Cas spécial pour prix_achat : arrêter temporairement l'auto-refresh
                if col_name == "prix_achat" and new_value and new_value.strip() and new_value != "0":
                    # Arrêter temporairement l'auto-refresh pour éviter les conflits
                    old_auto_refresh = self.auto_refresh_enabled
                    self.auto_refresh_enabled = False
                    
                    try:
                        # Actualiser immédiatement pour transférer
                        self.actualiser()
                        
                        # Notifier les changements
                        if self.on_data_changed:
                            self.on_data_changed()
                        
                    finally:
                        # Relancer l'auto-refresh après un délai
                        def relancer_auto_refresh():
                            self.auto_refresh_enabled = old_auto_refresh
                            if self.auto_refresh_enabled:
                                self.demarrer_auto_refresh()
                        
                        # Relancer après 2 secondes
                        self.parent.after(2000, relancer_auto_refresh)
                
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