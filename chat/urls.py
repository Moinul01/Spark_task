from django.urls import path
from .views import (
    ChatSessionListView, 
    ChatSessionDetailView, 
    MessageListView,
    ChatView, 
    ChatHistoryView
)

urlpatterns = [
    path('sessions/', ChatSessionListView.as_view(), name='chat-sessions'),
    path('sessions/<int:pk>/', ChatSessionDetailView.as_view(), name='chat-session-detail'),
    path('sessions/<int:chat_session_id>/messages/', MessageListView.as_view(), name='chat-messages'),
    path('send/', ChatView.as_view(), name='chat-send'),
    path('history/', ChatHistoryView.as_view(), name='chat-history'),
]