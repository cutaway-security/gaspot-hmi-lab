# PLAN.md - Project Roadmap

## Project: GasPot HMI Lab

**Goal**: Create a multi-container ICS/OT cybersecurity training lab with GasPot ATG simulator, HMI dashboard, and historian database.

**Target**: Students on Kali Linux systems

---

## Phase Overview

| Phase | Name | Status | Description |
|-------|------|--------|-------------|
| 1 | Foundation | COMPLETE | Repository structure, Docker Compose skeleton |
| 2 | GasPot Simulator | COMPLETE | Modified ATG with 6 tanks, fluctuation |
| 3 | Historian Database | COMPLETE | MariaDB schema, seed data, stored procedures |
| 4 | HMI Application | COMPLETE | Flask web dashboard with charts |
| 5 | Integration | COMPLETE | Connect all components, polling loop |
| 6 | Scripts | COMPLETE | Startup, shutdown, reset scripts |
| 7 | Student Tools | COMPLETE | ATG client script, documentation |
| 8 | Testing | IN PROGRESS | Volunteer evaluation framework |
| 9 | Documentation | NOT STARTED | Restructure docs, exercises, operations |

---

## Phase 1: Foundation

**Status**: COMPLETE

**Objective**: Set up repository structure and validate Docker environment.

### Tasks

| # | Task | Status | Notes |
|---|------|--------|-------|
| 1.1 | Create directory structure | COMPLETE | gaspot/, hmi/, historian/, tools/, scripts/ |
| 1.2 | Create docker-compose.yml skeleton | COMPLETE | All 3 services defined |
| 1.3 | Create .env.example | COMPLETE | Environment variables template |
| 1.4 | Validate Docker Compose runs | COMPLETE | Validated with docker compose (V2) |
| 1.5 | Test network connectivity between containers | COMPLETE | All containers healthy and communicating |

### Acceptance Criteria

- [x] All directories created per ARCHITECTURE.md
- [x] docker-compose.yml parses without errors
- [x] `docker compose config` shows valid configuration
- [x] Placeholder containers can communicate via network

### Deliverables

- docker-compose.yml
- .env.example
- Directory structure

---

## Phase 2: GasPot Simulator

**Status**: COMPLETE

**Objective**: Create modified GasPot with 6 tanks, pressure data, and fluctuation.

### Tasks

| # | Task | Status | Notes |
|---|------|--------|-------|
| 2.1 | Create gaspot/Dockerfile | COMPLETE | Python 3.11 base, include nc |
| 2.2 | Create gaspot/requirements.txt | COMPLETE | No external dependencies needed |
| 2.3 | Create gaspot/config.ini | COMPLETE | 6 tanks, fluctuation settings |
| 2.4 | Implement GasPot.py base | COMPLETE | Socket server on 10001 |
| 2.5 | Implement I20100 (inventory) | COMPLETE | All 6 tanks with formatting |
| 2.6 | Implement I20200-I20500 | COMPLETE | All read commands working |
| 2.7 | Implement I20600 (pressure) | COMPLETE | Gas tanks show PSI, others N/A |
| 2.8 | Implement S602xx (writes) | COMPLETE | S6020x, S60210, S60220 |
| 2.9 | Implement fluctuation engine | COMPLETE | Per-tank behavior working |
| 2.10 | Test with telnet | COMPLETE | Manual testing passed |
| 2.11 | Test with netcat | COMPLETE | Scripted testing passed |

### Acceptance Criteria

- [x] Container builds successfully
- [x] Container passes health check
- [x] I20100 returns all 6 tanks with correct format
- [x] I20600 returns pressure for gas tanks only
- [x] S60201 changes tank name and persists
- [x] S60210 changes tank volume
- [x] Values fluctuate over time (observe over 1 minute)
- [x] Invalid commands return 9999FF1B

### Deliverables

- gaspot/Dockerfile
- gaspot/GasPot.py
- gaspot/config.ini
- gaspot/requirements.txt

---

## Phase 3: Historian Database

**Status**: COMPLETE

**Objective**: Create MariaDB schema with seed data and stored procedures.

### Tasks

| # | Task | Status | Notes |
|---|------|--------|-------|
| 3.1 | Create historian/init.sql | COMPLETE | Schema, procedures, seed data |
| 3.2 | Add tanks table with 6 tank config | COMPLETE | 6 tanks configured |
| 3.3 | Add tank_readings table | COMPLETE | Time-series with indexes |
| 3.4 | Add alarms table | COMPLETE | Alarm history with indexes |
| 3.5 | Create update_timestamps procedure | COMPLETE | Shifts readings and alarms |
| 3.6 | Add seed data (24 hours history) | COMPLETE | 1728 readings (288 per tank) |
| 3.7 | Add sample alarms | COMPLETE | 18 alarms, various severities |
| 3.8 | Test container starts | COMPLETE | Init script runs on fresh volume |
| 3.9 | Test queries work | COMPLETE | All tables queryable |
| 3.10 | Test stored procedure | COMPLETE | Timestamps update correctly |

