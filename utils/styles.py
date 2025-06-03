#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Styles et utilitaires d'interface utilisateur
"""

import tkinter as tk
from tkinter import ttk
from config.settings import AppSettings

class StyleManager:
    """Gestionnaire des styles de l'interface"""
    
    def __init__(self, settings: AppSettings):
        self.settings = settings
        self.style = ttk.Style()
        self.configurer_theme()
    
    def configurer_theme(self):
        """Configure le thème global de l'application"""
        self.style.theme_use('clam')
        
        # Styles des boutons
        boutons_config = [
            ('Primary', self.settings.colors['primary']),
            ('Success', self.settings.colors['success']),
            ('Danger', self.settings.colors['danger']),
            ('Secondary', self.settings.colors['secondary']),
            ('Export', '#6C757D')
        ]
        
        for nom, couleur in boutons_config:
            self.style.configure(
                f'{nom}.TButton',
                background=couleur,
                foreground='white',
                font=('Segoe UI', 10, 'bold'),
                relief='flat',
                borderwidth=0,
                padding=(10, 5)
            )
            
            # Effet hover
            self.style.map(
                f'{nom}.TButton',
                background=[('active', self._darken_color(couleur))]
            )
        
        # Styles des entrées
        self.style.configure(
            'Modern.TEntry',
            fieldbackground=self.settings.colors['white'],
            borderwidth=2,
            relief='solid',
            font=('Segoe UI', 11),
            padding=5
        )
        
        # Styles des notebooks (onglets)
        self.style.configure(
            'Modern.TNotebook',
            background=self.settings.colors['light'],
            borderwidth=0,
            tabmargins=[0, 5, 0, 0]
        )
        
        self.style.configure(
            'Modern.TNotebook.Tab',
            background=self.settings.colors['gray_medium'],
            foreground=self.settings.colors['text_dark'],
            font=('Segoe UI', 11, 'bold'),
            padding=[20, 10],
            borderwidth=0
        )
        
        self.style.map(
            'Modern.TNotebook.Tab',
            background=[('selected', self.settings.colors['primary'])],
            foreground=[('selected', 'white')]
        )
        
        # Styles des treeviews (tableaux)
        self.style.configure(
            'Modern.Treeview',
            background=self.settings.colors['white'],
            foreground=self.settings.colors['text_dark'],
            fieldbackground=self.settings.colors['white'],
            font=('Segoe UI', 10),
            rowheight=80,
            borderwidth=0
        )
        
        self.style.configure(
            'Modern.Treeview.Heading',
            background=self.settings.colors['primary'],
            foreground='white',
            font=('Segoe UI', 11, 'bold'),
            borderwidth=1,
            relief='solid'
        )
        
        self.style.map(
            'Modern.Treeview.Heading',
            background=[('active', self._darken_color(self.settings.colors['primary']))]
        )
        
        # Styles pour les prix colorés
        self.style.configure(
            'Prix.Positif.TLabel',
            foreground='#28a745',
            font=('Segoe UI', 10, 'bold')
        )
        
        self.style.configure(
            'Prix.Negatif.TLabel',
            foreground='#dc3545',
            font=('Segoe UI', 10, 'bold')
        )
    
    def _darken_color(self, color: str, factor: float = 0.8) -> str:
        """Assombrit une couleur hexadécimale"""
        try:
            # Supprimer le # si présent
            color = color.lstrip('#')
            
            # Convertir en RGB
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            
            # Assombrir
            r = int(r * factor)
            g = int(g * factor)
            b = int(b * factor)
            
            # Reconvertir en hex
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return color  # Retourner la couleur originale en cas d'erreur
    
    def creer_header(self, parent) -> tk.Frame:
        """Crée le header de l'application"""
        header_frame = tk.Frame(parent, bg=self.settings.colors['dark'], height=60)
        header_frame.pack(fill='x', pady=(0, 15))
        header_frame.pack_propagate(False)
        
        titre = tk.Label(
            header_frame, 
            text=self.settings.window_config['title'],
            bg=self.settings.colors['dark'], 
            fg=self.settings.colors['accent'],
            font=('Segoe UI', 20, 'bold')
        )
        titre.pack(expand=True)
        
        return header_frame
    
    def creer_champ_saisie(self, parent, label: str, variable: tk.StringVar, 
                          width: int = 15, required: bool = False) -> ttk.Entry:
        """Crée un champ de saisie avec label"""
        frame = tk.Frame(parent, bg=self.settings.colors['white'])
        frame.pack(side="left", padx=(0, 12))
        
        color = self.settings.colors['danger'] if required else self.settings.colors['text_dark']
        label_widget = tk.Label(
            frame, 
            text=label, 
            bg=self.settings.colors['white'], 
            fg=color, 
            font=('Segoe UI', 9, 'bold')
        )
        label_widget.pack()
        
        entry = ttk.Entry(
            frame, 
            textvariable=variable, 
            width=width, 
            style='Modern.TEntry', 
            font=('Segoe UI', 11)
        )
        entry.pack()
        
        return entry
    
    def configurer_treeview_couleurs(self, treeview: ttk.Treeview):
        """Configure les tags de couleur pour un treeview"""
        # Tags pour alternance de couleurs
        treeview.tag_configure('odd', background='#F8F9FA')
        treeview.tag_configure('even', background='white')
        
        # Tags pour prix colorés
        treeview.tag_configure(
            'prix_positif', 
            foreground='#28a745', 
            font=('Segoe UI', 10, 'bold')
        )
        treeview.tag_configure(
            'prix_negatif', 
            foreground='#dc3545', 
            font=('Segoe UI', 10, 'bold')
        )
    
    def creer_bouton_icone(self, parent, text: str, command, style: str, 
                          side: str = "left", **kwargs) -> ttk.Button:
        """Crée un bouton avec icône et style"""
        button = ttk.Button(
            parent, 
            text=text, 
            command=command, 
            style=f'{style}.TButton',
            **kwargs
        )
        button.pack(side=side, padx=5, ipady=4, ipadx=10)
        return button
    
    def creer_labelframe_moderne(self, parent, title: str) -> tk.LabelFrame:
        """Crée un LabelFrame avec style moderne"""
        frame = tk.LabelFrame(
            parent,
            text=title,
            bg=self.settings.colors['white'],
            fg=self.settings.colors['primary'],
            font=('Segoe UI', 12, 'bold'),
            relief='solid',
            borderwidth=1,
            padx=15,
            pady=10
        )
        return frame
    
    def appliquer_effet_survol(self, widget, color_normal: str, color_hover: str):
        """Applique un effet de survol à un widget"""
        def on_enter(e):
            widget.configure(bg=color_hover)
        
        def on_leave(e):
            widget.configure(bg=color_normal)
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

class UIHelpers:
    """Fonctions utilitaires pour l'interface"""
    
    @staticmethod
    def centrer_fenetre(window, width: int, height: int):
        """Centre une fenêtre sur l'écran"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    @staticmethod
    def creer_tooltip(widget, text: str):
        """Crée un tooltip pour un widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(
                tooltip,
                text=text,
                background="lightyellow",
                relief="solid",
                borderwidth=1,
                font=("Segoe UI", 9)
            )
            label.pack()
            
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    @staticmethod
    def animer_widget(widget, propriete: str, valeur_cible, duree: int = 500):
        """Anime une propriété d'un widget (basique)"""
        # Animation simple - peut être étendue
        try:
            widget.configure(**{propriete: valeur_cible})
        except:
            pass
    
    @staticmethod
    def creer_separateur(parent, orientation: str = "horizontal") -> ttk.Separator:
        """Crée un séparateur visuel"""
        separator = ttk.Separator(parent, orient=orientation)
        if orientation == "horizontal":
            separator.pack(fill="x", pady=10)
        else:
            separator.pack(fill="y", padx=10)
        return separator 