# Splunk Intermediate Course - 2 Day Outline

## Course Overview

This comprehensive 2-day intermediate Splunk course teaches advanced search techniques, data analysis, visualization, and knowledge object management using the **Buttercup Games** e-commerce scenario.

**Company Context**: Buttercup Games is an online and retail gaming company that needs to analyze web traffic, sales data, security events, and game telemetry to optimize operations and ensure security.

## Prerequisites
- Completion of Splunk Fundamentals 1 or equivalent experience
- Basic understanding of SPL (Search Processing Language)
- Familiarity with Splunk web interface

## Course Objectives
By the end of this course, students will be able to:
- Write complex searches using advanced SPL commands
- Create visualizations and interactive dashboards
- Extract and manage fields from unstructured data
- Enrich data using lookups, aliases, and calculated fields
- Create and manage knowledge objects (tags, event types, macros, workflow actions)
- Build and accelerate data models
- Apply best practices for search performance and knowledge management

---

## Day 1: Search Fundamentals and Data Analysis

### Module 1: Beyond Search Fundamentals (1 hour)
**Topics**:
- Search fundamentals review (case sensitivity, wildcards, filtering)
- Using the Job Inspector for troubleshooting
- Understanding search modes (Verbose, Fast, Smart)
- Using the table command for result formatting

**Lab 1**: Beyond Search Fundamentals (30 minutes)
- L1S1-L1S4, L1C1-L1C2

**Data Sources**: index=web (access_combined_wcookie), index=security (linux_secure)

---

### Module 2: Using Transforming Commands for Visualizations (1.5 hours)
**Topics**:
- Chart command for two-dimensional analysis
- Timechart for time-series visualization
- Creating dashboards with panels
- Using limit and useother options
- Formatting visualizations (axis labels, colors, scales)
- Trellis layouts for independent visualizations

**Lab 2**: Transforming Commands for Visualizations (45 minutes)
- Create stacked column charts
- Build "IT Ops" dashboard with drilldown
- Format charts with custom labels
- Create trellis layout visualizations
- L2S1-L2S5

**Data Sources**: linux_secure, vendor_sales, cisco_wsa_squid, access_combined

---

### Module 3: Using Trendlines, Mapping, and Single Value Commands (1.5 hours)
**Topics**:
- Trendline command with simple moving average (sma)
- Single value visualizations with trend indicators and sparklines
- Geographic visualizations with iplocation and geostats
- Choropleth maps using geom command
- Cluster maps for geographic data
- Addtotals command for summary rows

**Lab 3**: Trendlines, Mapping, and Single Value (45 minutes)
- Create trendlines for security events
- Build single value KPIs with sparklines
- Create choropleth map of US sales by state
- Build cluster map of international sales
- Add summary totals to reports
- L3S1-L3S5

**Data Sources**: linux_secure, vendor_sales, cisco_wsa_squid, access_combined

---

### Module 4: Filtering Results and Manipulating Data (1.5 hours)
**Topics**:
- Eval command for data transformation
- Mathematical calculations (bytes to megabytes, ratios)
- Search and where commands for filtering
- Case function for multi-condition logic
- If function with LIKE operator
- Data classification and categorization

**Lab 4**: Filtering and Manipulating Data (45 minutes)
- Convert bytes to megabytes
- Calculate GET/POST ratios
- Filter results with search command
- Classify data using case function
- Challenge: Content type classification
- L4S1-L4S4, L4C1

**Data Sources**: access_combined, linux_secure, cisco_wsa_squid

---

### Module 5: Correlating Events (1 hour)
**Topics**:
- Transaction command for event correlation
- Grouping events by session ID (JSESSIONID)
- Transaction-generated fields (duration, eventcount)
- Calculating transaction duration in minutes
- Using startswith and endswith for transaction boundaries
- Transaction performance considerations

**Lab 5**: Correlating Events (30 minutes)
- Create transactions by session ID
- Calculate session durations
- Filter long-running sessions
- Track shopping cart to purchase workflow
- L5S1-L5S4

**Data Sources**: access_combined_wcookie (web sessions)

---

### Module 6: Introduction to Lookups (1.5 hours)
**Topics**:
- Understanding lookup tables
- Creating CSV lookup files
- Defining lookup definitions
- Configuring automatic lookups
- Using inputlookup and outputlookup
- Enriching data with external information
- HTTP status code lookups

**Lab 6**: Introduction to Lookups (45 minutes)
- Create HTTP status lookup
- Define lookup definitions
- Configure automatic lookups
- Enrich web logs with status descriptions
- Use inputlookup and outputlookup
- L6S1-L6S5

**Data Sources**: access_combined, http_status_lookup.csv

---

## Day 2: Knowledge Objects and Data Models

### Module 7: Creating and Managing Fields (1.5 hours)
**Topics**:
- Understanding field extractions
- Using the Field Extractor (FX) UI
- Regex extraction method
- Delimiter extraction method
- Validating field extractions
- Managing extracted fields

