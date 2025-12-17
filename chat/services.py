import openai
from django.conf import settings
from .rag_pipeline import RAGPipeline

openai.api_key = settings.OPENAI_API_KEY

class ChatService:
    def __init__(self):
        self.rag_pipeline = RAGPipeline()
    
    def generate_response(self, user_query, chat_history=None):
        """
        Generate response using RAG pipeline
        """
        # Retrieve relevant documents
        retrieved_docs = self.rag_pipeline.retrieve(user_query)
        
        # Format context from retrieved documents
        context = self._format_context(retrieved_docs)
        
        # Prepare messages for OpenAI
        messages = self._prepare_messages(user_query, context, chat_history)
        
        # Generate response
        response = self._call_openai(messages)
        
        # Extract and store metadata
        metadata = {
            'retrieved_docs': [{'content': doc.page_content[:200] + '...', **doc.metadata} for doc in retrieved_docs],
            'context_used': bool(retrieved_docs),
            'model': 'gpt-3.5-turbo',
        }
        
        return response, metadata
    
    def _format_context(self, retrieved_docs):
        """Format retrieved documents into context string"""
        if not retrieved_docs:
            return "No relevant documents found in the knowledge base."
        
        context_parts = ["Relevant information from knowledge base:"]
        for i, doc in enumerate(retrieved_docs, 1):
            source = doc.metadata.get('source', 'Unknown')
            title = doc.metadata.get('title', 'Untitled')
            content = doc.page_content[:500]  # Limit context length
            context_parts.append(f"[Document {i} - {title} ({source})]:\n{content}")
        
        return "\n\n".join(context_parts)
    
    def _prepare_messages(self, user_query, context, chat_history=None):
        """Prepare messages for OpenAI API"""
        system_prompt = f"""You are a helpful AI assistant for a chatbot service. Use the following context to answer the user's question when relevant.

        {context}

        Guidelines:
        1. If the context contains relevant information, use it to formulate your answer.
        2. If the context doesn't contain relevant information, acknowledge this and provide a helpful answer based on your general knowledge.
        3. When using information from the context, you can mention that it's based on available documentation.
        4. Be concise, accurate, and helpful.
        5. If the user asks about something outside the context, say you don't have specific information but try to help generally.
        6. Format your responses in a readable way with paragraphs when appropriate."""
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add chat history if available
        if chat_history:
            for msg in chat_history:
                role = "user" if msg.is_user else "assistant"
                messages.append({"role": role, "content": msg.content})
        
        # Add current query
        messages.append({"role": "user", "content": user_query})
        
        return messages
    
    def _call_openai(self, messages):
        """Call OpenAI API"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1
            )
            return response.choices[0].message.content.strip()
        except openai.error.RateLimitError:
            return "I'm currently experiencing high demand. Please try again in a moment."
        except openai.error.AuthenticationError:
            return "Authentication error with AI service. Please contact support."
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)[:100]}"