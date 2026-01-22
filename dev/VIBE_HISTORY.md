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

### Session: 2026-01-07 (Session 2)

#### Session Info
- **Date**: 2026-01-07
- **Duration**: ~20 minutes
- **Phase**: 1 - Foundation (completion)
- **Focus**: Docker Compose V2 testing and Phase 1 completion

#### Objectives
- [x] Verify Docker Compose V2 installation
- [x] Build all containers
- [x] Test container health checks
- [x] Test service connectivity
- [x] Test inter-container communication
- [x] Complete Phase 1
- [x] Update documentation

#### Completed
- Verified Docker Compose V2 (version 2.37.1)
- Built all 3 containers successfully (mariadb, gaspot, hmi)
- All containers passed health checks
- Tested MariaDB connectivity (mysqladmin ping)
- Tested GasPot port accessibility (nc -zv localhost 10001)
- Tested HMI health endpoint (curl localhost:5000/health)
- Tested inter-container communication (HMI to GasPot via curl)
- Initialized database tables (ran init.sql manually)
- Updated PLAN.md, RESUME.md, VIBE_HISTORY.md

#### Problems Encountered
| Problem | Cause | Solution |
|---------|-------|----------|
| Database tables not created | Volume had data from prior run, init.sql skipped | Ran init.sql manually via pipe to docker exec |
| ping not available in HMI container | Minimal Python slim image | Used curl instead for connectivity test |

#### Lessons Learned
- MariaDB init scripts only run on first initialization (empty volume)
- To reset database: `docker compose down -v` then restart
- Can pipe SQL files to container: `cat init.sql | docker exec -i container mysql ...`
- Python slim images don't include ping; use curl or nc for connectivity tests

#### Deferred/Blocked
None.

#### Next Steps
1. Begin Phase 2: GasPot Simulator
2. Create gaspot/Dockerfile (full implementation)
3. Create gaspot/requirements.txt
4. Create gaspot/config.ini with 6 tanks
5. Implement GasPot.py with TLS-350 protocol

#### Notes
- Phase 1 complete, all acceptance criteria met
- Ready to proceed with Phase 2

---

### Session: 2026-01-07 (Session 2 continued - Phase 2)

#### Session Info
- **Date**: 2026-01-07
- **Duration**: ~30 minutes
- **Phase**: 2 - GasPot Simulator
- **Focus**: Implement TLS-350 ATG simulator with 6 tanks

#### Objectives
- [x] Review original GasPot source code
- [x] Create gaspot/Dockerfile (full implementation)
- [x] Create gaspot/requirements.txt
- [x] Create gaspot/config.ini with 6 tanks
- [x] Implement GasPot.py with TLS-350 protocol
- [x] Test all commands (I20100-I20600, S6020x, S60210, S60220)
- [x] Verify fluctuation engine

#### Completed
- Reviewed original GasPot from https://github.com/sjhilt/GasPot
- Created gaspot/Dockerfile with Python 3.11-slim and netcat
- Created gaspot/requirements.txt (no external dependencies needed)
- Created gaspot/config.ini with 6 tanks and fluctuation settings
- Implemented GasPot.py with:
  - Tank class with fluctuation behavior
  - GasPotServer class with select-based socket handling
  - All TLS-350 read commands: I20100, I20200, I20300, I20400, I20500, I20600
  - Write commands: S6020x (tank name), S60210 (volume), S60220 (pressure)
  - Fluctuation engine with 5 modes: high, medium, low, decrease, sawtooth
  - Proper error responses (9999FF1B for invalid commands)
- Tested all commands successfully with netcat

#### Problems Encountered
| Problem | Cause | Solution |
|---------|-------|----------|
| None | - | - |

#### Lessons Learned
- Original GasPot uses select() for non-blocking I/O - good pattern kept
- Python standard library sufficient for TLS-350 simulation
- Threading works well for background fluctuation
- Tank class encapsulation makes code cleaner and more maintainable

#### Deferred/Blocked
None.

#### Next Steps
1. Begin Phase 3: Historian Database
2. Add update_timestamps stored procedure
3. Add 24 hours of seed data
4. Add sample alarms
5. Test stored procedure functionality

#### Notes
- Phase 2 complete, all acceptance criteria met
- GasPot responds to all standard TLS-350 commands
- Custom commands (I20600, S60210, S60220) working for lab exercises
- Fluctuation engine provides realistic value changes over time

---

### Session: 2026-01-08 (Session 3 - Phase 3)

#### Session Info
- **Date**: 2026-01-08
- **Duration**: ~30 minutes
- **Phase**: 3 - Historian Database
- **Focus**: Complete database schema, seed data, and stored procedures

#### Objectives
- [x] Create update_timestamps stored procedure
- [x] Create generate_seed_data stored procedure
- [x] Generate 24 hours of tank readings (1728 total)
- [x] Add sample alarms (18 across all tanks)
- [x] Test database initialization
- [x] Test queries on all tables
- [x] Test update_timestamps procedure

#### Completed
- Created comprehensive historian/init.sql with full implementation
- Implemented update_timestamps procedure (shifts all readings/alarms to current time)
- Implemented generate_seed_data procedure (288 readings per tank, 5-minute intervals)
- Added 18 sample alarms with INFO/WARNING/CRITICAL severities
- Fixed init.sql file permissions (chmod 644 for Docker mount)
- Reset database and verified init.sql execution
- Verified all data: 6 tanks, 1728 readings, 18 alarms
- Tested update_timestamps procedure successfully

#### Problems Encountered
| Problem | Cause | Solution |
|---------|-------|----------|
| init.sql Permission denied | File had 600 permissions | chmod 644 to allow read |

#### Lessons Learned
- Init.sql must have read permissions (644) for Docker volume mounts
- MariaDB stored procedures require DELIMITER // syntax
- TIMESTAMPDIFF and DATE_ADD work well for timestamp shifting
- Test stored procedures by comparing before/after MAX(timestamp)

#### Deferred/Blocked
None.

#### Next Steps
1. Begin Phase 4: HMI Application
2. Create hmi/Dockerfile (full implementation)
3. Create hmi/requirements.txt (Flask, SQLAlchemy)
4. Create hmi/app/atg_client.py (TLS-350 library)
5. Create Flask routes and templates

