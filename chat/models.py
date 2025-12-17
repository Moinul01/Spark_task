from django.db import models
from django.conf import settings

class ChatSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_sessions')
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title or 'Untitled'}"
    
    def save(self, *args, **kwargs):
        # Generate title from first message if empty
        if not self.title and self.pk:
            first_message = self.messages.filter(is_user=True).first()
            if first_message:
                content = first_message.content
                self.title = content[:50] + '...' if len(content) > 50 else content
        super().save(*args, **kwargs)

class Message(models.Model):
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    is_user = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)  # Store RAG context, citations, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        role = "User" if self.is_user else "Bot"
        return f"{role}: {self.content[:50]}..."