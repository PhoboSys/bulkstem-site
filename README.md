# bulkstem.com

Purpose: the public website of BulkStem — the landing page, the privacy page and the Sparkle update feed — served as plain static files by GitHub Pages; how the files are laid out, how the release pipeline fills in the constants and how the copy is checked.
Owner: Thales (site build and checks); Roman approves the page and every publication.

No application source lives here. The copy comes word for word from the brief `docs/product/landing-prompt-lovable.md` (v1.2, D-043) in the BulkStem knowledge base (`PhoboSys/bulkstem`); the design is the adopted `/v2` direction (D-041), recorded in `docs/product/landing-review.md`; the site is built in this repository, without Lovable code (D-042).

There is no build step and no framework: GitHub Pages serves the files exactly as they are in `main`.

## Files

| Path | What it is |
|---|---|
| `index.html` | The landing page: hero, example figures, Reports, How it works, What it calculates, Principles, Trust, FAQ, Download, footer. |
| `privacy.html` | The privacy page: the website collects nothing; the application stores all data locally. Same header and footer. |
| `assets/site.css` | The only stylesheet, hand-written, with the design tokens as custom properties on `:root`. Light theme always (D-043). |
| `assets/site.js` | The only script: a fade on `.reveal` blocks, off under `prefers-reduced-motion`. All content is readable without it. |
| `assets/fonts/` | Self-hosted Inter Tight (variable, OFL) for headings and figures; see `assets/fonts/README.md`. Without the file the system stack renders. |
| `img/` | `icon.svg` (the app icon, also the favicon) and the six screenshots `screenshot-{plan,cargo,report}[-dark].png` at 2200 × 1464. |
| `scripts/check-copy.py` | The copy check (below). |
| `sitemap.xml`, `robots.txt` | For search engines. |
| `updates/appcast.xml` | Sparkle feed; entries and zips are added by the release pipeline of `PhoboSys/bulkstem` (private). |
| `CNAME` | Custom domain `bulkstem.com`. |
| `.nojekyll` | Tells GitHub Pages to serve the files without Jekyll. |

Rules:

- `updates/appcast.xml` is written only by the release pipeline. Never edit it by hand, and never move it: every installed copy of BulkStem reads `https://bulkstem.com/updates/appcast.xml`.
- `CNAME` and `.nojekyll` stay as they are.
- No request may leave bulkstem.com: no fonts, scripts, images or stylesheets from other hosts, no analytics, no cookies. Asset paths are relative.
- Every sentence on the page comes from the brief. Change the brief first, then the page, then run the copy check.

## Screenshots

The six screenshots are copies of the originals in `docs/product/screenshots/site/` of the Summermark repository (`PhoboSys/bulkstem`). They are regenerated for every release that changes these screens by the command block in that folder's `README.md`; copy the new files here under the same names. Never resize or re-encode them. The page shows the light plan in the hero, the light report in Reports and the dark cargo window in the navy section "How it works"; the other three files are kept for the same set.

## Constants

Three literal placeholders stand in `index.html` and `privacy.html` until the release pipeline replaces them in the published copy:

| Constant | Where | Set by |
|---|---|---|
| `DOWNLOAD_URL` | the three "Download for Mac" buttons (`href`) | the release pipeline: the latest notarized zip |
| `RELEASE_NOTES_URL` | the release-notes link under the download button (`href` and visible text) and "Release notes" in the footer | the release pipeline |
| `CONTACT_EMAIL` | the FAQ answer "Who makes it?" and the footer (`mailto:` link and visible text) | Roman (still open) |

The pipeline replaces them with one command per file (macOS `sed`):

```bash
sed -i '' -e 's|DOWNLOAD_URL|https://…|g' -e 's|RELEASE_NOTES_URL|https://…|g' -e 's|CONTACT_EMAIL|…|g' index.html privacy.html
```

## Copy check

Every double-quoted string of the brief's CONTENT section must appear on the page, the retired v1 phrases must not, the `<title>` must be exact and the meta description must equal the hero subheadline. Python 3, standard library only:

```bash
python3 scripts/check-copy.py ~/Summermark/docs/product/landing-prompt-lovable.md
```

It prints the number of strings checked and every miss, and exits with 1 on any miss. Run it before every publication, on the page with the constants still in place: the brief names `CONTACT_EMAIL` and `RELEASE_NOTES_URL` literally.

## Preview locally

```bash
python3 -m http.server 8080
```

Then open http://localhost:8080/ (and `/privacy.html`). Stop the server with Ctrl-C.