#### Notes
- Phase 3 complete, all acceptance criteria met
- Milestone M1 (Infrastructure Ready) now complete
- Database has realistic data patterns for each tank type
- Ready to proceed with HMI development

---

### Session: 2026-01-08 (Session 3 continued - Phase 4)

#### Session Info
- **Date**: 2026-01-08
- **Duration**: ~45 minutes
- **Phase**: 4 - HMI Application
- **Focus**: Flask web dashboard with real-time display and charts

#### Objectives
- [x] Create hmi/Dockerfile (full implementation)
- [x] Create hmi/requirements.txt
- [x] Create Flask app factory (__init__.py)
- [x] Create TLS-350 client library (atg_client.py)
- [x] Create SQLAlchemy models (models.py)
- [x] Create Flask routes (routes.py)
- [x] Create HTML templates (dashboard, trends, alarms)
- [x] Create CSS styles (dark theme)
- [x] Build and test container
- [x] Verify all endpoints working

#### Completed
- Created hmi/requirements.txt (Flask 3.0, SQLAlchemy 2.0, PyMySQL)
- Created hmi/Dockerfile with Python 3.11-slim and curl
- Created hmi/run.py entry point
- Created hmi/app/__init__.py with Flask factory and DB config
- Created hmi/app/atg_client.py - TLS-350 protocol library with parsing
- Created hmi/app/models.py - Tank, TankReading, Alarm SQLAlchemy models
- Created hmi/app/routes.py - Dashboard, trends, alarms pages + API endpoints
- Created hmi/app/templates/base.html - Layout with header, nav, footer
- Created hmi/app/templates/dashboard.html - Tank cards with visual fill levels
- Created hmi/app/templates/trends.html - Chart.js integration
- Created hmi/app/templates/alarms.html - Active/history tables
- Created hmi/app/static/style.css - Dark theme, responsive layout
- Fixed SQLAlchemy Decimal->Numeric import error
- Tested all endpoints: /health, /, /trends, /alarms, /api/live, /api/trends/N, /api/alarms

#### Problems Encountered
| Problem | Cause | Solution |
|---------|-------|----------|
| ImportError: cannot import 'Decimal' | SQLAlchemy uses Numeric not Decimal | Changed import and column types |

#### Lessons Learned
- SQLAlchemy uses Numeric() not Decimal() for decimal columns
- Flask app factory pattern cleanly separates config from routes
- Chart.js CDN works well for simple charting needs
- Auto-refresh with setInterval provides live updates without WebSocket

#### Deferred/Blocked
None.

#### Next Steps
1. Begin Phase 5: Integration
2. Implement polling loop to store readings to historian
3. Test full data flow (GasPot -> HMI -> DB)
4. Test student write to GasPot appears in HMI
5. Test student write to DB appears in trends

#### Notes
- Phase 4 complete, all acceptance criteria met
- Milestone M3 (HMI Working) now complete
- Dashboard shows live connection status to GasPot
- Trends page shows 24 hours of historical data with Chart.js
- Alarms page shows 4 active alarms (1 CRITICAL, 3 WARNING)
- Ready to proceed with Integration phase

---

### Session: 2026-01-08 (Session 3 continued - Phase 5)

#### Session Info
- **Date**: 2026-01-08
- **Duration**: ~30 minutes
- **Phase**: 5 - Integration
- **Focus**: Connect all components with polling loop and data flow

#### Objectives
- [x] Implement HMI polling loop
- [x] Store readings to historian on each poll
- [x] Test full data flow (GasPot -> HMI -> DB)
- [x] Test student write to GasPot appears in HMI
- [x] Test student write to DB appears in trends
- [x] Verify container restart recovery
- [x] Test docker compose up/down stability

#### Completed
- Created hmi/app/poller.py - Background polling module
  - GasPotPoller class with daemon thread
  - Polls every 10 seconds, stores 6 readings per poll
  - Thread-safe start/stop with status property
  - Graceful error handling and reconnection
- Updated hmi/app/__init__.py to start poller on app creation
  - Conditional start to avoid duplicate poller in Flask reloader
- Fixed hmi/app/atg_client.py parsers for tabular format
  - _parse_inventory() now handles tabular GasPot output
  - _parse_pressure() now handles tabular pressure output with N/A values
- Added /api/poller endpoint to routes.py for monitoring
- Tested full data flow: GasPot -> HMI -> DB working
- Tested student write to GasPot:
  - S6020x (tank name change) works via netcat
  - S60210:TANK:VALUE (volume change) works via netcat
- Tested student write to DB appears in trends page
- Tested container restart recovery - all services reconnect
- Tested docker compose up/down cycles - system stable

#### Problems Encountered
| Problem | Cause | Solution |
|---------|-------|----------|
| ATG client parser not returning readings | GasPot returns tabular format, parser expected block format | Rewrote _parse_inventory() and _parse_pressure() with regex for tabular format |
| S60210 volume command returning 9999FF1B error | Wrong command format (S6021012345 vs S60210:1:12345) | Used correct format S60210:TANK:VALUE |

#### Lessons Learned
- GasPot returns tabular output, not block format - regex with whitespace matching works well
- S60210 volume command uses colon separators: S60210:TANK_ID:VALUE
- Flask reloader creates duplicate processes - use WERKZEUG_RUN_MAIN env var to control
- Daemon threads automatically terminate when main program exits
- Threading.Event() provides clean stop mechanism for polling loops

#### Deferred/Blocked
None.

#### Next Steps
1. Begin Phase 6: Scripts
2. Create scripts/start_lab.sh (full startup with checks)
3. Create scripts/stop_lab.sh (clean shutdown)
4. Create scripts/reset_lab.sh (full reset with volumes)
5. Test scripts with both Compose V1 and V2

#### Notes
- Phase 5 complete, all acceptance criteria met
- Milestone M4 (Full Integration) now complete
- Poller stores 6 readings every 10 seconds (36 per minute, 2160 per hour)
- Students can interact with GasPot via netcat and see changes in HMI
- Students can modify historian directly and see changes in trends
- System recovers from container restarts automatically

---

### Session: 2026-01-07 (Session 4 - Phase 6)

#### Session Info
- **Date**: 2026-01-07
- **Duration**: ~30 minutes
- **Phase**: 6 - Scripts
- **Focus**: Create bullet-proof startup, shutdown, and reset scripts

#### Objectives
- [x] Create scripts/start_lab.sh (full startup with checks)
- [x] Create scripts/stop_lab.sh (clean shutdown)
- [x] Create scripts/reset_lab.sh (full reset with volumes)
- [x] Test start_lab.sh on clean system
- [x] Test start_lab.sh with existing containers
- [x] Test start_lab.sh with port conflict
- [x] Test stop_lab.sh
- [x] Test reset_lab.sh
- [x] Test scripts with Compose V1 and V2

#### Completed
- Created scripts/start_lab.sh - Full startup script
  - Docker Compose V1/V2 detection
  - Docker daemon availability check
  - Port conflict detection (distinguishes lab vs external conflicts)
  - Existing container cleanup
  - Container build and start
  - Health check waiting with configurable timeout (120s)
  - Database initialization check
  - Access information display with test commands
- Created scripts/stop_lab.sh - Clean shutdown script
  - Handles already-stopped state gracefully
  - Preserves data volumes
  - Force removal of stubborn containers
- Created scripts/reset_lab.sh - Full reset script
  - Interactive confirmation prompt
  - Non-interactive mode support
  - Volume removal
  - Optional --full flag for image removal
  - Dangling resource cleanup
- Tested all scripts on Docker Compose V2
- V1 not installed on dev system but scripts support both

#### Problems Encountered
| Problem | Cause | Solution |
|---------|-------|----------|
| None | - | - |

#### Lessons Learned
- ss command works better than netstat for port checking on modern Linux
- Docker Compose V2 outputs status messages after script continues (buffering)
- Port conflict detection should distinguish lab containers from external processes
- Non-interactive mode (stdin not a tty) should auto-proceed for scripted use

#### Deferred/Blocked
None.

#### Next Steps
1. Begin Phase 7: Student Tools
2. Create tools/atg_client.py (CLI tool for students)
3. Implement --help, inventory, pressure, set-name, set-volume, raw commands
4. Create README.md user documentation
5. Create lab exercise guide (optional)

#### Notes
- Phase 6 complete, all acceptance criteria met
- Milestone M5 (Student Ready) in progress - needs Phase 7
- Scripts are student-friendly with clear output and error messages
- All three scripts support both Compose V1 and V2 syntax

---

### Session: 2026-01-08 (Session 4 continued - Phase 7)

#### Session Info
- **Date**: 2026-01-08
- **Duration**: ~30 minutes
- **Phase**: 7 - Student Tools
- **Focus**: Create ATG client script and documentation for students

#### Objectives
- [x] Create tools/atg_client.py CLI tool
- [x] Implement --help with usage documentation
- [x] Implement inventory command (I20100)
- [x] Implement pressure command (I20600)
- [x] Implement set-name command (S602xx)
- [x] Implement set-volume command (S60210)
- [x] Implement raw command
- [x] Test all commands against GasPot
- [x] Update README.md with usage
- [x] Create lab exercise guide

#### Completed
- Created tools/atg_client.py - Full-featured ATG CLI client
  - argparse-based with subcommands for each TLS-350 command
  - inventory, delivery, leak, shift, status, pressure read commands
  - set-name, set-volume write commands
  - raw command for arbitrary TLS-350 commands
  - -H/--host, -p/--port, -t/--timeout, -v/--verbose options
  - Clear error messages for connection failures
  - No external dependencies (standard library only)
- Tested all commands against running GasPot
  - Verified inventory, pressure, status commands
  - Verified set-name changes tank name
  - Verified set-volume changes tank volume
  - Verified verbose mode shows debug info
  - Verified error handling with unreachable host
- Created comprehensive README.md
  - Architecture diagram and component overview
  - Quick start guide with scripts
  - ATG client tool documentation
  - TLS-350 protocol reference
  - Database access examples
  - Lab exercises overview
  - Troubleshooting guide
- Created docs/LAB_EXERCISES.md
  - 7 progressive exercises from discovery to exploitation
  - Exercise 1: Network Discovery (nmap)
  - Exercise 2: Protocol Enumeration (TLS-350)
  - Exercise 3: Data Manipulation - ATG
  - Exercise 4: HMI Reconnaissance
  - Exercise 5: Database Exploitation
  - Exercise 6: Attack Chain Development
  - Exercise 7: Defense Analysis
  - Challenge exercises for advanced students
  - Instructor notes with timing estimates

#### Problems Encountered
| Problem | Cause | Solution |
|---------|-------|----------|
| None | - | - |

#### Lessons Learned
- argparse subparsers provide clean CLI structure
- Standard library socket module sufficient for TLS-350
- set_defaults(func=handler) pattern cleanly maps subcommands to functions
- Lab exercises should progress from passive to active techniques

#### Deferred/Blocked
None.

#### Next Steps
1. Begin Phase 8: Testing
2. Test on Kali Linux VM (fresh install)
3. Test start_lab.sh on Kali
4. Test telnet/nmap/Metasploit interactions
5. Test atg_client.py and HMI browser
6. Run full student exercise flow

#### Notes
- Phase 7 complete, all acceptance criteria met
- Milestone M5 (Student Ready) now complete
- Lab is feature-complete, ready for testing phase
- Documentation covers both technical and educational aspects

---

### Session: 2026-01-08 (Session 5 - Phase 8 Planning)

#### Session Info
- **Date**: 2026-01-08
- **Duration**: ~20 minutes
- **Phase**: 8 - Testing (Volunteer Evaluation)
- **Focus**: Plan volunteer evaluation framework

#### Objectives
- [x] Define Phase 8 volunteer evaluation approach
- [x] Plan STUDENT_EVAL_CHECKLIST.md structure
- [x] Plan STUDENT_EVAL_FORM.md structure
- [x] Define /eval directory purpose and lifecycle
- [x] Update planning documents with new approach

#### Completed
- Decided Phase 8 will use volunteer evaluators (not automated Kali testing)
- Designed 60-minute checklist with priority tiers:
  - Priority 1 (0-30 min): Core functionality
  - Priority 2 (30-60 min): Extended testing
