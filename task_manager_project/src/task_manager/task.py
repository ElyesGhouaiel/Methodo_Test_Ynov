from datetime import datetime
from enum import Enum
import time
import uuid


class Priority(Enum):
    """Niveaux de priorité des tâches"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Status(Enum):
    """Statuts possibles des tâches"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"


class Task:
    """Une tâche avec toutes ses propriétés"""
    
    def __init__(self, title, description="", priority=Priority.MEDIUM):
        # Validation des paramètres
        if not title or not title.strip():
            raise ValueError("Le titre de la tâche ne peut pas être vide")
        
        if not isinstance(priority, Priority):
            raise TypeError("La priorité doit être une instance de Priority")
        
        # Initialisation des attributs
        self.id = str(uuid.uuid4())  # ID unique garanti
        self.title = title.strip()
        self.description = description
        self.priority = priority
        self.status = Status.TODO
        self.created_at = datetime.now()
        self.completed_at = None
        self.project_id = None
    
    def mark_completed(self):
        """Marquer la tâche comme terminée"""
        self.status = Status.DONE
        self.completed_at = datetime.now()
    
    def update_priority(self, new_priority):
        """Mettre à jour la priorité de la tâche"""
        if not isinstance(new_priority, Priority):
            raise TypeError("La nouvelle priorité doit être une instance de Priority")
        self.priority = new_priority
    
    def assign_to_project(self, project_id):
        """Assigner la tâche à un projet"""
        self.project_id = project_id
    
    def to_dict(self):
        """Convertir la tâche en dictionnaire pour sérialisation JSON"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority.value,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'project_id': self.project_id
        }
    
    @classmethod
    def from_dict(cls, data):
        """Créer une tâche depuis un dictionnaire"""
        # Créer la tâche avec les paramètres de base
        task = cls(
            title=data['title'],
            description=data.get('description', ''),
            priority=Priority(data['priority'])
        )
        
        # Restaurer les autres attributs
        task.id = data['id']
        task.status = Status(data['status'])
        task.created_at = datetime.fromisoformat(data['created_at'])
        
        if data.get('completed_at'):
            task.completed_at = datetime.fromisoformat(data['completed_at'])
        
        task.project_id = data.get('project_id')
        
        return task
    
    def __str__(self):
        """Représentation en chaîne de caractères"""
        return f"Task(id={self.id}, title='{self.title}', status={self.status.value}, priority={self.priority.value})"
    
    def __repr__(self):
        """Représentation pour le debugging"""
        return self.__str__() 