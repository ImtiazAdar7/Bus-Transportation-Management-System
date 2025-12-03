# Author: Imtiaz Ahmed 2013552642
from config import Config
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class AdminModel:
    """Model to manage admin data and authentication codes."""

    @staticmethod
    def create_tables():
        """Create admins and website_auth_codes tables if they don't exist."""
        db = Config.get_db()
        cursor = db.cursor()

        # Admins table
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
        )
        """)

        # Website auth code table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS website_auth_codes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            code VARCHAR(100) UNIQUE NOT NULL
        )
        """)

        db.commit()
        cursor.close()
        db.close()


    @staticmethod
    def insert_default_codes():
        """Insert default website auth codes."""
        db = Config.get_db()
        cursor = db.cursor()

        cursor.execute("""
        INSERT IGNORE INTO website_auth_codes (code)
        VALUES ('cse327proj'), ('mma3'), ('bus_management')
        """)

        db.commit()
        cursor.close()
        db.close()


    @staticmethod
    def is_valid_auth_code(code):
        """Check if a website auth code exists in DB."""
        db = Config.get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM website_auth_codes WHERE code=%s", (code,))
        found = cursor.fetchone()

        cursor.close()
        db.close()

        return found is not None


    @staticmethod
    def find_by_username(username):
        """Find an admin by username."""
        db = Config.get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM admins WHERE username=%s", (username,))
        admin = cursor.fetchone()

        cursor.close()
        db.close()

        return admin


    @staticmethod
    def create_admin(data):
        """Insert a new admin record into DB."""
        db = Config.get_db()
        cursor = db.cursor()

        sql = """
        INSERT INTO admins
        (first_name, last_name, age, username, website_auth_code, dob, gender, password)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            data["first_name"], data["last_name"], data["age"],
            data["username"], data["website_auth_code"],
            data["dob"], data["gender"], data["password"]
        )

        try:
            cursor.execute(sql, values)
            db.commit()
            success = True
        except Exception as e:
            print("DB ERROR:", e)
            db.rollback()
            success = False

        cursor.close()
        db.close()
        return success
