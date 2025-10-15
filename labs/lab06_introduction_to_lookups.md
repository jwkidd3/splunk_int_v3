# Lab 6: Introduction to Lookups

**Splunk Intermediate – Lab Exercises**

> **Note**: This lab should be completed in a non-production environment.

## Lab Description

This lab covers:
- Understanding lookup tables and their purpose
- Using the lookup command to enrich data
- Creating and configuring lookup definitions
- Using automatic lookups
- Working with CSV lookup files
- Enriching HTTP status codes with descriptions
- Using inputlookup and outputlookup commands

## Scenario

You are a Splunk administrator for Buttercup Games. The operations team receives web access logs with HTTP status codes (like 200, 404, 500) but needs human-readable descriptions. The sales team wants to enrich product IDs with product names and categories. You'll use lookups to add this contextual information to search results.

---

## Task 1: Understanding Lookup Tables

### Scenario

Before creating lookups, understand what lookup tables are and how they work in Splunk.

### Step 1.1: View HTTP Status Codes Without Lookups

Run a search showing HTTP status codes:

```spl
index=web sourcetype=access_combined
| stats count by status
| sort status
```

**Expected Results**: A table showing status codes (200, 404, 500, etc.) without descriptions

### Step 1.2: Understand Lookup Purpose

Lookups allow you to:
- Add descriptive information to codes (e.g., 404 → "Not Found")
- Enrich IP addresses with geographic data
- Map product IDs to product names
- Add any external reference data to events

### Step 1.3: View Sample Lookup File Structure

A typical HTTP status lookup CSV file looks like this:

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

**Key Points**:
- First row contains field names (headers)
- First field (status) is the lookup key
- Additional fields provide enrichment data

---

## Task 2: Creating a Lookup File

### Scenario

Create a lookup file to map HTTP status codes to descriptions.

### Step 2.1: Create HTTP Status Lookup File

1. Navigate to **Settings** → **Lookups** → **Lookup table files**
2. Click **New Lookup Table File**
3. Configure:
   - Destination app: **Search & Reporting** (or your class app)
   - Upload file: Create a CSV file named `http_status_lookup.csv` with the content above
4. Click **Save**

Alternatively, if the file already exists in `$SPLUNK_HOME/etc/apps/search/lookups/`, you can reference it directly.

### Step 2.2: Verify Lookup File Contents

Use inputlookup to view the lookup table:

```spl
| inputlookup http_status_lookup.csv
```

**Expected Results**: All rows from the lookup table are displayed

**Save this search as**: `L6S1`

> **Note**: The inputlookup command:
> - Reads data from a lookup file
> - Can be used as a data source (starts with pipe |)
> - Useful for verifying lookup content
> - Returns lookup data as search results

---

## Task 3: Using the Lookup Command

### Scenario

Manually enrich web access logs with status code descriptions using the lookup command.

### Step 3.1: Perform Basic Lookup

Use the lookup command to add descriptions:

```spl
index=web sourcetype=access_combined
| lookup http_status_lookup.csv status OUTPUT status_description status_type
| table _time clientip status status_description status_type
```

**Expected Results**: Web events now include status_description and status_type fields

### Step 3.2: Aggregate with Lookup Fields

Create statistics using the enriched data:

```spl
index=web sourcetype=access_combined
| lookup http_status_lookup.csv status OUTPUT status_description status_type
| stats count by status, status_description, status_type
| sort status
```

**Expected Results**: Count of events by status code with descriptions

### Step 3.3: Filter Using Lookup Fields

Filter results based on lookup fields:

```spl
index=web sourcetype=access_combined
| lookup http_status_lookup.csv status OUTPUT status_description status_type
| search status_type="Client Error" OR status_type="Server Error"
| stats count by status, status_description
| sort -count
```

**Expected Results**: Only error status codes (4xx and 5xx) with their counts

**Save this search as**: `L6S2`

> **Tip**: The lookup command syntax:
> - `lookup <lookup-file> <input-field> OUTPUT <output-field1> <output-field2>`
> - Must specify which fields to retrieve from the lookup
> - Can lookup multiple fields at once

---

## Task 4: Creating an Automatic Lookup

### Scenario

Configure an automatic lookup so that status descriptions are always added without manually using the lookup command.

### Step 4.1: Create Lookup Definition

1. Navigate to **Settings** → **Lookups** → **Lookup definitions**
2. Click **New Lookup Definition**
3. Configure:
   - Destination app: **Search & Reporting** (or your class app)
   - Name: `http_status_lookup`
   - Type: **File-based**
   - Lookup file: `http_status_lookup.csv`
4. Click **Save**

### Step 4.2: Configure Automatic Lookup

1. Navigate to **Settings** → **Lookups** → **Automatic lookups**
2. Click **New Automatic Lookup**
3. Configure:
   - Destination app: **Search & Reporting** (or your class app)
   - Name: `auto_http_status_lookup`
   - Lookup table: `http_status_lookup`
   - Apply to: **sourcetype**
   - Named: `access_combined`
   - Lookup input fields: `status`
   - Lookup output fields: `status_description, status_type`
4. Click **Save**

### Step 4.3: Test Automatic Lookup

Now search without the lookup command:

```spl
index=web sourcetype=access_combined
| table _time status status_description status_type
```

**Expected Results**: The status_description and status_type fields are automatically populated

### Step 4.4: Verify Automatic Lookup is Working

```spl
index=web sourcetype=access_combined
| stats count by status_description
| sort -count
```

**Expected Results**: Statistics by status description without manually calling the lookup command

