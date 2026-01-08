-- GasPot HMI Lab - Historian Database Schema
-- Complete implementation with seed data and stored procedures
--
-- Tables:
--   tanks - Tank configuration (6 tanks)
--   tank_readings - Time-series sensor data
--   alarms - Alarm history
--
-- Stored Procedures:
--   update_timestamps() - Shift historical data to current time
--   generate_seed_data() - Create 24 hours of realistic readings

-- ============================================================================
-- SCHEMA DEFINITION
-- ============================================================================

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

-- ============================================================================
-- TANK CONFIGURATION
-- ============================================================================

-- Clear existing data for clean initialization
DELETE FROM alarms;
DELETE FROM tank_readings;
DELETE FROM tanks;

-- Initial tank configuration (6 tanks)
INSERT INTO tanks (tank_id, product_name, tank_type, max_capacity, capacity_unit, has_pressure) VALUES
(1, 'NG-MAIN',     'NATURAL_GAS', 50000, 'MCF', TRUE),
(2, 'NG-RESERVE',  'NATURAL_GAS', 50000, 'MCF', TRUE),
(3, 'NG-FEED',     'NATURAL_GAS', 10000, 'MCF', TRUE),
(4, 'DIESEL-PRI',  'DIESEL',      10000, 'GAL', FALSE),
(5, 'DIESEL-RES',  'DIESEL',      10000, 'GAL', FALSE),
(6, 'WATER-UTIL',  'WATER',       25000, 'GAL', FALSE);

-- ============================================================================
-- STORED PROCEDURES
-- ============================================================================

DELIMITER //

-- Procedure to update timestamps to current time
-- This shifts all historical data so the most recent reading is NOW
DROP PROCEDURE IF EXISTS update_timestamps//
CREATE PROCEDURE update_timestamps()
BEGIN
    DECLARE offset_seconds INT;
    DECLARE max_reading_time DATETIME;
    DECLARE max_alarm_time DATETIME;

    -- Get the most recent timestamp from readings
    SELECT MAX(timestamp) INTO max_reading_time FROM tank_readings;

    -- Get the most recent timestamp from alarms
    SELECT MAX(timestamp) INTO max_alarm_time FROM alarms;

    -- Calculate offset from readings (primary)
    IF max_reading_time IS NOT NULL THEN
        SET offset_seconds = TIMESTAMPDIFF(SECOND, max_reading_time, NOW());

        -- Update tank_readings timestamps
        UPDATE tank_readings
        SET timestamp = DATE_ADD(timestamp, INTERVAL offset_seconds SECOND);
    END IF;

    -- Update alarms timestamps using same offset
    IF max_alarm_time IS NOT NULL AND offset_seconds IS NOT NULL THEN
        UPDATE alarms
        SET timestamp = DATE_ADD(timestamp, INTERVAL offset_seconds SECOND);
    END IF;

    SELECT 'Timestamps updated successfully' AS status;
END//

