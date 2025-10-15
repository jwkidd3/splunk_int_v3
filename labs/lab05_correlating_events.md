# Lab 5: Correlating Events

**Splunk Intermediate – Lab Exercises**

> **Note**: This lab should be completed in a non-production environment.

## Lab Description

This lab covers:
- Using the transaction command to correlate related events
- Grouping events by session identifiers
- Calculating transaction duration
- Filtering transactions by duration
- Using startswith and endswith parameters
- Analyzing user sessions and workflows

## Scenario

You are a Splunk administrator for Buttercup Games, an e-commerce company. The web development team needs to analyze user sessions to understand customer behavior, identify long-running transactions, and track the complete purchase workflow from browsing to checkout.

---

## Task 1: Creating Basic Transactions by Session ID

### Scenario

The e-commerce team wants to group all web events that belong to the same user session to understand customer behavior.

### Step 1.1: View Individual Events

First, examine individual web events:

```spl
index=web sourcetype=access_combined_wcookie
| table _time JSESSIONID clientip action productId
| sort _time
```

**Expected Results**: Individual events showing timestamp, session ID, client IP, action, and product ID

### Step 1.2: Create Transactions by Session ID

Use the transaction command to group events by JSESSIONID:

```spl
index=web sourcetype=access_combined_wcookie
| transaction JSESSIONID
| table JSESSIONID duration eventcount
```

**Expected Results**: Each row represents a complete session, showing the session ID, duration in seconds, and number of events in the session

### Step 1.3: Display Actions Within Each Transaction

Show the sequence of actions within each session:

```spl
index=web sourcetype=access_combined_wcookie
| transaction JSESSIONID
| table _time JSESSIONID clientip action duration eventcount
| sort -duration
```

**Expected Results**: Sessions sorted by duration, showing all fields for analysis

**Save this search as**: `L5S1`

> **Note**: The transaction command:
> - Groups events that share common field values
> - Automatically calculates duration (time between first and last event)
> - Adds eventcount (number of events in the transaction)
> - Combines multiple events into a single result

---

## Task 2: Calculating and Analyzing Transaction Duration

### Scenario

The operations team wants to identify sessions that take longer than expected, as they may indicate performance issues or complex customer journeys.

### Step 2.1: Calculate Duration in Minutes

Convert the duration field from seconds to minutes:

```spl
index=web sourcetype=access_combined_wcookie
| transaction JSESSIONID
| eval durationMinutes = round(duration/60, 1)
| table JSESSIONID clientip durationMinutes eventcount
| sort -durationMinutes
```

**Expected Results**: Sessions with duration displayed in minutes, rounded to 1 decimal place

### Step 2.2: Add Duration Statistics

Calculate statistics about session durations:

```spl
index=web sourcetype=access_combined_wcookie
| transaction JSESSIONID
| eval durationMinutes = round(duration/60, 1)
| stats count as Sessions,
        avg(durationMinutes) as "Avg Duration (min)",
        max(durationMinutes) as "Max Duration (min)",
        min(durationMinutes) as "Min Duration (min)"
```

**Expected Results**: Summary statistics showing the distribution of session durations

### Step 2.3: Categorize Sessions by Duration

Classify sessions into duration categories:

```spl
index=web sourcetype=access_combined_wcookie
| transaction JSESSIONID
| eval durationMinutes = round(duration/60, 1)
| eval durationCategory = case(
    durationMinutes < 1, "Quick (< 1 min)",
    durationMinutes >= 1 AND durationMinutes < 5, "Normal (1-5 min)",
    durationMinutes >= 5 AND durationMinutes < 10, "Long (5-10 min)",
    durationMinutes >= 10, "Very Long (> 10 min)"
)
| stats count by durationCategory
| sort -count
```

**Expected Results**: Count of sessions in each duration category

**Save this search as**: `L5S2`

> **Tip**: Understanding session duration helps identify:
> - Performance bottlenecks
> - User engagement patterns
> - Abandoned shopping carts
> - Complex purchase workflows

