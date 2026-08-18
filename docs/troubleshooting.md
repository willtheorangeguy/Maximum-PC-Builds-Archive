# Maximum PC Builds Archive — Troubleshooting

## Current prices look stale

Check whether the daily job is still running:

1. Open the Actions tab and look at **Update PC Part Prices**.
2. Check the last successful run against today's date.

If it has been failing, the files hold whatever the last good run wrote. Nothing in a build
file records when its prices were fetched, so staleness is invisible from the file itself —
see [Roadmap](./roadmap.md).

## The scraper workflow is failing

Most likely PCPartPicker changed its markup. The scraper parses their pages with
BeautifulSoup, so a layout change breaks extraction without warning.

The workflow log will show whether it failed at fetch or at parse. See [Scraper](./scraper.md).

You can also trigger it manually from the Actions tab to reproduce.

## A part shows no current price

Usually discontinued. If PCPartPicker has no active listing there is no price to scrape, which
is expected for hardware this old rather than a fault.

## A PCPartPicker link does not open

The lists live under the archive's own PCPartPicker account. If a list was deleted or made
private, the link fails while the Markdown copy still works — which is one reason the archive
keeps its own copies.

## A build is in the index but the file is missing

Report it. The index is maintained by hand alongside the files, so the two can drift.

## The website shows different prices from the Markdown

Expected. The website is in **US dollars** and the Markdown in **Canadian dollars**. Both are
generated from the same data.

If they disagree beyond the exchange rate, the `gh-pages` build is probably older than the
last scrape.

## Prices differ from what I see at a retailer

The scraper reads PCPartPicker's aggregate rather than visiting retailers directly, and its
figures lag. Treat archived prices as indicative.

## Running the scraper locally does nothing

```bash
pip install -r requirements.txt
python scraper.py
```

It rewrites the Markdown files in place, so check `git diff` rather than the console. See
[Scraper](./scraper.md).
