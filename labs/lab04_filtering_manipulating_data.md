# Lab 4: Filtering Results and Manipulating Data

**Splunk Intermediate – Lab Exercises**

> **Note**: This lab should be completed in a non-production environment.

## Lab Description

This lab covers:
- Using the eval command to calculate and create new fields
- Converting units and performing mathematical operations
- Using the search command to filter results
- Using the where command for complex filtering
- Using the case function to classify data into categories
- Using the if function for conditional logic
- Using the LIKE operator for pattern matching

## Scenario

You are a Splunk administrator for Buttercup Games. The IT team needs to convert network usage from bytes to megabytes, the web team wants to analyze the ratio of GET to POST requests, and the sales team needs to classify transaction sizes for reporting purposes.

---

## Task 1: Converting Bytes to Megabytes

### Scenario

Network logs record bandwidth usage in bytes, but the IT team needs to see this data in megabytes for easier interpretation.

### Step 1.1: View Raw Bytes Data

First, look at the raw bytes data:

```spl
index=network sourcetype=cisco_wsa_squid
| stats sum(sc_bytes) as total_bytes by cs_username
| sort -total_bytes
```

**Expected Results**: A table showing total bytes by username

### Step 1.2: Convert Bytes to Megabytes

Use the eval command to convert bytes to megabytes:

```spl
index=network sourcetype=cisco_wsa_squid
| stats sum(sc_bytes) as total_bytes by cs_username
| eval megabytes = round(total_bytes/(1024*1024), 2)
| table cs_username total_bytes megabytes
| sort -megabytes
```

**Expected Results**: A table with an additional "megabytes" column showing the converted values rounded to 2 decimal places

### Step 1.3: Display Only Megabytes

Show only the most useful fields:

```spl
index=network sourcetype=cisco_wsa_squid
| stats sum(sc_bytes) as total_bytes by cs_username
| eval megabytes = round(total_bytes/(1024*1024), 2)
| fields cs_username megabytes
| rename cs_username as "User", megabytes as "Usage (MB)"
| sort -"Usage (MB)"
```

**Expected Results**: A clean table with User and Usage (MB) columns

**Save this search as**: `L4S1`

> **Note**: The eval command is used to:
> - Create new fields
> - Calculate values using mathematical operations
> - Convert units
> - The round() function formats numbers to a specified number of decimal places

---

## Task 2: Calculating GET to POST Ratio

### Scenario

The web development team wants to understand the ratio of GET requests to POST requests to optimize their application.

### Step 2.1: Count GET and POST Requests

Count the number of GET and POST requests:

```spl
index=web sourcetype=access_combined
| stats count(eval(method="GET")) as GET, count(eval(method="POST")) as POST
```

**Expected Results**: A single row showing the count of GET and POST requests

### Step 2.2: Calculate the Ratio

Calculate the GET to POST ratio:

```spl
index=web sourcetype=access_combined
| stats count(eval(method="GET")) as GET, count(eval(method="POST")) as POST
| eval Ratio = round(GET/POST, 2)
| table GET POST Ratio
```

**Expected Results**: A table showing GET count, POST count, and their ratio

### Step 2.3: Add Interpretation

Add a field that interprets the ratio:

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

**Expected Results**: A table with an interpretation of the GET/POST ratio

**Save this search as**: `L4S2`

> **Tip**: Use eval with stats to perform calculations on subsets of data before aggregating results.

---

## Task 3: Filtering with the Search Command

### Scenario

The security team wants to identify IP addresses that have attempted to log in more than 3 times.

### Step 3.1: Count Login Attempts by IP

Create a count of login attempts by source IP:

```spl
index=security sourcetype=linux_secure
| stats count by src_ip
```

**Expected Results**: A table showing the count of events for each source IP

### Step 3.2: Filter Using Search Command

Use the search command to filter results where count is greater than 3:

```spl
index=security sourcetype=linux_secure
| stats count by src_ip
| search count > 3
| sort -count
```

**Expected Results**: Only source IPs with more than 3 login attempts are shown, sorted by count in descending order

### Step 3.3: Add Additional Filters

Combine multiple search filters:

```spl
index=security sourcetype=linux_secure "failed password"
| stats count by src_ip
| search count > 3
| sort -count
| head 10
```

**Expected Results**: Top 10 source IPs with more than 3 failed password attempts

**Save this search as**: `L4S3`

> **Note**: The search command:
> - Filters results after transforming commands
> - Can be used multiple times in a search pipeline
> - Supports comparison operators: >, <, >=, <=, =, !=
> - Can filter on field presence: search fieldname=* (field exists)

---

## Task 4: Classifying Data with the Case Function

### Scenario

The network team wants to classify bandwidth usage into Small, Medium, and Large categories based on bytes transferred.

### Step 4.1: View Bytes Distribution

First, examine the bytes data:

