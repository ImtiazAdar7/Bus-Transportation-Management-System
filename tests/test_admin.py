import pytest
from controllers.admin_controllers import AdminController
from models.driver_model import DriverModel

def test_admin_register_success():
    data = {
        "first_name": "adarbhaiya",
        "last_name": "adar1",
        "age": "26",
        "username": "adarbhaiya",
        "website_auth_code": "cse327proj",
        "gender": "Male",
        "password": "adarbhaiya",
        "dob": None
    }
    response, status = AdminController.register(data)
    assert status == 201
    assert response["message"] == "Admin Registered Successfully"

def test_admin_login_success():
    # First, register
    data = {
        "first_name": "Adarbhaiya",
        "last_name": "Test Kore",
        "age": "30",
        "username": "bhaiya",
        "website_auth_code": "cse327proj",
        "gender": "Male",
        "password": "bhaiya1",
        "dob": None
    }
    AdminController.register(data)

    # Now login
    login_data = {"username": "bhaiya", "password": "bhaiya1"}
    resp, status = AdminController.login(login_data)
    assert status == 200
    assert "token" in resp

def test_assign_driver_and_remove():
    # Create driver
    driver_data = {
        "first_name": "Kalam",
        "last_name": "Mia",
        "age": "40",
        "username": "kalam123",
        "email": "kalam@gmail.com",
        "dob": None,
        "gender": "Male",
        "password": "kalam"
    }
    DriverModel.create_driver(driver_data)
    driver = DriverModel.find_by_email("kalam@gmail.com")
    driver_id = driver["id"]

    # Assign driver
    resp, status = AdminController.assign_driver(driver_id)
    assert status == 200
    assert "assigned" in resp["message"]

    # Driver should be removed from original table
    assert DriverModel.find_by_id(driver_id) is None
