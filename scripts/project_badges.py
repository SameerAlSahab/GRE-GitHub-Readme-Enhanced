#!/usr/bin/env python3
"""GRE | project_badges.py

Live badges and widgets for a PROJECT README (as opposed to a profile README):
stars, forks, issues, PRs, build status (passing/failing), license, release, last commit,
top language, size, contributors, downloads, coverage, package-registry versions,
star-history chart, contributors wall, repo pin card, owner rank card, and fun stickers.

Usage:
  python project_badges.py badges OWNER/REPO --workflow ci.yml --branch main
  python project_badges.py badges OWNER/REPO --set stars forks issues build license release --color FF1493
  python project_badges.py stars-history OWNER/REPO
  python project_badges.py contributors OWNER/REPO
  python project_badges.py pin OWNER/REPO --theme dark
  python project_badges.py stickers --kinds prs-welcome maintained made-with-love
  python project_badges.py registry --npm my-pkg --pypi my-pkg --crates my-crate

Notes:
  * Build-status badges keep shields' own green/red. Don't force --color on them (the script won't),
    otherwise a failing build would look just as pretty as a passing one.
  * --color sets the VALUE side of count badges; --label-color sets the label side.
"""
import argparse
from urllib.parse import quote

S = "https://img.shields.io"

# name -> (path template, label-for-alt, logo)
BADGES = {
    "stars": ("github/stars/{r}", "Stars", "github"),
    "forks": ("github/forks/{r}", "Forks", "github"),
    "watchers": ("github/watchers/{r}", "Watchers", "github"),
    "issues": ("github/issues/{r}", "Open issues", "github"),
    "issues-closed": ("github/issues-closed/{r}", "Closed issues", "github"),
    "prs": ("github/issues-pr/{r}", "Open PRs", "github"),
    "license": ("github/license/{r}", "License", None),
    "release": ("github/v/release/{r}", "Latest release", "github"),
    "tag": ("github/v/tag/{r}", "Latest tag", "github"),
    "last-commit": ("github/last-commit/{r}", "Last commit", "git"),
    "commit-activity": ("github/commit-activity/m/{r}", "Commits per month", "git"),
    "top-language": ("github/languages/top/{r}", "Top language", None),
    "code-size": ("github/languages/code-size/{r}", "Code size", None),
    "repo-size": ("github/repo-size/{r}", "Repo size", None),
    "contributors": ("github/contributors/{r}", "Contributors", "github"),
    "downloads": ("github/downloads/{r}/total", "Downloads", "github"),
    "created": ("github/created-at/{r}", "Created", None),
}
STATUS = {"build"}  # built from --workflow
DEFAULT_SET = ["build", "release", "license", "stars", "forks", "issues", "last-commit"]

STICKERS = {
    "prs-welcome": ("PRs welcome", f"{S}/badge/PRs-welcome-brightgreen?style={{style}}"),
    "maintained": ("Maintained", f"{S}/badge/maintained-yes-brightgreen?style={{style}}"),
    "made-with-love": ("Made with love", f"{S}/badge/made%20with-%E2%9D%A4-{{c}}?style={{style}}"),
    "open-source": ("Open source", f"{S}/badge/open%20source-yes-{{c}}?style={{style}}"),
    "works-on-my-machine": ("Works on my machine", f"{S}/badge/works%20on-my%20machine-{{c}}?style={{style}}"),
    "no-ai-slop": ("Hand written", f"{S}/badge/hand-written-yes-{{c}}?style={{style}}"),
    "wip": ("Work in progress", f"{S}/badge/status-work%20in%20progress-orange?style={{style}}"),
    "experimental": ("Experimental", f"{S}/badge/status-experimental-orange?style={{style}}"),
    "use-at-own-risk": ("Use at your own risk", f"{S}/badge/use%20at-your%20own%20risk-red?style={{style}}"),
}


def repo_ok(r):
    if r.count("/") != 1 or " " in r:
        raise SystemExit("error: repo must look like OWNER/REPO")
    return r


def badge_url(path, style, color=None, label_color=None, logo=None, logo_color="white", extra=""):
    q = [f"style={style}"]
    if color:
        q.append(f"color={color.lstrip('#')}")
    if label_color:
        q.append(f"labelColor={label_color.lstrip('#')}")
    if logo:
        q.append(f"logo={logo}&logoColor={logo_color}")
    if extra:
        q.append(extra)
    return f"{S}/{path}?" + "&".join(q)


def link_for(name, r, branch):
    base = f"https://github.com/{r}"
    return {"stars": f"{base}/stargazers", "forks": f"{base}/forks", "watchers": f"{base}/watchers",
            "issues": f"{base}/issues", "issues-closed": f"{base}/issues?q=is%3Aissue+is%3Aclosed",
            "prs": f"{base}/pulls", "license": f"{base}/blob/{branch}/LICENSE", "release": f"{base}/releases",
            "tag": f"{base}/tags", "last-commit": f"{base}/commits/{branch}", "contributors": f"{base}/graphs/contributors",
            "downloads": f"{base}/releases", "build": f"{base}/actions", "commit-activity": f"{base}/graphs/commit-activity"
            }.get(name, base)


def emit(items, center, fmt):
    """items: [(alt, url, href)]"""
    if fmt == "md":
        out = [f"[![{a}]({u})]({h})" for a, u, h in items]
        return " ".join(out)
    out = [f'<a href="{h}"><img src="{u}" alt="{a}" /></a>' for a, u, h in items]
    if center:
        return '<p align="center">\n  ' + "\n  ".join(out) + "\n</p>"
    return "\n".join(out)


