# Lab 7: Alerts and Scheduled Searches

**Duration:** 30 minutes
**Difficulty:** Intermediate

## Objectives

In this lab, you will learn to:
- Create real-time and scheduled alerts
- Configure alert triggers and conditions
- Set up alert actions (email, webhook, script)
- Implement alert throttling and suppression
- Manage and troubleshoot alerts
- Apply alert best practices

## Prerequisites

- Completed Labs 1-6
- Training data loaded in the `training` index
- Understanding of search and statistical commands

---

## Exercise 1: Creating Your First Alert

**Scenario:** Monitor for high error rates on your web application.

### Task 1.1: Create a Scheduled Alert

**Steps:**
1. Create this search:
```spl
index=training sourcetype=web_access
| stats count as total,
        sum(eval(if(status>=400, 1, 0))) as errors
| eval error_rate = round((errors/total)*100, 2)
| where error_rate > 5
```

2. Click "Save As" → "Alert"
3. Title: "High Error Rate Alert"
4. Description: "Triggers when error rate exceeds 5%"
5. Permissions: Shared in App

**Configure Alert Settings:**
- Alert type: Scheduled
- Time Range: Last 60 minutes
- Cron Schedule: */15 * * * * (every 15 minutes)
- Trigger condition: Number of Results is greater than 0
- Trigger: Once
- Save

**Test:** Run the alert manually to verify it works.

### Task 1.2: Add Email Action

**Configure email alert:**
1. Edit alert → "Add Actions"
2. Select "Send email"
3. To: your-email@company.com
4. Subject: "ALERT: High Error Rate Detected"
5. Message:
```
High error rate detected in web access logs.

Error Rate: $result.error_rate$%
Total Requests: $result.total$
Errors: $result.errors$

Please investigate immediately.
```
6. Include: Results Table, Inline
7. Save

**Note:** Ensure email server is configured in Settings → Server Settings → Email Settings

### Task 1.3: Test the Alert

**Trigger the alert manually:**
1. Open the alert
2. Click "Edit" → "Edit Actions"
3. Click "Run" to test
4. Verify email received (if email configured)

---

## Exercise 2: Real-Time Alerts

**Scenario:** Create alerts that trigger immediately when conditions are met.

### Task 2.1: Create Real-Time Security Alert

**Create alert for failed login attempts:**
```spl
index=training sourcetype=security_events event_type="login_failure"
| stats count by user, src_ip
| where count > 3
```

**Alert Settings:**
- Alert type: Real-time
- Trigger condition: Per-Result
- Trigger: For each result
- Throttle: 5 minutes
- Save

**Alert Action:**
- Add webhook or script action
- Or log to separate index for investigation

### Task 2.2: Create Threshold Alert

**Monitor for slow response times:**
```spl
index=training sourcetype=web_access
| eval slow_response = if(response_time > 2000, 1, 0)
| stats sum(slow_response) as slow_count
| where slow_count > 10
```

**Alert Settings:**
- Alert type: Scheduled
- Schedule: Every 5 minutes
- Trigger: Number of Results > 0
- Action: Email + Log Event

### Task 2.3: Create Anomaly Detection Alert

**Detect unusual traffic patterns:**
```spl
index=training sourcetype=web_access
| timechart span=5m count as requests
| streamstats window=12 avg(requests) as avg_requests, stdev(requests) as stdev_requests
| eval upper_threshold = avg_requests + (2 * stdev_requests)
| eval lower_threshold = avg_requests - (2 * stdev_requests)
| where requests > upper_threshold OR requests < lower_threshold
```

**Alert Settings:**
- Schedule: Every 10 minutes
- Trigger: Number of Results > 0
- Description: "Traffic volume deviation from normal"

---

## Exercise 3: Alert Triggers and Conditions

**Scenario:** Configure sophisticated trigger conditions.

### Task 3.1: Number of Results Trigger

**Alert when specific users appear in security events:**
```spl
index=training sourcetype=security_events severity="high"
| stats count by user
| where count > 2
```

**Trigger:**
- Trigger condition: Number of Results
- Trigger if: greater than 0

### Task 3.2: Number of Hosts Trigger

**Alert when multiple hosts report errors:**
```spl
index=training sourcetype=application level="ERROR"
| stats count by host
```

**Trigger:**
- Trigger condition: Number of Hosts
- Trigger if: greater than 5

### Task 3.3: Number of Sources Trigger

**Alert when errors appear across multiple sources:**
```spl
index=training sourcetype=application level="ERROR"
| stats count by source
```

**Trigger:**
- Trigger condition: Number of Sources
- Trigger if: greater than 3

### Task 3.4: Custom Condition with eval

**Complex condition using result fields:**
```spl
index=training sourcetype=web_access
| stats count as requests,
        avg(response_time) as avg_rt,
        sum(eval(if(status>=400, 1, 0))) as errors
| eval alert_score = (errors * 2) + if(avg_rt > 1000, 10, 0)
| where alert_score > 15
```

