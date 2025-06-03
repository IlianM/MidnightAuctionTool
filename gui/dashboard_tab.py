#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Onglet Dashboard avec statistiques sous forme de cartes - CustomTkinter
"""

import customtkinter as ctk
from tkinter import ttk

from config.settings import AppSettings
from services.data_manager import DataManager
from utils.styles import StyleManager

class DashboardTab:
    """Onglet Dashboard avec cartes statistiques CustomTkinter"""
    
    def __init__(self, parent, settings: AppSettings, data_manager: DataManager, 
                 style_manager: StyleManager):
        self.parent = parent
        self.settings = settings
        self.data_manager = data_manager
        self.style_manager = style_manager
        
        # Créer le frame principal
        self.frame = ctk.CTkFrame(parent)
        
        # Widgets des cartes
        self.cartes = {}
        
        self.creer_interface()
    
    def creer_interface(self):
        """Crée l'interface du dashboard avec CustomTkinter"""
        main_frame = ctk.CTkFrame(self.frame)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre du dashboard
        titre = ctk.CTkLabel(
            main_frame,
            text="📊 DASHBOARD - VUE D'ENSEMBLE",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        titre.pack(pady=(0, 30))
        
        # Container pour les cartes
        cards_container = ctk.CTkFrame(main_frame)
        cards_container.pack(fill="both", expand=True)
        
        # Ligne 1: Statistiques principales
        row1 = ctk.CTkFrame(cards_container)
        row1.pack(fill="x", pady=(0, 15), padx=10)
        
        self.creer_carte(row1, "🚗", "VÉHICULES REPÉRÉS", "0", "En phase de recherche", "#0ea5e9", 0)
        self.creer_carte(row1, "🏆", "VÉHICULES ACHETÉS", "0", "Acquisitions réalisées", "#22c55e", 1)
        self.creer_carte(row1, "💰", "MARGE TOTALE", "0€", "Bénéfice cumulé", "#f59e0b", 2)
        self.creer_carte(row1, "📈", "MARGE MOYENNE", "0€", "Par véhicule acheté", "#6b7280", 3)
        
        # Ligne 2: Performance et analyse
        row2 = ctk.CTkFrame(cards_container)
        row2.pack(fill="x", pady=(0, 15), padx=10)
        
        self.creer_carte(row2, "✅", "TAUX DE RÉUSSITE", "0%", "Achats rentables", "#22c55e", 0)
        self.creer_carte(row2, "🥇", "MEILLEUR ACHAT", "N/A", "Plus grosse marge", "#22c55e", 1)
        self.creer_carte(row2, "📉", "PIRE ACHAT", "N/A", "Plus grosse perte", "#ef4444", 2)
        self.creer_carte(row2, "💸", "BUDGET INVESTI", "0€", "Capital engagé", "#3b82f6", 3)
        
        # Ligne 3: Informations détaillées
        row3 = ctk.CTkFrame(cards_container)
        row3.pack(fill="x", padx=10)
        
        self.creer_carte(row3, "🎯", "PRIX MOYEN D'ACHAT", "0€", "Ticket moyen", "#0ea5e9", 0)
        self.creer_carte(row3, "⚡", "DERNIÈRE ACTIVITÉ", "N/A", "Dernier achat", "#6b7280", 1)
        self.creer_carte(row3, "📊", "RENTABILITÉ", "0%", "ROI global", "#f59e0b", 2)
        self.creer_carte(row3, "🔥", "MARQUE FAVORITE", "N/A", "Marque la + achetée", "#3b82f6", 3)
    
    def creer_carte(self, parent, icone, titre, valeur, description, couleur, column):
        """Crée une carte statistique moderne avec CustomTkinter"""
        # Frame de la carte avec couleur personnalisée
        carte_frame = ctk.CTkFrame(parent, fg_color=couleur, corner_radius=15)
        carte_frame.grid(row=0, column=column, sticky="nsew", padx=10, pady=10)
        
        # Configuration pour expansion égale
        parent.grid_columnconfigure(column, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        # Header avec icône
        header_frame = ctk.CTkFrame(carte_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(15, 5))
        
        icone_label = ctk.CTkLabel(
            header_frame,
            text=icone,
            font=ctk.CTkFont(size=28),
            text_color="white"
        )
        icone_label.pack(side="left")
        
        titre_label = ctk.CTkLabel(
            header_frame,
            text=titre,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="white"
        )
        titre_label.pack(side="right")
        
        # Valeur principale
        valeur_label = ctk.CTkLabel(
            carte_frame,
            text=valeur,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        valeur_label.pack(pady=(5, 3))
        
        # Description
        desc_label = ctk.CTkLabel(
            carte_frame,
            text=description,
            font=ctk.CTkFont(size=11),
            text_color="#E0E0E0"
        )
        desc_label.pack(pady=(0, 15))
        
        # Stocker les références pour mise à jour
        self.cartes[titre] = {
            'valeur': valeur_label,
            'description': desc_label
        }
    
    def actualiser(self):
        """Met à jour toutes les cartes avec les données actuelles"""
        stats = self.data_manager.get_statistiques()
        
        # Statistiques de base
        nb_reperage = stats['total_reperage']
        nb_achetes = stats['total_achetes']
        marge_totale = stats['marge_totale']
        marge_moyenne = stats['marge_moyenne']
        
        # Calculs avancés
        taux_reussite = self._calculer_taux_reussite()
        meilleur_achat = self._obtenir_meilleur_achat()
        pire_achat = self._obtenir_pire_achat()
        budget_investi = self._calculer_budget_investi()
        prix_moyen = self._calculer_prix_moyen_achat()
        derniere_activite = self._obtenir_derniere_activite()
        rentabilite = self._calculer_rentabilite()
        marque_favorite = self._obtenir_marque_favorite()
        
        # Mise à jour des cartes
        self._mettre_a_jour_carte("VÉHICULES REPÉRÉS", f"{nb_reperage}", f"{nb_reperage} véhicules en phase de recherche")
        self._mettre_a_jour_carte("VÉHICULES ACHETÉS", f"{nb_achetes}", f"{nb_achetes} acquisitions réalisées")
        self._mettre_a_jour_carte("MARGE TOTALE", f"{marge_totale:.0f}€", f"Bénéfice cumulé sur {nb_achetes} achats")
        self._mettre_a_jour_carte("MARGE MOYENNE", f"{marge_moyenne:.0f}€", "Par véhicule acheté")
        self._mettre_a_jour_carte("TAUX DE RÉUSSITE", f"{taux_reussite:.1f}%", f"{stats['vehicules_rentables']}/{nb_achetes} achats rentables")
        self._mettre_a_jour_carte("MEILLEUR ACHAT", meilleur_achat['texte'], meilleur_achat['description'])
        self._mettre_a_jour_carte("PIRE ACHAT", pire_achat['texte'], pire_achat['description'])
        self._mettre_a_jour_carte("BUDGET INVESTI", f"{budget_investi:.0f}€", "Capital engagé total")
        self._mettre_a_jour_carte("PRIX MOYEN D'ACHAT", f"{prix_moyen:.0f}€", "Ticket moyen par véhicule")
        self._mettre_a_jour_carte("DERNIÈRE ACTIVITÉ", derniere_activite['texte'], derniere_activite['description'])
        self._mettre_a_jour_carte("RENTABILITÉ", f"{rentabilite:.1f}%", "ROI global sur investissements")
        self._mettre_a_jour_carte("MARQUE FAVORITE", marque_favorite['texte'], marque_favorite['description'])
    
    def _mettre_a_jour_carte(self, titre, valeur, description):
        """Met à jour une carte spécifique"""
        if titre in self.cartes:
            self.cartes[titre]['valeur'].configure(text=valeur)
            self.cartes[titre]['description'].configure(text=description)
    
    def _calculer_taux_reussite(self):
        """Calcule le taux de réussite (% achats rentables)"""
        stats = self.data_manager.get_statistiques()
        if stats['total_achetes'] == 0:
            return 0
        return (stats['vehicules_rentables'] / stats['total_achetes']) * 100
    
    def _obtenir_meilleur_achat(self):
        """Trouve le meilleur achat (plus grosse marge)"""
        if not self.data_manager.vehicules_achetes:
            return {'texte': 'N/A', 'description': 'Aucun achat réalisé'}
        
        meilleur = max(self.data_manager.vehicules_achetes, key=lambda v: v.calculer_marge())
        marge = meilleur.calculer_marge()
        return {
            'texte': f"+{marge:.0f}€",
            'description': f"{meilleur.marque} {meilleur.modele}"
        }
    
    def _obtenir_pire_achat(self):
        """Trouve le pire achat (plus grosse perte)"""
        if not self.data_manager.vehicules_achetes:
            return {'texte': 'N/A', 'description': 'Aucun achat réalisé'}
        
        pire = min(self.data_manager.vehicules_achetes, key=lambda v: v.calculer_marge())
        marge = pire.calculer_marge()
        if marge >= 0:
            return {'texte': 'Aucune perte', 'description': 'Tous les achats sont rentables !'}
        return {
            'texte': f"{marge:.0f}€",
            'description': f"{pire.marque} {pire.modele}"
        }
    
    def _calculer_budget_investi(self):
        """Calcule le budget total investi"""
        return sum(v.get_prix_numerique('prix_achat') for v in self.data_manager.vehicules_achetes)
    
    def _calculer_prix_moyen_achat(self):
        """Calcule le prix moyen d'achat"""
        if not self.data_manager.vehicules_achetes:
            return 0
        budget = self._calculer_budget_investi()
        return budget / len(self.data_manager.vehicules_achetes)
    
    def _obtenir_derniere_activite(self):
        """Obtient la dernière activité"""
        if not self.data_manager.vehicules_achetes:
            return {'texte': 'N/A', 'description': 'Aucune activité'}
        
        # Prendre le dernier véhicule acheté (assumant qu'ils sont dans l'ordre)
        dernier = self.data_manager.vehicules_achetes[-1]
        return {
            'texte': dernier.date_achat.split()[0] if dernier.date_achat else 'N/A',
            'description': f"{dernier.marque} {dernier.modele}"
        }
    
    def _calculer_rentabilite(self):
        """Calcule le ROI global"""
        budget = self._calculer_budget_investi()
        if budget == 0:
            return 0
        stats = self.data_manager.get_statistiques()
        return (stats['marge_totale'] / budget) * 100
    
    def _obtenir_marque_favorite(self):
        """Trouve la marque la plus achetée"""
        if not self.data_manager.vehicules_achetes:
            return {'texte': 'N/A', 'description': 'Aucun achat réalisé'}
        
        marques = {}
        for v in self.data_manager.vehicules_achetes:
            marques[v.marque] = marques.get(v.marque, 0) + 1
        
        marque_fav = max(marques, key=marques.get)
        count = marques[marque_fav]
        return {
            'texte': marque_fav,
            'description': f"{count} véhicule{'s' if count > 1 else ''} acheté{'s' if count > 1 else ''}"
        } 