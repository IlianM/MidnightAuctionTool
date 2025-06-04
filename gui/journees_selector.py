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

from services.journees_manager import JourneesManager
from utils.tooltips import ajouter_tooltip


class CarteJournee(ctk.CTkFrame):
    """Widget carte pour afficher une base de données d'enchère"""
    
    def __init__(self, parent, info_journee: Dict[str, Any], on_select: Callable, on_edit: Callable, on_delete: Callable):
        super().__init__(parent)
        
        self.info_journee = info_journee
        self.on_select = on_select
        self.on_edit = on_edit
        self.on_delete = on_delete
        
        self.configure(height=200, width=350, corner_radius=15)
        self.grid_propagate(False)
        
        self.creer_interface()
    
    def creer_interface(self):
        """Crée l'interface de la carte"""
        # Header avec titre et date
        header_frame = ctk.CTkFrame(self, height=60, corner_radius=10)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
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
        stats_frame.pack(fill="x", padx=10, pady=5)
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
        
        # Boutons d'action
        actions_frame = ctk.CTkFrame(self, height=50)
        actions_frame.pack(fill="x", padx=10, pady=(5, 10))
        actions_frame.pack_propagate(False)
        
        # Bouton principal - Lancer
        open_btn = ctk.CTkButton(
            actions_frame,
            text="🚀 LANCER",
            command=lambda: self.on_select(self.info_journee['fichier']),
            font=ctk.CTkFont(size=14, weight="bold"),
            height=35,
            width=150
        )
        open_btn.pack(side="left", padx=5, pady=7)
        
        # Boutons secondaires
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="✏️",
            command=lambda: self.on_edit(self.info_journee['fichier']),
            font=ctk.CTkFont(size=12),
            width=35,
            height=35
        )
        edit_btn.pack(side="right", padx=2, pady=7)
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️",
            command=lambda: self.on_delete(self.info_journee['fichier']),
            font=ctk.CTkFont(size=12),
            width=35,
            height=35,
            fg_color="red",
            hover_color="darkred"
        )
        delete_btn.pack(side="right", padx=2, pady=7)
        
        # Tooltips
        ajouter_tooltip(open_btn, f"Lancer l'application avec la base de données '{self.info_journee['nom']}'")
        ajouter_tooltip(edit_btn, "Modifier les informations de cette base de données")
        ajouter_tooltip(delete_btn, "Supprimer définitivement cette base de données")
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
        self.dialog.geometry("600x500")
        self.dialog.resizable(False, False)
        
        # Centrer la dialog
        self.center_dialog()
        
        # Rendre la dialog modale
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Variables
        self.vars = {
            'nom': tk.StringVar(value=self.journee_info.get('nom', '')),
            'date': tk.StringVar(value=self.journee_info.get('date', datetime.now().strftime("%Y-%m-%d"))),
            'lieu': tk.StringVar(value=self.journee_info.get('lieu', '')),
            'description': tk.StringVar(value=self.journee_info.get('description', ''))
        }
        
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
        height = 500
        
        pos_x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        pos_y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        
        self.dialog.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
    
    def create_interface(self):
        """Crée l'interface de la dialog"""
        # Frame principal
        main_frame = tk.Frame(self.dialog, bg='white', padx=30, pady=30)
        main_frame.pack(fill='both', expand=True)
        
        # Titre
        title_text = "🗃️ NOUVELLE BASE DE DONNÉES" if self.mode == "create" else "✏️ MODIFIER LA BASE DE DONNÉES"
        title_label = tk.Label(
            main_frame,
            text=title_text,
            font=('Segoe UI', 20, 'bold'),
            bg='white',
            fg='#2E86AB'
        )
        title_label.pack(pady=(0, 20))
        
        # Information
        info_text = "Chaque base de données est complètement séparée\navec ses propres véhicules et paramètres."
        info_label = tk.Label(
            main_frame,
            text=info_text,
            font=('Segoe UI', 11),
            bg='white',
            fg='#666666'
        )
        info_label.pack(pady=(0, 20))
        
        # Formulaire
        form_frame = tk.Frame(main_frame, bg='white')
        form_frame.pack(fill='x', pady=(0, 30))
        
        # Nom de l'enchère
        self.create_field(form_frame, "Nom de l'enchère:", self.vars['nom'], 0)
        self.entry_nom = self.last_entry
        
        # Date
        self.create_field(form_frame, "Date (YYYY-MM-DD):", self.vars['date'], 1)
        
        # Lieu
        self.create_field(form_frame, "Lieu:", self.vars['lieu'], 2)
        
        # Description
        tk.Label(
            form_frame,
            text="Description:",
            font=('Segoe UI', 14, 'bold'),
            bg='white',
            fg='#333333'
        ).grid(row=3, column=0, sticky='nw', pady=(10, 5), padx=(0, 15))
        
        self.text_description = tk.Text(
            form_frame,
            font=('Segoe UI', 12),
            height=4,
            relief='solid',
            borderwidth=1
        )
        self.text_description.grid(row=3, column=1, sticky='ew', pady=(10, 5))
        self.text_description.insert('1.0', self.vars['description'].get())
        
        # Configuration du grid
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Boutons
        buttons_frame = tk.Frame(main_frame, bg='white')
        buttons_frame.pack(fill='x')
        
        # Bouton Annuler
        cancel_btn = tk.Button(
            buttons_frame,
            text="❌ Annuler",
            font=('Segoe UI', 14, 'bold'),
            bg='#F44336',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            command=self.on_cancel
        )
        cancel_btn.pack(side='left', padx=(0, 10))
        
        # Bouton OK
        ok_text = "✅ Créer" if self.mode == "create" else "✅ Modifier"
        ok_btn = tk.Button(
            buttons_frame,
            text=ok_text,
            font=('Segoe UI', 14, 'bold'),
            bg='#4CAF50',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            command=self.on_ok
        )
        ok_btn.pack(side='right', padx=(10, 0))
    
    def create_field(self, parent, label_text, var, row):
        """Crée un champ de formulaire"""
        tk.Label(
            parent,
            text=label_text,
            font=('Segoe UI', 14, 'bold'),
            bg='white',
            fg='#333333'
        ).grid(row=row, column=0, sticky='w', pady=(10, 5), padx=(0, 15))
        
        entry = tk.Entry(
            parent,
            textvariable=var,
            font=('Segoe UI', 12),
            relief='solid',
            borderwidth=1
        )
        entry.grid(row=row, column=1, sticky='ew', pady=(10, 5), ipady=5)
        
        self.last_entry = entry
    
    def on_ok(self, event=None):
        """Valide la dialog"""
        nom = self.vars['nom'].get().strip()
        if not nom:
            messagebox.showerror("Erreur", "Le nom de l'enchère est obligatoire")
            return
        
        self.result = {
            'nom': nom,
            'date': self.vars['date'].get().strip(),
            'lieu': self.vars['lieu'].get().strip(),
            'description': self.text_description.get('1.0', 'end-1c').strip()
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
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
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
        
        # Barre d'actions
        actions_frame = ctk.CTkFrame(self.frame, height=60)
        actions_frame.pack(fill="x", padx=20, pady=10)
        actions_frame.pack_propagate(False)
        
        # Bouton nouvelle base
        new_btn = ctk.CTkButton(
            actions_frame,
            text="➕ NOUVELLE BASE",
            command=self.nouvelle_journee,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=200
        )
        new_btn.pack(side="left", padx=15, pady=10)
        
        # Bouton actualiser
        refresh_btn = ctk.CTkButton(
            actions_frame,
            text="🔄 Actualiser",
            command=self.actualiser_affichage,
            font=ctk.CTkFont(size=12),
            height=40,
            width=120
        )
        refresh_btn.pack(side="right", padx=15, pady=10)
        
        # Zone de cartes avec scroll
        self.scrollable_frame = ctk.CTkScrollableFrame(self.frame, label_text="📋 BASES DE DONNÉES DISPONIBLES")
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Container pour les cartes
        self.cartes_container = ctk.CTkFrame(self.scrollable_frame)
        self.cartes_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tooltips
        ajouter_tooltip(new_btn, "Créer une nouvelle base de données complètement séparée")
        ajouter_tooltip(refresh_btn, "Actualiser la liste des bases de données disponibles")
    
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
                self.supprimer_journee
            )
            
            carte.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
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