# GasPot Modifications

This document describes the modifications made to the original GasPot project to create the GasPot HMI Lab simulator.

---

## Original Project

**Repository**: https://github.com/sjhilt/GasPot

**Authors**: Kyle Wilhoit, Stephen Hilt (TrendMicro)

**License**: CC0 1.0 Universal (Public Domain)

**Original Purpose**: GasPot was created as a honeypot to simulate Veeder-Root Guardian AST (Automatic Tank Gauge) systems commonly found at gas stations. It was designed to attract and log malicious activity targeting these industrial control systems.

---

## Summary of Changes

| Feature | Original GasPot | GasPot HMI Lab |
|---------|-----------------|----------------|
| Tanks | 4 tanks (gas station) | 6 tanks (natural gas terminal) |
| Tank Types | Gasoline products | Natural Gas, Diesel, Water |
| Pressure Support | No | Yes (gas tanks only) |
| Volume Write | No | Yes (S60210 command) |
| Pressure Write | No | Yes (S60220 command) |
| Value Fluctuation | No | Yes (5 modes) |
| Configuration | Hardcoded | config.ini file |
| Architecture | Single-file script | Class-based with Tank objects |
| Logging | Honeypot logging | Simplified for lab use |

---

## Detailed Modifications

### 1. Tank Configuration

**Original**: 4 tanks with gasoline products (Diesel, Regular, Plus, Premium)

**Modified**: 6 tanks representing a natural gas distribution terminal:

| Tank | Product | Type | Capacity | Unit | Has Pressure |
|------|---------|------|----------|------|--------------|
| 1 | NG-MAIN | Natural Gas | 50,000 | MCF | Yes |
| 2 | NG-RESERVE | Natural Gas | 50,000 | MCF | Yes |
| 3 | NG-FEED | Natural Gas | 10,000 | MCF | Yes |
| 4 | DIESEL-PRI | Diesel | 10,000 | GAL | No |
| 5 | DIESEL-RES | Diesel | 10,000 | GAL | No |
| 6 | WATER-UTIL | Water | 25,000 | GAL | No |

**Rationale**: Natural gas terminal scenario provides more diverse tank types and introduces pressure as a data point for gas tanks.

### 2. Added I20600 Command (Pressure Sensor Report)

**Original**: Not implemented

**Added**: I20600 returns pressure readings for tanks that support pressure monitoring.

```
PRESSURE SENSOR REPORT

TANK PRODUCT             PRESSURE    STATUS
  1  NG-MAIN              485.2 PSI  NORMAL
  2  NG-RESERVE           520.8 PSI  NORMAL
  3  NG-FEED              445.0 PSI  NORMAL
  4  DIESEL-PRI             N/A      ATMOSPHERIC
  5  DIESEL-RES             N/A      ATMOSPHERIC
  6  WATER-UTIL             N/A      ATMOSPHERIC
```

**Rationale**: Adds another data point for students to enumerate and manipulate. Realistic for pressurized natural gas storage.

### 3. Added S60210 Command (Set Tank Volume)

**Original**: Only S602xx for tank names

**Added**: S60210:TANK_ID:VALUE sets the volume for a specified tank.

```bash
# Set tank 1 volume to 99999
echo -e '\x01S60210:1:99999\n' | nc localhost 10001
```

**Rationale**: Allows students to manipulate tank volumes, simulating data integrity attacks.

### 4. Added S60220 Command (Set Tank Pressure)

**Original**: Not implemented

**Added**: S60220:TANK_ID:VALUE sets the pressure for tanks that support it.

```bash
# Set tank 1 pressure to 999.9
echo -e '\x01S60220:1:999.9\n' | nc localhost 10001
```

**Rationale**: Allows manipulation of pressure values for attack scenarios.

### 5. Value Fluctuation Engine

**Original**: Static values

**Added**: Background thread that fluctuates tank values over time with 5 modes:

| Mode | Behavior | Use Case |
|------|----------|----------|
| high | Large random changes (+/- 2%) | Active consumption/filling |
| medium | Moderate changes (+/- 1%) | Normal operations |
| low | Small changes (+/- 0.5%) | Stable storage |
| decrease | Gradual decline (-0.1% to -0.5%) | Consumption without refill |
| sawtooth | Decrease then sudden increase | Fill cycles |

**Configuration** (config.ini):
```ini
[fluctuation]
enabled = true
interval = 5
```

**Rationale**: Makes the simulation more realistic. Students see changing values, making it clearer this is a "live" system.

### 6. Configuration File (config.ini)

**Original**: Values hardcoded in Python

**Added**: External configuration file for:
- Station name and address
- Tank definitions (name, type, capacity, initial values)
- Fluctuation settings

**Example**:
```ini
[station]
name = RIVERSIDE NATURAL GAS TERMINAL
address = 1234 Industrial Way

[tank1]
name = NG-MAIN
type = NATURAL_GAS
capacity = 50000
volume = 38420
temperature = 58.2
pressure = 485.2
fluctuation = high

[fluctuation]
enabled = true
interval = 5
```

**Rationale**: Easier customization without code changes. Instructors can modify tank configurations for different scenarios.

### 7. Code Architecture

**Original**: Single procedural script with global variables

**Modified**: Object-oriented design:

- `Tank` class: Encapsulates tank state and fluctuation behavior
- `GasPotServer` class: Handles socket connections and command parsing
- Separate configuration loading from `config.ini`
- Threading for fluctuation engine

**Rationale**: Cleaner code, easier to maintain and extend.

### 8. Response Formatting

**Original**: Gas station format with gallons

**Modified**: Updated header and units for natural gas terminal:
- Station name: "RIVERSIDE NATURAL GAS TERMINAL"
- Volume units: MCF (thousand cubic feet) for gas, GAL for liquids
- Added pressure column for gas tanks

### 9. Removed Features

The following honeypot-specific features were removed as they are not needed for a training lab:

- Extensive logging of attacker activity
- IP address tracking
- Attack pattern detection
- Integration with external logging systems

---

## Protocol Compatibility

The modified GasPot maintains compatibility with the TLS-350 protocol:

### Preserved Commands

| Command | Function | Compatibility |
|---------|----------|---------------|
| I20100 | Tank Inventory Report | Full |
| I20200 | Tank Delivery Report | Full |
| I20300 | Tank Leak Detect Report | Full |
| I20400 | Tank Shift Report | Full |
| I20500 | Tank Status Report | Full |
| S602xx | Set Tank Name | Full |

### Extended Commands

| Command | Function | Notes |
|---------|----------|-------|
| I20600 | Pressure Sensor Report | Lab extension |
| S60210 | Set Tank Volume | Lab extension |
| S60220 | Set Tank Pressure | Lab extension |

### Error Handling

Invalid or unrecognized commands return the standard TLS-350 error response:
```
9999FF1B
```

---

## Files Changed

| File | Description |
|------|-------------|
| GasPot.py | Complete rewrite with class-based architecture |
| config.ini | New file for tank and station configuration |
| Dockerfile | Updated for lab deployment |
| requirements.txt | No external dependencies (standard library only) |

---

## Testing Compatibility

The modified simulator has been tested with:

- Manual telnet/netcat commands
- Python ATG client (tools/atg_client.py)
- Nmap atg-info.nse script (from Redpoint)
- Standard TLS-350 command sequences

---

## References

- Original GasPot: https://github.com/sjhilt/GasPot
- TrendMicro Research: https://www.trendmicro.com/en_us/research.html
- Veeder-Root TLS-350 Documentation
- Rapid7 ATG Research: https://www.rapid7.com/blog/post/2015/01/22/the-internet-of-gas-station-tank-gauges/
