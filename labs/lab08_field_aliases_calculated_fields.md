# Lab 8: Working with Field Aliases and Calculated Fields

**Splunk Intermediate – Lab Exercises**

> **Note**: This lab should be completed in a non-production environment.

## Lab Description

This lab covers:
- Creating field aliases to normalize field names across sourcetypes
- Using field aliases for data model compliance
- Creating calculated fields to perform automatic computations
- Understanding when to use field aliases vs calculated fields
- Managing and troubleshooting field aliases and calculated fields
- Working with multiple aliases for the same field

## Scenario

You are a Splunk administrator for Buttercup Games. Different data sources use different field names for the same type of data (e.g., "user", "username", "cs_username"). You need to normalize these field names using field aliases. Additionally, you need to create calculated fields to automatically convert bytes to megabytes for bandwidth analysis.

---

## Task 1: Understanding Field Aliases

### Scenario

Multiple sourcetypes contain username information but use different field names. Create field aliases to normalize these field names.

### Step 1.1: Identify Field Name Inconsistencies

Examine different sourcetypes:

```spl
index=network sourcetype=cisco_wsa_squid
| table cs_username
| head 10
```

```spl
index=security sourcetype=linux_secure
| table user
| head 10
```

**Expected Results**: Different field names (cs_username, user) representing the same concept

### Step 1.2: Understand the Problem

Create a search trying to use a common field name:

```spl
(index=network sourcetype=cisco_wsa_squid) OR (index=security sourcetype=linux_secure)
| stats count by user
```

**Expected Results**: Only shows users from linux_secure, missing cisco_wsa_squid users

---

## Task 2: Creating Field Aliases

### Scenario

Create field aliases to map different username fields to a common name.

### Step 2.1: Create Field Alias for Cisco WSA Squid

Create an alias to map cs_username to user:

1. Navigate to **Settings** → **Fields** → **Field aliases**
2. Click **New Field Alias**
3. Configure:
   - Destination app: **search** (or class_Fund2)
   - Name: `cisco_wsa_username_alias`
   - Apply to: **sourcetype: cisco_wsa_squid**
   - Field alias: `user` = `cs_username`
4. Click **Save**

### Step 2.2: Test the Field Alias

Wait ~1 minute for knowledge bundle replication, then test:

```spl
index=network sourcetype=cisco_wsa_squid
| stats count by user
```

**Expected Results**: The user field now appears with values from cs_username

### Step 2.3: Verify Both Field Names Work

Test that both original and alias work:

```spl
index=network sourcetype=cisco_wsa_squid
| table cs_username user
```

**Expected Results**: Both cs_username and user show the same values

**Save this search as**: `L8S1`

> **Note**: Field aliases:
> - Create alternate names for existing fields
> - Both original and alias field names work in searches
> - Do not duplicate data; they reference the same field
> - Are applied at search time

---

## Task 3: Testing Unified Search Across Sourcetypes

### Scenario

Test that the field alias allows you to search across multiple sourcetypes using the common field name.

### Step 3.1: Test Unified Search

Now search across multiple sourcetypes using the common field name:

```spl
(index=network sourcetype=cisco_wsa_squid) OR (index=security sourcetype=linux_secure)
| stats count by user, sourcetype
| sort -count
```

**Expected Results**: Both sourcetypes now return data using the common "user" field

**Save this search as**: `L8S2`

> **Tip**: Field aliases enable:
> - Data normalization across different sources
> - Consistent field naming in dashboards and reports
> - Simplified searches across multiple sourcetypes
> - Common Information Model (CIM) compliance

---

## Task 4: Creating Calculated Fields

### Scenario

Create a calculated field that automatically converts sc_bytes to megabytes for easier analysis.

### Step 4.1: View Raw Bytes Data

First, look at the raw byte values:

```spl
index=network sourcetype=cisco_wsa_squid
| table cs_username sc_bytes
| sort -sc_bytes
| head 10
```

