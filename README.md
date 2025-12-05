# rugby-xpoints

**rugby-xpoints** est un projet Python permettant d’analyser les performances des buteurs de rugby.  
Il calcule la grandeur **xPoints**, qui représente les points espérés (expected points) d’un coup de pied, et fournit des statistiques détaillées sur les joueurs et leurs tirs.

---

## Fonctionnalités

- Calcul des angles et distances par rapport aux poteaux.
- Estimation de la probabilité de réussite de chaque coup à l'aide d'une régression logistique.
- Calcul de la valeur **xPoints** pour chaque tentative (pénalité ou transformation).
- Statistiques détaillées pour chaque joueur et pour la compétition entière.
- Interface graphique simple pour saisir les tirs sur un terrain interactif.

---

## Scripts principaux

| Script | Description | Entrée | Sortie |
|--------|-------------|--------|--------|
| `repertoireV3.py` | Saisie des tirs via interface graphique et sauvegarde dans CSV | Image du terrain `rugby_xPoints.png` | `repertoire.csv` |
| `calcul_proba.py` | Calcule la probabilité de réussite des tirs | `repertoire.csv` | Fichier CSV avec colonnes `proba` et `xPoints` |
| `stats_joueurs.py` | Génère des statistiques par joueur et par compétition | CSV générés par `calcul_proba.py` ou `repertoireV3.py` | `stats_joueurs_<competition>_<journee>.csv` et `stats_joueurs_<competition>.csv` |

---

## Prérequis

- Python >= 3.11
- Dépendances (installables via Poetry) :
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `scikit-learn`

---

## Installation locale

1. Cloner le dépôt GitHub :

```bash
git clone https://github.com/mariuspascal1/rugby-xpoints.git
cd rugby-xpoints
```
2. Installer poetry si ce n'est pas déjà fait :

```bash
pip install poetry
```

3. Installer les dépendances et créer un environnement virtuel :
```bash
poetry install
```

---

## Utilisation 
Les scripts sont exécutables via les commandes :
```bash
poetry run calcul_proba
poetry run repertoire
poetry run stats_joueurs
```

---

## Analyse statique du code

Le projet utilise Ruff pour analyser automatiquement la qualité du code :

Pour vérifier le code : 
```bash
poetry run ruff check .
```

Pour effectuer la correction des erreurs detectées :
```bash
poetry run ruff check --fix .
```
La configuration de Ruff est incluse dans le fichier pyproject.toml.

## Lien vers le dépôt GitHub
https://github.com/mariuspascal1/rugby-xpoints