---

## Task 3: Filtering Transactions by Duration

### Scenario

The development team wants to focus on sessions longer than 1 minute to investigate potential performance issues.

### Step 3.1: Filter Long-Running Sessions

Filter transactions to show only those longer than 1 minute:

```spl
index=web sourcetype=access_combined_wcookie
| transaction JSESSIONID
| eval durationMinutes = round(duration/60, 1)
| where durationMinutes > 1
| table _time JSESSIONID clientip durationMinutes eventcount action
| sort -durationMinutes
```

**Expected Results**: Only sessions longer than 1 minute are displayed

### Step 3.2: Analyze Actions in Long Sessions

Examine what actions occur in long-running sessions:

```spl
index=web sourcetype=access_combined_wcookie
| transaction JSESSIONID
| eval durationMinutes = round(duration/60, 1)
| where durationMinutes > 1
| stats count by action
| sort -count
```

**Expected Results**: Breakdown of actions that occur in sessions longer than 1 minute

### Step 3.3: Identify High-Event Sessions

Find sessions with many events:

```spl
index=web sourcetype=access_combined_wcookie
| transaction JSESSIONID
| eval durationMinutes = round(duration/60, 1)
| where eventcount > 10
| table JSESSIONID clientip durationMinutes eventcount
| sort -eventcount
```

**Expected Results**: Sessions with more than 10 events, indicating active user engagement

**Save this search as**: `L5S3`

> **Note**: Filtering transactions helps you:
> - Focus on specific session types
> - Identify outliers and anomalies
> - Investigate performance issues
> - Understand engaged vs. quick visitors

---

## Task 4: Using Startswith and Endswith Parameters

### Scenario

The sales team wants to track complete purchase workflows - from when a customer adds an item to their cart until they complete the purchase.

### Step 4.1: Define Purchase Workflow Transactions

Create transactions that start with "addtocart" and end with "purchase":

```spl
index=web sourcetype=access_combined_wcookie
| transaction clientip startswith="action=addtocart" endswith="action=purchase"
| table _time clientip duration eventcount
```

**Expected Results**: Only transactions that begin with adding to cart and end with a purchase

### Step 4.2: Analyze Complete Purchase Workflows

Examine the details of complete purchase workflows:

```spl
index=web sourcetype=access_combined_wcookie
| transaction clientip startswith="action=addtocart" endswith="action=purchase"
| eval durationMinutes = round(duration/60, 1)
| table clientip durationMinutes eventcount productId
| sort -durationMinutes
```

**Expected Results**: Complete purchase workflows with duration and event count

### Step 4.3: Calculate Purchase Conversion Metrics

Calculate statistics for purchase workflows:

```spl
index=web sourcetype=access_combined_wcookie
| transaction clientip startswith="action=addtocart" endswith="action=purchase"
| eval durationMinutes = round(duration/60, 1)
| stats count as "Completed Purchases",
        avg(durationMinutes) as "Avg Time to Purchase (min)",
        avg(eventcount) as "Avg Events in Purchase Flow"
```

**Expected Results**: Summary metrics for successful purchase workflows

### Step 4.4: Compare Abandoned vs. Completed Carts

Compare sessions that added items but didn't purchase:

```spl
index=web sourcetype=access_combined_wcookie action=addtocart OR action=purchase
| transaction JSESSIONID maxspan=30m
| eval purchaseCompleted = if(searchmatch("action=purchase"), "Yes", "No")
| stats count by purchaseCompleted
```

**Expected Results**: Count of sessions with completed vs. abandoned purchases

**Save this search as**: `L5S4`

> **Note**: startswith and endswith parameters:
> - Filter transactions to specific event patterns
> - Must match the raw event text or use field=value syntax
> - Useful for analyzing specific workflows
> - Help track conversion funnels and user journeys

---

## Task 5: Advanced Transaction Options

### Scenario

Fine-tune transaction creation with additional parameters for more accurate session analysis.

### Step 5.1: Use Maxspan Parameter

Limit transactions to a maximum time span:

