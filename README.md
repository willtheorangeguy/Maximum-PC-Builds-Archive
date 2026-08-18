<!-- Logo -->
<h1 align="center">
  <img src="https://raw.githubusercontent.com/willtheorangeguy/.github/main/icons/Maximum-PC-Builds-Archive/logo.png" height="250px" width="400px" alt="Maximum PC Builds Archive">
  <br>
  Maximum PC Builds Archive
  <br>
</h1>

<!-- Copy -->
<h4 align="center">Every Maximum PC magazine build, archived as part lists — with the printed price alongside today's.</h4>

<!-- Badges -->
<div align="center">
  <img alt="Gitleaks State" src="https://github.com/willtheorangeguy/Maximum-PC-Builds-Archive/actions/workflows/gitleaks.yml/badge.svg">
  <img alt="Price Updates" src="https://github.com/willtheorangeguy/Maximum-PC-Builds-Archive/actions/workflows/update-prices.yml/badge.svg">
  <img alt="GitHub Issues" src="https://img.shields.io/github/issues/willtheorangeguy/Maximum-PC-Builds-Archive">
  <img alt="GitHub Pull Requests" src="https://img.shields.io/github/issues-pr/willtheorangeguy/Maximum-PC-Builds-Archive">
</div>

<!-- Navigation -->
<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#usage">Usage</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#support">Support</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#credits">Credits</a> •
  <a href="#attribution">Attribution</a> •
  <a href="#license">License</a>
</p>

<!-- Hero -->
![screenshot](https://raw.githubusercontent.com/willtheorangeguy/.github/main/icons/Maximum-PC-Builds-Archive/welcome.gif)

## Key Features

- Builds spanning many issues, in Budget, Mid-Range, and Turbo tiers.
- AMD and Intel variants for the years the magazine split them.
- Three representations of every build: PCPartPicker, Markdown, and a web page.
- Both the **printed price** and the **current price**, so you can see the drift.
- Prices refreshed daily by a scraper running in GitHub Actions.
- Markdown in Canadian dollars, the website in US dollars, PCPartPicker in any currency.

## Usage

Find a build in the [build index](docs/builds.md), then open whichever representation suits — see [`docs/usage.md`](docs/usage.md).

## Documentation

Full documentation lives in [`docs/`](docs/README.md):
[Build index](docs/builds.md) · [Usage](docs/usage.md) · [Architecture](docs/architecture.md) · [Scraper](docs/scraper.md) · [FAQ](docs/faq.md) · [Troubleshooting](docs/troubleshooting.md) · [Roadmap](docs/roadmap.md)

## Support

Open a [GitHub Discussion](https://github.com/willtheorangeguy/Maximum-PC-Builds-Archive/discussions/new) or file an [issue](https://github.com/willtheorangeguy/Maximum-PC-Builds-Archive/issues/new/choose).

## Contributing

Contributions welcome. See the org-wide [Contributing Guide](https://github.com/willtheorangeguy/.github/blob/main/CONTRIBUTING.md) and [Code of Conduct](https://github.com/willtheorangeguy/.github/blob/main/CODE_OF_CONDUCT.md).

## Credits

Price data via [PCPartPicker](https://pcpartpicker.com/). Scraping with [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/).

## Attribution

The builds were originally published by **Maximum PC** magazine. This is an unofficial
archive of the component selections, not affiliated with or endorsed by the magazine or its
publisher. See [`CONTENT_LICENSE.md`](CONTENT_LICENSE.md).

## License

- **Code:** MIT — see [`LICENSE.md`](LICENSE.md)
- **Compiled data:** see [`CONTENT_LICENSE.md`](CONTENT_LICENSE.md) and [Attribution](#attribution)