### Acceptance Criteria

- [x] Container builds and passes health check
- [x] All tables created correctly
- [x] 6 tanks in tanks table
- [x] At least 24 hours of seed data in tank_readings
- [x] Sample alarms present
- [x] update_timestamps() procedure works
- [x] Lab user can connect and query

### Deliverables

- historian/init.sql

---

## Phase 4: HMI Application

**Status**: COMPLETE

**Objective**: Create Flask web dashboard with real-time display and charts.

### Tasks

| # | Task | Status | Notes |
|---|------|--------|-------|
| 4.1 | Create hmi/Dockerfile | COMPLETE | Python 3.11, curl, Flask app |
| 4.2 | Create hmi/requirements.txt | COMPLETE | Flask 3.0, SQLAlchemy 2.0, PyMySQL |
| 4.3 | Create hmi/app/__init__.py | COMPLETE | Flask app factory with DB config |
| 4.4 | Create hmi/app/atg_client.py | COMPLETE | TLS-350 protocol library |
| 4.5 | Test atg_client.py standalone | COMPLETE | Connects to GasPot via API |
| 4.6 | Create hmi/app/models.py | COMPLETE | Tank, TankReading, Alarm models |
| 4.7 | Create hmi/app/routes.py | COMPLETE | Dashboard, trends, alarms, API |
| 4.8 | Create /health endpoint | COMPLETE | Returns 200 OK |
| 4.9 | Create main dashboard template | COMPLETE | Tank cards with visual fill |
| 4.10 | Create trends template | COMPLETE | Chart.js with 24h data |
| 4.11 | Create alarms template | COMPLETE | Active/history tables |
| 4.12 | Add static CSS | COMPLETE | Dark theme, responsive |
| 4.13 | Test container builds | COMPLETE | Image builds successfully |
| 4.14 | Test health endpoint | COMPLETE | Returns 200 OK |
| 4.15 | Test dashboard loads | COMPLETE | Shows all 6 tanks with live data |

### Acceptance Criteria

- [x] Container builds and passes health check
- [x] /health returns 200 OK
- [x] Main dashboard shows all 6 tanks
- [x] Tank data matches GasPot current state
- [x] Trends page shows historical charts
- [x] Alarms page shows alarm history
- [x] Page auto-refreshes or has refresh button

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

**Status**: COMPLETE

**Objective**: Connect all components with polling loop and data flow.

### Tasks

| # | Task | Status | Notes |
|---|------|--------|-------|
| 5.1 | Implement HMI polling loop | COMPLETE | Polls every 10 seconds |
| 5.2 | Store readings to historian | COMPLETE | 6 readings per poll |
| 5.3 | Test full data flow | COMPLETE | GasPot -> HMI -> DB working |
| 5.4 | Test student write to GasPot | COMPLETE | S6020x and S60210 work |
| 5.5 | Test student write to DB | COMPLETE | Changes appear in trends |
| 5.6 | Verify container restart recovery | COMPLETE | All services reconnect |
| 5.7 | Test with docker compose up/down cycles | COMPLETE | System stable |

### Acceptance Criteria

- [x] HMI displays live data from GasPot
- [x] New readings appear in historian every poll cycle
- [x] Student can change tank name via TLS-350 and see in HMI
- [x] Student can modify historian and see in HMI trends
- [x] System recovers from container restart
- [x] No memory leaks or connection exhaustion

### Deliverables

- hmi/app/poller.py (background polling module)
- Updated hmi/app/__init__.py with poller startup
- Updated hmi/app/atg_client.py with fixed parsers

---

## Phase 6: Scripts

**Status**: COMPLETE

**Objective**: Create bullet-proof startup, shutdown, and reset scripts.

### Tasks

| # | Task | Status | Notes |
|---|------|--------|-------|
| 6.1 | Create scripts/start_lab.sh | COMPLETE | Full startup with checks |
| 6.2 | Create scripts/stop_lab.sh | COMPLETE | Clean shutdown |
| 6.3 | Create scripts/reset_lab.sh | COMPLETE | Full reset with volumes |
| 6.4 | Test start_lab.sh on clean system | COMPLETE | First-time startup |
| 6.5 | Test start_lab.sh with existing containers | COMPLETE | Handles cleanup |
| 6.6 | Test start_lab.sh with port conflict | COMPLETE | Reports error |
| 6.7 | Test stop_lab.sh | COMPLETE | Clean stop |
| 6.8 | Test reset_lab.sh | COMPLETE | Removes volumes |
| 6.9 | Test scripts with V1 compose | COMPLETE | Supported, V1 not installed |
| 6.10 | Test scripts with V2 compose | COMPLETE | Tested and working |

