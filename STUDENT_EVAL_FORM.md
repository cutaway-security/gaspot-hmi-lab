# GasPot HMI Lab - Student Evaluation Form

## Instructions

1. Fill out this form as you complete the STUDENT_EVAL_CHECKLIST.md
2. Type your answers directly in this file
3. Use the specified format for each question (YES/NO, ratings, free text)
4. You can submit at any time - partial evaluations are valuable
5. **Remove the Appendix before submitting for AI review**

---

## Evaluator Information

**Date**: [YYYY-MM-DD]
**Operating System**: [e.g., Kali 2024.1, Ubuntu 22.04]
**Docker Version**: [output of docker --version]
**Experience Level**: [years in IT/cybersecurity]
**Time Spent**: [total minutes, even if incomplete]
**Completed Through**: [P1.1 / P1.2 / ... / P2.4]

---

## Priority 1: Core Functionality

### Q1: Prerequisites Check
Were all prerequisites met? (Docker, Docker Compose, ports available)

- PREREQUISITES_MET: [YES/NO]
- DOCKER_VERSION: [version string]
- COMPOSE_VERSION: [version string]
- PORT_CONFLICTS: [NONE / list any conflicts]
- ISSUES: [describe any issues or leave blank]

---

### Q2: Startup Script
Did start_lab.sh complete successfully?

- STARTUP_SUCCESS: [YES/NO]
- STARTUP_TIME: [approximate seconds to complete]
- ERRORS_DISPLAYED: [NONE / describe errors]
- WARNINGS_DISPLAYED: [NONE / describe warnings]
- ACCESS_INFO_CLEAR: [YES/NO] (did it show how to access the lab?)
- ISSUES: [describe any issues or leave blank]

---

### Q3: HMI Dashboard Visual Review
Did the web interface load and display correctly?

- DASHBOARD_LOADS: [YES/NO/PARTIAL]
- TRENDS_LOADS: [YES/NO/PARTIAL]
- ALARMS_LOADS: [YES/NO/PARTIAL]
- TANK_DATA_VISIBLE: [YES/NO] (can you see volume, temperature values?)
- LAYOUT_CORRECT: [YES/NO/PARTIAL]
- VISUAL_ISSUES: [describe any visual problems or leave blank]

---

### Q4: ATG Client Read Commands
Did the ATG client read commands work?

- HELP_WORKS: [YES/NO]
- INVENTORY_WORKS: [YES/NO]
- PRESSURE_WORKS: [YES/NO]
- OUTPUT_READABLE: [YES/NO] (is the output format clear?)
- COMMAND_ERRORS: [NONE / describe errors]
- ISSUES: [describe any issues or leave blank]

---

### Q5: ATG Client Write Commands
Did the ATG client write commands work?

- SET_NAME_WORKS: [YES/NO]
- CHANGE_VERIFIED: [YES/NO] (did inventory show the new name?)
- RESET_WORKS: [YES/NO] (could you restore original name?)
- COMMAND_ERRORS: [NONE / describe errors]
- ISSUES: [describe any issues or leave blank]

---

### Q6: Database Access
Did direct database access work?

- CONNECTION_WORKS: [YES/NO]
- QUERY_WORKS: [YES/NO]
- SIX_TANKS_VISIBLE: [YES/NO]
- CONNECTION_ERRORS: [NONE / describe errors]
- ISSUES: [describe any issues or leave blank]

---

## Priority 2: Extended Testing

### Q7: Integration Check
Did ATG changes appear in the HMI?

- COMPLETED: [YES/NO/SKIPPED]
- CHANGE_VISIBLE_IN_HMI: [YES/NO/NA]
- REFRESH_REQUIRED: [YES/NO/NA] (did you need to refresh the browser?)
- ISSUES: [describe any issues or leave blank]

---

### Q8: Lifecycle Scripts
Did stop and restart scripts work?

- COMPLETED: [YES/NO/SKIPPED]
- STOP_WORKS: [YES/NO/NA]
- CONTAINERS_STOPPED: [YES/NO/NA]
- RESTART_WORKS: [YES/NO/NA]
- HMI_ACCESSIBLE_AFTER_RESTART: [YES/NO/NA]
- ISSUES: [describe any issues or leave blank]

---

### Q9: Lab Exercise Attempt
Were the lab exercises clear and functional?

