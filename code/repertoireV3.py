import pandas as pd
import math
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import csv
import os
import numpy as np
import tkinter as tk
from tkinter import simpledialog, ttk
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

tous_les_coups = []

def start_interface():
    root = tk.Tk()
    root.title("Saisie des informations")
    
    tk.Label(root, text="Joueur:").grid(row=0, column=0)
    entry_joueur = tk.Entry(root)
    entry_joueur.grid(row=0, column=1)
    
    tk.Label(root, text="Équipe:").grid(row=1, column=0)
    entry_equipe = tk.Entry(root)
    entry_equipe.grid(row=1, column=1)
    
    tk.Label(root, text="Compétition:").grid(row=2, column=0)
    entry_competition = tk.Entry(root)
    entry_competition.grid(row=2, column=1)
    
    tk.Label(root, text="Journée:").grid(row=3, column=0)
    entry_journee = tk.Entry(root)
    entry_journee.grid(row=3, column=1)
    
    tk.Label(root, text="Type (pénalité/transformation):").grid(row=4, column=0)
    entry_type = tk.Entry(root)
    entry_type.grid(row=4, column=1)
    
    def valider():
        nom_joueur = entry_joueur.get()
        nom_equipe = entry_equipe.get()
        competition = entry_competition.get()
        journee = entry_journee.get()
        type_coup = entry_type.get()
        gérer_terrain('rugby_xPoints.png', nom_joueur, nom_equipe, competition, journee, type_coup)
    
    btn_valider = tk.Button(root, text="Valider", command=valider)
    btn_valider.grid(row=5, column=0, columnspan=2)
    
    root.mainloop()

def calculer_angle(xA, yA, xB, yB, x, y):
    dA = math.sqrt((xA - x) ** 2 + (yA - y) ** 2)
    dB = math.sqrt((xB - x) ** 2 + (yB - y) ** 2)
    dAB = math.sqrt((xB - xA) ** 2 + (yB - yA) ** 2)
    
    cos_theta = (dA ** 2 + dB ** 2 - dAB ** 2) / (2 * dA * dB)
    theta = math.acos(cos_theta)
    theta_degrees = math.degrees(theta)
    
    return theta_degrees

def calculer_distance(xA, yA, xB, yB, x, y):
    milieu_A_B = ((xA + xB) / 2, (yA + yB) / 2)
    return math.sqrt((milieu_A_B[0] - x) ** 2 + (milieu_A_B[1] - y) ** 2)

def gérer_terrain(image_path, nom_joueur, nom_equipe, competition, journee, type_coup):
    global tous_les_coups  # Utiliser la variable globale

    xA, yA = 7.556818181818187, 29.77272727272728  # Poteau gauche
    xB, yB = 7.651515151515156, 39.90530303030304  # Poteau droit

    def on_click(event):
        x, y = event.xdata, event.ydata
        if x is None or y is None:
            return  # Éviter les erreurs si clic hors zone
        
        if event.button == 1:
            resultat = "réussi"
            couleur = 'go'
        elif event.button == 3:
            resultat = "raté"
            couleur = 'ro'
        else:
            return

        angle = calculer_angle(xA, yA, xB, yB, x, y)
        distance = calculer_distance(xA, yA, xB, yB, x, y)
        
        # Ajouter le coup à la liste globale
        tous_les_coups.append([nom_joueur, nom_equipe, competition, journee, type_coup, x, y, resultat, angle, distance])

        plt.plot(x, y, couleur)
        plt.draw()

        # Sauvegarder immédiatement après chaque clic
        sauvegarder_coups("data/repertoire.csv")

        print(f"Coup de pied {resultat} ajouté : {x}, {y}, Angle: {angle:.2f}°, Distance: {distance:.2f}")

    def dessiner_terrain():
        img = mpimg.imread(image_path)
        fig, ax = plt.subplots()
        ax.imshow(img, extent=[0, 60, 0, 70])
        ax.set_aspect('equal')
        plt.title(f"Coups de pied - {nom_joueur} ({nom_equipe}) - {competition} - Journée {journee}")
        fig.canvas.mpl_connect('button_press_event', on_click)
        plt.show()

    dessiner_terrain()

