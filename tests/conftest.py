import os
import sys
import pytest

# project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import Config
from controllers.admin_controllers import AdminController
from models.driver_model import DriverModel
from models.passenger_model import PassengerModel
from models.assigned_driver_model import AssignedDriverModel

@pytest.fixture(scope="session")
def db():
    conn = Config.get_db(test=True)
    yield conn
    conn.close()



@pytest.fixture(autouse=True)
def setup_and_clean_db(db):
    cursor = db.cursor()

    # Create tables if they don't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        age VARCHAR(10),
        username VARCHAR(100) UNIQUE,
        website_auth_code VARCHAR(50),
        dob DATE NULL,
        gender VARCHAR(20),
        password VARCHAR(255)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS website_auth_codes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        code VARCHAR(100) UNIQUE NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drivers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        age VARCHAR(10),
        username VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        dob DATE NULL,
        gender VARCHAR(20),
        password VARCHAR(255)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assigned_drivers (
        id INT PRIMARY KEY,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        age VARCHAR(10),
        username VARCHAR(100),
        email VARCHAR(100),
        dob DATE NULL,
        gender VARCHAR(20),
        password VARCHAR(255)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passengers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        age VARCHAR(10),
        username VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        dob DATE NULL,
        gender VARCHAR(20),
        password VARCHAR(255)
    )""")

    # Insert default auth codes if missing
    cursor.execute("""
    INSERT IGNORE INTO website_auth_codes (code)
    VALUES ('cse327proj'), ('mma3'), ('bus_management')
    """)

    db.commit()

    # Clean tables
    for table in ["admins", "drivers", "assigned_drivers", "passengers"]:
        cursor.execute(f"DELETE FROM {table}")

    db.commit()
    cursor.close()