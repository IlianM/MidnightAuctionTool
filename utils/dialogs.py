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


class DialogInfoVehicule:
    """Dialog d'information complète sur un véhicule"""
    
    def __init__(self, parent, vehicule):
        self.parent = parent
        self.vehicule = vehicule
        self.mousewheel_bound = False
        
        # Créer la fenêtre dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"🚗 Informations - Lot {vehicule.lot}")
        self.dialog.geometry("800x700")
        self.dialog.resizable(True, True)
        self.dialog.minsize(700, 600)
        
        # Centrer la dialog
        self.center_dialog()
        
        # Rendre la dialog modale
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Créer l'interface
        self.create_interface()
        
        # Bind des événements
        self.dialog.bind('<Escape>', self.on_close)
        
        # Protocole de fermeture
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Attendre la fermeture de la dialog
        self.dialog.wait_window()
    
    def center_dialog(self):
        """Centre la dialog sur l'écran"""
        self.dialog.update_idletasks()
        
        # Obtenir les dimensions
        width = 800
        height = 700
        
        # Calculer la position pour centrer
        pos_x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        pos_y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        
        self.dialog.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
    
    def create_interface(self):
        """Crée l'interface de la dialog"""
        # Scrollable frame principal
        canvas = tk.Canvas(self.dialog, bg='white')
        scrollbar = ttk.Scrollbar(self.dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Header avec couleur
        header_frame = tk.Frame(scrollable_frame, bg=self.get_couleur_hex(), height=80)
        header_frame.pack(fill='x', padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        # Titre du véhicule
        titre_text = f"🚗 {self.vehicule.marque} {self.vehicule.modele}"
        if self.vehicule.annee:
            titre_text += f" ({self.vehicule.annee})"
        
        titre_label = tk.Label(
            header_frame,
            text=titre_text,
            font=('Segoe UI', 24, 'bold'),
            bg=self.get_couleur_hex(),
            fg='white'
        )
        titre_label.pack(expand=True)
        
        # Informations principales
        main_frame = tk.Frame(scrollable_frame, bg='white', padx=30, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Section identité
        self.create_section(main_frame, "🆔 IDENTITÉ", [
            ("Numéro de lot", self.vehicule.lot),
            ("Marque", self.vehicule.marque),
            ("Modèle", self.vehicule.modele),
            ("Année", self.vehicule.annee or "Non spécifiée"),
            ("Kilométrage", self.vehicule.kilometrage or "Non spécifié"),
            ("Motorisation", self.vehicule.motorisation or "Non spécifiée")
        ])
        
        # Section financière
        prix_max = self.vehicule.prix_max_achat or "Non calculé"
        marge = ""
        if self.vehicule.a_prix_achat():
            marge_val = self.vehicule.calculer_marge()
            marge = f"{marge_val:+.0f}€" if marge_val != 0 else "0€"
        
        self.create_section(main_frame, "💰 FINANCIER", [
            ("Prix de revente estimé", f"{self.vehicule.prix_revente}€" if self.vehicule.prix_revente else "Non défini"),
            ("Coût des réparations", f"{self.vehicule.cout_reparations}€" if self.vehicule.cout_reparations else "Non défini"),
            ("Temps de réparations", f"{self.vehicule.temps_reparations}h" if self.vehicule.temps_reparations else "Non défini"),
            ("Prix maximum calculé", prix_max),
            ("Prix d'achat réel", f"{self.vehicule.prix_achat}€" if self.vehicule.prix_achat else "Non acheté"),
            ("Marge réalisée", marge or "N/A")
        ])
        
        # Section réparations
        self.create_section(main_frame, "🔧 RÉPARATIONS", [
            ("Description des travaux", self.vehicule.chose_a_faire or "Aucune description"),
        ], multiline_fields=["Description des travaux"])
        
        # Section métadonnées
        couleur_texte = {
            'turquoise': 'Turquoise 🟦',
            'vert': 'Vert 🟢', 
            'orange': 'Orange 🟠',
            'rouge': 'Rouge 🔴'
        }.get(self.vehicule.couleur, self.vehicule.couleur)
        
        self.create_section(main_frame, "📋 MÉTADONNÉES", [
            ("Statut", self.vehicule.statut),
            ("Couleur", couleur_texte),
            ("Champ libre", self.vehicule.champ_libre or "Vide"),
            ("Réservé aux professionnels", "Oui" if self.vehicule.reserve_professionnels else "Non"),
            ("Date d'achat", self.vehicule.date_achat or "Non acheté")
        ], multiline_fields=["Champ libre"])
        
        # Bouton de fermeture
        close_frame = tk.Frame(scrollable_frame, bg='white', pady=20)
        close_frame.pack(fill='x')
        
        close_btn = tk.Button(
            close_frame,
            text="✅ Fermer",
            font=('Segoe UI', 16, 'bold'),
            bg='#2E86AB',
            fg='white',
            relief='flat',
            padx=30,
            pady=10,
            command=self.on_close
        )
        close_btn.pack()
        
        # Placement des éléments
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel seulement pour cette fenêtre
        def _on_mousewheel(event):
            try:
                # Vérifier que le canvas et la dialog existent encore
                if canvas.winfo_exists() and self.dialog.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except (tk.TclError, AttributeError):
                # Widget détruit, ignorer
                pass
        
        # Bind seulement sur cette fenêtre et ses enfants
        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
        self.dialog.bind("<MouseWheel>", _on_mousewheel)
        self.mousewheel_bound = True
    
    def get_couleur_hex(self):
        """Retourne la couleur hex selon la couleur du véhicule"""
        couleurs = {
            'turquoise': '#1ABC9C',
            'vert': '#2ECC71',
            'orange': '#F39C12', 
            'rouge': '#E74C3C'
        }
        return couleurs.get(self.vehicule.couleur, '#1ABC9C')
    
    def create_section(self, parent, titre, champs, multiline_fields=None):
        """Crée une section d'informations"""
        if multiline_fields is None:
            multiline_fields = []
        
        # Frame de la section
        section_frame = tk.Frame(parent, bg='white', pady=10)
        section_frame.pack(fill='x', pady=(0, 20))
        
        # Titre de section
        titre_label = tk.Label(
            section_frame,
            text=titre,
            font=('Segoe UI', 18, 'bold'),
            bg='white',
            fg='#2C3E50'
        )
        titre_label.pack(anchor='w', pady=(0, 10))
        
        # Champs
        for nom, valeur in champs:
            champ_frame = tk.Frame(section_frame, bg='white')
            champ_frame.pack(fill='x', pady=2)
            
            # Label du champ
            nom_label = tk.Label(
                champ_frame,
                text=f"{nom}:",
                font=('Segoe UI', 14, 'bold'),
                bg='white',
                fg='#34495E',
                width=25,
                anchor='w'
            )
            nom_label.pack(side='left', padx=(10, 5))
            
            # Valeur du champ
            if nom in multiline_fields and str(valeur) and len(str(valeur)) > 10:
                # Formater avec retour à la ligne tous les 50 caractères
                texte_formate = self.formater_texte_avec_retours_ligne(str(valeur), 50)
                
                # Champ multiline pour les longues descriptions (5 lignes maximum)
                nb_lignes = min(5, max(2, len(texte_formate.split('\n'))))
                valeur_text = tk.Text(
                    champ_frame,
                    font=('Segoe UI', 14),
                    height=nb_lignes,
                    width=40,
                    wrap=tk.WORD,
                    relief='flat',
                    bg='#F8F9FA',
                    state='normal'
                )
                valeur_text.insert('1.0', texte_formate)
                valeur_text.config(state='disabled')
                valeur_text.pack(side='left', padx=(5, 10), fill='x', expand=True)
            else:
                # Champ simple
                valeur_label = tk.Label(
                    champ_frame,
                    text=str(valeur),
                    font=('Segoe UI', 14),
                    bg='white',
                    fg='#2C3E50',
                    anchor='w'
                )
                valeur_label.pack(side='left', padx=(5, 10), fill='x', expand=True)
    
    def formater_texte_avec_retours_ligne(self, texte, largeur=50):
        """Formate un texte avec retours à la ligne tous les X caractères"""
        if not texte or len(texte) <= largeur:
            return texte
        
        # Diviser en mots pour éviter de couper au milieu d'un mot
        mots = texte.split()
        lignes = []
        ligne_actuelle = ""
        
        for mot in mots:
            # Si ajouter ce mot dépasse la largeur
            if len(ligne_actuelle + " " + mot) > largeur:
                if ligne_actuelle:  # Si la ligne n'est pas vide
                    lignes.append(ligne_actuelle)
                    ligne_actuelle = mot
                else:  # Mot trop long, le forcer
                    lignes.append(mot)
                    ligne_actuelle = ""
            else:
                if ligne_actuelle:
                    ligne_actuelle += " " + mot
                else:
                    ligne_actuelle = mot
        
        # Ajouter la dernière ligne si elle n'est pas vide
        if ligne_actuelle:
            lignes.append(ligne_actuelle)
        
        return "\n".join(lignes)
    
    def on_close(self, event=None):
        """Ferme la dialog en nettoyant correctement les événements"""
        try:
            # Unbind tous les événements mousewheel spécifiquement liés à cette dialog
            if self.mousewheel_bound:
                # Unbind de tous les widgets de cette dialog
                for widget in [self.dialog] + self.get_all_children(self.dialog):
                    try:
                        widget.unbind("<MouseWheel>")
                    except:
                        pass
                self.mousewheel_bound = False
        except:
            pass
        
        # Détruire la dialog
        self.dialog.destroy()
    
    def get_all_children(self, widget):
        """Retourne tous les widgets enfants récursivement"""
        children = []
        try:
            for child in widget.winfo_children():
                children.append(child)
                children.extend(self.get_all_children(child))
        except:
            pass
        return children


def afficher_info_vehicule(parent, vehicule):
    """Fonction utilitaire pour afficher les informations d'un véhicule"""
    DialogInfoVehicule(parent, vehicule) 