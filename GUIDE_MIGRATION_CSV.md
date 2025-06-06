# 📊📄 Guide de Migration - Ancienne vers Nouvelle Version

## 🎯 Pour qui est ce guide ?

Ce guide est destiné aux utilisateurs qui ont :
- ✅ Des données dans l'**ancienne version** du logiciel
- ✅ Seulement le fichier `.exe` (pas de fichier Python)
- ✅ Besoin de **migrer leurs données** vers la nouvelle version

## 🔄 **NOUVEAUTÉ : Import PDF Automatique !**

La nouvelle version peut maintenant **importer directement des fichiers PDF** ! Plus besoin de convertir manuellement.

### **📄 Option 1: Import PDF (RECOMMANDÉ)**

Si vous avez des **catalogues PDF** ou des **listes de véhicules en PDF** :

1. **Cliquez sur le bouton rose** `📄 Importer PDF` dans l'interface
2. **Sélectionnez votre fichier PDF**
3. **Le système analyse automatiquement** :
   - 📊 **Tableaux** dans le PDF (méthode principale)
   - 📝 **Texte brut** si pas de tableaux détectés
   - 🚗 **Marques de voitures** reconnues automatiquement
   - 💰 **Prix** extraits avec les symboles € 
   - 📅 **Années** et 📏 **kilomètres** détectés
4. **Donnez un nom** à votre nouvelle base
5. **Vérifiez les résultats** et ajustez si nécessaire

