# Azure Function App for User Registration and Email Notifications

## Overview

This Azure Function App provides a serverless solution for handling user registrations and sending email notifications. The app includes an HTTP-triggered function for user registration and a queue-triggered function for sending emails based on user actions (signup, login, logout, and account updates).

## Features

- **User Registration**: Accepts user details via an HTTP POST request and validates input.
- **Queue-based Email Sending**: Utilizes Azure Storage Queue to handle email requests asynchronously.
- **Dynamic Email Content**: Sends personalized emails based on user actions.

## Architecture

The app consists of two main functions:

1. **UserRequests**: An HTTP-triggered function that processes user registration requests.
2. **EmailSender**: A queue-triggered function that sends emails based on messages in the Azure Storage Queue.

## Prerequisites

- An Azure account with access to Azure Functions and Azure Storage.
- Python 3.6 or later installed locally for development and testing.
- Necessary Azure SDKs and libraries installed.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**:
   Ensure you have the required libraries installed:
   ```bash
   pip install azure-functions azure-storage-queue
   ```

3. **Configure Environment Variables**:
   Set the following environment variables in your Azure Function App settings or local `.env` file:
   - `AzureWebJobsStorage`: Connection string for your Azure Storage account.
   - `SMTP_SERVER`: SMTP server address for sending emails.
   - `SMTP_PORT`: SMTP server port (usually 587 for TLS).
   - `SMTP_USER`: Your SMTP username.
   - `SMTP_PASSWORD`: Your SMTP password.
   - `SMTP_FROM_EMAIL`: The sender email address (must match a verified sender identity).

4. **Deploy the Function App**:
   Deploy your Function App to Azure using your preferred method (Azure CLI, VS Code, etc.).

## Usage

### User Registration

To register a new user, send a POST request to the `/register` endpoint with the following JSON body:

```json
{
    "username": "exampleuser",
    "email": "user@example.com",
    "password": "securepassword",
    "first_name": "First",
    "last_name": "Last"
}
```

**Response**:
- On success: `202 Accepted`
- On failure: `400 Bad Request` with a message indicating missing fields.

### Email Sending

When a user registers, the `UserRequests` function sends a message to the Azure Storage Queue. The `EmailSender` function processes these messages and sends emails based on the action specified in the queue message.

### Supported Actions
- **signup**: Sends a welcome email to the user.
- **login**: Sends a login notification email.
- **logout**: Sends a logout notification email.
- **account_update**: Sends an email confirming account updates.

## Logging

The app includes logging for both the user requests and email sending processes. You can view the logs in the Azure portal under the "Log Stream" for your Function App.

## Contributing

Contributions are welcome! Please create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.



## Helpful CLI commands
### To fetch app settings 
func azure functionapp fetch-app-settings <APP_NAME>
### To deploy function app
func azure functionapp publish <APP_NAME>
### To reference key from key vault
@Microsoft.KeyVault(SecretUri=https://<YourVaultName>.vault.azure.net/secrets/<SecretName>/<SecretVersion>)


