# Icon format

Version 1. Applies to `apps/`, `files/` and `badges/`. System symbols (`symbols/`) have a
separate specification.

## Principle

An app icon is **layered content**, not a finished image. The developer supplies the
background and the foreground; the shell applies the shape, border, shadows, glass and
themes. This way every Dock icon has the same shape and reacts to the same themes.

File icons (`files/`), instead, are free-form objects (folders, documents, Trash): the shell
applies no mask or body, only the shadow of the context. For file icons **the side is the
full canvas**: a 64 pt file icon is the 1024 canvas drawn at 64 pt, with no reductions (no
824 body, no factors like the former 92 %); the bands that depend on the side (`min_size` of
the folder symbol, of the label and of the badges) are compared with this side. In the Dock a
place (folder, Trash) uses the canvas of the neighboring apps, the one that overflows the body
by 100/824.

## Canvas and grid

All measures are on a **1024 × 1024** canvas.

| Element | Measure |
| --- | --- |
| Body (where the shell clips) | 824 × 824 at (100, 100) |
| Body corners | smooth, radius 215, smoothing 0.55 |
| Square keyline | 600 × 600 at (212, 212) |
| Large circle keyline | Ø 600, center (512, 512) |
| Small circle keyline | Ø 424, center (512, 512) |
| Vertical keyline | 520 × 680 at (252, 172) |
| Horizontal keyline | 680 × 520 at (172, 252) |
| Document keyline (file icons) | 684 × 904 at (170, 60) |
| Folder keyline | 956 × 776 at (34, 116) (Amalfi folder, 2026-10-17; the proportions below derive the former 944 × 760 at (40, 132)) |
| Volume keyline (disks and servers) | 944 × 583 at (40, 220.4) |
| Trash keyline | 656 × 824 at (184, 100): bin with the base at y 924, rim 667 |
| Badge | Ø 824 disc centered on its own 1024 canvas (see Badges) |

The main content sits in one of the keylines; full-canvas icons (a drawn background, like
Calendar or Photos) fill the whole body.

## Proportion system (φ = 1.618)

It is the symbol system ([`symbol-format.md`](symbol-format.md)) scaled to the 1024 canvas
with **1 u = 30 px**: the Ø 600 circle keyline is the Ø 20 u circle of the symbols, the
Regular stroke (1.5 u) is 45 px. In `design/app-icons.sketch` the symbol `Grid / Golden 1024`
(light blue) draws it over `Grid / Overlay` (pink): Grid page and `Golden overlay` layer in
every Grid Check artboard.

### The existing keylines

| Keyline | Where it comes from |
| --- | --- |
| Body 824 | canvas − 2 × 100; radius 215 ≈ 0.26 × side (smoothing 0.55) |
| Square and circle 600 | base quantity (20 u) |
| Circle 424 | 600 / √2: circle inscribed in the square inscribed in the 600 circle |
| Vertical 520 × 680, horizontal 680 × 520 | same perimeter as the 600 square (520 + 680 = 2 × 600), area 98 %; ratio 1.31, not golden |
| Document 684 × 904, folder 944 × 760 | measured in the reference file manager at large icons (1× capture, 128 pt icons): sheet body 86 × 114 (0.668 × 0.883 of the canvas, without the ≈ 5 pt per side shadow that the shell adds; 96 × 124 with the shadow), folder 118 × 94 (0.922 × 0.734); at 64 pt 42 × 56 and 59 × 47, same ratios. The sheet is the earlier drawing (648 × 824) scaled by 904 / 824 = 1.0971 around the center and narrowed in width to 684 (measured ratio 1.32, no longer √φ): lines, figures and extensions scale by 1.0971 without distortion, only the outline and the fold follow the width. The folder is the earlier one (824 × 663) scaled by 944 / 824 = 1.1456 around the center: 944 × 760 against 944 × 752 measured (1 %, within tolerance). In the Dock the folder measures 1.13 times the body of the neighboring apps (54 against 48 px at 2×), that is 0.905 of the canvas: matches 944 / 1024 |
| Volume 944 × 583 | the earlier slab (824 × 509: long side the body, short side 824 / φ, front band 509 / φ² from y 572) scaled by 1.1456 around the center like the folder: the reference volume icon is an upright box (0.71 × 0.86 of the canvas on the Desktop), a different shape from the slab, so it is not measured directly; front band 222.8 from y 580.7 |
| Optical disc Ø 944 | Ø 824 scaled like the folder; stop zone Ø 361, inner ring Ø 264, hole Ø 128 (the earlier measures × 1.1456) |
| Trash 656 × 824 | measured in the Dock (2× capture): the bin is as tall as the app body (49 against 48 px) and rests on the same base, 0.86 of the body wide; with the sheets inside it is 1.10 of the body tall. The earlier drawing (584 × 734, base at 914) is scaled by 824 / 734 = 1.1226 and the base moved to 924: bin 656 × 824 (rim 667), with the sheets 913 (1.11 of the body); it stays narrower than the reference (0.81 of the body) because the shape is our own |
| Badge 315 and 509 | body / φ² and body / φ: the badge box goes from the edge of the body to the golden line (x and y 415 and 609) |

All of them remain: the golden system completes them, it does not replace them.

### Quantities

