# Lab 2: Transforming Commands for Visualizations

**Splunk Intermediate – Lab Exercises**

## Objectives

- Create visualizations with chart command
- Build dashboards with drilldown
- Format charts with custom labels and scales
- Create trellis layout visualizations

---

## Task 1: Stacked Column Chart

```spl
index=security sourcetype=linux_secure
| chart count over vendor_action by src_ip
```

Convert to **Column Chart** visualization (stacked).

**Save as**: `L2S1`

---

## Task 2: Dashboard with Drilldown

1. From saved search `L2S1`, click **Save As** → **Dashboard Panel**
2. Dashboard Title: **IT Ops**
3. Panel Title: **Vendor Actions by Source IP**
4. Click **Edit** → **Edit Drilldown**
5. Set drilldown: `index=security sourcetype=linux_secure src_ip=$click.value$`
6. Test by clicking on an IP

**Save as**: `L2S2`

---

## Task 3: Top Products

### Step 1: All Products

```spl
index=web sourcetype=vendor_sales
| stats count by product_name
| sort -count
```

### Step 2: Top 5 Only

```spl
index=web sourcetype=vendor_sales
| top limit=5 product_name
```

### Step 3: Alternative with head

```spl
index=web sourcetype=vendor_sales
| stats count by product_name
| sort -count
| head 5
```

**Save as**: `L2S3`

---

## Task 4: Chart Formatting

### Step 1: Basic Usage Chart

```spl
index=network sourcetype=cisco_wsa_squid
| timechart sum(usage) as "Total Usage"
```

### Step 2: Custom Label

```spl
index=network sourcetype=cisco_wsa_squid
| timechart sum(usage) as "Total Bandwidth Usage (bytes)"
```

### Step 3: Apply Logarithmic Scale

1. Click **Visualization** tab
2. **Format** → **Y-Axis**
3. Select **Scale**: Logarithmic

**Save as**: `L2S4`

---

## Task 5: Trellis Layout

### Step 1: Multi-Series Chart

```spl
sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy, Spain)
| timechart sum(price) by VendorCountry
```

### Step 2: Enable Trellis

1. Click **Visualization** tab → **Line Chart**
2. **Format** → **General** → Enable **Trellis Layout**
3. Split By: VendorCountry
4. Columns: 2

**Save as**: `L2S5`

---

## Challenge: Sales Dashboard

Create dashboard with:
1. Top 5 products by revenue (Bar chart)
2. Sales by country over time (Trellis)
3. Daily purchase count (Area chart)

Add drilldown to each panel.

**Save as**: `L2C1`

---

## Summary

- `chart` creates visualizations by grouping data
- `top` shows top N values with count/percent
- Drilldown makes dashboards interactive
- Trellis layouts compare multiple series side-by-side
- Logarithmic scales help visualize data with large ranges

---

**Lab 2 Complete!**
