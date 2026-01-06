# RESUME.md - Development Status and Session Context

## Purpose

This document provides context for resuming development after a break or when starting a new Claude Code session. It mirrors the PLAN.md structure but includes additional session-specific context.

**Last Updated**: Not yet started

---

## Current State

### Active Phase

**Phase**: 1 - Foundation
**Status**: NOT STARTED

### Current Task

**Task**: None - Development not yet started

### Blockers

None identified.

### Open Questions

None.

---

## Session Context

### Previous Session Summary

No previous sessions.

### What Was Being Worked On

Nothing - project initialization.

### What Needs To Happen Next

1. Read all documentation (CLAUDE.md, ARCHITECTURE.md, PLAN.md, VIBE_HISTORY.md)
2. Confirm understanding of project structure
3. Begin Phase 1: Foundation
4. Create directory structure
5. Create docker-compose.yml skeleton

### Environment State

- Containers: Not created
- Database: Not initialized
- GasPot: Not implemented
- HMI: Not implemented
- Scripts: Not created

---

## Phase Status Mirror

This section mirrors PLAN.md for quick reference during session startup.

### Phase 1: Foundation - NOT STARTED

| # | Task | Status |
|---|------|--------|
| 1.1 | Create directory structure | NOT STARTED |
| 1.2 | Create docker-compose.yml skeleton | NOT STARTED |
| 1.3 | Create .env.example | NOT STARTED |
| 1.4 | Validate Docker Compose runs | NOT STARTED |
| 1.5 | Test network connectivity between containers | NOT STARTED |

### Phase 2: GasPot Simulator - NOT STARTED

| # | Task | Status |
|---|------|--------|
| 2.1 | Create gaspot/Dockerfile | NOT STARTED |
| 2.2 | Create gaspot/requirements.txt | NOT STARTED |
| 2.3 | Create gaspot/config.ini | NOT STARTED |
| 2.4 | Implement GasPot.py base | NOT STARTED |
| 2.5 | Implement I20100 (inventory) | NOT STARTED |
| 2.6 | Implement I20200-I20500 | NOT STARTED |
| 2.7 | Implement I20600 (pressure) | NOT STARTED |
| 2.8 | Implement S602xx (writes) | NOT STARTED |
| 2.9 | Implement fluctuation engine | NOT STARTED |
| 2.10 | Test with telnet | NOT STARTED |
| 2.11 | Test with netcat | NOT STARTED |

### Phase 3: Historian Database - NOT STARTED

| # | Task | Status |
|---|------|--------|
| 3.1 | Create historian/init.sql | NOT STARTED |
| 3.2 | Add tanks table with 6 tank config | NOT STARTED |
| 3.3 | Add tank_readings table | NOT STARTED |
| 3.4 | Add alarms table | NOT STARTED |
| 3.5 | Create update_timestamps procedure | NOT STARTED |
| 3.6 | Add seed data (24 hours history) | NOT STARTED |
| 3.7 | Add sample alarms | NOT STARTED |
| 3.8 | Test container starts | NOT STARTED |
| 3.9 | Test queries work | NOT STARTED |
| 3.10 | Test stored procedure | NOT STARTED |

### Phase 4: HMI Application - NOT STARTED

| # | Task | Status |
|---|------|--------|
| 4.1 | Create hmi/Dockerfile | NOT STARTED |
| 4.2 | Create hmi/requirements.txt | NOT STARTED |
| 4.3 | Create hmi/app/__init__.py | NOT STARTED |
| 4.4 | Create hmi/app/atg_client.py | NOT STARTED |
| 4.5 | Test atg_client.py standalone | NOT STARTED |
| 4.6 | Create hmi/app/models.py | NOT STARTED |
| 4.7 | Create hmi/app/routes.py | NOT STARTED |
| 4.8 | Create /health endpoint | NOT STARTED |
| 4.9 | Create main dashboard template | NOT STARTED |
| 4.10 | Create trends template | NOT STARTED |
| 4.11 | Create alarms template | NOT STARTED |
| 4.12 | Add static CSS | NOT STARTED |
| 4.13 | Test container builds | NOT STARTED |
| 4.14 | Test health endpoint | NOT STARTED |
| 4.15 | Test dashboard loads | NOT STARTED |

