import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(receiver_email: str) -> None:
    """
    Sends an email using SMTP.

    Parameters:
        body (str): Email body.

    Raises:
        smtplib.SMTPException: If an error occurs during SMTP communication.
        Exception: If an unknown error occurs.
    """
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        
        sender_email = os.getenv('SENDER_EMAIL')
        sender_password = os.getenv('SENDER_PASSWORD')
        subject = 'Invite to PSG DigiSign: You have been invited to sign this document.'
        body = '''
Dear user,
You are cordially invited to digitally sign an important document using PSG DigiSign, to sign the document.
Please follow this link to sign the document: http://localhost:3000
Your prompt attention to this matter is appreciated.\n
Best regards,
PSG DigiSign
'''
        msg = MIMEMultipart()

        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        server.login(sender_email, sender_password)

        server.sendmail(sender_email, receiver_email, msg.as_string())

        server.quit()
    except smtplib.SMTPException as e:
        raise e
    except Exception as e:
        raise e