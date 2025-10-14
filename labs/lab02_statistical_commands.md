# Lab 2: Statistical Commands and Transformations

**Duration:** 45 minutes
**Difficulty:** Intermediate

## Objectives

In this lab, you will learn to:
- Use stats, chart, and timechart for data aggregation
- Apply eval expressions and functions for data transformation
- Perform statistical analysis on search results
- Create calculated fields and metrics

## Prerequisites

- Completed Lab 1
- Training data loaded in the `training` index

---

## Exercise 1: Stats Command Mastery

**Scenario:** Analyze web traffic patterns to understand user behavior and system performance.

### Task 1.1: Basic Statistical Aggregation

Calculate basic metrics for web access logs:

```spl
index=training sourcetype=web_access
| stats count as total_requests,
        dc(clientip) as unique_ips,
        dc(user) as unique_users,
        avg(bytes) as avg_bytes,
        avg(response_time) as avg_response_time
```

**Questions:**
1. What is the total number of requests?
2. How many unique users accessed the system?
3. What is the average response time?

### Task 1.2: Stats with Grouping (BY clause)

Analyze requests by HTTP method and status:

```spl
index=training sourcetype=web_access
| stats count as requests,
        avg(response_time) as avg_response_time,
        avg(bytes) as avg_bytes
        by method, status
| eval avg_response_time = round(avg_response_time, 2)
| eval avg_bytes = round(avg_bytes, 0)
| sort -requests
```

**Questions:**
1. Which method/status combination has the most requests?
2. Which has the highest average response time?
3. Are there any patterns between status codes and response times?

### Task 1.3: Multiple Statistical Functions

Comprehensive user activity analysis:

```spl
index=training sourcetype=web_access user!="-"
| stats count as requests,
        dc(url) as unique_urls,
        min(response_time) as min_rt,
        max(response_time) as max_rt,
        avg(response_time) as avg_rt,
        stdev(response_time) as stdev_rt,
        sum(bytes) as total_bytes
        by user
| eval avg_rt = round(avg_rt, 2)
| eval stdev_rt = round(stdev_rt, 2)
| eval total_mb = round(total_bytes/1024/1024, 2)
| sort -requests
| head 10
```

**Challenge:** Add a field that calculates the coefficient of variation (CV = stdev/mean) for response times. Which user has the most variable response times?

---

## Exercise 2: Chart Command

**Scenario:** Visualize relationships between different dimensions in your data.

### Task 2.1: Basic Chart

Create a chart showing request counts by method and status:

```spl
index=training sourcetype=web_access
| chart count by method, status
```

**Question:** How does this differ from the stats command output?

### Task 2.2: Chart with Limit

Show top URLs by user:

```spl
index=training sourcetype=web_access user!="-"
| chart count over url by user limit=5
| sort -count
| head 20
```

**Question:** Which URLs are most popular across users?

### Task 2.3: Chart with Statistical Functions

Average response time by hour and status code:

```spl
index=training sourcetype=web_access
| eval hour = strftime(_time, "%H")
| chart avg(response_time) over hour by status
| foreach * [eval <<FIELD>> = round('<<FIELD>>', 2)]
```

**Challenge:** Modify to show the 95th percentile response time instead of average.

---

## Exercise 3: Timechart Command

**Scenario:** Analyze trends over time to identify patterns and anomalies.

### Task 3.1: Basic Timechart

Show request volume over time:

```spl
index=training sourcetype=web_access
| timechart span=1h count as requests
```

**Question:** Are there any notable spikes or drops in traffic?

### Task 3.2: Timechart with Multiple Metrics

Track multiple metrics over time:

```spl
index=training sourcetype=web_access
| timechart span=30m
    count as requests,
    avg(response_time) as avg_response_time,
    avg(bytes) as avg_bytes,
    dc(user) as unique_users
```

**Question:** Do response times correlate with request volume?

### Task 3.3: Timechart by Dimension

Show request trends by status code category:

```spl
index=training sourcetype=web_access
| eval status_category = case(
    status < 300, "Success",
    status < 400, "Redirect",
    status < 500, "Client Error",
    status >= 500, "Server Error",
    1=1, "Unknown"
)
| timechart span=1h count by status_category
```

**Challenge:** Add a calculated field showing error rate percentage over time.

---

## Exercise 4: Eval Command Deep Dive

**Scenario:** Transform and enrich data using eval functions.

### Task 4.1: String Functions

Extract and manipulate URL components:

```spl
index=training sourcetype=web_access
| eval url_length = len(url)
| eval url_lower = lower(url)
| eval has_api = if(like(url, "%/api/%"), "yes", "no")
| eval url_type = case(
    like(url, "%/admin%"), "Admin",
    like(url, "%/api/%"), "API",
    like(url, "%/products%"), "Product",
    1=1, "Other"
)
| stats count by url_type, has_api
| sort -count
```

**Question:** What percentage of requests are API calls?

### Task 4.2: Mathematical Functions

Calculate performance metrics:

```spl
index=training sourcetype=web_access
| eval response_time_sec = response_time / 1000
| eval bytes_kb = bytes / 1024
| eval throughput_kbps = bytes_kb / response_time_sec
| eval performance_score = case(
    response_time < 100 AND status < 400, 100,
    response_time < 500 AND status < 400, 75,
    response_time < 1000 AND status < 400, 50,
    status >= 400, 0,
    1=1, 25
)
| stats avg(performance_score) as avg_score,
        avg(throughput_kbps) as avg_throughput
        by user
| eval avg_score = round(avg_score, 2)
| eval avg_throughput = round(avg_throughput, 2)
| where avg_score > 0
| sort -avg_score
| head 10
```

