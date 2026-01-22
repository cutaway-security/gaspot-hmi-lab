# GasPot HMI Lab - Student Evaluation Checklist

## Purpose

This checklist guides volunteer evaluators through testing the GasPot HMI Lab. Your feedback helps improve the lab experience for future students.

**Estimated Time**: 60 minutes total
**Priority 1** (0-30 min): Core functionality - complete these first
**Priority 2** (30-60 min): Extended testing - complete if time permits

---

## Before You Start

1. **Read STUDENT_EVAL_FORM.md completely** - Understand what feedback is needed
2. **Read the Appendix in STUDENT_EVAL_FORM.md** - See example answer format and depth
3. **Open STUDENT_EVAL_FORM.md in a text editor** - You will type answers as you go
4. **You can submit at any time** - Partial evaluations are valuable

### Requirements

- Linux system (Kali, Ubuntu, or similar)
- Docker and Docker Compose installed
- Web browser
- Terminal access
- Text editor for the eval form

---

## Priority 1: Core Functionality (0-30 minutes)

Complete these tests first. These validate the most critical functionality.

### P1.1 Environment Check (0-5 minutes)

**Goal**: Verify your system can run the lab.

1. Open a terminal
2. Run: `docker --version`
3. Run: `docker compose version`
4. Check that ports 5000, 10001, and 3306 are not in use:
   ```bash
   ss -tuln | grep -E '5000|10001|3306'
   ```
5. **Record in eval form**: Q1 (prerequisites)

### P1.2 Start the Lab (5-10 minutes)

**Goal**: Validate the startup script works correctly.

1. Navigate to the lab directory
2. Read the README.md file (this is your primary documentation)
3. Run the startup script:
   ```bash
   ./scripts/start_lab.sh
   ```
4. Wait for the script to complete
5. Note any errors or warnings displayed
6. **Record in eval form**: Q2 (startup script)

### P1.3 HMI Dashboard - Visual Review (10-15 minutes)

**Goal**: Verify the web interface loads and displays correctly.

1. Open a web browser
2. Navigate to: http://localhost:5000
3. Check the main Dashboard page:
   - Do tank cards display?
   - Are values visible (volume, temperature)?
   - Is the page layout correct?
4. Click on "Trends" - does the page load?
5. Click on "Alarms" - does the page load?
6. **Record in eval form**: Q3 (HMI visual review)

### P1.4 ATG Client Tool - Basic Commands (15-20 minutes)

**Goal**: Verify the ATG client tool works.

1. In terminal, run:
   ```bash
   python3 tools/atg_client.py --help
   ```
2. Get tank inventory:
   ```bash
   python3 tools/atg_client.py inventory
   ```
3. Get pressure readings:
   ```bash
   python3 tools/atg_client.py pressure
   ```
4. Note if output appears correct and readable
5. **Record in eval form**: Q4 (ATG client read commands)

### P1.5 ATG Client Tool - Write Commands (20-25 minutes)

**Goal**: Verify data manipulation works.

1. Note the current name of Tank 1 from the inventory output
2. Change the tank name:
   ```bash
   python3 tools/atg_client.py set-name 1 "EVAL-TEST"
   ```
3. Verify the change:
   ```bash
   python3 tools/atg_client.py inventory
   ```
4. Check if Tank 1 now shows "EVAL-TEST"
5. Reset the name (use original name from step 1):
   ```bash
   python3 tools/atg_client.py set-name 1 "NG-MAIN"
   ```
6. **Record in eval form**: Q5 (ATG client write commands)

### P1.6 Database Access (25-30 minutes)

**Goal**: Verify direct database access works.

1. Connect to the database:
   ```bash
   docker exec -it gaspot-historian mysql -u lab -ppassword historian
   ```
2. Run a query:
   ```sql
   SELECT * FROM tanks;
   ```
3. Verify 6 tanks are displayed
4. Exit the database:
   ```sql
   exit
   ```
5. **Record in eval form**: Q6 (database access)

---

## Priority 2: Extended Testing (30-60 minutes)

Complete these if time permits. These validate integration and usability.

### P2.1 Integration Check (30-35 minutes)

**Goal**: Verify changes in ATG appear in HMI.

1. Change a tank name via ATG client:
   ```bash
   python3 tools/atg_client.py set-name 2 "MODIFIED"
   ```
2. Refresh the HMI dashboard in your browser
3. Check if Tank 2 shows the new name
4. Reset the name:
   ```bash
   python3 tools/atg_client.py set-name 2 "NG-RESERVE"
   ```
5. **Record in eval form**: Q7 (integration)

### P2.2 Stop and Reset Scripts (35-40 minutes)

**Goal**: Verify lifecycle scripts work.

1. Stop the lab:
   ```bash
   ./scripts/stop_lab.sh
   ```
2. Verify containers stopped:
   ```bash
   docker ps
   ```
3. Restart the lab:
   ```bash
   ./scripts/start_lab.sh
   ```
4. Verify the HMI is accessible again at http://localhost:5000
5. **Record in eval form**: Q8 (lifecycle scripts)

### P2.3 Lab Exercise Attempt (40-55 minutes)

**Goal**: Validate lab exercises are clear and functional.

1. Open **exercises/README.md** to see the exercise overview
2. Choose one exercise to attempt:
   - **exercises/E02_ENUMERATION.md** (Protocol Enumeration) OR
   - **exercises/E03_HMI_RECONNAISSANCE.md** (HMI Reconnaissance) OR
   - **exercises/E04_ATG_MANIPULATION.md** (ATG Data Manipulation)
3. Follow the exercise instructions
4. Note any confusion, errors, or unclear instructions
5. **Record in eval form**: Q9 (lab exercises)

**Reference documentation** (if needed):
- exercises/docs/PROTOCOL_REFERENCE.md - TLS-350 ATG protocol commands
- exercises/docs/DATABASE_REFERENCE.md - Database schema and queries

### P2.4 Final Review (55-60 minutes)

**Goal**: Capture overall impressions.

1. Review your eval form - fill in any skipped questions
2. Complete Q10-Q12 (overall ratings and comments)
3. Save the eval form
4. Stop the lab if still running:
   ```bash
   ./scripts/stop_lab.sh
   ```

---

## After Testing

1. **Save your completed STUDENT_EVAL_FORM.md**
2. **Remove the Appendix** from your form before submission for AI review
3. **Submit your evaluation** as instructed by the lab maintainers

---

## Troubleshooting During Testing

### Containers won't start
```bash
# Check for port conflicts
ss -tuln | grep -E '5000|10001|3306'

# Check Docker status
docker info

# View logs
docker compose logs
```

### ATG client errors
```bash
# Check if GasPot is running
nc -zv localhost 10001

# Try verbose mode
python3 tools/atg_client.py -v inventory
```

### Database connection fails
```bash
# Check if container is running
docker ps | grep historian

# Check container logs
docker logs gaspot-historian
```

---

## Thank You

Your feedback is valuable for improving this lab. Even partial evaluations help identify issues and areas for improvement.
