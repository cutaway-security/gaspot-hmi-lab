# Challenge 2: Detection Script

## The Challenge

You've attacked the system. Now flip perspectives: build a monitoring tool that would detect the attacks you performed.

Good security isn't just about finding vulnerabilities - it's about building defenses.

---

## Requirements

Your script should monitor for:

1. **Tank name changes** - Alert when product names change
2. **Sudden volume changes** - Flag readings that differ significantly from previous values
3. **New alarms appearing** - Track alarm insertions
4. **Database anomalies** - Detect gaps or suspicious patterns in readings

---

## Detection Logic

### Tank Name Changes

Store known tank names and compare on each poll:

```python
KNOWN_TANKS = {
    1: "NG-MAIN",
    2: "NG-RESERVE",
    3: "NG-FEED",
    4: "DIESEL-PRI",
    5: "DIESEL-RES",
    6: "WATER-UTIL"
}

def check_tank_names():
    current = get_current_tank_names()  # Implement this
    for tank_id, expected in KNOWN_TANKS.items():
        if current.get(tank_id) != expected:
            alert(f"Tank {tank_id} name changed: {expected} -> {current.get(tank_id)}")
```

### Volume Anomalies

Tank volumes shouldn't change drastically between readings:

```python
MAX_VOLUME_CHANGE_PERCENT = 10  # 10% change is suspicious

def check_volume_anomalies(previous, current):
    for tank_id in current:
        prev_vol = previous.get(tank_id, {}).get('volume', 0)
        curr_vol = current[tank_id]['volume']

        if prev_vol > 0:
            change_pct = abs(curr_vol - prev_vol) / prev_vol * 100
            if change_pct > MAX_VOLUME_CHANGE_PERCENT:
                alert(f"Tank {tank_id} volume changed {change_pct:.1f}%")
```

### New Alarms

Track alarm IDs to detect new insertions:

```python
def check_new_alarms(known_alarm_ids):
    current_alarms = get_alarms_from_db()  # Implement this

    for alarm in current_alarms:
        if alarm['id'] not in known_alarm_ids:
            alert(f"New alarm: {alarm['severity']} - {alarm['message']}")
            known_alarm_ids.add(alarm['id'])

    return known_alarm_ids
```

---

## Starter Code

```python
#!/usr/bin/env python3
"""
ICS Monitoring and Detection Script
GasPot HMI Lab - Challenge Exercise
"""

import socket
import subprocess
import time
import datetime
import json
import re

# Configuration
ATG_HOST = "localhost"
ATG_PORT = 10001
POLL_INTERVAL = 10  # seconds
ALERT_LOG = "alerts.log"

def log(message):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {message}")

def alert(message):
    """Log an alert"""
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alert_msg = f"[{ts}] ALERT: {message}"
    print(f"\033[91m{alert_msg}\033[0m")  # Red text
    with open(ALERT_LOG, 'a') as f:
        f.write(alert_msg + '\n')

def get_atg_inventory():
    """Query ATG for current inventory"""
    # TODO: Implement TLS-350 I20100 query
    # Parse response into dict of tank data
    pass

def get_db_alarms():
    """Query database for all alarms"""
    # TODO: Implement database query
    pass

def get_db_readings(minutes=5):
    """Get recent readings from database"""
    # TODO: Implement database query
    pass

class Monitor:
    def __init__(self):
        self.previous_inventory = {}
        self.known_alarm_ids = set()
        self.baseline_names = {}

    def establish_baseline(self):
        """Record initial state"""
        log("Establishing baseline...")
        inventory = get_atg_inventory()
        if inventory:
            self.previous_inventory = inventory
            self.baseline_names = {
                tank_id: data.get('product_name')
                for tank_id, data in inventory.items()
            }

        alarms = get_db_alarms()
        if alarms:
            self.known_alarm_ids = {a['id'] for a in alarms}

        log(f"Baseline: {len(self.baseline_names)} tanks, {len(self.known_alarm_ids)} alarms")

    def check_all(self):
        """Run all detection checks"""
        self.check_names()
        self.check_volumes()
        self.check_alarms()
        # TODO: Add more checks

    def check_names(self):
        """Check for tank name changes"""
        # TODO: Implement
        pass

    def check_volumes(self):
        """Check for suspicious volume changes"""
        # TODO: Implement
        pass

    def check_alarms(self):
        """Check for new alarms"""
        # TODO: Implement
        pass

    def run(self):
        """Main monitoring loop"""
        self.establish_baseline()

        log(f"Starting monitoring (poll interval: {POLL_INTERVAL}s)")
        log("Press Ctrl+C to stop")

        try:
            while True:
                self.check_all()
                time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            log("Monitoring stopped")

def main():
    monitor = Monitor()
    monitor.run()

if __name__ == "__main__":
    main()
```

---

## Additional Detection Ideas

**Reading Gaps**: Alert if the database hasn't received new readings recently:

```python
def check_reading_freshness():
    query = "SELECT MAX(timestamp) FROM tank_readings"
    result = run_sql(query)
    # Parse timestamp and compare to now
    # Alert if more than 2 poll cycles old
```

**Pressure Anomalies**: Gas tanks should maintain pressure within ranges:

```python
PRESSURE_RANGE = (400, 600)  # Normal PSI range

def check_pressure():
    # Query ATG for pressure readings
    # Alert if outside normal range
```

**Database Modifications**: Track record counts for unexpected changes:

```python
def check_record_counts():
    counts = {
        'tanks': run_sql("SELECT COUNT(*) FROM tanks"),
        'readings': run_sql("SELECT COUNT(*) FROM tank_readings"),
        'alarms': run_sql("SELECT COUNT(*) FROM alarms")
    }
    # Compare to previous counts
    # Alert on unexpected decreases (deletions)
```

---

## Bonus Points

- Add email or Slack alerts
- Create a simple web dashboard for alerts
- Implement alert correlation (multiple related alerts = higher severity)
- Add configurable thresholds
- Export alerts in SIEM-compatible format (syslog, JSON)

---

## Testing

1. Start your monitor in one terminal:
   ```bash
   python3 your_monitor.py
   ```

2. In another terminal, perform attacks:
   ```bash
   python3 tools/atg_client.py set-name 1 "HACKED"
   python3 tools/atg_client.py set-volume 2 0
   ```

3. Watch for alerts in the monitor

---

## What You'll Learn

- Building detection logic for ICS environments
- Baselining normal behavior
- Anomaly detection techniques
- Defensive programming and monitoring

---

## Notes

**Real ICS Monitoring**: Tools like Claroty, Dragos, and Nozomi Networks do this commercially. Your simple script demonstrates the core concepts behind their detection engines.

**False Positives**: In production, you'd need to tune thresholds carefully. Too sensitive = alert fatigue. Too loose = missed attacks.
