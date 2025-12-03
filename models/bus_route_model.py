'''Author: Samiul Ahamed Fhyas'''
from typing import List, Dict, Optional, Tuple
from config import Config


class BusRouteModel:
    """Data access for bus routes and list of buses."""

    @staticmethod
    def _fetchall(query: str, params: Tuple = ()) -> List[Dict]:
        db = Config.get_db()
        cur = db.cursor(dictionary=True)
        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
        db.close()
        return rows

    @staticmethod
    def get_all_routes() -> List[Dict]:
        return BusRouteModel._fetchall("SELECT * FROM bus_routes")

    @staticmethod
    def _parse_route(r: str) -> Tuple[str, str]:
        if not r or "-" not in r:
            return ("", "")
        a, b = r.split("-", 1)
        return a.strip(), b.strip()

    @staticmethod
    def _brand_to_type(brand: str) -> str:
        if not brand:
            return "Non-AC"
        brand_lower = brand.lower()
        if any(k in brand_lower for k in ["green", "hanif"]):
            return "AC"
        return "Non-AC"

    @staticmethod
    def _brand_rating(brand: str) -> float:
        if not brand:
            return 3.5
        bl = brand.lower()
        if "green" in bl:
            return 4.5
        if "hanif" in bl:
            return 4.2
        return 4.0

    @staticmethod
    def _estimate_fare(brand: str, src: str, dst: str) -> float:
        base = 700.0
        if BusRouteModel._brand_to_type(brand) == "AC":
            base += 300.0
        approx = max(1, abs(len(src) - len(dst)) + (len(src) + len(dst)) // 4)
        return round(base + approx * 20.0, 2)

    @staticmethod
    def all_enriched_routes() -> List[Dict]:
        routes = BusRouteModel.get_all_routes()
        enriched: List[Dict] = []
        for row in routes:
            a, b = BusRouteModel._parse_route(row.get("route"))
            row_copy = dict(row)
            row_copy["bus_type"] = BusRouteModel._brand_to_type(
                row_copy.get("brand", "")
            )
            row_copy["operator"] = row_copy.get("brand")
            row_copy["rating"] = BusRouteModel._brand_rating(row_copy.get("brand", ""))
            row_copy["fare"] = BusRouteModel._estimate_fare(
                row_copy.get("brand", ""), a, b
            )
            row_copy["departure_time"] = (
                str(row_copy.get("time")) if row_copy.get("time") is not None else ""
            )
            row_copy.pop("time", None)
            row_copy["seat_availability"] = int(row_copy.get("capacity") or 0)
            row_copy["from"] = a
            row_copy["to"] = b
            enriched.append(row_copy)
        return enriched

    @staticmethod
    def distinct_stations_and_operators() -> Dict[str, List[str]]:
        routes = BusRouteModel.get_all_routes()
        stations = set()
        operators = set()
        for row in routes:
            r = row.get("route", "")
            a, b = BusRouteModel._parse_route(r)
            if a:
                stations.add(a)
            if b:
                stations.add(b)
            brand = row.get("brand")
            if brand:
                operators.add(brand)
        return {
            "stations": sorted(stations),
            "operators": sorted(operators),
        }

    @staticmethod
    def search_routes(
        src: str,
        dst: str,
        departure_date: Optional[str] = None,
        bus_type: Optional[str] = None,
        operator: Optional[str] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        sort_by: Optional[str] = None,
    ) -> List[Dict]:
        """
        Search routes by simple matching on `route` field formatted as "Src-Dst".
        Since the schema lacks fare/type, we enrich rows on the fly.
        """
        # Base fetch and in-Python filter/enrich for flexibility
        routes = BusRouteModel.get_all_routes()

        def parse_route(r: str) -> Tuple[str, str]:
            if not r or "-" not in r:
                return ("", "")
            a, b = r.split("-", 1)
            return a.strip(), b.strip()

        def brand_to_type(brand: str) -> str:
            if not brand:
                return "Non-AC"
            brand_lower = brand.lower()
            if any(k in brand_lower for k in ["green", "hanif"]):
                return "AC"
            return "Non-AC"

        def brand_rating(brand: str) -> float:
            if not brand:
                return 3.5
            bl = brand.lower()
            if "green" in bl:
                return 4.5
            if "hanif" in bl:
                return 4.2
            return 4.0

        def estimate_fare(brand: str, src: str, dst: str) -> float:
            base = 700.0
            if brand_to_type(brand) == "AC":
                base += 300.0
          
            approx = max(1, abs(len(src) - len(dst)) + (len(src) + len(dst)) // 4)
            return round(base + approx * 20.0, 2)

        # Normalize inputs
        src_norm = (src or "").strip().lower()
        dst_norm = (dst or "").strip().lower()
        type_norm = (bus_type or "").strip().lower() or None
        op_norm = (operator or "").strip().lower() or None

        enriched: List[Dict] = []
        for row in routes:
            a, b = parse_route(row.get("route"))
            if a.lower() != src_norm or b.lower() != dst_norm:
                continue

            row_copy = dict(row)  # avoid mutating original
            bt = brand_to_type(row_copy.get("brand", ""))
            row_copy["bus_type"] = bt
            row_copy["operator"] = row_copy.get("brand")
            row_copy["rating"] = brand_rating(row_copy.get("brand", ""))
            row_copy["fare"] = estimate_fare(row_copy.get("brand", ""), a, b)
            # Normalize time for JSON and avoid exposing raw timedelta/time object
            row_copy["departure_time"] = (
                str(row_copy.get("time")) if row_copy.get("time") is not None else ""
            )
            if "time" in row_copy:
                # Remove the original non-JSON-serializable value
                row_copy.pop("time", None)
            row_copy["seat_availability"] = int(row_copy.get("capacity") or 0)
            row_copy["from"] = a
            row_copy["to"] = b

            # Apply filters
            if type_norm and row_copy["bus_type"].lower() != type_norm:
                continue
            if op_norm and (row_copy.get("operator", "").lower() != op_norm):
                continue
            if price_min is not None and row_copy["fare"] < float(price_min):
                continue
            if price_max is not None and row_copy["fare"] > float(price_max):
                continue
            enriched.append(row_copy)

        # Sorting
        if sort_by:
            key = sort_by.lower()
            if key == "price":
                enriched.sort(key=lambda x: x.get("fare", 0.0))
            elif key == "rating":
                enriched.sort(key=lambda x: x.get("rating", 0.0), reverse=True)
            elif key == "departure":
                enriched.sort(key=lambda x: x.get("departure_time", ""))

        return enriched

    @staticmethod
    def suggest_alternatives(src: str, dst: str) -> List[Dict]:
        """
        Suggest routes that share the source or the destination when no exact match.
        """
        routes = BusRouteModel.get_all_routes()
        src_norm = (src or "").strip().lower()
        dst_norm = (dst or "").strip().lower()

        suggestions: List[Dict] = []
        for row in routes:
            r = row.get("route", "")
            if "-" not in r:
                continue
            a, b = (s.strip().lower() for s in r.split("-", 1))
            if a == src_norm or b == dst_norm or b == src_norm or a == dst_norm:
                suggestions.append(
                    {
                        "id": row.get("id"),
                        "operator": row.get("brand"),
                        "route": row.get("route"),
                        "time": str(row.get("time")),
                        "capacity": row.get("capacity"),
                    }
                )
        # Deduplicate by (route,time,operator)
        seen = set()
        unique = []
        for s in suggestions:
            k = (s["route"], s["time"], s["operator"])
            if k in seen:
                continue
            seen.add(k)
            unique.append(s)
        return unique[:10]

    @staticmethod
    def get_route_by_id(route_id: int) -> Optional[Dict]:
        rows = BusRouteModel._fetchall(
            "SELECT * FROM bus_routes WHERE id=%s", (route_id,)
        )
        return rows[0] if rows else None
