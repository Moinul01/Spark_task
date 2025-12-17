from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    source = models.CharField(max_length=200, blank=True)
    document_type = models.CharField(max_length=50, choices=[
        ('faq', 'FAQ'),
        ('article', 'Article'),
        ('manual', 'Manual'),
        ('knowledge_base', 'Knowledge Base'),
        ('other', 'Other')
    ], default='article')
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-extract title from content if not provided
        if not self.title and self.content:
            self.title = self.content[:100].strip()
            if len(self.content) > 100:
                self.title += '...'
        super().save(*args, **kwargs)