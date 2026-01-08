# Database Reference

This document provides reference information for the GasPot HMI Lab historian database, including schema details and useful queries for the exercises.

---

## Table of Contents

1. [Connection Information](#connection-information)
2. [Database Schema](#database-schema)
3. [Table: tanks](#table-tanks)
4. [Table: tank_readings](#table-tank_readings)
5. [Table: alarms](#table-alarms)
6. [Useful Queries](#useful-queries)
7. [Data Manipulation Examples](#data-manipulation-examples)

---

## Connection Information

### Credentials

| Parameter | Value |
|-----------|-------|
| Host | localhost |
| Port | 3306 |
| Database | historian |
| Username | lab |
| Password | password |

### Connection Methods

**Via Docker (recommended):**
```bash
docker exec -it gaspot-historian mysql -u lab -ppassword historian
```

**Direct connection (if MySQL client installed):**
```bash
mysql -h localhost -P 3306 -u lab -ppassword historian
```

**Note:** The `-ppassword` has no space between `-p` and the password.

---

## Database Schema

The historian database contains three tables:

| Table | Purpose | Records |
|-------|---------|---------|
| tanks | Tank configuration (reference data) | 6 rows (static) |
| tank_readings | Time-series tank measurements | ~1700+ rows (grows over time) |
| alarms | Alarm history | ~20+ rows (grows over time) |

### Entity Relationship

```
tanks (1) ----< (many) tank_readings
tanks (1) ----< (many) alarms
```

---

## Table: tanks

Tank configuration and reference data. This table is static and defines the 6 tanks in the system.

### Schema

```sql
CREATE TABLE tanks (
    tank_id INT PRIMARY KEY,
    product_name VARCHAR(20) NOT NULL,
    tank_type ENUM('NATURAL_GAS', 'DIESEL', 'WATER') NOT NULL,
    max_capacity DECIMAL(10,2) NOT NULL,
    capacity_unit VARCHAR(10) NOT NULL,
    has_pressure BOOLEAN DEFAULT FALSE
);
```

### Columns

| Column | Type | Description |
|--------|------|-------------|
| tank_id | INT | Primary key (1-6) |
| product_name | VARCHAR(20) | Display name (e.g., "NG-MAIN") |
| tank_type | ENUM | Type: NATURAL_GAS, DIESEL, or WATER |
| max_capacity | DECIMAL(10,2) | Maximum capacity |
| capacity_unit | VARCHAR(10) | Unit: MCF or GAL |
| has_pressure | BOOLEAN | Whether tank has pressure sensor |

### Current Data

| tank_id | product_name | tank_type | max_capacity | capacity_unit | has_pressure |
|---------|--------------|-----------|--------------|---------------|--------------|
| 1 | NG-MAIN | NATURAL_GAS | 50000.00 | MCF | 1 |
| 2 | NG-RESERVE | NATURAL_GAS | 50000.00 | MCF | 1 |
| 3 | NG-FEED | NATURAL_GAS | 10000.00 | MCF | 1 |
| 4 | DIESEL-PRI | DIESEL | 10000.00 | GAL | 0 |
| 5 | DIESEL-RES | DIESEL | 10000.00 | GAL | 0 |
| 6 | WATER-UTIL | WATER | 25000.00 | GAL | 0 |

---

## Table: tank_readings

Time-series data storing periodic tank measurements from the HMI polling loop.

### Schema

```sql
CREATE TABLE tank_readings (
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
```

### Columns

| Column | Type | Description |
|--------|------|-------------|
| id | BIGINT | Auto-increment primary key |
| tank_id | INT | Foreign key to tanks table |
| timestamp | DATETIME | When reading was recorded |
| volume | DECIMAL(10,2) | Current volume (MCF or GAL) |
| tc_volume | DECIMAL(10,2) | Temperature-compensated volume |
| ullage | DECIMAL(10,2) | Empty space in tank |
| height | DECIMAL(6,2) | Product height (inches) |
| water_content | DECIMAL(6,2) | Water in tank |
| temperature | DECIMAL(5,2) | Temperature (Fahrenheit) |
| pressure | DECIMAL(6,2) | Pressure (PSI, NULL if N/A) |

### Notes

- New readings are added every ~10 seconds by the HMI poller
- Initial seed data contains ~24 hours of historical readings
- Pressure is NULL for tanks 4-6 (non-pressurized)

---

## Table: alarms

Alarm history tracking system alerts and events.

### Schema

```sql
CREATE TABLE alarms (
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
```

### Columns

| Column | Type | Description |
|--------|------|-------------|
| id | BIGINT | Auto-increment primary key |
| tank_id | INT | Foreign key to tanks table |
| timestamp | DATETIME | When alarm occurred |
| alarm_type | VARCHAR(50) | Type (e.g., LOW_LEVEL, OVERPRESSURE) |
| severity | ENUM | INFO, WARNING, or CRITICAL |
| message | VARCHAR(255) | Human-readable alarm message |
| acknowledged | BOOLEAN | Whether operator acknowledged |

### Alarm Types

| Type | Description |
|------|-------------|
| LOW_LEVEL | Tank volume below threshold |
| HIGH_LEVEL | Tank volume above threshold |
| OVERPRESSURE | Pressure exceeds safe limit |
| UNDERPRESSURE | Pressure below safe limit |
| HIGH_TEMP | Temperature exceeds threshold |
| LOW_TEMP | Temperature below threshold |
| LEAK_DETECTED | Possible leak detected |
| SENSOR_FAULT | Sensor malfunction |

### Severity Levels

| Severity | Description | Display |
|----------|-------------|---------|
| INFO | Informational | Blue |
| WARNING | Needs attention | Yellow |
| CRITICAL | Immediate action required | Red |

---

## Useful Queries

### Exploring the Schema

```sql
-- List all tables
SHOW TABLES;

-- Describe table structure
DESCRIBE tanks;
DESCRIBE tank_readings;
DESCRIBE alarms;

-- Count records
SELECT COUNT(*) FROM tank_readings;
SELECT COUNT(*) FROM alarms;
```

### Tank Information

```sql
-- List all tanks
SELECT * FROM tanks;

-- List tanks with pressure sensors
SELECT * FROM tanks WHERE has_pressure = TRUE;

-- List tanks by type
SELECT * FROM tanks WHERE tank_type = 'NATURAL_GAS';
```

### Tank Readings

```sql
-- Latest reading for each tank
SELECT t.product_name, tr.*
FROM tank_readings tr
JOIN tanks t ON tr.tank_id = t.tank_id
WHERE tr.timestamp = (
    SELECT MAX(timestamp)
    FROM tank_readings
    WHERE tank_id = tr.tank_id
)
ORDER BY tr.tank_id;

-- Recent readings (last 10)
SELECT * FROM tank_readings
ORDER BY timestamp DESC
LIMIT 10;

-- Readings for specific tank
SELECT * FROM tank_readings
WHERE tank_id = 1
ORDER BY timestamp DESC
LIMIT 20;

-- Average volume by tank (last hour)
SELECT tank_id, AVG(volume) as avg_volume
FROM tank_readings
WHERE timestamp > DATE_SUB(NOW(), INTERVAL 1 HOUR)
GROUP BY tank_id;

-- Volume range by tank
SELECT tank_id,
       MIN(volume) as min_vol,
       MAX(volume) as max_vol,
       MAX(volume) - MIN(volume) as range
FROM tank_readings
GROUP BY tank_id;
```

### Alarms

```sql
-- All alarms (most recent first)
SELECT * FROM alarms ORDER BY timestamp DESC;

-- Active (unacknowledged) alarms
SELECT * FROM alarms
WHERE acknowledged = FALSE
ORDER BY timestamp DESC;

-- Critical alarms only
SELECT * FROM alarms
WHERE severity = 'CRITICAL'
ORDER BY timestamp DESC;

-- Alarm count by severity
SELECT severity, COUNT(*) as count
FROM alarms
GROUP BY severity;

-- Alarm count by tank
SELECT t.product_name, COUNT(a.id) as alarm_count
FROM tanks t
LEFT JOIN alarms a ON t.tank_id = a.tank_id
GROUP BY t.tank_id, t.product_name;

-- Alarms with tank names
SELECT a.*, t.product_name
FROM alarms a
JOIN tanks t ON a.tank_id = t.tank_id
ORDER BY a.timestamp DESC;
```

### Historical Analysis

```sql
-- Readings per hour
SELECT DATE_FORMAT(timestamp, '%Y-%m-%d %H:00') as hour,
       COUNT(*) as readings
FROM tank_readings
GROUP BY hour
ORDER BY hour DESC
LIMIT 24;

-- Temperature trends for tank 1
SELECT timestamp, temperature
FROM tank_readings
WHERE tank_id = 1
ORDER BY timestamp DESC
LIMIT 100;
```

---

## Data Manipulation Examples

These examples demonstrate how an attacker could modify historical data.

### Modifying Tank Readings

```sql
-- Change the most recent volume reading for tank 1
UPDATE tank_readings
SET volume = 0
WHERE tank_id = 1
ORDER BY timestamp DESC
LIMIT 1;

-- Set all recent readings to suspicious values
UPDATE tank_readings
SET volume = 99999
WHERE tank_id = 1
AND timestamp > DATE_SUB(NOW(), INTERVAL 10 MINUTE);

-- Modify temperature readings
UPDATE tank_readings
SET temperature = 999.99
WHERE tank_id = 1
ORDER BY timestamp DESC
LIMIT 5;
```

### Creating False Alarms

```sql
-- Insert a fake critical alarm
INSERT INTO alarms (tank_id, alarm_type, severity, message, timestamp)
VALUES (1, 'OVERFLOW', 'CRITICAL', 'Tank overflow detected - EVACUATE', NOW());

-- Insert multiple alarms
INSERT INTO alarms (tank_id, alarm_type, severity, message, timestamp)
VALUES
(1, 'LEAK_DETECTED', 'CRITICAL', 'Leak detected - immediate action required', NOW()),
(2, 'OVERPRESSURE', 'CRITICAL', 'Pressure exceeding safe limits', NOW());

-- Create alarm backdated by 1 hour
INSERT INTO alarms (tank_id, alarm_type, severity, message, timestamp)
VALUES (3, 'SENSOR_FAULT', 'WARNING', 'Sensor malfunction detected',
        DATE_SUB(NOW(), INTERVAL 1 HOUR));
```

### Acknowledging Alarms

```sql
-- Acknowledge all alarms (hide them from active view)
UPDATE alarms SET acknowledged = TRUE;

-- Acknowledge specific alarm
UPDATE alarms SET acknowledged = TRUE WHERE id = 5;

-- Un-acknowledge to make alarms visible again
UPDATE alarms SET acknowledged = FALSE WHERE id = 5;
```

### Deleting Evidence

```sql
-- Delete alarms you created
DELETE FROM alarms WHERE message LIKE '%EVACUATE%';

-- Delete recent readings (cover tracks)
DELETE FROM tank_readings
WHERE timestamp > DATE_SUB(NOW(), INTERVAL 5 MINUTE);
```

### Cleanup

After experimenting, you can reset the lab:

```bash
./scripts/reset_lab.sh
./scripts/start_lab.sh
```

---

## Stored Procedures

### update_timestamps

Updates all timestamps in the database to be relative to the current time. Called automatically by `start_lab.sh`.

```sql
-- Call manually if needed
CALL update_timestamps();
```

This shifts all readings and alarms so the most recent data appears current, making the seed data appear fresh.

---

## Security Notes

The database credentials are intentionally weak for this lab:

| User | Password | Privileges |
|------|----------|------------|
| lab | password | Full access to historian database |
| root | admin | Full MySQL admin |

In a real environment, attackers could:
- Guess weak credentials
- Use SQL injection to access the database
- Exploit unpatched database vulnerabilities

---

## Quick Reference

### Connection
```bash
docker exec -it gaspot-historian mysql -u lab -ppassword historian
```

### Essential Queries
```sql
-- Schema
SHOW TABLES;
DESCRIBE tank_readings;

-- Current state
SELECT * FROM tanks;
SELECT * FROM tank_readings ORDER BY timestamp DESC LIMIT 10;
SELECT * FROM alarms WHERE acknowledged = FALSE;

-- Manipulation
UPDATE tank_readings SET volume = 0 WHERE tank_id = 1 ORDER BY timestamp DESC LIMIT 1;
INSERT INTO alarms (tank_id, alarm_type, severity, message, timestamp)
VALUES (1, 'CRITICAL', 'CRITICAL', 'Attack message', NOW());
```
