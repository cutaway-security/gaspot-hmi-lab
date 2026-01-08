# ARCHITECTURE.md - System Design and Technical Standards

## Overview

The GasPot HMI Lab simulates a Natural Gas Distribution Terminal with tank monitoring capabilities. The system consists of three Docker containers that communicate via a bridge network.

---

## Documentation Structure

The project documentation is organized into three categories based on audience:

```
gaspot-hmi-lab/
    README.md                     # Project overview and quick start

    docs/                         # Operations & Maintenance (lab operators)
        OPERATIONS.md             # Container management, troubleshooting
        GASPOT_MODIFICATIONS.md   # Changes from original GasPot project

    exercises/                    # Student Content (lab users)
        README.md                 # Scenario introduction and getting started
        E01_DISCOVERY.md          # Exercise 1: Network reconnaissance
        E02_ENUMERATION.md        # Exercise 2: Protocol analysis
        E03_ATG_MANIPULATION.md   # Exercise 3: ATG data manipulation
        E04_HMI_RECONNAISSANCE.md # Exercise 4: Web interface analysis
        E05_DATABASE_EXPLOITATION.md  # Exercise 5: Historian attacks
        E06_ATTACK_CHAIN.md       # Exercise 6: Combined attack scenario
        E07_DEFENSE_ANALYSIS.md   # Exercise 7: Security assessment
        challenges/               # Additional challenge exercises
            C01_AUTOMATED_ATTACK.md
            C02_DETECTION_SCRIPT.md
            C03_PROTOCOL_ANALYSIS.md
        docs/                     # Reference materials for students
            PROTOCOL_REFERENCE.md # TLS-350 commands, ATG client usage
            DATABASE_REFERENCE.md # Database schema, useful queries
        INSTRUCTOR_GUIDE.md       # Teaching guide with goals and approaches

    dev/                          # Development (not distributed to main)
        ARCHITECTURE.md           # This file - technical design
        PLAN.md                   # Project roadmap and phases
        RESUME.md                 # Session context for development
        VIBE_HISTORY.md           # Lessons learned and activity log
```

### Documentation Audiences

| Directory | Audience | Purpose |
|-----------|----------|---------|
| README.md | Everyone | Quick orientation and getting started |
| docs/ | Lab operators, maintainers | Deploy, manage, troubleshoot the lab |
| exercises/ | Students, learners | Hands-on security exercises |
| exercises/docs/ | Students | Reference materials during exercises |
| dev/ | Developers | Internal development tracking |

### Key Files by Use Case

| Use Case | Primary Document |
|----------|------------------|
| "How do I start the lab?" | README.md |
| "How do I run exercises?" | exercises/README.md |
| "What TLS-350 commands exist?" | exercises/docs/PROTOCOL_REFERENCE.md |
| "What's the database schema?" | exercises/docs/DATABASE_REFERENCE.md |
| "Container won't start" | docs/OPERATIONS.md |
| "What was changed from original GasPot?" | docs/GASPOT_MODIFICATIONS.md |
| "How should I teach this lab?" | exercises/INSTRUCTOR_GUIDE.md |

---

## System Architecture

```
+------------------+                              +------------------+
|   Student Host   |------- TLS-350 ------------>|    GasPot        |
|   (Kali Linux)   |       TCP/10001             |   Container      |
|                  |                             |                  |
|  Tools:          |       Commands:             |   6 Tanks:       |
|  - telnet        |       I20100 (inventory)    |   - 3x Nat Gas   |
|  - atg_client.py |       I20200 (delivery)     |   - 2x Diesel    |
|  - nmap NSE      |       I20300 (leak)         |   - 1x Water     |
|  - Metasploit    |       I20400 (shift)        |                  |
|                  |       I20500 (status)       |   Fluctuation    |
|                  |       I20600 (pressure)     |   Engine         |
|                  |       S602xx (writes)       |                  |
+------------------+<----------------------------+--------+---------+
                                                          |
        +------------------+                              |
        |   Web Browser    |                              |
        |   HTTP/5000      |                              |
        +--------+---------+                              |
                 |                                        |
                 v                                        |
        +------------------+     TLS-350 Poll    +--------+
        |       HMI        |<--------------------+
        |   Container      |     Every 5-10 sec
        |   (Flask App)    |
        |                  |
        |  Views:          |
        |  - Tank Overview |------+
        |  - Trends/Charts |      |
        |  - Alarm Status  |      |  SQL Write
        |  - History Log   |      |  (readings)
        +------------------+      |
                 |                v
                 |       +------------------+
                 +------>|    MariaDB       |
              SQL Read   |   Historian      |
             (trends)    |   Container      |
                         |   TCP/3306       |
                         |                  |
                         |  Tables:         |
                         |  - tank_readings |
                         |  - alarms        |
                         |  - tanks         |
                         +------------------+
                                  ^
                                  |
                         +--------+---------+
                         |   Student Host   |
                         |   mysql client   |
                         |                  |
                         |   Can modify:    |
                         |   - History      |
                         |   - Alarm states |
                         +------------------+
```

