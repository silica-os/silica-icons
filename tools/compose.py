"""Composes layered icons as the shell would (body mask, layer order)
and writes a check sheet. Usage: python tools/compose.py [--dark] [--size N] [--out file.png]

The generic folder (`folder-symbol`) is composed with `compose_folder(dir, size, dark, symbol,
tint, full)`: back, middle (only when `full`), front, engraved symbol and tint, with the same
rules as the shell.
Badges (`badges/`) are placed on top of an already composed icon with `compose_badges(img, names, dark)`.
The generic file (`file-glyph`) is composed with `compose_file(dir, size, dark, ext, kind,
category)`: back, glyph (a symbol of the kind, or `app_icon`), front and the extension label.

Dependencies: pillow, resvg-py. The Inter font must be passed with --fonts if the SVGs contain text.
"""
import argparse
import io
import json
from pathlib import Path

import re

import numpy as np
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


def compose(icon_dir: Path, size: int, dark: bool, fonts: list[str]) -> Image.Image:
    manifest = json.loads((icon_dir / "icon.json").read_text())
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    for layer in manifest["layers"]:
        if layer.get("dynamic") or layer.get("when"):
            # Drawn by compose_file / compose_folder (glyph, middle sheet of a full folder).
            continue
        out.alpha_composite(render(layer_file(icon_dir, layer["file"], dark), size, fonts))
    dyn = manifest.get("dynamic") or {}
    if dyn.get("type") == "clock":
        for hand in dyn["hands"]:
            out.alpha_composite(render(layer_file(icon_dir, hand["file"], dark), size, fonts))
        out.alpha_composite(render(layer_file(icon_dir, dyn["cap"], dark), size, fonts))
    if manifest["kind"] == "app":
        out.putalpha(ImageChops.multiply(out.split()[3], body_mask(size)))
    return out


def render_string(svg: str, size: int, fonts: list[str]) -> Image.Image:
    data = resvg_py.svg_to_bytes(svg_string=svg, width=size, height=size, font_dirs=fonts)
    return Image.open(io.BytesIO(bytes(data))).convert("RGBA")


def folder_band(dyn: dict, side: float) -> dict | None:
    """The `symbol.sizes` band for an icon of side `side` (body, in pt): the first with
    `min_size` <= side; None below the last one (no symbol)."""
    for band in sorted(dyn["symbol"]["sizes"], key=lambda b: -b["min_size"]):
        if side >= band["min_size"]:
            return band
    return None


def tint_matrix(tint: str, ramp: dict) -> np.ndarray:
    """3 × 4 matrix (RGB → RGB + offset, values 0–1): the drawing's luminance goes from
    tint × shade (at luminance[0]) to the tint lightened toward white by glow (at luminance[1])."""
    t = np.array([int(tint[i:i + 2], 16) / 255 for i in (1, 3, 5)])
    shade = t * ramp["shade"]
    glow = t + (1 - t) * ramp["glow"]
    lo, hi = ramp["luminance"]
    k = (glow - shade) / (hi - lo)
    lum = np.array([0.2126, 0.7152, 0.0722])
    return np.column_stack([np.outer(k, lum), shade - k * lo])


def apply_tint(img: Image.Image, m: np.ndarray) -> Image.Image:
    a = np.asarray(img).astype(np.float64) / 255
    rgb = a[..., :3] @ m[:, :3].T + m[:, 3]
    a[..., :3] = np.clip(rgb, 0, 1)
    return Image.fromarray((a * 255 + 0.5).astype(np.uint8), "RGBA")


def compose_folder(icon_dir: Path, size: int, dark: bool, symbol: str | None = None,
                   tint: str | None = None, full: bool = False,
                   fonts: list[str] | None = None) -> Image.Image:
    """The generic folder at `size` px of canvas: back, middle sheet (only when `full`, the folder
    has items), front, engraved symbol (band chosen on the icon side, which for file icons is the
    full canvas) and tint. `tint` is a #rrggbb color or a label name; it recolours the layers
    with `"tint": true` and the symbol, never the middle sheet."""
    fonts = fonts or []
    manifest = json.loads((icon_dir / "icon.json").read_text())
    dyn = manifest["dynamic"]
    m = None
    if tint:
        m = tint_matrix(dyn["tint"]["labels"].get(tint, tint), dyn["tint"])
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    for layer in manifest["layers"]:
        if layer.get("when") == "not-empty" and not full:
            continue
        img = render(layer_file(icon_dir, layer["file"], dark), size, fonts)
        out.alpha_composite(apply_tint(img, m) if m is not None and layer.get("tint") else img)
    band = folder_band(dyn, size)
    sym_file = ROOT / "symbols" / (band or {}).get("weight", "regular") / f"{symbol}.svg"
    if symbol and band and sym_file.exists():
        fx = dyn["effect"]  # one engraving for every theme
        x, y, w, h = dyn["symbol"]["box"]
        sc = band["scale"]
        cx, cy = x + w / 2, y + h / 2
        w, h = w * sc, h * sc
        inner = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", sym_file.read_text(), flags=re.S)

        def layer(color: str, opacity: float, dy: float) -> str:
            return (f'<g opacity="{opacity}" transform="translate({cx - w / 2},{cy - h / 2 + dy}) '
                    f'scale({w / 24},{h / 24})">' + inner.replace("currentColor", color) + "</g>")

        glow = (layer(fx["highlight"], fx["highlight_opacity"], max(fx["offset"], 0.5 * 1024 / size))
                if band.get("highlight", True) else "")
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">'
               + glow + layer(fx["color"], fx["opacity"], 0) + "</svg>")
        sym = render_string(svg, size, fonts)
        out.alpha_composite(apply_tint(sym, m) if m is not None else sym)
    return out


