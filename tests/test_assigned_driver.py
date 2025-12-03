"""
Author: Test Suite
Unit tests for assigned driver functionality.

To run these tests:
    python -m pytest tests/test_assigned_driver.py -v
    OR
    python tests/test_assigned_driver.py
"""

import sys
import os

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.driver_model import DriverModel
from models.assigned_driver_model import AssignedDriverModel
from controllers.admin_controllers import AdminController


def test_get_all_assigned_drivers():
    """Test retrieving all assigned drivers."""
    assigned_drivers = AssignedDriverModel.get_all_assigned_drivers()
    
    assert isinstance(assigned_drivers, list)
    print("✓ Retrieved all assigned drivers successfully")


def test_assign_driver_workflow():
    """Test the complete workflow of assigning a driver."""
    # Create a driver
    driver_data = {
        "first_name": "Assigned",
        "last_name": "Driver",
        "age": "35",
        "username": "assigned_driver_test",
        "email": "assigned_driver_test@gmail.com",
        "dob": None,
        "gender": "Male",
        "password": "driverpass123"
    }
    DriverModel.create_driver(driver_data)
    
    # Find the driver
    driver = DriverModel.find_by_email("assigned_driver_test@gmail.com")
    assert driver is not None
    driver_id = driver["id"]
    
    # Assign the driver
    response, status = AdminController.assign_driver(driver_id)
    
    assert status == 200
    assert "assigned" in response["message"].lower()
    
    # Driver should be removed from drivers table
    assert DriverModel.find_by_id(driver_id) is None
    
    # Driver should be in assigned_drivers table
    assigned_drivers = AssignedDriverModel.get_all_assigned_drivers()
    assigned_driver = next((d for d in assigned_drivers if d["id"] == driver_id), None)
    assert assigned_driver is not None
    assert assigned_driver["email"] == "assigned_driver_test@gmail.com"
    
    print("✓ Driver assignment workflow completed successfully")


def test_assign_nonexistent_driver():
    """Test assigning a driver that doesn't exist."""
    invalid_driver_id = 99999
    
    response, status = AdminController.assign_driver(invalid_driver_id)
    
    assert status == 404
    assert "not found" in response["message"].lower()
    print("✓ Non-existent driver assignment correctly rejected")


def test_assigned_driver_data_integrity():
    """Test that assigned driver data is preserved correctly."""
    # Create a driver
    driver_data = {
        "first_name": "Data",
        "last_name": "Test",
        "age": "40",
        "username": "data_test_driver",
        "email": "data_test_driver@gmail.com",
        "dob": None,
        "gender": "Female",
        "password": "testpass123"
    }
    DriverModel.create_driver(driver_data)
    
    # Get original driver data
    original_driver = DriverModel.find_by_email("data_test_driver@gmail.com")
    driver_id = original_driver["id"]
    
    # Assign driver
    AdminController.assign_driver(driver_id)
    
    # Check assigned driver data
    assigned_drivers = AssignedDriverModel.get_all_assigned_drivers()
    assigned_driver = next((d for d in assigned_drivers if d["id"] == driver_id), None)
    
    assert assigned_driver is not None
    assert assigned_driver["first_name"] == original_driver["first_name"]
    assert assigned_driver["last_name"] == original_driver["last_name"]
    assert assigned_driver["email"] == original_driver["email"]
    assert assigned_driver["username"] == original_driver["username"]
    
    print("✓ Assigned driver data integrity verified")


# Run all tests
if __name__ == "__main__":
    print("\n=== Running Assigned Driver Tests ===\n")
    
    try:
        test_get_all_assigned_drivers()
        test_assign_driver_workflow()
        test_assign_nonexistent_driver()
        test_assigned_driver_data_integrity()
        
        print("\nAll assigned driver tests passed!\n")
    except AssertionError as e:
        print(f"\n Test failed: {e}\n")
    except Exception as e:
        print(f"\n Error running tests: {e}\n")

