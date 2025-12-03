from flask import Blueprint, request, jsonify, current_app
import uuid
from datetime import datetime
from models.seat_model import SeatModel
from models.booking_model import BookingModel

bp = Blueprint('passenger', __name__, url_prefix='/api/passenger')

def _get_mysql_config():
    # expects MYSQL_CONFIG dict in config.py
    return current_app.config.get('MYSQL_CONFIG')

# Initialize models inside requests
def _seat_model():
    return SeatModel(_get_mysql_config())

def _booking_model():
    return BookingModel(_get_mysql_config())

@bp.route('/search_buses', methods=['POST'])
def search_buses():
    data = request.get_json() or {}
    source = data.get('source')
    destination = data.get('destination')
    travel_date = data.get('travel_date')
    if not source or not destination or not travel_date:
        return jsonify({'success': False, 'message': 'source, destination and travel_date are required'}), 400
    try:
        seats = _seat_model().find_buses(source, destination, travel_date)
        return jsonify({'success': True, 'buses': seats})
    except Exception as e:
        current_app.logger.exception("Error searching buses")
        return jsonify({'success': False, 'message': 'Unable to fetch buses. Please try again later.'}), 500

@bp.route('/seat_layout', methods=['GET'])
def seat_layout():
    """
    Query params: bus_id, travel_date
    """
    bus_id = request.args.get('bus_id')
    travel_date = request.args.get('travel_date')
    if not bus_id or not travel_date:
        return jsonify({'success': False, 'message': 'bus_id and travel_date are required'}), 400
    try:
        layout = _seat_model().get_seat_layout(bus_id, travel_date)
        return jsonify({'success': True, 'layout': layout})
    except Exception as e:
        current_app.logger.exception("Error loading seat layout")
        return jsonify({'success': False, 'message': 'Unable to fetch seat details. Please check your internet connection or try again later.'}), 500

@bp.route('/lock_seat', methods=['POST'])
def lock_seat():
    data = request.get_json() or {}
    bus_id = data.get('bus_id')
    seat_no = data.get('seat_no')
    passenger_id = data.get('passenger_id')
    session_id = data.get('session_id') or str(uuid.uuid4())
    if not bus_id or not seat_no:
        return jsonify({'success': False, 'message': 'bus_id and seat_no are required'}), 400
    try:
        ok, msg = _seat_model().lock_seat(bus_id, seat_no, session_id, passenger_id)
        if ok:
            return jsonify({'success': True, 'message': msg, 'session_id': session_id})
        else:
            return jsonify({'success': False, 'message': msg}), 409
    except Exception as e:
        current_app.logger.exception("Error locking seat")
        return jsonify({'success': False, 'message': 'Unable to reserve seat right now. Please try again later.'}), 500

@bp.route('/release_seat', methods=['POST'])
def release_seat():
    """
    Request JSON: { "bus_id": <int>, "seat_no": "A1", "session_id": "<id>" }
    """
    data = request.get_json() or {}
    bus_id = data.get('bus_id')
    seat_no = data.get('seat_no')
    session_id = data.get('session_id')
    if not bus_id or not seat_no or not session_id:
        return jsonify({'success': False, 'message': 'bus_id, seat_no and session_id are required'}), 400
    try:
        _seat_model().release_seat(bus_id, seat_no, session_id)
        return jsonify({'success': True, 'message': 'Seat released.'})
    except Exception as e:
        current_app.logger.exception("Error releasing seat")
        return jsonify({'success': False, 'message': 'Unable to release seat. Please try again later.'}), 500

@bp.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    data = request.get_json() or {}
    session_id = data.get('session_id')
    passenger_id = data.get('passenger_id')
    travel_date = data.get('travel_date')
    payment_status = data.get('payment_status')
    transaction_id = data.get('transaction_id')
    if not session_id or not passenger_id or not travel_date or not payment_status:
        return jsonify({'success': False, 'message': 'session_id, passenger_id, travel_date and payment_status are required'}), 400
    # If payment failed -> inform
    if payment_status != 'success':
        try:
            # Quick DB delete:
            from models.seat_model import SeatModel
            sm = SeatModel(_get_mysql_config())
            conn = sm._get_conn()
            cur = conn.cursor()
            cur.execute("DELETE FROM seat_reservations WHERE session_id=%s;", (session_id,))
            conn.commit()
            cur.close()
            conn.close()
        except Exception:
            current_app.logger.exception("Error releasing on payment failure")
        return jsonify({'success': False, 'message': 'Payment unsuccessful. Please retry or choose another payment method.'}), 402

    # Payment success -> confirm bookings
    try:
        ok, msg, created = _booking_model().confirm_booking(session_id, passenger_id, travel_date, payment_status, transaction_id)
        if not ok:
            return jsonify({'success': False, 'message': msg}), 409
        # Return booking summary
        return jsonify({'success': True, 'message': 'Ticket booked successfully.', 'bookings': created})
    except Exception as e:
        current_app.logger.exception("Error confirming booking")
        return jsonify({'success': False, 'message': 'Unable to confirm booking. Your payment will be refunded if deducted.'}), 500
