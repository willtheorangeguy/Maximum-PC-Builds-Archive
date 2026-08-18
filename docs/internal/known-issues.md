# Known Issues — Maximum-PC-Builds-Archive

Concrete defects and gaps found while writing this repository's documentation in
August 2026. **Nothing here was changed** — each one needs a code, configuration, or
licensing decision rather than a documentation one.

Ordered by severity. See [`docs/roadmap.md`](../roadmap.md) for the narrative version,
which also covers deliberate non-goals.


**6 open:** 3 medium, 3 low.

## 1. The hero GIF never rendered — a /blob/ URL serves HTML, not an image

**Severity:** Medium  
**Where:** `README.md`, the screenshot image

**What:** It pointed at `github.com/willtheorangeguy/Maximum-PC-Builds-Archive/blob/main/docs/images/welcome.gif`. A `/blob/` URL returns a GitHub HTML page rather than image bytes.

**Why it matters:** The animated demo has not been displaying on the repository front page. Same fault found in `Moms-Canning-Timer`.

**Suggested fix:** Fixed in this sweep — the hero and logo now come from `.github/icons/Maximum-PC-Builds-Archive/` via `raw.githubusercontent.com`.

## 2. A build-index row linked to the wrong file

**Severity:** Medium  
**Where:** `README.md` (previous version) table of contents, January 2018 Turbo row

**What:** The January 2018 Turbo entry linked to `/2018/March/Turbo.md`. `2018/January/Turbo.md` exists and is a different build.

**Why it matters:** A reader following the index for January's Turbo build silently got March's parts and prices. Nothing checks that index links resolve, let alone that they point at the right month, and the index is maintained by hand across roughly 88 rows.

**Suggested fix:** Corrected in this sweep. The durable fix is generating the index from the directory tree, or a CI check that every link resolves and matches its row.

## 3. Current prices carry no timestamp, so staleness is invisible

**Severity:** Medium  
**Where:** the build Markdown files; `scraper.py`

**What:** `scraper.py` rewrites the current-price column daily under `update-prices.yml`, but nothing records when a file was last updated.

**Why it matters:** If the workflow fails for a week or a month, the prices look exactly as authoritative as fresh ones. There is no way to tell a current figure from a stale one without opening the Actions tab.

**Suggested fix:** Have the scraper write a "prices as of <date>" line into each file it touches. One change, and it makes every build self-describing.

## 4. CC BY 4.0 is applied to build lists published by a magazine

**Severity:** Low  
**Where:** `CONTENT_LICENSE.md`

**What:** The repository ships a Creative Commons Attribution 4.0 licence over the content. The component selections were published by Maximum PC magazine.

**Why it matters:** CC BY is a grant, and the selections were not this repository's to grant. Part lists are closer to fact than to creative expression, so the practical risk is low — the statement is still not accurate. Same pattern as `FBI-Application-Guide` and the transcript archives.

**Suggested fix:** Replace with a provenance notice: where the builds came from, that no rights in them are claimed, and that MIT covers the tooling and the price data this project collected.

## 5. The PCPartPicker account name in every link is worth verifying

**Severity:** Low  
**Where:** `docs/builds.md`, 76 links

**What:** All PCPartPicker links use `pcpartpicker.com/user/willtheornageguy/` — note `ornage` rather than `orange`, unlike the GitHub username `willtheorangeguy`.

**Why it matters:** It is consistent across all 76 links, which suggests it is genuinely the account name rather than a per-link typo. Worth confirming once: if it is wrong, every PCPartPicker link in the archive is dead.

**Suggested fix:** Open one link. If the account is `willtheorangeguy`, a single find-and-replace fixes all 76.

## 6. Build-index links used two inconsistent path forms

**Severity:** Low  
**Where:** `README.md` (previous version) table of contents

**What:** Most Markdown links were root-relative — `](/2021/January/AMD%20Budget.md)` — but nine were written without the leading slash, `](2021/February/Intel%20Mid-Range.md)`.

**Why it matters:** Both happened to resolve from a README at the repository root, so the inconsistency was invisible. It stopped being invisible the moment the table moved into `docs/`, where the two forms resolve differently — nine rows broke and the rest did not.

**Suggested fix:** Normalised in this sweep. Generating the index from the directory tree would prevent the class of problem entirely.


---

## Also, across every repository

**`.bandit` is present on disk but untracked in git.** Verified in PyWorkout, treklogger,
skyscanner-cli, booking-cli, piggy, and aibot — the config file exists locally in each but
`git ls-files` does not know about it, so none of it reached GitHub.

The August 2026 security sweep therefore looks complete locally and landed nowhere. Worth
checking across all 44 repositories it covered.