| Quantity | Values | Use |
| --- | --- | --- |
| Series A (from the keyline) | **600 · 371 · 229 · 142 · 87 · 54** (600 / φⁿ); intermediate √φ steps: 472 · 292 · 180 · 112 · 69 | sides and diameters of the main pieces |
| Series B (from the body) | 824 · 509 · 315 · 194 | pieces measured on the body (Photo Viewer lens 316, Mail paper 508, Mustache mustache 522 within tolerance) |
| Rectangles | golden 600 × 371 (wide, at (212, 326.5)) and 371 × 600 (tall); √2 (424 × 300); horizontal and vertical keylines | cards, screens, photos, disks |
| Golden lines of the body | x and y = 415 and 609 (100 + 824 / φ² and 100 + 824 / φ) | dividers, horizons, off-center pieces |
| Thicknesses | 13.5 · 17 · 22 · 28 · 35 · 45 · 57 (45 × √φⁿ, like the symbol weights) | text lines, outlines, hands, stems, handles |
| Gaps between repeated pieces | equal to the thickness (1 : 1) for dense lines (Mail, Terminal, files); thickness × φ for airy text (Text Editor); piece / φ² or piece / φ³ between tiles and keys | rhythm |
| Radii | 215 · 169 · 133 · 104 · 82 · 64 · 51 · 40 · 31 · 25 · 19 · 15 (215 / √φⁿ); capsule = half the height; nested piece = outer radius − distance | corners |
| Center | footprint of the foreground centered on (512, 512) | composition |

Allowed internal ratios: φ, √φ, √2, 1 : 1, 1 : 2. Tolerance: a measure complies with the
system if it is within 3 % of the quantity or within 4 px. The lengths of individual text
lines and the positions of illustrative details are not constrained.

Deliberate exceptions:

- file icons come out of the app body and fill almost the whole canvas, as in the
  reference (see The existing keylines): sheet 684 × 904 from (170, 60), folder 944 × 760 from
  (40, 132), both centered on (512, 512). History: the starting drawing (sheet 520 × 680,
  folder 680 × 520) was brought to the 824 body (sheet 648 × 824 at the √φ ratio, folder
  824 × 663), then to the full canvas with the file manager measures (v0.2.0). The sheet content is
  centered on y 469 (473 before), above the extension; the front panel of the folder is
  944 × 619 from y 273.1 (0.815 of the height; in the reference 0.82);
- the Trash is 656 wide (rim 667) and 824 tall, with the bin base at y 924, on the bottom of the
  app body: in the Dock it rests on the same line and has the same height;
- the fold of the sheets (174 × 176: the earlier 165 × 160, scaled in width by 684 / 648 and in
  height by 904 / 824) is not on the series: changing it means redrawing the path of every
  sheet; it stays until the sheets are redrawn;
- the Trash is neither sheet nor folder: it has its own keyline, measured in the Dock;
- Stack Close (the Dock button that closes an open stack) is in `badges/` as `stack-close`
  (badges.json → `dock`): the same disc and material as the file badges, with a cross;
- the file types added for Mustache (spreadsheet, presentation, font, disk image, executable,
  document, web page) have the figure in the 461 × 292 box centered on
  (512, 473), like Code and Image (the width of the text lines of the sheets, 461 ≈ 472 within
  tolerance; 292 series A); the spreadsheet table has gaps of 13.5, the slide is
  461 × 285 (ratio φ), the globe Ø 292 with meridians of 13.5, "Aa" is Inter SemiBold in
  outlines with capital height 292, the disk of the disk image is 461 × 229 (series A).
  These measures are on the 824 sheet and in the SVGs they all scale by 1.0971 around (512, 512)
  (box 506 × 320 centered on (512, 469));
- volumes are 824 × 509 slabs with radius 64 and the server is three units 155 tall with gaps
  of 22, on the 824 drawing; in the SVGs they scale by 1.1456 around the center (slab 944 × 583,
  radius 73).

In the SVGs the scale is in a single attribute: `transform` on the `icon` group (`icon-dark`)
for folders, volumes and Trash; for the sheets the group scales everything by 1.0971 and the
outline (`Page`) and the fold (`Corner`) additionally have a horizontal reduction of 684 / 711
around the axis of the sheet. The paths stay those of the 824 drawing.

### Optical corrections and deviations from the pure ratio

| Icon | Pure ratio | Chosen | Reason |
| --- | --- | --- | --- |
| Clock | dial on the Ø 600 keyline | full body (ticks up to Ø 740) | a small clock in the white body loses legibility; the numbers sit on Ø 480 ≈ 472 |
| Fonts | capitals block centered on y 512 | 335…655 (center 495) | optical center above the geometric one; in x the glyph footprint is centered on 512 |
| Help | question mark centered on its footprint | center x 508 | the mass of the curl is on the right |
| Calendar | disc Ø 472 | Ø 460 (within tolerance) | the base of the disc stays on the 812 keyline and the month–disc gap at 54 |
| Text Editor | centered composition | sheet at x 248…736, pen diagonal up to x 905 | the pen is the second subject; it stays inside the body |
| Store, padlock | center of the footprint on the center | center on 512 with the handle included | bag and padlock have the same base (794) |
| Mustache | foreground in a keyline | profile flush with the body (margin 64), glasses from x 182 to 842, lenses Ø 229 (stroke 22) centered on the golden line y 415, mustache 522 wide | full-canvas portrait: the profile follows the corners of the body |

## Folder of an icon

```
apps/<id>/
  icon.json              manifest
  background.svg         background (1024 canvas, fills at least the body)
  foreground.svg         foreground (1024 canvas)
  background-dark.svg    optional: background for dark themes
  foreground-dark.svg    optional: foreground for dark themes
  preview.png            256 px preview of the Default theme, composed (documentation only)
```

`<id>` is lowercase with hyphens (`text-editor`). All SVGs have
`viewBox="0 0 1024 1024"`; coordinates are those of the canvas, so the layers
overlap without offsets.

