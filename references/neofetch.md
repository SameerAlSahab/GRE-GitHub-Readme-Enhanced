# Terminal / neofetch profile card

Turns a GitHub profile into a terminal-style card: symbol art on the left, stats and (optionally) the user's own PC specs on the right. It sits in a README as a ```text code block, so it's static (GitHub can't show ANSI colors); re-run the script to refresh it.

## Run
```
python scripts/neofetch_card.py USER --fence                 # GitHub + this machine
python scripts/neofetch_card.py USER --art avatar --fence     # avatar converted to symbols (pip install pillow)
python scripts/neofetch_card.py --profile profile.json        # reuse fetch_profile.py output
python scripts/neofetch_card.py USER --no-local               # GitHub fields only
python scripts/neofetch_card.py USER --hide GPU Packages
```
Art choices: `auto` (Android → android bot, Linux → tux, else generic), `tux`, `android`, `gh`, `avatar`, `none`, or a path to the user's own ASCII file. `--invert` flips avatar brightness for light themes. `--detailed` uses a longer character ramp.

## Where it must run
- **GitHub fields** work anywhere with internet to api.github.com.
- **PC details** are read from the machine running the script. If Claude runs it in its sandbox, it will print the *sandbox's* specs, not the user's. For real specs, give the user the one-line command to run themselves, or ask them to paste their specs and pass them in by editing the output.
- **Avatar art** needs Pillow and access to avatars.githubusercontent.com; it falls back to a built-in logo with a note if either is missing.

## Output (example)
```text
    .--.       demo@github
   |o_o |      ───────────
   |:_/ |      Name: Demo Dev
  //   \ \     Repos: 42
 (|     | )    Followers: 120
/'\_   _/`\    Langs: C++, Kotlin, Python
\___)=(___/    Joined: 2018 (8y)

               OS: Ubuntu 24.04 LTS
               Kernel: 6.8.0
               CPU: Intel i5 (8)
               Memory: 4012MiB / 15890MiB
```

## Privacy
Hostname, username, IP and MAC are never printed. CPU/GPU/RAM/laptop model are shown on purpose; tell the user what is in the card and let them `--hide` anything before they publish a public README.

## Ideas to extend
Add a `Music:` row linking the current song, a `Now:` row for what they're building, or alternate fields (`Shell`, `Editor`, `Distro`) typed by the user.
