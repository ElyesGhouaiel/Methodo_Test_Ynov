import unittest
from weather_service import get_temperature

class TestWeather(unittest.TestCase):

    def test_get_temperature_paris(self):
        """Test basique qui va poser problème"""
        temp = get_temperature("Paris")
        # Comment tester ça ? L'API peut être en panne, lente, différente...
        self.assertIsNotNone(temp)  # Test très faible

if __name__ == '__main__':
    unittest.main()
