# Project Starter Pack

The **user** (the person with the idea) is the **idea generator / designer**. This pack exists so they are **freed from** folder layout and “how do I save this properly?” **Agents own that entirely** using **normal industry practice**: **Git**, a committed **`package-lock.json`**, **build**, and **optional remote + CI** — not custom per-save archive systems. The user’s **first step** is always **inspiration**.

For optional off-machine backup and remotes, read **[INDUSTRY_STANDARD_VERSIONING.md](INDUSTRY_STANDARD_VERSIONING.md)** from the top when you need it.

**Platforms:** Linux, macOS, and Windows are supported (CI runs Linux + Windows). Prerequisites and OS notes: **[docs/PLATFORMS.md](docs/PLATFORMS.md)**.

See also [AGENTS.md](AGENTS.md), [FOR_USER.md](FOR_USER.md), and [CONTRIBUTING.md](CONTRIBUTING.md) if you change the pack. **Publishing this factory repo to GitHub:** [docs/PUBLISHING.md](docs/PUBLISHING.md). **Older `psp-…` apps** (before a template refresh): [docs/UPGRADE_NOTES_CHILD_PROJECTS.md](docs/UPGRADE_NOTES_CHILD_PROJECTS.md).

**Why names start with `PSP` / `psp-`:** it marks apps that came from this pack so they stay easy to spot next to other folders. The prefix is applied by bootstrap; you choose the creative title, not the plumbing.

## Fresh-agent contract (read this once)

Within one read of this file you should know:

1. **Who the user is** — repo hygiene is **not** their job; they supply **ideas and creative direction**.
2. **Exact sequence** — step **0** below (inspiration) → steps **1–3** (mechanical) → work in the **new** repo; see [WORKFLOW.md](WORKFLOW.md) if unsure *new vs existing*.
3. **Never ask the user** — standard paths, default backup (git + lockfile + build), or baseline checks; only ask if the **project title/slug** is unusable (collision or illegal name). Bootstrap always adds **`PSP `** to the display title and **`psp-`** to the folder/npm name so PSP-started projects are easy to recognize.

Details: [AGENTS.md](AGENTS.md) · [INDUSTRY_STANDARD_VERSIONING.md](INDUSTRY_STANDARD_VERSIONING.md) (Git + optional remote). Promise to the user: [FOR_USER.md](FOR_USER.md).

---

## Step 0 — Inspiration (user)

The user has a spark: what to try, build, or explore. **They do not create project folders by hand.**

**After** the new repo exists, inspiration lives in **`DESIGN.md`** and/or **`ideas/INBOX.md`** in that **new** repo — not inside `Project-Starter-Pack`.

---

## Steps 1–3 — Mechanical (agent)

1. **Open this repo** (`Project-Starter-Pack` — wherever you cloned it, e.g. `…/Project-Starter-Pack`) and read **[AGENTS.md](AGENTS.md)**.
2. **Bootstrap** from this directory:

   ```bash
   # Linux / macOS
   python3 scripts/bootstrap_new_project.py --title "Your Project Title"
   ```

   On **Windows**, use `python` instead of `python3` (Python 3.10+ on PATH). See **[docs/PLATFORMS.md](docs/PLATFORMS.md)**.

   **Naming:** the **display title** in the app and docs becomes **`PSP Your Project Title`**. The **folder name** (and `package.json` name) becomes **`psp-your-project-title`** as a sibling of `Project-Starter-Pack` (default: the **parent directory of the folder that contains this repo** — wherever you cloned the pack). You can still type **`PSP …`** or the old **`(PSP) …`** in `--title`; it will not be doubled.

   Options: `--slug my-slug` (if the default from the title is wrong; `psp-` is added if missing), **`--dest /path/to/parent`** if your projects live somewhere other than the default parent (e.g. an archive folder).

   Bootstrap also copies **`docs/INDUSTRY_STANDARD_VERSIONING.md`** and **`docs/GITHUB_SETUP_WALKTHROUGH.md`** into the new project — Git basics plus optional guided GitHub setup.

