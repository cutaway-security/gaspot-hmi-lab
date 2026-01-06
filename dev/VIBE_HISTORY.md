# VIBE_HISTORY.md - Lessons Learned and Session Activity Log

## Purpose

This document maintains a history of development sessions, lessons learned, problems encountered, and solutions applied. It serves as institutional memory for the project and helps avoid repeating mistakes.

---

## Session Log

### Session Template

Copy this template for each new session:

```markdown
## Session: YYYY-MM-DD

### Session Info
- **Date**: 
- **Duration**: 
- **Phase**: 
- **Focus**: 

### Objectives
- [ ] Objective 1
- [ ] Objective 2

### Completed
- Item 1
- Item 2

### Problems Encountered
| Problem | Cause | Solution |
|---------|-------|----------|
| Description | Root cause | How it was fixed |

### Lessons Learned
- Lesson 1
- Lesson 2

### Deferred/Blocked
- Item (reason)

### Next Steps
1. Step 1
2. Step 2

### Notes
Additional context or observations.
```

---

## Sessions

### Session: 2026-01-06 (Session 1)

#### Session Info
- **Date**: 2026-01-06
- **Duration**: ~30 minutes
- **Phase**: 1 - Foundation
- **Focus**: Project setup and initial structure

#### Objectives
- [x] Read and understand project documentation
- [x] Review original GasPot project
- [x] Create directory structure
- [x] Create docker-compose.yml
- [x] Create .env.example
- [x] Validate Docker Compose configuration
- [ ] Test network connectivity between containers

#### Completed
- Read all documentation (CLAUDE.md, ARCHITECTURE.md, PLAN.md, RESUME.md, VIBE_HISTORY.md)
- Reviewed original GasPot at https://github.com/sjhilt/GasPot
- Analyzed GasPot.py, Dockerfile, and config.ini.dist
- Decided to use Option A: fork and modify original GasPot
- Created directory structure (gaspot/, hmi/, historian/, tools/, scripts/)
- Created docker-compose.yml with all 3 services
- Created .env.example with environment variables
- Created placeholder Dockerfiles for gaspot and hmi
- Created historian/init.sql with schema and tank configuration
- Validated configuration with `docker-compose config`

#### Problems Encountered
| Problem | Cause | Solution |
|---------|-------|----------|
| Docker Compose V2 not available | Older Docker installation | User upgrading Docker |

#### Lessons Learned
- Development system has Docker Compose V1 only (`docker-compose` not `docker compose`)
- Original GasPot has CC0 license (public domain) - free to modify
- Original GasPot implements I20100-I20500 and S6020x, but not I20600 (pressure)

#### Deferred/Blocked
- Task 1.5: Test network connectivity (blocked on Docker upgrade)

#### Next Steps
1. User upgrades Docker to get Compose V2
2. Resume Phase 1, Task 1.5
3. Build and start containers
4. Test network connectivity
5. Complete Phase 1 acceptance criteria
6. Begin Phase 2: GasPot Simulator

#### Notes
- Original GasPot uses select() for non-blocking socket I/O - good pattern to keep
- Original has 4 tanks, need to expand to 6 (3 NG, 2 Diesel, 1 Water)
- Need to add I20600 (pressure) and S60210/S60220 (set volume/pressure) commands
- Need to implement fluctuation engine for dynamic values

---

---

## Lessons Learned Summary

This section aggregates important lessons across all sessions for quick reference.

### Container Development

*No lessons recorded yet.*

### TLS-350 Protocol

*No lessons recorded yet.*

### Docker Compose

- Check for both V1 (`docker-compose`) and V2 (`docker compose`) availability
- Use version detection in scripts to support both syntaxes
- `docker-compose config` validates YAML even without building images

### Flask/HMI

*No lessons recorded yet.*

### MariaDB/Historian

*No lessons recorded yet.*

### Testing

*No lessons recorded yet.*

### Scripts

*No lessons recorded yet.*

---

## Common Problems and Solutions

This section documents recurring issues and their solutions.

### Problem: [Template]

**Symptoms**: 
- What you observe

**Cause**: 
- Root cause

**Solution**:
```bash
# Commands or code to fix
```

**Prevention**:
- How to avoid in future

---

## Technical Discoveries

Document technical findings that aren't obvious from documentation.

### TLS-350 Protocol

*No discoveries recorded yet.*

### Docker/Containers

*No discoveries recorded yet.*

### Python/Flask

*No discoveries recorded yet.*

### MariaDB

*No discoveries recorded yet.*

---

## Decision Log

Track important decisions and their rationale.