### What does NOT go in the layers

The shell adds these by itself; if they are present, the result doubles:

- the body mask and its luminous border (the "Rim"): a reflection along the body's edge, drawn by
  the shell at the icon's width, with a vertical alpha gradient from top to bottom: light `0x40` → `0x0D`,
  dark `0x20` → `0x08` (user decision 2026-10-16: half of the earlier `0x80` → `0x1A` and `0x40` → `0x0F`;
  silica-ui 3c82c30b);
- the shadow of the foreground on the background and the shadow of the icon on the Dock;
- the glass blur and the reflection of the Clear themes.

Shadows and gradients **internal** to the drawing (between two parts of the foreground) are
part of the illustration and stay.

This also holds for `file` icons: all of them (sheets, folders, Trash, volumes and badges) are
**flat**, only fills, internal gradients and a thin outline of the sheet or slab, with no
ground shadow and no external or internal shadows made with filters: the context shadow is
added by the shell (IC-01). There is no `filter` in the SVGs of `files/`. The sheets, folders
and Trash drawn before the file types for Mustache had the ground shadow and the shadows of
the pieces: they were flattened with the same rule, without changing shape, colors or
proportions.

Vertical gradient of sheets and folders: measured in the reference file manager at large icons (Rec. 709
luminance between 10 % and 90 % of the front panel height, away from edges and symbols), the
folder drops by about 27 out of 255 (RGB 127 200 243 at the top, 96 174 225 at the bottom) and
the sheet without a preview does not drop (245 uniform). The sheets therefore go from `#FFFFFF`
to `#F8F9FB` (drop ≈ 4) and the folders have only two
steps, with half the measured drop by design choice (panel `#82C4FD` to `#68B0FA`, drop ≈ 16;
back `#4497F8` to `#3589F1`), against
≈ 31 when they followed the measure and ≈ 64 for folders and ≈ 12 for sheets before.

**Fold shadow.** Under the folded corner of the sheet a soft shadow falls on the page: a
circle Ø 131.6 centered on the inner corner of the fold, (697.3, 220.2) in the 1024 canvas,
with a radial gradient from black at 16 % in the center to transparent at the edge, drawn
between the page and the corner and clipped to the page (`Fold-shadow` group). The corner
hides most of it: what shows is a soft halo along the fold's lower and left edges. No filter.

**No dark variants.** Sheets and folders are the same in every theme, as in the reference:
there is no `-dark` artwork for `file-generic` or `folder-generic` (the Apps Kit has no dark
sheet or folder, 2026-10-17), and their glyph, label and engraving colors are the same in
Light and Dark. The volumes, the Trash and the badges keep theirs.

**Layered sheet and folder.** `file-generic` is two layers, `back` (the sheet) and `front`
(the folded corner with the soft shadow it casts on the page, clipped to the sheet);
`folder-generic` is three, `back` (back panel with the tab), `middle` (the white sheet that
peeks out when the folder has items) and `front` (front panel). Whoever draws them (the
thumbnail service, Mustache, the Dock) puts its own content between the layers: see Generic
file and Generic folder. The layer SVGs come from the Apps Kit with Sketch's inner and drop
shadows as SVG filters; `<layer>.png` next to each is the same layer rendered at 1024 for
renderers without filters.

**Trash.** A rounded-square bin (superellipse, exponent 4.6) that narrows toward the base
(base 0.86 of the rim), modelled in 3D and projected from 13° above (`tools/trash/`), on the
Trash keyline: the generator solves the height so that the rim is 667 wide, the wall 656 and the
bin 824 tall from y 100 to the base at y 924. It has the outer wall, the inner back
wall, the floor and a rim with its own thickness. The wall is a single shape whose horizontal
gradient is sampled from the model (diffuse light from the upper left, a soft specular and a
Fresnel edge), translucent frosted glass (light) or graphite (dark); no filters. In the full
Trash the documents, photo and folder of the set stick out of the opening, clipped so they
never cross the sides, and the same pile shows through the wall blurred and faint: rendered,
Gaussian-blurred and embedded as a small PNG (`<image>`, data URI) clipped to the wall, the
only raster in `files/`, because the shell does not apply SVG filters.

### Text

Text in SVGs uses only Inter (provided by the shell). It is better to convert it to outlines
when it does not need to change.

## `icon.json` manifest

```json
{
  "format": 1,
  "id": "mail",
  "name": "Mail",
  "kind": "app",
  "keyline": "landscape",
  "layers": [
    { "role": "background", "file": "background.svg" },
    { "role": "foreground", "file": "foreground.svg", "shadow": "neutral" }
  ],
  "variants": {
    "dark": { "background": "background-dark.svg", "foreground": "foreground-dark.svg" }
  },
  "dynamic": null
}
```

| Field | Values |
| --- | --- |
| `kind` | `app` (shape imposed by the shell) or `file` (free-form) |
| `keyline` | `square`, `circle`, `circle-small`, `portrait`, `landscape`, `full`; for volumes `volume` (documentation only: the shell does not clip `file` icons) |
| `layers` | bottom to top: one `background` and 1 to 4 foreground layers |
| `shadow` | shadow the shell draws under the layer: `neutral`, `chromatic` (taken from the layer color) or `none` |
| `variants.dark` | replacement layers for Dark, Clear Dark and Tinted Dark |
| `dynamic` | content updated at runtime, see below |
| `rendered` | the whole icon as designed, with its relief, shadows and glass, PNG at 1024 from the design file's layer styles, one per theme: `default`, `dark`, `clear`, `clear-dark`, `tinted`, `tinted-dark`. Clear renders have a translucent body (the shell adds the backdrop blur behind) and a grey foreground; Tinted renders use the default blue tint, so the shell recolours them only for another tint. The SVG layers stay for custom tints and dynamic content |

