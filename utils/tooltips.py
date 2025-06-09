#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de tooltips amélioré avec détection d'inactivité et tooltips contextuels
"""

import tkinter as tk
from typing import Optional, Dict
import time

# Variable globale pour la taille de police des tooltips
TOOLTIP_FONT_SIZE = 11

def set_tooltip_font_size(size: int):
    """Définit la taille de police globale pour tous les tooltips"""
    global TOOLTIP_FONT_SIZE
    TOOLTIP_FONT_SIZE = max(8, min(20, size))  # Limiter entre 8 et 20

def get_tooltip_font_size() -> int:
    """Retourne la taille de police actuelle des tooltips"""
    return TOOLTIP_FONT_SIZE

class AdvancedToolTip:
    """
    Classe pour tooltips avancés avec détection d'inactivité et contexte dynamique
    """
    
    def __init__(self, widget, text: str = "", delay: int = 1000, wraplength: int = 350, 
                 font_size: Optional[int] = None, inactivity_delay: int = 500):
        """
        Initialise un tooltip avancé
        
        Args:
            widget: Widget auquel attacher le tooltip
            text: Texte à afficher (peut être une fonction pour contenu dynamique)
            delay: Délai en millisecondes avant affichage (défaut: 1000ms)
            wraplength: Largeur maximale du texte (défaut: 350px)
            font_size: Taille de police (défaut: utilise la taille globale)
            inactivity_delay: Délai d'inactivité requis en ms (défaut: 500ms)
        """
        self.widget = widget
        self.text = text
        self.delay = delay
        self.wraplength = wraplength
        self.font_size = font_size or TOOLTIP_FONT_SIZE
        self.inactivity_delay = inactivity_delay
        
        self.tooltip_window: Optional[tk.Toplevel] = None
        self.after_id: Optional[str] = None
        self.inactivity_check_id: Optional[str] = None
        
        # Variables pour détecter l'inactivité
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.last_activity_time = 0
        self.is_mouse_in_widget = False
        self.key_pressed = False
        self.app_has_focus = True  # Nouveau: pour gérer Alt+Tab
        
        # Bind les événements seulement si nécessaire (pas pour tooltips contextuels)
        self._auto_bind = True
        if hasattr(widget, '_tooltip_manual_mode'):
            self._auto_bind = False
        
        if self._auto_bind:
            self.widget.bind("<Enter>", self.on_enter)
            self.widget.bind("<Leave>", self.on_leave)
            self.widget.bind("<Motion>", self.on_motion)
            
            # Bind global pour les touches clavier
            try:
                self.widget.winfo_toplevel().bind("<KeyPress>", self.on_key_press, add=True)
                self.widget.winfo_toplevel().bind("<KeyRelease>", self.on_key_release, add=True)
                self.widget.winfo_toplevel().bind("<FocusIn>", self.on_app_focus_in, add=True)
                self.widget.winfo_toplevel().bind("<FocusOut>", self.on_app_focus_out, add=True)
            except:
                pass  # Ignore si impossible
    
    def on_enter(self, event):
        """Quand la souris entre dans le widget"""
        self.is_mouse_in_widget = True
        self.last_mouse_x = event.x_root
        self.last_mouse_y = event.y_root
        self.last_activity_time = time.time()
        self.start_inactivity_check(event)
    
    def on_leave(self, event):
        """Quand la souris quitte le widget"""
        self.is_mouse_in_widget = False
        self.cancel_all()
        self.hide_tooltip()
    
    def on_motion(self, event):
        """Quand la souris bouge"""
        # Vérifier si la souris a vraiment bougé (éviter les micro-mouvements)
        if abs(event.x_root - self.last_mouse_x) > 2 or abs(event.y_root - self.last_mouse_y) > 2:
            self.last_mouse_x = event.x_root
            self.last_mouse_y = event.y_root
            self.last_activity_time = time.time()
            
            # Redémarrer la vérification d'inactivité
            self.cancel_all()
            self.hide_tooltip()
            if self.is_mouse_in_widget:
                self.start_inactivity_check(event)
    
    def on_key_press(self, event):
        """Quand une touche est pressée"""
        self.key_pressed = True
        self.last_activity_time = time.time()
        self.cancel_all()
        self.hide_tooltip()
    
    def on_key_release(self, event):
        """Quand une touche est relâchée"""
        self.key_pressed = False
        self.last_activity_time = time.time()
        # Redémarrer la vérification si on est toujours dans le widget
        if self.is_mouse_in_widget:
            try:
                # Créer un événement fictif avec la dernière position connue
                fake_event = type('Event', (), {
                    'x_root': self.last_mouse_x,
                    'y_root': self.last_mouse_y
                })()
                self.start_inactivity_check(fake_event)
            except:
                pass
    
    def start_inactivity_check(self, event):
        """Démarre la vérification d'inactivité"""
        self.cancel_all()
        self.inactivity_check_id = self.widget.after(50, lambda: self.check_inactivity(event))
    
    def check_inactivity(self, event):
        """Vérifie si l'utilisateur est inactif"""
        current_time = time.time()
        time_since_activity = (current_time - self.last_activity_time) * 1000  # En millisecondes
        
        # Vérifier les conditions d'inactivité
        if (self.is_mouse_in_widget and 
            not self.key_pressed and 
            time_since_activity >= self.inactivity_delay):
            
            # L'utilisateur est inactif, afficher le tooltip après le délai normal
            self.after_id = self.widget.after(self.delay, lambda: self.show_tooltip(event))
        else:
            # Continuer à vérifier l'inactivité
            if self.is_mouse_in_widget:
                self.inactivity_check_id = self.widget.after(50, lambda: self.check_inactivity(event))
    
    def cancel_all(self):
        """Annule tous les timers"""
        if self.after_id:
            try:
                self.widget.after_cancel(self.after_id)
            except:
                pass
            self.after_id = None
        if self.inactivity_check_id:
            try:
                self.widget.after_cancel(self.inactivity_check_id)
            except:
                pass
            self.inactivity_check_id = None
    
    def get_text(self, event=None):
        """Récupère le texte à afficher (peut être dynamique)"""
        if callable(self.text):
            try:
                return self.text(event)
            except:
                return "Erreur dans le tooltip dynamique"
        return self.text
    
    def show_tooltip(self, event):
        """Affiche le tooltip avec police configurée"""
        if self.tooltip_window or not self.is_mouse_in_widget:
            return
        
        # Vérifier que le widget existe encore
        try:
            if not self.widget.winfo_exists():
                return
        except:
            # Le widget n'existe plus, ne pas créer le tooltip
            return
        
        text_to_show = self.get_text(event)
        if not text_to_show:
            return
        
        # Créer la fenêtre tooltip
        try:
            self.tooltip_window = tk.Toplevel(self.widget)
        except tk.TclError:
            # Le widget parent n'existe plus, abandonner
            return
        
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_attributes('-topmost', True)  # Toujours au dessus
        
        # Position du tooltip (légèrement décalé de la souris)
        x = event.x_root + 15
        y = event.y_root + 10
        
        # Vérifier les bords de l'écran
        screen_width = self.tooltip_window.winfo_screenwidth()
        screen_height = self.tooltip_window.winfo_screenheight()
        
        # Créer le label avec le texte
        label = tk.Label(
            self.tooltip_window,
            text=text_to_show,
            background="#FFFFDD",
            foreground="#000000",
            relief="solid",
            borderwidth=1,
            font=("Segoe UI", self.font_size),
            wraplength=self.wraplength,
            justify="left",
            padx=12,
            pady=8
        )
        label.pack()
        
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
            try:
                self.tooltip_window.destroy()
            except:
                pass  # Ignorer les erreurs si la fenêtre est déjà détruite
            finally:
                self.tooltip_window = None
    
    def update_text(self, new_text):
        """Met à jour le texte du tooltip"""
        self.text = new_text
        # Si un tooltip est déjà affiché, le cacher pour forcer un rafraîchissement
        if self.tooltip_window:
            self.hide_tooltip()
    
    def destroy(self):
        """Détruit complètement le tooltip et nettoie les ressources"""
        self.cancel_all()
        self.hide_tooltip()
        self.is_mouse_in_widget = False
        
        # Retirer les bindings si possible
        try:
            self.widget.unbind("<Enter>")
            self.widget.unbind("<Leave>")
            self.widget.unbind("<Motion>")
        except:
            pass
        
        # Nettoyer les variables
        self.text = None
        self.widget = None
    
    def on_app_focus_in(self, event):
        """Quand l'application reprend le focus (après Alt+Tab)"""
        # Réactiver les tooltips si la souris est dans le widget
        if self.is_mouse_in_widget:
            try:
                self.key_pressed = False
                self.last_activity_time = 0
            except:
                pass
    
    def on_app_focus_out(self, event):
        """Quand l'application perd le focus (Alt+Tab)"""
        # Cacher tous les tooltips
        self.hide_tooltip()