### Phase 5: Integration - NOT STARTED

| # | Task | Status |
|---|------|--------|
| 5.1 | Implement HMI polling loop | NOT STARTED |
| 5.2 | Store readings to historian | NOT STARTED |
| 5.3 | Test full data flow | NOT STARTED |
| 5.4 | Test student write to GasPot | NOT STARTED |
| 5.5 | Test student write to DB | NOT STARTED |
| 5.6 | Verify container restart recovery | NOT STARTED |
| 5.7 | Test with docker compose up/down cycles | NOT STARTED |

### Phase 6: Scripts - NOT STARTED

| # | Task | Status |
|---|------|--------|
| 6.1 | Create scripts/start_lab.sh | NOT STARTED |
| 6.2 | Create scripts/stop_lab.sh | NOT STARTED |
| 6.3 | Create scripts/reset_lab.sh | NOT STARTED |
| 6.4 | Test start_lab.sh on clean system | NOT STARTED |
| 6.5 | Test start_lab.sh with existing containers | NOT STARTED |
| 6.6 | Test start_lab.sh with port conflict | NOT STARTED |
| 6.7 | Test stop_lab.sh | NOT STARTED |
| 6.8 | Test reset_lab.sh | NOT STARTED |
| 6.9 | Test scripts with V1 compose | NOT STARTED |
| 6.10 | Test scripts with V2 compose | NOT STARTED |

### Phase 7: Student Tools - NOT STARTED

| # | Task | Status |
|---|------|--------|
| 7.1 | Create tools/atg_client.py | NOT STARTED |
| 7.2 | Implement --help | NOT STARTED |
| 7.3 | Implement inventory command | NOT STARTED |
| 7.4 | Implement pressure command | NOT STARTED |
| 7.5 | Implement set-name command | NOT STARTED |
| 7.6 | Implement set-volume command | NOT STARTED |
| 7.7 | Implement raw command | NOT STARTED |
| 7.8 | Test all commands | NOT STARTED |
| 7.9 | Create README.md | NOT STARTED |
| 7.10 | Create lab exercise guide | NOT STARTED |

### Phase 8: Testing - NOT STARTED

| # | Task | Status |
|---|------|--------|
| 8.1 | Test on Kali Linux VM | NOT STARTED |
| 8.2 | Test start_lab.sh | NOT STARTED |
| 8.3 | Test telnet interaction | NOT STARTED |
| 8.4 | Test nmap NSE script | NOT STARTED |
| 8.5 | Test Metasploit module | NOT STARTED |
| 8.6 | Test atg_client.py | NOT STARTED |
| 8.7 | Test HMI in browser | NOT STARTED |
| 8.8 | Test mysql client | NOT STARTED |
| 8.9 | Run full student exercise flow | NOT STARTED |
| 8.10 | Document any issues | NOT STARTED |

---

## Known Issues

None yet.

---

## Files Created

None yet.

---

## Files Modified

None yet.

---

## Testing Notes

None yet.

---

## Decisions Made

| Date | Decision | Rationale |
|------|----------|-----------|
| - | Use 6 tanks (3 NG, 2 Diesel, 1 Water) | Realistic facility simulation |
| - | HMI polls GasPot (Option A) | Cleaner separation of concerns |
| - | Use weak passwords (password, admin) | Student lab environment |
| - | Support both Compose V1 and V2 | Student environment compatibility |

---

## Quick Commands

```bash
# Check container status
docker compose ps

# View all logs
docker compose logs -f

# Test GasPot
echo -e '\x01I20100\n' | nc localhost 10001

# Test HMI
curl http://localhost:5000/health

# Test MariaDB
docker exec gaspot-historian mysql -u lab -ppassword historian -e "SELECT * FROM tanks;"

# Restart all containers
docker compose restart

# Full reset
docker compose down -v
```

---

## Next Session Checklist

When starting next session:

1. [ ] Read CLAUDE.md
2. [ ] Read ARCHITECTURE.md
3. [ ] Read PLAN.md
4. [ ] Read this file (RESUME.md)
5. [ ] Read VIBE_HISTORY.md
6. [ ] State understanding of current status
7. [ ] List proposed next steps
8. [ ] Wait for confirmation before proceeding
