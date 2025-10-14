# Lab 6: Building Interactive Dashboards

**Duration:** 45 minutes
**Difficulty:** Intermediate

## Objectives

In this lab, you will learn to:
- Create dashboards using the Dashboard Editor
- Add and configure dashboard panels
- Implement dashboard inputs (time pickers, dropdowns, text inputs)
- Use tokens to create interactivity
- Link panels for coordinated analysis
- Share and manage dashboards

## Prerequisites

- Completed Labs 1-5
- Understanding of reports and visualizations
- Training data loaded in the `training` index

---

## Exercise 1: Creating Your First Dashboard

**Scenario:** Build a basic monitoring dashboard for web traffic.

### Task 1.1: Create a New Dashboard

**Steps:**
1. From Splunk Home, click "Dashboards"
2. Click "Create New Dashboard"
3. Dashboard Title: "Web Traffic Monitoring"
4. Dashboard ID: web_traffic_monitoring
5. Permissions: Shared in App
6. Dashboard Type: Classic Dashboards
7. Click "Create"

### Task 1.2: Add First Panel - Traffic Overview

**Add a panel:**
1. Click "Add Panel" → "New" → "Visualization"
2. Search:
```spl
index=training sourcetype=web_access
| timechart span=1h count as "Requests"
```
3. Select visualization: Line Chart
4. Panel Title: "Traffic Overview - Last 24 Hours"
5. Click "Add to Dashboard"

**Edit Dashboard:**
- Click "Edit" to enter edit mode
- Drag panel to resize
- Click "Save"

### Task 1.3: Add KPI Panel

**Add Single Value panel:**
1. Add Panel → New
2. Search:
```spl
index=training sourcetype=web_access
| stats count as "Total Requests",
        avg(response_time) as "Avg Response Time"
| eval "Avg Response Time" = round('Avg Response Time', 2)
```
3. Visualization: Single Value
4. Title: "Key Metrics"
5. Add to Dashboard

### Task 1.4: Add Status Distribution Panel

**Add Pie Chart:**
1. Add Panel → New
2. Search:
```spl
index=training sourcetype=web_access
| eval status_category = case(
    status < 300, "Success",
    status < 400, "Redirect",
    status < 500, "Client Error",
    status >= 500, "Server Error"
)
| stats count by status_category
```
3. Visualization: Pie Chart
4. Title: "Request Status Distribution"
5. Add to Dashboard

**Save Dashboard**

---

## Exercise 2: Adding Dashboard Inputs

**Scenario:** Make your dashboard interactive with input controls.

### Task 2.1: Add Time Range Picker

**Add time input:**
1. Edit Dashboard
2. Click "Add Input" → "Time"
3. Settings:
   - Token: `time_token`
   - Label: "Time Range"
   - Default: Last 24 hours
   - Search when changed: Yes
4. Save

**Update all panel searches** to use the time picker (already applied by default when using dashboard time range)

### Task 2.2: Add Dropdown for User Selection

**Add dropdown input:**
1. Add Input → "Dropdown"
2. Settings:
   - Token: `user_token`
   - Label: "Select User"
   - Search on change: Yes
3. Dynamic Options search:
```spl
index=training sourcetype=web_access user!="-"
| stats count by user
| sort -count
```
4. Dynamic Options:
   - Field for Label: user
   - Field for Value: user
5. Default: * (all users)
6. Save

**Add a new panel using this token:**
```spl
index=training sourcetype=web_access user=$user_token$
| timechart span=30m count as Requests
```

### Task 2.3: Add Multiselect for HTTP Methods

**Add multiselect dropdown:**
1. Add Input → "Multiselect"
2. Settings:
   - Token: `method_token`
   - Label: "HTTP Methods"
   - Delimiter: space
3. Static Options:
   - GET
   - POST
   - PUT
   - DELETE
4. Default: All
5. Save

**Create panel with multiselect:**
```spl
index=training sourcetype=web_access method IN ($method_token$)
| stats count by method, status
| sort -count
```

### Task 2.4: Add Text Input for URL Search

**Add text input:**
1. Add Input → "Text"
2. Settings:
   - Token: `url_token`
   - Label: "Search URL"
   - Default: *
3. Save

**Panel search:**
```spl
index=training sourcetype=web_access url="*$url_token$*"
| stats count by url, method
| sort -count
| head 20
```

---

## Exercise 3: Working with Tokens

**Scenario:** Use tokens to create dynamic, interconnected dashboards.

### Task 3.1: Set Token from Search

