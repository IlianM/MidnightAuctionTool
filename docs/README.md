# 🚗 Gestionnaire d'Enchères Véhicules

Un outil professionnel pour gérer vos achats de véhicules en enchères. Calculez automatiquement les prix maximums d'achat, suivez vos véhicules repérés, et optimisez votre rentabilité.

## �� Fonctionnalités

- 📊 **Dashboard interactif** avec statistiques visuelles en temps réel
- 🔍 **Saisie rapide** de véhicules avec informations complètes
- 💰 **Calcul automatique** du prix maximum d'achat basé sur vos critères
- 📊 **Tableau interactif** pour gérer tous vos véhicules
- 🎨 **Coloration intelligente** des prix (rentable/non rentable)
- 📄 **Export CSV** pour impression et archivage
- ⚙️ **Paramètres personnalisables** (tarifs, marges, commissions)
- 🏆 **Suivi des achats** avec statistiques détaillées

## 💻 Installation

### Pré-requis
- Python 3.8 ou plus récent
- Windows, macOS ou Linux

### 1. Télécharger le projet
```bash
git clone https://github.com/votre-repo/MidnightTuneTool.git
cd MidnightTuneTool
```

### 2. Installer les dépendances
```bash
pip install ttkbootstrap pillow
```

### 3. Générer les données de démonstration (optionnel)
```bash
python demo_data_v4_modulaire.py
```

### 4. Lancer l'application
```bash
python main.py
```

## 🚀 Guide d'utilisation

### Premier lancement
1. **Lancez l'application** : `python main.py`
2. **Configurez vos paramètres** dans l'onglet "⚙️ Paramètres"
   - Tarif horaire main d'œuvre
   - Marge minimum souhaitée
   - Commission de la maison d'enchères
   - Frais fixes par véhicule

### Vue d'ensemble - Dashboard
1. **Onglet "📊 Dashboard"** - Vue d'ensemble de votre activité
2. **Cartes statistiques en temps réel** :
   - 🚗 **Véhicules repérés** : Nombre de véhicules en phase de recherche
   - 🏆 **Véhicules achetés** : Total des acquisitions réalisées
   - 💰 **Marge totale** : Bénéfice cumulé sur tous vos achats
   - 📈 **Marge moyenne** : Bénéfice moyen par véhicule
   - ✅ **Taux de réussite** : Pourcentage d'achats rentables
   - 🥇 **Meilleur achat** : Véhicule avec la plus grosse marge
   - 📉 **Pire achat** : Véhicule avec la plus grosse perte (ou aucune si tout est rentable)
   - 💸 **Budget investi** : Capital total engagé
   - 🎯 **Prix moyen d'achat** : Ticket moyen par véhicule
   - ⚡ **Dernière activité** : Date et véhicule du dernier achat
   - 📊 **Rentabilité** : ROI global de vos investissements
   - 🔥 **Marque favorite** : Marque la plus achetée

3. **Actualisation automatique** : Les statistiques se mettent à jour en temps réel

### Ajouter un véhicule
1. **Onglet "🔍 Phase de Repérage"**
2. **Remplissez les informations** :
   - N° de lot (obligatoire)
   - Marque et modèle (obligatoire)
   - Année, kilométrage
   - Coût et temps des réparations
   - Prix de revente estimé
3. **Le prix maximum d'achat se calcule automatiquement**
4. **Cliquez sur "➕ AJOUTER VÉHICULE"**

### Gérer vos véhicules
- **Édition directe** : Double-cliquez sur une cellule pour la modifier
- **Changer le statut** : Double-cliquez sur "Statut" → Menu déroulant
- **Marquer comme acheté** : Saisissez le prix d'achat OU utilisez le bouton "🏆 MARQUER ACHETÉ"
- **Recherche** : Tapez dans la barre de recherche (lot, marque, modèle)

### Coloration des prix
- 🟢 **Vert** : Achat rentable (prix ≤ prix max)
- 🔴 **Rouge** : Achat à perte (prix > prix max)
- ⚪ **Neutre** : Véhicule en repérage

### Suivi des achats
1. **Onglet "🏆 Véhicules Acquis"**
2. **Consultez vos statistiques** :
   - Marge totale
   - Marge moyenne
   - Nombre de véhicules rentables/à perte
3. **Actions disponibles** :
   - Supprimer un véhicule
   - Remettre en phase de repérage

### Export et sauvegarde
- **Export CSV** : Bouton "📄 EXPORTER" → Compatible Excel/LibreOffice
- **Sauvegarde automatique** : Toutes vos données sont sauvegardées automatiquement
- **Fichiers générés** :
  - `donnees_encheres.json` : Vos véhicules
  - `parametres_encheres.json` : Vos réglages

## ⚙️ Configuration avancée

### Paramètres de calcul
- **Tarif horaire** : Coût de la main d'œuvre (€/h)
- **Type de marge** : Pourcentage ou montant fixe
- **Commission** : Pourcentage de la maison d'enchères
- **Frais fixes** : Coûts administratifs par véhicule

### Formule de calcul
```
Prix Max = Prix Revente - Coût Réparations - (Temps × Tarif Horaire) 
           - Commission - Frais Fixes - Marge Minimum
```

## 🛟 Résolution de problèmes

### L'application ne se lance pas
```bash
# Vérifiez Python
python --version

# Réinstallez les dépendances
pip install --upgrade ttkbootstrap pillow
```

### Erreur "Module not found"
```bash
# Assurez-vous d'être dans le bon dossier
cd MidnightTuneTool

# Vérifiez la structure des fichiers
ls -la
```

### Interface trop petite/grande
- **Maximisez la fenêtre** ou redimensionnez-la
- Les colonnes du tableau sont ajustables en largeur

## 📞 Support

- **Erreurs** : Vérifiez les messages dans la console
- **Données corrompues** : Supprimez `donnees_encheres.json` pour repartir à zéro
- **Réinitialisation** : Bouton "🔄 RÉINITIALISER" dans les paramètres

## 📈 Conseils d'utilisation

### Pour maximiser vos profits
1. **Soyez réaliste** sur les prix de revente
2. **Incluez tous les coûts** (pièces + main d'œuvre)
3. **Gardez une marge de sécurité** (15-20% minimum)
4. **Suivez vos statistiques** pour ajuster votre stratégie

### Bonnes pratiques
- **Mettez à jour régulièrement** vos paramètres selon le marché
- **Exportez vos données** périodiquement
- **Utilisez la recherche** pour retrouver rapidement un véhicule
- **Vérifiez les calculs** avant les enchères importantes

---

**Version 4.0** - Gestionnaire professionnel d'enchères véhicules 🚗✨ 