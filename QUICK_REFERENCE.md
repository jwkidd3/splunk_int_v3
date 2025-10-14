# Splunk Intermediate - Quick Reference Guide

## Essential SPL Commands

### Advanced Search Commands

#### Subsearch
```spl
index=main [search index=security | return user]
```
- Runs inner search first
- Maximum 50,000 results
- Use `return` to control output

#### Transaction
```spl
index=main | transaction user maxpause=30m
```
- Groups related events
- Options: `maxpause`, `maxspan`, `startswith`, `endswith`
- Creates `duration` and `eventcount` fields

#### Multisearch
```spl
| multisearch
    [search index=web | eval source="Web"]
    [search index=app | eval source="App"]
```
- Runs searches in parallel
- Faster than append

### Statistical Commands

#### Stats
```spl
| stats count, avg(response_time), dc(user) by status
```
- Most flexible aggregation
- Functions: count, sum, avg, min, max, dc, values, list

#### Chart
```spl
| chart count over url by status
```
- Two-dimensional aggregation
- Like a pivot table

#### Timechart
```spl
| timechart span=1h count by status
```
- Time-series aggregation
- Use `span` for time bucket size

### Eval Functions

#### String Functions
```spl
| eval url_lower = lower(url)
| eval url_len = len(url)
| eval has_api = if(like(url, "%/api/%"), "yes", "no")
```

#### Math Functions
```spl
| eval rt_sec = response_time / 1000
| eval rounded = round(value, 2)
| eval percentage = (part/total) * 100
```

#### Date/Time Functions
```spl
| eval hour = strftime(_time, "%H")
| eval day = strftime(_time, "%A")
| eval yesterday = relative_time(now(), "-1d@d")
```

#### Case Statement
```spl
| eval category = case(
    value < 10, "Low",
    value < 50, "Medium",
    value < 100, "High",
    1=1, "Very High"
)
```

## Field Extraction

### Rex Command
```spl
| rex field=message "order #(?<order_id>\d+)"
| rex field=url "/api/(?<endpoint>[^/]+)"
```

### Calculated Fields
Settings → Fields → Calculated Fields
```spl
case(status < 300, "Success", status < 400, "Redirect", 1=1, "Error")
```

## Lookups

### Manual Lookup
```spl
| lookup users.csv username as user OUTPUT department, role
```

### Inputlookup
```spl
| inputlookup users.csv
```

### Outputlookup
```spl
| stats count by user
| outputlookup user_stats.csv
```

### Append to Lookup
```spl
| outputlookup append=true historical_data.csv
```

## Visualization Reference

| Data Type | Best Visualization |
|-----------|-------------------|
| Time trends | Line Chart |
| Category comparison | Column/Bar Chart |
| Composition (parts of whole) | Pie Chart |
| KPIs/Single metrics | Single Value, Gauge |
| Correlation | Scatter Plot |
| Multi-dimensional | Bubble Chart |
| Detailed data | Table |

## Dashboard Tokens

### Using Tokens
```spl
index=training user=$user_token$ status=$status_token$
```

### Setting Tokens (XML)
```xml
<set token="selected_user">$row.user$</set>
<eval token="score">$value$ * 100</eval>
<unset token="temp_token"/>
```

### Form Inputs
```xml
<input type="dropdown" token="dept_token">
  <label>Department</label>
  <choice value="*">All</choice>
  <default>*</default>
</input>
```

## Alert Triggers

### Number of Results
```
Trigger if: Number of Results > 0
```

### Custom Condition
```spl
| stats count, avg(response_time) as avg_rt
| where count > 100 AND avg_rt > 1000
```

### Throttling
```
Suppress for: 1 hour
Throttle by fields: user, host
```

## Data Model & tstats

### Basic tstats
```spl
| tstats count from datamodel=Web_Traffic
```

### With Grouping
```spl
| tstats count from datamodel=Web_Traffic
    by Web_Access.method, Web_Access.status
| rename Web_Access.* as *
```

### Time-based
```spl
| tstats count from datamodel=Web_Traffic
    where earliest=-24h
    by _time span=1h
```

## Performance Tips

