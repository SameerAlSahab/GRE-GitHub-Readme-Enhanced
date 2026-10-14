#!/usr/bin/env python3
"""GRE | neofetch_card.py

Render a GitHub profile as a neofetch-style terminal card: symbol art on the left, a mix of
the person's GitHub stats and (optionally) their own machine's specs on the right.
Output is plain text meant for a ```text code block in a README (GitHub can't show ANSI colors).

Run it ON THE USER'S MACHINE for real PC details; run it anywhere with --no-local for GitHub-only.

Usage:
  python neofetch_card.py USER                       # fetch profile via API + read this PC
  python neofetch_card.py --profile profile.json     # reuse output of fetch_profile.py
  python neofetch_card.py USER --art avatar          # avatar -> ASCII (needs: pip install pillow)
  python neofetch_card.py USER --art android --no-local
  python neofetch_card.py USER --fence               # wrap in ```text ... ```
  python neofetch_card.py USER --ansi                # colored, for terminal preview only

Privacy: hostname, username, IP and MAC are never printed. Review the output before you publish;
CPU/GPU/RAM/model are shown because the person asked for a "my setup" look.
"""
import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ARTS = {
    "tux": [
        "    .--.    ",
        "   |o_o |   ",
        "   |:_/ |   ",
        "  //   \\ \\  ",
        " (|     | ) ",
        "/'\\_   _/`\\ ",
        "\\___)=(___/ ",
    ],
    "android": [
        "   \\  ___  /  ",
        "   .-'   '-.  ",
        "  /  o   o  \\ ",
        " |           |",
        " |___________|",
        "  |  |   |  | ",
        "  |__|   |__| ",
    ],
    "gh": [
        "   .-\"\"\"\"-.   ",
        "  / ^    ^ \\  ",
        " |    ..    | ",
        "  \\  '--'  /  ",
        "  /`-.__.-'\\  ",
        " /  /    \\  \\ ",
        "(__/      \\__)",
    ],
}
RAMP = " .'`^\",:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
RAMP_SIMPLE = " .:-=+*#%@"


# ------------------------------------------------------------------ local system info
def sh(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=4).stdout.strip()
    except Exception:
        return ""


def is_android():
    return bool(os.environ.get("ANDROID_ROOT")) or os.path.exists("/system/build.prop")


