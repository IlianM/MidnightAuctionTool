#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modèles de données pour les véhicules
"""

from datetime import datetime
from typing import Dict, List, Optional

class Vehicule:
    """Modèle de données pour un véhicule"""
    
    def __init__(self, data: Dict = None):
        """Initialise un véhicule avec les données fournies"""
        if data is None:
            data = {}
        
        self.lot = data.get('lot', '')
        self.marque = data.get('marque', '')
        self.modele = data.get('modele', '')
        self.annee = data.get('annee', '')
        self.kilometrage = data.get('kilometrage', '')
        self.chose_a_faire = data.get('chose_a_faire', '')
        self.cout_reparations = data.get('cout_reparations', '')
        self.temps_reparations = data.get('temps_reparations', '')
        self.prix_revente = data.get('prix_revente', '')  # Prix de revente ESTIMÉ
        self.prix_vente_final = data.get('prix_vente_final', '')  # Prix de vente RÉEL
        self.prix_max_achat = data.get('prix_max_achat', '')
        self.prix_achat = data.get('prix_achat', '')
        self.statut = data.get('statut', 'Repérage')
        self.date_achat = data.get('date_achat', '')
        
        # NOUVEAUX CHAMPS
        self.motorisation = data.get('motorisation', '')
        self.champ_libre = data.get('champ_libre', '')
        self.reserve_professionnels = data.get('reserve_professionnels', False)
        self.couleur = data.get('couleur', 'turquoise')  # Par défaut turquoise
    
    def to_dict(self) -> Dict:
        """Convertit le véhicule en dictionnaire"""
        return {
            'lot': self.lot,
            'marque': self.marque,
            'modele': self.modele,
            'annee': self.annee,
            'kilometrage': self.kilometrage,
            'chose_a_faire': self.chose_a_faire,
            'cout_reparations': self.cout_reparations,
            'temps_reparations': self.temps_reparations,
            'prix_revente': self.prix_revente,
            'prix_vente_final': self.prix_vente_final,
            'prix_max_achat': self.prix_max_achat,
            'prix_achat': self.prix_achat,
            'statut': self.statut,
            'date_achat': self.date_achat,
            # NOUVEAUX CHAMPS
            'motorisation': self.motorisation,
            'champ_libre': self.champ_libre,
            'reserve_professionnels': self.reserve_professionnels,
            'couleur': self.couleur
        }
    
    def est_achete(self) -> bool:
        """Vérifie si le véhicule est acheté"""
        return self.statut == "Acheté"
    
    def a_prix_achat(self) -> bool:
        """Vérifie si le véhicule a un prix d'achat"""
        return self.prix_achat and self.prix_achat.strip() and self.prix_achat != "0"
    
    def marquer_achete(self):
        """Marque le véhicule comme acheté avec la date actuelle"""
        self.statut = "Acheté"
        self.date_achat = datetime.now().strftime("%d/%m/%Y")
    
    def remettre_en_reperage(self):
        """Remet le véhicule en repérage"""
        self.statut = "Repérage"
        self.date_achat = ""
    
    def get_prix_numerique(self, champ: str) -> float:
        """Récupère la valeur numérique d'un prix"""
        try:
            valeur = getattr(self, champ, '0')
            if isinstance(valeur, str):
                # Nettoyer la chaîne (enlever €, espaces, etc.)
                valeur = valeur.replace('€', '').replace(',', '.').strip()
            return float(valeur) if valeur else 0.0
        except (ValueError, AttributeError):
            return 0.0
    
    def calculer_prix_max_automatique(self, settings) -> str:
        """
        NOUVEAU : Calcule automatiquement le prix maximum conseillé selon les paramètres
        """
        try:
            prix_revente = self.get_prix_numerique('prix_revente')
            cout_reparations = self.get_prix_numerique('cout_reparations')
            temps_reparations = self.get_prix_numerique('temps_reparations')
            
            if prix_revente <= 0:
                return ""  # Pas de calcul possible sans prix de revente
            
            prix_max = settings.calculer_prix_max(prix_revente, cout_reparations, temps_reparations)
            return f"{prix_max:.0f}€" if prix_max > 0 else "0€"
            
        except Exception as e:
            print(f"⚠️ Erreur calcul prix max automatique: {e}")
            return ""
    
    def calculer_prix_max_avec_parametres(self, parametres: Dict) -> str:
        """
        NOUVEAU : Calcule le prix maximum avec des paramètres spécifiques d'une journée
        """
        try:
            prix_revente = self.get_prix_numerique('prix_revente')
            cout_reparations = self.get_prix_numerique('cout_reparations')
            temps_reparations = self.get_prix_numerique('temps_reparations')
            
            if prix_revente <= 0:
                return ""  # Pas de calcul possible sans prix de revente
            
            # Récupérer les paramètres de la journée
            tarif_horaire = parametres.get('tarif_horaire', 45.0)
            commission_vente = parametres.get('commission_vente', 8.5)
            marge_securite = parametres.get('marge_securite', 200.0)
            
            # Main d'œuvre = Temps × Tarif horaire
            main_oeuvre = temps_reparations * tarif_horaire
            
            # Commission vente = pourcentage du prix de revente
            commission = prix_revente * (commission_vente / 100)
            
            # Calcul final
            prix_max = prix_revente - (cout_reparations + main_oeuvre) - commission - marge_securite
            
            # Ne pas retourner de valeur négative
            prix_max = max(0, prix_max)
            return f"{prix_max:.0f}€" if prix_max > 0 else "0€"
            
        except Exception as e:
            print(f"⚠️ Erreur calcul prix max avec paramètres: {e}")
            return ""
    
    def mettre_a_jour_prix_max(self, settings):
        """Met à jour automatiquement le prix maximum calculé"""
        self.prix_max_achat = self.calculer_prix_max_automatique(settings)
    
    def mettre_a_jour_prix_max_avec_parametres(self, parametres: Dict):
        """Met à jour le prix max avec des paramètres spécifiques"""
        self.prix_max_achat = self.calculer_prix_max_avec_parametres(parametres)
    
    def calculer_marge(self) -> float:
        """Calcule la marge RÉELLE (prix vente final - prix achat - coûts réparations)"""
        if not self.a_prix_achat():
            return 0.0
        
        prix_vente_final = self.get_prix_numerique('prix_vente_final')
        prix_achat = self.get_prix_numerique('prix_achat')
        cout_reparations = self.get_prix_numerique('cout_reparations')
        
        if prix_vente_final <= 0:
            return 0.0  # Pas encore vendu
        
        return prix_vente_final - prix_achat - cout_reparations
    
    def calculer_ecart_budget(self) -> float:
        """Calcule l'écart par rapport au budget (prix max - prix achat)"""
        if not self.a_prix_achat():
            return 0.0
        
        prix_max = self.get_prix_numerique('prix_max_achat')
        prix_achat = self.get_prix_numerique('prix_achat')
        return prix_max - prix_achat
    
    def calculer_marge_pourcentage(self) -> float:
        """Calcule la marge RÉELLE en pourcentage ((prix_vente_final - prix_achat - coûts) / prix_achat * 100)"""
        prix_achat = self.get_prix_numerique('prix_achat')
        if prix_achat <= 0:
            return 0.0
        
        marge_euros = self.calculer_marge()
        if marge_euros == 0.0:  # Pas encore vendu
            return 0.0
        
        return (marge_euros / prix_achat) * 100
    
    def calculer_ecart_budget_pourcentage(self) -> float:
        """Calcule l'écart budget en pourcentage ((prix_max - prix_achat) / prix_achat * 100)"""
        prix_achat = self.get_prix_numerique('prix_achat')
        if prix_achat <= 0:
            return 0.0
        
        ecart_euros = self.calculer_ecart_budget()
        return (ecart_euros / prix_achat) * 100
    
    def get_marge_str(self) -> str:
        """Retourne la marge formatée selon le contexte (écart budget en repérage, marge réelle si vendu)"""
        if not self.a_prix_achat():
            return "N/A"
        
        # Si vendu (prix vente final renseigné)
        prix_vente_final = self.get_prix_numerique('prix_vente_final')
        if prix_vente_final > 0:
            # Afficher la marge réelle
            marge_euros = self.calculer_marge()
            marge_pourcentage = self.calculer_marge_pourcentage()
            
            signe_euros = "+" if marge_euros >= 0 else ""
            signe_pourcent = "+" if marge_pourcentage >= 0 else ""
            
            return f"{signe_euros}{marge_euros:.0f}€ ({signe_pourcent}{marge_pourcentage:.1f}%)"
        else:
            # Afficher l'écart budget (véhicule acheté mais pas encore vendu)
            ecart_euros = self.calculer_ecart_budget()
            ecart_pourcentage = self.calculer_ecart_budget_pourcentage()
            
            signe_euros = "+" if ecart_euros >= 0 else ""
            signe_pourcent = "+" if ecart_pourcentage >= 0 else ""
            
            return f"Budget: {signe_euros}{ecart_euros:.0f}€ ({signe_pourcent}{ecart_pourcentage:.1f}%)"
    
    def get_ecart_budget_str(self) -> str:
        """Retourne l'écart budget formaté pour l'onglet repérage"""
        if not self.a_prix_achat():
            return "N/A"
        
        ecart_euros = self.calculer_ecart_budget()
        ecart_pourcentage = self.calculer_ecart_budget_pourcentage()
        
        signe_euros = "+" if ecart_euros >= 0 else ""
        signe_pourcent = "+" if ecart_pourcentage >= 0 else ""
        
        return f"{signe_euros}{ecart_euros:.0f}€ ({signe_pourcent}{ecart_pourcentage:.1f}%)"
    
    def est_rentable(self) -> bool:
        """Vérifie si l'achat est rentable (prix achat <= prix max)"""
        if not self.a_prix_achat():
            return True  # Pas encore acheté, considéré comme neutre
        
        prix_max = self.get_prix_numerique('prix_max_achat')
        prix_achat = self.get_prix_numerique('prix_achat')
        return prix_achat <= prix_max
    
    def get_tag_couleur(self) -> str:
        """Retourne le tag de couleur pour l'affichage basé sur la couleur choisie par l'utilisateur"""
        # Mapper les couleurs vers les tags
        couleur_to_tag = {
            'turquoise': 'couleur_turquoise',
            'vert': 'couleur_vert', 
            'orange': 'couleur_orange',
            'rouge': 'couleur_rouge'
        }
        return couleur_to_tag.get(self.couleur, 'couleur_turquoise')
    
    def valider(self) -> tuple[bool, str]:
        """Valide les données du véhicule"""
        if not self.lot.strip():
            return False, "Le numéro de lot est obligatoire"
        
        if not self.marque.strip():
            return False, "La marque est obligatoire"
        
        return True, ""
    
    def to_csv_row(self) -> List[str]:
        """Convertit le véhicule en ligne CSV pour export (MODIFIÉE avec nouveaux champs)"""
        marge = self.calculer_marge()
        marge_str = f"{marge:.0f}€" if marge != 0 else "N/A"
        
        return [
            self.lot,
            self.marque,
            self.modele,
            self.annee,
            self.kilometrage,
            self.motorisation,  # NOUVEAU
            self.chose_a_faire,
            f"{self.cout_reparations}€" if self.cout_reparations else '',
            f"{self.temps_reparations}h" if self.temps_reparations else '',
            f"{self.prix_revente}€" if self.prix_revente else '',
            self.prix_max_achat,
            f"{self.prix_achat}€" if self.prix_achat else '',
            self.statut,
            marge_str,
            self.champ_libre,  # NOUVEAU
            "Oui" if self.reserve_professionnels else "Non",  # NOUVEAU
            self.couleur  # NOUVEAU
        ]
    
    def to_table_row(self) -> tuple:
        """Convertit le véhicule en ligne pour affichage tableau (MODIFIÉE avec nouveaux champs)"""
        return (
            self.lot, self.marque, self.modele, self.annee, self.kilometrage,
            self.motorisation, self.chose_a_faire, self.cout_reparations, self.temps_reparations,
            self.prix_revente, self.prix_max_achat, self.prix_achat, self.statut,
            self.champ_libre, "Oui" if self.reserve_professionnels else "Non"
        )
    
    def to_achetes_row(self) -> tuple:
        """Convertit le véhicule en ligne pour tableau des achetés"""
        marge = self.calculer_marge()
        marge_str = f"+{marge:.0f}€" if marge > 0 else f"{marge:.0f}€"
        
        return (
            self.lot, self.marque, self.modele, self.annee,
            self.prix_achat, self.prix_max_achat, marge_str, self.date_achat
        ) 