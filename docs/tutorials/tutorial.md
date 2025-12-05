## Tutorial : Utiliser le projet rugby-xpoints

Ce tutoriel explique comment utiliser les différents scripts du projet rugby-xpoints pour analyser les performances des buteurs de rugby à partir de la métrique expected points (xPoints).
Il est destiné aux nouveaux utilisateurs souhaitant comprendre le fonctionnement du projet étape par étape.

---

## Objectifs du projet

Le projet permet :

d’enregistrer les coups de pied (pénalités, transformations) d’un joueur depuis une interface graphique ;

de calculer l’angle de tir, la distance et la probabilité de réussite via un modèle de régression logistique ;

de générer un fichier CSV contenant toutes les tentatives enregistrées ;

de calculer des statistiques par journée et globales ;

d’exporter des métriques utiles comme :

pourcentage de réussite,

nombre de points marqués,

difficulté moyenne,

xPoints,

rating (points / xPoints).

---

## 1. Installation du projet
### 1.1 Cloner le dépôt GitHub
git clone https://github.com/mariuspascal1/rugby-xpoints.git
cd rugby-xpoints

### 1.2 Installer les dépendances via Poetry
poetry install


Assure-toi d’utiliser Python ≥ 3.11 car certains modules graphiques (Tkinter) ne sont pas stables sous Python 3.14.

---

## 2. Enregistrer des coups via l’interface graphique

Le script principal pour collecter les données est :

rugby_xpoints/repertoireV3.py


Lance-le avec Poetry :

poetry run python -m rugby_xpoints.repertoireV3

### 2.1 Saisie des informations joueur

Une fenêtre s’ouvre et te demande :

Nom du joueur

Équipe

Compétition

Journée

Type de coup (pénalité / transformation)

Clique sur Valider pour ouvrir le terrain.

### 2.2 Enregistrer des coups

Une image du terrain s’affiche.

Clic gauche → coup réussi

Clic droit → coup raté

À chaque clic, le script calcule automatiquement :

la distance du point aux poteaux,

l’angle visuel,

puis enregistre le coup dans data/repertoire.csv.

Tu peux cliquer autant de fois que nécessaire : le fichier est mis à jour à chaque interaction.

---

## 3. Calculer les probabilités et xPoints

Le fichier contenant les coups permet ensuite de calculer la probabilité de réussite d’un tir grâce à une régression logistique.

Commande :

poetry run python -m rugby_xpoints.calcul_proba


Une fenêtre apparaît et te demande :

la compétition,

éventuellement la journée.

Le script :

charge data/repertoire.csv,

calcule l’angle / distance pour chaque tir,

entraîne une régression logistique,

calcule la probabilité de réussite,

génère un fichier CSV :

data/coups_joueurs_<competition>_<journee>.csv

---

## 4. Générer les statistiques des joueurs

Deux scripts produisent les statistiques finales.

### 4.1 Statistiques par journée
poetry run python -m rugby_xpoints.stats_joueurs


Choisis :

compétition,

journée.

Ce script génère :

stats_joueurs_<competition>_<journee>.csv


Avec :

pourcentage de réussite,

tirs réussis / tentés,

total xPoints,

difficulté moyenne,

rating (points / xPoints).

### 4.2 Statistiques globales (toute la compétition)

Si tu laisses la journée vide → stats globales :

stats_joueurs_<competition>.csv

---

## 5. Générer la documentation

La documentation est construite avec Sphinx.

Commande :

poetry run sphinx-build docs/source docs/build


Le site HTML est généré dans :

docs/build/index.html

## 6. Lancer les tests unitaires

Les tests se trouvent dans :

tests/test_calculs.py


Pour les exécuter :

poetry run pytest