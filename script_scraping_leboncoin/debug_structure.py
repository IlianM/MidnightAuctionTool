#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de debug pour analyser la structure HTML de Leboncoin
"""

import requests
from bs4 import BeautifulSoup
import re

def analyze_leboncoin_structure():
    """Analyse la structure HTML d'une page de résultats Leboncoin"""
    
    url = "https://www.leboncoin.fr/recherche?category=2&text=bmw%20118d&regdate=2011-2013&mileage=90000-110000"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0',
        'Referer': 'https://www.leboncoin.fr/'
    }
    
    print("🔍 ANALYSE DE LA STRUCTURE HTML LEBONCOIN")
    print("=" * 60)
    print(f"🌐 URL analysée: {url}")
    
    try:
        session = requests.Session()
        session.headers.update(headers)
        response = session.get(url, timeout=15)
        
        print(f"📊 Statut: {response.status_code}")
        print(f"📏 Taille: {len(response.content)} bytes")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Rechercher différents types de conteneurs
        print("\n🔍 RECHERCHE DE CONTENEURS D'ANNONCES:")
        
        # Test 1: Liens vers annonces
        links = soup.find_all('a', href=re.compile(r'/\w+/\d+\.htm'))
        print(f"📌 Liens vers annonces (.htm): {len(links)}")
        
        # Test 2: Éléments avec data-qa-id
        qa_containers = soup.find_all(attrs={'data-qa-id': re.compile(r'.*ad.*', re.I)})
        print(f"📌 Éléments data-qa-id contenant 'ad': {len(qa_containers)}")
        
        # Test 3: Classes contenant 'ad' ou 'card'
        ad_classes = soup.find_all(class_=re.compile(r'.*(ad|card).*', re.I))
        print(f"📌 Classes contenant 'ad' ou 'card': {len(ad_classes)}")
        
        # Test 4: Recherche de prix (pattern € )
        price_elements = soup.find_all(string=re.compile(r'\d+.*€'))
        print(f"📌 Éléments contenant des prix: {len(price_elements)}")
        
        # Analyser les premières annonces trouvées
        if links:
            print(f"\n📋 ANALYSE DES PREMIERS LIENS:")
            for i, link in enumerate(links[:3]):
                print(f"\n--- Annonce {i+1} ---")
                print(f"🔗 Href: {link.get('href', 'N/A')}")
                
                # Chercher le conteneur parent de ce lien
                parent = link.parent
                level = 0
                while parent and level < 5:
                    print(f"Parent niveau {level}: {parent.name} - classes: {parent.get('class', [])}")
                    
                    # Chercher le titre dans ce parent
                    title_candidates = parent.find_all(['h1', 'h2', 'h3', 'h4', 'p'], string=re.compile(r'BMW|bmw', re.I))
                    if title_candidates:
                        print(f"  🏷️  Titre trouvé: {title_candidates[0].get_text(strip=True)}")
                    
                    # Chercher le prix dans ce parent
                    price_candidates = parent.find_all(string=re.compile(r'\d+.*€'))
                    if price_candidates:
                        print(f"  💰 Prix trouvé: {price_candidates[0].strip()}")
                    
                    # Chercher l'année dans ce parent
                    year_candidates = parent.find_all(string=re.compile(r'\b20[01][0-9]\b'))
                    if year_candidates:
                        print(f"  📅 Année trouvée: {year_candidates[0].strip()}")
                    
                    # Chercher le kilométrage dans ce parent
                    km_candidates = parent.find_all(string=re.compile(r'\d+.*km', re.I))
                    if km_candidates:
                        print(f"  🏃 Kilométrage trouvé: {km_candidates[0].strip()}")
                    
                    parent = parent.parent
                    level += 1
                    
                    if level >= 2:  # Limiter pour éviter trop de verbose
                        break
        
        # Sauvegarder un échantillon du HTML pour inspection manuelle
        print(f"\n💾 SAUVEGARDE D'UN ÉCHANTILLON HTML...")
        with open('debug_sample.html', 'w', encoding='utf-8') as f:
            # Sauvegarder juste la partie avec les annonces
            ads_section = soup.find('div', string=re.compile(r'annonces?', re.I))
            if ads_section:
                f.write(str(ads_section.parent))
            else:
                f.write(str(soup)[:50000])  # Premier 50KB du HTML
        
        print("✅ Échantillon sauvegardé dans 'debug_sample.html'")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    analyze_leboncoin_structure() 