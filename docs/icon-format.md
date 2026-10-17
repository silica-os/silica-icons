# Icon format

Versions 1 and 2. Format 1 applies to `apps/`, `files/` and `badges/`; format 2 (layered app
icons, see [Format 2](#format-2-layered-app-icons)) applies to `apps/` only and is in its pilot:
Mustache, Terminal and Clock use it, the other apps stay on format 1. System symbols
(`symbols/`) have a separate specification.

## Principle

An app icon is **layered content**, not a finished image. The developer supplies the
background and the foreground; the shell applies the shape, border, shadows, glass and
themes. This way every Dock icon has the same shape and reacts to the same themes.

File icons (`files/`), instead, are free-form objects (folders, documents, Trash): the shell
applies no mask or body, only the shadow of the context. For file icons **the side is the
full canvas**: a 64 pt file icon is the 1024 canvas drawn at 64 pt, with no reductions (no
824 body, no factors like the former 92 %); the bands that depend on the side (`min_size` of
the badges) are compared with this side. In the Dock a
place (folder, Trash) uses the canvas of the neighboring apps, the one that overflows the body
by 100/824.

## Canvas and grid

All measures are on a **1024 × 1024** canvas.

| Element | Measure |
| --- | --- |
| Body (where the shell clips) | 824 × 824 at (100, 100) |
| Body corners | smooth, radius 215, smoothing 0.55; the reference outline is the Apps Kit `Icon / Background` Body path, exported as `tools/body.svg` (drawn there as radius 214, smoothing 0.6) |
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
Regular stroke (1.5 u) is 45 px. The design source, the Silica 1.0 Amalfi Apps Kit (Sketch), has
the `Grid / Overlay` symbol (Grid page, artboard `Grid / Icon 1024`; a hidden instance in every icon
artboard). The golden grid symbol `Grid / Golden 1024` exists only in the legacy
`design/app-icons.sketch`.

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
  824 × 663), then to the full canvas with the file manager measures (v0.2.0). The front panel of the folder is
  944 × 619 from y 273.1 (0.815 of the height; in the reference 0.82);
- the Trash is 656 wide (rim 667) and 824 tall, with the bin base at y 924, on the bottom of the
  app body: in the Dock it rests on the same line and has the same height;
- the fold of the sheets (174 × 176: the earlier 165 × 160, scaled in width by 684 / 648 and in
  height by 904 / 824) is not on the series: changing it means redrawing the path of every
  sheet; it stays until the sheets are redrawn;
- the Trash is neither sheet nor folder: it has its own keyline, measured in the Dock;
- Stack Close (the Dock button that closes an open stack) is in `badges/` as `stack-close`
  (badges.json → `dock`): the same disc and material as the file badges, with a cross;
- volumes are 824 × 509 slabs with radius 64 and the server is three units 155 tall with gaps
  of 22, on the 824 drawing; in the SVGs they scale by 1.1456 around the center (slab 944 × 583,
  radius 73).

In the SVGs of volumes and Trash the scale is in a single attribute: `transform` on the `icon`
group (`icon-dark`); the paths stay those of the 824 drawing. The layers of `file-generic` and
`folder-generic` are exported from the Apps Kit in canvas coordinates.

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

Format 1 (the format 2 folder, with `layers/`, is in [Format 2](#format-2-layered-app-icons)):

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
added by the shell (IC-01). The SVGs of `files/` have no `filter`, except the layers of
`file-generic` and `folder-generic` (see Layered sheet and folder). The earlier sheets, folders
and Trash had the ground shadow and the shadows of the pieces: they were flattened with the
same rule, without changing shape, colors or proportions.

Vertical gradient of sheets and folders: measured in the reference file manager at large icons (Rec. 709
luminance between 10 % and 90 % of the front panel height, away from edges and symbols), the
folder drops by about 27 out of 255 (RGB 127 200 243 at the top, 96 174 225 at the bottom) and
the sheet without a preview does not drop (245 uniform). The sheets go from `#FFFFFF`
to `#EBEFF7` (drop ≈ 16, by design choice; Apps Kit `Files / File 1024`, layer `back`) and the folders have only two
steps, with half the measured drop by design choice (panel `#82C4FD` to `#68B0FA`, drop ≈ 16;
back `#4497F8` to `#3589F1`), against
≈ 31 when they followed the measure and ≈ 64 for folders and ≈ 12 for sheets before.

**Fold shadow.** Under the folded corner of the sheet a soft shadow falls on the page: the
drop shadow of the fold (offset −2, 8, blur 48, `#3A4A6A` at 20 %), clipped to the sheet by a
mask inside the `front` layer. The corner hides most of it: what shows is a soft halo along the
fold's lower and left edges.

**No dark variants.** Sheets and folders are the same in every theme, as in the reference:
there is no `-dark` artwork for `file-generic` or `folder-generic` (the Apps Kit has no dark
sheet or folder, 2026-10-17), and they are the same in
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
| `content_area` | optional, `file-generic` and `folder-generic`: `[x, y, w, h]` in the 1024 canvas, the flat area where a generator can put content; informative |
| `shadow` | shadow the shell draws under the layer: `neutral`, `chromatic` (taken from the layer color) or `none` |
| `variants.dark` | replacement layers for Dark and Tinted Dark |
| `dynamic` | content updated at runtime, see below |
| `rendered` | the whole icon as designed, with its relief, shadows and glass, PNG at 1024 from the design file's layer styles, one per theme: `default`, `dark`, `clear`, `tinted`, `tinted-dark`. The clear render has a translucent body (the shell adds the backdrop blur behind) and a grey foreground; Tinted renders use the default blue tint, so the shell recolours them only for another tint. The SVG layers stay for custom tints and dynamic content |

`file` icons have a single `artwork` layer (`icon.svg`, `icon-dark.svg`) and no
background, except `file-generic` (`back`, `front`) and `folder-generic` (`back`,
`middle`, `front`), drawn bottom to top.

| Layer field | Meaning |
| --- | --- |
| `file` | SVG in the icon folder; a dark variant, where there is one, is in `variants.dark.<role>` |
| `when` | `not-empty`: drawn only for a folder with at least one item (`middle` of `folder-generic`) |

## Themes

The shell generates five themes from the layers; clear exists only in light (there is no dark clear
theme):

| Theme | Background | Foreground |
| --- | --- | --- |
| Default | `background` | `foreground` |
| Dark | `background-dark`, otherwise graphite `#3a3a3c → #161618` | `foreground-dark`, otherwise `foreground` |
| Clear (light only) | light glass (white 50 % → 25 % over the blurred backdrop) | `foreground` in grayscale, luminance mapped to 105–255 |
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

`files/file-generic` is the only document icon, in two layers on the 1024 canvas:

```json
"layers": [
  { "role": "back",  "file": "back.svg" },
  { "role": "front", "file": "front.svg" }
],
"content_area": [230, 270, 564, 630]
```

**Order** (bottom to top): `back` (the sheet, 684 × 904 at (170, 60)) → [content drawn by the
generator] → `front` (the folded corner with its soft shadow on the page). `icon.png` is the
plain sheet (back and front). `content_area` is `[x, y, w, h]` in the canvas: the flat part of
the sheet, below the fold and clear of the rounded corners, where content can go. It is
informative only.

Composition (symbols, text, tints, type mapping) belongs to the thumbnail generator in
silica-desktop; this repo only provides the layers.

Design source: the Silica 1.0 Amalfi Apps Kit (Sketch), artboard `Files / File 1024`, layers
`back` and `front` in the `Artwork` group.

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
generic folder, see Principle):

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
  (x₀ − 100 k, y₀ − 100 k). It is drawn after the icon and after the
  theme mapping: the badge is not tinted and does not go through Clear or Tinted.
- Variants: `-dark` in the Dark and Tinted Dark themes; the light one in the others.
- Precedence: at the bottom right `unreadable` wins, then `locked`, then `cloud` (the others
  are not shown). Below 32 pt only one badge remains, the first of `order`: `unreadable`,
  `alias`, `locked`, `cloud`.
- No shadow or luminous border from the shell: the disc already has its thin outline (black
  15 % in light, white 20 % in dark, solid white around the prohibition sign).
- The badge follows the state of the icon (selection, dragging, cell shadow): it is part of
  the composed icon. In the Dock and in Faro it is not shown.

Reference: `tools/compose.py`, `compose_badges(icon, names, dark)`.

Apps Kit: the generic file and folder, volumes and badges are artboards in the Icons page, one row
per icon with the dark variant beside it (`Files / Folder 1024`, `Files / Folder Full 1024`,
`Files / File 1024` from y 25852; volumes and badges from y 47208).

### Generic folder

`files/folder-generic` is the only folder icon, in three layers on the 1024 canvas:

```json
"layers": [
  { "role": "back",   "file": "back.svg" },
  { "role": "middle", "file": "middle.svg", "when": "not-empty" },
  { "role": "front",  "file": "front.svg" }
],
"content_area": [94, 353, 836, 480]
```

**Order** (bottom to top): `back` (back panel with the tab) → `middle` → `front` (front panel)
→ [content drawn by the generator]. `middle` (the white sheet, 840 × 620 at (92, 230), visible
from y 230 to the front panel's top at 293) is drawn only when the folder has at least one item
(`when: not-empty`); an empty folder is `back` + `front`. `icon.png` is the empty folder,
`icon-full.png` the folder with `middle`. `content_area` is `[x, y, w, h]` in the canvas: the
flat part of the front panel (956 × 599 from (34, 293)), clear of its corners. It is
informative only.

Composition (symbols, text, tints, special folders) belongs to the thumbnail generator in
silica-desktop; this repo only provides the layers.

Design source: the Silica 1.0 Amalfi Apps Kit (Sketch), artboards `Files / Folder 1024` and
`Files / Folder Full 1024`, layers `back`, `middle` (Full only) and `front` in the `Artwork` group.

## Format 2: layered app icons

An app icon in format 2 is a stack of named layers that the icon service composes at runtime in
four appearances: **light, dark, clear, tinted**. Clear exists only in light; tinted has a light and a
dark form, so the five themes of format 1 remain. Pilot icons: `mustache`, `terminal`, `clock`.

### Files

```
apps/<id>/
  icon.json                 manifest, "format": 2
  layers/<layer>.svg        one file per layer, 1024 canvas, viewBox 0 0 1024 1024
  layers/<layer>-dark.svg   optional: the layer as drawn for the dark forms
  layers/background.svg     optional, only for a drawn background; otherwise a gradient in icon.json
  icon.png, icon-dark.png   flat fallback, light and dark
  preview.png               documentation only
```

- Canvas, body and clip are those of format 1 (body 824 at (100, 100), smooth corners; outline
  `tools/body.svg`). Layers are drawn unclipped; the service clips the whole stack to the body.
- The layer id is lowercase kebab-case, unique in the icon, equal to the file stem and to the
  group name in the Apps Kit. `background` and `fallback` are reserved.
- Layers are listed **bottom to top**. The background is not in the list: it is always the bottom.
  Required: the background and at least one `body` layer; at most 9 layers in total.
- As in format 1, no body mask, rim or cast shadow is drawn into a layer (see What does NOT go in
  the layers); internal shading and gradients stay in the SVG. Text is outlined.

### Manifest

```json
{
  "format": 2, "id": "terminal", "name": "Terminal", "kind": "app", "keyline": "square",
  "background": { "light": { "gradient": ["#28282c", "#08080a"] },
                  "dark":  { "gradient": ["#1e1e22", "#040405"] } },
  "layers": [
    { "id": "output", "role": "detail", "min_size": 32,
      "clear": { "mode": "ramp" }, "tinted": { "mode": "ramp" } },
    { "id": "prompt", "role": "body", "clear": { "mode": "light" }, "tinted": { "mode": "light" } },
    { "id": "cursor", "role": "detail", "clear": { "mode": "ramp" }, "tinted": { "mode": "accent" } }
  ],
  "fallback": { "light": "icon.png", "dark": "icon-dark.png" }
}
```

| Icon field | Meaning |
| --- | --- |
| `background.light` | `{ "gradient": [top, bottom] }` (vertical, over the body height) or `{ "file": "layers/background.svg" }` |
| `background.dark` | same shape; default graphite `#3a3a3c → #141416` |
| `layers` | the layers, bottom to top |
| `glass` | optional tuning of the `glass` mode: `{ "top", "bottom", "blur" }` |
| `fallback` | `{ "light", "dark", "time" }`: the flat icons; `time` is the clock pose baked in |

There is no `rendered` and no `variants` in format 2. Clear and tinted backgrounds are the same
for every icon (no per-icon override): only layers carry per-icon choices.

| Layer field | Default | Meaning |
| --- | --- | --- |
| `id` | required | layer id; the file is `layers/<id>.svg` |
| `role` | required | `body`, `detail`, `highlight` or `dynamic`; sets the defaults below |
| `opacity` | 1 | layer opacity |
| `blend` | `normal` | `normal`, `multiply` or `screen` |
| `shadow` | `neutral` for body and dynamic, else `none` | cast shadow drawn by the service (format 1 values) |
| `min_size` | 0 | drawn only when the icon side in pt is at least this |
| `clear`, `tinted` | by role | `{ "mode", "opacity", "luma": [lo, hi] }` for that appearance |
| `dark` | `{}` | overrides for the dark forms: `file` (default `layers/<id>-dark.svg` when it exists), `opacity`, `blend`, `shadow`, and a `tinted` object for tinted dark; missing keys inherit. No `clear` here: clear is light only |
| `dynamic` | none | for role `dynamic` only, see below |

| Role | clear | tinted | Use |
| --- | --- | --- | --- |
| `body` | `ramp` | `ramp` | the raised main pieces |
| `detail` | `ramp` | `ramp` | flat marks: lines, ticks, numerals |
| `highlight` | `keep` at opacity 0.6 | `keep` at opacity 0.6 | white sheens |
| `dynamic` | `ramp` | `ramp` | parts that move (clock hands and cap) |

A dark recolour is a `-dark.svg` drawn in the Apps Kit, never a colour rule in the manifest.

### Composition

Inputs: the appearance, the system light or dark form, the accent T (default `Accent/Amalfi`,
`#0e77e6`), the side in pt, the time. L is the OKLab lightness of a source pixel; alpha is never
changed by a mode, then the layer opacity applies.

1. Resolve each layer for the dark form when dark; drop layers with `min_size` above the side and
   layers whose mode is `hide`.
2. Background, over the body height:

   | Appearance | Light form | Dark form |
   | --- | --- | --- |
   | light / dark | `background.light` | `background.dark` |
   | clear | white 50 % → 25 % over the blurred backdrop | none: clear is light only |
   | tinted | T mixed with white 90 % → 76 % | T mixed with black 62 % → 84 % |

3. Each layer, bottom to top, through its mode (light and dark draw every layer as drawn):

   | Mode | clear (light only) | tinted, light form | tinted, dark form |
   | --- | --- | --- | --- |
   | `ramp` | grey, L → 105…255 | L 0 → T with black 70 %, 0.5 → T, 1 → white | L 0 → T with black 70 %, 1 → T with white 60 % |
   | `light` | grey, L → 200…255 | white shaded by L (200…255) | T with white 70 %, shaded by L |
   | `glass` | white glass, see below | not allowed | not allowed |
   | `accent` | not allowed | OKLCH(L, chroma and hue of T), chroma reduced into sRGB | same |
   | `keep` | as drawn | as drawn | as drawn |
   | `hide` | not drawn | not drawn | not drawn |

   `luma: [lo, hi]` replaces the ends of the ramp for one layer: grey levels 0–255 in clear,
   positions 0–1 on the tinted ramp in tinted.
   `glass`: inside the layer's alpha the stack below is blurred (σ 12 canvas units) and covered
   by white at opacity 0.85 (top of the layer) → 0.55 (bottom), with a 4-unit light lip along
   its top edge. At most one glass layer per icon.
4. Cast shadows from the layer alpha (neutral, or chromatic from its mean colour) in light, dark
   and tinted; in clear only for body and dynamic layers, at half strength.
5. Blend, clip to the body, draw the rim (format 1 values; clear and tinted use the light ones).

`tools/compose.py` follows steps 1–3 and 5 without shadows and rim (`--appearance clear|tinted`,
`--dark` for light and tinted only, `--accent`, `--time`): the check sheet shows the layers and their
transforms, the service adds shadows, rim and the backdrop blur. It clips with `tools/body.svg`,
renders every layer at the final size (hands already turned, their baked shadow offsets turned with
them, since resvg applies `feOffset` along the canvas axes), widens each filter region to the shape's
reach (the Sketch export writes regions from the shape before boolean operations, which clip some
shadows) and anti-aliases with 4 × 4 premultiplied samples per pixel.

### Dynamic layers

```json
{ "id": "hand-second", "role": "dynamic", "min_size": 64, "tinted": { "mode": "accent" },
  "dynamic": { "kind": "clock-hand", "unit": "second", "pivot": [512, 512] } }
```

`kind` is `clock-hand`, `clock-cap`, `calendar-month` or `calendar-day`; `unit` is `hour`,
`minute` or `second`; `pivot` is a canvas point (default `[512, 512]`); `source` is
`local-time` (default). A hand is drawn pointing to 12 and turns with the angles of the Clock
section above; the appearance transform is applied to the unrotated layer, then the layer turns,
then its shadow is cast (offset stays downward). The second hand follows the format 1 update rule.

### Fallback

`icon.png` and `icon-dark.png` are the whole icon at 1024, flat (body, layers, dynamic parts at
`fallback.time`), exported from the Apps Kit artboards. They serve where nothing composes: the
desktop entry, the hicolor copy, other desktops, a compiled file that does not load. For Clock
they show the hands at 10:09:30, the pose of the Apps Kit artboards.

During the pilot the format 1 renders `icon-clear.png` and `icon-tinted*.png` of the three pilot
icons stay in the repository as regression references for the service output (they are no longer
sources and have no hands on Clock); they are removed when the pilot ends.

### Apps Kit convention

In each `Apps / <Name> 1024` and `Apps / <Name> Dark 1024` artboard the artwork is one top-level
group per layer, named exactly the layer id, in manifest order, above the `Icon / Background`
instance (whose body style gives the background gradient). Clock's hands and cap are symbol
instances named `hand-hour`, `hand-minute`, `hand-second`, `cap`, from the full-canvas
`Dynamic / Clock / …` symbols drawn at 12; their layer files are those symbols. Light and dark
artboards have the same ids in the same order; a `-dark.svg` is exported only where the dark
group differs. Properties live only in `icon.json`; the ids in Sketch and in the manifest must
match one to one. `Grid / Overlay` is not exported.

### Format 1 icons

A format 1 app icon reads as format 2 with one `body` layer (`foreground.svg`) and the background
file; the clear and tinted looks come from the same rules. The other apps keep format 1 until
they move to `layers/`.

## Icons without layers

An app that has only a freedesktop icon (an already composed PNG or SVG) is reduced to the
square keyline and placed on a neutral background (white in light, graphite in dark).
