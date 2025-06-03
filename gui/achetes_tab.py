#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Onglet véhicules achetés - CustomTkinter
"""

import customtkinter as ctk
from tkinter import ttk, messagebox
import csv
from datetime import datetime

from config.settings import AppSettings
from services.data_manager import DataManager
from utils.styles import StyleManager

class AchetesTab:
    """Onglet véhicules achetés avec CustomTkinter"""
    
    def __init__(self, parent, settings: AppSettings, data_manager: DataManager, 
                 style_manager: StyleManager, on_data_changed=None):
        self.parent = parent
        self.settings = settings
        self.data_manager = data_manager
        self.style_manager = style_manager
        self.on_data_changed = on_data_changed
        
        # Variables d'interface
        self.tree_achetes = None
        
        # Créer le frame principal
        self.frame = ctk.CTkFrame(parent)
        
        self.creer_interface()
    
    def creer_interface(self):
        """Crée l'interface de l'onglet achetés avec CustomTkinter"""
        # Créer un scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self.frame)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre
        titre = ctk.CTkLabel(
            self.scrollable_frame,
            text="🏆 VÉHICULES ACHETÉS",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titre.pack(pady=(0, 20))
        
        # Frame pour les statistiques rapides
        stats_frame = ctk.CTkFrame(self.scrollable_frame)
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # Statistiques
        self.label_stats = ctk.CTkLabel(
            stats_frame,
            text="Chargement des statistiques...",
            font=ctk.CTkFont(size=14)
        )
        self.label_stats.pack(pady=15)
        
        # Frame pour les boutons
        buttons_frame = ctk.CTkFrame(self.scrollable_frame)
        buttons_frame.pack(fill="x", pady=(0, 15))
        
        # Boutons d'action
        export_button = ctk.CTkButton(
            buttons_frame,
            text="📊 Exporter CSV",
            command=self.exporter_csv,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        export_button.pack(side="left", padx=10, pady=10)
        
        refresh_button = ctk.CTkButton(
            buttons_frame,
            text="🔄 Actualiser",
            command=self.actualiser,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        refresh_button.pack(side="left", padx=10, pady=10)
        
        # Barre de recherche (juste au-dessus du tableau)
        self.creer_barre_recherche(self.scrollable_frame)
        
        # Frame pour le tableau
        tableau_frame = ctk.CTkFrame(self.scrollable_frame)
        tableau_frame.pack(fill="both", expand=True)
        
        # Tableau des véhicules achetés
        self.creer_tableau(tableau_frame)
    
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
    
    def creer_tableau(self, parent):
        """Crée le tableau des véhicules achetés"""
        # Frame pour le scrollbar avec hauteur minimale
        container = ctk.CTkFrame(parent)
        container.pack(fill="both", expand=True, padx=15, pady=15)
        container.configure(height=250)  # Hauteur minimale de 250px
        
        # Treeview (tableau)
        columns = ("lot", "marque", "modele", "annee", "prix_achat", "prix_revente", "marge", "date_achat")
        self.tree_achetes = ttk.Treeview(container, columns=columns, show="headings", height=8)  # Hauteur optimisée
        
        # Configuration du style pour agrandir la police
        style = ttk.Style()
        style.configure("Treeview", font=('Segoe UI', 25), rowheight=70)
        style.configure("Treeview.Heading", font=('Roboto', 25, 'bold'))
        
        # Configuration des colonnes
        headings = {
            "lot": "LOT",
            "marque": "MARQUE", 
            "modele": "MODÈLE",
            "annee": "ANNÉE",
            "prix_achat": "PRIX ACHAT",
            "prix_revente": "PRIX REVENTE",
            "marge": "MARGE",
            "date_achat": "DATE ACHAT"
        }
        
        for col, heading in headings.items():
            self.tree_achetes.heading(col, text=heading)
            if col in ["prix_achat", "prix_revente", "marge"]:
                self.tree_achetes.column(col, width=100, anchor="center")
            elif col in ["lot", "annee"]:
                self.tree_achetes.column(col, width=80, anchor="center")
            else:
                self.tree_achetes.column(col, width=120, anchor="w")
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree_achetes.yview)
        h_scrollbar = ttk.Scrollbar(container, orient="horizontal", command=self.tree_achetes.xview)
        
        self.tree_achetes.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Placement
        self.tree_achetes.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configuration du grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
    
    def actualiser(self):
        """Met à jour l'affichage des véhicules achetés"""
        # Effacer le tableau
        for item in self.tree_achetes.get_children():
            self.tree_achetes.delete(item)
        
        # Remplir avec les véhicules achetés
        vehicules_achetes = self.filtrer_vehicules(self.data_manager.vehicules_achetes)
        total_marge = 0
        total_investissement = 0
        
        for vehicule in vehicules_achetes:
            prix_achat = vehicule.get_prix_numerique('prix_achat')
            prix_revente = vehicule.get_prix_numerique('prix_revente')
            cout_reparations = vehicule.get_prix_numerique('cout_reparations')
            
            # Calcul des coûts totaux et de la marge
            cout_total = prix_achat + cout_reparations
            marge = prix_revente - cout_total
            
            # Couleur selon la rentabilité
            if cout_total <= prix_revente:
                tags = ("rentable",)    # Vert - rentable
            else:
                tags = ("non_rentable",)  # Rouge - à perte
            
            self.tree_achetes.insert("", "end", values=(
                vehicule.lot,
                vehicule.marque,
                vehicule.modele,
                vehicule.annee,
                f"{prix_achat:.0f}€",
                f"{prix_revente:.0f}€",
                f"{marge:+.0f}€",
                vehicule.date_achat if vehicule.date_achat else "N/A"
            ), tags=tags)
            
            total_marge += marge
            total_investissement += prix_achat
        
        # Configuration des couleurs (même logique que repérage)
        self.tree_achetes.tag_configure("rentable", background="#4CAF50", foreground="white")    # Vert avec texte blanc
        self.tree_achetes.tag_configure("non_rentable", background="#F44336", foreground="white") # Rouge avec texte blanc
        
        # Mise à jour des statistiques
        nb_achetes = len(vehicules_achetes)
        marge_moyenne = total_marge / nb_achetes if nb_achetes > 0 else 0
        
        stats_text = f"💰 {nb_achetes} véhicules achetés | Marge totale: {total_marge:+.0f}€ | Marge moyenne: {marge_moyenne:+.0f}€ | Investissement: {total_investissement:.0f}€"
        self.label_stats.configure(text=stats_text)
    
    def exporter_csv(self):
        """Exporte les données vers un fichier CSV"""
        try:
            from tkinter import filedialog
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Fichiers CSV", "*.csv")],
                title="Exporter les véhicules achetés"
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                    writer = csv.writer(csvfile, delimiter=';')
                    
                    # En-têtes
                    writer.writerow([
                        "N° LOT", "MARQUE", "MODÈLE", "ANNÉE", "PRIX ACHAT", 
                        "PRIX REVENTE", "MARGE", "DATE ACHAT", "KM", "RÉPARATIONS"
                    ])
                    
                    # Données
                    for vehicule in self.data_manager.vehicules_achetes:
                        writer.writerow([
                            vehicule.lot,
                            vehicule.marque,
                            vehicule.modele,
                            vehicule.annee,
                            vehicule.prix_achat,
                            vehicule.prix_revente,
                            f"{vehicule.calculer_marge():.0f}",
                            vehicule.date_achat if vehicule.date_achat else "",
                            vehicule.kilometrage,
                            vehicule.chose_a_faire
                        ])
                
                messagebox.showinfo("✅ Succès", f"Export réussi vers:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de l'export: {e}")

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