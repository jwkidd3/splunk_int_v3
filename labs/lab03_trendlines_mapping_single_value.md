# Lab 3: Trendlines, Mapping, and Single Value

**Splunk Intermediate – Lab Exercises**

## Objectives

- Apply trendlines with simple moving averages
- Create single value visualizations with sparklines
- Use iplocation for geographic enrichment
- Build choropleth and cluster maps
- Add totals with addtotals command

---

## Task 1: Trendlines

### Step 1: Basic Timechart

```spl
index=security sourcetype=linux_secure "failed password"
| timechart count as failures
```

### Step 2: Add Trendline

```spl
index=security sourcetype=linux_secure "failed password"
| timechart count as failures
| trendline sma4(failures) as trend
```

### Step 3: Adjust Period

```spl
index=security sourcetype=linux_secure "failed password"
| timechart count as failures
| trendline sma10(failures) as trend
```

Larger periods (sma10) create smoother trend lines.

**Save as**: `L3S1`

---

## Task 2: Single Value Visualizations

### Step 1: Basic Single Value

```spl
index=security sourcetype=linux_secure "failed password"
| stats count as "Failed Login Attempts"
```

### Step 2: With Trend Indicator

```spl
index=security sourcetype=linux_secure "failed password"
| timechart count as failures
| streamstats current=f last(failures) as previous
| eval change=round(((failures-previous)/previous)*100,2)
| tail 1
| table failures change
```

### Step 3: Add Sparkline

```spl
index=security sourcetype=linux_secure "failed password"
| timechart count as failures
```

1. Switch to **Single Value** visualization
2. **Format** → Enable **Sparkline** and **Trend indicator**

**Save as**: `L3S2`

---

## Task 3: Choropleth Maps

### Step 1: Aggregate by State

```spl
sourcetype=vendor_sales VendorCountry="United States"
| chart sum(price) as TotalSales over VendorStateProvince
```

### Step 2: Create Map

```spl
sourcetype=vendor_sales VendorCountry="United States"
| chart sum(price) as TotalSales over VendorStateProvince
| geom geo_us_states featureIdField=VendorStateProvince
```

Switch to **Choropleth Map** visualization.

**Save as**: `L3S3`

---

## Task 4: Cluster Maps

### Step 1: Use iplocation

```spl
index=web sourcetype=access_combined action=purchase
| iplocation clientip
| stats sum(price) as revenue by Country
```

### Step 2: Create Cluster Map

```spl
index=web sourcetype=access_combined action=purchase
| iplocation clientip
| geostats sum(price) as revenue by Country
```

### Step 3: By City

```spl
index=web sourcetype=access_combined action=purchase
| iplocation clientip
| geostats latfield=lat longfield=lon sum(price) as revenue by clientip
```

Switch to **Cluster Map** visualization and zoom in.

**Save as**: `L3S4`

---

## Task 5: Addtotals

### Step 1: Basic Table

```spl
sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy, Spain)
| chart sum(price) as Revenue over product_name by VendorCountry
```

### Step 2: Add Column Totals

```spl
sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy, Spain)
| chart sum(price) as Revenue over product_name by VendorCountry
| addtotals col=t row=f label="Total" fieldname="Total_Revenue"
```

### Step 3: Add Row Totals

```spl
sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy, Spain)
| chart sum(price) as Revenue over product_name by VendorCountry
| addtotals col=f row=t label="Total Sales"
```

### Step 4: Both Totals

```spl
sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy, Spain)
| chart sum(price) as Revenue over product_name by VendorCountry
| addtotals col=t row=t label="Grand Total" fieldname="Total"
```

**Save as**: `L3S5`

---

## Challenge: Security Dashboard

Create dashboard with:
1. Failed login count (single value with sparkline)
2. Failed login trend (line chart with sma4)
3. Attack sources map (cluster map by src_ip)
4. Top 10 sources (table with totals)

**Save as**: `L3C1`

---

## Summary

- Trendlines (sma) smooth fluctuations and highlight patterns
- Single values show metrics with trends and sparklines
- iplocation extracts geo data from IPs automatically
- Choropleth maps show data density by region
- Cluster maps group geographic points
- addtotals adds row/column totals to tables

---

**Lab 3 Complete!**
