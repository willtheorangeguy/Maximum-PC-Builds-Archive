# Maximum PC Builds Archive — Roadmap

Gaps and limitations, observed from the repository. Concrete defects are in
[`internal/known-issues.md`](./internal/known-issues.md).

## Staleness is invisible

Build files carry a current price with no indication of when it was fetched. If the daily
workflow has been failing for a month, the numbers look exactly as authoritative as fresh
ones.

A "prices as of" line per file, written by the scraper, would fix that in a single change and
is the most valuable item here.

## The price history is collected and unused

Because the scraper rewrites prices in place every day, the git history already contains a
daily price series for every tracked component going back to when automation started.

That is a genuinely interesting dataset — component depreciation over years — and nothing
surfaces it. Extracting it would need no new collection, only reading what is already
committed.

## Gaps

**The build index is maintained by hand.** It lists every build with links to three
representations, and nothing checks that the Markdown links resolve or that every file appears.
It has already drifted once — see [`internal/known-issues.md`](./internal/known-issues.md).

**One upstream, no fallback.** Every current price comes from PCPartPicker. A layout change
there stops all price updating, and there is no secondary source.

**Discontinued parts degrade quietly.** An unavailable component simply shows no current
price, which is indistinguishable from a scrape failure.

**No coverage record.** Nothing states which issues are archived and which are missing, so a
gap in the years looks the same as an issue that had no build.

**The website build is not automated alongside prices.** Prices update daily on `main`;
`gh-pages` can lag.

## Non-goals

- **Being a shopping list.** Most of this hardware is discontinued. The archive exists for the
  comparison between printed and current prices.
- **Reproducing the magazine.** It records which parts each build specified, not the articles
  around them.
