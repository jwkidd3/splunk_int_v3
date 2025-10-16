# Splunk Intermediate Training Course v3

A comprehensive 2-day intermediate-level Splunk training program covering advanced search techniques, data modeling, visualizations, and knowledge object management using the **Buttercup Games** e-commerce scenario.

## Course Overview

This repository contains all materials needed to deliver or take a 2-day Splunk intermediate training course, including:
- **12 hands-on lab exercises** in Markdown format
- Interactive reveal.js presentation
- **Buttercup Games data generation scripts** (~27,000 events)
- Dockerized Splunk environment
- Complete course outline and documentation
- **4 dedicated Splunk indexes** (web, security, network, games)

### Target Audience
- Splunk users with basic SPL knowledge
- Those who have completed Splunk Fundamentals 1
- IT professionals wanting to advance their Splunk skills

### What You'll Learn
- Advanced search techniques (Job Inspector, search modes, case sensitivity)
- Transforming commands for visualizations (chart, timechart, trellis layouts)
- Geographic visualizations and trendlines
- Data manipulation with eval functions
- Event correlation with transaction command
- Creating and managing lookups
- Field extraction (regex and delimiter methods)
- Field aliases and calculated fields
- Tags, event types, and search macros
- Workflow actions for external integrations
- Building and accelerating data models
- Using the Pivot interface for data model reporting

## Quick Start

**For complete setup instructions**, see `QUICK_START.md` or `labs/lab00_data_loading.md`

### 1. Start Splunk Environment

```bash
# Windows
scripts\start-splunk.bat

# Access Splunk at: http://localhost:8000
# Username: admin  |  Password: password
```

### 2. Generate Buttercup Games Data

```bash
# Windows
scripts\generate-data.bat

# Or directly with Python
python scripts/data-generators/generate_buttercup_data.py
```

This creates ~27,000 events across multiple data sources in the `data/` directory.

### 3. Create 4 Indexes in Splunk

In Splunk Web UI: **Settings** → **Indexes** → **New Index**

Create these indexes:
- **web** - Online store and vendor sales
- **security** - Authentication events
- **network** - Proxy logs
- **games** - Game telemetry

### 4. Upload Data to Indexes

Upload each file to its designated index:

| File | Sourcetype | Index |
|------|------------|-------|
| web_access.log | access_combined_wcookie | **web** |
| vendor_sales.csv | vendor_sales | **web** |
| linux_secure.log | linux_secure | **security** |
| cisco_wsa_squid.log | cisco_wsa_squid | **network** |
| simcube_beta.csv | SimCubeBeta | **games** |

**Detailed upload instructions**: See `labs/lab00_data_loading.md`

### 5. Upload Lookup Files

**Settings** → **Lookups** → **Lookup table files** → Upload:
- `http_status_lookup.csv`
- `product_catalog.csv`

### 6. Start Lab 1

Open `labs/lab01_beyond_search_fundamentals.md` and begin!

## Course Structure

### Day 1: Search Fundamentals and Data Analysis (6 labs)

#### Lab 1: Beyond Search Fundamentals (30 min)
- Search fundamentals review, Job Inspector, search modes, table command

#### Lab 2: Transforming Commands for Visualizations (45 min)
- Chart, timechart, dashboards, trellis layouts

#### Lab 3: Trendlines, Mapping, and Single Value (45 min)
- Trendlines, single value KPIs, geographic visualizations, choropleth maps

#### Lab 4: Filtering and Manipulating Data (45 min)
- Eval functions, case/if logic, data transformation

#### Lab 5: Correlating Events (30 min)
- Transaction command, session tracking, event correlation

#### Lab 6: Introduction to Lookups (45 min)
- Creating lookups, automatic lookups, inputlookup/outputlookup

### Day 2: Knowledge Objects and Data Models (6 labs)

#### Lab 7: Creating and Managing Fields (45 min)
- Field Extractor UI, regex and delimiter extraction

#### Lab 8: Field Aliases and Calculated Fields (45 min)
- Username normalization, unit conversion, calculated fields

#### Lab 9: Tags and Event Types (45 min)
- Creating tags, defining event types, use cases

#### Lab 10: Creating and Using Macros (45 min)
- Search macros, arguments, validation

#### Lab 11: Workflow Actions (30 min)
- GET/POST/Search workflows, external integrations

#### Lab 12: Creating Data Models (60 min)
- Data model structure, Pivot interface, acceleration

**Total Duration**: 2 days (~8.5 hours of hands-on labs)

## Repository Structure

```
splunk_int_v3/
├── data/                                      # Generated Buttercup Games data
│   ├── web_access.log                         # 15,000 events → index=web
│   ├── vendor_sales.csv                       # 5,000 records → index=web
│   ├── linux_secure.log                       # 2,000 events → index=security
│   ├── cisco_wsa_squid.log                    # 3,000 events → index=network
│   ├── simcube_beta.csv                       # 2,000 events → index=games
│   ├── http_status_lookup.csv                 # Lookup table
│   └── product_catalog.csv                    # Lookup table
├── labs/                                      # 13 Lab exercises (Markdown)
│   ├── lab00_data_loading.md                  # Data loading activity
│   ├── lab01_beyond_search_fundamentals.md
│   ├── lab02_transforming_commands_visualizations.md
│   ├── lab03_trendlines_mapping_single_value.md
│   ├── lab04_filtering_manipulating_data.md
│   ├── lab05_correlating_events.md
│   ├── lab06_introduction_to_lookups.md
│   ├── lab07_creating_managing_fields.md
│   ├── lab08_field_aliases_calculated_fields.md
│   ├── lab09_tags_event_types.md
│   ├── lab10_creating_using_macros.md
│   ├── lab11_workflow_actions.md
│   └── lab12_creating_data_models.md
├── old labs/                                  # Original PDF lab files (reference)
├── presentation/                              # reveal.js presentation
│   ├── index.html
│   └── README.md
├── scripts/                                   # Utility scripts
│   ├── data-generators/
│   │   ├── generate_buttercup_data.py        # Buttercup Games data generator
│   │   └── generate_sample_data.py           # (old, not used)
│   ├── cleanup-splunk.bat
│   ├── generate-data.bat
│   ├── start-splunk.bat
│   ├── stop-splunk.bat
│   └── update_course.bat
├── CLAUDE.md                                  # Documentation for Claude Code
├── COURSE_UPDATE_SUMMARY.md                   # Complete course update summary
├── LAB_UPDATE_GUIDE.md                        # Lab specifications
├── PRESENTATION_UPDATE_NOTES.md               # Presentation update guide
├── QUICK_REFERENCE.md                         # SPL command reference
├── QUICK_START.md                             # 5-step quick start guide
├── README.md                                  # This file
└── outline.md                                 # Complete 2-day course outline
```

