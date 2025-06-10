#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de recherche et analyse d'annonces automobiles sur Leboncoin.fr
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import re
import statistics
from typing import List, Dict, Optional
from urllib.parse import urlencode, quote

class LeboncoinScraper:
    """Classe pour scraper les annonces Leboncoin"""
    
    def __init__(self):
        self.base_url = "https://www.leboncoin.fr/recherche"
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
        ]
        
        # Configuration de session pour éviter les blocages
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
        
    def build_search_url(self, modele: str, annee_min: int, annee_max: int, 
                        km_min: int, km_max: int) -> str:
        """Construit l'URL de recherche Leboncoin"""
        params = {
            'category': '2',  # Catégorie voitures
            'text': modele,
            'regdate': f'{annee_min}-{annee_max}',
            'mileage': f'{km_min}-{km_max}'
        }
        return f"{self.base_url}?{urlencode(params, quote_via=quote)}"
    
    def get_random_user_agent(self) -> str:
        """Retourne un User-Agent aléatoire"""
        return random.choice(self.user_agents)
    
    def extract_price(self, price_text: str) -> Optional[int]:
        """Extrait le prix numérique d'un texte"""
        if not price_text:
            return None
        # Nettoyer le texte (espaces normaux, insécables, etc.)
        clean_text = price_text.replace('\u00A0', ' ').replace('&nbsp;', ' ').strip()
        # Recherche d'un nombre (avec espaces possibles) suivi de €
        price_match = re.search(r'(\d+(?:[\s\u00A0]+\d+)*)\s*€', clean_text)
        if price_match:
            # Supprimer tous les espaces et caractères non-numériques sauf les chiffres
            price_str = re.sub(r'[^\d]', '', price_match.group(1))
            return int(price_str)
        return None
    
    def extract_year(self, text: str) -> Optional[int]:
        """Extrait l'année d'un texte"""
        if not text:
            return None
        # Recherche d'une année (4 chiffres entre 1990 et 2030)
        year_match = re.search(r'\b(19[9]\d|20[0-3]\d)\b', text)
        if year_match:
            return int(year_match.group(1))
        return None
    
    def extract_mileage(self, text: str) -> Optional[int]:
        """Extrait le kilométrage d'un texte"""
        if not text:
            return None
        # Recherche de kilométrage (nombre suivi de km)
        km_match = re.search(r'(\d+(?:\s?\d+)*)\s*km', text.replace(' ', ''), re.IGNORECASE)
        if km_match:
            return int(km_match.group(1).replace(' ', ''))
        return None
    
    def scrape_page(self, url: str) -> List[Dict]:
        """Scrape une page de résultats Leboncoin"""
        # Mise à jour du User-Agent pour cette requête
        self.session.headers.update({
            'User-Agent': self.get_random_user_agent(),
            'Referer': 'https://www.leboncoin.fr/'
        })
        
        try:
            response = self.session.get(url, timeout=15, allow_redirects=True)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            annonces = []
            
            # Recherche des annonces (sélecteurs Leboncoin actualisés)
            ads_containers = soup.find_all('article', {'data-qa-id': 'aditem_container'})
                
            for container in ads_containers:
                try:
                    # Extraction du titre
                    title_elem = container.find(attrs={'data-test-id': 'adcard-title'})
                    title = title_elem.get_text(strip=True) if title_elem else ""
                    
                    # Extraction du prix
                    price_elem = container.find(attrs={'data-test-id': 'price'})
                    price_text = price_elem.get_text(strip=True) if price_elem else ""
                    price = self.extract_price(price_text)
                    
                    # Extraction du lien
                    link_elem = container.find('a', href=re.compile(r'/ad/voitures/'))
                    link = ""
                    if link_elem and link_elem.get('href'):
                        link = link_elem['href']
                        if link.startswith('/'):
                            link = f"https://www.leboncoin.fr{link}"
                    
                    # Extraction des paramètres (année, kilométrage, etc.)
                    params_elem = container.find(attrs={'data-test-id': 'ad-params-light'})
                    params_text = params_elem.get_text(strip=True) if params_elem else ""
                    
                    # Alternative: recherche dans les labels détaillés
                    if not params_text:
                        labels_container = container.find(attrs={'data-test-id': 'ad-params-labels'})
                        if labels_container:
                            params_text = labels_container.get_text(strip=True)
                    
                    # Extraction de l'année et du kilométrage
                    combined_text = f"{title} {params_text}"
                    year = self.extract_year(combined_text)
                    mileage = self.extract_mileage(combined_text)
                    
                    # Ajouter l'annonce si elle a des données valides ET si elle correspond au modèle recherché
                    if title and price and year and mileage:
                        annonces.append({
                            'titre': title,
                            'prix': price,
                            'annee': year,
                            'kilometrage': mileage,
                            'lien': link
                        })
                        
                except Exception as e:
                    # Ignorer silencieusement les erreurs d'extraction individuelles
                    continue
            
            return annonces
            
        except requests.RequestException as e:
            print(f"❌ Erreur lors de la requête: {e}")
            if "403" in str(e) or "Forbidden" in str(e):
                print("🚫 Erreur 403 - Leboncoin bloque probablement les requêtes automatisées")
                print("💡 Suggestions:")
                print("   - Vérifiez que l'URL fonctionne dans un navigateur")
                print("   - Essayez avec des critères de recherche différents")
                print("   - Attendez quelques minutes avant de relancer")
            return []
    
    def is_relevant_ad(self, title: str, modele: str) -> bool:
        """Vérifie si une annonce correspond au modèle recherché"""
        title_lower = title.lower()
        modele_parts = modele.lower().split()
        
        # Vérifier que tous les mots-clés du modèle sont présents
        for part in modele_parts:
            if part not in title_lower:
                return False
        return True
    
    def search_ads(self, modele: str, annee_min: int, annee_max: int, 
                   km_min: int, km_max: int, nb_annonces: int = 50) -> List[Dict]:
        """Recherche des annonces selon les critères spécifiés"""
        
        url = self.build_search_url(modele, annee_min, annee_max, km_min, km_max)
        print(f"\n🔗 Lien de recherche: {url}")
        print(f"🔎 Recherche: {modele} | {annee_min}–{annee_max} | {km_min:,}–{km_max:,} km")
        print("⏳ Récupération en cours...")
        
        # Attendre un peu avant la première requête
        time.sleep(random.uniform(1, 2))
        
        all_ads = []
        page = 1
        max_pages = 10  # Limite pour éviter les boucles infinies
        
        while len(all_ads) < nb_annonces and page <= max_pages:
            # Construction de l'URL avec pagination
            page_url = f"{url}&page={page}" if page > 1 else url
            
            # Scraping de la page
            raw_ads = self.scrape_page(page_url)
            
            if not raw_ads:
                break
            
            # Filtrer les annonces pertinentes
            filtered_ads = [ad for ad in raw_ads if self.is_relevant_ad(ad['titre'], modele)]
            
            all_ads.extend(filtered_ads)
            
            if filtered_ads:
                print(f"📄 Page {page}: {len(filtered_ads)} annonces pertinentes récupérées (total: {len(all_ads)})")
            else:
                print(f"📄 Page {page}: aucune annonce pertinente trouvée")
            
            # Délai entre les requêtes (plus long pour éviter les blocages)
            if page < max_pages and len(all_ads) < nb_annonces:
                time.sleep(random.uniform(3, 6))
            page += 1
        
        # Limiter au nombre demandé
        return all_ads[:nb_annonces]

