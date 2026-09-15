#!/usr/bin/env python3
"""
Turn the photos Tony sends into responsive site imagery.

    tools/build-images.py --status     what's supplied, what's still missing
    tools/build-images.py              build derivatives from assets/images/_src/
    tools/build-images.py --apply      build, then swap the placeholders in the HTML

Drop originals into assets/images/_src/ named after the slot key, any format,
as large as they came:  hero.jpg, mecca.png, portrait-studio.jpeg, ...

Outputs assets/images/<key>-<width>.{avif,webp,jpg} plus <picture> markup.
Needs Pillow (jpg/webp) and ffmpeg (avif). Missing ffmpeg just skips avif.
"""

import argparse, json, re, shutil, subprocess, sys
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "images" / "_src"
OUT = ROOT / "assets" / "images"
FOCUS_FILE = SRC / "focus.json"

WIDTHS = [640, 960, 1440, 1920, 2560]

# key -> how it is used. `match` lists the exact data-slot strings in the HTML.
SLOTS = {
    "hero": dict(
        ratio=None, sizes="100vw", cover=True,
        alt="Tony Magnetic in Tokyo, 2006",
        match=["Hero image — portrait or campaign shot, 2560px wide"],
    ),
    "mecca": dict(
        ratio=(16, 9), sizes="(max-width: 64rem) 100vw, 86rem",
        alt="Tony Magnetic at the Agenda trade show, New York, 2014",
        match=["Mecca USA — archive campaign or product shot",
               "Mecca USA — archive campaign, 1995–96"],
    ),
    "munich": dict(
        ratio=(4, 5), sizes="(max-width: 64rem) 100vw, 62rem",
        alt="Marienplatz, Munich",
        match=["Munich — store interior or streetwear editorial",
               "Munich — retail space or product wall"],
    ),
    "year-of": dict(
        ratio=(3, 2), sizes="(max-width: 64rem) 100vw, 62rem",
        alt="Gold and silver selfedge on The Year of… denim",
        match=["“The Year of…” — denim detail, selvage or hardware",
               "“The Year of…” — denim detail, hardware or selvage"],
    ),
    "tony-only-tony": dict(
        ratio=(4, 5), sizes="(max-width: 64rem) 100vw, 62rem",
        alt="Tony Only Tony garment",
        match=["Tony Only Tony — label or garment shot"],
    ),
    "tonymagnetic": dict(
        ratio=(16, 9), sizes="(max-width: 64rem) 100vw, 86rem",
        alt="TonyMagnetic INC collection",
        match=["TonyMagnetic INC — current collection lookbook"],
    ),
    "hongkong": dict(
        ratio=(16, 9), sizes="(max-width: 64rem) 100vw, 86rem",
        alt="A Hong Kong street, photographed for The Year of…",
        match=["Hong Kong — street or skyline"],
    ),
    "maximal": dict(
        ratio=(3, 2), sizes="(max-width: 64rem) 100vw, 62rem",
        alt="Hong Kong at night",
        match=["Maximal Concepts — hospitality work"],
    ),
    "portrait-studio": dict(
        ratio=(4, 5), sizes="(max-width: 64rem) 100vw, 38rem",
        alt="Tony Magnetic in the studio",
        match=["Portrait — Tony in the studio"],
    ),
    "portrait-about": dict(
        ratio=(4, 5), sizes="(max-width: 64rem) 100vw, 38rem",
        alt="Tony Magnetic",
        match=["Portrait — Tony, present day"],
    ),
    # Extra slides for the chapter slideshows. All 3:2 — the slideshow box is
    # 16:10 on desktop and 4:5 on phones, and object-fit does the rest.
    "year-of-embroidery": dict(
        ratio=(3, 2), sizes="(max-width: 64rem) 100vw, 86rem",
        alt="White foliate embroidery across the back pocket of The Year of… jeans",
        match=["Slide — year-of-embroidery"],
    ),
    "year-of-patch": dict(
        ratio=(3, 2), sizes="(max-width: 64rem) 100vw, 86rem",
        alt="The Year of… leather patch, Year of the Dog, on raw selvage denim",
        match=["Slide — year-of-patch"],
    ),
    "year-of-cans": dict(
        ratio=(3, 2), sizes="(max-width: 64rem) 100vw, 86rem",
        alt="The Year of… flame-embroidered jeans, shot against gold cans, 2006",
        match=["Slide — year-of-cans"],
    ),
    "year-of-pocket": dict(
        ratio=(3, 2), sizes="(max-width: 64rem) 100vw, 86rem",
        alt="Folded pair of The Year of… jeans with gold-embroidered pocket",
        match=["Slide — year-of-pocket"],
    ),
    "pitchers-only-lookbook": dict(
        ratio=(3, 2), sizes="(max-width: 64rem) 100vw, 86rem",
        alt="Pitchers Only Shove Day tee, worn with a catcher's mitt",
        match=["Slide — pitchers-only-lookbook"],
    ),
    "jumpshot-hoodie": dict(
        ratio=(3, 2), sizes="(max-width: 64rem) 100vw, 86rem",
        alt="Jumpshot hoodie, front and back, washed black with arched logo and Call Game script",
        match=["Slide — jumpshot-hoodie"],
    ),
    "pitchers-only-tee": dict(
        ratio=(3, 2), sizes="(max-width: 64rem) 100vw, 86rem",
        alt="Pitchers Only Electrix Tour 2026 tee, acid-washed grey",
        match=["Slide — pitchers-only-tee"],
    ),
    "jumpshot-cap": dict(
        ratio=(3, 2), sizes="(max-width: 64rem) 100vw, 86rem",
        alt="Jumpshot washed cotton cap with outlined arch logo",
        match=["Slide — jumpshot-cap"],
    ),
    "northstar-cap": dict(
        ratio=(3, 2), sizes="(max-width: 64rem) 100vw, 86rem",
        alt="Northstar navy cap with embroidered star emblem",
        match=["Slide — northstar-cap"],
    ),
    "jumpshot-tote": dict(
        ratio=(3, 2), sizes="(max-width: 64rem) 100vw, 86rem",
        alt="Jumpshot canvas tote, Call Game print",
        match=["Slide — jumpshot-tote"],
    ),
}

