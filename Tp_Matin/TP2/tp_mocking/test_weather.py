import unittest
import requests
from unittest.mock import patch, Mock,mock_open, patch
from weather_service import save_weather_report
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

    def setUp(self):
        """Fixture : données communes à tous les tests"""
        self.test_city = "Paris"
        self.sample_weather_data = {
            'main': {
                'temp': 22.0
            }
        }

    @patch('weather_service.requests.get')
    def test_get_temperature_success_with_fixture(self, mock_get):
        """Test avec données de la fixture"""

        fake_response = Mock()
        fake_response.status_code = 200
        fake_response.json.return_value = self.sample_weather_data

        mock_get.return_value = fake_response

        result = get_temperature(self.test_city)

        self.assertEqual(result, 22.0)
        mock_get.assert_called_once_with(
            'http://api.openweathermap.org/data/2.5/weather',
            params={
                'q': self.test_city,
                'appid': '441f54eb9b8819b3a05d1674294bb055',
                'units': 'metric'
            }
        )

    @patch('weather_service.requests.get')
    def test_multiple_cities(self, mock_get):
        """Test plusieurs villes avec une seule méthode"""

        cities_and_temps = [
            ("Paris", 25.0),
            ("Londres", 18.5),
            ("Tokyo", 30.2)
        ]

        for city, expected_temp in cities_and_temps:
            with self.subTest(city=city):
                fake_response = Mock()
                fake_response.status_code = 200
                fake_response.json.return_value = {'main': {'temp': expected_temp}}
                mock_get.return_value = fake_response

                result = get_temperature(city)
                self.assertEqual(result, expected_temp)

                mock_get.assert_called_with(
                    'http://api.openweathermap.org/data/2.5/weather',
                    params={
                        'q': city,
                        'appid': '441f54eb9b8819b3a05d1674294bb055',
                        'units': 'metric'
                    }
                )

class TestWeatherReport(unittest.TestCase):

    def setUp(self):
        self.test_city = "Paris"
        self.fixed_datetime = "2024-01-01T12:00:00"

    @patch('weather_service.datetime')
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    @patch('weather_service.get_temperature')
    def test_save_weather_report_success(self, mock_get_temp, mock_file, mock_datetime):
        mock_get_temp.return_value = 20.5
        mock_datetime.now.return_value.isoformat.return_value = self.fixed_datetime

        result = save_weather_report(self.test_city)
        self.assertTrue(result)
        mock_get_temp.assert_called_once_with(self.test_city)
        self.assertEqual(mock_file.call_count, 2)
        mock_file.assert_any_call("weather_log.json", 'r')
        mock_file.assert_any_call("weather_log.json", 'w')

if __name__ == '__main__':
    unittest.main()
