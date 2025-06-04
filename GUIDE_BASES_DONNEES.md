# 🗃️ GUIDE - SYSTÈME DE BASES DE DONNÉES SÉPARÉES

## 🎯 **CONCEPT PRINCIPAL**

L'application utilise maintenant un système de **bases de données complètement séparées**. Chaque enchère a son propre fichier JSON et ses données sont totalement isolées des autres.

---

## 🚀 **DÉMARRAGE DE L'APPLICATION**

### **1. Page de sélection**

Au lancement, vous arrivez sur le **sélecteur de base de données** :

- **🗃️ Titre** : "SÉLECTEUR DE BASE DE DONNÉES"
- **📋 Cartes** : Toutes vos bases disponibles
- **➕ Bouton "NOUVELLE BASE"** : Pour créer une nouvelle base
- **🚀 Bouton "LANCER"** : Pour ouvrir une base

### **2. Cartes des bases**

Chaque base de données est représentée par une **carte** affichant :
- **🗃️ Nom de la base**
- **📅 Date** et **📍 lieu**
- **🔍 Nombre de véhicules en repérage**
- **✅ Nombre de véhicules achetés**
- **💰 Total investi**
- **📄 Nom du fichier** (pour info)
- **🚀 Bouton "LANCER"** pour utiliser cette base
- **✏️ Modifier** et **🗑️ Supprimer**

---

## 📂 **STRUCTURE DES FICHIERS**

### **🗂️ Dossier `journees_data/`**

Toutes les bases sont stockées dans le dossier `journees_data/` :

```
journees_data/
├── 20241225_143052_Enchère_Manheim.json
├── 20241226_091530_BCA_Bordeaux.json
├── 20241227_150000_Aramisauto.json
└── migration_20241224_120000.json
```

### **📄 Format des fichiers**

Chaque fichier contient :
- **Informations** de l'enchère (nom, date, lieu)
- **Véhicules de repérage** avec leurs données
- **Véhicules achetés** avec prix d'achat
- **Paramètres spécifiques** (tarifs, commissions, marges)

---

## 🆕 **CRÉER UNE NOUVELLE BASE**

### **➕ Nouvelle base de données**

1. Cliquez sur **"➕ NOUVELLE BASE"**
2. Remplissez le formulaire :
   - **Nom de l'enchère** (obligatoire)
   - **Date** (YYYY-MM-DD)
   - **Lieu** 
   - **Description**
3. Cliquez **"✅ Créer"**

### **📄 Nom du fichier automatique**

Le fichier est créé automatiquement avec le format :
```
YYYYMMDD_HHMMSS_NomEnchère.json
```

Exemple : `20241225_143052_Enchère_Manheim.json`

---

## 🚀 **UTILISER UNE BASE**

### **🎯 Sélection et lancement**

1. **Choisissez** la base à utiliser
2. Cliquez sur **"🚀 LANCER"**
3. L'application s'ouvre avec **cette base uniquement**

### **🔙 Interface principale**

Une fois lancée, vous avez :
- **🔙 Bouton retour** : Revient au sélecteur
- **Interface habituelle** : Repérage, Achetés, Paramètres
- **Données isolées** : Seuls les véhicules de cette base

---

## ⚙️ **AVANTAGES DU SYSTÈME**

### **🔒 Séparation totale**

- **Aucun mélange** entre enchères différentes
- **Données propres** par événement
- **Historique préservé** par base

### **📊 Gestion flexible**

- **Paramètres dédiés** par enchère
- **Stratégies différentes** selon le contexte
- **Archivage naturel** des anciennes enchères

### **🛡️ Sécurité**

- **Un fichier corrompu** n'affecte pas les autres
- **Sauvegarde** et **restauration** sélectives
- **Migration** automatique des anciennes données

---

## 🔧 **GESTION DES BASES**

### **✏️ Modifier une base**

1. Cliquez sur **"✏️"** de la carte
2. Modifiez les informations
3. **Les véhicules** ne sont pas affectés

