import pandas as pd
import numpy as np
import math
import sys
import os
from sklearn.linear_model import LogisticRegression
import tkinter as tk
from tkinter import simpledialog

def get_user_input():
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale

    competition = simpledialog.askstring("Entrée utilisateur", "Compétition :")
    
    # Demander la journée en tant que chaîne
    journee_str = simpledialog.askstring("Entrée utilisateur", "Journée (laisser vide pour toute la compétition) :")
    
    # Si l'utilisateur entre une valeur vide, mettre journee à None
    if journee_str == "":
        journee = None
    else:
        # Sinon, convertir la chaîne en entier
        try:
            journee = int(journee_str)
        except ValueError:
            journee = None
    
    return competition, journee

# Calculer l'angle entre les poteaux
def calculer_angle(xA, yA, xB, yB, x, y):
    dA = math.sqrt((xA - x) ** 2 + (yA - y) ** 2)
    dB = math.sqrt((xB - x) ** 2 + (yB - y) ** 2)
    dAB = math.sqrt((xB - xA) ** 2 + (yB - yA) ** 2)
    
    cos_theta = (dA ** 2 + dB ** 2 - dAB ** 2) / (2 * dA * dB)
    theta = math.acos(cos_theta)
    theta_degrees = math.degrees(theta)
    
    return theta_degrees

# Calculer la distance au milieu entre les poteaux
def calculer_distance(xA, yA, xB, yB, x, y):
    milieu_A_B = ((xA + xB) / 2, (yA + yB) / 2)
    return math.sqrt((milieu_A_B[0] - x) ** 2 + (milieu_A_B[1] - y) ** 2)

# Charger et entraîner le modèle de régression logistique
def charger_modele():
    data = pd.read_csv('data/repertoire.csv') 
    data['resultat'] = data['resultat'].map({'réussi': 1, 'raté': 0})
    X = data[['angle', 'distance']]
    y = data['resultat']
    model = LogisticRegression()
    model.fit(X, y)
    return model

# Calculer la probabilité de réussite pour une entrée spécifique
def probabilite_reussite(model, angle, distance):
    prob = model.predict_proba([[angle, distance]])[0][1]
    return prob

# Fonction principale pour traiter les données de la journée n
def coups_joueurs(journee, competition):
    # Charger le modèle
    model = charger_modele()

    # Charger les données à partir du fichier CSV avec le bon séparateur
    data = pd.read_csv('data/repertoire.csv')  # Spécifier le séparateur
    print(data.columns)  # Imprimer les colonnes pour vérification

    # Filtrer les données pour n'inclure que celles de la compétition et de la journée
    if journee is None:
        # Si journee est None, on ne filtre pas sur la journée, on prend toutes les journées de la compétition
        data_copy = data[data['competition'] == competition].copy()  # Crée une copie pour éviter les avertissements
    else:
        # Sinon, on filtre à la fois sur la compétition et la journée
        data_copy = data[(data['competition'] == competition) & (data['journee'] == journee)].copy()

    # Si aucune donnée n'est trouvée
    if data_copy.empty:
        print(f"Aucune donnée trouvée pour la compétition {competition} et la journée {journee}.")
        return

    # Coordonnées des poteaux
    xA, yA, xB, yB = 7.556818181818187, 29.77272727272728, 7.651515151515156, 39.90530303030304

    # Calculer les angles et distances pour chaque coup
    data_copy.loc[:, 'angle'] = data_copy.apply(lambda row: calculer_angle(xA, yA, xB, yB, row['x'], row['y']), axis=1)
    data_copy.loc[:, 'distance'] = data_copy.apply(lambda row: calculer_distance(xA, yA, xB, yB, row['x'], row['y']), axis=1)

    # Calculer les probabilités de réussite pour chaque coup
    data_copy.loc[:, 'proba'] = data_copy.apply(lambda row: probabilite_reussite(model, row['angle'], row['distance']), axis=1)

    # Calculer les xPoints selon le type de coup
    data_copy.loc[:, 'xPoints'] = np.where(data_copy['type'] == 'transformation', data_copy['proba'] * 2, data_copy['proba'] * 3)

    # Créer un dossier pour sauvegarder les fichiers, si nécessaire
    dossier = f'data/coups_joueurs_{str(competition)}_{str(journee)}'

    # Sauvegarder les données mises à jour dans le fichier coups_joueurs{n}.csv
    nom_fichier = f'data/coups_joueurs_{str(competition)}_{str(journee)}.csv'
    data_copy.to_csv(nom_fichier, index=False)
    print(f"Données pour la compétition {competition} et la journée {journee} sauvegardées dans {nom_fichier} avec les colonnes proba et xPoints.")