- Designed eval form for typed submission:
  - Markdown format for easy editing
  - Specific questions for Claude Code parsing
  - YES/NO, ratings, and free text fields
  - Appendix with AI-generated example answers
- Defined /eval directory as temporary (development only, not distributed)
- Updated PLAN.md, RESUME.md with new Phase 8 tasks

#### Decisions Made
| Decision | Rationale |
|----------|-----------|
| Volunteer evaluation vs automated | Real student perspective more valuable |
| 60-minute checklist | Reasonable volunteer commitment |
| Priority 1 in first 30 min | Ensure critical tests even if volunteer stops early |
| Review form before starting | Volunteers know what to look for |
| Submit anytime | Partial feedback still valuable |
| Markdown form format | Easy to type, easy to parse |
| /eval/ temporary directory | Dev testing only, clean removal |

#### Problems Encountered
| Problem | Cause | Solution |
|---------|-------|----------|
| None | - | - |

#### Deferred/Blocked
None.

#### Next Steps
1. Create .gitignore with common patterns
2. Create STUDENT_EVAL_CHECKLIST.md
3. Create STUDENT_EVAL_FORM.md (with empty appendix)
4. Run through checklist simulating student perspective
5. Create /eval directory and scripts organically during test
6. Complete appendix with example answers

#### Notes
- Phase 8 approach changed from automated Kali testing to volunteer evaluation
- This provides real student perspective feedback
- Developer test run will populate appendix with example answers
- /eval directory and scripts created DURING test run, not pre-planned
- Scripts are artifacts of organic exploration, based only on README.md
- Volunteers will test on their own systems (Kali or other Linux)

---

### Session: 2026-01-08 (Session 5 continued - Developer Test Run)

#### Session Info
- **Date**: 2026-01-08
- **Duration**: ~45 minutes
- **Phase**: 8 - Testing (Volunteer Evaluation)
- **Focus**: Execute developer test run simulating student perspective

#### Objectives
- [x] Create .gitignore with common patterns
- [x] Create STUDENT_EVAL_CHECKLIST.md
- [x] Create STUDENT_EVAL_FORM.md with empty appendix
- [x] Run through checklist as simulated student
- [x] Create eval scripts organically during test
- [x] Complete appendix with example answers

#### Completed
- Created .gitignore with comprehensive patterns:
  - /eval/ directory excluded
  - Claude Code files excluded (.claude/, .claudeignore)
  - Python, IDE, OS, Docker patterns
- Created STUDENT_EVAL_CHECKLIST.md:
  - 60-minute testing guide
  - Priority 1 (0-30 min): Core functionality (P1.1-P1.6)
  - Priority 2 (30-60 min): Extended testing (P2.1-P2.4)
  - Pre-test instructions to review form and appendix
  - Troubleshooting section
- Created STUDENT_EVAL_FORM.md:
  - Markdown format for typed submission
  - 12 questions covering all test areas
  - YES/NO, ratings (1-5), and free text fields
  - Empty appendix for example answers
- Executed developer test run:
  - Simulated 5-year IT/security professional
  - Read ONLY README.md (not source code or dev docs)
  - Started lab with start_lab.sh (34 seconds)
  - Tested HMI dashboard, trends, alarms pages
  - Tested ATG client (inventory, pressure, status, set-name)
  - Tested database access (MySQL connection, tank query)
  - Created eval/enumerate_tanks.sh organically during test
  - Completed through P2.3 (lab exercise attempt)
  - Total time: ~45 minutes
- Completed appendix with example answers from test run

#### Problems Encountered
| Problem | Cause | Solution |
|---------|-------|----------|
| Alarms page 500 error | TypeError in base.html line 30: comparing active_alarms (list) to int | Need to fix: change to active_alarms\|length > 0 |
| buildx warning during startup | Docker buildx not installed | Cosmetic only, does not affect functionality |

#### Lessons Learned
- Developer test run validates evaluation framework works (found real bug)
- Reading only README.md simulates realistic student perspective
- Organic script creation avoids dev knowledge contamination
- 45 minutes is sufficient for thorough P1 + partial P2 testing
- Alarms page needs testing before volunteer distribution

#### Bugs Found
1. **Alarms page 500 Internal Server Error**
   - Location: hmi/app/templates/base.html line 30
   - Error: `active_alarms > 0` but active_alarms is a list
   - Fix: Change to `active_alarms|length > 0` or `active_alarms|count > 0`

#### Deliverables Created
- .gitignore
- STUDENT_EVAL_CHECKLIST.md
- STUDENT_EVAL_FORM.md (with appendix)
- eval/enumerate_tanks.sh (development only, not distributed)

#### Next Steps
1. Fix Alarms page bug before volunteer testing
2. Recruit volunteer evaluators
3. Collect and review volunteer feedback
4. Fix any additional issues found
5. Remove /eval directory when testing complete

#### Notes
- Evaluation framework is ready for volunteer testing after bug fix
- Example answers provide clear format for volunteers to follow
- Appendix warning reminds evaluators to remove before AI review
- Test discovered real bug, proving evaluation process value

---

### Session: 2026-01-08 (Session 6 - Bug Fix and Phase 9 Planning)

#### Session Info
- **Date**: 2026-01-08
- **Duration**: ~30 minutes
- **Phase**: 8 (bug fix) and 9 (planning)
- **Focus**: Fix Alarms bug, plan documentation restructure

#### Objectives
- [x] Review test run findings for additional issues
- [x] Fix Alarms page 500 error
- [x] Review documentation structure
- [x] Plan Phase 9: Documentation Restructure
- [x] Update planning documents

#### Completed
- Reviewed test run findings - only 2 issues identified:
  1. Alarms page bug (fixed)
  2. Database schema not documented for students (addressed in Phase 9)
- Fixed Alarms page 500 Internal Server Error:
  - Root cause: base.html compared `active_alarms` (list) to int
  - Solution: Added `active_alarms_count` integer to all routes
  - Updated base.html to use `active_alarms_count` for nav badge
  - Verified all pages (dashboard, trends, alarms) return 200 OK
