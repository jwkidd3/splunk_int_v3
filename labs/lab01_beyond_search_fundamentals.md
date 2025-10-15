# Lab 1: Beyond Search Fundamentals

**Splunk Intermediate – Lab Exercises**

> **Note**: This lab should be completed in a non-production environment.

## Lab Description

This lab covers:
- Search fundamentals review
- Using the Job Inspector
- Understanding search modes
- Using the table command

## Scenario

You are a Splunk administrator for Buttercup Games, an e-commerce company that sells games and gaming equipment. You need to analyze web traffic and security data to ensure the platform is running smoothly and securely.

---

## Task 1: Search Fundamentals Questions

Answer the following questions about Splunk search fundamentals:

### Questions

1. **Are search terms case-sensitive?**
   - Test this by searching for `productid` vs `productId`

2. **What is the wildcarding character?**
   - How would you search for all product IDs?

3. **What is the most efficient way to filter search results?**
   - Index-time vs search-time filtering

4. **What are the default fields always present in events?**
   - List the 5 default fields

### Step 1.1: Test Case Sensitivity

Run this search to find events with productId:

```spl
index=web sourcetype=access_combined_wcookie productId=*
```

**Expected Results**: Events containing product IDs

Now try with lowercase:

```spl
index=web sourcetype=access_combined_wcookie productid=*
```

**Question**: Do you get the same results? What does this tell you about field names?

### Step 1.2: Identify Default Fields

Run a basic search and examine the fields:

```spl
index=web sourcetype=access_combined_wcookie
| head 10
```

**Question**: What fields appear in the "Interesting Fields" section by default?

**Save this search as**: `L1S1`

---

## Task 2: Using the Job Inspector

The Job Inspector helps troubleshoot search performance issues and understand how Splunk processes searches.

### Scenario

A colleague reports that their search `index=web productid=*` returns no results, but they know products are being sold on the website. Use the Job Inspector to troubleshoot.

### Step 2.1: Run the Problematic Search

Run this search:

```spl
index=web productid=*
```

**Expected Results**: Possibly no results or unexpected results

### Step 2.2: Open Job Inspector

1. After the search completes, click the **Job** menu (appears near search bar)
2. Select **Inspect Job**
3. Examine the following tabs:
   - **Header**: Search ID, user, app context
   - **Execution Costs**: Resource usage
   - **Search Job Properties**: Settings used

### Step 2.3: Analyze the Issue

Look at the search in the Job Inspector:

1. Check the **Search** tab
2. Look for how Splunk interpreted your search terms
3. Notice how field names are case-sensitive

### Step 2.4: Correct the Search

Now run the corrected search:

```spl
index=web sourcetype=access_combined_wcookie productId=*
```

### Step 2.5: Compare Using Job Inspector

1. Open Job Inspector for this search
2. Compare execution statistics with the previous search
3. Note the difference in events scanned and results returned

**Save this search as**: `L1S2`

> **Note**: The Job Inspector shows you:
> - How long each phase took
> - How many events were scanned
> - Whether knowledge objects were used
> - Optimization opportunities

---

## Task 3: Search Performance – Search Modes

Compare the performance of different search modes: Verbose, Fast, and Smart.

### Background

Splunk has three search modes:
- **Verbose**: Returns all fields and events (slowest, most complete)
- **Fast**: Returns minimal fields (fastest, may miss some data)
- **Smart**: Splunk decides based on the search (balanced)

### Step 3.1: Set Up the Test Search

Use this base search:

```spl
index=web sourcetype=access_combined_wcookie action=purchase
| stats count by product_name
```

### Step 3.2: Run in Fast Mode

1. Enter the search above
2. Before running, click the **Search Mode** dropdown (near time picker)
3. Select **Fast Mode**
4. Note the execution time when complete

### Step 3.3: Run in Verbose Mode

1. Run the same search
2. Select **Verbose Mode**
3. Note the execution time when complete

