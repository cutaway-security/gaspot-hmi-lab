# PLAN.md - Project Roadmap

## Project: GasPot HMI Lab

**Goal**: Create a multi-container ICS/OT cybersecurity training lab with GasPot ATG simulator, HMI dashboard, and historian database.

**Target**: Students on Kali Linux systems

---

## Phase Overview

| Phase | Name | Status | Description |
|-------|------|--------|-------------|
| 1 | Foundation | NOT STARTED | Repository structure, Docker Compose skeleton |
| 2 | GasPot Simulator | NOT STARTED | Modified ATG with 6 tanks, fluctuation |
| 3 | Historian Database | NOT STARTED | MariaDB schema, seed data, stored procedures |
| 4 | HMI Application | NOT STARTED | Flask web dashboard with charts |
| 5 | Integration | NOT STARTED | Connect all components, polling loop |
| 6 | Scripts | NOT STARTED | Startup, shutdown, reset scripts |
| 7 | Student Tools | NOT STARTED | ATG client script, documentation |
| 8 | Testing | NOT STARTED | End-to-end validation on Kali |

---

## Phase 1: Foundation

**Status**: NOT STARTED

**Objective**: Set up repository structure and validate Docker environment.

### Tasks

| # | Task | Status | Notes |
|---|------|--------|-------|
| 1.1 | Create directory structure | NOT STARTED | See ARCHITECTURE.md for layout |
| 1.2 | Create docker-compose.yml skeleton | NOT STARTED | All 3 services defined |
| 1.3 | Create .env.example | NOT STARTED | Environment variables template |
| 1.4 | Validate Docker Compose runs | NOT STARTED | Use placeholder images |
| 1.5 | Test network connectivity between containers | NOT STARTED | Ping between containers |

### Acceptance Criteria

- [ ] All directories created per ARCHITECTURE.md
- [ ] docker-compose.yml parses without errors
- [ ] `docker compose config` shows valid configuration
- [ ] Placeholder containers can communicate via network

### Deliverables

- docker-compose.yml
- .env.example
- Directory structure

---

## Phase 2: GasPot Simulator

**Status**: NOT STARTED

**Objective**: Create modified GasPot with 6 tanks, pressure data, and fluctuation.

### Tasks

| # | Task | Status | Notes |
|---|------|--------|-------|
| 2.1 | Create gaspot/Dockerfile | NOT STARTED | Python 3.11 base, include nc |
| 2.2 | Create gaspot/requirements.txt | NOT STARTED | Minimal dependencies |
| 2.3 | Create gaspot/config.ini | NOT STARTED | 6 tanks, station name |
| 2.4 | Implement GasPot.py base | NOT STARTED | Socket server on 10001 |
| 2.5 | Implement I20100 (inventory) | NOT STARTED | All 6 tanks |
| 2.6 | Implement I20200-I20500 | NOT STARTED | Other read commands |
| 2.7 | Implement I20600 (pressure) | NOT STARTED | Custom command |
| 2.8 | Implement S602xx (writes) | NOT STARTED | Tank name and value changes |
| 2.9 | Implement fluctuation engine | NOT STARTED | Per-tank behavior |
| 2.10 | Test with telnet | NOT STARTED | Manual command testing |
| 2.11 | Test with netcat | NOT STARTED | Scripted command testing |

### Acceptance Criteria

- [ ] Container builds successfully
- [ ] Container passes health check
- [ ] I20100 returns all 6 tanks with correct format
- [ ] I20600 returns pressure for gas tanks only
- [ ] S60201 changes tank name and persists
- [ ] S60210 changes tank volume
- [ ] Values fluctuate over time (observe over 1 minute)
- [ ] Invalid commands return 9999FF1B

### Deliverables

- gaspot/Dockerfile
- gaspot/GasPot.py
- gaspot/config.ini
- gaspot/requirements.txt

---

## Phase 3: Historian Database

**Status**: NOT STARTED

**Objective**: Create MariaDB schema with seed data and stored procedures.

### Tasks

| # | Task | Status | Notes |
|---|------|--------|-------|
| 3.1 | Create historian/init.sql | NOT STARTED | Schema from ARCHITECTURE.md |
| 3.2 | Add tanks table with 6 tank config | NOT STARTED | Reference data |
| 3.3 | Add tank_readings table | NOT STARTED | Time-series data |
| 3.4 | Add alarms table | NOT STARTED | Alarm history |
| 3.5 | Create update_timestamps procedure | NOT STARTED | Adjust historical data |
| 3.6 | Add seed data (24 hours history) | NOT STARTED | Realistic patterns |
| 3.7 | Add sample alarms | NOT STARTED | Various severities |
| 3.8 | Test container starts | NOT STARTED | Init script runs |
| 3.9 | Test queries work | NOT STARTED | SELECT from all tables |
| 3.10 | Test stored procedure | NOT STARTED | Timestamps update |

