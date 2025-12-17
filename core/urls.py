from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

def home_view(request):
    return HttpResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>🤖 AI Chatbot API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
                .container { max-width: 900px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 40px; border-radius: 20px; backdrop-filter: blur(10px); }
                h1 { font-size: 2.5em; margin-bottom: 20px; }
                .api-list { background: rgba(255,255,255,0.15); padding: 30px; border-radius: 15px; margin: 30px 0; }
                .endpoint { margin: 15px 0; padding: 15px; background: rgba(255,255,255,0.2); border-radius: 10px; display: flex; align-items: center; }
                .method { padding: 5px 12px; border-radius: 6px; font-weight: bold; margin-right: 15px; min-width: 70px; text-align: center; }
                .post { background: #10b981; }
                .get { background: #3b82f6; }
                .put { background: #f59e0b; }
                .delete { background: #ef4444; }
                a { color: #93c5fd; text-decoration: none; font-weight: bold; }
                a:hover { text-decoration: underline; }
                .feature { display: flex; align-items: center; margin: 20px 0; }
                .feature-icon { font-size: 24px; margin-right: 15px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 AI Chatbot Backend API</h1>
                <p>RAG-powered chatbot with JWT authentication, chat history, and background tasks</p>
                
                <div class="feature">
                    <div class="feature-icon">🔐</div>
                    <div><strong>JWT Authentication</strong> - Secure user authentication with email verification</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">🧠</div>
                    <div><strong>RAG Pipeline</strong> - Retrieval-Augmented Generation with FAISS vector search</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">💾</div>
                    <div><strong>Chat History</strong> - Persistent storage of all conversations</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">⚡</div>
                    <div><strong>Background Tasks</strong> - Automatic cleanup and email notifications</div>
                </div>
                
                <div class="api-list">
                    <h2>📡 API Endpoints</h2>
                    
                    <div class="endpoint">
                        <span class="method post">POST</span>
                        <div>
                            <strong>/api/users/signup/</strong> - Register new user<br>
                            <small>Body: {"username": "...", "email": "...", "password": "...", "password2": "..."}</small>
                        </div>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method post">POST</span>
                        <div>
                            <strong>/api/users/login/</strong> - Login & get JWT tokens<br>
                            <small>Body: {"email": "...", "password": "..."}</small>
                        </div>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method get">GET</span>
                        <div>
                            <strong>/api/chat/history/</strong> - Get all chat sessions<br>
                            <small>Headers: Authorization: Bearer &lt;token&gt;</small>
                        </div>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method post">POST</span>
                        <div>
                            <strong>/api/chat/send/</strong> - Send message to chatbot<br>
                            <small>Body: {"message": "...", "chat_session_id": "optional"}</small>
                        </div>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method get">GET</span>
                        <div>
                            <strong><a href="/admin/">/admin/</a></strong> - Django Admin Panel
                        </div>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method get">GET</span>
                        <div>
                            <strong><a href="/swagger/">/swagger/</a></strong> - Interactive API Documentation
                        </div>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method get">GET</span>
                        <div>
                            <strong><a href="/redoc/">/redoc/</a></strong> - Alternative API Docs
                        </div>
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.3);">
                    <p>🚀 Built with Django REST Framework, OpenAI GPT, FAISS, Celery, and JWT</p>
                </div>
            </div>
        </body>
        </html>
    """)

# Swagger documentation
schema_view = get_schema_view(
    openapi.Info(
        title="AI Chatbot API",
        default_version='v1',
        description="RAG-powered chatbot with authentication and background tasks",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@chatbot.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API Endpoints
    path('api/users/', include('users.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/knowledge/', include('knowledge.urls')),
]