def local_info():
    d = {}
    sysname = platform.system()
    if is_android():
        rel = sh("getprop ro.build.version.release")
        d["OS"] = f"Android {rel}".strip()
        model = (sh("getprop ro.product.manufacturer") + " " + sh("getprop ro.product.model")).strip()
        if model:
            d["Host"] = model
        rom = sh("getprop ro.build.display.id")
        if rom:
            d["ROM"] = rom
    elif sysname == "Linux":
        try:
            m = re.search(r'PRETTY_NAME="?([^"\n]+)', open("/etc/os-release").read())
            d["OS"] = m.group(1) if m else "Linux"
        except OSError:
            d["OS"] = "Linux"
        try:
            name = open("/sys/devices/virtual/dmi/id/product_name").read().strip()
            ver = open("/sys/devices/virtual/dmi/id/product_version").read().strip()
            if name and name.lower() not in ("to be filled by o.e.m.", "system product name"):
                d["Host"] = f"{name} {ver}".strip()
        except OSError:
            pass
    elif sysname == "Darwin":
        d["OS"] = f"macOS {platform.mac_ver()[0]}"
        model = sh("sysctl -n hw.model")
        if model:
            d["Host"] = model
    elif sysname == "Windows":
        d["OS"] = f"Windows {platform.release()} {platform.version()}"
    d["Kernel"] = platform.release()

    try:
        secs = float(open("/proc/uptime").read().split()[0])
        h, m = divmod(int(secs // 60), 60)
        dd, h = divmod(h, 24)
        d["Uptime"] = (f"{dd}d " if dd else "") + f"{h}h {m}m"
    except OSError:
        pass

    for tool, cmd in (("dpkg", "dpkg-query -f '.\\n' -W 2>/dev/null | wc -l"), ("pacman", "pacman -Qq 2>/dev/null | wc -l"),
                      ("rpm", "rpm -qa 2>/dev/null | wc -l")):
        if shutil.which(tool):
            n = sh(cmd)
            if n.isdigit() and int(n) > 0:
                d["Packages"] = f"{n} ({tool})"
            break

    shell = os.environ.get("SHELL") or os.environ.get("COMSPEC") or ""
    if shell:
        d["Shell"] = os.path.basename(shell).replace(".exe", "")
    term = os.environ.get("TERM_PROGRAM") or ("Windows Terminal" if os.environ.get("WT_SESSION") else os.environ.get("TERM", ""))
    if term:
        d["Terminal"] = term

    cpu = ""
    try:
        txt = open("/proc/cpuinfo").read()
        m = re.search(r"model name\s*:\s*(.+)", txt) or re.search(r"Hardware\s*:\s*(.+)", txt)
        cpu = m.group(1).strip() if m else ""
    except OSError:
        pass
    if not cpu and sysname == "Darwin":
        cpu = sh("sysctl -n machdep.cpu.brand_string")
    if not cpu:
        cpu = os.environ.get("PROCESSOR_IDENTIFIER", "") or platform.processor()
    if is_android() and not cpu:
        cpu = sh("getprop ro.soc.model") or sh("getprop ro.board.platform")
    if cpu:
        cpu = re.sub(r"\((R|TM|tm)\)|\bCPU\b|@.*$", "", cpu)
        cpu = re.sub(r"\s+", " ", cpu).strip()
        d["CPU"] = f"{cpu} ({os.cpu_count()})"

    if shutil.which("lspci"):
        g = [re.sub(r"^.*?: ", "", l) for l in sh("lspci").splitlines() if re.search(r"VGA|3D|Display", l)]
        if g:
            d["GPU"] = re.sub(r"\s*\(rev .*\)", "", g[0])[:48]

    try:
        mem = {k: int(v.split()[0]) for k, v in (l.split(":", 1) for l in open("/proc/meminfo"))}
        tot, av = mem["MemTotal"] // 1024, mem.get("MemAvailable", 0) // 1024
        d["Memory"] = f"{tot - av}MiB / {tot}MiB"
    except (OSError, KeyError, ValueError):
        if sysname == "Darwin":
            b = sh("sysctl -n hw.memsize")
            if b.isdigit():
                d["Memory"] = f"{int(b) // 2**30}GiB"
    return d


# ------------------------------------------------------------------ art
def avatar_art(url, width=26, invert=False, detailed=False):
    from io import BytesIO
    from urllib.request import Request, urlopen
    from PIL import Image, ImageOps
    req = Request(url + ("&" if "?" in url else "?") + "s=128", headers={"User-Agent": "gre-skill"})
    img = Image.open(BytesIO(urlopen(req, timeout=15).read())).convert("L")
    img = ImageOps.autocontrast(img)
    img = img.resize((width, max(1, int(width * 0.5))))  # characters are ~2x taller than wide
    ramp = RAMP if detailed else RAMP_SIMPLE
    if invert:
        ramp = ramp[::-1]
    px = img.load()
    return ["".join(ramp[px[x, y] * (len(ramp) - 1) // 255] for x in range(img.width)) for y in range(img.height)]


# ------------------------------------------------------------------ assemble
def years_ago(iso):
    t = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    y = (datetime.now(timezone.utc) - t).days // 365
    return f"{t.year} ({y}y)" if y else str(t.year)


def github_info(p):
    d = {}
    if p.get("name"):
        d["Name"] = p["name"]
    if p.get("bio"):
        d["Bio"] = p["bio"][:60]
    if p.get("company"):
        d["Company"] = p["company"]
    if p.get("location"):
        d["Location"] = p["location"]
    d["Repos"] = str(p["public_repos"])
    d["Stars"] = str(p.get("total_stars", 0))
    d["Followers"] = str(p["followers"])
    langs = list(p.get("languages", {}))[:4]
    if langs:
        d["Langs"] = ", ".join(langs)
    d["Joined"] = years_ago(p["created_at"])
    return d


def hex_to_ansi(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"\033[38;2;{r};{g};{b}m"


def render(title, art, groups, ansi=False, accent="FF1493"):
    c = hex_to_ansi(accent) if ansi else ""
    rst = "\033[0m" if ansi else ""
    right = [f"{c}{title}{rst}", "─" * len(title)]
    for g in groups:
        if not g:
            continue
        for k, v in g.items():
            right.append(f"{c}{k}{rst}: {v}")
        right.append("")
    while right and right[-1] == "":
        right.pop()
    w = max(len(l) for l in art) if art else 0
    n = max(len(art), len(right))
    art = art + [""] * (n - len(art))
    right = right + [""] * (n - len(right))
    return "\n".join(f"{c}{a.ljust(w)}{rst}   {r}".rstrip() for a, r in zip(art, right))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("user", nargs="?")
    ap.add_argument("--profile", help="JSON from fetch_profile.py (skips the network call)")
    ap.add_argument("--art", default="auto", help="auto | tux | android | gh | avatar | none | path/to/art.txt")
    ap.add_argument("--art-width", type=int, default=26)
    ap.add_argument("--invert", action="store_true", help="flip avatar brightness (use for light README backgrounds)")
    ap.add_argument("--detailed", action="store_true", help="avatar: use the long 70-level ramp")
    ap.add_argument("--no-local", action="store_true", help="GitHub fields only (no PC specs)")
    ap.add_argument("--no-github", action="store_true", help="PC specs only")
    ap.add_argument("--hide", nargs="*", default=[], help="field names to drop, e.g. --hide GPU Packages")
    ap.add_argument("--accent", default="FF1493")
    ap.add_argument("--ansi", action="store_true")
    ap.add_argument("--fence", action="store_true", help="wrap in a ```text code fence")
    a = ap.parse_args()

    profile = None
    if a.profile:
        profile = json.load(open(a.profile, encoding="utf-8"))
    elif a.user and not a.no_github:
        from fetch_profile import fetch
        profile = fetch(a.user)
    if not profile and not a.no_github:
        ap.error("give a USER or --profile (or use --no-github)")

    local = {} if a.no_local else local_info()
    gh = github_info(profile) if profile and not a.no_github else {}
    drop = {h.lower() for h in a.hide}
    local = {k: v for k, v in local.items() if k.lower() not in drop}
    gh = {k: v for k, v in gh.items() if k.lower() not in drop}

    art = None
    choice = a.art
    if choice == "avatar":
        try:
            art = avatar_art(profile["avatar_url"], a.art_width, a.invert, a.detailed)
        except Exception as e:
            print(f"# avatar art unavailable ({type(e).__name__}: {e}); using a built-in logo. "
                  f"Needs: pip install pillow, and network access to avatars.githubusercontent.com", file=sys.stderr)
            choice = "auto"
    if art is None:
        if choice in ("auto", "avatar"):
            choice = "android" if is_android() else ("tux" if platform.system() == "Linux" else "gh")
        if choice in ARTS:
            art = ARTS[choice]
        elif choice == "none":
            art = []
        elif os.path.exists(choice):
            art = open(choice, encoding="utf-8").read().splitlines()
        else:
            ap.error(f"unknown art '{choice}'")

    login = profile["login"] if profile else "me"
    title = f"{login}@github"
    out = render(title, art, [gh, local], a.ansi, a.accent)
    print(f"```text\n{out}\n```" if a.fence else out)


if __name__ == "__main__":
    main()
