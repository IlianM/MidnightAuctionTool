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
        columns = ("lot", "marque", "modele", "annee", "prix_achat", "prix_max", "prix_vente_final", "marge_euro", "marge_pourcent", "date_achat")
        self.tree_achetes = ttk.Treeview(container, columns=columns, show="headings", height=10)
        
        # Configuration du style
        self.configurer_style_tableau()
        
        # Variables pour le tri
        self.tri_actuel = {'colonne': None, 'sens': 'asc'}  # 'asc' ou 'desc'
        
        # Configuration des colonnes
        headings = {
            "lot": "LOT ↕",
            "marque": "MARQUE ↕",
            "modele": "MODÈLE ↕",
            "annee": "ANNÉE ↕",
            "prix_achat": "PRIX ACHAT ↕",
            "prix_max": "PRIX MAX ↕",
            "prix_vente_final": "PRIX VENTE ↕",
            "marge_euro": "MARGE €",
            "marge_pourcent": "MARGE %",
            "date_achat": "DATE ACHAT ↕"
        }
        
        for col, heading in headings.items():
            self.tree_achetes.heading(col, text=heading)
            
            # Ajouter le callback de tri pour les colonnes avec ↕
            if "↕" in heading:
                self.tree_achetes.heading(col, command=lambda c=col: self.trier_par_colonne(c))
            
            # Largeurs des colonnes
            if col == "lot":
                self.tree_achetes.column(col, width=80, anchor="center")
            elif col in ["marque", "modele"]:
                self.tree_achetes.column(col, width=120, anchor="w")
            elif col == "annee":
                self.tree_achetes.column(col, width=80, anchor="center")
            elif col in ["prix_achat", "prix_max", "prix_vente_final"]:
                self.tree_achetes.column(col, width=110, anchor="center")
            elif col in ["marge_euro", "marge_pourcent"]:
                self.tree_achetes.column(col, width=100, anchor="center")
            elif col == "date_achat":
                self.tree_achetes.column(col, width=100, anchor="center")
            else:
                self.tree_achetes.column(col, width=100, anchor="center")
        
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
        
        # Configuration des tags de couleur (MODIFIÉS pour nouvelles couleurs utilisateur)
        self.tree_achetes.tag_configure('couleur_turquoise', background='#1ABC9C', foreground='white')
        self.tree_achetes.tag_configure('couleur_vert', background='#2ECC71', foreground='white')
        self.tree_achetes.tag_configure('couleur_orange', background='#F39C12', foreground='white')
        self.tree_achetes.tag_configure('couleur_rouge', background='#E74C3C', foreground='white')
        
        # Tags pour la rentabilité (garde certains pour les besoins spéciaux)
        self.tree_achetes.tag_configure('en_attente', background='#F39C12', foreground='white')  # Orange pour en attente
        self.tree_achetes.tag_configure('rentable', background='#2ECC71', foreground='white')    # Vert pour rentable
        self.tree_achetes.tag_configure('non_rentable', background='#E74C3C', foreground='white')  # Rouge pour perte
        
        # Bind pour édition au double-clic (MODIFIÉ pour popup sur lot)
        self.tree_achetes.bind("<Double-1>", self.on_double_click)
        
        # Variables d'édition inline
        self.edit_entry = None
        self.editing_item = None
        self.editing_column = None
        
        # Ajouter tooltip au tableau
        ajouter_tooltip(self.tree_achetes, """Tableau des véhicules achetés avec indication de rentabilité :
• Couleur selon choix utilisateur + indication de rentabilité
• Double-clic sur LOT pour voir les détails complets
• Double-clic sur autre colonne pour modifier
• Marge calculée automatiquement""")
    
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
        
        # Remplir avec les véhicules achetés filtrés
        vehicules_achetes = self.filtrer_vehicules(self.data_adapter.vehicules_achetes)
        vehicules_achetes = self.appliquer_tri(vehicules_achetes)
        
        for vehicule in vehicules_achetes:
            # Calculer la marge RÉELLE (seulement si prix vente final renseigné)
            marge_euros = vehicule.calculer_marge()
            marge_pourcentage = vehicule.calculer_marge_pourcentage()
            
            # Formatage des marges
            if vehicule.get_prix_numerique('prix_vente_final') > 0:
                # Véhicule vendu - vraie marge
                marge_euro_str = f"{marge_euros:+.0f}€"
                marge_pourcent_str = f"{marge_pourcentage:+.1f}%"
                tag_rentabilite = "rentable" if marge_euros >= 0 else "non_rentable"
            else:
                # Véhicule pas encore vendu
                marge_euro_str = "En attente"
                marge_pourcent_str = "En attente"
                tag_rentabilite = "en_attente"
            
            # Utiliser la couleur choisie par l'utilisateur avec indication de rentabilité
            tag_couleur = vehicule.get_tag_couleur()
            tags = (tag_couleur, tag_rentabilite)
            
            if self.tree_achetes and self.tree_achetes.winfo_exists():
                self.tree_achetes.insert("", "end", values=(
                    vehicule.lot,
                    vehicule.marque,
                    vehicule.modele,
                    vehicule.annee,
                    f"{vehicule.prix_achat}€" if vehicule.prix_achat else "0€",
                    vehicule.prix_max_achat or "N/A",
                    f"{vehicule.prix_vente_final}€" if vehicule.prix_vente_final else "",
                    marge_euro_str,
                    marge_pourcent_str,
                    vehicule.date_achat
                ), tags=tags)
        
        # Mettre à jour les statistiques
        self.mettre_a_jour_stats()
    
    def arreter_auto_refresh(self):
        """Arrête l'actualisation automatique"""
        self.auto_refresh_enabled = False

    def actualiser(self):
        """Met à jour l'affichage du tableau"""
        # Effacer le tableau
        for item in self.tree_achetes.get_children():
            self.tree_achetes.delete(item)
        
        # Remplir avec les véhicules achetés filtrés
        vehicules_achetes = self.filtrer_vehicules(self.data_adapter.vehicules_achetes)
        vehicules_achetes = self.appliquer_tri(vehicules_achetes)
        
        for vehicule in vehicules_achetes:
            # Calculer la marge RÉELLE (seulement si prix vente final renseigné)
            marge_euros = vehicule.calculer_marge()
            marge_pourcentage = vehicule.calculer_marge_pourcentage()
            
            # Formatage des marges
            if vehicule.get_prix_numerique('prix_vente_final') > 0:
                # Véhicule vendu - vraie marge
                marge_euro_str = f"{marge_euros:+.0f}€"
                marge_pourcent_str = f"{marge_pourcentage:+.1f}%"
                tag_rentabilite = "rentable" if marge_euros >= 0 else "non_rentable"
            else:
                # Véhicule pas encore vendu
                marge_euro_str = "En attente"
                marge_pourcent_str = "En attente"
                tag_rentabilite = "en_attente"
            
            # Utiliser la couleur choisie par l'utilisateur avec indication de rentabilité
            tag_couleur = vehicule.get_tag_couleur()
            tags = (tag_couleur, tag_rentabilite)
            
            self.tree_achetes.insert("", "end", values=(
                vehicule.lot,
                vehicule.marque,
                vehicule.modele,
                vehicule.annee,
                f"{vehicule.prix_achat}€" if vehicule.prix_achat else "0€",
                vehicule.prix_max_achat or "N/A",
                f"{vehicule.prix_vente_final}€" if vehicule.prix_vente_final else "",
                marge_euro_str,
                marge_pourcent_str,
                vehicule.date_achat
            ), tags=tags)
        
        # Configuration des couleurs pour les tags de couleurs utilisateur
        self.tree_achetes.tag_configure('couleur_turquoise', background='#1ABC9C', foreground='white')
        self.tree_achetes.tag_configure('couleur_vert', background='#2ECC71', foreground='white')
        self.tree_achetes.tag_configure('couleur_orange', background='#F39C12', foreground='white')
        self.tree_achetes.tag_configure('couleur_rouge', background='#E74C3C', foreground='white')
        
        # Surcharge pour indication de rentabilité (priorité sur couleur utilisateur)
        self.tree_achetes.tag_configure("rentable", background="#4CAF50", foreground="white")    # Vert pour rentable
        self.tree_achetes.tag_configure("non_rentable", background="#F44336", foreground="white") # Rouge pour perte
        self.tree_achetes.tag_configure("en_attente", background="#FF9800", foreground="white")  # Orange pour en attente
        
        # Mettre à jour les statistiques
        self.mettre_a_jour_stats()
        
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
                        "PRIX MAX", "PRIX VENTE", "MARGE €", "MARGE %", "DATE ACHAT", "KM", "MOTORISATION"
                    ])
                    
                    # Données
                    for vehicule in self.data_adapter.vehicules_achetes:
                        marge_euros = vehicule.calculer_marge()
                        marge_pourcentage = vehicule.calculer_marge_pourcentage()
                        
                        writer.writerow([
                            vehicule.lot,
                            vehicule.marque,
                            vehicule.modele,
                            vehicule.annee,
                            vehicule.prix_achat,
                            vehicule.prix_max_achat,
                            vehicule.prix_revente,
                            f"{marge_euros:+.0f}",
                            f"{marge_pourcentage:+.1f}",
                            vehicule.date_achat if vehicule.date_achat else "",
                            vehicule.kilometrage,
                            vehicule.motorisation
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
                    ["LOT", "MARQUE", "MODÈLE", "ANNÉE", "PRIX ACHAT", "PRIX VENTE", "MARGE", "DATE"]
                ]
                
                for vehicule in self.data_adapter.vehicules_achetes:
                    prix_achat = vehicule.get_prix_numerique('prix_achat')
                    prix_revente = vehicule.get_prix_numerique('prix_revente')
                    cout_reparations = vehicule.get_prix_numerique('cout_reparations')
                    
                    # Fonction pour formater avec retour à la ligne
                    def formater_cellule(texte, max_chars=12):
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
                    
                    # Calcul de la marge
                    if prix_revente > 0:
                        marge = prix_revente - prix_achat - cout_reparations
                        marge_str = f"{marge:+.0f}€"
                        prix_revente_str = f"{prix_revente:.0f}€"
                    else:
                        marge_str = "En attente"
                        prix_revente_str = "-"
                    
                    # Formater la date
                    date_formatee = vehicule.date_achat if vehicule.date_achat else "N/A"
                    if len(date_formatee) > 8:
                        date_formatee = date_formatee[:8] + "..."
                    
                    data.append([
                        vehicule.lot,
                        formater_cellule(vehicule.marque, 10),
                        formater_cellule(vehicule.modele, 10),
                        vehicule.annee,
                        f"{prix_achat:.0f}€",
                        prix_revente_str,
                        marge_str,
                        date_formatee
                    ])
                
                # Créer le tableau avec largeurs adaptées
                table = Table(data, colWidths=[
                    0.6*inch,  # LOT
                    0.9*inch,  # MARQUE  
                    0.9*inch,  # MODÈLE
                    0.6*inch,  # ANNÉE
                    0.8*inch,  # PRIX ACHAT
                    0.8*inch,  # PRIX VENTE
                    0.8*inch,  # MARGE
                    0.7*inch   # DATE
                ])
                
                # Style du tableau
                table.setStyle(TableStyle([
                    # En-tête
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 8),  # Police plus petite pour en-têtes
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    
                    # Corps du tableau
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 7),  # Police plus petite pour contenu
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Grille plus fine
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Alignement vertical en haut
                    
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
        """Gestion du double-clic : popup info pour le lot, édition pour les autres colonnes"""
        try:
            # Fermer l'édition précédente si elle existe
            self.finish_edit()
            
            # Identifier l'élément et la colonne cliqués
            item = self.tree_achetes.identify_row(event.y)
            column = self.tree_achetes.identify_column(event.x)
            
            if not item or column == "#0":
                return
            
            # Vérifier si c'est la colonne du lot (première colonne)
            col_index = int(column.replace('#', '')) - 1
            if col_index == 0:  # Colonne lot
                # Afficher la popup d'informations
                index = self.tree_achetes.index(item)
                vehicules_affiches = self.filtrer_vehicules(self.data_adapter.vehicules_achetes)
                
                if 0 <= index < len(vehicules_affiches):
                    vehicule = vehicules_affiches[index]
                    from utils.dialogs import afficher_info_vehicule
                    afficher_info_vehicule(self.parent.winfo_toplevel(), vehicule)
                return
            
            # Pour les autres colonnes, procéder à l'édition normale
            columns_names = ["lot", "marque", "modele", "annee", "prix_achat", "prix_max", "prix_vente_final", "marge_euro", "marge_pourcent", "date_achat"]
            
            if 0 <= col_index < len(columns_names):
                col_name = columns_names[col_index]
                
                # INTERDIRE l'édition des colonnes marge (calculées automatiquement)
                if col_name in ["marge_euro", "marge_pourcent"]:
                    messagebox.showinfo("Information", "La marge est calculée automatiquement.\nModifiez le prix d'achat, prix de vente final ou coût des réparations pour la changer.")
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
            
            # Créer le widget d'édition
            self.edit_entry = tk.Entry(self.tree_achetes, font=('Segoe UI', 20))
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
            vehicules_affiches = self.filtrer_vehicules(self.data_adapter.vehicules_achetes)
            vehicules_tries = self.appliquer_tri(vehicules_affiches)
            
            if 0 <= index < len(vehicules_tries):
                vehicule = vehicules_tries[index]
            
                # Récupérer le nom de la colonne
                columns_names = ["lot", "marque", "modele", "annee", "prix_achat", "prix_max", "prix_vente_final", "marge_euro", "marge_pourcent", "date_achat"]
                col_index = int(self.editing_column.replace('#', '')) - 1
                
                if 0 <= col_index < len(columns_names):
                    col_name = columns_names[col_index]
                    
                    # Mapper les noms de colonnes vers les attributs
                    if col_name == "prix_max":
                        setattr(vehicule, "prix_max_achat", new_value)
                    else:
                        # Mettre à jour le véhicule directement
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

    def mettre_a_jour_stats(self):
        """Met à jour les statistiques affichées"""
        try:
            vehicules_achetes = self.filtrer_vehicules(self.data_adapter.vehicules_achetes)
            nb_achetes = len(vehicules_achetes)
            marge_moyenne = self.calculer_marge_moyenne(vehicules_achetes)
            
            stats_text = f"💰 {nb_achetes} véhicules achetés | Marge totale: {self.calculer_marge_totale(vehicules_achetes):+.0f}€ | Marge moyenne: {marge_moyenne:+.0f}€ | Investissement: {self.calculer_investissement_total(vehicules_achetes):.0f}€"
            if hasattr(self, 'label_stats') and self.label_stats.winfo_exists():
                self.label_stats.configure(text=stats_text)
        except Exception as e:
            print(f"⚠️ Erreur mise à jour stats: {e}")
    
    def calculer_marge_totale(self, vehicules):
        """Calcule la marge totale des véhicules achetés"""
        return sum(v.calculer_marge() for v in vehicules)
    
    def calculer_marge_moyenne(self, vehicules):
        """Calcule la marge moyenne des véhicules achetés"""
        if not vehicules:
            return 0.0
        return self.calculer_marge_totale(vehicules) / len(vehicules)
    
    def calculer_investissement_total(self, vehicules):
        """Calcule l'investissement total des véhicules achetés"""
        return sum(v.get_prix_numerique('prix_achat') for v in vehicules)
    
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
        
        # Actualiser l'affichage avec le tri
        self.actualiser()
    
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
            'prix_achat': 'prix_achat',
            'prix_max': 'prix_max_achat',
            'prix_vente_final': 'prix_vente_final',
            'date_achat': 'date_achat'
        }
        
        attribut = attribut_map.get(colonne)
        if not attribut:
            return vehicules
        
        def get_sort_key(vehicule):
            """Fonction pour récupérer la clé de tri"""
            valeur = getattr(vehicule, attribut, '')
            
            # Traitement spécial selon le type de donnée
            if colonne in ['prix_achat', 'prix_max', 'prix_vente_final']:
                # Valeurs numériques
                try:
                    return float(str(valeur).replace('€', '').replace(',', '.').strip()) if valeur else 0
                except:
                    return 0
            elif colonne == 'annee':
                # Années
                try:
                    return int(str(valeur)) if valeur else 0
                except:
                    return 0
            else:
                # Texte (insensible à la casse)
                return str(valeur).lower() if valeur else ''
        
        return sorted(vehicules, key=get_sort_key, reverse=sens_inverse) 