---

## Data Flow

### Primary Data Flow

1. **GasPot maintains authoritative state** for all tank data (volume, temp, pressure)
2. **Students interact via TLS-350** on port 10001
   - Read operations: I20100, I20200, I20300, I20400, I20500, I20600
   - Write operations: S602xx commands change GasPot's internal state
3. **HMI polls GasPot periodically** (every 5-10 seconds) via TLS-350
   - Fetches current values for volume, temperature, pressure
   - Stores readings to historian with timestamp
4. **HMI displays**:
   - Current state (from latest poll)
   - Historical trends (from database queries)
5. **Students can modify historian directly** via SQL
   - Changes appear in HMI historical charts
   - Does NOT affect GasPot's current state

### Student Exercise Flow

1. **Discovery**: Use nmap to find port 10001
2. **Enumeration**: Send I20100 via telnet/script, see inventory
3. **Observe**: View same data in HMI web interface
4. **Manipulate**: Send S60210 to change tank volume
5. **Verify**: See change reflected in HMI display
6. **Historical Attack**: Connect to MariaDB, modify past records
7. **Analysis**: Observe manipulated history in HMI charts

---

## Tank Configuration

### Tank Inventory

| Tank # | Product | Type | Capacity | Unit | Has Pressure | Fluctuation |
|--------|---------|------|----------|------|--------------|-------------|
| 1 | NG-MAIN | Natural Gas | 50000 | MCF | Yes | High |
| 2 | NG-RESERVE | Natural Gas | 50000 | MCF | Yes | Low |
| 3 | NG-FEED | Natural Gas | 10000 | MCF | Yes | Medium |
| 4 | DIESEL-PRI | Diesel | 10000 | GAL | No | Decrease |
| 5 | DIESEL-RES | Diesel | 10000 | GAL | No | Static |
| 6 | WATER-UTIL | Water | 25000 | GAL | No | Sawtooth |

### Tank Data Points

**Natural Gas Tanks (1-3)**:
| Metric | Unit | Range |
|--------|------|-------|
| Volume | MCF | 0-50000 |
| TC Volume | MCF | 0-50000 |
| Ullage | MCF | 0-50000 |
| Pressure | PSI | 200-800 |
| Temperature | F | 40-90 |
| Water | GAL | 0-50 |

**Diesel Fuel Tanks (4-5)**:
| Metric | Unit | Range |
|--------|------|-------|
| Volume | GAL | 0-10000 |
| TC Volume | GAL | 0-10000 |
| Ullage | GAL | 0-10000 |
| Height | IN | 0-96 |
| Temperature | F | 40-100 |
| Water | IN | 0-2 |

**Water Tank (6)**:
| Metric | Unit | Range |
|--------|------|-------|
| Volume | GAL | 0-25000 |
| TC Volume | GAL | 0-25000 |
| Ullage | GAL | 0-25000 |
| Height | IN | 0-120 |
| Temperature | F | 35-80 |

---

## TLS-350 Protocol Specification

### Command Format

```
Command Structure: 0x01 + COMMAND + 0x0A
                   ^       ^        ^
                   |       |        +-- Newline terminator
                   |       +----------- Command string (e.g., "I20100")
                   +------------------- SOH byte (Ctrl+A)
```

### Supported Commands

**Read Commands**:
| Code | Name | Description |
|------|------|-------------|
| I20100 | In-Tank Inventory Report | Volume, TC Volume, Ullage, Height, Water, Temp for all tanks |
| I20200 | In-Tank Delivery Report | Recent delivery information |
| I20300 | In-Tank Leak Detect Report | Leak status for all tanks |
| I20400 | In-Tank Shift Report | Shift inventory tracking |
| I20500 | In-Tank Status Report | Current status of all tanks |
| I20600 | Pressure Sensor Report | Pressure readings (gas tanks only) |

