# Lab 11: Creating and Using Workflow Actions

**Splunk Intermediate – Lab Exercises**

> **Note**: This lab should be completed in a non-production environment.

## Lab Description

This lab covers:
- Understanding workflow actions and their types
- Creating GET workflow actions for external links
- Creating POST workflow actions for submitting data
- Creating Search workflow actions for contextual searches
- Configuring field value parameters in workflow actions
- Testing and validating workflow actions
- Best practices for workflow action design

## Scenario

You are a Splunk administrator for Buttercup Games. The security team needs quick access to WHOIS information for suspicious IP addresses. The operations team wants to quickly search for all failed login attempts from a specific IP. You'll create workflow actions that appear in the event viewer and enable these contextual investigations.

---

## Task 1: Understanding Workflow Actions

### Scenario

Learn about the three types of workflow actions and when to use each.

### Step 1.1: Types of Workflow Actions

**GET Workflow Actions**:
- Open external URLs
- Pass field values as URL parameters
- Example: WHOIS lookup, Google search, threat intel lookup

**POST Workflow Actions**:
- Submit data to external systems
- Send field values in POST body
- Example: Create ticket, submit to API

**Search Workflow Actions**:
- Perform a new Splunk search
- Use field values in search criteria
- Example: Investigate related events, drill down

### Step 1.2: Use Cases

Common workflow action scenarios:
- IP address → WHOIS lookup
- Username → HR system lookup
- Error code → Knowledge base search
- Server name → Monitoring dashboard
- Hash value → Threat intelligence platform

---

## Task 2: Creating a GET Workflow Action

### Scenario

Create a GET workflow action that looks up IP address information using whois.is.

### Step 2.1: Identify the Target URL

The URL pattern for WHOIS lookup:
```
http://who.is/whois-ip/ip-address/[IP_ADDRESS]
```

Example:
```
http://who.is/whois-ip/ip-address/192.168.1.100
```

### Step 2.2: Create the GET Workflow Action

1. Navigate to **Settings** → **Fields** → **Workflow actions**
2. Click **New Workflow Action**
3. Configure:
   - **Name**: `get_whois_info`
   - **Label**: `Get WHOIS info for IP: $src_ip$`
   - **Apply only to specific fields**: Yes
     - Field name: `src_ip`
   - **Action type**: `link`
   - **Link method**: `get`
   - **URI**: `http://who.is/whois-ip/ip-address/$src_ip$`
   - **Open link in**: `New window`
   - **Show action in**: `Both` (Event menu and Field menu)
4. Click **Save**

### Step 2.3: Test the GET Workflow Action

1. Run this search:
```spl
index=security sourcetype=linux_secure
| table _time src_ip user action
```

2. In the search results, click on an event to expand it
3. Click on the **src_ip** field value
4. Look for the workflow action: "Get WHOIS info for IP: [IP]"
5. Click the workflow action
6. Verify it opens whois.is with the IP address

**Expected Results**: A new browser window opens with WHOIS information for the selected IP address

**Save this search as**: `L11S1`

> **Note**: GET workflow actions:
> - Use `$field_name$` to reference field values in URLs
> - Can pass multiple field values as URL parameters
> - Open in new windows to preserve Splunk session
> - Work with any external web service

---

## Task 3: Creating Additional GET Workflow Actions

### Scenario

Create more GET workflow actions for common investigation tasks.

### Step 3.1: Create Google Search Workflow Action

Create a workflow action to Google search for usernames:

1. Navigate to **Settings** → **Fields** → **Workflow actions**
2. Click **New Workflow Action**
3. Configure:
   - **Name**: `google_search_user`
   - **Label**: `Google search for: $user$`
   - **Apply only to specific fields**: Yes
     - Field name: `user`
   - **Action type**: `link`
   - **Link method**: `get`
   - **URI**: `https://www.google.com/search?q=$user$`
   - **Open link in**: `New window`
4. Click **Save**

### Step 3.2: Create Product Search Workflow Action

Create a workflow action to view product details:

1. Click **New Workflow Action**
2. Configure:
   - **Name**: `view_product_details`
   - **Label**: `View details for: $product_name$`
   - **Apply only to specific fields**: Yes
     - Field name: `product_name`
   - **Action type**: `link`
   - **Link method**: `get`
   - **URI**: `http://www.buttercupgames.com/products/$productId$`
   - **Open link in**: `New window`
3. Click **Save**

### Step 3.3: Create Multi-Field Workflow Action

Create a workflow action using multiple field values:

1. Click **New Workflow Action**
2. Configure:
   - **Name**: `investigate_user_ip`
   - **Label**: `Investigate $user$ from $src_ip$`
   - **Apply to all fields**: Yes
   - **Action type**: `link`
   - **Link method**: `get`
   - **URI**: `http://internal-security-portal.com/investigate?user=$user$&ip=$src_ip$`
   - **Open link in**: `New window`
