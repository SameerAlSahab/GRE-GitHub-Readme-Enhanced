#!/usr/bin/env python3
"""GRE | typing_svg.py

Turn plain-text lines (emoji welcome) into a ready-to-paste readme-typing-svg embed.
Doing the URL-encoding by script avoids the #1 failure: a broken emoji or a stray
space that silently kills the animation.

Usage:
  python typing_svg.py "Android / AOSP ROM Developer ⚡" "Hardware Security & Reverse Engineering 👨🏻‍💻" "Bricks phones for science 💎"
  python typing_svg.py "hi, i'm sam" "i break phones for fun" --color 00E5FF --size 22 --format url
"""
import argparse
import sys
import unicodedata
from urllib.parse import quote

HOST = "https://readme-typing-svg.demolab.com"


def enc(line: str) -> str:
    # ';' is the line separator for the service, so it can't appear inside a line.
    # Spaces become '+', everything else is percent-encoded UTF-8 (this is what makes emoji work).
    return quote(line.strip().replace(";", ","), safe="").replace("%20", "+")


def visual_len(s: str) -> int:
    """Rough on-screen width in monospace cells (emoji and CJK count as 2)."""
    n = 0
    for ch in s:
        if ch in "\u200d\ufe0f":
            continue
        if unicodedata.east_asian_width(ch) in ("W", "F") or ord(ch) >= 0x1F000:
            n += 2
        else:
            n += 1
    return n


def build_url(lines, font, weight, size, duration, pause, color, center, vcenter,
              width, height, repeat, random_order, letter_spacing):
    params = [
        ("font", font.replace(" ", "+")),
        ("weight", str(weight)),
        ("size", str(size)),
        ("duration", str(duration)),
        ("pause", str(pause)),
        ("color", color.lstrip("#").upper()),
        ("center", str(center).lower()),
        ("vCenter", str(vcenter).lower()),
        ("width", str(width)),
    ]
    if height:
        params.append(("height", str(height)))
    if letter_spacing:
        params.append(("letterSpacing", letter_spacing))
    if not repeat:
        params.append(("repeat", "false"))
    if random_order:
        params.append(("random", "true"))
    params.append(("lines", ";".join(enc(l) for l in lines)))
    return HOST + "?" + "&".join(f"{k}={v}" for k, v in params)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lines", nargs="+", help="one string per typed line (3-4 is the sweet spot)")
    ap.add_argument("--font", default="Fira Code")
    ap.add_argument("--weight", type=int, default=500)
    ap.add_argument("--size", type=int, default=20)
    ap.add_argument("--duration", type=int, default=3000, help="ms to type one line")
    ap.add_argument("--pause", type=int, default=900, help="ms to hold a finished line")
    ap.add_argument("--color", default="FF1493", help="hex, with or without #")
    ap.add_argument("--width", type=int, default=0, help="px; 0 = estimate from the longest line")
    ap.add_argument("--height", type=int, default=0)
    ap.add_argument("--left", action="store_true", help="left-align instead of center")
    ap.add_argument("--no-repeat", action="store_true", help="type once and stop")
    ap.add_argument("--random", action="store_true")
    ap.add_argument("--letter-spacing", default="")
    ap.add_argument("--format", choices=["html", "md", "url"], default="html")
    a = ap.parse_args()

    longest = max(visual_len(l) for l in a.lines)
    width = a.width or min(max(320, int(longest * a.size * 0.62) + 40), 880)

    if len(a.lines) > 5:
        print("# note: more than 5 lines gets tiresome to watch; consider trimming.", file=sys.stderr)
    for l in a.lines:
        if visual_len(l) > 60:
            print(f"# note: '{l[:30]}...' is long ({visual_len(l)} cells); it may clip on mobile.", file=sys.stderr)
        if ";" in l:
            print(f"# note: ';' in '{l[:30]}...' replaced with ',' (';' is the line separator).", file=sys.stderr)

    url = build_url(a.lines, a.font, a.weight, a.size, a.duration, a.pause, a.color,
                    not a.left, not a.left, width, a.height, not a.no_repeat, a.random, a.letter_spacing)
    alt = "Typing animation: " + " / ".join(a.lines)
    alt = alt.replace('"', "&quot;")

    if a.format == "url":
        print(url)
    elif a.format == "md":
        print(f"![{alt}]({url})")
    else:
        align = "left" if a.left else "center"
        print(f'<p align="{align}">\n  <img src="{url}" alt="{alt}" />\n</p>')


if __name__ == "__main__":
    main()