### 1. Filter Early
```spl
index=main status>=400 earliest=-1h | stats count by url
```

### 2. Use Specific Time Ranges
```spl
earliest=-1h latest=now
```

### 3. Limit Fields
```spl
| fields _time, user, status, response_time
```

### 4. Use Base Searches (Dashboard)
```xml
<search id="base">
  <query>index=main</query>
</search>
<search base="base">
  <query>| stats count by status</query>
</search>
```

### 5. Avoid Wildcards at Start
```spl
url="/api/*"  ← Good
url="*/api/*" ← Slow
```

## Common Patterns

### Calculate Rate
```spl
| stats count as total,
        sum(eval(if(status>=400, 1, 0))) as errors
        by host
| eval error_rate = round((errors/total)*100, 2)
```

### Moving Average
```spl
| timechart span=10m avg(response_time) as avg_rt
| streamstats window=6 avg(avg_rt) as moving_avg
```

### Percentiles
```spl
| stats perc50(response_time) as median,
        perc90(response_time) as p90,
        perc95(response_time) as p95,
        perc99(response_time) as p99
```

### Top N Results
```spl
| stats count by url
| sort -count
| head 10
```

### Rare Values
```spl
| rare limit=10 url
```

## Regular Expressions

### Common Patterns
- `.` - Any character
- `\d` - Digit (0-9)
- `\w` - Word character (a-z, A-Z, 0-9, _)
- `\s` - Whitespace
- `*` - Zero or more
- `+` - One or more
- `?` - Zero or one
- `[abc]` - Character class
- `(?<name>...)` - Named capture group

### Examples
```spl
# Extract order ID
| rex "order[:\s]+(?<order_id>\d+)"

# Extract IP address
| rex "(?<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"

# Extract quoted string
| rex "\"(?<quoted_text>[^\"]+)\""
```

## Keyboard Shortcuts

### Splunk Web
- `Ctrl + \` - Focus search bar
- `Ctrl + Shift + E` - Export results
- `Ctrl + S` - Save search

### Dashboard Navigation
- `Arrow keys` - Navigate slides (presentation)
- `ESC` - Overview mode (presentation)

## Common Gotchas

1. **Subsearch Limits**: Default 50,000 results, 60 second timeout
2. **Transaction Performance**: Can be slow on large datasets
3. **Token Syntax**: Use `$token$` not `{token}`
4. **Case Sensitivity**: Field names are case-sensitive
5. **Eval vs. Where**: `where` requires boolean expression, `eval` creates fields
6. **Stats vs. Chart**: Stats is more flexible, chart is for 2D aggregation

## Index Time vs. Search Time

### Index Time
- Fastest (processed once during indexing)
- Requires reindexing to change
- Examples: sourcetype, host, source

### Search Time
- Slower (processed every search)
- Can be changed without reindexing
- Examples: field extractions, lookups, calculated fields

## Best Practices

### Searches
1. Use specific indexes and time ranges
2. Filter before aggregating
3. Use fields command to limit data
4. Test on small time ranges first
5. Save commonly used searches

### Dashboards
1. Keep panel count under 10
2. Use base searches for shared data
3. Implement appropriate refresh intervals
4. Test with realistic data volumes
5. Document complex logic

### Alerts
1. Use descriptive names
2. Include context in alert messages
3. Implement throttling to prevent spam
4. Test trigger conditions thoroughly
5. Monitor alert performance

### Data Models
1. Start with simple structure
2. Test before accelerating
3. Monitor acceleration health
4. Document objects and fields
5. Use meaningful names

## Troubleshooting

### Search Running Slow
- Check time range
- Verify index is specified
- Look for inefficient regex
- Consider summary indexing

### No Results
- Verify time range
- Check index permissions
- Verify field names (case-sensitive)
- Test simplified version

### Dashboard Not Loading
- Check search syntax
- Verify token usage
- Test base searches independently
- Check browser console for errors

### Alert Not Triggering
- Run search manually
- Check trigger conditions
- Verify schedule is enabled
- Check alert permissions

---

**Keep this guide handy during labs and real-world Splunk work!**
