# Lab 10: Creating and Using Macros

**Splunk Intermediate – Lab Exercises**

> **Note**: This lab should be completed in a non-production environment.

## Lab Description

This lab covers:
- Understanding search macros and their benefits
- Creating basic search macros
- Creating macros with arguments
- Using macros in searches
- Adding validation to macro arguments
- Nesting macros within other macros
- Managing and troubleshooting macros
- Best practices for macro development

## Scenario

You are a Splunk administrator for Buttercup Games. The sales team frequently analyzes European sales data (Germany, France, Italy) and needs to convert revenue to different currencies. Instead of writing complex searches repeatedly, you'll create reusable macros that encapsulate this logic and accept parameters for currency conversion.

---

## Task 1: Understanding Search Macros

### Scenario

Learn what macros are and why they're useful before creating them.

### Step 1.1: Example of Repetitive Search

The sales team runs this search frequently:

```spl
sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy)
| stats sum(price) as USD by product_name
| sort -USD
```

**Problem**: This search is typed repeatedly with minor variations

### Step 1.2: Benefits of Macros

Macros provide:
- **Reusability**: Write once, use many times
- **Consistency**: Ensure searches use the same logic
- **Maintainability**: Update in one place
- **Simplification**: Hide complexity behind simple names
- **Parameters**: Accept arguments for flexibility

### Step 1.3: Macro Syntax

Macros are invoked using backticks:
```spl
`macro_name`
`macro_with_args(value1, value2)`
```

---

## Task 2: Creating a Basic Search Macro

### Scenario

Create a macro called "Europe_sales" that encapsulates the European sales search.

### Step 2.1: Create the Macro

1. Navigate to **Settings** → **Advanced search** → **Search macros**
2. Click **New Search Macro**
3. Configure:
   - Destination app: **search** (or class_Fund2)
   - Name: `Europe_sales`
   - Definition:
   ```
   sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy) | stats sum(price) as USD by product_name
   ```
   - Use eval-based definition: **No**
4. Click **Save**

### Step 2.2: Test the Basic Macro

Use the macro in a search:

```spl
`Europe_sales`
| sort -USD
```

**Expected Results**: European sales data by product, same as the original search

### Step 2.3: Enhance the Search Using the Macro

Extend the macro with additional logic:

```spl
`Europe_sales`
| sort -USD
| head 10
| eval formatted_usd = "$" + tostring(round(USD, 2), "commas")
| table product_name formatted_usd
```

**Expected Results**: Top 10 European products with formatted USD values

**Save this search as**: `L10S1`

> **Note**: Basic macros:
> - Encapsulate search logic
> - Are invoked with backticks: `macro_name`
> - Can be combined with additional search commands
> - Make searches more readable and maintainable

---

## Task 3: Creating Macros with Arguments

### Scenario

Create a macro that converts sales to different currencies using exchange rates as arguments.

### Step 3.1: Plan the Macro with Arguments

The macro should:
- Accept three arguments: currency name, currency symbol, exchange rate
- Convert USD to the specified currency
- Format the output with the currency symbol

Example usage:
```spl
`convert_sales(euro,€,0.79)`
`convert_sales(GBP,£,0.64)`
```

### Step 3.2: Create the Macro with Arguments

1. Navigate to **Settings** → **Advanced search** → **Search macros**
2. Click **New Search Macro**
3. Configure:
   - Destination app: **search** (or class_Fund2)
   - Name: `convert_sales(3)`
     - Note: (3) indicates 3 arguments
   - Definition:
   ```
   | stats sum(price) as USD by product_name | eval $currency$="$symbol$"+tostring(round(USD*$rate$,2),"commas")
   ```
   - Arguments: `currency, symbol, rate`
   - Use eval-based definition: **No**
4. Click **Save**

### Step 3.3: Test the Macro with Arguments

Convert European sales to Euros:

```spl
sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy)
`convert_sales(euro,€,0.79)`
| table product_name USD euro
| sort -USD
```

**Expected Results**: Sales shown in both USD and Euros

### Step 3.4: Use with Different Currencies

Convert to British Pounds:

```spl
sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy)
`convert_sales(GBP,£,0.64)`
| table product_name USD GBP
| sort -USD
```

**Expected Results**: Sales shown in USD and GBP

**Save this search as**: `L10S2`

