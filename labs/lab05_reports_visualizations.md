# Lab 5: Creating Reports and Visualizations

**Duration:** 45 minutes
**Difficulty:** Intermediate

## Objectives

In this lab, you will learn to:
- Create effective reports using various visualization types
- Choose appropriate visualizations for different data types
- Format and customize visualizations
- Schedule reports for automatic delivery
- Share reports with other users
- Optimize report performance

## Prerequisites

- Completed Labs 1-4
- Training data loaded in the `training` index
- Understanding of statistical commands

---

## Exercise 1: Understanding Visualization Types

**Scenario:** Learn when to use each visualization type for maximum impact.

### Task 1.1: Column Chart - Comparing Categories

Create a column chart showing request volumes by method:

```spl
index=training sourcetype=web_access
| stats count as Requests by method
| sort -Requests
```

**Visualization Settings:**
1. Click "Visualization" tab
2. Select "Column Chart"
3. Format → Y-Axis Title: "Number of Requests"
4. Format → X-Axis Title: "HTTP Method"

**Question:** Which HTTP method is most common?

### Task 1.2: Line Chart - Trends Over Time

Show response time trends:

```spl
index=training sourcetype=web_access
| timechart span=1h avg(response_time) as "Avg Response Time (ms)"
```

**Visualization:** Line Chart

**Questions:**
1. Are there any notable spikes in response time?
2. What might cause these patterns?

### Task 1.3: Pie Chart - Composition/Distribution

Show the composition of HTTP status codes:

```spl
index=training sourcetype=web_access
| eval status_category = case(
    status < 300, "Success (2xx)",
    status < 400, "Redirect (3xx)",
    status < 500, "Client Error (4xx)",
    status >= 500, "Server Error (5xx)"
)
| stats count by status_category
```

**Visualization:** Pie Chart

**Question:** What percentage of requests are successful?

### Task 1.4: Area Chart - Volume Over Time

Visualize request volume trends:

```spl
index=training sourcetype=web_access
| eval status_type = if(status < 400, "Success", "Error")
| timechart span=30m count by status_type
```

**Visualization:** Area Chart (Stacked)

**Question:** How does the error volume compare to successful requests over time?

---

## Exercise 2: Advanced Visualizations

**Scenario:** Use specialized visualizations for specific analytical needs.

### Task 2.1: Single Value - KPI Display

Show key performance indicator:

```spl
index=training sourcetype=web_access
| stats avg(response_time) as avg_rt
| eval avg_rt = round(avg_rt, 2)
```