**Question:** Which user has the best average performance score?

### Task 4.3: Date/Time Functions

Analyze activity patterns by time of day:

```spl
index=training sourcetype=web_access
| eval hour = tonumber(strftime(_time, "%H"))
| eval day_of_week = strftime(_time, "%A")
| eval time_period = case(
    hour >= 0 AND hour < 6, "Night",
    hour >= 6 AND hour < 12, "Morning",
    hour >= 12 AND hour < 18, "Afternoon",
    hour >= 18, "Evening"
)
| stats count as requests,
        dc(user) as unique_users,
        avg(response_time) as avg_rt
        by time_period
| eval avg_rt = round(avg_rt, 2)
| sort hour
```

**Question:** Which time period has the highest activity?

### Task 4.4: Conditional Logic

Create a comprehensive request classification:

```spl
index=training sourcetype=web_access
| eval status_type = case(
    status >= 200 AND status < 300, "Success",
    status >= 300 AND status < 400, "Redirect",
    status >= 400 AND status < 500, "Client Error",
    status >= 500, "Server Error"
)
| eval response_category = case(
    response_time < 100, "Fast",
    response_time < 500, "Normal",
    response_time < 2000, "Slow",
    1=1, "Very Slow"
)
| eval size_category = case(
    bytes < 1000, "Small",
    bytes < 10000, "Medium",
    bytes < 100000, "Large",
    1=1, "Very Large"
)
| stats count by status_type, response_category, size_category
| sort -count
```

**Challenge:** Add a risk score based on status, response time, and failed authentication attempts.

---

## Exercise 5: Advanced Statistical Analysis

**Scenario:** Perform in-depth analysis to identify outliers and trends.

### Task 5.1: Percentile Analysis

Find response time percentiles:

```spl
index=training sourcetype=web_access
| stats count,
        perc50(response_time) as median,
        perc90(response_time) as p90,
        perc95(response_time) as p95,
        perc99(response_time) as p99,
        max(response_time) as max
        by url
| where count > 100
| sort -p99
| head 10
```

**Question:** Which URLs have the worst 99th percentile response times?

### Task 5.2: Rate Calculations

Calculate error rates and success rates:

```spl
index=training sourcetype=web_access
| eval is_error = if(status >= 400, 1, 0)
| eval is_success = if(status >= 200 AND status < 300, 1, 0)
| stats count as total,
        sum(is_error) as errors,
        sum(is_success) as successes
        by user
| eval error_rate = round((errors / total) * 100, 2)
| eval success_rate = round((successes / total) * 100, 2)
| where total > 10
| sort -error_rate
```

**Question:** Which users have error rates above 10%?

### Task 5.3: Moving Averages

Calculate rolling average response time:

```spl
index=training sourcetype=web_access
| timechart span=10m avg(response_time) as avg_rt
| streamstats window=6 avg(avg_rt) as moving_avg_rt
| eval avg_rt = round(avg_rt, 2)
| eval moving_avg_rt = round(moving_avg_rt, 2)
| eval deviation = round(avg_rt - moving_avg_rt, 2)
```

**Challenge:** Identify time periods where the response time deviates significantly from the moving average.

---

## Exercise 6: Combining Statistical Commands

**Scenario:** Build a comprehensive performance dashboard query.

### Task 6.1: Multi-Stage Analysis

Create a complete performance analysis:

```spl
index=training sourcetype=web_access
| eval hour = strftime(_time, "%Y-%m-%d %H:00")
| stats count as requests,
        dc(user) as unique_users,
        dc(clientip) as unique_ips,
        sum(eval(if(status >= 400, 1, 0))) as errors,
        avg(response_time) as avg_rt,
        perc95(response_time) as p95_rt,
        sum(bytes) as total_bytes
        by hour
| eval error_rate = round((errors / requests) * 100, 2)
| eval avg_rt = round(avg_rt, 2)
| eval p95_rt = round(p95_rt, 2)
| eval total_mb = round(total_bytes / 1024 / 1024, 2)
| sort -hour
| head 24
```

**Question:** What patterns do you see in the data over the last 24 hours?

---

## Bonus Challenge

Create a comprehensive user behavior analysis that:
1. Categorizes users by activity level (low, medium, high)
2. Calculates multiple statistical measures for each category
3. Identifies outliers using standard deviation
4. Presents results in a clear, actionable format

**Hint:** You'll need to use stats, eval, and possibly eventstats.

---

## Key Takeaways

- **stats** - Most flexible aggregation command, use for grouping and calculations
- **chart** - Creates two-dimensional aggregations (like pivot tables)
- **timechart** - Specifically designed for time-series analysis
- **eval** - Essential for data transformation and calculated fields
- Use statistical functions (avg, sum, count, perc, stdev) to gain insights
- Combine commands to build complex analytical queries

## Common Functions Reference

### Statistical Functions
- `count()` - Count events
- `dc()` - Distinct count
- `avg()`, `sum()`, `min()`, `max()` - Basic math
- `stdev()`, `var()` - Statistical measures
- `perc##()` - Percentiles (perc50, perc95, etc.)

### Eval Functions
- String: `len()`, `lower()`, `upper()`, `substr()`, `replace()`
- Math: `round()`, `ceil()`, `floor()`, `abs()`, `sqrt()`
- Date: `strftime()`, `strptime()`, `now()`, `relative_time()`
- Conditional: `if()`, `case()`, `coalesce()`, `like()`

## Next Steps

In Lab 3, you'll learn about field extractions to extract structured data from unstructured logs.

---

**Lab Complete!**
