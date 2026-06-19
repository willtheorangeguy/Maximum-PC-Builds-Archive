#!/usr/bin/env python3
"""
PC Parts Price Scraper for the Maximum PC Builds Archive website (gh-pages).

The website stores each month's builds as HTML tables in `<year>/<month>/index.html`.
Every build table is followed by a "View On" link to its PCPartPicker saved list
(`pcpartpicker.com/user/<handle>/saved/<id>`). This script scrapes the current
prices from each saved list and updates the matching price cells in place.

Parts are matched by PCPartPicker product ID (parsed from the item-cell link),
which is exact and robust, so no fuzzy name matching is required.

This is the HTML counterpart of the Markdown `scraper.py` on the `main` branch:
same cloudscraper session and 429 backoff, different input/output format.
"""

import os
import re
import sys
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin

import cloudscraper
import requests
from bs4 import BeautifulSoup

# Configure logging
log_level = logging.DEBUG if os.getenv('DEBUG') else logging.INFO
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# A build = one HTML table immediately followed by its "View On" saved-list link.
SAVED_URL_RE = re.compile(
    r'https?://(?:[a-z]+\.)?pcpartpicker\.com/user/[A-Za-z0-9_]+/saved/[A-Za-z0-9]+'
)
TABLE_RE = re.compile(r'<table class="pcpp-part-list">.*?</table>', re.DOTALL)
ROW_RE = re.compile(r'<tr\b.*?</tr>', re.DOTALL)
PRODUCT_ID_RE = re.compile(r'/product/([A-Za-z0-9]+)')


