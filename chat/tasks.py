from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import ChatSession, Message

@shared_task
def cleanup_old_chats():
    """
    Delete chat sessions older than 30 days
    """
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    try:
        # Delete messages first (due to foreign key constraints)
        old_messages = Message.objects.filter(
            created_at__lt=thirty_days_ago
        )
        message_count = old_messages.count()
        old_messages.delete()
        
        # Delete old chat sessions (those with no messages or all messages deleted)
        old_sessions = ChatSession.objects.filter(
            updated_at__lt=thirty_days_ago
        )
        session_count = old_sessions.count()
        old_sessions.delete()
        
        return {
            'task': 'cleanup_old_chats',
            'status': 'success',
            'deleted_sessions': session_count,
            'deleted_messages': message_count,
            'timestamp': timezone.now().isoformat()
        }
    except Exception as e:
        return {
            'task': 'cleanup_old_chats',
            'status': 'error',
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }

@shared_task
def send_daily_stats():
    """
    Send daily statistics email to admin
    """
    try:
        # Calculate statistics
        total_users = settings.AUTH_USER_MODEL.objects.count()
        total_sessions = ChatSession.objects.count()
        total_messages = Message.objects.count()
        active_sessions_today = ChatSession.objects.filter(
            updated_at__gte=timezone.now() - timedelta(days=1)
        ).count()
        
        subject = 'Daily Chatbot Statistics'
        message = f"""
        Daily Statistics Report:
        
        Total Users: {total_users}
        Total Chat Sessions: {total_sessions}
        Total Messages: {total_messages}
        Active Sessions (Last 24h): {active_sessions_today}
        
        Report generated at: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],  # Send to admin
            fail_silently=True,
        )
        
        return {
            'task': 'send_daily_stats',
            'status': 'success',
            'timestamp': timezone.now().isoformat()
        }
    except Exception as e:
        return {
            'task': 'send_daily_stats',
            'status': 'error',
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }