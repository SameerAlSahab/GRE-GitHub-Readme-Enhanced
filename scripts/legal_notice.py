#!/usr/bin/env python3
"""GRE | legal_notice.py

Drafts for the legal-ish parts of a project README. These are TEMPLATES, not legal advice.

Subcommands:
  takedown        DMCA takedown notice DRAFT for a rights holder (refuses if required facts are missing)
  readme-policy   "Copyright & DMCA" section for a README (how people can contact you about infringement)
  license-section "License" section with badge, SPDX id, and copyright line
  third-party     THIRD_PARTY_NOTICES / "Credits" table from name|license|url entries

Examples:
  python legal_notice.py takedown --name "Jane Doe" --email jane@example.com \\
      --address "12 Example St, Dhaka, Bangladesh" \\
      --work "My Android ROM manifest and build scripts, first published 2024" \\
      --original-url https://github.com/jane/rom \\
      --infringing-url https://github.com/copycat/rom-fork/blob/main/build.sh
  python legal_notice.py readme-policy --email jane@example.com
  python legal_notice.py license-section --spdx MIT --holder "Jane Doe" --year 2026 --repo jane/rom
  python legal_notice.py third-party "libfoo|MIT|https://github.com/foo/libfoo" "somefont|OFL-1.1|https://example.com"

Rules baked in: the person signing must be the copyright owner or an authorized agent, the facts must be
true, and the notice is made under penalty of perjury. Claude drafts; the human reviews and submits it.
"""
import argparse
import sys
from datetime import date

DISCLAIMER = ("<!-- DRAFT. Not legal advice. Only the copyright owner (or an authorized agent) may send this, "
              "every statement must be true, and it is made under penalty of perjury. "
              "Consider asking a lawyer. Do not send it if you are unsure the material is infringing "
              "(fair use, licenses and public-domain material are not infringement). -->\n")

TAKEDOWN = """{disclaimer}
# DMCA takedown notice (draft)

**To:** GitHub Copyright Agent (submit through GitHub's DMCA takedown form, confirm the current link in GitHub's DMCA policy docs)
**Date:** {date}

Hello,

I am writing to notify you of material hosted on GitHub that infringes my copyright{agent_clause}.

## 1. The copyrighted work
{work}

Original location(s):
{originals}

## 2. The infringing material
The following URL(s) contain material that I believe copies the work above without authorization:
{infringing}

{extent}
## 3. My contact information
- Name: {name}
- Email: {email}
- Address: {address}
{phone}
## 4. Statements
- I have a good faith belief that use of the copyrighted material described above is not authorized by the copyright owner, its agent, or the law.
- I have taken fair use into consideration.
- I swear, under penalty of perjury, that the information in this notification is accurate and that I am the copyright owner, or am authorized to act on behalf of the owner of an exclusive right that is allegedly infringed.

## 5. Signature
/s/ {name}
"""

POLICY = """## Copyright & DMCA

This project respects other people's intellectual property and asks that you do too.

- Third-party code, fonts and assets keep their original licenses; see [Credits](#credits) where applicable.
- If you believe something in this repository infringes your copyright, email **{email}** with: what the work is, where it appears here (links), and how to reach you. I'll look into it promptly and remove material that shouldn't be here.
- Formal notices can also be sent to GitHub through its [DMCA process](https://docs.github.com/en/site-policy/content-removal-policies/dmca-takedown-policy).
- This project is provided as is, with no affiliation with or endorsement by any trademark owner named in it.
"""

LICENSE_SEC = """## License

{badge}

{line}
{copyright}
"""

NAMES = {"MIT": "MIT License", "Apache-2.0": "Apache License 2.0", "GPL-3.0": "GNU GPL v3.0",
         "GPL-2.0": "GNU GPL v2.0", "AGPL-3.0": "GNU AGPL v3.0", "LGPL-3.0": "GNU LGPL v3.0",
         "MPL-2.0": "Mozilla Public License 2.0", "BSD-3-Clause": "BSD 3-Clause License",
         "BSD-2-Clause": "BSD 2-Clause License", "ISC": "ISC License", "Unlicense": "The Unlicense",
         "CC0-1.0": "CC0 1.0 Universal", "CC-BY-4.0": "Creative Commons Attribution 4.0"}


def cmd_takedown(a):
    missing = [k for k in ("name", "email", "address", "work", "original_url", "infringing_url") if not getattr(a, k)]
    if missing:
        sys.exit("error: cannot draft a takedown without these facts: " + ", ".join("--" + m.replace("_", "-") for m in missing)
                 + "\nAsk the user for them. Never invent contact details, URLs or the description of the work.")
    agent = f", as authorized agent of {a.owner}" if a.owner else ""
    print(TAKEDOWN.format(
        disclaimer=DISCLAIMER, date=date.today().isoformat(), agent_clause=agent, work=a.work,
        originals="\n".join(f"- {u}" for u in a.original_url),
        infringing="\n".join(f"- {u}" for u in a.infringing_url),
        extent=(f"Extent of copying: {a.extent}\n\n" if a.extent else ""),
        name=a.name, email=a.email, address=a.address,
        phone=(f"- Phone: {a.phone}\n" if a.phone else "")))


def cmd_policy(a):
    print(POLICY.format(email=a.email))


def cmd_license(a):
    name = NAMES.get(a.spdx, a.spdx)
    badge = f"[![License: {a.spdx}](https://img.shields.io/badge/License-{a.spdx.replace('-', '--')}-{a.color.lstrip('#')}?style={a.style})]"
    badge += f"(https://github.com/{a.repo}/blob/{a.branch}/LICENSE)" if a.repo else "(LICENSE)"
    line = f"Released under the **{name}**. See [LICENSE](LICENSE) for the full text."
    cr = f"\nCopyright (c) {a.year} {a.holder}" if a.holder else ""
    print(LICENSE_SEC.format(badge=badge, line=line, copyright=cr))


def cmd_third(a):
    rows = []
    for e in a.entries:
        parts = [p.strip() for p in e.split("|")]
        while len(parts) < 3:
            parts.append("")
        rows.append(f"| {parts[0]} | {parts[1]} | {('[link](' + parts[2] + ')') if parts[2] else ''} |")
    print("## Credits\n\nBuilt with or bundling the following; each keeps its own license.\n\n"
          "| project | license | source |\n|---|---|---|\n" + "\n".join(rows) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("takedown")
    p.add_argument("--name"); p.add_argument("--email"); p.add_argument("--address"); p.add_argument("--phone")
    p.add_argument("--work", help="what the copyrighted work is, in plain words")
    p.add_argument("--original-url", action="append", help="where the original lives (repeatable)")
    p.add_argument("--infringing-url", action="append", help="exact URLs of the infringing files/repos (repeatable)")
    p.add_argument("--owner", help="if you are an agent: the rights owner's name")
    p.add_argument("--extent", help="optional: what was copied (e.g. 'entire build.sh, verbatim')")
    p.set_defaults(fn=cmd_takedown)

    p = sub.add_parser("readme-policy"); p.add_argument("--email", required=True); p.set_defaults(fn=cmd_policy)

    p = sub.add_parser("license-section")
    p.add_argument("--spdx", required=True); p.add_argument("--holder"); p.add_argument("--year", default=str(date.today().year))
    p.add_argument("--repo"); p.add_argument("--branch", default="main")
    p.add_argument("--color", default="blue"); p.add_argument("--style", default="for-the-badge")
    p.set_defaults(fn=cmd_license)

    p = sub.add_parser("third-party"); p.add_argument("entries", nargs="+", help="'name|license|url'")
    p.set_defaults(fn=cmd_third)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
