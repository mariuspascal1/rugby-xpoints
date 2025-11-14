import pandas as pd
import glob
import sys
import tkinter as tk
from tkinter import simpledialog, ttk

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

def creer_stats_joueurs(journee, competition):
    # Charger les données à partir du fichier coups_joueurs{n}.csv
    nom_fichier = f'coups_joueurs_{competition}_{journee}.csv'
    data = pd.read_csv(nom_fichier)

    # Créer des colonnes temporaires pour les calculs
    data['points'] = 0
    data.loc[(data['resultat'] == 'réussi') & (data['type'] == 'pénalité'), 'points'] = 3
    data.loc[(data['resultat'] == 'réussi') & (data['type'] == 'transformation'), 'points'] = 2

    # Calculer les statistiques
    stats = data.groupby(['joueur', 'equipe', 'journee']).agg(
        pourcentage_reussite=('resultat', lambda x: (x == 'réussi').sum() / len(x) * 100 if len(x) > 0 else 0),
        tirs_reussis=('resultat', lambda x: (x == 'réussi').sum()),
        total_coups_de_pieds=('resultat', 'count'),
        nombre_de_points_marqués=('points', 'sum'),
        total_xPoints=('xPoints', 'sum'),
        difficulté=('proba', lambda x: 1 - x.mean() if len(x) > 0 else 1)
    ).reset_index()

    # Renommer les colonnes
    stats.rename(columns={
        'pourcentage_reussite': 'Pourcentage de réussite',
        'tirs_reussis': 'Tirs réussis',
        'total_coups_de_pieds': 'Total de tentatives',
        'nombre_de_points_marqués': 'Nombre de points marqués',
        'total_xPoints': 'Nombre total de xPoints',
        'difficulté': 'Difficulté',
        'rating': 'Rating'
    }, inplace=True)

    # Calculer le rating
    stats['Rating'] = stats['Nombre de points marqués'] / stats['Nombre total de xPoints'].replace(0, 1)

    # Limiter à 2 chiffres après la virgule pour les colonnes concernées
    cols_to_round = ['Pourcentage de réussite', 'Nombre total de xPoints', 'Difficulté', 'Rating']
    stats[cols_to_round] = stats[cols_to_round].round(2)

    # Conversion des colonnes en type numérique
    numeric_cols = ['Pourcentage de réussite', 'Tirs réussis', 'Total de tentatives', 
                    'Nombre de points marqués', 'Nombre total de xPoints', 
                    'Difficulté', 'Rating']
    stats[numeric_cols] = stats[numeric_cols].apply(pd.to_numeric, errors='coerce')

    # Sauvegarder les statistiques dans le fichier stats_joueurs{n}.csv
    stats_nom_fichier = f'stats_joueurs_{competition}_{journee}.csv'
    stats.to_csv(stats_nom_fichier, index=False)
    print(f"Statistiques pour la journée {journee} sauvegardées dans {stats_nom_fichier}.")

# Fonction pour créer les statistiques globales (inchangée)
def creer_stats_competition(competition):
    # Charger directement le fichier avec toutes les données pour la compétition
    nom_fichier = f'coups_joueurs_{competition}_None.csv'
    df_global = pd.read_csv(nom_fichier)

    # Créer des colonnes temporaires pour les calculs
    df_global['points'] = 0
    df_global.loc[(df_global['resultat'] == 'réussi') & (df_global['type'] == 'pénalité'), 'points'] = 3
    df_global.loc[(df_global['resultat'] == 'réussi') & (df_global['type'] == 'transformation'), 'points'] = 2

    # Calculer les statistiques globales
    stats_global = df_global.groupby(['joueur', 'equipe']).agg(
        tirs_reussis=('resultat', lambda x: (x == 'réussi').sum()),
        total_coups_de_pieds=('resultat', 'count'),
        nombre_de_points_marqués=('points', 'sum'),
        total_xPoints=('xPoints', 'sum'),
        difficulté=('proba', lambda x: 1 - x.mean() if len(x) > 0 else 1)
    ).reset_index()

    # Ajouter le pourcentage de réussite
    stats_global['pourcentage_reussite'] = stats_global['tirs_reussis'] / stats_global['total_coups_de_pieds'].replace(0, 1) * 100
    # Ajouter le rating
    stats_global['rating'] = stats_global['nombre_de_points_marqués'] / stats_global['total_xPoints'].replace(0, 1)

    # Limiter à 2 chiffres après la virgule pour les colonnes concernées
    cols_to_round = ['pourcentage_reussite', 'nombre_de_points_marqués', 'total_xPoints', 'difficulté', 'rating']
    stats_global[cols_to_round] = stats_global[cols_to_round].round(2)

    # Renommer les colonnes
    stats_global = stats_global.rename(columns={
        'rating': 'Rating',
        'pourcentage_reussite': 'Pourcentage de réussite',
        'tirs_reussis': 'Tirs réussis',
        'total_coups_de_pieds': 'Total de tentatives',
        'nombre_de_points_marqués': 'Nombre de points marqués',
        'total_xPoints': 'Nombre total de xPoints',
        'difficulté': 'Difficulté'
    })

    # Sauvegarder le fichier final
    stats_global.to_csv(f'stats_joueurs_{competition}.csv', index=False)
    print(f"Statistiques globales sauvegardées dans stats_joueurs_{competition}.csv.")

