from controllers.driver_controllers import DriverController
from models.driver_model import DriverModel

def test_driver_register_and_login():
    driver_data = {
        "first_name": "Faruk",
        "last_name": "Khan",
        "age": "31",
        "username": "faruk_driver",
        "email": "faruk@gmail.com",
        "dob": None,
        "gender": "Male",
        "password": "faruk123"
    }

    # Register
    resp, status = DriverController.register(driver_data)
    assert status == 201

    # Login
    login_data = {"email": "faruk@gmail.com", "password": "faruk123"}
    resp, status = DriverController.login(login_data)
    assert status == 200
    assert "token" in resp