`file` icons have a single `artwork` layer (`icon.svg`, `icon-dark.svg`) and no
background, except `file-generic` (`back`, `glyph`, `front`) and `folder-generic` (`back`,
`middle`, `front`), drawn bottom to top.

| Layer field | Meaning |
| --- | --- |
| `file` | SVG in the icon folder; a dark variant, where there is one, is in `variants.dark.<role>` |
| `dynamic` | `true`: no file, the slot where the renderer draws the dynamic content (the glyph of `file-generic`) |
| `when` | `not-empty`: drawn only for a folder with at least one item (`middle` of `folder-generic`) |
| `tint` | folders: `true` if the folder tint recolors the layer |

## Themes

The shell generates six themes from the layers:

| Theme | Background | Foreground |
| --- | --- | --- |
| Default | `background` | `foreground` |
| Dark | `background-dark`, otherwise graphite `#3a3a3c → #161618` | `foreground-dark`, otherwise `foreground` |
| Clear Light | light glass (white 50 % → 25 % over the blurred backdrop) | `foreground` in grayscale, luminance mapped to 105–255 |
| Clear Dark | dark glass (graphite 50 % → black 55 %) | as above, mapped to 150–255 |
| Tinted Light | tint lightened to 90 % → 76 % | luminance mapped to the tint (dark → tint → white) |
| Tinted Dark | tint darkened to 62 % → 84 % | luminance mapped from dark tint to light tint |

In the dark themes the background is neutral and the color stays on the foreground (Mail,
Store, Help): it is the rule of the set.

## Dynamic content

`dynamic` describes the layers that the shell updates at runtime.

### Clock

```json
"dynamic": {
  "type": "clock",
  "hands": [
    { "unit": "hour",   "file": "hand-hour.svg" },
    { "unit": "minute", "file": "hand-minute.svg" },
    { "unit": "second", "file": "hand-second.svg", "min_size": 64 }
  ],
  "cap": "cap.svg"
}
```

Each hand is drawn pointing to 12 and rotates around (512, 512):
hours = (h mod 12 + m/60 + s/3600) × 30°, minutes = (m + s/60) × 6°, seconds = s × 6°.
`cap` (hub and pin) goes above the hands. The second hand is shown only from
`min_size` pt up; it updates every second if visible, otherwise every minute, never
while the icon is off screen.

### Calendar

```json
"dynamic": {
  "type": "calendar",
  "month": { "font": "Inter", "size": 190, "weight": 900, "tracking": 0,
             "color": "#f5222f", "dark_color": "#ff5a62",
             "box": [212, 144, 600, 230], "case": "upper", "format": "short" },
  "day":   { "font": "Inter", "size": 308, "weight": 700, "tracking": 0,
             "color": "#ffffff", "dark_color": "#f2f4f8", "box": [212, 426, 600, 372] },
  "refresh": "midnight"
}
```

Month as the localized three-letter abbreviation in capitals (`OCT`, `OTT`), centred in `box`
(Amalfi icon, 2026-10-16; the full month name is no longer used). Day without a leading zero,
centred in the red disc. Updates at local midnight and on date or time zone change.

### Generic file

`files/file-generic` is the only document icon. There are no per-type icons: the renderer
(the thumbnail service, Mustache, the Dock) composes every file icon from the two layers of
the sheet, a glyph between them and the extension it writes itself.

```json
"layers": [
  { "role": "back", "file": "back.svg" },
  { "role": "glyph", "dynamic": true },
  { "role": "front", "file": "front.svg" }
],
"dynamic": {
  "type": "file-glyph",
  "glyph": { "box": [262, 262, 500, 500],
             "symbol": { "sizes": [ { "min_size": 128, "weight": "light" },
                                    { "min_size": 64,  "weight": "regular" },
                                    { "min_size": 16,  "weight": "semibold" } ] },
             "app_icon": { "body": [303.67, 303.67, 416.67, 416.67] } },
  "label": { "font": "Inter", "size": 111.67, "weight": 500, "tracking": 0,
             "box": [270.64, 763.7, 482.72, 136.04], "case": "upper",
             "max_chars": 5, "max_width": 482.72, "overflow": "shrink", "min_size": 32 },
  "label_alone": { "font": "Inter", "size": 175.53, "weight": 900, "tracking": 0,
                   "box": [219.08, 362.8, 585.84, 212.83], "case": "upper",
                   "max_chars": 5, "max_width": 585.84, "overflow": "shrink", "min_size": 32 },
  "kinds": { "pdf": { "glyph": "doc-text", "color": "#e2332b" }, "code": {...}, ... },
  "colors": { "document": {...}, "data": {...}, "code": {...},
              "archive": {...}, "media": {...}, "other": {...} },
  "overrides": { "json": "data", "epub": "document", "blend": "media", ... },
  "types": {
    "mime": { "application/pdf": "pdf", "text/csv": "spreadsheet",
              "application/json": { "category": "data" }, ... },
    "extensions": { "pdf": "pdf", "xlsx": "spreadsheet", "sh": "executable", ... }
  },
  "fallback": "unknown"
}
```

**Order** (bottom to top): `back` → glyph → `front` → label. The front is the folded corner
and the shadow it casts on the page; nothing the renderer draws reaches it.

Measures on the 1024 canvas (fraction of the side in brackets; the sheet is 684 × 904 at
(170, 60), the fold covers x 650…854, y 60…264):

