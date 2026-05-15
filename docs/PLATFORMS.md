# Platforms and prerequisites

Project Starter Pack is tested on **Linux** and **Windows** in CI. **macOS** usually matches Linux for local use.

## What you need

| Tool | Purpose |
|------|---------|
| **Python 3.10+** | Runs `scripts/bootstrap_new_project.py` (agents run this; you do not need to memorize it). |
| **Node.js 20+** (22 recommended) | `npm install` / `npm run build` in the template and in each new `psp-…` project. |
| **Git** | Local history; optional GitHub remote (see [GITHUB_SETUP_WALKTHROUGH.md](GITHUB_SETUP_WALKTHROUGH.md)). |
| **Cursor** (recommended) | Loads `.cursor/rules/` in the factory and in each child project. |

## Bootstrap command (by OS)

From the **Project-Starter-Pack** repo root:

```bash
# Linux / macOS
python3 scripts/bootstrap_new_project.py --title "Your Project Title"
```

```powershell
# Windows (Command Prompt or PowerShell; Python 3.10+ on PATH)
python scripts/bootstrap_new_project.py --title "Your Project Title"
```

If `python` / `python3` is missing, install Python from [python.org](https://www.python.org/downloads/) (Windows: check **“Add python.exe to PATH”**) or your package manager.

## Where new projects are created

By default, bootstrap creates a **sibling folder** next to `Project-Starter-Pack` (same parent directory as the folder that contains this repo). Use **`--dest /path/to/parent`** if your projects live somewhere else (works on all platforms; use forward slashes or OS-native paths).

## OS-specific notes

| OS | Notes |
|----|--------|
| **Linux** | Full support. If `http://localhost:PORT` fails but `http://127.0.0.1:PORT` works, the template’s `server.host: true` in `vite.config.ts` is already set for that case. |
| **macOS** | Same as Linux for bootstrap and Vite. Install Git via Xcode Command Line Tools or Homebrew if needed. |
| **Windows** | Use **Git for Windows** for `git` in PowerShell or **Git Bash**. CI runs the same bash smoke tests as Linux. Long paths: keep project folders reasonably short if you hit path limits. Antivirus can lock `node_modules` during bootstrap — close editors on a half-finished `psp-…` folder and retry if cleanup fails. |

## Child projects (after bootstrap)

Each new **`psp-…`** app is a normal **Vite + TypeScript** web project: `npm run dev`, `npm run build`, optional GitHub CI from the template. No extra platform-specific pack changes are required for end users beyond installing the tools above.

Contributors: see [CONTRIBUTING.md](../CONTRIBUTING.md) for local smoke tests and the CI matrix.
