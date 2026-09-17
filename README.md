# Manus CLI

[![Release](https://img.shields.io/github/v/release/ehadsagency-ai/manus-cli)](https://github.com/ehadsagency-ai/manus-cli/releases/latest)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Built with Typer](https://img.shields.io/badge/CLI-Typer%20%2B%20Rich-informational)](https://github.com/ehadsagency-ai/manus-cli)

> AI-native command-line interface for [Manus](https://github.com/ehadsagency-ai/manus-cli) — chat, 12 professional roles, and optional GitHub Spec-Kit–style workflows that leave versionable artifacts under `.manus/`. Built with **Typer** and **Rich**.

**Honest metrics (2026-09-17T15:10:00CEST):** ★0 · forks 0 · 1 author · 0 commits/7d · GitHub Releases through **v5.5.7** · PyPI **not published** · Hype Score **7/25** (Portfolio Ready ≥25).

---

## What it does

Manus CLI brings Manus AI into the terminal:

- **Chat** with role + mode flags (`speed` / `balanced` / `quality`)
- **12 roles** (assistant, developer, data-scientist, writer, teacher, analyst, researcher, debugger, architect, copywriter, consultant, reviewer)
- **Spec-driven mode** — constitution → specify → plan → tasks → implement → clarify; artifacts land in `.manus/` for git
- **Interactive splash** via `manus start` / `manus chat -i`
- **Local config** under `~/.config/manus/` (API key not logged)

Requires a Manus API key and network access for API calls.

---

## Install

### From GitHub (current supported path)

```bash
pip3 install "git+https://github.com/ehadsagency-ai/manus-cli.git"
```

### From source (dev)

```bash
git clone https://github.com/ehadsagency-ai/manus-cli.git
cd manus-cli
pip3 install -e .
```

> **PyPI:** `pip install manus-cli` is a **planned** distribution path — not live yet. Install from GitHub or source for now.

### Requirements

- Python **3.8+**
- macOS, Linux, or Windows (WSL)
- Internet for Manus API calls

---

## Verification

```bash
manus --version
# Expect a Manus CLI version line (releases go through v5.5.7)

manus start   # optional: splash + interactive session
```

If `manus: command not found`, add your user pip `bin` to `PATH` (see Troubleshooting).

---

## Quick start

```bash
# 1) Configure API key (stored in ~/.config/manus/config.json)
manus configure --api-key "$MANUS_API_KEY"
manus configure --show

# 2) List roles
manus roles

# 3a) Simple chat with a role
manus chat "Explain this repo layout" --role developer

# 3b) Spec-driven project scaffolding (creates .manus/ artifacts)
manus chat "Create a REST API for a todo app" --spec-driven

# 3c) Interactive mode
manus start
# or: manus chat -i
```

---

## Command reference

| Command | Purpose |
|---------|---------|
| `manus --version` / `manus -v` | Print CLI version |
| `manus version` | Detailed version info |
| `manus start` | Interactive splash + chat (`--role`, `--mode`) |
| `manus configure` | Set API key / defaults (`--api-key`, `--default-role`, `--default-mode`, `--show`) |
| `manus roles` | List the 12 professional roles |
| `manus chat "<msg>"` | One-shot or interactive chat (`--role/-r`, `--mode/-m`, `--spec-driven`, `--interactive/-i`) |
| `manus task "<desc>"` | Task-oriented prompt |
| `manus history` | Show / clear conversation history (`--limit`, `--clear`) |
| `manus update` | Upgrade from GitHub |
| `manus session` | Session info / rotate (`--new`, `--clear`) — added in **v5.5.7** (CLI vs Web session separation) |

Exit interactive mode with `exit`, `quit`, `q`, `bye`, or `Ctrl+C`.

---

## Configuration & environment

Config file: **`~/.config/manus/config.json`**

Typical keys (shape from live docs):

```json
{
  "api_key": "sk-...",
  "default_role": "assistant",
  "default_mode": "balanced",
  "streaming": false,
  "spec_driven": {
    "enabled": true,
    "auto_detect": true,
    "complexity_threshold": "moderate"
  }
}
```

- Prefer `manus configure --api-key …` over pasting secrets into shell history when possible.
- Optional history file: `~/.manus_history`
- Spec artifacts: project-local `.manus/` (safe to commit if you intend to version them)

---

## Troubleshooting

| Symptom | What to try |
|---------|-------------|
| `manus: command not found` | Add pip user bin to PATH, e.g. `export PATH="$HOME/.local/bin:$PATH"` (Linux) or `~/Library/Python/3.x/bin` (macOS), then re-open the shell |
| `No such option: --version` | Reinstall a recent release: `pip3 install --upgrade --force-reinstall git+https://github.com/ehadsagency-ai/manus-cli.git` |
| `Template not found` | Force-reinstall so package data/templates are included |
| API / auth errors | `manus configure --show` — confirm key + network; retry with a short `manus chat "test"` |
| CLI and Web chats colliding | Upgrade to **≥ v5.5.7** (separate CLI session IDs) or `manus session --new` |

Uninstall:

```bash
pip3 uninstall manus-cli
# optional: rm -rf ~/.config/manus/  &&  rm -f ~/.manus_history
```

---

## Status (portfolio-honest)

| Item | State |
|------|-------|
| Latest GitHub Release | **v5.5.7** (2025-12-15) — Session Separation CLI/Web |
| Install path | GitHub / source |
| PyPI | ❌ not published (planned) |
| Stars / forks | 0 / 0 |
| Weekly commits (as of analysis) | 0 |
| Independent download / SLA numbers | none claimed here |

Live upstream README is longer and more promotional (ASCII splash, “production ready”, code-grade badges). This draft keeps the **evidenced** CLI surface and trims unverified marketing.

---

## Contributing

Solo-maintained today. Useful PRs: docs fixes, Windows/PATH install notes, tests, and packaging for a future PyPI publish (**planned**).

```bash
git clone https://github.com/ehadsagency-ai/manus-cli.git
cd manus-cli
python -m venv venv && source venv/bin/activate
pip3 install -e .
python -m pytest tests/   # if present in your checkout
```

Open an issue or PR on GitHub.

---

## License

MIT · © ehadsagency-ai