Exercises are located in the **exercises/** directory:
- exercises/README.md - Overview and scenario introduction
- exercises/E02_ENUMERATION.md - Protocol enumeration
- exercises/E03_ATG_MANIPULATION.md - ATG data manipulation

Reference documentation:
- exercises/docs/PROTOCOL_REFERENCE.md - TLS-350 ATG protocol
- exercises/docs/DATABASE_REFERENCE.md - Database schema and queries

- COMPLETED: [YES/NO/SKIPPED]
- EXERCISE_ATTEMPTED: [E02 / E03 / other / NA]
- EXERCISE_FILE_FOUND: [YES/NO/NA] (could you find the exercise?)
- INSTRUCTIONS_CLEAR: [YES/NO/PARTIAL/NA]
- EXERCISE_WORKED: [YES/NO/PARTIAL/NA]
- REFERENCE_DOCS_HELPFUL: [YES/NO/NA] (if you used them)
- CONFUSION_POINTS: [describe any confusing parts or leave blank]
- ISSUES: [describe any issues or leave blank]

---

## Overall Assessment

### Q10: Documentation Quality
Rate the quality of the documentation.

Documentation is organized as:
- README.md - Quick start and overview
- exercises/ - Student exercises and reference docs
- docs/ - Operations and maintenance

- RATING: [1-5] (1=poor, 5=excellent)
- FOUND_EXERCISES_EASILY: [YES/NO]
- FOUND_REFERENCE_DOCS: [YES/NO]
- MISSING_INFO: [describe anything missing or leave blank]
- CONFUSING_SECTIONS: [describe any confusing parts or leave blank]

---

### Q11: Overall Lab Experience
Rate the overall lab experience.

- RATING: [1-5] (1=poor, 5=excellent)
- BEST_ASPECTS: [what worked well]
- WORST_ASPECTS: [what needs improvement]
- WOULD_RECOMMEND: [YES/NO]

---

### Q12: Specific Feedback
Any additional comments or suggestions?

- BUGS_FOUND: [describe any bugs or leave blank]
- FEATURE_REQUESTS: [describe any desired features or leave blank]
- OTHER_COMMENTS: [any other feedback]

---

## Submission

1. Save this file
2. **Remove the Appendix section below** before submitting for AI review
3. Submit as instructed by the lab maintainers

---
---

## APPENDIX: Example Answers

**WARNING**: This appendix contains example answers created during developer testing. **DO NOT include this appendix when submitting your evaluation for AI review**, as it may bias the analysis.

Human volunteers should answer in their own words based on their actual experience.

**REMOVE THIS ENTIRE APPENDIX SECTION BEFORE SUBMISSION FOR AI REVIEW.**

---

### Example Evaluator Information

**Date**: 2026-01-08
**Operating System**: Ubuntu 25.10
**Docker Version**: Docker version 28.2.2, build 28.2.2-0ubuntu1
**Experience Level**: 5 years IT/cybersecurity, new to ICS/OT
**Time Spent**: 35 minutes
**Completed Through**: P2.3

---

### Example Q1: Prerequisites Check

- PREREQUISITES_MET: YES
- DOCKER_VERSION: Docker version 28.2.2, build 28.2.2-0ubuntu1
- COMPOSE_VERSION: Docker Compose version 2.37.1+ds1-0ubuntu2
- PORT_CONFLICTS: NONE (lab was already running from previous session)
- ISSUES:

---

### Example Q2: Startup Script

- STARTUP_SUCCESS: YES
- STARTUP_TIME: N/A (containers already running)
- ERRORS_DISPLAYED: NONE
- WARNINGS_DISPLAYED: NONE
- ACCESS_INFO_CLEAR: YES
- ISSUES:

---

### Example Q3: HMI Dashboard Visual Review

- DASHBOARD_LOADS: YES
- TRENDS_LOADS: YES
- ALARMS_LOADS: YES
- TANK_DATA_VISIBLE: YES
- LAYOUT_CORRECT: YES
- VISUAL_ISSUES: None - all pages load correctly, alarm badge shows count in nav bar

---

### Example Q4: ATG Client Read Commands

- HELP_WORKS: YES
- INVENTORY_WORKS: YES
- PRESSURE_WORKS: YES
- OUTPUT_READABLE: YES
- COMMAND_ERRORS: NONE
- ISSUES: Help text is comprehensive, shows all commands with examples

---

### Example Q5: ATG Client Write Commands

- SET_NAME_WORKS: YES
- CHANGE_VERIFIED: YES
- RESET_WORKS: YES
- COMMAND_ERRORS: NONE
- ISSUES: Commands provide feedback ("Tank 1 name set to: EVAL-TEST")

---

### Example Q6: Database Access

- CONNECTION_WORKS: YES
- QUERY_WORKS: YES
- SIX_TANKS_VISIBLE: YES
- CONNECTION_ERRORS: NONE
- ISSUES: Note - "docker exec -it" fails in non-TTY environments, use "docker exec" without -it for scripts

---

### Example Q7: Integration Check

- COMPLETED: YES
- CHANGE_VISIBLE_IN_HMI: YES
- REFRESH_REQUIRED: NO (API showed change immediately)
- ISSUES:

---

### Example Q8: Lifecycle Scripts

- COMPLETED: SKIPPED
- STOP_WORKS: NA
- CONTAINERS_STOPPED: NA
- RESTART_WORKS: NA
- HMI_ACCESSIBLE_AFTER_RESTART: NA
- ISSUES: Skipped to preserve running lab state

---

### Example Q9: Lab Exercise Attempt

- COMPLETED: YES
- EXERCISE_ATTEMPTED: E02
- EXERCISE_FILE_FOUND: YES
- INSTRUCTIONS_CLEAR: YES
- EXERCISE_WORKED: YES
- REFERENCE_DOCS_HELPFUL: YES
- CONFUSION_POINTS: None - exercise was well-structured with clear steps
- ISSUES: All commands in exercise worked as documented. Verbose mode (-v) shows protocol details which is educational.

---

### Example Q10: Documentation Quality

- RATING: 5
- FOUND_EXERCISES_EASILY: YES
- FOUND_REFERENCE_DOCS: YES
- MISSING_INFO: None - documentation is comprehensive
- CONFUSING_SECTIONS: None

---

### Example Q11: Overall Lab Experience

- RATING: 5
- BEST_ASPECTS: Clean documentation structure, exercises build logically, ATG client tool is intuitive, scenario narrative is engaging without being gimmicky
- WORST_ASPECTS: None identified in this test
- WOULD_RECOMMEND: YES

---

### Example Q12: Specific Feedback

- BUGS_FOUND: None
- FEATURE_REQUESTS: None
- OTHER_COMMENTS: As someone new to ICS/OT, the lab provides good hands-on exposure to industrial protocols. The casual tone in exercises makes it approachable without being CTF-style. Reference documentation in exercises/docs/ is comprehensive and easy to find.

---

**END OF APPENDIX - REMOVE BEFORE SUBMISSION**