class DataAnalyzer:
    """Classe pour analyser les données des annonces"""
    
    @staticmethod
    def analyze_prices(annonces: List[Dict]) -> Dict:
        """Analyse statistique des prix"""
        if not annonces:
            return {}
        
        prices = [ad['prix'] for ad in annonces if ad.get('prix')]
        
        if not prices:
            return {}
        
        return {
            'minimum': min(prices),
            'maximum': max(prices),
            'moyenne': int(statistics.mean(prices)),
            'mediane': int(statistics.median(prices)),
            'nombre': len(prices)
        }
    
    @staticmethod
    def display_results(annonces: List[Dict], criteres: Dict):
        """Affiche les résultats de l'analyse"""
        print("\n" + "="*60)
        print("📊 RÉSULTATS DE L'ANALYSE")
        print("="*60)
        
        # Affichage des critères de recherche
        print(f"🔎 Recherche : {criteres['modele']} ({criteres['annee_min']}–{criteres['annee_max']}), "
              f"{criteres['km_min']:,}–{criteres['km_max']:,} km")
        print(f"📄 Annonces analysées : {len(annonces)}")
        
        if len(annonces) < 10:
            print("⚠️  AVERTISSEMENT: Moins de 10 annonces trouvées. "
                  "Les statistiques peuvent ne pas être représentatives.")
        
        # Analyse des prix
        stats = DataAnalyzer.analyze_prices(annonces)
        
        if stats:
            print(f"\n💰 Prix minimum : {stats['minimum']:,} €")
            print(f"💰 Prix maximum : {stats['maximum']:,} €")
            print(f"📈 Prix moyen : {stats['moyenne']:,} €")
            print(f"📊 Prix médian : {stats['mediane']:,} €")
        else:
            print("\n❌ Impossible de calculer les statistiques de prix")
        
        # Affichage des liens
        if annonces:
            print(f"\n🔗 Liens des annonces:")
            for i, ad in enumerate(annonces, 1):
                if ad.get('lien'):
                    print(f"- {ad['lien']}")
                else:
                    print(f"- Annonce {i}: {ad.get('titre', 'Titre non disponible')}")

