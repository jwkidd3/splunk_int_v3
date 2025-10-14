# Lab 9: Advanced Dashboard Techniques

**Duration:** 45 minutes
**Difficulty:** Advanced

## Objectives

In this lab, you will learn to:
- Edit Simple XML for dashboard customization
- Implement advanced drilldowns and navigation
- Use base searches for performance optimization
- Create dynamic content with JavaScript
- Implement advanced token manipulation
- Build form-based dashboards
- Apply CSS styling to dashboards

## Prerequisites

- Completed Labs 1-8
- Understanding of dashboards and tokens
- Basic knowledge of XML (helpful)
- Training data loaded in the `training` index

---

## Exercise 1: Introduction to Simple XML

**Scenario:** Learn the structure and syntax of Simple XML dashboards.

### Task 1.1: View Dashboard XML

**Access XML source:**
1. Open any dashboard
2. Click "Edit" → "Edit Source"
3. Examine the XML structure

**Basic Structure:**
```xml
<dashboard>
  <label>Dashboard Title</label>
  <row>
    <panel>
      <title>Panel Title</title>
      <search>
        <query>index=training | stats count</query>
        <earliest>-24h</earliest>
        <latest>now</latest>
      </search>
      <option name="charting.chart">line</option>
    </panel>
  </row>
</dashboard>
```

### Task 1.2: Edit XML Directly

**Modify panel via XML:**
1. Edit Source
2. Find a panel
3. Change panel title:
```xml
<title>Updated Panel Title</title>
```
4. Add description:
```xml
<title>Updated Panel Title</title>
<description>This panel shows key metrics</description>
```
5. Save

### Task 1.3: Add Custom Options

**Customize visualization:**
```xml
<chart>
  <title>Traffic Trend</title>
  <search>
    <query>index=training sourcetype=web_access | timechart count</query>
  </search>
  <option name="charting.chart">line</option>
  <option name="charting.axisTitleX.text">Time</option>
  <option name="charting.axisTitleY.text">Requests</option>
  <option name="charting.legend.placement">bottom</option>
  <option name="charting.lineWidth">2</option>
  <option name="charting.chart.showDataLabels">none</option>
</chart>
```

---

## Exercise 2: Advanced Drilldown Configuration

**Scenario:** Implement sophisticated drilldown behaviors.

### Task 2.1: Link to Custom Search

**Configure drilldown in XML:**
```xml
<table>
  <title>Error Summary</title>
  <search>
    <query>
      index=training sourcetype=web_access status>=400
      | stats count by status, url
      | sort -count
    </query>
  </search>
  <drilldown>
    <link target="_blank">
      <![CDATA[
        search?q=index=training sourcetype=web_access status=$row.status$ url="$row.url$"&earliest=-24h&latest=now
      ]]>
    </link>
  </drilldown>
</table>
```

### Task 2.2: Conditional Drilldown

**Different actions based on click:**
```xml
<chart>
  <title>Status Distribution</title>
  <search>
    <query>
      index=training sourcetype=web_access
      | stats count by status
    </query>
  </search>
  <drilldown>
    <condition field="status">
      <set token="selected_status">$click.value$</set>
      <eval token="status_label">
        case($click.value$ &lt; 300, "Success",
             $click.value$ &lt; 400, "Redirect",
             $click.value$ &lt; 500, "Client Error",
             1=1, "Server Error")
      </eval>
    </condition>
  </drilldown>
</chart>
```

### Task 2.3: Link to Another Dashboard

**Navigate to related dashboard:**
```xml
<drilldown>
  <link target="_blank">
    /app/search/detailed_analysis?form.user=$row.user$&amp;form.time_token.earliest=-24h
  </link>
</drilldown>
```

### Task 2.4: Multi-Action Drilldown

**Set multiple tokens and conditionals:**
```xml
<drilldown>
  <set token="selected_user">$row.user$</set>
  <set token="selected_dept">$row.department$</set>
  <eval token="show_details">if($row.count$ &gt; 100, "true", "false")</eval>
  <condition field="user">
    <set token="user_filter">user="$click.value$"</set>
  </condition>
</drilldown>
```

---

## Exercise 3: Base Searches for Performance

**Scenario:** Use base searches to share results across panels.

### Task 3.1: Define Base Search

**Create reusable search:**
```xml
<search id="base_traffic_search">
  <query>
    index=training sourcetype=web_access
    | lookup users.csv username as user OUTPUT department, city
    | eval status_category = case(
        status &lt; 300, "Success",
        status &lt; 400, "Redirect",
        status &lt; 500, "Client Error",
        status >= 500, "Server Error"
      )
  </query>
  <earliest>$time_token.earliest$</earliest>
  <latest>$time_token.latest$</latest>
</search>
```

