#!/usr/bin/env python3
"""GRE | badge.py

Generate shields.io badges for skills / languages / tools and for social links,
with one consistent look. Handles shields' escaping rules (- -> --, _ -> __, spaces, '+', '#').

Usage:
  python badge.py python kotlin cpp bash linux --style for-the-badge
  python badge.py python kotlin --color FF1493            # force one accent for every badge (cohesive look)
  python badge.py --link "Telegram=https://t.me/you" --link "GitHub=https://github.com/you" --center
  python badge.py "Reverse Engineering" --logo ghidra --color 262626   # custom label

Unknown names still work: the slug is guessed from the name. If the logo doesn't show,
look the slug up on https://simpleicons.org and pass --logo <slug>.
"""
import argparse
import re
from urllib.parse import quote

# key -> (label, simple-icons slug, brand hex)
TECH = {
    "python": ("Python", "python", "3776AB"),
    "kotlin": ("Kotlin", "kotlin", "7F52B0"),
    "java": ("Java", "openjdk", "ED8B00"),
    "cpp": ("C++", "cplusplus", "00599C"),
    "c": ("C", "c", "A8B9CC"),
    "rust": ("Rust", "rust", "000000"),
    "go": ("Go", "go", "00ADD8"),
    "javascript": ("JavaScript", "javascript", "F7DF1E"),
    "typescript": ("TypeScript", "typescript", "3178C6"),
    "bash": ("Bash", "gnubash", "4EAA25"),
    "shell": ("Shell", "gnubash", "4EAA25"),
    "lua": ("Lua", "lua", "2C2D72"),
    "php": ("PHP", "php", "777BB4"),
    "ruby": ("Ruby", "ruby", "CC342D"),
    "swift": ("Swift", "swift", "F05138"),
    "dart": ("Dart", "dart", "0175C2"),
    "flutter": ("Flutter", "flutter", "02569B"),
    "html": ("HTML5", "html5", "E34F26"),
    "css": ("CSS3", "css3", "1572B6"),
    "react": ("React", "react", "20232A"),
    "vue": ("Vue.js", "vuedotjs", "4FC08D"),
    "svelte": ("Svelte", "svelte", "FF3E00"),
    "nextjs": ("Next.js", "nextdotjs", "000000"),
    "nodejs": ("Node.js", "nodedotjs", "5FA04E"),
    "tailwind": ("Tailwind CSS", "tailwindcss", "06B6D4"),
    "linux": ("Linux", "linux", "FCC624"),
    "android": ("Android", "android", "3DDC84"),
    "arch": ("Arch Linux", "archlinux", "1793D1"),
    "ubuntu": ("Ubuntu", "ubuntu", "E95420"),
    "debian": ("Debian", "debian", "A81D33"),
    "fedora": ("Fedora", "fedora", "51A2DA"),
    "nixos": ("NixOS", "nixos", "5277C3"),
    "kali": ("Kali Linux", "kalilinux", "557C94"),
    "docker": ("Docker", "docker", "2496ED"),
    "git": ("Git", "git", "F05032"),
    "github": ("GitHub", "github", "181717"),
    "githubactions": ("GitHub Actions", "githubactions", "2088FF"),
    "gradle": ("Gradle", "gradle", "02303A"),
    "cmake": ("CMake", "cmake", "064F8C"),
    "neovim": ("Neovim", "neovim", "57A143"),
    "vim": ("Vim", "vim", "019733"),
    "arduino": ("Arduino", "arduino", "00878F"),
    "raspberrypi": ("Raspberry Pi", "raspberrypi", "A22846"),
    "sqlite": ("SQLite", "sqlite", "003B57"),
    "postgresql": ("PostgreSQL", "postgresql", "4169E1"),
    "mongodb": ("MongoDB", "mongodb", "47A248"),
    "redis": ("Redis", "redis", "DC382D"),
    "nginx": ("Nginx", "nginx", "009639"),
    "firebase": ("Firebase", "firebase", "FFCA28"),
    "figma": ("Figma", "figma", "F24E1E"),
    # social / link badges
    "telegram": ("Telegram", "telegram", "26A5E4"),
    "discord": ("Discord", "discord", "5865F2"),
    "youtube": ("YouTube", "youtube", "FF0000"),
    "x": ("X", "x", "000000"),
    "twitter": ("Twitter", "x", "000000"),
    "instagram": ("Instagram", "instagram", "E4405F"),
    "reddit": ("Reddit", "reddit", "FF4500"),
    "twitch": ("Twitch", "twitch", "9146FF"),
    "mastodon": ("Mastodon", "mastodon", "6364FF"),
    "bluesky": ("Bluesky", "bluesky", "0285FF"),
    "gmail": ("Gmail", "gmail", "EA4335"),
    "kofi": ("Ko-fi", "kofi", "FF5E5B"),
    "buymeacoffee": ("Buy Me a Coffee", "buymeacoffee", "FFDD00"),
    "stackoverflow": ("Stack Overflow", "stackoverflow", "F58025"),
    "xda": ("XDA", "xdadevelopers", "EA7C07"),
}
ALIASES = {"c++": "cpp", "cplusplus": "cpp", "js": "javascript", "ts": "typescript", "node": "nodejs",
           "golang": "go", "gh": "github", "tg": "telegram", "postgres": "postgresql", "gnubash": "bash",
           "html5": "html", "css3": "css", "tailwindcss": "tailwind", "archlinux": "arch", "yt": "youtube"}


