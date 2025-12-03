"""
Author: Samiul Ahamed Fhyas
To run these tests:
    python -m pytest tests/test_bus_search.py -v
    OR
    python tests/test_bus_search.py
"""

import sys
import os

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from controllers.route_controller import RouteController
from models.bus_route_model import BusRouteModel


def test_search_with_valid_route():
    """Test searching for a valid route returns results."""
    # Search for a route that exists in the database
    params = {"from": "Feni", "to": "Dhaka", "date": "2025-12-05"}

    response, status_code = RouteController.search(params)

    # Check the response
    assert status_code == 200
    assert "buses" in response
    assert len(response["buses"]) > 0
    print(f"✓ Found {len(response['buses'])} buses for Feni to Dhaka")


def test_search_missing_required_fields():
    """Test search fails when required fields are missing."""
    # Missing 'to' field
    params = {"from": "Dhaka", "date": "2025-12-05"}

    response, status_code = RouteController.search(params)

    # Should return 400 error
    assert status_code == 400
    assert "message" in response
    print("✓ Search correctly rejects missing required fields")


def test_search_with_no_results():
    """Test search returns suggestions when no exact match found."""
    # Search for a route that doesn't exist
    params = {"from": "Tokyo", "to": "Paris", "date": "2025-12-05"}

    response, status_code = RouteController.search(params)

    # Should return empty buses list but may have suggestions
    assert status_code == 200
    assert "buses" in response
    assert len(response["buses"]) == 0
    assert "suggestions" in response
    print("✓ Search returns empty results with suggestions for invalid route")


def test_search_with_bus_type_filter():
    """Test filtering search results by bus type."""
    params = {
        "from": "Dhaka",
        "to": "Chittagong",
        "date": "2025-12-05",
        "bus_type": "AC",
    }

    response, status_code = RouteController.search(params)

    # Check all results are AC type
    assert status_code == 200
    if len(response["buses"]) > 0:
        for bus in response["buses"]:
            assert bus["bus_type"] == "AC"
        print(f"✓ Filter by bus type works - found {len(response['buses'])} AC buses")
    else:
        print("✓ No AC buses found for this route (filter working)")


def test_search_with_price_range():
    """Test filtering by price range."""
    params = {
        "from": "Dhaka",
        "to": "Cox's Bazar",
        "date": "2025-12-05",
        "price_min": "500",
        "price_max": "1000",
    }

    response, status_code = RouteController.search(params)

    # Check all results are within price range
    assert status_code == 200
    if len(response["buses"]) > 0:
        for bus in response["buses"]:
            assert 500 <= bus["fare"] <= 1000
        print(f"✓ Price filter works - found {len(response['buses'])} buses in range")
    else:
        print("✓ No buses in price range (filter working)")


def test_search_sorting_by_price():
    """Test sorting results by price."""
    params = {
        "from": "Chittagong",
        "to": "Dhaka",
        "date": "2025-12-05",
        "sort_by": "price",
    }

    response, status_code = RouteController.search(params)

    # Check results are sorted by price (ascending)
    assert status_code == 200
    if len(response["buses"]) > 1:
        fares = [bus["fare"] for bus in response["buses"]]
        assert fares == sorted(fares)
        print(f"✓ Sorting by price works - {fares}")
    else:
        print("✓ Not enough buses to test sorting")


def test_get_all_enriched_routes():
    """Test getting all routes with enriched data."""
    routes = BusRouteModel.all_enriched_routes()

    # Check we got results
    assert len(routes) > 0

    # Check first route has required enriched fields
    first_route = routes[0]
    assert "bus_type" in first_route
    assert "operator" in first_route
    assert "rating" in first_route
    assert "fare" in first_route
    assert "departure_time" in first_route
    assert "seat_availability" in first_route
    assert "from" in first_route
    assert "to" in first_route

    print(f"✓ Got {len(routes)} enriched routes with all required fields")


def test_distinct_stations_and_operators():
    """Test getting distinct stations and operators."""
    meta = BusRouteModel.distinct_stations_and_operators()

    # Check structure
    assert "stations" in meta
    assert "operators" in meta

    # Check we have data
    assert len(meta["stations"]) > 0
    assert len(meta["operators"]) > 0

    # Check they are sorted
    assert meta["stations"] == sorted(meta["stations"])
    assert meta["operators"] == sorted(meta["operators"])

    print(
        f"✓ Found {len(meta['stations'])} stations and {len(meta['operators'])} operators"
    )


# Run all tests
if __name__ == "__main__":
    print("\n=== Running Bus Search Tests ===\n")

    try:
        test_search_with_valid_route()
        test_search_missing_required_fields()
        test_search_with_no_results()
        test_search_with_bus_type_filter()
        test_search_with_price_range()
        test_search_sorting_by_price()
        test_get_all_enriched_routes()
        test_distinct_stations_and_operators()

        print("\nAll tests passed!\n")
    except AssertionError as e:
        print(f"\n Test failed: {e}\n")
    except Exception as e:
        print(f"\n Error running tests: {e}\n")
