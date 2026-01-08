# Exercise 4: HMI Reconnaissance

## The Situation

The HMI (Human-Machine Interface) is what operators actually use day-to-day. It's a web application that shows tank status, historical trends, and alarms.

Let's see what we can learn from it - and whether it has its own vulnerabilities.

---

## What You'll Learn

- How HMI systems present operational data
- API endpoints and data formats
- Information disclosure through web interfaces

---

## Tasks

### 1. Explore the Interface

Open the HMI dashboard:

```
http://localhost:5000
```

Spend a few minutes clicking around. Visit each page:
- **Dashboard** - Main view with tank cards
- **Trends** - Historical charts
- **Alarms** - Alert history

### 2. Watch for Updates

Stay on the Dashboard page and watch for about 30 seconds. See how the "Last Update" timestamp changes? The HMI polls the ATG periodically and refreshes the display.

If you modified tank values in the previous exercise, you'll see those changes appear here automatically.

### 3. Open Developer Tools

Press F12 (or right-click and select "Inspect") to open your browser's developer tools. Go to the Network tab.

Now refresh the page. Watch the requests that get made. You should see:
- The initial page load
- API calls for data
- Periodic refresh requests

### 4. Find the API Endpoints

The HMI uses a REST API to fetch data. Let's access it directly:

```bash
# Live tank data
curl http://localhost:5000/api/live | python3 -m json.tool

# Alarm list
curl http://localhost:5000/api/alarms | python3 -m json.tool

# Trend data for tank 1
curl http://localhost:5000/api/trends/1 | python3 -m json.tool
```

### 5. Examine the Data

Look at what the API returns:
- Tank configurations and current readings
- Historical data points with timestamps
- Alarm details including messages and severity

Is any of this information that should be protected?

### 6. Check for Authentication

Try accessing the API from a different context:

```bash
# No cookies, no session - does it still work?
curl -s http://localhost:5000/api/live | head -20
```

Did it require any authentication? Any API keys?

### 7. Enumerate All Tanks

The trends endpoint takes a tank ID. What tanks exist?

```bash
for i in 1 2 3 4 5 6 7 8; do
    echo "Tank $i:"
    curl -s "http://localhost:5000/api/trends/$i" | head -5
    echo ""
done
```

Notice how valid tanks return data while invalid ones return empty arrays or errors? This is a common enumeration technique.

---

## Think About It

The HMI exposes:
- Real-time operational data
- Historical trends
- Alarm states and messages

All without authentication.

Consider:
- What could an attacker learn from passive monitoring?
- Could this API be used for reconnaissance before an attack?
- What if someone wrote a script to continuously log this data?

---

## API Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/live | GET | Current readings for all tanks |
| /api/alarms | GET | Active and recent alarms |
| /api/trends/{tank_id} | GET | Historical data for specific tank |
| /health | GET | Service health check |

---

## What's Next

We've seen the ATG and HMI. There's one more component: the historian database where all this data gets stored. Direct database access opens up different attack possibilities.

Continue to [Exercise 5: Database Exploitation](E05_DATABASE_EXPLOITATION.md)

---

## Notes

**HMI Security**: Many real HMIs have similar issues - unauthenticated APIs, information disclosure, sometimes even default credentials. Web security testing techniques apply here.

**Polling Frequency**: This HMI polls every 10 seconds. On a real network, that's detectable traffic an attacker could observe or manipulate.
