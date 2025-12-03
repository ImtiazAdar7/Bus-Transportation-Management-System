# Author: Imtiaz Ahmed 2013552642
from config import Config

class PassengerModel:
    """Model to manage passengers."""
    @staticmethod
    def find_by_email(email):
        """Find a passenger by email."""
        db = Config.get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM passengers WHERE email = %s", (email,))
        user = cursor.fetchone()

        cursor.close()
        db.close()
        return user

    @staticmethod
    def create_passenger(data):
        """Insert a new passenger record."""
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
