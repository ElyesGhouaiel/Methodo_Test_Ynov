import pytest
from fonctions import *

def test_additionner_cas_positif():
    assert additionner(2, 3) == 5

def test_additionner_cas_negatif():
    assert additionner(-2, -3) == -5

def test_est_pair_nombre_pair():
    assert est_pair(4) == True

def test_est_pair_nombre_impair():
    assert est_pair(3) == False

def test_est_pair_zero():
    assert est_pair(0) == True

def test_valider_email_valide():
    assert valider_email("test@example.com") == True

def test_valider_email_sans_arobase():
    assert valider_email("testexample.com") == False

def test_valider_email_sans_point():
    assert valider_email("test@example") == False

def test_calculer_moyenne_liste_normale():
    assert calculer_moyenne([10, 15, 20]) == 15

def test_calculer_moyenne_liste_vide():
    assert calculer_moyenne([]) == 0

def test_calculer_moyenne_une_note():
    assert calculer_moyenne([18]) == 18

def test_convertir_temperature_zero():
    assert convertir_temperature(0) == 32

def test_convertir_temperature_eau_bouillante():
    assert convertir_temperature(100) == 212

def test_additionner_type_error():
    with pytest.raises(TypeError):
        additionner("a", 5)

def test_est_pair_type_error():
    with pytest.raises(TypeError):
        est_pair("8")

def test_valider_email_type_error():
    with pytest.raises(TypeError):
        valider_email(999)

def test_calculer_moyenne_type_error():
    with pytest.raises(TypeError):
        calculer_moyenne("pas une liste")

def test_calculer_moyenne_valeur_invalide():
    with pytest.raises(ValueError):
        calculer_moyenne([12, "erreur", 18])

def test_convertir_temperature_type_error():
    with pytest.raises(TypeError):
        convertir_temperature(None)
import pytest
from fonctions import *

def test_additionner_cas_positif():
    assert additionner(2, 3) == 5

def test_additionner_cas_negatif():
    assert additionner(-2, -3) == -5

def test_est_pair_nombre_pair():
    assert est_pair(4) == True

def test_est_pair_nombre_impair():
    assert est_pair(3) == False

def test_est_pair_zero():
    assert est_pair(0) == True

def test_valider_email_valide():
    assert valider_email("test@example.com") == True

def test_valider_email_sans_arobase():
    assert valider_email("testexample.com") == False

def test_valider_email_sans_point():
    assert valider_email("test@example") == False

def test_calculer_moyenne_liste_normale():
    assert calculer_moyenne([10, 15, 20]) == 15

def test_calculer_moyenne_liste_vide():
    assert calculer_moyenne([]) == 0

def test_calculer_moyenne_une_note():
    assert calculer_moyenne([18]) == 18

def test_convertir_temperature_zero():
    assert convertir_temperature(0) == 32

def test_convertir_temperature_eau_bouillante():
    assert convertir_temperature(100) == 212

def test_additionner_type_error():
    with pytest.raises(TypeError):
        additionner("a", 5)

def test_est_pair_type_error():
    with pytest.raises(TypeError):
        est_pair("8")

def test_valider_email_type_error():
    with pytest.raises(TypeError):
        valider_email(999)

def test_calculer_moyenne_type_error():
    with pytest.raises(TypeError):
        calculer_moyenne("pas une liste")

def test_calculer_moyenne_valeur_invalide():
    with pytest.raises(ValueError):
        calculer_moyenne([12, "erreur", 18])

def test_convertir_temperature_type_error():
    with pytest.raises(TypeError):
        convertir_temperature(None)