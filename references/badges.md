# Badges and icons (shields.io, skillicons)

Used for skills, languages, tools and social links. Cohesion beats variety: pick one `style` and one color strategy for the whole page.

## Snippet
```markdown
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
[![Telegram](https://img.shields.io/badge/Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/you)
```
Generate with `python scripts/badge.py python kotlin cpp --style for-the-badge` and for links `--link "Telegram=https://t.me/you"`.

## Color strategy (choose one)
- **Brand colors** (`--color auto`): recognisable, busier. Good for a big skills grid.
- **Single accent** (`--color FF1493`): every badge in the page accent. This is what makes a handmade page look designed. Default for GRE.
- **Monochrome dark** (`--color 1a1a1a` + `--label-color`): hacker look.

## Styles
`for-the-badge` (big, bold, default), `flat`, `flat-square` (tight, good for a counters row), `plastic`, `social`.

## Escaping rules (the script does this)
In the label: `-` becomes `--`, `_` becomes `__`, space becomes `%20` or `_`, `+` becomes `%2B`, `#` becomes `%23`.
Two-segment form `badge/<text>-<color>` shows only the text on a colored background.

## Logos
`logo=<slug>` uses a simple-icons slug (find it on simpleicons.org). If no logo appears the slug is wrong or the brand icon was removed from simple-icons; try another slug, or drop the logo. Light brand colors need `logoColor=black` (the script picks this automatically).

## skillicons.dev (icon-only strips)
`https://skillicons.dev/icons?i=python,kotlin,cpp,linux&theme=dark&perline=10`
Great as a clean alternative to badge walls. Don't use both for the same list.

## Link badges worth having
Telegram, GitHub, X, YouTube, Discord, Gmail, XDA, Ko-fi. Make every link badge actually clickable and never invent a URL; ask for it or leave it out.
