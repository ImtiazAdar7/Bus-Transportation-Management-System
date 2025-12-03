# Author: Imtiaz Ahmed 2013552642
from config import Config

class PassengerModel:
    """Model to manage passengers."""
    @staticmethod
    def find_by_email(email):
        """
        Find a passenger by email address.

        Args:
            email (str): Email address of the passenger

        Returns:
            dict or None: Passenger dictionary if found, None otherwise
        """
        db = Config.get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM passengers WHERE email = %s", (email,))
        user = cursor.fetchone()

        cursor.close()
        db.close()
        return user

    @staticmethod
    def create_passenger(data):
        """
        Insert a new passenger record into the database.

        Args:
            data (dict): Passenger details with keys:
                - first_name (str)
                - last_name (str)
                - age (str)
                - username (str)
                - email (str)
                - dob (str, optional)
                - gender (str)
                - password (str): Hashed password

        Returns:
            bool: True if successful
        """
        db = Config.get_db()
        cursor = db.cursor()

        sql = """
        INSERT INTO passengers
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
