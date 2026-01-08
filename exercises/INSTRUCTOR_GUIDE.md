# Instructor Guide

## Overview

This guide helps instructors use the GasPot HMI Lab effectively in training environments. It covers learning objectives, timing, facilitation tips, and discussion points for each exercise.

---

## Course Design

### Target Audience

- Security professionals learning ICS/OT security
- IT staff transitioning to OT security roles
- Penetration testers expanding to industrial systems
- Students in cybersecurity programs

### Prerequisites

Students should have:
- Basic networking knowledge (TCP/IP, ports, services)
- Familiarity with Linux command line
- Basic understanding of web applications
- SQL fundamentals helpful but not required

### Total Time

| Component | Duration |
|-----------|----------|
| Setup and Introduction | 15 min |
| Core Exercises (E01-E07) | 2.5 hours |
| Discussion and Wrap-up | 15 min |
| **Total** | **~3 hours** |

Challenge exercises add 1-2 additional hours for advanced students.

---

## Environment Setup

### Before Class

1. Test the lab environment on your teaching system:
   ```bash
   ./scripts/start_lab.sh
   ```

2. Verify all services are accessible:
   - HMI: http://localhost:5000
   - ATG: `nc -zv localhost 10001`
   - Database: `docker exec gaspot-historian mysqladmin ping -u lab -ppassword`

3. Pre-download Docker images to avoid classroom network issues:
   ```bash
   docker compose pull
   ```

### Deployment Options

**Individual Labs**: Each student runs their own instance
- Pros: Full isolation, no conflicts
- Cons: Requires Docker on each machine

**Shared Instance**: One lab accessible to all students
- Pros: Simple setup, demonstrates shared access risks
- Cons: Students may interfere with each other's exercises

**Virtual Machines**: Pre-built VMs with lab installed
- Pros: Consistent environment, easy distribution
- Cons: Larger download, more resources needed

### Network Considerations

If students access a shared instance over the network, update the ATG client:
```bash
python3 tools/atg_client.py -H <server-ip> inventory
```

---

## Exercise Breakdown

### E01: Network Discovery

**Purpose**: Introduce students to ICS service identification.

**Goal**: Students successfully identify ATG, HMI, and database services.

**Approach**:
- Use nmap for service scanning
- Verify connectivity with netcat
- Research TLS-350 protocol background

**Time**: 15 minutes

**Key Points**:
- ICS services often use non-standard ports
- Many industrial protocols predate security considerations
- Service banners may reveal device types

**Discussion Questions**:
- What would a full network scan look like in a real facility?
- How would you find these services on a Class B network?
- What risks come with scanning production ICS networks?

---

### E02: Protocol Enumeration

**Purpose**: Teach the TLS-350 protocol and information gathering.

**Goal**: Students enumerate all tanks and document facility configuration.

**Approach**:
- Send raw protocol commands with netcat
- Use the ATG client tool for easier interaction
- Document findings in a structured format

**Time**: 20 minutes

**Key Points**:
- Protocol requires no authentication
- Significant operational data exposed
- All queries are indistinguishable from normal operations

**Discussion Questions**:
- What could an attacker learn from this information?
- How might this data be used for a targeted attack?
- Would this enumeration be logged anywhere?

---

### E03: ATG Manipulation

**Purpose**: Demonstrate write capabilities and operational impact.

**Goal**: Students successfully modify tank names and volumes.

**Approach**:
- Modify tank names via protocol
- Change volume readings
- Observe changes in HMI

**Time**: 20 minutes

**Key Points**:
- Write commands require no additional privileges
- Changes take effect immediately
- No audit trail of modifications

**Discussion Questions**:
- What real-world decisions might operators make based on false data?
- Could this cause safety incidents?
- How would you verify ATG data integrity?

**Safety Discussion**: This is a good time to discuss the Oldsmar water treatment incident (2021) where an attacker modified chemical levels through remote access.

---

### E04: HMI Reconnaissance

**Purpose**: Explore web-based HMI vulnerabilities.

**Goal**: Students identify API endpoints and information disclosure.

**Approach**:
- Browse the HMI interface
- Use browser developer tools
- Query API endpoints directly

**Time**: 15 minutes

**Key Points**:
- Modern HMIs are web applications with web vulnerabilities
- APIs often lack authentication
- Developer tools reveal application architecture

**Discussion Questions**:
- What traditional web vulnerabilities might apply to HMIs?
- How is HMI security different from typical web security?
- What data would you monitor if you had persistent API access?

---

### E05: Database Exploitation

**Purpose**: Demonstrate historian database risks and manipulation.

**Goal**: Students access the database and modify historical data.

**Approach**:
- Connect with weak credentials
- Query operational data
- Modify readings and inject alarms

**Time**: 25 minutes

**Key Points**:
- Historian databases contain valuable operational intelligence
- Historical data manipulation can hide incidents
- False alarms can cause operational disruption

**Discussion Questions**:
- How might database access differ from ATG access in terms of impact?
- What would forensic analysis reveal after these modifications?
- How could database integrity be protected?