def cmd_badges(a):
    r = repo_ok(a.repo)
    names = a.set or DEFAULT_SET
    items = []
    for n in names:
        if n == "build":
            if not a.workflow:
                print("# note: 'build' skipped: pass --workflow <file.yml> (see scan_repo.py ci list)", file=__import__("sys").stderr)
                continue
            url = badge_url(f"github/actions/workflow/status/{r}/{a.workflow}", a.style, None, a.label_color,
                            "githubactions", extra=f"branch={a.branch}")
            items.append(("Build status", url, link_for("build", r, a.branch)))
        elif n in BADGES:
            path, alt, logo = BADGES[n]
            url = badge_url(path.format(r=r), a.style, a.color, a.label_color, logo)
            items.append((alt, url, link_for(n, r, a.branch)))
        else:
            raise SystemExit(f"unknown badge '{n}'. choices: build, " + ", ".join(BADGES))
    if a.codecov:
        items.append(("Coverage", f"https://codecov.io/gh/{r}/branch/{a.branch}/graph/badge.svg", f"https://codecov.io/gh/{r}"))
    print(emit(items, a.center, a.format))


def cmd_stars_history(a):
    r = repo_ok(a.repo)
    base = f"https://api.star-history.com/svg?repos={r}&type=Date"
    print(f'<a href="https://star-history.com/#{r}&Date">\n'
          f'  <picture>\n'
          f'    <source media="(prefers-color-scheme: dark)" srcset="{base}&theme=dark" />\n'
          f'    <source media="(prefers-color-scheme: light)" srcset="{base}" />\n'
          f'    <img alt="Star History Chart" src="{base}" />\n'
          f'  </picture>\n</a>')


def cmd_contributors(a):
    r = repo_ok(a.repo)
    print(f'<a href="https://github.com/{r}/graphs/contributors">\n'
          f'  <img src="https://contrib.rocks/image?repo={r}" alt="Contributors" />\n</a>')


def cmd_pin(a):
    r = repo_ok(a.repo)
    o, n = r.split("/")
    url = f"https://github-readme-stats.vercel.app/api/pin/?username={o}&repo={n}&theme={a.theme}"
    print(f'<a href="https://github.com/{r}"><img src="{url}" alt="{r}" /></a>')


def cmd_stickers(a):
    c = a.color.lstrip("#")
    items = []
    for k in a.kinds:
        alt, tpl = STICKERS[k]
        items.append((alt, tpl.format(style=a.style, c=c), "#"))
    if a.format == "md":
        print(" ".join(f"![{al}]({u})" for al, u, _ in items))
    else:
        out = [f'<img src="{u}" alt="{al}" />' for al, u, _ in items]
        print('<p align="center">\n  ' + "\n  ".join(out) + "\n</p>" if a.center else "\n".join(out))


def cmd_registry(a):
    items = []
    for pkg in a.npm:
        items.append((f"npm {pkg}", badge_url(f"npm/v/{quote(pkg, safe='@/')}", a.style, None, a.label_color, "npm"),
                      f"https://www.npmjs.com/package/{pkg}"))
        items.append((f"npm downloads", badge_url(f"npm/dm/{quote(pkg, safe='@/')}", a.style, None, a.label_color), f"https://www.npmjs.com/package/{pkg}"))
    for pkg in a.pypi:
        items.append((f"PyPI {pkg}", badge_url(f"pypi/v/{pkg}", a.style, None, a.label_color, "pypi"), f"https://pypi.org/project/{pkg}/"))
        items.append(("Python versions", badge_url(f"pypi/pyversions/{pkg}", a.style, None, a.label_color), f"https://pypi.org/project/{pkg}/"))
    for pkg in a.crates:
        items.append((f"crates.io {pkg}", badge_url(f"crates/v/{pkg}", a.style, None, a.label_color, "rust"), f"https://crates.io/crates/{pkg}"))
    if not items:
        raise SystemExit("give --npm / --pypi / --crates")
    print(emit(items, a.center, a.format))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p, fmt_default="html"):
        p.add_argument("--style", default="for-the-badge", choices=["for-the-badge", "flat", "flat-square", "plastic", "social"])
        p.add_argument("--label-color", default=None, help="hex for the label side, e.g. 1a1a1a")
        p.add_argument("--center", action="store_true")
        p.add_argument("--format", choices=["html", "md"], default=fmt_default)

    p = sub.add_parser("badges")
    p.add_argument("repo")
    p.add_argument("--set", nargs="*", help="build " + " ".join(BADGES))
    p.add_argument("--workflow", help="workflow file name, e.g. ci.yml (needed for the build badge)")
    p.add_argument("--branch", default="main")
    p.add_argument("--color", default=None, help="value-side hex for count badges (not applied to build status)")
    p.add_argument("--codecov", action="store_true")
    common(p)
    p.set_defaults(fn=cmd_badges)

    p = sub.add_parser("stars-history"); p.add_argument("repo"); p.set_defaults(fn=cmd_stars_history)
    p = sub.add_parser("contributors"); p.add_argument("repo"); p.set_defaults(fn=cmd_contributors)
    p = sub.add_parser("pin"); p.add_argument("repo"); p.add_argument("--theme", default="dark"); p.set_defaults(fn=cmd_pin)

    p = sub.add_parser("stickers")
    p.add_argument("--kinds", nargs="+", default=["prs-welcome", "maintained"], choices=list(STICKERS))
    p.add_argument("--color", default="FF1493")
    common(p)
    p.set_defaults(fn=cmd_stickers)

    p = sub.add_parser("registry")
    p.add_argument("--npm", nargs="*", default=[]); p.add_argument("--pypi", nargs="*", default=[])
    p.add_argument("--crates", nargs="*", default=[])
    common(p)
    p.set_defaults(fn=cmd_registry)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
