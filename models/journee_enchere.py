#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modèle pour représenter une journée d'enchère
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any
from models.vehicule import Vehicule
from config.settings import AppSettings


class JourneeEnchere:
    """Modèle pour une journée d'enchère avec ses véhicules et paramètres"""
    
    def __init__(self, data: Dict[str, Any] = None):
        if data:
            self.id = data.get('id', '')
            self.nom = data.get('nom', '')
            self.date = data.get('date', '')
            self.lieu = data.get('lieu', '')
            self.description = data.get('description', '')
            self.date_creation = data.get('date_creation', datetime.now().isoformat())
            self.parametres = data.get('parametres', {})
            
            # Charger les véhicules
            vehicules_rep_data = data.get('vehicules_reperage', [])
            self.vehicules_reperage = [Vehicule(v_data) for v_data in vehicules_rep_data]
            
            vehicules_ach_data = data.get('vehicules_achetes', [])
            self.vehicules_achetes = [Vehicule(v_data) for v_data in vehicules_ach_data]
        else:
            # Nouvelle journée
            self.id = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.nom = f"Enchère du {datetime.now().strftime('%d/%m/%Y')}"
            self.date = datetime.now().strftime("%Y-%m-%d")
            self.lieu = ""
            self.description = ""
            self.date_creation = datetime.now().isoformat()
            self.parametres = {
                'tarif_horaire': 45.0,
                'commission_vente': 8.5,
                'marge_securite': 200.0
            }
            self.vehicules_reperage: List[Vehicule] = []
            self.vehicules_achetes: List[Vehicule] = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit la journée en dictionnaire pour sauvegarde"""
        return {
            'id': self.id,
            'nom': self.nom,
            'date': self.date,
            'lieu': self.lieu,
            'description': self.description,
            'date_creation': self.date_creation,
            'parametres': self.parametres,
            'vehicules_reperage': [v.to_dict() for v in self.vehicules_reperage],
            'vehicules_achetes': [v.to_dict() for v in self.vehicules_achetes]
        }
    
    def get_nb_vehicules_reperage(self) -> int:
        """Retourne le nombre de véhicules en repérage"""
        return len(self.vehicules_reperage)
    
    def get_nb_vehicules_achetes(self) -> int:
        """Retourne le nombre de véhicules achetés"""
        return len(self.vehicules_achetes)
    
    def get_total_investissement(self) -> float:
        """Calcule le total investi dans cette enchère"""
        total = 0.0
        for vehicule in self.vehicules_achetes:
            try:
                prix = float(vehicule.prix_achat.replace(',', '.')) if vehicule.prix_achat else 0.0
                total += prix
            except:
                pass
        return total
    
    def get_info_carte(self) -> Dict[str, Any]:
        """Retourne les informations pour affichage en carte"""
        return {
            'nom': self.nom,
            'date': self.date,
            'lieu': self.lieu,
            'nb_reperage': self.get_nb_vehicules_reperage(),
            'nb_achetes': self.get_nb_vehicules_achetes(),
            'investissement': self.get_total_investissement(),
            'date_creation': self.date_creation
        }
    
    def mettre_a_jour_parametre(self, nom: str, valeur: Any):
        """Met à jour un paramètre de la journée"""
        self.parametres[nom] = valeur
        
        # Recalculer les prix max pour tous les véhicules
        for vehicule in self.vehicules_reperage:
            vehicule.mettre_a_jour_prix_max_avec_parametres(self.parametres)
    
    def ajouter_vehicule_reperage(self, vehicule: Vehicule):
        """Ajoute un véhicule en repérage"""
        vehicule.mettre_a_jour_prix_max_avec_parametres(self.parametres)
        self.vehicules_reperage.append(vehicule)
    
    def marquer_vehicule_achete(self, index: int, prix_achat: str):
        """Marque un véhicule comme acheté et le transfère"""
        if 0 <= index < len(self.vehicules_reperage):
            vehicule = self.vehicules_reperage[index]
            vehicule.prix_achat = prix_achat
            vehicule.statut = "Acheté"
            vehicule.date_achat = datetime.now().strftime("%Y-%m-%d")
            
            # Transférer vers les achetés
            self.vehicules_achetes.append(vehicule)
            del self.vehicules_reperage[index] 