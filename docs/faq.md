# Maximum PC Builds Archive — FAQ

## Why are the Markdown files in CAD and the website in USD?

Deliberate, reflecting where each is read. PCPartPicker will show either, plus most other
currencies — it is the one to use if you want prices in your own.

## Are the current prices accurate?

They are as accurate as the last successful scrape, which runs daily at 02:00 UTC. If the
workflow has been failing, prices are stale and nothing in the file says so.

Printed prices never change — those are historical fact.

## Where do the prices come from?

PCPartPicker, which aggregates retailers including Newegg, Amazon, and Best Buy. The scraper
reads PCPartPicker rather than visiting those retailers directly.

## Can I still buy these parts?

Often not. Many are years old and discontinued, so a current price may be for a remaining
listing rather than a going rate — and an unavailable part may show no price at all.

The archive's value is the comparison, not a shopping list.

## Why do some months have AMD and Intel versions?

Because the magazine split them for those issues. The folder structure follows the source
rather than imposing a uniform scheme.

## Is this affiliated with Maximum PC?

No. It is an unofficial archive of the component selections. It does not reproduce the
magazine's articles or reviews.

## Why keep three copies of everything?

They do different jobs. PCPartPicker is live and buyable but cannot hold a historical price;
the Markdown is diffable and works offline; the website is browsable. Only the latter two
preserve the printed price. See [Architecture](./architecture.md).

## The prices in git history — is that useful?

Potentially very. Because the scraper rewrites prices in place daily, the commit history is a
price series for every tracked part. Nothing currently surfaces it. See
[Roadmap](./roadmap.md).

## How do I add a build?

Add the Markdown file under the right year and month, and add a row to
[the build index](./builds.md). If it has a PCPartPicker list, link it too.

## Can I reuse the data?

The compiled data is covered by `CONTENT_LICENSE.md`; the code is MIT. Note the builds
originated with the magazine — see [Architecture](./architecture.md).
