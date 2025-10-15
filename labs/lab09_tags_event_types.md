# Lab 9: Creating Tags and Event Types

**Splunk Intermediate – Lab Exercises**

> **Note**: This lab should be completed in a non-production environment.

## Lab Description

This lab covers:
- Understanding tags and their purpose
- Creating tags for field values
- Creating tags for multiple related values
- Understanding event types and their uses
- Creating event types for common searches
- Setting event type priorities
- Using tags and event types in searches
- Best practices for tags and event types

## Scenario

You are a Splunk administrator for Buttercup Games. The security team needs to identify privileged users across multiple systems where they're referenced by different variations (admin, administrator, sysadmin, etc.). The web operations team wants to easily search for web errors without remembering complex status code ranges. You'll use tags and event types to solve these problems.

---

## Task 1: Understanding Tags

### Scenario

Your organization has privileged users identified by various names: admin, administrator, sysadmin, itmadmin, sapadmin. Create a single tag to identify all of them.

### Step 1.1: Identify User Variations

First, see the different privileged user names:

```spl
index=security sourcetype=linux_secure
| stats count by user
| sort -count
```

**Expected Results**: Various user names including admin, administrator, sysadmin, etc.

### Step 1.2: Search Without Tags

Try searching for all privileged users without tags:

```spl
index=security sourcetype=linux_secure (user=admin OR user=administrator OR user=sysadmin OR user=itmadmin OR user=sapadmin)
| stats count by user
```

**Expected Results**: All privileged users, but requires a complex search string

---

## Task 2: Creating Tags for Field Values

### Scenario

Create a tag called "privileged_user" that applies to all administrative user variations.

### Step 2.1: Create Tag for First Value (admin)

1. Run this search:
```spl
index=security sourcetype=linux_secure user=admin
```

2. In the **Fields** sidebar, click on **user**
3. Locate the value **admin** in the list
4. Click the three dots (⋯) next to "admin"
5. Select **Edit Tags**
6. In the tag dialog:
   - Enter tag name: `privileged_user`
   - Click **Save**

### Step 2.2: Add Tag to Additional Values

Repeat the process for other administrative users:

1. Search for `user=administrator`
2. Tag it with: `privileged_user`
3. Repeat for:
   - `user=sysadmin` → tag: `privileged_user`
   - `user=itmadmin` → tag: `privileged_user`
   - `user=sapadmin` → tag: `privileged_user`

### Step 2.3: Alternative Method - Settings Menu

You can also create tags via Settings:

1. Navigate to **Settings** → **Tags**
2. Click **New Tag**
3. Configure:
   - Name: `privileged_user`
   - Field/Value pairs:
     - Field: `user`, Value: `admin`
     - Field: `user`, Value: `administrator`
     - Field: `user`, Value: `sysadmin`
     - Field: `user`, Value: `itmadmin`
     - Field: `user`, Value: `sapadmin`
4. Click **Save**

### Step 2.4: Test the Tag

Search using the tag:

```spl
index=security sourcetype=linux_secure tag=privileged_user
| stats count by user
```

**Expected Results**: All events where user is tagged as privileged_user

**Save this search as**: `L9S1`

> **Note**: Tags:
> - Create meaningful names for field values
> - Enable searching by tag instead of multiple field values
> - Can be applied to any field-value pair
> - Are search-time operations
> - Make searches simpler and more readable

---

## Task 3: Using Tags in Searches

### Scenario

Demonstrate the power of tags in various search scenarios.

### Step 3.1: Simple Tag Search

Search for all privileged user activity:

```spl
index=security sourcetype=linux_secure tag=privileged_user
| timechart count by user
```

**Expected Results**: Timeline of privileged user activity

### Step 3.2: Combine Tags with Other Criteria

Search for failed logins by privileged users:

```spl
index=security sourcetype=linux_secure tag=privileged_user "failed password"
| stats count by user, src_ip
| sort -count
```

**Expected Results**: Failed login attempts by privileged users

### Step 3.3: Negate Tag

Search for non-privileged users:

```spl
index=security sourcetype=linux_secure NOT tag=privileged_user
| stats count by user
| sort -count
```

**Expected Results**: All users except privileged users

**Save this search as**: `L9S2`

