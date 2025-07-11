# TaskManager - Module de Gestion de Tâches

## 📋 Description

Module complet de gestion de tâches avec toutes les bonnes pratiques :
- Tests unitaires et d'intégration
- Mocking des dépendances externes
- Organisation professionnelle du code
- Couverture de code 95%+

## 🏗️ Structure du projet

```
task_manager_project/
├── src/task_manager/           # Code source principal
│   ├── task.py                # Entité Task + Priority/Status
│   ├── manager.py             # Gestionnaire TaskManager  
│   └── services.py            # Services externes (Email/Report)
├── tests/                     # Tests complets
│   ├── test_task.py          # Tests unitaires Task
│   ├── test_manager.py       # Tests unitaires Manager
│   ├── test_services.py      # Tests d'intégration Services
│   └── fixtures/             # Données de test
└── requirements.txt          # Dépendances
```

## 🚀 Installation

```bash
pip install -r requirements.txt
```

## 💻 Utilisation rapide

```python
from src.task_manager import TaskManager, Priority

# Créer un gestionnaire
manager = TaskManager()

# Ajouter des tâches
task_id = manager.add_task(
    title="Ma première tâche",
    description="Description détaillée", 
    priority=Priority.HIGH
)

# Marquer comme terminée
task = manager.get_task(task_id)
task.mark_completed()

# Sauvegarder
manager.save_to_file("mes_taches.json")

# Statistiques
stats = manager.get_statistics()
print(f"Tâches terminées : {stats['completed_tasks']}")
```

## 🧪 Tests

**⚠️ À FAIRE par le binôme :**

1. **Tests unitaires** (test_task.py, test_manager.py)
2. **Tests d'intégration** (test_services.py) 
3. **Mocking des services externes**
4. **Couverture 95%+**
5. **Configuration pytest.ini + Makefile**
6. **CI/CD GitHub Actions**

```bash
# Lancer les tests
pytest

# Avec couverture  
pytest --cov=src/task_manager --cov-report=html
```

## 📊 Fonctionnalités implémentées

✅ **Entité Task complète**
- Priorités (LOW, MEDIUM, HIGH, URGENT)
- Statuts (TODO, IN_PROGRESS, DONE, CANCELLED)
- Sérialisation JSON

✅ **Gestionnaire TaskManager**
- CRUD complet des tâches
- Filtrage par statut/priorité/projet
- Sauvegarde/chargement JSON
- Statistiques détaillées

✅ **Services externes**
- EmailService (notifications mockables)
- ReportService (rapports CSV/JSON)

## 🎯 Prochaines étapes (pour le binôme)

1. **Phase 3** : Implémenter TOUS les tests
2. **Phase 4** : Configuration automatisation (pytest.ini, Makefile, CI/CD)
3. **Phase 5** : Demo script + validation finale

**Objectif** : 95%+ couverture de tests sur tout le module !

---

*Code développé selon les spécifications du TP Projet Final* 