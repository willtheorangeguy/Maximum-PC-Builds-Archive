# Maximum PC Builds Archive — Documentation

An archive of the PC builds published in Maximum PC magazine, kept as part lists in three
parallel forms, with a scraper that keeps current prices fresh.

```
Maximum-PC-Builds-Archive/
├── docs/
│   ├── README.md          this page
│   ├── builds.md          the full build index
│   ├── usage.md           the three representations
│   ├── architecture.md    how the archive is organised
│   ├── scraper.md         the daily price updater
│   ├── faq.md             currencies, accuracy, coverage
│   ├── troubleshooting.md stale or missing prices
│   ├── roadmap.md         gaps and non-goals
│   └── legal/             privacy policy and terms
├── 2018/ … 2021/          one folder per year, then per month
├── scraper.py             the price updater
└── requirements.txt
```

## Pages

- [Build index](./builds.md) — every build, with links to all three forms
- [Usage](./usage.md) — which representation to use, and what each gives you
- [Architecture](./architecture.md) — the folder scheme, the branches, the currencies
- [Scraper](./scraper.md) — the daily price update
- [FAQ](./faq.md) — currencies, price accuracy, coverage
- [Troubleshooting](./troubleshooting.md) — prices not updating, missing builds
- [Roadmap](./roadmap.md) — gaps and non-goals

## Three representations, three currencies

The same build exists three ways, and the currency differs by design:

| Where | Currency | Shows |
|---|---|---|
| PCPartPicker | Any it supports | Current price only |
| Markdown, in this repo | Canadian dollars | Printed **and** current |
| Website, on `gh-pages` | US dollars | Printed **and** current |

Only the last two preserve the original printed price, which is the point of an archive — the
interesting figure is the gap between what a build cost then and what it costs now.

## The prices are moving targets

`scraper.py` runs daily and rewrites the current prices in the Markdown files. So the
repository's history is partly a price series, and any given file is accurate as of its last
successful run rather than as of the magazine issue.
