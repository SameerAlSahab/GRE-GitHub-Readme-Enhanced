#!/usr/bin/env python3
"""GRE | ytmusic.py

Build the "Now Playing" README block for YTMusicReadme from any YouTube / YouTube Music
link or a bare video id.

Usage:
  python ytmusic.py "https://music.youtube.com/watch?v=-eGM0IJc70Y"
  python ytmusic.py https://youtu.be/-eGM0IJc70Y --heading "Currently on repeat"
  python ytmusic.py -eGM0IJc70Y --credit
"""
import argparse
import re
import sys
from urllib.parse import parse_qs, quote, urlparse

WIDGET = "https://ytmusicreadme.vercel.app/api/widget?url="
CREDIT = "*Make yours from my [YTMusicReadme](https://github.com/SameerAlSahab/YTMusicReadme)*"


def video_id(s: str) -> str:
    s = s.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", s):
        return s
    u = urlparse(s if "://" in s else "https://" + s)
    if u.netloc.endswith("youtu.be"):
        vid = u.path.strip("/").split("/")[0]
    else:
        vid = (parse_qs(u.query).get("v") or [""])[0]
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", vid or ""):
        sys.exit("error: could not find an 11-character video id in that input")
    return vid


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("link")
    ap.add_argument("--heading", default="Now Playing")
    ap.add_argument("--level", type=int, default=2, help="markdown heading level")
    ap.add_argument("--credit", action="store_true", help="append a link to the widget project")
    a = ap.parse_args()

    vid = video_id(a.link)
    target = f"https://music.youtube.com/watch?v={vid}"
    block = f"{'#' * a.level} {a.heading}\n[![Now Playing]({WIDGET}{quote(target, safe='')})]({target})"
    if a.credit:
        block += "\n" + CREDIT
    print(block)


if __name__ == "__main__":
    main()
