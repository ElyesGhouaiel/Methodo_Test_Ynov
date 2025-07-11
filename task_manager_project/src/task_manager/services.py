import smtplib
import csv
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from email.message import Message
from .task import Task, Priority, Status


class EmailService:
    """Service d'envoi d'emails (à mocker dans les tests)"""
    
    def __init__(self, smtp_server: str = "smtp.gmail.com", port: int = 587):
        """Initialiser le service email"""
        self.smtp_server = smtp_server
        self.port = port
    
    def _validate_email(self, email: str) -> bool:
        """Valider le format d'un email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def send_task_reminder(self, email: str, task_title: str, due_date: Optional[datetime] = None) -> bool:
        """Simuler l'envoi d'un email de rappel"""
        # Validation de l'email
        if not self._validate_email(email):
            raise ValueError(f"Email invalide : {email}")
        
        # Validation des paramètres
        if not task_title or not task_title.strip():
            raise ValueError("Le titre de la tâche ne peut pas être vide")
        
        try:
            # Créer le message
            subject = f"Rappel : {task_title}"
            due_text = f" (échéance : {due_date.strftime('%d/%m/%Y')})" if due_date else ""
            body = f"N'oubliez pas votre tâche : {task_title}{due_text}"
            
            # Créer l'objet Message
            msg = Message()
            msg.set_payload(body)
            msg["Subject"] = subject
            msg["From"] = "noreply@taskmanager.com"
            msg["To"] = email
            
            # Simuler la connexion SMTP
            smtp = smtplib.SMTP(self.smtp_server, self.port)
            smtp.send_message(msg)
            smtp.quit()
            
            # Log pour simulation
            print(f"[EMAIL] Envoi à {email} - Sujet: {subject}")
            print(f"[EMAIL] Corps: {body}")
            
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email : {e}")
            return False
    
    def send_completion_notification(self, email: str, task_title: str) -> bool:
        """Simuler l'envoi d'un email de confirmation de tâche terminée"""
        # Validation de l'email
        if not self._validate_email(email):
            raise ValueError(f"Email invalide : {email}")
        
        # Validation des paramètres
        if not task_title or not task_title.strip():
            raise ValueError("Le titre de la tâche ne peut pas être vide")
        
        try:
            # Simuler l'envoi
            subject = f"Tâche terminée : {task_title}"
            body = f"Félicitations ! Vous avez terminé la tâche : {task_title}"
            
            # Créer l'objet Message
            msg = Message()
            msg.set_payload(body)
            msg["Subject"] = subject
            msg["From"] = "noreply@taskmanager.com"
            msg["To"] = email
            
            # Simuler la connexion SMTP
            smtp = smtplib.SMTP(self.smtp_server, self.port)
            smtp.send_message(msg)
            smtp.quit()
            
            # Log pour simulation
            print(f"[EMAIL] Notification de completion à {email}")
            print(f"[EMAIL] Sujet: {subject}")
            print(f"[EMAIL] Corps: {body}")
            
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'envoi de la notification : {e}")
            return False
    
    def send_daily_summary(self, email: str, completed_tasks: int, pending_tasks: int) -> bool:
        """Simuler l'envoi d'un résumé quotidien"""
        if not self._validate_email(email):
            raise ValueError(f"Email invalide : {email}")
        
        try:
            subject = "Résumé quotidien de vos tâches"
            body = f"""Bonjour,

Voici votre résumé quotidien :
- Tâches terminées aujourd'hui : {completed_tasks}
- Tâches en attente : {pending_tasks}

