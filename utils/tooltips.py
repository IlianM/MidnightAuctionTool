#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de tooltips amélioré avec délai de 1 seconde
"""

import tkinter as tk
from typing import Optional

class ToolTip:
    """
    Classe pour créer des tooltips avec délai de 1 seconde
    """
    
    def __init__(self, widget, text: str, delay: int = 1000, wraplength: int = 300):
        """
        Initialise un tooltip pour un widget
        
        Args:
            widget: Widget auquel attacher le tooltip
            text: Texte à afficher
            delay: Délai en millisecondes avant affichage (défaut: 1000ms = 1s)
            wraplength: Largeur maximale du texte (défaut: 300px)
        """
        self.widget = widget
        self.text = text
        self.delay = delay
        self.wraplength = wraplength
        
        self.tooltip_window: Optional[tk.Toplevel] = None
        self.after_id: Optional[str] = None
        
        # Bind les événements
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.widget.bind("<Motion>", self.on_motion)
    
    def on_enter(self, event):
        """Démarre le timer pour afficher le tooltip"""
        self.schedule_tooltip(event)
    
    def on_leave(self, event):
        """Cache le tooltip et annule le timer"""
        self.cancel_tooltip()
        self.hide_tooltip()
    
    def on_motion(self, event):
        """Remet à zéro le timer si la souris bouge"""
        self.cancel_tooltip()
        self.schedule_tooltip(event)
    
    def schedule_tooltip(self, event):
        """Programme l'affichage du tooltip après le délai"""
        self.cancel_tooltip()
        self.after_id = self.widget.after(self.delay, lambda: self.show_tooltip(event))
    
    def cancel_tooltip(self):
        """Annule le timer du tooltip"""
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
    
    def show_tooltip(self, event):
        """Affiche le tooltip avec police agrandie"""
        if self.tooltip_window or not self.text:
            return
        
        # Créer la fenêtre tooltip
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        
        # Position du tooltip (légèrement décalé de la souris)
        x = event.x_root + 15
        y = event.y_root + 10
        
        # Vérifier les bords de l'écran
        screen_width = self.tooltip_window.winfo_screenwidth()
        screen_height = self.tooltip_window.winfo_screenheight()
        
        # Créer temporairement le label pour mesurer sa taille (POLICE DOUBLÉE : 9 -> 18)
        temp_label = tk.Label(
            self.tooltip_window,
            text=self.text,
            background="#FFFFDD",
            foreground="#000000",
            relief="solid",
            borderwidth=1,
            font=("Segoe UI", 18),  # TAILLE DOUBLÉE : 9 -> 18
            wraplength=self.wraplength,
            justify="left",
            padx=12,  # Augmenté aussi le padding
            pady=8    # Augmenté aussi le padding
        )
        temp_label.pack()
        
        # Mettre à jour pour obtenir la taille réelle
        self.tooltip_window.update_idletasks()
        width = self.tooltip_window.winfo_reqwidth()
        height = self.tooltip_window.winfo_reqheight()
        
        # Ajuster la position si nécessaire
        if x + width > screen_width:
            x = event.x_root - width - 15
        if y + height > screen_height:
            y = event.y_root - height - 10
        
        # Positionner la fenêtre
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
    
    def hide_tooltip(self):
        """Cache le tooltip"""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
    
    def update_text(self, new_text: str):
        """Met à jour le texte du tooltip"""
        self.text = new_text


def ajouter_tooltip(widget, text: str, delay: int = 1000, wraplength: int = 300) -> ToolTip:
    """
    Fonction utilitaire pour ajouter facilement un tooltip à un widget
    
    Args:
        widget: Widget auquel attacher le tooltip
        text: Texte à afficher
        delay: Délai en millisecondes (défaut: 1000ms = 1s)
        wraplength: Largeur maximale du texte (défaut: 300px)
    
    Returns:
        Instance ToolTip créée
    """
    return ToolTip(widget, text, delay, wraplength)


