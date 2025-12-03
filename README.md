# Bus Transportation Management System

Flask backend + React (Vite) frontend.

## Quick start

Run backend:

```
python app.py
```

Run frontend:

```
npm install
npm run dev
```

Backend has CORS enabled. Default API base is the same origin where Flask is running.

## New Features: Bus Search & Seat Layout

- Search by `From`, `To`, and travel `Date`.
- Filter by bus type (AC/Non-AC), price range, and operator.
- Sort by price, rating, or departure time.
- If no exact match, suggestions show alternative routes that share source/destination.
- View seat layout and proceed to booking (placeholder).

### API Endpoints

- `GET /api/routes/search?from=Feni&to=Dhaka&date=2025-12-03&bus_type=AC&price_min=500&price_max=1500&operator=Green%20Line&sort_by=price`
  - Returns `{ buses: [...], suggestions: [...] }`.
- `GET /api/routes/seat-layout/:route_id?date=2025-12-03`
  - Returns `{ route, travel_date, available_seats, layout }`.

Note: Fare, bus type, and rating are enriched from brand heuristics without changing the DB schema. Seat availability equals bus capacity until booking is implemented.