**Write Commands**:
| Code | Name | Format | Description |
|------|------|--------|-------------|
| S60201 | Set Tank 1 Name | S60201NEWNAME | Change tank 1 product name |
| S60202 | Set Tank 2 Name | S60202NEWNAME | Change tank 2 product name |
| S60203 | Set Tank 3 Name | S60203NEWNAME | Change tank 3 product name |
| S60204 | Set Tank 4 Name | S60204NEWNAME | Change tank 4 product name |
| S60210 | Set Tank Volume | S60210:TANK:VALUE | Set volume for specified tank |
| S60220 | Set Tank Pressure | S60220:TANK:VALUE | Set pressure for specified tank |

### Response Format

**I20100 Response Example**:
```
JAN 06, 2026  2:34 PM

     RIVERSIDE NATURAL GAS TERMINAL


IN-TANK INVENTORY

TANK PRODUCT             VOLUME TC VOLUME   ULLAGE   HEIGHT    WATER     TEMP
  1  NG-MAIN              38420    38105    11580    72.45     12.5    58.20
  2  NG-RESERVE           44850    44520     5150    84.30      8.2    56.80
  3  NG-FEED               8240     8180     1760    62.10      4.1    59.40
  4  DIESEL-PRI            6842     6790     3158    65.50      0.40   68.50
  5  DIESEL-RES            9850     9780      150    94.20      0.10   65.20
  6  WATER-UTIL           18500    18500     6500    88.80      0.00   52.40
```

**I20600 Response Example**:
```
JAN 06, 2026  2:34 PM

     RIVERSIDE NATURAL GAS TERMINAL


PRESSURE SENSOR REPORT

TANK PRODUCT             PRESSURE    STATUS
  1  NG-MAIN              485.2 PSI  NORMAL
  2  NG-RESERVE           520.8 PSI  NORMAL
  3  NG-FEED              445.0 PSI  NORMAL
  4  DIESEL-PRI             N/A      ATMOSPHERIC
  5  DIESEL-RES             N/A      ATMOSPHERIC
  6  WATER-UTIL             N/A      ATMOSPHERIC
```

**Error Response**:
```
9999FF1B
```
Returned when command is not recognized or malformed.

---

## Database Schema

```sql
-- Tank configuration (reference data)
CREATE TABLE tanks (
    tank_id INT PRIMARY KEY,
    product_name VARCHAR(20) NOT NULL,
    tank_type ENUM('NATURAL_GAS', 'DIESEL', 'WATER') NOT NULL,
    max_capacity DECIMAL(10,2) NOT NULL,
    capacity_unit VARCHAR(10) NOT NULL,
    has_pressure BOOLEAN DEFAULT FALSE
);

-- Tank readings (time-series data)
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

-- Alarm history
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

-- Stored procedure for timestamp updates
DELIMITER //
CREATE PROCEDURE update_timestamps()
BEGIN
    DECLARE offset_seconds INT;
    SET offset_seconds = TIMESTAMPDIFF(SECOND, 
        (SELECT MAX(timestamp) FROM tank_readings), 
        NOW());
    
    UPDATE tank_readings 
    SET timestamp = DATE_ADD(timestamp, INTERVAL offset_seconds SECOND);
    
    UPDATE alarms 
    SET timestamp = DATE_ADD(timestamp, INTERVAL offset_seconds SECOND);
END //
DELIMITER ;

-- Initial tank configuration
INSERT INTO tanks VALUES
(1, 'NG-MAIN',     'NATURAL_GAS', 50000, 'MCF', TRUE),
(2, 'NG-RESERVE',  'NATURAL_GAS', 50000, 'MCF', TRUE),
(3, 'NG-FEED',     'NATURAL_GAS', 10000, 'MCF', TRUE),
(4, 'DIESEL-PRI',  'DIESEL',      10000, 'GAL', FALSE),
(5, 'DIESEL-RES',  'DIESEL',      10000, 'GAL', FALSE),
(6, 'WATER-UTIL',  'WATER',       25000, 'GAL', FALSE);
```

---

## Container Configuration

### Docker Compose Version Compatibility

**CRITICAL**: Docker Compose V1 vs V2