def main():
    competition, journee = get_user_input()
    if journee is None: #0 pour faire les stats de toute la compétition
        creer_stats_competition(competition)
    else:
        creer_stats_joueurs(journee, competition)

if __name__ == "__main__":
    main()


"""import pandas as pd
import glob
import sys
import tkinter as tk
from tkinter import simpledialog

def get_user_input():
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale

    nom_joueur = simpledialog.askstring("Entrée utilisateur", "Joueur :")
    nom_equipe = simpledialog.askstring("Entrée utilisateur", "Équipe :")
    competition = simpledialog.askstring("Entrée utilisateur", "Compétition :")
    journee = simpledialog.askinteger("Entrée utilisateur", "Journée :")
    type_coup = simpledialog.askstring("Entrée utilisateur", "Type (pénalité/transformation) :")
    
    return nom_joueur, nom_equipe, competition, journee, type_coup

def creer_nom_fichier(nom_joueur, nom_equipe, competition, journee, type_coup):
    elements = ["coups_joueurs"]
    if competition: elements.append(competition)
    if journee: elements.append(str(journee))
    if nom_equipe: elements.append(nom_equipe)
    if nom_joueur: elements.append(nom_joueur)
    if type_coup: elements.append(type_coup)
    
    return "_".join(elements) + ".csv"

def creer_stats_joueurs():
    nom_joueur, nom_equipe, competition, journee, type_coup = get_user_input()
    nom_fichier = creer_nom_fichier(nom_joueur, nom_equipe, competition, journee, type_coup)
    
    try:
        data = pd.read_csv(nom_fichier)
    except FileNotFoundError:
        print(f"Fichier {nom_fichier} introuvable.")
        return
    
    data['points'] = 0
    data.loc[(data['resultat'] == 'réussi') & (data['type'] == 'pénalité'), 'points'] = 3
    data.loc[(data['resultat'] == 'réussi') & (data['type'] == 'transformation'), 'points'] = 2

    stats = data.groupby(['joueur', 'equipe', 'journee']).agg(
        pourcentage_reussite=('resultat', lambda x: (x == 'réussi').sum() / len(x) * 100 if len(x) > 0 else 0),
        tirs_reussis=('resultat', lambda x: (x == 'réussi').sum()),
        total_coups_de_pieds=('resultat', 'count'),
        nombre_de_points_marqués=('points', 'sum'),
        total_xPoints=('xPoints', 'sum'),
        difficulté=('proba', lambda x: 1 - x.mean() if len(x) > 0 else 1)
    ).reset_index()
    
    stats.rename(columns={
        'pourcentage_reussite': 'Pourcentage de réussite',
        'tirs_reussis': 'Tirs réussis',
        'total_coups_de_pieds': 'Total de tentatives',
        'nombre_de_points_marqués': 'Nombre de points marqués',
        'total_xPoints': 'Nombre total de xPoints',
        'difficulté': 'Difficulté'
    }, inplace=True)
    
    stats['Rating'] = stats['Nombre de points marqués'] / stats['Nombre total de xPoints'].replace(0, 1)
    stats[['Pourcentage de réussite', 'Nombre total de xPoints', 'Difficulté', 'Rating']] = stats[['Pourcentage de réussite', 'Nombre total de xPoints', 'Difficulté', 'Rating']].round(2)
    
    stats_nom_fichier = nom_fichier.replace("coups_joueurs", "stats_joueurs")
    stats.to_csv(stats_nom_fichier, index=False)
    print(f"Statistiques sauvegardées dans {stats_nom_fichier}.")

if __name__ == "__main__":
    creer_stats_joueurs()"""
