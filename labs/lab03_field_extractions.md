# Lab 3: Working with Fields and Field Extractions

**Duration:** 45 minutes
**Difficulty:** Intermediate

## Objectives

In this lab, you will learn to:
- Understand how Splunk extracts fields from data
- Create custom field extractions using the Field Extractor (FX)
- Use the rex command for inline field extraction
- Create calculated fields
- Manage and optimize field extractions

## Prerequisites

- Completed Labs 1 and 2
- Training data loaded in the `training` index
- Understanding of regular expressions (helpful but not required)

---

## Exercise 1: Understanding Automatic Field Extraction

**Scenario:** Examine how Splunk automatically extracts fields from different data types.

### Task 1.1: Explore Automatic Fields

View fields extracted from web access logs:

```spl
index=training sourcetype=web_access
| head 10
| table _time, _raw, clientip, method, url, status, bytes, response_time
```

**Questions:**
1. Which fields are automatically extracted?
2. Which fields are present in the raw data but not extracted?
3. Click on an event - what fields are shown in the left sidebar?

### Task 1.2: Examine JSON Data

Look at application logs (JSON format):

```spl
index=training sourcetype=application
| head 10
| table _time, timestamp, level, component, user, message
```

**Question:** How does field extraction differ between JSON and other formats?

### Task 1.3: Compare Field Extraction Performance

```spl
index=training
| stats count by sourcetype
| appendcols [search index=training | stats dc(_raw) as raw_events]
```

**Question:** Which sourcetype has the most automatic field extractions?

---

## Exercise 2: Using the Rex Command

**Scenario:** Extract custom fields from logs using inline regular expressions.

### Task 2.1: Basic Rex Extraction

Extract order IDs from application messages:

```spl
index=training sourcetype=application component="PaymentService"
| rex field=message "order #(?<order_id>\d+)"
| where isnotnull(order_id)
| stats count by order_id
| sort -count
```

**Question:** How many unique order IDs were processed?

### Task 2.2: Multiple Field Extraction

Extract multiple fields from web access logs:

```spl
index=training sourcetype=web_access url="/api/*"
| rex field=url "/api/(?<api_endpoint>[^/?]+)(?:\?id=(?<resource_id>\d+))?"
| stats count by api_endpoint, resource_id
| sort -count
```

**Challenge:** Modify the rex to also extract any additional query parameters.

### Task 2.3: Extract Response Time Categories

Create performance categories from response times:

```spl
index=training sourcetype=web_access
| rex field=_raw "response_time=(?<rt_ms>\d+)"
| eval rt_category = case(
    rt_ms < 100, "Excellent",
    rt_ms < 500, "Good",
    rt_ms < 1000, "Fair",
    rt_ms < 2000, "Poor",
    1=1, "Critical"
)
| stats count by rt_category, method
| sort rt_category
```

**Question:** What percentage of requests fall into each category?

### Task 2.4: Extract User Agent Components

Parse user agent strings:

```spl
index=training sourcetype=web_access
| rex field=_raw "\"(?<user_agent>[^\"]+)\"$"
| rex field=user_agent "Mozilla/[^\(]+\((?<os_info>[^)]+)"
| rex field=user_agent "(?<browser>Chrome|Firefox|Safari|Edge|MSIE)/(?<browser_version>[\d.]+)"
| stats count by browser, os_info
| sort -count
```

**Question:** Which browser and OS combination is most common?

---

## Exercise 3: Field Extractor (FX) - UI Method

**Scenario:** Use Splunk's GUI to create persistent field extractions.

### Task 3.1: Extract Session Duration

1. Run this search:
```spl
index=training sourcetype=application message="Session created*"
| head 100
```

2. Click on "Extract New Fields" (or open Field Extractor from Settings)
3. Select a sample event
4. Use the UI to extract the session ID from the message
5. Name the field: `session_id`
6. Set permissions: App = "search", Sharing = "App"

**Manual alternative using regex:**
```spl
index=training sourcetype=application message="Session created*"
| rex field=message "Session created for (?<extracted_user>\w+)"
| stats count by extracted_user
```

### Task 3.2: Validate Field Extraction

