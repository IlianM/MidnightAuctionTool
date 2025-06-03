#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Service de calcul des prix maximums et marges
"""

from config.settings import AppSettings

class PriceCalculator:
    """Calculateur de prix pour les véhicules"""
    
    def __init__(self, settings: AppSettings):
        self.settings = settings
    
    def calculer_prix_max(self, prix_revente: str, cout_reparations: str, temps_reparations: str) -> str:
        """
        Calcule le prix maximum d'achat basé sur:
        - Prix de revente estimé
        - Coût des réparations
        - Temps de réparations (converti en coût main d'œuvre)
        - Commission de la maison d'enchères
        - Frais fixes
        - Marge minimale souhaitée
        """
        try:
            # Conversion en float
            prix_rev = float(prix_revente or 0)
            cout_rep = float(cout_reparations or 0)
            temps_rep = float(temps_reparations or 0)
            
            # Calcul du coût main d'œuvre
            cout_main_oeuvre = temps_rep * self.settings.parametres['tarif_horaire']
            
            # Coût total des réparations
            cout_total_reparations = cout_rep + cout_main_oeuvre
            
            # Prix net après réparations
            prix_net = prix_rev - cout_total_reparations
            
            # Commission de la maison d'enchères
            commission = prix_net * (self.settings.parametres['commission_enchere'] / 100)
            
            # Prix après commission et frais fixes
            prix_apres_commission = prix_net - commission - self.settings.parametres['frais_fixes']
            
            # Calcul de la marge
            if self.settings.parametres['marge_type'] == 'pourcentage':
                marge = prix_apres_commission * (self.settings.parametres['marge_valeur'] / 100)
            else:
                marge = self.settings.parametres['marge_valeur']
            
            # Prix maximum d'achat
            prix_max = prix_apres_commission - marge
            
            # Formater le résultat
            return f"{max(0, prix_max):.0f}€"
            
        except (ValueError, ZeroDivisionError, TypeError):
            return "0€"
    
    def calculer_details_prix(self, prix_revente: str, cout_reparations: str, temps_reparations: str) -> dict:
        """
        Calcule tous les détails du prix pour affichage détaillé
        Retourne un dictionnaire avec toutes les étapes de calcul
        """
        try:
            # Conversion en float
            prix_rev = float(prix_revente or 0)
            cout_rep = float(cout_reparations or 0)
            temps_rep = float(temps_reparations or 0)
            
            # Calculs étape par étape
            cout_main_oeuvre = temps_rep * self.settings.parametres['tarif_horaire']
            cout_total_reparations = cout_rep + cout_main_oeuvre
            prix_net = prix_rev - cout_total_reparations
            commission = prix_net * (self.settings.parametres['commission_enchere'] / 100)
            prix_apres_commission = prix_net - commission - self.settings.parametres['frais_fixes']
            
            if self.settings.parametres['marge_type'] == 'pourcentage':
                marge = prix_apres_commission * (self.settings.parametres['marge_valeur'] / 100)
                marge_type = f"{self.settings.parametres['marge_valeur']}%"
            else:
                marge = self.settings.parametres['marge_valeur']
                marge_type = f"{marge}€"
            
            prix_max = prix_apres_commission - marge
            
            return {
                'prix_revente': prix_rev,
                'cout_reparations': cout_rep,
                'temps_reparations': temps_rep,
                'tarif_horaire': self.settings.parametres['tarif_horaire'],
                'cout_main_oeuvre': cout_main_oeuvre,
                'cout_total_reparations': cout_total_reparations,
                'prix_net': prix_net,
                'commission_taux': self.settings.parametres['commission_enchere'],
                'commission_montant': commission,
                'frais_fixes': self.settings.parametres['frais_fixes'],
                'prix_apres_commission': prix_apres_commission,
                'marge_type': marge_type,
                'marge_montant': marge,
                'prix_max': max(0, prix_max),
                'rentable': prix_max > 0
            }
            
        except (ValueError, ZeroDivisionError, TypeError):
            return {
                'prix_revente': 0, 'cout_reparations': 0, 'temps_reparations': 0,
                'tarif_horaire': 0, 'cout_main_oeuvre': 0, 'cout_total_reparations': 0,
                'prix_net': 0, 'commission_taux': 0, 'commission_montant': 0,
                'frais_fixes': 0, 'prix_apres_commission': 0, 'marge_type': 'N/A',
                'marge_montant': 0, 'prix_max': 0, 'rentable': False
            }
    
    def formater_kilometrage(self, valeur: str) -> str:
        """Formate automatiquement le kilométrage"""
        if valeur and valeur.isdigit() and not valeur.endswith(',000 km'):
            return f"{valeur},000 km"
        return valeur
    
    def calculer_marge_vehicule(self, prix_max: str, prix_achat: str) -> tuple[float, bool]:
        """
        Calcule la marge d'un véhicule et indique si c'est rentable
        Retourne (marge, est_rentable)
        """
        try:
            prix_max_num = float(prix_max.replace('€', '').replace(',', '.') or 0)
            prix_achat_num = float(prix_achat.replace('€', '').replace(',', '.') or 0)
            
            if prix_achat_num == 0:
                return 0.0, True  # Pas encore acheté
            
            marge = prix_max_num - prix_achat_num
            est_rentable = marge >= 0
            
            return marge, est_rentable
            
        except (ValueError, TypeError):
            return 0.0, True
    
    def obtenir_couleur_prix(self, prix_max: str, prix_achat: str) -> str:
        """
        Retourne la couleur à utiliser pour afficher le prix d'achat
        'vert' si rentable, 'rouge' si à perte, 'neutre' si pas d'achat
        """
        if not prix_achat or prix_achat.strip() == '' or prix_achat == '0':
            return 'neutre'
        
        marge, est_rentable = self.calculer_marge_vehicule(prix_max, prix_achat)
        return 'vert' if est_rentable else 'rouge'
    
    def simuler_achat(self, prix_revente: str, cout_reparations: str, 
                     temps_reparations: str, prix_achat_propose: str) -> dict:
        """
        Simule un achat avec un prix proposé
        Retourne les détails de rentabilité
        """
        details = self.calculer_details_prix(prix_revente, cout_reparations, temps_reparations)
        
        try:
            prix_achat = float(prix_achat_propose.replace('€', '').replace(',', '.') or 0)
            marge_reelle = details['prix_max'] - prix_achat
            profit_theorique = details['prix_apres_commission'] - prix_achat
            
            return {
                'prix_max_recommande': details['prix_max'],
                'prix_achat_propose': prix_achat,
                'marge_vs_recommande': marge_reelle,
                'profit_theorique': profit_theorique,
                'rentable': marge_reelle >= 0,
                'pourcentage_marge': (marge_reelle / prix_achat * 100) if prix_achat > 0 else 0,
                'conseil': self._generer_conseil_achat(marge_reelle, profit_theorique)
            }
            
        except (ValueError, TypeError):
            return {
                'prix_max_recommande': 0, 'prix_achat_propose': 0,
                'marge_vs_recommande': 0, 'profit_theorique': 0,
                'rentable': False, 'pourcentage_marge': 0,
                'conseil': "Données invalides"
            }
    
    def _generer_conseil_achat(self, marge: float, profit: float) -> str:
        """Génère un conseil d'achat basé sur les marges"""
        if marge > 1000:
            return "🟢 Excellente affaire ! Achat fortement recommandé"
        elif marge > 500:
            return "🟡 Bonne affaire, achat recommandé"
        elif marge > 0:
            return "🟠 Marge faible mais acceptable"
        elif marge > -500:
            return "🔴 Perte légère, à éviter"
        else:
            return "🔴 Perte importante ! Ne pas acheter" 