def sauvegarder_coups(fichier_sauvegarde):
    global tous_les_coups  # Utiliser la liste globale
    mode = 'a' if os.path.exists(fichier_sauvegarde) else 'w'

    with open(fichier_sauvegarde, mode, newline='') as file:
        writer = csv.writer(file)
        if mode == 'w':  # Si le fichier est nouveau, ajouter les en-têtes
            writer.writerow(["joueur", "equipe", "competition", "journee", "type", "x", "y", "resultat", "angle", "distance"])
        
        # Écrire les nouvelles entrées
        writer.writerows(tous_les_coups)

    print(f"Les données ont été sauvegardées dans {fichier_sauvegarde}")


def main():
    start_interface() 

if __name__ == "__main__":
    main()


"""import pandas as pd
import math
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import csv
import os
import numpy as np
import tkinter as tk
from tkinter import simpledialog
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

def get_user_input():
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale

    nom_joueur = simpledialog.askstring("Entrée utilisateur", "Joueur :")
    nom_equipe = simpledialog.askstring("Entrée utilisateur", "Équipe :")
    competition = simpledialog.askstring("Entrée utilisateur", "Compétition :")
    journee = simpledialog.askinteger("Entrée utilisateur", "Journée :")
    type_coup = simpledialog.askstring("Entrée utilisateur", "Type (pénalité/transformation) :")
    
    return nom_joueur, nom_equipe, competition, journee, type_coup

def calculer_angle(xA, yA, xB, yB, x, y):
    dA = math.sqrt((xA - x) ** 2 + (yA - y) ** 2)
    dB = math.sqrt((xB - x) ** 2 + (yB - y) ** 2)
    dAB = math.sqrt((xB - xA) ** 2 + (yB - yA) ** 2)
    
    cos_theta = (dA ** 2 + dB ** 2 - dAB ** 2) / (2 * dA * dB)
    theta = math.acos(cos_theta)
    theta_degrees = math.degrees(theta)
    
    return theta_degrees

def calculer_distance(xA, yA, xB, yB, x, y):
    milieu_A_B = ((xA + xB) / 2, (yA + yB) / 2)
    return math.sqrt((milieu_A_B[0] - x) ** 2 + (milieu_A_B[1] - y) ** 2)

def gérer_terrain(image_path, nom_joueur, nom_equipe, competition, journee, type_coup):
    tous_les_coups = []
    xA, yA = 7.556818181818187, 29.77272727272728  # Poteau gauche
    xB, yB = 7.651515151515156, 39.90530303030304  # Poteau droit

    def on_click(event):
        x, y = event.xdata, event.ydata
        if event.button == 1:
            resultat = "réussi"
            couleur = 'go'
        elif event.button == 3:
            resultat = "raté"
            couleur = 'ro'
        else:
            return

        angle = calculer_angle(xA, yA, xB, yB, x, y)
        distance = calculer_distance(xA, yA, xB, yB, x, y)
        
        tous_les_coups.append([nom_joueur, nom_equipe, competition, journee, type_coup, x, y, resultat, angle, distance])
        plt.plot(x, y, couleur)
        plt.draw()
        print(f"Coup de pied {resultat} ajouté : {x}, {y}, Angle: {angle:.2f}°, Distance: {distance:.2f}")

    def dessiner_terrain():
        img = mpimg.imread(image_path)
        fig, ax = plt.subplots()
        ax.imshow(img, extent=[0, 60, 0, 70])
        ax.set_aspect('equal')
        plt.title(f"Coups de pied - {nom_joueur} ({nom_equipe}) - {competition} - Journée {journee}")
        fig.canvas.mpl_connect('button_press_event', on_click)
        plt.show()

    def sauvegarder_coups(fichier_sauvegarde):
        mode = 'a' if os.path.exists(fichier_sauvegarde) else 'w'
        with open(fichier_sauvegarde, mode='a', newline='') as file:
            writer = csv.writer(file)
            if mode == 'w':
                writer.writerow(["joueur", "equipe", "competition", "journee", "type", "x", "y", "resultat", "angle", "distance"])
            writer.writerows(tous_les_coups)
        print(f"Les données ont été sauvegardées dans {fichier_sauvegarde}")

    dessiner_terrain()
    fichier_sauvegarde = "repertoire_modifie1.csv"
    sauvegarder_coups(fichier_sauvegarde)

if __name__ == "__main__":
    nom_joueur, nom_equipe, competition, journee, type_coup = get_user_input()
    image_path = 'rugby_xPoints.png'
    gérer_terrain(image_path, nom_joueur, nom_equipe, competition, journee, type_coup)"""