Test your new field extraction:

```spl
index=training sourcetype=application
| where isnotnull(session_id)
| stats count by session_id
| sort -count
```

**Question:** How many events have the new field?

---

## Exercise 4: Advanced Rex Techniques

**Scenario:** Use advanced regex patterns for complex extractions.

### Task 4.1: Extract with Named Groups

Extract multiple transaction details:

```spl
index=training sourcetype=application component="OrderService"
| rex field=message "Order #(?<order_num>\d+) (?<order_action>created|shipped|delivered) by (?<order_user>\w+)"
| where isnotnull(order_num)
| stats count by order_action, order_user
| sort -count
```

**Question:** Which user has created the most orders?

### Task 4.2: Mode Parameter (sed mode)

Use rex in sed mode to clean data:

```spl
index=training sourcetype=web_access
| rex mode=sed field=url "s/\?.*$//"
| stats count by url
| sort -count
| head 20
```

**Question:** How does this differ from the original URL counts?

### Task 4.3: Multi-Value Field Extraction

Extract all query parameters from URLs:

```spl
index=training sourcetype=web_access url="*?*"
| rex max_match=0 field=url "\?(?<query_params>[^\"]+)"
| rex max_match=0 field=query_params "(?<param_key>\w+)="
| stats count by param_key
| sort -count
```

**Challenge:** Extract both parameter names AND values as paired fields.

### Task 4.4: Negative Lookahead/Lookbehind

Extract log levels that are followed by specific components:

```spl
index=training sourcetype=application
| rex field=message "(?<severity_word>error|fail|success|complete)(?=.*Service)"
| where isnotnull(severity_word)
| stats count by severity_word, component
```

---

## Exercise 5: Calculated Fields

**Scenario:** Create persistent calculated fields through the UI.

### Task 5.1: Create a Calculated Field via UI

**Via UI (recommended for persistent fields):**
1. Settings → Fields → Calculated Fields
2. Click "New Calculated Field"
3. Select app: "search"
4. Apply to sourcetype: "web_access"
5. Name: `status_category`
6. Eval expression:
```
case(status < 300, "Success", status < 400, "Redirect", status < 500, "Client Error", status >= 500, "Server Error")
```

**Test with search:**
```spl
index=training sourcetype=web_access
| stats count by status_category
```

### Task 5.2: Create Response Performance Field

Create a calculated field for response performance:

**Eval expression for calculated field:**
```
case(response_time < 100, "Fast", response_time < 500, "Normal", response_time < 2000, "Slow", 1=1, "Critical")
```

**Test:**
```spl
index=training sourcetype=web_access
| stats avg(response_time) as avg_rt by response_performance
| sort avg_rt
```

### Task 5.3: Create Data Volume Field

Create a field to categorize data transfer sizes:

```spl
index=training sourcetype=web_access
| eval size_mb = round(bytes/1024/1024, 3)
| eval size_category = case(
    size_mb < 0.001, "Tiny",
    size_mb < 0.01, "Small",
    size_mb < 0.1, "Medium",
    size_mb < 1, "Large",
    1=1, "Very Large"
)
| stats count, sum(size_mb) as total_mb by size_category
| eval total_mb = round(total_mb, 2)
```

**Challenge:** Make this a calculated field and use it in subsequent searches.

---

## Exercise 6: Field Aliases

**Scenario:** Create field aliases for consistent naming across different sourcetypes.

### Task 6.1: Create Field Alias via UI

**Via UI:**
1. Settings → Fields → Field Aliases
2. New Field Alias
3. App: "search"
4. Sourcetype: "application"
5. Name: `user_alias`
6. Alias: `username` = `user`

**Test:**
```spl
index=training sourcetype=application
| stats count by username, user
```

**Question:** Can you now use both `user` and `username` to refer to the same field?

### Task 6.2: Cross-Sourcetype Field Normalization

Create aliases to normalize user field names:

```spl
index=training (sourcetype=web_access OR sourcetype=application)
| eval normalized_user = coalesce(user, username, userid)
| stats count by normalized_user, sourcetype
| sort -count
```

