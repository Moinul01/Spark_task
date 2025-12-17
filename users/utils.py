import uuid
from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(user):
    """
    Send verification email to user
    """
    token = str(uuid.uuid4())
    user.verification_token = token
    user.save()
    
    verification_url = f"{settings.FRONTEND_URL}/verify-email/{token}"
    
    subject = 'Verify Your Email - AI Chatbot'
    message = f"""
    Hi {user.username},
    
    Welcome to AI Chatbot! Please verify your email address by clicking the link below:
    
    {verification_url}
    
    This link will expire in 24 hours.
    
    If you didn't create an account with us, please ignore this email.
    
    Best regards,
    The AI Chatbot Team
    """
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .button {{ display: inline-block; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; }}
            .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 AI Chatbot</h1>
            </div>
            <div class="content">
                <h2>Hi {user.username},</h2>
                <p>Welcome to AI Chatbot! Please verify your email address to complete your registration.</p>
                
                <p style="text-align: center; margin: 30px 0;">
                    <a href="{verification_url}" class="button">Verify Email Address</a>
                </p>
                
                <p>Or copy and paste this link in your browser:</p>
                <p style="background: #eee; padding: 10px; border-radius: 5px; word-break: break-all;">
                    {verification_url}
                </p>
                
                <p>This link will expire in 24 hours.</p>
                
                <p>If you didn't create an account with us, please ignore this email.</p>
                
                <div class="footer">
                    <p>Best regards,<br>The AI Chatbot Team</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending verification email: {e}")
        return False