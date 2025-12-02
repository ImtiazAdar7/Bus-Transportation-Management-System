from flask import Flask, redirect, url_for, session, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from routes.passenger_routes import passenger_bp
from routes.admin_routes import admin_bp
from routes.driver_routes import driver_bp

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)   # IMPORTANT!
app.config["SECRET_KEY"] = "busmanagement-secret-key"

app.register_blueprint(passenger_bp)

app.register_blueprint(admin_bp)

app.register_blueprint(driver_bp)


@app.get("/")
def home():
    return {"message": "Bus Management System Project For CSE327"}

if __name__ == "__main__":
    app.run(debug=True)
