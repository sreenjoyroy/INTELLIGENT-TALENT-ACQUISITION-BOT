import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

# Gmail SMTP Configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(recipient: str, subject: str, html_content: str, attachments: list = None):
    try:
        message = MIMEMultipart()
        message['From'] = EMAIL_SENDER
        message['To'] = recipient
        message['Subject'] = subject

        message.attach(MIMEText(html_content, 'html'))

        # Attach files if any
        if attachments:
            for file_path in attachments:
                with open(file_path, 'rb') as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                    message.attach(part)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, recipient, message.as_string())

        print(f"✅ Email sent successfully to {recipient}")

    except Exception as e:
        print(f"❌ Failed to send email to {recipient}: {e}")


# High-level email functions

def send_email_to_hr(hr_email: str, subject: str, body: str):
    html_content = f"""
    <html>
        <body>
            <p>{body}</p>
        </body>
    </html>
    """
    send_email(hr_email, subject, html_content)


def send_email_to_applicant(applicant_email: str, subject: str, body: str):
    html_content = f"""
    <html>
        <body>
            <p>{body}</p>
        </body>
    </html>
    """
    send_email(applicant_email, subject, html_content)

def send_engagement_email(applicant_email: str, applicant_name: str) -> bool:
    try:
        subject = "We’re excited to meet you!"
        message = f"""
        <html>
        <body>
            <p>Hi <strong>{applicant_name}</strong>,</p>
            <p>Thank you for applying! We loved reviewing your profile and are excited to take things forward with you.</p>
            <p>Could you please share your availability for a quick chat or interview?</p>
            <p>Looking forward to connecting with you soon.</p>
            <br>
            <p>Best regards,<br>
            <strong>Talent Acquisition Team</strong></p>
        </body>
        </html>
        """

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = applicant_email

        mime_text = MIMEText(message, "html")
        msg.attach(mime_text)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, applicant_email, msg.as_string())

        print(f"✅ Engagement email sent to {applicant_email}")
        return True

    except Exception as e:
        print(f"❌ Failed to send engagement email to {applicant_email}. Error: {e}")
        return False
