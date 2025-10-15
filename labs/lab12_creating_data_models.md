# Lab 12: Creating Data Models

**Splunk Intermediate – Lab Exercises**

> **Note**: This lab should be completed in a non-production environment.

## Lab Description

This lab covers:
- Understanding data models and their purpose
- Creating root event datasets
- Adding auto-extracted fields to data models
- Creating child datasets with constraints
- Creating grandchild datasets
- Adding eval expression fields
- Adding lookup fields to data models
- Using the Pivot interface
- Creating pivot reports and visualizations
- Building dashboards from pivot reports
- Accelerating data models for performance

## Scenario

You are a Splunk administrator for Buttercup Games. The marketing team needs to analyze website activity but doesn't know SPL. You'll create a data model called "Buttercup Games Site Activity" that organizes web events into a hierarchical structure, enabling non-technical users to create reports using the Pivot interface.

---

## Task 1: Understanding Data Models

### Scenario

Learn what data models are and how they benefit your organization.

### Step 1.1: Data Model Concepts

**Data Models**:
- Hierarchical representation of datasets
- Organize data into parent-child relationships
- Enable Pivot interface for non-SPL users
- Can be accelerated for fast performance

**Components**:
- **Root Event Dataset**: Base search defining all events
- **Child Datasets**: Subsets with additional constraints
- **Grandchild Datasets**: Further refinements
- **Fields**: Auto-extracted, eval expressions, lookups, geo IP
- **Constraints**: Filters that define each dataset

### Step 1.2: Use Cases

Data models are ideal for:
- Enabling non-technical users to create reports
- Standardizing data access across teams
- Improving search performance with acceleration
- Creating consistent field definitions
- Building pivot tables and visualizations

### Step 1.3: Planning the Data Model

We'll create: **Buttercup Games Site Activity**

Structure:
```
Buttercup Games Site Activity (Root)
└── Web requests (Root Event)
    ├── Successful requests (status<400)
    │   └── purchases (action=purchase productId=*)
    └── Failed requests (status>399)
        └── removed (action=remove productId=*)
```

---

## Task 2: Creating the Root Event Dataset

### Scenario

Create the root event dataset that defines the base data for the model.

### Step 2.1: Create New Data Model

1. Navigate to **Settings** → **Data models**
2. Click **New Data Model**
3. Configure:
   - **Title**: `Buttercup Games Site Activity`
   - **ID**: `buttercup_games_site_activity`
   - **App**: **search** (or class_Fund2)
   - **Description**: `Website activity data model for Buttercup Games e-commerce platform`
4. Click **Create**

### Step 2.2: Add Root Event Dataset

1. In the data model editor, click **Add Dataset**
2. Select **Root Event**
3. Configure:
   - **Dataset Name**: `Web requests`
   - **Dataset ID**: `web_requests`
   - **Constraints**:
     ```
     index=web sourcetype=access_combined
     ```
   - **Description**: `All web requests from the Buttercup Games online store`
4. Click **Preview** to verify events appear
5. Click **Save**

**Expected Results**: The root event dataset shows web access logs

### Step 2.3: Verify Root Dataset

In the data model editor:
- Root event "Web requests" appears
- Preview shows sample events
- Event count is displayed

---

## Task 3: Adding Auto-Extracted Fields

### Scenario

Add fields that are automatically extracted from the events to the data model.

### Step 3.1: Add Auto-Extracted Fields

1. With "Web requests" dataset selected, click **Add Field** → **Auto-Extracted**
2. Select fields to include:
   - `action`
   - `bytes`
   - `categoryId`
   - `clientip`
   - `date_mday`
   - `productId`
   - `product_name`
   - `req_time`
   - `status`
3. Click **Add Fields**

### Step 3.2: Configure Field Properties

For each field, configure:

**action**:
- Display Name: `Action`
- Field Type: `String`
- Description: `User action (purchase, addtocart, remove, view)`

**bytes**:
- Display Name: `Bytes`
- Field Type: `Number`
- Description: `Response size in bytes`

