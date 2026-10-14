<div align="center">

# payload-peek

**List and extract partitions from Android OTA `payload.bin` files without flashing anything.**

<p align="center">
  <a href="https://github.com/octocat-dev/payload-peek/actions"><img src="https://img.shields.io/github/actions/workflow/status/octocat-dev/payload-peek/ci.yml?style=for-the-badge&labelColor=1a1a1a&logo=githubactions&logoColor=white&branch=main" alt="Build status" /></a>
  <a href="https://github.com/octocat-dev/payload-peek/releases"><img src="https://img.shields.io/github/v/release/octocat-dev/payload-peek?style=for-the-badge&color=FF1493&labelColor=1a1a1a&logo=github&logoColor=white" alt="Latest release" /></a>
  <a href="https://github.com/octocat-dev/payload-peek/blob/main/LICENSE"><img src="https://img.shields.io/github/license/octocat-dev/payload-peek?style=for-the-badge&color=FF1493&labelColor=1a1a1a" alt="License" /></a>
  <a href="https://github.com/octocat-dev/payload-peek/commits/main"><img src="https://img.shields.io/github/last-commit/octocat-dev/payload-peek?style=for-the-badge&color=FF1493&labelColor=1a1a1a&logo=git&logoColor=white" alt="Last commit" /></a>
</p>

<a href="https://github.com/octocat-dev/payload-peek/issues/new?labels=bug">Report a bug</a> ·
<a href="https://github.com/octocat-dev/payload-peek/issues/new?labels=enhancement">Request a feature</a>

</div>

## About

Full OTA packages ship as a single `payload.bin`. Getting one partition out of it usually means flashing or running a heavyweight toolchain. payload-peek reads the manifest, shows what is inside, and extracts only what you ask for.

### Features

- Lists partitions with size and hash, in a table or as JSON
- Extracts one partition, several, or all of them
- Verifies SHA-256 after extraction
- Reads full OTAs only. Incremental payloads are rejected with a clear error
- No dependencies beyond the Python standard library

> [!NOTE]
> Incremental (delta) payloads are not supported yet. See the roadmap.

## Getting started

### Prerequisites

Python 3.9 or newer.

### Installation

```bash
git clone https://github.com/octocat-dev/payload-peek.git
cd payload-peek
python -m pip install .
```

Check it worked:

```bash
payload-peek --version
```

## Usage

```bash
payload-peek list payload.bin
payload-peek extract payload.bin boot vendor_boot -o out/
```

```text
partition      size      sha256
boot           64 MiB    9f2c…e1a0
vendor_boot    96 MiB    41b7…03cd
system         3.2 GiB   c8d1…77f2
```

| option | what it does |
|---|---|
| `-o, --out DIR` | output directory, default `./out` |
| `--json` | machine-readable listing |
| `--no-verify` | skip the hash check after extraction |

> [!WARNING]
> Extracting is read-only, but flashing what you extracted is not. Back up first, and check the build matches your device.

## Roadmap

- [x] Full OTA listing and extraction
- [x] SHA-256 verification
- [ ] Incremental payload support
- [ ] Streaming extraction from a URL

## Contributing

Run `python -m unittest` before opening a pull request. Bug reports with the payload's `ro.build.fingerprint` get fixed fastest.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](https://github.com/octocat-dev/payload-peek/blob/main/LICENSE)

Released under the **MIT License**. See [LICENSE](LICENSE).

Copyright (c) 2026 Octo Dev