| Element | Box (x, y, w, h) | Details |
| --- | --- | --- |
| Glyph box | 262, 262, 500, 500 (0.2559, 0.2559, 0.4883, 0.4883) | centred at (512, 512); the widest of the former type figures (500–506) |
| Symbol | the symbol's 24 u canvas fills the glyph box: 1 u = 20.83 (0.0203) | live area (20 u) 416.67 at (303.67, 303.67) (0.4069 at 0.2966) |
| App icon | the composed app icon with its 824 body on 303.67, 303.67, 416.67, 416.67 | scale 0.50566: the 1024 app canvas is 517.8 at (253.10, 253.10) (0.5057 at 0.2472) |
| Label (with a glyph) | 270.64, 763.7, 482.72, 136.04 (0.2643, 0.7458, 0.4714, 0.1329) | Inter Medium 500 (`opsz` 14), size 111.67 (0.1091), baseline y 872.34 (0.8519) |
| Label alone (no glyph) | 219.08, 362.8, 585.84, 212.83 (0.2139, 0.3543, 0.5721, 0.2078) | Inter Black 900, size 175.53 (0.1714), baseline y 533.06 (0.5206) |

- **Symbol**: `symbols/<weight>/<glyph>.svg`, `currentColor` replaced by the kind's `color`,
  flat (no engraving, no shadow), opacity 1. The weight is the first `sizes` band with
  `min_size` ≤ icon side in pt (the full canvas, see Principle): Light from 128, Regular from
  64, Semibold from 16; below 16 no glyph. Stroke in the canvas: Light 24.6, Regular 31.3,
  Semibold 44.8 (1.18, 1.5, 2.15 u).
- **App icon**: instead of a symbol the renderer may put an app icon (the document of an app
  that owns its type, an app bundle): composed as in the Dock (shape, rim and glass of the
  current theme, no Dock shadow), its body fitted to `app_icon.body`. It is not recolored.
- **Colors**: the same in Light and Dark (the sheet does not change). The symbol and the
  label take the kind's `color`; with an app icon or without a glyph the label takes the
  category color (`colors`, see below).
- **Label**: the extension without the dot, uppercase (`case`), centered horizontally in the
  `box`, the natural Inter line (1.2102 × size) centered vertically, so the baseline is at
  y + h/2 − 0.605 × size + 0.96875 × size. Up to `max_chars` (5) characters; wider than
  `max_width` the size shrinks proportionally, always centered (`XHTML`, `WOFF2`, `QCOW2`
  fit at full size). More than 5 characters or no extension: no label, never truncated (the
  glyph alone; without a glyph, the `fallback` kind). Below `min_size` (32 pt) no label.
  For `.tar.<x>` the final extension (`GZ`, `XZ`).
- **Kinds** (`kinds`, from the former type icons, colors from their manifests):

  | Kind | Glyph | Color | Extensions (summary) |
  | --- | --- | --- | --- |
  | `pdf` | `doc-text` | `#e2332b` | pdf |
  | `text` | `text-align-left` | `#8e8e93` | txt, md, log, rst |
  | `document` | `doc-text` | `#2f7cf6` | rtf, odt, doc, docx, pages |
  | `spreadsheet` | `chart-bar` | `#1f9d55` | xlsx, xls, ods, numbers, csv, tsv |
  | `presentation` | `chart-pie` | `#f2780c` | pptx, ppt, odp, key |
  | `font` | `text-size` | `#ff2d55` | ttf, otf, ttc, woff, woff2 |
  | `disk-image` | `disc` | `#8e8e93` | iso, img, dmg, qcow2, vdi, vmdk |
  | `executable` | `terminal` | `#ff6a00` | sh, bash, zsh, fish, run, bin, appimage |
  | `web` | `globe` | `#2f7cf6` | html, htm, xhtml, mhtml |
  | `code` | `code` | `#7a5af8` | rs, dart, py, js, ts, c, go, java, css… |
  | `archive` | `archive` | `#8e8e93` | zip, tar, gz, xz, zst, 7z, rar, deb, rpm… |
  | `image` | `photo` | `#2f7cf6` | the common formats |
  | `audio` | `music-note` | `#ff2d55` | the common formats |
  | `video` | `film` | `#8e8e93` | the common formats |
  | `unknown` | `question` | `#8e8e93` | fallback: no glyph and no usable extension |

  The PDF kind keeps the red of the former PDF pill; its label is red like the glyph.

- **Category color** (only without a kind: app icon or label alone), in order: the
  extension's `overrides`, then the `category` of the `types.mime` entry, then the category
  of the MIME type (shared-mime-info): `text/*` and office documents → `document`; JSON, XML,
  YAML, CSV, databases → `data`; sources and scripts → `code`; archives and packages →
  `archive`; `image/*`, `audio/*`, `video/*`, fonts → `media`; everything else → `other`.
  `overrides` maps a single extension to a category or a color (`{"json": "data"}`,
  `{"sketch": {"color": "#f7b500"}}`).