3. **Open the created sibling folder** in Cursor and implement there — not inside `Project-Starter-Pack`.

4. **GitHub first, then build** — **first** handoff (**Beat A**): premium message from **[docs/HANDOFF_MESSAGES.md](docs/HANDOFF_MESSAGES.md)** (checklist, copy-friendly path, GitHub **YES** / **NO**). No `npm run dev` or idea-file lecture yet. If **YES**, follow **[docs/GITHUB_SETUP_WALKTHROUGH.md](docs/GITHUB_SETUP_WALKTHROUGH.md)** in the child. **Beat B** after GitHub or **NO**: same handoff doc — local dev + invite what to build. Details: [AGENTS.md](AGENTS.md) steps 5–6.

---

## Trigger phrase (copy-paste)

> I’d like to start a new project — please use the **Project Starter Pack** from the projects list. Title: **“…”**. Handle layout and git; I only want to design.

---

## Optional: Karpathy-style factory review

Structured audit checklist (assumptions, simplicity, boundaries, verified commands): **[docs/PSP_REVIEW_KARPATHY_LENS.md](docs/PSP_REVIEW_KARPATHY_LENS.md)**. Behavioral defaults for all edits in this repo: **[`.cursor/rules/karpathy-guidelines.mdc`](.cursor/rules/karpathy-guidelines.mdc)** (from [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills), MIT).

## Cursor rule (recommended)

So every fresh agent gets the same instruction without the user repeating the path, add a **rule** in Cursor Settings. Snippet: [CURSOR_USER_RULE_SNIPPET.md](CURSOR_USER_RULE_SNIPPET.md).

---

## What gets created (default template `web-vite-ts`)

- **Naming** — display title **`PSP …`**; folder + npm name **`psp-…`** as a sibling of `Project-Starter-Pack` (default parent = directory that contains this repo).
- **Vite + TypeScript** — `npm run dev` / `npm run build`. Each child gets a **unique dev port** (`5200–6099`) at bootstrap so multiple PSP projects can run in Cursor without fighting over `5173`.
- **CI** — workflow in the template (install + build) for hosts that run it.
- **Idea layer** — root **`DESIGN.md`**, **`ideas/INBOX.md`**; **`docs/`** for longer notes (includes **`INDUSTRY_STANDARD_VERSIONING.md`** and **`GITHUB_SETUP_WALKTHROUGH.md`** after bootstrap).
- **`.cursor/rules`** in the child — **`user-project-standard`**, **`github-setup-offer`** (YES/NO GitHub prompt), **`github-push-offer`** (optional commit/push reminder after meaningful work when `origin` exists), plus **`karpathy-guidelines`** ([andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills), MIT); delete rules you do not want.

Remote hosting is **one-time** when the user wants off-machine backup — see **[INDUSTRY_STANDARD_VERSIONING.md](INDUSTRY_STANDARD_VERSIONING.md)** and [AGENTS.md](AGENTS.md).

## More templates later

**v1 ships one stack:** `template/web-vite-ts` (Vite + TypeScript). That is enough for fast web/creative work.

**Adding another template later:** create `template/<your-template-id>/` (copy the shape of `web-vite-ts`: `package.json`, `README.md`, `.github/workflows`, placeholders if needed), then extend `bootstrap_new_project.py` with a `--template` flag (or a small registry dict) so agents pick the right folder. Keep each template **minimal** and **`npm run build`**-clean before documenting it in this README.

Until then, the default stays **`web-vite-ts`**.

## Scope (v1)

**In scope:** one **web** stack (Vite + TypeScript), local dev, production build, optional CI in the child from the template, and the human vs agent contract above.

**Out of scope for v1:** native mobile apps, backend-only services, monorepos, or non-Node toolchains — add another `template/…` when you need those, not by stretching this template.

## Third-party notices

**`karpathy-guidelines.mdc`** (factory and template) is adapted from [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) (MIT). Full attribution and disclaimer: **[docs/THIRD_PARTY_NOTICES.md](docs/THIRD_PARTY_NOTICES.md)**.
