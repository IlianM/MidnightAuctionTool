# 🚗 Script de Recherche Leboncoin - Voitures

Ce script Python permet d'effectuer une recherche automatisée sur Leboncoin.fr dans la catégorie Voitures, d'extraire les données des annonces et de fournir une analyse statistique détaillée.

## 🎯 Fonctionnalités

- ✅ Recherche personnalisée par modèle, année et kilométrage
- ✅ Construction automatique d'URL Leboncoin avec paramètres
- ✅ Extraction des données : titre, prix, année, kilométrage, liens
- ✅ Analyse statistique complète (min, max, moyenne, médiane)
- ✅ Interface console interactive
- ✅ Gestion des User-Agents aléatoires pour éviter les blocages
- ✅ Délais automatiques entre les requêtes

## 📋 Prérequis

- Python 3.7 ou supérieur
- Connexion Internet

## 🚀 Installation

1. **Cloner ou télécharger les fichiers**
   ```bash
   # Les fichiers nécessaires :
   # - leboncoin_scraper.py
   # - requirements.txt
   # - README.md
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Utilisation

### Lancement du script
```bash
python leboncoin_scraper.py
```

### Paramètres demandés
Le script vous demandera de saisir :

1. **Nom du modèle** (ex: `BMW 118d`)
2. **Année minimum** (ex: `2011`)
3. **Année maximum** (ex: `2013`)
4. **Kilométrage minimum** (ex: `90000`)
5. **Kilométrage maximum** (ex: `110000`)
6. **Nombre d'annonces à analyser** (défaut: `50`)

### Exemple d'exécution
```
🚗 RECHERCHE LEBONCOIN - VOITURES
========================================
🏷️  Nom du modèle (ex: BMW 118d): BMW 118d
📅 Année minimum (ex: 2011): 2011
📅 Année maximum (ex: 2013): 2013
🏃 Kilométrage minimum (ex: 90000): 90000
🏃 Kilométrage maximum (ex: 110000): 110000
📊 Nombre d'annonces à analyser (défaut: 50): 30

🔗 URL de recherche: https://www.leboncoin.fr/recherche?category=2&text=BMW+118d&regdate=2011-2013&mileage=90000-110000
🔎 Recherche : BMW 118d (2011–2013), 90,000–110,000 km
⏳ Récupération des annonces en cours...
📄 Analyse de la page 1...
✅ 15 annonces récupérées (total: 15)
📄 Analyse de la page 2...
✅ 12 annonces récupérées (total: 27)

============================================================
📊 RÉSULTATS DE L'ANALYSE
============================================================
🔎 Recherche : BMW 118d (2011–2013), 90,000–110,000 km
📄 Annonces analysées : 27

💰 Prix minimum : 5,200 €
💰 Prix maximum : 8,900 €
📈 Prix moyen : 7,050 €
📊 Prix médian : 7,100 €

🔗 Liens des annonces:
- https://www.leboncoin.fr/voitures/1234567890.htm
- https://www.leboncoin.fr/voitures/1234567891.htm
- ...
```

## 🛠️ Architecture du Code

### Classes principales

- **`LeboncoinScraper`** : Gère le scraping des pages Leboncoin
  - Construction d'URL dynamique
  - Extraction des données des annonces
  - Gestion des User-Agents et délais

- **`DataAnalyzer`** : Analyse statistique des données
  - Calculs statistiques (min, max, moyenne, médiane)
  - Affichage formaté des résultats

### Fonctions utilitaires

- `get_user_input()` : Interface console interactive
- `main()` : Fonction principale d'orchestration

## ⚠️ Limitations et Considérations

- **Respect du site** : Le script inclut des délais entre requêtes (1-2 secondes)
- **User-Agents rotatifs** : Pour éviter les blocages automatiques
- **Limite de pages** : Maximum 10 pages parcourues par recherche
- **Données valides** : Seules les annonces avec prix, année et kilométrage sont analysées
- **Seuil d'avertissement** : Alerte si moins de 10 annonces trouvées

## 🔧 Personnalisation

### Modifier les critères de recherche
Vous pouvez ajuster les paramètres dans la fonction `build_search_url()` :
```python
params = {
    'category': '2',  # Catégorie voitures
    'text': modele,
    'regdate': f'{annee_min}-{annee_max}',
    'mileage': f'{km_min}-{km_max}',
    # Ajouter d'autres paramètres si nécessaire
}
```

### Modifier les délais
Ajustez les délais dans `search_ads()` :
```python
time.sleep(random.uniform(1, 2))  # Modifier ces valeurs
```

## 📊 Format des Données Extraites

Chaque annonce contient :
```python
{
    'titre': "BMW 118d Sport",
    'prix': 7500,
    'annee': 2012,
    'kilometrage': 95000,
    'lien': "https://www.leboncoin.fr/voitures/..."
}
```

## 🐛 Dépannage

### Erreurs communes

1. **Pas d'annonces trouvées**
   - Vérifiez vos critères de recherche
   - Essayez avec des plages plus larges

2. **Erreurs de connexion**
   - Vérifiez votre connexion Internet
   - Le site peut être temporairement indisponible

3. **Erreurs de parsing**
   - Leboncoin peut avoir modifié sa structure HTML
   - Le script inclut des sélecteurs de fallback

### Debug

Pour activer plus de logs, modifiez la verbosité dans le code :
```python
# Ajouter des print() supplémentaires pour débugger
```

## 📝 Licence

Ce script est fourni à des fins éducatives. Respectez les conditions d'utilisation de Leboncoin.fr.

## 🤝 Contribution

N'hésitez pas à suggérer des améliorations ou à signaler des bugs ! 