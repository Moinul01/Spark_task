from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import ChatSession, Message
from .serializers import ChatSessionSerializer, MessageSerializer, ChatRequestSerializer
from .services import ChatService

class ChatSessionListView(generics.ListCreateAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ChatSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        chat_session_id = self.kwargs.get('chat_session_id')
        chat_session = get_object_or_404(
            ChatSession, 
            id=chat_session_id, 
            user=self.request.user
        )
        return Message.objects.filter(chat_session=chat_session)

class ChatView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatRequestSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_query = serializer.validated_data['message']
        chat_session_id = serializer.validated_data.get('chat_session_id')
        
        # Get or create chat session
        if chat_session_id:
            chat_session = get_object_or_404(
                ChatSession, 
                id=chat_session_id, 
                user=request.user
            )
        else:
            # Create new chat session with title from first message
            title = user_query[:50] + "..." if len(user_query) > 50 else user_query
            chat_session = ChatSession.objects.create(
                user=request.user,
                title=title
            )
        
        # Get chat history for context (last 10 messages)
        chat_history = Message.objects.filter(
            chat_session=chat_session
        ).order_by('-created_at')[:10]
        
        # Save user message
        user_message = Message.objects.create(
            chat_session=chat_session,
            content=user_query,
            is_user=True
        )
        
        # Generate response using RAG pipeline
        chat_service = ChatService()
        
        try:
            bot_response, metadata = chat_service.generate_response(
                user_query, 
                list(reversed(chat_history))  # Reverse to maintain chronological order
            )
        except Exception as e:
            bot_response = "I apologize, but I encountered an error processing your request. Please try again."
            metadata = {'error': str(e)}
        
        # Save bot response
        bot_message = Message.objects.create(
            chat_session=chat_session,
            content=bot_response,
            is_user=False,
            metadata=metadata
        )
        
        # Update chat session timestamp
        chat_session.save()
        
        return Response({
            'success': True,
            'chat_session': ChatSessionSerializer(chat_session).data,
            'user_message': MessageSerializer(user_message).data,
            'bot_response': MessageSerializer(bot_message).data,
            'chat_session_id': chat_session.id,
            'message': 'Response generated successfully'
        }, status=status.HTTP_201_CREATED)

class ChatHistoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSessionSerializer
    
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)