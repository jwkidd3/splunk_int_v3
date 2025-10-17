# Lab 12: Creating Data Models

**Splunk Intermediate – Lab Exercises**

## Objectives

- Create root event datasets
- Add auto-extracted, eval, and lookup fields
- Create child and grandchild datasets
- Use Pivot interface for reporting
- Build dashboards from pivots
- Accelerate data models

---

## Task 1: Data Model Concepts

### Components

- **Root Event Dataset**: Base search
- **Child Datasets**: Subsets with constraints
- **Grandchild Datasets**: Further refinements
- **Fields**: Auto-extracted, eval, lookups

### Planned Structure

```
Buttercup Games Site Activity
└── Web requests
    ├── Successful requests (status<400)
    │   └── purchases
    └── Failed requests (status>399)
        └── removed
```

---

## Task 2: Create Root Dataset

### Step 1: Create Data Model

1. **Settings** → **Data models**
2. **New Data Model**
3. Configure:
   - Title: `Buttercup Games Site Activity`
   - ID: `buttercup_games_site_activity`
   - Description: `Website activity for e-commerce platform`

### Step 2: Add Root Event

1. **Add Dataset** → **Root Event**
2. Configure:
   - Name: `Web requests`
   - ID: `web_requests`
   - Constraints: `index=web sourcetype=access_combined`
   - Description: `All web requests from online store`
3. **Preview** → **Save**

---

## Task 3: Add Fields

### Auto-Extracted Fields

1. Select "Web requests" dataset
2. **Add Field** → **Auto-Extracted**
3. Select fields:
   - `action`, `bytes`, `categoryId`, `clientip`
   - `productId`, `product_name`, `req_time`, `status`
4. **Add Fields**

### Configure Field Properties

- **action**: String, "User action"
- **bytes**: Number, "Response size in bytes"
- **status**: Number, "HTTP status code"
- **req_time**: Number, "Request time in seconds"

---

## Task 4: Create Child Datasets

### Successful Requests

1. Right-click **Web requests**
2. **Add Child** → **Event**
3. Configure:
   - Name: `Successful requests`
   - ID: `successful_requests`
   - Constraints: `status<400`
   - Description: `Successful HTTP requests (200-399)`

### Failed Requests

1. Right-click **Web requests**
2. **Add Child** → **Event**
3. Configure:
   - Name: `Failed requests`
   - ID: `failed_requests`
   - Constraints: `status>399`
   - Description: `Failed HTTP requests (400+)`

---

## Task 5: Create Grandchild Datasets

### Purchases

1. Right-click **Successful requests**
2. **Add Child** → **Event**
3. Configure:
   - Name: `purchases`
   - Constraints: `action=purchase productId=*`
   - Description: `Completed purchases`

### Removed Items

1. Right-click **Failed requests**
2. **Add Child** → **Event**
3. Configure:
   - Name: `removed`
   - Constraints: `action=remove productId=*`
   - Description: `Items removed from cart`

---

## Task 6: Add Eval Fields

### Day Field

1. Select **Web requests**
2. **Add Field** → **Eval Expression**
3. Configure:
   - Field name: `day`
   - Expression: `strftime(_time, "%m-%d %A")`
   - Type: String

### Megabytes Field

1. **Add Field** → **Eval Expression**
2. Configure:
   - Field name: `megabytes`
   - Expression: `round(bytes/(1024*1024), 2)`
   - Type: Number

### Response Category

1. **Add Field** → **Eval Expression**
2. Configure:
   - Field name: `response_category`
   - Expression: `case(req_time<0.1, "Fast", req_time>=0.1 AND req_time<0.5, "Normal", req_time>=0.5 AND req_time<1, "Slow", req_time>=1, "Very Slow")`
   - Type: String

---

## Task 7: Add Lookup Field

### Step 1: Verify Lookup

```spl
| inputlookup http_status_lookup.csv
```

If missing, create lookup definition (from Lab 6).

### Step 2: Add to Data Model

1. Select **Web requests**
2. **Add Field** → **Lookup**
3. Configure:
   - Lookup: `http_status_lookup`
   - Input field: `status`
   - Output fields: `status_description`

---

## Task 8: Use Pivot

### Step 1: Purchase Count Report

1. Click **Pivot** on "Web requests"
2. Configure:
   - Dataset: `purchases`
   - Split Rows: `Product Name`
   - Values: `Count`
3. **Run Pivot**

**Save as**: `L12S1`

### Step 2: Time-Based Purchases

1. New pivot
2. Configure:
   - Dataset: `purchases`
   - Split Rows: `_time` (by day)
   - Split Columns: `Product Name`
   - Values: `Count`
3. Switch to **Column Chart**

**Save as**: `L12S2`

### Step 3: Status Distribution

1. New pivot
2. Configure:
   - Dataset: `Web requests`
   - Split Rows: `Status Description`
   - Values: `Count`
3. Switch to **Pie Chart**

**Save as**: `L12S3`

---

## Task 9: Build Dashboard

### Step 1: Daily Purchases Panel

1. Create pivot: purchases by day
2. **Save As** → **Dashboard Panel**
3. Configure:
   - Dashboard: New → `Weekly Website Activity`
   - Panel Title: `Daily Purchases`
   - Visualization: `Column Chart`

### Step 2: Error Rate Panel

1. Create pivot: failed requests by hour
2. Add to dashboard
3. Panel Title: `Error Rate Over Time`
4. Visualization: `Line Chart`

### Step 3: Top Products Panel

1. Create pivot: purchases by product (top 10)
2. Add to dashboard
3. Panel Title: `Top 10 Products`
4. Visualization: `Bar Chart`

### Step 4: Status Distribution Panel

1. Create pivot: status type counts
2. Add to dashboard
3. Panel Title: `HTTP Status Distribution`
4. Visualization: `Pie Chart`

---

## Task 10: Accelerate Data Model

### Step 1: Enable Acceleration

1. In data model editor: **Edit** → **Edit Acceleration**
2. Configure:
   - Accelerate: Yes
   - Time Range: Last 7 days
3. **Save**

### Step 2: Monitor Progress

1. **Settings** → **Data models**
2. Check **Acceleration** column
3. Wait for completion (shows percentage)

### Step 3: Test Performance

Open pivot reports - should be significantly faster after acceleration.

---

## Challenge: E-commerce Data Model

Extend with:

1. **Additional Children**:
   - `cart_additions`, `cart_removals`, `product_views`
   - `high_value_purchases` (price>100)

2. **Eval Fields**:
   - `hour_of_day`, `is_weekend`, `revenue_category`

3. **Lookups**:
   - Product categories, client geolocation

4. **Dashboard**: E-commerce Executive Summary

**Save as**: `L12C1`

---

## Summary

- Data models organize data hierarchically
- Root event datasets define base search
- Child datasets add constraints for subsets
- Auto-extracted fields from existing extractions
- Eval fields create calculated values
- Lookup fields enrich with external data
- Pivot creates reports without SPL
- Acceleration improves performance
- Data models empower non-technical users

---

**Lab 12 Complete! Course Complete!**
