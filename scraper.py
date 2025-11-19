#!/usr/bin/env python3
"""
PC Parts Price Scraper for Maximum PC Builds Archive

This script scrapes current prices from PCPartPicker for all builds in the repository
and updates the markdown files with the latest pricing information.
"""

import os
import re
import sys
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

# Configure logging
log_level = logging.DEBUG if os.getenv('DEBUG') else logging.INFO
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PCPartPickerScraper:
    """Scraper for PCPartPicker build lists."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.delay = 2  # Delay between requests in seconds
    
    def extract_pcpartpicker_url(self, markdown_content: str) -> Optional[str]:
        """Extract the PCPartPicker list URL from markdown content."""
        match = re.search(r'\[PCPartPicker Part List\]\((https://ca\.pcpartpicker\.com/list/[a-zA-Z0-9]+)\)', markdown_content)
        if match:
            return match.group(1)
        return None
    
    def scrape_build_prices(self, url: str) -> Dict[str, Tuple[str, str]]:
        """
        Scrape prices from a PCPartPicker build list.
        
        Returns a dict mapping product names to (price, retailer) tuples.
        """
        try:
            logger.info(f"Scraping prices from: {url}")
            time.sleep(self.delay)  # Be respectful to the server
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # PCPartPicker uses a table structure for parts list
            prices = {}
            
            # Try multiple strategies to find the parts list
            parts_table = None
            
            # Strategy 1: Look for table with specific classes
            parts_table = soup.find('table', class_='pcpp-partlist__table')
            
            # Strategy 2: Look for table by ID
            if not parts_table:
                parts_table = soup.find('table', {'id': 'partlist'})
            
            # Strategy 3: Look for any table containing part information
            if not parts_table:
                all_tables = soup.find_all('table')
                for table in all_tables:
                    # Check if this table has the expected structure
                    if table.find('td', class_=lambda x: x and 'td__' in str(x)):
                        parts_table = table
                        logger.debug("Found parts table using fallback method")
                        break
            
            # Strategy 4: Look for tbody directly (sometimes table is implicit)
            if not parts_table:
                tbody = soup.find('tbody')
                if tbody and tbody.find('tr'):
                    # Check if tbody has the right structure
                    if tbody.find('td', class_=lambda x: x and 'td__' in str(x)):
                        # Create a pseudo-table element
                        parts_table = tbody
                        logger.debug("Found parts list in tbody")
            
            if not parts_table:
                logger.warning(f"Could not find parts table on {url}")
                logger.debug(f"Page has {len(soup.find_all('table'))} tables, {len(soup.find_all('tbody'))} tbody elements")
                # Save HTML for debugging if in debug mode
                if logger.level <= logging.DEBUG:
                    debug_file = f"/tmp/pcpartpicker_debug_{url.split('/')[-1]}.html"
                    with open(debug_file, 'w') as f:
                        f.write(soup.prettify())
                    logger.debug(f"Saved HTML to {debug_file} for inspection")
                return prices
            
            rows = parts_table.find_all('tr')
            logger.debug(f"Found {len(rows)} rows in parts table")
            
            for row in rows:
                # Try to find component column with multiple strategies
                # PCPartPicker uses versioned classes like td__component-2025
                component_td = row.find('td', class_=lambda x: x and any(
                    cls.startswith('td__component') for cls in (x if isinstance(x, list) else [x])
                ))
                
                if not component_td:
                    continue
                
                # Extract product name - try multiple approaches
                # Look for td__name or td__name-2025
                name_td = row.find('td', class_=lambda x: x and any(
                    cls.startswith('td__name') for cls in (x if isinstance(x, list) else [x])
                ))
                
                if not name_td:
                    continue
                
                product_link = name_td.find('a', href=lambda x: x and '/product/' in str(x))
                
                if not product_link:
                    continue
                
                product_name = product_link.get_text(strip=True)
                
                # Extract price - look for td__price or td__price-2025
                price_td = row.find('td', class_=lambda x: x and any(
                    cls.startswith('td__price') for cls in (x if isinstance(x, list) else [x])
                ))
                
                if not price_td:
                    continue
                
                # Price is in a link with class pp_async_mr
                price_link = price_td.find('a', class_='pp_async_mr')
                if price_link:
                    price_text = price_link.get_text(strip=True)
                    retailer_href = price_link.get('href', '')
                else:
                    # Fallback to getting all text from the cell
                    price_text = price_td.get_text(strip=True)
                    retailer_href = ''
                
                # Extract retailer - check td__where column for better info
                retailer = 'Unknown'
                where_td = row.find('td', class_='td__where')
                if where_td:
                    where_link = where_td.find('a')
                    if where_link:
                        retailer_href = where_link.get('href', '')
                        # Get alt text from image if available
                        img = where_link.find('img')
                        if img and img.get('alt'):
                            retailer = img.get('alt')
                
                # If we didn't get retailer from td__where, try from price link
                if retailer == 'Unknown' and retailer_href:
                    # Properly parse URL to extract domain for security
                    try:
                        parsed_url = urlparse(retailer_href)
                        domain = parsed_url.netloc.lower()
                        
                        # Whitelist of known trusted retailer domains
                        # This is for display purposes only, not security-sensitive
                        trusted_retailers = {
                            'www.amazon.ca': 'Amazon Canada',
                            'amazon.ca': 'Amazon Canada',
                            'www.amazon.com': 'Amazon Canada',
                            'amazon.com': 'Amazon Canada',
                            'www.newegg.ca': 'Newegg Canada',
                            'newegg.ca': 'Newegg Canada',
                            'www.newegg.com': 'Newegg Canada',
                            'newegg.com': 'Newegg Canada',
                            'www.bestbuy.ca': 'Best Buy Canada',
                            'bestbuy.ca': 'Best Buy Canada',
                            'www.bestbuy.com': 'Best Buy Canada',
                            'bestbuy.com': 'Best Buy Canada',
                            'www.vuugo.com': 'Vuugo',
                            'vuugo.com': 'Vuugo',
                            'www.canadacomputers.com': 'Canada Computers',
                            'canadacomputers.com': 'Canada Computers',
                        }
                        
                        retailer = trusted_retailers.get(domain, 'Unknown')
                    except Exception:
                        pass
                
                # Clean up price text (remove "Add", "From", etc.)
                price_match = re.search(r'\$[\d,]+\.?\d*', price_text)
                if price_match:
                    price = price_match.group(0)
                else:
                    price = '-'
                
                if product_name:
                    prices[product_name] = (price, retailer)
                    logger.debug(f"Found: {product_name} - {price} @ {retailer}")
            
            logger.info(f"Scraped {len(prices)} prices from {url}")
            return prices
            
        except requests.RequestException as e:
            logger.error(f"Failed to scrape {url}: {e}")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {e}")
            return {}
    
    def update_markdown_file(self, filepath: Path, prices: Dict[str, Tuple[str, str]]) -> bool:
        """
        Update a markdown file with new prices.
        
        Returns True if the file was modified, False otherwise.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            lines = content.split('\n')
            modified = False
            
            for i, line in enumerate(lines):
                # Skip non-table rows
                if not line.startswith('|') or '**Type**' in line or 'Price' in line and 'Print Price' in line:
                    continue
                
                # Parse table row
                parts = [p.strip() for p in line.split('|')]
                if len(parts) < 5:
                    continue
                
                # Extract product name from markdown link
                item_cell = parts[2]
                match = re.search(r'\[([^\]]+)\]', item_cell)
                if not match:
                    continue
                
                product_name = match.group(1)
                
                # Check if we have updated price for this product
                if product_name in prices:
                    price, retailer = prices[product_name]
                    
                    # Update the price cell (parts[3])
                    if price != '-':
                        new_price_cell = f' {price} @ {retailer} '
                    else:
                        new_price_cell = ' - '
                    
                    # Only update if different
                    if parts[3] != new_price_cell:
                        parts[3] = new_price_cell
                        lines[i] = '|'.join(parts)
                        modified = True
                        logger.debug(f"Updated {product_name}: {new_price_cell}")
            
            if modified:
                new_content = '\n'.join(lines)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                logger.info(f"Updated {filepath}")
                return True
            else:
                logger.debug(f"No changes needed for {filepath}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to update {filepath}: {e}")
            return False


