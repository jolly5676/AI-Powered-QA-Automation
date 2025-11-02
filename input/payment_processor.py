"""
Module: payment_processor
Handles payment validation, transaction processing, and refund workflows.
"""

import uuid
import datetime


def validate_payment(card_number: str, expiry_date: str, cvv: str, amount: float) -> bool:
    """
    Validate card and payment details.
    """
    if len(card_number) != 16:
        raise ValueError("Invalid card number length")
    if len(cvv) != 3:
        raise ValueError("Invalid CVV")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")
    return True


def process_payment(user_id: str, amount: float) -> dict:
    """
    Process a payment and return transaction details.
    """
    transaction_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()
    return {"transaction_id": transaction_id, "user_id": user_id, "amount": amount, "status": "SUCCESS", "timestamp": timestamp}


def issue_refund(transaction_id: str, amount: float) -> dict:
    """
    Issue a refund and return confirmation details.
    """
    refund_id = str(uuid.uuid4())
    return {"refund_id": refund_id, "transaction_id": transaction_id, "amount": amount, "status": "REFUNDED"}
