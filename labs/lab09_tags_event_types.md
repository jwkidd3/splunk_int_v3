# Lab 9: Tags and Event Types

**Splunk Intermediate – Lab Exercises**

## Objectives

- Create tags for field values
- Create event types for common searches
- Set event type priorities
- Use tags and event types in searches

---

## Task 1: Identify User Variations

```spl
index=security sourcetype=linux_secure
| stats count by user
| sort -count
```

Multiple privileged users: admin, administrator, sysadmin, itmadmin, sapadmin.

### Without Tags

```spl
index=security sourcetype=linux_secure (user=admin OR user=administrator OR user=sysadmin OR user=itmadmin OR user=sapadmin)
| stats count by user
```

Complex search required.

---

## Task 2: Create Tags

### Step 1: Via Field Sidebar

1. Run: `index=security sourcetype=linux_secure user=admin`
2. In **Fields** sidebar, click **user**
3. Click dots (⋯) next to "admin"
4. **Edit Tags**
5. Tag name: `privileged_user`

### Step 2: Tag Additional Values

Repeat for:
- `user=administrator` → tag: `privileged_user`
- `user=sysadmin` → tag: `privileged_user`
- `user=itmadmin` → tag: `privileged_user`
- `user=sapadmin` → tag: `privileged_user`

### Step 3: Via Settings (Alternative)

1. **Settings** → **Tags**
2. **New Tag**
3. Name: `privileged_user`
4. Add field/value pairs for each user

### Step 4: Test Tag

```spl
index=security sourcetype=linux_secure tag=privileged_user
| stats count by user
```

**Save as**: `L9S1`

---

## Task 3: Use Tags

### Simple Search

```spl
index=security sourcetype=linux_secure tag=privileged_user
| timechart count by user
```

### Combined with Criteria

```spl
index=security sourcetype=linux_secure tag=privileged_user "failed password"
| stats count by user, src_ip
| sort -count
```

### Negate Tag

```spl
index=security sourcetype=linux_secure NOT tag=privileged_user
| stats count by user
| sort -count
```

**Save as**: `L9S2`

---

## Task 4: Create Event Types

### Step 1: Create Web Error Event Type

```spl
(index=web sourcetype=access_combined OR sourcetype=cisco_wsa_squid) status>500
| stats count by status, sourcetype
```

### Step 2: Save as Event Type

1. **Save As** → **Event Type**
2. Configure:
   - Name: `web_error`
   - Search: `(sourcetype=access_combined OR sourcetype=cisco_wsa_squid) status>500`
   - Priority: `1` (Highest)
   - Color: Red
   - Tags: `error`, `web`, `server_error`

### Step 3: Via Settings (Alternative)

1. **Settings** → **Event types**
2. **New Event Type**
3. Configure as above

### Step 4: Test

```spl
index=web eventtype=web_error
| stats count by status, sourcetype
| sort -count
```

**Save as**: `L9S3`

---

## Task 5: Event Type Tags

### Search by Tag

```spl
index=web tag=error
| stats count by sourcetype, status
```

### Create Success Event Type

1. **Settings** → **Event types**
2. **New Event Type**
3. Configure:
   - Name: `web_success`
   - Search: `(sourcetype=access_combined OR sourcetype=cisco_wsa_squid) status>=200 status<300`
   - Priority: `1`
   - Tags: `success`, `web`

### Compare Event Types

```spl
index=web (eventtype=web_error OR eventtype=web_success)
| eval event_category = case(
    eventtype="web_error", "Error",
    eventtype="web_success", "Success",
    1=1, "Other"
)
| timechart count by event_category
```

---

## Task 6: Security Event Types

### Failed Authentication

1. **Settings** → **Event types**
2. **New Event Type**
3. Configure:
   - Name: `failed_authentication`
   - Search: `sourcetype=linux_secure "failed password"`
   - Priority: `1`
   - Tags: `authentication`, `failure`, `security`

### Successful Authentication

1. **New Event Type**
2. Configure:
   - Name: `successful_authentication`
   - Search: `sourcetype=linux_secure "session opened"`
   - Priority: `1`
   - Tags: `authentication`, `success`, `security`

### Analyze Patterns

```spl
index=security (eventtype=failed_authentication OR eventtype=successful_authentication)
| eval auth_result = if(eventtype="failed_authentication", "Failed", "Successful")
| stats count by auth_result, user
| sort -count
```

**Save as**: `L9S4`

---

## Task 7: Event Type Priority

### Priority Values

- 1 = Highest
- 2 = High
- 3 = Medium
- 4 = Low
- 5 = Lowest

### Create Overlapping Types

1. **web_transaction** (Priority: 3)
   - Search: `sourcetype=access_combined`
   - Tags: `web`, `transaction`

2. **high_value_purchase** (Priority: 1)
   - Search: `sourcetype=access_combined action=purchase price>100`
   - Tags: `web`, `transaction`, `high_value`

Higher priority wins when both match.

---

## Challenge: Security Tagging System

Create comprehensive security tags and event types:

1. **Tags**:
   - `critical_server`: web-01, db-01, app-01
   - `privileged_port`: 22, 3389, 443, 8443
   - `suspicious_action`: failed, denied, blocked

2. **Event Types**:
   - `security_critical`: Critical servers with failed actions
   - `brute_force_attempt`: Multiple failures from same IP
   - `privilege_escalation`: Privileged users on non-standard ports

3. **Dashboard**: Security Overview with all event types

**Save as**: `L9C1`

---

## Summary

- Tags create labels for field-value pairs
- Multiple values can share the same tag
- Event types save search strings as reusable objects
- Priority determines which event type applies (1=Highest, 5=Lowest)
- Tags on event types enable `tag=tagname` searches
- Syntax: `tag=tagname` and `eventtype=typename`
- Simplifies complex searches and improves dashboards

---

**Lab 9 Complete!**
