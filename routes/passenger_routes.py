# Author: Imtiaz Ahmed 2013552642
from flask import Blueprint, request
from controllers.passenger_controller import PassengerController

passenger_bp = Blueprint("passenger_bp", __name__, url_prefix="/api/passenger")

@passenger_bp.post("/register")
def register_passenger():
    """
    Register a new passenger.

    Expects JSON payload with passenger details.
    Returns success message and HTTP status code.
    """
    return PassengerController.register(request.json)

@passenger_bp.post("/login")
def passenger_login():
    """
    Login a passenger.

    Expects JSON payload with email and password.
    Returns JWT token, username, message, and status code.
    """
    return PassengerController.login(request.json)
