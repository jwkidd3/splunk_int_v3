# Splunk Intermediate Training Course v3

A comprehensive 2-day intermediate-level Splunk training program covering advanced search techniques, data modeling, dashboards, and alerts.

## Course Overview

This repository contains all materials needed to deliver or take a 2-day Splunk intermediate training course, including:
- 9 hands-on lab exercises
- Interactive reveal.js presentation
- Sample data generation scripts
- Dockerized Splunk environment
- Complete course outline and documentation

### Target Audience
- Splunk users with basic SPL knowledge
- Those who have completed Splunk Fundamentals 1
- IT professionals wanting to advance their Splunk skills

### What You'll Learn
- Advanced SPL commands (subsearches, transaction, multisearch)
- Statistical analysis and transformations
- Field extraction techniques
- Data enrichment with lookups
- Report and dashboard creation
- Alert configuration and management
- Data models and Pivot interface
- Advanced dashboard customization with Simple XML

## Quick Start

### 1. Start Splunk Environment

```bash
# Windows
scripts\start-splunk.bat

# After container starts, access Splunk at:
# http://localhost:8000
# Username: admin
# Password: password
```

### 2. Generate Sample Data

```bash
# Windows
scripts\generate-data.bat

# Or directly with Python
python scripts/data-generators/generate_sample_data.py
```

### 3. Upload Data to Splunk

1. Log in to Splunk (http://localhost:8000)
2. Create a new index called `training`
3. Upload data files from the `data/` directory
4. Set sourcetype appropriately:
   - `web_access.log` → sourcetype: `web_access`
   - `application.log` → sourcetype: `application`
   - `security_events.log` → sourcetype: `security_events`

### 4. View Presentation

```bash
cd presentation
python -m http.server 8080

# Open browser to http://localhost:8080
```

## Course Structure

### Day 1: Advanced Searching and Data Analysis

#### Module 1: Advanced Search Commands (1 hour)
- Subsearches and their use cases
- Transaction command for event grouping
- Multisearch for combining searches
- **Lab 1**: Advanced Search Commands (30 minutes)

#### Module 2: Statistical Commands and Transformations (1.5 hours)
- Stats, chart, and timechart commands
- Eval expressions and functions
- Statistical functions and aggregations
- **Lab 2**: Statistical Commands and Transformations (45 minutes)

#### Module 3: Working with Fields and Field Extractions (1.5 hours)
- Understanding field extractions
- Rex command for inline extraction
- Creating custom field extractions
- Calculated fields and aliases
- **Lab 3**: Working with Fields and Field Extractions (45 minutes)

#### Module 4: Lookups and Data Enrichment (1.5 hours)
- Creating and managing CSV lookups
- Automatic lookups
- KV Store lookups
- Data enrichment strategies
- **Lab 4**: Lookups and Data Enrichment (45 minutes)

### Day 2: Reports, Dashboards, and Alerts

#### Module 5: Creating Reports and Visualizations (1.5 hours)
- Building effective reports
- Visualization types and best practices
- Formatting and customizing reports
- Scheduling reports
- **Lab 5**: Creating Reports and Visualizations (45 minutes)

#### Module 6: Building Interactive Dashboards (1.5 hours)
- Dashboard editor overview
- Adding panels and visualizations
- Dashboard inputs and tokens
- Drilldowns and navigation
- **Lab 6**: Building Interactive Dashboards (45 minutes)

#### Module 7: Alerts and Scheduled Searches (1 hour)
- Creating real-time and scheduled alerts
- Alert actions and triggers
- Throttling and alert management
- **Lab 7**: Alerts and Scheduled Searches (30 minutes)

#### Module 8: Data Models and Pivot (1.5 hours)
- Understanding data models
- Creating data models
- Using the Pivot interface
- Accelerating data models
- **Lab 8**: Data Models and Pivot (45 minutes)

#### Module 9: Advanced Dashboard Techniques (1.5 hours)
- Simple XML customization
- Base searches for performance
- Form-based dashboards
- Advanced token manipulation
- **Lab 9**: Advanced Dashboard Techniques (45 minutes)

## Repository Structure

```
splunk_int_v3/
├── data/                           # Generated sample data files
│   ├── web_access.log
│   ├── application.log
│   ├── security_events.log
│   ├── products.csv
│   ├── users.csv
│   └── threat_intel.csv
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
├── README.md                       # This file
└── CLAUDE.md                       # Documentation for Claude Code
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

## Sample Data

The data generation script creates realistic training data:

### Web Access Logs (10,000 events)
- HTTP requests with methods, URLs, status codes
- Response times and bytes transferred
- User and IP information

### Application Logs (5,000 events)
- JSON-formatted application events
- Multiple components (AuthService, PaymentService, etc.)
- Error levels and session tracking

### Security Events (1,000 events)
- Login attempts (success/failure)
- Unauthorized access attempts
- Geographic and department information

### Lookup Tables
- **users.csv**: User information (department, city, role)
- **products.csv**: Product catalog with pricing
- **threat_intel.csv**: Threat intelligence data

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
- Run directly: `python scripts/data-generators/generate_sample_data.py`

### Presentation Not Loading
- Use a local web server (Python http.server or Node.js http-server)
- Don't just open the file directly if resources fail to load

## Lab Tips

1. **Complete labs in order** - Each builds on previous knowledge
2. **Take notes** - Document useful searches and techniques
3. **Experiment** - Try variations of the exercises
4. **Save searches** - Keep useful queries for reference
5. **Ask questions** - Discuss with instructor or peers

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
- Check the troubleshooting section
- Review lab prerequisites
- Ensure Splunk environment is running
- Verify sample data is uploaded correctly

---

**Ready to learn? Start with Module 1!**