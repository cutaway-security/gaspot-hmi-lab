-- GasPot HMI Lab - Historian Database Schema
-- Phase 1: Minimal schema for validation
-- Phase 3: Full implementation with seed data

-- Tank configuration (reference data)
CREATE TABLE IF NOT EXISTS tanks (
    tank_id INT PRIMARY KEY,
    product_name VARCHAR(20) NOT NULL,
    tank_type ENUM('NATURAL_GAS', 'DIESEL', 'WATER') NOT NULL,
    max_capacity DECIMAL(10,2) NOT NULL,
    capacity_unit VARCHAR(10) NOT NULL,
    has_pressure BOOLEAN DEFAULT FALSE
);

-- Tank readings (time-series data)
CREATE TABLE IF NOT EXISTS tank_readings (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    tank_id INT NOT NULL,
    timestamp DATETIME NOT NULL,
    volume DECIMAL(10,2),
    tc_volume DECIMAL(10,2),
    ullage DECIMAL(10,2),
    height DECIMAL(6,2),
    water_content DECIMAL(6,2),
    temperature DECIMAL(5,2),
    pressure DECIMAL(6,2),
    FOREIGN KEY (tank_id) REFERENCES tanks(tank_id),
    INDEX idx_tank_time (tank_id, timestamp)
);

-- Alarm history
CREATE TABLE IF NOT EXISTS alarms (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    tank_id INT NOT NULL,
    timestamp DATETIME NOT NULL,
    alarm_type VARCHAR(50) NOT NULL,
    severity ENUM('INFO', 'WARNING', 'CRITICAL') NOT NULL,
    message VARCHAR(255),
    acknowledged BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (tank_id) REFERENCES tanks(tank_id),
    INDEX idx_alarm_time (timestamp)
);

-- Initial tank configuration (6 tanks)
INSERT INTO tanks (tank_id, product_name, tank_type, max_capacity, capacity_unit, has_pressure) VALUES
(1, 'NG-MAIN',     'NATURAL_GAS', 50000, 'MCF', TRUE),
(2, 'NG-RESERVE',  'NATURAL_GAS', 50000, 'MCF', TRUE),
(3, 'NG-FEED',     'NATURAL_GAS', 10000, 'MCF', TRUE),
(4, 'DIESEL-PRI',  'DIESEL',      10000, 'GAL', FALSE),
(5, 'DIESEL-RES',  'DIESEL',      10000, 'GAL', FALSE),
(6, 'WATER-UTIL',  'WATER',       25000, 'GAL', FALSE);

-- Verify setup
SELECT 'Historian database initialized' AS status;
SELECT COUNT(*) AS tank_count FROM tanks;
