#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier la connectivité avec Leboncoin.fr
"""

import requests
import time

def test_leboncoin_access():
    """Test simple d'accès à Leboncoin"""
    
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
        'Cache-Control': 'max-age=0'
    }
    
    # URLs de test
    test_urls = [
        "https://www.leboncoin.fr/",
        "https://www.leboncoin.fr/recherche?category=2",
        "https://www.leboncoin.fr/recherche?category=2&text=bmw%20118d&regdate=2011-2013&mileage=90000-110000"
    ]
    
    print("🧪 TEST DE CONNECTIVITÉ LEBONCOIN")
    print("=" * 50)
    
    session = requests.Session()
    session.headers.update(headers)
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n{i}. Test de l'URL: {url}")
        
        try:
            response = session.get(url, timeout=10)
            print(f"   ✅ Statut: {response.status_code}")
            print(f"   📏 Taille: {len(response.content)} bytes")
            
            # Vérifier si c'est une vraie page ou une page d'erreur
            if response.status_code == 200:
                if "leboncoin" in response.text.lower():
                    print("   🎯 Page Leboncoin détectée")
                else:
                    print("   ⚠️  Contenu suspect (possible redirection)")
                    
            # Délai entre les tests
            if i < len(test_urls):
                print("   ⏱️  Attente de 3 secondes...")
                time.sleep(3)
                
        except requests.RequestException as e:
            print(f"   ❌ Erreur: {e}")
    
    print(f"\n{'=' * 50}")
    print("Test terminé !")

if __name__ == "__main__":
    test_leboncoin_access() 