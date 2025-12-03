"""
Author: Test Suite
Unit tests for analytics functionality.

To run these tests:
    python -m pytest tests/test_analytics.py -v
    OR
    python tests/test_analytics.py
"""

import sys
import os

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from controllers.analytics_controller import AnalyticsController


def test_get_stats_structure():
    """Test that analytics stats return the correct structure."""
    response, status = AnalyticsController.get_stats()
    
    assert status == 200
    assert "total_routes" in response
    assert "top_routes" in response
    assert "top_destinations" in response
    assert "bus_type_distribution" in response
    assert "fare_comparison" in response
    
    print("✓ Analytics stats structure is correct")


def test_get_stats_data_types():
    """Test that analytics stats return correct data types."""
    response, status = AnalyticsController.get_stats()
    
    assert isinstance(response["total_routes"], int)
    assert isinstance(response["top_routes"], list)
    assert isinstance(response["top_destinations"], list)
    assert isinstance(response["bus_type_distribution"], list)
    assert isinstance(response["fare_comparison"], list)
    
    # Check top_routes structure
    if len(response["top_routes"]) > 0:
        assert "route" in response["top_routes"][0]
        assert "count" in response["top_routes"][0]
    
    # Check top_destinations structure
    if len(response["top_destinations"]) > 0:
        assert "destination" in response["top_destinations"][0]
        assert "count" in response["top_destinations"][0]
    
    # Check bus_type_distribution structure
    assert len(response["bus_type_distribution"]) == 2
    for item in response["bus_type_distribution"]:
        assert "type" in item
        assert "count" in item
    
    # Check fare_comparison structure
    if len(response["fare_comparison"]) > 0:
        assert "operator" in response["fare_comparison"][0]
        assert "avg_fare" in response["fare_comparison"][0]
    
    print("✓ Analytics stats data types are correct")


def test_get_stats_top_routes_limit():
    """Test that top_routes is limited to 10 items."""
    response, status = AnalyticsController.get_stats()
    
    assert len(response["top_routes"]) <= 10
    print("✓ Top routes limit is correct")


def test_get_stats_top_destinations_limit():
    """Test that top_destinations is limited to 8 items."""
    response, status = AnalyticsController.get_stats()
    
    assert len(response["top_destinations"]) <= 8
    print("✓ Top destinations limit is correct")


# Run all tests
if __name__ == "__main__":
    print("\n=== Running Analytics Tests ===\n")
    
    try:
        test_get_stats_structure()
        test_get_stats_data_types()
        test_get_stats_top_routes_limit()
        test_get_stats_top_destinations_limit()
        
        print("\nAll analytics tests passed!\n")
    except AssertionError as e:
        print(f"\n Test failed: {e}\n")
    except Exception as e:
        print(f"\n Error running tests: {e}\n")

