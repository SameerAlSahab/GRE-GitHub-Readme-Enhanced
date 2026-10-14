# Stats, trophies, counters, snake

All of these are SVGs from third-party servers. Pick a theme that matches the page accent and use `snippets.py` to build the URLs.

## githubstats.tech card (100+ themes)
```html
<p align="center">
<img alt="USER's GitHub Stats" src="https://www.githubstats.tech/api/card?username=USER&theme=sakura-blossom&size=small&show_name=1&show_grade=1&show_stars=1&show_commits=1&show_prs=1&show_issues=1&show_contributed=1&show_year=0&show_top_repo=0" />
</p>
```
`python scripts/snippets.py stats USER --theme sakura-blossom --center`
- Params: `username`, `theme`, `size` (small/default/large), and `show_name`, `show_grade`, `show_stars`, `show_commits`, `show_prs`, `show_issues`, `show_contributed`, `show_year`, `show_top_repo` (1/0).
- **The user must star https://github.com/SameerAlSahab/InsaneGitStatsGen to activate their card.** Tell them; otherwise it won't render.
- Theme slugs: `sakura-blossom` is confirmed. The site lists named themes (Catppuccin Mocha, Tokyo Night, Dracula, Cyberpunk 2077, Nord, Gruvbox Material, Monokai Pro, Synthwave Neon, One Dark, Rose Pine, AMOLED Black, Emerald Dark, Matrix, Horizon Dark, Solarized Dark, plus flag themes). Slugs for those aren't guaranteed to be plain kebab-case, so verify: if web access is available fetch https://www.githubstats.tech; otherwise tell the user to pick on the site and paste the URL from its Markdown copy button.
- Cached about 30 minutes.

## Trophies (github-profile-trophy)
`https://github-profile-trophy.vercel.app/?username=USER&theme=darkhub&column=7&row=1&margin-w=12&margin-h=12&no-frame=true&no-bg=true`
Common themes: `flat`, `onedark`, `gruvbox`, `dracula`, `monokai`, `nord`, `darkhub`, `radical`, `tokyonight`, `matrix`, `discord`, `algolia`. `no-bg` + `no-frame` blends it into any README background. Public instance is sometimes rate-limited; for a big profile suggest self-hosting.

## Profile views (komarev)
`https://komarev.com/ghpvc/?username=USER&label=Profile+views&color=ff1493&style=flat-square`
Counts page loads, so it climbs on its own. Put it in a counters row with `flat-square` badges. Optional `abbreviated=true`.

## Top languages
`python scripts/snippets.py langs USER --layout donut --count 6 --hide html css --center`
Layouts: `compact` (default), `donut`, `donut-vertical`, `pie`. Counts languages by repo bytes, so it over-weights generated or vendored code; hide noise with `--hide`. Served by the public github-readme-stats instance, which is often rate-limited. Pair it with the stats card in a two-column table: `python scripts/snippets.py pair URL1 URL2`.

## Activity graph
`python scripts/snippets.py activity USER --color FF1493 --center`
A line chart of contributions over the last 31 days (github-readme-activity-graph). It draws on a solid background, so match `--bg` to the viewer's theme (`0D1117` dark). Good as a full-width strip under the stats row.

## Quote card
`python scripts/snippets.py quote --theme dark --center`
Random developer quote on every load. Cute once, noise twice; skip it on project READMEs.

## Streak
`https://streak-stats.demolab.com/?user=USER&theme=dark&hide_border=true`

## Snake (contribution graph eater)
Needs a GitHub Action in the profile repo (`.github/workflows/snake.yml`), which writes SVGs to an `output` branch:
```yaml
name: Generate Snake
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
```
Embed with `python scripts/snippets.py snake USER` (a `<picture>` with dark/light sources).

## Restraint
One stats card + one fun element (trophies or snake or streak). Stacking all of them makes the page look like a dashboard from 2021.
