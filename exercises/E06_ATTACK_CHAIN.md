# Exercise 6: Attack Chain

## The Situation

You've compromised individual components. Now it's time to think like an attacker and chain these techniques into a coherent attack scenario.

Real attackers don't just poke at systems randomly. They have objectives, and they combine techniques to achieve them.

---

## What You'll Learn

- How to combine multiple attack vectors
- Sequencing attacks for maximum impact
- Thinking through attacker objectives

---

## The Scenario

**Objective**: Create confusion and distrust in the facility's monitoring systems.

Imagine you're a malicious actor who wants to:
1. Make operators believe there's an emergency
2. Undermine their confidence in the monitoring systems
3. Leave minimal evidence of your actions

Let's execute this plan.

---

## Phase 1: Create Diversion

First, inject some alarming (pun intended) alerts to get operators' attention:

```bash
docker exec -it gaspot-historian mysql -u lab -ppassword historian -e "
INSERT INTO alarms (tank_id, alarm_type, severity, message, timestamp)
VALUES
(1, 'LEAK_DETECTED', 'CRITICAL', 'Major leak detected - immediate action required', NOW()),
(2, 'OVERPRESSURE', 'CRITICAL', 'Pressure exceeding safe operating limits', NOW()),
(3, 'SENSOR_FAULT', 'WARNING', 'Multiple sensor failures detected', NOW());
"
```

Check the HMI Alarms page. Three new alerts just appeared. If this were real, operators would be scrambling.

---

## Phase 2: Manipulate ATG Data

While operators are distracted by the alarms, modify the ATG to show incorrect data:

```bash
# Rename tanks to something concerning
python3 tools/atg_client.py set-name 1 "LEAK-SHUTOFF"
python3 tools/atg_client.py set-name 2 "CRITICAL"

# Show tanks as nearly empty
python3 tools/atg_client.py set-volume 1 100
python3 tools/atg_client.py set-volume 2 50
```

Refresh the HMI Dashboard. Tank 1 and 2 now show alarming names and near-zero levels.

---

## Phase 3: Poison Historical Data

Modify the historian so even the trend charts look wrong:

```bash
docker exec -it gaspot-historian mysql -u lab -ppassword historian -e "
UPDATE tank_readings
SET volume = volume * 0.1
WHERE tank_id IN (1, 2)
AND timestamp > DATE_SUB(NOW(), INTERVAL 1 HOUR);
"
```

Check the Trends page for tanks 1 and 2. The historical data now shows a dramatic decline.

---

## Phase 4: Observe the Impact

Take a moment to review what you've created:

**Dashboard**: Two tanks showing near-empty with alarming names
**Trends**: Historical data showing rapid decline
**Alarms**: Multiple critical alerts demanding attention

If you were an operator, what would you think? What actions might you take?

---

## Phase 5: Document the Attack

For your assessment report, create a timeline:

| Time | Action | Component | Impact |
|------|--------|-----------|--------|
| T+0 | Injected false alarms | Database | Operators alerted |
| T+1 | Changed tank names | ATG | Visual confusion |
| T+2 | Modified volumes | ATG | False low-level readings |
| T+3 | Altered history | Database | Trends show false decline |

---

## Phase 6: Clean Up

Reset the environment for the next exercise:

```bash
./scripts/reset_lab.sh
./scripts/start_lab.sh
```

Wait for all containers to be healthy before continuing.

---

## Think About It

This attack took maybe 5 minutes to execute. Consider:

- **Detection**: Would anyone have noticed in real-time?
- **Response**: How would operators verify what's real vs. fake?
- **Recovery**: How do you restore trust in the data?
- **Prevention**: What controls would have stopped this?

---

## Variations to Consider

Other attack objectives might include:

**Stealth Manipulation**: Gradually change values by small amounts over time. Much harder to detect than sudden changes.

**Safety System Bypass**: Manipulate readings to prevent alarms from triggering when they should.

**Ransomware Staging**: Demonstrate access and threaten to disrupt operations unless paid.

**Competitive Intelligence**: Just read data over time to understand production capacity, delivery schedules, etc.

---

## What's Next

You've demonstrated significant vulnerabilities. Now let's analyze them systematically and develop recommendations.

Continue to [Exercise 7: Defense Analysis](E07_DEFENSE_ANALYSIS.md)

---

## Notes

**Real Incidents**: Similar attack chains have been observed in the wild. The 2021 Oldsmar water treatment incident involved an attacker modifying chemical levels through an HMI - a direct parallel to what you just demonstrated.

**Attack Trees**: Security professionals use "attack trees" to model how attackers combine techniques. This exercise followed a simple tree: Access -> Enumerate -> Manipulate -> Obscure.
