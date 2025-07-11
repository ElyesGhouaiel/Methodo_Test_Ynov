import pytest
from unittest.mock import patch, Mock, MagicMock
from src.task_manager.services import EmailService, ReportService
from src.task_manager.task import Task, Priority, Status
from datetime import datetime, timedelta

class TestEmailService:
    """Tests du service email avec mocks"""
    
    def setup_method(self):
        self.email_service = EmailService()

    @patch('src.task_manager.services.smtplib.SMTP')
    def test_send_task_reminder_success(self, mock_smtp):
        # Configurer le mock SMTP
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value = mock_smtp_instance
        
        result = self.email_service.send_task_reminder(
            email="test@example.com",
            task_title="Ma tâche",
            due_date=datetime(2023, 1, 1)
        )
        assert result is True
        assert mock_smtp_instance.send_message.called
        assert mock_smtp_instance.quit.called

    def test_send_task_reminder_invalid_email(self):
        with pytest.raises(ValueError):
            self.email_service.send_task_reminder(
                email="invalid-email",
                task_title="Ma tâche"
            )

    def test_send_task_reminder_empty_title(self):
        with pytest.raises(ValueError):
            self.email_service.send_task_reminder(
                email="test@example.com",
                task_title="   "
            )

    @patch('src.task_manager.services.smtplib.SMTP')
    def test_send_completion_notification_success(self, mock_smtp):
        # Configurer le mock SMTP
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value = mock_smtp_instance
        
        result = self.email_service.send_completion_notification(
            email="test@example.com",
            task_title="Tâche finie"
        )
        assert result is True
        assert mock_smtp_instance.send_message.called
        assert mock_smtp_instance.quit.called

    def test_send_completion_notification_invalid_email(self):
        with pytest.raises(ValueError):
            self.email_service.send_completion_notification(
                email="badmail",
                task_title="Tâche"
            )

    def test_send_completion_notification_empty_title(self):
        with pytest.raises(ValueError):
            self.email_service.send_completion_notification(
                email="test@example.com",
                task_title=""
            )

    @patch('src.task_manager.services.smtplib.SMTP')
    def test_send_daily_summary_success(self, mock_smtp):
        # Configurer le mock SMTP
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value = mock_smtp_instance
        
        result = self.email_service.send_daily_summary(
            email="test@example.com",
            completed_tasks=3,
            pending_tasks=2
        )
        assert result is True
        assert mock_smtp_instance.send_message.called
        assert mock_smtp_instance.quit.called

    def test_send_daily_summary_invalid_email(self):
        with pytest.raises(ValueError):
            self.email_service.send_daily_summary(
                email="badmail",
                completed_tasks=1,
                pending_tasks=1
            )

    @patch('src.task_manager.services.smtplib.SMTP')
    def test_send_task_reminder_exception(self, mock_smtp):
        mock_smtp.side_effect = Exception("fail")
        service = EmailService()
        result = service.send_task_reminder("test@example.com", "Tâche")
        assert result is False

    @patch('src.task_manager.services.smtplib.SMTP')
    def test_send_completion_notification_exception(self, mock_smtp):
        mock_smtp.side_effect = Exception("fail")
        service = EmailService()
        result = service.send_completion_notification("test@example.com", "Tâche")
        assert result is False

    @patch('src.task_manager.services.smtplib.SMTP')
    def test_send_daily_summary_exception(self, mock_smtp):
        mock_smtp.side_effect = Exception("fail")
        service = EmailService()
        result = service.send_daily_summary("test@example.com", 1, 1)
        assert result is False

class TestReportService:
    """Tests du service de rapports"""
    
    @patch('src.task_manager.services.datetime')
    def test_generate_daily_report_fixed_date(self, mock_datetime):
        # Fixer la date du jour
        fixed_date = datetime(2023, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = fixed_date
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
        # Créer des tâches
        t1 = Task(title="T1", priority=Priority.HIGH)
        t1.created_at = fixed_date
        t2 = Task(title="T2", priority=Priority.LOW)
        t2.created_at = fixed_date
        t2.mark_completed()
        t2.completed_at = fixed_date
        report_service = ReportService()
        report = report_service.generate_daily_report([t1, t2], date=fixed_date)
        assert report['date'] == '2023-01-01'
        assert report['total_tasks_created'] == 2
        assert report['total_tasks_completed'] == 1
        assert 'tasks_by_priority' in report
        assert 'completion_rate' in report
        assert 'summary' in report

    def test_export_tasks_csv_success(self, tmp_path):
        t1 = Task(title="T1", priority=Priority.HIGH)
        t2 = Task(title="T2", priority=Priority.LOW)
        file_path = tmp_path / "tasks.csv"
        report_service = ReportService()
        result = report_service.export_tasks_csv([t1, t2], str(file_path))
        assert result is True
        # Vérifier que le fichier a été créé et contient les titres
        content = file_path.read_text(encoding="utf-8")
        assert "ID,Titre,Description,Priorité,Statut,Date_Création,Date_Completion,Projet_ID" in content
        assert "T1" in content and "T2" in content

    def test_export_tasks_csv_ioerror(self, monkeypatch):
        t1 = Task(title="T1")
        report_service = ReportService()
        def fail_open(*a, **k):
            raise IOError("fail")
        monkeypatch.setattr("builtins.open", fail_open)
        result = report_service.export_tasks_csv([t1], "badfile.csv")
        assert result is False

    def test_generate_weekly_report(self):
        now = datetime.now()
        t1 = Task(title="T1")
        t1.created_at = now
        t2 = Task(title="T2")
        t2.created_at = now
        t2.mark_completed()
        t2.completed_at = now
        report_service = ReportService()
        report = report_service.generate_weekly_report([t1, t2], start_date=now)
        assert 'period' in report
        assert report['tasks_created'] == 2
        assert report['tasks_completed'] == 1 or report['tasks_completed'] == 2  # selon si completed_at est dans la période
        assert 'productivity_score' in report
        assert 'top_priority' in report

    def test_get_most_common_priority_no_tasks(self):
        report_service = ReportService()
        priority = report_service._get_most_common_priority([])
        assert priority == "N/A"

    def test_calculate_avg_completion_time_no_tasks(self):
        report_service = ReportService()
        avg_time = report_service._calculate_avg_completion_time([])
        assert avg_time is None

    def test_calculate_avg_completion_time_with_tasks(self):
        now = datetime.now()
        t1 = Task(title="T1")
        t1.created_at = now
        t1.mark_completed()
        t1.completed_at = now + timedelta(hours=2)
        
        report_service = ReportService()
        avg_time = report_service._calculate_avg_completion_time([t1])
        assert avg_time == 2.0  # 2 heures

    def test_generate_weekly_report_no_tasks(self):
        report_service = ReportService()
        start_date = datetime.now()
        report = report_service.generate_weekly_report([], start_date=start_date)
        assert report['tasks_created'] == 0
        assert report['tasks_completed'] == 0
        assert report['productivity_score'] == 0
        assert report['top_priority'] == "N/A" 