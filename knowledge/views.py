from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Document
from .serializers import DocumentSerializer
from chat.rag_pipeline import RAGPipeline

class DocumentListView(generics.ListCreateAPIView):
    queryset = Document.objects.filter(is_active=True)
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admins can manage knowledge base
    
    def perform_create(self, serializer):
        document = serializer.save()
        
        # Update RAG knowledge base
        rag_pipeline = RAGPipeline()
        rag_pipeline.update_knowledge_base([{
            'title': document.title,
            'content': document.content,
            'source': document.source,
            'type': document.document_type
        }])

class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAdminUser]

class KnowledgeBaseStatsView(APIView):
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        rag_pipeline = RAGPipeline()
        stats = rag_pipeline.get_stats()
        
        return Response({
            'database_stats': {
                'total_documents': Document.objects.count(),
                'active_documents': Document.objects.filter(is_active=True).count(),
            },
            'vector_store_stats': stats,
        })