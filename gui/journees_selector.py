#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface de sélection des journées d'enchères - Choix de base de données
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import locale
import os

from services.journees_manager import JourneesManager
from utils.tooltips import ajouter_tooltip


class CarteJournee(ctk.CTkFrame):
    """Widget carte pour afficher une base de données d'enchère"""
    
    def __init__(self, parent, info_journee: Dict[str, Any], on_select: Callable, on_edit: Callable, on_delete: Callable, on_export: Callable = None):
        super().__init__(parent)
        
        self.info_journee = info_journee
        self.on_select = on_select
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.on_export_callback = on_export
        
        self.configure(height=200, width=350, corner_radius=15)
        self.grid_propagate(False)
        
        self.creer_interface()
    
    def creer_interface(self):
        """Crée l'interface de la carte"""
        # Header avec titre et date
        header_frame = ctk.CTkFrame(self, height=60, corner_radius=10)
        header_frame.pack(fill="x", padx=15, pady=(15, 8))
        header_frame.pack_propagate(False)
        
        # Titre de la journée
        titre = ctk.CTkLabel(
            header_frame,
            text=f"🗃️ {self.info_journee['nom'][:25]}{'...' if len(self.info_journee['nom']) > 25 else ''}",
            font=ctk.CTkFont(size=16, weight="bold"),
            wraplength=300
        )
        titre.pack(pady=(10, 5))
        
        # Date et lieu
        date_str = self.format_date(self.info_journee['date'])
        lieu_str = f" - {self.info_journee['lieu']}" if self.info_journee['lieu'] else ""
        sous_titre = ctk.CTkLabel(
            header_frame,
            text=f"📅 {date_str}{lieu_str}",
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        )
        sous_titre.pack()
        
        # Corps avec statistiques
        stats_frame = ctk.CTkFrame(self, height=80)
        stats_frame.pack(fill="x", padx=15, pady=8)
        stats_frame.pack_propagate(False)
        
        # Statistiques en grille
        stats_grid = ctk.CTkFrame(stats_frame)
        stats_grid.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Première ligne
        row1 = ctk.CTkFrame(stats_grid)
        row1.pack(fill="x", pady=2)
        
        ctk.CTkLabel(row1, text=f"🔍 Repérage: {self.info_journee['nb_reperage']}", 
                    font=ctk.CTkFont(size=11)).pack(side="left", padx=5)
        ctk.CTkLabel(row1, text=f"✅ Achetés: {self.info_journee['nb_achetes']}", 
                    font=ctk.CTkFont(size=11)).pack(side="right", padx=5)
        
        # Deuxième ligne
        row2 = ctk.CTkFrame(stats_grid)
        row2.pack(fill="x", pady=2)
        
        investissement = self.format_prix(self.info_journee['investissement'])
        ctk.CTkLabel(row2, text=f"💰 Investi: {investissement}", 
                    font=ctk.CTkFont(size=11)).pack(side="left", padx=5)
        
        # Nom du fichier (petit)
        nom_fichier = self.info_journee['fichier'][:15] + "..." if len(self.info_journee['fichier']) > 15 else self.info_journee['fichier']
        ctk.CTkLabel(row2, text=f"📄 {nom_fichier}", 
                    font=ctk.CTkFont(size=9), text_color="gray50").pack(side="right", padx=5)
        
        # Boutons
        boutons_frame = ctk.CTkFrame(self, fg_color=["#F8F9FA", "#2B2B2B"])
        boutons_frame.pack(fill="x", padx=15, pady=(15, 15))
        
        # Bouton Ouvrir
        ouvrir_btn = ctk.CTkButton(
            boutons_frame,
            text="📂 Ouvrir",
            command=lambda: self.on_select(self.info_journee['fichier']),
            font=ctk.CTkFont(size=14, weight="bold"),
            width=100,
            height=35,
            fg_color="#1ABC9C",
            hover_color="#16A085"
        )
        ouvrir_btn.pack(side="left", padx=(10, 8))
        
        # Bouton Modifier
        modifier_btn = ctk.CTkButton(
            boutons_frame,
            text="✏️",
            command=lambda: self.on_edit(self.info_journee['fichier']),
            font=ctk.CTkFont(size=12, weight="bold"),
            width=35,
            height=35,
            fg_color="#2ECC71",
            hover_color="#27AE60"
        )
        modifier_btn.pack(side="left", padx=8)
        
        # Bouton Export
        export_btn = ctk.CTkButton(
            boutons_frame,
            text="📤",
            command=lambda: self.on_export(self.info_journee['fichier']),
            font=ctk.CTkFont(size=12, weight="bold"),
            width=35,
            height=35,
            fg_color="#F39C12",
            hover_color="#E67E22"
        )
        export_btn.pack(side="left", padx=8)
        
        # Bouton Supprimer
        supprimer_btn = ctk.CTkButton(
            boutons_frame,
            text="🗑️",
            command=lambda: self.on_delete(self.info_journee['fichier']),
            font=ctk.CTkFont(size=12, weight="bold"),
            width=35,
            height=35,
            fg_color="#E74C3C",
            hover_color="#C0392B"
        )
        supprimer_btn.pack(side="right", padx=(8, 10))
        
        # Tooltips
        ajouter_tooltip(ouvrir_btn, f"Ouvrir la base de données '{self.info_journee['nom']}'")
        ajouter_tooltip(modifier_btn, f"Modifier les informations de base '{self.info_journee['nom']}'")
        ajouter_tooltip(export_btn, f"Exporter '{self.info_journee['nom']}' vers un fichier JSON")
        ajouter_tooltip(supprimer_btn, f"Supprimer définitivement '{self.info_journee['nom']}'")
        ajouter_tooltip(titre, f"Base créée le {self.format_date_creation()}")
    
    def format_date(self, date_str: str) -> str:
        """Formate une date pour affichage"""
        try:
            if date_str:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                return date_obj.strftime("%d/%m/%Y")
            return "Date non définie"
        except:
            return date_str or "Date non définie"
    
    def format_date_creation(self) -> str:
        """Formate la date de création"""
        try:
            date_str = self.info_journee['date_creation']
            date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return date_obj.strftime("%d/%m/%Y à %H:%M")
        except:
            return "Date inconnue"
    
    def format_prix(self, prix: float) -> str:
        """Formate un prix pour affichage"""
        if prix == 0:
            return "0€"
        return f"{prix:,.0f}€".replace(',', ' ')

    def on_export(self, nom_fichier):
        """Callback pour l'export de cette journée"""
        # Utiliser le callback passé en paramètre si disponible
        if self.on_export_callback:
            self.on_export_callback(nom_fichier)
            return
        
        # Trouver le sélecteur principal dans la hiérarchie (fallback)
        parent = self.master
        while parent:
            if hasattr(parent, 'exporter_journee_specifique'):
                parent.exporter_journee_specifique(nom_fichier)
                return
            parent = getattr(parent, 'master', None)
        
        # Si on n'arrive pas à trouver la méthode, afficher une erreur
        from tkinter import messagebox
        messagebox.showerror("Erreur", "Impossible de trouver la fonction d'export")


