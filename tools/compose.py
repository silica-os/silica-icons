"""Composes layered icons as the shell would (body mask, layer order)
and writes a check sheet. Usage:
python tools/compose.py [--dark] [--appearance light|clear|tinted] [--accent #rrggbb] [--size N] [--out file.png]

App icons in format 2 (`icon.json` "format": 2, `layers/`) are composed in the four appearances of
docs/icon-format.md, Format 2 (light, dark, clear, tinted; `--dark` picks the dark form). Format 1 icons
are composed as before; `--appearance clear|tinted` does not apply to them (their clear and tinted
looks are the pre-rendered PNGs). The cast shadows and the rim are drawn by the icon service, not here.

Layered file icons (`files/file-generic`, `files/folder-generic`) are composited from their layers only, in
manifest order; the `when: not-empty` layer (folder `middle`) is drawn when `full=True`. Symbols, text and
tints belong to the thumbnail generator in silica-desktop.
Badges (`badges/`) are placed on top of an already composed icon with `compose_badges(img, names, dark)`.

Dependencies: pillow, resvg-py, numpy. The Inter font must be passed with --fonts if the SVGs contain text.
"""
import argparse
import io
import json
from pathlib import Path

import numpy as np
import resvg_py
from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
ACCENT = "#0e77e6"  # Accent/Amalfi


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


def compose(icon_dir: Path, size: int, dark: bool, fonts: list[str], full: bool = False,
            appearance: str = "light", accent: str = ACCENT, time: str | None = None) -> Image.Image:
    manifest = json.loads((icon_dir / "icon.json").read_text())
    if manifest.get("format") == 2:
        return compose2(icon_dir, manifest, size, appearance, dark, accent, time, fonts)
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


# Format 2 (docs/icon-format.md, Format 2). Images are float arrays, straight RGBA in 0..1.

GRAPHITE = ("#3a3a3c", "#141416")
ROLE_MODES = {  # role -> (clear, tinted, opacity factor of those modes)
    "body": ("ramp", "ramp", 1.0),
    "detail": ("ramp", "ramp", 1.0),
    "highlight": ("keep", "keep", 0.6),
    "dynamic": ("ramp", "ramp", 1.0),
}
GLASS = {"top": 0.85, "bottom": 0.55, "blur": 12.0}
TINT_DARKEN = 0.7  # tinted light ramp: L 0 is the accent mixed with black 70 % (as in tinted dark)


def hex_rgb(h: str) -> np.ndarray:
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])


def mix(a: np.ndarray, b: np.ndarray, t: float) -> np.ndarray:
    """a mixed with b at t (t = share of b)."""
    return a * (1 - t) + b * t


WHITE, BLACK = np.ones(3), np.zeros(3)


def to_linear(c: np.ndarray) -> np.ndarray:
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def to_srgb(c: np.ndarray) -> np.ndarray:
    c = np.clip(c, 0, None)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)


def oklab(rgb: np.ndarray) -> np.ndarray:
    r, g, b = np.moveaxis(to_linear(rgb), -1, 0)
    l = np.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b)
    m = np.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b)
    s = np.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b)
    return np.stack([0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
                     1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
                     0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s], -1)


def oklab_to_linear(lab: np.ndarray) -> np.ndarray:
    L, a, b = np.moveaxis(lab, -1, 0)
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return np.stack([4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
                     -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
                     -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s], -1)


def accent_map(L: np.ndarray, accent: np.ndarray) -> np.ndarray:
    """OKLCH(L, C of the accent, h of the accent), chroma reduced until the colour is in sRGB."""
    _, a, b = oklab(accent)
    lo, hi = np.zeros_like(L), np.ones_like(L)
    for _ in range(16):  # largest share of the accent chroma that stays in gamut
        mid = (lo + hi) / 2
        lin = oklab_to_linear(np.stack([L, a * mid, b * mid], -1))
        ok = np.all((lin >= -1e-4) & (lin <= 1 + 1e-4), -1)
        lo, hi = np.where(ok, mid, lo), np.where(ok, hi, mid)
    return to_srgb(np.clip(oklab_to_linear(np.stack([L, a * lo, b * lo], -1)), 0, 1))


