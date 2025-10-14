# Splunk Intermediate Course - Presentation

This directory contains the reveal.js presentation for the 2-day Splunk Intermediate course.

## Viewing the Presentation

### Option 1: Open in Browser (Simple)

Simply open `index.html` in any modern web browser:

```bash
open index.html
```

Or navigate to the file and double-click it.

### Option 2: Serve with Python (Recommended)

For full functionality and proper loading of all resources:

```bash
# Python 3
python -m http.server 8080

# Then open browser to:
# http://localhost:8080
```

### Option 3: Serve with Node.js

```bash
npx http-server -p 8080

# Then open browser to:
# http://localhost:8080
```

## Navigation

- **Arrow keys**: Navigate slides
- **Space**: Next slide
- **Shift + Space**: Previous slide
- **ESC**: Overview mode
- **F**: Fullscreen
- **S**: Speaker notes (if enabled)

## Presentation Structure

### Day 1
1. **Module 1**: Advanced Search Commands (subsearches, transaction, multisearch)
2. **Module 2**: Statistical Commands & Transformations (stats, chart, timechart, eval)
3. **Module 3**: Fields & Field Extractions (rex, calculated fields, field aliases)
4. **Module 4**: Lookups & Data Enrichment (CSV lookups, automatic lookups, KV Store)

### Day 2
5. **Module 5**: Reports & Visualizations (visualization types, scheduling)
6. **Module 6**: Interactive Dashboards (inputs, tokens, drilldowns)
7. **Module 7**: Alerts & Scheduled Searches (scheduled/real-time alerts, throttling)
8. **Module 8**: Data Models & Pivot (data model creation, acceleration, tstats)
9. **Module 9**: Advanced Dashboard Techniques (Simple XML, base searches, forms)

## Customization

### Changing Theme

Edit line 9 in `index.html`:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/theme/black.css">
```

Available themes: black, white, league, beige, sky, night, serif, simple, solarized

### Adding Custom Styles

Custom CSS is included in the `<style>` section of the HTML file. Modify as needed.

## Dependencies

All dependencies are loaded from CDN:
- reveal.js 4.5.0
- highlight.js (for code syntax highlighting)

No local installation required!

## Printing to PDF

1. Open the presentation in Chrome/Chromium
2. Add `?print-pdf` to the URL: `index.html?print-pdf`
3. Open print dialog (Ctrl/Cmd + P)
4. Set destination to "Save as PDF"
5. Print

## License

This presentation is part of the Splunk Intermediate training course materials.
