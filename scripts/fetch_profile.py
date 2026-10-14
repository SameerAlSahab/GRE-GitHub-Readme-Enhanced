#!/usr/bin/env python3
"""GRE | fetch_profile.py

Pull a user's public GitHub data so GRE can write a README from facts instead of guesses.
Stdlib only. Uses the REST API; set GITHUB_TOKEN to lift the 60 requests/hour limit.

Usage:
  python fetch_profile.py USER                 # JSON summary to stdout
  python fetch_profile.py USER --bytes         # also weigh languages by bytes (extra API calls)
  python fetch_profile.py USER --save-readme current_readme.md

Output keys: login, name, bio, company, location, blog, twitter, followers, following,
public_repos, created_at, avatar_url, total_stars, languages (by repo count or bytes),
topics, top_repos (by stars), recent_repos (by push), has_profile_readme, profile_readme.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from collections import Counter

API = "https://api.github.com"


def get(path, accept="application/vnd.github+json", raw=False):
    req = urllib.request.Request(API + path if path.startswith("/") else path)
    req.add_header("Accept", accept)
    req.add_header("User-Agent", "gre-skill")
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=20) as r:
        data = r.read()
    return data.decode("utf-8", "replace") if raw else json.loads(data)


def fetch(user: str, by_bytes: bool = False) -> dict:
    try:
        u = get(f"/users/{user}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            sys.exit(f"error: no GitHub user named '{user}'")
        if e.code in (403, 429):
            sys.exit("error: rate limited by GitHub. Set GITHUB_TOKEN or wait an hour.")
        raise
    repos = get(f"/users/{user}/repos?per_page=100&sort=pushed&type=owner")
    own = [r for r in repos if not r.get("fork")]

    langs = Counter(r["language"] for r in own if r.get("language"))
    if by_bytes:
        langs = Counter()
        for r in own[:10]:
            try:
                for k, v in get(f"/repos/{user}/{r['name']}/languages").items():
                    langs[k] += v
            except Exception:
                pass
    topics = Counter(t for r in own for t in (r.get("topics") or []))

    def slim(r):
        return {"name": r["name"], "description": r.get("description"), "stars": r["stargazers_count"],
                "language": r.get("language"), "url": r["html_url"], "topics": r.get("topics", []),
                "pushed_at": r.get("pushed_at")}

    readme = None
    try:
        readme = get(f"/repos/{user}/{user}/readme", accept="application/vnd.github.raw", raw=True)
    except Exception:
        pass

    return {
        "login": u["login"], "name": u.get("name"), "bio": u.get("bio"), "company": u.get("company"),
        "location": u.get("location"), "blog": u.get("blog"), "twitter": u.get("twitter_username"),
        "followers": u["followers"], "following": u["following"], "public_repos": u["public_repos"],
        "created_at": u["created_at"], "avatar_url": u["avatar_url"],
        "total_stars": sum(r["stargazers_count"] for r in own),
        "languages": dict(langs.most_common(8)),
        "topics": [t for t, _ in topics.most_common(12)],
        "top_repos": [slim(r) for r in sorted(own, key=lambda r: -r["stargazers_count"])[:6]],
        "recent_repos": [slim(r) for r in own[:6]],
        "has_profile_readme": readme is not None,
        "profile_readme": readme,
        "note": "repos list is capped at the 100 most recently pushed; stats are public data only",
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("user")
    ap.add_argument("--bytes", action="store_true", help="weigh languages by bytes of code")
    ap.add_argument("--save-readme", metavar="PATH", help="write the current profile README here")
    a = ap.parse_args()

    d = fetch(a.user, a.bytes)
    if a.save_readme and d["profile_readme"]:
        with open(a.save_readme, "w", encoding="utf-8") as f:
            f.write(d["profile_readme"])
    if a.save_readme:
        d["profile_readme"] = f"(saved to {a.save_readme})" if d["has_profile_readme"] else None
    print(json.dumps(d, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