**categoryId**:
- Display Name: `Category ID`
- Field Type: `String`
- Description: `Product category identifier`

**clientip**:
- Display Name: `Client IP`
- Field Type: `IPv4`
- Description: `Client IP address`

**productId**:
- Display Name: `Product ID`
- Field Type: `String`
- Description: `Product identifier`

**product_name**:
- Display Name: `Product Name`
- Field Type: `String`
- Description: `Product name`

**req_time**:
- Display Name: `Request Time`
- Field Type: `Number`
- Description: `Request processing time in seconds`

**status**:
- Display Name: `HTTP Status`
- Field Type: `Number`
- Description: `HTTP response status code`

### Step 3.3: Save and Verify Fields

1. Click **Save** after adding all fields
2. Preview the dataset to verify fields appear
3. Check that field types are correct

---

## Task 4: Creating Child Datasets

### Scenario

Create child datasets to organize events into successful and failed requests.

### Step 4.1: Create "Successful Requests" Child Dataset

1. Right-click on **Web requests** dataset
2. Select **Add Child** → **Event**
3. Configure:
   - **Dataset Name**: `Successful requests`
   - **Dataset ID**: `successful_requests`
   - **Constraints**: `status<400`
   - **Description**: `Successful HTTP requests (status codes 200-399)`
4. Click **Preview** to verify only successful requests appear
5. Click **Save**

### Step 4.2: Create "Failed Requests" Child Dataset

1. Right-click on **Web requests** dataset
2. Select **Add Child** → **Event**
3. Configure:
   - **Dataset Name**: `Failed requests`
   - **Dataset ID**: `failed_requests`
   - **Constraints**: `status>399`
   - **Description**: `Failed HTTP requests (status codes 400+)`
4. Click **Preview** to verify only error requests appear
5. Click **Save**

**Expected Results**: Two child datasets appear under "Web requests" in the hierarchy

---

## Task 5: Creating Grandchild Datasets

### Scenario

Create grandchild datasets to further refine successful and failed requests.

### Step 5.1: Create "Purchases" Grandchild Dataset

1. Right-click on **Successful requests** dataset
2. Select **Add Child** → **Event**
3. Configure:
   - **Dataset Name**: `purchases`
   - **Dataset ID**: `purchases`
   - **Constraints**: `action=purchase productId=*`
   - **Description**: `Completed purchase transactions`
4. Click **Preview** to verify only purchases appear
5. Click **Save**

### Step 5.2: Create "Removed" Grandchild Dataset

1. Right-click on **Failed requests** dataset
2. Select **Add Child** → **Event**
3. Configure:
   - **Dataset Name**: `removed`
   - **Dataset ID**: `removed`
   - **Constraints**: `action=remove productId=*`
   - **Description**: `Items removed from cart`
4. Click **Preview** to verify only remove actions appear
5. Click **Save**

**Expected Results**: Hierarchical structure with grandchildren:
```
Web requests
├── Successful requests
│   └── purchases
└── Failed requests
    └── removed
```

---

## Task 6: Adding Eval Expression Fields

### Scenario

Create calculated fields using eval expressions.

### Step 6.1: Add Day Field

1. Select **Web requests** root dataset
2. Click **Add Field** → **Eval Expression**
3. Configure:
   - **Field Name**: `day`
   - **Display Name**: `Day`
   - **Eval Expression**: `strftime(_time, "%m-%d %A")`
   - **Field Type**: `String`
   - **Description**: `Day of month and day of week`
4. Click **Preview** to verify the field shows dates like "01-15 Monday"
5. Click **Save**

### Step 6.2: Add Megabytes Field

1. Click **Add Field** → **Eval Expression**
2. Configure:
   - **Field Name**: `megabytes`
   - **Display Name**: `Megabytes`
   - **Eval Expression**: `round(bytes/(1024*1024), 2)`
   - **Field Type**: `Number`
   - **Description**: `Response size in megabytes`