| Version | Command | Status |
|---------|---------|--------|
| V1 | `docker-compose` (hyphen) | Deprecated July 2023 |
| V2 | `docker compose` (space) | Current |

Scripts MUST support both command syntaxes for student environment compatibility.

**Detection Logic**:
```bash
if docker compose version &>/dev/null; then
    COMPOSE_CMD="docker compose"
elif docker-compose version &>/dev/null; then
    COMPOSE_CMD="docker-compose"
else
    echo "Docker Compose not found"
    exit 1
fi
```

### Docker Compose Configuration

```yaml
services:
  mariadb:
    image: mariadb:10.11
    container_name: gaspot-historian
    environment:
      MYSQL_ROOT_PASSWORD: admin
      MYSQL_DATABASE: historian
      MYSQL_USER: lab
      MYSQL_PASSWORD: password
    volumes:
      - historian_data:/var/lib/mysql
      - ./historian/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    ports:
      - "3306:3306"
    networks:
      - labnet
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "lab", "-ppassword"]
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 30s
    restart: unless-stopped

  gaspot:
    build:
      context: ./gaspot
      dockerfile: Dockerfile
    container_name: gaspot-simulator
    ports:
      - "10001:10001"
    networks:
      - labnet
    depends_on:
      mariadb:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "nc -z localhost 10001 || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
    restart: unless-stopped

  hmi:
    build:
      context: ./hmi
      dockerfile: Dockerfile
    container_name: gaspot-hmi
    environment:
      GASPOT_HOST: gaspot-simulator
      GASPOT_PORT: 10001
      DB_HOST: gaspot-historian
      DB_PORT: 3306
      DB_USER: lab
      DB_PASSWORD: password
      DB_NAME: historian
    ports:
      - "5000:5000"
    networks:
      - labnet
    depends_on:
      gaspot:
        condition: service_healthy
      mariadb:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 15s
    restart: unless-stopped

networks:
  labnet:
    driver: bridge
    name: gaspot-lab-network

volumes:
  historian_data:
    name: gaspot-historian-data
```

### Container Details

**gaspot-historian (MariaDB)**:
- Image: mariadb:10.11
- Purpose: Store historical tank readings and alarms
- Credentials: root/admin, lab/password
- Database: historian
- Health Check: mysqladmin ping

**gaspot-simulator (GasPot)**:
- Base Image: python:3.11-slim
- Purpose: Simulate TLS-350 ATG
- Port: 10001
- Health Check: nc -z localhost 10001
- Dependencies: None (but waits for mariadb for ordering)

**gaspot-hmi (Flask)**:
- Base Image: python:3.11-slim
- Purpose: Web dashboard
- Port: 5000
- Health Check: curl http://localhost:5000/health
- Dependencies: gaspot-simulator, gaspot-historian

---

## Startup/Shutdown Scripts

### Startup Script (start_lab.sh)

