# Project Starter Pack — review runbook (Karpathy lens)

Use this when the user (or you) want a **structured audit** of the factory repo. It applies the four principles from **[multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)** (see `.cursor/rules/karpathy-guidelines.mdc`).

**Success criteria for “review done”:** every section has a one-line verdict (OK / gap / N/A) plus evidence (file path, command output, or test name).

---

## 1. Think before coding — assumptions & tradeoffs

| Question | Where to look |
|----------|----------------|
| What is assumed about **OS** (paths, shell, `python3` / `npm` on PATH)? | `README.md`, `CONTRIBUTING.md`, `scripts/bootstrap_new_project.py` |
| What is assumed about **`--dest`** and default parent? | Same + `WORKFLOW.md` |
| What happens for **non-ASCII titles** (slug failure)? | `slugify` / `exit_if_slug_invalid` in bootstrap (hint suggests `--slug`) |
| What is **out of scope** for v1 (second template, backend, etc.)? | `README.md` “Scope (v1)” |

**Verdict lines:** list explicit assumptions; flag silent failures or undocumented edges.

---

## 2. Simplicity first — minimum moving parts

| Question | Where to look |
|----------|----------------|
| Is bootstrap **one script** with a clear sequence, or split logic that could merge? | `scripts/bootstrap_new_project.py` |
| Is template **minimal** (no speculative libs)? | `template/web-vite-ts/package.json` |
| Do docs **repeat** the same paragraph in five places, or point to a single source of truth? | `README.md`, `AGENTS.md`, `FOR_USER.md` |

**Verdict lines:** name any over-abstraction or doc sprawl worth trimming (only if the user asked to improve docs).

---

## 3. Surgical changes — factory vs child boundaries

| Question | Where to look |
|----------|----------------|
| Does anything in the factory **reach into** child-specific business logic? | `template/` only via copy + placeholders |
| Do Cursor rules **contradict** each other (`starter-pack-bootstrap` vs `karpathy-guidelines`)? | `.cursor/rules/*.mdc` |
| Does the child template **avoid** starter-pack-only paths? | `template/web-vite-ts/*` |

**Verdict lines:** boundary violations or rule conflicts.

---

## 4. Goal-driven execution — verify, don’t guess

Run from repo root (see `CONTRIBUTING.md` for the canonical list):

1. `python -m py_compile scripts/bootstrap_new_project.py` → verify: exit 0  
2. `python -m unittest discover -s tests -p "test_*.py" -v` → verify: all OK  
3. `cd template/web-vite-ts && npm ci && npm run build` → verify: exit 0  
4. Bootstrap smoke (disposable parent, e.g. `RUNNER_TEMP` or `/tmp`) → verify: `npm ci && npm run build` in the new folder, then optional same **dev + curl** pattern as CI (`npm run dev -- --host 127.0.0.1 --port 34174 --strictPort` + HTTP check).  
5. CI parity → verify: `.github/workflows/ci.yml` on **ubuntu-latest** and **windows-latest** matches the above, including **headless dev** (curl) and **npm fetch retry** `env`.

**Verdict lines:** any step failing or missing from CI.

---

## Output template (paste into chat or issue)

```text
## Karpathy-lens review (Project-Starter-Pack)

### 1. Think before coding
- Assumptions: …
- Gaps: …

### 2. Simplicity first
- …

### 3. Surgical changes
- …

### 4. Goal-driven execution
- Commands run: …
- Results: …
```

When the user says **“Karpathy review the starter pack”**, follow this file, run the commands, then fill the template.