**Trigger:**
- Trigger condition: Custom
- Custom condition: search alert_score > 15

---

## Exercise 4: Alert Actions

**Scenario:** Configure various actions when alerts trigger.

### Task 4.1: Email Action with Rich Formatting

**Enhanced email alert:**
```spl
index=training sourcetype=web_access status>=500
| stats count as server_errors,
        values(url) as affected_urls,
        values(clientip) as source_ips
        by host
```

**Email Configuration:**
- Subject: "CRITICAL: Server Errors on $result.host$"
- Message:
```
CRITICAL ALERT: Server Errors Detected

Host: $result.host$
Error Count: $result.server_errors$

Affected URLs:
$result.affected_urls$

Source IPs:
$result.source_ips$

Time: $trigger_time$

Link to search: $results_link$
```
- Priority: High
- Include results as: CSV attachment

### Task 4.2: Webhook Action

**Send alert to external system:**

**Create alert:**
```spl
index=training sourcetype=security_events severity="high"
| stats count, values(event_type) as event_types by user
```

**Add Webhook Action:**
1. Add Actions → Webhook
2. URL: https://your-webhook-url.com/alerts
3. Method: POST
4. Payload:
```json
{
  "alert_name": "High Severity Security Event",
  "user": "$result.user$",
  "event_count": "$result.count$",
  "event_types": "$result.event_types$",
  "timestamp": "$trigger_time$"
}
```

### Task 4.3: Log Event Action

**Write alert results to summary index:**
```spl
index=training sourcetype=web_access
| stats count as requests,
        avg(response_time) as avg_rt,
        sum(eval(if(status>=400, 1, 0))) as errors
        by host
| where errors > 10
```

**Add Action: Log Event**
- Log to index: summary
- This creates searchable alert history

### Task 4.4: Script Action (Advanced)

**Run custom script when alert triggers:**

**Example Python script** (save as alert_script.py in bin/):
```python
import sys
import json

# Read alert results
results = json.load(sys.stdin)

for result in results:
    # Custom logic here
    print(f"Processing alert for: {result.get('user')}")

    # Could:
    # - Update external system
    # - Create ticket
    # - Send custom notification
```

**Configure:**
1. Add Actions → Run a Script
2. Filename: alert_script.py

---

## Exercise 5: Alert Throttling and Suppression

**Scenario:** Prevent alert fatigue with smart throttling.

### Task 5.1: Basic Throttling

**Throttle by time:**
```spl
index=training sourcetype=web_access status>=400
| stats count by url
| where count > 100
```

**Throttle Settings:**
- Suppress triggering: Yes
- Suppress for: 1 hour
- This prevents re-alerting for 1 hour after triggering

### Task 5.2: Field-Based Throttling

**Throttle per specific field value:**
```spl
index=training sourcetype=security_events event_type="login_failure"
| stats count by user
| where count > 5
```

