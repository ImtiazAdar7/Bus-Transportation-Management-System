# Author: Imtiaz Ahmed 2013552642
from flask import Blueprint, request
from controllers.admin_controllers import AdminController

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/api/admin")

@admin_bp.post("/register")
def register_admin():
    """
    Register a new admin.

    Expects JSON payload with admin details.
    Returns JSON message and HTTP status code.
    """
    return AdminController.register(request.json)

@admin_bp.post("/login")
def login_admin():
    """
    Login an admin.

    Expects JSON payload with username and password.
    Returns JWT token, username, message, and status code.
    """
    return AdminController.login(request.json)

@admin_bp.get("/drivers")
def get_all_drivers():
    """
    Get all drivers.

    Returns a list of all drivers with status code 200.
    """
    return AdminController.get_all_drivers()

@admin_bp.post("/assign_driver/<int:driver_id>")
def assign_driver(driver_id):
    """
    Assign a driver by ID.

    Moves driver from drivers table to assigned_drivers table.
    """
    return AdminController.assign_driver(driver_id)

@admin_bp.delete("/delete_driver/<int:driver_id>")
def delete_driver(driver_id):
    """
    Delete a driver by ID.

    Returns success or error message.
    """
    return AdminController.delete_driver(driver_id)