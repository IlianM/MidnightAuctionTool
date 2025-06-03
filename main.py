#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire d'Enchères Véhicules - Version CustomTkinter
Application moderne pour gérer l'achat de véhicules en enchères
avec calcul automatique des prix maximums rentables.
"""

import sys
import traceback
import customtkinter as ctk

from gui.main_window import MainWindow

def main():
    """Point d'entrée principal de l'application (CustomTkinter)"""
    try:
        # Configuration de CustomTkinter
        ctk.set_appearance_mode("light")  # Mode clair par défaut
        ctk.set_default_color_theme("blue")  # Thème bleu
        
        # Création de la fenêtre principale
        root = ctk.CTk()
        root.title("🚗 Gestionnaire d'Enchères Véhicules")
        root.geometry("1400x900")
        
        # Initialisation de l'application
        app = MainWindow(root)
        
        print("🚀 Application initialisée avec CustomTkinter")
        
        # Lancement de la boucle principale
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Erreur critique lors du démarrage: {e}")
        traceback.print_exc()
        input("Appuyez sur Entrée pour fermer...")
        sys.exit(1)

if __name__ == "__main__":
    main() 