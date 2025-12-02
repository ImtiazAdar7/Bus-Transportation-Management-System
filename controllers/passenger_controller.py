# Author: Imtiaz Ahmed 2013552642
import datetime
import jwt
from flask_bcrypt import Bcrypt
from config import Config
from models.passenger_model import PassengerModel

bcrypt = Bcrypt()

class PassengerController:
    """Controller to manage passenger registration and login."""

    @staticmethod
    def register(data):
        """Register a new passenger."""
        existing = PassengerModel.find_by_email(data["email"])
        if existing:
            return {"message": "Email already exists"}, 400

        hashed_password = bcrypt.generate_password_hash(data["password"]).decode()
        data["password"] = hashed_password

        PassengerModel.create_passenger(data)
        return {"message": "Passenger Registered Successfully"}, 201

    @staticmethod
    def login(data):
        """Passenger login and return JWT token."""
        user = PassengerModel.find_by_email(data["email"])
        if not user:
            return {"message": "User not found"}, 404

        if not bcrypt.check_password_hash(user["password"], data["password"]):
            return {"message": "Incorrect password"}, 401

        token = jwt.encode(
            {
                "id": user["id"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
            },
            Config.SECRET_KEY,
            algorithm="HS256"
        )

        return {
            "message": "Login successful",
            "token": token,
            "username": user["username"]
        }, 200
