import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'cleanup-old-chats-every-day': {
        'task': 'chat.tasks.cleanup_old_chats',
        'schedule': 86400.0,  # Every 24 hours
    },
    'send-daily-stats': {
        'task': 'chat.tasks.send_daily_stats',
        'schedule': 86400.0,  # Every 24 hours
    },
}