- `types` is **the** map of the repo (type → kind); whoever resolves a file's icon
  (SilicaIcon, Mustache, the Dock, the thumbnail service) keeps no map of its own. A
  `types.mime` entry is a kind (`"text/csv": "spreadsheet"`) or no kind with a category
  (`"application/json": {"category": "data"}`: label alone). Resolution order for a regular
  file:
  0. the MIME type is brought to its canonical name with the shared-mime-info `aliases`
     (`text/xml` → `application/xml`, `text/x-yaml` → `application/yaml`);
  0b. if the type comes only from the name and `globs2` gives several types of the same
     weight for that extension (ambiguous name: `.ts` is TypeScript, Qt Linguist or MPEG-TS
     depending on the system), step 4 (`types.extensions`) applies before steps 1–3; if the
     content decides the type (magic), the normal order stays;
  1. the MIME type (shared-mime-info, from content and name) in `types.mime`, exact;
  2. the same with the subtype `*` (`image/*`, `audio/*`, `video/*`, `font/*`);
  3. the parents of the type (`sub-class-of` of shared-mime-info, in order), repeating 1 and 2:
     a `text/x-…` type without an entry stays text and not code only if no parent is in the map;
  4. the lowercase extension in `types.extensions` (the last one after the dot; for `.tar.<x>`
     names the final extension applies, which is already in the map as an archive);
  5. otherwise no kind: label alone in the category color; without an extension or beyond
     `max_chars`, the `fallback` kind.
  An executable without an extension (`x` bit and type `application/x-executable`,
  `application/x-pie-executable`, `application/x-shellscript`) gets `executable` at
  step 1; a file with the `x` bit but of another type (a `.py`) keeps the kind of its type.
- **An explicit entry always wins over the parents.** Step 3 follows `sub-class-of`, and in
  shared-mime-info many data formats descend from code or text types:
  `application/json` is a subclass of `application/json5` → `application/ecmascript` →
  `text/javascript` (it would get `code`), `application/xml`, `application/yaml`,
  `application/toml`, `application/sql`, `text/calendar` and `text/vcard` of `text/plain`
  (they would get `text`), EPUB, ODF documents without a kind and the Apple formats of
  `application/zip` (they would get `archive`). For these `types.mime` has an explicit
  entry, because it is deterministic: it does not depend on the database version or on which
  parent is met first, and a `"json": "data"` in `overrides` alone would never be enough,
  because `overrides` counts only when no kind was found. An explicit entry
  also covers the children (`application/geo+json`, `application/ld+json` go through
  `application/json`; the `+xml` types through `application/xml`). The added entries (from the
  shared-mime-info database, main branch, October 2026):
  - category `data`: `application/json`, `application/json5`, `application/xml`,
    `application/xml-dtd`, `application/yaml`, `application/toml`, `application/sql`,
    `text/calendar`, `text/vcard`, KMZ, ODF databases;
  - category `document`: Jupyter notebooks (`application/x-ipynb+json`), EPUB, FictionBook,
    CBZ/CBR comics, PostScript, XPS and OpenXPS, TeX, e-mail (`message/rfc822`), ODF drawings,
    charts and formulas, Visio, OpenOffice 1 Draw and Math, HWPX;
  - category `media`: ODF image, `model/3mf`;
  - kinds: ODF flat XML (`fodt`, `fods`, `fodp`), Office templates and macro-enabled
    variants (`dotx`, `dotm`, `xltx`, `xltm`, `potx`, `potm`, `ppsx`, `ppsm`, `sldx`, `sldm`),
    Pages, Numbers and Keynote, OpenOffice 1 Writer, Calc and Impress → `document`,
    `spreadsheet`, `presentation`; TypeScript (`application/typescript`, which
    shared-mime-info makes descend from `application/x-executable`), Dart, C#, Julia, Elixir,
    Erlang, Haskell, Nim, OCaml, Sass and Scala → `code` (otherwise `text/plain` would make
    them text, even though their extension is in `types.extensions`).

  Left to the parents, on purpose: ZIP packages (`appx`, `msix`, `xpi`, `oxt`, `pkpass`)
  are archives; the other sources without an entry (Fortran, Pascal, Lisp…) and the text
  formats (subtitles, patches, systemd units) stay `text`; the types that derive from a
  kind (`pptm` from `pptx`, EXE and DLL from `application/x-executable`) take its kind.

Design source: the Silica 1.0 Amalfi Apps Kit (Sketch), artboard `Files / File 1024`, layers
`Sheet` (→ `back`) and `Fold` (→ `front`). `icon.png` is the plain sheet (back and front).
Reference: `tools/compose.py`, `compose_file(dir, side, dark, ext, kind, category, app_icon)`.

### Volumes

`files/volume-*` are the mounted disks and servers, on the volume keyline (944 × 583). They
have no dynamic content: whoever shows a volume (sidebar and windows of Mustache, Desktop,
Dock) chooses the icon like this, from the first case that applies:

| Icon | When |
| --- | --- |
| `volume-network` | network mount: file system type `nfs`, `nfs4`, `cifs`, `smb3`, `9p`, `fuse.sshfs`, `fuse.rclone`, `davfs`; or a GVfs mount with scheme `smb`, `sftp`, `ftp`, `ftps`, `dav`, `davs`, `nfs`, `afp`; also applies to a server in the sidebar not yet mounted |
| `volume-disk-image` | loop device with a file behind it (`/dev/loop*`, interface `org.freedesktop.UDisks2.Loop` with `BackingFile`): a mounted image, even if it is an ISO |
| `volume-optical` | optical drive: `Drive.Optical` true in UDisks2, or `optical_*` media in `Drive.MediaCompatibility` or a `/dev/sr*` device |
| `volume-external` | removable or external drive: `Drive.Removable` or `Drive.MediaRemovable` true, or `Drive.ConnectionBus` `usb`, `sdio` or `ieee1394`; SD cards and flash drives included |
| `volume-internal` | everything else: the root `/`, the other partitions of internal disks (`ConnectionBus` empty, NVMe and SATA) and a volume about which nothing is known |

Without UDisks2 (or for a mount that UDisks2 does not know) `/proc/self/mountinfo` (file system
type and device) and `/sys/block/<disk>/removable` are used. The name is the volume's
(`IdLabel`), not the icon's. The `NETWORK` folder of the generic folder remains for network
*folders* inside a volume; the volume itself is `volume-network`.

