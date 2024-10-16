import os
import json
import logging
import base64
import azure.functions as func
from azure.storage.queue import QueueClient
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from helper_functions import send_email, generate_confirmation_token


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Retrieve the connection string from environment variables
CONNECTION_STRING = os.getenv('AzureWebJobsStorage')

# Initialize the Queue Client
queue_client = QueueClient.from_connection_string(CONNECTION_STRING, "emailqueue")


@app.function_name(name="EmailSender")
@app.queue_trigger(arg_name="msg", queue_name="emailqueue", connection="AzureWebJobsStorage")
async def push_email(msg: func.QueueMessage) -> None:
    """
    Processes a message from the email queue and sends an email.
    Args: 
        msg: The incoming queue message
        queue_name: The name of the queue
        connection: The connection string for the storage account

    Returns: None

    """
    logging.info(f"Processing message: {msg.get_body().decode()}")
    message = json.loads(msg.get_body().decode())
    action = message.get('action')

    if action == 'signup':
        await register_email(message)
    elif action == 'login':
        await login_email(message)
    elif  action == 'logout':
        await logout_email(message)
    elif action == 'reset':
        await reset_password_email(message)
    elif action == 'confirm':
        await confirm_email(message)
    elif action == 'notify':
        await notify_user(message)
    elif action == 'deleted_user':
        await deleted_user_email(message)
    else:
        logging.warning(f"Unknown action: {action}")


async def register_email(message):
    """
    Sends a registration confirmation email to the user.
    
    Args:
        message (dict): The message containing user details (from the queue).
        
    Returns:
        None
    """
    try:
        # Extract user data from the message
        to_email = message.get('email')
        first_name = message.get('first_name')
        last_name = message.get('last_name')
        username = message.get('username')

        # Generate a confirmation token
        confirmation_token = generate_confirmation_token()

        # Compose the email content
        subject = "Welcome to Our Platform!"
        body = f"Dear {first_name} {last_name},\n\n" \
               f"Thank you for registering with us! Your username is {username}.\n" \
               f"Your confirmation token is: {confirmation_token}\n\n" \
               "We are excited to have you on board. If you have any questions, feel free to contact us.\n\n" \
               "Best regards,\nThe Team"

        # Send the email using the send_email helper function
        send_email(to_email, subject, body)

        logging.info(f"Registration email sent successfully to {to_email}.")
    except Exception as e:
        logging.error(f"Failed to send registration email: {str(e)}")


async def login_email(message):
    """
    Sends an email notification to the user after a successful login.
    Includes a warning if the login did not originate from the user,
    and provides a link to reset their password.

    Args:
        message (dict): The message containing user details and login information (from the queue).
        
    Returns:
        None
    """
    try:
        # Extract user data and login details from the message
        to_email = message.get('email')
        first_name = message.get('first_name')
        last_name = message.get('last_name')
        username = message.get('username')
        login_ip = message.get('login_ip', 'Unknown IP')
        login_time = message.get('login_time', 'Unknown time')

        # Compose the email content
        subject = "Account Login Notification"

        body = f"Dear {first_name} {last_name},\n\n" \
            f"We noticed a login to your account (Username: {username}) on {login_time} from {login_ip}.\n\n" \
            "If this login attempt was made by you, no further action is required.\n\n" \
            "If this login did not originate from you, we recommend that you reset your password immediately to secure your account.\n\n" \
            "Please visit your account profile to reset your password:\n" \
            "If you have any questions or need further assistance, feel free to contact us.\n\n" \
            "Best regards,\nThe Security Team"

        # Send the email using the send_email helper function
        send_email(to_email, subject, body)

        logging.info(f"Login notification email sent successfully to {to_email}.")
    except Exception as e:
        logging.error(f"Failed to send login notification email: {str(e)}")


async def logout_email(message):
    """
    Sends an email notification to the user upon logout.

    Args:
        message (dict): A dictionary containing user data and action details, including:
                        - username
                        - email
                        - first_name
                        - last_name
                        - login_ip (if available)
                        - logout_time

    Returns:
        None
    """
    # Extract user details from the message
    username = message.get('username')
    email = message.get('email')
    first_name = message.get('first_name')
    last_name = message.get('last_name')
    logout_time = message.get('logout_time')  # This should be included in the message
    logout_ip = message.get('logout_ip', 'Unknown IP')  # Default to 'Unknown IP' if not available

    # Email body with logout notification
    body = f"Dear {first_name} {last_name},\n\n" \
           f"We noticed that you logged out of your account (Username: {username}) on {logout_time} from {logout_ip}.\n\n" \
           "If this logout was done by you, no further action is required.\n\n" \
           "If you did not initiate this logout, please log in again and update your password to secure your account.\n\n" \
           "You can visit your account profile to reset your password or review account activity:\n" \
           "If you have any questions or need further assistance, feel free to contact us.\n\n" \
           "Best regards,\nThe Security Team"

    # Subject of the email
    subject = "Logout Notification - Your Account"

    # Send the email using the send_email function
    try:
        send_email(to_email=email, subject=subject, body=body)
        logging.info(f"Logout notification email sent to {email} successfully.")
    except Exception as e:
        logging.error(f"Failed to send logout email to {email}: {str(e)}")