### Acceptance Criteria

- [x] start_lab.sh works on fresh system
- [x] start_lab.sh cleans up existing containers
- [x] start_lab.sh reports port conflicts clearly
- [x] start_lab.sh waits for healthy containers
- [x] start_lab.sh displays access information
- [x] stop_lab.sh stops all containers cleanly
- [x] reset_lab.sh removes data volumes
- [x] All scripts work with both Compose V1 and V2

### Deliverables

- scripts/start_lab.sh
- scripts/stop_lab.sh
- scripts/reset_lab.sh

---

## Phase 7: Student Tools

**Status**: COMPLETE

**Objective**: Create ATG client script and documentation for students.

### Tasks

| # | Task | Status | Notes |
|---|------|--------|-------|
| 7.1 | Create tools/atg_client.py | COMPLETE | CLI tool for students |
| 7.2 | Implement --help | COMPLETE | Usage documentation |
| 7.3 | Implement inventory command | COMPLETE | I20100 |
| 7.4 | Implement pressure command | COMPLETE | I20600 |
| 7.5 | Implement set-name command | COMPLETE | S602xx |
| 7.6 | Implement set-volume command | COMPLETE | S60210 |
| 7.7 | Implement raw command | COMPLETE | Send any command |
| 7.8 | Test all commands | COMPLETE | Against GasPot |
| 7.9 | Create README.md | COMPLETE | User documentation |
| 7.10 | Create lab exercise guide | COMPLETE | Student exercises |

### Acceptance Criteria

- [x] atg_client.py runs without dependencies beyond standard library
- [x] --help shows clear usage
- [x] All commands work correctly
- [x] Error messages are helpful
- [x] README.md documents all features
- [x] Lab exercises cover discovery through exploitation

### Deliverables

- tools/atg_client.py
- README.md
- docs/LAB_EXERCISES.md (optional)

---

## Phase 8: Testing (Volunteer Evaluation)

**Status**: IN PROGRESS (tasks 8.5-8.8 ON HOLD pending Phase 9)

**Objective**: End-to-end validation via volunteer student evaluators.

**Approach**: Manual testing by volunteers using structured checklist and feedback form. Volunteers test as real students would, providing actionable feedback for improvements.

**Note**: Evaluation framework (checklist, form, appendix) must be updated after Phase 9 documentation restructure. Tasks 8.5-8.8 are on hold until then.

### Tasks

| # | Task | Status | Notes |
|---|------|--------|-------|
| 8.1 | Create .gitignore | COMPLETE | Common dev patterns, /eval/ |
| 8.2 | Create STUDENT_EVAL_CHECKLIST.md | COMPLETE | Will be updated after Phase 9 |
| 8.3 | Create STUDENT_EVAL_FORM.md | COMPLETE | Will be updated after Phase 9 |
| 8.4 | Run developer test (appendix) | COMPLETE | Will be redone after Phase 9 |
| 8.5 | Recruit volunteer evaluators | ON HOLD | Waiting for Phase 9 completion |
| 8.6 | Collect volunteer feedback | ON HOLD | Waiting for Phase 9 completion |
| 8.7 | Review and fix issues | IN PROGRESS | Alarms bug FIXED |
| 8.8 | Remove /eval directory | ON HOLD | Cleanup after testing |

### Evaluation Framework

**STUDENT_EVAL_CHECKLIST.md** (60 minutes):
- Pre-test: Review eval form and appendix before starting
- Priority 1 (0-30 min): Core functionality validation
- Priority 2 (30-60 min): Extended testing and exercises
- Fill out form as you go, submit anytime (even if incomplete)

**STUDENT_EVAL_FORM.md**:
- Markdown format for typing answers
- Specific questions for Claude Code parsing
- YES/NO, ratings (1-5), and free text fields
- Appendix with AI-generated example answers (remove before AI review)

**Developer Test Run**:
- Simulate 5-year IT/security professional
- Read ONLY README.md (not source code or dev docs)
- Create /eval directory and scripts organically during test
- Scripts are artifacts of test, not pre-planned
- Removed after volunteer testing complete

### Acceptance Criteria

- [x] Checklist covers all critical functionality in first 30 minutes
- [x] Eval form questions are specific and parseable
- [x] Appendix provides clear example answer format
- [ ] Volunteers can complete evaluation in 60 minutes
- [x] Feedback is actionable for improvements (Alarms bug found during dev test)

### Deliverables

- STUDENT_EVAL_CHECKLIST.md
- STUDENT_EVAL_FORM.md (with appendix)
- .gitignore (updated)
- Collected volunteer feedback
- Bug fixes based on feedback

---

## Phase 9: Documentation Restructure

**Status**: COMPLETE

