import pandas as pd
import numpy as np
import math
import logging
from sklearn.linear_model import LogisticRegression
import tkinter as tk
from tkinter import simpledialog

# ---------- CONFIGURATION DU LOGGING ----------
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,  # Change en DEBUG si tu veux plus de détails
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)


# ---------- INTERACTION UTILISATEUR ----------
def get_user_input():
    logger.info("Ouverture de la fenêtre de saisie utilisateur.")

    root = tk.Tk()
    root.withdraw()

    competition = simpledialog.askstring("Entrée utilisateur", "Compétition :")
    logger.debug(f"Compétition saisie : {competition}")

    journee_str = simpledialog.askstring(
        "Entrée utilisateur", "Journée (laisser vide pour toute la compétition) :"
    )

    if journee_str == "":
        journee = None
        logger.info(
            "Aucune journée sélectionnée : traitement pour toute la compétition."
        )
    else:
        try:
            journee = int(journee_str)
            logger.debug(f"Journée saisie : {journee}")
        except ValueError:
            logger.warning(f"Valeur invalide entrée pour la journée : {journee_str}")
            journee = None

    return competition, journee


# ---------- CALCUL DES ANGLES & DISTANCES ----------
def calculer_angle(xA, yA, xB, yB, x, y):
    try:
        dA = math.sqrt((xA - x) ** 2 + (yA - y) ** 2)
        dB = math.sqrt((xB - x) ** 2 + (yB - y) ** 2)
        dAB = math.sqrt((xB - xA) ** 2 + (yB - yA) ** 2)

        cos_theta = (dA**2 + dB**2 - dAB**2) / (2 * dA * dB)
        theta = math.acos(cos_theta)
        angle = math.degrees(theta)

        logger.debug(f"Angle calculé : {angle:.2f}°")
        return angle

    except Exception as e:
        logger.critical(f"Erreur lors du calcul d'angle : {e}")
        raise


def calculer_distance(xA, yA, xB, yB, x, y):
    try:
        milieu_A_B = ((xA + xB) / 2, (yA + yB) / 2)
        distance = math.sqrt((milieu_A_B[0] - x) ** 2 + (milieu_A_B[1] - y) ** 2)

        logger.debug(f"Distance calculée : {distance:.2f}")
        return distance

    except Exception as e:
        logger.critical(f"Erreur lors du calcul de distance : {e}")
        raise


# ---------- CHARGEMENT DU MODÈLE ----------
def charger_modele():
    logger.info("Chargement du fichier repertoire.csv...")

    try:
        data = pd.read_csv("data/repertoire.csv")
    except FileNotFoundError:
        logger.error("Fichier data/repertoire.csv introuvable !")
        raise

    logger.info("Données chargées. Entraînement du modèle...")
    logger.debug(f"Colonnes disponibles : {list(data.columns)}")

    data["resultat"] = data["resultat"].map({"réussi": 1, "raté": 0})
    X = data[["angle", "distance"]]
    y = data["resultat"]

    model = LogisticRegression()
    model.fit(X, y)

    logger.info("Modèle de régression logistique entraîné avec succès.")
    return model


# ---------- CALCUL DE LA PROBABILITÉ ----------
def probabilite_reussite(model, angle, distance):
    try:
        prob = model.predict_proba([[angle, distance]])[0][1]
        logger.debug(f"Probabilité calculée : {prob:.4f}")
        return prob
    except Exception as e:
        logger.error(f"Erreur lors du calcul de probabilité : {e}")
        raise


# ---------- PIPELINE PRINCIPAL ----------
def coups_joueurs(journee, competition):
    logger.info(
        f"Début du traitement pour compétition={competition}, journée={journee}"
    )

    model = charger_modele()

    try:
        data = pd.read_csv("data/repertoire.csv")
    except FileNotFoundError:
        logger.error("Impossible de charger repertoire.csv dans data/")
        return

    # Filtrage
    if journee is None:
        data_copy = data[data["competition"] == competition].copy()
        logger.info("Traitement sur l'ensemble de la compétition.")
    else:
        data_copy = data[
            (data["competition"] == competition) & (data["journee"] == journee)
        ].copy()
        logger.info(f"Traitement pour la journée {journee}.")

    if data_copy.empty:
        logger.warning("Aucune donnée à traiter.")
        return

    logger.info(f"{len(data_copy)} coups trouvés pour traitement.")

    xA, yA, xB, yB = 7.5568, 29.7727, 7.6515, 39.9053

    # Calculs
    data_copy.loc[:, "angle"] = data_copy.apply(
        lambda row: calculer_angle(xA, yA, xB, yB, row["x"], row["y"]), axis=1
    )
    data_copy.loc[:, "distance"] = data_copy.apply(
        lambda row: calculer_distance(xA, yA, xB, yB, row["x"], row["y"]), axis=1
    )
    data_copy.loc[:, "proba"] = data_copy.apply(
        lambda row: probabilite_reussite(model, row["angle"], row["distance"]), axis=1
    )
    data_copy.loc[:, "xPoints"] = np.where(
        data_copy["type"] == "transformation",
        data_copy["proba"] * 2,
        data_copy["proba"] * 3,
    )

    # Sauvegarde
    nom_fichier = f"data/coups_joueurs_{competition}_{journee}.csv"
    data_copy.to_csv(nom_fichier, index=False)
    logger.info(f"Fichier sauvegardé : {nom_fichier}")


# ---------- LANCEMENT ----------
def main():
    logger.info("Lancement du script calcul_proba.py")
    competition, journee = get_user_input()
    coups_joueurs(journee, competition)
    logger.info("Script terminé avec succès.")


if __name__ == "__main__":
    main()
