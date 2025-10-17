# Lab 11: Workflow Actions

**Splunk Intermediate – Lab Exercises**

## Objectives

- Create GET workflow actions for external links
- Create POST workflow actions for data submission
- Create Search workflow actions for contextual searches
- Use field values as parameters

---

## Task 1: Workflow Action Types

### GET Actions
- Open external URLs
- Pass field values as URL parameters
- Example: WHOIS lookup, threat intel

### POST Actions
- Submit data to external systems
- Send field values in POST body
- Example: Create ticket, API submission

### Search Actions
- Launch new Splunk searches
- Use field values in search criteria
- Example: Investigate related events

---

## Task 2: GET Workflow Action

### Step 1: Create WHOIS Lookup

1. **Settings** → **Fields** → **Workflow actions**
2. **New Workflow Action**
3. Configure:
   - Name: `get_whois_info`
   - Label: `Get WHOIS info for IP: $src_ip$`
   - Apply to field: `src_ip`
   - Action type: `link`
   - Link method: `get`
   - URI: `http://who.is/whois-ip/ip-address/$src_ip$`
   - Open in: `New window`
   - Show in: `Both`

### Step 2: Test

```spl
index=security sourcetype=linux_secure
| table _time src_ip user action
```

Click on src_ip value → Workflow action appears.

**Save as**: `L11S1`

---

## Task 3: Additional GET Actions

### Google Search for User

1. **New Workflow Action**
2. Configure:
   - Name: `google_search_user`
   - Label: `Google search for: $user$`
   - Apply to field: `user`
   - Action type: `link`
   - Link method: `get`
   - URI: `https://www.google.com/search?q=$user$`

### Product Details

1. **New Workflow Action**
2. Configure:
   - Name: `view_product_details`
   - Label: `View details for: $product_name$`
   - Apply to field: `product_name`
   - Action type: `link`
   - URI: `http://www.buttercupgames.com/products/$productId$`

---

## Task 4: POST Workflow Action

### Create Security Ticket

1. **Settings** → **Fields** → **Workflow actions**
2. **New Workflow Action**
3. Configure:
   - Name: `create_security_ticket`
   - Label: `Create security ticket for $src_ip$`
   - Apply to field: `src_ip`
   - Action type: `link`
   - Link method: `post`
   - URI: `http://ticketing-system.local/api/create_ticket`
   - Post arguments: `priority=high&source_ip=$src_ip$&user=$user$&event_time=$_time$&action=failed_login`

### Test

```spl
index=security sourcetype=linux_secure "failed password"
| table _time src_ip user
```

Click event → Look for "Create security ticket" action.

---

## Task 5: Search Workflow Actions

### Step 1: Failed Login Investigation

1. **Settings** → **Fields** → **Workflow actions**
2. **New Workflow Action**
3. Configure:
   - Name: `search_failed_login_by_ip`
   - Label: `Search failed logins by IP: $src_ip$`
   - Apply to field: `src_ip`
   - Action type: `search`
   - Search: `index=security sourcetype=linux_secure "failed password" src_ip=$src_ip$ | stats count by user, src_ip | sort -count`
   - Time range: Earliest `-7d`, Latest `now`

### Step 2: Test

```spl
index=security sourcetype=linux_secure
| table _time src_ip user
```

Click src_ip → Select workflow action → New search launches.

**Save as**: `L11S2`

---

## Task 6: User Activity Search

### Create Action

1. **New Workflow Action**
2. Configure:
   - Name: `search_user_activity`
   - Label: `View all activity for: $user$`
   - Apply to field: `user`
   - Action type: `search`
   - Search: `(index=security OR index=web OR index=network) user=$user$ | stats count by index, sourcetype, action | sort -count`
   - Time range: Earliest `-24h`, Latest `now`

### Product Purchase History

1. **New Workflow Action**
2. Configure:
   - Name: `search_product_purchases`
   - Label: `View purchase history: $product_name$`
   - Apply to field: `product_name`
   - Action type: `search`
   - Search: `index=web sourcetype=access_combined action=purchase product_name="$product_name$" | timechart count | trendline sma4(count) as trend`
   - Time range: Earliest `-30d`, Latest `now`

**Save as**: `L11S3`

---

## Task 7: Manage Actions

### View All Actions

1. **Settings** → **Fields** → **Workflow actions**
2. Review configured actions
3. Check field applicability and permissions

### Test Actions

```spl
index=security sourcetype=linux_secure
| table src_ip user action
```

For each action:
1. Click appropriate field
2. Verify action appears
3. Click and verify it works

### Troubleshoot

**Action doesn't appear**:
- Check field name (case-sensitive)
- Verify sourcetype filter
- Check app context and permissions

**Action fails**:
- Check URL syntax
- Verify field references
- Test external endpoints

---

## Challenge: Security Investigation Workflow

Create comprehensive workflow:

1. **GET Actions**:
   - WHOIS for src_ip
   - Threat intel lookup (VirusTotal)
   - GeoIP map

2. **POST Actions**:
   - Create incident ticket
   - Block IP via firewall API
   - Send Slack alert

3. **Search Actions**:
   - All activity from IP (7 days)
   - All activity for user (24 hours)
   - Similar failed login patterns

4. **Dashboard**: Recent security events with workflow actions

**Save as**: `L11C1`

---

## Summary

- Workflow actions enable contextual investigation
- GET opens URLs with field values as parameters
- POST submits data to external systems
- Search launches new Splunk searches
- Field references use `$field_name$` syntax
- Apply to specific fields to control visibility
- Configure time ranges for search actions
- Improves investigation efficiency

---

**Lab 11 Complete!**
