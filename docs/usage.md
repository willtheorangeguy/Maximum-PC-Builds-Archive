# Maximum PC Builds Archive — Usage

## Finding a build

Start at the [build index](./builds.md). Rows are grouped by year and issue, with the build
tier — Budget, Mid-Range, or Turbo — and links to all three representations.

For the years the magazine split them, AMD and Intel variants appear as separate rows.

## Which representation to use

### PCPartPicker

Best for **buying**. The lists live under the archive's PCPartPicker account, so the site
prices them live against retailers and flags compatibility problems.

Currency is whatever you set on PCPartPicker. It shows only the current price — the printed
price is not carried across.

### Markdown, in this repository

Best for **reading offline or comparing**. Each file is a plain table, so it diffs, greps, and
survives without a network.

Prices are in **Canadian dollars**, and each part carries both the printed price and the
current one.

### The website

Best for **browsing**. Generated from the same data and published from the `gh-pages` branch.

Prices are in **US dollars**, with printed and current side by side.

## Reading a Markdown build

Each row is a component with its printed price and its current price. The difference between
those two columns is the archive's reason for existing — some parts have collapsed in price,
others have not moved, and a few cost more now than when the issue went out.

## Downloading

```
main       the Markdown builds and the scraper
gh-pages   the built website
```

Both are downloadable as ZIPs from the GitHub interface.

## A caution on prices

Current prices come from a daily scrape and are only as good as its last successful run.
Printed prices are fixed and historical. See [Scraper](./scraper.md) and
[FAQ](./faq.md).