PAGES = ["index.html", "work.html", "about.html", "contact.html"]
HAVE_FFMPEG = shutil.which("ffmpeg") is not None


def find_source(key):
    for p in sorted(SRC.glob(f"{key}.*")):
        if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp", ".heic"}:
            return p
    return None


def load_focus():
    if FOCUS_FILE.exists():
        try:
            return json.loads(FOCUS_FILE.read_text())
        except json.JSONDecodeError as e:
            sys.exit(f"focus.json is not valid JSON: {e}")
    return {}


def crop_to_ratio(im, ratio, focus):
    """Crop to `ratio`, keeping the focal point (fx, fy in 0..1) in frame."""
    tw, th = ratio
    target = tw / th
    w, h = im.size
    current = w / h
    fx, fy = focus
    if abs(current - target) < 1e-6:
        return im
    if current > target:                       # too wide -> trim sides
        new_w = round(h * target)
        left = round(fx * w - new_w / 2)
        left = max(0, min(left, w - new_w))
        return im.crop((left, 0, left + new_w, h))
    new_h = round(w / target)                  # too tall -> trim top/bottom
    top = round(fy * h - new_h / 2)
    top = max(0, min(top, h - new_h))
    return im.crop((0, top, w, top + new_h))


def encode_avif(jpg_path, avif_path):
    r = subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(jpg_path),
         "-c:v", "libaom-av1", "-crf", "32", "-cpu-used", "6",
         "-still-picture", "1", "-pix_fmt", "yuv420p", str(avif_path)],
        capture_output=True, text=True)
    if r.returncode != 0:
        print(f"      avif failed: {r.stderr.strip().splitlines()[-1:] or '?'}")
        return False
    return True


def build(key, spec, focus_map, quiet=False):
    src = find_source(key)
    if not src:
        return None
    im = Image.open(src)
    im = ImageOps.exif_transpose(im)           # honour camera rotation
    if im.mode not in ("RGB", "L"):
        im = im.convert("RGB")

    focus = focus_map.get(key, [0.5, 0.5])
    if spec["ratio"]:
        im = crop_to_ratio(im, spec["ratio"], focus)

    natural_w, natural_h = im.size
    widths = [w for w in WIDTHS if w <= natural_w] or [natural_w]
    if natural_w not in widths and natural_w < max(WIDTHS):
        widths.append(natural_w)
    widths = sorted(set(widths))

    made = []
    for w in widths:
        h = round(im.height * w / im.width)
        resized = im.resize((w, h), Image.LANCZOS)
        jpg = OUT / f"{key}-{w}.jpg"
        webp = OUT / f"{key}-{w}.webp"
        avif = OUT / f"{key}-{w}.avif"
        resized.save(jpg, "JPEG", quality=82, optimize=True, progressive=True)
        resized.save(webp, "WEBP", quality=80, method=6)
        ok_avif = encode_avif(jpg, avif) if HAVE_FFMPEG else False
        made.append((w, h, ok_avif))
        if not quiet:
            print(f"      {w:>5}px  jpg {jpg.stat().st_size//1024:>4}KB   "
                  f"webp {webp.stat().st_size//1024:>4}KB"
                  + (f"   avif {avif.stat().st_size//1024:>4}KB" if ok_avif else ""))

    biggest = max(made)[0]
    ref_h = round(natural_h * biggest / natural_w)
    return dict(widths=[m[0] for m in made], avif=all(m[2] for m in made),
                width=biggest, height=ref_h, source=src.name)