> **Tip**: Macros with arguments:
> - Name format: `macro_name(N)` where N is the number of arguments
> - Arguments referenced with dollar signs: `$arg_name$`
> - Arguments are positional and required
> - Make macros flexible and reusable

---

## Task 4: Adding Validation to Macros

### Scenario

Add validation to ensure the exchange rate argument is a valid number.

### Step 4.1: Edit the Macro to Add Validation

1. Navigate to **Settings** → **Advanced search** → **Search macros**
2. Find and click on `convert_sales(3)`
3. Add validation expression:
   - Validation Expression: `isnum($rate$)`
   - Validation Error Message: `Exchange rate must be a numeric value`
4. Click **Save**

### Step 4.2: Test Validation with Valid Input

```spl
sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy)
`convert_sales(euro,€,0.79)`
| table product_name USD euro
```

**Expected Results**: Search runs successfully

### Step 4.3: Test Validation with Invalid Input

```spl
sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy)
`convert_sales(euro,€,invalid)`
| table product_name USD euro
```

**Expected Results**: Error message: "Exchange rate must be a numeric value"

> **Note**: Validation:
> - Ensures arguments meet requirements
> - Provides clear error messages to users
> - Uses eval functions: isnum(), isnotnull(), match(), etc.
> - Multiple conditions can be combined with AND/OR
> - Example: `isnum($rate$) AND $rate$ > 0`

---

## Task 5: Combining Macros

### Scenario

Combine the Europe_sales macro with the convert_sales macro.

### Step 5.1: Update Europe_sales Macro to Be More Modular

1. Edit the `Europe_sales` macro
2. Change definition to:
   ```
   sourcetype=vendor_sales VendorCountry IN (Germany, France, Italy)
   ```
3. Click **Save**

### Step 5.2: Use Both Macros Together

```spl
`Europe_sales`
`convert_sales(euro,€,0.79)`
| table product_name USD euro
| sort -USD
```

**Expected Results**: European sales converted to Euros

### Step 5.3: Create Multiple Currency View

```spl
`Europe_sales`
| stats sum(price) as USD by product_name
| eval euro = "€" + tostring(round(USD*0.79,2),"commas")
| eval GBP = "£" + tostring(round(USD*0.64,2),"commas")
| eval JPY = "¥" + tostring(round(USD*110.5,2),"commas")
| table product_name USD euro GBP JPY
| sort -USD
```

**Expected Results**: Sales in multiple currencies

**Save this search as**: `L10S3`

---

## Task 6: Creating Nested Macros

### Scenario

Create a macro that calls another macro internally.

### Step 6.1: Create Regional Sales Macros

Create macros for different regions:

1. **Asia_sales**:
```
sourcetype=vendor_sales VendorCountry IN (Japan, China, South Korea)
```

2. **Americas_sales**:
```
sourcetype=vendor_sales VendorCountry IN (United States, Canada, Mexico)
```

### Step 6.2: Create Multi-Region Analysis Macro

Create a macro that uses the regional macros:

1. Name: `regional_comparison`
2. Definition:
```
( `Europe_sales` ) OR ( `Asia_sales` ) OR ( `Americas_sales` )
```

### Step 6.3: Use the Nested Macro

```spl
`regional_comparison`
| stats sum(price) as total_sales by VendorCountry
| sort -total_sales
```

**Expected Results**: Sales from all three regions combined

---

## Task 7: Advanced Macro Techniques

### Scenario

Create more sophisticated macros for common analysis patterns.

### Step 7.1: Create Time Range Macro

Create a macro for last business week:

1. Name: `last_business_week`
2. Definition:
```
earliest=-7d@w1 latest=@w1
```

Usage:
```spl
index=web sourcetype=access_combined `last_business_week`
| timechart count
```

### Step 7.2: Create Filter Macro with Argument

Create a macro to filter by product category:

1. Name: `filter_category(1)`
2. Arguments: `category`
3. Definition:
```
categoryId="$category$"
```
4. Validation: `isnotnull($category$)`

Usage:
```spl
index=web sourcetype=access_combined_wcookie
`filter_category(STRATEGY)`
| stats sum(price) as revenue by product_name
```

### Step 7.3: Create Performance Threshold Macro

Create a macro for slow response times:

1. Name: `slow_requests(1)`
2. Arguments: `threshold`
3. Definition:
```
req_time > $threshold$
```
4. Validation: `isnum($threshold$) AND $threshold$ > 0`
5. Error message: `Threshold must be a positive number`