### Acceptance Criteria

- [ ] Container builds and passes health check
- [ ] All tables created correctly
- [ ] 6 tanks in tanks table
- [ ] At least 24 hours of seed data in tank_readings
- [ ] Sample alarms present
- [ ] update_timestamps() procedure works
- [ ] Lab user can connect and query

### Deliverables

- historian/init.sql

---

## Phase 4: HMI Application

**Status**: NOT STARTED

**Objective**: Create Flask web dashboard with real-time display and charts.

### Tasks

| # | Task | Status | Notes |
|---|------|--------|-------|
| 4.1 | Create hmi/Dockerfile | NOT STARTED | Python 3.11, include curl |
| 4.2 | Create hmi/requirements.txt | NOT STARTED | Flask, SQLAlchemy, etc. |
| 4.3 | Create hmi/app/__init__.py | NOT STARTED | Flask app factory |
| 4.4 | Create hmi/app/atg_client.py | NOT STARTED | TLS-350 protocol library |
| 4.5 | Test atg_client.py standalone | NOT STARTED | Connect to GasPot |
| 4.6 | Create hmi/app/models.py | NOT STARTED | SQLAlchemy models |
| 4.7 | Create hmi/app/routes.py | NOT STARTED | Flask routes |
| 4.8 | Create /health endpoint | NOT STARTED | For health check |
| 4.9 | Create main dashboard template | NOT STARTED | Tank overview |
| 4.10 | Create trends template | NOT STARTED | Chart.js charts |
| 4.11 | Create alarms template | NOT STARTED | Alarm display |
| 4.12 | Add static CSS | NOT STARTED | Basic styling |
| 4.13 | Test container builds | NOT STARTED | Image builds |
| 4.14 | Test health endpoint | NOT STARTED | Returns 200 |
| 4.15 | Test dashboard loads | NOT STARTED | Shows tank data |

### Acceptance Criteria

- [ ] Container builds and passes health check
- [ ] /health returns 200 OK
- [ ] Main dashboard shows all 6 tanks
- [ ] Tank data matches GasPot current state
- [ ] Trends page shows historical charts
- [ ] Alarms page shows alarm history
- [ ] Page auto-refreshes or has refresh button

### Deliverables

