# Author: Imtiaz Ahmed 2013552642
from config import Config

class AssignedDriverModel:
    """Model to manage assigned drivers."""
    @staticmethod
    def create_assigned_driver(driver):
        """Assign a driver to the assigned_drivers table."""
        db = Config.get_db()
        cursor = db.cursor()

        sql = """
        INSERT INTO assigned_drivers 
        (id, first_name, last_name, age, username, email, dob, gender, password)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        values = (
            driver["id"], driver["first_name"], driver["last_name"], driver["age"],
            driver["username"], driver["email"], driver["dob"],
            driver["gender"], driver["password"]
        )
        cursor.execute(sql, values)
        db.commit()
        cursor.close()
        db.close()
        return True

    @staticmethod
    def get_all_assigned_drivers():
        """Return all assigned drivers."""
        db = Config.get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM assigned_drivers")
        drivers = cursor.fetchall()
        cursor.close()
        db.close()
        return drivers
