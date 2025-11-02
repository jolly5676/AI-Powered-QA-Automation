"""
Module: inventory_manager
Manages inventory for retail or warehouse operations.
"""

def add_item(inventory: dict, item_name: str, quantity: int):
    """Add a new item or restock existing."""
    if quantity <= 0:
        raise ValueError("Quantity must be positive.")
    inventory[item_name] = inventory.get(item_name, 0) + quantity
    return inventory


def remove_item(inventory: dict, item_name: str, quantity: int):
    """Remove a specific quantity of an item."""
    if item_name not in inventory:
        raise ValueError("Item not found in inventory.")
    if inventory[item_name] < quantity:
        raise ValueError("Insufficient stock to remove.")
    inventory[item_name] -= quantity
    return inventory


def check_availability(inventory: dict, item_name: str) -> bool:
    """Check if an item is available in stock."""
    return inventory.get(item_name, 0) > 0
