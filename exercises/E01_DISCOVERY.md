# Exercise 1: Network Discovery

## The Situation

You've just connected your laptop to the facility's operational technology (OT) network. The network administrator gave you a range to work with, but for this lab, everything is running locally on standard ports.

Your first job: figure out what services are running and what you're dealing with.

---

## What You'll Learn

- How to identify ICS services on a network
- What the TLS-350 ATG service looks like
- Basic reconnaissance techniques for OT environments

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
