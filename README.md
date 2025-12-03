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

## Documentation

This project uses Sphinx for generating API documentation from docstrings. All important functions include Sphinx-formatted docstrings.

### Generating Documentation with Sphinx

#### Prerequisites

Install Sphinx and required extensions:

```bash
pip install sphinx sphinx-rtd-theme
```

#### Initial Setup (First Time Only)

1. Navigate to the project root directory.

2. Initialize Sphinx documentation (if not already done):

```bash
sphinx-quickstart docs
```

When prompted:
- Root path: Press Enter (use default)
- Separate source and build: Yes
- Name prefix: Press Enter (default)
- Project name: Bus Transportation Management System
- Author: Your name/team
- Version: 1.0
- Release: 1.0.0
- Language: en

3. Configure `docs/source/conf.py`:

Add these lines to enable autodoc and set up the path:

```python
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

html_theme = 'sphinx_rtd_theme'
```

#### Generating Documentation

1. Create or update the main documentation file (`docs/source/index.rst`):

```rst
Bus Transportation Management System Documentation
==================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

2. Generate module documentation:

```bash
sphinx-apidoc -o docs/source/ . --separate
```

This will create `.rst` files for all modules in `docs/source/`.

3. Build the HTML documentation:

```bash
cd docs
make html
```

Or on Windows:

```bash
cd docs
.\make.bat html
```

4. View the documentation:

Open `docs/_build/html/index.html` in your web browser.

#### Quick Commands Summary

```bash
# Install Sphinx (one time)
pip install sphinx sphinx-rtd-theme

# Generate module documentation (when code changes)
sphinx-apidoc -o docs/source/ . --separate

# Build HTML documentation
cd docs && make html  # Linux/Mac
cd docs && .\make.bat html  # Windows

# View documentation
# Open docs/_build/html/index.html in browser
```

#### Updating Documentation

After making code changes:

1. Regenerate module files: `sphinx-apidoc -o docs/source/ . --separate`
2. Rebuild HTML: `cd docs && make html`
3. Refresh your browser to see updates

The documentation will automatically include all functions with Sphinx docstrings from your controllers and models.
