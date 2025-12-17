from django.urls import path
from .views import DocumentListView, DocumentDetailView, KnowledgeBaseStatsView

urlpatterns = [
    path('documents/', DocumentListView.as_view(), name='document-list'),
    path('documents/<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),
    path('stats/', KnowledgeBaseStatsView.as_view(), name='knowledge-stats'),
]