# Textes prédéfinis pour les tooltips
TOOLTIPS = {
    # Saisie rapide
    'lot': "Numéro du lot de vente. Obligatoire pour identifier le véhicule.",
    'marque': "Marque du véhicule (ex: Renault, Peugeot). Obligatoire.",
    'modele': "Modèle exact du véhicule (ex: Clio, 308).",
    'annee': "Année de mise en circulation du véhicule.",
    'kilometrage': "Kilométrage affiché au compteur (sera formaté automatiquement).",
    'prix_revente': "Prix de revente estimé une fois réparé (€).",
    'cout_reparations': "Coût estimé des réparations nécessaires (€).",
    'temps_reparations': "Temps estimé pour les réparations (heures).",
    'chose_a_faire': "Description des réparations ou points d'attention.",
    
    # Boutons saisie
    'btn_ajouter': "Ajoute le véhicule à la liste de repérage avec les informations saisies.",
    'btn_vider': "Efface tous les champs de saisie pour recommencer.",
    
    # Recherche
    'recherche': "Tapez pour filtrer par numéro de lot, marque ou modèle. La recherche est instantanée.",
    'btn_effacer_recherche': "Efface le texte de recherche et affiche tous les véhicules.",
    
    # Actions tableau
    'btn_supprimer': "Supprime le véhicule sélectionné définitivement.",
    'btn_marquer_achete': "Marque le véhicule comme acheté et demande le prix d'achat réel.",
    'btn_actualiser': "Met à jour l'affichage et sauvegarde les données.",
    
    # Colonnes tableau
    'col_lot': "Numéro de lot - Double-clic pour modifier",
    'col_marque': "Marque du véhicule - Double-clic pour modifier",
    'col_modele': "Modèle du véhicule - Double-clic pour modifier",
    'col_annee': "Année du véhicule - Double-clic pour modifier",
    'col_kilometrage': "Kilométrage - Double-clic pour modifier",
    'col_prix_revente': "Prix de revente estimé - Double-clic pour modifier",
    'col_cout_reparations': "Coût des réparations - Double-clic pour modifier",
    'col_temps_reparations': "Temps de réparations en heures - Double-clic pour modifier",
    'col_prix_max': "Prix maximum calculé automatiquement selon vos paramètres. Non modifiable.",
    'col_prix_achat': "Prix d'achat réel - Double-clic pour modifier",
    'col_statut': "Statut du véhicule (Repérage/Acheté). Non modifiable directement.",
    
    # Paramètres
    'param_tarif_horaire': "Votre tarif horaire pour les réparations (€/heure).",
    'param_commission_vente': "Commission prélevée lors de la vente (pourcentage).",
    'param_marge_securite': "Marge de sécurité à déduire du calcul pour les imprévus (€).",
    'param_mode_sombre': "Active/désactive le mode sombre de l'interface.",
    
    # NOUVEAUX PARAMÈTRES D'INTERFACE
    'param_hauteur_lignes_tableau': "Hauteur des lignes dans les tableaux en pixels (recommandé: 25-40).",
    'param_taille_police_tableau': "Taille de la police du contenu des tableaux (recommandé: 12-18).",
    'param_taille_police_entetes': "Taille de la police des en-têtes de colonnes (recommandé: 14-20).",
    'param_taille_police_titres': "Taille de la police des titres principaux (recommandé: 18-24).",
    'param_taille_police_boutons': "Taille de la police des boutons (recommandé: 10-16).",
    'param_taille_police_labels': "Taille de la police des étiquettes (recommandé: 10-16).",
    'param_taille_police_champs': "Taille de la police des champs de saisie (recommandé: 10-16).",
    'param_largeur_colonnes_auto': "Ajuste automatiquement la largeur des colonnes selon le contenu.",
    
    # Boutons paramètres
    'btn_sauvegarder_param': "Sauvegarde les paramètres dans le fichier de configuration.",
    'btn_reinitialiser_param': "Remet tous les paramètres aux valeurs par défaut.",
    'btn_aide_param': "Affiche l'aide détaillée sur les paramètres.",
    
    # Export
    'btn_export_csv': "Exporte la liste des véhicules achetés vers un fichier CSV.",
} 