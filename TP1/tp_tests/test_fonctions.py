import unittest
from fonctions import *

class TestFonctions(unittest.TestCase):

    def test_additionner_cas_positif(self):
        self.assertEqual(additionner(2, 3), 5)

    def test_additionner_cas_negatif(self):
        self.assertEqual(additionner(-2, -3), -5)

    def test_est_pair_nombre_pair(self):
        self.assertTrue(est_pair(4))

    def test_est_pair_nombre_impair(self):
        self.assertFalse(est_pair(3))

    def test_est_pair_zero(self):
        self.assertTrue(est_pair(0))

    def test_valider_email_valide(self):
        self.assertTrue(valider_email("test@example.com"))

    def test_valider_email_sans_arobase(self):
        self.assertFalse(valider_email("testexample.com"))

    def test_valider_email_sans_point(self):
        self.assertFalse(valider_email("test@example"))

    def test_calculer_moyenne_liste_normale(self):
        self.assertEqual(calculer_moyenne([10, 15, 20]), 15)

    def test_calculer_moyenne_liste_vide(self):
        self.assertEqual(calculer_moyenne([]), 0)

    def test_calculer_moyenne_une_note(self):
        self.assertEqual(calculer_moyenne([18]), 18)

    def test_convertir_temperature_zero(self):
        self.assertEqual(convertir_temperature(0), 32)

    def test_convertir_temperature_eau_bouillante(self):
        self.assertEqual(convertir_temperature(100), 212)
    
    def test_additionner_type_error(self):
        with self.assertRaises(TypeError):
            additionner("a", 5)

    def test_est_pair_type_error(self):
        with self.assertRaises(TypeError):
            est_pair(3.5)  # pas un int

    def test_valider_email_type_error(self):
        with self.assertRaises(TypeError):
            valider_email(12345)

    def test_calculer_moyenne_type_error(self):
        with self.assertRaises(TypeError):
            calculer_moyenne("pas une liste")

    def test_calculer_moyenne_valeur_invalide(self):
        with self.assertRaises(ValueError):
            calculer_moyenne([10, "quinze", 20])

    def test_convertir_temperature_type_error(self):
        with self.assertRaises(TypeError):
            convertir_temperature("trente")

if __name__ == '__main__':
    unittest.main()
