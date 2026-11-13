# bulkstem.com

The public download page and the update feed of BulkStem (GitHub Pages). No application source lives here.

- `index.html` — one hero section and the download button (D-229); static, no scripts. The button is GitHub's stable link `releases/latest/download/BulkStem.zip`: every release uploads its zip a second time under that constant name, so the page needs no change for a release.
- `design/og-card.html` — the source of `img/og.png`, the card shown when the link is shared.
- `updates/appcast.xml` — Sparkle feed; entries and zips are added by the release pipeline of `PhoboSys/bulkstem` (private).
- `CNAME` — custom domain `bulkstem.com`.
