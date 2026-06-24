-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 24, 2026 at 02:44 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `duka_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `bidhaa`
--

CREATE TABLE `bidhaa` (
  `id` int(11) NOT NULL,
  `bar_code` varchar(50) DEFAULT NULL,
  `jina_la_bidhaa` varchar(100) NOT NULL,
  `bei_ya_kununua` decimal(10,2) NOT NULL,
  `bei_ya_kuuza` decimal(10,2) NOT NULL,
  `idadi_ya_stoo` int(11) NOT NULL,
  `tarehe_ya_kuingizwa` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `mauzo`
--

CREATE TABLE `mauzo` (
  `id` int(11) NOT NULL,
  `namba_ya_risiti` varchar(50) NOT NULL,
  `id_ya_bidhaa` int(11) DEFAULT NULL,
  `idadi_iliyozuiliwa` int(11) NOT NULL,
  `jumla_ya_bei` decimal(10,2) DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `watumiaji`
--

CREATE TABLE `watumiaji` (
  `id` int(11) NOT NULL,
  `jina_la_mtumiaji` varchar(50) NOT NULL,
  `nywila` varchar(255) NOT NULL,
  `cheo` enum('Admin','cashier') DEFAULT 'cashier'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bidhaa`
--
ALTER TABLE `bidhaa`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `bar_code` (`bar_code`);

--
-- Indexes for table `mauzo`
--
ALTER TABLE `mauzo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_ya_bidhaa` (`id_ya_bidhaa`);

--
-- Indexes for table `watumiaji`
--
ALTER TABLE `watumiaji`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `jina_la_mtumiaji` (`jina_la_mtumiaji`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bidhaa`
--
ALTER TABLE `bidhaa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `mauzo`
--
ALTER TABLE `mauzo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `watumiaji`
--
ALTER TABLE `watumiaji`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `mauzo`
--
ALTER TABLE `mauzo`
  ADD CONSTRAINT `mauzo_ibfk_1` FOREIGN KEY (`id_ya_bidhaa`) REFERENCES `bidhaa` (`id`) ON DELETE SET NULL;
SET FOREIGN_KEY_CHECKS=1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
