from flask import Flask, redirect, url_for, session, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from routes.passenger_routes import passenger_bp
from routes.admin_routes import admin_bp
from routes.driver_routes import driver_bp
from routes.route_routes import route_bp
from routes.analytics_routes import analytics_bp

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)  # IMPORTANT!
app.config["SECRET_KEY"] = "busmanagement-secret-key"

app.register_blueprint(passenger_bp)

app.register_blueprint(admin_bp)

app.register_blueprint(driver_bp)

app.register_blueprint(route_bp)

app.register_blueprint(analytics_bp)

@app.get("/")
def home():
    """
    Home endpoint for the Bus Management System API.

    Returns:
        dict: A welcome message for the Bus Management System Project.
    """
    return {"message": "Bus Management System Project For CSE327"}

if __name__ == "__main__":
    app.run(debug=True)
