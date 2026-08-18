# Maximum PC Builds Archive — Architecture

## Layout

```
2018/January/{Budget,Mid-Range,Turbo}.md
2018/February/…
…
2021/October/{AMD Budget, AMD Mid-Range, AMD Turbo, Intel Budget, …}.md
scraper.py
requirements.txt
.github/workflows/update-prices.yml
```

Year, then month, then one file per build tier. The AMD and Intel split appears only in the
years the magazine used it, so the folder shape follows the source rather than imposing a
uniform scheme.

## Two branches, two artefacts

| Branch     | Holds                                       |
| ---------- | ------------------------------------------- |
| `main`     | Markdown builds, the scraper, documentation |
| `gh-pages` | The generated website                       |

The website is a **derived artefact**. The Markdown files are the source of truth, and the
published pages are one rendering of them — which is why the currency can differ between the
two without either being wrong.

## Three representations, deliberately

| Form         | Currency      | Printed price | Current price             |
| ------------ | ------------- | ------------- | ------------------------- |
| PCPartPicker | Any supported | No            | Yes, live                 |
| Markdown     | CAD           | Yes           | Yes, from the last scrape |
| Website      | USD           | Yes           | Yes, from the last scrape |

PCPartPicker is a live service and cannot carry a historical figure, which is why the archive
keeps its own copies. Losing the printed price would leave nothing to compare against, and the
comparison is the whole point.

The CAD/USD split reflects where each is read rather than an inconsistency.

## Prices are rewritten in place

`scraper.py` runs daily under `update-prices.yml` and edits the current-price column of the
Markdown files, committing the result.

Two consequences:

- **A build file is accurate as of the last successful run**, not as of the issue date.
- **The git history is partly a price series.** Every daily commit records what those parts
  cost that day, which is a more interesting dataset than the files themselves and is not
  currently surfaced anywhere.

The printed price column is never touched, which is what keeps the archive honest.

## The scraper depends on someone else's markup

Prices come from PCPartPicker, parsed with BeautifulSoup. PCPartPicker aggregates retailers —
the scraper does not visit Newegg, Amazon, or Best Buy itself.

That makes one site the single point of failure for the whole price-updating story, and a
layout change there breaks parsing with no warning. See [Scraper](./scraper.md).

## Provenance

The component selections were published by Maximum PC magazine. This repository records which
parts each build specified and tracks their prices; it does not reproduce the magazine's
articles or reviews.