INTER_ASCENT, INTER_LINE = 0.96875, 1.2102  # Inter hhea: 1984 / 2048 and (1984 + 494) / 2048


def inter_font(fonts: list[str]) -> Path | None:
    for d in [*fonts, str(Path.home() / "Library/Fonts"), "/usr/share/fonts"]:
        for f in sorted(Path(d).rglob("Inter*.ttf")) if Path(d).is_dir() else []:
            if "Italic" not in f.name:
                return f
    return None


def draw_label(out: Image.Image, label: dict, text: str, color: str, fonts: list[str]) -> None:
    """Writes `text` centered in the `box` (1024 canvas): a line of natural height (1.2102 × size)
    centered vertically; if wider than `max_width` the size shrinks proportionally."""
    from PIL import ImageFont
    path = inter_font(fonts)
    if path is None or not text:
        return
    ss = 4
    k = out.width / 1024 * ss
    size = label["size"]
    font = ImageFont.truetype(str(path), max(1, round(size * k)))
    font.set_variation_by_axes([14, label["weight"]])
    width = font.getlength(text) / k + label.get("tracking", 0) * (len(text) - 1)
    if width > label["max_width"]:
        size *= label["max_width"] / width
        font = ImageFont.truetype(str(path), max(1, round(size * k)))
        font.set_variation_by_axes([14, label["weight"]])
        width = font.getlength(text) / k
    x, y, w, h = label["box"]
    baseline = y + h / 2 - INTER_LINE * size / 2 + INTER_ASCENT * size
    layer = Image.new("RGBA", (out.width * ss, out.height * ss), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text(((x + w / 2 - width / 2) * k, baseline * k), text, font=font,
                               fill=color, anchor="ls")
    out.alpha_composite(layer.resize(out.size, Image.LANCZOS))


def glyph_band(bands: list[dict], side: float) -> dict | None:
    for band in sorted(bands, key=lambda b: -b["min_size"]):
        if side >= band["min_size"]:
            return band
    return None


def compose_file(icon_dir: Path, size: int, dark: bool, ext: str | None,
                 kind: str | None = None, category: str | None = None,
                 app_icon: Image.Image | None = None,
                 fonts: list[str] | None = None) -> Image.Image:
    """The generic file (`file-glyph`): back, the glyph between back and front, front, then the
    extension label. The glyph is `app_icon` (an already composed 1024 app icon, its 824 body
    fitted to `glyph.app_icon.body`) or the symbol of `kind` in its color; without either the
    label is written alone (`label_alone`, color of `category`). Without a usable extension and
    without a glyph, the `fallback` kind is used."""
    fonts = fonts or []
    manifest = json.loads((icon_dir / "icon.json").read_text())
    dyn = manifest["dynamic"]
    text = None
    if ext and len(ext) <= dyn["label"]["max_chars"]:
        text = ext.upper()
    if kind is None and app_icon is None and text is None:
        kind = dyn["fallback"]
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    color = None
    for layer in manifest["layers"]:
        if layer["role"] != "glyph":
            out.alpha_composite(render(layer_file(icon_dir, layer["file"], dark), size, fonts))
            continue
        px = size / 1024
        if app_icon is not None:
            bx, by, bw, _ = dyn["glyph"]["app_icon"]["body"]
            k = bw / 824
            side = max(1, round(1024 * k * px))
            out.alpha_composite(app_icon.resize((side, side), Image.LANCZOS),
                                (round((bx - 100 * k) * px), round((by - 100 * k) * px)))
        elif kind is not None:
            spec = dyn["kinds"][kind]
            color = spec["color"]
            band = glyph_band(dyn["glyph"]["symbol"]["sizes"], size)
            sym_file = ROOT / "symbols" / (band or {}).get("weight", "regular") / f"{spec['glyph']}.svg"
            if band and sym_file.exists():
                x, y, w, h = dyn["glyph"]["box"]
                inner = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", sym_file.read_text(), flags=re.S)
                svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">'
                       f'<g transform="translate({x},{y}) scale({w / 24},{h / 24})">'
                       + inner.replace("currentColor", color) + "</g></svg>")
                out.alpha_composite(render_string(svg, size, fonts))
    if text is None:
        return out
    if app_icon is None and kind is None:
        label = dyn["label_alone"]
        cat = dyn["overrides"].get(ext.lower(), category or "other")
        color = (cat if isinstance(cat, dict) else dyn["colors"][cat])["color"]
    else:
        label = dyn["label"]
        if color is None:
            cat = dyn["overrides"].get(ext.lower(), category or "other")
            color = (cat if isinstance(cat, dict) else dyn["colors"][cat])["color"]
    if size >= label.get("min_size", 0):
        draw_label(out, label, text, color, fonts)
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
