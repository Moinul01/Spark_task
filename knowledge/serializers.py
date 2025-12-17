from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'content', 'source', 'document_type', 'is_active', 'uploaded_at', 'updated_at']
        read_only_fields = ['id', 'uploaded_at', 'updated_at']
    
    def validate_content(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Content must be at least 10 characters long.")
        return value.strip()