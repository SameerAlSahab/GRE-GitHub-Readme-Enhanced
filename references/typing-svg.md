# Typing animation (readme-typing-svg)

An animated, self-typing banner line. It is the first thing people see, so it carries the identity of the page.

## Snippet
```html
<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=20&duration=3000&pause=900&color=FF1493&center=true&vCenter=true&width=800&lines=Line+one+%E2%9A%A1;Line+two;Line+three+%F0%9F%92%8E" alt="Typing animation" />
</p>
```

**Always generate it with the script**, never by hand. Emoji must be percent-encoded UTF-8 and a single wrong byte kills the animation:
`python scripts/typing_svg.py "line one ⚡" "line two" "line three 💎" --color FF1493`

## Parameters
| param | meaning | default used by GRE |
|---|---|---|
| `lines` | typed lines, separated by a literal `;` (so `;` can't appear inside a line) | required |
| `font` | any Google Font, spaces as `+` | `Fira+Code` |
| `weight`, `size` | font weight / px | 500 / 20 |
| `duration` | ms to type one line | 3000 |
| `pause` | ms to hold a finished line | 900 |
| `color` | hex without `#` | the page accent |
| `center`, `vCenter` | center horizontally / vertically in the box | true |
| `width`, `height` | canvas size px; too small clips text | width ≈ longest line, ≤ 880 |
| `repeat=false` | type once and stop | off |
| `random=true` | shuffle line order | off |
| `letterSpacing` | e.g. `0.1em` | off |
| `multiline=true` | each line stays on screen below the last | off |

## How to write the lines (analyze the user, don't template)
Pull from `fetch_profile.py` output or what the user told you:
1. **Line 1: what they are**, in their own words ("Android / AOSP ROM Developer").
2. **Line 2: the deeper specialty or obsession** ("Hardware Security & Reverse Engineering").
3. **Line 3: a personality line**, something only this person would say ("Bricks phones for science").
4. Optional line 4: a current project or a joke.

Rules: 3-4 lines, each under ~45 characters (mobile clips past ~60). At most one emoji per line, and not on every line. Real facts only. Apply the human-writing rules; a typing line is the most visible sentence on the page.

## Gotchas
- Served by a third-party host; if it's down the `alt` text shows. Write a useful alt.
- `readme-typing-svg.demolab.com` is the maintained host; older hosts are dead.
- Keep the accent `color` identical to badges and dividers.
