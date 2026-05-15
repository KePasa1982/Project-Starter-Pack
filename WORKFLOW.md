# Workflow — which folder should the agent use?

Ultra-short decision tree for the **user** and agents.

## New idea → brand-new repo

The user has a **new** inspiration and wants a **new** project folder.

1. They use the trigger (see [README.md](README.md)): *start a new project … use the **Project Starter Pack***.
2. Agent opens **`Project-Starter-Pack`**, reads **README.md** first, runs [scripts/bootstrap_new_project.py](scripts/bootstrap_new_project.py) (new folder name is always **`psp-…`** beside the starter pack’s parent unless `--dest` says otherwise; in-app title is **`PSP …`**).
3. Agent continues in the **new sibling folder** (not inside the starter pack).
4. Agent sends **Beat A** from **`docs/HANDOFF_MESSAGES.md`** (premium layout + GitHub **YES** / **NO** only — no dev-server checklist yet). If **YES**, follow **`docs/GITHUB_SETUP_WALKTHROUGH.md`** in the child. **Beat B** from the same handoff doc after GitHub or **NO**.
5. After GitHub finishes or user says **NO**: GitHub result (if any), local **`npm run dev`** reminder, then invite them to describe what to build (walkthrough **Phase 5**).

**Optional remote:** **`docs/INDUSTRY_STANDARD_VERSIONING.md`** in the child for reference.

**Inspiration capture:** **`DESIGN.md`** and **`ideas/INBOX.md`** in the **new** repo when they start designing — not in the first bootstrap message.

## Idea → existing project

The user wants to extend something **already** on disk (e.g. another game repo, an older prototype).

1. **Do not** run the starter-pack bootstrap for that.
2. Open that **existing** project in Cursor and work there, following **that** repo’s `AGENTS.md`.

## Improving the starter pack itself

The user (or an agent) is changing templates, scripts, or this documentation.

1. Open **`Project-Starter-Pack`** as the workspace.
2. Follow [AGENTS.md](AGENTS.md) here; do not treat this repo as an app to ship — it is the **factory**.
