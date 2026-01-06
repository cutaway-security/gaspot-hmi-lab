# CLAUDE.md - Project Rules and Guidelines

## Project Overview

GasPot HMI Lab is a multi-container ICS/OT cybersecurity training environment simulating a Natural Gas Distribution Terminal. Students interact with a simulated Automatic Tank Gauge (ATG) via TLS-350 protocol, observe data on an HMI dashboard, and explore historian database vulnerabilities.

**Repository**: https://github.com/cutaway-security/gaspot-hmi-lab
**Development Branch**: claude-dev

### Container Architecture

| Container | Purpose | Port | Technology |
|-----------|---------|------|------------|
| gaspot-simulator | TLS-350 ATG Simulator | 10001 | Python |
| gaspot-hmi | Web-based HMI Dashboard | 5000 | Flask |
| gaspot-historian | Time-series Database | 3306 | MariaDB |

---

## Essential Documents (Read in Order)

Before starting any development session, read these documents in order:

1. **ARCHITECTURE.md** - System design, container configuration, data flow, troubleshooting
2. **PLAN.md** - Project roadmap, current phase, milestones, completion status
3. **RESUME.md** - Development status, what is in progress, blockers, session context
4. **VIBE_HISTORY.md** - Lessons learned, session activity, problems encountered

**At session start**: Confirm you have read these documents before proceeding. List your understanding of the current state and next steps.

---

## CRITICAL: Development Process Rules

### Issue Resolution Requirements

**STOP AND VERIFY - DO NOT PROCEED WITHOUT RESOLUTION**

Container and service issues MUST be fully resolved before declaring success or moving to the next task. Past development sessions have failed due to moving forward without fixing critical issues.

When encountering issues:

1. **STOP** - Do not continue to next task
2. **DIAGNOSE** - Use troubleshooting commands to identify root cause
3. **FIX** - Implement a solution
4. **VERIFY** - Confirm the fix works with actual testing
5. **DOCUMENT** - Record the issue and solution in VIBE_HISTORY.md
6. **ASK** - If unable to resolve after reasonable attempts, STOP and ask for clarifying directions

**Never assume a container or service is working without verification.**

### Verification Requirements

| Component | Verification Method |
|-----------|-------------------|
| Container running | `docker compose ps` shows "Up" status |
| Container healthy | `docker inspect --format='{{.State.Health.Status}}' <container>` returns "healthy" |
| GasPot responding | `echo -e '\x01I20100\n' \| nc localhost 10001` returns inventory |
| HMI responding | `curl -f http://localhost:5000/health` returns 200 |
| MariaDB responding | `docker exec gaspot-historian mysqladmin ping -u lab -ppassword` returns "alive" |
| Network connectivity | `docker exec <container> ping <other-container>` succeeds |

### Phase Completion Process

Before moving to the next phase:

1. **Verify** - All components of current phase working
2. **Test** - Run integration tests if applicable
3. **Document** - Update VIBE_HISTORY.md with session activity
4. **Summarize** - Provide summary of completed work
5. **Plan** - List steps for next phase
6. **Confirm** - Wait for user confirmation before proceeding

---

## Absolute Requirements

- NO emoji, icons, or Unicode symbols in source code, output, or documentation
- NO stubs, placeholders, or fake data - implement real functionality or mark clearly as TODO with explanation
- NO claiming code works without testing - be honest about untested code
- NO moving forward when containers or services have unresolved issues
- All network operations require error handling with specific exception types, timeouts, and retry logic
- NO spaces in file or folder names
- All output files must contain a timestamp in the filename (format: YYYYMMDD_HHMMSS)
- Use weak passwords appropriate for student lab: password, admin, Password0!

---

## Technical Constraints

### GasPot Simulator

| Constraint | Value |
|------------|-------|
| Python Version | 3.11+ |
| Protocol | TLS-350 (Veeder Root ATG) |
| Port | 10001 |
| Operations | Read (I20xxx) and Write (S602xx) commands |
| Tanks | 6 (3 Natural Gas, 2 Diesel, 1 Water) |

### HMI Application

| Constraint | Value |
|------------|-------|
| Python Version | 3.11+ |
| Framework | Flask |
| Port | 5000 |
| Frontend | HTML/CSS/JavaScript with Chart.js |
| Database | SQLAlchemy with MariaDB |

### Historian Database

| Constraint | Value |
|------------|-------|
| Database | MariaDB 10.11 |
| Port | 3306 |
| Credentials | User: lab / Password: password |
| Root Password | admin |
| Database Name | historian |

### Docker Configuration

| Constraint | Value |
|------------|-------|
| Compose Version | Support both V1 and V2 syntax |
| Network | User-defined bridge (gaspot-lab-network) |
| Health Checks | Required for all containers |
| Restart Policy | unless-stopped |

---

## Code Quality Standards

### All Scripts

- Every network operation must handle timeouts and have fallback behavior
- Log errors properly - never swallow exceptions silently
- Validate inputs at system boundaries (IP address, port, address ranges)
- Include type hints on all function signatures (Python)
- Prefer strong verbs over adjective-heavy descriptions in comments
- All protocol interactions must respect safety constraints
- Check for required libraries at startup with clear error message if missing