Usage:
```spl
index=web sourcetype=access_combined
`slow_requests(1.0)`
| stats count by uri
| sort -count
```

---

## Task 8: Managing and Documenting Macros

### Scenario

Follow best practices for macro management.

### Step 8.1: Add Descriptions to Macros

1. Edit each macro
2. Add a description explaining:
   - Purpose of the macro
   - Expected arguments
   - Example usage
3. Click **Save**

Example description for convert_sales:
```
Converts USD sales to specified currency.
Arguments:
  - currency: Field name for converted currency (e.g., euro, GBP)
  - symbol: Currency symbol (e.g., €, £)
  - rate: Exchange rate from USD to target currency
Example: `convert_sales(euro,€,0.79)`
```

### Step 8.2: Create Macro Naming Conventions

Follow these conventions:
- Use lowercase with underscores
- Make names descriptive
- Include units in names if relevant (e.g., `convert_bytes_to_mb`)
- Group related macros with common prefixes

### Step 8.3: Test Macros Regularly

Create a test dashboard:
```spl
| makeresults
| eval macro_name = "Europe_sales"
| eval status = "testing"
```

Verify macros work after Splunk upgrades or changes.

---

## Challenge Exercise (Optional)

### Challenge 1: Create Comprehensive Sales Analysis Macro System

Create a set of integrated macros:

1. **Region Macros**:
   - `region_filter(1)`: Accept region name, return filter
   - Regions: Europe, Asia, Americas, Africa

2. **Time Period Macros**:
   - `time_period(1)`: Accept period (day, week, month, quarter)
   - Calculate appropriate earliest/latest

3. **Currency Conversion Macro**:
   - `multi_currency_convert`: Convert to EUR, GBP, JPY simultaneously

4. **Analysis Macro**:
   - `sales_analysis(2)`: Accept region and time period
   - Return formatted report with multiple currencies

Example usage:
```spl
`sales_analysis(Europe, week)`
```

**Save this search as**: `L10C1`

### Challenge 2: Create Performance Monitoring Macros

Create macros for web performance monitoring:

1. **Threshold Macros**:
   - `fast_requests`: req_time < 0.1
   - `normal_requests`: req_time >= 0.1 AND req_time < 0.5
   - `slow_requests`: req_time >= 0.5 AND req_time < 1.0
   - `very_slow_requests`: req_time >= 1.0

2. **Metric Calculation Macro**:
   - `performance_metrics`: Calculate avg, p50, p95, p99 response times

3. **Alert Condition Macro**:
   - `performance_alert(1)`: Accept threshold, return alert condition

Create a dashboard using these macros showing:
- Request distribution by performance category
- Performance metrics over time
- Alerts for degraded performance

**Save this search as**: `L10C2`

---

## Summary

In this lab, you learned:
- ✓ What search macros are and their benefits
- ✓ How to create basic search macros
- ✓ How to create macros with arguments for flexibility
- ✓ How to add validation to macro arguments
- ✓ How to nest macros within other macros
- ✓ How to manage and document macros
- ✓ Best practices for macro naming and organization

## Key Takeaways

1. **Macros** encapsulate reusable search logic
2. **Invocation syntax**: Backticks around macro name: `macro_name`
3. **Arguments**: Defined as `macro_name(N)` where N is the argument count
4. **Argument references**: Use `$arg_name$` in the definition
5. **Validation**: Use `isnum()`, `isnotnull()`, `match()` to validate arguments
6. **Error messages**: Provide clear validation error messages to users
7. **Nesting**: Macros can call other macros for modularity
8. **Documentation**: Add descriptions explaining purpose and usage
9. Macros improve **readability**, **consistency**, and **maintainability**
10. Macros are **search-time** operations

---

## Data Sources Used

- **sourcetype=vendor_sales**: Retail store transaction data with VendorCountry, product_name, and price fields for sales analysis and currency conversion
- **index=web, sourcetype=access_combined**: Web access logs with req_time for performance macros
- **index=web, sourcetype=access_combined_wcookie**: Web logs with categoryId and productId for filtering macros

## Next Steps

In Lab 11, you'll learn to create workflow actions that enable contextual links and searches from event data, making investigation workflows more efficient.

---

**Lab 10 Complete!**
