# GasPot HMI Lab - Security Assessment Exercises

## The Scenario

You've just joined Cutaway Security as a junior consultant. Your first big assignment? A security assessment of Riverside Natural Gas Terminal - a mid-sized facility that stores and distributes natural gas and diesel fuel to local distributors.

The facility manager, after reading about ransomware attacks on pipelines, decided it was time to get a professional security review. "We've been running these systems for years without any problems," she told your boss during the kickoff call. "But I want to make sure we're not the next headline."

Your task is straightforward: find out what an attacker with network access could do to their operational technology systems. No need to be subtle - this is an authorized assessment on an isolated lab environment. Break things, document what you find, and help them understand their risk.

---

## What You're Working With

The Riverside terminal runs a pretty typical setup for this industry:

**Automatic Tank Gauges (ATGs)** - Veeder-Root TLS-350 systems that monitor tank levels, temperature, and pressure. These have been the industry standard for decades. They communicate using a proprietary protocol over TCP port 10001.

**HMI Dashboard** - A web-based interface (port 5000) where operators monitor all six tanks in real-time. Shows current levels, historical trends, and any alarms.

**Historian Database** - A MariaDB instance (port 3306) that stores all the historical readings. Operators use this for reporting and trend analysis.

The facility has six tanks total:
- Three natural gas storage tanks (pressurized)
- Two diesel tanks (atmospheric)
- One water utility tank

---

## Before You Start

Make sure the lab environment is running:

```bash
./scripts/start_lab.sh
```

Verify you can access:
- HMI Dashboard: http://localhost:5000
- ATG: `nc localhost 10001` (type Ctrl+A then I20100 and Enter)
- Database: `docker exec -it gaspot-historian mysql -u lab -ppassword historian`

---

## The Exercises

Work through these exercises in order. Each one builds on what you learned before.

| Exercise | Focus | Time |
|----------|-------|------|
| [E01: Discovery](E01_DISCOVERY.md) | Find what's on the network | 15 min |
| [E02: Enumeration](E02_ENUMERATION.md) | Learn the protocol and gather intel | 20 min |
| [E03: HMI Reconnaissance](E03_HMI_RECONNAISSANCE.md) | Explore the operator interface | 15 min |
| [E04: ATG Manipulation](E04_ATG_MANIPULATION.md) | See what you can change | 20 min |
| [E05: Database Exploitation](E05_DATABASE_EXPLOITATION.md) | Access the historical data | 25 min |
| [E06: Attack Chain](E06_ATTACK_CHAIN.md) | Put it all together | 30 min |
| [E07: Defense Analysis](E07_DEFENSE_ANALYSIS.md) | Write up your findings | 30 min |

Total time: approximately 2.5 hours

---

## Challenge Exercises

Finished early or want to go deeper? Try these:

| Challenge | Description |
|-----------|-------------|
| [C01: Automated Attack](challenges/C01_AUTOMATED_ATTACK.md) | Script the attack chain |
| [C02: Detection Script](challenges/C02_DETECTION_SCRIPT.md) | Build a monitoring tool |
| [C03: Protocol Analysis](challenges/C03_PROTOCOL_ANALYSIS.md) | Deep dive into TLS-350 |

---

## Reference Documentation

Need to look something up?

- [TLS-350 ATG Protocol Reference](docs/PROTOCOL_REFERENCE.md) - Protocol commands and ATG client usage
- [Database Reference](docs/DATABASE_REFERENCE.md) - Schema, queries, and manipulation examples

---

## A Note on Realism

This lab simulates real vulnerabilities found in actual ICS environments. The TLS-350 protocol really does work this way - no authentication, no encryption, commands sent in cleartext. Researchers have found thousands of these devices exposed directly to the internet.

The weak database credentials? Also realistic. Default passwords and simple credentials are disturbingly common in industrial environments where "it's always worked this way."

The goal here isn't just to hack a pretend gas station. It's to understand why these systems are vulnerable, what the real-world impact could be, and what can be done to fix it.

---

## Resetting the Lab

Made a mess of things? No problem:

```bash
./scripts/reset_lab.sh
./scripts/start_lab.sh
```

This wipes all data and starts fresh. Do this between exercises if you want a clean slate, or at the end of your session.

---

## Ready?

Start with [Exercise 1: Discovery](E01_DISCOVERY.md) and see what you can find.
