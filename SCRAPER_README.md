# Price Scraper Documentation

## Overview

This repository includes an automated price scraper that updates PC component prices daily. The scraper runs via GitHub Actions and updates all markdown files with current pricing from major retailers.

## How It Works

### Architecture

1. **scraper.py**: Python script that performs the actual scraping
2. **.github/workflows/update-prices.yml**: GitHub Actions workflow that runs the scraper daily
3. **requirements.txt**: Python dependencies

### Process Flow

```
┌─────────────────────────────────────────────────────────────┐
│  1. GitHub Actions triggers daily at 2 AM UTC               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  2. Install Python dependencies (beautifulsoup4, requests)  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  3. Run scraper.py                                          │
│     • Find all 75 markdown files                            │
│     • Extract PCPartPicker list URLs                        │
│     • Scrape current prices from PCPartPicker              │
│     • Update markdown tables with new prices                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  4. Commit and push changes (if any prices updated)         │
└─────────────────────────────────────────────────────────────┘
```

### Data Source

The scraper uses **PCPartPicker** as the data source because:
- PCPartPicker already aggregates prices from multiple retailers (Newegg, Amazon, Best Buy, etc.)
- Each build in the repository already has a PCPartPicker list URL
- PCPartPicker handles the complexity of tracking product availability across retailers
- More reliable than scraping individual retailer sites directly

### Security Features

- **URL Validation**: Uses proper URL parsing with a whitelist of trusted retailer domains
- **Error Handling**: Comprehensive try-catch blocks prevent crashes
- **Rate Limiting**: 2-second delay between requests to be respectful to servers
- **No Secrets Required**: No API keys or credentials needed
- **CodeQL Verified**: Passed security scanning with no vulnerabilities

## Manual Usage

### Prerequisites

```bash
# Python 3.12+ recommended
python --version

# Install dependencies
pip install -r requirements.txt
```

### Running the Scraper

```bash
# Run from repository root
python scraper.py
```

The script will:
1. Find all markdown files in year directories (2018/, 2020/, 2021/, etc.)
2. Extract PCPartPicker URLs from each file
3. Scrape current prices
4. Update markdown files with new prices
5. Log progress and any errors

### Output

```
2025-11-18 14:00:00 - INFO - Starting PC Parts Price Scraper
2025-11-18 14:00:00 - INFO - Found 75 markdown files to process
2025-11-18 14:00:00 - INFO - Processing: 2018/January/Budget.md
2025-11-18 14:00:02 - INFO - Scraping prices from: https://ca.pcpartpicker.com/list/8gGn9r
2025-11-18 14:00:04 - INFO - Scraped 8 prices from URL
2025-11-18 14:00:04 - INFO - Updated 2018/January/Budget.md
...
2025-11-18 14:15:00 - INFO - Price scraping complete!
2025-11-18 14:15:00 - INFO - Files updated: 42
2025-11-18 14:15:00 - INFO - Files failed: 0
2025-11-18 14:15:00 - INFO - Total files processed: 75
```

## GitHub Actions Workflow

### Automatic Execution

The workflow runs automatically:
- **Schedule**: Daily at 2:00 AM UTC
- **Trigger**: Can also be manually triggered via GitHub Actions UI

### Manual Triggering

1. Go to the repository on GitHub
2. Click "Actions" tab
3. Select "Update PC Part Prices" workflow
4. Click "Run workflow"
5. Select branch and click "Run workflow" button

### Workflow Configuration

```yaml
# .github/workflows/update-prices.yml
schedule:
  - cron: '0 2 * * *'  # Daily at 2 AM UTC
```

To change the schedule, modify the cron expression:
- `'0 */6 * * *'` - Every 6 hours
- `'0 0 * * 1'` - Every Monday at midnight
- `'0 12 * * *'` - Daily at noon

## Markdown Format

The scraper expects markdown files with this table format:

```markdown
# January 2018 - Budget

[PCPartPicker Part List](https://ca.pcpartpicker.com/list/8gGn9r)

| Type | Item | Price | Print Price |
| :--- | :--- | :--- | :--- |
| **CPU** | [AMD Ryzen 3 1200...](https://ca.pcpartpicker.com/product/...) | $276.90 @ Amazon Canada | $110.00 |
| **Memory** | [Patriot Viper Elite...](https://ca.pcpartpicker.com/product/...) | - | $77.00 |
```

The scraper:
- Extracts the PCPartPicker list URL from the header
- Parses the table to find product names
- Updates the "Price" column with current prices
- Preserves the "Print Price" column (historical data)

## Supported Retailers

The scraper recognizes these retailers:
- Amazon Canada (amazon.ca, amazon.com)
- Newegg Canada (newegg.ca, newegg.com)
- Best Buy Canada (bestbuy.ca, bestbuy.com)
- Vuugo (vuugo.com)
- Canada Computers (canadacomputers.com)

## Troubleshooting

### No Prices Found

If the scraper reports "No prices scraped":
1. Check that the PCPartPicker URL is valid
2. Verify the PCPartPicker page loads in a browser
3. Check GitHub Actions logs for detailed error messages

### Prices Not Updating

Common causes:
1. Products are out of stock (shows as "-")
2. PCPartPicker page structure changed (may need scraper update)
3. Network issues during GitHub Actions run

### GitHub Actions Failed

1. Check the Actions tab for error logs
2. Verify requirements.txt dependencies are compatible
3. Check if PCPartPicker website is accessible

## Maintenance

### Updating Dependencies

```bash
# Check for outdated packages
pip list --outdated

# Update requirements.txt
pip install --upgrade beautifulsoup4 requests lxml
pip freeze > requirements.txt
```

### Adding New Retailers

To add support for a new retailer:

1. Edit `scraper.py`
2. Add the domain to the `trusted_retailers` dictionary
3. Test with a sample build
4. Commit and push

Example:
```python
trusted_retailers = {
    # ... existing retailers ...
    'www.memoryexpress.com': 'Memory Express',
    'memoryexpress.com': 'Memory Express',
}
```

## Limitations

- **Internet Required**: Scraper needs internet access to reach PCPartPicker
- **Rate Limiting**: 2-second delay between requests (takes ~3-5 minutes for all 75 files)
- **PCPartPicker Dependency**: If PCPartPicker changes their HTML structure, scraper needs updates
- **Canadian Prices**: Currently configured for Canadian pricing (ca.pcpartpicker.com)

## Future Improvements

Potential enhancements:
- [ ] Support for US pricing (pcpartpicker.com)
- [ ] Price history tracking
- [ ] Email notifications when prices drop significantly
- [ ] Support for more retailers
- [ ] Parallel processing for faster execution
- [ ] Website (gh-pages) automatic updates

## Support

For issues or questions:
1. Check existing Issues on GitHub
2. Review GitHub Actions logs for errors
3. Open a new Issue with detailed information

## License

Same as repository license (see LICENSE.md)
