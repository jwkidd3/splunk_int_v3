# Lab 10: Creating and Using Macros

**Splunk Intermediate – Lab Exercises**

## Objectives

- Create basic search macros
- Create macros with arguments
- Add validation to macro arguments
- Nest macros within other macros
- Use macros to simplify searches

---

## Task 1: Repetitive Search Example

### Problem

Sales team runs this frequently:

```spl
sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy)
| stats sum(price) as USD by product_name
| sort -USD
```

Macros provide reusability, consistency, and simplification.

### Syntax

```spl
`macro_name`
`macro_with_args(value1, value2)`
```

---

## Task 2: Basic Macro

### Step 1: Create Macro

1. **Settings** → **Advanced search** → **Search macros**
2. **New Search Macro**
3. Configure:
   - Name: `Europe_sales`
   - Definition: `sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy) | stats sum(price) as USD by product_name`

### Step 2: Test

```spl
`Europe_sales`
| sort -USD
```

### Step 3: Extend

```spl
`Europe_sales`
| sort -USD
| head 10
| eval formatted_usd = "$" + tostring(round(USD, 2), "commas")
| table product_name formatted_usd
```

**Save as**: `L10S1`

---

## Task 3: Macros with Arguments

### Step 1: Create convert_sales Macro

1. **Settings** → **Advanced search** → **Search macros**
2. **New Search Macro**
3. Configure:
   - Name: `convert_sales(3)`
   - Arguments: `currency, symbol, rate`
   - Definition: `| stats sum(price) as USD by product_name | eval $currency$="$symbol$"+tostring(round(USD*$rate$,2),"commas")`

### Step 2: Test with Euros

```spl
sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy)
`convert_sales(euro,€,0.79)`
| table product_name USD euro
| sort -USD
```

### Step 3: Test with GBP

```spl
sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy)
`convert_sales(GBP,£,0.64)`
| table product_name USD GBP
| sort -USD
```

**Save as**: `L10S2`

---

## Task 4: Add Validation

### Step 1: Edit Macro

1. Find `convert_sales(3)` macro
2. Add:
   - Validation Expression: `isnum($rate$)`
   - Error Message: `Exchange rate must be a numeric value`

### Step 2: Test Valid Input

```spl
sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy)
`convert_sales(euro,€,0.79)`
| table product_name USD euro
```

Works correctly.

### Step 3: Test Invalid Input

```spl
sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy)
`convert_sales(euro,€,invalid)`
| table product_name USD euro
```

Returns error: "Exchange rate must be a numeric value"

---

## Task 5: Combine Macros

### Step 1: Simplify Europe_sales

Edit macro definition:
```
sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy)
```

### Step 2: Use Together

```spl
`Europe_sales`
`convert_sales(euro,€,0.79)`
| table product_name USD euro
| sort -USD
```

### Step 3: Multiple Currencies

```spl
`Europe_sales`
| stats sum(price) as USD by product_name
| eval euro = "€" + tostring(round(USD*0.79,2),"commas")
| eval GBP = "£" + tostring(round(USD*0.64,2),"commas")
| eval JPY = "¥" + tostring(round(USD*110.5,2),"commas")
| table product_name USD euro GBP JPY
| sort -USD
```

**Save as**: `L10S3`

---

## Task 6: Nested Macros

### Create Regional Macros

1. **Asia_sales**: `sourcetype=vendor_sales VendorCountry IN (Japan, China, South Korea)`
2. **Americas_sales**: `sourcetype=vendor_sales VendorCountry IN (United States, Canada, Mexico)`

### Create Multi-Region Macro

Name: `regional_comparison`
Definition: `( `Europe_sales` ) OR ( `Asia_sales` ) OR ( `Americas_sales` )`

### Use

```spl
`regional_comparison`
| stats sum(price) as total_sales by VendorCountry
| sort -total_sales
```

---

## Task 7: Advanced Techniques

### Time Range Macro

Name: `last_business_week`
Definition: `earliest=-7d@w1 latest=@w1`

Usage:
```spl
index=web sourcetype=access_combined `last_business_week`
| timechart count
```

### Category Filter Macro

Name: `filter_category(1)`
Arguments: `category`
Definition: `categoryId="$category$"`
Validation: `isnotnull($category$)`

Usage:
```spl
index=web sourcetype=access_combined_wcookie
`filter_category(STRATEGY)`
| stats sum(price) as revenue by product_name
```

### Performance Threshold Macro

Name: `slow_requests(1)`
Arguments: `threshold`
Definition: `req_time > $threshold$`
Validation: `isnum($threshold$) AND $threshold$ > 0`

Usage:
```spl
index=web sourcetype=access_combined
`slow_requests(1.0)`
| stats count by uri
| sort -count
```

---

## Task 8: Document Macros

Add descriptions to each macro:

Example for convert_sales:
```
Converts USD sales to specified currency.
Arguments:
  - currency: Field name (e.g., euro, GBP)
  - symbol: Currency symbol (e.g., €, £)
  - rate: Exchange rate from USD
Example: `convert_sales(euro,€,0.79)`
```

---

## Challenge: Sales Analysis System

Create integrated macros:
1. `region_filter(1)`: Accept region, return filter
2. `time_period(1)`: Accept period (day/week/month)
3. `multi_currency_convert`: Convert to EUR, GBP, JPY
4. `sales_analysis(2)`: Accept region and time

Usage: ``sales_analysis(Europe, week)``

**Save as**: `L10C1`

---

## Summary

- Macros encapsulate reusable search logic
- Invocation: Backticks around name: `` `macro_name` ``
- Arguments: Define as `macro_name(N)` where N = count
- Reference arguments with `$arg_name$`
- Validation uses isnum(), isnotnull(), match()
- Macros can call other macros
- Add descriptions explaining purpose and usage
- Macros are search-time operations

---

**Lab 10 Complete!**
