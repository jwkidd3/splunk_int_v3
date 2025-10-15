# Lab 3: Using Trendlines, Mapping, and Single Value Commands

**Splunk Intermediate – Lab Exercises**

> **Note**: This lab should be completed in a non-production environment.

## Lab Description

This lab covers:
- Using the trendline command with simple moving averages
- Creating single value visualizations with trend indicators and sparklines
- Using iplocation for geographic data enrichment
- Creating choropleth maps for regional data
- Creating cluster maps for geographic distribution
- Using addtotals to add row and column totals

## Scenario

You are a Splunk administrator for Buttercup Games. The security team needs to identify trends in failed login attempts, the sales team wants geographic visualizations of sales data, and management needs single value metrics with trend indicators for executive dashboards.

---

## Task 1: Using Trendlines with Simple Moving Averages

### Scenario

The security team wants to identify trends in failed password attempts to detect potential brute force attacks.

### Step 1.1: Create Basic Timechart of Failed Passwords

First, create a timechart of failed password attempts:

```spl
index=security sourcetype=linux_secure "failed password"
| timechart count as failures
```

**Expected Results**: A line chart showing the count of failed password attempts over time

### Step 1.2: Add Simple Moving Average Trendline

Add a trendline using a simple moving average (SMA) with a 4-period window:

```spl
index=security sourcetype=linux_secure "failed password"
| timechart count as failures
| trendline sma4(failures) as trend
```

**Expected Results**: The chart now displays two lines - the actual failure count and a smoothed trend line

### Step 1.3: Customize the Trendline Period

Try different trendline periods to see the effect:

```spl
index=security sourcetype=linux_secure "failed password"
| timechart count as failures
| trendline sma10(failures) as trend
```

**Expected Results**: A smoother trend line with less variation, using a 10-period moving average

**Save this search as**: `L3S1`

> **Note**: Simple Moving Average (SMA) trendlines help:
> - Smooth out short-term fluctuations
> - Highlight longer-term trends
> - Identify anomalies in the data
> - The number indicates the period: sma4 = 4-period average, sma10 = 10-period average

---

## Task 2: Creating Single Value Visualizations

### Scenario

Create executive dashboard metrics showing total failed login attempts with trend indicators.

### Step 2.1: Create Basic Single Value

Create a single value showing total failed password attempts:

```spl
index=security sourcetype=linux_secure "failed password"
| stats count as "Failed Login Attempts"
```

**Expected Results**: A single number showing the total count

### Step 2.2: Add Trend Indicator

Add a trend indicator by comparing with previous period:

```spl
index=security sourcetype=linux_secure "failed password"
| timechart count as failures
| streamstats current=f last(failures) as previous
| eval change=round(((failures-previous)/previous)*100,2)
| tail 1
| table failures change
```

**Expected Results**: Shows current count and percentage change from previous period

### Step 2.3: Create Single Value with Sparkline

Create a single value visualization with an embedded sparkline:

```spl
index=security sourcetype=linux_secure "failed password"
| timechart count as failures
```

1. Switch to **Visualization** tab
2. Select **Single Value** visualization
3. Click **Format**
4. Under **Sparkline**:
   - Enable sparkline
   - Show sparkline on the visualization
5. Under **Trend**:
   - Enable trend indicator
   - Compare with previous value

**Expected Results**: A single value displaying the current count with a small sparkline chart and trend arrow (up/down)

**Save this search as**: `L3S2`

> **Tip**: Single value visualizations are perfect for:
> - Executive dashboards
> - KPI monitoring
> - Quick at-a-glance metrics
> - Trend indicators show whether values are increasing or decreasing

---

## Task 3: Creating Choropleth Maps

### Scenario

The sales team wants to visualize retail sales across US states using a choropleth map.

### Step 3.1: Aggregate Sales by State

Create a chart showing total sales by state:

```spl
sourcetype=vendor_sales VendorCountry="United States"
| chart sum(price) as TotalSales over VendorStateProvince
```

**Expected Results**: A table showing total sales for each state

### Step 3.2: Create Choropleth Map

Add the geom command to create a choropleth map:

```spl
sourcetype=vendor_sales VendorCountry="United States"
| chart sum(price) as TotalSales over VendorStateProvince
| geom geo_us_states featureIdField=VendorStateProvince
```

1. Switch to **Visualization** tab
2. Select **Choropleth Map**
3. The map displays with states shaded by total sales value

**Expected Results**: A US map with states colored by sales intensity - darker colors indicate higher sales

### Step 3.3: Format the Choropleth Map

Format the map for better visualization:

1. Click **Format** → **Colors**
2. Select a color scheme (e.g., Blue to Red)
3. Adjust the color ranges for better distribution
4. Add a legend showing the value ranges

**Save this search as**: `L3S3`

> **Note**: Choropleth maps are ideal for:
> - Showing data density across geographic regions
> - Comparing values across states, countries, or regions
> - Identifying geographic patterns and hotspots
> - The geom command joins geographic boundary data with your results

---

## Task 4: Creating Cluster Maps

### Scenario

Create a cluster map showing online sales distribution by country.

### Step 4.1: Use iplocation to Enrich Data

Use the iplocation command to extract geographic information from IP addresses:

```spl
index=web sourcetype=access_combined action=purchase
| iplocation clientip
| stats sum(price) as revenue by Country
```

**Expected Results**: A table showing total revenue by country

### Step 4.2: Create Cluster Map with Geostats

Create a cluster map using the geostats command:

