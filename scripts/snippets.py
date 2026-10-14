#!/usr/bin/env python3
"""GRE | snippets.py

One-stop generator for the "widget" components so URLs are never typed by hand.

Subcommands:
  divider    capsule-render thin colored line          snippets.py divider --color FF1493
  header     capsule-render banner (waving, etc.)      snippets.py header --text "hey, i'm sam" --color FF1493,8A2BE2
  views      komarev profile-views counter             snippets.py views USER --color ff1493
  stats      githubstats.tech card (100+ themes)       snippets.py stats USER --theme sakura-blossom
  trophy     github-profile-trophy row                 snippets.py trophy USER --theme darkhub
  streak     streak-stats card                         snippets.py streak USER --theme dark
  icons      skillicons.dev icon strip                 snippets.py icons python,kotlin,cpp,linux
  snake      <picture> block for Platane/snk output    snippets.py snake USER
  langs      top-languages card (github-readme-stats)  snippets.py langs USER --theme tokyonight
  activity   contribution line graph                   snippets.py activity USER --color FF1493
  quote      random dev quote card                     snippets.py quote --theme dark
  workflow   GitHub Action for snake / blog-posts      snippets.py workflow snake
  pair       two images side by side (table layout)    snippets.py pair URL1 URL2

Notes:
  * githubstats.tech only activates for users who starred its repo; theme slugs come from the site's
    generator (https://www.githubstats.tech). 'sakura-blossom' is known-good.
  * All outputs are HTML <img>/<picture> so they can sit inside <p align="center">.
"""
import argparse
from urllib.parse import quote_plus


def wrap(inner: str, center: bool) -> str:
    return f'<p align="center">\n  {inner}\n</p>' if center else inner


def color_param(c: str) -> str:
    """'FF1493' -> 'FF1493'; 'FF1493,8A2BE2' -> '0:FF1493,100:8A2BE2' (capsule-render gradient)."""
    parts = [p.strip().lstrip("#") for p in c.split(",") if p.strip()]
    if len(parts) == 1:
        return parts[0]
    step = 100 // (len(parts) - 1)
    return ",".join(f"{i * step if i < len(parts) - 1 else 100}:{p}" for i, p in enumerate(parts))


def cmd_divider(a):
    url = f"https://capsule-render.vercel.app/api?type=rect&color={color_param(a.color)}&height={a.height}&section={a.section}"
    return wrap(f'<img width="100%" src="{url}" alt="" />', False)


def cmd_header(a):
    q = [f"type={a.type}", f"color={color_param(a.color)}", f"height={a.height}", f"section={a.section}"]
    if a.text:
        q += [f"text={quote_plus(a.text)}", f"fontSize={a.font_size}", f"fontColor={a.font_color.lstrip('#')}"]
        q.append("fontAlignY=" + str(a.font_align_y))
    if a.desc:
        q += [f"desc={quote_plus(a.desc)}", f"descSize={a.desc_size}", "descAlignY=" + str(a.font_align_y + 18)]
    if a.animation:
        q.append(f"animation={a.animation}")
    url = "https://capsule-render.vercel.app/api?" + "&".join(q)
    alt = a.text or "banner"
    return f'<img width="100%" src="{url}" alt="{alt}" />'


def cmd_views(a):
    url = (f"https://komarev.com/ghpvc/?username={a.user}&label={quote_plus(a.label)}"
           f"&color={a.color.lstrip('#').lower()}&style={a.style}")
    if a.abbreviated:
        url += "&abbreviated=true"
    return wrap(f'<img src="{url}" alt="{a.user} profile views" />', a.center)


STAT_FLAGS = ["name", "grade", "stars", "commits", "prs", "issues", "contributed", "year", "top_repo"]


def cmd_stats(a):
    on = {"name", "grade", "stars", "commits", "prs", "issues", "contributed"}  # sensible default set
    on |= set(a.show)
    on -= set(a.hide)
    flags = "&".join(f"show_{f}={1 if f in on else 0}" for f in STAT_FLAGS)
    url = f"https://www.githubstats.tech/api/card?username={a.user}&theme={a.theme}&size={a.size}&{flags}"
    return wrap(f'<img alt="{a.user} GitHub stats" src="{url}" />', a.center)