-- Procedure to generate seed data
-- Creates 24 hours of readings at 5-minute intervals (288 readings per tank)
DROP PROCEDURE IF EXISTS generate_seed_data//
CREATE PROCEDURE generate_seed_data()
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE reading_time DATETIME;
    DECLARE base_time DATETIME;

    -- Tank 1 variables (NG-MAIN - high fluctuation)
    DECLARE t1_vol DECIMAL(10,2) DEFAULT 38420;
    DECLARE t1_pressure DECIMAL(6,2) DEFAULT 485.2;
    DECLARE t1_temp DECIMAL(5,2) DEFAULT 58.2;

    -- Tank 2 variables (NG-RESERVE - low fluctuation)
    DECLARE t2_vol DECIMAL(10,2) DEFAULT 44850;
    DECLARE t2_pressure DECIMAL(6,2) DEFAULT 520.8;
    DECLARE t2_temp DECIMAL(5,2) DEFAULT 56.8;

    -- Tank 3 variables (NG-FEED - medium fluctuation)
    DECLARE t3_vol DECIMAL(10,2) DEFAULT 8240;
    DECLARE t3_pressure DECIMAL(6,2) DEFAULT 445.0;
    DECLARE t3_temp DECIMAL(5,2) DEFAULT 59.4;

    -- Tank 4 variables (DIESEL-PRI - decreasing)
    DECLARE t4_vol DECIMAL(10,2) DEFAULT 8500;
    DECLARE t4_temp DECIMAL(5,2) DEFAULT 68.5;

    -- Tank 5 variables (DIESEL-RES - static)
    DECLARE t5_vol DECIMAL(10,2) DEFAULT 9850;
    DECLARE t5_temp DECIMAL(5,2) DEFAULT 65.2;

    -- Tank 6 variables (WATER-UTIL - sawtooth)
    DECLARE t6_vol DECIMAL(10,2) DEFAULT 15000;
    DECLARE t6_temp DECIMAL(5,2) DEFAULT 52.4;
    DECLARE t6_direction INT DEFAULT 1;

    -- Start 24 hours ago
    SET base_time = DATE_SUB(NOW(), INTERVAL 24 HOUR);

    -- Generate 288 readings (every 5 minutes for 24 hours)
    WHILE i < 288 DO
        SET reading_time = DATE_ADD(base_time, INTERVAL (i * 5) MINUTE);

        -- Tank 1: High fluctuation (+/- 50)
        SET t1_vol = t1_vol + (RAND() * 100 - 50);
        SET t1_vol = GREATEST(30000, LEAST(45000, t1_vol));
        SET t1_pressure = t1_pressure + (RAND() * 10 - 5);
        SET t1_pressure = GREATEST(400, LEAST(600, t1_pressure));
        SET t1_temp = t1_temp + (RAND() * 1 - 0.5);
        SET t1_temp = GREATEST(55, LEAST(65, t1_temp));

        INSERT INTO tank_readings (tank_id, timestamp, volume, tc_volume, ullage, height, water_content, temperature, pressure)
        VALUES (1, reading_time, t1_vol, t1_vol * 0.995, 50000 - t1_vol, (t1_vol / 50000) * 96, 12.5 + RAND() * 5, t1_temp, t1_pressure);

        -- Tank 2: Low fluctuation (+/- 10)
        SET t2_vol = t2_vol + (RAND() * 20 - 10);
        SET t2_vol = GREATEST(40000, LEAST(48000, t2_vol));
        SET t2_pressure = t2_pressure + (RAND() * 2 - 1);
        SET t2_pressure = GREATEST(480, LEAST(560, t2_pressure));
        SET t2_temp = t2_temp + (RAND() * 0.5 - 0.25);
        SET t2_temp = GREATEST(54, LEAST(60, t2_temp));

        INSERT INTO tank_readings (tank_id, timestamp, volume, tc_volume, ullage, height, water_content, temperature, pressure)
        VALUES (2, reading_time, t2_vol, t2_vol * 0.995, 50000 - t2_vol, (t2_vol / 50000) * 96, 8.2 + RAND() * 2, t2_temp, t2_pressure);

        -- Tank 3: Medium fluctuation (+/- 25)
        SET t3_vol = t3_vol + (RAND() * 50 - 25);
        SET t3_vol = GREATEST(6000, LEAST(9500, t3_vol));
        SET t3_pressure = t3_pressure + (RAND() * 4 - 2);
        SET t3_pressure = GREATEST(400, LEAST(500, t3_pressure));
        SET t3_temp = t3_temp + (RAND() * 0.8 - 0.4);
        SET t3_temp = GREATEST(56, LEAST(63, t3_temp));

        INSERT INTO tank_readings (tank_id, timestamp, volume, tc_volume, ullage, height, water_content, temperature, pressure)
        VALUES (3, reading_time, t3_vol, t3_vol * 0.995, 10000 - t3_vol, (t3_vol / 10000) * 96, 4.1 + RAND() * 2, t3_temp, t3_pressure);

        -- Tank 4: Decreasing (consumption)
        SET t4_vol = t4_vol - (RAND() * 8);
        SET t4_vol = GREATEST(5000, t4_vol);
        SET t4_temp = t4_temp + (RAND() * 1 - 0.5);
        SET t4_temp = GREATEST(60, LEAST(75, t4_temp));

        INSERT INTO tank_readings (tank_id, timestamp, volume, tc_volume, ullage, height, water_content, temperature, pressure)
        VALUES (4, reading_time, t4_vol, t4_vol * 0.995, 10000 - t4_vol, (t4_vol / 10000) * 96, 0.4 + RAND() * 0.2, t4_temp, NULL);

        -- Tank 5: Static (minimal change)
        SET t5_vol = t5_vol + (RAND() * 4 - 2);
        SET t5_vol = GREATEST(9700, LEAST(9950, t5_vol));
        SET t5_temp = t5_temp + (RAND() * 0.5 - 0.25);
        SET t5_temp = GREATEST(62, LEAST(70, t5_temp));

        INSERT INTO tank_readings (tank_id, timestamp, volume, tc_volume, ullage, height, water_content, temperature, pressure)
        VALUES (5, reading_time, t5_vol, t5_vol * 0.995, 10000 - t5_vol, (t5_vol / 10000) * 96, 0.1 + RAND() * 0.1, t5_temp, NULL);

        -- Tank 6: Sawtooth pattern (fill/drain cycle)
        IF t6_direction = 1 THEN
            SET t6_vol = t6_vol + 150;
            IF t6_vol >= 23000 THEN
                SET t6_direction = -1;
            END IF;
        ELSE
            SET t6_vol = t6_vol - 75;
            IF t6_vol <= 12000 THEN
                SET t6_direction = 1;
            END IF;
        END IF;
        SET t6_temp = t6_temp + (RAND() * 0.6 - 0.3);
        SET t6_temp = GREATEST(45, LEAST(60, t6_temp));

        INSERT INTO tank_readings (tank_id, timestamp, volume, tc_volume, ullage, height, water_content, temperature, pressure)
        VALUES (6, reading_time, t6_vol, t6_vol, 25000 - t6_vol, (t6_vol / 25000) * 120, 0, t6_temp, NULL);

        SET i = i + 1;
    END WHILE;

    SELECT CONCAT('Generated ', i * 6, ' tank readings') AS status;