def get_user_input():
    """Récupère les paramètres de recherche depuis la console"""
    print("🚗 RECHERCHE LEBONCOIN - VOITURES")
    print("="*40)
    
    modele = input("🏷️  Nom du modèle (ex: BMW 118d): ").strip()
    
    while True:
        try:
            annee_min = int(input("📅 Année minimum (ex: 2011): "))
            break
        except ValueError:
            print("❌ Veuillez entrer une année valide")
    
    while True:
        try:
            annee_max = int(input("📅 Année maximum (ex: 2013): "))
            if annee_max >= annee_min:
                break
            else:
                print("❌ L'année maximum doit être supérieure ou égale à l'année minimum")
        except ValueError:
            print("❌ Veuillez entrer une année valide")
    
    while True:
        try:
            km_min = int(input("🏃 Kilométrage minimum (ex: 90000): "))
            break
        except ValueError:
            print("❌ Veuillez entrer un kilométrage valide")
    
    while True:
        try:
            km_max = int(input("🏃 Kilométrage maximum (ex: 110000): "))
            if km_max >= km_min:
                break
            else:
                print("❌ Le kilométrage maximum doit être supérieur ou égal au minimum")
        except ValueError:
            print("❌ Veuillez entrer un kilométrage valide")
    
    nb_annonces_input = input("📊 Nombre d'annonces à analyser (défaut: 50): ").strip()
    nb_annonces = 50
    if nb_annonces_input:
        try:
            nb_annonces = int(nb_annonces_input)
        except ValueError:
            print("❌ Nombre invalide, utilisation de la valeur par défaut: 50")
    
    return {
        'modele': modele,
        'annee_min': annee_min,
        'annee_max': annee_max,
        'km_min': km_min,
        'km_max': km_max,
        'nb_annonces': nb_annonces
    }

def main():
    """Fonction principale"""
    try:
        # Récupération des paramètres utilisateur
        criteres = get_user_input()
        
        # Initialisation du scraper
        scraper = LeboncoinScraper()
        
        # Recherche des annonces
        annonces = scraper.search_ads(
            criteres['modele'],
            criteres['annee_min'],
            criteres['annee_max'],
            criteres['km_min'],
            criteres['km_max'],
            criteres['nb_annonces']
        )
        
        # Affichage des résultats
        DataAnalyzer.display_results(annonces, criteres)
        
    except KeyboardInterrupt:
        print("\n⏹️  Recherche interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    main()