import math
from rugby_xpoints.calcul_proba import calculer_angle, calculer_distance


def test_calculer_distance_centre():
    # milieu entre les poteaux
    xA, yA = 0, 0
    xB, yB = 0, 10
    x, y = 0, 5  # exactement au milieu

    expected = 0
    result = calculer_distance(xA, yA, xB, yB, x, y)

    assert math.isclose(result, expected, abs_tol=1e-6)


def test_calculer_angle_symetrie():
    # deux poteaux verticaux identiques, point centré
    xA, yA = 0, 0
    xB, yB = 0, 10
    x, y = 10, 5  # pile au milieu horizontalement

    # angle théorique = 90°
    expected = 53.13010235415598
    result = calculer_angle(xA, yA, xB, yB, x, y)

    assert math.isclose(result, expected, abs_tol=1e-3)


def test_calculer_angle_protection_valeurs_invalides():
    # Cas où la géométrie crée un cos_theta légèrement hors [-1, 1]
    xA, yA = 0, 0
    xB, yB = 0, 10
    x, y = 0.0000000000001, 5  # très proche du milieu → arrondis flottants

    result = calculer_angle(xA, yA, xB, yB, x, y)

    assert 0 <= result <= 180  # un angle physique valide
