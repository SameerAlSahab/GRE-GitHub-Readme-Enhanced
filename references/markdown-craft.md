# Markdown craft (what GitHub renders natively)

Small features that make a README feel hand-built. Reach for these before reaching for another widget.

## Spoiler / collapsible (`<details>`)
GitHub has no `||spoiler||` syntax. `<details>` is the spoiler: closed by default, click to reveal.
```markdown
<details>
<summary>🎁 click me, i dare you</summary>

anything markdown goes here, including images and code.

</details>
```
**Blank line after `</summary>` and before `</details>` is mandatory**, or the inside won't render as markdown. `<details open>` starts expanded.
Uses: hide the long tech list, a "things nobody asked about me" easter egg, a secret song, a full project list, a joke punchline. Keep the `<summary>` text playful; it is the only part visible.

## Strikethrough
`~~text~~`. In a human README it is a joke device: a self-correction the writer "forgot" to delete.
```markdown
I write ~~clean~~ working code and ~~sleep~~ coffee.
Currently learning ~~Rust~~ how to explain Rust to myself.
```
Use one or two per page; more becomes a gimmick. Don't strike through facts.

## Alerts
```markdown
> [!NOTE]
> neutral info
> [!TIP]
> helpful hint
> [!IMPORTANT]
> must-read
> [!WARNING]
> careful
> [!CAUTION]
> danger
```
Good for "dm me for ROM questions, not for 'is it dead?'" style notes. One per page.

## Other native features
- **Footnotes:** `text[^1]` with `[^1]: note` at the bottom. Nice for jokes in small print.
- **Task list:** `- [x] done` / `- [ ] planned`. A "now learning / roadmap" list that people can see ticking.
- **Tables** with alignment `:---:`. Layout trick: a borderless 2-column table with images (see html-craft.md).
- **Mermaid:** a fenced ```` ```mermaid ```` block renders diagrams (good for a project architecture or "my brain" flowchart).
- **Math / colored text:** `$\color{hotpink}{\text{like this}}$` renders colored text through the math engine. Font differs from body text, so use sparingly and check the preview.
- **Emoji shortcodes:** `:sparkles:` etc. Raw emoji are fine too.
- **`<kbd>`:** `<kbd>Ctrl</kbd>+<kbd>C</kbd>` keyboard keys.
- **`<sub>` / `<sup>`:** small print and super-script jokes.
- **Hidden comment:** `<!-- you found it -->` is invisible but readable in source; a quiet easter egg for people who view raw.
- **Horizontal rule:** `---`. The capsule-render divider is the colored alternative.
- **Anchors:** headings auto-link as `#lowercase-with-dashes`; use for a mini table of contents or "back to top".
- **Line break inside a paragraph:** end the line with two spaces or `<br>`.

## Emoji in headings
One emoji per heading is a style, an emoji in front of every heading and bullet is a tell. Prefer none in body text.