def ramp(L: np.ndarray, stops: list[tuple[float, np.ndarray]]) -> np.ndarray:
    xs = [p for p, _ in stops]
    return np.stack([np.interp(L, xs, [c[i] for _, c in stops]) for i in range(3)], -1)


def over(dst: np.ndarray, src: np.ndarray, blend: str = "normal") -> np.ndarray:
    sa, da = src[..., 3:], dst[..., 3:]
    sc, dc = src[..., :3], dst[..., :3]
    if blend == "multiply":
        sc = mix(sc, sc * dc, da)
    elif blend == "screen":
        sc = mix(sc, 1 - (1 - sc) * (1 - dc), da)
    a = sa + da * (1 - sa)
    c = (sc * sa + dc * da * (1 - sa)) / np.maximum(a, 1e-9)
    return np.concatenate([c, a], -1)


def vertical(size: int, top: np.ndarray, bottom: np.ndarray, a_top: float = 1, a_bottom: float = 1) -> np.ndarray:
    """A body-high vertical gradient (y 100 -> 924 of the canvas) filling the canvas."""
    t = np.clip((np.arange(size) + 0.5 - 100 * size / 1024) / (824 * size / 1024), 0, 1)[:, None, None]
    rgb = top * (1 - t) + bottom * t
    a = a_top * (1 - t) + a_bottom * t
    return np.broadcast_to(np.concatenate([rgb, a], -1), (size, size, 4)).copy()


def as_array(img: Image.Image) -> np.ndarray:
    return np.asarray(img, dtype=np.float64) / 255


def to_image(arr: np.ndarray) -> Image.Image:
    return Image.fromarray(np.round(np.clip(arr, 0, 1) * 255).astype(np.uint8), "RGBA")


def background2(icon_dir: Path, spec: dict, size: int, appearance: str, dark: bool,
                accent: np.ndarray, fonts: list[str]) -> np.ndarray:
    if appearance == "light":
        b = spec.get("dark", {"gradient": list(GRAPHITE)}) if dark else spec["light"]
        if "file" in b:
            return as_array(render(icon_dir / b["file"], size, fonts))
        return vertical(size, hex_rgb(b["gradient"][0]), hex_rgb(b["gradient"][1]))
    if appearance == "clear":
        if dark:
            return vertical(size, hex_rgb(GRAPHITE[0]), BLACK, 0.50, 0.55)
        return vertical(size, WHITE, WHITE, 0.50, 0.25)
    if dark:  # tinted
        return vertical(size, mix(accent, BLACK, 0.62), mix(accent, BLACK, 0.84))
    return vertical(size, mix(accent, WHITE, 0.90), mix(accent, WHITE, 0.76))


def transform(px: np.ndarray, mode: str, appearance: str, dark: bool, accent: np.ndarray,
              luma: list | None) -> np.ndarray:
    """The per-appearance colour transform of one layer (alpha unchanged)."""
    if mode in ("keep", "glass") or appearance == "light":
        return px
    L = np.clip(oklab(px[..., :3])[..., 0], 0, 1)
    if appearance == "clear":
        if mode == "light":
            lo, hi = 200, 255
        else:
            lo, hi = luma or ((150, 255) if dark else (105, 255))
        rgb = np.repeat(((lo + (hi - lo) * L) / 255)[..., None], 3, -1)
    elif mode == "accent":
        rgb = accent_map(L, accent)
    elif mode == "light":
        ink = mix(accent, WHITE, 0.70) if dark else WHITE
        rgb = ink * ((200 + 55 * L) / 255)[..., None]
    else:  # tinted ramp
        if luma:
            L = luma[0] + (luma[1] - luma[0]) * L
        if dark:
            rgb = ramp(L, [(0, mix(accent, BLACK, 0.70)), (1, mix(accent, WHITE, 0.60))])
        else:
            rgb = ramp(L, [(0, mix(accent, BLACK, TINT_DARKEN)), (0.5, accent), (1, WHITE)])
    return np.concatenate([rgb, px[..., 3:]], -1)


