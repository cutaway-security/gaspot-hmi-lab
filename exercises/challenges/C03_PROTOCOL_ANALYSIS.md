# Challenge 3: Protocol Analysis

## The Challenge

Go deeper into the TLS-350 protocol. Use Wireshark to capture and analyze the traffic, then document the protocol structure in detail.

This is the kind of reverse engineering that security researchers do when analyzing industrial protocols.

---

## Requirements

1. **Capture** TLS-350 traffic with Wireshark
2. **Document** the protocol structure (framing, commands, responses)
3. **Identify** patterns and anomalies
4. **Create** a simple protocol dissector (optional)

---

## Part 1: Traffic Capture

### Setup Wireshark

Start Wireshark and capture on the loopback interface:

```bash
# Option 1: GUI
wireshark &
# Select "Loopback: lo" interface

# Option 2: Command line
tshark -i lo -f "port 10001" -w atg_capture.pcap
```

### Generate Traffic

While capturing, run various ATG commands:

```bash
# Read commands
python3 tools/atg_client.py inventory
python3 tools/atg_client.py pressure
python3 tools/atg_client.py status

# Write commands
python3 tools/atg_client.py set-name 1 "TEST"
python3 tools/atg_client.py set-volume 1 12345

# Raw commands
echo -e '\x01I20100\n' | nc localhost 10001
echo -e '\x01I20600\n' | nc localhost 10001
```

### Stop Capture

Stop the capture and save the pcap file for analysis.

---

## Part 2: Protocol Documentation

Analyze your capture and document:

### Frame Structure

```
[SOH] [COMMAND] [LF]
  ^       ^       ^
  |       |       +-- 0x0A Line Feed
  |       +---------- Variable length ASCII
  +------------------ 0x01 Start of Header

Response:
[DATA...] [ETX]
    ^       ^
    |       +-- 0x03 End of Text
    +---------- Variable length ASCII
```

### Command Catalog

| Command | Type | Description | Response |
|---------|------|-------------|----------|
| I20100 | Read | Tank inventory | Multi-line report |
| I20200 | Read | Delivery report | Multi-line report |
| I20300 | Read | Leak test | Multi-line report |
| I20400 | Read | Shift report | Multi-line report |
| I20500 | Read | Status report | Multi-line report |
| I20600 | Read | Pressure report | Multi-line report |
| S6020x | Write | Set tank x name | None |
| S60210:t:v | Write | Set tank t volume to v | None |
| S60220:t:v | Write | Set tank t pressure to v | None |

### Response Format

Document the structure of inventory response:

```
[DATE/TIME]

     [STATION NAME]


[REPORT TITLE]

[HEADER ROW]
[DATA ROW 1]
[DATA ROW 2]
...
[ETX]
```

### Field Positions

For the inventory response, map the column positions:

| Field | Start Column | Width | Type |
|-------|--------------|-------|------|
| TANK | 0 | 3 | Integer |
| PRODUCT | 5 | 20 | String |
| VOLUME | 26 | 10 | Decimal |
| TC VOLUME | 37 | 10 | Decimal |
| ... | ... | ... | ... |

---

## Part 3: Traffic Analysis

Look for these patterns in your capture:

### Session Behavior
- How long do connections stay open?
- Is there any session state?
- What happens with multiple concurrent connections?

### Error Handling
- Send an invalid command: `echo -e '\x01INVALID\n' | nc localhost 10001`
- What error response is returned?
- How does the protocol signal errors?

### Timing
- How long between command and response?
- Any timeouts observed?

---

## Part 4: Wireshark Dissector (Advanced)

Create a Lua dissector for Wireshark:

```lua
-- tls350.lua - TLS-350 Protocol Dissector
-- Place in ~/.local/lib/wireshark/plugins/

local tls350 = Proto("TLS350", "TLS-350 ATG Protocol")

-- Fields
local f_soh = ProtoField.uint8("tls350.soh", "Start of Header", base.HEX)
local f_command = ProtoField.string("tls350.command", "Command")
local f_data = ProtoField.string("tls350.data", "Data")

tls350.fields = { f_soh, f_command, f_data }

function tls350.dissector(buffer, pinfo, tree)
    local length = buffer:len()
    if length == 0 then return end

    pinfo.cols.protocol = tls350.name

    local subtree = tree:add(tls350, buffer(), "TLS-350 Protocol")

    -- Check for SOH (0x01)
    local first_byte = buffer(0, 1):uint()
    if first_byte == 0x01 then
        subtree:add(f_soh, buffer(0, 1))
        -- TODO: Parse command
        pinfo.cols.info = "Command: " .. buffer(1):string()
    else
        -- Response data
        subtree:add(f_data, buffer())
        pinfo.cols.info = "Response"
    end
end

-- Register for TCP port 10001
local tcp_table = DissectorTable.get("tcp.port")
tcp_table:add(10001, tls350)
```

### Testing the Dissector

1. Save the file to your Wireshark plugins directory
2. Restart Wireshark or reload Lua plugins
3. Capture TLS-350 traffic
4. Verify packets show as "TLS-350" protocol

---

## Documentation Template

Create a protocol specification document:

```markdown
# TLS-350 Protocol Specification

## Overview
- Transport: TCP
- Default Port: 10001
- Encoding: ASCII
- Authentication: None

## Message Format
### Request
[diagram]

### Response
[diagram]

## Commands
### I20100 - Tank Inventory
[detailed description]
[example request hex dump]
[example response hex dump]
[parsed fields]

### S602xx - Set Tank Name
[detailed description]
...

## Error Codes
[list of error responses]

## Security Considerations
[analysis of protocol weaknesses]
```

---

## Bonus Points

- Compare your findings to the actual Veeder-Root TLS-350 documentation
- Identify any undocumented commands the simulator might accept
- Write a Scapy layer for TLS-350
- Create a Python library that generates and parses protocol messages

---

## What You'll Learn

- Protocol reverse engineering techniques
- Wireshark dissector development
- Industrial protocol structure analysis
- Documentation of technical specifications

---

## Resources

- Wireshark Lua API: https://www.wireshark.org/docs/wsdg_html_chunked/wsluarm.html
- Scapy documentation: https://scapy.readthedocs.io/
- Original TLS-350 research: Rapid7 ATG blog posts

---

## Notes

**Real Protocol Analysis**: Security researchers use these techniques to analyze unknown protocols in malware, industrial systems, and proprietary applications.

**Protocol Documentation**: Well-documented protocol specifications are essential for building detection rules, creating honeypots, and understanding attack surfaces.