class DialogJournee:
    """Dialog pour créer/modifier une base de données d'enchère"""
    
    def __init__(self, parent, mode="create", journee_info=None):
        self.parent = parent
        self.mode = mode
        self.journee_info = journee_info or {}
        self.result = None
        
        # Créer la fenêtre dialog
        self.dialog = tk.Toplevel(parent)
        title = "Nouvelle base de données" if mode == "create" else "Modifier la base de données"
        self.dialog.title(title)
        self.dialog.geometry("600x600")  # Plus petite sans description
        self.dialog.resizable(True, True)  # RENDABLE REDIMENSIONNABLE
        self.dialog.minsize(700, 700)     # Taille minimale
        
        # Centrer la dialog
        self.center_dialog()
        
        # Rendre la dialog modale
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Variables
        self.vars = {
            'nom': tk.StringVar(value=self.journee_info.get('nom', '')),
            'lieu': tk.StringVar(value=self.journee_info.get('lieu', ''))
        }
        
        # Date avec widget calendrier
        date_existante = self.journee_info.get('date', '')
        if date_existante:
            try:
                from datetime import datetime
                self.date_selectionnee = datetime.strptime(date_existante, "%Y-%m-%d").date()
            except:
                from datetime import date
                self.date_selectionnee = date.today()
        else:
            from datetime import date
            self.date_selectionnee = date.today()
        
        # Créer l'interface
        self.create_interface()
        
        # Focus sur le nom
        self.entry_nom.focus_set()
        
        # Bind des événements
        self.dialog.bind('<Return>', self.on_ok)
        self.dialog.bind('<Escape>', self.on_cancel)
        
        # Attendre la fermeture de la dialog
        self.dialog.wait_window()
    
    def center_dialog(self):
        """Centre la dialog sur l'écran"""
        self.dialog.update_idletasks()
        
        width = 600
        height = 600
        
        pos_x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        pos_y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        
        self.dialog.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
    
    def create_interface(self):
        """Crée l'interface de la dialog"""
        # Frame principal avec scrollbar pour gérer le redimensionnement
        main_canvas = tk.Canvas(self.dialog, bg='white')
        scrollbar = tk.Scrollbar(self.dialog, orient="vertical", command=main_canvas.yview)
        self.scrollable_frame = tk.Frame(main_canvas, bg='white')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack du canvas avec redimensionnement adaptatif
        main_canvas.pack(side="left", fill="both", expand=True, padx=30, pady=30)
        scrollbar.pack(side="right", fill="y", pady=30)
        
        # Titre plus grand
        title_text = "🗃️ NOUVELLE BASE DE DONNÉES" if self.mode == "create" else "✏️ MODIFIER LA BASE DE DONNÉES"
        title_label = tk.Label(
            self.scrollable_frame,
            text=title_text,
            font=('Segoe UI', 24, 'bold'),  # Police plus grande
            bg='white',
            fg='#2E86AB'
        )
        title_label.pack(pady=(20, 25))  # Plus d'espace
        
        # Information avec police plus grande
        info_text = "Chaque base de données est complètement séparée\navec ses propres véhicules et paramètres."
        info_label = tk.Label(
            self.scrollable_frame,
            text=info_text,
            font=('Segoe UI', 14),  # Police plus grande
            bg='white',
            fg='#666666'
        )
        info_label.pack(pady=(0, 30))  # Plus d'espace
        
        # Formulaire avec plus d'espace
        form_frame = tk.Frame(self.scrollable_frame, bg='white')
        form_frame.pack(fill='x', pady=(0, 30))
        
        # Nom de l'enchère avec champ plus grand
        self.create_field(form_frame, "Nom de l'enchère:", self.vars['nom'], 0, height=40)
        self.entry_nom = self.last_entry
        
        # Date avec calendrier plus grand
        tk.Label(
            form_frame,
            text="Date:",
            font=('Segoe UI', 16, 'bold'),  # Police plus grande
            bg='white',
            fg='#333333'
        ).grid(row=1, column=0, sticky='w', pady=(15, 10), padx=(0, 20))
        
        try:
            from tkcalendar import DateEntry
            self.date_entry = DateEntry(
                form_frame,
                width=15,  # Plus large
                background='darkblue',
                foreground='white',
                borderwidth=2,
                font=('Segoe UI', 14),  # Police plus grande
                date_pattern='dd/mm/yyyy',
                year=self.date_selectionnee.year,
                month=self.date_selectionnee.month,
                day=self.date_selectionnee.day
            )
            self.date_entry.grid(row=1, column=1, sticky='ew', pady=(15, 10), ipady=10)  # Plus de padding
        except ImportError:
            # Fallback vers champ texte si tkcalendar n'est pas disponible
            date_str = self.date_selectionnee.strftime("%d/%m/%Y")
            self.vars['date'] = tk.StringVar(value=date_str)
            self.date_entry = tk.Entry(
                form_frame,
                textvariable=self.vars['date'],
                font=('Segoe UI', 14),
                relief='solid',
                borderwidth=1
            )
            self.date_entry.grid(row=1, column=1, sticky='ew', pady=(15, 10), ipady=10)
        
        # Lieu avec champ plus grand
        self.create_field(form_frame, "Lieu:", self.vars['lieu'], 2, height=40)
        
        # Configuration du grid pour adaptation
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Boutons plus grands
        buttons_frame = tk.Frame(self.scrollable_frame, bg='white')
        buttons_frame.pack(fill='x', pady=(30, 20))
        
        # Bouton Annuler plus grand
        cancel_btn = tk.Button(
            buttons_frame,
            text="❌ Annuler",
            font=('Segoe UI', 16, 'bold'),  # Plus grand
            bg='#F44336',
            fg='white',
            relief='flat',
            padx=25,  # Plus de padding
            pady=12,
            command=self.on_cancel
        )
        cancel_btn.pack(side='left', padx=(0, 15))
        
        # Bouton OK plus grand
        ok_text = "✅ Créer" if self.mode == "create" else "✅ Modifier"
        ok_btn = tk.Button(
            buttons_frame,
            text=ok_text,
            font=('Segoe UI', 16, 'bold'),  # Plus grand
            bg='#4CAF50',
            fg='white',
            relief='flat',
            padx=25,  # Plus de padding
            pady=12,
            command=self.on_ok
        )
        ok_btn.pack(side='right', padx=(15, 0))
        
        # Bind mouse wheel pour scroll
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_field(self, parent, label_text, var, row, height=30):
        """Crée un champ de formulaire avec hauteur configurable"""
        tk.Label(
            parent,
            text=label_text,
            font=('Segoe UI', 16, 'bold'),  # Police plus grande
            bg='white',
            fg='#333333'
        ).grid(row=row, column=0, sticky='w', pady=(15, 10), padx=(0, 20))
        
        entry = tk.Entry(
            parent,
            textvariable=var,
            font=('Segoe UI', 14),  # Police plus grande
            relief='solid',
            borderwidth=1
        )
        entry.grid(row=row, column=1, sticky='ew', pady=(15, 10), ipady=10)  # Plus de padding vertical
        
        self.last_entry = entry
    
    def on_ok(self, event=None):
        """Valide la dialog"""
        nom = self.vars['nom'].get().strip()
        if not nom:
            messagebox.showerror("Erreur", "Le nom de l'enchère est obligatoire")
            return
        
        # Récupérer la date
        try:
            if hasattr(self.date_entry, 'get_date'):
                # Widget calendrier
                date_obj = self.date_entry.get_date()
                date_str = date_obj.strftime("%Y-%m-%d")
            else:
                # Champ texte fallback
                date_input = self.date_entry.get()
                if '/' in date_input:
                    # Format DD/MM/YYYY vers YYYY-MM-DD
                    from datetime import datetime
                    date_obj = datetime.strptime(date_input, "%d/%m/%Y")
                    date_str = date_obj.strftime("%Y-%m-%d")
                else:
                    date_str = date_input
        except:
            from datetime import date
            date_str = date.today().strftime("%Y-%m-%d")
        
        self.result = {
            'nom': nom,
            'date': date_str,
            'lieu': self.vars['lieu'].get().strip(),
            'description': ''  # Toujours vide maintenant
        }
        
        self.dialog.destroy()
    
    def on_cancel(self, event=None):
        """Annule la dialog"""
        self.result = None
        self.dialog.destroy()


