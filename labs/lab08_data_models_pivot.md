# Lab 8: Data Models and Pivot

**Duration:** 45 minutes
**Difficulty:** Intermediate

## Objectives

In this lab, you will learn to:
- Understand data model concepts and structure
- Create data models with objects and fields
- Use the Pivot interface for data exploration
- Accelerate data models for performance
- Build reports using Pivot
- Understand when to use data models vs. raw searches

## Prerequisites

- Completed Labs 1-7
- Training data loaded in the `training` index
- Understanding of fields and lookups

---

## Exercise 1: Understanding Data Models

**Scenario:** Learn what data models are and when to use them.

### Task 1.1: Explore Existing Data Models

**View built-in data models:**
1. Navigate to Settings → Data models
2. Browse available data models
3. Open "Internal Audit Logs" data model
4. Examine its structure

**Questions:**
1. What objects does it contain?
2. What fields are defined?
3. What are the relationships between objects?

### Task 1.2: Data Model Concepts

**Key Concepts:**

**Data Model** - Hierarchical structure representing your data
- **Objects** - Datasets (similar to tables)
- **Fields** - Attributes (columns)
- **Constraints** - Filters defining the data
- **Relationships** - Links between objects (parent-child)

**Benefits:**
- Standardize data access
- Enable Pivot interface
- Support acceleration
- Abstract complexity from users

### Task 1.3: When to Use Data Models

**Use data models when:**
- Multiple users need consistent access to data
- Non-SPL users need to analyze data (Pivot)
- Performance is critical (acceleration)
- Data structure is complex but predictable

**Use raw searches when:**
- Ad-hoc analysis
- One-time investigation
- Data structure is unknown or varies
- No acceleration needed

---

## Exercise 2: Creating Your First Data Model

**Scenario:** Create a data model for web traffic analysis.

### Task 2.1: Create Base Data Model

**Steps:**
1. Settings → Data models → New Data Model
2. Data Model Title: "Web Traffic Analysis"
3. Data Model ID: web_traffic_analysis
4. App: search
5. Save

### Task 2.2: Add Root Event Object

**Create root object:**
1. Click "Add Object" → "Root Event"
2. Object Name: "Web Access Logs"
3. Constraints:
```spl
index=training sourcetype=web_access
```
4. Save

**Add fields:**
1. Edit object → "Add Field" → "Auto-Extracted"
2. Select fields:
   - clientip (rename to "Client IP")
   - method (rename to "HTTP Method")
   - url (rename to "URL")
   - status (rename to "Status Code")
   - bytes (rename to "Bytes Transferred")
   - response_time (rename to "Response Time")
3. Save each field

### Task 2.3: Add Calculated Fields

**Add eval-based fields:**

**Field 1: Status Category**
1. Add Field → "Eval Expression"
2. Field Name: "Status Category"
3. Eval Expression:
```
case(status < 300, "Success", status < 400, "Redirect", status < 500, "Client Error", status >= 500, "Server Error")
```
4. Field Type: string
5. Save

**Field 2: Response Category**
1. Add Field → "Eval Expression"
2. Field Name: "Response Category"
3. Eval Expression:
```
case(response_time < 100, "Fast", response_time < 500, "Normal", response_time < 2000, "Slow", 1=1, "Critical")
```
4. Field Type: string
5. Save

**Field 3: Bytes (MB)**
1. Add Field → "Eval Expression"
2. Field Name: "Data Transfer (MB)"
3. Eval Expression:
```
round(bytes/1024/1024, 3)
```
4. Field Type: number
5. Save

### Task 2.4: Add Lookup Field

**Enrich with user data:**
1. Add Field → "Lookup"
2. Field Name: "Department"
3. Lookup: users.csv
4. Input Field: user = username
5. Output Field: department
6. Save

Repeat for:
- City (user = username → city)
- Role (user = username → role)

---

## Exercise 3: Using the Pivot Interface

**Scenario:** Create reports using the Pivot interface without writing SPL.

### Task 3.1: Basic Pivot Report

**Create traffic volume report:**
1. Open Data Model: "Web Traffic Analysis"
2. Click "Pivot"
3. Select Object: "Web Access Logs"

**Configure Pivot:**
- Split Rows: HTTP Method
- Split Columns: Status Category
- Values: Count

**Result:** Cross-tab showing request counts by method and status

**Save as Report:** "Traffic by Method and Status"

### Task 3.2: Time-Based Pivot

**Create trend analysis:**
1. Start new Pivot from same data model
2. Configure:
   - Split Rows: _time (span = 1 hour)
   - Values: Count of records
   - Filter: _time = Last 24 hours

**Visualization:** Line Chart

**Save as Report:** "Hourly Traffic Trend"

