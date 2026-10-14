# Dividers and banners (capsule-render)

## Thin colored divider
```html
<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=FF1493&height=2&section=header"/>
```
`python scripts/snippets.py divider --color FF1493 --height 2`
Use between major sections only (2-4 per page). Height 2-4 is a hairline; 6+ becomes a bar.

## Banner header / footer
`python scripts/snippets.py header --type waving --text "hey, i'm sam" --color FF1493,8A2BE2 --animation fadeIn`
Place the footer variant (`--section footer`) as the last element for a bookend.

| param | notes |
|---|---|
| `type` | `waving` `venom` `shark` `slice` `soft` `egg` `cylinder` `rect` `transparent` |
| `color` | hex; `0:hexA,100:hexB` for a gradient; `auto`; `timeAuto` (changes with time of day) |
| `height` | 120-220 for banners |
| `text`, `fontSize`, `fontColor`, `fontAlign`, `fontAlignY` | banner title. `+` for spaces |
| `desc`, `descSize`, `descAlignY` | subtitle |
| `animation` | `fadeIn` `scaleIn` `blink` `blinking` `twinkling` |
| `section` | `header` (curve at bottom) or `footer` (curve at top) |

## Gotchas
- `width="100%"` keeps it responsive. Don't set px widths.
- If you already have a typing animation, skip the banner text, or the top of the page gets noisy. A text-less `waving` banner above a typing line works well.