Bonne journée !"""
            
            # Créer l'objet Message
            msg = Message()
            msg.set_payload(body)
            msg["Subject"] = subject
            msg["From"] = "noreply@taskmanager.com"
            msg["To"] = email
            
            # Simuler la connexion SMTP
            smtp = smtplib.SMTP(self.smtp_server, self.port)
            smtp.send_message(msg)
            smtp.quit()
            
            print(f"[EMAIL] Résumé quotidien envoyé à {email}")
            print(f"[EMAIL] {completed_tasks} terminées, {pending_tasks} en attente")
            
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'envoi du résumé : {e}")
            return False


class ReportService:
    """Service de génération de rapports"""
    
    def generate_daily_report(self, tasks: List[Task], date: Optional[datetime] = None) -> Dict[str, Any]:
        """Générer un rapport quotidien"""
        target_date = date or datetime.now()
        
        # Filtrer les tâches du jour (créées ou terminées)
        daily_tasks = []
        completed_today = []
        
        for task in tasks:
            # Tâches créées aujourd'hui
            if task.created_at.date() == target_date.date():
                daily_tasks.append(task)
            
            # Tâches terminées aujourd'hui
            if (task.completed_at and 
                task.completed_at.date() == target_date.date()):
                completed_today.append(task)
        
        # Calcul des métriques
        report = {
            'date': target_date.strftime('%Y-%m-%d'),
            'total_tasks_created': len(daily_tasks),
            'total_tasks_completed': len(completed_today),
            'tasks_by_priority': {
                priority.value: len([t for t in daily_tasks if t.priority == priority])
                for priority in Priority
            },
            'completion_rate': (len(completed_today) / len(daily_tasks) * 100) if daily_tasks else 0,
            'summary': {
                'most_common_priority': self._get_most_common_priority(daily_tasks),
                'average_completion_time': self._calculate_avg_completion_time(completed_today),
                'pending_urgent_tasks': len([t for t in tasks if t.priority == Priority.URGENT and t.status != Status.DONE])
            }
        }
        
        return report
    
    def _get_most_common_priority(self, tasks: List[Task]) -> str:
        """Trouver la priorité la plus commune"""
        if not tasks:
            return "N/A"
        
        priority_counts = {}
        for task in tasks:
            priority_counts[task.priority.value] = priority_counts.get(task.priority.value, 0) + 1
        
        # Utiliser une fonction lambda pour comparer les valeurs
        return max(priority_counts.items(), key=lambda x: x[1])[0] if priority_counts else "N/A"
    
    def _calculate_avg_completion_time(self, completed_tasks: List[Task]) -> Optional[float]:
        """Calculer le temps moyen de completion en heures"""
        if not completed_tasks:
            return None
        
        total_hours = 0
        valid_tasks = 0
        
        for task in completed_tasks:
            if task.completed_at and task.created_at:
                duration = task.completed_at - task.created_at
                total_hours += duration.total_seconds() / 3600
                valid_tasks += 1
        
        return total_hours / valid_tasks if valid_tasks > 0 else None
    
    def export_tasks_csv(self, tasks: List[Task], filename: str) -> bool:
        """Exporter les tâches vers un fichier CSV"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # En-têtes
                headers = [
                    'ID', 'Titre', 'Description', 'Priorité', 'Statut',
                    'Date_Création', 'Date_Completion', 'Projet_ID'
                ]
                writer.writerow(headers)
                
                # Données des tâches
                for task in tasks:
                    row = [
                        task.id,
                        task.title,
                        task.description,
                        task.priority.value,
                        task.status.value,
                        task.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        task.completed_at.strftime('%Y-%m-%d %H:%M:%S') if task.completed_at else '',
                        task.project_id or ''
                    ]
                    writer.writerow(row)
            
            print(f"Export CSV réussi : {filename}")
            return True
            
        except (IOError, OSError, PermissionError) as e:
            print(f"Erreur lors de l'export CSV : {e}")
            return False
    
    def generate_weekly_report(self, tasks: List[Task], start_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Générer un rapport hebdomadaire"""
        if start_date is None:
            start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Calculer la période de 7 jours
        end_date = start_date.replace(hour=23, minute=59, second=59)
        
        weekly_tasks = [
            task for task in tasks
            if start_date <= task.created_at <= end_date
        ]
        
        completed_this_week = [
            task for task in tasks
            if (task.completed_at and start_date <= task.completed_at <= end_date)
        ]
        
        return {
            'period': f"{start_date.strftime('%Y-%m-%d')} au {end_date.strftime('%Y-%m-%d')}",
            'tasks_created': len(weekly_tasks),
            'tasks_completed': len(completed_this_week),
            'productivity_score': (len(completed_this_week) / len(weekly_tasks) * 100) if weekly_tasks else 0,
            'top_priority': self._get_most_common_priority(weekly_tasks)
        } 