def key_of(name: str) -> str:
    k = name.strip().lower()
    if k in ALIASES:
        return ALIASES[k]
    k2 = re.sub(r"[\s\-_.]", "", k)
    return ALIASES.get(k2, k2)


def guess_slug(name: str) -> str:
    """Single-word names usually match their simple-icons slug; phrases never do."""
    return "" if re.search(r"\s", name.strip()) else re.sub(r"[^a-z0-9]", "", name.lower())


def luminance(hexcolor: str) -> float:
    r, g, b = (int(hexcolor[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def esc(label: str) -> str:
    return quote(label.replace("-", "--").replace("_", "__"), safe="")


def make_url(label, slug, color, style, logo_color=None, label_color=None):
    color = color.lstrip("#").upper()
    if logo_color is None:
        logo_color = "black" if luminance(color) > 0.55 else "white"
    url = f"https://img.shields.io/badge/{esc(label)}-{color}?style={style}"
    if slug:
        url += f"&logo={slug}&logoColor={logo_color}"
    if label_color:
        url += f"&labelColor={label_color.lstrip('#')}"
    return url


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*", help="tech names (python, kotlin, c++, ...) or any custom label")
    ap.add_argument("--link", action="append", default=[], metavar="NAME=URL",
                    help="clickable social badge, e.g. Telegram=https://t.me/you (repeatable)")
    ap.add_argument("--style", default="for-the-badge",
                    choices=["for-the-badge", "flat", "flat-square", "plastic", "social"])
    ap.add_argument("--color", default="auto", help="'auto' = brand colors, or one hex for all badges")
    ap.add_argument("--logo", help="override the simple-icons slug (single badge)")
    ap.add_argument("--logo-color", help="override logo color for all badges")
    ap.add_argument("--center", action="store_true", help="wrap in <p align=center> (emits HTML <img> tags)")
    ap.add_argument("--format", choices=["md", "html"], default=None)
    a = ap.parse_args()

    items = []  # (label, slug, color, href)
    for n in a.names:
        k = key_of(n)
        label, slug, brand = TECH.get(k, (n, guess_slug(n), "555555"))
        if a.logo and len(a.names) == 1:
            slug = a.logo
        items.append((label, slug, brand, None))
    for spec in a.link:
        name, _, href = spec.partition("=")
        k = key_of(name)
        label, slug, brand = TECH.get(k, (name, guess_slug(name), "555555"))
        items.append((label, slug, brand, href))

    if not items:
        ap.error("give at least one name or --link")

    fmt = a.format or ("html" if a.center else "md")
    out = []
    for label, slug, brand, href in items:
        color = brand if a.color == "auto" else a.color
        url = make_url(label, slug, color, a.style, a.logo_color)
        if fmt == "md":
            img = f"![{label}]({url})"
            out.append(f"[{img}]({href})" if href else img)
        else:
            img = f'<img src="{url}" alt="{label}" />'
            out.append(f'<a href="{href}">{img}</a>' if href else img)

    if fmt == "html":
        body = "\n  ".join(out)
        print(f'<p align="center">\n  {body}\n</p>' if a.center else "\n".join(out))
    else:
        print(" ".join(out))


if __name__ == "__main__":
    main()
