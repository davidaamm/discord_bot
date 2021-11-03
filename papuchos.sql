-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 03, 2021 at 10:26 PM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 7.3.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `chismestrum`
--

-- --------------------------------------------------------

--
-- Table structure for table `papuchos`
--

CREATE TABLE `papuchos` (
  `discord_id` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `sub` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `plataforma` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `nick` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `papuchos`
--

INSERT INTO `papuchos` (`discord_id`, `nombre`, `sub`, `plataforma`, `nick`) VALUES
('143551428202332160', 'MarFon', '', 'epic', 'MarFon'),
('170302385262952450', 'tiranodiego', '', 'epic', 'tiranodiego'),
('394253183855099905', 'H. Pavel', '', 'epic', 'hpavelr'),
('727384087714857050', 'Sicaac', '', 'epic', 'sicaac'),
('731236277780742234', 'deividaam', '1634875690.896845', 'epic', 'deividaam');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `papuchos`
--
ALTER TABLE `papuchos`
  ADD PRIMARY KEY (`discord_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
