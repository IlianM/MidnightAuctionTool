#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Onglet véhicules achetés - CustomTkinter
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
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

class AchetesTab:
    """Onglet véhicules achetés avec CustomTkinter"""
    
    def __init__(self, parent, settings: AppSettings, data_adapter, 
                 style_manager, on_data_changed=None):
        self.parent = parent
        self.settings = settings
        self.data_adapter = data_adapter  # Nouveau nom pour le gestionnaire de données
        self.style_manager = style_manager
        self.on_data_changed = on_data_changed
        
        # Variables d'interface
        self.tree_achetes = None
        
        # Variables pour l'actualisation automatique
        self.auto_refresh_enabled = True
        self.auto_refresh_interval = 500  # 5 secondes
        self.last_data_hash = None
        
        # Créer l'interface directement dans le parent (onglet du TabView)
        self.creer_interface()
        
        # Démarrer l'actualisation automatique
        self.demarrer_auto_refresh()
    
    def creer_interface(self):
        """Crée l'interface de l'onglet achetés avec CustomTkinter"""
        # Créer un scrollable frame directement dans le parent
        self.scrollable_frame = ctk.CTkScrollableFrame(self.parent)
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
        
        # Ajouter tooltip aux statistiques
        ajouter_tooltip(self.label_stats, "Statistiques automatiques calculées à partir des véhicules achetés : nombre total, marge totale, marge moyenne et investissement total.")
        
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
        ajouter_tooltip(export_button, TOOLTIPS['btn_export_csv'])
        
        # Bouton export PDF
        export_pdf_button = ctk.CTkButton(
            buttons_frame,
            text="📄 Exporter PDF",
            command=self.exporter_pdf,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        export_pdf_button.pack(side="left", padx=10, pady=10)
        ajouter_tooltip(export_pdf_button, "Exporter les véhicules achetés vers un document PDF professionnel")
        
        refresh_button = ctk.CTkButton(
            buttons_frame,
            text="🔄 Actualiser",
            command=self.actualiser,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        refresh_button.pack(side="right", padx=15, pady=10)
        ajouter_tooltip(refresh_button, "Met à jour l'affichage des véhicules achetés et recalcule les statistiques.")
        
        # Barre de recherche (juste au-dessus du tableau)
        self.creer_barre_recherche(self.scrollable_frame)
        
        # Frame pour le tableau
        tableau_frame = ctk.CTkFrame(self.scrollable_frame)
        tableau_frame.pack(fill="both", expand=True)
        
        # Tableau des véhicules achetés
        self.creer_tableau(tableau_frame)
        
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
        ajouter_tooltip(self.entry_recherche, "Recherche instantanée parmi les véhicules achetés par numéro de lot, marque ou modèle.")
        ajouter_tooltip(clear_button, "Efface le texte de recherche et affiche tous les véhicules achetés.")
    
    def creer_tableau(self, parent):
        """Crée le tableau des véhicules achetés"""
        # Frame pour le scrollbar avec hauteur minimale
        container = ctk.CTkFrame(parent)
        container.pack(fill="both", expand=True, padx=15, pady=15)
        container.configure(height=250)  # Hauteur minimale de 250px
        
        # Treeview (tableau) avec description et prix de revente vide pour véhicules fraîchement achetés
        columns = ("lot", "marque", "modele", "annee", "prix_achat", "prix_revente", "description_reparations", "marge", "date_achat")
        self.tree_achetes = ttk.Treeview(container, columns=columns, show="headings", height=8)  # Hauteur optimisée
        
        # Configuration du style pour agrandir la police
        style = ttk.Style()
        style.configure("Treeview", font=('Segoe UI', 20), rowheight=50)  # Police normale pour cohérence
        style.configure("Treeview.Heading", font=('Segoe UI', 16, 'bold'))  # Police plus petite pour les en-têtes
        
        # Configuration des colonnes
        headings = {
            "lot": "LOT",
            "marque": "MARQUE", 
            "modele": "MODÈLE",
            "annee": "ANNÉE",
            "prix_achat": "PRIX ACHAT",
            "prix_revente": "PRIX REVENTE",
            "description_reparations": "DESCRIPTION RÉPAR",  # NOUVEAU
            "marge": "MARGE",
            "date_achat": "DATE ACHAT"
        }
        
        for col, heading in headings.items():
            self.tree_achetes.heading(col, text=heading)
            if col in ["prix_achat", "prix_revente", "marge"]:
                self.tree_achetes.column(col, width=100, anchor="center")
            elif col in ["lot", "annee"]:
                self.tree_achetes.column(col, width=80, anchor="center")
            elif col == "description_reparations":
                self.tree_achetes.column(col, width=200, anchor="w")  # Plus large pour la description
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
        
        # Bind pour édition au double-clic
        self.tree_achetes.bind("<Double-1>", self.on_double_click)
        
        # Variables d'édition inline
        self.edit_entry = None
        self.editing_item = None
        self.editing_column = None
        
        # Ajouter tooltip au tableau
        ajouter_tooltip(self.tree_achetes, """Tableau des véhicules achetés avec indication de rentabilité :
• Fond ORANGE = véhicule acheté, en attente de vente
• Fond VERT = achat rentable (marge positive)
• Fond ROUGE = achat à perte (marge négative)
• Double-clic pour modifier les cellules (sauf marge qui est automatique)""")
    
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
            print(f"⚠️ Erreur auto-refresh achetés: {e}")
            if self.auto_refresh_enabled and hasattr(self.parent, 'winfo_exists') and self.parent.winfo_exists():
                self.parent.after(self.auto_refresh_interval, self.auto_refresh)
    
    def calculer_hash_donnees(self):
        """Calcule un hash des données pour détecter les changements"""
        try:
            # Créer une représentation des données importantes
            data_repr = []
            
            # Ajouter les véhicules achetés
            for v in self.data_adapter.vehicules_achetes:
                data_repr.append(f"{v.lot}|{v.marque}|{v.modele}|{v.prix_revente}|{v.prix_achat}|{v.cout_reparations}")
            
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
        if self.tree_achetes and self.tree_achetes.winfo_exists():
            for item in self.tree_achetes.get_children():
                self.tree_achetes.delete(item)
        
        # Remplir avec les véhicules achetés
        vehicules_achetes = self.filtrer_vehicules(self.data_adapter.vehicules_achetes)
        total_marge = 0
        total_investissement = 0
        
        for vehicule in vehicules_achetes:
            prix_achat = vehicule.get_prix_numerique('prix_achat')
            prix_revente = vehicule.get_prix_numerique('prix_revente')
            cout_reparations = vehicule.get_prix_numerique('cout_reparations')
            
            # Vérifier si le véhicule a un prix de revente renseigné
            prix_revente_renseigne = vehicule.prix_revente and vehicule.prix_revente.strip() and vehicule.prix_revente != "0"
            
            if not prix_revente_renseigne:  # Véhicule acheté mais pas encore vendu
                marge_affichage = "En attente"
                tags = ("en_attente",)
                marge = 0  # Pour les stats
                prix_revente_affichage = ""  # Vide dans le tableau
            else:
                # Véhicule vendu, calcul de la marge réelle
                cout_total = prix_achat + cout_reparations
                marge = prix_revente - cout_total
                marge_affichage = f"{marge:+.0f}€"
                prix_revente_affichage = f"{prix_revente:.0f}€"
                
                # Couleur selon la rentabilité
                if marge >= 0:
                    tags = ("rentable",)    # Vert - rentable
                else:
                    tags = ("non_rentable",)  # Rouge - à perte
            
            if self.tree_achetes and self.tree_achetes.winfo_exists():
                self.tree_achetes.insert("", "end", values=(
                    vehicule.lot,
                    vehicule.marque,
                    vehicule.modele,
                    vehicule.annee,
                    f"{prix_achat:.0f}€",
                    prix_revente_affichage,  # Vide si pas vendu
                    vehicule.chose_a_faire,  # Description des réparations
                    marge_affichage,
                    vehicule.date_achat if vehicule.date_achat else "N/A"
                ), tags=tags)
            
            total_marge += marge
            total_investissement += prix_achat
        
        # Configuration des couleurs
        if self.tree_achetes and self.tree_achetes.winfo_exists():
            self.tree_achetes.tag_configure("rentable", background="#4CAF50", foreground="white")
            self.tree_achetes.tag_configure("non_rentable", background="#F44336", foreground="white")
            self.tree_achetes.tag_configure("en_attente", background="#FF9800", foreground="white")  # Orange pour en attente
        
        # Mise à jour des statistiques
        nb_achetes = len(vehicules_achetes)
        marge_moyenne = total_marge / nb_achetes if nb_achetes > 0 else 0
        
        stats_text = f"💰 {nb_achetes} véhicules achetés | Marge totale: {total_marge:+.0f}€ | Marge moyenne: {marge_moyenne:+.0f}€ | Investissement: {total_investissement:.0f}€"
        if hasattr(self, 'label_stats') and self.label_stats.winfo_exists():
            self.label_stats.configure(text=stats_text)
    
    def arreter_auto_refresh(self):
        """Arrête l'actualisation automatique"""
        self.auto_refresh_enabled = False

    def actualiser(self):
        """Met à jour l'affichage des véhicules achetés"""
        # Effacer le tableau
        for item in self.tree_achetes.get_children():
            self.tree_achetes.delete(item)
        
        # Remplir avec les véhicules achetés
        vehicules_achetes = self.filtrer_vehicules(self.data_adapter.vehicules_achetes)
        total_marge = 0
        total_investissement = 0
        
        for vehicule in vehicules_achetes:
            prix_achat = vehicule.get_prix_numerique('prix_achat')
            prix_revente = vehicule.get_prix_numerique('prix_revente')
            cout_reparations = vehicule.get_prix_numerique('cout_reparations')
            
            # Vérifier si le véhicule a un prix de revente renseigné
            prix_revente_renseigne = vehicule.prix_revente and vehicule.prix_revente.strip() and vehicule.prix_revente != "0"
            
            if not prix_revente_renseigne:  # Véhicule acheté mais pas encore vendu
                marge_affichage = "En attente"
                tags = ("en_attente",)
                marge = 0  # Pour les stats
                prix_revente_affichage = ""  # Vide dans le tableau
            else:
                # Véhicule vendu, calcul de la marge réelle
                cout_total = prix_achat + cout_reparations
                marge = prix_revente - cout_total
                marge_affichage = f"{marge:+.0f}€"
                prix_revente_affichage = f"{prix_revente:.0f}€"
                
                # Couleur selon la rentabilité
                if marge >= 0:
                    tags = ("rentable",)    # Vert - rentable
                else:
                    tags = ("non_rentable",)  # Rouge - à perte
            
            self.tree_achetes.insert("", "end", values=(
                vehicule.lot,
                vehicule.marque,
                vehicule.modele,
                vehicule.annee,
                f"{prix_achat:.0f}€",
                prix_revente_affichage,  # Vide si pas vendu
                vehicule.chose_a_faire,  # Description des réparations
                marge_affichage,
                vehicule.date_achat if vehicule.date_achat else "N/A"
            ), tags=tags)
            
            total_marge += marge
            total_investissement += prix_achat
        
        # Configuration des couleurs (même logique que repérage)
        self.tree_achetes.tag_configure("rentable", background="#4CAF50", foreground="white")    # Vert avec texte blanc
        self.tree_achetes.tag_configure("non_rentable", background="#F44336", foreground="white") # Rouge avec texte blanc
        self.tree_achetes.tag_configure("en_attente", background="#FF9800", foreground="white")  # Orange pour en attente
        
        # Mise à jour des statistiques
        nb_achetes = len(vehicules_achetes)
        marge_moyenne = total_marge / nb_achetes if nb_achetes > 0 else 0
        
        stats_text = f"💰 {nb_achetes} véhicules achetés | Marge totale: {total_marge:+.0f}€ | Marge moyenne: {marge_moyenne:+.0f}€ | Investissement: {total_investissement:.0f}€"
        self.label_stats.configure(text=stats_text)
        
        # Mettre à jour le hash pour l'auto-refresh
        self.last_data_hash = self.calculer_hash_donnees()

    def exporter_csv(self):
        """Exporte les données vers un fichier CSV"""
        try:
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
                        "PRIX REVENTE", "DESCRIPTION RÉPARATIONS", "MARGE", "DATE ACHAT", "KM"
                    ])
                    
                    # Données
                    for vehicule in self.data_adapter.vehicules_achetes:
                        writer.writerow([
                            vehicule.lot,
                            vehicule.marque,
                            vehicule.modele,
                            vehicule.annee,
                            vehicule.prix_achat,
                            "",  # Prix de revente vide
                            vehicule.chose_a_faire,  # Description des réparations
                            f"{vehicule.calculer_marge():.0f}",
                            vehicule.date_achat if vehicule.date_achat else "",
                            vehicule.kilometrage
                        ])
                
                messagebox.showinfo("✅ Succès", f"Export réussi vers:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de l'export: {e}")

    def exporter_pdf(self):
        """Exporte les données vers un fichier PDF professionnel"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Fichiers PDF", "*.pdf")],
                title="Exporter les véhicules achetés en PDF"
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
                    textColor=colors.HexColor('#2E86AB'),
                    spaceAfter=30,
                    alignment=1  # Centré
                )
                
                # Récupérer le nom de la journée
                journee_nom = "Enchère"
                if hasattr(self.data_adapter, 'journee') and self.data_adapter.journee:
                    journee_nom = self.data_adapter.journee.nom
                
                # Titre principal
                titre = f"🏆 RAPPORT VÉHICULES ACHETÉS - {journee_nom.upper()}"
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
                nb_achetes = len(self.data_adapter.vehicules_achetes)
                total_investissement = sum(v.get_prix_numerique('prix_achat') for v in self.data_adapter.vehicules_achetes)
                total_marge = sum(v.get_prix_numerique('prix_revente') - v.get_prix_numerique('prix_achat') - v.get_prix_numerique('cout_reparations') 
                                for v in self.data_adapter.vehicules_achetes if v.prix_revente and v.prix_revente.strip())
                marge_moyenne = total_marge / nb_achetes if nb_achetes > 0 else 0
                
                stats_text = f"""
                <b>📊 STATISTIQUES</b><br/>
                • Nombre de véhicules achetés : <b>{nb_achetes}</b><br/>
                • Investissement total : <b>{total_investissement:,.0f}€</b><br/>
                • Marge totale : <b>{total_marge:+,.0f}€</b><br/>
                • Marge moyenne : <b>{marge_moyenne:+,.0f}€</b>
                """
                
                stats_style = ParagraphStyle(
                    'StatsStyle',
                    parent=styles['Normal'],
                    fontSize=12,
                    spaceAfter=30,
                    backColor=colors.HexColor('#F5F5F5'),
                    borderColor=colors.HexColor('#2E86AB'),
                    borderWidth=1,
                    borderPadding=10
                )
                elements.append(Paragraph(stats_text, stats_style))
                elements.append(Spacer(1, 20))
                
                # Titre du tableau
                table_title = Paragraph("<b>📋 DÉTAIL DES VÉHICULES</b>", styles['Heading2'])
                elements.append(table_title)
                elements.append(Spacer(1, 10))
                
                # Données du tableau
                data = [
                    ["LOT", "MARQUE", "MODÈLE", "ANNÉE", "PRIX ACHAT", "PRIX REVENTE", "MARGE", "DATE ACHAT"]
                ]
                
                for vehicule in self.data_adapter.vehicules_achetes:
                    prix_achat = vehicule.get_prix_numerique('prix_achat')
                    prix_revente = vehicule.get_prix_numerique('prix_revente')
                    cout_reparations = vehicule.get_prix_numerique('cout_reparations')
                    
                    # Calcul de la marge
                    if prix_revente > 0:
                        marge = prix_revente - prix_achat - cout_reparations
                        marge_str = f"{marge:+.0f}€"
                        prix_revente_str = f"{prix_revente:.0f}€"
                    else:
                        marge_str = "En attente"
                        prix_revente_str = "-"
                    
                    data.append([
                        vehicule.lot,
                        vehicule.marque,
                        vehicule.modele,
                        vehicule.annee,
                        f"{prix_achat:.0f}€",
                        prix_revente_str,
                        marge_str,
                        vehicule.date_achat if vehicule.date_achat else "N/A"
                    ])
                
                # Créer le tableau
                table = Table(data, colWidths=[0.8*inch, 1.2*inch, 1.2*inch, 0.8*inch, 1*inch, 1*inch, 1*inch, 1*inch])
                
                # Style du tableau
                table.setStyle(TableStyle([
                    # En-tête
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
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
                
                # Pied de page
                elements.append(Spacer(1, 30))
                footer_style = ParagraphStyle(
                    'FooterStyle',
                    parent=styles['Normal'],
                    fontSize=8,
                    textColor=colors.grey,
                    alignment=1
                )
                footer_text = f"Gestionnaire d'Enchères - Rapport généré automatiquement - {date_rapport}"
                elements.append(Paragraph(footer_text, footer_style))
                
                # Construire le document
                doc.build(elements)
                
                messagebox.showinfo("✅ Succès", f"Export PDF réussi vers:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de l'export PDF: {e}")

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

    def on_double_click(self, event):
        """Démarre l'édition inline sur double-clic"""
        try:
            # Fermer l'édition précédente si elle existe
            self.finish_edit()
            
            # Identifier l'élément et la colonne cliqués
            item = self.tree_achetes.identify_row(event.y)
            column = self.tree_achetes.identify_column(event.x)
            
            if not item or column == "#0":
                return
            
            # Vérifier si la colonne peut être éditée
            col_index = int(column.replace('#', '')) - 1
            columns_names = ["lot", "marque", "modele", "annee", "prix_achat", "prix_revente", "description_reparations", "marge", "date_achat"]
            
            if 0 <= col_index < len(columns_names):
                col_name = columns_names[col_index]
                
                # INTERDIRE l'édition des colonnes marge et date_achat
                if col_name in ["marge", "date_achat"]:
                    if col_name == "marge":
                        messagebox.showinfo("Information", "La marge est calculée automatiquement.\nModifiez le prix de revente pour la changer.")
                    else:
                        messagebox.showinfo("Information", "La date d'achat est gérée automatiquement.")
                    return
            
            # Récupérer les coordonnées de la cellule
            bbox = self.tree_achetes.bbox(item, column)
            if not bbox:
                return
            
            # Stocker les informations d'édition
            self.editing_item = item
            self.editing_column = column
            
            # Récupérer la valeur actuelle
            values = self.tree_achetes.item(item)['values']
            current_value = values[col_index] if col_index < len(values) else ""
            
            # Créer le widget d'édition avec police normale
            self.edit_entry = tk.Entry(self.tree_achetes, font=('Segoe UI', 14))
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
            index = self.tree_achetes.index(self.editing_item)
            vehicule = self.data_adapter.vehicules_achetes[index]
            
            # Récupérer le nom de la colonne
            columns_names = ["lot", "marque", "modele", "annee", "prix_achat", "prix_revente", "description_reparations", "marge", "date_achat"]
            col_index = int(self.editing_column.replace('#', '')) - 1
            
            if 0 <= col_index < len(columns_names):
                col_name = columns_names[col_index]
                
                # Mapper description_reparations vers chose_a_faire dans le modèle
                if col_name == "description_reparations":
                    setattr(vehicule, "chose_a_faire", new_value)
                else:
                    # Mettre à jour le véhicule
                    setattr(vehicule, col_name, new_value)
                
                # Sauvegarder
                self.data_adapter.sauvegarder_donnees()
                
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