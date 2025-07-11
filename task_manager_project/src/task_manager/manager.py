import json
import os
from typing import List, Optional, Dict, Any
from .task import Task, Priority, Status


class TaskManager:
    """Gestionnaire principal des tâches"""
    
    def __init__(self, storage_file="tasks.json"):
        """Initialiser le gestionnaire de tâches"""
        self.tasks: List[Task] = []
        self.storage_file = storage_file
    
    def add_task(self, title: str, description: str = "", priority: Priority = Priority.MEDIUM) -> str:
        """Créer et ajouter une nouvelle tâche"""
        task = Task(title=title, description=description, priority=priority)
        self.tasks.append(task)
        return task.id
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Trouver une tâche par son ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_tasks_by_status(self, status: Status) -> List[Task]:
        """Filtrer les tâches par statut"""
        return [task for task in self.tasks if task.status == status]
    
    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        """Filtrer les tâches par priorité"""
        return [task for task in self.tasks if task.priority == priority]
    
    def get_tasks_by_project(self, project_id: str) -> List[Task]:
        """Filtrer les tâches par projet"""
        return [task for task in self.tasks if task.project_id == project_id]
    
    def delete_task(self, task_id: str) -> bool:
        """Supprimer une tâche par son ID"""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                return True
        return False
    
    def update_task_status(self, task_id: str, new_status: Status) -> bool:
        """Mettre à jour le statut d'une tâche"""
        task = self.get_task(task_id)
        if task:
            task.status = new_status
            if new_status == Status.DONE:
                task.mark_completed()
            return True
        return False
    
    def save_to_file(self, filename: Optional[str] = None) -> bool:
        """Sauvegarder toutes les tâches en JSON"""
        file_to_use = filename or self.storage_file
        
        try:
            # Créer le répertoire si nécessaire
            os.makedirs(os.path.dirname(file_to_use), exist_ok=True) if os.path.dirname(file_to_use) else None
            
            # Convertir toutes les tâches en dictionnaires
            tasks_data = [task.to_dict() for task in self.tasks]
            
            # Sauvegarder en JSON
            with open(file_to_use, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except (IOError, OSError, PermissionError) as e:
            print(f"Erreur lors de la sauvegarde : {e}")
            return False
    
    def load_from_file(self, filename: Optional[str] = None) -> bool:
        """Charger les tâches depuis JSON"""
        file_to_use = filename or self.storage_file
        
        try:
            # Vérifier que le fichier existe
            if not os.path.exists(file_to_use):
                print(f"Fichier {file_to_use} introuvable, initialisation d'une liste vide")
                self.tasks = []
                return True
            
            # Charger et parser le JSON
            with open(file_to_use, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
            
            # Recréer les tâches depuis les dictionnaires
            self.tasks = []
            for task_data in tasks_data:
                try:
                    task = Task.from_dict(task_data)
                    self.tasks.append(task)
                except (KeyError, ValueError, TypeError) as e:
                    print(f"Erreur lors du chargement d'une tâche : {e}")
                    continue
            
            return True
            
        except (IOError, OSError, json.JSONDecodeError) as e:
            print(f"Erreur lors du chargement : {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retourner des statistiques sur les tâches"""
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks if t.status == Status.DONE])
        
        # Statistiques par priorité
        tasks_by_priority = {}
        for priority in Priority:
            tasks_by_priority[priority.value] = len([t for t in self.tasks if t.priority == priority])
        
        # Statistiques par statut
        tasks_by_status = {}
        for status in Status:
            tasks_by_status[status.value] = len([t for t in self.tasks if t.status == status])
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            'tasks_by_priority': tasks_by_priority,
            'tasks_by_status': tasks_by_status,
        }
    
    def get_all_tasks(self) -> List[Task]:
        """Retourner toutes les tâches"""
        return self.tasks.copy()
    
    def clear_all_tasks(self) -> None:
        """Supprimer toutes les tâches"""
        self.tasks.clear()
    
    def count_tasks(self) -> int:
        """Retourner le nombre total de tâches"""
        return len(self.tasks)
    
    def __str__(self) -> str:
        """Représentation en chaîne de caractères"""
        return f"TaskManager({len(self.tasks)} tâches, fichier: {self.storage_file})"
    
    def __repr__(self) -> str:
        """Représentation pour le debugging"""
        return self.__str__() 