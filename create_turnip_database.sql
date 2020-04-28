DROP DATABASE IF EXISTS turnip;
CREATE DATABASE turnip;
USE turnip;

SET NAMES utf8mb4;
SET character_set_client = utf8mb4;
	
CREATE TABLE buy_data (
	user_id VARCHAR(16) NOT NULL,
    island_id VARCHAR(32) NOT NULL,
    price SMALLINT UNSIGNED,
    datetime_observed DATETIME,
    PRIMARY KEY (user_id, island_id, datetime_observed)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE sell_data (
	user_id VARCHAR(16) NOT NULL,
    island_id VARCHAR(32) NOT NULL,
    price SMALLINT UNSIGNED,
    datetime_observed DATETIME,
    PRIMARY KEY (user_id, island_id, datetime_observed)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