---

### E06: Attack Chain

**Purpose**: Combine techniques into a realistic attack scenario.

**Goal**: Students execute a coordinated multi-vector attack.

**Approach**:
- Follow attack phases sequentially
- Document timeline and actions
- Observe cumulative impact

**Time**: 30 minutes

**Key Points**:
- Real attacks combine multiple techniques
- Sequencing matters for impact and stealth
- Coordinated attacks are harder to detect and respond to

**Discussion Questions**:
- How would incident responders untangle this attack?
- What was the single most impactful action?
- Where were the best opportunities for detection?

---

### E07: Defense Analysis

**Purpose**: Transition from offensive to defensive thinking.

**Goal**: Students document vulnerabilities and propose mitigations.

**Approach**:
- Systematic vulnerability cataloging
- Risk assessment
- Control mapping and prioritization

**Time**: 30 minutes

**Key Points**:
- Assessment findings need actionable recommendations
- Prioritization is critical for resource-limited environments
- ICS security requires balancing security with operational requirements

**Discussion Questions**:
- Which vulnerabilities are most critical to address?
- What quick wins could be implemented immediately?
- How do you communicate these findings to non-technical stakeholders?

---

## Challenge Exercises

### C01: Automated Attack Script

**Purpose**: Apply programming skills to security automation.

**Appropriate For**: Students with Python experience.

**Time**: 45-60 minutes

**Discussion**: Compare student implementations. Discuss detection opportunities created by automation.

### C02: Detection Script

**Purpose**: Build defensive monitoring capabilities.

**Appropriate For**: Students interested in defensive security.

**Time**: 45-60 minutes

**Discussion**: Have students attack each other's monitors. What alerts triggered? What was missed?

### C03: Protocol Analysis

**Purpose**: Deep protocol reverse engineering.

**Appropriate For**: Advanced students, those interested in research.

**Time**: 60-90 minutes

**Discussion**: Compare documented protocol to actual Veeder-Root specifications.

---

## Facilitation Tips

### Pacing

- Start with a brief demo of the HMI dashboard to orient students
- Allow struggling students to work with partners
- Have fast finishers help others or start challenge exercises

### Common Issues

| Issue | Solution |
|-------|----------|
| Docker not starting | Check Docker daemon: `systemctl status docker` |
| Port already in use | Stop other services or use `./scripts/stop_lab.sh` |
| Database connection fails | Wait for container health check or restart |
| ATG not responding | Verify container status: `docker compose ps` |

### Lab Reset

Between sessions or if things go wrong:
```bash
./scripts/reset_lab.sh
./scripts/start_lab.sh
```

---

## Discussion Topics

### ICS vs IT Security

- Availability often prioritized over confidentiality
- Legacy systems with long lifecycles
- Safety implications of security failures
- Vendor relationships and support contracts

### Real-World Incidents

- Oldsmar water treatment (2021) - HMI manipulation
- Colonial Pipeline (2021) - IT/OT convergence risks
- Ukraine power grid (2015, 2016) - Coordinated ICS attacks
- Triton/TRISIS (2017) - Safety system targeting

### Career Paths

- ICS penetration testing
- OT security engineering
- Industrial incident response
- Security architecture for critical infrastructure

---

## Assessment Ideas

### Knowledge Check

After the exercises, students should be able to:
- [ ] Explain the TLS-350 protocol and its security implications
- [ ] Demonstrate ATG enumeration and manipulation
- [ ] Identify common HMI vulnerabilities
- [ ] Access and query historian databases
- [ ] Propose appropriate security controls for ICS environments

### Practical Assessment

Consider having students:
- Write a one-page assessment summary of findings
- Create a prioritized remediation roadmap
- Present findings as if to facility management

---

## Additional Resources

### Standards and Frameworks

- NIST SP 800-82: Guide to ICS Security
- IEC 62443: Industrial Automation Security
- NERC CIP: Energy sector requirements

### Training and Certification

- SANS ICS curriculum (GICSP, GRID, GCIP)
- ISA/IEC 62443 Cybersecurity Certificate Program
- Vendor-specific certifications (Claroty, Dragos, etc.)

### Research and News

- ICS-CERT Advisories
- CISA ICS Resources
- SANS ICS Blog

---

## Customization

### Adding Exercises

The lab can be extended with additional scenarios:
- Network segmentation bypass
- Man-in-the-middle attacks
- Persistence mechanisms
- Custom malware simulation

### Adjusting Difficulty

**Easier**: Provide more hints, pre-fill documentation templates
**Harder**: Remove the ATG client tool, require raw protocol interaction

### Industry Focus

Adapt the scenario for specific industries:
- Oil and gas (current scenario)
- Water/wastewater treatment
- Manufacturing
- Power generation

---

## Feedback

If you use this lab in training, we welcome feedback on:
- Exercise clarity and pacing
- Technical issues encountered
- Suggestions for improvements
- Additional exercises you'd like to see

Submit feedback via GitHub issues on the project repository.