### **🗑️ Supprimer une base**

1. Cliquez sur **"🗑️"** rouge
2. **⚠️ ATTENTION** : Suppression définitive du fichier
3. **Impossible** de supprimer la dernière base

### **🔄 Actualiser**

- Bouton **"🔄 Actualiser"** pour recharger la liste
- Détecte les nouveaux fichiers ajoutés manuellement

---

## 🔄 **MIGRATION AUTOMATIQUE**

### **📦 Données existantes**

L'application migre automatiquement :
- **Ancien système** `journees_encheres.json` → Fichiers séparés
- **Très ancien système** `donnees_encheres.json` → Nouvelle base
- **Fichiers sauvegardés** avec extension `.backup`

### **✅ Aucune perte**

- **Tous les véhicules** sont préservés
- **Paramètres** conservés
- **Historique** intact

---

## 🎯 **WORKFLOW RECOMMANDÉ**

### **📅 Avant chaque enchère**

1. **Créer** une nouvelle base avec nom explicite
2. **Configurer** les paramètres spécifiques
3. **Saisir** les véhicules d'intérêt

### **🏆 Pendant l'enchère**

1. **Lancer** la base de l'enchère en cours
2. **Marquer** les véhicules achetés
3. **Suivre** les investissements en temps réel

### **📊 Après l'enchère**

1. **Analyser** les résultats
2. **Conserver** la base pour historique
3. **Créer** une nouvelle base pour la prochaine

---

## 📂 **UTILISATION AVANCÉE**

### **💾 Sauvegarde manuelle**

Copiez le dossier `journees_data/` pour sauvegarder toutes vos bases :
```
backup_20241225/
└── journees_data/
    ├── base1.json
    ├── base2.json
    └── ...
```

### **🔄 Partage de bases**

Vous pouvez partager une base spécifique :
1. Copiez le fichier `.json` souhaité
2. Placez-le dans le dossier `journees_data/` de l'autre installation
3. Actualisez la liste

### **🛠️ Maintenance**

- **Nettoyage** : Supprimez les bases très anciennes
- **Organisation** : Renommez les fichiers si nécessaire
- **Archivage** : Déplacez les anciennes bases dans un dossier à part

---

## 🚀 **AVANTAGES POUR L'UTILISATEUR**

### **🎯 Clarté d'utilisation**

- **Plus de mélange** entre enchères d'il y a 1 an et aujourd'hui
- **Vision claire** de chaque événement
- **Navigation intuitive** entre bases

### **⚡ Performance**

- **Chargement plus rapide** (une seule base à la fois)
- **Interface réactive** avec données ciblées
- **Moins de mémoire** utilisée

### **🔧 Flexibilité**

- **Paramètres adaptés** à chaque enchère
- **Stratégies différentes** selon le contexte
- **Historique préservé** sans encombrement

---

## 💡 **CONSEILS D'UTILISATION**

### **📝 Nommage des bases**

Utilisez des noms explicites :
- ✅ "Enchère Manheim Paris - 25/12/2024"
- ✅ "BCA Bordeaux Décembre"
- ❌ "Test" ou "Enchère 1"

### **🗂️ Organisation**

- **Une base** = **Une enchère** ou **Un événement**
- **Archivez** les bases très anciennes
- **Conservez** les bases importantes pour référence

### **🔄 Habitudes**

- **Créez** la base avant l'enchère
- **Lancez** uniquement la base du jour
- **Retournez** au sélecteur entre enchères

---

## 🎯 **RÉSUMÉ SIMPLE**

1. **🗃️ Sélecteur** : Choisir quelle base utiliser
2. **🚀 Lancer** : Ouvrir l'application avec cette base
3. **🔙 Retour** : Revenir au sélecteur pour changer de base
4. **➕ Nouveau** : Créer une base pour une nouvelle enchère

**Chaque base = Ses propres véhicules et paramètres !** 