3. Click **Save**

### Step 6.3: Add Response Category Field

1. Click **Add Field** → **Eval Expression**
2. Configure:
   - **Field Name**: `response_category`
   - **Display Name**: `Response Category`
   - **Eval Expression**:
   ```
   case(req_time<0.1, "Fast", req_time>=0.1 AND req_time<0.5, "Normal", req_time>=0.5 AND req_time<1, "Slow", req_time>=1, "Very Slow")
   ```
   - **Field Type**: `String`
   - **Description**: `Response time category`
3. Click **Save**

---

## Task 7: Adding Lookup Fields

### Scenario

Add a lookup field to enrich status codes with descriptions.

### Step 7.1: Verify Lookup File Exists

Ensure the http_status_lookup.csv exists from Lab 6:

```spl
| inputlookup http_status_lookup.csv
```

If it doesn't exist, create it with:
```csv
status,status_description,status_type
200,OK,Success
201,Created,Success
204,No Content,Success
301,Moved Permanently,Redirection
302,Found,Redirection
304,Not Modified,Redirection
400,Bad Request,Client Error
401,Unauthorized,Client Error
403,Forbidden,Client Error
404,Not Found,Client Error
500,Internal Server Error,Server Error
502,Bad Gateway,Server Error
503,Service Unavailable,Server Error
```

### Step 7.2: Create Lookup Definition

If not already created:
1. Navigate to **Settings** → **Lookups** → **Lookup definitions**
2. Create definition: `http_status_lookup`
3. Reference file: `http_status_lookup.csv`

### Step 7.3: Add Lookup Field to Data Model

1. Select **Web requests** root dataset
2. Click **Add Field** → **Lookup**
3. Configure:
   - **Lookup Name**: `http_status_lookup`
   - **Input Field**: `status`
   - **Output Fields**: Select `status_description`
4. Configure field properties:
   - **Display Name**: `Status Description`
   - **Field Type**: `String`
   - **Description**: `HTTP status code description`
5. Click **Save**

### Step 7.4: Add Additional Lookup Field

Add status_type from the same lookup:
1. Click **Add Field** → **Lookup**
2. Configure:
   - **Lookup Name**: `http_status_lookup`
   - **Input Field**: `status`
   - **Output Fields**: Select `status_type`
3. Configure:
   - **Display Name**: `Status Type`
   - **Field Type**: `String`
4. Click **Save**

---

## Task 8: Using the Pivot Interface

### Scenario

Use Pivot to create reports without writing SPL.

### Step 8.1: Open Pivot

1. In the data model editor, click **Pivot** on the "Web requests" dataset
2. The Pivot interface opens

### Step 8.2: Create Purchase Count Report

1. In Pivot:
   - **Split Rows**: Add `Product Name`
   - **Split Columns**: None
   - **Filters**: Select dataset: `purchases`
   - **Values**: Add `Count` (automatic)
2. Click **Run Pivot**

**Expected Results**: Table showing count of purchases by product

### Step 8.3: Create Time-Based Purchase Report

1. Create new pivot
2. Configure:
   - **Dataset**: `purchases`
   - **Split Rows**: `_time` (binned by day)
   - **Split Columns**: `Product Name`
   - **Values**: `Count`
3. Click **Run Pivot**
4. Switch to **Column Chart** visualization

**Expected Results**: Chart showing purchases over time by product

**Save this search as**: `L12S1`

### Step 8.4: Create Status Code Distribution Report

1. Create new pivot
2. Configure:
   - **Dataset**: `Web requests`
   - **Split Rows**: `Status Description`
   - **Values**: `Count`
3. Click **Run Pivot**
4. Switch to **Pie Chart** visualization

**Expected Results**: Pie chart showing distribution of HTTP status codes

**Save this search as**: `L12S2`

---

## Task 9: Creating Advanced Pivot Reports

### Scenario

Create more sophisticated reports using pivot.

### Step 9.1: Create Revenue by Product Report

