"""
Author: Test Suite
Unit tests for route seat layout functionality.

To run these tests:
    python -m pytest tests/test_route_seat_layout.py -v
    OR
    python tests/test_route_seat_layout.py
"""

import sys
import os

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from controllers.route_controller import RouteController
from models.bus_route_model import BusRouteModel


def test_seat_layout_success():
    """Test getting seat layout for a valid route."""
    # Get a route from the database
    routes = BusRouteModel.get_all_routes()
    
    if len(routes) > 0:
        route_id = routes[0]["id"]
        travel_date = "2025-12-05"
        
        response, status = RouteController.seat_layout(route_id, travel_date)
        
        assert status == 200
        assert "route" in response
        assert "travel_date" in response
        assert "available_seats" in response
        assert "layout" in response
        
        # Check route structure
        assert "id" in response["route"]
        assert "operator" in response["route"]
        assert "capacity" in response["route"]
        
        # Check layout structure
        assert isinstance(response["layout"], list)
        if len(response["layout"]) > 0:
            assert isinstance(response["layout"][0], list)
        
        print("✓ Seat layout retrieved successfully")


def test_seat_layout_invalid_route():
    """Test getting seat layout for a non-existent route."""
    invalid_route_id = 99999
    travel_date = "2025-12-05"
    
    response, status = RouteController.seat_layout(invalid_route_id, travel_date)
    
    assert status == 404
    assert "message" in response
    print("✓ Invalid route correctly handled")


def test_seat_layout_structure():
    """Test that seat layout has correct structure with aisle."""
    routes = BusRouteModel.get_all_routes()
    
    if len(routes) > 0:
        route_id = routes[0]["id"]
        travel_date = "2025-12-05"
        
        response, status = RouteController.seat_layout(route_id, travel_date)
        
        if status == 200 and len(response["layout"]) > 0:
            # Check that rows have proper structure (seats and aisle)
            for row in response["layout"]:
                # Row should be a list
                assert isinstance(row, list)
                # Should have at least one seat
                has_seat = any(seat is not None for seat in row)
                assert has_seat
            
            print("✓ Seat layout structure is correct")


def test_seat_layout_capacity_match():
    """Test that available_seats matches route capacity."""
    routes = BusRouteModel.get_all_routes()
    
    if len(routes) > 0:
        route_id = routes[0]["id"]
        travel_date = "2025-12-05"
        
        response, status = RouteController.seat_layout(route_id, travel_date)
        
        if status == 200:
            capacity = response["route"]["capacity"]
            available_seats = response["available_seats"]
            
            # Available seats should match capacity (no booking integration yet)
            assert available_seats == capacity
            print("✓ Seat capacity matches route capacity")


# Run all tests
if __name__ == "__main__":
    print("\n=== Running Route Seat Layout Tests ===\n")
    
    try:
        test_seat_layout_success()
        test_seat_layout_invalid_route()
        test_seat_layout_structure()
        test_seat_layout_capacity_match()
        
        print("\nAll seat layout tests passed!\n")
    except AssertionError as e:
        print(f"\n Test failed: {e}\n")
    except Exception as e:
        print(f"\n Error running tests: {e}\n")

