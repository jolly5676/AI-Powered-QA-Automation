"""
Module: email_notifier
Provides simple functionality to send emails and track notifications.
"""

def send_email(recipient: str, subject: str, body: str):
    """Simulate sending an email."""
    if "@" not in recipient:
        raise ValueError("Invalid email address.")
    print(f"Email sent to {recipient} with subject: {subject}")
    return True


def log_notification(recipient: str, subject: str):
    """Log email notifications."""
    print(f"Notification logged for {recipient}: {subject}")
    return {"recipient": recipient, "subject": subject, "status": "LOGGED"}
