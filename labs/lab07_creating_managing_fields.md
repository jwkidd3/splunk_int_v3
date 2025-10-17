# Lab 7: Creating and Managing Fields

**Splunk Intermediate – Lab Exercises**

## Objectives

- Use Field Extractor (FX) for custom fields
- Extract fields with regular expressions
- Extract fields with delimiters
- Validate field extractions
- Manage and remove extractions

---

## Task 1: Regex Field Extraction

### Step 1: View Raw Logs

```spl
index=security sourcetype=linux_secure
| head 10
```

Look for text like "from 192.168.1.100 port 52394"

### Step 2: Open Field Extractor

1. Run search above
2. Click **Event Actions** → **Extract Fields**
3. Select **Regular Expression**

### Step 3: Extract src Field

1. Highlight IP address in sample event
2. Field name: `src`
3. **Add Extraction**
4. Splunk generates regex: `from\s+(?<src>[^\s]+)`

### Step 4: Extract port Field

1. Highlight port number
2. Field name: `port`
3. **Add Extraction**
4. Splunk generates regex: `port\s+(?<port>\d+)`

### Step 5: Save Extraction

1. **Next** → **Save**
2. Name: `linux_secure_src_port_extraction`
3. Apply to sourcetype: `linux_secure`

### Step 6: Test

Wait ~1 minute, then:

```spl
index=security sourcetype=linux_secure
| stats count by src, port
| sort -count
```

**Save as**: `L7S1`

---

## Task 2: Delimiter Extraction

### Step 1: View SimCubeBeta Data

```spl
index=games sourcetype=SimCubeBeta
| head 10
```

Format: `time,src,version,misc,user,CharacterName,action,role`

### Step 2: Open Field Extractor

1. Click **Event Actions** → **Extract Fields**
2. Select **Delimiters**
3. Choose delimiter: **Comma**

### Step 3: Name Fields

Assign names to columns:
1. `time`
2. `src`
3. `version`
4. `misc`
5. `user`
6. `CharacterName`
7. `action`
8. `role`

### Step 4: Save

1. **Next** → **Save**
2. Name: `simcube_delimiter_extraction`
3. Apply to sourcetype: `SimCubeBeta`

### Step 5: Test

Wait ~1 minute, then:

```spl
index=games sourcetype=SimCubeBeta
| stats count by CharacterName, action, role
| sort -count
```

### Step 6: Validate All Fields

```spl
index=games sourcetype=SimCubeBeta
| table time src version user CharacterName action role
```

**Save as**: `L7S2`

---

## Task 3: Validate Extractions

### Step 1: Check Extraction Rate

```spl
index=security sourcetype=linux_secure
| stats count(src) as src_count, count as total_count
| eval extraction_rate = round((src_count/total_count)*100, 2)
| eval status = if(extraction_rate < 90, "Needs Review", "Good")
| table total_count src_count extraction_rate status
```

### Step 2: Find Failed Extractions

```spl
index=security sourcetype=linux_secure
| where isnull(src)
| table _raw
```

### Step 3: Validate IP Format

```spl
index=security sourcetype=linux_secure
| where isnotnull(src)
| eval is_valid_ip = if(match(src, "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"), "Yes", "No")
| stats count by is_valid_ip
```

### Step 4: Validate Port Range

```spl
index=security sourcetype=linux_secure
| where isnotnull(port)
| eval port_num = tonumber(port)
| eval is_valid_port = if(port_num >= 1 AND port_num <= 65535, "Yes", "No")
| stats count by is_valid_port
```

**Save as**: `L7S3`

---

## Task 4: Manage Extractions

### View All Extractions

1. **Settings** → **Fields** → **Field extractions**
2. Review your extractions
3. Check sourcetype and status

### Edit Extraction

1. Click extraction name
2. Review regex pattern
3. Click **Open in Search** to test
4. Edit if needed

### Disable/Enable

1. Click **Disable** to turn off temporarily
2. Click **Enable** to reactivate

### Delete

1. Click **Delete** to remove permanently

---

## Challenge: Extract Query Parameters

Extract productId, categoryId, and action from web URIs.

Example: `/cart/action=addtocart&productId=MB-1234&categoryId=STRATEGY`

Test:
```spl
index=web sourcetype=access_combined
| stats count by productId, categoryId, action
```

**Save as**: `L7C1`

---

## Summary

- Field Extractor (FX) creates extractions without writing regex
- Regular expressions for unstructured data
- Delimiter-based for consistently delimited data
- Extractions are search-time operations
- Wait ~1 minute for knowledge bundle replication
- Validate extraction rate and field values
- Manage via Settings → Fields → Field extractions

---

**Lab 7 Complete!**
