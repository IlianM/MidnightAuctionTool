# 📄 Guide Import PDF - Reconnaissance Automatique de Véhicules

## 🎯 **Nouvelle Fonctionnalité : Import PDF Intelligent**

La nouvelle version peut automatiquement **analyser des fichiers PDF** et extraire les données de véhicules pour créer une base de données complète !

---

## 🚀 **Comment Utiliser l'Import PDF**

### **Étape 1: Accéder à la Fonction**
1. **Ouvrez le logiciel** 
2. Sur l'écran de sélection des bases, cliquez sur le **bouton rose** :
   ```
   📄 Importer PDF
   ```

### **Étape 2: Sélectionner le Fichier**
1. **Choisissez votre PDF** dans l'explorateur
2. **Donnez un nom** à votre future base de données
3. **Confirmez** - L'analyse commence automatiquement

### **Étape 3: Analyse Automatique**
Le système effectue une **double analyse** :

1. **🗂️ Recherche de Tableaux**
   - Détecte les tableaux structurés
   - Analyse les en-têtes de colonnes
   - Extrait ligne par ligne

2. **📝 Analyse de Texte Brut** (si pas de tableau)
   - Recherche les marques automobiles
   - Extrait prix, années, kilomètres
   - Reconstitue les informations véhicule

---

## ✅ **Types de PDF Supportés**

### **📊 PDFs avec Tableaux (Optimal)**
```
| LOT | MARQUE   | MODÈLE  | ANNÉE | KM     | PRIX    |
|-----|----------|---------|-------|--------|---------|
| 001 | Peugeot  | 308     | 2018  | 120000 | 8500€   |
| 002 | Renault  | Clio    | 2020  | 80000  | 12000€  |
```

### **📝 PDFs avec Texte Libre**
```
Lot 1 : Peugeot 308 de 2018, 120 000 km - Prix estimé : 8500€
Lot 2 : Renault Clio de 2020, 80 000 km - Prix : 12000€
Véhicule 3 : BMW Série 3 2019 - 95000 km - 18500€
```

### **📋 Catalogues d'Enchères**
```
ENCHÈRES AUTOMOBILES - 15 JANVIER 2024

N°1  PEUGEOT 308 Active
     Année : 2018 | Kilométrage : 120 000 km
     Estimation : 8 000 - 9 000 €

N°2  RENAULT CLIO Zen  
     Année : 2020 | Kilométrage : 80 000 km
     Estimation : 11 500 - 12 500 €
```

---

## 🧠 **Reconnaissance Automatique**

### **🚗 Marques Automobiles Reconnues**
Le système reconnaît automatiquement **25+ marques** :
- **Françaises** : Peugeot, Renault, Citroën, Dacia
- **Allemandes** : Volkswagen, VW, Audi, BMW, Mercedes, Opel
- **Japonaises** : Toyota, Honda, Nissan, Mazda, Mitsubishi, Suzuki
- **Coréennes** : Hyundai, Kia
- **Autres** : Ford, Volvo, Seat, Skoda, Fiat, Alfa, Mini, Smart

### **💰 Formats de Prix Reconnus**
- `8500€`, `8 500 €`, `8.500€`
- `8500`, `8 500` (sans symbole)
- `8500,00€`, `8.500,00€`

### **📅 Formats d'Années**
- `2018`, `2020`, `2024` (4 chiffres)
- Années entre 1980 et 2030

### **📏 Formats Kilométrage**
- `120000 km`, `120 000 km`
- `120000 kilomètres`, `120k km`

---

## 🔍 **Mapping Automatique des Colonnes**

Si votre PDF contient un tableau, le système mappe automatiquement :

| **Champ Application** | **Noms Colonnes Reconnus** |
|-----------------------|-----------------------------|
| **LOT** | `lot`, `n°lot`, `numero`, `n°`, `num` |
| **MARQUE** | `marque`, `brand`, `constructeur` |
| **MODÈLE** | `modele`, `modèle`, `model`, `nom` |
| **ANNÉE** | `annee`, `année`, `year`, `an` |
| **KILOMÉTRAGE** | `kilometrage`, `km`, `mileage` |
| **MOTORISATION** | `motorisation`, `moteur`, `carburant` |
| **PRIX REVENTE** | `prix`, `revente`, `vente`, `price` |
| **PRIX ACHAT** | `achat`, `achete`, `acheté` |
| **RÉPARATIONS** | `reparation`, `cout`, `repair` |
| **DESCRIPTION** | `description`, `travaux`, `notes` |