**Lab 7**: Creating and Managing Fields (45 minutes)
- Extract IP and port from linux_secure (regex)
- Extract fields from game logs (delimiter)
- Validate extractions
- Manage field permissions
- L7S1-L7S3

**Data Sources**: linux_secure, SimCubeBeta (games index)

**Important**: Wait ~1 minute after creating extractions for knowledge object replication

---

### Module 8: Working with Field Aliases and Calculated Fields (1.5 hours)
**Topics**:
- Field aliases for username normalization
- Multiple aliases across sourcetypes
- Calculated fields with eval expressions
- Converting units (bytes to megabytes)
- Best practices for field naming
- Knowledge object permissions

**Lab 8**: Field Aliases and Calculated Fields (45 minutes)
- Create username field aliases
- Normalize usernames across data sources
- Create calculated field for megabytes
- Apply aliases to multiple sourcetypes
- L8S1-L8S3

**Data Sources**: cisco_wsa_squid, cisco_firewall, access_combined

---

### Module 9: Creating Tags and Event Types (1.5 hours)
**Topics**:
- Understanding tags vs event types
- Creating tags for field values
- Tagging multiple values (privileged users)
- Creating event types for common searches
- Event type priorities
- Searching with tags and event types
- Use cases for tags vs event types

**Lab 9**: Tags and Event Types (45 minutes)
- Create privileged_user tag
- Tag multiple admin variants
- Create web_error event type
- Search using tags and event types
- L9S1-L9S4

**Data Sources**: security index, access_combined, cisco_wsa_squid

---

### Module 10: Creating and Using Macros (1.5 hours)
**Topics**:
- Search macros for reusable searches
- Basic macros (no arguments)
- Macros with arguments
- Currency conversion example
- Macro validation with error messages
- Nested macros
- Macro best practices

**Lab 10**: Creating and Using Macros (45 minutes)
- Create Europe_sales macro
- Create convert_sales macro with arguments
- Add validation (isnum)
- Test macros with different currencies
- Nest macros
- L10S1-L10S3

**Data Sources**: vendor_sales

**Macro Examples**:
- `Europe_sales` → Filter sales for Germany, France, Italy
- `convert_sales(currency,symbol,rate)` → Convert USD to other currencies

---

### Module 11: Creating and Using Workflow Actions (1 hour)
**Topics**:
- GET workflow actions (external links)
- POST workflow actions
- Search workflow actions
- WHOIS IP lookups
- Security investigation workflows
- Opening external tools from Splunk
- Workflow action best practices

**Lab 11**: Workflow Actions (30 minutes)
- Create GET workflow for WHOIS lookups
- Create POST workflow action
- Create Search workflow for failed logins
- Test workflows from events
- L11S1-L11S3

**Data Sources**: linux_secure (src_ip field)

---

### Module 12: Creating Data Models (2 hours)
**Topics**:
- Understanding data models
- Root events, child datasets, grandchild datasets
- Auto-extracted fields
- Eval expression fields
- Lookup fields in data models
- Using the Pivot interface
- Creating pivot reports and dashboards
- Data model acceleration
- tstats command for performance

**Lab 12**: Creating Data Models (60 minutes)
- Create "Buttercup Games Site Activity" data model
- Define root event: Web requests
- Add auto-extracted fields
- Create child datasets (Successful/Failed requests)
- Create grandchild datasets (purchases, removed)
- Add eval expression field (day of week)
- Add lookup field (status description)
- Create pivot reports
- Build "Weekly Website Activity" dashboard
- Enable data model acceleration
- L12S1-L12S3

**Data Sources**: access_combined

**Data Model Structure**:
```
Buttercup Games Site Activity
└── Web requests (root)
    ├── Successful requests (status<400)
    │   └── purchases (action=purchase productId=*)
    └── Failed requests (status>399)
        └── removed (action=remove productId=*)
```

---

## Lab Exercises Summary

| Lab | Title | Duration | Save Tags |
|-----|-------|----------|-----------|
| Lab 1 | Beyond Search Fundamentals | 30 min | L1S1-L1S4, L1C1-L1C2 |
| Lab 2 | Transforming Commands for Visualizations | 45 min | L2S1-L2S5 |
| Lab 3 | Trendlines, Mapping, Single Value | 45 min | L3S1-L3S5 |
| Lab 4 | Filtering and Manipulating Data | 45 min | L4S1-L4S4, L4C1 |
| Lab 5 | Correlating Events | 30 min | L5S1-L5S4 |
| Lab 6 | Introduction to Lookups | 45 min | L6S1-L6S5 |
| Lab 7 | Creating and Managing Fields | 45 min | L7S1-L7S3 |
| Lab 8 | Field Aliases and Calculated Fields | 45 min | L8S1-L8S3 |
| Lab 9 | Tags and Event Types | 45 min | L9S1-L9S4 |
| Lab 10 | Creating and Using Macros | 45 min | L10S1-L10S3 |
| Lab 11 | Workflow Actions | 30 min | L11S1-L11S3 |
| Lab 12 | Creating Data Models | 60 min | L12S1-L12S3 |

