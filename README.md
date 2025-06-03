# 🚗 Gestionnaire d'Enchères Véhicules

Un outil professionnel pour gérer vos achats de véhicules en enchères. Calculez automatiquement les prix maximums d'achat, suivez vos véhicules repérés, et optimisez votre rentabilité.

## 🚀 DÉMARRAGE RAPIDE

### Pour les utilisateurs (sans connaissances techniques)
1. **Double-cliquez sur `CREER_EXE.bat`** pour créer l'application
2. **Attendez la fin de la création** (3-10 minutes)
3. **L'EXE sera dans le dossier `Gestionnaire_Encheres_Distribution`**
4. **Distribuez ce dossier** à vos utilisateurs

### Pour les développeurs
```bash
# Lancer l'application en mode développement
python main.py

# Créer l'EXE manuellement
python build_tools/build_exe.py

# Générer des données de démonstration
python data_demo/demo_data_v4_modulaire.py
```

## 📁 Structure du Projet

```
📁 MidnightTuneTool/
├── 📄 main.py                      # 🚀 Point d'entrée principal
├── 📄 CREER_EXE.bat                # 🛠️ Script création EXE (SIMPLE)
├── 📄 README.md                    # 📋 Ce fichier
├── 📄 donnees_encheres.json        # 💾 Données des véhicules
├── 📄 parametres_encheres.json     # ⚙️ Paramètres utilisateur
│
├── 📁 config/                      # ⚙️ Configuration application
├── 📁 models/                      # 🏗️ Modèles de données (Vehicule)
├── 📁 services/                    # 🔧 Services métier (DataManager, Calculator)
├── 📁 gui/                         # 🎨 Interface utilisateur (onglets)
├── 📁 utils/                       # 🛠️ Utilitaires (styles)
│
├── 📁 docs/                        # 📚 DOCUMENTATION
│   ├── 📄 README.md               # Guide utilisateur complet
│   ├── 📄 BUILD_EXE_GUIDE.md      # Guide technique EXE
│   ├── 📄 PROCEDURE_COMPLETE_EXE.md # Procédure complète
│   ├── 📄 README_CREATION_EXE.md  # Guide simple EXE
│   └── 📄 GUIDE_UTILISATEUR_FINAL.md # Guide utilisateur final
│
├── 📁 build_tools/                 # 🏗️ OUTILS DE CONSTRUCTION
│   ├── 📄 build_exe.py            # Script principal création EXE
│   └── 📄 CREER_EXE.bat           # Script batch (dans build_tools)
│
├── 📁 data_demo/                   # 🎯 DONNÉES DE DÉMONSTRATION
│   └── 📄 demo_data_v4_modulaire.py # Générateur de données test
│
└── 📁 exe_build/                   # 📦 FICHIERS GÉNÉRÉS (après build)
    └── 📄 Gestionnaire_Encheres.exe
```

## ✨ Fonctionnalités

- 📊 **Dashboard interactif** avec statistiques visuelles en temps réel
- 🔍 **Saisie rapide** de véhicules avec informations complètes
- 💰 **Calcul automatique** du prix maximum d'achat basé sur vos critères
- 📊 **Tableau interactif** pour gérer tous vos véhicules
- 🎨 **Coloration intelligente** des prix (rentable/non rentable)
- 📄 **Export CSV** pour impression et archivage
- ⚙️ **Paramètres personnalisables** (tarifs, marges, commissions)
- 🏆 **Suivi des achats** avec statistiques détaillées

## 🎯 Utilisation selon votre profil

### 👤 Utilisateur final (sans technique)
1. **Récupérez** le ZIP de l'application
2. **Décompressez** dans un dossier
3. **Double-cliquez** sur `Gestionnaire_Encheres.exe`
4. **Suivez** le guide dans l'onglet "⚙️ Paramètres"

### 🛠️ Créateur/Distributeur
1. **Double-cliquez** sur `CREER_EXE.bat` à la racine
2. **Attendez** la création automatique (5-10 min)
3. **Récupérez** le dossier `Gestionnaire_Encheres_Distribution`
4. **Compressez** en ZIP et distribuez

### 💻 Développeur
1. **Clonez** le projet
2. **Installez** les dépendances : `pip install ttkbootstrap pillow`
3. **Lancez** en développement : `python main.py`
4. **Consultez** `/docs/` pour la documentation technique

## 📚 Documentation Complète

- **[📋 Guide Utilisateur](docs/README.md)** - Guide complet d'utilisation
- **[🏗️ Guide Technique EXE](docs/BUILD_EXE_GUIDE.md)** - Documentation technique 
- **[🎯 Guide Simple EXE](docs/README_CREATION_EXE.md)** - Instructions 2 minutes
- **[📖 Guide Utilisateur Final](docs/GUIDE_UTILISATEUR_FINAL.md)** - Pour vos clients

## 🔧 Développement

### Prérequis
- Python 3.8+
- ttkbootstrap (`pip install ttkbootstrap`)
- pillow (`pip install pillow`)
- PyInstaller pour l'EXE (`pip install pyinstaller`)

### Architecture
- **MVC Pattern** : Séparation claire entre modèles, vues et services
- **Structure modulaire** : Chaque composant dans son dossier
- **Configuration centralisée** : Settings dans `/config/`
- **Interface moderne** : ttkbootstrap pour le style

### Commandes utiles
```bash
# Développement
python main.py

# Données de test
python data_demo/demo_data_v4_modulaire.py

# Build EXE
python build_tools/build_exe.py

# Build simple
python build_tools/CREER_EXE.bat
```

## 📦 Distribution

### Automatique (recommandé)
```bash
# À la racine du projet
CREER_EXE.bat
```

### Manuelle
```bash
cd build_tools
python build_exe.py
```

### Résultat
- **EXE standalone** : `exe_build/Gestionnaire_Encheres.exe`
- **Package distribution** : `Gestionnaire_Encheres_Distribution/`
- **Taille** : ~25-50MB
- **Compatibilité** : Windows 10/11

## 🆘 Support

### Utilisateurs
- **Problème EXE** : Vérifiez votre antivirus
- **Données perdues** : Fichiers `.json` dans le dossier
- **Bug** : Redémarrez l'application

### Développeurs
- **Issues** : Consultez `/docs/` pour résolution
- **Build problème** : Voir `docs/BUILD_EXE_GUIDE.md`
- **Architecture** : Code documenté et structuré

---

**Version 4.0** - Structure modulaire et build automatique 🚗✨

🎉 **Votre application est maintenant organisée, documentée et prête à distribuer !** 