#### **Types de PDF Supportés :**
- ✅ **Catalogues de vente** avec tableaux
- ✅ **Listes de véhicules** structurées  
- ✅ **Rapports d'enchères** exportés
- ✅ **Documents** contenant marques et prix
- ✅ **PDFs** avec texte sélectionnable (pas d'images scannées)

#### **Données Automatiquement Reconnues :**
| **Type de Donnée** | **Mots-clés Reconnus** |
|-------------------|----------------------|
| **Marques Auto** | Peugeot, Renault, Citroën, VW, Audi, BMW, Mercedes, Ford, Toyota, etc. |
| **Prix** | `1500€`, `2 500 €`, `3500`, suivi de € |
| **Années** | `2018`, `2020`, formats 4 chiffres |
| **Kilomètres** | `120000 km`, `50 000 kilomètres` |
| **Colonnes** | `lot`, `marque`, `modèle`, `prix`, `achat`, etc. |

---

### **📊 Option 2: Import CSV (Méthode Classique)**

Si l'import PDF ne fonctionne pas ou si vous préférez CSV :

### **Étape 1: Exporter vos données depuis l'ancienne version**

1. **Ouvrez votre ancienne version** du logiciel
2. **Exportez vos données en CSV** :
   - Allez dans `Menu` → `Exporter` → `CSV`
   - Ou utilisez le bouton `📊 Exporter CSV` s'il existe
   - **Importante** : Exportez VOS DEUX ONGLETS :
     - Les véhicules **en repérage**
     - Les véhicules **achetés**

3. **Sauvegardez les fichiers CSV** dans un endroit facile à retrouver (ex: Bureau)

---

### **Étape 2: Préparer le fichier CSV pour l'import**

Si vous avez **2 fichiers CSV séparés** (repérage + achetés), vous pouvez :

**Option A - Combiner les fichiers :**
1. Ouvrez les 2 fichiers CSV dans Excel/LibreOffice
2. Copiez toutes les lignes du fichier "achetés" dans le fichier "repérage"
3. Sauvegardez le fichier combiné

**Option B - Importer séparément :**
1. Importez d'abord le fichier "repérage"
2. Puis importez le fichier "achetés" dans une nouvelle base

---

### **Étape 3: Importer dans la nouvelle version**

1. **Ouvrez la nouvelle version** du logiciel
2. Sur l'écran de sélection des bases de données, cliquez sur :
   ```
   📊 Importer CSV
   ```

3. **Sélectionnez votre fichier CSV**

4. **Donnez un nom** à votre nouvelle base de données :
   ```
   Exemple: "Mes données - Ancienne version"
   ```

5. **Attendez l'import** - Une fenêtre de progression s'affiche

6. **Vérifiez le résultat** - Un message vous indiquera :
   - ✅ Nombre de véhicules importés
   - 📊 Répartition (repérage vs achetés)

---

## 🗂️ Colonnes CSV Reconnues Automatiquement

Le système reconnaît automatiquement ces noms de colonnes :

| Type de Donnée | Noms Reconnus |
|----------------|---------------|
| **Numéro de lot** | `lot`, `n°lot`, `numero lot`, `LOT`, `N° LOT` |
| **Marque** | `marque`, `MARQUE`, `Marque` |
| **Modèle** | `modele`, `modèle`, `MODELE`, `MODÈLE` |
| **Année** | `annee`, `année`, `ANNEE`, `ANNÉE` |
| **Kilométrage** | `kilometrage`, `kilométrage`, `km`, `KM` |
| **Prix de revente** | `prix_revente`, `prix revente`, `PRIX REVENTE` |
| **Coût réparations** | `cout_reparations`, `coût réparations`, `COUT REPARATIONS` |
| **Temps réparations** | `temps_reparations`, `temps réparations`, `TEMPS REPARATIONS` |
| **Prix d'achat** | `prix_achat`, `prix achat`, `PRIX ACHAT` |
| **Statut** | `statut`, `STATUT`, `Statut` |

---

## 🔧 Que Faire si l'Import Échoue ?

### **Problème 1: Erreur d'encodage**
```
❌ Erreur: Erreur d'encodage du fichier CSV
```
**Solution :**
1. Ouvrez votre CSV dans Excel
2. `Fichier` → `Enregistrer sous`
3. Choisissez `CSV UTF-8` comme format
4. Réessayez l'import

### **Problème 2: Colonnes non reconnues**
```
❌ Erreur: Certaines colonnes non trouvées
```
**Solution :**
1. Vérifiez les noms de colonnes dans votre CSV
2. Renommez-les selon le tableau ci-dessus
3. Exemple : `Prix_Achat` → `prix_achat`

### **Problème 3: Séparateur de colonnes**
**Solution :**
Le système détecte automatiquement `;` ou `,` mais si ça ne marche pas :
1. Ouvrez le CSV dans un éditeur de texte
2. Remplacez tous les `;` par des `,` (ou vice versa)
3. Sauvegardez et réessayez

---

## ✅ Vérification Après Import

Après l'import réussi :

1. **Ouvrez votre nouvelle base** en cliquant sur `📂 Ouvrir`

2. **Vérifiez les onglets :**
   - 🔍 **Repérage** : Véhicules non achetés
   - 🏆 **Achetés** : Véhicules avec prix d'achat

3. **Vérifiez les données :**
   - Nombres de véhicules corrects
   - Prix affichés correctement
   - Calculs automatiques fonctionnent

4. **Testez les nouvelles fonctionnalités :**
   - Colonnes **Motorisation** et **Champ libre**
   - **Couleurs** des lignes (turquoise par défaut)
   - **Tri** des colonnes
   - **Export PDF** amélioré

---

## 🚀 Nouvelles Fonctionnalités Disponibles

Après la migration, vous bénéficiez de :

### **Améliorations Interface :**
- 📱 Interface plus moderne
- 🎨 Choix de couleurs pour les lignes
- 📏 Polices agrandies et ajustables
- 🔍 Recherche instantanée
- ↕️ Tri par colonne

### **Nouvelles Colonnes :**
- 🚗 **Motorisation** (Diesel, Essence, Hybride...)
- 📝 **Champ libre** (notes personnelles)
- ✅ **Réservé aux professionnels**
- 💰 **Prix de vente final** (distinction avec estimation)

### **Calculs Améliorés :**
- 💸 **Vraie marge** = Prix vente final - Prix achat - Coûts
- 📊 **Écart budget** = Prix max - Prix achat
- 📈 Statistiques automatiques plus précises

### **Exports Modernisés :**
- 📄 **PDF professionnel** avec toutes les colonnes
- 📊 **CSV complet** avec nouveaux champs
- 🏷️ **Retour à la ligne automatique** dans les PDFs

---

## ❓ Aide et Support

Si vous rencontrez des problèmes :

1. **Vérifiez ce guide** en premier
2. **Testez avec un petit fichier CSV** pour identifier le problème
3. **Contactez le support** avec :
   - Le message d'erreur exact
   - Les premières lignes de votre fichier CSV
   - Le nombre de lignes dans votre fichier

---

## 🎉 Félicitations !

Une fois l'import terminé, vous avez :
- ✅ Toutes vos données migrées
- 🆕 Accès aux nouvelles fonctionnalités  
- 🗃️ Système de bases de données séparées
- 💾 Sauvegarde automatique améliorée

**Bon business avec la nouvelle version ! 🚗💰** 