```bash
#!/bin/bash
set -e

# Detect Docker Compose version
detect_compose() {
    if docker compose version &>/dev/null; then
        COMPOSE_CMD="docker compose"
        echo "[OK] Docker Compose V2 detected"
    elif docker-compose version &>/dev/null; then
        COMPOSE_CMD="docker-compose"
        echo "[WARN] Docker Compose V1 detected (deprecated)"
    else
        echo "[ERROR] Docker Compose not found"
        echo "Install: https://docs.docker.com/compose/install/"
        exit 1
    fi
}

# Pre-flight checks
preflight_checks() {
    if ! docker info &>/dev/null; then
        echo "[ERROR] Docker daemon not running"
        echo "Try: sudo systemctl start docker"
        exit 1
    fi
    
    for port in 10001 5000 3306; do
        if ss -tuln | grep -q ":${port} "; then
            echo "[ERROR] Port ${port} already in use"
            echo "Check: sudo lsof -i :${port}"
            exit 1
        fi
    done
    
    if $COMPOSE_CMD ps -q 2>/dev/null | grep -q .; then
        echo "[WARN] Existing containers found, stopping..."
        $COMPOSE_CMD down --remove-orphans
    fi
    
    echo "[OK] Pre-flight checks passed"
}

# Start services with health verification
start_services() {
    echo "Starting containers..."
    $COMPOSE_CMD up -d
    
    echo "Waiting for MariaDB..."
    timeout 60 bash -c 'until docker inspect --format="{{.State.Health.Status}}" gaspot-historian 2>/dev/null | grep -q "healthy"; do sleep 2; done' || {
        echo "[ERROR] MariaDB failed to become healthy"
        $COMPOSE_CMD logs mariadb
        exit 1
    }
    
    echo "Waiting for GasPot..."
    timeout 30 bash -c 'until nc -z localhost 10001 2>/dev/null; do sleep 2; done' || {
        echo "[ERROR] GasPot failed to start on port 10001"
        $COMPOSE_CMD logs gaspot
        exit 1
    }
    
    echo "Waiting for HMI..."
    timeout 30 bash -c 'until curl -sf http://localhost:5000/health &>/dev/null; do sleep 2; done' || {
        echo "[ERROR] HMI failed health check"
        $COMPOSE_CMD logs hmi
        exit 1
    }
    
    echo "[OK] All services healthy"
}

# Update timestamps
update_timestamps() {
    echo "Updating historian timestamps..."
    docker exec gaspot-historian mysql -u lab -ppassword historian \
        -e "CALL update_timestamps();" 2>/dev/null || {
        echo "[WARN] Timestamp update failed (non-critical)"
    }
}

# Display status
show_status() {
    echo ""
    echo "=========================================="
    echo "  GasPot HMI Lab Started Successfully"
    echo "=========================================="
    echo ""
    echo "Access Points:"
    echo "  GasPot (TLS-350):  telnet localhost 10001"
    echo "  HMI Dashboard:     http://localhost:5000"
    echo "  MariaDB:           mysql -h localhost -P 3306 -u lab -ppassword historian"
    echo ""
    echo "Useful Commands:"
    echo "  View logs:         $COMPOSE_CMD logs -f"
    echo "  Stop lab:          ./stop_lab.sh"
    echo "  Container status:  $COMPOSE_CMD ps"
    echo ""
}

# Main
detect_compose
preflight_checks
start_services
update_timestamps
show_status
```

### Shutdown Script (stop_lab.sh)

```bash
#!/bin/bash

detect_compose() {
    if docker compose version &>/dev/null; then
        COMPOSE_CMD="docker compose"
    elif docker-compose version &>/dev/null; then
        COMPOSE_CMD="docker-compose"
    else
        echo "[ERROR] Docker Compose not found"
        exit 1
    fi
}

stop_lab() {
    echo "Stopping GasPot HMI Lab..."
    $COMPOSE_CMD stop
    $COMPOSE_CMD down --remove-orphans
    
    if $COMPOSE_CMD ps -q 2>/dev/null | grep -q .; then
        echo "[WARN] Some containers still running"
        $COMPOSE_CMD ps
    else
        echo "[OK] All containers stopped"
    fi
}

detect_compose
stop_lab
```

### Reset Script (reset_lab.sh)

```bash
#!/bin/bash

detect_compose() {
    if docker compose version &>/dev/null; then
        COMPOSE_CMD="docker compose"
    elif docker-compose version &>/dev/null; then
        COMPOSE_CMD="docker-compose"
    else
        echo "[ERROR] Docker Compose not found"
        exit 1
    fi
}

reset_lab() {
    echo "Resetting GasPot HMI Lab..."
    echo "This will remove all containers AND data volumes."
    read -p "Are you sure? (y/N): " response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        $COMPOSE_CMD down -v --remove-orphans
        echo "[OK] Lab reset complete"
    else
        echo "Reset cancelled"
    fi
}

detect_compose
reset_lab
```

---

## Troubleshooting

### Quick Diagnostics

| Symptom | Command | What to Look For |
|---------|---------|------------------|
| Container not starting | `docker compose logs <service>` | Error messages at startup |
| Unhealthy status | `docker inspect --format='{{json .State.Health}}' <container> \| jq` | FailingStreak, last log output |
| Network issues | `docker network inspect gaspot-lab-network` | Container attachments, IP addresses |
| Port conflicts | `ss -tuln \| grep <port>` | Existing listeners |
| Permission errors | `docker compose logs <service> 2>&1 \| grep -i permission` | File/socket access issues |

### Common Issues and Solutions

**Issue: "docker-compose: command not found"**
```bash
# Check if V2 is installed
docker compose version

# If V2 works, use space instead of hyphen
docker compose up -d  # NOT docker-compose
```