async def delete_user_email(message):
    """
    Sends an email notification to the user upon account deletion.

    Args:
        message (dict): A dictionary containing user data and action details, including:
                        - username
                        - email
                        - first_name
                        - last_name
                        - deletion_time

    Returns:
        None
    """
    # Extract user details from the message
    username = message.get('username')
    email = message.get('email')
    first_name = message.get('first_name')
    last_name = message.get('last_name')
    deletion_time = message.get('deletion_time')  # Ensure this is passed in the message

    # Email body with account deletion notification
    body = f"Dear {first_name} {last_name},\n\n" \
           f"We want to confirm that your account (Username: {username}) has been successfully deleted on {deletion_time}.\n\n" \
           "If this account deletion was initiated by you, no further action is required.\n\n" \
           "However, if you did not request this deletion, please contact our support team immediately for assistance.\n\n" \
           "Please note that once your account is deleted, all associated data, including personal information, will be permanently removed from our system.\n\n" \
           "If you have any questions or need further assistance, feel free to contact us.\n\n" \
           "Best regards,\nThe Security Team"

    # Subject of the email
    subject = "Account Deletion Confirmation"

    # Send the email using the send_email function
    try:
        send_email(to_email=email, subject=subject, body=body)
        logging.info(f"Account deletion confirmation email sent to {email} successfully.")
    except Exception as e:
        logging.error(f"Failed to send account deletion email to {email}: {str(e)}")


async def reset_password_email(message):
    """
    Sends an email to the user with a password reset link.

    Args:
        message (dict): A dictionary containing user data and action details, including:
                        - username
                        - email
                        - first_name
                        - last_name
                        - reset_link

    Returns:
        None
    """
    # Extract user details from the message
    username = message.get('username')
    email = message.get('email')
    first_name = message.get('first_name')
    last_name = message.get('last_name')
    reset_link = message.get('reset_link')  # Ensure this is passed in the message

    # Email body with password reset link
    body = f"Dear {first_name} {last_name},\n\n" \
           f"We received a request to reset the password for your account (Username: {username}).\n\n" \
           "To reset your password, please click on the following link:\n" \
           f"{reset_link}\n\n" \
           "If you did not request a password reset, please ignore this email.\n\n" \
           "If you have any questions or need further assistance, feel free to contact us.\n\n" \
           "Best regards,\nThe Support Team"

    # Subject of the email
    subject = "Password Reset Request"

    # Send the email using the send_email function
    try:
        send_email(to_email=email, subject=subject, body=body)
        logging.info(f"Password reset email sent to {email} successfully.")
    except Exception as e:
        logging.error(f"Failed to send password reset email to {email}: {str(e)}")


async def confirm_email(message):
    """
    Sends an email to the user to confirm their registration.

    Args:
        message (dict): A dictionary containing user data and action details, including:
                        - username
                        - email
                        - first_name
                        - last_name

    Returns:
        None
    """
    # Extract user details from the message
    username = message.get('username')
    email = message.get('email')
    first_name = message.get('first_name')
    last_name = message.get('last_name')

    # Email body with account confirmation message
    body = f"Dear {first_name} {last_name},\n\n" \
           f"Thank you for confirming your registration on our platform (Username: {username}).\n\n" \
           "You are now an active member of our community.\n\n" \
           "If you have any questions or need further assistance, feel free to contact us.\n\n" \
           "Best regards,\nThe Team"

    # Subject of the email
    subject = "Registration Confirmation"

    # Send the email using the send_email function
    try:
        send_email(to_email=email, subject=subject, body=body)
        logging.info(f"Registration confirmation email sent to {email} successfully.")
    except Exception as e:
        logging.error(f"Failed to send registration confirmation email to {email}: {str(e)}")


async def notify_user(message):
    """
    Sends a general notification email to the user.

    Args:
        message (dict): A dictionary containing user data and action details, including:
                        - username
                        - email
                        - first_name
                        - last_name
                        - notification_message

    Returns:
        None
    """
    # Extract user details from the message
    username = message.get('username')
    email = message.get('email')
    first_name = message.get('first_name')
    last_name = message.get('last_name')
    notification_message = message.get('notification_message')  # Ensure this is passed in the message

    # Email body with the notification message
    body = f"Dear {first_name} {last_name},\n\n" \
           f"We have an important message for you regarding your account (Username: {username}).\n\n" \
           f"{notification_message}\n\n" \
           "If you have any questions or need further assistance, feel free to contact us.\n\n" \
           "Best regards,\nThe Support Team"

    # Subject of the email
    subject = "Important Notification"

    # Send the email using the send_email function
    try:
        send_email(to_email=email, subject=subject, body=body)
        logging.info(f"Notification email sent to {email} successfully.")
    except Exception as e:
        logging.error(f"Failed to send notification email to {email}: {str(e)}")


async def deleted_user_email(message):
    """
    Sends an email notification to the user upon account deletion.

    Args:
        message (dict): A dictionary containing user data and action details, including:
                        - username
                        - email
                        - first_name
                        - last_name
                        - deletion_time

    Returns:
        None
    """
    # Extract user details from the message
    username = message.get('username')
    email = message.get('email')
    first_name = message.get('first_name')
    last_name = message.get('last_name')
    deletion_time = message.get('deletion_time')  # Ensure this is passed in the message

    # Email body with account deletion notification
    body = f"Dear {first_name} {last_name},\n\n" \
           f"We want to confirm that your account (Username: {username}) has been successfully deleted on {deletion_time}.\n\n" \
           "If this account deletion was initiated by you, no further action is required.\n\n" \
           "However, if you did not request this deletion, please contact our support team immediately for assistance.\n\n" \
           "Please note that once your account is deleted, all associated data, including personal information, will be permanently removed from our system.\n\n" \
           "If you have any questions or need further assistance, feel free to contact us.\n\n" \
           "Best regards,\nThe Security Team"

    # Subject of the email
    subject = "Account Deletion Confirmation"

    # Send the email using the send_email function
    try:
        send_email(to_email=email, subject=subject, body=body)
        logging.info(f"Account deletion confirmation email sent to {email} successfully.")
    except Exception as e:
        logging.error(f"Failed to send account deletion email to {email}: {str(e)}")


