# Lab 4: Lookups and Data Enrichment

**Duration:** 45 minutes
**Difficulty:** Intermediate

## Objectives

In this lab, you will learn to:
- Create and manage CSV lookups
- Configure automatic lookups
- Use lookup commands in searches
- Implement lookup-based data enrichment
- Use inputlookup and outputlookup commands
- Understand KV Store lookups

## Prerequisites

- Completed Labs 1-3
- Training data loaded in the `training` index
- Lookup CSV files generated (products.csv, users.csv, threat_intel.csv)

---

## Exercise 1: Manual Lookup Usage

**Scenario:** Enrich web access logs with user information.

### Task 1.1: Upload Lookup File

**Via UI:**
1. Settings → Lookups → Lookup table files
2. Click "New Lookup Table File"
3. Destination app: "search"
4. Upload `data/users.csv`
5. Destination filename: `users.csv`

**Verify upload:**
```spl
| inputlookup users.csv
| table username, email, department, city, country, role
```

**Question:** How many users are in the lookup table?

### Task 1.2: Basic Lookup Command

Enrich web logs with user information:

```spl
index=training sourcetype=web_access user!="-"
| lookup users.csv username as user
| stats count by user, department, city
| sort -count
```

**Questions:**
1. Which department has the most web activity?
2. Which city generates the most requests?

### Task 1.3: Lookup with Multiple Fields

Enrich and analyze by multiple dimensions:

```spl
index=training sourcetype=web_access user!="-"
| lookup users.csv username as user OUTPUT department, city, country, role
| stats count as requests,
        dc(url) as unique_urls,
        avg(response_time) as avg_rt
        by department, role
| eval avg_rt = round(avg_rt, 2)
| sort -requests
```

**Question:** Do admin users have different usage patterns than regular users?

---

## Exercise 2: Automatic Lookups

**Scenario:** Configure lookups to run automatically whenever data is searched.

### Task 2.1: Define Lookup Definition

**Via UI:**
1. Settings → Lookups → Lookup definitions
2. Click "New Lookup Definition"
3. Destination app: "search"
4. Name: `user_lookup`
5. Type: "File-based"
6. Lookup file: `users.csv`
7. Save

### Task 2.2: Configure Automatic Lookup

**Via UI:**
1. Settings → Lookups → Automatic lookups
2. Click "New"
3. Destination app: "search"
4. Name: `auto_user_lookup`
5. Lookup table: `user_lookup`
6. Apply to: sourcetype = `web_access`
7. Lookup input fields: `user = username`
8. Lookup output fields: `department, city, country, role`
9. Save

**Test automatic lookup:**
```spl
index=training sourcetype=web_access user!="-"
| stats count by department, role
| sort -count
```

**Question:** Do you see department and role fields without using the lookup command?

### Task 2.3: Verify Automatic Enrichment

Test that enrichment happens automatically:

```spl
index=training sourcetype=web_access user="alice"
| table _time, user, department, city, role, url, status
```

**Challenge:** Create an automatic lookup for the products.csv file.

---

## Exercise 3: Advanced Lookup Techniques

**Scenario:** Implement sophisticated lookup strategies for data analysis.

### Task 3.1: Lookup with WILDCARD Matching

First, upload threat_intel.csv, then use it:

```spl
| inputlookup threat_intel.csv
| table ip_address, threat_level, threat_type, description
```

Create a search to match threat intelligence:

```spl
index=training sourcetype=web_access
| lookup threat_intel.csv ip_address as clientip OUTPUT threat_level, threat_type, description
| where isnotnull(threat_level)
| stats count by clientip, threat_level, threat_type
| sort -count
```

**Question:** Are any of our web requests coming from threat IPs?

### Task 3.2: OUTPUTNEW - Preserve Existing Values

Use OUTPUTNEW to avoid overwriting existing fields:

```spl
index=training sourcetype=web_access user!="-"
| eval department = "Unknown"
| lookup users.csv username as user OUTPUTNEW department
| stats count by department
```

**Question:** What's the difference between OUTPUT and OUTPUTNEW?

### Task 3.3: Case-Insensitive Lookups

Handle case variations in lookup fields:

```spl
index=training sourcetype=web_access user!="-"
| eval user_lower = lower(user)
| lookup users.csv username as user_lower
| stats count by username, department
```

**Challenge:** Modify users.csv to have all lowercase usernames and test.

---

## Exercise 4: Inputlookup and Outputlookup

**Scenario:** Create and maintain dynamic lookup tables.

### Task 4.1: Create a New Lookup from Search Results

Generate a lookup table of user activity metrics:

```spl
index=training sourcetype=web_access user!="-"
| stats count as total_requests,
        dc(url) as unique_urls,
        avg(response_time) as avg_response_time,
        sum(eval(if(status>=400, 1, 0))) as errors
        by user
| eval avg_response_time = round(avg_response_time, 2)
| eval error_rate = round((errors/total_requests)*100, 2)
| outputlookup user_activity_metrics.csv
```

**Verify:**
```spl
| inputlookup user_activity_metrics.csv
| sort -total_requests
```

**Question:** Which users have the highest error rates?

### Task 4.2: Update Existing Lookup

Add new calculations to the lookup:

```spl
| inputlookup user_activity_metrics.csv
| eval activity_score = case(
    total_requests > 500, "High",
    total_requests > 200, "Medium",
    1=1, "Low"
)
| eval performance_score = case(
    avg_response_time < 500 AND error_rate < 5, "Excellent",
    avg_response_time < 1000 AND error_rate < 10, "Good",
    1=1, "Poor"
)
| outputlookup user_activity_metrics.csv
```

**Verify:**
```spl
| inputlookup user_activity_metrics.csv
| stats count by activity_score, performance_score
```

### Task 4.3: Append to Lookup

Create a historical tracking system:

```spl
index=training sourcetype=web_access earliest=-1h
| stats count as requests by user
| eval timestamp = now()
| eval date = strftime(timestamp, "%Y-%m-%d %H:00")
| outputlookup append=true user_activity_history.csv
```

**View history:**
```spl
| inputlookup user_activity_history.csv
| sort -timestamp
| head 50
```

**Challenge:** Create a search that tracks error rates over time using outputlookup append.

---

## Exercise 5: Lookup-Based Enrichment Patterns

**Scenario:** Implement common lookup patterns for data enrichment.

### Task 5.1: Multi-Lookup Enrichment

Enrich data with multiple lookups:

```spl
index=training sourcetype=web_access user!="-"
| lookup users.csv username as user OUTPUT department, city, role
| lookup threat_intel.csv ip_address as clientip OUTPUT threat_level
| stats count as requests,
        dc(url) as unique_urls,
        sum(eval(if(isnotnull(threat_level), 1, 0))) as threat_hits
        by user, department, role
| eval threat_percentage = round((threat_hits/requests)*100, 2)
| where threat_hits > 0
| sort -threat_hits
```

**Question:** Which users/departments have the most threat intelligence hits?

### Task 5.2: Lookup-Based Filtering

Use lookups to create dynamic filters:

```spl
index=training sourcetype=web_access
| lookup users.csv username as user OUTPUT role
| where role="admin"
| stats count by user, url
| sort -count
```

**Question:** What are admin users accessing most frequently?

### Task 5.3: Conditional Lookup Logic

Apply different enrichment based on conditions:

```spl
index=training sourcetype=web_access
| lookup users.csv username as user OUTPUT department, role
| eval access_level = case(
    role="admin", "full",
    department="IT", "elevated",
    department="Engineering", "elevated",
    1=1, "standard"
)
| where url like "%/admin%" AND access_level!="full"
| table _time, user, department, role, access_level, url
```

**Question:** Are any non-admin users accessing admin URLs?

---

## Exercise 6: Product Lookup Enrichment

**Scenario:** Enrich e-commerce data with product information.

### Task 6.1: Upload and Test Product Lookup

Upload products.csv and test:

```spl
| inputlookup products.csv
| table product_id, product_name, category, price, vendor, stock_level
| sort product_name
```

### Task 6.2: Enrich Search Data

Extract product references and enrich:

```spl
index=training sourcetype=web_access url="/products/*"
| rex field=url "/products/(?<product_name>\w+)"
| lookup products.csv product_name OUTPUT category, price, vendor
| where isnotnull(category)
| stats count as views,
        values(price) as price,
        values(vendor) as vendor
        by product_name, category
| sort -views
```