1. Create new pivot
2. Configure:
   - **Dataset**: `purchases`
   - **Split Rows**: `Product Name`
   - **Values**: Click **Add Column Value**
     - Function: `Sum`
     - Field: `bytes`
3. Rename column to "Total Bytes"
4. Click **Run Pivot**

**Expected Results**: Total bytes transferred per product

### Step 9.2: Create Performance Report

1. Create new pivot
2. Configure:
   - **Dataset**: `Web requests`
   - **Split Rows**: `Response Category`
   - **Split Columns**: `Action`
   - **Values**: `Count`
3. Click **Run Pivot**
4. Switch to **Stacked Bar Chart**

**Expected Results**: Shows distribution of response times across different actions

**Save this search as**: `L12S3`

### Step 9.3: Create Daily Activity Report

1. Create new pivot
2. Configure:
   - **Dataset**: `Web requests`
   - **Split Rows**: `day`
   - **Values**:
     - `Count` (rename to "Total Requests")
     - `Average` of `req_time` (rename to "Avg Response Time")
3. Click **Run Pivot**

**Expected Results**: Daily summary with request count and average response time

---

## Task 10: Building a Dashboard from Pivots

### Scenario

Create a comprehensive dashboard called "Weekly Website Activity" using pivot reports.

### Step 10.1: Create First Dashboard Panel

1. Create a pivot report showing daily purchases:
   - Dataset: `purchases`
   - Split Rows: `_time` (day)
   - Values: `Count`
2. Click **Save As** → **Dashboard Panel**
3. Configure:
   - **Dashboard**: New Dashboard
   - **Dashboard Title**: `Weekly Website Activity`
   - **Dashboard ID**: `weekly_website_activity`
   - **Panel Title**: `Daily Purchases`
   - **Panel Content**: `Column Chart`
4. Click **Save**

### Step 10.2: Add Error Rate Panel

1. Create pivot report:
   - Dataset: `Failed requests`
   - Split Rows: `_time` (hour)
   - Values: `Count`
2. Add to existing dashboard:
   - **Dashboard**: `Weekly Website Activity`
   - **Panel Title**: `Error Rate Over Time`
   - **Panel Content**: `Line Chart`
3. Click **Save**

### Step 10.3: Add Top Products Panel

1. Create pivot report:
   - Dataset: `purchases`
   - Split Rows: `Product Name`
   - Values: `Count`
   - Sort: Descending
   - Limit: 10
2. Add to dashboard:
   - **Panel Title**: `Top 10 Products`
   - **Panel Content**: `Bar Chart`
3. Click **Save**

### Step 10.4: Add Status Distribution Panel

1. Create pivot report:
   - Dataset: `Web requests`
   - Split Rows: `Status Type`
   - Values: `Count`
2. Add to dashboard:
   - **Panel Title**: `HTTP Status Distribution`
   - **Panel Content**: `Pie Chart`
3. Click **Save**

### Step 10.5: Add Performance Metrics Panel

1. Create pivot report:
   - Dataset: `Web requests`
   - Values:
     - `Average` of `req_time`
     - `Count`
2. Add to dashboard:
   - **Panel Title**: `Overall Performance`
   - **Panel Content**: `Single Value`
3. Click **Save**

**Expected Results**: Dashboard with 5 panels showing comprehensive website activity

---

## Task 11: Accelerating the Data Model

### Scenario

Accelerate the data model for faster pivot performance.

### Step 11.1: Enable Acceleration

1. In the data model editor, click **Edit** → **Edit Acceleration**
2. Configure:
   - **Accelerate**: Yes
   - **Acceleration Time Range**: Last 7 days
   - **Summary Range**: All time
3. Click **Save**

> **Note**: Acceleration builds summary tables in the background, significantly improving pivot performance

### Step 11.2: Monitor Acceleration Progress

1. Navigate to **Settings** → **Data models**
2. Locate "Buttercup Games Site Activity"
3. Check the **Acceleration** column
4. Wait for acceleration to complete (shows percentage)