### Task 3.2: Use Base Search in Panels

**Reference base search:**
```xml
<row>
  <panel>
    <title>Requests by Department</title>
    <chart>
      <search base="base_traffic_search">
        <query>| stats count by department</query>
      </search>
      <option name="charting.chart">pie</option>
    </chart>
  </panel>

  <panel>
    <title>Status Distribution</title>
    <chart>
      <search base="base_traffic_search">
        <query>| stats count by status_category</query>
      </search>
      <option name="charting.chart">column</option>
    </chart>
  </panel>

  <panel>
    <title>Geographic Distribution</title>
    <table>
      <search base="base_traffic_search">
        <query>
          | stats count, dc(user) as unique_users by city
          | sort -count
        </query>
      </search>
    </table>
  </panel>
</row>
```

**Benefits:**
- Runs base search once
- Reduces load on Splunk
- Faster dashboard load times
- Consistent data across panels

### Task 3.3: Post-Process with Base Search

**Complex post-processing:**
```xml
<search base="base_traffic_search" id="dept_stats">
  <query>
    | stats count as requests,
            avg(response_time) as avg_rt,
            dc(user) as unique_users
            by department
  </query>
</search>

<panel>
  <title>Department Activity</title>
  <table>
    <search base="dept_stats">
      <query>| sort -requests | head 10</query>
    </search>
  </table>
</panel>

<panel>
  <title>Department Performance</title>
  <chart>
    <search base="dept_stats">
      <query>| sort -avg_rt | head 10</query>
    </search>
    <option name="charting.chart">bar</option>
  </chart>
</panel>
```

---

## Exercise 4: Form-Based Dashboards

**Scenario:** Create dashboards with sophisticated input handling.

### Task 4.1: Convert to Form Dashboard

**Change dashboard type:**
```xml
<form version="1.1">
  <label>Traffic Analysis Form</label>
  <fieldset submitButton="true" autoRun="false">
    <!-- Inputs go here -->
  </fieldset>
  <!-- Panels go here -->
</form>
```

**Key differences:**
- `<form>` instead of `<dashboard>`
- `<fieldset>` contains inputs
- submitButton controls when searches run
- autoRun determines initial execution

### Task 4.2: Add Multiple Inputs

**Complex input configuration:**
```xml
<fieldset submitButton="true" autoRun="false">
  <input type="time" token="time_token" searchWhenChanged="false">
    <label>Time Range</label>
    <default>
      <earliest>-24h@h</earliest>
      <latest>now</latest>
    </default>
  </input>

  <input type="dropdown" token="dept_token" searchWhenChanged="false">
    <label>Department</label>
    <choice value="*">All Departments</choice>
    <default>*</default>
    <fieldForLabel>department</fieldForLabel>
    <fieldForValue>department</fieldForValue>
    <search>
      <query>
        index=training sourcetype=web_access user!="-"
        | lookup users.csv username as user OUTPUT department
        | stats count by department
        | sort department
      </query>
    </search>
  </input>

  <input type="multiselect" token="status_token" searchWhenChanged="false">
    <label>Status Codes</label>
    <choice value="2*">2xx Success</choice>
    <choice value="3*">3xx Redirect</choice>
    <choice value="4*">4xx Client Error</choice>
    <choice value="5*">5xx Server Error</choice>
    <default>2*,3*,4*,5*</default>
    <prefix>(</prefix>
    <suffix>)</suffix>
    <valuePrefix>status="</valuePrefix>
    <valueSuffix>"</valueSuffix>
    <delimiter> OR </delimiter>
  </input>

  <input type="text" token="search_token" searchWhenChanged="false">
    <label>Search Text</label>
    <default>*</default>
  </input>

  <input type="radio" token="view_token" searchWhenChanged="true">
    <label>View Type</label>
    <choice value="summary">Summary</choice>
    <choice value="detailed">Detailed</choice>
    <default>summary</default>
  </input>
</fieldset>
```

### Task 4.3: Token Dependencies in Forms

**Dependent inputs:**
```xml
<input type="dropdown" token="dept_token">
  <label>Department</label>
  <choice value="*">All</choice>
  <default>*</default>
  <fieldForLabel>department</fieldForLabel>
  <fieldForValue>department</fieldForValue>
  <search>
    <query>
      | inputlookup users.csv
      | stats count by department
    </query>
  </search>
  <change>
    <set token="show_user_selector">true</set>
  </change>
</input>

<input type="dropdown" token="user_token" depends="$show_user_selector$">
  <label>User</label>
  <choice value="*">All</choice>
  <default>*</default>
  <fieldForLabel>username</fieldForLabel>
  <fieldForValue>username</fieldForValue>
  <search>
    <query>
      | inputlookup users.csv
      | search department=$dept_token$
      | stats count by username
    </query>
  </search>
</input>
```

