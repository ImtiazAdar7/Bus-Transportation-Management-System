import mysql.connector
from datetime import datetime, timedelta
from mysql.connector import Error

# --- SQL to create helper tables (run once in your DB) ---
#
# CREATE TABLE seat_reservations (
#   id INT AUTO_INCREMENT PRIMARY KEY,
#   bus_id INT NOT NULL,
#   seat_no VARCHAR(16) NOT NULL,
#   passenger_id INT NULL,
#   session_id VARCHAR(64) NOT NULL,
#   reserved_at DATETIME NOT NULL,
#   expires_at DATETIME NOT NULL,
#   UNIQUE KEY ux_bus_seat (bus_id, seat_no)
# );
#
# CREATE TABLE bookings (
#   id INT AUTO_INCREMENT PRIMARY KEY,
#   passenger_id INT NOT NULL,
#   bus_id INT NOT NULL,
#   seat_no VARCHAR(16) NOT NULL,
#   travel_date DATE NOT NULL,
#   fare DECIMAL(10,2) NOT NULL,
#   payment_status VARCHAR(32) NOT NULL,
#   transaction_id VARCHAR(128),
#   booked_at DATETIME DEFAULT CURRENT_TIMESTAMP
# );
#
# Update the rest of your schema for buses/seats as appropriate.
# ---------------------------------------------------------------

class SeatModel:
    def __init__(self, mysql_config):
        self.mysql_config = mysql_config

    def _get_conn(self):
        return mysql.connector.connect(**self.mysql_config)

    def find_buses(self, source, destination, travel_date):
        sql = """
        SELECT b.id AS bus_id, b.name AS bus_name, b.departure_time, b.arrival_time, b.fare
        FROM buses b
        WHERE b.source=%s AND b.destination=%s
        ORDER BY b.departure_time;
        """
        try:
            conn = self._get_conn()
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, (source, destination))
            rows = cur.fetchall()
            cur.close()
            conn.close()
            # attach travel_date for front-end
            for r in rows:
                r['travel_date'] = str(travel_date)
            return rows
        except Error as e:
            raise

    def get_seat_layout(self, bus_id, travel_date):
        seats_sql = "SELECT seat_no, row_pos, col_pos FROM seats WHERE bus_id=%s ORDER BY seat_no;"
        booked_sql = "SELECT seat_no FROM bookings WHERE bus_id=%s AND travel_date=%s;"
        reserved_sql = "SELECT seat_no, session_id, expires_at FROM seat_reservations WHERE bus_id=%s AND expires_at > NOW();"

        try:
            conn = self._get_conn()
            cur = conn.cursor(dictionary=True)
            cur.execute(seats_sql, (bus_id,))
            seats = cur.fetchall()

            cur.execute(booked_sql, (bus_id, travel_date))
            booked_rows = cur.fetchall()
            booked_set = {r['seat_no'] for r in booked_rows}

            cur.execute(reserved_sql, (bus_id,))
            reserved_rows = cur.fetchall()
            reserved_map = {r['seat_no']: {'session_id': r['session_id'], 'expires_at': r['expires_at']} for r in reserved_rows}

            layout = []
            for s in seats:
                seat_no = s['seat_no']
                status = 'available'
                meta = {}
                if seat_no in booked_set:
                    status = 'booked'
                elif seat_no in reserved_map:
                    status = 'reserved'
                    meta = reserved_map[seat_no]
                layout.append({
                    'seat_no': seat_no,
                    'status': status,
                    'meta': meta,
                    'row_pos': s.get('row_pos'),
                    'col_pos': s.get('col_pos'),
                })

            cur.close()
            conn.close()
            return layout
        except Error as e:
            raise

    def lock_seat(self, bus_id, seat_no, session_id, passenger_id=None, lock_seconds=300):
        expires_at = datetime.utcnow() + timedelta(seconds=lock_seconds)
        try:
            conn = self._get_conn()
            cur = conn.cursor()
            conn.start_transaction()

            cur.execute("SELECT COUNT(1) FROM bookings WHERE bus_id=%s AND seat_no=%s;", (bus_id, seat_no))
            booked_count = cur.fetchone()[0]
            if booked_count > 0:
                conn.rollback()
                cur.close()
                conn.close()
