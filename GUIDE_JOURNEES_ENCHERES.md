# 🏁 GUIDE - SYSTÈME DE JOURNÉES D'ENCHÈRES

## 🎯 **NOUVEAU SYSTÈME**

L'application a été **complètement réorganisée** pour gérer **plusieurs journées d'enchères distinctes**, chacune avec ses propres véhicules et paramètres.

---

## 🚀 **DÉMARRAGE DE L'APPLICATION**

### **1. Page d'accueil - Sélection des journées**

Au lancement, vous arrivez sur la **page de sélection des journées d'enchères** :

- **🏆 Titre principal** : "GESTIONNAIRE D'ENCHÈRES VÉHICULES"
- **📋 Zone de cartes** : Affiche toutes vos journées d'enchères sous forme de cartes
- **➕ Bouton "NOUVELLE JOURNÉE"** : Pour créer une nouvelle enchère

### **2. Cartes des journées**

Chaque journée est représentée par une **carte moderne** affichant :
- **🏆 Nom de l'enchère**
- **📅 Date** et **📍 lieu** (si renseignés)
- **🔍 Nombre de véhicules en repérage**
- **✅ Nombre de véhicules achetés**
- **💰 Total investi**
- **🚀 Bouton "OUVRIR"** pour accéder à la journée
- **✏️ Bouton modifier** et **🗑️ bouton supprimer**

---

## 📋 **GESTION DES JOURNÉES**

### **✨ Créer une nouvelle journée**

1. Cliquez sur **"➕ NOUVELLE JOURNÉE"**
2. Remplissez le formulaire :
   - **Nom de l'enchère** (obligatoire) : Ex. "Enchère Manheim Paris"
   - **Date** (format YYYY-MM-DD) : Ex. "2024-12-25"
   - **Lieu** : Ex. "Paris - Rungis"
   - **Description** : Notes ou informations complémentaires
3. Cliquez **"✅ Créer"**

### **✏️ Modifier une journée**

1. Cliquez sur le bouton **"✏️"** de la carte
2. Modifiez les informations souhaitées
3. Cliquez **"✅ Modifier"**

### **🗑️ Supprimer une journée**

1. Cliquez sur le bouton **"🗑️"** rouge de la carte
2. **⚠️ ATTENTION** : Tous les véhicules et données seront **définitivement perdus**
3. Confirmez la suppression

> **📌 Note** : Impossible de supprimer la dernière journée restante

---

## 🚗 **INTERFACE PRINCIPALE D'UNE JOURNÉE**

### **🔙 Barre de navigation**

En haut de l'interface :
- **🔙 Bouton "Retour aux journées"** : Revient à la sélection
- **🏆 Nom de la journée** avec date et lieu
- **📊 Statistiques** : Nombre de véhicules en repérage et achetés

### **📑 Onglets disponibles**

1. **🔍 Repérage** : Gestion des véhicules à évaluer
2. **🏆 Véhicules Achetés** : Véhicules déjà acquis
3. **⚙️ Paramètres** : Configuration **spécifique à cette journée**

---

## ⚙️ **PARAMÈTRES PAR JOURNÉE**

### **🎯 Principe fondamental**

Chaque journée d'enchère a ses **propres paramètres** :
- **💰 Tarif horaire** différent selon l'enchère
- **💸 Commission de vente** variable
- **🛡️ Marge de sécurité** adaptée
- **🎨 Mode sombre** personnel

### **📊 Calcul du Prix Maximum**

Le prix maximum d'achat est **calculé automatiquement** selon la formule :

```
Prix Max = Prix Revente - (Coût Réparations + Main d'Œuvre) - Commission Vente - Marge Sécurité
```

Où :
- **Main d'Œuvre** = Temps Réparations × Tarif Horaire
- **Commission** = Prix Revente × (% Commission / 100)

### **🔧 Modifier les paramètres**

1. Allez dans l'onglet **"⚙️ Paramètres"**
2. Ajustez les valeurs selon votre stratégie pour cette enchère
3. Cliquez **"💾 Sauvegarder les paramètres"**
4. **✅ Tous les prix maximums** sont automatiquement recalculés

---

## 🚀 **AVANTAGES DU NOUVEAU SYSTÈME**

### **🎯 Séparation claire**

- **Chaque enchère** est indépendante
- **Paramètres dédiés** à chaque événement
- **Historique** maintenu par journée

### **📊 Gestion optimisée**

- **Stratégies différentes** selon l'enchère (tarifs, marges)
- **Comparaison** entre journées
- **Archivage** naturel des anciennes enchères

### **🔒 Sécurité des données**

- **Isolation** des données par journée
- **Migration automatique** des anciennes données
- **Sauvegarde indépendante** de chaque journée

---

## 📂 **MIGRATION DES DONNÉES**

### **🔄 Migration automatique**

Au premier lancement, l'application :
1. **Détecte** automatiquement les anciennes données
2. **Crée** une journée "Migration - Données existantes"
3. **Transfère** tous vos véhicules et paramètres
4. **Conserve** l'intégralité de vos données

### **✅ Aucune perte de données**

- Tous vos véhicules sont préservés
- Vos paramètres sont conservés
- Votre historique reste intact

---

## 🎯 **WORKFLOW RECOMMANDÉ**

### **📅 Avant une enchère**

1. **Créer** une nouvelle journée avec nom, date, lieu
2. **Configurer** les paramètres (tarifs, commissions, marges)
3. **Saisir** les véhicules d'intérêt en repérage

### **🏆 Pendant l'enchère**

1. **Ouvrir** la journée correspondante
2. **Marquer** les véhicules achetés avec prix réel
3. **Suivre** en temps réel : rentabilité et investissement

### **📊 Après l'enchère**

1. **Analyser** les résultats dans l'onglet "Véhicules Achetés"
2. **Conserver** la journée pour historique
3. **Créer** une nouvelle journée pour la prochaine enchère

---

## 🔧 **FONCTIONNALITÉS CONSERVÉES**

### **✅ Toutes vos fonctionnalités préférées**

- **🔍 Saisie rapide** de véhicules
- **📋 Tableaux** interactifs avec édition
- **🔎 Recherche** instantanée
- **💡 Tooltips** avec polices agrandies
- **🏆 Dialog** moderne pour prix d'achat
- **📊 Calcul automatique** des prix maximum
- **📁 Export CSV** des données

### **⚡ Améliorations**

- **Interface** plus moderne avec CustomTkinter
- **Navigation** intuitive entre journées
- **Paramètres** flexibles par enchère
- **🎨 Cartes** élégantes pour les journées

---

## 📞 **ASSISTANCE**

### **❓ Besoin d'aide ?**

- **Survolez** les éléments pour voir les tooltips explicatifs
- **Cliquez** sur "❓ Aide" dans les paramètres
- **Consultez** ce guide pour toute question

### **🎯 Fonctionnement optimal**

Le système a été conçu pour une **utilisation intuitive** :
- **Navigation** naturelle entre journées et interface
- **Sauvegarde automatique** de toutes les modifications
- **Feedback visuel** pour toutes les actions

---

## 🚀 **PROFITEZ DE VOTRE NOUVELLE EXPÉRIENCE !**

Le système de journées d'enchères rend votre gestion **plus professionnelle, plus organisée et plus efficace**. 

**Bonne enchère !** 🏆 