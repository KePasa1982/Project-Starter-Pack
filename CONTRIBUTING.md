# Contributing to Project Starter Pack

This repo is the **factory**: templates, bootstrap script, and documentation. Child apps live in separate folders created by `scripts/bootstrap_new_project.py`.

## Before you open a PR

1. **Python** — `python -m py_compile scripts/bootstrap_new_project.py` (or `python3 …` if that is what you use locally)
2. **Unit tests** — `python -m unittest discover -s tests -p "test_*.py" -v` (includes **template Cursor rules**: Karpathy + `user-project-standard`, and `AGENTS.md.template` pointers)
3. **Template** — from repo root: `cd template/web-vite-ts && npm ci && npm run build`
4. **Bootstrap smoke** — disposable parent, e.g. `DEST=/tmp` (or `"$RUNNER_TEMP/psp-smoke-parent"` like CI):  
   `rm -rf "$DEST/psp-ci-smoke-test" && mkdir -p "$DEST" && python scripts/bootstrap_new_project.py --title "Smoke" --slug psp-ci-smoke-test --dest "$DEST"`  
   then `cd "$DEST/psp-ci-smoke-test" && npm ci && npm run build`, then the same **headless dev check** CI uses (from repo root: `cd` into the child, `npm run dev -- --host 127.0.0.1 --port 34174 --strictPort` in background, `curl -sf http://127.0.0.1:34174/`, kill PID), then remove the folder.

CI runs **Linux and Windows** (see `.github/workflows/ci.yml`): `py_compile`, unit tests, template **`npm ci` + `npm run build`**, bootstrap under **`RUNNER_TEMP`**, then **`npm ci` + `npm run build`** in the child. A **short headless `npm run dev` + curl** check (`127.0.0.1:34174`) runs on **Linux** only; Windows skips that step (background dev jobs are flaky there) but still runs the full bootstrap smoke through build.

**npm / network:** CI sets **`NPM_CONFIG_FETCH_RETRIES`** (and related npm env vars) so transient registry failures are retried automatically.

**Local platforms:** **macOS** usually matches Linux. **Windows:** CI uses **bash**; for native **PowerShell** smoke, see below.

**Older child folders:** [docs/UPGRADE_NOTES_CHILD_PROJECTS.md](docs/UPGRADE_NOTES_CHILD_PROJECTS.md).

**If bootstrap cleanup fails** (disk full, file locks, antivirus): close editors pointing at the folder, retry, or delete the half-made `psp-…` path manually — bootstrap prints which path failed.

**Optional factory audit** (assumptions + command checklist): [docs/PSP_REVIEW_KARPATHY_LENS.md](docs/PSP_REVIEW_KARPATHY_LENS.md).

## Windows (PowerShell) — same smoke without bash

From repo root (adjust `$dest`):

```powershell
$dest = Join-Path $env:TEMP "psp-smoke-parent"
$child = Join-Path $dest "psp-ci-smoke-test"
Remove-Item -Recurse -Force $child -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $dest | Out-Null
python scripts/bootstrap_new_project.py --title "Smoke" --slug psp-ci-smoke-test --dest $dest
Set-Location $child; npm ci; npm run build
```

For the **headless dev + curl** step CI runs, easiest on Windows is **Git Bash** (same script as Linux). In plain PowerShell you can mirror the loop from `.github/workflows/ci.yml` with `Invoke-WebRequest` and a background job if you need local parity.

## Changelog

User-visible changes to the pack (bootstrap behavior, template defaults, docs) belong in **[CHANGELOG.md](CHANGELOG.md)** with a short dated entry.

The repo root **`.gitignore`** excludes **`template/**/node_modules`** and build output under **`template/`** — run installs only inside `template/web-vite-ts` locally; never commit those folders (the committed **`package-lock.json`** is what CI and clones use).

## Dependency bumps

If you change `template/web-vite-ts/package.json`, run **`npm install`** in that folder and **commit the updated `package-lock.json`** so `npm ci` keeps working in CI and for anyone copying the template only.
