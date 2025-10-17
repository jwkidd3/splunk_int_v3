# Lab 1: Beyond Search Fundamentals

**Splunk Intermediate – Lab Exercises**

## Objectives

- Use Job Inspector for troubleshooting
- Compare search modes (Fast/Verbose/Smart)
- Use table command for field display

---

## Task 1: Job Inspector

### Step 1: Run Problematic Search

```spl
index=web productid=*
```

Note: Returns few/no results due to case sensitivity

### Step 2: Open Job Inspector

1. Click **Job** → **Inspect Job**
2. Review **Execution Costs** tab
3. Check **Search Job Properties**

### Step 3: Fix and Compare

```spl
index=web sourcetype=access_combined_wcookie productId=*
```

Compare Job Inspector results with previous search.

**Save as**: `L1S1`

---

## Task 2: Search Modes

### Test Search

```spl
index=web sourcetype=access_combined_wcookie action=purchase
| stats count by product_name
```

### Steps

1. Run search in **Fast Mode** - note time
2. Run search in **Verbose Mode** - note time
3. Run search in **Smart Mode** - note time
4. Compare execution times

**Save as**: `L1S2`

> **Tip**: Smart mode is recommended for most searches.

---

## Task 3: Table Command

### Step 1: Basic Table

```spl
index=web sourcetype=access_combined_wcookie
| table clientip action status
```

### Step 2: Add Fields and Sort

```spl
index=web sourcetype=access_combined_wcookie action=purchase
| table _time clientip product_name price status
| sort -price
| head 20
```

Shows top 20 purchases by price.

**Save as**: `L1S3`

---

## Challenge: Failed Login Table

Create a table showing failed SSH attempts with: time, source IP, username.

**Hint**: `index=security sourcetype=linux_secure "failed password"`

**Save as**: `L1C1`

---

## Summary

- Job Inspector troubleshoots search performance
- Search modes: Fast (quick), Verbose (complete), Smart (balanced)
- Table command displays specified fields only
- Always filter by index and sourcetype first

---

**Lab 1 Complete!**
