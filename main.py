#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire d'Enchères Véhicules - Version bases de données séparées
Application moderne pour gérer l'achat de véhicules en enchères
avec bases de données complètement séparées par enchère.
"""

import sys
import traceback
import customtkinter as ctk

from gui.journees_selector import JourneesSelector
from gui.main_window import MainWindow


class Application:
    """Application principale avec sélection de base de données"""
    
    def __init__(self):
        # Configuration de CustomTkinter
        ctk.set_appearance_mode("light")  # Mode clair par défaut
        ctk.set_default_color_theme("blue")  # Thème bleu
        
        # Création de la fenêtre principale
        self.root = ctk.CTk()
        self.root.title("🗃️ Sélecteur de Base de Données - Enchères Véhicules")
        self.root.geometry("1400x900")
        
        # Variables d'état
        self.current_interface = None
        self.journee_active = None
        self.journees_manager = None
        
        # Démarrer avec la sélection des bases de données
        self.afficher_selection_journees()
    
    def afficher_selection_journees(self):
        """Affiche l'interface de sélection des bases de données"""
        # Nettoyer l'interface actuelle
        self.nettoyer_interface()
        
        # Mettre à jour le titre
        self.root.title("🗃️ Sélecteur de Base de Données - Enchères Véhicules")
        
        # Créer l'interface de sélection
        self.current_interface = JourneesSelector(
            self.root,
            self.on_journee_selected
        )
        self.current_interface.frame.pack(fill="both", expand=True)
        
        print("🗃️ Interface de sélection des bases de données affichée")
    
    def on_journee_selected(self, journee, journees_manager):
        """Callback appelé quand une base de données est sélectionnée"""
        self.journee_active = journee
        self.journees_manager = journees_manager
        
        print(f"🚀 Base de données sélectionnée: {journee.nom}")
        
        # Lancer l'application avec cette base
        self.lancer_application_principale()
    
    def lancer_application_principale(self):
        """Lance l'application principale avec la base sélectionnée"""
        # Nettoyer l'interface actuelle
        self.nettoyer_interface()
        
        # Créer l'interface principale avec la journée
        self.current_interface = MainWindow(
            self.root,
            self.journee_active,
            self.journees_manager,
            self.retour_selection_journees
        )
        
        print(f"🚀 Application lancée avec: {self.journee_active.nom}")
    
    def retour_selection_journees(self):
        """Retourne à la sélection des bases de données"""
        print("🔙 Retour au sélecteur de bases de données")
        self.afficher_selection_journees()
    
    def nettoyer_interface(self):
        """Nettoie l'interface actuelle"""
        if self.current_interface and hasattr(self.current_interface, 'frame'):
            self.current_interface.frame.destroy()
        elif self.current_interface:
            # Pour MainWindow qui modifie directement la root
            for widget in self.root.winfo_children():
                widget.destroy()
        
        self.current_interface = None
    
    def run(self):
        """Lance la boucle principale de l'application"""
        try:
            print("🗃️ Application initialisée avec système de bases séparées")
            self.root.mainloop()
            
        except Exception as e:
            print(f"❌ Erreur critique lors de l'exécution: {e}")
            traceback.print_exc()
            input("Appuyez sur Entrée pour fermer...")


def main():
    """Point d'entrée principal de l'application"""
    try:
        app = Application()
        app.run()
        
    except Exception as e:
        print(f"❌ Erreur critique lors du démarrage: {e}")
        traceback.print_exc()
        input("Appuyez sur Entrée pour fermer...")
        sys.exit(1)


if __name__ == "__main__":
    main() 