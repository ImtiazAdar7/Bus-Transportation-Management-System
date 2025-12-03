# Author: Imtiaz Ahmed 2013552642
from config import Config
from typing import List, Dict, Optional

class BookingModel:
    """Model to manage bookings."""
    
    @staticmethod
    def create_table():
        """
        Create bookings table if it doesn't exist.

        Creates table with foreign key constraints if referenced tables exist,
        otherwise creates without foreign keys.
        """
        db = Config.get_db()
        cursor = db.cursor()
        
        try:
            # Try to create with foreign keys first
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                bus_route_id INT NOT NULL,
                passenger_id INT NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                KEY bus_route_id (bus_route_id),
                KEY passenger_id (passenger_id),
                CONSTRAINT fk_bookings_bus_route FOREIGN KEY (bus_route_id) 
                    REFERENCES bus_routes(id) ON DELETE CASCADE ON UPDATE CASCADE,
                CONSTRAINT fk_bookings_passenger FOREIGN KEY (passenger_id) 
                    REFERENCES passengers(id) ON DELETE CASCADE ON UPDATE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
            """)
            db.commit()
        except Exception:
            # If foreign keys fail (e.g., referenced tables don't exist yet), create without them
            try:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS bookings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    bus_route_id INT NOT NULL,
                    passenger_id INT NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    KEY bus_route_id (bus_route_id),
                    KEY passenger_id (passenger_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
                """)
                db.commit()
            except Exception:
                # Table might already exist, which is fine
                db.rollback()
        finally:
            cursor.close()
            db.close()
    
    @staticmethod
    def create_booking(bus_route_id: int, passenger_id: int, price: float) -> int:
        """
        Create a new booking and return the booking ID.

        Args:
            bus_route_id (int): ID of the bus route being booked.
            passenger_id (int): ID of the passenger making the booking.
            price (float): Price of the booking.

        Returns:
            int: The ID of the newly created booking.
        """
        # Ensure table exists before creating booking
        BookingModel.create_table()
        
        db = Config.get_db()
        cursor = db.cursor()
        
        sql = """
        INSERT INTO bookings (bus_route_id, passenger_id, price)
        VALUES (%s, %s, %s)
        """
        
        cursor.execute(sql, (bus_route_id, passenger_id, price))
        db.commit()
        booking_id = cursor.lastrowid
        
        cursor.close()
        db.close()
        return booking_id
    
    @staticmethod
    def get_bookings_by_passenger(passenger_id: int) -> List[Dict]:
        """
        Get all bookings for a specific passenger with route details.

        Args:
            passenger_id (int): ID of the passenger.

        Returns:
            List[Dict]: List of booking dictionaries with route information.
                       Each booking includes booking_id, bus_route_id, passenger_id,
                       price, operator, route, departure_time, and capacity.

        Raises:
            Exception: If database error occurs.
        """
        # Ensure table exists before querying
        BookingModel.create_table()
        
        db = Config.get_db()
        cursor = db.cursor(dictionary=True)
        
        try:
            sql = """
            SELECT 
                b.id as booking_id,
                b.bus_route_id,
                b.passenger_id,
                b.price,
                br.brand as operator,
                br.route,
                br.time as departure_time,
                br.capacity
            FROM bookings b
            JOIN bus_routes br ON b.bus_route_id = br.id
            WHERE b.passenger_id = %s
            ORDER BY b.id DESC
            """
            
            cursor.execute(sql, (passenger_id,))
            bookings = cursor.fetchall()
            
            # Convert Decimal to float for JSON serialization
            for booking in bookings:
                if 'price' in booking and booking['price'] is not None:
                    booking['price'] = float(booking['price'])
                if 'departure_time' in booking and booking['departure_time'] is not None:
                    booking['departure_time'] = str(booking['departure_time'])
            
            return bookings
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
        finally:
            cursor.close()
            db.close()
    
    @staticmethod
    def get_booking_by_id(booking_id: int) -> Optional[Dict]:
        """
        Get a booking by its ID.

        Args:
            booking_id (int): The ID of the booking to retrieve.

        Returns:
            Optional[Dict]: Booking dictionary if found, None otherwise.
        """
        # Ensure table exists before querying
        BookingModel.create_table()
        
        db = Config.get_db()
        cursor = db.cursor(dictionary=True)
        
        sql = "SELECT * FROM bookings WHERE id = %s"
        cursor.execute(sql, (booking_id,))
        booking = cursor.fetchone()
        
        cursor.close()
        db.close()
        return booking

