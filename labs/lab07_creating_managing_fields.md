# Lab 7: Creating and Managing Fields

**Splunk Intermediate – Lab Exercises**

> **Note**: This lab should be completed in a non-production environment.

## Lab Description

This lab covers:
- Using the Field Extractor (FX) to create custom fields
- Extracting fields using regular expressions (regex)
- Extracting fields using delimiters
- Validating field extractions
- Managing and removing field extractions
- Testing extractions before saving
- Understanding permissions for field extractions

## Scenario

You are a Splunk administrator for Buttercup Games. The security team needs to extract source IP addresses and ports from Linux authentication logs. The game development team needs to extract multiple fields from comma-delimited game telemetry data (SimCubeBeta). You'll use the Field Extractor to create these custom field extractions.

---

## Task 1: Extracting Fields Using Regular Expressions

### Scenario

Linux secure logs contain authentication attempts with source IP addresses and ports embedded in the raw text. Extract these fields using regex-based extraction.

### Step 1.1: Examine Raw Linux Secure Logs

First, view the raw events:

```spl
index=security sourcetype=linux_secure
| head 10
```

**Expected Results**: Raw log events containing text like "from 192.168.1.100 port 52394"

### Step 1.2: Open Field Extractor

1. Run the search above
2. In the **Events** view, locate an event with "from" and "port" in it
3. Click **Event Actions** (▼) → **Extract Fields**
4. Select extraction method: **Regular Expression**

### Step 1.3: Extract Source IP Address (src)

1. In the Field Extractor interface, highlight the IP address in the sample event
2. Field name: `src`
3. Click **Add Extraction**
4. Splunk generates a regex pattern like: `from\s+(?<src>[^\s]+)`

### Step 1.4: Extract Port Number

1. In the same event, highlight the port number
2. Field name: `port`
3. Click **Add Extraction**
4. Splunk generates a regex pattern like: `port\s+(?<port>\d+)`

### Step 1.5: Validate the Extraction

1. Click **Next** to see the extraction validation
2. Review sample events to ensure fields are extracted correctly
3. Check that src shows IP addresses and port shows port numbers
4. If incorrect, adjust the regex or reselect the sample

### Step 1.6: Save the Field Extraction

1. Click **Next** → **Save**
2. Configure:
   - Name: `linux_secure_src_port_extraction`
   - Apply to: **sourcetype = linux_secure**
   - Permission: **App** (shared in app)
   - Destination app: **search** or your class app
3. Click **Finish**

### Step 1.7: Test the New Fields

Wait approximately 1 minute for knowledge objects to replicate, then test:

```spl
index=security sourcetype=linux_secure
| stats count by src, port
| sort -count
```

**Expected Results**: A table showing counts grouped by source IP and port

**Save this search as**: `L7S1`

> **Note**: After creating field extractions:
> - Wait ~1 minute for knowledge bundle replication
> - New fields appear in the field sidebar
> - Fields are extracted at search time, not index time
> - Regular expressions can be complex; use the Field Extractor to generate them

---

## Task 2: Extracting Fields Using Delimiters

### Scenario

The game development team logs SimCubeBeta game telemetry in comma-delimited format. Extract multiple fields using delimiter-based extraction.

### Step 2.1: Examine SimCubeBeta Raw Data

View the raw game telemetry events:

```spl
index=games sourcetype=SimCubeBeta
| head 10
```

**Expected Results**: Comma-delimited events like:
```
2024-01-15T10:30:45,192.168.50.25,v1.2.3,misc_data,user123,DragonSlayer,attack,warrior
```

Format: `time,src,version,misc,user,CharacterName,action,role`

### Step 2.2: Open Field Extractor for Delimiter Extraction

1. Run the search above
2. Click **Event Actions** (▼) → **Extract Fields**
3. Select extraction method: **Delimiters**

### Step 2.3: Select Delimiter

1. Choose delimiter: **Comma**
2. The Field Extractor automatically identifies the fields
3. Review the field preview