## Prerequisites

### Software Requirements
- Docker Desktop (for Splunk container)
- Python 3.7+ (for data generation)
- Modern web browser (for Splunk UI and presentation)

### Knowledge Requirements
- Completion of Splunk Fundamentals 1 or equivalent
- Basic understanding of SPL (Search Processing Language)
- Familiarity with Splunk web interface
- Basic command line skills

## Buttercup Games Scenario

**Company**: Buttercup Games - E-commerce and retail gaming company

All labs use realistic data from Buttercup Games operations:

### index=web (~20,000 events)
- **Web Access Logs**: Online store activity with session tracking (JSESSIONID)
  - Product views, cart actions, purchases
  - Products: Mediocre Kingdoms, Grand Theft Scooter, Halo, FIFA, etc.
- **Vendor Sales**: Retail store sales across regions
  - VendorID ranges: 1000-2999 (USA), 3000-3999 (Canada), 5000-6999 (Europe)

### index=security (~2,000 events)
- **Linux Secure Logs**: Authentication events
  - Failed passwords, session tracking, invalid users

### index=network (~3,000 events)
- **Cisco WSA Squid**: Proxy logs with web usage patterns

### index=games (~2,000 events)
- **SimCube Beta**: Game telemetry with player actions and character data

### Lookup Tables
- **http_status_lookup.csv**: HTTP status codes with descriptions
- **product_catalog.csv**: Buttercup Games product information

## Environment Management

### Start Splunk
```bash
scripts\start-splunk.bat
```
Creates or starts Splunk container on port 8000

### Stop Splunk
```bash
scripts\stop-splunk.bat
```
Stops the Splunk container

### Clean Up
```bash
scripts\cleanup-splunk.bat
```
Removes container and image completely

### Generate Data
```bash
scripts\generate-data.bat
```
Creates all sample data files in the `data/` directory

## Troubleshooting

### Splunk Container Won't Start
- Ensure Docker Desktop is running
- Check port 8000 is not in use
- Try cleanup and restart: `cleanup-splunk.bat` then `start-splunk.bat`

### Data Generation Fails
- Ensure Python 3.7+ is installed
- Check Python is in system PATH
- Run directly: `python scripts/data-generators/generate_buttercup_data.py`

### No Search Results After Upload
- Check time range (try "All time")
- Verify file went to correct index
- Run verification search: `| tstats count where index=* by index, sourcetype`

### Presentation Not Loading
- Use a local web server (Python http.server or Node.js http-server)
- Don't just open the file directly if resources fail to load

## Lab Tips

1. **Complete labs in order** - Each builds on previous knowledge
2. **Take notes** - Document useful searches and techniques
3. **Experiment** - Try variations of the exercises
4. **Save searches** - Keep useful queries for reference
5. **Ask questions** - Discuss with instructor or peers

## Course Documentation

- **QUICK_START.md**: 5-step quick setup guide
- **labs/lab00_data_loading.md**: Detailed data upload instructions for 4 indexes
- **outline.md**: Complete 2-day course outline with all 12 labs
- **COURSE_UPDATE_SUMMARY.md**: Summary of course structure and content
- **LAB_UPDATE_GUIDE.md**: Lab specifications and structure
- **QUICK_REFERENCE.md**: SPL command reference

## Additional Resources

- [Splunk Documentation](https://docs.splunk.com/)
- [Splunk Community](https://community.splunk.com/)
- [Splunk Education](https://www.splunk.com/en_us/training.html)
- [Splunk Answers](https://community.splunk.com/t5/Splunk-Answers/bd-p/answers)

## Contributing

This is a training course repository. For updates or corrections:
1. Test changes thoroughly
2. Update relevant documentation
3. Ensure all labs still work
4. Update presentation if needed

## License

This course is provided for educational purposes. Splunk is a registered trademark of Splunk Inc.

## Support

For issues with course materials:
- Check the troubleshooting section above
- Review `labs/lab00_data_loading.md` for data upload help
- Ensure all 4 indexes are created (web, security, network, games)
- Verify data is uploaded correctly: `| tstats count where index=* by index, sourcetype`

---

## Verify Setup

After loading data, run this search to confirm all indexes have data:

```spl
| tstats count where index=* by index, sourcetype
| sort index sourcetype
```

**Expected Results**:

| index | sourcetype | count |
|-------|------------|-------|
| games | SimCubeBeta | ~2,000 |
| network | cisco_wsa_squid | ~3,000 |
| security | linux_secure | ~2,000 |
| web | access_combined_wcookie | ~15,000 |
| web | vendor_sales | ~5,000 |

---

**Ready to learn? Start with Lab 1!** 🎮