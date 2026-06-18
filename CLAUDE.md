# CLAUDE.md

## Project Overview

This is the **Maximum PC Builds Archive** — an archive of PC builds featured in Maximum PC magazine. Content is stored as Markdown files organized by year/month, with a companion website on the `gh-pages` branch. A Python scraper automatically updates part prices daily via GitHub Actions.

## Repository Structure

```
├── 2018/, 2020/, 2021/   # Build archives by year → month → build markdown files
├── docs/                  # Documentation assets (images, etc.)
├── .github/
│   ├── workflows/         # GitHub Actions (gitleaks, update-prices)
│   ├── agents/            # GitHub Copilot agent configs
│   └── ISSUE_TEMPLATE/    # Issue templates
├── scraper.py             # PCPartPicker price scraper (Python 3.12)
├── requirements.txt       # Python deps: beautifulsoup4, requests, lxml
├── README.md              # Main docs with table of contents linking all builds
└── CONTRIBUTING.md        # Contribution guidelines
```

## Build File Conventions

- Each build is a Markdown file named by category: `AMD Budget.md`, `Intel Turbo.md`, etc.
- Pre-2020 builds: Budget, Mid-Range, Turbo categories only.
- 2020+: Separate AMD and Intel variants for each tier.
- Files contain PCPartPicker list links and component tables with prices.

## Development

### Price Scraper

```bash
pip install -r requirements.txt
python scraper.py          # Updates prices in all build markdown files
DEBUG=1 python scraper.py  # Verbose logging
```

The scraper (`scraper.py`) extracts PCPartPicker URLs from markdown files, scrapes current prices, and updates the files in-place. It runs daily at 2 AM UTC via `.github/workflows/update-prices.yml`.

### CI/CD

- **update-prices.yml** — Daily automated price scraping, commits changes directly to main.
- **gitleaks.yml** — Secret scanning on pushes/PRs.
- **GitHub Pages** — The `gh-pages` branch serves the website.

## Commit Message Convention

Format: `type(scope): description`

Examples from history:

- `feat(pip): bump lxml to 6.1.0`
- `fix(github-actions/workflows): update dependencies of gitleaks action to v3`

## Key Guidelines

- Never commit `.env` files or secrets.
- When adding a new magazine issue: create markdown files in the appropriate `year/month/` folder, then update the README table of contents.
- The scraper respects rate limits (2s delay between requests) — do not reduce this.
- Python version: 3.12. Dependencies are pinned in `requirements.txt`.