def cmd_trophy(a):
    q = [f"username={a.user}", f"theme={a.theme}", f"column={a.column}", f"row={a.row}",
         "margin-w=12", "margin-h=12"]
    if a.no_frame:
        q.append("no-frame=true")
    if a.no_bg:
        q.append("no-bg=true")
    if a.title:
        q.append("title=" + a.title)
    url = "https://github-profile-trophy.vercel.app/?" + "&".join(q)
    return wrap(f'<img src="{url}" alt="{a.user} trophies" />', a.center)


def cmd_streak(a):
    q = [f"user={a.user}", f"theme={a.theme}", "hide_border=true"]
    url = "https://streak-stats.demolab.com/?" + "&".join(q)
    return wrap(f'<img src="{url}" alt="{a.user} streak" />', a.center)


def cmd_icons(a):
    url = f"https://skillicons.dev/icons?i={a.names}&theme={a.theme}&perline={a.perline}"
    return wrap(f'<img src="{url}" alt="skills" />', a.center)


def cmd_snake(a):
    base = f"https://raw.githubusercontent.com/{a.user}/{a.user}/{a.branch}"
    return (f'<picture>\n'
            f'  <source media="(prefers-color-scheme: dark)" srcset="{base}/github-snake-dark.svg">\n'
            f'  <source media="(prefers-color-scheme: light)" srcset="{base}/github-snake.svg">\n'
            f'  <img alt="contribution snake" src="{base}/github-snake.svg" width="100%">\n'
            f'</picture>')


def cmd_langs(a):
    q = [f"username={a.user}", f"layout={a.layout}", f"theme={a.theme}", "hide_border=true",
         f"langs_count={a.count}", "bg_color=00000000" if a.transparent else ""]
    if a.hide:
        q.append("hide=" + ",".join(a.hide))
    url = "https://github-readme-stats.vercel.app/api/top-langs/?" + "&".join(x for x in q if x)
    return wrap(f'<img src="{url}" alt="{a.user} top languages" />', a.center)


def cmd_activity(a):
    c = a.color.lstrip("#")
    q = [f"username={a.user}", f"color={c}", f"line={c}", "point=FFFFFF", "area=true", f"area_color={c}",
         "hide_border=true", f"bg_color={a.bg.lstrip('#')}"]
    url = "https://github-readme-activity-graph.vercel.app/graph?" + "&".join(q)
    return wrap(f'<img src="{url}" alt="{a.user} contribution activity" width="100%" />', a.center)


def cmd_quote(a):
    url = f"https://quotes-github-readme.vercel.app/api?type={a.type}&theme={a.theme}"
    return wrap(f'<img src="{url}" alt="random developer quote" />', a.center)


def cmd_pair(a):
    cells = "".join(f'\n    <td valign="top" width="50%"><img src="{u}" alt="{alt}" width="100%" /></td>'
                    for u, alt in zip(a.urls, a.alts or ["", ""]))
    return f"<table>\n  <tr>{cells}\n  </tr>\n</table>"


WORKFLOWS = {
    "snake": """name: Generate Snake
on:
  schedule: [{ cron: "0 */12 * * *" }]
  workflow_dispatch:
  push: { branches: [main] }
permissions:
  contents: write
jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: Platane/snk/svg-only@v3
        with:
          github_user_name: ${{ github.repository_owner }}
          outputs: |
            dist/github-snake.svg
            dist/github-snake-dark.svg?palette=github-dark
      - uses: crazy-max/ghaction-github-pages@v3.1.0
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
""",
    "blog-posts": """# Put <!-- BLOG-POST-LIST:START --><!-- BLOG-POST-LIST:END --> in README.md where the list should appear.
name: Latest blog posts
on:
  schedule: [{ cron: "0 6 * * *" }]
  workflow_dispatch:
permissions:
  contents: write
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: gautamkrishnar/blog-post-workflow@v1
        with:
          feed_list: "https://example.com/feed.xml"   # your RSS/Atom feed
          max_post_count: 5
""",
}


