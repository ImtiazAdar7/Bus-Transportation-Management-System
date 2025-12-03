'''Author: Samiul Ahamed Fhyas'''
from typing import Any, Dict
from models.bus_route_model import BusRouteModel


class RouteController:
    """Controller for searching routes and fetching seat layout."""

    @staticmethod
    def search(params: Dict[str, Any]):
        """
        Search for bus routes based on various filters.

        Args:
            params (dict): Search parameters with optional keys:
                - from (str): Source location
                - to (str): Destination location
                - date (str): Travel date
                - bus_type (str, optional): Filter by bus type (AC/Non-AC)
                - operator (str, optional): Filter by operator name
                - price_min (float, optional): Minimum price filter
                - price_max (float, optional): Maximum price filter
                - sort_by (str, optional): Sort by 'price', 'rating', or 'departure'

        Returns:
            tuple: (dict with buses list and suggestions, HTTP status code)
        """
        src = (params.get("from") or params.get("src") or "").strip()
        dst = (params.get("to") or params.get("dst") or "").strip()
        date = (params.get("date") or params.get("travel_date") or "").strip()
        bus_type = (params.get("bus_type") or params.get("type") or "").strip() or None
        operator = (params.get("operator") or "").strip() or None
        sort_by = (params.get("sort_by") or "").strip() or None

        try:
            price_min = (
                float(params.get("price_min"))
                if params.get("price_min") not in (None, "")
                else None
            )
        except ValueError:
            price_min = None
        try:
            price_max = (
                float(params.get("price_max"))
                if params.get("price_max") not in (None, "")
                else None
            )
        except ValueError:
            price_max = None

        if not src or not dst or not date:
            return {"message": "from, to and date are required"}, 400

        results = BusRouteModel.search_routes(
            src=src,
            dst=dst,
            departure_date=date,
            bus_type=bus_type,
            operator=operator,
            price_min=price_min,
            price_max=price_max,
            sort_by=sort_by,
        )

        if not results:
            suggestions = BusRouteModel.suggest_alternatives(src, dst)
            return {"buses": [], "suggestions": suggestions}, 200

        return {"buses": results, "suggestions": []}, 200

    @staticmethod
    def seat_layout(route_id: int, travel_date: str):
        """
        Get seat layout for a specific bus route.

        Args:
            route_id (int): ID of the bus route
            travel_date (str): Date of travel

        Returns:
            tuple: (dict with route details, travel_date, available_seats, and layout, HTTP status code)
        """
        route = BusRouteModel.get_route_by_id(route_id)
        if not route:
            return {"message": "Route not found"}, 404

        capacity = int(route.get("capacity") or 0)

        # Generate a 2+2 layout per row with an aisle in between
        rows = []
        seat_no = 1
        # Try to fill rows of 4; if remaining, add last row accordingly
        full_rows = capacity // 4
        remainder = capacity % 4

        def seat(label: str):
            nonlocal seat_no
            s = {"id": seat_no, "label": label, "available": True}
            seat_no += 1
            return s

        for _ in range(full_rows):
            rows.append(
                [
                    seat(f"{seat_no:02d}A"),
                    seat(f"{seat_no:02d}B"),
                    None,
                    seat(f"{seat_no:02d}C"),
                    seat(f"{seat_no:02d}D"),
                ]
            )

        if remainder:
            last = []
            positions = ["A", "B", "C", "D"]
            for i in range(remainder):
                last.append(seat(f"{seat_no:02d}{positions[i]}"))
            # insert aisle placeholder between B and C positions
            if len(last) <= 2:
                last = last + [None, None]
            elif len(last) == 3:
                last = last[:2] + [None] + last[2:]
            rows.append(last)

        return {
            "route": {
                "id": route.get("id"),
                "operator": route.get("brand"),
                "reg": route.get("reg"),
                "route": route.get("route"),
                "time": str(route.get("time")),
                "capacity": capacity,
            },
            "travel_date": travel_date,
            "available_seats": capacity,  # No booking integration yet
            "layout": rows,
        }, 200

    @staticmethod
    def meta():
        """
        Get metadata about available stations and operators.

        Returns:
            tuple: (dict with stations and operators lists, HTTP status code)
        """
        meta = BusRouteModel.distinct_stations_and_operators()
        return meta, 200

    @staticmethod
    def all_routes():
        """
        Get all bus routes with enriched data (fare, rating, bus_type, etc.).

        Returns:
            tuple: (dict with buses list, HTTP status code)
        """
        routes = BusRouteModel.all_enriched_routes()
        return {"buses": routes}, 200