- hmi/Dockerfile
- hmi/requirements.txt
- hmi/app/__init__.py
- hmi/app/atg_client.py
- hmi/app/models.py
- hmi/app/routes.py
- hmi/app/templates/*.html
- hmi/app/static/*.css

---

## Phase 5: Integration

**Status**: NOT STARTED

**Objective**: Connect all components with polling loop and data flow.

### Tasks

| # | Task | Status | Notes |
|---|------|--------|-------|
| 5.1 | Implement HMI polling loop | NOT STARTED | Poll GasPot every 5-10 sec |
| 5.2 | Store readings to historian | NOT STARTED | On each poll |
| 5.3 | Test full data flow | NOT STARTED | GasPot -> HMI -> DB |
| 5.4 | Test student write to GasPot | NOT STARTED | Changes appear in HMI |
| 5.5 | Test student write to DB | NOT STARTED | Changes appear in trends |
| 5.6 | Verify container restart recovery | NOT STARTED | Services reconnect |
| 5.7 | Test with docker compose up/down cycles | NOT STARTED | Stability |

### Acceptance Criteria

- [ ] HMI displays live data from GasPot
- [ ] New readings appear in historian every poll cycle
- [ ] Student can change tank name via TLS-350 and see in HMI
- [ ] Student can modify historian and see in HMI trends
- [ ] System recovers from container restart
- [ ] No memory leaks or connection exhaustion

### Deliverables

- Updated hmi/app/routes.py with polling
- Integration test documentation

---

## Phase 6: Scripts

**Status**: NOT STARTED

**Objective**: Create bullet-proof startup, shutdown, and reset scripts.

### Tasks

| # | Task | Status | Notes |
|---|------|--------|-------|
| 6.1 | Create scripts/start_lab.sh | NOT STARTED | Full startup with checks |
| 6.2 | Create scripts/stop_lab.sh | NOT STARTED | Clean shutdown |
| 6.3 | Create scripts/reset_lab.sh | NOT STARTED | Full reset with volumes |
| 6.4 | Test start_lab.sh on clean system | NOT STARTED | First-time startup |
| 6.5 | Test start_lab.sh with existing containers | NOT STARTED | Handles cleanup |
| 6.6 | Test start_lab.sh with port conflict | NOT STARTED | Reports error |
| 6.7 | Test stop_lab.sh | NOT STARTED | Clean stop |
| 6.8 | Test reset_lab.sh | NOT STARTED | Removes volumes |
| 6.9 | Test scripts with V1 compose | NOT STARTED | docker-compose syntax |
| 6.10 | Test scripts with V2 compose | NOT STARTED | docker compose syntax |

### Acceptance Criteria

- [ ] start_lab.sh works on fresh system
- [ ] start_lab.sh cleans up existing containers
- [ ] start_lab.sh reports port conflicts clearly
- [ ] start_lab.sh waits for healthy containers
- [ ] start_lab.sh displays access information
- [ ] stop_lab.sh stops all containers cleanly
- [ ] reset_lab.sh removes data volumes
- [ ] All scripts work with both Compose V1 and V2

### Deliverables

- scripts/start_lab.sh
- scripts/stop_lab.sh
- scripts/reset_lab.sh

---

## Phase 7: Student Tools

**Status**: NOT STARTED

**Objective**: Create ATG client script and documentation for students.

### Tasks

| # | Task | Status | Notes |
|---|------|--------|-------|
| 7.1 | Create tools/atg_client.py | NOT STARTED | CLI tool for students |
| 7.2 | Implement --help | NOT STARTED | Usage documentation |
| 7.3 | Implement inventory command | NOT STARTED | I20100 |
| 7.4 | Implement pressure command | NOT STARTED | I20600 |
| 7.5 | Implement set-name command | NOT STARTED | S602xx |
| 7.6 | Implement set-volume command | NOT STARTED | S60210 |
| 7.7 | Implement raw command | NOT STARTED | Send any command |
| 7.8 | Test all commands | NOT STARTED | Against GasPot |
| 7.9 | Create README.md | NOT STARTED | User documentation |
| 7.10 | Create lab exercise guide | NOT STARTED | Student exercises |

### Acceptance Criteria

- [ ] atg_client.py runs without dependencies beyond standard library
- [ ] --help shows clear usage
- [ ] All commands work correctly
- [ ] Error messages are helpful
- [ ] README.md documents all features
- [ ] Lab exercises cover discovery through exploitation

### Deliverables

- tools/atg_client.py
- README.md
- docs/LAB_EXERCISES.md (optional)

---

## Phase 8: Testing

**Status**: NOT STARTED

**Objective**: End-to-end validation on target Kali Linux environment.

### Tasks

| # | Task | Status | Notes |
|---|------|--------|-------|
| 8.1 | Test on Kali Linux VM | NOT STARTED | Fresh install |
| 8.2 | Test start_lab.sh | NOT STARTED | On Kali |
| 8.3 | Test telnet interaction | NOT STARTED | Built-in telnet |
| 8.4 | Test nmap NSE script | NOT STARTED | atg-info.nse |
| 8.5 | Test Metasploit module | NOT STARTED | atg_client |
| 8.6 | Test atg_client.py | NOT STARTED | Student tool |
| 8.7 | Test HMI in browser | NOT STARTED | Firefox on Kali |
| 8.8 | Test mysql client | NOT STARTED | Direct DB access |
| 8.9 | Run full student exercise flow | NOT STARTED | End-to-end |
| 8.10 | Document any issues | NOT STARTED | In VIBE_HISTORY.md |

### Acceptance Criteria

- [ ] All scripts work on Kali Linux
- [ ] Students can discover and enumerate GasPot
- [ ] Students can modify tank values
- [ ] Students can view and modify historian
- [ ] HMI displays correctly in Firefox
- [ ] No errors or warnings during normal operation

### Deliverables

- Test results documentation
- Any bug fixes discovered

---

## Milestones

| Milestone | Target | Phases | Status |
|-----------|--------|--------|--------|
| M1: Infrastructure Ready | - | 1, 3 | NOT STARTED |
| M2: GasPot Working | - | 2 | NOT STARTED |
| M3: HMI Working | - | 4 | NOT STARTED |
| M4: Full Integration | - | 5 | NOT STARTED |
| M5: Student Ready | - | 6, 7 | NOT STARTED |
| M6: Release Ready | - | 8 | NOT STARTED |

---

## Risk Register

| Risk | Impact | Mitigation |
|------|--------|------------|
| TLS-350 protocol parsing issues | High | Extensive testing with multiple tools |
| Docker Compose V1/V2 incompatibility | Medium | Test both, use detection in scripts |
| MariaDB slow startup | Medium | Adequate start_period in health check |
| Flask/GasPot connection issues | High | Retry logic, clear error messages |
| Student environment variations | Medium | Test on clean Kali, document requirements |

---

## Notes

- Development environment: Ubuntu Linux
- Target deployment: Kali Linux
- All passwords are intentionally weak for lab use
- Do NOT use this configuration in production