class JourneesSelector:
    """Interface de sélection des bases de données d'enchères"""
    
    def __init__(self, parent, on_journee_selected: Callable):
        self.parent = parent
        self.on_journee_selected = on_journee_selected
        
        # Gestionnaire des journées
        self.journees_manager = JourneesManager()
        
        # Frame principal
        self.frame = ctk.CTkFrame(parent)
        
        self.creer_interface()
        self.actualiser_affichage()
    
    def creer_interface(self):
        """Crée l'interface principale"""
        # Header
        header_frame = ctk.CTkFrame(self.frame, height=140)
        header_frame.pack(fill="x", padx=25, pady=(25, 15))  # AMÉLIORATION: padding augmenté
        header_frame.pack_propagate(False)
        
        # Titre principal
        titre = ctk.CTkLabel(
            header_frame,
            text="🗃️ SÉLECTEUR DE BASE DE DONNÉES",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titre.pack(pady=(15, 5))
        
        sous_titre = ctk.CTkLabel(
            header_frame,
            text="Choisissez une base de données d'enchère à utiliser",
            font=ctk.CTkFont(size=16),
            text_color="gray60"
        )
        sous_titre.pack(pady=(0, 5))
        
        # Information importante
        info_label = ctk.CTkLabel(
            header_frame,
            text="💡 Chaque base est complètement séparée avec ses propres véhicules et paramètres",
            font=ctk.CTkFont(size=12),
            text_color="#2E86AB"
        )
        info_label.pack(pady=(5, 15))
        
        # Frame pour les boutons d'action - AMÉLIORATION DU PADDING
        actions_frame = ctk.CTkFrame(self.frame)
        actions_frame.pack(fill="x", padx=35, pady=25)  # AMÉLIORATION: padding augmenté
        
        # Bouton Nouvelle Base - TURQUOISE (action principale positive)
        nouvelle_btn = ctk.CTkButton(
            actions_frame,
            text="➕ Nouvelle Base",
            command=self.nouvelle_journee,
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            height=40,
            fg_color="#1ABC9C",  # CHANGÉ: Turquoise cohérent (principale positive)
            hover_color="#16A085"
        )
        nouvelle_btn.pack(side="left", padx=(15, 12))  # AMÉLIORATION: margin interne augmenté
        
        # Bouton Import CSV - VERT (action secondaire positive)
        import_csv_btn = ctk.CTkButton(
            actions_frame,
            text="📊 Importer CSV",
            command=self.importer_csv,
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            height=40,
            fg_color="#2ECC71",  # CHANGÉ: Vert cohérent (action utile)
            hover_color="#27AE60"
        )
        import_csv_btn.pack(side="left", padx=12)  # AMÉLIORATION: margin équilibré
        
        # Bouton Import PDF - ORANGE (action spécialisée)
        import_pdf_btn = ctk.CTkButton(
            actions_frame,
            text="📄 Importer PDF",
            command=self.importer_pdf,
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            height=40,
            fg_color="#F39C12",  # GARDÉ: Orange cohérent (spécialisé)
            hover_color="#E67E22"
        )
        import_pdf_btn.pack(side="left", padx=12)  # AMÉLIORATION: margin équilibré
        
        # Bouton Import JSON - BLEU (action technique)
        import_btn = ctk.CTkButton(
            actions_frame,
            text="📥 Importer JSON",
            command=self.importer_journee,
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            height=40,
            fg_color="#3498DB",  # CHANGÉ: Bleu plus doux et cohérent
            hover_color="#2980B9"
        )
        import_btn.pack(side="left", padx=12)  # AMÉLIORATION: margin équilibré
        
        # Bouton Export Tout - VIOLET (action administrative)
        export_btn = ctk.CTkButton(
            actions_frame,
            text="📤 Exporter Tout",
            command=self.exporter_toutes_journees,
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            height=40,
            fg_color="#8E44AD",  # CHANGÉ: Violet plus doux et cohérent
            hover_color="#7D3C98"
        )
        export_btn.pack(side="right", padx=(12, 15))  # AMÉLIORATION: margin interne augmenté
        
        # Tooltips
        ajouter_tooltip(nouvelle_btn, "Créer une nouvelle base de données vide")
        ajouter_tooltip(import_csv_btn, "Importer des données depuis un fichier CSV exporté de l'ancienne version")
        ajouter_tooltip(import_pdf_btn, "Importer des données depuis un fichier PDF avec reconnaissance automatique")
        ajouter_tooltip(import_btn, "Importer une base de données depuis un fichier JSON")
        ajouter_tooltip(export_btn, "Exporter toutes les bases vers un dossier")
        
        # Container scrollable pour les cartes - AMÉLIORATION DU PADDING
        self.cartes_container = ctk.CTkScrollableFrame(self.frame)
        self.cartes_container.pack(fill="both", expand=True, padx=25, pady=(0, 25))  # AMÉLIORATION: padding augmenté
        
        # Configurer le grid du container
        self.cartes_container.grid_columnconfigure(0, weight=1)
        self.cartes_container.grid_columnconfigure(1, weight=1)
        self.cartes_container.grid_columnconfigure(2, weight=1)
    
    def actualiser_affichage(self):
        """Met à jour l'affichage des cartes"""
        # Effacer les cartes existantes
        for widget in self.cartes_container.winfo_children():
            widget.destroy()
        
        # Récupérer les bases disponibles
        journees_info = self.journees_manager.get_journees_disponibles()
        
        if not journees_info:
            # Aucune base
            no_data_label = ctk.CTkLabel(
                self.cartes_container,
                text="🗃️ Aucune base de données\n\nCliquez sur 'Nouvelle Base' pour commencer",
                font=ctk.CTkFont(size=16),
                text_color="gray50"
            )
            no_data_label.pack(expand=True, pady=50)
            return
        
        # Créer les cartes en grille
        self.creer_grille_cartes(journees_info)
    
    def creer_grille_cartes(self, journees_info):
        """Crée la grille de cartes des bases de données"""
        # Configuration de la grille (3 colonnes)
        nb_colonnes = 3
        
        for i, info in enumerate(journees_info):
            row = i // nb_colonnes
            col = i % nb_colonnes
            
            # Créer la carte
            carte = CarteJournee(
                self.cartes_container,
                info,
                self.selectionner_journee,
                self.modifier_journee,
                self.supprimer_journee,
                self.exporter_journee_specifique
            )
            
            carte.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        # Configuration du grid pour que les cartes s'étendent
        for col in range(nb_colonnes):
            self.cartes_container.grid_columnconfigure(col, weight=1)
    
    def nouvelle_journee(self):
        """Crée une nouvelle base de données"""
        dialog = DialogJournee(self.frame.winfo_toplevel(), mode="create")
        
        if dialog.result:
            nom_fichier = self.journees_manager.creer_nouvelle_journee(
                dialog.result['nom'],
                dialog.result['date'],
                dialog.result['lieu'],
                dialog.result['description']
            )
            
            self.actualiser_affichage()
            messagebox.showinfo("✅ Succès", f"Base de données '{dialog.result['nom']}' créée avec succès !\nFichier: {nom_fichier}")
    
    def modifier_journee(self, nom_fichier: str):
        """Modifie une base de données existante"""
        # Charger les infos actuelles
        journees = self.journees_manager.get_journees_disponibles()
        journee_info = next((j for j in journees if j['fichier'] == nom_fichier), None)
        
        if not journee_info:
            messagebox.showerror("Erreur", "Base de données non trouvée")
            return
        
        dialog = DialogJournee(
            self.frame.winfo_toplevel(),
            mode="edit",
            journee_info=journee_info
        )
        
        if dialog.result:
            if self.journees_manager.modifier_journee(
                nom_fichier,
                dialog.result['nom'],
                dialog.result['date'],
                dialog.result['lieu'],
                dialog.result['description']
            ):
                self.actualiser_affichage()
                messagebox.showinfo("✅ Succès", "Base de données modifiée avec succès !")
            else:
                messagebox.showerror("❌ Erreur", "Erreur lors de la modification")
    
    def supprimer_journee(self, nom_fichier: str):
        """Supprime une base de données"""
        # Récupérer le nom pour affichage
        journees = self.journees_manager.get_journees_disponibles()
        journee_info = next((j for j in journees if j['fichier'] == nom_fichier), None)
        
        if not journee_info:
            messagebox.showerror("Erreur", "Base de données non trouvée")
            return
        
        # Ne pas supprimer s'il ne reste qu'une base
        if len(journees) <= 1:
            messagebox.showwarning("Attention", "Impossible de supprimer la dernière base de données.")
            return
        
        reponse = messagebox.askyesno(
            "Confirmation",
            f"Supprimer définitivement la base '{journee_info['nom']}' ?\n\n"
            f"📄 Fichier: {nom_fichier}\n"
            f"⚠️ Tous les véhicules et données seront perdus !\n"
            f"Cette action est irréversible."
        )
        
        if reponse:
            if self.journees_manager.supprimer_journee(nom_fichier):
                self.actualiser_affichage()
                messagebox.showinfo("✅ Succès", "Base de données supprimée avec succès !")
            else:
                messagebox.showerror("❌ Erreur", "Erreur lors de la suppression")
    
    def selectionner_journee(self, nom_fichier: str):
        """Sélectionne une base de données et lance l'application"""
        journee = self.journees_manager.charger_journee_fichier(nom_fichier)
        if journee:
            print(f"🚀 Base sélectionnée: {journee.nom} ({nom_fichier})")
            self.on_journee_selected(journee, self.journees_manager)
    
    def importer_csv(self):
        """Importe des données depuis un fichier CSV"""
        from tkinter import filedialog, simpledialog
        
        # Sélectionner le fichier CSV
        fichier = filedialog.askopenfilename(
            title="Sélectionner un fichier CSV à importer",
            filetypes=[
                ("Fichiers CSV", "*.csv"),
                ("Tous les fichiers", "*.*")
            ],
            initialdir=os.path.expanduser("~")
        )
        
        if not fichier:
            return
        
        # Demander le nom de la nouvelle journée
        nom_journee = simpledialog.askstring(
            "Nom de la base de données",
            "Entrez un nom pour la nouvelle base de données :",
            initialvalue=f"Import CSV - {os.path.basename(fichier).replace('.csv', '')}"
        )
        
        if not nom_journee:
            return
        
        # Créer une fenêtre de progression
        progress_window = tk.Toplevel(self.frame.winfo_toplevel())
        progress_window.title("Import en cours...")
        progress_window.geometry("400x200")
        progress_window.resizable(False, False)
        progress_window.transient(self.frame.winfo_toplevel())
        progress_window.grab_set()
        
        # Centrer la fenêtre
        progress_window.update_idletasks()
        x = (progress_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (progress_window.winfo_screenheight() // 2) - (200 // 2)
        progress_window.geometry(f"400x200+{x}+{y}")
        
        # Contenu de la fenêtre de progression
        progress_frame = tk.Frame(progress_window, bg='white', padx=30, pady=30)
        progress_frame.pack(fill='both', expand=True)
        
        tk.Label(
            progress_frame,
            text="📊 Import CSV en cours...",
            font=('Segoe UI', 16, 'bold'),
            bg='white',
            fg='#FF9800'
        ).pack(pady=(0, 10))
        
        progress_label = tk.Label(
            progress_frame,
            text="Lecture du fichier CSV...",
            font=('Segoe UI', 12),
            bg='white',
            fg='#333333'
        )
        progress_label.pack(pady=(0, 20))
        
        # Fonction pour effectuer l'import en arrière-plan
        def effectuer_import():
            try:
                progress_label.config(text="Analyse du fichier CSV...")
                progress_window.update()
                
                succes, message = self.journees_manager.importer_donnees_csv(fichier, nom_journee)
                
                progress_window.destroy()
                
                if succes:
                    self.actualiser_affichage()
                    messagebox.showinfo("✅ Import CSV réussi", message)
                else:
                    messagebox.showerror("❌ Erreur d'import CSV", message)
                    
            except Exception as e:
                progress_window.destroy()
                messagebox.showerror("❌ Erreur", f"Erreur inattendue lors de l'import :\n{e}")
        
        # Lancer l'import après un court délai
        progress_window.after(100, effectuer_import)
    
    def importer_pdf(self):
        """Importe des données depuis un fichier PDF"""
        from tkinter import filedialog
        
        fichier = filedialog.askopenfilename(
            title="Sélectionner un fichier PDF à importer",
            filetypes=[
                ("Fichiers PDF", "*.pdf"),
                ("Tous les fichiers", "*.*")
            ],
            initialdir=os.path.expanduser("~")
        )
        
        if fichier:
            succes, message = self.journees_manager.importer_donnees_pdf(fichier)
            
            if succes:
                self.actualiser_affichage()
                messagebox.showinfo("✅ Import PDF réussi", message)
            else:
                messagebox.showerror("❌ Erreur d'import PDF", message)
    
    def importer_journee(self):
        """Importe une journée depuis un fichier JSON"""
        from tkinter import filedialog
        
        fichier = filedialog.askopenfilename(
            title="Sélectionner un fichier JSON à importer",
            filetypes=[
                ("Fichiers JSON", "*.json"),
                ("Tous les fichiers", "*.*")
            ],
            initialdir=os.path.expanduser("~")
        )
        
        if fichier:
            succes, message = self.journees_manager.importer_journee_json(fichier)
            
            if succes:
                self.actualiser_affichage()
                messagebox.showinfo("✅ Import réussi", message)
            else:
                messagebox.showerror("❌ Erreur d'import", message)
    
    def exporter_toutes_journees(self):
        """Exporte toutes les journées vers un dossier"""
        from tkinter import filedialog
        
        dossier = filedialog.askdirectory(
            title="Sélectionner le dossier de destination pour l'export",
            initialdir=os.path.expanduser("~")
        )
        
        if dossier:
            succes, message = self.journees_manager.exporter_toutes_journees_json(dossier)
            
            if succes:
                messagebox.showinfo("✅ Export réussi", message)
            else:
                messagebox.showerror("❌ Erreur d'export", message)
    
    def exporter_journee_specifique(self, nom_fichier: str):
        """Exporte une journée spécifique"""
        from tkinter import filedialog
        
        # Récupérer les infos de la journée pour le nom par défaut
        journees = self.journees_manager.get_journees_disponibles()
        journee_info = next((j for j in journees if j['fichier'] == nom_fichier), None)
        
        if not journee_info:
            messagebox.showerror("Erreur", "Journée non trouvée")
            return
        
        # Nom par défaut
        nom_defaut = f"{journee_info['nom'].replace(' ', '_')}_export.json"
        
        fichier = filedialog.asksaveasfilename(
            title="Exporter la journée vers...",
            defaultextension=".json",
            filetypes=[
                ("Fichiers JSON", "*.json"),
                ("Tous les fichiers", "*.*")
            ],
            initialdir=os.path.expanduser("~"),
            initialfile=nom_defaut
        )
        
        if fichier:
            succes, message = self.journees_manager.exporter_journee_json(nom_fichier, fichier)
            
            if succes:
                messagebox.showinfo("✅ Export réussi", message)
            else:
                messagebox.showerror("❌ Erreur d'export", message) 