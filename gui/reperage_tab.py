#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Onglet de repérage des véhicules - CustomTkinter
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox

from config.settings import AppSettings
from services.data_manager import DataManager
from utils.styles import StyleManager
from models.vehicule import Vehicule

class ReperageTab:
    """Onglet principal de repérage des véhicules avec CustomTkinter"""
    
    def __init__(self, parent, settings: AppSettings, data_manager: DataManager, 
                 style_manager: StyleManager, on_data_changed=None):
        self.parent = parent
        self.settings = settings
        self.data_manager = data_manager
        self.style_manager = style_manager
        self.on_data_changed = on_data_changed
        
        # Variables d'interface
        self.vars_saisie = {}
        self.tree_reperage = None
        self.edit_entry = None  # Widget d'édition temporaire
        self.editing_item = None
        self.editing_column = None
        
        # Créer le frame principal
        self.frame = ctk.CTkFrame(parent)
        
        self.creer_interface()
    
    def creer_interface(self):
        """Crée l'interface complète de l'onglet repérage avec CustomTkinter"""
        main_frame = ctk.CTkFrame(self.frame)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre
        titre = ctk.CTkLabel(
            main_frame,
            text="🔍 REPÉRAGE DE VÉHICULES",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titre.pack(pady=(0, 20))
        
        # Saisie rapide
        self.creer_section_saisie(main_frame)
        
        # Tableau véhicules
        self.creer_section_tableau(main_frame)
        
        # Boutons actions
        self.creer_section_actions(main_frame)
    
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
        ctk.CTkLabel(row1, text="N° LOT:", width=80).pack(side="left", padx=5)
        ctk.CTkEntry(row1, textvariable=self.vars_saisie['lot'], width=100).pack(side="left", padx=5)
        
        # Marque
        ctk.CTkLabel(row1, text="MARQUE:", width=80).pack(side="left", padx=5)
        ctk.CTkEntry(row1, textvariable=self.vars_saisie['marque'], width=120).pack(side="left", padx=5)
        
        # Modèle
        ctk.CTkLabel(row1, text="MODÈLE:", width=80).pack(side="left", padx=5)
        ctk.CTkEntry(row1, textvariable=self.vars_saisie['modele'], width=120).pack(side="left", padx=5)
        
        # Année
        ctk.CTkLabel(row1, text="ANNÉE:", width=80).pack(side="left", padx=5)
        ctk.CTkEntry(row1, textvariable=self.vars_saisie['annee'], width=80).pack(side="left", padx=5)
        
        # Ligne 2: Prix et coûts
        row2 = ctk.CTkFrame(grid_frame)
        row2.pack(fill="x", pady=5)
        
        # Kilométrage
        ctk.CTkLabel(row2, text="KM:", width=80).pack(side="left", padx=5)
        ctk.CTkEntry(row2, textvariable=self.vars_saisie['kilometrage'], width=100).pack(side="left", padx=5)
        
        # Prix revente
        ctk.CTkLabel(row2, text="PRIX REVENTE:", width=100).pack(side="left", padx=5)
        ctk.CTkEntry(row2, textvariable=self.vars_saisie['prix_revente'], width=100).pack(side="left", padx=5)
        
        # Coût réparations
        ctk.CTkLabel(row2, text="COÛT RÉPAR:", width=100).pack(side="left", padx=5)
        ctk.CTkEntry(row2, textvariable=self.vars_saisie['cout_reparations'], width=100).pack(side="left", padx=5)
        
        # Temps réparations
        ctk.CTkLabel(row2, text="TEMPS (h):", width=80).pack(side="left", padx=5)
        ctk.CTkEntry(row2, textvariable=self.vars_saisie['temps_reparations'], width=80).pack(side="left", padx=5)
        
        # Ligne 3: Description
        row3 = ctk.CTkFrame(grid_frame)
        row3.pack(fill="x", pady=5)
        
        ctk.CTkLabel(row3, text="DESCRIPTION:", width=100).pack(side="left", padx=5)
        ctk.CTkEntry(row3, textvariable=self.vars_saisie['chose_a_faire'], width=400).pack(side="left", padx=5, fill="x", expand=True)
        
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
        
        clear_button = ctk.CTkButton(
            buttons_frame,
            text="🗑️ VIDER",
            command=self.vider_champs,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        clear_button.pack(side="left", padx=10, pady=10)
    
    def creer_section_tableau(self, parent):
        """Crée la section tableau simplifiée"""
        tableau_frame = ctk.CTkFrame(parent)
        tableau_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Titre tableau
        titre_tableau = ctk.CTkLabel(
            tableau_frame,
            text="📋 VÉHICULES EN REPÉRAGE",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        titre_tableau.pack(pady=(15, 20))
        
        # Container pour le tableau
        container = ctk.CTkFrame(tableau_frame)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # Tableau
        columns = ("lot", "marque", "modele", "annee", "kilometrage", "prix_revente", "cout_reparations", "temps_reparations", "statut")
        self.tree_reperage = ttk.Treeview(container, columns=columns, show="headings", height=20)
        
        # Configuration du style pour agrandir la police
        style = ttk.Style()
        style.configure("Treeview", font=('Segoe UI', 14), rowheight=30)
        style.configure("Treeview.Heading", font=('Segoe UI', 16, 'bold'))
        
        # Configuration des colonnes
        headings = {
            "lot": "LOT",
            "marque": "MARQUE",
            "modele": "MODÈLE", 
            "annee": "ANNÉE",
            "kilometrage": "KM",
            "prix_revente": "PRIX REVENTE",
            "cout_reparations": "COÛT RÉPAR",
            "temps_reparations": "TEMPS (h)",
            "statut": "STATUT"
        }
        
        for col, heading in headings.items():
            self.tree_reperage.heading(col, text=heading)
            if col in ["lot", "annee", "kilometrage", "temps_reparations"]:
                self.tree_reperage.column(col, width=80, anchor="center")
            elif col in ["prix_revente", "cout_reparations"]:
                self.tree_reperage.column(col, width=100, anchor="center")
            elif col == "statut":
                self.tree_reperage.column(col, width=100, anchor="center")
            else:
                self.tree_reperage.column(col, width=120, anchor="w")
        
        # Configuration des tags de couleur
        self.tree_reperage.tag_configure('reperage', background='#E3F2FD')  # Bleu clair
        self.tree_reperage.tag_configure('achete', background='#E8F5E8')    # Vert clair
        self.tree_reperage.tag_configure('perte', background='#FFEBEE')     # Rouge clair
        
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
        
        buy_button = ctk.CTkButton(
            actions_frame,
            text="🏆 Marquer Acheté",
            command=self.marquer_achete,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        buy_button.pack(side="left", padx=10, pady=15)
        
        refresh_button = ctk.CTkButton(
            actions_frame,
            text="🔄 Actualiser",
            command=self.actualiser,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        refresh_button.pack(side="right", padx=20, pady=15)
    
    def ajouter_vehicule(self):
        """Ajoute un véhicule au repérage"""
        # Validation basique
        if not self.vars_saisie['lot'].get() or not self.vars_saisie['marque'].get():
            messagebox.showwarning("Attention", "Le n° de lot et la marque sont obligatoires")
            return
        
        try:
            # Créer le véhicule
            vehicule = Vehicule(
                lot=self.vars_saisie['lot'].get(),
                marque=self.vars_saisie['marque'].get(),
                modele=self.vars_saisie['modele'].get(),
                annee=self.vars_saisie['annee'].get(),
                kilometrage=self.vars_saisie['kilometrage'].get(),
                prix_revente=self.vars_saisie['prix_revente'].get(),
                chose_a_faire=self.vars_saisie['chose_a_faire'].get(),
                cout_reparations=self.vars_saisie['cout_reparations'].get(),
                temps_reparations=self.vars_saisie['temps_reparations'].get()
            )
            
            # Ajouter au data manager
            self.data_manager.ajouter_vehicule(vehicule)
            
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
                self.data_manager.supprimer_vehicule(index)
                self.actualiser()
                
                if self.on_data_changed:
                    self.on_data_changed()
                
                messagebox.showinfo("✅ Succès", "Véhicule supprimé !")
                
            except Exception as e:
                messagebox.showerror("❌ Erreur", f"Erreur lors de la suppression: {e}")
    
    def marquer_achete(self):
        """Marque le véhicule comme acheté"""
        selection = self.tree_reperage.selection()
        if not selection:
            messagebox.showwarning("Attention", "Sélectionnez un véhicule à marquer comme acheté")
            return
        
        # Demander le prix d'achat
        from tkinter import simpledialog
        prix_achat = simpledialog.askstring("Prix d'achat", "Entrez le prix d'achat (€):")
        
        if prix_achat:
            try:
                index = self.tree_reperage.index(selection[0])
                vehicule = self.data_manager.vehicules_reperage[index]
                vehicule.prix_achat = prix_achat
                vehicule.statut = "Acheté"
                vehicule.date_achat = "2024-12-20"  # Date actuelle simplifiée
                
                # Déplacer vers les achetés
                self.data_manager.marquer_achete(index)
                self.actualiser()
                
                if self.on_data_changed:
                    self.on_data_changed()
                
                messagebox.showinfo("✅ Succès", "Véhicule marqué comme acheté !")
                
            except Exception as e:
                messagebox.showerror("❌ Erreur", f"Erreur: {e}")
    
    def actualiser(self):
        """Met à jour l'affichage du tableau"""
        # Effacer le tableau
        for item in self.tree_reperage.get_children():
            self.tree_reperage.delete(item)
        
        # Remplir avec les véhicules en repérage
        for vehicule in self.data_manager.vehicules_reperage:
            # Déterminer le tag de couleur selon le statut
            if vehicule.statut == "Acheté":
                tags = ("achete",)
            elif hasattr(vehicule, 'calculer_marge') and vehicule.calculer_marge() < 0:
                tags = ("perte",)
            else:
                tags = ("reperage",)
            
            self.tree_reperage.insert("", "end", values=(
                vehicule.lot,
                vehicule.marque,
                vehicule.modele,
                vehicule.annee,
                vehicule.kilometrage,
                vehicule.prix_revente,
                vehicule.cout_reparations,
                vehicule.temps_reparations,
                vehicule.statut
            ), tags=tags)
    
    def on_double_click(self, event):
        """Démarre l'édition inline sur double-clic"""
        try:
            # Fermer l'édition précédente si elle existe
            self.finish_edit()
            
            # Identifier l'élément et la colonne cliqués
            item = self.tree_reperage.identify_row(event.y)
            column = self.tree_reperage.identify_column(event.x)
            
            if not item or column == "#0":
                return
            
            # Récupérer les coordonnées de la cellule
            bbox = self.tree_reperage.bbox(item, column)
            if not bbox:
                return
            
            # Stocker les informations d'édition
            self.editing_item = item
            self.editing_column = column
            
            # Récupérer la valeur actuelle
            col_index = int(column.replace('#', '')) - 1
            values = self.tree_reperage.item(item)['values']
            current_value = values[col_index] if col_index < len(values) else ""
            
            # Créer le widget d'édition
            self.edit_entry = tk.Entry(self.tree_reperage)
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
        """Sauvegarde la modification"""
        if not self.edit_entry or not self.editing_item:
            return
        
        try:
            # Récupérer la nouvelle valeur
            new_value = self.edit_entry.get()
            
            # Récupérer l'index de la ligne et le véhicule
            index = self.tree_reperage.index(self.editing_item)
            vehicule = self.data_manager.vehicules_reperage[index]
            
            # Récupérer le nom de la colonne
            columns_names = ["lot", "marque", "modele", "annee", "kilometrage", "prix_revente", "cout_reparations", "temps_reparations", "statut"]
            col_index = int(self.editing_column.replace('#', '')) - 1
            
            if 0 <= col_index < len(columns_names):
                col_name = columns_names[col_index]
                
                # Mettre à jour le véhicule
                setattr(vehicule, col_name, new_value)
                
                # Sauvegarder
                self.data_manager.sauvegarder_donnees()
                
                # Actualiser l'affichage
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