```spl
index=web sourcetype=access_combined
| stats count by bytes
| sort bytes
```

**Expected Results**: A distribution of byte values

### Step 4.2: Create Simple Classification

Use the case function to classify data sizes:

```spl
index=web sourcetype=access_combined
| eval dataSize = case(
    bytes < 2000, "Small",
    bytes >= 2000 AND bytes < 5000, "Medium",
    bytes >= 5000, "Large"
)
| stats count by dataSize
```

**Expected Results**: A table showing the count of events in each category (Small, Medium, Large)

### Step 4.3: Add Default Case

Add a default value for null or unexpected data:

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

**Expected Results**: Includes an "Unknown" category for any data that doesn't match the other conditions

### Step 4.4: Create Multi-Tier Classification

Create a more detailed classification:

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

**Expected Results**: A chart showing the distribution of data sizes across different HTTP status codes

**Save this search as**: `L4S4`

> **Note**: The case function:
> - Evaluates conditions in order
> - Returns the value for the first true condition
> - Use `1=1` as the last condition to create a default/else case
> - Syntax: case(condition1, value1, condition2, value2, ..., defaultCondition, defaultValue)

---

## Task 5: Using the Where Command

### Scenario

Filter results using more complex conditions than the search command allows.

### Step 5.1: Compare Search and Where Commands

Using search command:

```spl
index=web sourcetype=access_combined
| stats avg(bytes) as avg_bytes by action
| search avg_bytes > 5000
```

Using where command:

```spl
index=web sourcetype=access_combined
| stats avg(bytes) as avg_bytes by action
| where avg_bytes > 5000
```

**Expected Results**: Both return the same results, but where offers more capabilities

### Step 5.2: Use Where with String Functions

Use where with string comparison:

```spl
index=web sourcetype=access_combined
| stats count by action, status
| where action="purchase" AND status>=200 AND status<300
```

**Expected Results**: Only shows purchase actions with successful HTTP status codes (2xx)

### Step 5.3: Use Where with Like Operator

Use the LIKE operator for pattern matching:

```spl
index=web sourcetype=access_combined
| stats count by useragent
| where useragent LIKE "%Mobile%"
| sort -count
```

**Expected Results**: Only user agents containing "Mobile"

> **Note**: Differences between search and where:
> - **search**: Uses SPL search syntax, supports wildcards (*)
> - **where**: Uses expression syntax, supports functions like LIKE, isnotnull(), etc.
> - **where**: Generally faster for numeric comparisons
> - **search**: More intuitive for text searching

---

## Challenge Exercise (Optional)

### Challenge 1: Classify HTTP Content Types

Create a classification system for HTTP content types using the if function and LIKE operator:

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

**Expected Results**: A table showing total megabytes transferred by content category

**Additional Steps**:
1. Add more detailed classifications (e.g., separate image/jpeg from image/png)
2. Calculate the percentage of total bandwidth for each category
3. Create a pie chart visualization
4. Add a column showing which category uses the most bandwidth

**Save this search as**: `L4C1`

### Challenge 2: Advanced Transaction Sizing

Create a multi-dimensional classification that considers both bytes and request count:

1. Calculate average bytes per request by client IP
2. Classify IPs into categories based on:
   - Request count (Low: <10, Medium: 10-50, High: >50)
   - Average bytes (Small: <5000, Medium: 5000-10000, Large: >10000)
3. Create a combined category like "High Volume - Large Files"
4. Visualize the distribution in a bubble chart

**Save this search as**: `L4C2`

---

## Summary

In this lab, you learned:
- ✓ How to use eval to create calculated fields and convert units
- ✓ How to perform mathematical operations like division and rounding
- ✓ How to use the search command to filter results after transforming commands
- ✓ How to use the case function to classify data into categories
- ✓ How to use the if function for conditional logic
- ✓ How to use the where command for complex filtering
- ✓ How to use the LIKE operator for pattern matching

## Key Takeaways

1. **eval** is essential for creating new fields and calculating values
2. **round()** function formats numeric data to a specified precision
3. **search** command filters results and can be used multiple times in a pipeline
4. **case** function evaluates conditions in order and returns the first match
5. **where** command offers more advanced filtering capabilities than search
6. **LIKE** operator enables pattern matching with wildcards (%)
7. **1=1** in case function creates a default/else condition
8. Always provide a default case to handle unexpected or null values

---

## Data Sources Used

- **index=network, sourcetype=cisco_wsa_squid**: Web proxy logs with sc_bytes and cs_username for bandwidth analysis
- **index=web, sourcetype=access_combined**: Web access logs with method, bytes, status, and action fields
- **index=security, sourcetype=linux_secure**: Linux authentication logs with src_ip for security analysis

## Next Steps

In Lab 5, you'll learn to correlate events using the transaction command to group related events and analyze user sessions and workflows.

---

**Lab 4 Complete!**
