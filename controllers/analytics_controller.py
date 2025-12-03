'''Author: Samiul Ahamed Fhyas'''
from typing import Any, Dict
from models.bus_route_model import BusRouteModel


class AnalyticsController:
    """Controller for analytics and statistics."""

    @staticmethod
    def get_stats():
        """Return passenger-relevant statistics for analytics dashboard."""
        routes = BusRouteModel.all_enriched_routes()

        # Route popularity (count by from-to pair)
        route_popularity = {}

        # Bus type distribution
        bus_type_count = {"AC": 0, "Non-AC": 0}

        # Fare by operator for comparison
        fare_by_operator = {}

        # Destinations frequency
        destinations = {}
        sources = {}

        for route in routes:
            op = route.get("operator") or "Unknown"
            bt = route.get("bus_type") or "Non-AC"
            fare = route.get("fare", 0)
            from_loc = route.get("from", "")
            to_loc = route.get("to", "")

            # Route popularity
            route_key = f"{from_loc} → {to_loc}"
            route_popularity[route_key] = route_popularity.get(route_key, 0) + 1

            # Bus type
            bus_type_count[bt] = bus_type_count.get(bt, 0) + 1

            # Average fare per operator (for comparison shopping)
            if op not in fare_by_operator:
                fare_by_operator[op] = []
            fare_by_operator[op].append(fare)

            # Popular destinations
            if to_loc:
                destinations[to_loc] = destinations.get(to_loc, 0) + 1
            if from_loc:
                sources[from_loc] = sources.get(from_loc, 0) + 1

        # Compute average fares by operator
        avg_fare_by_operator = {
            op: round(sum(fares) / len(fares), 2) if fares else 0
            for op, fares in fare_by_operator.items()
        }

        # Top 10 routes by frequency
        top_routes = sorted(route_popularity.items(), key=lambda x: x[1], reverse=True)[
            :10
        ]

        # Top 8 destinations
        top_destinations = sorted(
            destinations.items(), key=lambda x: x[1], reverse=True
        )[:8]

        # Fare comparison by operator (sorted by avg fare)
        fare_comparison = [
            {"operator": op, "avg_fare": fare}
            for op, fare in avg_fare_by_operator.items()
        ]
        fare_comparison = sorted(fare_comparison, key=lambda x: x["avg_fare"])

        return {
            "total_routes": len(routes),
            "top_routes": [{"route": r[0], "count": r[1]} for r in top_routes],
            "top_destinations": [
                {"destination": d[0], "count": d[1]} for d in top_destinations
            ],
            "bus_type_distribution": [
                {"type": "AC", "count": bus_type_count["AC"]},
                {"type": "Non-AC", "count": bus_type_count["Non-AC"]},
            ],
            "fare_comparison": fare_comparison,
        }, 200