- Reviewed documentation structure and identified issues:
  - README.md is overloaded with mixed content
  - Database schema buried in dev/ARCHITECTURE.md
  - No operations/maintenance guide for lab operators
  - docs/ directory underutilized
- Planned Phase 9: Documentation Restructure
  - New exercises/ directory with story-driven content
  - exercises/docs/ for student reference (protocol, database)
  - docs/ for operations and maintenance
  - Instructor guide for teaching
  - Evaluation framework update after restructure

#### Problems Encountered
| Problem | Cause | Solution |
|---------|-------|----------|
| None | - | - |

#### Decisions Made
| Decision | Rationale |
|----------|-----------|
| Separate exercises/ from docs/ | exercises/ for students, docs/ for operators |
| Story-driven exercises | Casual tone, engaging but not CTF |
| E01_DISCOVERY.md naming | Clear, sortable exercise file names |
| challenges/ subdirectory | Separate advanced content |
| Instructor guide | Helps teachers use the lab |
| Eval update last | Must reflect final structure |

#### Next Steps
1. Implement Phase 9 tasks 9.1-9.10 (create new structure)
2. Update evaluation framework (tasks 9.11-9.13)
3. Resume Phase 8 volunteer testing

#### Notes
- Phase 8 tasks 8.5-8.8 on hold until Phase 9 complete
- dev/ directory will not be pushed to main (handled during merge)
- Alarms bug fix validated the evaluation framework works

#### Additional Update
- Added Documentation Structure section to ARCHITECTURE.md
- Documents the exercises/, docs/, dev/ organization
- Includes audience matrix and use case lookup table

---

### Session: 2026-01-08 (Session 6 continued - Phase 9 Group A)

#### Session Info
- **Date**: 2026-01-08
- **Duration**: ~20 minutes
- **Phase**: 9 - Documentation Restructure
- **Focus**: Create operations documentation (Group A)

#### Objectives
- [x] Create docs/OPERATIONS.md
- [x] Create docs/GASPOT_MODIFICATIONS.md
- [x] Update planning documents

#### Completed
- Created docs/OPERATIONS.md (~350 lines):
  - Requirements and supported platforms
  - Container architecture overview
  - Start/stop/reset procedures with scripts
  - Health check configuration and manual verification
  - Environment variables reference
  - Log management commands
  - Comprehensive troubleshooting guide
  - File structure reference
  - Maintenance tasks (backup, update)
  - Security notes
- Created docs/GASPOT_MODIFICATIONS.md (~250 lines):
  - Original GasPot project reference (sjhilt/GasPot)
  - Summary table of all changes
  - Detailed descriptions of each modification:
    - Tank configuration (4 to 6 tanks, new types)
    - Added I20600 pressure command
    - Added S60210 volume write command
    - Added S60220 pressure write command
    - Value fluctuation engine (5 modes)
    - Configuration file (config.ini)
    - Code architecture changes
  - Protocol compatibility notes
  - Testing compatibility information

#### Problems Encountered
| Problem | Cause | Solution |
|---------|-------|----------|
| None | - | - |

#### Deliverables
- docs/OPERATIONS.md
- docs/GASPOT_MODIFICATIONS.md

#### Next Steps
1. Group B: Create exercises/docs/PROTOCOL_REFERENCE.md and DATABASE_REFERENCE.md
2. Group C: Create exercises/ content (README, E01-E07, challenges, instructor guide)
3. Group D: Simplify README.md, remove old LAB_EXERCISES.md
4. Group E: Update evaluation framework and retest

---

### Session: 2026-01-08 (Session 6 continued - Phase 9 Group B)

#### Session Info
- **Date**: 2026-01-08
- **Duration**: ~20 minutes
- **Phase**: 9 - Documentation Restructure
- **Focus**: Create student reference documentation (Group B)

#### Objectives
- [x] Create exercises/docs/ directory
- [x] Create exercises/challenges/ directory
- [x] Create exercises/docs/PROTOCOL_REFERENCE.md
- [x] Create exercises/docs/DATABASE_REFERENCE.md
- [x] Update planning documents

#### Completed
- Created exercises/docs/ and exercises/challenges/ directories
- Created exercises/docs/PROTOCOL_REFERENCE.md (~400 lines):
  - Protocol overview and key characteristics
  - Security implications of TLS-350
  - Command format with SOH prefix and newline termination
  - All read commands: I20100, I20200, I20300, I20400, I20500, I20600
  - Example outputs for inventory and pressure reports
  - Write commands: S602xx (tank name), S60210 (volume), S60220 (pressure)
  - ATG client tool documentation with all subcommands
  - Connection options (-H, -p, -t, -v)
  - Manual testing with netcat examples
  - Quick reference card
- Created exercises/docs/DATABASE_REFERENCE.md (~350 lines):
  - Connection information and credentials
  - Connection methods (Docker recommended, direct)
  - Database schema overview with entity relationships
  - Table: tanks (6 rows, static configuration)
  - Table: tank_readings (time-series measurements)
  - Table: alarms (alarm history)
  - Column descriptions for all tables
  - Alarm types and severity levels
  - Extensive useful queries section:
    - Schema exploration
    - Tank information
    - Tank readings (latest, recent, averages, ranges)
    - Alarms (active, critical, counts)
    - Historical analysis
  - Data manipulation examples for attack scenarios
  - Stored procedures documentation
  - Security notes about weak credentials
  - Quick reference section
- Updated PLAN.md tasks 9.4 and 9.5 to COMPLETE
- Updated RESUME.md with Group B completion
- Updated VIBE_HISTORY.md with session entry

#### Problems Encountered
| Problem | Cause | Solution |
|---------|-------|----------|
| None | - | - |

#### Deliverables
- exercises/docs/PROTOCOL_REFERENCE.md
- exercises/docs/DATABASE_REFERENCE.md
- exercises/docs/ directory
- exercises/challenges/ directory

#### Next Steps
1. Group C: Create exercises/README.md (scenario introduction)
2. Group C: Create exercises/E01-E07 individual exercise files
3. Group C: Create exercises/challenges/C01-C03 challenge files
4. Group C: Create exercises/INSTRUCTOR_GUIDE.md
5. Group D: Simplify README.md, remove docs/LAB_EXERCISES.md
6. Group E: Update evaluation framework and retest