4. Click **Save**

---

## Task 4: Creating POST Workflow Actions

### Scenario

Create a POST workflow action to submit security incidents to a ticketing system.

### Step 4.1: Understand POST Actions

POST workflow actions:
- Send data in request body, not URL
- More secure for sensitive data
- Support complex data structures
- Require receiving endpoint that accepts POST

### Step 4.2: Create Security Incident POST Action

1. Navigate to **Settings** → **Fields** → **Workflow actions**
2. Click **New Workflow Action**
3. Configure:
   - **Name**: `create_security_ticket`
   - **Label**: `Create security ticket for $src_ip$`
   - **Apply only to specific fields**: Yes
     - Field name: `src_ip`
   - **Action type**: `link`
   - **Link method**: `post`
   - **URI**: `http://ticketing-system.local/api/create_ticket`
   - **Post arguments**:
     ```
     priority=high&source_ip=$src_ip$&user=$user$&event_time=$_time$&action=failed_login
     ```
   - **Open link in**: `New window`
4. Click **Save**

### Step 4.3: Test POST Workflow Action

Note: POST actions require a functioning endpoint. In a lab environment:

```spl
index=security sourcetype=linux_secure "failed password"
| table _time src_ip user
```

Click on an event and look for the "Create security ticket" workflow action.

> **Tip**: POST workflow actions are ideal for:
> - Creating tickets in external systems
> - Submitting data to APIs
> - Triggering automated workflows
> - Sending sensitive data securely

---

## Task 5: Creating Search Workflow Actions

### Scenario

Create search workflow actions that launch new Splunk searches based on field values.

### Step 5.1: Create Failed Login Investigation Action

1. Navigate to **Settings** → **Fields** → **Workflow actions**
2. Click **New Workflow Action**
3. Configure:
   - **Name**: `search_failed_login_by_ip`
   - **Label**: `Search failed logins by IP: $src_ip$`
   - **Apply only to specific fields**: Yes
     - Field name: `src_ip`
   - **Action type**: `search`
   - **Search string**:
     ```
     index=security sourcetype=linux_secure "failed password" src_ip=$src_ip$ | stats count by user, src_ip | sort -count
     ```
   - **Search view**: `flashtimeline`
   - **Time range**:
     - **Earliest**: `-7d`
     - **Latest**: `now`
4. Click **Save**

### Step 5.2: Test the Search Workflow Action

1. Run this search:
```spl
index=security sourcetype=linux_secure
| table _time src_ip user
```

2. Click on an **src_ip** field value
3. Select the workflow action: "Search failed logins by IP: [IP]"
4. Verify a new search launches showing all failed logins from that IP

**Expected Results**: A new search window opens showing failed login attempts from the selected IP address over the last 7 days

**Save this search as**: `L11S2`

### Step 5.3: Create User Activity Investigation Action

Create a workflow action to investigate all activity for a user:

1. Click **New Workflow Action**
2. Configure:
   - **Name**: `search_user_activity`
   - **Label**: `View all activity for: $user$`
   - **Apply only to specific fields**: Yes
     - Field name: `user`
   - **Action type**: `search`
   - **Search string**:
     ```
     (index=security OR index=web OR index=network) user=$user$ | stats count by index, sourcetype, action | sort -count
     ```
   - **Search view**: `flashtimeline`
   - **Time range**:
     - **Earliest**: `-24h`
     - **Latest**: `now`
3. Click **Save**

### Step 5.4: Create Product Purchase History Action

Create a workflow action to view purchase history for a product:

1. Click **New Workflow Action**
2. Configure:
   - **Name**: `search_product_purchases`
   - **Label**: `View purchase history: $product_name$`
   - **Apply only to specific fields**: Yes
     - Field name: `product_name`
   - **Action type**: `search`
   - **Search string**:
     ```
     index=web sourcetype=access_combined action=purchase product_name="$product_name$" | timechart count | trendline sma4(count) as trend
     ```
   - **Search view**: `flashtimeline`
   - **Time range**:
     - **Earliest**: `-30d`
     - **Latest**: `now`
3. Click **Save**

**Save this search as**: `L11S3`

> **Note**: Search workflow actions:
> - Launch new Splunk searches
> - Can use any field value as search parameter
> - Support time range configuration
> - Choose appropriate search view (flashtimeline, smart, etc.)
> - Use quotes around `$field$` if field may contain spaces

---

## Task 6: Advanced Workflow Action Techniques

### Scenario

Create more sophisticated workflow actions with conditional logic.

### Step 6.1: Create Conditional Workflow Actions

Workflow actions can be limited to specific sourcetypes:

1. Create workflow action
2. In **Show action in fields**: Add field and sourcetype filters
3. Example: Only show for src_ip in linux_secure sourcetype