**Create a drilldown panel:**
1. Add a table panel:
```spl
index=training sourcetype=web_access user!="-"
| lookup users.csv username as user OUTPUT department
| stats count as requests by department
| sort -requests
```
2. Visualization: Table
3. Title: "Requests by Department"

**Configure drilldown:**
1. Edit panel → Drilldown: "On"
2. Drilldown Type: "Set a token"
3. Token name: `selected_dept`
4. Token value: `$row.department$`

**Add dependent panel:**
```spl
index=training sourcetype=web_access
| lookup users.csv username as user OUTPUT department
| search department="$selected_dept$"
| timechart span=1h count
```
Title: "Activity for $selected_dept$"

### Task 3.2: Use eval with Tokens

**Create conditional search based on tokens:**
```spl
index=training sourcetype=web_access
| eval search_filter = if("$user_token$"="*", "true", user="$user_token$")
| search $search_filter$
| stats count by user
```

### Task 3.3: Token Dependencies

**Create dependent input:**
1. Add Dropdown for Department
2. Add second Dropdown for User
3. Make User dropdown depend on Department selection:

**Department dropdown search:**
```spl
index=training sourcetype=web_access user!="-"
| lookup users.csv username as user OUTPUT department
| stats count by department
| sort department
```

**User dropdown search (dependent):**
```spl
index=training sourcetype=web_access user!="-"
| lookup users.csv username as user OUTPUT department
| search department="$dept_token$"
| stats count by user
| sort user
```

---

## Exercise 4: Advanced Panel Configuration

**Scenario:** Customize panel behavior and appearance.

### Task 4.1: Configure Panel Refresh

**Set auto-refresh:**
1. Edit panel
2. More Options → Refresh every: 5 minutes
3. Save

**Best for:** Real-time monitoring panels

### Task 4.2: Add Panel Description

**Add context to panels:**
1. Edit panel
2. Description: "Shows request volume trends over selected time range. Spikes may indicate traffic surges or potential issues."
3. Save

### Task 4.3: Configure Drilldown Behavior

**Link to search:**
1. Edit panel
2. Drilldown: On
3. Drilldown Type: "Link to search"
4. Configure drilldown search:
```spl
index=training sourcetype=web_access $click.value$
| table _time, user, url, status, response_time
```

### Task 4.4: Format Panel

**Customize appearance:**
1. Edit panel
2. Format tab:
   - Chart Colors: Custom
   - Chart Overlay: None
   - Legend Position: Right
   - Show Data Labels: No
3. Save

---

## Exercise 5: Creating a Multi-Page Dashboard

**Scenario:** Build a comprehensive dashboard with multiple views.

### Task 5.1: Create Main Overview Page

**Dashboard: "Operations Dashboard - Overview"**

Panels:
1. **KPIs Row:**
   - Total Requests (Single Value)
   - Unique Users (Single Value)
   - Error Rate (Gauge)
   - Avg Response Time (Single Value)

2. **Trends Row:**
   - Traffic Over Time (Line Chart)
   - Status Distribution (Pie Chart)

3. **Details Row:**
   - Top URLs (Table)
   - Top Users (Table)

### Task 5.2: Create Detail Page

**Dashboard: "Operations Dashboard - Details"**

Panels:
1. User Activity Analysis (Table with drilldown)
2. Response Time Analysis (Line Chart)
3. Error Analysis (Column Chart)
4. Department Comparison (Bar Chart)

### Task 5.3: Link Dashboards

**Add navigation:**
1. Edit Overview Dashboard
2. Add HTML panel:
```html
<p style="text-align:center;">
  <a href="/app/search/operations_dashboard_details">View Detailed Analysis →</a>
</p>
```

Add reverse link in Details dashboard.

---

## Exercise 6: Dashboard Layout and Design

**Scenario:** Create an aesthetically pleasing and functional layout.

### Task 6.1: Organize with Rows

**Create structured layout:**
1. Edit Dashboard
2. Add Row
3. Name: "Key Performance Indicators"
4. Add 4 single value panels in this row
5. Resize to equal widths

**Add more rows:**
- Row 2: "Traffic Trends" (2 wide panels)
- Row 3: "Detailed Analysis" (1 full-width table)

### Task 6.2: Use HTML Panels for Headers

**Add section headers:**
1. Add Panel → HTML
2. HTML content:
```html
<h2 style="text-align:center; padding:10px; background-color:#1e93c6; color:white;">
  Web Traffic Analysis Dashboard
</h2>
<p style="text-align:center; color:#666;">
  Monitor web application performance and user activity in real-time
</p>
```

### Task 6.3: Color Coordination

