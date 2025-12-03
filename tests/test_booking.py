"""
Author: Test Suite
Unit tests for booking functionality.

To run these tests:
    python -m pytest tests/test_booking.py -v
    OR
    python tests/test_booking.py
"""

import sys
import os

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from controllers.passenger_controller import PassengerController
from models.passenger_model import PassengerModel
from models.booking_model import BookingModel
from models.bus_route_model import BusRouteModel
import jwt
from config import Config
import datetime


def test_create_booking_success():
    """Test creating a booking successfully."""
    # First, create a passenger
    passenger_data = {
        "first_name": "Test",
        "last_name": "User",
        "age": "25",
        "username": "testuser_booking",
        "email": "testuser_booking@gmail.com",
        "dob": None,
        "gender": "Male",
        "password": "testpass123"
    }
    PassengerController.register(passenger_data)
    
    # Get passenger ID
    passenger = PassengerModel.find_by_email("testuser_booking@gmail.com")
    passenger_id = passenger["id"]
    
    # Create a token for the passenger
    token = jwt.encode(
        {
            "id": passenger_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        },
        Config.SECRET_KEY,
        algorithm="HS256"
    )
    
    # Get a route to book
    routes = BusRouteModel.get_all_routes()
    if len(routes) > 0:
        route_id = routes[0]["id"]
        price = 500.0
        
        # Create booking
        booking_data = {
            "bus_route_id": route_id,
            "price": price
        }
        
        response, status = PassengerController.create_booking(booking_data, token)
        
        assert status == 201
        assert "booking_id" in response.get_json()
        print("✓ Booking created successfully")


def test_get_my_bookings():
    """Test retrieving bookings for a passenger."""
    # Create a passenger
    passenger_data = {
        "first_name": "Booking",
        "last_name": "Tester",
        "age": "30",
        "username": "booking_tester",
        "email": "booking_tester@gmail.com",
        "dob": None,
        "gender": "Female",
        "password": "testpass456"
    }
    PassengerController.register(passenger_data)
    
    # Get passenger ID
    passenger = PassengerModel.find_by_email("booking_tester@gmail.com")
    passenger_id = passenger["id"]
    
    # Create a token
    token = jwt.encode(
        {
            "id": passenger_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        },
        Config.SECRET_KEY,
        algorithm="HS256"
    )
    
    # Get bookings
    response, status = PassengerController.get_my_bookings(token)
    
    assert status == 200
    assert "bookings" in response.get_json()
    print("✓ Retrieved bookings successfully")


def test_create_booking_unauthorized():
    """Test creating a booking without authentication."""
    booking_data = {
        "bus_route_id": 1,
        "price": 500.0
    }
    
    # Try with invalid token
    response, status = PassengerController.create_booking(booking_data, "invalid_token")
    
    assert status == 401
    print("✓ Unauthorized booking correctly rejected")


def test_booking_model_get_booking_by_id():
    """Test getting a booking by ID."""
    # Create a passenger
    passenger_data = {
        "first_name": "Model",
        "last_name": "Test",
        "age": "28",
        "username": "model_test",
        "email": "model_test@gmail.com",
        "dob": None,
        "gender": "Male",
        "password": "testpass789"
    }
    PassengerModel.create_passenger(passenger_data)
    passenger = PassengerModel.find_by_email("model_test@gmail.com")
    passenger_id = passenger["id"]
    
    # Get a route
    routes = BusRouteModel.get_all_routes()
    if len(routes) > 0:
        route_id = routes[0]["id"]
        
        # Create booking directly via model
        booking_id = BookingModel.create_booking(route_id, passenger_id, 600.0)
        
        # Retrieve booking
        booking = BookingModel.get_booking_by_id(booking_id)
        
        assert booking is not None
        assert booking["bus_route_id"] == route_id
        assert booking["passenger_id"] == passenger_id
        assert float(booking["price"]) == 600.0
        print("✓ Booking retrieved by ID successfully")


# Run all tests
if __name__ == "__main__":
    print("\n=== Running Booking Tests ===\n")
    
    try:
        test_create_booking_success()
        test_get_my_bookings()
        test_create_booking_unauthorized()
        test_booking_model_get_booking_by_id()
        
        print("\nAll booking tests passed!\n")
    except AssertionError as e:
        print(f"\n Test failed: {e}\n")
    except Exception as e:
        print(f"\n Error running tests: {e}\n")

