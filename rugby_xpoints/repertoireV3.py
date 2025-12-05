import math
import logging
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import csv
import os
import tkinter as tk

# ---------- CONFIGURATION DU LOGGING ----------
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

tous_les_coups = []


# ---------- INTERFACE UTILISATEUR ----------
def start_interface():
    """
    Ouvre une interface Tkinter permettant de saisir l’identité du tireur,
    son équipe, la compétition, la journée et le type de coup de pied.

    L’interface valide ensuite les entrées utilisateur et lance l’affichage
    du terrain interactif permettant de cliquer pour enregistrer des tirs.

    Returns:
        None
    """
    logger.info("Ouverture de l'interface graphique de saisie.")

    root = tk.Tk()
    root.title("Saisie des informations")

    # Champs utilisateur
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
        """
        Valide la saisie utilisateur et lance l'affichage interactif du terrain.

        Returns:
            None
        """
        nom_joueur = entry_joueur.get()
        nom_equipe = entry_equipe.get()
        competition = entry_competition.get()
        journee = entry_journee.get()
        type_coup = entry_type.get()

        logger.info(
            f"Saisie utilisateur validée : joueur={nom_joueur}, équipe={nom_equipe}, "
            f"compétition={competition}, journée={journee}, type={type_coup}"
        )

        gérer_terrain(
            "rugby_xPoints.png", nom_joueur, nom_equipe, competition, journee, type_coup
        )

    # Bouton validation
    btn_valider = tk.Button(root, text="Valider", command=valider)
    btn_valider.grid(row=5, column=0, columnspan=2)

    root.mainloop()


# ---------- CALCUL ANGLE ----------
def calculer_angle(xA, yA, xB, yB, x, y):
    """
    Calcule l’angle visible entre les deux poteaux depuis un point donné.

    Args:
        xA (float): Position x du poteau gauche.
        yA (float): Position y du poteau gauche.
        xB (float): Position x du poteau droit.
        yB (float): Position y du poteau droit.
        x (float): Coordonnée x du point du tir.
        y (float): Coordonnée y du point du tir.

    Returns:
        float: Angle en degrés.

    Raises:
        Exception: Si un problème mathématique survient (ex: division par zéro).
    """
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
        logger.critical(f"Erreur lors du calcul de l'angle : {e}")
        raise


# ---------- CALCUL DISTANCE ----------
def calculer_distance(xA, yA, xB, yB, x, y):
    """
    Calcule la distance entre un point de tir et le milieu des poteaux.

    Args:
        xA, yA, xB, yB (float): Coordonnées des poteaux.
        x, y (float): Coordonnées du tir.

    Returns:
        float: Distance entre le tir et le centre des poteaux.

    Raises:
        Exception: Si une erreur mathématique survient.
    """
    try:
        milieu_A_B = ((xA + xB) / 2, (yA + yB) / 2)
        distance = math.sqrt((milieu_A_B[0] - x) ** 2 + (milieu_A_B[1] - y) ** 2)
        logger.debug(f"Distance calculée : {distance:.2f}")
        return distance

    except Exception as e:
        logger.critical(f"Erreur lors du calcul de la distance : {e}")
        raise


# ---------- INTERACTION AVEC LE TERRAIN ----------
def gérer_terrain(image_path, nom_joueur, nom_equipe, competition, journee, type_coup):
    """
    Affiche un terrain interactif permettant à l'utilisateur de cliquer
    pour enregistrer des coups de pied.

    Chaque clic :
      - bouton gauche = tir réussi
      - bouton droit = tir raté

    Les informations géométriques (angle, distance) sont calculées automatiquement.

    Args:
        image_path (str): Chemin de l'image du terrain.
        nom_joueur (str): Nom du buteur.
        nom_equipe (str): Nom de l'équipe.
        competition (str): Nom de la compétition.
        journee (str): Numéro de journée.
        type_coup (str): "pénalité" ou "transformation".

    Returns:
        None
    """
    global tous_les_coups

    logger.info("Chargement de l'image du terrain...")

    if not os.path.exists(image_path):
        logger.error(f"Image introuvable : {image_path}")
        return

    # Coordonnées des poteaux
    xA, yA = 7.5568, 29.7727
    xB, yB = 7.6515, 39.9053

    def on_click(event):
        """
        Callback appelé lors d’un clic sur le terrain.

        Args:
            event: Événement Matplotlib contenant les coordonnées du clic.

        Returns:
            None
        """
        x, y = event.xdata, event.ydata

        if x is None or y is None:
            logger.warning("Clic en dehors de la zone valide du terrain.")
            return

        if event.button == 1:
            resultat = "réussi"
        elif event.button == 3:
            resultat = "raté"
        else:
            return

        angle = calculer_angle(xA, yA, xB, yB, x, y)
        distance = calculer_distance(xA, yA, xB, yB, x, y)

        logger.info(
            f"Clic enregistré : ({x:.1f}, {y:.1f}) - {resultat}, "
            f"angle={angle:.2f}, distance={distance:.2f}"
        )

        tous_les_coups.append(
            [
                nom_joueur,
                nom_equipe,
                competition,
                journee,
                type_coup,
                x,
                y,
                resultat,
                angle,
                distance,
            ]
        )

        couleur = "go" if resultat == "réussi" else "ro"
        plt.plot(x, y, couleur)
        plt.draw()

        sauvegarder_coups("data/repertoire.csv")

    def dessiner_terrain():
        """
        Affiche l'image du terrain et prépare la capture graphique des clics.

        Returns:
            None
        """
        try:
            img = mpimg.imread(image_path)
        except Exception as e:
            logger.error(f"Erreur lors du chargement de l'image : {e}")
            return

        logger.info("Affichage du terrain interactif.")
        fig, ax = plt.subplots()
        ax.imshow(img, extent=[0, 60, 0, 70])
        ax.set_aspect("equal")

        plt.title(
            f"Coups de pied - {nom_joueur} ({nom_equipe}) "
            f"- {competition} - Journée {journee}"
        )

        fig.canvas.mpl_connect("button_press_event", on_click)
        plt.show()

    dessiner_terrain()


# ---------- SAUVEGARDE ----------
def sauvegarder_coups(fichier_sauvegarde):
    """
    Sauvegarde toutes les entrées présentes dans `tous_les_coups`
    dans un fichier CSV (création ou ajout).

    Args:
        fichier_sauvegarde (str): Chemin du CSV où écrire les données.

    Returns:
        None
    """
    global tous_les_coups

    mode = "a" if os.path.exists(fichier_sauvegarde) else "w"

    try:
        with open(fichier_sauvegarde, mode, newline="") as file:
            writer = csv.writer(file)

            if mode == "w":
                logger.info("Création d'un nouveau fichier repertoire.csv.")
                writer.writerow(
                    [
                        "joueur",
                        "equipe",
                        "competition",
                        "journee",
                        "type",
                        "x",
                        "y",
                        "resultat",
                        "angle",
                        "distance",
                    ]
                )

            writer.writerows(tous_les_coups)

        logger.info(f"Fichier mis à jour : {fichier_sauvegarde}")

    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde CSV : {e}")


# ---------- MAIN ----------
def main():
    """
    Point d'entrée du script.
    Lance l'interface graphique pour la saisie des informations,
    puis ouvre le terrain interactif.

    Returns:
        None
    """
    logger.info("Lancement du script repertoireV3.py")
    start_interface()
    logger.info("Script terminé.")


if __name__ == "__main__":
    main()