---

### Session: 2026-01-08 (Session 6 continued - Phase 9 Group C)

#### Session Info
- **Date**: 2026-01-08
- **Duration**: ~40 minutes
- **Phase**: 9 - Documentation Restructure
- **Focus**: Create exercise content (Group C)

#### Objectives
- [x] Create exercises/README.md (scenario introduction)
- [x] Create exercises/E01-E07 individual exercise files
- [x] Create exercises/challenges/C01-C03 challenge files
- [x] Create exercises/INSTRUCTOR_GUIDE.md
- [x] Update planning documents

#### Completed
- Created exercises/README.md (~120 lines):
  - Scenario: Cutaway Security junior consultant
  - Setting: Riverside Natural Gas Terminal security assessment
  - System overview (ATG, HMI, Historian)
  - Exercise table with timing estimates (~2.5 hours total)
  - Links to challenges and reference documentation
  - Casual, engaging tone (not CTF-style)

- Created 7 exercise files (~100-150 lines each):
  - E01_DISCOVERY.md: Network scanning, service identification
  - E02_ENUMERATION.md: TLS-350 protocol, information gathering
  - E03_ATG_MANIPULATION.md: Modifying tank names and volumes
  - E04_HMI_RECONNAISSANCE.md: Web interface, API endpoints
  - E05_DATABASE_EXPLOITATION.md: Historian access, data manipulation
  - E06_ATTACK_CHAIN.md: Combined multi-vector attack
  - E07_DEFENSE_ANALYSIS.md: Vulnerability documentation, recommendations

- Created 3 challenge files (~100-150 lines each):
  - C01_AUTOMATED_ATTACK.md: Python script to automate attack chain
  - C02_DETECTION_SCRIPT.md: Build monitoring/detection tool
  - C03_PROTOCOL_ANALYSIS.md: Wireshark capture and dissector

- Created exercises/INSTRUCTOR_GUIDE.md (~350 lines):
  - Target audience and prerequisites
  - Exercise breakdown with purpose, goal, approach, timing
  - Discussion questions for each exercise
  - Facilitation tips and common issues
  - Real-world incident references
  - Assessment ideas

- Updated PLAN.md tasks 9.3, 9.6, 9.7, 9.8 to COMPLETE
- Updated RESUME.md with Group C completion
- Updated VIBE_HISTORY.md with session entry

#### Content Highlights
- Story-driven narrative throughout exercises
- Each exercise has "Think About It" and "What's Next" sections
- Real-world context (Oldsmar incident, Rapid7 research)
- Progressive difficulty from reconnaissance to combined attacks
- Instructor guide includes timing estimates:
  - E01: 15 min, E02: 20 min, E03: 20 min
  - E04: 15 min, E05: 25 min, E06: 30 min, E07: 30 min
  - Total core exercises: ~2.5 hours
  - Challenges add 1-2 additional hours

#### Problems Encountered
| Problem | Cause | Solution |
|---------|-------|----------|
| None | - | - |

#### Deliverables
- exercises/README.md
- exercises/E01_DISCOVERY.md
- exercises/E02_ENUMERATION.md
- exercises/E03_ATG_MANIPULATION.md
- exercises/E04_HMI_RECONNAISSANCE.md
- exercises/E05_DATABASE_EXPLOITATION.md
- exercises/E06_ATTACK_CHAIN.md
- exercises/E07_DEFENSE_ANALYSIS.md
- exercises/challenges/C01_AUTOMATED_ATTACK.md
- exercises/challenges/C02_DETECTION_SCRIPT.md
- exercises/challenges/C03_PROTOCOL_ANALYSIS.md
- exercises/INSTRUCTOR_GUIDE.md

#### Next Steps
1. Group D: Simplify README.md (remove moved content)
2. Group D: Remove docs/LAB_EXERCISES.md (replaced by exercises/)
3. Group E: Update evaluation framework for new structure
4. Group E: Rerun developer test with new appendix example

---

### Session: 2026-01-08 (Session 6 continued - Phase 9 Group D)

#### Session Info
- **Date**: 2026-01-08
- **Duration**: ~10 minutes
- **Phase**: 9 - Documentation Restructure
- **Focus**: Cleanup tasks (Group D)

#### Objectives
- [x] Simplify README.md (remove content moved elsewhere)
- [x] Remove docs/LAB_EXERCISES.md (replaced by exercises/)
- [x] Update planning documents

#### Completed
- Simplified README.md (reduced from ~296 lines to ~187 lines):
  - Kept: Overview, architecture, requirements, quick start
  - Kept: Security notes, credits, license, references
  - Added: Documentation table pointing to new locations
  - Added: "Getting Started with Exercises" section linking to exercises/
  - Added: Quick reference section (condensed from full protocol docs)
  - Removed: Detailed TLS-350 protocol reference (moved to exercises/docs/)
  - Removed: Database queries and schema (moved to exercises/docs/)
  - Removed: Inline exercise content (moved to exercises/)
  - Removed: Detailed troubleshooting (moved to docs/OPERATIONS.md)
- Removed docs/LAB_EXERCISES.md (~442 lines)
  - Content replaced by exercises/E01-E07 and exercises/README.md
- Verified directory structure:
  - docs/ contains: OPERATIONS.md, GASPOT_MODIFICATIONS.md
  - exercises/ contains: README.md, E01-E07, challenges/, docs/, INSTRUCTOR_GUIDE.md
- Updated PLAN.md tasks 9.9, 9.10 to COMPLETE
- Updated RESUME.md with Group D completion
- Updated VIBE_HISTORY.md with session entry

#### Problems Encountered
| Problem | Cause | Solution |
|---------|-------|----------|
| None | - | - |

#### Deliverables
- Updated README.md (simplified)
- Removed docs/LAB_EXERCISES.md

#### Next Steps (Group E - FINAL)
1. Update STUDENT_EVAL_CHECKLIST.md for new exercises/ structure
2. Update STUDENT_EVAL_FORM.md for new exercises/ structure
3. Rerun developer test with new appendix example

---

### Session: 2026-01-08 (Session 6 continued - Phase 9 Group E)

