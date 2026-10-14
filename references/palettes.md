# Palettes (cohesion is the whole trick)

Pick ONE accent and use it everywhere: typing `color`, divider `color`, komarev `color`, badge color (`--color`), stats theme. A handmade page looks "designed" mostly because everything agrees.

How to choose: ask the user, or infer from their vibe (bio, languages, favorite color). Default to the accent they already use.

| vibe | accent | secondary | note |
|---|---|---|---|
| hot pink / sakura | `FF1493` | `FFB6C1`, `8A2BE2` | githubstats theme `sakura-blossom` |
| catppuccin mocha | `CBA6F7` mauve | `F5C2E7` pink, `89B4FA` blue, `A6E3A1` green, `FAB387` peach, `F38BA8` red | cozy, popular |
| tokyo night | `7AA2F7` | `BB9AF7`, `7DCFFF`, `9ECE6A`, `E0AF68`, `F7768E` | cool neon blue |
| dracula | `BD93F9` | `FF79C6`, `50FA7B`, `8BE9FD`, `F1FA8C`, `FF5555` | classic dev purple |
| nord | `88C0D0` | `81A1C1`, `5E81AC`, `A3BE8C`, `EBCB8C`, `BF616A` | calm, muted |
| gruvbox | `FABD2F` | `FB4934`, `B8BB26`, `83A598`, `D3869B`, `FE8019` | warm retro |
| rose pine | `C4A7E7` | `EBBCBA`, `9CCFD8`, `F6C177`, `EB6F92` | soft |
| matrix / hacker | `00FF41` | `008F11`, `0D0208` | terminal green, pairs with the neofetch card |
| cyber / synthwave | `00E5FF` | `FF2A6D`, `D1F7FF`, `7700FF` | neon |

## Rules
- Gradient only in the banner (`color=0:hexA,100:hexB`); everything else stays one flat accent.
- On GitHub dark and light both exist. Avoid pure white/black dependent images; prefer transparent backgrounds (`no-bg=true`) and mid-tone accents.
- Match stats/trophy themes to the palette name when the service has one (e.g. Catppuccin, Tokyo Night, Dracula, Nord). Verify the slug (see stats-trophies.md).
