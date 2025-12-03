import mysql.connector
from datetime import datetime
from mysql.connector import Error

class BookingModel:
    def __init__(self, mysql_config):
        self.mysql_config = mysql_config

    def _get_conn(self):
        return mysql.connector.connect(**self.mysql_config)

    def confirm_booking(self, session_id, passenger_id, travel_date, payment_status, transaction_id=None):
        try:
            conn = self._get_conn()
            cur = conn.cursor(dictionary=True)
            conn.start_transaction()

            cur.execute("SELECT bus_id, seat_no FROM seat_reservations WHERE session_id=%s AND expires_at > NOW() FOR UPDATE;", (session_id,))
            reserved = cur.fetchall()
            if not reserved:
                conn.rollback()
                cur.close()
                conn.close()
                return False, "No active reservation found (maybe expired).", []

            created = []
            for r in reserved:
                bus_id = r['bus_id']
                seat_no = r['seat_no']

                cur.execute("SELECT COUNT(1) AS c FROM bookings WHERE bus_id=%s AND seat_no=%s AND travel_date=%s;", (bus_id, seat_no, travel_date))
                if cur.fetchone()['c'] > 0:
                    conn.rollback()
                    cur.close()
                    conn.close()
                    return False, f"Seat {seat_no} is already booked.", []

                fare = 0.0
                cur.execute("SELECT fare FROM buses WHERE id=%s LIMIT 1;", (bus_id,))
                row = cur.fetchone()
                if row and row.get('fare') is not None:
                    fare = row['fare']

                cur.execute(
                    "INSERT INTO bookings (passenger_id, bus_id, seat_no, travel_date, fare, payment_status, transaction_id, booked_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                    (passenger_id, bus_id, seat_no, travel_date, fare, payment_status, transaction_id, datetime.utcnow())
                )
                booking_id = cur.lastrowid
                created.append({
                    'booking_id': booking_id,
                    'bus_id': bus_id,
                    'seat_no': seat_no,
                    'fare': fare
                })

            cur.execute("DELETE FROM seat_reservations WHERE session_id=%s;", (session_id,))

            conn.commit()
            cur.close()
            conn.close()
            return True, "Booking confirmed.", created
        except Error as e:
            try:
                conn.rollback()
            except:
                pass
            raise
