# Tony Magnetic — personal site

A static, dependency-free site for Anthony “TonyMagnetic” Thorne. Four pages, self-hosted
fonts, no build step, no tracking. Open `index.html` or serve the folder.

```bash
python3 -m http.server 4321 --directory .
```

## Structure

```
index.html      Home — hero, quote, chapters, bio intro, approach, contact CTA
work.html       The eight chapters, long-form (anchors: #mecca #munich #the-year-of
                #hong-kong #maximal-concepts #hamachi-hunters #tony-only-tony #tonymagnetic)
about.html      Full bio, timeline, personal notes
contact.html    Contact details and what he takes on
assets/css/site.css
assets/js/site.js       Mobile menu, sticky header, scroll reveals, chapter slideshows
                        and the chapters view switch
assets/fonts/           Newsreader + Manrope (latin subsets, self-hosted)
assets/images/          Generated derivatives (empty until you build)
assets/images/_src/     Put original photos here, named by slot key
tools/build-images.py   Crops, resizes, encodes AVIF/WebP/JPEG, rewrites the HTML
IMAGES.md               Shot list, sourcing routes, rights notes
```

## Chapters: one markup, three views

Every chapter on the home and work pages is the same block — a `.chapter-media` holding
one or more `<figure class="slide">` frames, then a `.chapter-text` with the caption and
copy. The section's `data-view` attribute picks how that renders, and the pill switch in
the section head sets it (remembered in `localStorage` as `chapters-view`):

| Mode | What it does |
|---|---|
| `slideshow` (default) | Full-width panel, frames cross-fade under the text. Auto-advances every ~5s only while on screen, pauses on hover/focus, never under `prefers-reduced-motion`. |
| `detailed` | The editorial layout — one frame, caption below, offset blocks. Dots still let you flick through the frames. |
| `list` | Compact index rows with a thumbnail and the first paragraph. |

Adding a mode is one CSS block keyed on `.chapters[data-view="…"]` plus a button in the
switch. Print always uses the detailed layout. The work page's heading is the same slide
machinery run full-bleed (`.page-heading--slideshow`), cycling one frame from each chapter. To give a chapter another frame, add a
slot to `tools/build-images.py`, drop a placeholder `<div class="slot" data-slot="Slide —
key">` inside a new `<figure class="slide">`, and run the build with `--apply`.

## Design

Adapted from the editorial layout language of ospaced.com — large display serif, uppercase
letterspaced labels, generous section rhythm, full-bleed hero, alternating offset feature
blocks — with a palette shifted toward denim rather than warm interiors.

| Token | Value | Use |
|---|---|---|
| `--raw` | `#fbf6ec` | page ground, under a soft warm/denim light wash at the top of the page |
| `--paper` | `#fffdf8` | lifted panels |
| `--selvage` | `#eee5d5` | fills, rules |
| `--ink` | `#1b1c1e` | body text |
| `--indigo` | `#2f3f5c` | denim — selection, slot tints |
| `--rinse` | `#6d7c93` | washed denim |
| `--rust` | `#8a4b32` | accent — labels, the dot in the wordmark |
| `--orange` | `#bf4e16` | contact block |

Type: **Newsreader** (display serif) + **Manrope** (sans).

## Before this goes live

**1. Replace the image placeholders.** See [IMAGES.md](IMAGES.md) for where to source
each photograph and the rights questions worth settling first, then run
`tools/build-images.py --apply` to generate responsive derivatives and wire them in.
The manual route: Every grey diagonal-hatched block is a `<div class="slot">`
with a `data-slot` label saying what belongs there. Swap each one for an `<img>`:

```html
<!-- from -->
<div class="slot" data-slot="Mecca USA — archive campaign or product shot" style="--slot-ratio: 16 / 9"></div>
<!-- to -->
<img src="assets/images/mecca-campaign.jpg" alt="Mecca USA campaign, 1996" width="1920" height="1080">
```

Slots needed: hero shot, portrait (×2), and one image per chapter — Mecca USA, Munich,
“The Year of…”, Tony Only Tony, TonyMagnetic INC.

**2. Confirm the contact email.** `contact.html` currently uses `hello@tonymagnetic.com`
as a placeholder — it is marked with a `TODO` comment.

**3. Check the biography with Tony.** See sourcing notes below.

**4. Set the real domain.** `canonical` and `og:url` on each page currently point at
`https://tonymagnetic.com/`.

## Sourcing notes

His LinkedIn profile could not be read directly — LinkedIn blocks automated access and
returns a login wall. The career details came from public search results *describing* that
profile, so they carry his own framing but were not read from the page itself. Worth
confirming with him:

- Launching **Mecca USA** in New York in summer 1995 with Tony Shellman and Lando Felix.
  Independent coverage of Mecca credits Shellman and Felix as founders and does not mention
  Tony, so his exact role and title should be stated the way he states it.
- The **Munich** retail platform — dates and nature are unconfirmed; the timeline entry
  says “late 1990s”, which is an inference, not a source.
- **Tony Only Tony** — confirmed as his label by name only; no dates.

Sourced and solid:

- The denim line **“The Year of…”** and the Gucci / Comme des Garçons quote come from his
  April 2007 profile in the South China Morning Post, along with the L'Eau d'Issey and
  Prada/Armani details used on the About page.
- **TonyMagnetic INC** — he is listed as President; the company filed a clothing trademark
  on 30 August 2019 covering tops, bottoms, t-shirts, pants, shorts, sweatshirts, hoodies,
  shirts, jackets, headwear and footwear.
- Based in **Ho Chi Minh City, Vietnam**; Instagram [@tonymagnetic](https://www.instagram.com/tonymagnetic/).

All prose describing his working philosophy (the Approach section, the “builder of brands,
not seasons” framing) is written copy, not quotation. It should read like him or be rewritten.
