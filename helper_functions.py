import os
import logging
import smtplib
import random
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to_email, subject, body):
    """
    Sends an email to the specified address.

    :param to_email: Recipient's email address
    :param subject: Subject of the email
    :param body: Body of the email
    """
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_from = os.getenv("SMTP_FROM_EMAIL")

    # Create the MIME message
    msg = MIMEMultipart()
    msg['From'] = smtp_from  # Set the From email address
    msg['To'] = to_email     # Set the recipient's email address
    msg['Subject'] = subject  # Set the subject

    # Attach the email body to the message
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, to_email, msg.as_string())
            logging.info(f"Email sent to {to_email} successfully.")
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")


def generate_confirmation_token(length=6):
    """
    Generates a random confirmation token.

    The token consists of uppercase letters, lowercase letters, digits, 
    and allowed special characters.

    Args:
        length (int): The length of the token to be generated. Default is 6.

    Returns:
        str: A randomly generated token of the specified length.
    """
    # Define the character pool for the token
    allowed_characters = string.ascii_uppercase + string.ascii_lowercase + string.digits + "!@#$%^&*"
    
    # Randomly select characters from the allowed pool
    token = ''.join(random.choice(allowed_characters) for _ in range(length))
    
    return token