import os
import json
import logging
import base64
import azure.functions as func
from azure.storage.queue import QueueClient
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Retrieve the connection string from environment variables
CONNECTION_STRING = os.getenv('AzureWebJobsStorage')

# Initialize the Queue Client
queue_client = QueueClient.from_connection_string(CONNECTION_STRING, "emailqueue")

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

# HTTP Trigger Function
@app.function_name(name="UserRequests")
@app.route(route="register", methods=["POST"])
def user_requests(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Parse the request body
        req_body = req.get_json()
        logging.info("Received registration request.")

        # Validate the input
        required_fields = ["username", "email", "password", "first_name", "last_name"]
        missing_fields = [field for field in required_fields if field not in req_body]

        if missing_fields:
            logging.warning(f"Missing fields: {', '.join(missing_fields)}")
            return func.HttpResponse(
                f"Missing fields: {', '.join(missing_fields)}",
                status_code=400
            )

        # Create the new user object
        new_user = {
            "username": req_body["username"],
            "email": req_body["email"],
            "password": req_body["password"],  # Be cautious with handling passwords!
            "first_name": req_body["first_name"],
            "last_name": req_body["last_name"]
        }

        # Add the request to the queue with action type
        message = json.dumps({
            "action": "signup",
            "email": req_body["email"],
            "user": new_user
        })
        encoded_message = base64.b64encode(message.encode('utf-8')).decode('utf-8')
        queue_client.send_message(encoded_message)

        logging.info(f"User request added to the queue for {new_user['username']}.")
        return func.HttpResponse(
            "User request added to the queue.",
            status_code=202
        )
    
    except Exception as e:
        logging.error(f"An error occurred in user_requests: {str(e)}")
        return func.HttpResponse(
            f"An error occurred: {str(e)}",
            status_code=500
        )


# HTTP Trigger Function
@app.function_name(name="EmailSender")
@app.queue_trigger(arg_name="msg", queue_name="emailqueue", connection="AzureWebJobsStorage")
def push_email(msg: func.QueueMessage) -> None:
    logging.info(f"Processing message: {msg.get_body().decode()}")
    try:
        # Get the message body and parse it
        email_request = msg.get_json()
        action = email_request["action"]
        email = email_request["email"]
        logging.info(f"Processing email request for action: {action}")

        # Determine the email subject and body based on the action
        if action == "signup":
            subject = "Welcome to Our Service!"
            body = "Thank you for signing up. We're glad to have you!"
        elif action == "login":
            subject = "Login Notification"
            body = "You have successfully logged in."
        elif action == "logout":
            subject = "Logout Notification"
            body = "You have successfully logged out."
        elif action == "account_update":
            subject = "Account Update"
            body = "Your account details have been updated."
        else:
            logging.warning(f"Unknown action: {action}")
            return  # Skip unknown actions

        # Send the email
        send_email(email, subject, body)

    except Exception as e:
        logging.error(f"Failed to process queue message: {str(e)}")