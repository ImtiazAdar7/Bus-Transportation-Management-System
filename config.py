# Author: Imtiaz Ahmed 2013552642
import mysql.connector

class Config:
    SECRET_KEY = "busmanagement-secret-key"
    PROD_DB = "bus_management"
    TEST_DB = "bus_management_test"

    @staticmethod
    def get_db(test=False):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=Config.TEST_DB if test else Config.PROD_DB
        )