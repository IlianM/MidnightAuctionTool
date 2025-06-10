# 🔍 Onglet Recherche LeBonCoin

## 📋 Vue d'ensemble

L'onglet **Recherche** vous permet de chercher des véhicules directement sur LeBonCoin.fr depuis l'application, d'analyser les prix du marché et d'ajouter facilement des véhicules intéressants à votre liste de repérage.

## 🚀 Installation des dépendances

Avant d'utiliser l'onglet Recherche pour la première fois, vous devez installer les dépendances nécessaires :

### Méthode automatique (recommandée)
1. Exécutez le script `installer_dependances_scraping.py`
2. Suivez les instructions à l'écran

### Méthode manuelle
```bash
pip install requests beautifulsoup4 lxml
```

## 🎯 Fonctionnalités

### 🔍 Recherche personnalisée
- **Modèle** : Nom du véhicule à rechercher (ex: "BMW 118d")
- **Plage d'années** : Année minimum et maximum
- **Plage de kilométrage** : Kilométrage minimum et maximum
- **Nombre d'annonces** : Limite du nombre de résultats (1-200)

### 📊 Analyse automatique
- **Statistiques des prix** : Minimum, maximum, moyenne, médiane
- **Nombre d'annonces** : Total des annonces trouvées
- **Filtrage intelligent** : Seules les annonces pertinentes sont affichées

### 🛠️ Actions disponibles
- **Double-clic** : Ouvrir l'annonce dans le navigateur
- **Ajouter au repérage** : Transférer directement vers l'onglet Repérage
- **Export CSV** : Sauvegarder les résultats
- **Effacer** : Nettoyer les résultats

## 📱 Guide d'utilisation

### 1. Configuration de la recherche
1. Remplissez les champs de recherche :
   - **Modèle** : Soyez précis (ex: "BMW 118d", "Audi A3", "Volkswagen Golf")
   - **Années** : Définissez une plage réaliste
   - **Kilométrage** : Ajustez selon vos critères
   - **Nb annonces** : 50 par défaut (recommandé)

### 2. Lancement de la recherche
1. Cliquez sur **"🔍 Lancer la recherche"**
2. La barre de progression indique l'avancement
3. Le statut affiche les étapes en cours

### 3. Analyse des résultats
- **Tableau** : Liste des annonces avec titre, prix, année, kilométrage
- **Statistiques** : Analyse automatique des prix trouvés
- **Double-clic** : Ouvrir l'annonce complète sur LeBonCoin

### 4. Ajout au repérage
1. Sélectionnez une annonce dans le tableau
2. Cliquez sur **"➕ Ajouter au repérage"**
3. Le véhicule est automatiquement ajouté avec :
   - Le titre comme marque/modèle
   - L'année et le kilométrage
   - Le prix LeBonCoin comme référence
   - Le lien dans les commentaires

## ⚙️ Conseils d'utilisation

### 🎯 Optimiser vos recherches
- **Modèle précis** : "BMW 118d" plutôt que "BMW"
- **Plages réalistes** : Évitez des critères trop restrictifs
- **Multiple recherches** : Testez différentes variantes du modèle

### 📊 Analyser le marché
- Comparez les statistiques avec vos critères de repérage
- Identifiez les bonnes affaires (prix sous la médiane)
- Ajustez vos prix maximum en fonction du marché

### 🔄 Workflow recommandé
1. **Recherche** : Trouvez des véhicules intéressants
2. **Ajout** : Transférez vers le repérage
3. **Enrichissement** : Complétez les informations dans l'onglet Repérage
4. **Suivi** : Utilisez pour le repérage en salle d'enchères

## ⚠️ Limitations et considérations

### 🌐 Dépendance Internet
- Connexion Internet requise
- LeBonCoin doit être accessible
- Délais automatiques entre les requêtes

### 🚫 Blocages possibles
- LeBonCoin peut bloquer les requêtes automatisées
- User-Agents rotatifs pour minimiser les blocages
- Attendez quelques minutes en cas d'erreur 403

### 📝 Qualité des données
- Seules les annonces avec prix, année et kilométrage sont affichées
- Le filtrage se base sur la pertinence du titre
- Les prix peuvent varier selon la négociation

## 🔧 Dépannage

### ❌ Erreurs courantes

**"Module leboncoin_scraper non trouvé"**
- Vérifiez que le dossier `script_scraping_leboncoin` existe
- Exécutez `installer_dependances_scraping.py`

**"Aucune annonce trouvée"**
- Vérifiez vos critères de recherche
- Élargissez les plages d'années/kilométrage
- Testez avec un modèle plus générique

**"Erreur 403 - Forbidden"**
- LeBonCoin bloque temporairement
- Attendez 5-10 minutes avant de relancer
- Vérifiez que l'URL fonctionne dans un navigateur

**"Erreur de connexion"**
- Vérifiez votre connexion Internet
- LeBonCoin peut être temporairement indisponible
- Réessayez plus tard

### 🛠️ Résolution des problèmes

1. **Réinstaller les dépendances**
   ```bash
   pip uninstall requests beautifulsoup4 lxml
   pip install requests beautifulsoup4 lxml
   ```

2. **Tester la connexion**
   - Utilisez le script `test_connection.py` dans le dossier script_scraping_leboncoin

3. **Debug avancé**
   - Activez les logs détaillés dans le code si nécessaire
   - Vérifiez les changements de structure HTML de LeBonCoin

## 🎨 Interface utilisateur

### 📋 Section Paramètres
- **Layout responsive** : S'adapte à la taille de la fenêtre
- **Validation temps réel** : Erreurs affichées immédiatement
- **Sauvegarde automatique** : Les derniers paramètres sont mémorisés

### 📊 Section Résultats
- **Tableau interactif** : Tri et sélection des colonnes
- **Statistiques visuelles** : Affichage clair des métriques
- **Actions contextuelles** : Boutons intelligents selon la sélection

### 🎯 Intégration
- **Cohérence visuelle** : Style identique aux autres onglets
- **Workflow fluide** : Passage naturel vers le repérage
- **Sauvegarde automatique** : Intégration avec le système de journées

---

## 📞 Support

Pour toute question ou problème avec l'onglet Recherche :

1. Consultez cette documentation
2. Vérifiez le dossier `script_scraping_leboncoin/README.md`
3. Testez les scripts de debug inclus
4. Vérifiez que LeBonCoin est accessible depuis votre navigateur

**Note** : Cette fonctionnalité respecte les conditions d'utilisation de LeBonCoin et inclut des délais automatiques pour éviter la surcharge des serveurs. 