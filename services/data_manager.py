#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Service de gestion des données véhicules
"""

import json
import csv
import os
from typing import List, Optional
from tkinter import filedialog, messagebox

from models.vehicule import Vehicule
from config.settings import AppSettings

class DataManager:
    """Gestionnaire des données véhicules"""
    
    def __init__(self, settings: AppSettings):
        self.settings = settings
        self.vehicules_reperage: List[Vehicule] = []
        self.vehicules_achetes: List[Vehicule] = []
    
    def charger_donnees(self) -> bool:
        """Charge les données depuis le fichier JSON"""
        try:
            if not os.path.exists(self.settings.fichier_donnees):
                return True  # Pas de fichier = première utilisation
            
            with open(self.settings.fichier_donnees, 'r', encoding='utf-8') as f:
                donnees = json.load(f)
            
            # Charger véhicules de repérage
            vehicules_rep_data = donnees.get('vehicules_reperage', [])
            self.vehicules_reperage = [Vehicule(data) for data in vehicules_rep_data]
            
            # Charger véhicules achetés
            vehicules_ach_data = donnees.get('vehicules_achetes', [])
            self.vehicules_achetes = [Vehicule(data) for data in vehicules_ach_data]
            
            print(f"✅ Données chargées: {len(self.vehicules_reperage)} repérage, {len(self.vehicules_achetes)} achetés")
            return True
            
        except Exception as e:
            print(f"❌ Erreur chargement données: {e}")
            return False
    
    def sauvegarder_donnees(self) -> bool:
        """Sauvegarde les données dans le fichier JSON"""
        try:
            donnees = {
                'vehicules_reperage': [v.to_dict() for v in self.vehicules_reperage],
                'vehicules_achetes': [v.to_dict() for v in self.vehicules_achetes]
            }
            
            with open(self.settings.fichier_donnees, 'w', encoding='utf-8') as f:
                json.dump(donnees, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur sauvegarde données: {e}")
            messagebox.showerror("Erreur", f"Sauvegarde impossible: {e}")
            return False
    
    def ajouter_vehicule_reperage(self, vehicule: Vehicule) -> bool:
        """Ajoute un véhicule en repérage"""
        valide, message = vehicule.valider()
        if not valide:
            messagebox.showerror("Erreur", message)
            return False
        
        # Vérifier unicité du lot
        if self.vehicule_existe(vehicule.lot):
            messagebox.showerror("Erreur", f"Le lot {vehicule.lot} existe déjà")
            return False
        
        self.vehicules_reperage.append(vehicule)
        
        # Si prix d'achat renseigné, transférer automatiquement
        if vehicule.a_prix_achat():
            vehicule.marquer_achete()
            self.transferer_vers_achetes(vehicule)
        
        return self.sauvegarder_donnees()
    
    def vehicule_existe(self, lot: str) -> bool:
        """Vérifie si un véhicule avec ce lot existe déjà"""
        return any(v.lot == lot for v in self.vehicules_reperage + self.vehicules_achetes)
    
    def transferer_vers_achetes(self, vehicule: Vehicule):
        """Transfère un véhicule vers les achetés"""
        if not any(v.lot == vehicule.lot for v in self.vehicules_achetes):
            vehicule_copie = Vehicule(vehicule.to_dict())
            vehicule_copie.marquer_achete()
            self.vehicules_achetes.append(vehicule_copie)
    
    def supprimer_vehicule_reperage(self, index: int) -> bool:
        """Supprime un véhicule du repérage"""
        if 0 <= index < len(self.vehicules_reperage):
            del self.vehicules_reperage[index]
            return self.sauvegarder_donnees()
        return False
    
    def supprimer_vehicule_achete(self, index: int) -> bool:
        """Supprime un véhicule des achetés"""
        if 0 <= index < len(self.vehicules_achetes):
            del self.vehicules_achetes[index]
            return self.sauvegarder_donnees()
        return False
    
    def remettre_en_reperage(self, index: int) -> bool:
        """Remet un véhicule acheté en repérage"""
        if 0 <= index < len(self.vehicules_achetes):
            vehicule = self.vehicules_achetes[index]
            vehicule.remettre_en_reperage()
            
            # Ajouter au repérage
            self.vehicules_reperage.append(Vehicule(vehicule.to_dict()))
            
            # Supprimer des achetés
            del self.vehicules_achetes[index]
            
            return self.sauvegarder_donnees()
        return False
    
    def rechercher_vehicules(self, terme: str) -> List[Vehicule]:
        """Recherche des véhicules par terme"""
        if not terme:
            return self.vehicules_reperage
        
        terme = terme.lower()
        return [
            v for v in self.vehicules_reperage
            if (terme in v.lot.lower() or 
                terme in v.marque.lower() or 
                terme in v.modele.lower())
        ]
    
    def mettre_a_jour_vehicule_reperage(self, index: int, champ: str, valeur: str, skip_auto_transfer: bool = False) -> bool:
        """Met à jour un champ d'un véhicule en repérage"""
        vehicules_filtres = self.rechercher_vehicules("")  # Tous les véhicules pour l'instant
        
        if 0 <= index < len(vehicules_filtres):
            vehicule = vehicules_filtres[index]
            setattr(vehicule, champ, valeur)
            
            # Gestion automatique du statut SEULEMENT si pas de skip
            if not skip_auto_transfer:
                if champ == 'prix_achat':
                    if vehicule.a_prix_achat():
                        vehicule.marquer_achete()
                        self.transferer_vers_achetes(vehicule)
                    else:
                        vehicule.remettre_en_reperage()
                
                elif champ == 'statut' and valeur == "Acheté" and vehicule.a_prix_achat():
                    self.transferer_vers_achetes(vehicule)
            
            return self.sauvegarder_donnees()
        
        return False
    
    def exporter_csv(self) -> bool:
        """Exporte les données vers un fichier CSV"""
        if not self.vehicules_reperage:
            messagebox.showwarning("Attention", "Aucun véhicule à exporter")
            return False
        
        try:
            fichier = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Fichier CSV", "*.csv"), ("Tous les fichiers", "*.*")],
                title="Enregistrer le tableau"
            )
            
            if not fichier:
                return False
            
            with open(fichier, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                
                # En-têtes
                headers = [
                    "N° Lot", "Marque", "Modèle", "Année", "Kilométrage", 
                    "À Faire", "Coût Réparations", "Temps Réparations", 
                    "Prix Revente", "Prix Max Achat", "Prix Achat", "Statut", "Marge"
                ]
                writer.writerow(headers)
                
                # Données
                for vehicule in self.vehicules_reperage:
                    writer.writerow(vehicule.to_csv_row())
            
            messagebox.showinfo(
                "📄 Export réussi", 
                f"Tableau exporté vers:\n{fichier}\n\nPrêt pour impression !"
            )
            return True
            
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors de l'export: {e}")
            return False
    
    def get_statistiques(self) -> dict:
        """Retourne les statistiques des véhicules"""
        total_reperage = len(self.vehicules_reperage)
        total_achetes = len(self.vehicules_achetes)
        
        # Calculer marges
        marges = [v.calculer_marge() for v in self.vehicules_achetes if v.a_prix_achat()]
        marge_totale = sum(marges) if marges else 0
        marge_moyenne = marge_totale / len(marges) if marges else 0
        
        return {
            'total_reperage': total_reperage,
            'total_achetes': total_achetes,
            'marge_totale': marge_totale,
            'marge_moyenne': marge_moyenne,
            'vehicules_rentables': len([v for v in self.vehicules_achetes if v.est_rentable()]),
            'vehicules_a_perte': len([v for v in self.vehicules_achetes if not v.est_rentable() and v.a_prix_achat()])
        }

    def ajouter_vehicule(self, vehicule: Vehicule) -> bool:
        """Alias pour ajouter_vehicule_reperage"""
        return self.ajouter_vehicule_reperage(vehicule)

    def supprimer_vehicule(self, index: int) -> bool:
        """Alias pour supprimer_vehicule_reperage"""
        return self.supprimer_vehicule_reperage(index)

    def marquer_achete(self, index: int) -> bool:
        """Marque un véhicule comme acheté et le transfère"""
        if 0 <= index < len(self.vehicules_reperage):
            vehicule = self.vehicules_reperage[index]
            vehicule.marquer_achete()
            self.transferer_vers_achetes(vehicule)
            del self.vehicules_reperage[index]
            return self.sauvegarder_donnees()
        return False 