### Task 3.3: Multi-Dimensional Analysis

**Analyze by department and response time:**
1. New Pivot
2. Configure:
   - Split Rows: Department
   - Split Columns: Response Category
   - Values:
     - Count of records
     - Average of Response Time

**Filter:** Remove null departments

**Save as Report:** "Department Performance Analysis"

### Task 3.4: Statistical Pivot

**Calculate detailed statistics:**
1. New Pivot
2. Configure:
   - Split Rows: URL
   - Values:
     - Count
     - Average Response Time
     - Max Response Time
     - Sum of Bytes Transferred
   - Filter: Count > 100
   - Sort: By Count (descending)
   - Limit: 10

**Save as Report:** "Top 10 URLs Performance"

---

## Exercise 4: Advanced Data Model Features

**Scenario:** Create complex data models with hierarchies and relationships.

### Task 4.1: Add Child Object

**Create Error Events object:**
1. Edit Data Model: "Web Traffic Analysis"
2. Select "Web Access Logs" object
3. Add Object → "Child"
4. Object Name: "Error Events"
5. Constraints:
```spl
status >= 400
```
6. Save

**Add specific fields:**
- error_type (eval):
```
if(status < 500, "Client Error", "Server Error")
```

### Task 4.2: Add Search Object

**Create aggregated object:**
1. Add Object → "Search"
2. Object Name: "Hourly Statistics"
3. Search:
```spl
index=training sourcetype=web_access
| timechart span=1h
    count as requests,
    avg(response_time) as avg_response_time,
    dc(user) as unique_users
```
4. Save

**Use in Pivot:**
- This creates pre-aggregated data for faster analysis

### Task 4.3: Add Transaction Object

**Group related events:**
1. Add Object → "Transaction"
2. Object Name: "User Sessions"
3. Group By: user, clientip
4. Max Pause: 30m
5. Max Span: 4h
6. Save

**Fields to add:**
- Session Duration (eval): `duration`
- Event Count (eval): `eventcount`

---

## Exercise 5: Data Model Acceleration

**Scenario:** Accelerate data models for instant results.

### Task 5.1: Understand Acceleration

**What is acceleration?**
- Creates summary tables in background
- Enables instant Pivot results
- Uses tstats command behind the scenes
- Trades storage for speed

**When to accelerate?**
- Large data volumes
- Frequent Pivot usage
- Slow Pivot performance
- Stable data model design

### Task 5.2: Enable Acceleration

**Accelerate your data model:**
1. Settings → Data models
2. Open "Web Traffic Analysis"
3. Edit → Acceleration
4. Enable: Yes
5. Summary Range: Last 7 days
6. Save

**Note:** Acceleration build time depends on data volume

**Monitor acceleration:**
```spl
| rest /services/admin/summarization by_tstats=t
| search title="*web_traffic_analysis*"
| table title, summary_size, is_inprogress, complete_pct
```

### Task 5.3: Compare Performance

**Without acceleration:**
```spl
index=training sourcetype=web_access earliest=-7d
| stats count by method, status
```
*Note execution time*

**With acceleration (using tstats):**
```spl
| tstats count from datamodel=Web_Traffic_Analysis by Web_Access_Logs.method, Web_Access_Logs.status
```
*Note execution time - should be significantly faster*

### Task 5.4: Acceleration Best Practices

**Recommendations:**
1. **Start small** - Accelerate 7 days, expand if needed
2. **Monitor storage** - Acceleration uses disk space
3. **Stable models** - Don't accelerate during development
4. **Test first** - Verify model works before accelerating
5. **Schedule wisely** - Acceleration builds use resources

**Check acceleration health:**
```spl
| rest /services/admin/summarization
| where match(title, "web_traffic")
| table title, summary_size, summary_time_range, is_inprogress, complete_pct
```

---

## Exercise 6: Using tstats with Data Models

**Scenario:** Write high-performance searches using tstats.

### Task 6.1: Basic tstats Query

**Count events:**
```spl
| tstats count from datamodel=Web_Traffic_Analysis
```

**With time range:**
```spl
| tstats count from datamodel=Web_Traffic_Analysis where earliest=-24h
```

### Task 6.2: tstats with Grouping

**Group by fields:**
```spl
| tstats count from datamodel=Web_Traffic_Analysis
    by Web_Access_Logs.method, Web_Access_Logs.status
| rename Web_Access_Logs.* as *
```

**Tip:** Use rename to simplify field names

### Task 6.3: tstats with Statistics

