# Sourcing the photography

Eight images carry this site. The design is photo-led — big, quiet, full-bleed — which
means it looks expensive with good pictures and empty with bad ones. It is worth being
slow about this.

## The short version

**Ask Tony first, and ask him for the raw files.** He is the only clean source for most of
this, and he almost certainly has more than he thinks. Everything else on this page is
what to do for the gaps.

---

## What each slot needs

Keys match `tools/build-images.py`. Drop originals into `assets/images/_src/<key>.jpg`.

| Key | Ratio | Where it sits | What the picture has to do |
|---|---|---|---|
| `hero` | full-bleed | Homepage, behind the name | Carries the whole site. Him, or one strong campaign frame. Needs quiet space in the lower-left third — the name and standfirst sit there over a dark scrim. Landscape, 2560px+. |
| `portrait-studio` | 4:5 | Homepage bio block | Working portrait. Him in the room where the work happens, not a headshot. |
| `portrait-about` | 4:5 | About page | Second portrait, different register from the first — closer, or more formal. Can be the same shoot. |
| `mecca` | 16:9 | Mecca USA chapter | 1995–96. Campaign frame, lookbook page, hang tag, a rack in a store. Period texture beats resolution here. |
| `munich` | 4:5 | Munich chapter | The retail space, a product wall, a shopfront. Vertical. |
| `year-of` | 3:2 | “The Year of…” chapter | Denim, close. Selvage, hardware, stitch, a wash detail. This is the one slot where a macro shot does more than a garment shot. |
| `tony-only-tony` | 4:5 | Tony Only Tony chapter | A label, a neck tag, one garment shot clean. |
| `tonymagnetic` | 16:9 | Current work | Present-day lookbook. Should look decisively newer than the rest. |

Minimum 1600px on the long edge; 2400px+ preferred. Straight off the camera or the scanner
is ideal — don't send anything that has been through Instagram twice.

---

## Where to get them, cleanest first

### 1. Tony's own archive — for everything from 1995 to now

The only source that is unambiguously his to use. Specifically worth asking for:

- **Original shoot files** from any campaign he commissioned. If he paid the photographer,
  check the invoice or contract for what he actually licensed — commissioning a shoot does
  not automatically mean he owns the copyright, and "we used it in 1996" is not the same as
  "we can put it on a website in 2026." Where a photographer holds the rights, a short
  written permission naming the site is worth getting now.
