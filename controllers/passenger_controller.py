# Author: Imtiaz Ahmed 2013552642
import datetime
import jwt
from flask import jsonify
from flask_bcrypt import Bcrypt
from config import Config
from models.passenger_model import PassengerModel
from models.booking_model import BookingModel

bcrypt = Bcrypt()

class PassengerController:
    """Controller to manage passenger registration and login."""

    @staticmethod
    def _verify_token(token):
        """Verify JWT token and return passenger ID."""
        try:
            if not token:
                return None
            decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            return decoded.get("id")
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def register(data):
        """
        Register a new passenger.

        Args:
            data (dict): Passenger details with keys:
                - first_name (str)
                - last_name (str)
                - age (str)
                - username (str)
                - email (str)
                - dob (str, optional)
                - gender (str)
                - password (str)

        Returns:
            tuple: (dict with message, HTTP status code)
        """
        existing = PassengerModel.find_by_email(data["email"])
        if existing:
            return jsonify({"message": "Email already exists"}), 400

        hashed_password = bcrypt.generate_password_hash(data["password"]).decode()
        data["password"] = hashed_password

        PassengerModel.create_passenger(data)
        return jsonify({"message": "Passenger Registered Successfully"}), 201

    @staticmethod
    def login(data):
        """
        Login a passenger and return JWT token.

        Args:
            data (dict): Login credentials with keys:
                - email (str)
                - password (str)

        Returns:
            tuple: (dict with message, JWT token, username, HTTP status code)
        """
        user = PassengerModel.find_by_email(data["email"])
        if not user:
            return jsonify({"message": "User not found"}), 404

        if not bcrypt.check_password_hash(user["password"], data["password"]):
            return jsonify({"message": "Incorrect password"}), 401

        token = jwt.encode(
            {
                "id": user["id"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
            },
            Config.SECRET_KEY,
            algorithm="HS256"
        )

        return jsonify({
            "message": "Login successful",
            "token": token,
            "username": user["username"]
        }), 200

    @staticmethod
    def create_booking(data, token):
        """
        Create a new booking for the authenticated passenger.

        Args:
            data (dict): Booking details with keys:
                - bus_route_id (int): ID of the bus route to book
                - price (float): Price of the booking
            token (str): JWT authentication token

        Returns:
            tuple: (dict with message and booking_id, HTTP status code)
        """
        try:
            passenger_id = PassengerController._verify_token(token)
            if not passenger_id:
                return jsonify({"message": "Unauthorized. Please login."}), 401

            bus_route_id = data.get("bus_route_id")
            price = data.get("price")

            if not bus_route_id or price is None:
                return jsonify({"message": "bus_route_id and price are required"}), 400

            booking_id = BookingModel.create_booking(bus_route_id, passenger_id, float(price))
            return jsonify({
                "message": "Booking created successfully",
                "booking_id": booking_id
            }), 201
        except Exception as e:
            import traceback
            print(f"Error in create_booking: {str(e)}")
            print(traceback.format_exc())
            return jsonify({"message": f"Failed to create booking: {str(e)}"}), 500

    @staticmethod
    def get_my_bookings(token):
        """
        Get all bookings for the authenticated passenger.

        Args:
            token (str): JWT authentication token

        Returns:
            tuple: (dict with list of bookings, HTTP status code)
        """
        try:
            passenger_id = PassengerController._verify_token(token)
            if not passenger_id:
                return jsonify({"message": "Unauthorized. Please login."}), 401

            bookings = BookingModel.get_bookings_by_passenger(passenger_id)
            return jsonify({"bookings": bookings}), 200
        except Exception as e:
            import traceback
            print(f"Error in get_my_bookings: {str(e)}")
            print(traceback.format_exc())
            return jsonify({"message": f"Failed to fetch bookings: {str(e)}"}), 500
