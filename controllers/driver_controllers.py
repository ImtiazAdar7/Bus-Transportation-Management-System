# Author: Imtiaz Ahmed 2013552642
import datetime
import jwt
from flask_bcrypt import Bcrypt
from config import Config
from models.driver_model import DriverModel

bcrypt = Bcrypt()

class DriverController:
    """Controller for driver registration and login."""
    @staticmethod
    def register(data):
        """
                Register a new driver.

                Args:
                    data (dict): Driver details with keys:
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
        try:
            existing = DriverModel.find_by_email(data["email"])
            if existing:
                return {"message": "Email already exists"}, 400
            hashed_password = bcrypt.generate_password_hash(data["password"]).decode()
            data["password"] = hashed_password

            DriverModel.create_driver(data)
            return {"message": "Driver Registered Successfully"}, 201
        except Exception as e:
            print("Driver registration error:", e)
            return {"message": "Internal server error"}, 500

    @staticmethod
    def login(data):
        """
        Login a driver.

        Args:
            data (dict): Driver login details with keys:
                - email (str)
                - password (str)

        Returns:
            tuple: (dict with message, JWT token, username, HTTP status code)
        """
        user = DriverModel.find_by_email(data["email"])
        if not user:
            return {"message": "User not found"}, 404

        if not bcrypt.check_password_hash(user["password"], data["password"]):
            return {"message": "Incorrect password"}, 401

        token = jwt.encode(
            {"id": user["id"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)},
            Config.SECRET_KEY,
            algorithm="HS256"
        )

        return {
            "message": "Login successful",
            "token": token,
            "username": user["username"]
        }, 200
