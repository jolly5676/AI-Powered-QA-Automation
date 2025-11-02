"""
Module: user_authenticator
Performs simple username-password validation and session creation.
"""

import uuid


def authenticate_user(username: str, password: str) -> bool:
    """Authenticate user credentials."""
    if not username or not password:
        raise ValueError("Username or password cannot be empty.")
    return password == "secret123"


def create_session(username: str) -> dict:
    """Create a user session."""
    session_id = str(uuid.uuid4())
    return {"username": username, "session_id": session_id, "status": "ACTIVE"}


def logout_user(session_id: str) -> dict:
    """End a user session."""
    return {"session_id": session_id, "status": "TERMINATED"}
