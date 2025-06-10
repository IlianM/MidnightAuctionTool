#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Onglet de recherche LeBonCoin pour l'application de gestion d'enchères
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
import threading
import queue
import sys
import os

# Ajouter le chemin du script de scraping
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'script_scraping_leboncoin'))

try:
    from leboncoin_scraper import LeboncoinScraper, DataAnalyzer
except ImportError:
    print("⚠️ Module leboncoin_scraper non trouvé. Vérifiez que le script est dans le dossier script_scraping_leboncoin")

from models.vehicule import Vehicule
from datetime import datetime

class RechercheTab:
    """Onglet de recherche LeBonCoin"""
    
    def __init__(self, parent, settings, data_adapter, style_manager, on_data_changed=None):
        self.parent = parent
        self.settings = settings
        self.data_adapter = data_adapter
        self.style_manager = style_manager
        self.on_data_changed = on_data_changed
        
        # Variables pour le threading
        self.recherche_en_cours = False
        self.thread_recherche = None
        self.queue_resultats = queue.Queue()
        
        # Variables de stockage des résultats
        self.resultats_annonces = []
        self.stats_prix = {}
        
        # Interface
        self.creer_interface()
        
        # Démarrer le processus de vérification des résultats
        self.verifier_resultats()
    
    def creer_interface(self):
        """Crée l'interface de l'onglet recherche"""
        # Frame principal avec scroll
        self.main_frame = ctk.CTkScrollableFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Titre
        titre = ctk.CTkLabel(
            self.main_frame,
            text="🔍 Recherche LeBonCoin",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        titre.pack(pady=(0, 20))
        
        # Frame des paramètres
        self.creer_frame_parametres()
        
        # Frame des résultats
        self.creer_frame_resultats()
    
    def creer_frame_parametres(self):
        """Crée la section des paramètres de recherche"""
        # Frame des paramètres
        params_frame = ctk.CTkFrame(self.main_frame)
        params_frame.pack(fill="x", pady=(0, 20))
        
        # Titre de la section
        params_title = ctk.CTkLabel(
            params_frame,
            text="📋 Paramètres de recherche",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        params_title.pack(pady=(15, 10))
        
        # Grid pour organiser les paramètres
        params_grid = ctk.CTkFrame(params_frame)
        params_grid.pack(fill="x", padx=20, pady=(0, 20))
        
        # Modèle
        ctk.CTkLabel(params_grid, text="🏷️ Modèle:", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, sticky="w", padx=(10, 5), pady=10
        )
        self.entry_modele = ctk.CTkEntry(params_grid, placeholder_text="Ex: BMW 118d", width=200)
        self.entry_modele.grid(row=0, column=1, padx=5, pady=10)
        
        # Année minimum
        ctk.CTkLabel(params_grid, text="📅 Année min:", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=2, sticky="w", padx=(20, 5), pady=10
        )
        self.entry_annee_min = ctk.CTkEntry(params_grid, placeholder_text="2011", width=80)
        self.entry_annee_min.grid(row=0, column=3, padx=5, pady=10)
        
        # Année maximum
        ctk.CTkLabel(params_grid, text="📅 Année max:", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=4, sticky="w", padx=(20, 5), pady=10
        )
        self.entry_annee_max = ctk.CTkEntry(params_grid, placeholder_text="2015", width=80)
        self.entry_annee_max.grid(row=0, column=5, padx=5, pady=10)
        
        # Kilométrage minimum
        ctk.CTkLabel(params_grid, text="🏃 Km min:", font=ctk.CTkFont(weight="bold")).grid(
            row=1, column=0, sticky="w", padx=(10, 5), pady=10
        )
        self.entry_km_min = ctk.CTkEntry(params_grid, placeholder_text="80000", width=100)
        self.entry_km_min.grid(row=1, column=1, padx=5, pady=10)
        
        # Kilométrage maximum
        ctk.CTkLabel(params_grid, text="🏃 Km max:", font=ctk.CTkFont(weight="bold")).grid(
            row=1, column=2, sticky="w", padx=(20, 5), pady=10
        )
        self.entry_km_max = ctk.CTkEntry(params_grid, placeholder_text="120000", width=100)
        self.entry_km_max.grid(row=1, column=3, padx=5, pady=10)
        
        # Nombre d'annonces
        ctk.CTkLabel(params_grid, text="📊 Nb annonces:", font=ctk.CTkFont(weight="bold")).grid(
            row=1, column=4, sticky="w", padx=(20, 5), pady=10
        )
        self.entry_nb_annonces = ctk.CTkEntry(params_grid, placeholder_text="50", width=80)
        self.entry_nb_annonces.grid(row=1, column=5, padx=5, pady=10)
        
        # Bouton de recherche
        self.btn_rechercher = ctk.CTkButton(
            params_frame,
            text="🔍 Lancer la recherche",
            command=self.lancer_recherche,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=200
        )
        self.btn_rechercher.pack(pady=(0, 20))
        
        # Barre de progression
        self.progress_bar = ctk.CTkProgressBar(params_frame, width=400)
        self.progress_bar.pack(pady=(0, 10))
        self.progress_bar.set(0)
        
        # Label de statut
        self.label_statut = ctk.CTkLabel(
            params_frame,
            text="Prêt à rechercher",
            font=ctk.CTkFont(size=12)
        )
        self.label_statut.pack(pady=(0, 15))
    
    def creer_frame_resultats(self):
        """Crée la section d'affichage des résultats"""
        # Frame des résultats
        resultats_frame = ctk.CTkFrame(self.main_frame)
        resultats_frame.pack(fill="both", expand=True)
        
        # Titre de la section
        resultats_title = ctk.CTkLabel(
            resultats_frame,
            text="📊 Résultats de recherche",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        resultats_title.pack(pady=(15, 10))
        
        # Frame pour les statistiques
        self.stats_frame = ctk.CTkFrame(resultats_frame)
        self.stats_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Tableau des résultats
        self.creer_tableau_resultats(resultats_frame)
        
        # Frame des actions
        self.creer_frame_actions(resultats_frame)
    
    def creer_tableau_resultats(self, parent):
        """Crée le tableau des résultats"""
        # Frame pour le tableau
        tableau_frame = ctk.CTkFrame(parent)
        tableau_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Créer le treeview avec style
        style = ttk.Style()
        style.theme_use("clam")
        
        # Colonnes du tableau
        columns = ("Titre", "Prix", "Année", "Kilométrage", "Lien")
        
        self.treeview = ttk.Treeview(
            tableau_frame,
            columns=columns,
            show="headings",
            height=15
        )
        
        # Configuration des en-têtes
        self.treeview.heading("Titre", text="🚗 Titre")
        self.treeview.heading("Prix", text="💰 Prix")
        self.treeview.heading("Année", text="📅 Année")
        self.treeview.heading("Kilométrage", text="🏃 Kilométrage")
        self.treeview.heading("Lien", text="🔗 Lien")
        
        # Configuration des colonnes
        self.treeview.column("Titre", width=300, anchor="w")
        self.treeview.column("Prix", width=100, anchor="center")
        self.treeview.column("Année", width=80, anchor="center")
        self.treeview.column("Kilométrage", width=120, anchor="center")
        self.treeview.column("Lien", width=200, anchor="w")
        
        # Scrollbars
        scrollbar_v = ttk.Scrollbar(tableau_frame, orient="vertical", command=self.treeview.yview)
        scrollbar_h = ttk.Scrollbar(tableau_frame, orient="horizontal", command=self.treeview.xview)
        self.treeview.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        # Pack du tableau et scrollbars
        self.treeview.pack(side="left", fill="both", expand=True)
        scrollbar_v.pack(side="right", fill="y")
        scrollbar_h.pack(side="bottom", fill="x")
        
        # Binding pour double-clic (ouvrir lien)
        self.treeview.bind("<Double-1>", self.ouvrir_lien_selectionne)
    
    def creer_frame_actions(self, parent):
        """Crée les boutons d'actions sur les résultats"""
        actions_frame = ctk.CTkFrame(parent)
        actions_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        # Bouton pour ajouter à la liste de repérage
        btn_ajouter_reperage = ctk.CTkButton(
            actions_frame,
            text="➕ Ajouter au repérage",
            command=self.ajouter_selection_reperage,
            font=ctk.CTkFont(size=12, weight="bold"),
            width=180
        )
        btn_ajouter_reperage.pack(side="left", padx=(15, 10), pady=15)
        
        # Bouton pour exporter les résultats
        btn_exporter = ctk.CTkButton(
            actions_frame,
            text="📄 Exporter résultats",
            command=self.exporter_resultats,
            font=ctk.CTkFont(size=12, weight="bold"),
            width=160
        )
        btn_exporter.pack(side="left", padx=10, pady=15)
        
        # Bouton pour effacer les résultats
        btn_effacer = ctk.CTkButton(
            actions_frame,
            text="🗑️ Effacer",
            command=self.effacer_resultats,
            font=ctk.CTkFont(size=12, weight="bold"),
            width=100,
            fg_color="red",
            hover_color="darkred"
        )
        btn_effacer.pack(side="right", padx=(10, 15), pady=15)
    
    def valider_parametres(self):
        """Valide les paramètres de recherche"""
        erreurs = []
        
        # Vérifier le modèle
        modele = self.entry_modele.get().strip()
        if not modele:
            erreurs.append("Le modèle est obligatoire")
        
        # Vérifier les années
        try:
            annee_min = int(self.entry_annee_min.get())
            annee_max = int(self.entry_annee_max.get())
            if annee_min > annee_max:
                erreurs.append("L'année minimum doit être inférieure à l'année maximum")
            if annee_min < 1990 or annee_max > 2030:
                erreurs.append("Les années doivent être entre 1990 et 2030")
        except ValueError:
            erreurs.append("Les années doivent être des nombres valides")
        
        # Vérifier les kilométrages
        try:
            km_min = int(self.entry_km_min.get())
            km_max = int(self.entry_km_max.get())
            if km_min > km_max:
                erreurs.append("Le kilométrage minimum doit être inférieur au kilométrage maximum")
            if km_min < 0 or km_max > 500000:
                erreurs.append("Les kilométrages doivent être entre 0 et 500,000 km")
        except ValueError:
            erreurs.append("Les kilométrages doivent être des nombres valides")
        
        # Vérifier le nombre d'annonces
        try:
            nb_annonces = int(self.entry_nb_annonces.get() or "50")
            if nb_annonces < 1 or nb_annonces > 200:
                erreurs.append("Le nombre d'annonces doit être entre 1 et 200")
        except ValueError:
            erreurs.append("Le nombre d'annonces doit être un nombre valide")
        
        return erreurs
    
    def lancer_recherche(self):
        """Lance la recherche en arrière-plan"""
        if self.recherche_en_cours:
            messagebox.showinfo("Recherche en cours", "Une recherche est déjà en cours. Veuillez patienter.")
            return
        
        # Valider les paramètres
        erreurs = self.valider_parametres()
        if erreurs:
            messagebox.showerror("Erreurs de validation", "\n".join(erreurs))
            return
        
        # Récupérer les paramètres
        parametres = {
            'modele': self.entry_modele.get().strip(),
            'annee_min': int(self.entry_annee_min.get()),
            'annee_max': int(self.entry_annee_max.get()),
            'km_min': int(self.entry_km_min.get()),
            'km_max': int(self.entry_km_max.get()),
            'nb_annonces': int(self.entry_nb_annonces.get() or "50")
        }
        
        # Effacer les résultats précédents
        self.effacer_resultats()
        
        # Lancer la recherche dans un thread séparé
        self.recherche_en_cours = True
        self.btn_rechercher.configure(state="disabled", text="🔄 Recherche en cours...")
        self.progress_bar.set(0)
        self.label_statut.configure(text="Initialisation de la recherche...")
        
        self.thread_recherche = threading.Thread(
            target=self.executer_recherche,
            args=(parametres,),
            daemon=True
        )
        self.thread_recherche.start()
    
    def executer_recherche(self, parametres):
        """Exécute la recherche dans un thread séparé"""
        try:
            # Créer le scraper
            scraper = LeboncoinScraper()
            
            # Mettre à jour le statut
            self.queue_resultats.put(("statut", "Recherche des annonces..."))
            self.queue_resultats.put(("progress", 0.2))
            
            # Lancer la recherche
            annonces = scraper.search_ads(
                parametres['modele'],
                parametres['annee_min'],
                parametres['annee_max'],
                parametres['km_min'],
                parametres['km_max'],
                parametres['nb_annonces']
            )
            
            # Mettre à jour le statut
            self.queue_resultats.put(("statut", "Analyse des données..."))
            self.queue_resultats.put(("progress", 0.7))
            
            # Analyser les prix
            analyzer = DataAnalyzer()
            stats = analyzer.analyze_prices(annonces)
            
            # Mettre à jour le statut
            self.queue_resultats.put(("statut", f"Recherche terminée - {len(annonces)} annonces trouvées"))
            self.queue_resultats.put(("progress", 1.0))
            
            # Envoyer les résultats
            self.queue_resultats.put(("resultats", {"annonces": annonces, "stats": stats}))
            
        except Exception as e:
            self.queue_resultats.put(("erreur", str(e)))
        finally:
            self.queue_resultats.put(("fin", None))
    
    def verifier_resultats(self):
        """Vérifie périodiquement les résultats de la recherche"""
        try:
            while True:
                type_msg, data = self.queue_resultats.get_nowait()
                
                if type_msg == "statut":
                    self.label_statut.configure(text=data)
                elif type_msg == "progress":
                    self.progress_bar.set(data)
                elif type_msg == "resultats":
                    self.afficher_resultats(data["annonces"], data["stats"])
                elif type_msg == "erreur":
                    self.afficher_erreur(data)
                elif type_msg == "fin":
                    self.recherche_terminee()
                    
        except queue.Empty:
            pass
        
        # Programmer la prochaine vérification
        self.parent.after(100, self.verifier_resultats)
    
    def afficher_resultats(self, annonces, stats):
        """Affiche les résultats de la recherche"""
        self.resultats_annonces = annonces
        self.stats_prix = stats
        
        # Effacer le tableau
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        # Ajouter les annonces au tableau
        for annonce in annonces:
            self.treeview.insert("", "end", values=(
                annonce['titre'][:50] + "..." if len(annonce['titre']) > 50 else annonce['titre'],
                f"{annonce['prix']:,} €",
                annonce['annee'],
                f"{annonce['kilometrage']:,} km",
                annonce['lien'][:30] + "..." if len(annonce['lien']) > 30 else annonce['lien']
            ))
        
        # Afficher les statistiques
        self.afficher_statistiques(stats)
    
    def afficher_statistiques(self, stats):
        """Affiche les statistiques des prix"""
        # Effacer les anciens widgets de stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        if not stats:
            return
        
        # Titre des stats
        stats_title = ctk.CTkLabel(
            self.stats_frame,
            text="📊 Statistiques des prix",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        stats_title.pack(pady=(10, 5))
        
        # Frame pour les stats en ligne
        stats_row = ctk.CTkFrame(self.stats_frame)
        stats_row.pack(fill="x", padx=20, pady=(0, 15))
        
        # Statistiques
        stat_labels = [
            ("💰 Minimum", f"{stats['minimum']:,} €"),
            ("💰 Maximum", f"{stats['maximum']:,} €"),
            ("📈 Moyenne", f"{stats['moyenne']:,} €"),
            ("📊 Médiane", f"{stats['mediane']:,} €"),
            ("📄 Annonces", f"{stats['nombre']}")
        ]
        
        for i, (label, value) in enumerate(stat_labels):
            stat_frame = ctk.CTkFrame(stats_row)
            stat_frame.pack(side="left", fill="x", expand=True, padx=5, pady=10)
            
            ctk.CTkLabel(stat_frame, text=label, font=ctk.CTkFont(weight="bold")).pack(pady=(5, 0))
            ctk.CTkLabel(stat_frame, text=value, font=ctk.CTkFont(size=16)).pack(pady=(0, 5))
    
    def afficher_erreur(self, erreur):
        """Affiche une erreur de recherche"""
        messagebox.showerror("Erreur de recherche", f"Une erreur s'est produite :\n{erreur}")
        self.label_statut.configure(text=f"Erreur : {erreur}")
    
    def recherche_terminee(self):
        """Actions à effectuer quand la recherche est terminée"""
        self.recherche_en_cours = False
        self.btn_rechercher.configure(state="normal", text="🔍 Lancer la recherche")
        self.progress_bar.set(1)
        
        if len(self.resultats_annonces) == 0:
            self.label_statut.configure(text="Aucune annonce trouvée. Essayez d'autres critères.")
        elif len(self.resultats_annonces) < 10:
            self.label_statut.configure(text=f"⚠️ Seulement {len(self.resultats_annonces)} annonces trouvées - Critères peut-être trop restrictifs")
    
    def ouvrir_lien_selectionne(self, event):
        """Ouvre le lien de l'annonce sélectionnée"""
        selection = self.treeview.selection()
        if not selection:
            return
        
        item = self.treeview.item(selection[0])
        values = item['values']
        if len(values) >= 5:
            # Récupérer le lien complet depuis les résultats
            index = self.treeview.index(selection[0])
            if index < len(self.resultats_annonces):
                lien = self.resultats_annonces[index]['lien']
                import webbrowser
                webbrowser.open(lien)
    
    def ajouter_selection_reperage(self):
        """Ajoute l'annonce sélectionnée à la liste de repérage"""
        selection = self.treeview.selection()
        if not selection:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une annonce à ajouter.")
            return
        
        # Récupérer l'annonce sélectionnée
        index = self.treeview.index(selection[0])
        if index >= len(self.resultats_annonces):
            return
        
        annonce = self.resultats_annonces[index]
        
        # Créer un véhicule à partir de l'annonce
        try:
            vehicule = Vehicule()
            vehicule.marque_modele = annonce['titre']
            vehicule.annee = annonce['annee']
            vehicule.kilometrage = annonce['kilometrage']
            vehicule.prix_reperage = annonce['prix']  # Prix comme référence
            vehicule.commentaires = f"Trouvé sur LeBonCoin - {annonce['lien']}"
            
            # Ajouter à la liste de repérage
            self.data_adapter.ajouter_vehicule(vehicule)
            
            if self.on_data_changed:
                self.on_data_changed()
            
            messagebox.showinfo("Ajouté", f"Le véhicule '{annonce['titre']}' a été ajouté à la liste de repérage.")
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout : {e}")
    
    def exporter_resultats(self):
        """Exporte les résultats vers un fichier CSV"""
        if not self.resultats_annonces:
            messagebox.showwarning("Aucun résultat", "Aucun résultat à exporter.")
            return
        
        from tkinter import filedialog
        import csv
        
        # Demander le fichier de sauvegarde
        fichier = filedialog.asksaveasfilename(
            title="Exporter les résultats",
            defaultextension=".csv",
            filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")]
        )
        
        if not fichier:
            return
        
        try:
            with open(fichier, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # En-têtes
                writer.writerow(["Titre", "Prix", "Année", "Kilométrage", "Lien"])
                # Données
                for annonce in self.resultats_annonces:
                    writer.writerow([
                        annonce['titre'],
                        annonce['prix'],
                        annonce['annee'],
                        annonce['kilometrage'],
                        annonce['lien']
                    ])
            
            messagebox.showinfo("Export réussi", f"Résultats exportés vers :\n{fichier}")
        
        except Exception as e:
            messagebox.showerror("Erreur d'export", f"Erreur lors de l'export : {e}")
    
    def effacer_resultats(self):
        """Efface tous les résultats"""
        # Effacer le tableau
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        # Effacer les statistiques
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Réinitialiser les variables
        self.resultats_annonces = []
        self.stats_prix = {}
        
        # Réinitialiser la barre de progression
        self.progress_bar.set(0)
        self.label_statut.configure(text="Prêt à rechercher")