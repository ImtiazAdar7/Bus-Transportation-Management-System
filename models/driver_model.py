# Author: Imtiaz Ahmed 2013552642
from config import Config

class DriverModel:
    """Model to manage drivers."""
    @staticmethod
    def find_by_email(email):
        """Find a driver by email."""
        db = Config.get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM drivers WHERE email=%s", (email,))
        driver = cursor.fetchone()
        cursor.close()
        db.close()
        return driver

    @staticmethod
    def create_driver(data):
        """Insert a new driver record."""
        db = Config.get_db()
        cursor = db.cursor()

        sql = """
        INSERT INTO drivers
        (first_name, last_name, age, username, email, dob, gender, password)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """
        values = (
            data["first_name"], data["last_name"], data["age"],
            data["username"], data["email"], data["dob"],
            data["gender"], data["password"]
        )
        cursor.execute(sql, values)
        db.commit()
        cursor.close()
        db.close()
        return True

    @staticmethod
    def get_all_drivers():
        """Return all drivers."""
        db = Config.get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM drivers")
        drivers = cursor.fetchall()
        cursor.close()
        db.close()
        return drivers

    @staticmethod
    def find_by_id(driver_id):
        """Find a driver by ID."""
        db = Config.get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM drivers WHERE id=%s", (driver_id,))
        driver = cursor.fetchone()
        cursor.close()
        db.close()
        return driver

    @staticmethod
    def delete_driver(driver_id):
        """Delete a driver by ID."""
        db = Config.get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM drivers WHERE id=%s", (driver_id,))
        db.commit()
        rows = cursor.rowcount
        cursor.close()
        db.close()
        return rows > 0