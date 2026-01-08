# GasPot HMI Lab

A multi-container ICS/OT cybersecurity training environment simulating a Natural Gas Distribution Terminal. Students interact with a simulated Automatic Tank Gauge (ATG) via TLS-350 protocol, observe data on an HMI dashboard, and explore historian database vulnerabilities.

---

## Overview

This lab provides hands-on experience with:

- **ICS Protocol Interaction**: TLS-350 (Veeder-Root ATG) protocol used in fuel management systems
- **HMI Dashboard**: Web-based Human Machine Interface displaying real-time tank data
- **Historian Database**: Time-series database storing operational data
- **Attack Scenarios**: Discovery, enumeration, and manipulation of industrial systems

### Architecture

```
+------------------+     +------------------+     +------------------+
|   GasPot ATG     |     |    HMI Server    |     |    Historian     |
|  (TLS-350 Sim)   |<--->|  (Flask Web UI)  |<--->|   (MariaDB)      |
|  Port: 10001     |     |  Port: 5000      |     |  Port: 3306      |
+------------------+     +------------------+     +------------------+
```

| Component | Description | Port |
|-----------|-------------|------|
| gaspot-simulator | TLS-350 ATG simulator with 6 tanks | 10001 |
| gaspot-hmi | Flask web dashboard | 5000 |
| gaspot-historian | MariaDB time-series database | 3306 |

---

## Requirements

- Docker Engine 20.10+
- Docker Compose V2 (recommended) or V1
- 2GB RAM minimum
- Linux, macOS, or Windows with WSL2

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/cutaway-security/gaspot-hmi-lab.git
cd gaspot-hmi-lab
```

### 2. Start the Lab

```bash
./scripts/start_lab.sh
```

This will:
- Check for port conflicts
- Build container images
- Start all services
- Wait for health checks
- Display access information

### 3. Access the Lab

| Service | URL/Command |
|---------|-------------|
| HMI Dashboard | http://localhost:5000 |
| ATG (TLS-350) | `nc localhost 10001` |
| Database | `docker exec -it gaspot-historian mysql -u lab -ppassword historian` |

### 4. Stop the Lab

```bash
./scripts/stop_lab.sh
```

### 5. Reset the Lab

```bash
./scripts/reset_lab.sh
```

---

## Getting Started with Exercises

Once the lab is running, start the security assessment exercises:

**[exercises/README.md](exercises/README.md)** - Begin here

The exercises guide you through:
1. Network discovery and service identification
2. TLS-350 protocol enumeration
3. ATG data manipulation
4. HMI reconnaissance
5. Database exploitation
6. Combined attack scenarios
7. Defense analysis

Estimated time: ~2.5 hours for core exercises

---

## Documentation

| Document | Description |
|----------|-------------|
| [exercises/](exercises/) | Student exercises and challenges |
| [exercises/docs/PROTOCOL_REFERENCE.md](exercises/docs/PROTOCOL_REFERENCE.md) | TLS-350 ATG protocol and client tool |
| [exercises/docs/DATABASE_REFERENCE.md](exercises/docs/DATABASE_REFERENCE.md) | Database schema and queries |
| [exercises/INSTRUCTOR_GUIDE.md](exercises/INSTRUCTOR_GUIDE.md) | Teaching guide |
| [docs/OPERATIONS.md](docs/OPERATIONS.md) | Lab management and troubleshooting |
| [docs/GASPOT_MODIFICATIONS.md](docs/GASPOT_MODIFICATIONS.md) | Changes from original GasPot |

---

## Quick Reference

### ATG Client Tool

```bash
python3 tools/atg_client.py inventory      # Get tank data
python3 tools/atg_client.py pressure       # Get pressure readings
python3 tools/atg_client.py set-name 1 "X" # Change tank name
python3 tools/atg_client.py --help         # Full usage
```

### Manual ATG Commands

```bash
echo -e '\x01I20100\n' | nc localhost 10001   # Inventory
echo -e '\x01I20600\n' | nc localhost 10001   # Pressure
```

### Database Access

```bash
docker exec -it gaspot-historian mysql -u lab -ppassword historian
```

---

## Security Notes

This lab is intentionally vulnerable for training purposes:

- No authentication on ATG protocol
- Weak database credentials (lab/password)
- No encryption (HTTP, plain TCP)
- Direct database access enabled

**DO NOT deploy this in production environments.**

---

## Troubleshooting

See [docs/OPERATIONS.md](docs/OPERATIONS.md) for detailed troubleshooting.

Quick checks:
```bash
docker compose ps                    # Container status
docker compose logs -f               # View logs
ss -tuln | grep -E '10001|5000|3306' # Check ports
```

---

## Credits

- Original GasPot: https://github.com/sjhilt/GasPot (Kyle Wilhoit, Stephen Hilt)
- TLS-350 Protocol: Veeder-Root
- Lab Development: Cutaway Security

## License

This project is released under CC0 (Public Domain). Use freely for education and research.

## References

- Veeder-Root TLS-350 Documentation
- NIST SP 800-82: Guide to ICS Security
- ICS-CERT Advisories
- Rapid7 ATG Research: https://www.rapid7.com/blog/post/2015/01/22/the-internet-of-gas-station-tank-gauges/