```spl
index=web sourcetype=access_combined action=purchase
| iplocation clientip
| geostats sum(price) as revenue by Country
```

**Expected Results**: A world map with clusters of varying sizes representing revenue by geographic location

### Step 4.3: Create Cluster Map by City

Create a more detailed cluster map by city:

```spl
index=web sourcetype=access_combined action=purchase
| iplocation clientip
| geostats latfield=lat longfield=lon sum(price) as revenue by clientip
```

1. Switch to **Visualization** tab
2. Select **Cluster Map**
3. Zoom in to see individual clusters

**Expected Results**: A map with clusters that can be zoomed and explored, showing purchase locations

### Step 4.4: Customize Cluster Map Display

Adjust the clustering parameters:

```spl
index=web sourcetype=access_combined action=purchase
| iplocation clientip
| geostats latfield=lat longfield=lon globallimit=10 sum(price) as revenue by Country
```

**Expected Results**: Limited to top 10 countries by revenue

**Save this search as**: `L3S4`

> **Note**:
> - **iplocation** extracts geographic data (Country, City, lat, lon) from IP addresses
> - **geostats** is specifically designed for creating map visualizations
> - **Cluster maps** group nearby points into clusters for better visualization
> - **globallimit** parameter controls the maximum number of clusters displayed

---

## Task 5: Using Addtotals Command

### Scenario

Create a sales report with row and column totals.

### Step 5.1: Create Basic Sales Table

Create a table showing sales by product and country:

```spl
sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy, Spain)
| chart sum(price) as Revenue over product_name by VendorCountry
```

**Expected Results**: A table with products as rows and countries as columns

### Step 5.2: Add Column Totals

Add a total column summing across countries:

```spl
sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy, Spain)
| chart sum(price) as Revenue over product_name by VendorCountry
| addtotals col=t row=f label="Total" fieldname="Total_Revenue"
```

**Expected Results**: A new column "Total_Revenue" showing the sum across all countries for each product

### Step 5.3: Add Row Totals

Add a total row summing each country:

```spl
sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy, Spain)
| chart sum(price) as Revenue over product_name by VendorCountry
| addtotals col=f row=t label="Total Sales"
```

**Expected Results**: A new row "Total Sales" showing the sum of all products for each country

### Step 5.4: Add Both Row and Column Totals

Add both row and column totals:

```spl
sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy, Spain)
| chart sum(price) as Revenue over product_name by VendorCountry
| addtotals col=t row=t label="Grand Total" fieldname="Total"
```

**Expected Results**: A table with totals on both the right side (column totals) and bottom (row totals), including a grand total

**Save this search as**: `L3S5`

> **Note**: addtotals parameters:
> - `col=t` adds column totals (sum across rows)
> - `row=t` adds row totals (sum down columns)
> - `label="text"` sets the label for the total row
> - `fieldname="name"` sets the name for the total column

---

## Challenge Exercise (Optional)

### Challenge 1: Security Dashboard with Trends

Create a comprehensive security dashboard with the following panels:

1. **Failed Login Attempts** (Single Value)
   - Show total count for last 24 hours
   - Include sparkline for last 7 days
   - Add trend indicator comparing to previous day

2. **Failed Login Trend** (Line Chart)
   - Timechart with hourly bins
   - Add sma4 trendline
   - Highlight anomalies

3. **Attack Sources Map** (Cluster Map)
   - Use iplocation on src_ip
   - Show geographic distribution of failed logins
   - Size clusters by attempt count

4. **Top 10 Attack Sources** (Table)
   - Show src_ip, country, and count
   - Add totals row

**Dashboard Name**: Security Monitoring Dashboard

**Save this search as**: `L3C1`

### Challenge 2: Sales Performance Geographic Analysis

Create a sales analysis with multiple map types:

1. **US Retail Sales Choropleth Map**
   - Vendor_sales data
   - Show sales by state
   - Use custom color scheme

2. **Online Sales Cluster Map**
   - Access_combined data
   - Show purchases by country
   - Include revenue in tooltips

3. **Comparison Table**
   - Compare online vs retail by region
   - Add totals for each channel
   - Calculate percentage of total

Compare the insights gained from each visualization type.

---

## Summary

In this lab, you learned:
- ✓ How to use trendline with simple moving averages to smooth data
- ✓ How to create single value visualizations with trend indicators and sparklines
- ✓ How to use iplocation to enrich IP addresses with geographic data
- ✓ How to create choropleth maps for regional data visualization
- ✓ How to create cluster maps to show geographic distribution
- ✓ How to use addtotals to add row and column totals to tables

## Key Takeaways

1. **Trendlines** help identify patterns by smoothing short-term fluctuations
2. **Single value visualizations** are ideal for executive dashboards and KPI monitoring
3. **iplocation** automatically extracts Country, City, Region, latitude, and longitude from IP addresses
4. **Choropleth maps** use shading to show data intensity across geographic regions
5. **Cluster maps** group nearby points and are ideal for showing distribution patterns
6. **geostats** is the command specifically designed for creating map visualizations
7. **addtotals** simplifies adding summary rows and columns to tables

---

## Data Sources Used

- **index=security, sourcetype=linux_secure**: Linux authentication logs for failed password analysis
- **index=web, sourcetype=vendor_sales**: Retail store transaction data with VendorCountry and VendorStateProvince
- **index=web, sourcetype=access_combined**: Online store web access logs with clientip for geolocation

## Next Steps

In Lab 4, you'll learn to filter results and manipulate data using the eval, search, where, and case commands to transform and categorize your data.

---

**Lab 3 Complete!**