### Step 3.4: Run in Smart Mode

1. Run the same search
2. Select **Smart Mode** (default)
3. Note the execution time when complete

### Step 3.5: Compare Results

Create a comparison table:

| Search Mode | Execution Time | Events Scanned | Results |
|-------------|---------------|----------------|---------|
| Fast        |               |                |         |
| Verbose     |               |                |         |
| Smart       |               |                |         |

**Questions**:
1. Which mode was fastest?
2. Did all modes return the same number of results?
3. When would you use each mode?

**Save this search as**: `L1S3`

> **Tip**: For most searches, Smart mode is recommended. Use Fast mode when you need quick statistics and don't need all field data. Use Verbose mode when troubleshooting or when you need complete event information.

---

## Task 4: Using the Table Command

The `table` command displays specific fields in a tabular format.

### Scenario

Your security team wants to review web access logs showing only the client IP address, action taken, and HTTP status code.

### Step 4.1: Display Specific Fields

Run this search:

```spl
index=web sourcetype=access_combined_wcookie
| table clientip action status
```

**Expected Results**: A table with three columns showing clientip, action, and status

### Step 4.2: Add More Fields

Expand the table to include product information:

```spl
index=web sourcetype=access_combined_wcookie action=purchase
| table _time clientip action product_name price status
```

**Expected Results**: Purchase events with timestamp, IP, action, product name, price, and status

### Step 4.3: Sort the Table

Sort by price (highest first):

```spl
index=web sourcetype=access_combined_wcookie action=purchase
| table _time clientip action product_name price status
| sort -price
```

**Expected Results**: Same table sorted by price in descending order

### Step 4.4: Limit Results

Show only the top 20 purchases:

```spl
index=web sourcetype=access_combined_wcookie action=purchase
| table _time clientip action product_name price status
| sort -price
| head 20
```

**Expected Results**: Top 20 most expensive purchases

**Save this search as**: `L1S4`

> **Note**: The `table` command:
> - Displays only the specified fields
> - Preserves the order you specify
> - Removes all other fields from the results
> - Use `fields` instead if you want to keep other fields in the background

---

## Challenge Exercise (Optional)

### Challenge 1: Investigate Failed Logins

Using the security index, create a table showing failed SSH login attempts with the following columns:
- Time of attempt
- Source IP address
- Username attempted
- Reason for failure

**Hint**:
- index=security sourcetype=linux_secure
- Look for "failed password" events
- Use `table` to display _time, src_ip, user, and a field showing the failure reason

**Save this search as**: `L1C1`

### Challenge 2: Compare Search Efficiency

Create two searches that return the same results, but one uses efficient filtering and one doesn't:

**Inefficient**:
```spl
index=* | search sourcetype=access_combined_wcookie action=purchase
```

**Efficient**:
```spl
index=web sourcetype=access_combined_wcookie action=purchase
```

Use the Job Inspector to compare:
- Execution time
- Events scanned
- Resource usage

Document your findings.

---

## Summary

In this lab, you learned:
- ✓ Search terms are case-sensitive for field names
- ✓ How to use the Job Inspector to troubleshoot searches
- ✓ The differences between Verbose, Fast, and Smart search modes
- ✓ How to use the table command to display specific fields
- ✓ Best practices for efficient searching

## Key Takeaways

1. **Always specify index and sourcetype** for efficient searching
2. **Use Job Inspector** to troubleshoot and optimize searches
3. **Smart mode** is appropriate for most searches
4. **Field names are case-sensitive**, but field values are not
5. **Table command** is useful for creating clean, focused result sets

---

## Data Sources Used

- **index=web, sourcetype=access_combined_wcookie**: Web access logs from Buttercup Games online store
- **index=security, sourcetype=linux_secure**: Linux authentication logs

## Next Steps

In Lab 2, you'll learn to use transforming commands like `chart` and `timechart` to create visualizations and dashboards.

---

**Lab 1 Complete!**
