# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Splunk training course repository (splunk_int_v3) designed to provide a comprehensive 2-day intermediate-level Splunk training program. The repository includes:
- Dockerized Splunk environment for hands-on labs
- 9 detailed lab exercises in Markdown format
- Sample data generation scripts
- reveal.js presentation for instructor delivery
- Complete course outline and materials

## Repository Structure

```
splunk_int_v3/
├── data/                           # Generated sample data files
├── labs/                           # Lab exercises (Markdown)
│   ├── lab01_advanced_search_commands.md
│   ├── lab02_statistical_commands.md
│   ├── lab03_field_extractions.md
│   ├── lab04_lookups_data_enrichment.md
│   ├── lab05_reports_visualizations.md
│   ├── lab06_interactive_dashboards.md
│   ├── lab07_alerts_scheduled_searches.md
│   ├── lab08_data_models_pivot.md
│   └── lab09_advanced_dashboard_techniques.md
├── presentation/                   # reveal.js presentation
│   ├── index.html
│   └── README.md
├── scripts/                        # Utility scripts
│   ├── data-generators/
│   │   └── generate_sample_data.py
│   ├── cleanup-splunk.bat
│   ├── generate-data.bat
│   ├── start-splunk.bat
│   ├── stop-splunk.bat
│   └── update_course.bat
├── outline.md                      # Course outline
├── README.md                       # Main documentation
└── CLAUDE.md                       # This file
```

## Course Overview

### Day 1: Advanced Searching and Data Analysis
1. **Module 1**: Advanced Search Commands (subsearches, transaction, multisearch)
2. **Module 2**: Statistical Commands & Transformations (stats, chart, timechart, eval)
3. **Module 3**: Fields & Field Extractions (rex, calculated fields, field aliases)
4. **Module 4**: Lookups & Data Enrichment (CSV lookups, automatic lookups)

### Day 2: Reports, Dashboards, and Alerts
5. **Module 5**: Reports & Visualizations (charts, scheduling, formatting)
6. **Module 6**: Interactive Dashboards (inputs, tokens, drilldowns)
7. **Module 7**: Alerts & Scheduled Searches (scheduled/real-time alerts, throttling)
8. **Module 8**: Data Models & Pivot (data model creation, acceleration, tstats)
9. **Module 9**: Advanced Dashboard Techniques (Simple XML, base searches, forms)

## Environment Management

### Starting Splunk
```bash
scripts/start-splunk.bat
```
- Attempts to start existing `splunk` container
- If container doesn't exist, creates new one with:
  - Port: 8000 (mapped to localhost:8000)
  - Username: admin
  - Password: password
  - Image: splunk/splunk:latest (linux/amd64)
  - License: Automatically accepts Splunk terms

### Stopping Splunk
```bash
scripts/stop-splunk.bat
```
- Stops the running Splunk container without removing it

### Cleaning Up
```bash
scripts/cleanup-splunk.bat
```
- Removes the Splunk container forcefully
- Removes the splunk/splunk:latest image
- Use this to completely reset the environment

### Generating Sample Data
```bash
scripts/generate-data.bat
```
- Runs Python script to generate training data
- Creates web access logs, application logs, security events
- Generates lookup CSV files (users, products, threat intelligence)
- Data is stored in the `data/` directory

### Updating Course Materials
```bash
scripts/update_course.bat
```
- Pulls latest changes from git repository
- Designed for Windows environment (references C:\Users\Administrator\Desktop\splunk_int_v3)

## Data Generation

The `scripts/data-generators/generate_sample_data.py` script creates:
- **web_access.log**: 10,000 web server access logs
- **application.log**: 5,000 application logs (JSON format)
- **security_events.log**: 1,000 security events
- **products.csv**: Product lookup table
- **users.csv**: User information lookup table
- **threat_intel.csv**: Threat intelligence lookup table

Run with: `python scripts/data-generators/generate_sample_data.py`

## Presentation

The reveal.js presentation is located in `presentation/index.html`

To view:
```bash
cd presentation
python -m http.server 8080
# Open browser to http://localhost:8080
```

Or simply open `presentation/index.html` in a browser.

## Lab Structure

Each lab includes:
- Learning objectives
- Step-by-step exercises
- Sample SPL queries
- Questions and challenges
- Key takeaways
- Duration estimates

Labs are designed to be completed in sequence, building on previous knowledge.

## Architecture Notes

- **Platform**: Windows-based scripts (.bat files) designed for Windows training environments
- **Docker Setup**: Single-container Splunk deployment with persistent naming ("splunk")
- **Access**: Splunk Web UI accessible at http://localhost:8000 after container start
- **Credentials**: Hardcoded for training purposes (admin/password)
- **Data Format**: Labs use the `training` index
- **Course Duration**: 2 days (approximately 12-14 hours of instruction + labs)

## Prerequisites for Students

- Completion of Splunk Fundamentals 1 or equivalent experience
- Basic understanding of SPL (Search Processing Language)
- Familiarity with Splunk web interface

## Instructor Notes

- Each module includes a lab exercise
- Presentation slides align with lab content
- Sample data must be generated before labs
- Students should have access to Splunk instance (localhost or shared)
- Estimated time per module: 1-1.5 hours (lecture + lab)

## Development Context

This is a complete intermediate Splunk training course with all materials ready for delivery. The course covers advanced SPL, data modeling, dashboards, alerts, and performance optimization.
