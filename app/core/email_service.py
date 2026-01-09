from fastapi_mail import ConnectionConfig ,MessageSchema ,FastMail 
import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()
BASE_PATH = Path(__file__).resolve().parent.parent # This points to /app/

# Combine it to get the template folder
# Result: /home/singsys/personal-project/backend/app/templates/emails
TEMPLATE_DIR = BASE_PATH / "templates" / "emails"

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_STARTTLS=os.getenv("MAIL_TLS", "True") == "True",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL", "False") == "True",
    TEMPLATE_FOLDER=TEMPLATE_DIR # Now points correctly to /app/templates/emails
)

async def send_otp_email(email: str, otp: str):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .container {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 480px;
                margin: 0 auto;
                padding: 40px 20px;
                background-color: #ffffff;
            }}
            .logo {{
                font-weight: 900;
                font-size: 24px;
                color: #2D2E5F;
                text-decoration: none;
                margin-bottom: 30px;
                display: block;
            }}
            .card {{
                background: #F8FAFC;
                border-radius: 32px;
                padding: 40px;
                text-align: center;
                border: 1px solid #E2E8F0;
            }}
            .otp-code {{
                font-size: 42px;
                font-weight: 900;
                color: #5D5FEF;
                letter-spacing: 8px;
                margin: 20px 0;
                padding: 10px;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 12px;
                color: #94A3B8;
                text-align: center;
                line-height: 1.6;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="https://wrklyst.com" class="logo">Wrklyst</a>
            <div class="card">
                <h2 style="margin-top: 0; color: #1A1A1A;">Verify your email</h2>
                <p style="color: #64748B; font-size: 14px;">Use the following code to complete your sign up. This code will expire in 5 minutes.</p>
                <div class="otp-code">{otp}</div>
                <p style="color: #94A3B8; font-size: 12px;">If you didn't request this, you can safely ignore this email.</p>
            </div>
            <div class="footer">
                © 2025 Wrklyst Inc. <br>
                Designed for Efficiency. Secure File Management.
            </div>
        </div>
    </body>
    </html>
    """

    message = MessageSchema(
        subject="Your Wrklyst Verification Code",
        recipients=[email],
        body=html_content,
        subtype="html"  # Changed from plain to html
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)




async def send_confirmation_email(first_name:str , last_name:str,message_text:str,email:str):
    preview=message_text[:60]

    mail= MessageSchema(
        subject="We've received your message! - Wrklyst",
        recipients=[email],
        template_body={"firstname":first_name,"message_preview":preview},
        subtype="html"
    )
