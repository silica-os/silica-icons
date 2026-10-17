"""Composes layered icons as the shell would (body mask, layer order)
and writes a check sheet. Usage: python tools/compose.py [--dark] [--size N] [--out file.png]

Layered file icons (`files/file-generic`, `files/folder-generic`) are composited from their layers only, in
manifest order; the `when: not-empty` layer (folder `middle`) is drawn when `full=True`. Symbols, text and
tints belong to the thumbnail generator in silica-desktop.
Badges (`badges/`) are placed on top of an already composed icon with `compose_badges(img, names, dark)`.

Dependencies: pillow, resvg-py. The Inter font must be passed with --fonts if the SVGs contain text.
"""
import argparse
import io
import json
from pathlib import Path

import resvg_py
from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parent.parent


def render(path: Path, size: int, fonts: list[str]) -> Image.Image:
    data = resvg_py.svg_to_bytes(svg_path=str(path), width=size, height=size, font_dirs=fonts)
    return Image.open(io.BytesIO(bytes(data))).convert("RGBA")


def body_mask(size: int) -> Image.Image:
    # Approximation with a rounded rectangle; the shell uses the superellipse from the spec.
    m = Image.new("L", (size, size), 0)
    s = size / 1024
    ImageDraw.Draw(m).rounded_rectangle((100 * s, 100 * s, 924 * s, 924 * s), radius=215 * s, fill=255)
    return m


def layer_file(icon_dir: Path, name: str, dark: bool) -> Path:
    if dark:
        stem, ext = name.rsplit(".", 1)
        candidate = icon_dir / f"{stem}-dark.{ext}"
        if candidate.exists():
            return candidate
    return icon_dir / name


def compose(icon_dir: Path, size: int, dark: bool, fonts: list[str], full: bool = False) -> Image.Image:
    manifest = json.loads((icon_dir / "icon.json").read_text())
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    for layer in manifest["layers"]:
        if layer.get("when") == "not-empty" and not full:
            continue  # middle sheet: only for a folder with items
        out.alpha_composite(render(layer_file(icon_dir, layer["file"], dark), size, fonts))
    dyn = manifest.get("dynamic") or {}
    if dyn.get("type") == "clock":
        for hand in dyn["hands"]:
            out.alpha_composite(render(layer_file(icon_dir, hand["file"], dark), size, fonts))
        out.alpha_composite(render(layer_file(icon_dir, dyn["cap"], dark), size, fonts))
    if manifest["kind"] == "app":
        out.putalpha(ImageChops.multiply(out.split()[3], body_mask(size)))
    return out


def compose_badges(icon: Image.Image, names: list[str], dark: bool,
                   fonts: list[str] | None = None) -> Image.Image:
    """The badges `names` (alias, locked, unreadable, cloud) on top of the composed icon `icon`
    (square canvas): one per corner, chosen by priority; badge side from the `sizes` band
    (icon side in pt: for file icons the full canvas); in the `single` band only one, the first of
    `order`; no badge below the last band."""
    spec = json.loads((ROOT / "badges" / "badges.json").read_text())
    size = icon.width
    side = size
    band = next((b for b in sorted(spec["sizes"], key=lambda b: -b["min_size"]) if side >= b["min_size"]), None)
    out = icon.copy()
    if band is None:
        return out
    if band.get("single"):
        names = [n for n in spec["order"] if n in names][:1]
    chosen: dict[str, tuple[int, str]] = {}
    for name in names:
        b = spec["badges"].get(name)
        if b and (b["corner"] not in chosen or b["priority"] < chosen[b["corner"]][0]):
            chosen[b["corner"]] = (b["priority"], name)
    bx, by, bw, bh = spec["body"]
    for corner, (_, name) in chosen.items():
        b = spec["badges"][name]
        side_c = bw * band["fraction"]
        ax, ay = spec["corners"][corner]
        x0 = ax if ax <= bx else ax - side_c
        y0 = ay if ay <= by else ay - side_c
        k = side_c / bw
        px = size / 1024
        layer = render(ROOT / "badges" / (b["dark"] if dark else b["file"]), max(1, round(1024 * k * px)), fonts or [])
        out.alpha_composite(layer, (round((x0 - bx * k) * px), round((y0 - by * k) * px)))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dark", action="store_true")
    ap.add_argument("--size", type=int, default=192)
    ap.add_argument("--fonts", action="append", default=[])
    ap.add_argument("--out", default="build/contact-sheet.png")
    a = ap.parse_args()
    dirs = sorted(p.parent for p in ROOT.glob("*/*/icon.json"))
    cols = 8
    cell = a.size + 24
    rows = (len(dirs) + cols - 1) // cols
    bg = (40, 40, 44, 255) if a.dark else (236, 236, 240, 255)
    sheet = Image.new("RGBA", (cols * cell, rows * (cell + 16)), bg)
    draw = ImageDraw.Draw(sheet)
    for i, d in enumerate(dirs):
        x, y = (i % cols) * cell + 12, (i // cols) * (cell + 16) + 8
        sheet.alpha_composite(compose(d, a.size, a.dark, a.fonts), (x, y))
        draw.text((x, y + a.size + 4), d.name, fill=(255, 255, 255, 255) if a.dark else (40, 40, 44, 255))
    out = ROOT / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(out)


if __name__ == "__main__":
    main()
