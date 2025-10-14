# Lab 1: Advanced Search Commands

**Duration:** 30 minutes
**Difficulty:** Intermediate

## Objectives

In this lab, you will learn to:
- Use subsearches to create dynamic filters
- Group related events using the transaction command
- Combine multiple searches with multisearch
- Apply advanced search techniques to real-world scenarios

## Prerequisites

- Splunk instance running with training data loaded
- Access to the `training` index
- Basic understanding of SPL (Search Processing Language)

## Lab Setup

Ensure you have:
1. Started Splunk: `scripts/start-splunk.bat`
2. Logged in at http://localhost:8000 (admin/password)
3. Generated sample data: `scripts/generate-data.bat`
4. Uploaded data files to the `training` index

---

## Exercise 1: Using Subsearches

**Scenario:** You need to find all web access logs from users who have had failed login attempts in the security logs.

### Task 1.1: Identify Failed Login Users

First, let's find users with failed login attempts:

```spl
index=training sourcetype=security_events event_type="login_failure"
| stats count by user
| table user
```

**Question:** How many users have failed login attempts?

### Task 1.2: Use Subsearch to Filter Web Logs

Now use a subsearch to find web access logs from these users:

```spl
index=training sourcetype=web_access
    [search index=training sourcetype=security_events event_type="login_failure"
    | stats count by user
    | rename user as user_field
    | return 100 user_field]
| stats count by user, status
| sort -count
```

**Question:** Which user with failed logins has the most web activity?

### Task 1.3: Find High-Value Transactions

Find users who made purchases over $500, then find all their web sessions:

```spl
index=training sourcetype=web_access
    [search index=training sourcetype=application component="PaymentService"
    | rex field=message "order #(?<order_id>\d+)"
    | where random() % 10 == 0
    | stats count by user
    | return 50 user]
| stats count by user, url
| sort -count
```

**Challenge:** Modify the search to show only failed HTTP requests (status >= 400) for these users.

---

## Exercise 2: Transaction Command

**Scenario:** Track user sessions across multiple events to understand complete user journeys.

### Task 2.1: Create Basic Transactions

Group web events into sessions by user and IP address:

```spl
index=training sourcetype=web_access user!="-"
| transaction user clientip maxpause=30m
| table user, clientip, duration, eventcount, _time
| sort -duration
```

**Question:** What is the longest session duration? How many events does it contain?

### Task 2.2: Transaction with Start and End Events

Create transactions from login to logout:

```spl
index=training sourcetype=web_access
| transaction user startswith="/login" endswith="/logout" maxspan=4h
| where eventcount > 5
| table user, duration, eventcount, _time
| eval duration_minutes = round(duration/60, 2)
| table user, duration_minutes, eventcount
| sort -duration_minutes
```

**Question:** Which user has the longest login-to-logout session?

### Task 2.3: Identify Incomplete Transactions

Find sessions where users logged in but never logged out:

```spl
index=training sourcetype=web_access url IN ("/login", "/logout")
| transaction user startswith="/login" endswith="/logout" maxspan=4h
| where closed_txn=0
| table user, _time, eventcount, duration
```

**Question:** How many incomplete sessions are there? What might this indicate?

---

## Exercise 3: Multisearch Command

**Scenario:** Compare metrics across different data sources simultaneously.

### Task 3.1: Compare Event Counts

Compare event volumes across different sourcetypes:

```spl
| multisearch
    [search index=training sourcetype=web_access | eval source="Web Access"]
    [search index=training sourcetype=application | eval source="Application"]
    [search index=training sourcetype=security_events | eval source="Security"]
| stats count by source
| sort -count
```

**Question:** Which source has the most events?

### Task 3.2: Parallel User Analysis

Analyze user activity across web and application logs:

```spl
| multisearch
    [search index=training sourcetype=web_access
     | stats count as web_count by user]
    [search index=training sourcetype=application
     | stats count as app_count by user]
| stats sum(web_count) as web_events, sum(app_count) as app_events by user
| eval total = web_events + app_events
| sort -total
| head 10
```

**Question:** Who is the most active user across both systems?

### Task 3.3: Error Rate Comparison

Compare error rates between web and application logs:

```spl
| multisearch
    [search index=training sourcetype=web_access
     | eval error=if(status>=400, 1, 0)
     | stats count as total, sum(error) as errors
     | eval source="Web", error_rate=round((errors/total)*100, 2)]
    [search index=training sourcetype=application
     | eval error=if(level="ERROR" OR level="CRITICAL", 1, 0)
     | stats count as total, sum(error) as errors
     | eval source="Application", error_rate=round((errors/total)*100, 2)]
| table source, total, errors, error_rate
```

**Question:** Which system has a higher error rate?

---

## Exercise 4: Advanced Combined Techniques

**Scenario:** Investigate a potential security incident using advanced search techniques.

### Task 4.1: Identify Suspicious Activity Pattern

Find users with high error rates who also appear in security events:

```spl
index=training sourcetype=web_access
    [search index=training sourcetype=security_events severity="high"
    | stats count by user
    | where count > 2
    | return 20 user]
| stats count as attempts,
        sum(eval(if(status>=400, 1, 0))) as errors
        by user
| eval error_rate = round((errors/attempts)*100, 2)
| where error_rate > 10
| sort -error_rate
```

**Question:** Which users have both security events and high error rates?

### Task 4.2: Transaction Analysis for Incident Response

Track the complete activity timeline for a suspicious user:

```spl
index=training (sourcetype=web_access OR sourcetype=security_events) user="alice"
| transaction user maxspan=1h
| where eventcount > 10
| table _time, eventcount, duration, closed_txn
| eval duration_min = round(duration/60, 2)
```

**Challenge:** Expand this search to include application logs and identify any error patterns during these transactions.

---

## Bonus Challenge

Create a comprehensive search that:
1. Identifies users with failed security events
2. Uses subsearch to find their web activity
3. Groups their activity into transactions
4. Compares their behavior to normal users using multisearch

**Hint:** You'll need to combine subsearch, transaction, and multisearch commands.

---

## Key Takeaways

- **Subsearches** create dynamic filters based on search results (limited to 50,000 results by default)
- **Transaction command** groups events by common fields with time constraints
- **Multisearch** runs multiple searches in parallel for comparison
- Combining these commands enables complex analytical queries
- Always consider performance implications with subsearches and transactions

## Common Pitfalls

1. **Subsearch limitations:** Maximum 50,000 results (use `return` to control)
2. **Transaction performance:** Can be resource-intensive on large datasets
3. **Multisearch syntax:** Each subsearch must be complete and independent
4. **Field name conflicts:** Use `rename` to avoid field name collisions

## Next Steps

In Lab 2, you'll learn about statistical commands and transformations to aggregate and analyze your search results.

---

**Lab Complete!**

Save any searches you found particularly useful for future reference.