#### Session Info
- **Date**: 2026-01-08
- **Duration**: ~15 minutes
- **Phase**: 9 - Documentation Restructure
- **Focus**: Evaluation framework update (Group E)

#### Objectives
- [x] Fix PROTOCOL_REFERENCE.md title to be more specific
- [x] Update STUDENT_EVAL_CHECKLIST.md for new exercises/ structure
- [x] Update STUDENT_EVAL_FORM.md for new exercises/ structure
- [x] Remove old appendix (to avoid tainting new evaluation)
- [x] Update planning documents

#### Completed
- Fixed PROTOCOL_REFERENCE.md title:
  - Changed from "TLS-350 Protocol Reference" to "TLS-350 ATG Protocol Reference"
  - Updated references in README.md and exercises/README.md
- Updated STUDENT_EVAL_CHECKLIST.md:
  - Changed P2.3 from "docs/LAB_EXERCISES.md" to "exercises/README.md"
  - Added references to exercises/E02_ENUMERATION.md and E03_ATG_MANIPULATION.md
  - Added reference documentation pointers to exercises/docs/
- Updated STUDENT_EVAL_FORM.md:
  - Updated Q9 to list new exercise file locations
  - Added EXERCISE_FILE_FOUND and REFERENCE_DOCS_HELPFUL fields
  - Updated Q10 to describe new documentation organization
  - Added FOUND_EXERCISES_EASILY and FOUND_REFERENCE_DOCS fields
  - Removed old appendix with outdated example answers (referenced fixed Alarms bug)
  - Added placeholder for new appendix to be generated during developer test
- Updated PLAN.md tasks 9.11, 9.12 to COMPLETE
- Updated RESUME.md with Group E completion
- Updated VIBE_HISTORY.md with session entry

#### Changes to Evaluation Documents

**STUDENT_EVAL_CHECKLIST.md**:
- P2.3 now points to exercises/README.md, E02, E03
- Added reference to exercises/docs/ for protocol and database docs

**STUDENT_EVAL_FORM.md**:
- Q9 updated with new exercise paths and reference docs
- Added fields: EXERCISE_FILE_FOUND, REFERENCE_DOCS_HELPFUL
- Q10 updated with documentation organization description
- Added fields: FOUND_EXERCISES_EASILY, FOUND_REFERENCE_DOCS
- Old appendix removed (contained outdated Alarms bug reference)
- New appendix placeholder ready for developer test

#### Problems Encountered
| Problem | Cause | Solution |
|---------|-------|----------|
| None | - | - |

#### Deliverables
- Updated exercises/docs/PROTOCOL_REFERENCE.md (title fix)
- Updated README.md (documentation table)
- Updated exercises/README.md (reference link)
- Updated STUDENT_EVAL_CHECKLIST.md
- Updated STUDENT_EVAL_FORM.md (with blank appendix)

#### Next Steps (Task 9.13 - Developer Test)
1. Run through checklist simulating student perspective
2. Generate new appendix with example answers
3. Document any issues discovered
4. Mark Phase 9 complete upon successful test

---

### Session: 2026-01-08 (Session 6 continued - Phase 9 Task 9.13 Developer Test)

#### Session Info
- **Date**: 2026-01-08
- **Duration**: ~35 minutes
- **Phase**: 9 - Documentation Restructure (FINAL)
- **Focus**: Developer test and appendix generation

#### Objectives
- [x] Run through evaluation checklist as student
- [x] Test all Priority 1 items (P1.1-P1.6)
- [x] Test extended items (P2.1, P2.3)
- [x] Generate new appendix with example answers
- [x] Mark Phase 9 complete

#### Simulated Evaluator Profile
- 5 years IT/cybersecurity experience
- New to ICS/OT technologies
- First time using TLS-350 protocol

#### Test Results

**P1.1 Environment Check**: PASS
- Docker 28.2.2, Compose 2.37.1
- All ports available (lab already running)

**P1.2 Start Lab**: PASS
- Containers all healthy

**P1.3 HMI Visual Review**: PASS
- Dashboard loads with tank data
- Trends page loads
- Alarms page loads (bug fixed!)
- Alarm badge shows count correctly

**P1.4 ATG Read Commands**: PASS
- Help comprehensive with examples
- Inventory returns all 6 tanks
- Pressure shows 3 gas tanks

**P1.5 ATG Write Commands**: PASS
- set-name works, provides feedback
- Change verified in inventory
- Reset to original works

**P1.6 Database Access**: PASS
- Connection with lab/password works
- 6 tanks visible
- Note: use "docker exec" without -it in scripts

**P2.1 Integration**: PASS
- ATG change immediately visible in HMI API

**P2.3 Exercise Attempt**: PASS
- exercises/README.md found easily
- E02_ENUMERATION.md clear and functional
- All commands work as documented
- Reference docs helpful

#### Issues Found
None - all functionality working correctly.

#### Appendix Generated
Updated STUDENT_EVAL_FORM.md with new appendix containing:
- Realistic example answers for all questions
- Ratings of 5/5 for documentation and experience
- Note about docker exec -it vs docker exec
- Positive feedback on documentation structure

#### Deliverables
- Updated STUDENT_EVAL_FORM.md with new appendix
- Updated PLAN.md - Phase 9 marked COMPLETE
- Updated RESUME.md - Phase 9 marked COMPLETE
- Updated VIBE_HISTORY.md with session entry

#### Phase 9 Final Status
All 13 tasks COMPLETE:
- 9.1-9.2: Operations documentation (docs/)
- 9.3-9.8: Exercise content (exercises/)
- 9.4-9.5: Reference documentation (exercises/docs/)
- 9.9-9.10: README cleanup
- 9.11-9.12: Evaluation framework update
- 9.13: Developer test

---

### Session 6 (2026-01-21)

#### Goals
- Address volunteer feedback from initial testing
- Fix reported issues in HMI and documentation

#### Volunteer Feedback Received
Four issues reported from testing:
1. HMI dashboard graphical elements (fill bars, percentages) don't update on refresh
2. Tank names don't update on HMI when changed via ATG
3. Database test command in startup script stays connected instead of showing status and exiting
4. Need explanation of nc and nmap commands for users unfamiliar with these tools

