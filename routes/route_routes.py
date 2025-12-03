'''Author: Samiul Ahamed Fhyas'''
from flask import Blueprint, request
from controllers.route_controller import RouteController

route_bp = Blueprint("route_bp", __name__, url_prefix="/api/routes")


@route_bp.get("/search")
def search_routes():
    return RouteController.search(request.args)


@route_bp.get("/seat-layout/<int:route_id>")
def seat_layout(route_id: int):
    travel_date = request.args.get("date") or ""
    if not travel_date:
        return {"message": "date is required"}, 400
    return RouteController.seat_layout(route_id, travel_date)


@route_bp.get("/meta")
def routes_meta():
    return RouteController.meta()


@route_bp.get("/all")
def routes_all():
    return RouteController.all_routes()