### Step 11.3: Test Accelerated Performance

1. Open a pivot report
2. Compare search time before and after acceleration
3. Accelerated pivots should be significantly faster

> **Tip**: Acceleration benefits:
> - Faster pivot reports
> - Reduced load on indexers
> - Better user experience
> - Tradeoff: Uses disk space and CPU for summaries

---

## Challenge Exercise (Optional)

### Challenge 1: Create Comprehensive E-commerce Data Model

Extend the data model with:

1. **Additional Root Datasets**:
   - Security events (index=security)
   - Network events (index=network)

2. **Additional Child Datasets under Web requests**:
   - `cart_additions`: action=addtocart
   - `cart_removals`: action=remove
   - `product_views`: action=view
   - `high_value_purchases`: purchases with additional filter price>100

3. **Additional Eval Fields**:
   - `hour_of_day`: Extract hour from _time
   - `is_weekend`: Determine if day is weekend
   - `session_duration`: Calculate from transaction data
   - `revenue_category`: High/Medium/Low based on price

4. **Additional Lookup Fields**:
   - Product category descriptions
   - Client geolocation from clientip

5. **Create Advanced Dashboard**: "E-commerce Executive Summary"
   - Sales funnel visualization
   - Geographic revenue map
   - Hour-of-day heatmap
   - Weekend vs weekday comparison
   - High-value customer analysis

**Save this search as**: `L12C1`

### Challenge 2: Create Security Data Model

Create a new data model: "Security Events"

1. **Root Dataset**: All security events (index=security)

2. **Child Datasets**:
   - Authentication events
     - Successful logins
     - Failed logins
   - Privileged user activity
   - Suspicious activity

3. **Fields**:
   - Auto-extracted: src_ip, user, action
   - Eval: hour, day_of_week, is_privileged_user
   - Lookup: IP geolocation, threat intelligence

4. **Create Pivot Reports**:
   - Failed login attempts by IP
   - Privileged user activity timeline
   - Geographic distribution of logins
   - Authentication success rate

5. **Create Dashboard**: "Security Monitoring"

**Save this search as**: `L12C2`

---

## Summary

In this lab, you learned:
- ✓ What data models are and their benefits
- ✓ How to create root event datasets
- ✓ How to add auto-extracted fields to data models
- ✓ How to create child and grandchild datasets with constraints
- ✓ How to add eval expression fields for calculated values
- ✓ How to add lookup fields to enrich data
- ✓ How to use the Pivot interface to create reports without SPL
- ✓ How to create visualizations from pivot reports
- ✓ How to build dashboards from pivot reports
- ✓ How to accelerate data models for better performance

## Key Takeaways

1. **Data models** organize data into hierarchical structures
2. **Root event datasets** define the base search for the model
3. **Child datasets** add constraints to create subsets
4. **Grandchild datasets** further refine child datasets
5. **Auto-extracted fields** come from existing field extractions
6. **Eval fields** create calculated values
7. **Lookup fields** enrich data with external information
8. **Pivot interface** enables report creation without SPL knowledge
9. **Acceleration** improves performance by creating summary tables
10. Data models are ideal for **empowering non-technical users**
11. Data models support the **Common Information Model (CIM)**

---

## Data Sources Used

- **index=web, sourcetype=access_combined**: Web access logs with action, status, productId, product_name, clientip, bytes, req_time, categoryId for the Buttercup Games Site Activity data model

## Next Steps

Congratulations! You've completed all 12 labs in the Splunk Intermediate course. You now have the skills to:
- Create advanced searches and visualizations
- Build interactive dashboards
- Manage knowledge objects (field extractions, aliases, tags, event types, macros)
- Create workflow actions for efficient investigations
- Build data models for non-technical users

Consider pursuing:
- Splunk Advanced Certification
- Splunk Architect Certification
- Specialized courses (Security, IT Operations, Enterprise Administration)

---

**Lab 12 Complete! Course Complete!**