**Total Lab Time**: ~8.5 hours

---

## Data Sources

### Indexes and Sourcetypes

1. **index=web**
   - **sourcetype=access_combined**: Standard web access logs
   - **sourcetype=access_combined_wcookie**: Web logs with session cookies (JSESSIONID)
   - **sourcetype=vendor_sales**: Retail store sales data

2. **index=security**
   - **sourcetype=linux_secure**: Linux authentication logs (SSH, failed logins)

3. **index=network**
   - **sourcetype=cisco_wsa_squid**: Cisco Web Security Appliance / Squid proxy logs
   - **sourcetype=cisco_firewall**: Cisco firewall logs

4. **index=games**
   - **sourcetype=SimCubeBeta**: Game telemetry data (comma-delimited)

### Lookup Files

- **http_status_lookup.csv**: HTTP status codes and descriptions
- **product_catalog.csv**: Buttercup Games product information

### Key Fields by Sourcetype

**access_combined_wcookie**:
- clientip, method, url, status, bytes, req_time
- JSESSIONID, action, productId, product_name, categoryId, price

**vendor_sales**:
- VendorID, VendorCountry, VendorStateProvince
- productId, product_name, categoryId, price, quantity

**linux_secure**:
- src_ip, user, vendor_action (session opened, failed password, etc.)

**cisco_wsa_squid**:
- src_ip, cs_username, sc_bytes, status, method, url
- http_content_type, usage

**SimCubeBeta**:
- time, src, version, user, CharacterName, action, role

---

## Vendor ID Mappings (for vendor_sales)

| Vendor ID Range | Region |
|-----------------|--------|
| 1000-2999 | USA |
| 3000-3999 | Canada |
| 4000-4999 | Caribbean, Central & South America |
| 5000-6999 | Europe and Middle East |
| 7000-8999 | Asia and Pacific |
| 9000-9900 | Africa |
| 9901-9999 | Outliers (South Pole, etc.) |

---

## Product Categories

- **STRATEGY**: Strategy games (Mediocre Kingdoms, World of Cheese, etc.)
- **SIMULATION**: Simulation games (Grand Theft Scooter, The Sims, etc.)
- **ACTION**: Action games (Shrek Soccer, Halo, Call of Duty, etc.)
- **SPORTS**: Sports games (Madden NFL, FIFA, NBA 2K, etc.)
- **accessories**: Gaming peripherals (headsets, controllers, keyboards, etc.)

---

## Course Delivery Notes

### Day 1 Schedule (6.5 hours)
- 9:00-10:00: Module 1 + Lab 1
- 10:00-11:30: Module 2 + Lab 2
- 11:30-12:00: Break
- 12:00-1:30: Module 3 + Lab 3
- 1:30-2:30: Lunch
- 2:30-4:00: Module 4 + Lab 4
- 4:00-5:00: Module 5 + Lab 5
- 5:00-6:00: Module 6 + Lab 6 (partial)

### Day 2 Schedule (6.5 hours)
- 9:00-9:30: Module 6 + Lab 6 (complete)
- 9:30-11:00: Module 7 + Lab 7
- 11:00-11:15: Break
- 11:15-12:45: Module 8 + Lab 8
- 12:45-1:45: Lunch
- 1:45-3:15: Module 9 + Lab 9
- 3:15-4:45: Module 10 + Lab 10
- 4:45-5:15: Module 11 + Lab 11
- 5:15-6:30: Module 12 + Lab 12

### Instructor Preparation

1. **Before Class**:
   - Start Splunk instances for all students
   - Generate Buttercup Games data: `python scripts/data-generators/generate_buttercup_data.py`
   - Upload data to appropriate indexes with correct sourcetypes
   - Create indexes: web, security, network, games
   - Upload lookup files: http_status_lookup.csv, product_catalog.csv
   - Test all lab exercises

2. **Equipment Needed**:
   - Splunk Enterprise or Cloud instances (one per student + instructor)
   - Presentation system with reveal.js presentation
   - Lab exercise materials (markdown files)
   - Sample data files

3. **Knowledge Object Sharing**:
   - Create app context: class_Fund2 or search
   - Set appropriate permissions for knowledge objects
   - Remember: Field extractions take ~1 minute to replicate in search head clusters

---

## Assessment

Students should be able to:
- ✓ Write efficient searches using advanced SPL commands
- ✓ Create visualizations appropriate for different data types
- ✓ Extract fields from unstructured data
- ✓ Enrich data using lookups and calculated fields
- ✓ Create reusable knowledge objects (macros, tags, event types)
- ✓ Build data models and use the Pivot interface
- ✓ Apply performance best practices

---

## Next Steps After Course

- Practice with own organizational data
- Explore Splunk Certifications (Splunk Core Certified Power User)
- Join Splunk Community and .conf events
- Continue to Splunk Enterprise Security or ITSI courses