---

## Exercise 5: Token Manipulation

**Scenario:** Use advanced token techniques for dynamic dashboards.

### Task 5.1: Init Tokens

**Set tokens on dashboard load:**
```xml
<form>
  <label>Advanced Token Dashboard</label>
  <init>
    <set token="default_index">training</set>
    <set token="default_sourcetype">web_access</set>
    <eval token="current_time">now()</eval>
    <eval token="yesterday">relative_time(now(), "-1d@d")</eval>
  </init>
  <!-- Rest of dashboard -->
</form>
```

### Task 5.2: Token Change Handlers

**React to token changes:**
```xml
<input type="dropdown" token="metric_token">
  <label>Select Metric</label>
  <choice value="count">Request Count</choice>
  <choice value="response_time">Response Time</choice>
  <choice value="bytes">Data Transfer</choice>
  <default>count</default>
  <change>
    <eval token="metric_label">case($value$=="count", "Requests",
                                       $value$=="response_time", "Avg Response Time (ms)",
                                       $value$=="bytes", "Total Bytes")</eval>
    <eval token="stat_function">case($value$=="count", "count",
                                      $value$=="response_time", "avg(response_time)",
                                      $value$=="bytes", "sum(bytes)")</eval>
  </change>
</input>

<panel>
  <title>$metric_label$ by Department</title>
  <chart>
    <search>
      <query>
        index=training sourcetype=web_access
        | lookup users.csv username as user OUTPUT department
        | stats $stat_function$ as metric by department
      </query>
    </search>
  </chart>
</panel>
```

### Task 5.3: Conditional Panel Display

**Show/hide panels based on tokens:**
```xml
<input type="radio" token="analysis_type">
  <label>Analysis Type</label>
  <choice value="performance">Performance</choice>
  <choice value="security">Security</choice>
  <choice value="usage">Usage</choice>
  <default>performance</default>
  <change>
    <condition value="performance">
      <set token="show_performance">true</set>
      <unset token="show_security"></unset>
      <unset token="show_usage"></unset>
    </condition>
    <condition value="security">
      <unset token="show_performance"></unset>
      <set token="show_security">true</set>
      <unset token="show_usage"></unset>
    </condition>
    <condition value="usage">
      <unset token="show_performance"></unset>
      <unset token="show_security"></unset>
      <set token="show_usage">true</set>
    </condition>
  </change>
</input>

<row depends="$show_performance$">
  <panel>
    <title>Performance Metrics</title>
    <single>
      <search>
        <query>index=training sourcetype=web_access | stats avg(response_time)</query>
      </search>
    </single>
  </panel>
</row>

<row depends="$show_security$">
  <panel>
    <title>Security Events</title>
    <table>
      <search>
        <query>index=training sourcetype=security_events | stats count by event_type</query>
      </search>
    </table>
  </panel>
</row>

<row depends="$show_usage$">
  <panel>
    <title>Usage Statistics</title>
    <chart>
      <search>
        <query>index=training sourcetype=web_access | timechart count</query>
      </search>
    </chart>
  </panel>
</row>
```

---

## Exercise 6: HTML and CSS Styling

**Scenario:** Customize dashboard appearance with HTML and CSS.

### Task 6.1: Add HTML Panel with Styling

**Custom HTML panel:**
```xml
<panel>
  <html>
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 10px;
                color: white;
                text-align: center;">
      <h1 style="margin: 0; font-size: 2em;">Web Traffic Dashboard</h1>
      <p style="margin: 10px 0 0 0; font-size: 1.2em;">Real-time monitoring and analysis</p>
    </div>
  </html>
</panel>
```

### Task 6.2: Style Tokens in HTML

**Dynamic HTML content:**
```xml
<panel>
  <html>
    <div style="display: flex; justify-content: space-around; padding: 20px;">
      <div style="text-align: center; background: #f0f0f0; padding: 20px; border-radius: 8px; flex: 1; margin: 10px;">
        <h2 style="color: #667eea; margin: 0;">$total_requests$</h2>
        <p style="color: #666; margin: 5px 0 0 0;">Total Requests</p>
      </div>
      <div style="text-align: center; background: #f0f0f0; padding: 20px; border-radius: 8px; flex: 1; margin: 10px;">
        <h2 style="color: #764ba2; margin: 0;">$avg_response_time$ ms</h2>
        <p style="color: #666; margin: 5px 0 0 0;">Avg Response Time</p>
      </div>
      <div style="text-align: center; background: #f0f0f0; padding: 20px; border-radius: 8px; flex: 1; margin: 10px;">
        <h2 style="color: #d93f3c; margin: 0;">$error_rate$%</h2>
        <p style="color: #666; margin: 5px 0 0 0;">Error Rate</p>
      </div>
    </div>
  </html>
</panel>

<!-- Search to populate tokens -->
<search>
  <query>
    index=training sourcetype=web_access
    | stats count as total,
            avg(response_time) as avg_rt,
            sum(eval(if(status>=400,1,0))) as errors
    | eval error_rate = round((errors/total)*100, 2)
    | eval avg_rt = round(avg_rt, 0)
  </query>
  <done>
    <set token="total_requests">$result.total$</set>
    <set token="avg_response_time">$result.avg_rt$</set>
    <set token="error_rate">$result.error_rate$</set>
  </done>
</search>
```

