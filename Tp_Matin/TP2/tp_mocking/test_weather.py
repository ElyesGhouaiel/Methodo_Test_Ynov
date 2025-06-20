import unittest
import requests
from unittest.mock import patch, Mock
from weather_service import get_temperature

class TestWeather(unittest.TestCase):

    @patch('weather_service.requests.get')
    def test_get_temperature_success(self, mock_get):
        """Premier test avec mock - cas de succès"""

        # 1. Créer un objet Mock pour simuler la réponse HTTP
        fake_response = Mock()
        fake_response.status_code = 200

        # 2. Créer les données JSON simulées
        fake_response.json.return_value = {
            'main': {
                'temp': 25.5
            }
        }

        # 3. Configurer mock_get pour retourner fake_response
        mock_get.return_value = fake_response

        # 4. Appeler la fonction réelle
        result = get_temperature("Paris")

        # 5. Vérifier le résultat
        self.assertEqual(result, 25.5)

        # 6. Vérifier que requests.get a été appelé avec les bons paramètres
        mock_get.assert_called_once_with(
            'http://api.openweathermap.org/data/2.5/weather',
            params={
                'q': 'Paris',
                'appid': '441f54eb9b8819b3a05d1674294bb055',
                'units': 'metric'
            }
        )
    @patch('weather_service.requests.get')
    def test_get_temperature_city_not_found(self, mock_get):
        """Test quand la ville n'existe pas"""

        # 1. Créez un faux objet réponse avec status_code = 404
        fake_response = Mock()
        fake_response.status_code = 404

        # 2. Configurez le mock pour retourner cette fausse réponse
        mock_get.return_value = fake_response

        # 3. Appelez la fonction avec une ville invalide
        result = get_temperature("VilleInexistante")

        # 4. Vérifiez que le résultat est None
        self.assertIsNone(result)

        # 5. Vérifiez l'appel de l'API
        mock_get.assert_called_once_with(
            'http://api.openweathermap.org/data/2.5/weather',
            params={
                'q': 'VilleInexistante',
                'appid': '441f54eb9b8819b3a05d1674294bb055',
                'units': 'metric'
            }
        )

    @patch('weather_service.requests.get')
    def test_get_temperature_network_error(self, mock_get):
        """Test quand il y a une erreur réseau"""

        # Simule une exception réseau
        mock_get.side_effect = requests.exceptions.RequestException()

        # Appelez la fonction
        result = get_temperature("Paris")

        # Doit retourner None
        self.assertIsNone(result)

        # Vérifiez que l'appel a été tenté
        mock_get.assert_called_once()
    

if __name__ == '__main__':
    unittest.main()