# Alias pour compatibilité avec l'ancien système
ToolTip = AdvancedToolTip

class TreeviewColumnTooltip:
    """
    Classe spécialisée pour les tooltips de colonnes de tableaux
    Version simplifiée et robuste
    """
    
    def __init__(self, treeview, column_tooltips: Dict[str, str]):
        """
        Initialise les tooltips de colonnes
        
        Args:
            treeview: Widget Treeview
            column_tooltips: Dictionnaire {nom_colonne: texte_tooltip}
        """
        self.treeview = treeview
        self.column_tooltips = column_tooltips
        self.tooltips_by_column = {}  # Un tooltip par colonne
        self.current_column = None
        self.motion_after_id = None
        self.is_mouse_in_treeview = False
        
        # Créer un tooltip pour chaque colonne
        self._create_column_tooltips()
        
        # Bind les événements
        self.treeview.bind("<Motion>", self.on_motion, add=True)
        self.treeview.bind("<Leave>", self.on_leave, add=True)
        self.treeview.bind("<Enter>", self.on_enter, add=True)
        
        # Bind pour gestion focus (pour problème Alt+Tab)
        try:
            self.treeview.winfo_toplevel().bind("<FocusIn>", self.on_app_focus_in, add=True)
            self.treeview.winfo_toplevel().bind("<FocusOut>", self.on_app_focus_out, add=True)
        except:
            pass
    
    def _create_column_tooltips(self):
        """Crée un tooltip indépendant pour chaque colonne"""
        self.tooltips_by_column = {}
        
        for col_name, tooltip_text in self.column_tooltips.items():
            # Créer un tooltip désactivé pour cette colonne
            tooltip = AdvancedToolTip(
                self.treeview,
                text=tooltip_text,
                delay=800,
                inactivity_delay=300,
                wraplength=400
            )
            # Désactiver le tooltip par défaut
            tooltip.is_mouse_in_widget = False
            self.tooltips_by_column[col_name] = tooltip
    
    def on_enter(self, event):
        """Quand la souris entre dans le treeview"""
        self.is_mouse_in_treeview = True
        
    def on_leave(self, event):
        """Quand la souris quitte le treeview"""
        self.is_mouse_in_treeview = False
        self._hide_all_tooltips()
        self.current_column = None
        
        if self.motion_after_id:
            self.treeview.after_cancel(self.motion_after_id)
            self.motion_after_id = None
    
    def on_motion(self, event):
        """Gère le mouvement de souris avec délai"""
        # Annuler le traitement précédent
        if self.motion_after_id:
            self.treeview.after_cancel(self.motion_after_id)
        
        # Programmer le traitement avec un délai pour éviter trop d'appels
        self.motion_after_id = self.treeview.after(50, lambda: self._process_motion(event))
    
    def _process_motion(self, event):
        """Traite le mouvement de souris"""
        self.motion_after_id = None
        
        if not self.is_mouse_in_treeview:
            return
        
        try:
            # Identifier la colonne
            column = self.treeview.identify_column(event.x)
            
            if not column or column == "#0":
                # Pas sur une colonne valide
                if self.current_column:
                    self._hide_all_tooltips()
                    self.current_column = None
                return
            
            # Convertir le numéro de colonne en nom
            try:
                col_index = int(column.replace('#', '')) - 1
                columns = list(self.treeview['columns'])
                
                if 0 <= col_index < len(columns):
                    col_name = columns[col_index]
                else:
                    return
            except:
                return
            
            # Si on change de colonne
            if col_name != self.current_column:
                # Cacher tous les tooltips
                self._hide_all_tooltips()
                
                # Activer le tooltip de la nouvelle colonne
                if col_name in self.tooltips_by_column:
                    self.current_column = col_name
                    tooltip = self.tooltips_by_column[col_name]
                    
                    # Activer ce tooltip spécifique
                    tooltip.is_mouse_in_widget = True
                    tooltip.last_mouse_x = event.x_root
                    tooltip.last_mouse_y = event.y_root
                    tooltip.last_activity_time = 0  # Forcer la réinitialisation
                    tooltip.key_pressed = False
                    
                    # Démarrer la détection d'inactivité pour ce tooltip
                    tooltip.start_inactivity_check(event)
                
        except Exception as e:
            print(f"Erreur _process_motion: {e}")
    
    def _hide_all_tooltips(self):
        """Cache tous les tooltips de toutes les colonnes"""
        for tooltip in self.tooltips_by_column.values():
            try:
                tooltip.is_mouse_in_widget = False
                tooltip.cancel_all()
                tooltip.hide_tooltip()
            except:
                pass
    
    def on_app_focus_in(self, event):
        """Quand l'application reprend le focus (après Alt+Tab)"""
        # Réactiver les tooltips si la souris est dans le treeview
        if self.is_mouse_in_treeview and self.current_column:
            try:
                tooltip = self.tooltips_by_column.get(self.current_column)
                if tooltip:
                    tooltip.key_pressed = False
                    tooltip.last_activity_time = 0
            except:
                pass
    
    def on_app_focus_out(self, event):
        """Quand l'application perd le focus (Alt+Tab)"""
        # Cacher tous les tooltips
        self._hide_all_tooltips()
    
    def update_column_tooltips(self, new_tooltips: Dict[str, str]):
        """Met à jour les tooltips des colonnes"""
        self._hide_all_tooltips()
        self.current_column = None
        
        # Détruire les anciens tooltips
        for tooltip in self.tooltips_by_column.values():
            try:
                tooltip.destroy()
            except:
                pass
        
        # Recréer avec les nouveaux textes
        self.column_tooltips = new_tooltips
        self._create_column_tooltips()
    
    def cleanup(self):
        """Nettoie complètement le gestionnaire de tooltips"""
        self._hide_all_tooltips()
        
        # Annuler les tâches en attente
        if self.motion_after_id:
            try:
                self.treeview.after_cancel(self.motion_after_id)
            except:
                pass
            self.motion_after_id = None
        
        # Détruire tous les tooltips
        for tooltip in self.tooltips_by_column.values():
            try:
                tooltip.destroy()
            except:
                pass
        
        self.tooltips_by_column.clear()
        
        # Supprimer les bindings
        try:
            self.treeview.unbind("<Motion>")
            self.treeview.unbind("<Leave>")
            self.treeview.unbind("<Enter>")
        except:
            pass

