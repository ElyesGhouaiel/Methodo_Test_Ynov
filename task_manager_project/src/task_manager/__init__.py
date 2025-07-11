"""
Module de gestion de tâches TaskManager
"""

__version__ = "1.0.0"

from .task import Task, Priority, Status
from .manager import TaskManager
from .services import EmailService, ReportService

__all__ = [
    'Task', 'Priority', 'Status',
    'TaskManager', 
    'EmailService', 'ReportService'
] 