def main():
    competition, journee = get_user_input()
    coups_joueurs(journee, competition)
   
if __name__ == "__main__":
    main()

"""import pandas as pd
import numpy as np
import math
import sys
import os
from sklearn.linear_model import LogisticRegression

# Calculer l'angle entre les poteaux
def calculer_angle(xA, yA, xB, yB, x, y):
    dA = math.sqrt((xA - x) ** 2 + (yA - y) ** 2)
    dB = math.sqrt((xB - x) ** 2 + (yB - y) ** 2)
    dAB = math.sqrt((xB - xA) ** 2 + (yB - yA) ** 2)
    
    cos_theta = (dA ** 2 + dB ** 2 - dAB ** 2) / (2 * dA * dB)
    theta = math.acos(cos_theta)
    theta_degrees = math.degrees(theta)
    
    return theta_degrees

# Calculer la distance au milieu entre les poteaux
def calculer_distance(xA, yA, xB, yB, x, y):
    milieu_A_B = ((xA + xB) / 2, (yA + yB) / 2)
    return math.sqrt((milieu_A_B[0] - x) ** 2 + (milieu_A_B[1] - y) ** 2)

# Charger et entraîner le modèle de régression logistique
def charger_modele():
    data = pd.read_csv('repertoire.csv') 
    data['resultat'] = data['resultat'].map({'réussi': 1, 'raté': 0})
    X = data[['angle', 'distance']]
    y = data['resultat']
    model = LogisticRegression()
    model.fit(X, y)
    return model

# Calculer la probabilité de réussite pour une entrée spécifique
def probabilite_reussite(model, angle, distance):
    prob = model.predict_proba([[angle, distance]])[0][1]
    return prob

# Fonction principale pour traiter les données de la journée n
def main(n):
    # Charger le modèle
    model = charger_modele()

    # Charger les données à partir du fichier CSV avec le bon séparateur
    data = pd.read_csv('repertoire.csv')  # Spécifier le séparateur
    print(data.columns)  # Imprimer les colonnes pour vérification

    # Filtrer les données pour n'inclure que celles de la journée n
    data_n = data[data['journee'] == n].copy()  # Crée une copie pour éviter les avertissements

    # Si aucun coup n'est trouvé pour la journée n
    if data_n.empty:
        print(f"Aucune donnée trouvée pour la journée {n}.")
        return

    # Coordonnées des poteaux
    xA, yA, xB, yB = 7.556818181818187, 29.77272727272728, 7.651515151515156, 39.90530303030304

    # Calculer les angles et distances pour chaque coup
    data_n.loc[:, 'angle'] = data_n.apply(lambda row: calculer_angle(xA, yA, xB, yB, row['x'], row['y']), axis=1)
    data_n.loc[:, 'distance'] = data_n.apply(lambda row: calculer_distance(xA, yA, xB, yB, row['x'], row['y']), axis=1)

    # Calculer les probabilités de réussite pour chaque coup
    data_n.loc[:, 'proba'] = data_n.apply(lambda row: probabilite_reussite(model, row['angle'], row['distance']), axis=1)

    # Calculer les xPoints selon le type de coup
    data_n.loc[:, 'xPoints'] = np.where(data_n['type'] == 'transformation', data_n['proba'] * 2, data_n['proba'] * 3)

    # Créer un dossier pour sauvegarder les fichiers, si nécessaire
    dossier = f'coups_joueurs_{n}'

    # Sauvegarder les données mises à jour dans le fichier coups_joueurs{n}.csv
    nom_fichier = f'coups_joueurs{n}.csv'
    data_n.to_csv(nom_fichier, index=False)
    print(f"Données pour la journée {n} sauvegardées dans {nom_fichier} avec les colonnes proba et xPoints.")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Utilisation : python calcul_proba.py n")
    else:
        try:
            n = int(sys.argv[1])
            main(n)
        except ValueError:
            print("Veuillez entrer un nombre entier pour la journée.")
"""