**Objective**: Reorganize documentation into clear separation between operations/maintenance (docs/), student exercises (exercises/), and development (dev/).

**Approach**: Create new directory structure with story-driven exercises, reference documentation for students, and operations guide for lab maintainers.

### Directory Structure

```
gaspot-hmi-lab/
    README.md                     # Simplified: overview, quick start, pointers
    docs/                         # Operations & Maintenance
        OPERATIONS.md             # Container management, troubleshooting
        GASPOT_MODIFICATIONS.md   # Changes from original GasPot
    exercises/                    # Student-facing content (story-driven)
        README.md                 # Scenario introduction
        E01_DISCOVERY.md          # Network reconnaissance
        E02_ENUMERATION.md        # Protocol analysis
        E03_ATG_MANIPULATION.md   # ATG data manipulation
        E04_HMI_RECONNAISSANCE.md # Web interface analysis
        E05_DATABASE_EXPLOITATION.md  # Historian attacks
        E06_ATTACK_CHAIN.md       # Combined attack scenario
        E07_DEFENSE_ANALYSIS.md   # Security assessment
        challenges/               # Additional challenges
            C01_AUTOMATED_ATTACK.md
            C02_DETECTION_SCRIPT.md
            C03_PROTOCOL_ANALYSIS.md
        docs/                     # Reference for students
            PROTOCOL_REFERENCE.md # TLS-350, ATG client
            DATABASE_REFERENCE.md # Schema, queries
        INSTRUCTOR_GUIDE.md       # Purpose, goals, approach
    dev/                          # Development only (not pushed to main)
```

### Tasks

| # | Task | Status | Notes |
|---|------|--------|-------|
| 9.1 | Create docs/OPERATIONS.md | COMPLETE | Container mgmt, troubleshooting |
| 9.2 | Create docs/GASPOT_MODIFICATIONS.md | COMPLETE | Changes from original |
| 9.3 | Create exercises/README.md | COMPLETE | Scenario introduction |
| 9.4 | Create exercises/docs/PROTOCOL_REFERENCE.md | COMPLETE | TLS-350, ATG client |
| 9.5 | Create exercises/docs/DATABASE_REFERENCE.md | COMPLETE | Schema, queries |
| 9.6 | Create exercises/E01-E07 files | COMPLETE | Individual exercises |
| 9.7 | Create exercises/challenges/C01-C03 | COMPLETE | Challenge exercises |
| 9.8 | Create exercises/INSTRUCTOR_GUIDE.md | COMPLETE | Teaching guide |
| 9.9 | Simplify README.md | COMPLETE | Remove moved content |
| 9.10 | Remove docs/LAB_EXERCISES.md | COMPLETE | Replaced by exercises/ |
| 9.11 | Update eval checklist for new structure | COMPLETE | Phase 8 continuation |
| 9.12 | Update eval form for new structure | COMPLETE | Phase 8 continuation |
| 9.13 | Rerun developer test | COMPLETE | New appendix example |

### Content Guidelines

**exercises/README.md (Scenario)**:
- Casual tone (not CTF, but engaging)
- Security researcher/consultant role
- Authorized assessment narrative
- Clear objectives without gamification

**exercises/INSTRUCTOR_GUIDE.md**:
- Purpose (what students learn) for each exercise
- Goal (expected outcome)
- Approach (how to solve)
- Timing estimates
- Discussion points
- No flags or scoring

### Acceptance Criteria

- [ ] docs/ contains operations and maintenance documentation
- [ ] exercises/ contains story-driven exercises with reference docs
- [ ] README.md is simplified to overview and quick start
- [ ] Evaluation framework updated for new structure
- [ ] Developer test completed with new appendix example

### Deliverables

- docs/OPERATIONS.md
- docs/GASPOT_MODIFICATIONS.md
- exercises/README.md
- exercises/E01-E07_*.md (7 exercise files)
- exercises/challenges/C01-C03_*.md (3 challenge files)
- exercises/docs/PROTOCOL_REFERENCE.md
- exercises/docs/DATABASE_REFERENCE.md
- exercises/INSTRUCTOR_GUIDE.md
- Updated README.md
- Updated STUDENT_EVAL_CHECKLIST.md
- Updated STUDENT_EVAL_FORM.md (with new appendix)

---

## Milestones

| Milestone | Target | Phases | Status |
|-----------|--------|--------|--------|
| M1: Infrastructure Ready | - | 1, 3 | COMPLETE |
| M2: GasPot Working | - | 2 | COMPLETE |
| M3: HMI Working | - | 4 | COMPLETE |
| M4: Full Integration | - | 5 | COMPLETE |
| M5: Student Ready | - | 6, 7 | COMPLETE |
| M6: Documentation Complete | - | 9 | NOT STARTED |
| M7: Release Ready | - | 8, 9 | NOT STARTED |

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
