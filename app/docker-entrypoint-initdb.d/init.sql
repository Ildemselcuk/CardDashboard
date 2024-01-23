-- Adminer 4.8.1 MySQL 8.0.25 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
set sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

SET NAMES utf8mb4;

CREATE DATABASE `db1` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `db1`;

DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `alembic_version` (`version_num`) VALUES
('ea2dd3aa1090');

DROP TABLE IF EXISTS `card`;
CREATE TABLE `card` (
  `id` int NOT NULL AUTO_INCREMENT,
  `label` varchar(256) DEFAULT NULL,
  `card_no` varchar(256) DEFAULT NULL,
  `user_id` int NOT NULL,
  `status` varchar(256) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_user_card_uc` (`user_id`,`card_no`),
  CONSTRAINT `card_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `card` (`id`, `label`, `card_no`, `user_id`, `status`, `date_created`, `date_modified`) VALUES
(6,	'6',	'4057162210860601',	6,	'DELETED',	'2024-01-23 02:06:05',	'2024-01-23 06:30:35'),
(7,	'7',	'8738578582233561',	7,	'PASSIVE',	'2024-01-23 02:09:53',	'2024-01-23 02:09:53'),
(8,	'Test Card',	'499058007080103',	6,	'ACTIVE',	'2024-01-23 03:44:43',	'2024-01-23 03:44:43'),
(9,	'Test Changed Card',	'589058007080102',	6,	'PASSIVE',	'2024-01-23 06:12:48',	'2024-01-23 08:04:12');

DROP TABLE IF EXISTS `transactions`;
CREATE TABLE `transactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `amount` float DEFAULT NULL,
  `description` varchar(256) DEFAULT NULL,
  `card_id` int NOT NULL,
  `date_created` datetime DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `card_id` (`card_id`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`card_id`) REFERENCES `card` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `transactions` (`id`, `amount`, `description`, `card_id`, `date_created`, `date_modified`) VALUES
(2,	550,	'Test Process',	7,	'2024-01-23 05:25:25',	'2024-01-23 05:25:25'),
(3,	550,	'Test Process',	7,	'2024-01-23 05:25:25',	'2024-01-23 05:25:25');

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_user_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `user` (`id`, `email`, `password`, `date_created`, `date_modified`) VALUES
(6,	'test@test.com',	'test',	'2024-01-23 02:06:05',	'2024-01-23 02:06:05'),
(7,	'test1@test.com',	'test1',	'2024-01-23 02:09:53',	'2024-01-23 02:09:53');

-- 2024-01-23 05:05:52