def ajouter_tooltip(widget, text: str, delay: int = 1000, wraplength: int = 350, font_size: Optional[int] = None) -> AdvancedToolTip:
    """
    Fonction utilitaire pour ajouter facilement un tooltip avancé à un widget
    
    Args:
        widget: Widget auquel attacher le tooltip
        text: Texte à afficher
        delay: Délai en millisecondes (défaut: 1000ms)
        wraplength: Largeur maximale du texte (défaut: 350px)
        font_size: Taille de police (défaut: utilise la taille globale)
    
    Returns:
        Instance AdvancedToolTip créée
    """
    return AdvancedToolTip(widget, text, delay, wraplength, font_size)

def ajouter_tooltips_colonnes_tableau(treeview, data_adapter=None):
    """
    Ajoute des tooltips contextuels aux colonnes du tableau de repérage
    
    Args:
        treeview: Widget Treeview
        data_adapter: Adaptateur de données pour récupérer les paramètres
    
    Returns:
        Instance TreeviewColumnTooltip
    """
    # Récupérer les paramètres pour afficher les formules
    if data_adapter and hasattr(data_adapter, 'journee') and data_adapter.journee:
        parametres = data_adapter.journee.parametres
        tarif_horaire = parametres.get('tarif_horaire', 45.0)
        commission = parametres.get('commission_vente', 8.5)
        marge_securite = parametres.get('marge_securite', 200.0)
    else:
        tarif_horaire = 45.0
        commission = 8.5
        marge_securite = 200.0
    
    # Définir les tooltips spécifiques par colonne
    column_tooltips = {
        "lot": "🏷️ NUMÉRO DE LOT\n• Double-clic pour voir les détails complets du véhicule\n• Numéro unique d'identification à l'enchère",
        
        "marque": "🚗 MARQUE DU VÉHICULE\n• Double-clic pour modifier\n• Obligatoire pour l'ajout",
        
        "modele": "🔧 MODÈLE DU VÉHICULE\n• Double-clic pour modifier\n• Complément de la marque",
        
        "annee": "📅 ANNÉE DE MISE EN CIRCULATION\n• Double-clic pour modifier\n• Format: YYYY",
        
        "kilometrage": "📏 KILOMÉTRAGE AFFICHÉ\n• Double-clic pour modifier\n• Format automatique (ex: 120,000km)",
        
        "motorisation": "⚙️ TYPE DE MOTORISATION\n• Double-clic pour modifier\n• Ex: Diesel, Essence, Hybride, Électrique",
        
        "prix_revente": "💰 PRIX DE REVENTE ESTIMÉ\n• Double-clic pour modifier\n• Prix une fois le véhicule réparé\n• Utilisé pour calculer le prix maximum",
        
        "cout_reparations": "🔨 COÛT DES RÉPARATIONS\n• Double-clic pour modifier\n• Coût estimé des pièces et fournitures\n• Utilisé dans le calcul du prix maximum",
        
        "temps_reparations": "⏱️ TEMPS DE RÉPARATION\n• Double-clic pour modifier\n• En heures\n• Multiplié par le tarif horaire dans le calcul",
        
        "description_reparations": "📝 DESCRIPTION DES RÉPARATIONS\n• Double-clic pour modifier\n• Détail des travaux à effectuer\n• Notes et observations",
        
        "prix_max": f"🎯 PRIX MAXIMUM CALCULÉ\n• CALCUL AUTOMATIQUE - Non modifiable\n\n📊 FORMULE:\nPrix Max = Prix Revente - (Coût Réparations + Main d'Œuvre) - Commission - Marge Sécurité\n\n🔧 DÉTAIL:\n• Main d'Œuvre = Temps × {tarif_horaire}€/h\n• Commission = Prix Revente × {commission}%\n• Marge Sécurité = {marge_securite}€\n\n💡 Prix conseillé pour ne pas dépasser votre budget",
        
        "prix_achat": "💳 PRIX D'ACHAT RÉEL\n• Double-clic pour modifier\n• Prix payé aux enchères\n• Utilisé pour calculer l'écart budget",
        
        "marge": f"📈 ÉCART BUDGET\n• CALCUL AUTOMATIQUE - Non modifiable\n\n📊 FORMULE:\nÉcart = Prix Maximum - Prix d'Achat\n\n🎯 INTERPRÉTATION:\n• ✅ Positif = Respect du budget\n• ❌ Négatif = Dépassement de budget\n\nℹ️ Le Prix Maximum inclut déjà la marge de sécurité de {marge_securite}€",
        
        "statut": "🏷️ STATUT DU VÉHICULE\n• AUTOMATIQUE - Non modifiable\n• 'Repérage' = En cours d'évaluation\n• Utilisez 'Marquer Acheté' pour changer",
        
        "champ_libre": "📋 CHAMP LIBRE\n• Double-clic pour modifier\n• Zone pour notes personnalisées\n• Informations supplémentaires",
        
        "reserve_pro": "👔 RÉSERVÉ AUX PROFESSIONNELS\n• Double-clic pour modifier\n• Oui/Non\n• Indique si seuls les pros peuvent enchérir",
        
        "couleur": "🎨 COULEUR D'AFFICHAGE\n• Double-clic pour modifier\n• Choisir parmi : Turquoise, Vert, Orange, Rouge\n• Permet d'organiser visuellement les véhicules\n• Facilite l'identification rapide"
    }
    
    return TreeviewColumnTooltip(treeview, column_tooltips)

