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

@passenger_bp.post("/booking")
def create_booking():
    """
    Create a new booking for the authenticated passenger.

    Expects JSON payload with bus_route_id and price.
    Requires Authorization header with Bearer token.
    Returns booking confirmation and status code.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    return PassengerController.create_booking(request.json, token)

@passenger_bp.get("/bookings")
def get_my_bookings():
    """
    Get all bookings for the authenticated passenger.

    Requires Authorization header with Bearer token.
    Returns list of bookings and status code.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    return PassengerController.get_my_bookings(token)