| Date | Decision | Rationale | Alternatives Considered |
|------|----------|-----------|------------------------|
| 2026-01-06 | Fork and modify original GasPot (Option A) | CC0 license, saves time, solid architecture | Write from scratch (Option B) |
| - | 6 tanks total | Realistic facility | 4 tanks (too simple) |
| - | HMI polls GasPot | Clean separation | GasPot pushes (complex) |
| - | MariaDB 10.11 | Stable, well-documented | PostgreSQL, SQLite |
| - | Flask for HMI | Simple, sufficient | FastAPI, Django |
| - | Chart.js for charts | Simple, no build step | Plotly, D3 |

---

## Code Snippets

Useful code patterns discovered during development.

### TLS-350 Command Sending

```python
# Template - update when implemented
import socket

def send_atg_command(host, port, command):
    """Send TLS-350 command and return response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)
        s.connect((host, port))
        # Prefix with SOH (0x01), suffix with newline
        s.sendall(b'\x01' + command.encode() + b'\n')
        response = b''
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk
            if b'\x03' in chunk:  # ETX marks end
                break
        return response.decode('ascii', errors='replace')
```

### Docker Compose Version Detection

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

### Container Health Check

```bash
# Wait for container to be healthy
timeout 60 bash -c 'until docker inspect --format="{{.State.Health.Status}}" container_name 2>/dev/null | grep -q "healthy"; do sleep 2; done'
```

---

## Testing Notes

Document testing observations and edge cases.

### GasPot Testing

*No notes yet.*

### HMI Testing

*No notes yet.*

### Integration Testing

*No notes yet.*

---

## Environment Notes

Document environment-specific observations.

### Ubuntu Development

*No notes yet.*

### Kali Deployment

*No notes yet.*

---

## Performance Observations

Document any performance-related findings.

*No observations yet.*

---

## Security Notes

Document security-related findings (for lab context).

- All passwords intentionally weak for student access
- No authentication on GasPot (realistic ATG behavior)
- No HTTPS on HMI (lab simplicity)
- Direct database access enabled for students

---

## Future Improvements

Ideas for future enhancements (out of current scope).

- Add authentication option for GasPot
- Add HTTPS support for HMI
- Add more TLS-350 commands
- Add Modbus protocol support
- Add multi-site simulation
- Add network segmentation lab variant

---

## References

Useful links discovered during development.

### GasPot/TLS-350
- Original GasPot: https://github.com/sjhilt/GasPot
- Veeder-Root manuals: https://www.veeder.com/us/automatic-tank-gauging-products/tls-350-automatic-tank-gauge/tls-350-and-tls-3xx-series-manuals-and-guides
- Metasploit ATG module: https://github.com/rapid7/metasploit-framework/blob/master/modules/auxiliary/admin/atg/atg_client.rb
- Nmap atg-info.nse: https://github.com/digitalbond/Redpoint/blob/master/atg-info.nse

### Docker
- Docker Compose networking: https://docs.docker.com/compose/how-tos/networking/
- Health checks: https://docs.docker.com/compose/compose-file/05-services/#healthcheck
- Compose V2 migration: https://docs.docker.com/compose/releases/migrate/

### Flask
- Flask documentation: https://flask.palletsprojects.com/
- SQLAlchemy: https://www.sqlalchemy.org/

### MariaDB
- MariaDB Docker: https://hub.docker.com/_/mariadb
- MariaDB documentation: https://mariadb.com/kb/en/

---

## Appendix: Troubleshooting Commands

Quick reference for debugging.

```bash
# Container status
docker compose ps
docker ps -a

# Container logs
docker compose logs -f
docker compose logs -f gaspot
docker logs gaspot-simulator --tail=100

# Container health
docker inspect --format='{{json .State.Health}}' gaspot-simulator | jq
docker inspect --format='{{.State.Health.Status}}' gaspot-historian

# Network inspection
docker network ls
docker network inspect gaspot-lab-network

# Enter container shell
docker exec -it gaspot-simulator /bin/bash
docker exec -it gaspot-hmi /bin/sh
docker exec -it gaspot-historian mysql -u lab -ppassword historian

# Test GasPot
echo -e '\x01I20100\n' | nc localhost 10001
echo -e '\x01I20600\n' | nc localhost 10001

# Test HMI
curl -v http://localhost:5000/health
curl -s http://localhost:5000/ | head -50

# Test MariaDB
docker exec gaspot-historian mysqladmin ping -u lab -ppassword
docker exec gaspot-historian mysql -u lab -ppassword historian -e "SHOW TABLES;"

# Port checks
ss -tuln | grep -E '10001|5000|3306'
sudo lsof -i :10001

# Full reset
docker compose down -v --remove-orphans
docker system prune -f
```
