# GasPot HMI Lab - Operations Guide

This guide is for lab operators and maintainers who need to deploy, manage, and troubleshoot the GasPot HMI Lab environment.

For student exercises, see `exercises/README.md`.

---

## Table of Contents

1. [Requirements](#requirements)
2. [Container Architecture](#container-architecture)
3. [Starting the Lab](#starting-the-lab)
4. [Stopping the Lab](#stopping-the-lab)
5. [Resetting the Lab](#resetting-the-lab)
6. [Health Checks](#health-checks)
7. [Environment Variables](#environment-variables)
8. [Log Management](#log-management)
9. [Troubleshooting](#troubleshooting)
10. [File Structure](#file-structure)

---

## Requirements

### System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| RAM | 2 GB | 4 GB |
| Disk Space | 2 GB | 5 GB |
| Docker Engine | 20.10+ | Latest |
| Docker Compose | V1 or V2 | V2 |

### Supported Platforms

- Linux (Ubuntu, Kali, Debian, RHEL/CentOS)
- macOS (with Docker Desktop)
- Windows (with WSL2 and Docker Desktop)

### Required Ports

| Port | Service | Protocol |
|------|---------|----------|
| 5000 | HMI Web Dashboard | HTTP |
| 10001 | GasPot ATG Simulator | TCP (TLS-350) |
| 3306 | MariaDB Historian | MySQL |

---

## Container Architecture

### Container Overview

| Container Name | Service | Image | Purpose |
|----------------|---------|-------|---------|
| gaspot-historian | mariadb | mariadb:10.11 | Time-series database for tank readings and alarms |
| gaspot-simulator | gaspot | python:3.11-slim (custom) | TLS-350 ATG protocol simulator |
| gaspot-hmi | hmi | python:3.11-slim (custom) | Flask web dashboard |

### Network Configuration

All containers communicate via a user-defined bridge network:

- **Network Name**: gaspot-lab-network
- **Driver**: bridge
- **DNS**: Containers resolve each other by service name

### Data Persistence

| Volume | Container | Path | Purpose |
|--------|-----------|------|---------|
| gaspot-historian-data | gaspot-historian | /var/lib/mysql | Database files |

GasPot simulator state is held in memory and resets on container restart.

---

## Starting the Lab

### Using the Startup Script (Recommended)

```bash
./scripts/start_lab.sh
```

The script performs:
1. Docker Compose version detection (V1 or V2)
2. Docker daemon availability check
3. Port conflict detection
4. Cleanup of existing containers
5. Container build and start
6. Health check verification
7. Database timestamp update
8. Access information display

### Manual Start

```bash
# Docker Compose V2
docker compose up -d

# Docker Compose V1 (deprecated)
docker-compose up -d
```

### Verifying Startup

```bash
# Check container status
docker compose ps

# Expected output: all containers "Up" and "healthy"
```

### First-Time Initialization

On first start with an empty database volume:
1. MariaDB runs `/docker-entrypoint-initdb.d/init.sql`
2. Tables are created (tanks, tank_readings, alarms)
3. Seed data is generated (24 hours of readings, sample alarms)
4. Timestamps are updated to current time

---

## Stopping the Lab

### Using the Stop Script (Recommended)

```bash
./scripts/stop_lab.sh
```

This stops containers but preserves data volumes.

### Manual Stop

```bash
# Stop and remove containers (preserve data)
docker compose down

# Stop only (containers remain)
docker compose stop
```

---

## Resetting the Lab

### Using the Reset Script

```bash
./scripts/reset_lab.sh
```

This will:
1. Prompt for confirmation
2. Stop all containers
3. Remove all containers
4. Delete data volumes (database will reinitialize on next start)

### Manual Reset

```bash
# Remove containers and volumes
docker compose down -v

# Full cleanup (including images)
docker compose down -v --rmi all

# Remove specific volume
docker volume rm gaspot-historian-data
```

### Reset Options

| Command | Containers | Volumes | Images |
|---------|------------|---------|--------|
| `docker compose stop` | Stopped | Kept | Kept |
| `docker compose down` | Removed | Kept | Kept |
| `docker compose down -v` | Removed | Removed | Kept |
| `docker compose down -v --rmi all` | Removed | Removed | Removed |

---

## Health Checks

### Container Health Status

```bash
# View health status
docker compose ps

# Detailed health info for specific container
docker inspect --format='{{json .State.Health}}' gaspot-historian | jq
docker inspect --format='{{json .State.Health}}' gaspot-simulator | jq
docker inspect --format='{{json .State.Health}}' gaspot-hmi | jq
```

### Health Check Configuration

| Container | Test Command | Interval | Timeout | Retries | Start Period |
|-----------|--------------|----------|---------|---------|--------------|
| gaspot-historian | `mysqladmin ping` | 10s | 5s | 10 | 30s |
| gaspot-simulator | `nc -z localhost 10001` | 10s | 5s | 5 | 10s |
| gaspot-hmi | `curl -f http://localhost:5000/health` | 10s | 5s | 5 | 15s |

### Manual Health Verification

```bash
# Test MariaDB
docker exec gaspot-historian mysqladmin ping -u lab -ppassword

# Test GasPot
nc -zv localhost 10001

# Test HMI
curl -f http://localhost:5000/health
```

---

## Environment Variables

### HMI Container Environment

| Variable | Default | Description |
|----------|---------|-------------|
| GASPOT_HOST | gaspot-simulator | GasPot container hostname |
| GASPOT_PORT | 10001 | GasPot TLS-350 port |
| DB_HOST | gaspot-historian | Database hostname |
| DB_PORT | 3306 | Database port |
| DB_USER | lab | Database username |
| DB_PASSWORD | password | Database password |
| DB_NAME | historian | Database name |

### MariaDB Container Environment

| Variable | Default | Description |
|----------|---------|-------------|
| MYSQL_ROOT_PASSWORD | admin | Root password |
| MYSQL_DATABASE | historian | Database name |
| MYSQL_USER | lab | Application user |
| MYSQL_PASSWORD | password | Application password |

### Customization

To customize, create a `.env` file in the project root:

```bash
cp .env.example .env
# Edit .env with your values
```

---

## Log Management

### Viewing Logs

```bash
# All containers
docker compose logs -f

# Specific container
docker compose logs -f gaspot
docker compose logs -f hmi
docker compose logs -f mariadb

# Last N lines
docker compose logs --tail=100 hmi

# Since timestamp
docker compose logs --since="2026-01-08T12:00:00" gaspot
```

### Log Locations Inside Containers

| Container | Log Location |
|-----------|--------------|
| gaspot-historian | stdout/stderr (MariaDB default) |
| gaspot-simulator | stdout/stderr (Python logging) |
| gaspot-hmi | stdout/stderr (Flask/Gunicorn) |

### Exporting Logs

```bash
# Export to file
docker compose logs > lab_logs.txt

# Export specific container
docker logs gaspot-hmi > hmi_logs.txt 2>&1
```

---

## Troubleshooting

### Quick Diagnostics

| Symptom | Command | What to Look For |
|---------|---------|------------------|
| Container not starting | `docker compose logs <service>` | Error messages at startup |
| Unhealthy status | `docker inspect --format='{{json .State.Health}}' <container>` | FailingStreak, Log entries |
| Network issues | `docker network inspect gaspot-lab-network` | Container attachments |
| Port conflicts | `ss -tuln \| grep -E '5000\|10001\|3306'` | Existing listeners |

### Common Issues

#### Port Already in Use

```bash
# Find process using port
ss -tulnp | grep 10001
sudo lsof -i :10001

# Kill process or change port in docker-compose.yml
```

#### MariaDB Slow to Start

MariaDB may take 30-60 seconds on first initialization. The startup script waits automatically. For manual starts:

```bash
# Watch initialization progress
docker compose logs -f mariadb

# Wait for healthy status
timeout 60 bash -c 'until docker inspect --format="{{.State.Health.Status}}" gaspot-historian | grep -q "healthy"; do sleep 2; done'
```

#### Database Tables Missing

If the database volume existed but tables are missing:

```bash
# Option 1: Full reset
./scripts/reset_lab.sh
./scripts/start_lab.sh

# Option 2: Manual reinitialize
docker compose down -v
docker compose up -d
```

#### GasPot Not Responding

```bash
# Check if container is running
docker compose ps gaspot

# Check logs for errors
docker compose logs gaspot

# Test connectivity
nc -zv localhost 10001

# Test command (should return inventory)
echo -e '\x01I20100\n' | nc localhost 10001
```

#### HMI Dashboard Not Loading

```bash
# Check container status
docker compose ps hmi

# Check logs
docker compose logs hmi

# Test health endpoint
curl -v http://localhost:5000/health

# Check if HMI can reach GasPot
docker exec gaspot-hmi nc -zv gaspot-simulator 10001
```

#### Containers Cannot Communicate

```bash
# Verify network exists
docker network ls | grep gaspot

# Verify containers on same network
docker network inspect gaspot-lab-network

# Test DNS resolution
docker exec gaspot-hmi ping -c 1 gaspot-simulator
docker exec gaspot-hmi ping -c 1 gaspot-historian
```

### Container Shell Access

```bash
# GasPot (bash available)
docker exec -it gaspot-simulator /bin/bash

# HMI (sh only in slim image)
docker exec -it gaspot-hmi /bin/sh

# MariaDB (mysql client)
docker exec -it gaspot-historian mysql -u lab -ppassword historian
```

---

## File Structure

```
gaspot-hmi-lab/
    docker-compose.yml        # Container orchestration
    .env.example              # Environment template

    scripts/
        start_lab.sh          # Start lab with health checks
        stop_lab.sh           # Stop lab (preserve data)
        reset_lab.sh          # Full reset (delete data)

    gaspot/
        Dockerfile            # GasPot container build
        GasPot.py             # TLS-350 simulator implementation
        config.ini            # Tank and station configuration
        requirements.txt      # Python dependencies (none)

    hmi/
        Dockerfile            # HMI container build
        run.py                # Flask entry point
        requirements.txt      # Python dependencies
        app/
            __init__.py       # Flask app factory
            routes.py         # Web routes and API endpoints
            models.py         # SQLAlchemy models
            atg_client.py     # TLS-350 protocol library
            poller.py         # Background polling module
            templates/        # Jinja2 HTML templates
            static/           # CSS and JavaScript

    historian/
        init.sql              # Database schema, procedures, seed data

    tools/
        atg_client.py         # Student CLI tool

    docs/
        OPERATIONS.md         # This file
        GASPOT_MODIFICATIONS.md  # Changes from original GasPot

    exercises/
        README.md             # Student exercises introduction
        E01-E07_*.md          # Individual exercises
        challenges/           # Advanced challenges
        docs/                 # Reference materials
        INSTRUCTOR_GUIDE.md   # Teaching guide
```

---

## Maintenance Tasks

### Updating Container Images

```bash
# Rebuild all images
docker compose build --no-cache

# Rebuild specific image
docker compose build --no-cache hmi
```

### Updating Seed Data

1. Edit `historian/init.sql`
2. Reset the lab: `./scripts/reset_lab.sh`
3. Start the lab: `./scripts/start_lab.sh`

### Backing Up Database

```bash
# Export database
docker exec gaspot-historian mysqldump -u lab -ppassword historian > backup.sql

# Restore database
cat backup.sql | docker exec -i gaspot-historian mysql -u lab -ppassword historian
```

---

## Security Notes

This lab uses intentionally weak credentials for educational purposes:

| Component | Username | Password |
|-----------|----------|----------|
| MariaDB root | root | admin |
| MariaDB application | lab | password |
| GasPot | N/A | No authentication |
| HMI | N/A | No authentication |

**Do NOT deploy this configuration in production environments.**

For production deployments, you would need:
- Strong, unique passwords
- TLS encryption for all services
- Authentication on HMI and GasPot
- Network segmentation
- Firewall rules
