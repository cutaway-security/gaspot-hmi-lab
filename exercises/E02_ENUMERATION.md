# Exercise 2: Protocol Enumeration

## The Situation

You've found an ATG on port 10001. Now it's time to learn the protocol and see what information you can extract.

The TLS-350 protocol is text-based and surprisingly simple. Commands start with a special character (Ctrl+A, or hex 0x01) and end with a newline. No login required.

---

## What You'll Learn

- How the TLS-350 protocol works
- What information ATGs expose
- Using both manual and automated enumeration

---

## Tasks

### 1. Your First ATG Command

Let's send an inventory command. The TLS-350 "I20100" command returns tank inventory data:

```bash
echo -e '\x01I20100\n' | nc localhost 10001
```

The `\x01` is the hex code for Ctrl+A (Start of Header). Every TLS-350 command needs this prefix.

You should see a formatted report showing all tanks, their volumes, temperatures, and other metrics.

### 2. Use the ATG Client Tool

Typing hex codes gets old fast. The lab includes a Python tool that handles the protocol for you:

```bash
python3 tools/atg_client.py inventory
```

Much easier, right? Same data, less typing.

### 3. Enumerate Everything

The ATG has several report commands. Let's pull them all:

```bash
# Tank inventory (volume, temperature, height)
python3 tools/atg_client.py inventory

# Pressure readings (for gas tanks)
python3 tools/atg_client.py pressure

# Tank status
python3 tools/atg_client.py status

# Delivery reports
python3 tools/atg_client.py delivery

# Leak test results
python3 tools/atg_client.py leak

# Shift reports
python3 tools/atg_client.py shift
```

### 4. Document What You Found

Create a summary table of the facility. Fill in what you discovered:

| Tank | Product | Type | Volume | Capacity | Pressure | Status |
|------|---------|------|--------|----------|----------|--------|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |
| 6 | | | | | | |

### 5. Try Verbose Mode

Want to see what's happening under the hood?

```bash
python3 tools/atg_client.py -v inventory
```

The `-v` flag shows the raw bytes being sent and received. Useful for understanding the protocol.

---

## Think About It

- How much did you learn about this facility without any authentication?
- What could an attacker do with just this information?
- Would operators know you were querying their system?

---

## Key Findings to Note

For your assessment report, document:
- Number of tanks and their contents
- Which tanks are pressurized (safety critical)
- Current fill levels and capacity
- Any anomalies or concerns

---

## What's Next

Reading data is interesting, but what about writing? Let's see if we can modify things.

Continue to [Exercise 3: ATG Manipulation](E03_ATG_MANIPULATION.md)

---

## Reference

See [Protocol Reference](docs/PROTOCOL_REFERENCE.md) for the complete list of TLS-350 commands.

---

## Notes

**Protocol Quirk**: The TLS-350 protocol terminates responses with ETX (hex 0x03). The ATG client handles this automatically, but you might notice it in verbose mode.

**Real World**: These exact commands work on real Veeder-Root ATGs. The protocol hasn't changed significantly in decades.
