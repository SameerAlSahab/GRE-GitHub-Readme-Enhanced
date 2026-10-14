# Layouts (how to assemble the page)

Templates live in `assets/templates/`; finished, lint-clean samples of each are in `assets/examples/`. Placeholders: `{{USER}}`, `{{ACCENT}}` (hex without #), `{{ACCENT_LC}}` (lowercase hex), and `{{...}}` for text the user must supply. Replace every placeholder; never ship one.

| template | feel | components |
|---|---|---|
| `showcase.md` | the full handmade look | typing, badges, dividers, about, spoiler, stats, trophies, now playing, views |
| `minimal.md` | clean and quiet | short about, icon strip, one stats card, links |
| `terminal.md` | hacker | neofetch card, typing, mono badges, snake |
| `bento.md` | dense, card-based | typing, badges, now list, stats + languages side by side, activity graph, stack in a spoiler, blog list |
| `org.md` | organization page | waving banner, mission line, repo table |
| `project.md` | professional project README | badges, features, install, usage, warnings, roadmap, star history, contributors, license, credits (see project-readme.md) |

## Standard order (showcase)
1. **Typing animation** (above the fold, centered)
2. **Badge row**: links first (Telegram, GitHub, ...), then skills below a divider
3. **Divider**
4. **About**: 2-4 sentences in the user's voice + one strikethrough or `<details>` easter egg
5. **Skills** (badges or skillicons; never both)
6. **Projects**: 3-6 repos as a table or a short list with a real one-line description each (from `top_repos`)
7. **Divider**
8. **Stats** (+ trophies or snake, one of them)
9. **Now Playing**
10. **Footer**: profile views counter, a last human line

Above-the-fold rule: on a phone the first screen should already show the typing line and the first badge row. Don't put a 200px banner and a header both before it.

## Counting
A good page has ~6-9 distinct components. Over 12 and it reads as a widget dump, and the linter warns above ~22 images. When the user hands you ten ideas, use the best six and keep the rest in a `<details>`.

## Project list pattern (no CSS needed)
```markdown
| project | what it is |
|---|---|
| [**repo-name**](https://github.com/{{USER}}/repo-name) | {{one real sentence from the repo description}} |
```
