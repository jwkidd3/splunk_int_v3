# Lab 4: Filtering and Manipulating Data

**Splunk Intermediate – Lab Exercises**

## Objectives

- Use eval for calculations and unit conversion
- Filter results with search and where commands
- Classify data with case function
- Apply conditional logic with if function
- Use LIKE operator for pattern matching

---

## Task 1: Converting Bytes to Megabytes

### Step 1: View Raw Bytes

```spl
index=network sourcetype=cisco_wsa_squid
| stats sum(sc_bytes) as total_bytes by cs_username
| sort -total_bytes
```

### Step 2: Convert to MB

```spl
index=network sourcetype=cisco_wsa_squid
| stats sum(sc_bytes) as total_bytes by cs_username
| eval megabytes = round(total_bytes/(1024*1024), 2)
| table cs_username total_bytes megabytes
| sort -megabytes
```

### Step 3: Clean Display

```spl
index=network sourcetype=cisco_wsa_squid
| stats sum(sc_bytes) as total_bytes by cs_username
| eval megabytes = round(total_bytes/(1024*1024), 2)
| fields cs_username megabytes
| rename cs_username as "User", megabytes as "Usage (MB)"
| sort -"Usage (MB)"
```

**Save as**: `L4S1`

---

## Task 2: Calculate GET to POST Ratio

### Step 1: Count Methods

```spl
index=web sourcetype=access_combined
| stats count(eval(method="GET")) as GET, count(eval(method="POST")) as POST
```

### Step 2: Calculate Ratio

```spl
index=web sourcetype=access_combined
| stats count(eval(method="GET")) as GET, count(eval(method="POST")) as POST
| eval Ratio = round(GET/POST, 2)
| table GET POST Ratio
```

### Step 3: Add Interpretation

```spl
index=web sourcetype=access_combined
| stats count(eval(method="GET")) as GET, count(eval(method="POST")) as POST
| eval Ratio = round(GET/POST, 2)
| eval Interpretation = case(
    Ratio > 10, "Very High GET Usage",
    Ratio > 5, "High GET Usage",
    Ratio > 2, "Moderate GET Usage",
    Ratio <= 2, "Balanced Usage"
)
| table GET POST Ratio Interpretation
```

**Save as**: `L4S2`

---

## Task 3: Filtering with Search Command

### Step 1: Count by IP

```spl
index=security sourcetype=linux_secure
| stats count by src_ip
```

### Step 2: Filter with Search

```spl
index=security sourcetype=linux_secure
| stats count by src_ip
| search count > 3
| sort -count
```

### Step 3: Add Filters

```spl
index=security sourcetype=linux_secure "failed password"
| stats count by src_ip
| search count > 3
| sort -count
| head 10
```

**Save as**: `L4S3`

---

## Task 4: Classify Data with Case

### Step 1: View Bytes

```spl
index=web sourcetype=access_combined
| stats count by bytes
| sort bytes
```

### Step 2: Classify Sizes

```spl
index=web sourcetype=access_combined
| eval dataSize = case(
    bytes < 2000, "Small",
    bytes >= 2000 AND bytes < 5000, "Medium",
    bytes >= 5000, "Large"
)
| stats count by dataSize
```

### Step 3: Add Default Case

```spl
index=web sourcetype=access_combined
| eval dataSize = case(
    bytes < 2000, "Small",
    bytes >= 2000 AND bytes < 5000, "Medium",
    bytes >= 5000, "Large",
    1=1, "Unknown"
)
| stats count by dataSize
| sort -count
```

### Step 4: Multi-Tier

```spl
index=web sourcetype=access_combined
| eval dataSize = case(
    bytes < 1000, "Tiny",
    bytes >= 1000 AND bytes < 2000, "Small",
    bytes >= 2000 AND bytes < 5000, "Medium",
    bytes >= 5000 AND bytes < 10000, "Large",
    bytes >= 10000, "Very Large",
    1=1, "Unknown"
)
| chart count over dataSize by status
```

**Save as**: `L4S4`

---

## Task 5: Using Where Command

### Step 1: Compare Search vs Where

Search:
```spl
index=web sourcetype=access_combined
| stats avg(bytes) as avg_bytes by action
| search avg_bytes > 5000
```

Where:
```spl
index=web sourcetype=access_combined
| stats avg(bytes) as avg_bytes by action
| where avg_bytes > 5000
```

### Step 2: String Comparison

```spl
index=web sourcetype=access_combined
| stats count by action, status
| where action="purchase" AND status>=200 AND status<300
```

### Step 3: LIKE Operator

```spl
index=web sourcetype=access_combined
| stats count by useragent
| where useragent LIKE "%Mobile%"
| sort -count
```

**Save as**: `L4S5`

---

## Challenge: Content Type Classification

Classify HTTP content types:

```spl
index=web sourcetype=access_combined
| stats sum(bytes) as total_bytes by http_content_type
| eval contentCategory = if(http_content_type LIKE "image%", "graphic",
    if(http_content_type LIKE "text%", "text",
    if(http_content_type LIKE "application%", "application",
    "other")))
| stats sum(total_bytes) as bytes by contentCategory
| eval megabytes = round(bytes/(1024*1024), 2)
| table contentCategory megabytes
| sort -megabytes
```

**Save as**: `L4C1`

---

## Summary

- eval creates calculated fields using math operations
- round() formats numbers to specified decimal places
- search filters results after transforming commands
- case evaluates conditions in order, returns first match
- where supports advanced filtering with functions
- LIKE operator enables pattern matching with wildcards
- Use `1=1` in case for default/else condition

---

**Lab 4 Complete!**