def glass(below: np.ndarray, layer: np.ndarray, size: int, opacity: float, tune: dict) -> np.ndarray:
    """The layer as a translucent white glass piece over the blurred stack below it."""
    a = layer[..., 3:]
    rows = np.nonzero(a[..., 0].max(1) > 0)[0]
    if rows.size == 0:
        return below
    t = np.clip((np.arange(size) - rows[0]) / max(rows[-1] - rows[0], 1), 0, 1)[:, None, None]
    ga = (tune["top"] * (1 - t) + tune["bottom"] * t) * a * opacity
    sigma = tune["blur"] * size / 1024
    blurred = as_array(to_image(below).filter(ImageFilter.GaussianBlur(sigma)))
    out = below * (1 - a * opacity) + blurred * a * opacity
    out = over(out, np.concatenate([np.ones_like(a).repeat(3, -1), ga], -1))
    lip = max(1, round(4 * size / 1024))
    shifted = np.zeros_like(a)
    shifted[lip:] = a[:-lip]
    edge = np.clip(a - shifted, 0, 1) * opacity
    return over(out, np.concatenate([np.ones_like(a).repeat(3, -1), edge], -1))


def hand_angle(unit: str, time: str) -> float:
    h, m, s = (int(x) for x in time.split(":"))
    return {"hour": (h % 12 + m / 60 + s / 3600) * 30, "minute": (m + s / 60) * 6, "second": s * 6}[unit]


def compose2(icon_dir: Path, manifest: dict, size: int, appearance: str, dark: bool, accent_hex: str,
             time: str | None, fonts: list[str]) -> Image.Image:
    """A format 2 app icon in one appearance (light, clear, tinted; `dark` for the dark form)."""
    accent = hex_rgb(accent_hex)
    time = time or manifest.get("fallback", {}).get("time", "10:09:30")
    out = background2(icon_dir, manifest["background"], size, appearance, dark, accent, fonts)
    for layer in manifest["layers"]:
        lay = dict(layer)
        if dark:
            over_dark = layer.get("dark", {})
            for k, v in over_dark.items():
                lay[k] = {**layer.get(k, {}), **v} if k in ("clear", "tinted") else v
        if lay.get("min_size", 0) > size:
            continue
        role_clear, role_tinted, role_factor = ROLE_MODES[lay["role"]]
        opacity = lay.get("opacity", 1.0)
        mode, luma = "keep", None
        if appearance in ("clear", "tinted"):
            spec = lay.get(appearance, {})
            mode = spec.get("mode", role_clear if appearance == "clear" else role_tinted)
            factor = role_factor if "mode" not in spec else 1.0
            opacity *= spec.get("opacity", factor)
            luma = spec.get("luma")
        if mode == "hide":
            continue
        file = lay.get("file")
        if not file:
            dark_file = f"layers/{lay['id']}-dark.svg"
            file = dark_file if dark and (icon_dir / dark_file).exists() else f"layers/{lay['id']}.svg"
        img = render(icon_dir / file, size, fonts)
        px = transform(as_array(img), mode, appearance, dark, accent, luma)
        dyn = lay.get("dynamic") or {}
        if dyn.get("kind") == "clock-hand":
            cx, cy = (v * size / 1024 for v in dyn.get("pivot", [512, 512]))
            px = as_array(to_image(px).rotate(-hand_angle(dyn["unit"], time), Image.BICUBIC, center=(cx, cy)))
        if mode == "glass":
            out = glass(out, px, size, opacity, {**GLASS, **manifest.get("glass", {})})
            continue
        px = px.copy()
        px[..., 3] *= opacity
        out = over(out, px, lay.get("blend", "normal"))
    img = to_image(out)
    img.putalpha(ImageChops.multiply(img.split()[3], body_mask(size)))
    return img


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
    ap.add_argument("--appearance", choices=["light", "clear", "tinted"], default="light",
                    help="format 2 app icons only; light with --dark is the dark appearance")
    ap.add_argument("--accent", default=ACCENT, help="tinted accent, default Accent/Amalfi")
    ap.add_argument("--time", default=None, help="clock hands as h:m:s, default the fallback pose")
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
        sheet.alpha_composite(compose(d, a.size, a.dark, a.fonts, appearance=a.appearance, accent=a.accent, time=a.time), (x, y))
        draw.text((x, y + a.size + 4), d.name, fill=(255, 255, 255, 255) if a.dark else (40, 40, 44, 255))
    out = ROOT / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(out)


if __name__ == "__main__":
    main()