### Step 6.2: Create Multi-Step Investigation Workflow

Create a series of related workflow actions:

1. **Initial Investigation**: `search_ip_overview`
2. **Deep Dive**: `search_ip_detailed_activity`
3. **Correlation**: `search_related_ips`
4. **External**: `get_threat_intel`

Users follow the workflow:
Event → Initial Investigation → Deep Dive → Correlation → External Lookup

### Step 6.3: Use Tokens in Workflow Actions

Reference multiple fields in search workflow:

```
index=web sourcetype=access_combined clientip=$clientip$ action=$action$ productId=$productId$
| transaction JSESSIONID
| table _time clientip action productId duration
```

---

## Task 7: Managing Workflow Actions

### Scenario

Learn to view, edit, test, and troubleshoot workflow actions.

### Step 7.1: View All Workflow Actions

1. Navigate to **Settings** → **Fields** → **Workflow actions**
2. Review all configured workflow actions
3. Check which fields they apply to
4. Verify app context and permissions

### Step 7.2: Test Workflow Actions

Systematically test each workflow action:

```spl
index=security sourcetype=linux_secure
| table src_ip user action
```

For each workflow action:
1. Click on the appropriate field
2. Verify the action appears
3. Click the action
4. Verify it works as expected

### Step 7.3: Troubleshoot Common Issues

**Action doesn't appear**:
- Check field name matches exactly (case-sensitive)
- Verify sourcetype filter if applied
- Check app context and permissions
- Verify field exists in events

**Action fails or shows error**:
- Check URL syntax and field references
- Verify external endpoints are accessible
- Check for special characters in field values
- Test with URL encoding if needed

**Search action doesn't work**:
- Verify search syntax is valid
- Check time range settings
- Ensure index and sourcetype exist
- Test search independently first

---

## Challenge Exercise (Optional)

### Challenge 1: Create Comprehensive Security Workflow

Create a complete security investigation workflow system:

1. **GET Actions**:
   - WHOIS lookup for src_ip
   - Threat intelligence lookup (VirusTotal, AbuseIPDB)
   - GeoIP location map

2. **POST Actions**:
   - Create security incident ticket
   - Block IP address via firewall API
   - Send alert to Slack/Teams

3. **Search Actions**:
   - Search all activity from IP (last 7 days)
   - Search all activity for user (last 24 hours)
   - Search similar failed login patterns
   - Correlation search for related IPs

4. **Create Investigation Dashboard**:
   - Panel showing recent security events
   - Each event has workflow actions enabled
   - Quick investigation workflow

**Save this search as**: `L11C1`

### Challenge 2: Create E-commerce Analysis Workflow

Create workflow actions for e-commerce analysis:

1. **Product Investigation**:
   - View product details on website
   - Search purchase history
   - Search cart abandonment for product
   - View related products

2. **Customer Investigation**:
   - View customer profile
   - Search all purchases by customer
   - Search session details
   - Calculate customer lifetime value

3. **Performance Investigation**:
   - Search slow page loads for URI
   - Search error codes
   - View response time trends

Create a dashboard showing:
- Top products (with workflow actions)
- Top customers (with workflow actions)
- Slowest pages (with workflow actions)

**Save this search as**: `L11C2`

---

## Summary

In this lab, you learned:
- ✓ The three types of workflow actions (GET, POST, Search)
- ✓ How to create GET workflow actions for external links
- ✓ How to create POST workflow actions for submitting data
- ✓ How to create Search workflow actions for contextual searches
- ✓ How to use field values as parameters in workflow actions
- ✓ How to configure time ranges for search workflow actions
- ✓ How to test and troubleshoot workflow actions
- ✓ Best practices for workflow action design

## Key Takeaways

1. **Workflow actions** enable contextual investigation from event data
2. **GET actions** open external URLs with field values as parameters
3. **POST actions** submit data to external systems securely
4. **Search actions** launch new Splunk searches with field values
5. **Field references** use `$field_name$` syntax
6. **Apply to specific fields** to control where actions appear
7. **Test systematically** to ensure actions work as expected
8. **Time ranges** can be configured for search workflow actions
9. Workflow actions improve **investigation efficiency**
10. Create **related workflow actions** for multi-step investigations

---

## Data Sources Used

- **index=security, sourcetype=linux_secure**: Linux authentication logs with src_ip and user fields for security workflow actions
- **index=web, sourcetype=access_combined**: Web access logs for product and customer investigation workflow actions
- **index=web, sourcetype=access_combined_wcookie**: E-commerce logs with JSESSIONID, productId, and action for transaction analysis

## Next Steps

In Lab 12, you'll learn to create data models that organize your data into hierarchical datasets, enabling powerful pivot reporting and simplified data access for non-technical users.

---

**Lab 11 Complete!**