**Expected Results**: Large byte values that are difficult to interpret

### Step 4.2: Create Calculated Field for Megabytes

1. Navigate to **Settings** → **Fields** → **Calculated fields**
2. Click **New Calculated Field**
3. Configure:
   - Destination app: **search** (or class_Fund2)
   - Name: `cisco_wsa_megabytes`
   - Apply to: **sourcetype: cisco_wsa_squid**
   - Eval expression: `round(sc_bytes/(1024*1024), 2)`
   - Save as field: `sc_megabytes`
4. Click **Save**

### Step 4.3: Test the Calculated Field

Wait ~1 minute, then test:

```spl
index=network sourcetype=cisco_wsa_squid
| table cs_username sc_bytes sc_megabytes
| sort -sc_megabytes
```

**Expected Results**: A new field sc_megabytes showing the converted values

### Step 4.4: Use Calculated Field in Statistics

```spl
index=network sourcetype=cisco_wsa_squid
| stats sum(sc_megabytes) as "Total MB" by cs_username
| sort -"Total MB"
| head 10
```

**Expected Results**: Top 10 users by bandwidth usage in megabytes

**Save this search as**: `L8S3`

> **Note**: Calculated fields:
> - Automatically compute values at search time
> - Use eval expression syntax
> - Are applied to all searches for the specified sourcetype
> - Appear in the fields sidebar like extracted fields
> - Can reference other calculated fields

---

## Task 5: Advanced Calculated Field Examples

### Scenario

Create more complex calculated fields for different use cases.

### Step 5.1: Create Duration in Minutes Calculated Field

For transaction analysis, create a field that converts duration to minutes:

1. Navigate to **Settings** → **Fields** → **Calculated fields**
2. Click **New Calculated Field**
3. Configure:
   - Name: `duration_minutes`
   - Apply to: **sourcetype: access_combined_wcookie**
   - Eval expression: `round(duration/60, 1)`
   - Save as field: `duration_minutes`
4. Click **Save**

### Step 5.2: Create Response Time Category Field

Categorize response times:

1. Click **New Calculated Field**
2. Configure:
   - Name: `response_time_category`
   - Apply to: **sourcetype: access_combined**
   - Eval expression: `case(req_time < 0.1, "Fast", req_time >= 0.1 AND req_time < 0.5, "Normal", req_time >= 0.5 AND req_time < 1, "Slow", req_time >= 1, "Very Slow")`
   - Save as field: `response_category`
3. Click **Save**

### Step 5.3: Create Day of Week Field

Extract day of week from timestamp:

1. Click **New Calculated Field**
2. Configure:
   - Name: `day_of_week`
   - Apply to: **sourcetype: access_combined**
   - Eval expression: `strftime(_time, "%A")`
   - Save as field: `day_name`
3. Click **Save**

### Step 5.4: Test All Calculated Fields

```spl
index=web sourcetype=access_combined
| table _time day_name response_category req_time
| head 20
```

**Expected Results**: Events with calculated fields showing day name and response category

---

## Task 6: Supplemental Field Aliases

### Scenario

Create additional field aliases for HTTP method and action fields to ensure consistency.

### Step 6.1: Create HTTP Action Alias

1. Navigate to **Settings** → **Fields** → **Field aliases**
2. Click **New Field Alias**
3. Configure:
   - Name: `web_action_alias`
   - Apply to: **sourcetype: access_combined**
   - Field alias: `http_action` = `action`
4. Click **Save**

### Step 6.2: Create HTTP Method Alias

1. Click **New Field Alias**
2. Configure:
   - Name: `web_method_alias`
   - Apply to: **sourcetype: access_combined**
   - Field alias: `http_method` = `method`
3. Click **Save**

### Step 6.3: Test Supplemental Aliases

```spl
index=web sourcetype=access_combined
| stats count by http_action, http_method
```

**Expected Results**: Statistics using the new alias field names

---

## Task 7: Managing Field Aliases and Calculated Fields

