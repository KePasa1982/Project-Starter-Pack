# Project Starter Pack — instructions for AI agents (operator manual)

## Non-negotiable intent

The **user** must **not** be asked to design folder structure, backup strategy, or “how to organize the repo.” **You** infer **`PROJECT_NAME` / title** and **`PROJECT_SLUG`** from their words; **only** ask if the name is **unusable** (illegal slug, folder already exists) — never *“what folder layout do you want?”*

When the **user** wants a **new** project using **this starter pack**, this folder is the **factory**, not the product.

## Encoded process (order matters)

0. **User** — has an idea / inspiration (no folders required from them).
1. **Trigger** — they ask to start a new project using the **Project Starter Pack** (wording may vary).
2. **You** — open this repo, read **[README.md](README.md)** first, then this file.
3. **Bootstrap** — from repo root:

   ```bash
   # Linux / macOS: python3 …   |   Windows: python …  (Python 3.10+)
   python3 scripts/bootstrap_new_project.py --title "<from the user>"
   ```

   See **[docs/PLATFORMS.md](docs/PLATFORMS.md)** if the command is not found.

   The script always prefixes the **display title** with **`PSP `** and the **folder / npm slug** with **`psp-`** (unless `--slug` already starts with `psp-`) so PSP-born projects are easy to spot next to whatever else lives beside the starter pack. Add `--slug …` only if the auto slug from the title is wrong.

4. **Baseline bar** — you must verify (bootstrap does most of this):

   - **`.gitignore`** present (template).
   - **`package-lock.json`** present and **committed** in the initial commit (bootstrap uses a one-shot git author for that commit so it succeeds without global `user.name`; the user may **`git commit --amend --reset-author`** later if they care about author metadata).
   - **`README.md`** with install/run commands.
   - **`npm run build`** passes after bootstrap.
   - **No** custom code-history / per-save snapshot hooks in this pack — industry standard is **Git + remote + lockfile + CI** only (see [INDUSTRY_STANDARD_VERSIONING.md](INDUSTRY_STANDARD_VERSIONING.md)).

5. **Handoff (two beats — do not merge)** — bootstrap prints paths for **you** only. User-facing copy lives in **[docs/HANDOFF_MESSAGES.md](docs/HANDOFF_MESSAGES.md)** (also copied into each child’s `docs/`). Use those templates **verbatim in structure** — premium Markdown (tables, dividers, icons, copy-friendly code blocks). Cursor has **Copy** on fenced blocks; there are no custom HTML buttons.

   **Beat A — first reply (right after bootstrap):** send the **Beat A** template from **HANDOFF_MESSAGES.md** (fill `{{DISPLAY_TITLE}}`, `{{CHILD_FOLDER}}`). GitHub **YES** / **NO** only — no dev server or idea-file dump.

   **Beat B — after GitHub is finished or declined:** send the **Beat B** template from **HANDOFF_MESSAGES.md** (fill placeholders + correct GitHub status line). See step 6 and **[docs/GITHUB_SETUP_WALKTHROUGH.md](docs/GITHUB_SETUP_WALKTHROUGH.md)** Phase 5. Bootstrap does not create a remote or push.

6. **GitHub setup (mandatory in Beat A)** — if **YES**, open the child’s **`docs/GITHUB_SETUP_WALKTHROUGH.md`** and walk **phase by phase**. Use **their** path and GitHub username only in chat / local git — **never** commit personal data into **Project-Starter-Pack**. Never ask for tokens or passwords in chat.

   - **NO** — note they can connect later; go straight to **Beat B** (local dev + build invite). Do not nag.

   The child template includes **`.cursor/rules/github-setup-offer.mdc`** (two-beat handoff) and **`github-push-offer.mdc`** (after meaningful work, one-line offer to commit/push when `origin` exists — never without consent).

## Workspace rule

- **Workspace = `Project-Starter-Pack`** — scaffold or improve the pack and templates only.
- **Workspace = child project** — follow **that** repo’s `AGENTS.md`; do not improvise a second layout.

For *new repo vs existing*, see [WORKFLOW.md](WORKFLOW.md). **Industry standard only:** [INDUSTRY_STANDARD_VERSIONING.md](INDUSTRY_STANDARD_VERSIONING.md) — no custom archive-on-save in this pack.

## When editing the starter pack itself

Keep [FOR_USER.md](FOR_USER.md) short. Keep templates **minimal** and **`npm run build`** fast.

**Optional — Karpathy-style review:** To audit this factory repo with explicit assumptions, simplicity checks, and a command checklist, follow **[docs/PSP_REVIEW_KARPATHY_LENS.md](docs/PSP_REVIEW_KARPATHY_LENS.md)**. It pairs with the project rule **[`.cursor/rules/karpathy-guidelines.mdc`](.cursor/rules/karpathy-guidelines.mdc)** (vendored from [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills), MIT).

**Older `psp-…` child projects** (predating template changes): **[docs/UPGRADE_NOTES_CHILD_PROJECTS.md](docs/UPGRADE_NOTES_CHILD_PROJECTS.md)**.

**Stability:** avoid churn in bootstrap output, dev UX (`vite.config`, scripts), and handoff text unless there is a clear bug or an explicit request — future users depend on predictable behavior.

## What you must not do

- Ask the user to choose between ten folder layouts.
- Skip the baseline bar without the user **explicitly** choosing a different documented approach (default = **Git + remote + lockfile + build + CI** only — no custom archive-on-save systems in this pack).
- Commit secrets (real `.env` files, API keys).

## Git remote (one-time, not daily folder worry)

Agents **cannot** push without credentials on the user’s machine. For a **guided** first-time setup after bootstrap, use **[docs/GITHUB_SETUP_WALKTHROUGH.md](docs/GITHUB_SETUP_WALKTHROUGH.md)** (YES/NO offer, phased checklist). For reference-only remote steps, **[INDUSTRY_STANDARD_VERSIONING.md](INDUSTRY_STANDARD_VERSIONING.md)**. Do not ask the user to invent a parallel “version saving” scheme. Never ask them to paste tokens or passwords into chat.

**Privacy:** the factory repo stays **generic** (no real usernames, tokens, or home paths in committed files). Personal paths and GitHub account details belong in the **child** project session only.

## Optional: Cursor rule snippet

Point them to [CURSOR_USER_RULE_SNIPPET.md](CURSOR_USER_RULE_SNIPPET.md) so new-project chats always open this pack’s README first.