def find_build_markdown_files(root_dir: Path) -> List[Path]:
    """Find all markdown files containing PC builds."""
    markdown_files = []
    
    # Look in year directories (2018, 2020, 2021, etc.)
    for year_dir in root_dir.glob('20*'):
        if year_dir.is_dir():
            for md_file in year_dir.rglob('*.md'):
                markdown_files.append(md_file)
    
    return sorted(markdown_files)


def main():
    """Main function to scrape prices and update markdown files."""
    repo_root = Path(__file__).parent
    
    logger.info("Starting PC Parts Price Scraper")
    logger.info(f"Repository root: {repo_root}")
    
    # Find all markdown files
    markdown_files = find_build_markdown_files(repo_root)
    logger.info(f"Found {len(markdown_files)} markdown files to process")
    
    if not markdown_files:
        logger.error("No markdown files found!")
        return 1
    
    scraper = PCPartPickerScraper()
    files_updated = 0
    files_failed = 0
    
    for md_file in markdown_files:
        try:
            logger.info(f"\nProcessing: {md_file.relative_to(repo_root)}")
            
            # Read markdown file
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract PCPartPicker URL
            pcpp_url = scraper.extract_pcpartpicker_url(content)
            if not pcpp_url:
                logger.warning(f"No PCPartPicker URL found in {md_file.name}")
                continue
            
            # Scrape prices
            prices = scraper.scrape_build_prices(pcpp_url)
            if not prices:
                logger.warning(f"No prices scraped for {md_file.name}")
                files_failed += 1
                continue
            
            # Update markdown file
            if scraper.update_markdown_file(md_file, prices):
                files_updated += 1
            
        except Exception as e:
            logger.error(f"Failed to process {md_file}: {e}")
            files_failed += 1
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Price scraping complete!")
    logger.info(f"Files updated: {files_updated}")
    logger.info(f"Files failed: {files_failed}")
    logger.info(f"Total files processed: {len(markdown_files)}")
    logger.info(f"{'='*60}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