class PCPartPickerHTMLScraper:
    """Scrapes PCPartPicker saved lists and updates the website's HTML tables."""

    def __init__(self):
        # cloudscraper solves Cloudflare's JS challenge, which plain requests
        # cannot (PCPartPicker returns HTTP 403 to non-browser clients).
        self.session = cloudscraper.create_scraper()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/120.0.0.0 Safari/537.36'
        })
        self.delay = 2  # Delay between requests in seconds
        self.max_retries = 4  # Retries on HTTP 429 (rate limit)
        self.backoff_base = 30  # Seconds; doubles each retry (30, 60, 120, 240)

    def scrape_saved_list(self, url: str) -> Dict[str, Tuple[str, str]]:
        """
        Scrape a PCPartPicker saved list.

        Returns a dict mapping product ID -> (price, retailer). Products without
        an available price are omitted so they never clobber existing values.
        """
        try:
            logger.info(f"Scraping prices from: {url}")
            time.sleep(self.delay)  # Be respectful to the server

            # PCPartPicker rate-limits (HTTP 429) across a long bulk run.
            # Back off exponentially and retry rather than dropping the build.
            response = None
            for attempt in range(self.max_retries + 1):
                response = self.session.get(url, timeout=30)
                if response.status_code != 429:
                    break
                if attempt == self.max_retries:
                    logger.error(
                        f"Rate limited (429) on {url} after {self.max_retries} "
                        f"retries; giving up"
                    )
                    return {}
                wait = self.backoff_base * (2 ** attempt)
                retry_after = response.headers.get('Retry-After')
                if retry_after and retry_after.isdigit():
                    wait = max(wait, int(retry_after))
                logger.warning(
                    f"Rate limited (429) on {url}; backing off {wait}s "
                    f"(attempt {attempt + 1}/{self.max_retries})"
                )
                time.sleep(wait)

            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')

            prices: Dict[str, Tuple[str, str]] = {}
            for row in soup.find_all('tr'):
                # PCPartPicker uses versioned classes like td__component-2025
                name_td = row.find('td', class_=lambda x: x and any(
                    cls.startswith('td__name') for cls in (x if isinstance(x, list) else [x])
                ))
                if not name_td:
                    continue

                product_link = name_td.find('a', href=lambda h: h and '/product/' in str(h))
                if not product_link:
                    continue

                id_match = PRODUCT_ID_RE.search(product_link.get('href', ''))
                if not id_match:
                    continue
                product_id = id_match.group(1)

                price_td = row.find('td', class_=lambda x: x and any(
                    cls.startswith('td__price') for cls in (x if isinstance(x, list) else [x])
                ))
                if not price_td:
                    continue

                price_link = price_td.find('a', class_='pp_async_mr')
                price_text = price_link.get_text(strip=True) if price_link else price_td.get_text(strip=True)

                price_match = re.search(r'\$[\d,]+\.?\d*', price_text)
                if not price_match:
                    continue  # No price available; leave the existing cell alone
                price = price_match.group(0)

                # Retailer from the td__where logo alt text
                retailer = 'Unknown'
                where_td = row.find('td', class_='td__where')
                if where_td:
                    img = where_td.find('img')
                    if img and img.get('alt'):
                        retailer = img.get('alt')

                prices[product_id] = (price, retailer)
                logger.debug(f"Found: {product_id} - {price} @ {retailer}")

            logger.info(f"Scraped {len(prices)} priced parts from {url}")
            return prices

        except requests.RequestException as e:
            status = getattr(getattr(e, 'response', None), 'status_code', None)
            if status == 403:
                logger.error(
                    f"Failed to scrape {url}: HTTP 403 (Cloudflare block) - "
                    f"cloudscraper could not pass the challenge"
                )
            elif status is not None:
                logger.error(f"Failed to scrape {url}: HTTP {status} - {e}")
            else:
                logger.error(f"Failed to scrape {url}: {e}")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {e}")
            return {}

    def _update_table(self, table_html: str, prices: Dict[str, Tuple[str, str]]) -> str:
        """Return the table HTML with its first price cell per row refreshed."""

        def update_row(row_match: re.Match) -> str:
            row = row_match.group(0)

            # Product ID lives in the item-cell link
            item_match = re.search(
                r'pcpp-part-list-item">\s*<a href="([^"]+)"', row
            )
            if not item_match:
                return row
            item_href = item_match.group(1)
            id_match = PRODUCT_ID_RE.search(item_href)
            if not id_match:
                return row
            product_id = id_match.group(1)

            if product_id not in prices:
                return row
            price, retailer = prices[product_id]

            # Replace only the FIRST price cell (the live price; the other two
            # are Print Price / "Street" Price and must stay untouched).
            new_inner = f'\n        <a href="{item_href}">{price} @ {retailer}</a>\n      '
            new_cell = f'<td class="pcpp-part-list-price">{new_inner}</td>'
            updated, n = re.subn(
                r'<td class="pcpp-part-list-price">.*?</td>',
                lambda _m: new_cell,
                row,
                count=1,
                flags=re.DOTALL,
            )
            return updated if n else row

        return ROW_RE.sub(update_row, table_html)

    def update_html_file(self, filepath: Path) -> bool:
        """Update every build table in an HTML file. Returns True if changed."""
        try:
            content = filepath.read_text(encoding='utf-8')
        except Exception as e:
            logger.error(f"Failed to read {filepath}: {e}")
            return False

        tables = list(TABLE_RE.finditer(content))
        if not tables:
            logger.warning(f"No build tables found in {filepath}")
            return False

        # Pair each table with the first saved-list URL that follows it.
        new_content = content
        offset = 0  # track length change as we splice updated tables back in
        modified = False

        for table_match in tables:
            table_html = table_match.group(0)
            saved_match = SAVED_URL_RE.search(content, table_match.end())
            if not saved_match:
                logger.warning(
                    f"No saved-list link after a table in {filepath.name}; skipping"
                )
                continue
            saved_url = saved_match.group(0)

            prices = self.scrape_saved_list(saved_url)
            if not prices:
                logger.warning(f"No prices scraped for {saved_url}")
                continue

            updated_table = self._update_table(table_html, prices)
            if updated_table != table_html:
                start = table_match.start() + offset
                end = table_match.end() + offset
                new_content = new_content[:start] + updated_table + new_content[end:]
                offset += len(updated_table) - len(table_html)
                modified = True

        if modified:
            filepath.write_text(new_content, encoding='utf-8')
            logger.info(f"Updated {filepath}")
            return True

        logger.debug(f"No changes needed for {filepath}")
        return False


def find_build_html_files(root_dir: Path) -> List[Path]:
    """Find all `<year>/<month>/index.html` build pages."""
    html_files = []
    for year_dir in root_dir.glob('20*'):
        if year_dir.is_dir():
            for html_file in year_dir.rglob('index.html'):
                html_files.append(html_file)
    return sorted(html_files)


def main() -> int:
    repo_root = Path(__file__).parent

    logger.info("Starting PC Parts Price Scraper (HTML / website)")
    logger.info(f"Repository root: {repo_root}")

    html_files = find_build_html_files(repo_root)
    logger.info(f"Found {len(html_files)} build pages to process")

    if not html_files:
        logger.error("No build HTML files found!")
        return 1

    scraper = PCPartPickerHTMLScraper()
    files_updated = 0

    for html_file in html_files:
        logger.info(f"\nProcessing: {html_file.relative_to(repo_root)}")
        if scraper.update_html_file(html_file):
            files_updated += 1

    logger.info(f"\n{'=' * 60}")
    logger.info("Price scraping complete!")
    logger.info(f"Files updated: {files_updated}")
    logger.info(f"Total files processed: {len(html_files)}")
    logger.info(f"{'=' * 60}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
