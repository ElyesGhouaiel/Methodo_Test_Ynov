import pytest
from datetime import datetime, timedelta
from src.task_manager.task import Task, Priority, Status
import uuid

class TestTaskCreation:
    """Tests de création de tâches"""
    
    def test_create_task_minimal(self):
        t = Task(title="Test minimal")
        assert t.title == "Test minimal"
        assert t.description == ""
        assert t.priority == Priority.MEDIUM
        assert t.status == Status.TODO
        assert isinstance(t.created_at, datetime)
        assert t.completed_at is None
        assert t.project_id is None
        assert isinstance(t.id, str)
        assert isinstance(uuid.UUID(t.id), uuid.UUID)

    def test_create_task_complete(self):
        t = Task(title="Tâche complète", description="Desc", priority=Priority.HIGH)
        assert t.title == "Tâche complète"
        assert t.description == "Desc"
        assert t.priority == Priority.HIGH
        assert t.status == Status.TODO
        assert isinstance(t.created_at, datetime)
        assert t.completed_at is None
        assert t.project_id is None
        assert isinstance(t.id, str)

    def test_create_task_empty_title_raises_error(self):
        with pytest.raises(ValueError):
            Task(title="   ")
        with pytest.raises(ValueError):
            Task(title="")
        with pytest.raises(ValueError):
            Task(title=None)

    def test_create_task_invalid_priority(self):
        with pytest.raises(TypeError):
            Task(title="Test", priority="high")  # string au lieu de Priority.HIGH
        with pytest.raises(TypeError):
            Task(title="Test", priority=None)
        with pytest.raises(TypeError):
            Task(title="Test", priority=123)

    def test_task_repr(self):
        t = Task(title="Repr test")
        assert repr(t) == str(t)

class TestTaskOperations:
    """Tests des opérations sur les tâches"""
    
    def setup_method(self):
        self.task = Task(title="Opérations")
    
    def test_mark_completed_changes_status(self):
        assert self.task.status == Status.TODO
        assert self.task.completed_at is None
        self.task.mark_completed()
        assert self.task.status == Status.DONE
        assert isinstance(self.task.completed_at, datetime)
        assert self.task.completed_at >= self.task.created_at

    def test_update_priority_valid(self):
        self.task.update_priority(Priority.LOW)
        assert self.task.priority == Priority.LOW
        self.task.update_priority(Priority.URGENT)
        assert self.task.priority == Priority.URGENT

    def test_update_priority_invalid_type(self):
        with pytest.raises(TypeError):
            self.task.update_priority("HIGH")
        with pytest.raises(TypeError):
            self.task.update_priority(123)
        with pytest.raises(TypeError):
            self.task.update_priority(None)
        with pytest.raises(TypeError):
            self.task.update_priority(object())

    def test_assign_to_project(self):
        self.task.assign_to_project("PROJ-42")
        assert self.task.project_id == "PROJ-42"
        self.task.assign_to_project(None)
        assert self.task.project_id is None

class TestTaskSerialization:
    """Tests de sérialisation JSON"""
    
    def setup_method(self):
        self.task = Task(title="Sérialisation", description="Desc", priority=Priority.HIGH)
        self.task.assign_to_project("P1")
        self.task.mark_completed()
        self.task.created_at = datetime(2023, 1, 1, 12, 0, 0)
        self.task.completed_at = self.task.created_at + timedelta(hours=2)

    def test_to_dict_contains_all_fields(self):
        d = self.task.to_dict()
        assert set(d.keys()) == {"id", "title", "description", "priority", "status", "created_at", "completed_at", "project_id"}
        assert d["title"] == "Sérialisation"
        assert d["description"] == "Desc"
        assert d["priority"] == "high"
        assert d["status"] == "done"
        assert isinstance(d["created_at"], str)
        assert isinstance(d["completed_at"], str)
        assert d["project_id"] == "P1"

    def test_from_dict_recreates_task(self):
        d = self.task.to_dict()
        t2 = Task.from_dict(d)
        assert t2.id == self.task.id
        assert t2.title == self.task.title
        assert t2.description == self.task.description
        assert t2.priority == self.task.priority
        assert t2.status == self.task.status
        assert t2.created_at == self.task.created_at
        assert t2.completed_at == self.task.completed_at
        assert t2.project_id == self.task.project_id 