### Container Development

- All containers must have health checks
- Use named volumes for persistent data
- Use environment variables for configuration
- Containers must communicate via service names, not IP addresses
- Include curl or nc in images for health checks
- Log to stdout/stderr for docker logs compatibility

### TLS-350 Protocol Implementation

- All commands must be prefixed with 0x01 (Ctrl+A)
- All commands must be terminated with newline (0x0A)
- Handle partial reads and socket timeouts
- Validate command format before sending
- Parse responses correctly handling multi-line output

---

## Communication Style

- Focus on substance, skip unnecessary praise
- Be direct about problems - identify specific issues with line numbers
- Question assumptions and challenge problematic approaches
- Ground claims in evidence, not reflexive validation
- When stuck, explain what was tried and ask specific questions

---

## Documentation Updates Required

When making changes, update the appropriate documents:

| Change Type | Update |
|-------------|--------|
| Architecture change | dev/ARCHITECTURE.md |
| Phase completion | dev/PLAN.md |
| Session activity | dev/RESUME.md, dev/VIBE_HISTORY.md |
| Problem encountered | dev/VIBE_HISTORY.md |
| Lesson learned | dev/VIBE_HISTORY.md |
| New dependency | requirements.txt (in appropriate directory) |
| Usage change | README.md |

---

## Project Scope

### In Scope

**GasPot Simulator**:
- TLS-350 protocol simulation (I20100-I20600, S602xx)
- 6 tanks with realistic data (3 Natural Gas, 2 Diesel, 1 Water)
- Value fluctuation over time
- Pressure data for gas tanks
- Configuration via config.ini

**HMI Application**:
- Web dashboard showing all tank data
- Real-time updates via polling GasPot
- Historical trend charts from historian
- Alarm status display

**Historian Database**:
- Tank readings time-series storage
- Alarm history
- Stored procedures for timestamp updates
- Direct student SQL access

**Student Tools**:
- Python ATG client script
- Lab exercise documentation

**Infrastructure**:
- Docker Compose orchestration
- Bullet-proof startup/shutdown scripts
- Health checks for all containers

### Out of Scope

- Multi-site/multi-PLC scenarios
- Network discovery/subnet scanning
- Real ICS protocol implementations (Modbus, EtherNet/IP)
- Authentication/authorization on GasPot
- HTTPS for HMI
- Production hardening

---

## Testing

### Development Environment
- Ubuntu Linux (current LTS)

### Target Deployment Environment
- Kali Linux

### Test Procedure for Each Component

**GasPot**:
```bash
# Basic connectivity
nc -zv localhost 10001

# Send I20100 command
echo -e '\x01I20100\n' | nc localhost 10001

# Verify response contains tank data
```

**HMI**:
```bash
# Health endpoint
curl -f http://localhost:5000/health

# Main page loads
curl -s http://localhost:5000/ | grep -q "Natural Gas"
```

**Historian**:
```bash
# Connection test
docker exec gaspot-historian mysqladmin ping -u lab -ppassword

# Query test
docker exec gaspot-historian mysql -u lab -ppassword historian -e "SELECT COUNT(*) FROM tanks;"
```

---

## File Structure

```
gaspot-hmi-lab/
    CLAUDE.md                 # This file - rules and guidelines
    README.md                 # User documentation
    LICENSE
    docker-compose.yml        # Container orchestration
    .env.example              # Environment template
    dev/
        ARCHITECTURE.md       # System design + container management
        PLAN.md               # Roadmap and phases
        RESUME.md             # Session status and context
        VIBE_HISTORY.md       # Lessons learned and activity log
    gaspot/
        Dockerfile
        GasPot.py             # Modified ATG simulator
        config.ini            # Tank and station configuration
        requirements.txt
    hmi/
        Dockerfile
        app/
            __init__.py
            routes.py
            models.py
            atg_client.py     # TLS-350 protocol library
            templates/
            static/
        requirements.txt
    historian/
        init.sql              # Schema + seed data + stored procedures
    tools/
        atg_client.py         # Student CLI tool
    scripts/
        start_lab.sh          # Startup script
        stop_lab.sh           # Shutdown script
        reset_lab.sh          # Full reset script
```

---

## Session Workflow

### Starting a Session

1. Read CLAUDE.md (this file)
2. Read dev/ARCHITECTURE.md
3. Read dev/PLAN.md
4. Read dev/RESUME.md
5. Read dev/VIBE_HISTORY.md
6. State your understanding of current status
7. List proposed next steps
8. Wait for confirmation before proceeding

### During Development

1. Work on one task at a time
2. Test each change before moving on
3. Document issues in VIBE_HISTORY.md
4. Stop and ask if encountering persistent issues

### Ending a Session

1. Document what was accomplished in VIBE_HISTORY.md
2. Update RESUME.md with current state
3. Update PLAN.md with completion status
4. List any blockers or open questions
5. Provide summary of session
