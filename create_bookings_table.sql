-- Create bookings table if it doesn't exist
-- Run this script in your MySQL database to create the bookings table

USE bus_management;

-- Create bookings table
CREATE TABLE IF NOT EXISTS `bookings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bus_route_id` int(11) NOT NULL,
  `passenger_id` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bus_route_id` (`bus_route_id`),
  KEY `passenger_id` (`passenger_id`),
  CONSTRAINT `fk_bookings_bus_route` FOREIGN KEY (`bus_route_id`) REFERENCES `bus_routes` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_bookings_passenger` FOREIGN KEY (`passenger_id`) REFERENCES `passengers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