**Advanced Throttle:**
- Suppress triggering: Yes
- Suppress for: 30 minutes
- Fields: user
- This throttles per user (user X alert won't suppress user Y alert)

### Task 5.3: Dynamic Throttling

**Use alert metadata to implement smart throttling:**
```spl
index=training sourcetype=web_access
| stats count as errors by host
| where errors > 50
| lookup alert_history.csv host OUTPUT last_alert_time
| eval hours_since_alert = (now() - last_alert_time) / 3600
| where hours_since_alert > 2 OR isnull(last_alert_time)
```

This implements custom throttling logic within the search.

---

## Exercise 6: Alert Management

**Scenario:** Organize and maintain your alerts effectively.

### Task 6.1: Review Alert History

**View triggered alerts:**
```spl
index=_audit action="alert_fired"
| stats count by savedsearch_name, user
| sort -count
```

**View alert details:**
```spl
index=_internal sourcetype=scheduler savedsearch_name="High Error Rate Alert"
| table _time, status, result_count, run_time, alert_actions
```

### Task 6.2: Monitor Alert Performance

**Check alert execution times:**
```spl
index=_internal sourcetype=scheduler
| stats avg(run_time) as avg_run_time,
        max(run_time) as max_run_time,
        count as executions
        by savedsearch_name
| eval avg_run_time = round(avg_run_time, 2)
| sort -avg_run_time
```

**Question:** Are any alerts taking too long to run?

### Task 6.3: Identify Problematic Alerts

**Find alerts with errors:**
```spl
index=_internal sourcetype=scheduler status="failure"
| stats count by savedsearch_name, status
| sort -count
```

**Find alerts that never trigger:**
```spl
index=_internal sourcetype=scheduler
| stats count, sum(eval(if(result_count>0, 1, 0))) as triggers
        by savedsearch_name
| eval trigger_rate = round((triggers/count)*100, 2)
| where trigger_rate = 0
| sort -count
```

### Task 6.4: Optimize Alert Schedules

**View alert schedule distribution:**
```spl
| rest /services/saved/searches
| search is_scheduled=1 alert.track=1
| eval schedule_time = 'cron_schedule'
| stats count by schedule_time
| sort -count
```

**Best Practice:** Stagger alerts to avoid resource contention

---

## Exercise 7: Alert Best Practices

**Scenario:** Implement industry best practices for alerting.

### Task 7.1: Create Meaningful Alert Names

**Good Examples:**
- "CRITICAL - Server Error Rate > 5%"
- "WARNING - Disk Space Low on Production Servers"
- "INFO - Daily Backup Completion"

**Poor Examples:**
- "Alert 1"
- "Test"
- "Important"

### Task 7.2: Include Context in Alerts

**Good alert search:**
```spl
index=training sourcetype=web_access status>=500
| stats count as error_count,
        latest(_time) as last_error_time,
        values(url) as affected_urls,
        dc(clientip) as unique_ips
        by host
| eval last_error = strftime(last_error_time, "%Y-%m-%d %H:%M:%S")
| where error_count > 10
| table host, error_count, last_error, affected_urls, unique_ips
```

This provides full context for investigation.

### Task 7.3: Set Appropriate Thresholds

**Test threshold with historical data:**
```spl
index=training sourcetype=web_access earliest=-7d
| timechart span=1h count as requests
| stats avg(requests) as avg_requests,
        stdev(requests) as stdev_requests,
        perc95(requests) as p95_requests
| eval recommended_threshold = round(avg_requests + (2 * stdev_requests), 0)
```

Use statistical analysis to set realistic thresholds.

### Task 7.4: Document Alert Purpose

**Include in alert description:**
```
PURPOSE: Detect abnormal error rates that may indicate system issues

THRESHOLD: Error rate > 5% over 60 minutes

ACTION: Page on-call engineer

INVESTIGATION STEPS:
1. Check server health dashboard
2. Review recent deployments
3. Check error logs for patterns
4. Verify network connectivity

FALSE POSITIVE SCENARIOS:
- Maintenance windows
- Load testing
- Known issue already under investigation
```

---

## Exercise 8: Practical Alert Scenarios

**Scenario:** Create real-world alert solutions.

### Task 8.1: Application Health Alert

**Multi-condition health check:**
```spl
index=training sourcetype=application
| stats count as total_events,
        sum(eval(if(level="ERROR" OR level="CRITICAL", 1, 0))) as errors,
        avg(duration_ms) as avg_duration,
        dc(component) as active_components
| eval error_rate = round((errors/total_events)*100, 2)
| eval health_score = case(
    error_rate > 10, "CRITICAL",
    error_rate > 5, "WARNING",
    avg_duration > 1000, "WARNING",
    active_components < 5, "WARNING",
    1=1, "OK"
)
| where health_score != "OK"
```

### Task 8.2: Security Alert with Enrichment

**Enriched security alert:**
```spl
index=training sourcetype=security_events event_type="unauthorized_access"
| lookup users.csv username as user OUTPUT department, role, city
| lookup threat_intel.csv ip_address as src_ip OUTPUT threat_level
| stats count as attempts,
        values(department) as dept,
        values(role) as role,
        values(threat_level) as threat_level
        by user, src_ip
| where attempts > 3 OR isnotnull(threat_level)
```

### Task 8.3: SLA Violation Alert

**Monitor service level agreements:**
```spl
index=training sourcetype=web_access
| stats perc95(response_time) as p95_rt by url
| where p95_rt > 2000
| eval sla_violation = "95th percentile response time exceeds 2 second SLA"
| table url, p95_rt, sla_violation
```

---

## Bonus Challenge

Create a comprehensive alerting strategy that includes:
1. Critical alerts (page immediately)
2. Warning alerts (email, investigate within 1 hour)
3. Info alerts (daily summary email)
4. Proper throttling to prevent alert fatigue
5. Rich context in alert messages
6. Alert history tracking
7. Regular alert review process

---

## Key Takeaways

- **Real-time alerts** for immediate threats
- **Scheduled alerts** for trend analysis
- **Throttling** prevents alert fatigue
- **Context** in alerts speeds investigation
- **Test alerts** before deploying
- **Monitor alert performance** regularly
- **Document alerts** for team understanding
- **Use appropriate thresholds** based on data

## Alert Types Comparison

| Type | Use Case | Latency | Resource Usage |
|------|----------|---------|----------------|
| Real-time | Critical security, immediate threats | Seconds | High |
| Scheduled (frequent) | Operational monitoring | Minutes | Medium |
| Scheduled (periodic) | Trend analysis, SLA monitoring | Hours/Days | Low |

## Alert Action Types

- **Email** - Most common, good for humans
- **Webhook** - Integration with external systems
- **Script** - Custom automation logic
- **Log Event** - Create searchable audit trail
- **Add to Triggered Alerts** - UI management

## Next Steps

In Lab 8, you'll learn about Data Models and the Pivot interface for creating structured data representations.

---

**Lab Complete!**
