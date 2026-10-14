# Automation: snake and auto-updating lists (GitHub Actions)

Some components need a workflow in the profile repo (`USER/USER`). Generate the file, commit it to `.github/workflows/`, then run it once from the **Actions** tab (**Run workflow**), because scheduled runs only start after the first commit lands.

## Snake (contribution graph)
```bash
python scripts/snippets.py workflow snake      # prints .github/workflows/snake.yml
python scripts/snippets.py snake USER           # prints the <picture> embed
```
The workflow writes `github-snake.svg` and `github-snake-dark.svg` to an `output` branch every 12 hours. The embed reads from that branch, so it stays blank until the first run finishes.

## Latest blog posts
```bash
python scripts/snippets.py workflow blog-posts
```
1. Replace `feed_list` with the user's RSS or Atom feed URL (ask for it; never guess).
2. Put these two markers in `README.md` where the list should appear:
```markdown
<!-- BLOG-POST-LIST:START -->
<!-- BLOG-POST-LIST:END -->
```
3. Commit, then run the workflow once. Until then the section is empty, so mention it or drop the section.

## Rules
- Use `permissions: contents: write` only when the job commits back to the repo.
- Pin actions to a major version tag (`@v3`, `@v4`); never `@main`.
- Never paste a token into a README or workflow; use `${{ secrets.GITHUB_TOKEN }}` or repository secrets.
- Keep schedules infrequent (12-24 hours). Hourly cron on a profile repo is noise in the commit graph.
- Each workflow is a third-party dependency. One or two per profile is plenty.
