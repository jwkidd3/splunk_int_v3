# Lab 0: Data Loading Activity

**Splunk Intermediate – Lab Exercises**

> **Note**: This lab must be completed before starting Lab 1. Complete this in a non-production environment.

## Lab Description

This lab covers:
- Creating 4 indexes (web, security, network, games)
- Uploading training data files to appropriate indexes
- Uploading lookup files for data enrichment
- Verifying data was loaded correctly

## Scenario

You are setting up a Splunk training environment for Buttercup Games. Before the course begins, you need to load all training data into Splunk using **4 separate indexes**.

---

## Overview

This guide provides step-by-step instructions for loading Buttercup Games training data into Splunk using **4 separate indexes**.

---

## Prerequisites

- Splunk Enterprise running (http://localhost:8000)
- Admin access (username: `admin`, password: `password`)
- Generated data files in the `data/` directory

If you haven't generated the data yet:
```bash
python scripts/data-generators/generate_buttercup_data.py
```

---

## Index Structure Overview

The course uses **4 dedicated indexes**:

| Index | Purpose | Data Files | Event Count |
|-------|---------|------------|-------------|
| **web** | Online store and vendor sales | web_access.log, vendor_sales.csv | ~20,000 |
| **security** | Authentication and security | linux_secure.log | ~2,000 |
| **network** | Proxy and firewall logs | cisco_wsa_squid.log | ~3,000 |
| **games** | Game telemetry | simcube_beta.csv | ~2,000 |

**Total**: ~27,000 events

---

## Step 1: Create Indexes in Splunk

### Method 1: Via Splunk Web UI

1. Navigate to **Settings** → **Indexes**
2. Click **New Index** (top right)
3. Create each index:

#### Index 1: web
- **Index Name**: `web`
- **Index Data Type**: Events
- **Max Size**: 500MB (default is fine for training)
- Click **Save**

#### Index 2: security
- **Index Name**: `security`
- **Index Data Type**: Events
- **Max Size**: 100MB
- Click **Save**

#### Index 3: network
- **Index Name**: `network`
- **Index Data Type**: Events
- **Max Size**: 100MB
- Click **Save**

#### Index 4: games
- **Index Name**: `games`
- **Index Data Type**: Events
- **Max Size**: 100MB
- Click **Save**

### Method 2: Via CLI (indexes.conf)

Add to `$SPLUNK_HOME/etc/system/local/indexes.conf`:

```ini
[web]
homePath = $SPLUNK_DB/web/db
coldPath = $SPLUNK_DB/web/colddb
thawedPath = $SPLUNK_DB/web/thaweddb
maxTotalDataSizeMB = 500

[security]
homePath = $SPLUNK_DB/security/db
coldPath = $SPLUNK_DB/security/colddb
thawedPath = $SPLUNK_DB/security/thaweddb
maxTotalDataSizeMB = 100

[network]
homePath = $SPLUNK_DB/network/db
coldPath = $SPLUNK_DB/network/colddb
thawedPath = $SPLUNK_DB/network/thaweddb
maxTotalDataSizeMB = 100

[games]
homePath = $SPLUNK_DB/games/db
coldPath = $SPLUNK_DB/games/colddb
thawedPath = $SPLUNK_DB/games/thaweddb
maxTotalDataSizeMB = 100
```

Then restart Splunk: `splunk restart`

---

## Step 2: Upload Data to index=web

### File 1: web_access.log → index=web

This file contains web access logs with session tracking and product information.

**Upload Steps**:

1. **Settings** → **Add Data** → **Upload**
2. **Select File**: `data/web_access.log`
3. **Set Source Type**:
   - Click **Select Source Type**
   - Select **Web** category
   - Choose **access_combined_wcookie** from the list
   - (Or select **Manual** and type `access_combined_wcookie`)
4. **Input Settings**:
   - **Host**: Leave as default (`localhost` or your hostname)
   - **Index**: Select **web**
5. **Review**: Verify preview shows events with fields like `clientip`, `method`, `status`, `JSESSIONID`, `productId`
6. **Submit**

**Expected Result**: ~15,000 events with sourcetype=access_combined_wcookie in index=web

#### Alternative Sourcetype for Same File

Some labs use **access_combined** (without cookie) for the same data. To add this:

1. **Settings** → **Add Data** → **Upload**
2. **Select File**: `data/web_access.log` (same file)
3. **Set Source Type**: `access_combined`
4. **Input Settings**: Index = **web**
5. **Submit**

**Result**: Same data now searchable as both `sourcetype=access_combined_wcookie` and `sourcetype=access_combined`

---

### File 2: vendor_sales.csv → index=web

Retail store sales data across regions.

**Upload Steps**:

1. **Settings** → **Add Data** → **Upload**
2. **Select File**: `data/vendor_sales.csv`
3. **Set Source Type**:
   - Click **Manual**
   - Type: `vendor_sales`
   - Check **Indexed Extractions**: CSV
4. **Input Settings**:
   - **Index**: Select **web**
5. **Review**: Verify fields like `VendorID`, `VendorCountry`, `productId`, `price`, `quantity`
6. **Submit**

**Expected Result**: ~5,000 events with sourcetype=vendor_sales in index=web

---

## Step 3: Upload Data to index=security

### File: linux_secure.log → index=security

Linux authentication logs (SSH, failed passwords, session events).

**Upload Steps**:

1. **Settings** → **Add Data** → **Upload**
2. **Select File**: `data/linux_secure.log`
3. **Set Source Type**:
   - Select **Operating System** category
   - Choose **linux_secure**
4. **Input Settings**:
   - **Index**: Select **security**
5. **Review**: Verify events show authentication messages
6. **Submit**

**Expected Result**: ~2,000 events with sourcetype=linux_secure in index=security

---

## Step 4: Upload Data to index=network

### File: cisco_wsa_squid.log → index=network

Cisco Web Security Appliance / Squid proxy logs.

**Upload Steps**:

1. **Settings** → **Add Data** → **Upload**
2. **Select File**: `data/cisco_wsa_squid.log`
3. **Set Source Type**:
   - Click **Manual**
   - Type: `cisco_wsa_squid`
4. **Input Settings**:
   - **Index**: Select **network**
5. **Review**: Verify fields like `src_ip`, `cs_username`, `sc_bytes`, `status`, `url`
6. **Submit**

**Expected Result**: ~3,000 events with sourcetype=cisco_wsa_squid in index=network

---

## Step 5: Upload Data to index=games

### File: simcube_beta.csv → index=games

Game telemetry data for SimCube Beta (comma-delimited).

**Upload Steps**:

1. **Settings** → **Add Data** → **Upload**
2. **Select File**: `data/simcube_beta.csv`
3. **Set Source Type**:
   - Click **Manual**
   - Type: `SimCubeBeta`
   - Check **Indexed Extractions**: CSV
4. **Input Settings**:
   - **Index**: Select **games**
5. **Review**: Verify fields like `user`, `CharacterName`, `action`, `role`, `version`
6. **Submit**

**Expected Result**: ~2,000 events with sourcetype=SimCubeBeta in index=games

---

## Step 6: Upload Lookup Files

Lookup files don't go into indexes. They're uploaded as static reference files.

### Lookup 1: http_status_lookup.csv

**Upload Steps**:

1. **Settings** → **Lookups** → **Lookup table files**
2. Click **New Lookup Table File**
3. **Destination app**: Select **Search & Reporting** (or your class app)
4. **Choose File**: `data/http_status_lookup.csv`
5. **Destination filename**: `http_status_lookup.csv`
6. **Save**

### Lookup 2: product_catalog.csv

**Upload Steps**:

1. **Settings** → **Lookups** → **Lookup table files**
2. Click **New Lookup Table File**
3. **Destination app**: Select **Search & Reporting** (or your class app)
4. **Choose File**: `data/product_catalog.csv`
5. **Destination filename**: `product_catalog.csv`
6. **Save**

---

## Step 7: Verify Data Loading

Run this search to verify all data is loaded correctly:

```spl
| tstats count where index=* by index, sourcetype
| sort index sourcetype
```

### Expected Results Table

| index | sourcetype | count |
|-------|------------|-------|
| games | SimCubeBeta | ~2,000 |
| network | cisco_wsa_squid | ~3,000 |
| security | linux_secure | ~2,000 |
| web | access_combined | ~15,000 |
| web | access_combined_wcookie | ~15,000 |
| web | vendor_sales | ~5,000 |

**Note**: `access_combined` and `access_combined_wcookie` may show the same count if you uploaded the same file twice with different sourcetypes.

---

## Step 8: Verify Specific Indexes

### Verify index=web

```spl
index=web | stats count by sourcetype
```

Expected:
- access_combined or access_combined_wcookie: ~15,000
- vendor_sales: ~5,000

### Verify index=security

```spl
index=security | stats count by sourcetype
```

Expected:
- linux_secure: ~2,000

### Verify index=network

```spl
index=network | stats count by sourcetype
```

Expected:
- cisco_wsa_squid: ~3,000

### Verify index=games

```spl
index=games | stats count by sourcetype
```

Expected:
- SimCubeBeta: ~2,000

---

## Step 9: Test Key Fields

### Test Web Index (Products)

```spl
index=web sourcetype=access_combined_wcookie productId=*
| stats count by productId, product_name
| head 10
```

Should show products like "Mediocre Kingdoms", "World of Cheese", "Grand Theft Scooter", etc.

### Test Web Index (Vendor Sales)

```spl
index=web sourcetype=vendor_sales
| stats sum(price) as total_sales by VendorCountry
| sort -total_sales
```

Should show sales by country (USA, Canada, Germany, France, etc.)

### Test Security Index

```spl
index=security sourcetype=linux_secure "failed password"
| stats count by user
```

Should show failed login attempts by username.

### Test Network Index

```spl
index=network sourcetype=cisco_wsa_squid
| stats sum(sc_bytes) as total_bytes by cs_username
| eval total_MB = round(total_bytes/1024/1024, 2)
| fields cs_username total_MB
| sort -total_MB
```

Should show proxy usage by username in megabytes.

### Test Games Index

```spl
index=games sourcetype=SimCubeBeta
| stats count by action, role
```

Should show game actions (login, move, fight, etc.) by character role (warrior, mage, archer).

---

## Step 10: Test Lookups

### Test HTTP Status Lookup

```spl
| inputlookup http_status_lookup.csv
| head 10
```

Should show HTTP status codes (200, 404, 500, etc.) with descriptions.

### Test Product Catalog Lookup

```spl
| inputlookup product_catalog.csv
| head 10
```

Should show product details (productId, product_name, categoryId, price, etc.)

---

## Troubleshooting

### Problem: No events found in index

**Check**:
1. Verify index was created: **Settings** → **Indexes**
2. Check time range in search: Try **All time**
3. Verify file was uploaded to correct index
4. Check for ingestion errors: **Settings** → **Data inputs** → **Files & Directories**

### Problem: Wrong sourcetype assigned

**Fix**:
1. Delete the data: `index=web sourcetype=incorrect_type | delete`
2. Re-upload with correct sourcetype

### Problem: Fields not extracted

**Check**:
1. For CSV files: Ensure **Indexed Extractions = CSV** was selected
2. For logs: Splunk should auto-extract fields based on sourcetype
3. Verify sourcetype: `index=web | stats count by sourcetype`

### Problem: Lookup files not found

**Fix**:
1. Verify upload: **Settings** → **Lookups** → **Lookup table files**
2. Check app context: Lookup must be in the app you're using
3. Check permissions: Set to **Global** or **App** level

---

## Index Summary Table

| Index | Files | Sourcetypes | Labs Used In |
|-------|-------|-------------|--------------|
| **web** | web_access.log, vendor_sales.csv | access_combined, access_combined_wcookie, vendor_sales | Labs 1-6, 8-12 |
| **security** | linux_secure.log | linux_secure | Labs 1-4, 7-9, 11 |
| **network** | cisco_wsa_squid.log | cisco_wsa_squid | Labs 2-4, 8-9 |
| **games** | simcube_beta.csv | SimCubeBeta | Lab 7 |

---

## Key Fields by Index

### index=web (access_combined_wcookie)
- **Session**: JSESSIONID
- **Request**: clientip, method, url, status, bytes, req_time
- **Products**: action, productId, product_name, categoryId, price

### index=web (vendor_sales)
- **Vendor**: VendorID, VendorCountry, VendorStateProvince
- **Product**: productId, product_name, categoryId
- **Sale**: price, quantity

### index=security (linux_secure)
- **Auth**: user, src_ip, vendor_action
- **Events**: "session opened", "failed password", "authentication failure", "invalid user"

### index=network (cisco_wsa_squid)
- **Connection**: src_ip, cs_username
- **Request**: method, url, status, http_content_type
- **Traffic**: sc_bytes, usage

### index=games (SimCubeBeta)
- **Player**: user, CharacterName, role
- **Game**: action, version, time, src

---

## Quick Reference: SPL by Index

```spl
# Web traffic
index=web sourcetype=access_combined_wcookie

# Vendor sales
index=web sourcetype=vendor_sales

# Security events
index=security sourcetype=linux_secure

# Proxy logs
index=network sourcetype=cisco_wsa_squid

# Game telemetry
index=games sourcetype=SimCubeBeta

# All Buttercup Games data
index=web OR index=security OR index=network OR index=games

# Alternative (all indexes)
index IN (web, security, network, games)
```

---

## Data Retention

For this training course, data retention is not critical. However, if you need to reset:

### Clear All Training Data

```spl
# Delete all events from web index
index=web | delete

# Delete all events from security index
index=security | delete

# Delete all events from network index
index=network | delete

# Delete all events from games index
index=games | delete
```

**Warning**: This permanently deletes data. Only use in training environments.

### Regenerate Fresh Data

```bash
# Generate new data
python scripts/data-generators/generate_buttercup_data.py

# Follow this guide again to reload
```

---

## Next Steps

After loading all data:

1. **Verify setup** with queries above
2. **Open Lab 1**: `labs/lab01_beyond_search_fundamentals.md`
3. **Run first search**:
   ```spl
   index=web sourcetype=access_combined_wcookie productId=*
   ```
4. **Start learning!**

---

## Support

- **Course Outline**: See `outline.md` for complete course structure
- **Quick Start**: See `QUICK_START.md` for condensed setup instructions
- **Course Summary**: See `COURSE_UPDATE_SUMMARY.md` for all course details
- **Lab Details**: See individual lab files in `labs/` directory

---

---

## Summary

In this lab, you:
- ✓ Created 4 indexes (web, security, network, games)
- ✓ Uploaded web access logs (~15,000 events)
- ✓ Uploaded vendor sales data (~5,000 events)
- ✓ Uploaded security authentication logs (~2,000 events)
- ✓ Uploaded network proxy logs (~3,000 events)
- ✓ Uploaded game telemetry data (~2,000 events)
- ✓ Uploaded 2 lookup files (http_status_lookup, product_catalog)
- ✓ Verified all data loaded correctly (~27,000 total events)

## Key Takeaways

1. **Multiple indexes** organize data by type and improve search performance
2. **Sourcetype** determines how Splunk parses and extracts fields from data
3. **CSV files** require "Indexed Extractions = CSV" setting
4. **Lookup files** are uploaded separately, not to indexes
5. **Verification searches** confirm data was loaded correctly
6. **Alternative sourcetypes** (access_combined vs access_combined_wcookie) can reference the same data

---

**Data Loading Complete!** You're ready to start Lab 1. 🎮

---

**Lab 0 Complete!**
