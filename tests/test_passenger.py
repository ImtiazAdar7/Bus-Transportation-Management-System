from controllers.passenger_controller import PassengerController
from models.passenger_model import PassengerModel

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