"""import pandas as pd
import math
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import csv
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np



def gérer_terrain(image_path, nom_joueur, nom_equipe, journee, type_coup):
    tous_les_coups = []

    # Coordonnées des poteaux
    xA, yA = 7.556818181818187, 29.77272727272728  # Coordonnées du poteau gauche
    xB, yB = 7.651515151515156, 39.90530303030304   # Coordonnées du poteau droit

    def on_click(event):
        x, y = event.xdata, event.ydata
        if event.button in [1, 3]:  # Left or right click
            # Calcul de l'angle et de la distance
            angle = calculer_angle(xA, yA, xB, yB, x, y)
            distance = calculer_distance(xA, yA, xB, yB, x, y)

            # Determine if the click is left (réussi) or right (raté)
            resultat = 'réussi' if event.button == 1 else 'raté'

            # Add the kick information with the result to the list
            tous_les_coups.append([nom_joueur, nom_equipe, journee, x, y, resultat, angle, distance, type_coup])
            
            # Draw point on the field
            couleur = 'go' if event.button == 1 else 'ro'  # Green for left (réussi), red for right (raté)
            plt.plot(x, y, couleur)
            plt.draw()

            print(f"Coup ajouté : {nom_joueur}, {nom_equipe}, {journee}, ({x}, {y}), Résultat: {resultat}, Angle: {angle:.2f}°, Distance: {distance:.2f}")

    def dessiner_terrain():
        img = mpimg.imread(image_path)
        fig, ax = plt.subplots()
        ax.imshow(img, extent=[0, 60, 0, 70])  # Ajuster si nécessaire
        ax.set_aspect('equal')
        plt.title(f"Coups de pied - {nom_joueur} ({nom_equipe}) - Journée {journee} - type : {type_coup}")
        fig.canvas.mpl_connect('button_press_event', on_click)
        plt.show()

    def sauvegarder_coups(fichier_sauvegarde):
        # Vérifier si le fichier existe déjà et l'ouvrir en mode append (ajout)
        mode = 'a' if os.path.exists(fichier_sauvegarde) else 'w'  # Mode ajout ou écriture

        with open(fichier_sauvegarde, mode='a', newline='') as file:
            writer = csv.writer(file)
            if mode == 'w':  # Écrire l'en-tête uniquement lors de la création du fichier
                writer.writerow(["joueur", "equipe", "journee", "x", "y", "angle", "distance", "type"])  # En-tête CSV
            writer.writerows(tous_les_coups)
        print(f"Les données ont été sauvegardées dans {fichier_sauvegarde}")

    # Charger et dessiner le terrain
    dessiner_terrain()

    # Sauvegarder les coups dans un fichier CSV
    fichier_sauvegarde = "repertoire.csv"
    sauvegarder_coups(fichier_sauvegarde)

def calculer_angle(xA, yA, xB, yB, x, y):
    dA = math.sqrt((xA - x) ** 2 + (yA - y) ** 2)
    dB = math.sqrt((xB - x) ** 2 + (yB - y) ** 2)
    dAB = math.sqrt((xB - xA) ** 2 + (yB - yA) ** 2)
    
    cos_theta = (dA ** 2 + dB ** 2 - dAB ** 2) / (2 * dA * dB)
    theta = math.acos(cos_theta)
    theta_degrees = math.degrees(theta)
    
    return theta_degrees

def calculer_distance(xA, yA, xB, yB, x, y):
    milieu_A_B = ((xA + xB) / 2, (yA + yB) / 2)
    return math.sqrt((milieu_A_B[0] - x) ** 2 + (milieu_A_B[1] - y) ** 2)

# Afficher la heatmap des xPoints
def heatmap():
    # Charger les données du fichier CSV
    data = pd.read_csv('repertoire.csv')

    # Coordonnées des poteaux
    xA, yA = 7.556818181818187, 29.77272727272728  # Poteau gauche
    xB, yB = 7.651515151515156, 39.90530303030304   # Poteau droit

    # Calculer les angles et distances et les ajouter au DataFrame
    data['angle'] = data.apply(lambda row: calculer_angle(xA, yA, xB, yB, row['x'], row['y']), axis=1)
    data['distance'] = data.apply(lambda row: calculer_distance(xA, yA, xB, yB, row['x'], row['y']), axis=1)

    # Extraire les caractéristiques (angle, distance, x, y) et la cible (résultat)
    X = data[['angle', 'distance', 'x', 'y']]
    y = data['resultat'].map({'réussi': 1, 'raté': 0})

    # Créer et entraîner le modèle de régression logistique
    model = LogisticRegression()
    model.fit(X, y)

    # Créer une grille de points sur le terrain
    x_range = np.linspace(0, 60, 100)
    y_range = np.linspace(0, 70, 100)
    xx, yy = np.meshgrid(x_range, y_range)

    # Fonction pour prédire la probabilité de réussite sur chaque point de la grille
    def calculer_probabilites_grille(model, xx, yy):
        probas = np.zeros_like(xx)

        for i in range(xx.shape[0]):
            for j in range(xx.shape[1]):
                x, y = xx[i, j], yy[i, j]
                angle = calculer_angle(xA, yA, xB, yB, x, y)
                distance = calculer_distance(xA, yA, xB, yB, x, y)

                probas[i, j] = model.predict_proba([[angle, distance, x, y]])[0][1]

        return probas
    
    # Calculer la probabilité de réussite pour chaque point de la grille
    xpoints_grid = calculer_probabilites_grille(model, xx, yy)

    # Calculer le milieu entre A et B pour le masquage
    y_milieu = (yA + yB) / 2

    # Masquer la heatmap pour les conditions x < 0.15 * (y - y_milieu)^2 + 8
    mask = (xx < 0.015 * (yy - y_milieu) ** 2 + 8)
    xpoints_grid[mask] = np.nan

    # Afficher l'image du terrain
    img = mpimg.imread('rugby_xPoints.png')
    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, 60, 0, 70], aspect='auto')

    # Afficher la heatmap
    plt.imshow(xpoints_grid, extent=[0, 60, 0, 70], origin='lower', cmap='RdYlGn', alpha=0.7)
    plt.colorbar(label='Probabilité de réussite')
    plt.title("Heatmap des xPoints")
    plt.xlabel("Largeur du terrain (x)")
    plt.ylabel("Longueur du terrain (y)")
    plt.show()

# Afficher tout les coups de pieds du fichier repertoire.csv sur le terrain
def afficher_coups():
    # Charger les données à partir du fichier CSV
    data = pd.read_csv('repertoire.csv')

    # Charger l'image du terrain
    img = mpimg.imread('rugby_xPoints.png')
    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, 60, 0, 70])  # Ajuster si nécessaire
    ax.set_aspect('equal')

    # Afficher les coups de pieds sur le terrain
    for index, row in data.iterrows():
        x, y = row['x'], row['y']
        if row['resultat'] == 'réussi':
            couleur = 'go'  # Point vert
        else:
            couleur = 'ro'  # Point rouge
        ax.plot(x, y, couleur)

    plt.title("Coups de pieds des joueurs")
    plt.show()

# Récupération des arguments de la commande
if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == 'afficher':
            afficher_coups()
        elif sys.argv[1] == 'heatmap':
            heatmap()
    elif len(sys.argv) != 5:
        print("Utilisation : python repertoire.py NOM_JOUEUR NOM_ÉQUIPE JOURNÉE TYPE_COUPE")
    else:
        nom_joueur = sys.argv[1]
        nom_equipe = sys.argv[2]
        journee = int(sys.argv[3])
        type_coup = sys.argv[4]
        image_path = 'rugby_xPoints.png'  # Chemin vers ton image
        gérer_terrain(image_path, nom_joueur, nom_equipe, journee, type_coup)
"""