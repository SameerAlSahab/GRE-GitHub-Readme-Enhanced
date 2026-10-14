# Licensing, secrets, third-party content, and DMCA

**Not legal advice.** Say so when it matters. Claude flags, explains and drafts; the owner decides, signs and sends. Scan results are **review items, never accusations**.

## 1. What the scan checks (`scripts/scan_repo.py`)
| flag | meaning | what to do |
|---|---|---|
| no LICENSE file | default copyright law: nobody may legally reuse the code | offer license options (below); don't choose for them |
| manifest license ≠ LICENSE file | contradictory signals | ask which is intended, fix the other |
| copyleft SPDX headers inside a permissive repo | possible incompatibility | tell the user to review those files/directories |
| copyright holders in headers that aren't the owner | bundled third-party code | keep their headers; credit them; check their license allows redistribution |
| "proprietary / confidential / do not distribute" wording | may not be redistributable | flag clearly; ask where it came from |
| bundled binaries/firmware (`.so .apk .jar .img .bin ...`), fonts, media | redistribution rights unknown | ask about origin; prefer a download script or separate repo; credit and license them |
| vendored dirs (`vendor/ third_party/ external/`) | other people's code | list in Credits with licenses |
| secret-looking strings or files (`.env`, keys, keystores) | **possible leak** | see section 3 |
| existing `DMCA.md` / `NOTICE` | prior legal history | read it before writing a policy |

## 2. Choosing a license (ask, don't decide)
Present the trade-off, let the owner pick, then `legal_notice.py license-section`:
| license | in one line | fits |
|---|---|---|
| MIT / ISC | do almost anything, keep the notice | libraries, tools, max adoption |
| Apache-2.0 | like MIT plus an explicit patent grant | bigger projects, companies; AOSP itself uses it |
| MPL-2.0 | changes to *your files* must stay open | middle ground |
| GPL-3.0 | derivatives must be open under GPL | tools you want kept open |
| AGPL-3.0 | GPL plus network use counts as distribution | services/SaaS |
| GPL-2.0 | Linux-kernel-style; kernel and many drivers are GPL-2.0-only | kernel/device trees that derive from the kernel |
| Unlicense / CC0 | public-domain dedication | snippets, data |
| CC-BY-4.0 / CC-BY-SA-4.0 | for docs, art, text (not software) | documentation, images |
Mixing: a project can't just relicense other people's GPL code as MIT. For Android work: platform code is mostly Apache-2.0, the kernel is GPL-2.0, and vendor blobs are usually proprietary and often not redistributable by you.

## 3. Secrets found in the repo
1. Tell the user first, with masked values and `path:line` only. **Never print a full secret in chat or in a README.**
2. Rotate/revoke the credential. Deleting the file is not enough: it's in git history and in clones.
3. Then remove it from history (mention `git filter-repo`/BFG) and force-push, knowing forks keep their copies.
4. Add the pattern to `.gitignore` and offer `.env.example` with fake values.
5. Only then write the README.

## 4. README notices (`scripts/legal_notice.py`)
- `license-section --spdx MIT --holder "Name" --repo OWNER/REPO` → License section with badge.
- `third-party "name|license|url" ...` → Credits table for bundled/used projects.
- `readme-policy --email you@example.com` → "Copyright & DMCA" section: how to reach the maintainer about infringement, third-party assets keep their licenses, trademark disclaimer. Add it when the repo bundles third-party material, accepts user uploads, mirrors content, or the owner wants it.
- Trademark/affiliation line when naming companies or devices (ROMs, firmware, fan projects): "not affiliated with or endorsed by ...".

## 5. DMCA takedown notices
**When it's appropriate:** the *user owns the copyright* (or is an authorized agent) and found their original work copied without permission. Not for things they merely dislike, for material their own license allows others to use, for public-domain or fair-use material, or for works they don't own.

**Before drafting, collect (ask for any missing, never invent):** owner's legal name, real contact email and postal address, what the work is and where the original lives (URLs, first-publication date, commit history showing authorship), the exact infringing URLs, and what was copied. Check the license: if the user's license *permits* the copying with attribution, the issue is license compliance, not necessarily a takedown.

**Draft:** `python scripts/legal_notice.py takedown --name ... --email ... --address ... --work "..." --original-url ... --infringing-url ...`. It refuses to run with missing facts. The notice contains the statutory pieces: identification of the work, identification of the infringing material, contact info, good-faith statement, fair-use consideration, accuracy/authorization statement under penalty of perjury, signature.

**Tell the user:**
- they must read every statement and be sure it's true; knowingly false claims carry liability
- consider a lawyer for anything high-stakes
- GitHub has its own DMCA takedown form and policy: confirm the current link in GitHub docs; Claude cannot submit it
- GitHub typically publishes notices in a public repository, so use a contact they're comfortable making public

**If the user *received* a takedown:** don't help evade or hide; explain the options: remove the disputed content, or, if they believe it was a mistake or they have a license/fair use, file a counter-notice (also under penalty of perjury, includes consent to jurisdiction; a lawyer is wise). Help them document their license and authorship.

**Claude does not:** send or file anything, draft a notice for a work the user doesn't own, claim someone infringed based only on a scan, or advise on dodging a notice.