**Question:** Which product category is most popular?

### Task 6.3: Calculate Revenue Estimates

Create revenue calculations using lookup data:

```spl
index=training sourcetype=web_access url="/checkout*"
| rex field=url "\?id=(?<product_id>PROD\d+)"
| lookup products.csv product_id OUTPUT product_name, price, category
| where isnotnull(price)
| stats count as purchases,
        sum(price) as revenue,
        avg(price) as avg_price
        by category
| eval revenue = "$" + tostring(round(revenue, 2))
| eval avg_price = "$" + tostring(round(avg_price, 2))
| sort -purchases
```

**Question:** Which category generates the most revenue?

---

## Exercise 7: KV Store Lookups (Conceptual)

**Scenario:** Understand the difference between CSV and KV Store lookups.

### Task 7.1: Compare Lookup Types

**CSV Lookups:**
- Static files loaded into memory
- Good for relatively small datasets (< 1GB)
- Updated via outputlookup
- Simple to manage

**KV Store Lookups:**
- MongoDB-based storage
- Better for large datasets
- Support for complex queries
- Can be updated via REST API

### Task 7.2: When to Use Each Type

Create a decision matrix search:

```spl
| makeresults
| eval csv_use_cases="Small static data, Simple key-value, Infrequent updates, < 10K rows"
| eval kvstore_use_cases="Large datasets, Frequent updates, Complex queries, > 100K rows"
| table csv_use_cases, kvstore_use_cases
```

**Discussion:** Which lookup type would you use for:
1. User role mapping (20 users)?
2. IP geolocation database (1M entries)?
3. Daily threat intelligence feed (updated hourly)?

---

## Exercise 8: Lookup Performance Optimization

**Scenario:** Optimize lookup performance for large-scale searches.

### Task 8.1: Measure Lookup Performance

Compare performance with and without lookups:

```spl
index=training sourcetype=web_access user!="-"
| fields _time, user, url, status
```

vs.

```spl
index=training sourcetype=web_access user!="-"
| lookup users.csv username as user
| fields _time, user, url, status, department, city
```

**Question:** What is the performance difference?

### Task 8.2: Optimize Lookup Usage

Only lookup when needed:

```spl
index=training sourcetype=web_access user!="-" status>=400
| lookup users.csv username as user OUTPUT department, role
| stats count by department, role
```

**Best Practice:** Filter data before applying lookups.

### Task 8.3: Limit Lookup Output Fields

Request only necessary fields:

```spl
index=training sourcetype=web_access user!="-"
| lookup users.csv username as user OUTPUT department
| stats count by department
```

**Challenge:** Compare performance between OUTPUT department vs. OUTPUT department, city, country, role.

---

## Bonus Challenge

Create a comprehensive security monitoring system that:
1. Enriches web access logs with user information
2. Adds threat intelligence data
3. Creates risk scores based on:
   - User role and department
   - Threat level of source IPs
   - Error rates and suspicious patterns
4. Outputs high-risk events to a new lookup table for tracking

---

## Key Takeaways

- **CSV lookups** are ideal for static reference data
- **Automatic lookups** enrich data automatically at search time
- **Inputlookup** reads lookup tables, **outputlookup** writes them
- **Lookup commands** support OUTPUT, OUTPUTNEW, and other modifiers
- Use **lookup definitions** to manage and configure lookups
- **Performance**: Filter data before lookups, limit output fields
- **KV Store** for large, dynamic datasets requiring complex queries

## Lookup Commands Reference

```
| lookup <lookup-table> <input-field> as <event-field> OUTPUT <output-fields>
| inputlookup <lookup-table> [where <condition>]
| outputlookup <lookup-table> [append=true]
```

## Common Lookup Patterns

1. **Enrichment**: Add context to events
2. **Filtering**: Use lookup values as filters
3. **Translation**: Map codes to descriptions
4. **Classification**: Categorize events based on lookup data
5. **Tracking**: Maintain state across searches

## Next Steps

In Lab 5, you'll learn to create reports and visualizations to present your enriched data effectively.

---

**Lab Complete!**