**Visualization:** Single Value
**Settings:**
- Under Color: Add ranges
  - 0-500: Green (#65A637)
  - 500-1000: Yellow (#F7BC38)
  - 1000+: Red (#D93F3C)
- Caption: "Average Response Time (ms)"

**Question:** Is your average response time in the acceptable range?

### Task 2.2: Gauge - Performance Indicator

Create a gauge showing error rate:

```spl
index=training sourcetype=web_access
| stats count as total,
        sum(eval(if(status>=400, 1, 0))) as errors
| eval error_rate = round((errors/total)*100, 2)
| fields error_rate
```

**Visualization:** Radial Gauge
**Settings:**
- Range: 0-20
- Color ranges:
  - 0-2: Green
  - 2-5: Yellow
  - 5-20: Red

**Question:** What is your current error rate?

### Task 2.3: Bubble Chart - Multi-Dimensional Analysis

Compare users across multiple dimensions:

```spl
index=training sourcetype=web_access user!="-"
| lookup users.csv username as user OUTPUT department
| stats count as requests,
        avg(response_time) as avg_rt,
        sum(bytes) as total_bytes
        by user, department
| eval total_mb = total_bytes/1024/1024
| where requests > 50
| fields user, requests, avg_rt, total_mb
```

**Visualization:** Bubble Chart
- X-axis: requests
- Y-axis: avg_rt
- Size: total_mb

**Question:** Which users have high activity but good response times?

### Task 2.4: Scatter Plot - Correlation Analysis

Analyze relationship between response time and bytes transferred:

```spl
index=training sourcetype=web_access
| eval bytes_kb = bytes/1024
| table response_time, bytes_kb
| where response_time < 3000 AND bytes_kb < 100
```

**Visualization:** Scatter Chart

**Question:** Is there a correlation between bytes transferred and response time?

---

## Exercise 3: Tables and Statistics

**Scenario:** Create detailed tabular reports for comprehensive analysis.

### Task 3.1: Basic Statistics Table

Create a comprehensive user activity report:

```spl
index=training sourcetype=web_access user!="-"
| lookup users.csv username as user OUTPUT department, role
| stats count as Requests,
        dc(url) as "Unique URLs",
        avg(response_time) as "Avg RT (ms)",
        sum(bytes) as "Total Bytes",
        sum(eval(if(status>=400, 1, 0))) as Errors
        by user, department, role
| eval "Avg RT (ms)" = round('Avg RT (ms)', 2)
| eval "Total MB" = round('Total Bytes'/1024/1024, 2)
| eval "Error Rate %" = round((Errors/Requests)*100, 2)
| fields - "Total Bytes"
| sort -Requests
```

**Visualization:** Statistics Table
**Settings:**
- Enable totals
- Enable sorting
- Format numbers appropriately

**Question:** Which department has the highest total activity?

### Task 3.2: Formatted Table with Sparklines

Add sparklines to show trends:

```spl
index=training sourcetype=web_access user!="-"
| lookup users.csv username as user OUTPUT department
| timechart span=1h count by department limit=5
| fields _time, *
```

**Visualization:** Table
**Column Format:**
- Enable sparklines for department columns

**Question:** Which department shows the most variable activity pattern?

### Task 3.3: Table with Conditional Formatting

Create a table with color-coded cells:

```spl
index=training sourcetype=web_access user!="-"
| stats count as requests,
        avg(response_time) as avg_rt,
        max(response_time) as max_rt,
        sum(eval(if(status>=400, 1, 0))) as errors
        by user
| eval error_rate = round((errors/requests)*100, 2)
| eval avg_rt = round(avg_rt, 2)
| sort -error_rate
| head 20
```

**Visualization:** Table
**Format:**
- Error_rate: Color red if > 5%
- avg_rt: Color red if > 1000ms

---

## Exercise 4: Creating and Saving Reports

**Scenario:** Save and organize reports for reuse.

### Task 4.1: Save a Basic Report

Create and save a report:

```spl
index=training sourcetype=web_access
| timechart span=1h count as Requests, avg(response_time) as "Avg Response Time"
```

**Steps:**
1. Click "Save As" → "Report"
2. Title: "Web Traffic Overview"
3. Description: "Hourly web traffic and response time trends"
4. Time Range: "Last 7 days"
5. Permissions: Shared in App
6. Save

**Verify:** Go to Reports tab and find your report.

### Task 4.2: Create an Executive Summary Report

Build a comprehensive executive report:

```spl
index=training sourcetype=web_access
| stats count as "Total Requests",
        dc(clientip) as "Unique Visitors",
        dc(user) as "Unique Users",
        avg(response_time) as "Avg Response Time (ms)",
        perc95(response_time) as "95th Percentile RT (ms)",
        sum(bytes) as total_bytes,
        sum(eval(if(status>=400, 1, 0))) as errors
| eval "Total Data Transferred (GB)" = round(total_bytes/1024/1024/1024, 3)
| eval "Error Rate %" = round((errors/'Total Requests')*100, 2)
| eval "Avg Response Time (ms)" = round('Avg Response Time (ms)', 2)
| eval "95th Percentile RT (ms)" = round('95th Percentile RT (ms)', 2)
| fields - total_bytes, errors
| transpose
| rename column as "Metric", "row 1" as "Value"
```

**Save as:** "Executive Traffic Report"
**Visualization:** Statistics Table

### Task 4.3: Create a Detailed Analysis Report

Build a multi-panel report:

```spl
index=training sourcetype=web_access
| lookup users.csv username as user OUTPUT department, city
| stats count as requests,
        dc(user) as unique_users,
        avg(response_time) as avg_rt,
        sum(eval(if(status>=400, 1, 0))) as errors
        by department, city
| eval error_rate = round((errors/requests)*100, 2)
| eval avg_rt = round(avg_rt, 2)
| sort -requests
```

**Save as:** "Department Activity Analysis"

---

## Exercise 5: Scheduled Reports

**Scenario:** Automate report generation and delivery.

### Task 5.1: Schedule a Daily Report

Configure a scheduled report:

**Steps:**
1. Open saved report "Web Traffic Overview"
2. Edit → Edit Schedule
3. Schedule Report: Yes
4. Schedule: Daily at 8:00 AM
5. Time Range: Previous day (-1d@d to @d)
6. Schedule Window: Auto (recommended)
7. Schedule Priority: Default
8. Save

### Task 5.2: Email Report Delivery

Add email delivery to scheduled report:

**Steps:**
1. Edit Schedule (from saved report)
2. Add Action: "Send email"
3. To: (your email)
4. Subject: "Daily Web Traffic Report"
5. Message: "Please find the daily web traffic report attached."
6. Include: PDF, Inline visualization
7. Paper Size: A4
8. Paper Orientation: Landscape
9. Save

**Note:** Ensure Splunk email settings are configured (Settings → Server Settings → Email Settings)

### Task 5.3: Create a Weekly Summary Report

Build and schedule a weekly report:

```spl
index=training sourcetype=web_access earliest=-7d@w1 latest=@w1
| lookup users.csv username as user OUTPUT department
| stats count as requests,
        dc(user) as unique_users,
        avg(response_time) as avg_rt,
        sum(bytes) as total_bytes,
        sum(eval(if(status>=400, 1, 0))) as errors
        by department
| eval avg_rt = round(avg_rt, 2)
| eval total_gb = round(total_bytes/1024/1024/1024, 3)
| eval error_rate = round((errors/requests)*100, 2)
| fields department, requests, unique_users, avg_rt, total_gb, error_rate
| sort -requests
```

**Save and Schedule:**
- Report Title: "Weekly Department Summary"
- Schedule: Weekly on Monday at 9:00 AM
- Email delivery with PDF attachment

---

## Exercise 6: Report Formatting and Customization

**Scenario:** Enhance report appearance and readability.

### Task 6.1: Customize Chart Colors

Create a report with custom colors:

```spl
index=training sourcetype=web_access
| eval status_category = case(
    status < 300, "Success",
    status < 400, "Redirect",
    status < 500, "Client Error",
    status >= 500, "Server Error"
)
| timechart span=1h count by status_category
```

**Visualization:** Column Chart (Stacked)
**Format:**
1. Click "Format" button
2. Chart Colors:
   - Success: Green (#65A637)
   - Redirect: Blue (#1E93C6)
   - Client Error: Orange (#F7BC38)
   - Server Error: Red (#D93F3C)

### Task 6.2: Add Titles and Labels

Enhance a visualization with descriptive labels:

```spl
index=training sourcetype=web_access
| timechart span=1h avg(response_time) as "Response Time"
```

**Visualization:** Line Chart
**Format:**
- Chart Title: "Average Response Time Trend"
- X-Axis Title: "Time"
- Y-Axis Title: "Response Time (milliseconds)"
- Show Data Labels: Yes (for key points)
- Legend Position: Bottom

### Task 6.3: Multi-Series Overlay

Create a chart with multiple series:

```spl
index=training sourcetype=web_access
| timechart span=30m
    avg(response_time) as "Avg Response Time",
    perc95(response_time) as "95th Percentile",
    max(response_time) as "Max Response Time"
```

**Visualization:** Line Chart
**Format:**
- Multi-series overlay: Yes
- Line styles: Different for each series
- Show all series in legend

---

## Exercise 7: Report Performance Optimization

**Scenario:** Improve report performance for faster execution.

### Task 7.1: Use Summary Indexing Concept

Compare direct search vs. pre-aggregated search:

**Direct (slower):**
```spl
index=training sourcetype=web_access earliest=-30d
| timechart span=1h count by status
```

**Pre-aggregated concept:**
```spl
index=training sourcetype=web_access earliest=-1h
| timechart span=5m count by status
| appendcols [
    search index=summary_training earliest=-30d latest=-1h
    | timechart span=1h count by status
]
```

### Task 7.2: Optimize Search with tstats

Use tstats for better performance (requires accelerated datamodels):

```spl
| tstats count where index=training sourcetype=web_access by _time, status span=1h
| chart sum(count) as requests by _time, status
```

**Compare performance** with regular stats approach.

### Task 7.3: Limit Search Scope

Optimize by reducing data volume:

```spl
index=training sourcetype=web_access earliest=-24h
| fields _time, method, status, response_time
| timechart span=1h avg(response_time) by method
```

**Best Practices:**
- Use specific time ranges
- Use fields command early
- Filter unnecessary data

---

## Bonus Challenge

Create a comprehensive executive dashboard report that includes:
1. KPI single values (total requests, error rate, avg response time)
2. Trend visualization showing last 7 days
3. Department comparison table
4. Geographic distribution (by city)
5. Top 10 URLs by traffic
6. Schedule it to run daily at 7 AM with email delivery

---

## Key Takeaways

- **Choose the right visualization** for your data type and analysis goal
- **Line charts** for trends over time
- **Column/Bar charts** for comparing categories
- **Pie charts** for composition (use sparingly)
- **Tables** for detailed data analysis
- **Single values and gauges** for KPIs
- **Schedule reports** for automated delivery
- **Format visualizations** for clarity and professionalism
- **Optimize searches** for better performance

## Visualization Selection Guide

| Data Type | Best Visualization |
|-----------|-------------------|
| Time series trends | Line, Area chart |
| Category comparison | Column, Bar chart |
| Composition/Parts of whole | Pie chart (< 7 slices) |
| KPIs/Single metrics | Single Value, Gauge |
| Correlation | Scatter plot |
| Multi-dimensional | Bubble chart |
| Detailed data | Table |
| Geographic | Choropleth map |

## Report Best Practices

1. **Clear titles** and labels
2. **Appropriate time ranges** for context
3. **Color coding** for quick insights
4. **Limit data points** for readability
5. **Add context** with descriptions
6. **Test schedules** before deploying
7. **Optimize queries** for performance

## Next Steps

In Lab 6, you'll learn to build interactive dashboards that combine multiple reports and allow user interaction.

---

**Lab Complete!**
