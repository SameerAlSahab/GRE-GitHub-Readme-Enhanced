# HTML craft (what survives GitHub's sanitizer)

GitHub renders a safe subset of HTML. Everything else is silently removed, so know the line.

## Works
`<p>`, `<div>`, `<h1>`-`<h6>`, `<br>`, `<hr>`, `<a>`, `<img>`, `<picture>` + `<source>`, `<table>` family, `<details>`/`<summary>`, `<kbd>`, `<sub>`, `<sup>`, `<ins>`, `<del>`, `<b>`, `<i>`, `<em>`, `<strong>`, `<code>`, `<pre>`, `<blockquote>`, `<ul>/<ol>/<li>`, `<span>` (attributes stripped), `<video>` with GitHub-hosted src.
Attributes that work: `align` (`center|left|right`), `width`, `height`, `src`, `alt`, `href`, `valign` on `td`, `colspan`, `rowspan`, `open` on details, `media`/`srcset` on picture.

## Stripped (never use)
`style=`, `class=`, `<style>`, `<script>`, `<iframe>`, `<form>`, `<input>`, `<button>`, `<marquee>`, JS event handlers, `<link>`. No CSS means no custom fonts, no hover effects, no flex/grid. Animation comes from **SVG/GIF images**, not from page code.

## Centering
```html
<p align="center">
  <img src="..." alt="..." />
</p>
<h1 align="center">Title</h1>
<div align="center">any block</div>
```
Markdown inside an HTML block only renders if separated by blank lines. For images inside `<p align>`, use `<img>` tags (no markdown) to be safe.

## Side-by-side layout (2-column table)
```html
<table>
  <tr>
    <td valign="top" width="50%">
      <img src="STATS_URL" alt="stats" width="100%" />
    </td>
    <td valign="top" width="50%">
      <img src="TOP_LANGS_URL" alt="languages" width="100%" />
    </td>
  </tr>
</table>
```
`python scripts/snippets.py pair URL1 URL2 --alts "stats" "languages"` generates this table.
Tables show borders in light theme on some clients; it's acceptable. Keep to 2 columns; 3 gets cramped on mobile.

## Float an image right (text wraps)
`<img align="right" width="200" src="..." alt="..." />` placed before the paragraph.

## Dark / light aware images
```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="DARK_URL">
  <source media="(prefers-color-scheme: light)" srcset="LIGHT_URL">
  <img alt="description" src="LIGHT_URL">
</picture>
```
Use for the snake, logos, or any image with a baked-in background. Alternative: `![x](url#gh-dark-mode-only)` and `![x](url#gh-light-mode-only)`.

## Widths
GitHub's content column is about 880px; typing-svg `width` ≤ 880, images `width="100%"` or a fixed ≤ 800. On mobile everything scales down, so avoid text smaller than ~14px inside SVGs.

## Linking images
`<a href="..."><img src="..." alt="..."/></a>` makes any badge/card clickable.

## Image sources
External https URLs (proxied by GitHub), files in the repo (`assets/pic.png`), or drag-and-dropped uploads in the web editor. GIFs animate. Keep GIFs under ~5 MB.
