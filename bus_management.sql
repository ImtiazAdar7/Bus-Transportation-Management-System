-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 02, 2025 at 04:48 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bus_management`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `id` int(11) NOT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `age` varchar(10) DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  `website_auth_code` varchar(50) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`id`, `first_name`, `last_name`, `age`, `username`, `website_auth_code`, `dob`, `gender`, `password`) VALUES
(1, 'Adar', 'Bhai', '25', 'adarbhai', 'MMA3', '1999-09-14', 'Male', '$2b$12$1wl.9.rDP2O3UJUJWPPkdeKbSCw2iXTHr2y3oOM7LDoV8otT5/JYu');

-- --------------------------------------------------------

--
-- Table structure for table `assigned_drivers`
--

CREATE TABLE `assigned_drivers` (
  `id` int(11) NOT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `gender` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `assigned_drivers`
--

INSERT INTO `assigned_drivers` (`id`, `first_name`, `last_name`, `age`, `username`, `email`, `dob`, `gender`, `password`) VALUES
(3, 'Kaad', 'Uddin', 23, 'kaad', 'kaad@gmail.com', '5002-09-09', 'Male', '$2b$12$jnjBSITaj2iUOKp//mA2juNwZf.vnpSA3vE54lVRjsHNqCRR5rswS'),
(4, 'Jamal', 'Jamal', 20, 'jamal', 'jamal@yahoo.com', '2000-09-09', 'Male', '$2b$12$t/rYrnMghELIhvo7RmC7Ee08.UrrTbyDtPbmOXKaYXbP4OtGNyBt6'),
(5, 'Pamal', 'Khan', 23, 'pamal', 'pamal@yahoo.com', '2000-10-10', 'Male', '$2b$12$HtMVcUwfcIS.FY9ER0TLK.LTu9Kdml0By8iu489gd7K39JLQ7BP8G'),
(6, 'Hey', 'Khan', 24, 'hey', 'hey@gmail.com', '2011-02-22', 'Male', '$2b$12$1T95x8lEqU7Xna.i8RUMdeJa.qU2Fmm8B0vh1/UBC4VYjLer5C3Na');

-- --------------------------------------------------------

--
-- Table structure for table `bus_list`
--

CREATE TABLE `bus_list` (
  `id` int(11) NOT NULL,
  `brand` varchar(50) DEFAULT NULL,
  `model` varchar(50) DEFAULT NULL,
  `reg` varchar(50) DEFAULT NULL,
  `capacity` int(11) DEFAULT NULL,
  `made_in` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bus_list`
--

INSERT INTO `bus_list` (`id`, `brand`, `model`, `reg`, `capacity`, `made_in`) VALUES
(1, 'Star Line', 'strL-01', 'dhk-metro-0001', 40, 'China'),
(2, 'Star Line', 'strL-02', 'ctg-metro-0002', 45, 'India'),
(3, 'Star Line', 'strL-03', 'syl-metro-0003', 50, 'India'),
(4, 'Star Line', 'strL-04', 'raj-metro-0004', 42, 'Germany'),
(5, 'Star Line', 'strL-05', 'feni-metro-0005', 44, 'China'),
(6, 'Star Line', 'strL-06', 'bar-metro-0006', 48, 'Pakistan'),
(7, 'Star Line', 'strL-07', 'feni-metro-0007', 54, 'Bangladesh'),
(8, 'Star Line', 'strL-08', 'raj-metro-0008', 60, 'Germany'),
(9, 'Hanif Paribahan', 'han-01', 'syl-metro-0009', 50, 'India'),
(10, 'Hanif Paribahan', 'han-02', 'ran-metro-0010', 45, 'China'),
(11, 'Hanif Paribahan', 'han-03', 'syl-metro-0011', 40, 'China'),
(12, 'Hanif Paribahan', 'han-04', 'syl-metro-0012', 42, 'South Korea'),
(13, 'Hanif Paribahan', 'han-05', 'feni-metro-0013', 54, 'India'),
(14, 'Hanif Paribahan', 'han-06', 'dhk-metro-0014', 58, 'Pakistan'),
(15, 'Hanif Paribahan', 'han-07', 'feni-metro-0015', 50, 'Finland'),
(16, 'Hanif Paribahan', 'han-08', 'raj-metro-0016', 60, 'Japan'),
(17, 'Green Line', 'green-01', 'syl-metro-0017', 40, 'South Korea'),
(18, 'Green Line', 'green-02', 'ran-metro-0018', 45, 'Germany'),
(19, 'Green Line', 'green-03', 'syl-metro-0019', 50, 'China'),
(20, 'Green Line', 'green-04', 'syl-metro-0020', 40, 'Bangladesh'),
(21, 'Green Line', 'green-05', 'feni-metro-0021', 50, 'India'),
(22, 'Green Line', 'green-06', 'dhk-metro-0022', 40, 'Pakistan'),
(23, 'Green Line', 'green-07', 'feni-metro-0023', 42, 'Norway'),
(24, 'Green Line', 'green-08', 'raj-metro-0024', 54, 'Vietnam');