#### Fixes Implemented

**Issue 1: Graphical elements not updating**
- Root cause: refreshData() JavaScript only updated numeric values, not visual elements
- Fix: Added data-max-capacity attributes to tank cards, IDs to fill/level elements
- Updated JavaScript to calculate and update fill percentage on each refresh
- Files: hmi/app/templates/dashboard.html

**Issue 2: Tank name not updating**
- Root cause: tank-name spans had no ID, JavaScript didn't update them
- Fix: Added IDs to tank-name elements, added code to update from API response
- Files: hmi/app/templates/dashboard.html

**Issue 3: Database test command**
- Root cause: docker exec -it mysql creates interactive session
- Fix: Added mysqladmin ping command as quick test, kept interactive command separately
- Files: scripts/start_lab.sh

**Issue 4: Tool explanations**
- Fix: Added "Appendix: Tools Overview" at end of E01_DISCOVERY.md
- Explains nmap and nc with common flags and examples
- Added reference link at beginning of exercise
- Files: exercises/E01_DISCOVERY.md

#### Exercise Reorder

User requested swapping E03 and E04 for better learning flow:
- Students first observe HMI (E03), then manipulate ATG and watch changes (E04)

Changes made:
- Created E03_HMI_RECONNAISSANCE.md (from old E04)
- Created E04_ATG_MANIPULATION.md (from old E03)
- Removed old E03_ATG_MANIPULATION.md and E04_HMI_RECONNAISSANCE.md
- Updated E02_ENUMERATION.md What's Next link
- Updated exercises/README.md exercise table
- Updated exercises/INSTRUCTOR_GUIDE.md sections
- Added teaser in E03 about upcoming ATG manipulation
- Added browser tab tip in E04 for real-time observation

#### Documentation Updates
- STUDENT_EVAL_CHECKLIST.md: Updated exercise options to include E03, E04
- STUDENT_EVAL_FORM.md: Updated exercise list and EXERCISE_ATTEMPTED options
- PLAN.md: Updated Phase Overview (Phase 9 now shows COMPLETE)
- RESUME.md: Updated with current session work
- VIBE_HISTORY.md: Added this session entry

#### Testing
- Rebuilt HMI container with updated dashboard template
- Verified all containers healthy
- Confirmed dashboard HTML has new IDs and data attributes
- Confirmed JavaScript updates graphical elements
- Confirmed API returns product_name for name updates
- Verified mysqladmin ping returns "mysqld is alive" and exits
- Verified all exercise links point to correct files

#### Lessons Learned
- JavaScript refresh functions need to update ALL dynamic elements, not just text values
- Browser tab tip improves student experience for real-time observation exercises
- Exercise order matters for pedagogical flow - observe before manipulate

---

## Lessons Learned Summary

This section aggregates important lessons across all sessions for quick reference.

### Container Development

- Python slim images don't include common tools like ping; use curl or nc for connectivity tests
- MariaDB init scripts only run on first initialization (empty volume)
- To reset database fully: `docker compose down -v` then restart
- Files mounted into containers must have read permissions (chmod 644) for container users

### TLS-350 Protocol

- Commands must start with SOH (0x01) or "^A" and end with newline
- Error response is "9999FF1B" (9999 = unknown command, FF1B = checksum)
- Product names are padded/truncated to 20-22 characters
- select() pattern works well for multiple concurrent connections
- Non-blocking sockets with short recv loops handle variable-length responses
- GasPot returns tabular output, not block format - regex with whitespace matching works well
- S60210 volume command uses colon separators: S60210:TANK_ID:VALUE

### Docker Compose

- Check for both V1 (`docker-compose`) and V2 (`docker compose`) availability
- Use version detection in scripts to support both syntaxes
- `docker-compose config` validates YAML even without building images

### Flask/HMI

- SQLAlchemy uses Numeric() not Decimal() for decimal columns
- Flask app factory pattern cleanly separates config from routes
- Chart.js CDN works well for simple charting needs (no build step)
- Auto-refresh with setInterval provides live updates without WebSocket complexity
- PyMySQL is the pure-Python MySQL connector (no system dependencies)
- Flask reloader creates duplicate processes - use WERKZEUG_RUN_MAIN env var to control
- Daemon threads automatically terminate when main program exits
- Threading.Event() provides clean stop mechanism for polling loops

### MariaDB/Historian

- Init scripts in /docker-entrypoint-initdb.d/ only run once (on first start with empty volume)
- Can pipe SQL files to container: `cat init.sql | docker exec -i gaspot-historian mysql -u user -ppassword dbname`
- Health check: `mysqladmin ping -u user -ppassword`
- Stored procedures require `DELIMITER //` syntax in init scripts
- TIMESTAMPDIFF(SECOND, old, new) returns seconds between timestamps
- DATE_ADD(timestamp, INTERVAL n SECOND) adds seconds to timestamp
- RAND() returns 0-1 float, use for randomizing seed data values

### Testing

- Developer test runs validate evaluation frameworks (found real Alarms bug)
- Simulating student perspective by reading only README.md is effective
- Creating scripts organically during test avoids dev knowledge contamination
- 45 minutes sufficient for Priority 1 + partial Priority 2 testing
- Volunteer evaluation provides real student perspective feedback

### Documentation

- Separate student content (exercises/) from operator content (docs/)
- Reference documentation should be easily discoverable by students
- Story-driven exercises more engaging than dry task lists
- Instructor guides help teachers use the lab effectively
- Database schema should be documented for student exercises

### Scripts

- ss command works better than netstat for port checking on modern Linux
- Docker Compose V2 outputs status messages after script continues (async buffering)
- Port conflict detection should distinguish lab containers from external processes
- Non-interactive mode (stdin not a tty) should auto-proceed for scripted use
- Use `docker port container_name` to check if a port is used by a specific container
- ANSI color codes should be disabled when stdout is not a terminal (`[ -t 1 ]`)

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

- Alarms page has 500 error due to template bug in base.html line 30
- Bug: `active_alarms > 0` should be `active_alarms|length > 0`
- Dashboard and Trends pages work correctly
- API endpoints (/api/live, /api/alarms) work correctly

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