> **Tip**: Tags simplify searches by:
> - Replacing long OR statements
> - Making searches more readable
> - Enabling easier dashboard creation
> - Reducing search syntax errors

---

## Task 4: Creating Event Types

### Scenario

Create an event type to easily identify web error events (HTTP status codes > 500).

### Step 4.1: Create the Base Search

First, identify web error events:

```spl
(index=web sourcetype=access_combined OR sourcetype=cisco_wsa_squid) status>500
| stats count by status, sourcetype
```

**Expected Results**: Server error events from web sources

### Step 4.2: Create Event Type from Search

1. Run the search above
2. Click **Save As** → **Event Type**
3. Configure:
   - Name: `web_error`
   - Event Type ID: `web_error`
   - Search String: `(sourcetype=access_combined OR sourcetype=cisco_wsa_squid) status>500`
   - Priority: Leave at default (1 - Highest)
   - Color: Red
   - Tags: `error`, `web`, `server_error`
   - Destination app: **search** (or your class app)
4. Click **Save**

### Step 4.3: Alternative Method - Settings Menu

Create event type via Settings:

1. Navigate to **Settings** → **Event types**
2. Click **New Event Type**
3. Configure:
   - Name: `web_error`
   - Search string: `(sourcetype=access_combined OR sourcetype=cisco_wsa_squid) status>500`
   - Priority: `1` (Highest)
   - Tags: `error`, `web`, `server_error`
4. Click **Save**

### Step 4.4: Test the Event Type

Search using the event type:

```spl
index=web eventtype=web_error
| stats count by status, sourcetype
| sort -count
```

**Expected Results**: All web error events

**Save this search as**: `L9S3`

> **Note**: Event Types:
> - Save search strings as reusable objects
> - Can be searched using eventtype=name
> - Can include multiple criteria and sourcetypes
> - Can have associated tags
> - Priority determines which event type applies when multiple match

---

## Task 5: Working with Event Type Tags

### Scenario

Use tags associated with event types for easier searching.

### Step 5.1: Search Using Event Type Tags

Since we tagged the web_error event type with "error", we can search:

```spl
index=web tag=error
| stats count by sourcetype, status
```

**Expected Results**: Events matching the web_error event type via its tag

### Step 5.2: Create Additional Event Types with Tags

Create an event type for successful web transactions:

1. Navigate to **Settings** → **Event types**
2. Click **New Event Type**
3. Configure:
   - Name: `web_success`
   - Search string: `(sourcetype=access_combined OR sourcetype=cisco_wsa_squid) status>=200 status<300`
   - Priority: `1`
   - Tags: `success`, `web`
4. Click **Save**

### Step 5.3: Compare Event Types

Compare errors vs successes:

```spl
index=web (eventtype=web_error OR eventtype=web_success)
| eval event_category = case(
    eventtype="web_error", "Error",
    eventtype="web_success", "Success",
    1=1, "Other"
)
| timechart count by event_category
```

**Expected Results**: Timeline comparing errors and successful requests

---

## Task 6: Creating Event Types for Security Events

### Scenario

Create event types for different types of security events.

### Step 6.1: Create Failed Authentication Event Type

1. Navigate to **Settings** → **Event types**
2. Click **New Event Type**
3. Configure:
   - Name: `failed_authentication`
   - Search string: `sourcetype=linux_secure "failed password"`
   - Priority: `1`
   - Tags: `authentication`, `failure`, `security`
4. Click **Save**

### Step 6.2: Create Successful Authentication Event Type

1. Click **New Event Type**
2. Configure:
   - Name: `successful_authentication`
   - Search string: `sourcetype=linux_secure "session opened"`
   - Priority: `1`
   - Tags: `authentication`, `success`, `security`
3. Click **Save**

### Step 6.3: Use Event Types in Analysis

Analyze authentication patterns:

```spl
index=security (eventtype=failed_authentication OR eventtype=successful_authentication)
| eval auth_result = if(eventtype="failed_authentication", "Failed", "Successful")
| stats count by auth_result, user
| sort -count
```

**Expected Results**: Authentication attempts by user and result

**Save this search as**: `L9S4`

---

## Task 7: Managing Event Type Priority

### Scenario

When multiple event types match the same event, priority determines which applies.

### Step 7.1: Understanding Priority

Priority values:
- 1 = Highest priority
- 2 = High
- 3 = Medium
- 4 = Low
- 5 = Lowest