---

## 📊 **Résultats de l'Import**

### **Catégorisation Automatique**
- **🔍 Repérage** : Véhicules sans prix d'achat
- **🏆 Achetés** : Véhicules avec prix d'achat renseigné

### **Informations Affichées**
```
✅ Import PDF réussi !
📄 Fichier créé : pdf_import_20250104_143022_Catalogue_Encheres.json
📊 Données importées :
   • 15 véhicules en repérage
   • 8 véhicules achetés  
   • Total : 23 véhicules traités
```

---

## 🛠️ **Dépannage et Solutions**

### **❌ Problème : "Bibliothèque pdfplumber non installée"**
**Solution :**
```bash
pip install pdfplumber
```

### **❌ Problème : "Aucune donnée détectée"**
**Causes possibles :**
1. **PDF scanné** (image) → Convertissez en PDF avec texte sélectionnable
2. **Format non standard** → Vérifiez que les marques sont écrites correctement
3. **Langue étrangère** → Le système reconnaît les marques en français

**Solution :**
1. Testez la **sélection de texte** dans votre PDF
2. Vérifiez que les **marques sont en français** (Peugeot, pas PEUGEOT)
3. Si nécessaire, exportez votre PDF en **CSV** puis utilisez l'import CSV

### **❌ Problème : "Données incomplètes"**
**Solutions :**
1. **Ajustez manuellement** après import dans l'application
2. **Complétez les champs manquants** via l'interface
3. **Réorganisez votre PDF** pour une meilleure structure

### **❌ Problème : "Mauvaise catégorisation"**
Le système classe mal repérage/achetés ?
**Solution :**
1. **Déplacez les véhicules** entre onglets après import
2. **Éditez le statut** de chaque véhicule
3. **Ajoutez/modifiez** les prix d'achat

---

## ⚡ **Conseils pour un Import Optimal**

### **📄 Préparer votre PDF**
1. **Texte sélectionnable** (pas d'image scannée)
2. **Structure claire** avec marques visibles
3. **Tableaux bien formatés** si possible
4. **Prix en euros** avec symbole €

### **🎯 Optimiser les Résultats**
1. **Noms de marques français** (Volkswagen plutôt que VW si possible)
2. **Prix cohérents** (même format dans tout le document)
3. **Années complètes** (2018 plutôt que 18)
4. **Séparateurs clairs** entre véhicules

### **🔄 Après l'Import**
1. **Vérifiez les données** dans chaque onglet
2. **Complétez les champs manquants** (couleur, réparations, etc.)
3. **Ajustez les prix** si nécessaire
4. **Testez les nouvelles fonctionnalités** (tri, recherche, export)

---

## 🆕 **Avantages vs Import CSV**

| **Critère** | **Import PDF** | **Import CSV** |
|-------------|----------------|----------------|
| **Simplicité** | ⭐⭐⭐⭐⭐ Un seul clic | ⭐⭐⭐ Conversion requise |
| **Reconnaissance** | ⭐⭐⭐⭐ Automatique | ⭐⭐ Mapping manuel |
| **Formats** | ⭐⭐⭐ PDF natifs | ⭐⭐⭐⭐⭐ Universels |
| **Précision** | ⭐⭐⭐ Bonne | ⭐⭐⭐⭐⭐ Parfaite |

**Recommandation** : Essayez l'**import PDF** en premier, utilisez **CSV** en cas de problème.

---

## 🎉 **Prêt à Importer ?**

1. **Préparez votre PDF** avec les conseils ci-dessus
2. **Lancez l'import** avec le bouton `📄 Importer PDF`  
3. **Profitez de la reconnaissance automatique** !
4. **Ajustez si nécessaire** dans l'interface

**Bon import ! 🚗📄→💾** 