```spl
index=web sourcetype=access_combined_wcookie
| transaction JSESSIONID maxspan=30m
| eval durationMinutes = round(duration/60, 1)
| table JSESSIONID clientip durationMinutes eventcount
| sort -eventcount
```

**Expected Results**: Transactions limited to 30-minute windows, preventing unrealistic long sessions

### Step 5.2: Use Maxpause Parameter

Limit the pause between events within a transaction:

```spl
index=web sourcetype=access_combined_wcookie
| transaction clientip maxpause=5m maxspan=30m
| eval durationMinutes = round(duration/60, 1)
| where eventcount > 1
| table clientip durationMinutes eventcount action
| sort -durationMinutes
```

**Expected Results**: Transactions where events are no more than 5 minutes apart

### Step 5.3: Combine Multiple Parameters

Create precise transactions using multiple parameters:

```spl
index=web sourcetype=access_combined_wcookie
| transaction JSESSIONID maxspan=1h maxpause=10m startswith="action=view" endswith="action=purchase"
| eval durationMinutes = round(duration/60, 1)
| table JSESSIONID durationMinutes eventcount
| stats count as Purchases,
        avg(durationMinutes) as "Avg Duration",
        avg(eventcount) as "Avg Steps"
```

**Expected Results**: Refined purchase transactions with realistic time constraints

> **Tip**: Transaction command parameters:
> - **maxspan**: Maximum total time between first and last event
> - **maxpause**: Maximum time between individual events
> - **maxevents**: Maximum number of events in a transaction
> - **startswith/endswith**: Define transaction boundaries
> - Use these to prevent memory issues and create meaningful transactions

---

## Challenge Exercise (Optional)

### Challenge 1: Shopping Cart Abandonment Analysis

Create a comprehensive analysis of shopping cart abandonment:

1. Identify all sessions where users added items to cart
2. Determine which completed purchases and which didn't
3. Calculate abandonment rate
4. Analyze average time spent before abandonment
5. Identify products most frequently abandoned
6. Create a visualization showing abandonment by product category

**Hints**:
- Use transaction with JSESSIONID
- Check for presence of purchase action
- Calculate time from first addtocart to last event
- Use stats and chart commands for analysis

**Save this search as**: `L5C1`

### Challenge 2: Multi-Step User Journey Analysis

Track the complete user journey through the site:

1. Create transactions showing the sequence: view → addtocart → purchase
2. Calculate conversion rates at each step
3. Identify where users drop off most frequently
4. Calculate average time between each step
5. Create a funnel visualization

Example steps:
- Sessions with view: X
- Sessions with view + addtocart: Y
- Sessions with view + addtocart + purchase: Z
- Conversion rates: Y/X, Z/Y

**Save this search as**: `L5C2`

---

## Summary

In this lab, you learned:
- ✓ How to use the transaction command to correlate related events
- ✓ How to group events by session identifiers like JSESSIONID
- ✓ How to calculate and analyze transaction duration
- ✓ How to filter transactions by duration and event count
- ✓ How to use startswith and endswith to track specific workflows
- ✓ How to use maxspan and maxpause to create realistic transactions

## Key Takeaways

1. **transaction command** groups related events into single results based on common field values
2. **duration** is automatically calculated as the time between first and last event in seconds
3. **eventcount** shows the number of events grouped into each transaction
4. **startswith/endswith** parameters define transaction boundaries for workflow analysis
5. **maxspan** limits the total transaction duration
6. **maxpause** limits the time between events within a transaction
7. Convert duration to minutes using: `eval durationMinutes = round(duration/60, 1)`
8. Transaction analysis is powerful for understanding user behavior and identifying bottlenecks

---

## Data Sources Used

- **index=web, sourcetype=access_combined_wcookie**: Web access logs with JSESSIONID for session tracking, including clientip, action, productId, and timestamp

## Next Steps

In Lab 6, you'll learn about lookups and how to enrich your data by adding external reference information to your search results.

---

**Lab 5 Complete!**
