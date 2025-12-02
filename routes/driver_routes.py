# Author: Imtiaz Ahmed 2013552642
from flask import Blueprint, request
from controllers.driver_controllers import DriverController

driver_bp = Blueprint("driver_bp", __name__, url_prefix="/api/driver")

@driver_bp.post("/register")
def register_driver():
    """
    Register a new driver.

    Expects JSON payload with driver details.
    Returns success message and HTTP status code.
    """
    return DriverController.register(request.json)

@driver_bp.post("/login")
def driver_login():
    """
    Login a driver.

    Expects JSON payload with email and password.
    Returns JWT token, username, message, and status code.
    """
    return DriverController.login(request.json)