**Save this search as**: `L6S3`

> **Note**: Automatic lookups:
> - Apply lookups automatically to specified sourcetypes or sources
> - Eliminate the need for manual lookup commands
> - Run at search time, not index time
> - Can impact search performance if overused

---

## Task 5: Creating Product Lookup

### Scenario

Create a lookup to enrich product IDs with product names and categories.

### Step 5.1: Create Product Lookup File

Create a CSV file named `product_lookup.csv`:

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

Upload this file to Splunk:
1. Navigate to **Settings** → **Lookups** → **Lookup table files**
2. Click **New Lookup Table File**
3. Upload `product_lookup.csv`

### Step 5.2: Create Product Lookup Definition

1. Navigate to **Settings** → **Lookups** → **Lookup definitions**
2. Click **New Lookup Definition**
3. Configure:
   - Name: `product_lookup`
   - Type: **File-based**
   - Lookup file: `product_lookup.csv`
4. Click **Save**

### Step 5.3: Use Product Lookup

Enrich purchase data with product information:

```spl
index=web sourcetype=access_combined action=purchase productId=*
| lookup product_lookup productId OUTPUT product_name category
| stats sum(price) as revenue by product_name, category
| sort -revenue
```

**Expected Results**: Purchase data enriched with product names and categories

**Save this search as**: `L6S4`

---

## Task 6: Using Outputlookup

### Scenario

Create a dynamic lookup table by outputting search results to a lookup file.

### Step 6.1: Generate Top Users Lookup

Create a lookup of top users by bandwidth:

```spl
index=network sourcetype=cisco_wsa_squid
| stats sum(sc_bytes) as total_bytes by cs_username
| sort -total_bytes
| head 10
| outputlookup top_users_by_bandwidth.csv
```

**Expected Results**: Creates a new lookup file with the top 10 users

### Step 6.2: Verify the Created Lookup

View the created lookup:

```spl
| inputlookup top_users_by_bandwidth.csv
```

**Expected Results**: Displays the top 10 users with their bandwidth usage

### Step 6.3: Use the Dynamic Lookup

Use the generated lookup in another search:

```spl
index=network sourcetype=cisco_wsa_squid
| lookup top_users_by_bandwidth.csv cs_username OUTPUT total_bytes as baseline_usage
| where isnotnull(baseline_usage)
| stats sum(sc_bytes) as current_usage, max(baseline_usage) as baseline by cs_username
```

**Expected Results**: Compares current usage to baseline for top users

**Save this search as**: `L6S5`

> **Note**: outputlookup command:
> - Creates or updates a lookup file from search results
> - Useful for creating dynamic reference tables
> - Can be scheduled to update lookups regularly
> - Use `create_empty=false` to prevent creating empty files

---

## Challenge Exercise (Optional)

### Challenge 1: Create Vendor Region Lookup

Create a lookup that maps VendorID ranges to regions:

1. Create `vendor_region_lookup.csv`:
```csv
vendor_id_min,vendor_id_max,region
1000,2999,USA
3000,3999,Canada
4000,4999,Latin America
5000,6999,Europe
7000,8999,Asia Pacific
9000,9900,Africa
9901,9999,Other
```

2. Create a search that:
   - Reads vendor_sales data
   - Uses eval to match VendorID to the correct region
   - Aggregates sales by region
   - Creates a choropleth map of sales by region

**Hint**: Use eval with case() to match VendorID ranges

**Save this search as**: `L6C1`

### Challenge 2: Create and Maintain User Activity Lookup

Create an automated lookup maintenance system:

1. Create a scheduled search that runs every hour
2. Identifies users with suspicious activity (high failed login count)
3. Outputs to a lookup file: `suspicious_users.csv`
4. Create alerts that check if current authentication attempts match suspicious users

**Requirements**:
- Schedule: Every hour
- Threshold: More than 5 failed logins
- Output: username, failed_count, last_seen
- Create an alert that triggers when a suspicious user attempts login

**Save this search as**: `L6C2`

---

## Summary

In this lab, you learned:
- ✓ What lookups are and why they're useful for data enrichment
- ✓ How to create and upload lookup files in CSV format
- ✓ How to use the lookup command to manually enrich data
- ✓ How to create lookup definitions for reusable lookups
- ✓ How to configure automatic lookups for specific sourcetypes
- ✓ How to use inputlookup to view lookup contents
- ✓ How to use outputlookup to create dynamic lookup tables

## Key Takeaways

1. **Lookups** add contextual information from external files to your events
2. **CSV files** are the most common format for lookup tables
3. **Lookup definitions** make lookup files reusable across searches
4. **Automatic lookups** apply enrichment automatically at search time
5. **inputlookup** reads lookup data as search results
6. **outputlookup** creates or updates lookup files from search results
7. **Lookup syntax**: `lookup <lookup-name> <input-field> OUTPUT <output-fields>`
8. Automatic lookups eliminate repetitive lookup commands but can impact performance

---

## Data Sources Used

- **index=web, sourcetype=access_combined**: Web access logs with HTTP status codes
- **index=web, sourcetype=access_combined_wcookie**: Web logs with productId for product lookup enrichment
- **index=network, sourcetype=cisco_wsa_squid**: Web proxy logs with cs_username and sc_bytes
- **index=web, sourcetype=vendor_sales**: Retail sales data with VendorID for region mapping

## Next Steps

In Lab 7, you'll learn to create and manage custom field extractions using the Field Extractor, allowing you to extract structured data from unstructured log events.

---

**Lab 6 Complete!**