- **His Instagram back catalogue.** [@tonymagnetic](https://www.instagram.com/tonymagnetic/)
  is active but age-restricted and login-walled, so I could not see it — he can, and he can
  export the originals via Instagram's *Download Your Information*, which returns better
  files than anything scraped off the page.
- **Physical archive.** Hang tags, labels, lookbooks, line sheets, contact sheets, press
  clippings. A flatbed scan at 600dpi of a 1996 hang tag will out-perform a mediocre new
  photo in the `mecca` slot, and the rights are simple.
- **Product on hand.** The `year-of` and `tony-only-tony` slots are close-up detail shots.
  If he still owns one pair of the jeans and one labelled garment, those two slots can be
  shot properly in an afternoon with a window and a phone.

### 2. Commission the two portraits

Both portrait slots and the `tonymagnetic` lookbook slot want current photography, and Ho
Chi Minh City is not short of fashion photographers. This is the single highest-return
spend on the whole site — the hero and the two portraits are three of the eight images and
they set the tone for the other five. Get a buyout for web use in writing.

### 3. Archive and press routes — for the 1990s material

Only if his own archive comes up short, and all of these cost money and time:

- **South China Morning Post.** The April 2007 piece is
  [scmp.com/article/588186](https://www.scmp.com/article/588186/tony-magnetic). If it ran
  with a photograph, SCMP's syndication/reprints desk is who licenses it. Ask for the
  original frame, not the web crop.
- **Getty Images / WWD archive.** Both hold 1990s American streetwear editorial and trade
  coverage. Search Mecca USA by name and by year. Editorial-licence terms often restrict
  commercial use, so read what you are actually buying — a personal brand site may count as
  commercial.
- **Tony Shellman.** Co-founder of Mecca and publicly reachable through
  [makingabrand.co](https://makingabrand.co/mentors/tony-shellman/). If anyone has kept a
  usable Mecca archive it is likely to be one of the founders, and a direct ask costs nothing.

### 4. What not to do

Do not right-click images off Pinterest, resale listings, Instagram fan accounts, or old
editorial scans. Streetwear archive imagery circulates heavily and is heavily
photographer-owned; a personal brand site is a commercial use, and this is exactly the kind
of site that gets a rights letter. The same goes for anything I could have pulled from
search results — I did not download any of it, deliberately.

### 5. Licensed stock — last resort, and only for two slots

If `munich` never materialises, a licensed interior or shopfront frame can hold the slot,
and a licensed denim macro can hold `year-of`. Both are texture rather than record, so a
generic image does less damage there than it would in a portrait. Anywhere else — a stock
photo of a stranger standing in for Tony, or a stock rack of jeans standing in for his line
— reads as false and undoes the credibility the rest of the page is working for. Better to
cut the slot than fake it.

**Cutting a slot is fine.** The layout does not collapse without any given chapter image;
delete the `<div class="slot">` and the chapter runs as a text block. Six strong images
beat eight where two are padding.

---

---

## Status — updated after Tony's photos arrived

**5 of 8 slots filled.** Originals preserved in `assets/images/_candidates/supplied/`
(renamed for legibility; `contact-sheet.jpg` shows all fifteen at a glance).

| Slot | Source | Native | Verdict |
|---|---|---|---|
| `year-of` | archived denim macro | 1681×596 | good |
| `portrait-studio` | `tony-barrel-gallery.jpg` | 886×886 → 709×886 | usable, not retina |
| `tonymagnetic` | `year-of-hoodie-gallery.jpg` | 886×886 → 886×498 | usable, not retina |
| `portrait-about` | `tony-hamachi-portrait.jpg` | 360×540 → 360×450 | soft at full width |
| `tony-only-tony` | `fedora-cream-blazer.jpg` | 360×480 → 360×450 | soft at full width |
| `hero` | — | — | **still needed, 2560px** |
| `mecca` | — | — | **still needed** |
| `munich` | — | — | **still needed** |

### The binding constraint is resolution

Almost everything supplied has been through social media and come back downscaled —
360px to 886px on the long edge. The slots want 1600px+. They render acceptably at the
sizes the layout uses, but they are not retina-sharp and they cannot be enlarged.

**The single highest-value thing Tony can send is the camera-roll originals of the photos
he already sent.** Same pictures, four to eight times the pixels. No new shoot required.

The one exception is `sushi-service-3024.jpg` at 3024×3024 — the only supplied file with
hero-grade resolution.

### Not used, and why

- `navy-suit-UNCONFIRMED.jpg` — a phone screenshot with letterbox bars, and I could not
  confirm the subject is Tony (short hair, no locs — possibly a different person or a much
  earlier photo). Identify before using.
- `kswiss-eagle-detail.jpg`, `kswiss-box-track.jpg` — strong product shots of what appears
  to be a The Year Of × K-Swiss collaboration. **There is no slot for this and no mention of
  it on the site.** See the open questions in the handover notes.
- `sushi-service-3024.jpg`, `hamachi-hunters-truck.jpg`, `hamachi-festival-group.jpg`,
  `tony-food-street.jpg` — the food venture, which the site does not currently cover at all.
- `desert-ridge-pair.jpg`, `year-of-sweatshirt-desert.jpg`, `bw-hat-trench.jpg`,
  `tony-temple-selfie.jpg` — good images with no slot that fits, or too small.

## Fourth batch — September 2026, product shots

Six files arrived in `assets/images/`; originals kept in
`_candidates/supplied-2026-09/`, working copies in `_src/` under slide keys. They are
product photography for three brands the site had not mentioned — **Jumpshot**
(hoodie, cap, tote), **Pitchers Only** (tour tee, lookbook frame) and **Northstar** (cap)
— so they run as extra frames in the TonyMagnetic INC chapter slideshow, each captioned
with the brand name and nothing more. **Confirm with Tony what his role was** (own label,
design, production?) before the copy says anything about them.

`pitchers-2.jpg` was a web banner with "Gamer Collection / Shop now" baked in; only the
left third (the model) is used. All six are 600–1600px, so they hold up in the slideshow
box but are not retina-sharp — camera-roll originals would fix that.

Four more lookbook stills (`dog-038`, `-061`, `-114`, `-134`) now back *The Year of…* as
slides. Mecca, Munich, Hong Kong, Maximal and Tony Only Tony are still single-frame:
the remaining candidates are either too small (360px) or their venue is unconfirmed.

## Turning files into site imagery

Once anything arrives:

```bash
tools/build-images.py --status
```

Shows what has landed and what is still outstanding. Then:

```bash
tools/build-images.py --apply
```

Crops each original to its slot ratio, generates AVIF, WebP and JPEG at 640 / 960 / 1440 /
1920 / 2560px, and replaces the placeholder in the HTML with a full `<picture>` element —
correct `srcset`, `sizes`, intrinsic `width`/`height` so nothing shifts while loading, lazy
loading everywhere except the hero. AVIF lands around a tenth of the JPEG size.

Build one slot at a time with `--only hero`.

### Off-centre subjects

Cropping defaults to the middle of the frame. If a subject sits off to one side and is
getting cut, add `assets/images/_src/focus.json`:

```json
{ "hero": [0.32, 0.45], "portrait-about": [0.5, 0.3] }
```

Values are 0–1 across the original frame — `[0, 0]` is top-left. The crop keeps that point
in view. Re-run the build after editing.

### Alt text

The script writes a serviceable default per slot. Once the real images are in, open
`tools/build-images.py` and rewrite the `alt=` strings in `SLOTS` to describe the actual
photographs, then re-run. Screen-reader users and search engines both read these.