def picture_markup(key, spec, info, indent):
    pad = " " * indent
    def srcset(ext):
        return ", ".join(f"assets/images/{key}-{w}.{ext} {w}w" for w in info["widths"])
    sizes = spec["sizes"]
    lines = [f"{pad}<picture>"]
    if info["avif"]:
        lines.append(f'{pad}  <source type="image/avif" srcset="{srcset("avif")}" sizes="{sizes}">')
    lines.append(f'{pad}  <source type="image/webp" srcset="{srcset("webp")}" sizes="{sizes}">')
    extra = ' fetchpriority="high"' if key == "hero" else ' loading="lazy" decoding="async"'
    lines.append(
        f'{pad}  <img src="assets/images/{key}-{info["widths"][-1]}.jpg" '
        f'srcset="{srcset("jpg")}" sizes="{sizes}" '
        f'width="{info["width"]}" height="{info["height"]}" '
        f'alt="{spec["alt"]}"{extra}>')
    lines.append(f"{pad}</picture>")
    return "\n".join(lines)


def apply_to_html(built):
    changed = {}
    for page in PAGES:
        path = ROOT / page
        html = path.read_text()
        original = html
        for key, info in built.items():
            spec = SLOTS[key]
            for label in spec["match"]:
                pattern = re.compile(
                    r'([ \t]*)<div class="slot" data-slot="'
                    + re.escape(label) + r'"[^>]*></div>')
                def repl(m):
                    return picture_markup(key, spec, info, len(m.group(1)))
                html, n = pattern.subn(repl, html)
                if n:
                    changed.setdefault(page, []).append(f"{key} ×{n}")
        if html != original:
            path.write_text(html)
    return changed


def status():
    print(f"\n  {'slot':<18} {'ratio':<8} {'source':<28} state")
    print("  " + "-" * 72)
    missing = []
    for key, spec in SLOTS.items():
        src = find_source(key)
        ratio = f'{spec["ratio"][0]}:{spec["ratio"][1]}' if spec["ratio"] else "cover"
        if src:
            im = Image.open(src)
            state = f"{im.width}×{im.height}"
            if im.width < 1600:
                state += "  (small — 2000px+ preferred)"
        else:
            state = "MISSING"
            missing.append(key)
        print(f"  {key:<18} {ratio:<8} {(src.name if src else '—'):<28} {state}")
    print(f"\n  {len(SLOTS) - len(missing)}/{len(SLOTS)} supplied.")
    if missing:
        print("  still needed: " + ", ".join(missing))
    print()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--status", action="store_true", help="report what's supplied")
    ap.add_argument("--apply", action="store_true", help="rewrite the HTML placeholders")
    ap.add_argument("--only", help="build a single slot key")
    args = ap.parse_args()

    SRC.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    if args.status:
        status()
        return

    if not HAVE_FFMPEG:
        print("  note: ffmpeg not found — skipping AVIF, jpg + webp only.\n")

    focus_map = load_focus()
    keys = [args.only] if args.only else list(SLOTS)
    built = {}
    for key in keys:
        if key not in SLOTS:
            sys.exit(f"unknown slot '{key}'. known: {', '.join(SLOTS)}")
        src = find_source(key)
        if not src:
            print(f"  ·  {key:<18} no source in assets/images/_src/ — skipped")
            continue
        print(f"  ▸  {key:<18} from {src.name}")
        info = build(key, SLOTS[key], focus_map)
        if info:
            built[key] = info

    if not built:
        print("\n  Nothing built. Put originals in assets/images/_src/ named after the")
        print("  slot keys, then run again.  tools/build-images.py --status\n")
        return

    print(f"\n  Built {len(built)} image set(s).")

    if args.apply:
        changed = apply_to_html(built)
        if changed:
            print("\n  HTML updated:")
            for page, keys_ in changed.items():
                print(f"    {page}: {', '.join(keys_)}")
        else:
            print("\n  No placeholders matched — already replaced?")
    else:
        print("\n  Markup (or re-run with --apply to insert it automatically):\n")
        for key, info in built.items():
            print(picture_markup(key, SLOTS[key], info, 8))
            print()


if __name__ == "__main__":
    main()
