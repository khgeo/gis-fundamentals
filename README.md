# មូលដ្ឋានគ្រឹះនៃប្រព័ន្ធព័ត៌មានភូមិសាស្ត្រ
## Fundamentals of GIS: a Khmer-language textbook

[![CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

A complete one-semester (15-week) undergraduate GIS textbook written **in Khmer**, with
QGIS-based practical labs and examples drawn entirely from Cambodia.

សៀវភៅសិក្សា GIS ពេញលេញជាភាសាខ្មែរ សម្រាប់វគ្គសិក្សា ១ ឆមាស (១៥ សប្ដាហ៍)
ជាមួយលំហាត់អនុវត្តលើ QGIS និងឧទាហរណ៍ក្នុងបរិបទកម្ពុជា។

📖 **Read online:** https://khgeo.github.io/gis-fundamentals/

---

## What's inside

| | |
|---|---|
| Lessons | 15 (theory, 3 hours each) |
| Labs | 15 (QGIS practicals with real Cambodian data) |
| Interactive | Web maps, simulators, quizzes and self-check boxes |
| Software | QGIS 3.34 LTR, free and open source |
| Language | Khmer, with English technical terms in parentheses |
| License | CC BY-SA 4.0 |

## Repository structure

```
.
├── docs/
│   ├── index.md              # Landing page
│   ├── syllabus.md           # 15-week schedule + assessment
│   ├── glossary.md           # Khmer–English GIS terminology  ← read this first
│   ├── lessons/lesson-01…15.md   # Theory lessons
│   ├── workbook/lab-01…15.md     # QGIS practicals
│   ├── appendix/                 # Install guide, Cambodia dataset, references
│   └── assets/
│       ├── css/                  # Khmer typography, workbook and simulator styles
│       ├── js/                   # Interactive maps, simulators, quizzes
│       ├── svg/                  # Figures
│       └── data/                 # Small GeoJSON layers for web maps
├── mkdocs.yml                # Site + navigation config
├── requirements.txt
└── .github/workflows/deploy.yml   # Auto-publish to GitHub Pages
```

## Build locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve          # preview at http://127.0.0.1:8000
mkdocs build          # static site in ./site
```

## Publish to GitHub Pages

1. Create the repo on GitHub and push this folder to the `main` branch.
2. Repo **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Push. The workflow builds and publishes automatically.

## Export a PDF

Uncomment the `with-pdf` plugin block in `mkdocs.yml`, then:

```bash
pip install mkdocs-with-pdf
mkdocs build          # PDF lands in site/pdf/
```

> **Khmer PDF note:** the PDF renderer must have a Khmer font installed on the build
> machine, or Khmer text renders as boxes. On Ubuntu:
> `sudo apt install fonts-khmeros fonts-noto-khmer`

## Teaching datasets

The `Cambodia.zip` course dataset (43 layers) is **not** committed to this repo.
It is attached to the [latest GitHub Release](https://github.com/khgeo/gis-fundamentals/releases/latest)
and described in Appendix B. Only small GeoJSON extracts for the web maps live in `docs/assets/data/`.

## Contributing

Terminology corrections are the most valuable contribution. Khmer GIS vocabulary is
not yet standardised nationally. See `docs/glossary.md` and open an Issue or PR.

## Citation

```
YAM Sarath (2026). មូលដ្ឋានគ្រឹះនៃប្រព័ន្ធព័ត៌មានភូមិសាស្ត្រ
[Fundamentals of GIS: A Khmer-language textbook]. CC BY-SA 4.0.
https://github.com/khgeo/gis-fundamentals
```