### Task 6.3: Custom CSS (Using Dashboard Studio or JS)

**Inline CSS styling:**
```xml
<dashboard stylesheet="custom_dashboard.css">
  <label>Styled Dashboard</label>
  <!-- Dashboard content -->
</dashboard>
```

**Custom CSS file (appserver/static/custom_dashboard.css):**
```css
/* Panel headers */
.dashboard-panel .panel-head {
    background-color: #667eea;
    color: white;
}

/* Custom class for important panels */
.critical-panel {
    border: 3px solid #d93f3c;
    box-shadow: 0 0 10px rgba(217, 63, 60, 0.3);
}

/* Customize single value displays */
.single-value {
    font-size: 3em;
    font-weight: bold;
}
```

---

## Exercise 7: Dashboard Performance Optimization

**Scenario:** Optimize dashboard load times and responsiveness.

### Task 7.1: Use Global Search

**Share search across dashboard:**
```xml
<search id="global_search">
  <query>
    index=training sourcetype=web_access earliest=-24h
    | fields _time, user, url, status, response_time, bytes
  </query>
  <refresh>5m</refresh>
  <refreshType>delay</refreshType>
</search>
```

### Task 7.2: Implement Search Caching

**Configure refresh strategy:**
```xml
<search base="base_search">
  <query>| stats count by status</query>
  <refresh>10m</refresh>
  <refreshType>delay</refreshType>
</search>
```

**Refresh types:**
- `delay`: Waits for user interaction
- `interval`: Refreshes on schedule regardless

### Task 7.3: Limit Search Results

**Return only needed data:**
```xml
<search>
  <query>
    index=training sourcetype=web_access
    | stats count by url
    | sort -count
    | head 10
  </query>
</search>
```

**Best practices:**
- Use `head` to limit results
- Use `fields` to remove unnecessary fields
- Use specific time ranges
- Avoid `| table *`

---

## Bonus Challenge

Create an enterprise-grade dashboard that includes:
1. Form-based inputs with submit button
2. Base search shared across 6+ panels
3. Conditional panel display based on radio button
4. Custom HTML header with CSS styling
5. Advanced drilldown to another dashboard
6. Token-driven dynamic titles and descriptions
7. Performance-optimized searches
8. Professional color scheme and layout

---

## Key Takeaways

- **Simple XML** provides powerful customization options
- **Base searches** improve performance significantly
- **Advanced tokens** enable dynamic, responsive dashboards
- **Drilldowns** create interactive exploration workflows
- **Form dashboards** provide better user control
- **HTML/CSS** allow complete design customization
- **Performance optimization** ensures fast, responsive dashboards

## Simple XML Quick Reference

### Basic Structure
```xml
<dashboard>
  <label>Title</label>
  <row><panel>...</panel></row>
</dashboard>
```

### Common Elements
- `<search>` - Search definition
- `<chart>` - Chart visualization
- `<table>` - Table visualization
- `<single>` - Single value
- `<html>` - Custom HTML
- `<input>` - Form input

### Token Syntax
- `$token_name$` - Use token value
- `<set token="name">value</set>` - Set token
- `<unset token="name"/>` - Remove token
- `<eval token="name">expression</eval>` - Calculate token

## Dashboard Performance Checklist

- [ ] Use base searches for shared data
- [ ] Limit time ranges appropriately
- [ ] Use `fields` command early in searches
- [ ] Implement search result limits (`head`)
- [ ] Configure appropriate refresh intervals
- [ ] Avoid excessive panel count (< 10 recommended)
- [ ] Use summary indexes when possible
- [ ] Test with realistic data volumes

## Next Steps

Congratulations on completing all 9 labs! You now have advanced Splunk skills including:
- Advanced SPL commands
- Data modeling and pivot
- Interactive dashboards
- Alerts and monitoring
- Performance optimization

Continue practicing and explore Splunk documentation for even more advanced features.

---

**Lab Complete! Course Complete!**