### Step 2.4: Name the Fields

Assign field names to each column:
1. Field 1: `time`
2. Field 2: `src`
3. Field 3: `version`
4. Field 4: `misc`
5. Field 5: `user`
6. Field 6: `CharacterName`
7. Field 7: `action`
8. Field 8: `role`

### Step 2.5: Validate Delimiter Extraction

1. Review multiple sample events
2. Ensure all fields are correctly identified
3. Check for any malformed data
4. Adjust if necessary

### Step 2.6: Save the Delimiter Extraction

1. Click **Next** → **Save**
2. Configure:
   - Name: `simcube_delimiter_extraction`
   - Apply to: **sourcetype = SimCubeBeta**
   - Permission: **App**
   - Destination app: **search** or your class app
3. Click **Finish**

### Step 2.7: Test the Delimiter Extraction

Wait ~1 minute, then test:

```spl
index=games sourcetype=SimCubeBeta
| stats count by CharacterName, action, role
| sort -count
```

**Expected Results**: Counts of game actions by character and role

### Step 2.8: Validate All Fields

Test each extracted field:

```spl
index=games sourcetype=SimCubeBeta
| table time src version user CharacterName action role
```

**Expected Results**: A table displaying all extracted fields

**Save this search as**: `L7S2`

> **Tip**: Delimiter-based extractions are ideal for:
> - CSV files
> - Log files with consistent delimiters (comma, pipe, tab)
> - Structured data formats
> - Much simpler than regex for delimited data

---

## Task 3: Managing Field Extractions

### Scenario

Learn to view, edit, disable, and remove field extractions.

### Step 3.1: View All Field Extractions

1. Navigate to **Settings** → **Fields** → **Field extractions**
2. Review the extractions you created
3. Note the source type, app, and status

### Step 3.2: Edit a Field Extraction

1. Find your `linux_secure_src_port_extraction`
2. Click on it to view details
3. Review the regex pattern
4. You can edit:
   - Name
   - Regex pattern
   - Target sourcetype
   - Permissions

### Step 3.3: Test Before Saving Changes

When editing:
1. Click **Open in Search** to test the extraction
2. Verify it works correctly on sample data
3. Only save after validation

### Step 3.4: Disable a Field Extraction

1. In Field extractions list, locate an extraction
2. Click **Disable** to temporarily turn it off
3. The extraction remains but doesn't apply to searches
4. Click **Enable** to reactivate

### Step 3.5: Remove Invalid Extractions

If an extraction is incorrect:
1. Navigate to **Settings** → **Fields** → **Field extractions**
2. Locate the problematic extraction
3. Click **Delete**
4. Confirm deletion

> **Important**: After modifying field extractions, wait ~1 minute for changes to propagate to search heads.

---

## Task 4: Advanced Field Extraction Validation

### Scenario

Validate that field extractions work correctly and handle edge cases.

### Step 4.1: Check for Null Values

Verify fields are extracted from all relevant events:

```spl
index=security sourcetype=linux_secure
| stats count(src) as src_count, count as total_count
| eval extraction_rate = round((src_count/total_count)*100, 2)
| eval status = if(extraction_rate < 90, "Needs Review", "Good")
| table total_count src_count extraction_rate status
```

**Expected Results**: Shows percentage of events where src was extracted

### Step 4.2: Identify Failed Extractions

Find events where extraction failed:

```spl
index=security sourcetype=linux_secure
| where isnull(src)
| table _raw
```

**Expected Results**: Events where src field wasn't extracted (if any)

### Step 4.3: Validate Field Values

Check that extracted values match expected patterns:

```spl
index=security sourcetype=linux_secure
| where isnotnull(src)
| eval is_valid_ip = if(match(src, "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"), "Yes", "No")
| stats count by is_valid_ip
```

**Expected Results**: Confirms that extracted src values are valid IP addresses

### Step 4.4: Validate Port Number Ranges