### Scenario

Learn to view, edit, and troubleshoot field aliases and calculated fields.

### Step 7.1: View All Field Aliases

1. Navigate to **Settings** → **Fields** → **Field aliases**
2. Review all aliases
3. Check which app they belong to
4. Verify permissions

### Step 7.2: View All Calculated Fields

1. Navigate to **Settings** → **Fields** → **Calculated fields**
2. Review all calculated fields
3. Check the eval expressions
4. Verify they're applied to correct sourcetypes

### Step 7.3: Test Field Availability

Verify fields appear in searches:

```spl
index=network sourcetype=cisco_wsa_squid
| fieldsummary
| search field=user OR field=cs_username OR field=sc_megabytes
```

**Expected Results**: Shows field statistics confirming fields are available

### Step 7.4: Troubleshoot Missing Fields

If calculated fields don't appear:

1. Check the sourcetype matches exactly
2. Verify eval expression is valid
3. Wait for knowledge bundle replication
4. Check app context and permissions
5. Look for eval syntax errors

```spl
index=network sourcetype=cisco_wsa_squid
| eval test_calc = round(sc_bytes/(1024*1024), 2)
| table sc_bytes test_calc sc_megabytes
```

**Expected Results**: Compare manual eval with calculated field

---

## Challenge Exercise (Optional)

### Challenge 1: Create Unified Security Field Aliases

Normalize security-related fields across all sourcetypes:

1. Create aliases for source IP fields:
   - src, src_ip, source_ip, clientip → all map to "source_ip"
2. Create aliases for destination IP fields:
   - dest, dest_ip, destination_ip → all map to "dest_ip"
3. Create aliases for action fields:
   - vendor_action, action, activity → all map to "action"

Test with:
```spl
(index=security) OR (index=web) OR (index=network)
| stats count by source_ip, action
| sort -count
```

**Save this search as**: `L8C1`

### Challenge 2: Create Calculated Performance Metrics

Create a set of calculated fields for web performance analysis:

1. **throughput**: `(bytes/req_time)` - bytes per second
2. **efficiency_score**: Ratio of successful to total requests
3. **peak_hour**: Classify hours as peak (9-5) or off-peak
4. **request_size_category**: Classify bytes as small/medium/large

Create a dashboard showing:
- Average throughput by hour
- Efficiency score by day
- Request distribution by size category

**Save this search as**: `L8C2`

---

## Summary

In this lab, you learned:
- ✓ How to create field aliases to normalize field names across sourcetypes
- ✓ How to create multiple aliases for the same field
- ✓ How to create calculated fields using eval expressions
- ✓ The differences between field aliases and calculated fields
- ✓ How to manage, edit, and troubleshoot field aliases and calculated fields
- ✓ Best practices for field normalization and data consistency

## Key Takeaways

1. **Field aliases** create alternate names for existing fields without duplicating data
2. **Both original and alias names** work in searches after creating an alias
3. **Calculated fields** automatically compute values using eval expressions
4. **Field aliases** are ideal for normalizing field names across different sourcetypes
5. **Calculated fields** are ideal for recurring computations you want to automate
6. **Wait ~1 minute** after creating for knowledge bundle replication
7. **Permissions** control visibility (Private, App, Global)
8. Field aliases and calculated fields are **search-time operations**
9. Use calculated fields to enforce **Common Information Model (CIM)** compliance

---

## Data Sources Used

- **index=network, sourcetype=cisco_wsa_squid**: Web proxy logs with cs_username and sc_bytes fields
- **index=security, sourcetype=linux_secure**: Linux authentication logs with user field
- **index=web, sourcetype=access_combined**: Web access logs with method, action, and req_time fields
- **index=web, sourcetype=access_combined_wcookie**: Web logs with duration for transaction analysis

## Next Steps

In Lab 9, you'll learn to create tags and event types to categorize and classify events for easier searching and reporting.

---

**Lab 8 Complete!**