END//

DELIMITER ;

-- ============================================================================
-- GENERATE SEED DATA
-- ============================================================================

CALL generate_seed_data();

-- ============================================================================
-- SAMPLE ALARMS
-- ============================================================================

-- Generate alarms over the past 24 hours
INSERT INTO alarms (tank_id, timestamp, alarm_type, severity, message, acknowledged) VALUES
-- Tank 1 (NG-MAIN) alarms
(1, DATE_SUB(NOW(), INTERVAL 23 HOUR), 'PRESSURE_HIGH', 'WARNING', 'Tank 1 pressure above normal operating range (595 PSI)', FALSE),
(1, DATE_SUB(NOW(), INTERVAL 18 HOUR), 'VOLUME_CHANGE', 'INFO', 'Tank 1 volume decreased by 500 MCF in 1 hour', TRUE),
(1, DATE_SUB(NOW(), INTERVAL 12 HOUR), 'TEMPERATURE_VARIANCE', 'INFO', 'Tank 1 temperature fluctuation detected (3.2F change)', TRUE),
(1, DATE_SUB(NOW(), INTERVAL 6 HOUR), 'PRESSURE_RESTORED', 'INFO', 'Tank 1 pressure returned to normal range', TRUE),

-- Tank 2 (NG-RESERVE) alarms
(2, DATE_SUB(NOW(), INTERVAL 20 HOUR), 'SYSTEM_CHECK', 'INFO', 'Scheduled system verification completed for Tank 2', TRUE),

-- Tank 3 (NG-FEED) alarms
(3, DATE_SUB(NOW(), INTERVAL 16 HOUR), 'LOW_LEVEL', 'WARNING', 'Tank 3 level below 70% capacity (6850 MCF)', FALSE),
(3, DATE_SUB(NOW(), INTERVAL 14 HOUR), 'FILL_STARTED', 'INFO', 'Tank 3 fill operation initiated', TRUE),
(3, DATE_SUB(NOW(), INTERVAL 13 HOUR), 'FILL_COMPLETE', 'INFO', 'Tank 3 fill operation completed (8500 MCF)', TRUE),

-- Tank 4 (DIESEL-PRI) alarms
(4, DATE_SUB(NOW(), INTERVAL 22 HOUR), 'CONSUMPTION_RATE', 'INFO', 'Tank 4 consumption rate: 45 GAL/hour', TRUE),
(4, DATE_SUB(NOW(), INTERVAL 10 HOUR), 'LOW_LEVEL', 'WARNING', 'Tank 4 level below 70% capacity (6500 GAL)', FALSE),
(4, DATE_SUB(NOW(), INTERVAL 4 HOUR), 'LOW_LEVEL', 'CRITICAL', 'Tank 4 level below 60% capacity (5800 GAL)', FALSE),

-- Tank 5 (DIESEL-RES) alarms
(5, DATE_SUB(NOW(), INTERVAL 19 HOUR), 'SYSTEM_CHECK', 'INFO', 'Scheduled system verification completed for Tank 5', TRUE),

-- Tank 6 (WATER-UTIL) alarms
(6, DATE_SUB(NOW(), INTERVAL 21 HOUR), 'FILL_CYCLE_START', 'INFO', 'Tank 6 automatic fill cycle initiated', TRUE),
(6, DATE_SUB(NOW(), INTERVAL 17 HOUR), 'HIGH_LEVEL', 'WARNING', 'Tank 6 level above 90% capacity (22800 GAL)', TRUE),
(6, DATE_SUB(NOW(), INTERVAL 15 HOUR), 'DRAIN_CYCLE_START', 'INFO', 'Tank 6 drain cycle initiated', TRUE),
(6, DATE_SUB(NOW(), INTERVAL 8 HOUR), 'LOW_LEVEL', 'WARNING', 'Tank 6 level below 50% capacity (12200 GAL)', TRUE),
(6, DATE_SUB(NOW(), INTERVAL 5 HOUR), 'FILL_CYCLE_START', 'INFO', 'Tank 6 automatic fill cycle initiated', TRUE),
(6, DATE_SUB(NOW(), INTERVAL 2 HOUR), 'LEVEL_NORMAL', 'INFO', 'Tank 6 level returned to normal range', TRUE);

-- ============================================================================
-- VERIFICATION
-- ============================================================================

SELECT 'Historian database initialized successfully' AS status;
SELECT 'Table counts:' AS info;
SELECT 'tanks' AS table_name, COUNT(*) AS row_count FROM tanks
UNION ALL
SELECT 'tank_readings', COUNT(*) FROM tank_readings
UNION ALL
SELECT 'alarms', COUNT(*) FROM alarms;

SELECT 'Sample tank_readings (last 5):' AS info;
SELECT tank_id, timestamp, volume, pressure
FROM tank_readings
ORDER BY timestamp DESC
LIMIT 5;

SELECT 'Active alarms (not acknowledged):' AS info;
SELECT tank_id, alarm_type, severity, message
FROM alarms
WHERE acknowledged = FALSE;