Check that port numbers are in valid range (1-65535):

```spl
index=security sourcetype=linux_secure
| where isnotnull(port)
| eval port_num = tonumber(port)
| eval is_valid_port = if(port_num >= 1 AND port_num <= 65535, "Yes", "No")
| stats count by is_valid_port
```

**Expected Results**: All port numbers should be valid

**Save this search as**: `L7S3`

---

## Task 5: Working with Multiple Extractions

### Scenario

Sometimes you need multiple extractions for the same sourcetype to handle different log formats.

### Step 5.1: Check for Multiple Event Formats

Examine if your sourcetype has variations:

```spl
index=security sourcetype=linux_secure
| rex field=_raw "(?<event_type>session opened|failed password|accepted password|connection closed)"
| stats count by event_type
```

**Expected Results**: Different types of events in the same sourcetype

### Step 5.2: Create Conditional Extractions

If you need different extractions for different event types:

1. Create separate field extractions
2. Each with specific regex for its event type
3. Use transform specifications with conditions

Example regex patterns:
- For "session opened": `session opened for user (?<user>\w+)`
- For "failed password": `Failed password for (?<user>\w+) from (?<src>[^\s]+)`

### Step 5.3: Verify Multiple Extractions Work Together

```spl
index=security sourcetype=linux_secure
| stats count by user, src
| sort -count
```

**Expected Results**: Both user and src fields populated from different extraction patterns

---

## Challenge Exercise (Optional)

### Challenge 1: Extract Multiple Fields from Complex Logs

For web access logs, extract and create custom fields:

1. Extract query string parameters from URIs
2. Extract product category and ID from the URI path
3. Extract user agent components (browser, OS, device type)
4. Create a field extraction for each

Example URI: `/cart/action=addtocart&productId=MB-1234&categoryId=STRATEGY`

**Required extractions**:
- productId
- categoryId
- action from query string

Test with:
```spl
index=web sourcetype=access_combined
| stats count by productId, categoryId, action
```

**Save this search as**: `L7C1`

### Challenge 2: Create and Validate Game Statistics Extraction

For SimCubeBeta data, create additional computed extractions:

1. Extract hour from timestamp
2. Create field showing if it's peak gaming time (6pm-11pm)
3. Classify actions into categories (combat, social, economic)
4. Create a dashboard showing:
   - Actions per hour
   - Peak vs off-peak activity
   - Most popular character roles

**Save this search as**: `L7C2`

---

## Summary

In this lab, you learned:
- ✓ How to use the Field Extractor (FX) to create custom fields
- ✓ How to extract fields using regular expressions for unstructured data
- ✓ How to extract fields using delimiters for structured data
- ✓ How to validate field extractions to ensure accuracy
- ✓ How to manage, edit, disable, and remove field extractions
- ✓ How to handle multiple extraction patterns for the same sourcetype
- ✓ Best practices for field extraction validation

## Key Takeaways

1. **Field Extractor (FX)** provides a UI-driven way to create field extractions without writing regex
2. **Regular expression extractions** are used for unstructured or semi-structured data
3. **Delimiter-based extractions** are simpler and faster for consistently delimited data
4. **Field extractions are search-time operations**, not index-time
5. **Wait ~1 minute** after creating extractions for knowledge bundle replication
6. **Validate extractions** by checking extraction rates and field values
7. **Permissions** determine who can use the field extractions (private, app, or global)
8. Multiple extractions can coexist for the same sourcetype

---

## Data Sources Used

- **index=security, sourcetype=linux_secure**: Linux authentication logs with embedded IP addresses and ports in raw text
- **index=games, sourcetype=SimCubeBeta**: Game telemetry data in comma-delimited format with fields: time, src, version, misc, user, CharacterName, action, role

## Next Steps

In Lab 8, you'll learn to create field aliases and calculated fields to make existing fields more accessible and to create computed fields based on existing data.

---

**Lab 7 Complete!**
