.. Bus Transportation Management System documentation master file, created by
   sphinx-quickstart on Thu Dec  4 03:51:48 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Bus Transportation Management System Documentation
==================================================

Welcome to the Bus Transportation Management System documentation!

This is a comprehensive web application for managing bus transportation services, including:

* **Passenger Management**: Registration, login, and booking management
* **Driver Management**: Driver registration, assignment, and tracking
* **Admin Portal**: Administrative functions for managing the system
* **Route Management**: Bus route search, seat layout, and route information
* **Analytics**: Statistics and insights about routes and bookings

Getting Started
---------------

The system is built using:

* **Backend**: Flask (Python web framework)
* **Database**: MySQL
* **Authentication**: JWT tokens
* **Frontend**: React.js

API Overview
------------

The system provides RESTful APIs organized into the following modules:

* :doc:`controllers` - Business logic controllers
* :doc:`models` - Data models and database access
* :doc:`routes` - API route handlers
* :doc:`modules` - Core application modules

Documentation Structure
------------------------

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   modules
   controllers
   models
   routes

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