**Apply consistent color scheme:**
- Success metrics: Green (#65A637)
- Warning metrics: Yellow (#F7BC38)
- Error metrics: Red (#D93F3C)
- Info metrics: Blue (#1E93C6)

Apply to all panels consistently.

---

## Exercise 7: Practical Dashboard Examples

**Scenario:** Build real-world dashboard solutions.

### Task 7.1: Security Monitoring Dashboard

**Create dashboard with:**

**Panel 1: Failed Login Attempts**
```spl
index=training sourcetype=security_events event_type="login_failure"
| timechart span=1h count
```

**Panel 2: High Severity Events**
```spl
index=training sourcetype=security_events severity="high"
| stats count by event_type, user
| sort -count
```

**Panel 3: Geographic Distribution**
```spl
index=training sourcetype=security_events
| lookup users.csv username as user OUTPUT city, country
| stats count by country
| geom geo_countries featureIdField=country
```

### Task 7.2: Application Performance Dashboard

**Create dashboard with:**

**Panel 1: Response Time Percentiles**
```spl
index=training sourcetype=web_access
| timechart span=30m
    perc50(response_time) as "Median",
    perc90(response_time) as "90th",
    perc95(response_time) as "95th",
    perc99(response_time) as "99th"
```

**Panel 2: Error Rate by Endpoint**
```spl
index=training sourcetype=web_access
| stats count as total,
        sum(eval(if(status>=400, 1, 0))) as errors
        by url
| eval error_rate = round((errors/total)*100, 2)
| where total > 10
| sort -error_rate
| head 10
```

**Panel 3: Component Health**
```spl
index=training sourcetype=application
| stats count by component, level
| chart count over component by level
```

### Task 7.3: Business Metrics Dashboard

**Panel 1: User Engagement**
```spl
index=training sourcetype=web_access user!="-"
| lookup users.csv username as user OUTPUT department
| stats dc(user) as active_users,
        count as page_views,
        avg(response_time) as avg_load_time
        by department
| eval avg_load_time = round(avg_load_time, 2)
| sort -active_users
```

**Panel 2: Popular Products**
```spl
index=training sourcetype=web_access url="/products/*"
| rex field=url "/products/(?<product>\w+)"
| lookup products.csv product_name as product OUTPUT category, price
| stats count as views, values(price) as price by product, category
| sort -views
| head 10
```

---

## Exercise 8: Dashboard Permissions and Sharing

**Scenario:** Manage dashboard access and sharing.

### Task 8.1: Set Dashboard Permissions

**Configure permissions:**
1. Open Dashboard
2. Edit → Edit Permissions
3. Display For: App
4. Read permissions: Everyone
5. Write permissions: Admin role only
6. Save

### Task 8.2: Export Dashboard

**Export for backup or migration:**
1. Dashboard → Edit → Export
2. Save XML file

### Task 8.3: Clone Dashboard

**Create a copy:**
1. Dashboard → Edit → Clone
2. New Title: "Web Traffic Monitoring - Dev"
3. Use for testing changes

---

## Bonus Challenge

Create a comprehensive executive dashboard that:
1. Shows KPIs with color-coded thresholds
2. Has time range picker and department filter
3. Includes drilldown from summary to details
4. Uses tokens to link multiple panels
5. Has professional layout with headers and descriptions
6. Includes at least 8 different visualizations
7. Auto-refreshes every 5 minutes

---

## Key Takeaways

- **Dashboard inputs** make dashboards interactive
- **Tokens** enable dynamic searches and panel coordination
- **Drilldowns** allow users to explore data
- **Layout matters** - organize logically and aesthetically
- **Auto-refresh** for real-time monitoring
- **Permissions** control access and editing
- **Reusability** - clone dashboards for different teams/use cases

## Dashboard Best Practices

1. **Start with purpose** - What questions does it answer?
2. **Use consistent layout** - Group related information
3. **Limit panel count** - 6-10 panels per dashboard
4. **Provide context** - Add descriptions and labels
5. **Test interactivity** - Ensure tokens work correctly
6. **Optimize searches** - Fast panels improve UX
7. **Use appropriate visualizations** - Match viz to data
8. **Consider audience** - Executive vs. operational dashboards differ

## Common Dashboard Patterns

- **KPI Dashboard**: Single values, gauges, trends
- **Operational Dashboard**: Real-time monitoring, auto-refresh
- **Executive Dashboard**: High-level metrics, minimal detail
- **Analytical Dashboard**: Detailed tables, multiple dimensions
- **Security Dashboard**: Threat indicators, alerts, events

## Next Steps

In Lab 7, you'll learn to create alerts and scheduled searches to proactively monitor your systems.

---

**Lab Complete!**
