# Author: Imtiaz Ahmed 2013552642

import datetime
import jwt
import mysql
from flask_bcrypt import Bcrypt
from config import Config

from models.admin_model import AdminModel
from models.assigned_driver_model import AssignedDriverModel
from models.driver_model import DriverModel

bcrypt = Bcrypt()

class AdminController:
    """Controller to manage admin actions like registration, login, driver management."""

    @staticmethod
    def register(data):
        """
        Register a new admin.

        Args:
            data (dict): Admin details (first_name, last_name, age, username,
                     website_auth_code, dob, gender, password)

        Returns:
            tuple: (dict with message, HTTP status code)
        """
        # Auto-create required tables on first request
        AdminModel.create_tables()
        AdminModel.insert_default_codes()

        # Required fields
        required_fields = ["first_name", "last_name", "age", "username",
                           "website_auth_code", "gender", "password"]

        for f in required_fields:
            if f not in data or not data[f]:
                return {"message": f"{f} is required"}, 400

        # Validate username
        if AdminModel.find_by_username(data["username"]):
            return {"message": "Username already exists"}, 400

        # Validate website auth code from DB
        if not AdminModel.is_valid_auth_code(data["website_auth_code"]):
            return {"message": "Invalid website authentication code"}, 403

        # Clean DOB
        data["dob"] = data.get("dob") or None

        # Hash password
        data["password"] = bcrypt.generate_password_hash(data["password"]).decode()

        if not AdminModel.create_admin(data):
            return {"message": "Database error, registration failed"}, 500

        return {"message": "Admin Registered Successfully"}, 201


    @staticmethod
    def login(data):
        """Login as admin and return JWT token and status code."""

        # Find admin
        admin = AdminModel.find_by_username(data["username"])

        if not admin:
            return {"message": "Admin not found"}, 404

        # Check password
        if not bcrypt.check_password_hash(admin["password"], data["password"]):
            return {"message": "Incorrect password"}, 401

        # Create JWT
        token = jwt.encode(
            {
                "id": admin["id"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
            },
            Config.SECRET_KEY,
            algorithm="HS256"
        )

        return {
            "message": "Login successful",
            "token": token,
            "username": admin["username"]
        }, 200

    @staticmethod
    def get_all_drivers():
        """Return all drivers."""
        drivers = DriverModel.get_all_drivers()
        return {"drivers": drivers}, 200

    @staticmethod
    def assign_driver(driver_id):
        """Assign a driver and remove from drivers table."""
        driver = DriverModel.find_by_id(driver_id)
        if not driver:
            return {"message": "Driver not found"}, 404

        # Insert into assigned_drivers table
        AssignedDriverModel.create_assigned_driver(driver)

        # Remove from drivers table
        DriverModel.delete_driver(driver_id)

        return {"message": "Driver assigned and removed from drivers table"}, 200

    @staticmethod
    def delete_driver(driver_id):
        """Delete a driver by ID."""
        success = DriverModel.delete_driver(driver_id)
        if success:
            return {"message": "Driver deleted successfully"}, 200
        return {"message": "Driver not found"}, 404