**Multiple statistical functions:**
```spl
| tstats count,
          avg(Web_Access_Logs.response_time) as avg_rt,
          max(Web_Access_Logs.response_time) as max_rt,
          sum(Web_Access_Logs.bytes) as total_bytes
    from datamodel=Web_Traffic_Analysis
    by Web_Access_Logs.url
| rename Web_Access_Logs.url as url
| eval avg_rt = round(avg_rt, 2)
| sort -count
| head 20
```

### Task 6.4: tstats Time Charts

**Create time series:**
```spl
| tstats count from datamodel=Web_Traffic_Analysis
    by _time, Web_Access_Logs.status span=1h
| rename Web_Access_Logs.status as status
| timechart span=1h sum(count) as requests by status
```

---

## Exercise 7: Building Pivot Dashboards

**Scenario:** Create dashboards using Pivot reports.

### Task 7.1: Create Pivot-Based Dashboard

**Steps:**
1. Create multiple Pivot reports (from Exercise 3)
2. Create New Dashboard: "Web Traffic Analytics"
3. Add panels from existing Pivot reports:
   - "Traffic by Method and Status"
   - "Hourly Traffic Trend"
   - "Department Performance Analysis"
   - "Top 10 URLs Performance"

### Task 7.2: Add Pivot Inline Editor

**Create panel directly from Pivot:**
1. Edit Dashboard
2. Add Panel → "Pivot"
3. Select Data Model: "Web Traffic Analysis"
4. Configure Pivot inline
5. Add to dashboard

**Benefit:** Can edit Pivot configuration without leaving dashboard

### Task 7.3: Combine Pivot and SPL Panels

**Mix Pivot and custom searches:**

**Pivot Panel 1:** Basic metrics
**SPL Panel 2:** Complex analysis not possible in Pivot
```spl
index=training sourcetype=web_access
| eval hour = strftime(_time, "%H")
| stats avg(response_time) as avg_rt by hour, status
| where status >= 400
| chart avg(avg_rt) over hour by status
```

**Best Practice:** Use Pivot for standard reports, SPL for specialized analysis

---

## Exercise 8: Data Model Best Practices

**Scenario:** Apply best practices for maintainable data models.

### Task 8.1: Naming Conventions

**Use clear, descriptive names:**
- Data Model: "Web Traffic Analysis" (not "DM1")
- Object: "Web Access Logs" (not "Events")
- Field: "Response Time" (not "rt")

### Task 8.2: Documentation

**Add descriptions:**
1. Edit Data Model
2. For each object and field, add:
   - Description of what it represents
   - Example values
   - Special considerations

**Example:**
- Field: "Status Code"
- Description: "HTTP status code (200, 404, 500, etc.). Codes ≥400 indicate errors."

### Task 8.3: Organize Fields Logically

**Group related fields:**
- Identification: URL, Method, Status
- Performance: Response Time, Bytes
- Context: User, Department, City
- Derived: Categories, Scores

### Task 8.4: Version Control

**Maintain model versions:**
1. Export data model (JSON)
2. Save to version control
3. Document changes
4. Test before deploying

**Export:**
```bash
# Via CLI
splunk search "| datamodel Web_Traffic_Analysis" -output json
```

---

## Bonus Challenge

Create a comprehensive data model that:
1. Includes both web access and application logs
2. Has parent-child relationships
3. Includes lookup enrichment
4. Has calculated performance metrics
5. Is accelerated for 30 days
6. Powers a multi-panel dashboard
7. Includes both Pivot and tstats-based panels

---

## Key Takeaways

- **Data models** provide structured access to data
- **Pivot** enables analysis without SPL knowledge
- **Acceleration** dramatically improves performance
- **tstats** provides fastest searches on accelerated data models
- **Hierarchical objects** represent relationships
- **Calculated fields** add derived information
- **Best practices** ensure maintainability

## Data Model Components

| Component | Purpose | Example |
|-----------|---------|---------|
| Root Event | Base dataset | Web access logs |
| Child | Filtered subset | Only errors |
| Search | Aggregated data | Hourly statistics |
| Transaction | Grouped events | User sessions |

## Pivot vs. SPL

| Feature | Pivot | SPL |
|---------|-------|-----|
| Ease of use | High | Medium-Low |
| Flexibility | Medium | Very High |
| Performance | Fast (with acceleration) | Varies |
| Use case | Standard reports | Complex analysis |
| Users | Business users | Technical users |

## tstats Performance Tips

1. **Use specific time ranges** - Reduces data scanned
2. **Filter early** - Use WHERE clause
3. **Limit fields** - Only request needed fields
4. **Use summariesonly=true** - Forces acceleration usage
5. **Prefilter by indexed fields** - index, source, sourcetype

## Next Steps

In Lab 9, you'll learn advanced dashboard techniques including Simple XML customization and advanced interactions.

---

**Lab Complete!**
