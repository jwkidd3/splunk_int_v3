# Lab 6: Introduction to Lookups

**Splunk Intermediate – Lab Exercises**

## Objectives

- Create and upload CSV lookup files
- Use lookup command to enrich data
- Create lookup definitions
- Configure automatic lookups
- Use inputlookup and outputlookup commands

---

## Task 1: View Data Without Lookups

```spl
index=web sourcetype=access_combined
| stats count by status
| sort status
```

Status codes appear without descriptions.

---

## Task 2: Create Lookup File

### Step 1: Create http_status_lookup.csv

```csv
status,status_description,status_type
200,OK,Success
201,Created,Success
301,Moved Permanently,Redirection
302,Found,Redirection
400,Bad Request,Client Error
401,Unauthorized,Client Error
403,Forbidden,Client Error
404,Not Found,Client Error
500,Internal Server Error,Server Error
502,Bad Gateway,Server Error
503,Service Unavailable,Server Error
```

### Step 2: Upload to Splunk

1. **Settings** → **Lookups** → **Lookup table files**
2. **New Lookup Table File**
3. Upload `http_status_lookup.csv`

### Step 3: Verify Contents

```spl
| inputlookup http_status_lookup.csv
```

**Save as**: `L6S1`

---

## Task 3: Use Lookup Command

### Step 1: Basic Lookup

```spl
index=web sourcetype=access_combined
| lookup http_status_lookup.csv status OUTPUT status_description status_type
| table _time clientip status status_description status_type
```

### Step 2: Aggregate

```spl
index=web sourcetype=access_combined
| lookup http_status_lookup.csv status OUTPUT status_description status_type
| stats count by status, status_description, status_type
| sort status
```

### Step 3: Filter Using Lookup Fields

```spl
index=web sourcetype=access_combined
| lookup http_status_lookup.csv status OUTPUT status_description status_type
| search status_type="Client Error" OR status_type="Server Error"
| stats count by status, status_description
| sort -count
```

**Save as**: `L6S2`

---

## Task 4: Automatic Lookup

### Step 1: Create Lookup Definition

1. **Settings** → **Lookups** → **Lookup definitions**
2. **New Lookup Definition**
3. Configure:
   - Name: `http_status_lookup`
   - Type: File-based
   - Lookup file: `http_status_lookup.csv`

### Step 2: Configure Automatic Lookup

1. **Settings** → **Lookups** → **Automatic lookups**
2. **New Automatic Lookup**
3. Configure:
   - Name: `auto_http_status_lookup`
   - Lookup table: `http_status_lookup`
   - Apply to sourcetype: `access_combined`
   - Lookup input: `status`
   - Lookup output: `status_description, status_type`

### Step 3: Test

Wait ~1 minute, then:

```spl
index=web sourcetype=access_combined
| table _time status status_description status_type
```

Fields appear automatically without lookup command.

### Step 4: Verify

```spl
index=web sourcetype=access_combined
| stats count by status_description
| sort -count
```

**Save as**: `L6S3`

---

## Task 5: Product Lookup

### Step 1: Create product_lookup.csv

```csv
productId,product_name,category
MB-1234,Mediocre Kingdoms,STRATEGY
FS-5678,Final Sequel,ACTION
PZ-9012,Puzzle Fever,SIMULATION
BG-3456,Battle Galaxy,ACTION
RC-7890,Racing Rivals,SPORTS
SG-2345,Space Gladiators,ACTION
DB-6789,Dragon Battle,STRATEGY
SF-1357,Super Fighter,ACTION
```

### Step 2: Upload and Define

1. Upload via **Settings** → **Lookups** → **Lookup table files**
2. Create definition: `product_lookup`

### Step 3: Use in Search

```spl
index=web sourcetype=access_combined action=purchase productId=*
| lookup product_lookup productId OUTPUT product_name category
| stats sum(price) as revenue by product_name, category
| sort -revenue
```

**Save as**: `L6S4`

---

## Task 6: Outputlookup

### Step 1: Create Dynamic Lookup

```spl
index=network sourcetype=cisco_wsa_squid
| stats sum(sc_bytes) as total_bytes by cs_username
| sort -total_bytes
| head 10
| outputlookup top_users_by_bandwidth.csv
```

### Step 2: Verify

```spl
| inputlookup top_users_by_bandwidth.csv
```

### Step 3: Use Dynamic Lookup

```spl
index=network sourcetype=cisco_wsa_squid
| lookup top_users_by_bandwidth.csv cs_username OUTPUT total_bytes as baseline_usage
| where isnotnull(baseline_usage)
| stats sum(sc_bytes) as current_usage, max(baseline_usage) as baseline by cs_username
```

**Save as**: `L6S5`

---

## Challenge: Vendor Region Lookup

Create lookup mapping VendorID ranges to regions and aggregate sales by region.

**Save as**: `L6C1`

---

## Summary

- Lookups add external data to events
- CSV files are common lookup format
- Lookup definitions make files reusable
- Automatic lookups apply enrichment automatically
- inputlookup reads lookup data as results
- outputlookup creates/updates lookup files
- Syntax: `lookup <name> <input-field> OUTPUT <output-fields>`

---

**Lab 6 Complete!**