def ajouter_tooltips_colonnes_achetes(treeview, data_adapter=None):
    """
    Ajoute des tooltips contextuels aux colonnes du tableau véhicules achetés
    
    Args:
        treeview: Widget Treeview
        data_adapter: Adaptateur de données pour récupérer les paramètres
    
    Returns:
        Instance TreeviewColumnTooltip
    """
    # Récupérer les paramètres pour afficher les formules
    if data_adapter and hasattr(data_adapter, 'journee') and data_adapter.journee:
        parametres = data_adapter.journee.parametres
        tarif_horaire = parametres.get('tarif_horaire', 45.0)
        commission = parametres.get('commission_vente', 8.5)
        marge_securite = parametres.get('marge_securite', 200.0)
    else:
        tarif_horaire = 45.0
        commission = 8.5
        marge_securite = 200.0
    
    # Définir les tooltips spécifiques par colonne pour l'onglet achetés
    column_tooltips = {
        "lot": "🏷️ NUMÉRO DE LOT\n• Double-clic pour voir les détails complets du véhicule\n• Numéro unique d'identification à l'enchère",
        
        "marque": "🚗 MARQUE DU VÉHICULE\n• Double-clic pour modifier\n• Information de base du véhicule",
        
        "modele": "🔧 MODÈLE DU VÉHICULE\n• Double-clic pour modifier\n• Complément de la marque",
        
        "annee": "📅 ANNÉE DE MISE EN CIRCULATION\n• Double-clic pour modifier\n• Format: YYYY",
        
        "prix_achat": "💳 PRIX D'ACHAT RÉEL\n• Double-clic pour modifier\n• Prix payé aux enchères\n• ATTENTION: Non modifiable car utilisé pour les calculs",
        
        "prix_max": f"🎯 PRIX MAXIMUM CALCULÉ\n• CALCUL AUTOMATIQUE - Non modifiable\n\n📊 FORMULE:\nPrix Max = Prix Revente - (Coût Réparations + Main d'Œuvre) - Commission - Marge Sécurité\n\n🔧 DÉTAIL:\n• Main d'Œuvre = Temps × {tarif_horaire}€/h\n• Commission = Prix Revente × {commission}%\n• Marge Sécurité = {marge_securite}€\n\n💡 Budget alloué initialement",
        
        "prix_vente_final": "💰 PRIX DE VENTE FINAL\n• Double-clic pour modifier\n• Prix obtenu lors de la revente\n• Utilisé pour calculer la marge réelle",
        
        "marge": f"📈 MARGE RÉALISÉE\n• CALCUL AUTOMATIQUE - Non modifiable\n\n📊 FORMULE COMPLÈTE:\nMarge = Prix Vente Final - (Prix Achat + Coût Réparations + Main d'Œuvre + Commission d'Enchère)\n\n🔧 DÉTAIL:\n• Prix Achat = Prix payé aux enchères\n• Coût Réparations = Pièces et fournitures\n• Main d'Œuvre = Temps × {tarif_horaire}€/h\n• Commission Enchère = Prix Achat × {commission}%\n\n🎯 INTERPRÉTATION:\n• ✅ Positif = Bénéfice\n• ❌ Négatif = Perte\n\nℹ️ La marge de sécurité ({marge_securite}€) n'est PAS déduite ici car c'était juste une précaution pour le prix max",
        
        "date_achat": "📅 DATE D'ACHAT\n• AUTOMATIQUE - Non modifiable\n• Date à laquelle le véhicule a été marqué comme acheté\n• Format: JJ/MM/AAAA",
        
        "ecart_budget": f"📊 ÉCART / BUDGET INITIAL\n• CALCUL AUTOMATIQUE - Non modifiable\n\n📊 FORMULE:\nÉcart = Prix Maximum - Prix d'Achat\n\n🎯 INTERPRÉTATION:\n• ✅ Positif = Respect du budget initial\n• ❌ Négatif = Dépassement du budget\n\nℹ️ Le Prix Maximum inclut la marge de sécurité de {marge_securite}€",
        
        "cout_reparations": "🔨 COÛT DES RÉPARATIONS\n• Double-clic pour modifier\n• Coût réel des pièces et fournitures\n• Utilisé dans le calcul de la marge finale",
        
        "temps_reparations": "⏱️ TEMPS DE RÉPARATION\n• Double-clic pour modifier\n• Temps réel passé en heures\n• Multiplié par le tarif horaire dans le calcul de marge",
        
        "couleur": "🎨 COULEUR D'AFFICHAGE\n• Double-clic pour modifier\n• Choisir parmi : Turquoise, Vert, Orange, Rouge\n• Permet d'organiser visuellement les véhicules\n• Facilite l'identification rapide"
    }
    
    return TreeviewColumnTooltip(treeview, column_tooltips)

# Textes prédéfinis pour les tooltips (CONSERVÉS pour compatibilité)
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
    
    # Colonnes tableau (CONSERVÉS mais remplacés par le système contextuel pour les tableaux)
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
    'param_taille_police_tooltips': "Taille de la police des infobulles d'aide (recommandé: 9-14).",
    'param_largeur_colonnes_auto': "Ajuste automatiquement la largeur des colonnes selon le contenu.",
    
    # Boutons paramètres
    'btn_sauvegarder_param': "Sauvegarde les paramètres dans le fichier de configuration.",
    'btn_reinitialiser_param': "Remet tous les paramètres aux valeurs par défaut.",
    'btn_aide_param': "Affiche l'aide détaillée sur les paramètres.",
    
    # Export
    'btn_export_csv': "Exporte la liste des véhicules achetés vers un fichier CSV.",
} 