# Process Log Automation

This Python project automates the task of logging system processes, creating log files that contain details of all running processes such as process name, PID, memory usage, thread count, and the number of child processes. The log file is generated periodically and sent via email.

## Features

- **Automatic Process Logging**: Log files are created automatically, storing details like process name, PID, username, memory usage, and other information.
- **Email Sending**: The log files are emailed to the specified recipient.
- **Periodic Execution**: The logging task is executed periodically using Python's `schedule` library.
- **Internet Connectivity Check**: Ensures the system has an active internet connection before attempting to send an email.
- **Easy Setup**: Setup and configuration are simple, and the script works out-of-the-box with minimal configuration.

## Libraries Used

- **psutil**: To gather information about system processes.
- **schedule**: To automate the task of periodic execution.
- **smtplib**: For sending emails via an SMTP server.
- **email.mime**: For email formatting and attachment handling.

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ProcessLogAutomation.git