**Issue: Container marked unhealthy but service works**
```bash
# Check if healthcheck tool exists in container
docker exec <container> which curl
docker exec <container> which nc

# View healthcheck history
docker inspect --format='{{json .State.Health.Log}}' <container> | jq
```

**Issue: Containers cannot communicate**
```bash
# Verify same network
docker network inspect gaspot-lab-network

# Test DNS resolution from container
docker exec gaspot-hmi ping gaspot-simulator

# Test connectivity
docker exec gaspot-hmi nc -zv gaspot-simulator 10001
```

**Issue: MariaDB slow to start**
```bash
# Increase start_period in healthcheck
# Check initialization progress
docker compose logs -f mariadb
```

**Issue: Port already in use**
```bash
# Find process using port
sudo lsof -i :10001
sudo ss -tulnp | grep 10001

# Kill or stop conflicting process
```

**Issue: GasPot not responding to commands**
```bash
# Verify Ctrl+A prefix is being sent
# Test with raw bytes
echo -e '\x01I20100\n' | nc localhost 10001

# Check GasPot logs for command parsing
docker compose logs gaspot | grep -i command
```

### Viewing Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f gaspot

# Last N lines
docker compose logs --tail=100 hmi

# Since timestamp
docker compose logs --since="2026-01-06T12:00:00" gaspot
```

### Container Shell Access

```bash
# Interactive shell
docker exec -it gaspot-simulator /bin/bash
docker exec -it gaspot-hmi /bin/sh
docker exec -it gaspot-historian mysql -u lab -ppassword historian
```

### Reset Lab State

```bash
# Stop and remove containers (preserve data)
docker compose down

# Stop, remove containers AND volumes (fresh start)
docker compose down -v

# Remove specific volume
docker volume rm gaspot-historian-data

# Full cleanup (removes images too)
docker compose down -v --rmi all
```

---

## HMI Dashboard Design

### Main View - Tank Overview

```
+------------------------------------------------------------------+
|  RIVERSIDE NATURAL GAS TERMINAL - TANK MONITORING SYSTEM         |
|  Last Update: 2026-01-06 14:34:22                    [REFRESH]   |
+------------------------------------------------------------------+
|                                                                  |
|  NATURAL GAS STORAGE                                             |
|  +----------------+ +----------------+ +----------------+        |
|  | NG-MAIN    [1] | | NG-RESERVE [2] | | NG-FEED    [3] |        |
|  |  ########....  | |  ##########..  | |  ########....  |        |
|  |  38,420 MCF    | |  44,850 MCF    | |   8,240 MCF    |        |
|  |  485.2 PSI     | |  520.8 PSI     | |  445.0 PSI     |        |
|  |  58.2 F        | |  56.8 F        | |  59.4 F        |        |
|  |  [NORMAL]      | |  [NORMAL]      | |  [NORMAL]      |        |
|  +----------------+ +----------------+ +----------------+        |
|                                                                  |
|  FUEL STORAGE                          WATER STORAGE             |
|  +----------------+ +----------------+ +----------------+        |
|  | DIESEL-PRI [4] | | DIESEL-RES [5] | | WATER-UTIL [6] |        |
|  |  ######......  | |  ##########..  | |  #######.....  |        |
|  |   6,842 GAL    | |   9,850 GAL    | |  18,500 GAL    |        |
|  |  68.5 F        | |  65.2 F        | |  52.4 F        |        |
|  |  [NORMAL]      | |  [NORMAL]      | |  [LOW LEVEL]   |        |
|  +----------------+ +----------------+ +----------------+        |
|                                                                  |
+------------------------------------------------------------------+
|  [INVENTORY] [PRESSURE] [TRENDS] [ALARMS] [HISTORY]              |
+------------------------------------------------------------------+
```

### Navigation

| View | Purpose |
|------|---------|
| INVENTORY | Full tank data table |
| PRESSURE | Pressure readings for gas tanks |
| TRENDS | Historical charts |
| ALARMS | Current and historical alarms |
| HISTORY | Raw database queries |

---

## Security Considerations (Lab Context)

This is a training lab with intentionally weak security:

| Component | Credential | Purpose |
|-----------|------------|---------|
| MariaDB root | admin | Database administration |
| MariaDB lab user | password | Student access |
| GasPot | None | No authentication (realistic ATG) |
| HMI | None | No authentication |

**Do NOT use these configurations in production environments.**