### Badges

`badges/` contains the badges that the shell overlays on an already composed file or folder
icon. They are not icons with a manifest: each badge is a light and a dark SVG
(`alias.svg`, `alias-dark.svg`…) on the 1024 canvas, drawn as a centered Ø 824 disc (the body)
with the symbol in the 600 and 424 keylines. `badges/badges.json` summarizes the rules below
for implementers.

| Badge | Drawing | Corner | When |
| --- | --- | --- | --- |
| `alias` | curved arrow on a white disc (graphite in dark) | bottom left | the file is a symbolic link (`lstat`); a broken link additionally gets `unreadable` |
| `unreadable` | prohibition sign (white bar on a red disc) | bottom right | the user cannot read it: `access(R_OK)` false, for folders `R_OK` or `X_OK` false |
| `locked` | padlock on a white disc (graphite in dark) | bottom right | the file is locked: immutable or append-only attribute (`STATX_ATTR_IMMUTABLE`, `STATX_ATTR_APPEND`, `chattr +i`/`+a`); a missing write permission is not enough, otherwise half the system would have the padlock |
| `cloud` | blue cloud with a down arrow | bottom right | the content is not on disk: stated by whoever lists the files (a sync provider, a GVfs or rclone mount with network-only files). There is no freedesktop standard: Mustache shows it only when the source reports it |

Position and size (icon 1024 canvas; icon side in pt, that is the full canvas, as for the
generic folder and the label, see Principle):

| Icon side | Badge side | Box, bottom left | Box, bottom right | How many |
| --- | --- | --- | --- | --- |
| from 32 pt | 315 = 824 / φ² | x 100…415, y 609…924 | x 609…924, y 609…924 | one per corner |
| 16–31 pt | 509 = 824 / φ | x 100…609, y 415…924 | x 415…924, y 415…924 | only one |
| below 16 pt | — | — | — | none |

- The box goes from the edge of the app body (100…924) to the golden line: the badge rests
  on that corner, not on the drawing. The sheet (x 170…854, y 60…964) is narrower and taller
  than the body, so the badge sticks out a little to the left and sits above the bottom of the
  sheet; folders (x 34…990) and volumes are wider than the body, so the badge sits inside the
  drawing.
- To be verified with the new side rule: in the reference file manager at 128 pt icons the alias badge measures
  Ø ≈ 34 (0.27 of the canvas, from x ≈ 0.08 and up to ≈ 1 pt from the bottom of the canvas),
  here Ø 315 / 1024 = 0.31. Before, Mustache drew file icons at 92 %, so the rendered badge was
  0.28; the geometry has not changed in this version.
- Composition: the badge's 1024 canvas is scaled by k = side / 824 and shifted so that its body
  (100, 100, 824, 824) coincides with the box: origin of the badge canvas =
  (x₀ − 100 k, y₀ − 100 k). It is drawn after the icon, after the folder tint and after the
  theme mapping: the badge is not tinted and does not go through Clear or Tinted.
- Variants: `-dark` in the Dark, Clear Dark and Tinted Dark themes; the light one in the others.
- Precedence: at the bottom right `unreadable` wins, then `locked`, then `cloud` (the others
  are not shown). Below 32 pt only one badge remains, the first of `order`: `unreadable`,
  `alias`, `locked`, `cloud`.
- No shadow or luminous border from the shell: the disc already has its thin outline (black
  15 % in light, white 20 % in dark, solid white around the prohibition sign).
- The badge follows the state of the icon (selection, dragging, cell shadow): it is part of
  the composed icon. In the Dock and in Faro it is not shown.

Reference: `tools/compose.py`, `compose_badges(icon, names, dark)`.

`design/app-icons.sketch`: the file types, volumes and badges are in the Icons page (rows from
y 15280: files, volumes, badges), in Grid Check with the grids and in Showcase Files in light
and dark (from y 19200, one row per icon).

### Generic folder

`files/folder-generic` is the folder on which the shell (and Mustache) engraves a symbol from
`symbols/`: the special folders (Documents, Downloads, Pictures, Home…) and folders with a
tint. It is the only folder icon: a plain folder is the same icon without a symbol. The
layers carry no symbol.

```json
"layers": [
  { "role": "back",   "file": "back.svg",   "tint": true },
  { "role": "middle", "file": "middle.svg", "when": "not-empty", "tint": false },
  { "role": "front",  "file": "front.svg",  "tint": true }
]
```