**Challenge:** Create field aliases to make this normalization automatic.

---

## Exercise 7: Field Extraction Performance

**Scenario:** Understand the performance impact of field extractions.

### Task 7.1: Compare Extraction Methods

Test performance of different extraction methods:

```spl
index=training sourcetype=web_access
| rex field=_raw "status=(?<rex_status>\d+)"
| eval eval_status = status
| stats count by rex_status, eval_status
```

**Question:** Which method is faster for fields already automatically extracted?

### Task 7.2: Optimize Field Extractions

Limit field extraction to specific conditions:

```spl
index=training sourcetype=web_access status>=400
| rex field=_raw "status=(?<error_status>\d+)"
| stats count by error_status, url
| sort -count
```

**Best Practice:** Only extract fields when needed, especially in high-volume searches.

### Task 7.3: Late-Bound vs. Early-Bound

Understand when fields are extracted:

```spl
index=training sourcetype=web_access
| rex field=_raw "user=(?<late_bound_user>[^ ]+)"
| where status >= 400
| stats count by late_bound_user
```

**Question:** When is the rex extraction performed - before or after the where clause?

---

## Exercise 8: Practical Field Extraction Scenarios

**Scenario:** Apply field extractions to real-world problems.

### Task 8.1: Extract Transaction IDs

Create a comprehensive transaction tracking system:

```spl
index=training sourcetype=application
| rex field=message "(?<transaction_type>Payment|Order|Refund)[^\#]*\#(?<transaction_id>\d+)"
| where isnotnull(transaction_id)
| stats count as events,
        dc(user) as unique_users,
        values(component) as components
        by transaction_type, transaction_id
| sort -events
```

**Question:** Which transaction has the most associated events?

### Task 8.2: Parse Error Messages

Extract error codes and descriptions:

```spl
index=training sourcetype=application level IN ("ERROR", "CRITICAL")
| rex field=message "(?i)error[:\s]+(?<error_message>[^,\.]+)"
| rex field=message "code[:\s]+(?<error_code>\w+)"
| stats count by error_code, error_message
| sort -count
```

**Challenge:** Create categories for error types (network, database, validation, etc.)

### Task 8.3: Extract Performance Metrics

Pull out all numeric metrics from logs:

```spl
index=training sourcetype=application
| rex field=message "duration[_\s]*(?<duration_ms>\d+)"
| where isnotnull(duration_ms)
| stats avg(duration_ms) as avg_duration,
        max(duration_ms) as max_duration,
        perc95(duration_ms) as p95_duration
        by component
| eval avg_duration = round(avg_duration, 2)
| sort -avg_duration
```

---

## Bonus Challenge

Create a comprehensive field extraction solution that:
1. Extracts user journey information from web logs (entry page, exit page, pages visited)
2. Categorizes sessions by user behavior patterns
3. Calculates session metrics using extracted fields
4. Creates a calculated field for session quality score

---

## Key Takeaways

- **Automatic extraction** works well for structured data (JSON, KV pairs)
- **rex command** provides flexible inline extraction
- **Field Extractor UI** creates persistent extractions saved in props.conf
- **Calculated fields** create derived fields automatically
- **Field aliases** normalize field names across sources
- Performance: Extract fields only when needed, use automatic extraction when possible

## Field Extraction Best Practices

1. **Use automatic extraction** when possible (structured data)
2. **Rex for one-time extractions** in ad-hoc searches
3. **Field Extractor for persistent** extractions used repeatedly
4. **Calculated fields** for derived values used frequently
5. **Test extractions** on sample data before deploying
6. **Document regex patterns** for maintenance

## Regular Expression Quick Reference

- `.` - Any single character
- `*` - Zero or more of previous
- `+` - One or more of previous
- `?` - Zero or one of previous
- `\d` - Digit (0-9)
- `\w` - Word character (a-z, A-Z, 0-9, _)
- `\s` - Whitespace
- `[abc]` - Character class
- `(...)` - Capture group
- `(?<name>...)` - Named capture group

## Next Steps

In Lab 4, you'll learn about lookups and data enrichment to enhance your data with external information.

---

**Lab Complete!**