-- --------------------------------------------------------

--
-- Table structure for table `bus_routes`
--

CREATE TABLE `bus_routes` (
  `id` int(11) NOT NULL,
  `brand` varchar(50) DEFAULT NULL,
  `model` varchar(50) DEFAULT NULL,
  `reg` varchar(50) DEFAULT NULL,
  `route` varchar(100) DEFAULT NULL,
  `time` time DEFAULT NULL,
  `capacity` int(11) DEFAULT NULL,
  `made_in` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bus_routes`
--

INSERT INTO `bus_routes` (`id`, `brand`, `model`, `reg`, `route`, `time`, `capacity`, `made_in`) VALUES
(1, 'Star Line', 'strL-01', 'dhk-metro-0001', 'Feni-Dhaka', '06:30:00', 40, 'China'),
(2, 'Star Line', 'strL-02', 'ctg-metro-0002', 'Feni-Cox\'s Bazar', '08:00:00', 45, 'India'),
(3, 'Star Line', 'strL-03', 'syl-metro-0003', 'Feni-Cumilla', '09:15:00', 50, 'India'),
(4, 'Star Line', 'strL-04', 'raj-metro-0004', 'Dhaka-Cox\'s Bazar', '10:30:00', 42, 'Germany'),
(5, 'Star Line', 'strL-05', 'feni-metro-0005', 'Dhaka-Chittagong', '12:00:00', 44, 'China'),
(6, 'Star Line', 'strL-06', 'bar-metro-0006', 'Dhaka-Feni', '13:30:00', 48, 'Pakistan'),
(7, 'Star Line', 'strL-07', 'feni-metro-0007', 'Chittagong-Cox\'s Bazar', '15:00:00', 54, 'Bangladesh'),
(8, 'Star Line', 'strL-08', 'raj-metro-0008', 'Cox\'s Bazar-Dhaka', '16:30:00', 60, 'Germany'),
(9, 'Star Line', 'strL-09', 'khu-metro-0009', 'Cox\'s Bazar-Feni', '18:00:00', 60, 'US'),
(10, 'Hanif Paribahan', 'han-01', 'syl-metro-0009', 'Dhaka-Savar', '06:15:00', 50, 'India'),
(11, 'Hanif Paribahan', 'han-02', 'ran-metro-0010', 'Dhaka-Cox\'s Bazar', '07:45:00', 45, 'China'),
(12, 'Hanif Paribahan', 'han-03', 'syl-metro-0011', 'Dhaka-Sylhet', '09:30:00', 40, 'China'),
(13, 'Hanif Paribahan', 'han-04', 'syl-metro-0012', 'Savar-Cox\'s Bazar', '11:00:00', 42, 'South Korea'),
(14, 'Hanif Paribahan', 'han-05', 'feni-metro-0013', 'Chittagong-Dhaka', '12:45:00', 54, 'India'),
(15, 'Hanif Paribahan', 'han-06', 'dhk-metro-0014', 'Chittagong-Dhaka', '14:15:00', 58, 'Pakistan'),
(16, 'Hanif Paribahan', 'han-07', 'feni-metro-0015', 'Cox\'s Bazar-Dhaka', '15:45:00', 50, 'Finland'),
(17, 'Hanif Paribahan', 'han-08', 'raj-metro-0016', 'Sylhet-Dhaka', '17:30:00', 60, 'Japan'),
(18, 'Green Line', 'green-01', 'syl-metro-0017', 'Sylhet-Dhaka', '06:45:00', 40, 'South Korea'),
(19, 'Green Line', 'green-02', 'ran-metro-0018', 'Cox\'s Bazar-Dhaka', '08:30:00', 45, 'Germany'),
(20, 'Green Line', 'green-03', 'syl-metro-0019', 'Chittagong-Dhaka', '10:00:00', 50, 'China'),
(21, 'Green Line', 'green-04', 'syl-metro-0020', 'Dhaka-Cox\'s Bazar', '11:30:00', 40, 'Bangladesh'),
(22, 'Green Line', 'green-05', 'feni-metro-0021', 'Dhaka-Chittagong', '13:00:00', 50, 'India'),
(23, 'Green Line', 'green-06', 'dhk-metro-0022', 'Dhaka-Sylhet', '14:30:00', 40, 'Pakistan'),
(24, 'Green Line', 'green-07', 'feni-metro-0023', 'Chittagong-Sylhet', '16:00:00', 42, 'Norway'),
(25, 'Green Line', 'green-08', 'raj-metro-0024', 'Sylhet-Chittagong', '17:30:00', 54, 'Vietnam');

-- --------------------------------------------------------

--
-- Table structure for table `drivers`
--

CREATE TABLE `drivers` (
  `id` int(11) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `age` varchar(10) DEFAULT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `dob` date DEFAULT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `passengers`
--

CREATE TABLE `passengers` (
  `id` int(11) NOT NULL,
  `first_name` varchar(80) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `passengers`
--

INSERT INTO `passengers` (`id`, `first_name`, `last_name`, `age`, `username`, `email`, `dob`, `gender`, `password`) VALUES
(1, 'Imtiaz Ahmed', 'Adar', 25, 'imtiazadar', 'imtiazadar@gmail.com', '2000-09-14', 'Male', '$2b$12$A0/g/zEW0t8a5lMCPcZSYOTcJowmmXRPV4E3GvxeK4K8XDa85Yj/K'),
(2, 'Krim', 'Uddin', 22, 'krim', 'krim@gmail.com', '2005-09-11', 'Male', '$2b$12$7qbmO9IF.E7ZREdYQCaAQeIo8lQSAahV0rEzeYUfNdcyAW2ZuFt5C');

-- --------------------------------------------------------

--
-- Table structure for table `website_auth_codes`
--

CREATE TABLE `website_auth_codes` (
  `id` int(11) NOT NULL,
  `code` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `website_auth_codes`
--

INSERT INTO `website_auth_codes` (`id`, `code`) VALUES
(3, 'bus_management'),
(1, 'cse327proj'),
(2, 'mma3');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `assigned_drivers`
--
ALTER TABLE `assigned_drivers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `bus_list`
--
ALTER TABLE `bus_list`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `bus_routes`
--
ALTER TABLE `bus_routes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `drivers`
--
ALTER TABLE `drivers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `passengers`
--
ALTER TABLE `passengers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `website_auth_codes`
--
ALTER TABLE `website_auth_codes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `bus_list`
--
ALTER TABLE `bus_list`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `bus_routes`
--
ALTER TABLE `bus_routes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `drivers`
--
ALTER TABLE `drivers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `passengers`
--
ALTER TABLE `passengers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `website_auth_codes`
--
ALTER TABLE `website_auth_codes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