**Order** (bottom to top): `back` → `middle` → `front` → symbol (engraving). `middle` (the
white sheet, 840 × 620 at (92, 230), visible from y 230 to the front panel's top at 293) is
drawn only when the folder has at least one item (`when: not-empty`; it replaces the former
`full` variant); an empty folder, or one whose content cannot be read, is `back` + `front`.
`icon.png` is the empty folder, `icon-full.png` the folder with `middle`, both without symbol
and tint.

```json
"dynamic": {
  "type": "folder-symbol",
  "symbol": {
    "box": [354, 434, 316, 316],
    "sizes": [
      { "min_size": 128, "weight": "light",    "scale": 1 },
      { "min_size": 64,  "weight": "regular",  "scale": 1 },
      { "min_size": 32,  "weight": "semibold", "scale": 1,     "highlight": false },
      { "min_size": 16,  "weight": "semibold", "scale": 1.272, "highlight": false }
    ]
  },
  "effect": { "color": "#1a64c8", "opacity": 0.78, "highlight": "#ffffff",
              "highlight_opacity": 0.5, "offset": 4 },
  "tint": {
    "luminance": [0.35, 0.85], "shade": 0.72, "glow": 0.5, "layers": ["back", "front", "symbol"],
    "labels": { "red": "#f2382e", "orange": "#f98a17", "yellow": "#f5c400", "green": "#2fb350",
                "blue": "#2f7cf6", "purple": "#a052e0", "gray": "#8e8e93" }
  },
  "folders": { "HOME": "house", "DESKTOP": "display", "DOCUMENTS": "doc-text",
               "DOWNLOAD": "arrow-down-circle", "MUSIC": "music-note", "PICTURES": "photo",
               "VIDEOS": "film", "TEMPLATES": "doc-plus", "PUBLICSHARE": "share",
               "APPLICATIONS": "square-grid-2x2", "LIBRARY": "books-vertical", "SHARED": "person-2",
               "NETWORK": "network" },
  "fallback": null
}
```

Proportions (1024 canvas, folder keyline):

| Measure | Value | Where it comes from |
| --- | --- | --- |
| Front panel | 956 × 599 from (34, 293), center (512, 592.5) | Amalfi folder (`front`); formerly 944 × 619 from (40, 273.1) |
| Symbol live area (Ø 20 u) | 263.5 | 230 (series A, 600 / φ²) on the 824 folder, × 1.1456 |
| Symbol canvas (24 u), `box` | 316 × 316 at (354, 434) (0.3457, 0.4238, 0.3086), center (512, 592) on the front panel: 1 u = 13.17 px | live area × 24 / 20 |
| Stroke | Light 15.6 · Regular 19.8 · Semibold 28.3 | 1.18 · 1.5 · 2.15 u: on the 824 folder they were 13.6 · 17.3 · 24.7, the thicknesses 13.5 and 17 of the series |
| Small symbol (`scale` 1.272) | canvas 402, live area 335 | × √φ |
| Engraving (`offset`) | 4 px, at least half a rendered pixel | ≈ Light stroke / φ³ |

- **Symbol**: `symbols/<weight>/<name>.svg` from the same repo, colored in place of
  `currentColor`, centered in `box` and scaled by `scale` around the center. The band is the
  first of `sizes` with `min_size` ≤ icon side in pt (the full canvas, see Principle);
  below the last one (16 pt) the symbol is not drawn. The weight grows as the icon shrinks so
  that the rendered stroke stays between 1 and 4 px or so: Light from 128, Regular from 64,
  Semibold below, and below 32 even larger (× √φ).
- **Engraved effect** (`effect`, one for every theme): first the copy of the symbol in `highlight` with
  `highlight_opacity`, shifted down by `offset` (the lower edge of the engraving catches the
  light), then the symbol in `color` with `opacity`. Below 64 pt (`"highlight": false`) only
  the symbol: the half-pixel reflection would smear it.
- **Special folders** (`folders`): the keys are those of `xdg-user-dirs`
  (`XDG_<KEY>_DIR` in `~/.config/user-dirs.dirs`: DESKTOP, DOCUMENTS, DOWNLOAD, MUSIC,
  PICTURES, VIDEOS, TEMPLATES, PUBLICSHARE) plus five Silica keys: `HOME` (the user's
  folder), `APPLICATIONS` (`~/Applications` and the `applications` folders of the XDG data),
  `LIBRARY` (`~/.local/share`, the user's library), `SHARED` (shared folder) and
  `NETWORK` (network folder). The last two have no fixed path: they are given by whoever knows
  the folder (Mustache knows whether it is a network mount or a share). A folder that is not
  among these, or a symbol that does not exist in `symbols/`, gets `fallback`: `null`, the
  folder without a symbol. The Trash has an icon of its own. Mustache can also pass any symbol from `symbols/`.
- **Tint** (`tint`): a custom `#rrggbb` color or the name of a label in `labels`.
  The layers listed in `tint.layers` (`back`, `front` and the engraved symbol with its
  highlight; never `middle`, which stays white) go through a ramp on luminance: L = 0.2126 R +
  0.7152 G + 0.0722 B (sRGB, 0–1); from `luminance[0]` to `luminance[1]` the color goes from
  tint × `shade` to the tint lightened toward white by `glow` (outside the interval it stops
  at the extremes). It is linear, so it is a 4 × 5 color matrix (`ColorFilter.matrix`): the
  symbol stays darker than the panel and the reflection lighter, with the same color. Because
  the ramp is affine, tinting each listed layer and then compositing equals tinting the
  composed back + front + symbol. Without a tint the folder stays the blue drawing, with no
  ramp. Engraving (`effect`): `#1a64c8` at 0.78 over a white copy at 0.5 shifted down by 4
  (Light and Dark alike).
- **Other themes**: Clear and Tinted (Light and Dark) apply their rule to the folder already
  composed with the symbol (luminance mapped, see Themes), so the symbol stays the engraving
  darker than the panel; in the Clear themes the engraving reflection is removed
  (`highlight_opacity` 0), because the glass already has its border. The custom tint applies
  only in Default and Dark: Tinted uses the theme tint for all folders. Dark uses the same
  folder, engraving and tint ramp as Default.

Design source: the Silica 1.0 Amalfi Apps Kit (Sketch), artboards `Files / Folder 1024` and
`Files / Folder Full 1024`, layers `Back`, `Sheet` (→ `middle`) and `Front`. Reference:
`tools/compose.py`, `compose_folder(dir, side, dark, symbol, tint, full)`.

## Icons without layers

An app that has only a freedesktop icon (an already composed PNG or SVG) is reduced to the
square keyline and placed on a neutral background (white in light, graphite in dark).
