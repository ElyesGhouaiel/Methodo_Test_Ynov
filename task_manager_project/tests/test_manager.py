import pytest
from unittest.mock import patch, mock_open, MagicMock
import json
from src.task_manager.manager import TaskManager
from src.task_manager.task import Task, Priority, Status

class TestTaskManagerBasics:
    """Tests basiques du gestionnaire"""
    
    def setup_method(self):
        self.manager = TaskManager(storage_file="/tmp/test_tasks.json")
        self.manager.clear_all_tasks()

    def test_add_task_returns_id(self):
        task_id = self.manager.add_task("Titre", "Desc", Priority.HIGH)
        assert isinstance(task_id, str)
        task = self.manager.get_task(task_id)
        assert task is not None
        assert task.title == "Titre"
        assert task.description == "Desc"
        assert task.priority == Priority.HIGH

    def test_get_task_returns_none_if_not_found(self):
        assert self.manager.get_task("inexistant") is None

    def test_delete_task_removes_task(self):
        task_id = self.manager.add_task("A supprimer")
        assert self.manager.delete_task(task_id) is True
        assert self.manager.get_task(task_id) is None
        assert self.manager.delete_task("inexistant") is False

    def test_update_task_status(self):
        task_id = self.manager.add_task("A faire")
        assert self.manager.update_task_status(task_id, Status.DONE) is True
        task = self.manager.get_task(task_id)
        assert task is not None
        assert task.status == Status.DONE
        assert task.completed_at is not None
        assert self.manager.update_task_status("inexistant", Status.DONE) is False

    def test_get_tasks_by_status(self):
        t1 = self.manager.add_task("T1")
        t2 = self.manager.add_task("T2")
        self.manager.update_task_status(t2, Status.DONE)
        todos = self.manager.get_tasks_by_status(Status.TODO)
        dones = self.manager.get_tasks_by_status(Status.DONE)
        assert all(t.status == Status.TODO for t in todos)
        assert all(t.status == Status.DONE for t in dones)

    def test_get_tasks_by_priority(self):
        t1 = self.manager.add_task("T1", priority=Priority.LOW)
        t2 = self.manager.add_task("T2", priority=Priority.HIGH)
        lows = self.manager.get_tasks_by_priority(Priority.LOW)
        highs = self.manager.get_tasks_by_priority(Priority.HIGH)
        assert all(t.priority == Priority.LOW for t in lows)
        assert all(t.priority == Priority.HIGH for t in highs)

    def test_get_tasks_by_project(self):
        t1 = self.manager.add_task("T1")
        t2 = self.manager.add_task("T2")
        task1 = self.manager.get_task(t1)
        task2 = self.manager.get_task(t2)
        assert task1 is not None
        assert task2 is not None
        task1.assign_to_project("P1")
        task2.assign_to_project("P2")
        # Debug print pour vérifier l'état des tâches
        # print([(t.title, t.project_id) for t in self.manager.tasks])
        p1_tasks = self.manager.get_tasks_by_project("P1")
        # Correction : il se peut que project_id soit None par défaut, donc on vérifie bien l'assignation
        assert any(t.project_id == "P1" for t in self.manager.tasks)
        assert len(p1_tasks) == 1
        assert p1_tasks[0].project_id == "P1"

    def test_clear_all_tasks(self):
        self.manager.add_task("T1")
        self.manager.add_task("T2")
        self.manager.clear_all_tasks()
        assert self.manager.count_tasks() == 0

    def test_count_tasks(self):
        self.manager.clear_all_tasks()
        assert self.manager.count_tasks() == 0
        self.manager.add_task("T1")
        assert self.manager.count_tasks() == 1

    def test_get_all_tasks_returns_copy(self):
        self.manager.add_task("T1")
        tasks = self.manager.get_all_tasks()
        assert isinstance(tasks, list)
        assert tasks is not self.manager.tasks
        assert all(isinstance(t, Task) for t in tasks)

    def test_str_and_repr(self):
        s = str(self.manager)
        r = repr(self.manager)
        assert "TaskManager" in s
        assert "tâches" in s
        assert s == r

    def test_get_statistics(self):
        self.manager.clear_all_tasks()
        t1 = self.manager.add_task("T1", priority=Priority.LOW)
        t2 = self.manager.add_task("T2", priority=Priority.HIGH)
        self.manager.update_task_status(t2, Status.DONE)
        stats = self.manager.get_statistics()
        assert stats["total_tasks"] == 2
        assert stats["completed_tasks"] == 1
        assert "tasks_by_priority" in stats
        assert "tasks_by_status" in stats
        assert stats["tasks_by_priority"]["low"] == 1
        assert stats["tasks_by_priority"]["high"] == 1
        assert stats["tasks_by_status"]["done"] == 1

class TestTaskManagerPersistence:
    """Tests de sauvegarde/chargement avec mocks"""

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_to_file_success(self, mock_json_dump, mock_file):
        manager = TaskManager(storage_file="/tmp/test_tasks.json")
        manager.add_task("T1")
        result = manager.save_to_file()
        assert result is True
        mock_file.assert_called_with("/tmp/test_tasks.json", 'w', encoding='utf-8')
        assert mock_json_dump.called

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    @patch('json.load')
    def test_load_from_file_success(self, mock_json_load, mock_file, mock_exists):
        task_dict = Task(title="T1").to_dict()
        mock_json_load.return_value = [task_dict]
        manager = TaskManager(storage_file="/tmp/test_tasks.json")
        result = manager.load_from_file()
        assert result is True
        assert len(manager.tasks) == 1
        assert manager.tasks[0].title == "T1"

    @patch('os.path.exists', return_value=False)
    def test_load_from_file_file_not_found(self, mock_exists):
        manager = TaskManager(storage_file="/tmp/inexistant.json")
        result = manager.load_from_file()
        assert result is True
        assert manager.tasks == []

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump', side_effect=IOError("Erreur IO"))
    def test_save_to_file_ioerror(self, mock_json_dump, mock_file):
        manager = TaskManager(storage_file="/tmp/test_tasks.json")
        manager.add_task("T1")
        result = manager.save_to_file()
        assert result is False

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    @patch('json.load', side_effect=json.JSONDecodeError("err", "", 0))
    def test_load_from_file_json_error(self, mock_json_load, mock_file, mock_exists):
        manager = TaskManager(storage_file="/tmp/test_tasks.json")
        result = manager.load_from_file()
        assert result is False

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    @patch('json.load')
    def test_load_from_file_invalid_task_data(self, mock_json_load, mock_file, mock_exists):
        # Données de tâche invalides (manque le titre qui est requis)
        invalid_task_dict = {"id": "123", "description": "desc", "priority": "high"}
        mock_json_load.return_value = [invalid_task_dict]
        manager = TaskManager(storage_file="/tmp/test_tasks.json")
        result = manager.load_from_file()
        # Le chargement doit réussir même si une tâche est invalide
        assert result is True
        # La tâche invalide doit être ignorée
        assert len(manager.tasks) == 0 