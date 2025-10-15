# Lab 2: Using Transforming Commands for Visualizations

**Splunk Intermediate – Lab Exercises**

> **Note**: This lab should be completed in a non-production environment.

## Lab Description

This lab covers:
- Using the chart command for data visualization
- Creating timechart visualizations
- Building and configuring dashboards with drilldown
- Using limit and useother parameters to control chart display
- Formatting charts with custom labels and logarithmic scales
- Creating trellis layout visualizations

## Scenario

You are a Splunk administrator for Buttercup Games, an e-commerce company. The IT Operations team needs visual dashboards to monitor security events, sales trends, and web proxy usage. Your task is to create various chart visualizations and build an interactive dashboard for the team.

---

## Task 1: Creating Stacked Column Charts

### Scenario

The security team wants to visualize authentication attempts by source IP address to identify potential security threats.

### Step 1.1: Chart Vendor Actions by Source IP

Create a stacked column chart showing vendor actions grouped by source IP:

```spl
index=security sourcetype=linux_secure
| chart count over vendor_action by src_ip
```

**Expected Results**: A stacked column chart where each column represents a vendor_action, and the colors represent different source IP addresses

**Save this search as**: `L2S1`

### Step 1.2: Convert to Visualization

1. After running the search, click the **Visualization** tab
2. Select **Column Chart** from the visualization picker
3. Click **Format** to adjust the chart settings:
   - Chart Type: Stacked
   - Legend Position: Right
4. Observe how different source IPs are represented in the stacked columns

> **Note**: Stacked column charts are useful for showing the composition of categories and comparing totals across different groups.

---

## Task 2: Creating an IT Operations Dashboard

### Scenario

Create a dashboard called "IT Ops" that displays security monitoring visualizations with drilldown capabilities.

### Step 2.1: Create the Dashboard

1. From your saved search `L2S1`, click **Save As** → **Dashboard Panel**
2. Create a new dashboard:
   - Dashboard Title: **IT Ops**
   - Dashboard ID: `it_ops`
   - Dashboard Permission: Shared in App
3. Panel Title: **Vendor Actions by Source IP**
4. Panel Content: Statistics Table or Visualization
5. Click **Save**

### Step 2.2: Add Drilldown to the Dashboard

1. Navigate to **Dashboards** and open the **IT Ops** dashboard
2. Click **Edit**
3. Click on the panel and select **Edit Drilldown**
4. Configure drilldown settings:
   - On Click: Link to Search
   - Search String: `index=security sourcetype=linux_secure src_ip=$click.value$`
5. Save the dashboard

### Step 2.3: Test Drilldown

1. View the dashboard
2. Click on one of the source IP addresses in the visualization
3. Verify that it opens a new search filtered to that specific IP address

**Expected Results**: Clicking on any element in the chart should open a search with that value as a filter

**Save this search as**: `L2S2`

> **Tip**: Drilldown enables users to click on a visualization element and perform a deeper investigation of the data.

---

## Task 3: Using Limit and Useother Parameters

### Scenario

The sales team wants to see the top 5 products by sales, with all other products grouped together.

### Step 3.1: Chart Top Products Without Limit

First, see all products:

```spl
index=web sourcetype=vendor_sales
| chart count by product_name
```

**Expected Results**: A chart showing all products

### Step 3.2: Apply Limit to Show Top 5 Products

Now limit to the top 5 products:

```spl
index=web sourcetype=vendor_sales
| chart count by product_name limit=5
```

**Expected Results**: Only the top 5 products are shown, with an "OTHER" category for the rest

### Step 3.3: Remove the "OTHER" Category

Use `useother=f` to exclude the "OTHER" category:

```spl
index=web sourcetype=vendor_sales
| chart count by product_name limit=5 useother=f
```

**Expected Results**: Only the top 5 products are displayed, without the "OTHER" category

**Save this search as**: `L2S3`

> **Note**:
> - `limit=N` restricts the results to the top N values
> - `useother=f` excludes the "OTHER" category from the results
> - `useother=t` (default) includes an "OTHER" category for all remaining values

---

## Task 4: Formatting Charts with Custom Labels and Scales

### Scenario

Create a visualization of web proxy usage with custom formatting for better readability.

### Step 4.1: Create Basic Usage Chart

```spl
index=network sourcetype=cisco_wsa_squid
| timechart sum(usage) as "Total Usage"
```

**Expected Results**: A line chart showing total usage over time

### Step 4.2: Apply Custom Labels

Add custom labels to make the chart more descriptive:

