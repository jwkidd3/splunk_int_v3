# Lab 5: Correlating Events

**Splunk Intermediate – Lab Exercises**

## Objectives

- Use transaction command to group related events
- Calculate and analyze transaction duration
- Filter transactions by duration and event count
- Track workflows with startswith and endswith
- Use maxspan and maxpause parameters

---

## Task 1: Basic Transactions

### Step 1: View Individual Events

```spl
index=web sourcetype=access_combined_wcookie
| table _time JSESSIONID clientip action productId
| sort _time
```

### Step 2: Create Transactions

```spl
index=web sourcetype=access_combined_wcookie
| transaction JSESSIONID
| table JSESSIONID duration eventcount
```

### Step 3: Show Actions

```spl
index=web sourcetype=access_combined_wcookie
| transaction JSESSIONID
| table _time JSESSIONID clientip action duration eventcount
| sort -duration
```

**Save as**: `L5S1`

---

## Task 2: Analyze Duration

### Step 1: Convert to Minutes

```spl
index=web sourcetype=access_combined_wcookie
| transaction JSESSIONID
| eval durationMinutes = round(duration/60, 1)
| table JSESSIONID clientip durationMinutes eventcount
| sort -durationMinutes
```

### Step 2: Duration Statistics

```spl
index=web sourcetype=access_combined_wcookie
| transaction JSESSIONID
| eval durationMinutes = round(duration/60, 1)
| stats count as Sessions,
        avg(durationMinutes) as "Avg Duration (min)",
        max(durationMinutes) as "Max Duration (min)",
        min(durationMinutes) as "Min Duration (min)"
```

### Step 3: Categorize Sessions

```spl
index=web sourcetype=access_combined_wcookie
| transaction JSESSIONID
| eval durationMinutes = round(duration/60, 1)
| eval durationCategory = case(
    durationMinutes < 1, "Quick (< 1 min)",
    durationMinutes >= 1 AND durationMinutes < 5, "Normal (1-5 min)",
    durationMinutes >= 5 AND durationMinutes < 10, "Long (5-10 min)",
    durationMinutes >= 10, "Very Long (> 10 min)"
)
| stats count by durationCategory
| sort -count
```

**Save as**: `L5S2`

---

## Task 3: Filter Transactions

### Step 1: Long Sessions

```spl
index=web sourcetype=access_combined_wcookie
| transaction JSESSIONID
| eval durationMinutes = round(duration/60, 1)
| where durationMinutes > 1
| table _time JSESSIONID clientip durationMinutes eventcount action
| sort -durationMinutes
```

### Step 2: Analyze Long Session Actions

```spl
index=web sourcetype=access_combined_wcookie
| transaction JSESSIONID
| eval durationMinutes = round(duration/60, 1)
| where durationMinutes > 1
| stats count by action
| sort -count
```

### Step 3: High-Event Sessions

```spl
index=web sourcetype=access_combined_wcookie
| transaction JSESSIONID
| eval durationMinutes = round(duration/60, 1)
| where eventcount > 10
| table JSESSIONID clientip durationMinutes eventcount
| sort -eventcount
```

**Save as**: `L5S3`

---

## Task 4: Track Purchase Workflows

### Step 1: Cart to Purchase

```spl
index=web sourcetype=access_combined_wcookie
| transaction clientip startswith="action=addtocart" endswith="action=purchase"
| table _time clientip duration eventcount
```

### Step 2: Workflow Details

```spl
index=web sourcetype=access_combined_wcookie
| transaction clientip startswith="action=addtocart" endswith="action=purchase"
| eval durationMinutes = round(duration/60, 1)
| table clientip durationMinutes eventcount productId
| sort -durationMinutes
```

### Step 3: Purchase Metrics

```spl
index=web sourcetype=access_combined_wcookie
| transaction clientip startswith="action=addtocart" endswith="action=purchase"
| eval durationMinutes = round(duration/60, 1)
| stats count as "Completed Purchases",
        avg(durationMinutes) as "Avg Time to Purchase (min)",
        avg(eventcount) as "Avg Events in Purchase Flow"
```

### Step 4: Abandoned vs Completed

```spl
index=web sourcetype=access_combined_wcookie action=addtocart OR action=purchase
| transaction JSESSIONID maxspan=30m
| eval purchaseCompleted = if(searchmatch("action=purchase"), "Yes", "No")
| stats count by purchaseCompleted
```

**Save as**: `L5S4`

---

## Task 5: Advanced Options

### Step 1: Maxspan

```spl
index=web sourcetype=access_combined_wcookie
| transaction JSESSIONID maxspan=30m
| eval durationMinutes = round(duration/60, 1)
| table JSESSIONID clientip durationMinutes eventcount
| sort -eventcount
```

### Step 2: Maxpause

```spl
index=web sourcetype=access_combined_wcookie
| transaction clientip maxpause=5m maxspan=30m
| eval durationMinutes = round(duration/60, 1)
| where eventcount > 1
| table clientip durationMinutes eventcount action
| sort -durationMinutes
```

### Step 3: Combined Parameters

```spl
index=web sourcetype=access_combined_wcookie
| transaction JSESSIONID maxspan=1h maxpause=10m startswith="action=view" endswith="action=purchase"
| eval durationMinutes = round(duration/60, 1)
| table JSESSIONID durationMinutes eventcount
| stats count as Purchases,
        avg(durationMinutes) as "Avg Duration",
        avg(eventcount) as "Avg Steps"
```

**Save as**: `L5S5`

---

## Challenge: Shopping Cart Analysis

Analyze cart abandonment:
1. Identify sessions with addtocart actions
2. Determine completed vs abandoned purchases
3. Calculate abandonment rate
4. Analyze time before abandonment
5. Identify most abandoned products

**Save as**: `L5C1`

---

## Summary

- transaction groups events by common field values
- duration auto-calculates time between first and last event (seconds)
- eventcount shows number of events in transaction
- startswith/endswith define transaction boundaries
- maxspan limits total transaction duration
- maxpause limits time between events
- Convert duration to minutes: `eval durationMinutes = round(duration/60, 1)`

---

**Lab 5 Complete!**
