import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(sender_email: str, sender_password: str, receiver_email: str, subject: str, body: str) -> None:
    """
    Sends an email using SMTP.

    Parameters:
        sender_email (str): Sender's email address.
        sender_password (str): Sender's email password.
        receiver_email (str): Receiver's email address.
        subject (str): Email subject.
        body (str): Email body.

    Raises:
        smtplib.SMTPException: If an error occurs during SMTP communication.
        Exception: If an unknown error occurs.
    """
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

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