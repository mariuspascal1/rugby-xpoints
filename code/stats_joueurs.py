import pandas as pd
import tkinter as tk
from tkinter import simpledialog
import logging
import os

# ---------- CONFIGURATION LOGGING ----------
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)


# ---------- SAISIE UTILISATEUR ----------
def get_user_input():
    logger.info("Ouverture de la fenêtre de saisie des paramètres utilisateurs.")

    root = tk.Tk()
    root.withdraw()

    competition = simpledialog.askstring("Entrée utilisateur", "Compétition :")
    if not competition:
        logger.warning("Aucune compétition renseignée par l'utilisateur.")

    journee_str = simpledialog.askstring(
        "Entrée utilisateur", "Journée (laisser vide pour toute la compétition) :"
    )

    if journee_str == "":
        journee = None
        logger.info("L’utilisateur a choisi d'inclure toutes les journées.")
    else:
        try:
            journee = int(journee_str)
            logger.info(f"Journée sélectionnée : {journee}")
        except ValueError:
            logger.error("Valeur invalide entrée pour la journée. Passage à None.")
            journee = None

    logger.info(
        f"Saisie utilisateur terminée : competition={competition}, journee={journee}"
    )
    return competition, journee


# ---------- STATISTIQUES PAR JOURNÉE ----------
def creer_stats_joueurs(journee, competition):
    nom_fichier = f"data/coups_joueurs_{competition}_{journee}.csv"

    logger.info(f"Chargement des données : {nom_fichier}")

    if not os.path.exists(nom_fichier):
        logger.error(f"Fichier introuvable : {nom_fichier}")
        return

    try:
        data = pd.read_csv(nom_fichier)
    except Exception as e:
        logger.critical(f"Erreur lors de la lecture du fichier CSV : {e}")
        return

    if data.empty:
        logger.warning(f"Aucune donnée trouvée dans {nom_fichier}.")
        return

    logger.debug(f"Colonnes disponibles : {data.columns.tolist()}")

    # Création colonne points
    data["points"] = 0
    data.loc[
        (data["resultat"] == "réussi") & (data["type"] == "pénalité"), "points"
    ] = 3
    data.loc[
        (data["resultat"] == "réussi") & (data["type"] == "transformation"), "points"
    ] = 2

    logger.info("Calcul des statistiques joueur...")

    try:
        stats = (
            data.groupby(["joueur", "equipe", "journee"])
            .agg(
                pourcentage_reussite=(
                    "resultat",
                    lambda x: (x == "réussi").sum() / len(x) * 100,
                ),
                tirs_reussis=("resultat", lambda x: (x == "réussi").sum()),
                total_coups_de_pieds=("resultat", "count"),
                nombre_de_points_marqués=("points", "sum"),
                total_xPoints=("xPoints", "sum"),
                difficulté=("proba", lambda x: 1 - x.mean()),
            )
            .reset_index()
        )

    except Exception as e:
        logger.critical(f"Erreur lors du calcul des statistiques : {e}")
        return

    logger.debug(f"Stats calculées : {stats.head()}")

    # Calcul rating
    stats["Rating"] = stats["Nombre de points marqués"] / stats[
        "Nombre total de xPoints"
    ].replace(0, 1)

    # Arrondis
    cols = [
        "Pourcentage de réussite",
        "Nombre total de xPoints",
        "Difficulté",
        "Rating",
    ]
    stats[cols] = stats[cols].round(2)

    # Sauvegarde
    sortie = f"stats_joueurs_{competition}_{journee}.csv"
    try:
        stats.to_csv(sortie, index=False)
        logger.info(f"Statistiques enregistrées dans {sortie}")
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde du fichier {sortie} : {e}")


# ---------- STATISTIQUES GLOBALES ----------
def creer_stats_competition(competition):
    nom_fichier = f"coups_joueurs_{competition}_None.csv"

    logger.info(f"Chargement des données globales : {nom_fichier}")

    if not os.path.exists(nom_fichier):
        logger.error(f"Fichier global introuvable : {nom_fichier}")
        return

    try:
        df_global = pd.read_csv(nom_fichier)
    except Exception as e:
        logger.critical(f"Erreur lecture fichier global : {e}")
        return

    if df_global.empty:
        logger.warning("Aucune donnée disponible pour les statistiques globales.")
        return

    # Ajout points
    df_global["points"] = 0
    df_global.loc[
        (df_global["resultat"] == "réussi") & (df_global["type"] == "pénalité"),
        "points",
    ] = 3
    df_global.loc[
        (df_global["resultat"] == "réussi") & (df_global["type"] == "transformation"),
        "points",
    ] = 2

    logger.info("Calcul des statistiques globales...")

    try:
        stats_global = (
            df_global.groupby(["joueur", "equipe"])
            .agg(
                tirs_reussis=("resultat", lambda x: (x == "réussi").sum()),
                total_coups_de_pieds=("resultat", "count"),
                nombre_de_points_marqués=("points", "sum"),
                total_xPoints=("xPoints", "sum"),
                difficulté=("proba", lambda x: 1 - x.mean()),
            )
            .reset_index()
        )
    except Exception as e:
        logger.critical(f"Erreur calcul stats globales : {e}")
        return

    stats_global["pourcentage_reussite"] = (
        stats_global["tirs_reussis"] / stats_global["total_coups_de_pieds"] * 100
    )
    stats_global["rating"] = stats_global["nombre_de_points_marqués"] / stats_global[
        "total_xPoints"
    ].replace(0, 1)

    stats_global = stats_global.rename(
        columns={
            "rating": "Rating",
            "pourcentage_reussite": "Pourcentage de réussite",
            "tirs_reussis": "Tirs réussis",
            "total_coups_de_pieds": "Total de tentatives",
            "nombre_de_points_marqués": "Nombre de points marqués",
            "total_xPoints": "Nombre total de xPoints",
            "difficulté": "Difficulté",
        }
    )

    sortie = f"stats_joueurs_{competition}.csv"
    try:
        stats_global.to_csv(sortie, index=False)
        logger.info(f"Statistiques globales sauvegardées dans {sortie}")
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde globale : {e}")


# ---------- MAIN ----------
def main():
    logger.info("Démarrage du script stats_joueurs.py")

    competition, journee = get_user_input()

    if journee is None:
        creer_stats_competition(competition)
    else:
        creer_stats_joueurs(journee, competition)

    logger.info("Fin d'exécution du script.")


if __name__ == "__main__":
    main()
