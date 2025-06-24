<p align="center">
  <img src="https://img.shields.io/badge/Azure_Functions-2.0+-0062AD?logo=microsoftazure" alt="Azure Functions">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/SMTP-Integration-orange" alt="SMTP">
  <img src="https://img.shields.io/badge/Status-Active-success" alt="Status">
</p>

<div align="center">
  <h1>📧 Email Function App</h1>
  <p><em>Serverless Email Notification System for User Management</em></p>
</div>

---

## 📋 Table of Contents
- [📖 Overview](#-overview)
- [🎯 Learning Objectives](#-learning-objectives)
- [🛠️ Tech Stack](#️-tech-stack)
- [📁 Project Structure](#-project-structure)
- [🚀 Getting Started](#-getting-started)
- [💡 Usage](#-usage)
- [🏆 Key Features](#-key-features)
- [📚 Resources](#-resources)
- [👥 Contributors](#-contributors)

## 📖 Overview

This serverless Azure Function App provides a scalable solution for sending transactional emails based on user actions. The system processes queue messages to deliver personalized emails for user registration, authentication events, account management, and general notifications.

Built with modern serverless architecture principles, this application demonstrates advanced cloud-native patterns including queue-triggered processing, secure SMTP integration, and automated CI/CD deployment. The system is designed for high availability, cost-effectiveness, and seamless integration with existing user management systems.

## 🎯 Learning Objectives

Through this project, you will master:

- **Serverless Architecture**: Build and deploy Azure Functions with queue triggers
- **Asynchronous Processing**: Implement message queue patterns for reliable email delivery
- **Email Integration**: Configure SMTP protocols and email template systems
- **Cloud Security**: Manage secrets with Azure KeyVault and secure communications
- **CI/CD Pipeline**: Automate deployment with GitHub Actions
- **Error Handling**: Implement robust error management and retry mechanisms
- **Monitoring & Logging**: Set up comprehensive logging for production debugging

## 🛠️ Tech Stack

**Core Technologies:**
- **Azure Functions**: Serverless compute platform for event-driven processing
- **Python 3.10+**: Primary programming language with async/await support
- **Azure Storage Queues**: Message queuing service for asynchronous processing

**Development Tools:**
- **Azure KeyVault**: Secure secrets and configuration management
- **SMTP Protocol**: Industry-standard email transmission protocol
- **GitHub Actions**: Automated CI/CD pipeline for deployment
- **TLS Encryption**: Secure email transmission and data protection

## 📁 Project Structure

```
Email_FA/
├── function_app.py          # Main Azure Function entry point
├── helper_functions.py      # Email utilities and SMTP configuration
├── host.json               # Function app configuration
├── requirements.txt        # Python dependencies
├── .github/
│   └── workflows/          # CI/CD pipeline configuration
├── ARCHITECTURE.md         # System design documentation
├── SKILLS-INDEX.md        # Technical skills catalog
└── README.md              # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- **Azure Account**: Active Azure subscription with Functions service enabled
- **Python 3.10+**: Local development environment
- **Azure Functions Core Tools**: For local testing and deployment
- **SMTP Server Access**: Email service credentials (Gmail, SendGrid, etc.)
- **Git**: Version control system

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Email_FA
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   # Create local.settings.json for local development
   {
     "IsEncrypted": false,
     "Values": {
       "AzureWebJobsStorage": "your-storage-connection-string",
       "SMTP_SERVER": "your-smtp-server",
       "SMTP_PORT": "587",
       "EMAIL_USER": "your-email@domain.com",
       "EMAIL_PASSWORD": "your-app-password"
     }
   }
   ```

### Running the Project

1. **Local Development**:
   ```bash
   func start
   ```

2. **Deploy to Azure**:
   ```bash
   func azure functionapp publish <your-function-app-name>
   ```

3. **Test Queue Processing**:
   ```bash
   # Add message to queue via Azure Storage Explorer or code
   # Function will automatically trigger and process emails
## 💡 Usage

### Queue Message Format

Send messages to the Azure Storage Queue with the following JSON structure:

```json
{
  "action": "signup|login|logout|password_reset|account_deletion",
  "user_email": "user@example.com",
  "user_name": "John Doe",
  "additional_data": {
    "reset_token": "optional-token",
    "login_time": "2024-06-24T10:30:00Z"
  }
}
```

### Supported Email Types

- **User Registration**: Welcome emails for new users
- **Login Notifications**: Security alerts for account access
- **Logout Confirmations**: Notifications of session termination
- **Account Deletion**: Confirmation of account removal
- **Password Management**: Reset requests and change confirmations
- **Email Verification**: Account verification flows
- **General Notifications**: Custom user notifications

## 🏆 Key Features

- **Queue-Triggered Processing**: Asynchronously handles email requests through Azure Storage Queues
- **Multiple Email Templates**: Supports various notification types with personalized content
- **Scalable Architecture**: Leverages Azure Functions' serverless model for cost-effective scaling
- **Secure Email Delivery**: Uses TLS for SMTP communication with configurable email providers
- **Error Handling**: Robust error management with logging and retry mechanisms
- **CI/CD Integration**: Automated deployment via GitHub Actions
- **Configuration Management**: Secure handling of credentials via Azure KeyVault
- **Monitoring & Logging**: Comprehensive logging for debugging and monitoring

## 📚 Resources

- [Azure Functions Documentation](https://docs.microsoft.com/azure/azure-functions/)
- [Azure Storage Queues Guide](https://docs.microsoft.com/azure/storage/queues/)
- [Python SMTP Library Documentation](https://docs.python.org/3/library/smtplib.html)
- [GitHub Actions for Azure](https://docs.microsoft.com/azure/developer/github/github-actions)
- [SKILLS-INDEX.md](./SKILLS-INDEX.md) - Detailed technical skills catalog
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System design and architecture details

## 👥 Contributors

**Chigbu Joshua**
- 📧 Email: [chigbujoshua@yahoo.com](mailto:chigbujoshua@yahoo.com)
- 🐙 GitHub: [@yungryce](https://github.com/yungryce)
- 🎯 Role: Primary Author, Project Maintainer

*This project demonstrates serverless architecture and email integration patterns for modern cloud applications.*

## Prerequisites

- Azure subscription
- SMTP server credentials
- Python 3.10 or higher (for local development)

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd Email_FA
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `local.settings.json` file for local development:
   ```json
   {
     "IsEncrypted": false,
     "Values": {
       "AzureWebJobsStorage": "<storage-connection-string>",
       "FUNCTIONS_WORKER_RUNTIME": "python",
       "SMTP_SERVER": "smtp.example.com",
       "SMTP_PORT": "587",
       "SMTP_USER": "your-username",
       "SMTP_PASSWORD": "your-password",
       "SMTP_FROM_EMAIL": "noreply@example.com"
     }
   }
   ```

4. **Local Development**:
   ```bash
   func start
   ```

5. **Deploy to Azure**:
   ```bash
   func azure functionapp publish emailapp
   ```

## KeyVault Integration

For production environments, secure your credentials using Azure KeyVault:

```
@Microsoft.KeyVault(SecretUri=https://<YourVaultName>.vault.azure.net/secrets/<SecretName>/<SecretVersion>)
```

## CI/CD Pipeline

This project includes GitHub Actions workflows for continuous deployment:

- Automatic deployment on push to master branch
- Python dependency caching for faster builds
- Azure Functions Core Tools integration

## Helpful CLI Commands

### Fetch App Settings 
```bash
func azure functionapp fetch-app-settings <APP_NAME>
```

### Deploy Function App
```bash
func azure functionapp publish <APP_NAME>
```

## Testing

To test locally, you can:

1. Add messages to the queue via the Azure Portal
2. Use the Azure Functions Core Tools to trigger the function with sample data

## Skills Index

For a detailed mapping of technical skills implemented in this project, see [SKILLS-INDEX.md](./SKILLS-INDEX.md).

## Contributing

Contributions are welcome! Please create a pull request with your changes.

## License

This project is licensed under the MIT License.


