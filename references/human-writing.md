# Human writing (non-AI-sounding README text)

People can smell generated text in a README within two lines, and it makes a profile feel like a template. The goal is not to hide that an AI helped; it is to make the words sound like *this specific person*. That comes from specifics, opinions and uneven rhythm, which an AI will not add unless told to.

## Step 0: get the voice
Before writing a single line of prose, find the person's voice:
- Read how they wrote to you in this chat (casual? lowercase? punctuation? slang? a mix of languages?). Mirror it, including their language or dialect.
- If `fetch_profile.py` returned a `profile_readme`, `bio` and repo descriptions, read them for phrases they already use.
- Ask for one "ugly true fact" if you have nothing: a bug that cost them a week, a device they bricked, what they'd rather be doing.
Never invent achievements, employers, numbers or projects. If a detail is missing, ask or leave a `<!-- TODO: ... -->` comment and tell the user.

## The tells (avoid)
| tell | example | why it reads as AI |
|---|---|---|
| em dashes everywhere | "I build tools — fast, small, useful" | humans mostly use commas, periods, hyphens |
| stock vocabulary | passionate about, leveraging, crafting, delve, journey, cutting-edge, seamless, robust, innovative, empower, unlock, elevate, tapestry, landscape, realm, testament | none of these are how people talk about their hobby |
| "not just X, but Y" | "not just a developer, but a problem solver" | balanced rhetoric nobody uses casually |
| rule of three | "fast, secure, and scalable" | too tidy; real lists have two things or five |
| every bullet = emoji + **Bold**: text | "🚀 **Performance**: blazing fast" | uniform shape across the page |
| greeting/farewell boilerplate | "Hi there 👋 I'm ...", "Let's connect!", "Feel free to reach out" | every template has them |
| abstract claims, no nouns | "I enjoy solving complex challenges" | no device, no bug, no name anywhere |
| tidy symmetric sentences | every sentence 12-15 words | humans vary: 3 words, then 30 |
| emoji after every sentence | | reads like a social-media bot |

## What to do instead
1. **Name the thing.** "I port custom ROMs to a Snapdragon phone from 2019 that refuses to die" beats "I enjoy Android development".
2. **Include a small failure or opinion.** "I've bricked 4 phones. 3 on purpose." / "Kotlin > Java, fight me."
3. **Break rhythm.** Mix a fragment. A long sentence. A short one. Don't make paragraphs the same shape.
4. **Use their words.** Slang, in-jokes, the exact way they spell things, mixed languages if that's how they talk.
5. **One joke device, not five.** Strikethrough self-correction, a `<details>` easter egg, or a lowercase tone. Pick two.
6. **Cut the greeting.** Start with the interesting sentence.
7. **Fewer sections, more personality.** A short "about" plus a weird "currently" line beats six headings.
8. **Imperfection is fine.** A lowercase first letter, a missing comma, "idk" in the right place. Don't fake typos, just don't sand every edge off.
9. **Specific numbers once.** "7 ROMs", "since 2018", "3 AM" beat "numerous projects".
10. **Sparing emoji.** One or two on the whole page body (typing line and headings excluded).

## Before / after
| AI-sounding | human |
|---|---|
| "I'm a passionate Android developer leveraging cutting-edge technologies to craft seamless user experiences." | "I build Android ROMs. Mostly for phones the manufacturer gave up on." |
| "🔧 **Hardware Security**: Exploring vulnerabilities in embedded systems" | "i like opening devices that say *do not open*. then reading the firmware." |
| "Let's connect and build something amazing together!" | "DM me if your phone is bootlooping. I've seen worse." |
| "Currently learning Rust to expand my skill set." | "Currently learning ~~Rust~~ why the borrow checker hates me." |

## Self-check before delivering
Run `python scripts/lint_readme.py README.md`, then read the prose out loud once. If a sentence could appear on a stranger's README with the name swapped, rewrite it with something only this person would say.
