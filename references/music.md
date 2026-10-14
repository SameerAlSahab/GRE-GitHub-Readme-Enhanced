# Now Playing (YTMusicReadme)

A card for the song the user is into, rendered by YTMusicReadme.

## Snippet (exact format)
```markdown
## Now Playing
[![Now Playing](https://ytmusicreadme.vercel.app/api/widget?url=https%3A%2F%2Fmusic.youtube.com%2Fwatch%3Fv%3D-eGM0IJc70Y)](https://music.youtube.com/watch?v=-eGM0IJc70Y)
```
Generate: `python scripts/ytmusic.py "<any youtube or music.youtube link or video id>"`

## Rules
- The `url=` value is the **percent-encoded** `https://music.youtube.com/watch?v=<id>` link; the outer link wraps the image so clicking opens the song.
- No credit line by default. `--credit` appends a link to the widget project if the user wants one.
- Ask the user for the song; never pick one for them. If they say a title only, ask for the link (or search for it if web access exists and confirm the match).
- It's a static snapshot of the song they chose, so tell them to change the link when their taste changes.
- Heading wording is theirs to change ("Now Playing", "On repeat", "Current obsession").
