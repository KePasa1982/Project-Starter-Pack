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
| **Windows** | Use **Git for Windows** for `git` in PowerShell or **Git Bash**. CI runs the same bash smoke tests as Linux. Long paths: keep project folders reasonably short if you hit path limits. Antivirus can lock `node_modules` during bootstrap — close editors on a half-finished `psp-…` folder and retry if cleanup fails. See **First `npm run dev` on Windows** below. |

### First `npm run dev` on Windows

New **`psp-…`** projects set **`server.open`** to **`http://127.0.0.1:PORT/`** (your port is in `vite.config.ts` and the terminal **Local:** line). The dev server can work even when the browser does not open automatically.

| What you see | What to do |
|--------------|------------|
| Windows Firewall asks to allow **Node.js** | Choose **Allow** (private network is enough for localhost). Then run **`npm run dev`** again or open the URL manually. |
| Terminal shows **Local:** but no browser tab | Copy **`http://127.0.0.1:PORT/`** from the terminal (or your project README port) into Edge, Chrome, or Cursor’s browser panel. |
| Page will not load | Confirm the dev server is still running; try **`http://localhost:PORT/`** as well. |

Auto-open cannot be guaranteed on every PC (firewall, antivirus, corporate policy). The project is fine if **`npm run build`** passed at bootstrap — opening the preview URL by hand is normal.

### Windows terminal commands

Cursor’s integrated terminal on Windows often defaults to **Windows PowerShell 5**, which **does not** support chaining with `&&` (that works in **PowerShell 7+**, **Git Bash**, and macOS/Linux).

**Prefer one command per line** — copy-friendly and works in every shell:

```powershell
cd "D:\path\to\psp-your-project"
npm run dev
```

```powershell
cd "D:\path\to\psp-your-project"
npm run build
git add -A
git commit -m "Your message"
git push
```

| Error | Fix |
|-------|-----|
| `The token '&&' is not a valid statement separator` | Split the chain into separate lines (above), or install [PowerShell 7](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows) / use **Git Bash**. |

Agents and handoff templates in this pack follow this rule — see **[HANDOFF_MESSAGES.md](HANDOFF_MESSAGES.md)** and **[GITHUB_SETUP_WALKTHROUGH.md](GITHUB_SETUP_WALKTHROUGH.md)**.

## Child projects (after bootstrap)

Each new **`psp-…`** app is a normal **Vite + TypeScript** web project: `npm run dev`, `npm run build`, optional GitHub CI from the template. No extra platform-specific pack changes are required for end users beyond installing the tools above.

Contributors: see [CONTRIBUTING.md](../CONTRIBUTING.md) for local smoke tests and the CI matrix.
