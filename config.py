# Author: Imtiaz Ahmed 2013552642
import mysql.connector

class Config:
    SECRET_KEY = "busmanagement-secret-key"
    PROD_DB = "bus_management"
    TEST_DB = "bus_management_test"

    @staticmethod
    def get_db(test=False):
        """
        Get a database connection.

        Args:
            test (bool): If True, connects to test database, otherwise production database.

        Returns:
            mysql.connector.connection.MySQLConnection: Database connection object.
        """
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=Config.TEST_DB if test else Config.PROD_DB
        )