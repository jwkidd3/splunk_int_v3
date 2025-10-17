# Lab 8: Field Aliases and Calculated Fields

**Splunk Intermediate – Lab Exercises**

## Objectives

- Create field aliases to normalize field names
- Create calculated fields with eval expressions
- Understand when to use each technique
- Manage aliases and calculated fields

---

## Task 1: Identify Inconsistencies

### Different Field Names

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

Different fields (cs_username, user) represent same concept.

### Problem

```spl
(index=network sourcetype=cisco_wsa_squid) OR (index=security sourcetype=linux_secure)
| stats count by user
```

Only shows linux_secure users - missing cisco users.

---

## Task 2: Create Field Alias

### Step 1: Create Alias

1. **Settings** → **Fields** → **Field aliases**
2. **New Field Alias**
3. Configure:
   - Name: `cisco_wsa_username_alias`
   - Apply to sourcetype: `cisco_wsa_squid`
   - Field alias: `user` = `cs_username`

### Step 2: Test

Wait ~1 minute:

```spl
index=network sourcetype=cisco_wsa_squid
| stats count by user
```

### Step 3: Verify Both Names Work

```spl
index=network sourcetype=cisco_wsa_squid
| table cs_username user
```

Both fields show same values.

**Save as**: `L8S1`

---

## Task 3: Unified Search

```spl
(index=network sourcetype=cisco_wsa_squid) OR (index=security sourcetype=linux_secure)
| stats count by user, sourcetype
| sort -count
```

Both sourcetypes now return data using common "user" field.

**Save as**: `L8S2`

---

## Task 4: Calculated Fields

### Step 1: View Raw Bytes

```spl
index=network sourcetype=cisco_wsa_squid
| table cs_username sc_bytes
| sort -sc_bytes
| head 10
```

### Step 2: Create Calculated Field

1. **Settings** → **Fields** → **Calculated fields**
2. **New Calculated Field**
3. Configure:
   - Name: `cisco_wsa_megabytes`
   - Apply to sourcetype: `cisco_wsa_squid`
   - Eval expression: `round(sc_bytes/(1024*1024), 2)`
   - Save as field: `sc_megabytes`

### Step 3: Test

Wait ~1 minute:

```spl
index=network sourcetype=cisco_wsa_squid
| table cs_username sc_bytes sc_megabytes
| sort -sc_megabytes
```

### Step 4: Use in Stats

```spl
index=network sourcetype=cisco_wsa_squid
| stats sum(sc_megabytes) as "Total MB" by cs_username
| sort -"Total MB"
| head 10
```

**Save as**: `L8S3`

---

## Task 5: Advanced Calculated Fields

### Response Category

1. **Settings** → **Fields** → **Calculated fields**
2. **New Calculated Field**
3. Configure:
   - Name: `response_time_category`
   - Apply to sourcetype: `access_combined`
   - Expression: `case(req_time < 0.1, "Fast", req_time >= 0.1 AND req_time < 0.5, "Normal", req_time >= 0.5 AND req_time < 1, "Slow", req_time >= 1, "Very Slow")`
   - Field name: `response_category`

### Day of Week

1. **New Calculated Field**
2. Configure:
   - Name: `day_of_week`
   - Apply to sourcetype: `access_combined`
   - Expression: `strftime(_time, "%A")`
   - Field name: `day_name`

### Test

```spl
index=web sourcetype=access_combined
| table _time day_name response_category req_time
| head 20
```

**Save as**: `L8S4`

---

## Task 6: Manage Fields

### View All Aliases

1. **Settings** → **Fields** → **Field aliases**
2. Review all aliases
3. Check app and permissions

### View All Calculated Fields

1. **Settings** → **Fields** → **Calculated fields**
2. Review all calculated fields
3. Check eval expressions

### Verify Availability

```spl
index=network sourcetype=cisco_wsa_squid
| fieldsummary
| search field=user OR field=cs_username OR field=sc_megabytes
```

---

## Challenge: Unified Security Fields

Normalize security fields across all sourcetypes:
1. Source IP: src, src_ip, source_ip, clientip → `source_ip`
2. Dest IP: dest, dest_ip, destination_ip → `dest_ip`
3. Action: vendor_action, action, activity → `action`

Test:
```spl
(index=security) OR (index=web) OR (index=network)
| stats count by source_ip, action
| sort -count
```

**Save as**: `L8C1`

---

## Summary

- Field aliases create alternate names without duplicating data
- Both original and alias names work in searches
- Calculated fields compute values using eval expressions
- Aliases normalize field names across sourcetypes
- Calculated fields automate recurring computations
- Wait ~1 minute for knowledge bundle replication
- Manage via Settings → Fields

---

**Lab 8 Complete!**