### Step 7.2: Create Overlapping Event Types

Create two event types that might match the same events:

1. **web_transaction** (Priority: 3)
   - Search: `sourcetype=access_combined`
   - Tags: `web`, `transaction`

2. **high_value_purchase** (Priority: 1)
   - Search: `sourcetype=access_combined action=purchase price>100`
   - Tags: `web`, `transaction`, `high_value`

### Step 7.3: Test Priority Behavior

```spl
index=web sourcetype=access_combined action=purchase price>100
| table eventtype price
```

**Expected Results**: Events tagged with the higher-priority event type

---

## Task 8: Best Practices for Tags and Event Types

### Scenario

Follow best practices when creating tags and event types.

### Step 8.1: Naming Conventions

Use clear, descriptive names:
- **Tags**: lowercase, underscore-separated (e.g., `privileged_user`, `high_risk`)
- **Event Types**: lowercase, descriptive (e.g., `web_error`, `failed_authentication`)

### Step 8.2: Documentation

Document your tags and event types:
1. Use consistent tagging strategy
2. Document which event types exist
3. Train users on available tags
4. Create a knowledge article

### Step 8.3: Maintenance

Regularly review and update:
1. Remove obsolete tags
2. Update event type searches as data changes
3. Consolidate duplicate or similar event types
4. Verify tags are still relevant

---

## Challenge Exercise (Optional)

### Challenge 1: Comprehensive Security Tagging

Create a complete security tagging system:

1. **Create Tags**:
   - `critical_server`: Tag servers: web-01, db-01, app-01
   - `privileged_port`: Tag ports: 22, 3389, 443, 8443
   - `suspicious_action`: Tag actions: failed, denied, blocked

2. **Create Event Types**:
   - `security_critical`: Events on critical servers with failed actions
   - `brute_force_attempt`: Multiple failed attempts from same IP
   - `privilege_escalation`: Privileged users on non-standard ports

3. **Create Dashboard**: "Security Overview"
   - Failed authentications by source
   - Critical server activity
   - Brute force detection

**Save this search as**: `L9C1`

### Challenge 2: E-commerce Event Type System

Create event types for e-commerce analysis:

1. **Purchase Funnel Event Types**:
   - `browse_event`: action=view
   - `cart_event`: action=addtocart OR action=remove
   - `checkout_event`: action=purchase

2. **Value-Based Event Types**:
   - `small_transaction`: price<50
   - `medium_transaction`: price>=50 AND price<200
   - `large_transaction`: price>=200

3. **Performance Event Types**:
   - `fast_page`: req_time<0.1
   - `slow_page`: req_time>=1

Create a dashboard showing:
- Conversion funnel (browse → cart → purchase)
- Transaction value distribution
- Page performance metrics

**Save this search as**: `L9C2`

---

## Summary

In this lab, you learned:
- ✓ How to create tags for field values to group related data
- ✓ How to apply tags to multiple field values
- ✓ How to create event types to save common search patterns
- ✓ How to set event type priorities for overlapping matches
- ✓ How to use tags and event types in searches
- ✓ How to associate tags with event types
- ✓ Best practices for naming and managing tags and event types

## Key Takeaways

1. **Tags** create meaningful labels for field-value pairs
2. **Multiple values** can share the same tag for easy searching
3. **Event types** save search strings as reusable objects
4. **Priority** determines which event type applies when multiple match (1=Highest, 5=Lowest)
5. **Tags on event types** enable searching with `tag=tagname`
6. **Search syntax**: `tag=tagname` and `eventtype=typename`
7. Tags and event types are **search-time operations**
8. **Consistent naming** and documentation improve usability
9. Tags and event types simplify complex searches and improve dashboard creation

---

## Data Sources Used

- **index=security, sourcetype=linux_secure**: Linux authentication logs with user field for privileged user tagging
- **index=web, sourcetype=access_combined**: Web access logs with status codes for error event types
- **index=network, sourcetype=cisco_wsa_squid**: Web proxy logs with status codes for error event types
- **index=web, sourcetype=access_combined_wcookie**: E-commerce transactions for purchase event types

## Next Steps

In Lab 10, you'll learn to create and use macros to encapsulate complex search logic and create reusable search components with arguments.

---

**Lab 9 Complete!**
