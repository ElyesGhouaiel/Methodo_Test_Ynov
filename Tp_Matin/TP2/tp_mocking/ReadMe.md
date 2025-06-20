# TP2 – Mocking et Fixtures

> Méthodologies de tests – Ynov  
> Auteur : Elyes  
> Date : 2025-06-20

---

## Objectifs du TP

- Comprendre pourquoi mocker les dépendances externes
- Apprendre à créer et configurer des mocks
- Maîtriser les fixtures pour organiser les tests
- Tester des fonctions avec dépendances réelles

---

## Structure du projet

```

tp\_mocking/
├── weather\_service.py
└── test\_weather.py

```

---

## Prérequis

- Python 3.6+
- Module `requests` :  
```

pip install requests

````

---

##  Partie 1 – Le problème des dépendances

### Fonction testée

```python
def get_temperature(city):
  ...
  response = requests.get(...)
  if response.status_code == 200:
      return data['main']['temp']
  else:
      return None
````

### Test exécuté (sans mock)

```python
def test_get_temperature_paris(self):
    temp = get_temperature("Paris")
    self.assertIsNotNone(temp)
```

###  Résultat

* ❌ Avant d’avoir la vraie clé API → `AssertionError: unexpectedly None`
* ✅ Après avoir mis la clé API → test réussi

###  Réponses aux questions

1. **Que se passe-t-il si vous n’avez pas internet ?**
   → Le test échoue, car l’appel API ne peut pas se faire.

2. **Comment tester un code API qui retourne une erreur ?**
   → On ne peut pas de façon fiable sans mock. L’erreur doit être simulée.

3. **Comment être sûr que votre fonction gère tous les cas ?**
   → En testant chaque cas indépendamment via un mock, sans dépendre de l’API réelle.

---

## Partie 2 – Premier mock

### Objectif

* Simuler une réponse `200 OK` avec température 25.5
* Tester `get_temperature("Paris")` sans appel réseau

### ✔ Résultat

✅ Test réussi sans connexion internet.

---

## Partie 3 – Cas d’erreur

### Tests ajoutés

* ville inconnue (404)
* exception réseau (RequestException)

### Réponses

1. **Que doit retourner la fonction si `status_code != 200` ?**
   → `None`

2. **Comment vérifier que l’API a bien été appelée ?**
   → `mock_get.assert_called_once_with(...)`

✅ Tous les cas sont bien testés.

---

## Partie 4 – Fixtures

### Objectif

* Réutiliser des données types dans tous les tests
* Réduire la duplication

### Mise en place

```python
def setUp(self):
    self.test_city = "Paris"
    self.sample_weather_data = { 'main': { 'temp': 22.0 } }
```

✅ Test avec fixture passé avec succès.

---

## Partie 5 – Service plus complexe

### Nouvelle fonction

```python
def save_weather_report(city):
    temp = get_temperature(city)
    ...
    json.dump(reports, f)
```

### Test simulé

* température fixée à `20.5`
* date simulée `"2024-01-01T12:00:00"`
* fichier simulé avec `mock_open`

✅ Test passé avec succès

---

## 🔁 Partie 6 – Test paramétré

### Test de plusieurs villes en une seule méthode

```python
for city, expected_temp in cities_and_temps:
    with self.subTest(city=city):
        ...
```

✅ Trois villes testées : `Paris`, `Londres`, `Tokyo`

---

## Partie 7 – Réflexion

### 1. **Avantages du mock**

* Tests plus rapides, fiables, indépendants
* Plus besoin d’appels réseau réels

### 2. **Pourquoi chaque test doit être indépendant ?**

* Pour éviter les effets de bord
* Pour pouvoir exécuter les tests dans n’importe quel ordre

### 3. **Les mocks sont-ils réalistes ?**

* Oui, si on **respecte la structure exacte** de l’API
* Il faut consulter la documentation officielle

---

##  Bonnes pratiques appliquées

* Nommage clair des tests : `test_nomfonction_cas`
* Structure Arrange / Act / Assert
* Utilisation de `setUp()`
* Isolation totale des tests
* Patch bien ciblé (`requests.get`, `datetime`, `open`...)

---

## Bilan

✔ 6 tests fonctionnels
✔ Gestion des erreurs, réseau, fichiers
✔ Structure de projet claire
✔ TP validé avec succès 