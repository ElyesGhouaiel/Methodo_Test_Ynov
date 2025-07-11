#!/usr/bin/env python3
"""
Démonstration du module TaskManager
"""
from src.task_manager.manager import TaskManager
from src.task_manager.task import Priority, Status
from src.task_manager.services import EmailService

def main():
    print("=== Démonstration TaskManager ===\n")
    
    # Création du gestionnaire
    manager = TaskManager("demo_tasks.json")
    print("✅ Gestionnaire créé\n")
    
    # Ajout de tâches avec différentes priorités
    task1_id = manager.add_task("Implémenter la CI/CD", "Mettre en place GitHub Actions", Priority.HIGH)
    print(f"✅ Tâche 1 créée (ID: {task1_id})")
    
    task2_id = manager.add_task("Écrire les tests", "Atteindre 95% de couverture", Priority.HIGH)
    print(f"✅ Tâche 2 créée (ID: {task2_id})")
    
    task3_id = manager.add_task("Documenter l'API", "Générer la documentation", Priority.MEDIUM)
    print(f"✅ Tâche 3 créée (ID: {task3_id})")
    
    task4_id = manager.add_task("Refactoring", "Optimiser le code", Priority.LOW)
    print(f"✅ Tâche 4 créée (ID: {task4_id})\n")
    
    # Marquer certaines tâches comme terminées
    manager.get_task(task1_id).mark_completed()
    manager.get_task(task2_id).mark_completed()
    print("✅ 2 tâches marquées comme terminées\n")
    
    # Afficher les statistiques
    stats = manager.get_statistics()
    print("📊 Statistiques :")
    print(f"- Total des tâches : {stats['total']}")
    print(f"- Tâches terminées : {stats['completed']}")
    print(f"- Tâches en cours : {stats['in_progress']}")
    print(f"- Priorité haute : {stats['by_priority']['HIGH']}")
    print(f"- Priorité moyenne : {stats['by_priority']['MEDIUM']}")
    print(f"- Priorité basse : {stats['by_priority']['LOW']}\n")
    
    # Sauvegarder dans un fichier
    manager.save_to_file()
    print("✅ Tâches sauvegardées dans demo_tasks.json\n")
    
    # Recharger et vérifier
    new_manager = TaskManager("demo_tasks.json")
    new_manager.load_from_file()
    print("✅ Tâches rechargées avec succès")
    print(f"✅ Nombre de tâches après rechargement : {len(new_manager.get_all_tasks())}\n")
    
    # Démonstration du service d'email
    email_service = EmailService()
    try:
        email_service.send_task_reminder("demo@example.com", manager.get_task(task3_id))
        print("✅ Email de rappel envoyé pour la tâche 3\n")
    except Exception as e:
        print(f"ℹ️ Simulation d'envoi d'email (désactivé en démo) : {e}\n")
    
    print("🎉 Démo terminée avec succès !")

if __name__ == "__main__":
    main() 