```spl
index=network sourcetype=cisco_wsa_squid
| timechart sum(usage) as "Total Bandwidth Usage (bytes)"
```

### Step 4.3: Apply Logarithmic Scale

For data with large ranges, apply a logarithmic scale:

1. Run the search above
2. Click the **Visualization** tab
3. Click **Format** → **Y-Axis**
4. Select **Scale**: Logarithmic
5. Set **Y-Axis Title**: "Usage (log scale)"

**Expected Results**: The chart displays with a logarithmic scale on the y-axis, making it easier to visualize data with large value ranges

**Save this search as**: `L2S4`

> **Tip**: Use logarithmic scales when your data spans several orders of magnitude, such as bytes, network traffic, or financial data.

---

## Task 5: Creating Trellis Layout Visualizations

### Scenario

The sales team wants to compare sales trends across different countries side by side.

### Step 5.1: Create Multi-Series Chart

Create a chart showing sales by product for multiple countries:

```spl
sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy, Spain)
| timechart sum(price) by VendorCountry
```

**Expected Results**: A line chart with multiple series (one per country)

### Step 5.2: Convert to Trellis Layout

1. Click the **Visualization** tab
2. Select **Line Chart**
3. Click **Format** → **General**
4. Enable **Trellis Layout**
5. Configure trellis settings:
   - Split By: VendorCountry
   - Columns: 2
   - Show Independent Y-Axis: Yes

**Expected Results**: Multiple small charts (one per country) arranged in a grid layout, making it easy to compare trends

### Step 5.3: Create Trellis Chart for Product Categories

```spl
index=web sourcetype=access_combined action=purchase
| timechart count by categoryId
```

1. Convert to trellis layout with 3 columns
2. Enable independent y-axes for better comparison

**Expected Results**: A trellis layout showing purchase trends for each product category

**Save this search as**: `L2S5`

> **Note**: Trellis layouts are ideal for:
> - Comparing multiple series side by side
> - Reducing chart clutter when you have many series
> - Identifying patterns across different categories

---

## Challenge Exercise (Optional)

### Challenge 1: Advanced Dashboard with Multiple Visualizations

Create a comprehensive sales dashboard with the following panels:

1. **Top 5 Products by Revenue** (Bar chart)
   - Use limit=5 and useother=f
   - Sort by total price

2. **Sales by Country Over Time** (Trellis line chart)
   - Filter to top 4 countries
   - Use 2-column trellis layout

3. **Daily Purchase Count** (Area chart)
   - Show total purchases per day
   - Apply smoothing

4. **Product Category Distribution** (Pie chart)
   - Show percentage of sales by category

**Dashboard Name**: Sales Performance Dashboard

Add drilldown to each panel that filters by the clicked value.

**Save this search as**: `L2C1`

### Challenge 2: Logarithmic Scale Comparison

Create two versions of a chart showing web traffic bytes:

1. Linear scale version
2. Logarithmic scale version

Compare when each scale is more appropriate for data interpretation.

```spl
index=web sourcetype=access_combined
| timechart sum(bytes) by status
```

Document your observations about when to use each scale type.

---

## Summary

In this lab, you learned:
- ✓ How to use the chart command to create stacked column visualizations
- ✓ How to create dashboards with drilldown capabilities
- ✓ How to use limit and useother parameters to control chart display
- ✓ How to format charts with custom labels and logarithmic scales
- ✓ How to create trellis layout visualizations for comparing multiple series

## Key Takeaways

1. **Chart command** transforms data into visualizations by grouping data over one field and splitting by another
2. **Limit parameter** restricts results to top N values, improving chart readability
3. **Useother parameter** controls whether remaining values are grouped into an "OTHER" category
4. **Logarithmic scales** are useful for data spanning multiple orders of magnitude
5. **Trellis layouts** enable side-by-side comparison of multiple series in separate mini-charts
6. **Drilldown** makes dashboards interactive, allowing users to investigate specific data points

---

## Data Sources Used

- **index=security, sourcetype=linux_secure**: Linux authentication logs with vendor_action and src_ip fields
- **index=web, sourcetype=vendor_sales**: Retail store transaction data with VendorCountry and product_name
- **index=network, sourcetype=cisco_wsa_squid**: Web proxy logs with usage and bandwidth data
- **index=web, sourcetype=access_combined**: Online store web access logs with action, status, and bytes

## Next Steps

In Lab 3, you'll learn to use trendlines, mapping commands, and single value visualizations to enhance your analysis and create geographic visualizations.

---

**Lab 2 Complete!**
