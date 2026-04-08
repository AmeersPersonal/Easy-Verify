-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 04, 2026 at 06:43 PM
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
-- Database: `easyverify`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `check_token` (IN `p_user_id` INT)   BEGIN
    SELECT * FROM verifications
    WHERE user_id = p_user_id
    AND token = p_token;
    
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_company` (IN `p_id` INT)   BEGIN
    DELETE FROM companyx WHERE id = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_expired_tokens` (IN `p_user_id` INT)   BEGIN
    DELETE FROM verifications
    WHERE user_id = p_user_id
    AND expires_at <= NOW()
	AND (SELECT is_persistent FROM users WHERE id = p_user_id) = 0;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_user` (IN `p_user_id` INT)   BEGIN
    DELETE FROM users WHERE id = p_user_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `get_company` (IN `p_email` VARCHAR(255))   BEGIN
    SELECT * FROM companyx WHERE email = p_email;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `get_user` (IN `p_username` VARCHAR(100))   BEGIN
    SELECT * FROM users
    WHERE username = p_username OR email = p_username;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `get_verifications_by_user` (IN `p_user_id` INT)   BEGIN
    SELECT * FROM verifications
    WHERE user_id = p_user_id
    ORDER BY created_at DESC;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_company` (IN `p_user_id` INT, IN `p_name` VARCHAR(100), IN `p_email` VARCHAR(255), IN `p_pw` CHAR(100))   BEGIN
    INSERT INTO companyx (user_id, name, email, pw)
    VALUES (p_user_id, p_name, p_email, p_pw);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_user` (IN `p_username` VARCHAR(100), IN `p_email` VARCHAR(255), IN `p_pw` CHAR(60), IN `p_is_persistent` TINYINT(1))   INSERT INTO users (username, email, pw, is_persistent)
VALUES (p_username, p_email, p_pw, p_is_persistent)$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_verification` (IN `p_user_id` INT, IN `p_result` BOOLEAN, IN `p_method` TEXT, IN `p_policy` TEXT, IN `p_confidence` INT, IN `p_error_code` TEXT, IN `p_token` TEXT, IN `p_expires_at` TIMESTAMP)   BEGIN
    INSERT INTO verifications (user_id, result, method, policy, confidence, error_code, token, expires_at)
    VALUES (p_user_id, p_result, p_method, p_policy, p_confidence, p_error_code, p_token, p_expires_at);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `update_company` (IN `p_id` INT, IN `p_name` VARCHAR(100), IN `p_email` VARCHAR(255), IN `p_pw` CHAR(100))   BEGIN
    UPDATE companyx 
    SET name = p_name, email = p_email, pw = p_pw
    WHERE id = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `update_last_login` (IN `p_user_id` INT)   BEGIN
    UPDATE users
    SET last_login = CURRENT_TIMESTAMP
    WHERE id = p_user_id;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `companyx`
--

CREATE TABLE `companyx` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `pw` char(100) NOT NULL,
  `verified` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `pw` char(60) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `is_persistent` tinyint(1) NOT NULL,
  `last_login` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `pw`, `created_at`, `is_persistent`, `last_login`) VALUES
(1, 'testuser', 'test@test.com', 'fakehash123456789012345678901234567890123456789012345678901', '2026-03-25 16:13:48', 0, '2026-03-25 16:13:48');

-- --------------------------------------------------------

--
-- Table structure for table `verifications`
--

CREATE TABLE `verifications` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `result` tinyint(1) NOT NULL,
  `method` text DEFAULT NULL,
  `policy` text DEFAULT NULL,
  `confidence` int(11) DEFAULT NULL,
  `error_code` text DEFAULT NULL,
  `token` text NOT NULL,
  `expires_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `companyx`
--
ALTER TABLE `companyx`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `verifications`
--
ALTER TABLE `verifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `companyx`
--
ALTER TABLE `companyx`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `verifications`
--
ALTER TABLE `verifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `companyx`
--
ALTER TABLE `companyx`
  ADD CONSTRAINT `companyx_ibfk_1` FOREIGN KEY (`email`) REFERENCES `users` (`email`);

--
-- Constraints for table `verifications`
--
ALTER TABLE `verifications`
  ADD CONSTRAINT `verifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