def cmd_workflow(a):
    return WORKFLOWS[a.kind].rstrip()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("divider")
    p.add_argument("--color", default="FF1493")
    p.add_argument("--height", type=int, default=2)
    p.add_argument("--section", default="header", choices=["header", "footer"])
    p.set_defaults(fn=cmd_divider)

    p = sub.add_parser("header")
    p.add_argument("--type", default="waving",
                   choices=["waving", "venom", "shark", "slice", "soft", "egg", "cylinder", "rect", "transparent"])
    p.add_argument("--color", default="FF1493", help="hex, or 'a,b' for a gradient (also: auto, timeAuto)")
    p.add_argument("--height", type=int, default=200)
    p.add_argument("--section", default="header", choices=["header", "footer"])
    p.add_argument("--text", default="")
    p.add_argument("--desc", default="")
    p.add_argument("--font-size", type=int, default=50)
    p.add_argument("--desc-size", type=int, default=18)
    p.add_argument("--font-color", default="FFFFFF")
    p.add_argument("--font-align-y", type=int, default=40)
    p.add_argument("--animation", default="", choices=["", "fadeIn", "scaleIn", "blink", "blinking", "twinkling"])
    p.set_defaults(fn=cmd_header)

    p = sub.add_parser("views")
    p.add_argument("user")
    p.add_argument("--label", default="Profile views")
    p.add_argument("--color", default="ff1493")
    p.add_argument("--style", default="flat-square", choices=["flat", "flat-square", "for-the-badge", "plastic"])
    p.add_argument("--abbreviated", action="store_true")
    p.add_argument("--center", action="store_true")
    p.set_defaults(fn=cmd_views)

    p = sub.add_parser("stats")
    p.add_argument("user")
    p.add_argument("--theme", default="sakura-blossom")
    p.add_argument("--size", default="small", choices=["small", "default", "large"])
    p.add_argument("--show", nargs="*", default=[], choices=STAT_FLAGS)
    p.add_argument("--hide", nargs="*", default=[], choices=STAT_FLAGS)
    p.add_argument("--center", action="store_true")
    p.set_defaults(fn=cmd_stats)

    p = sub.add_parser("trophy")
    p.add_argument("user")
    p.add_argument("--theme", default="darkhub")
    p.add_argument("--column", type=int, default=7)
    p.add_argument("--row", type=int, default=1)
    p.add_argument("--title", default="")
    p.add_argument("--no-frame", action="store_true", default=True)
    p.add_argument("--no-bg", action="store_true", default=True)
    p.add_argument("--center", action="store_true")
    p.set_defaults(fn=cmd_trophy)

    p = sub.add_parser("streak")
    p.add_argument("user")
    p.add_argument("--theme", default="dark")
    p.add_argument("--center", action="store_true")
    p.set_defaults(fn=cmd_streak)

    p = sub.add_parser("icons")
    p.add_argument("names", help="comma-separated skillicons ids, e.g. python,kotlin,cpp")
    p.add_argument("--theme", default="dark", choices=["dark", "light"])
    p.add_argument("--perline", type=int, default=10)
    p.add_argument("--center", action="store_true")
    p.set_defaults(fn=cmd_icons)

    p = sub.add_parser("snake")
    p.add_argument("user")
    p.add_argument("--branch", default="output")
    p.set_defaults(fn=cmd_snake)

    p = sub.add_parser("langs")
    p.add_argument("user")
    p.add_argument("--theme", default="tokyonight")
    p.add_argument("--layout", default="compact", choices=["compact", "donut", "donut-vertical", "pie"])
    p.add_argument("--count", type=int, default=6)
    p.add_argument("--hide", nargs="*", default=[], help="languages to hide, e.g. html css")
    p.add_argument("--transparent", action="store_true")
    p.add_argument("--center", action="store_true")
    p.set_defaults(fn=cmd_langs)

    p = sub.add_parser("activity")
    p.add_argument("user")
    p.add_argument("--color", default="FF1493")
    p.add_argument("--bg", default="0D1117")
    p.add_argument("--center", action="store_true")
    p.set_defaults(fn=cmd_activity)

    p = sub.add_parser("quote")
    p.add_argument("--type", default="horizontal", choices=["horizontal", "vertical"])
    p.add_argument("--theme", default="dark")
    p.add_argument("--center", action="store_true")
    p.set_defaults(fn=cmd_quote)

    p = sub.add_parser("workflow")
    p.add_argument("kind", choices=sorted(WORKFLOWS))
    p.set_defaults(fn=cmd_workflow)

    p = sub.add_parser("pair")
    p.add_argument("urls", nargs=2)
    p.add_argument("--alts", nargs=2)
    p.set_defaults(fn=cmd_pair)

    a = ap.parse_args()
    print(a.fn(a))


if __name__ == "__main__":
    main()
