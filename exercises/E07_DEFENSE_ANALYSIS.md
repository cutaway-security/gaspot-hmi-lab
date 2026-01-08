# Exercise 7: Defense Analysis

## The Situation

You've broken things. You've demonstrated significant vulnerabilities. Now comes the part that actually helps the client: analyzing what you found and recommending fixes.

This is what separates penetration testing from just hacking around.

---

## What You'll Learn

- Systematic vulnerability assessment
- Risk prioritization
- Mapping findings to controls
- Writing actionable recommendations

---

## Tasks

### 1. Catalog the Vulnerabilities

Start by listing everything you found. Fill in this table:

| ID | Vulnerability | Component | Exploited In |
|----|---------------|-----------|--------------|
| V1 | No authentication on TLS-350 protocol | ATG | E02, E03 |
| V2 | Weak database credentials | Historian | E05 |
| V3 | Unauthenticated API endpoints | HMI | E04 |
| V4 | No encryption in transit | All | All |
| V5 | No integrity checking on data | All | E03, E05 |
| V6 | | | |
| V7 | | | |

Add any additional vulnerabilities you identified.

### 2. Assess Risk

For each vulnerability, consider:
- **Likelihood**: How easy is it to exploit?
- **Impact**: What's the worst-case outcome?
- **Risk**: Likelihood x Impact

| ID | Likelihood | Impact | Risk Level |
|----|------------|--------|------------|
| V1 | High (trivial to exploit) | High (operational disruption) | Critical |
| V2 | High (guessable credentials) | High (data manipulation) | Critical |
| V3 | | | |
| V4 | | | |
| V5 | | | |

### 3. Map to Security Controls

What controls would address each vulnerability? Consider:
- **Preventive**: Stop the attack from working
- **Detective**: Alert when an attack occurs
- **Corrective**: Recover from an attack

| ID | Preventive Control | Detective Control | Corrective Control |
|----|-------------------|-------------------|-------------------|
| V1 | Network segmentation, firewall rules | Network monitoring, anomaly detection | Incident response plan |
| V2 | Strong passwords, least privilege | Database audit logging | Backup restoration |
| V3 | | | |
| V4 | | | |
| V5 | | | |

### 4. Research Security Standards

Real ICS security assessments map findings to established frameworks. Research these standards:

**NIST SP 800-82** - Guide to ICS Security
- What does it say about network architecture?
- What authentication requirements does it recommend?

**IEC 62443** - Industrial Automation and Control Systems Security
- What security levels are defined?
- How should zone boundaries be protected?

**NERC CIP** (for energy sector)
- What are the critical asset requirements?
- What logging and monitoring is required?

### 5. Prioritize Recommendations

Not everything can be fixed at once. Prioritize by:
- Quick wins (low effort, high impact)
- Critical fixes (high risk items)
- Long-term improvements (architectural changes)

**Quick Wins**:
1. Change database password to something strong
2. Add firewall rules to restrict ATG access
3. Enable logging on all components

**Critical Fixes**:
1. ?
2. ?
3. ?

**Long-Term**:
1. ?
2. ?
3. ?

### 6. Write an Executive Summary

If you had to summarize your findings for a non-technical executive in one paragraph, what would you say?

```
The security assessment of Riverside Natural Gas Terminal identified
[number] vulnerabilities in the operational technology systems.
The most critical finding is [what]. An attacker with network access
could [impact]. We recommend [top priority action] as an immediate
priority, followed by [additional recommendations].
```

---

## Think About It

- How do ICS vulnerabilities differ from IT vulnerabilities?
- Why might these issues have persisted for years?
- What organizational barriers exist to fixing them?
- How do you balance security improvements with operational requirements?

---

## Additional Analysis Questions

For a thorough assessment, also consider:

**Attack Surface**:
- What network paths lead to these systems?
- Are there other entry points we didn't test?
- What about remote access or vendor connections?

**Defense in Depth**:
- If one control fails, what's the backup?
- Are there any compensating controls in place?
- How would an incident be detected?

**Operational Impact**:
- Which fixes require downtime?
- What's the maintenance window availability?
- Are there safety implications to changes?

---

## Assessment Complete

You've now:
- Discovered services through network reconnaissance
- Enumerated industrial protocols
- Manipulated operational data
- Explored web application vulnerabilities
- Exploited database access
- Chained techniques into realistic attacks
- Analyzed findings and developed recommendations

---

## What's Next

If you want to go deeper, try the challenge exercises:
- [C01: Automated Attack](challenges/C01_AUTOMATED_ATTACK.md) - Script the attack chain
- [C02: Detection Script](challenges/C02_DETECTION_SCRIPT.md) - Build monitoring tools
- [C03: Protocol Analysis](challenges/C03_PROTOCOL_ANALYSIS.md) - Deep dive into TLS-350

---

## Notes

**Real Reports**: A professional assessment report would include evidence screenshots, detailed reproduction steps, and specific remediation guidance tailored to the client's environment.

**Follow-Up**: Good consultants don't just hand over a report and walk away. Offer to help prioritize, assist with remediation, and perform validation testing after fixes are implemented.
