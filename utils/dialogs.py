#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dialogs personnalisées avec polices agrandies
"""

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class DialogPrixAchat:
    """Dialog personnalisée pour saisir le prix d'achat avec police agrandie"""
    
    def __init__(self, parent, title="Prix d'achat", message="Entrez le prix d'achat (€):"):
        self.parent = parent
        self.result = None
        
        # Créer la fenêtre dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x300")
        self.dialog.resizable(False, False)
        
        # Centrer la dialog
        self.center_dialog()
        
        # Rendre la dialog modale
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Créer l'interface
        self.create_interface(message)
        
        # Focus sur le champ d'entrée
        self.entry.focus_set()
        
        # Bind des événements
        self.dialog.bind('<Return>', self.on_ok)
        self.dialog.bind('<Escape>', self.on_cancel)
        
        # Attendre la fermeture de la dialog
        self.dialog.wait_window()
    
    def center_dialog(self):
        """Centre la dialog sur l'écran"""
        self.dialog.update_idletasks()
        
        # Obtenir les dimensions
        width = 500
        height = 300
        
        # Calculer la position pour centrer
        pos_x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        pos_y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        
        self.dialog.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
    
    def create_interface(self, message):
        """Crée l'interface de la dialog"""
        # Frame principal
        main_frame = tk.Frame(self.dialog, bg='white', padx=30, pady=30)
        main_frame.pack(fill='both', expand=True)
        
        # Icône et titre
        title_frame = tk.Frame(main_frame, bg='white')
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="🏆 MARQUER COMME ACHETÉ",
            font=('Segoe UI', 24, 'bold'),  # POLICE DOUBLÉE : 12 -> 24
            bg='white',
            fg='#2E86AB'
        )
        title_label.pack()
        
        # Message
        message_label = tk.Label(
            main_frame,
            text=message,
            font=('Segoe UI', 18),  # POLICE DOUBLÉE : 9 -> 18
            bg='white',
            fg='#333333'
        )
        message_label.pack(pady=(0, 20))
        
        # Champ de saisie
        entry_frame = tk.Frame(main_frame, bg='white')
        entry_frame.pack(fill='x', pady=(0, 30))
        
        self.entry = tk.Entry(
            entry_frame,
            font=('Segoe UI', 18),  # POLICE DOUBLÉE : 9 -> 18
            justify='center',
            relief='solid',
            borderwidth=2,
            highlightthickness=0
        )
        self.entry.pack(fill='x', ipady=10)
        
        # Ajouter placeholder et exemple
        self.entry.insert(0, "Ex: 5000")
        self.entry.bind('<FocusIn>', self.on_entry_focus_in)
        self.entry.bind('<FocusOut>', self.on_entry_focus_out)
        
        # Boutons
        buttons_frame = tk.Frame(main_frame, bg='white')
        buttons_frame.pack(fill='x')
        
        # Bouton Annuler
        cancel_btn = tk.Button(
            buttons_frame,
            text="❌ Annuler",
            font=('Segoe UI', 16, 'bold'),  # POLICE DOUBLÉE : 8 -> 16
            bg='#F44336',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            command=self.on_cancel
        )
        cancel_btn.pack(side='left', padx=(0, 10))
        
        # Bouton OK
        ok_btn = tk.Button(
            buttons_frame,
            text="✅ Valider",
            font=('Segoe UI', 16, 'bold'),  # POLICE DOUBLÉE : 8 -> 16
            bg='#4CAF50',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            command=self.on_ok
        )
        ok_btn.pack(side='right', padx=(10, 0))
    
    def on_entry_focus_in(self, event):
        """Efface le placeholder au focus"""
        if self.entry.get() == "Ex: 5000":
            self.entry.delete(0, tk.END)
            self.entry.config(fg='black')
    
    def on_entry_focus_out(self, event):
        """Remet le placeholder si vide"""
        if not self.entry.get():
            self.entry.insert(0, "Ex: 5000")
            self.entry.config(fg='gray')
    
    def on_ok(self, event=None):
        """Valide la saisie"""
        value = self.entry.get().strip()
        if value and value != "Ex: 5000":
            try:
                # Validation numérique basique
                float(value.replace(',', '.'))
                self.result = value
                self.dialog.destroy()
            except ValueError:
                # Affichage d'erreur avec police agrandie
                self.show_error("Veuillez entrer un nombre valide")
        else:
            self.show_error("Veuillez entrer un prix")
    
    def on_cancel(self, event=None):
        """Annule la dialog"""
        self.result = None
        self.dialog.destroy()
    
    def show_error(self, message):
        """Affiche un message d'erreur avec police agrandie"""
        error_dialog = tk.Toplevel(self.dialog)
        error_dialog.title("Erreur")
        error_dialog.geometry("400x200")
        error_dialog.resizable(False, False)
        error_dialog.transient(self.dialog)
        error_dialog.grab_set()
        
        # Centrer l'erreur
        pos_x = (error_dialog.winfo_screenwidth() // 2) - 200
        pos_y = (error_dialog.winfo_screenheight() // 2) - 100
        error_dialog.geometry(f"400x200+{pos_x}+{pos_y}")
        
        # Contenu de l'erreur
        error_frame = tk.Frame(error_dialog, bg='white', padx=20, pady=20)
        error_frame.pack(fill='both', expand=True)
        
        tk.Label(
            error_frame,
            text="⚠️ Erreur",
            font=('Segoe UI', 20, 'bold'),  # POLICE DOUBLÉE
            bg='white',
            fg='#F44336'
        ).pack(pady=(0, 10))
        
        tk.Label(
            error_frame,
            text=message,
            font=('Segoe UI', 16),  # POLICE DOUBLÉE
            bg='white',
            fg='#333333'
        ).pack(pady=(0, 20))
        
        tk.Button(
            error_frame,
            text="OK",
            font=('Segoe UI', 14, 'bold'),  # POLICE DOUBLÉE
            bg='#2E86AB',
            fg='white',
            relief='flat',
            padx=30,
            pady=8,
            command=error_dialog.destroy
        ).pack()
        
        # Auto-focus sur le bouton OK
        error_dialog.bind('<Return>', lambda e: error_dialog.destroy())
        error_dialog.bind('<Escape>', lambda e: error_dialog.destroy())


def demander_prix_achat(parent, title="Prix d'achat", message="Entrez le prix d'achat (€):"):
    """
    Fonction utilitaire pour demander un prix d'achat avec police agrandie
    
    Args:
        parent: Fenêtre parente
        title: Titre de la dialog
        message: Message à afficher
    
    Returns:
        str: Prix saisi ou None si annulé
    """
    dialog = DialogPrixAchat(parent, title, message)
    return dialog.result 