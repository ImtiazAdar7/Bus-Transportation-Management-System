from controllers.passenger_controller import PassengerController
from models.passenger_model import PassengerModel
from models.booking_model import BookingModel
from models.bus_route_model import BusRouteModel

def test_passenger_register_and_login():
    passenger_data = {
        "first_name": "Muhammamd Ali",
        "last_name": "Jinnah",
        "age": "55",
        "username": "jinnah",
        "email": "jinnah@gmail.com",
        "dob": None,
        "gender": "Male",
        "password": "quaid"
    }

    # Register
    resp, status = PassengerController.register(passenger_data)
    assert status == 201

    # Login
    login_data = {"email": "jinnah@gmail.com", "password": "quaid"}
    resp, status = PassengerController.login(login_data)
    assert status == 200
    assert "token" in resp


def test_create_booking():
    """Test creating a new booking for a passenger."""
    # First, register and login a passenger
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
    login_resp, _ = PassengerController.login({
        "email": "testuser_booking@gmail.com",
        "password": "testpass123"
    })
    token = login_resp.get_json()["token"]
    
    # Get a bus route to book
    routes = BusRouteModel.get_all_routes()
    assert len(routes) > 0, "No routes available for testing"
    route_id = routes[0]["id"]
    
    # Create booking
    booking_data = {
        "bus_route_id": route_id,
        "price": 500.00
    }
    resp, status = PassengerController.create_booking(booking_data, token)
    
    assert status == 201
    assert "booking_id" in resp.get_json()
    booking_id = resp.get_json()["booking_id"]
    assert isinstance(booking_id, int)
    assert booking_id > 0


def test_get_my_bookings():
    """Test retrieving all bookings for a passenger."""
    # Register and login a passenger
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
    login_resp, _ = PassengerController.login({
        "email": "booking_tester@gmail.com",
        "password": "testpass456"
    })
    token = login_resp.get_json()["token"]
    
    # Get passenger ID from token
    passenger_id = PassengerController._verify_token(token)
    assert passenger_id is not None
    
    # Get available routes
    routes = BusRouteModel.get_all_routes()
    assert len(routes) > 0, "No routes available for testing"
    
    # Create multiple bookings
    booking_ids = []
    for i, route in enumerate(routes[:3]):  # Create up to 3 bookings
        booking_id = BookingModel.create_booking(
            route["id"],
            passenger_id,
            500.00 + (i * 100)  # Different prices
        )
        booking_ids.append(booking_id)
    
    # Retrieve bookings
    resp, status = PassengerController.get_my_bookings(token)
    assert status == 200
    
    bookings = resp.get_json()["bookings"]
    assert isinstance(bookings, list)
    assert len(bookings) >= len(booking_ids)
    
    # Verify booking structure
    if len(bookings) > 0:
        booking = bookings[0]
        assert "booking_id" in booking
        assert "bus_route_id" in booking
        assert "passenger_id" in booking
        assert "price" in booking
        assert "operator" in booking
        assert "route" in booking


def test_bookings_sorted_by_newest_first():
    """Test that bookings are sorted by newest first (booking ID descending)."""
    # Register and login a passenger
    passenger_data = {
        "first_name": "Sort",
        "last_name": "Tester",
        "age": "28",
        "username": "sort_tester",
        "email": "sort_tester@gmail.com",
        "dob": None,
        "gender": "Male",
        "password": "testpass789"
    }
    
    PassengerController.register(passenger_data)
    login_resp, _ = PassengerController.login({
        "email": "sort_tester@gmail.com",
        "password": "testpass789"
    })
    token = login_resp.get_json()["token"]
    
    # Get passenger ID
    passenger_id = PassengerController._verify_token(token)
    
    # Get available routes
    routes = BusRouteModel.get_all_routes()
    assert len(routes) >= 2, "Need at least 2 routes for sorting test"
    
    # Create multiple bookings with a small delay to ensure different IDs
    booking_ids = []
    for route in routes[:3]:
        booking_id = BookingModel.create_booking(
            route["id"],
            passenger_id,
            600.00
        )
        booking_ids.append(booking_id)
    
    # Retrieve bookings
    resp, status = PassengerController.get_my_bookings(token)
    assert status == 200
    
    bookings = resp.get_json()["bookings"]
    assert len(bookings) >= len(booking_ids)
    
    # Verify bookings are sorted by booking_id descending (newest first)
    if len(bookings) >= 2:
        booking_ids_from_response = [b["booking_id"] for b in bookings if b["booking_id"] in booking_ids]
        # Check that they are in descending order
        for i in range(len(booking_ids_from_response) - 1):
            assert booking_ids_from_response[i] >= booking_ids_from_response[i + 1], \
                "Bookings should be sorted by newest first (descending booking_id)"
