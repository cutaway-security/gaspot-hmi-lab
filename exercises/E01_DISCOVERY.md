# Exercise 1: Network Discovery

## The Situation

You've just connected your laptop to the facility's operational technology (OT) network. The network administrator gave you a range to work with, but for this lab, everything is running locally on standard ports.

Your first job: figure out what services are running and what you're dealing with.

---

## What You'll Learn

- How to identify ICS services on a network
- What the TLS-350 ATG service looks like
- Basic reconnaissance techniques for OT environments

**New to network scanning tools?** See [Appendix: Tools Overview](#appendix-tools-overview) at the end of this document for explanations of nmap and netcat.

---

## Tasks

### 1. Find the ATG Service

The ATG should be listening on port 10001. Let's verify:

```bash
nmap -sV -p 10001 localhost
```

What does nmap report? You might see something like "ATG" or just an unknown service. That's normal - these industrial protocols aren't always in nmap's database.

### 2. Quick Check with Netcat

Sometimes the simplest tools work best:

```bash
nc -zv localhost 10001
```

If you see "Connection succeeded" - the ATG is there and listening.

### 3. Scan All Lab Services

Let's get the full picture:

```bash
nmap -sV -p 5000,10001,3306 localhost
```

You should find three services:
- Port 5000: The HMI web interface
- Port 10001: The ATG
- Port 3306: The historian database

### 4. Research Time

If you haven't worked with tank gauges before, take a few minutes to look up:
- What is a Veeder-Root TLS-350?
- What is the TLS-350 protocol used for?
- Why might these devices be interesting to attackers?

The Rapid7 blog post "The Internet of Gas Station Tank Gauges" is a good starting point.

---

## Think About It

Before moving on, consider:

- Were any of these ports protected by authentication just to connect?
- What would happen if these services were exposed to the internet?
- How would you find these services on a real network assessment?

---

## What's Next

You've found the services. Now let's see what they'll tell us.

Continue to [Exercise 2: Protocol Enumeration](E02_ENUMERATION.md)

---

## Notes

**Tip**: On a real assessment, you'd probably start with a broader scan and work your way down. Here we're keeping it focused since we already know what's in the lab.

**Real World**: Shodan and Censys have found thousands of ATGs exposed directly to the internet. Many respond to queries from anyone who connects.

---

## Appendix: Tools Overview

If you're not familiar with the network tools used in this exercise, here's a quick overview.

### nmap (Network Mapper)

**What it is**: A powerful open-source tool for network discovery and security auditing. It's the standard tool for finding what hosts and services are available on a network.

**Common flags used in this lab**:

| Flag | Purpose |
|------|---------|
| `-sV` | Service/version detection - tries to determine what software is running on open ports |
| `-p <ports>` | Specify which ports to scan (e.g., `-p 22,80,443` or `-p 1-1000`) |
| `-sT` | TCP connect scan (default when not running as root) |
| `-sS` | TCP SYN scan (faster, requires root privileges) |

**Example**:
```bash
nmap -sV -p 10001 localhost
```
This scans port 10001 on localhost and attempts to identify what service is running.

**Learn more**: https://nmap.org/book/man.html

### nc (netcat)

**What it is**: A versatile networking utility that reads and writes data across network connections. Often called the "Swiss Army knife" of networking tools, it can be used for port scanning, file transfers, and creating simple network connections.

**Common flags used in this lab**:

| Flag | Purpose |
|------|---------|
| `-z` | Zero-I/O mode - just scan for listening services without sending data |
| `-v` | Verbose - show connection status messages |
| `-w <secs>` | Timeout - wait specified seconds for a connection |

**Example**:
```bash
nc -zv localhost 10001
```
This checks if port 10001 is open on localhost without sending any data. You'll see "Connection succeeded" or "Connection refused".

**Sending data**:
```bash
echo -e '\x01I20100\n' | nc localhost 10001
```
This pipes a TLS-350 command to netcat, which sends it to the ATG and displays the response.

**Learn more**: `man nc` or https://man.openbsd.org/nc.1
