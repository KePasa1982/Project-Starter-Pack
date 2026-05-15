# For the user (Project Starter Pack)

Your **first step** is **inspiration** — a direction, a thing to try, a spark.

**Why `PSP` / `psp-` on names:** this pack tags projects it created so you can tell them apart from everything else on disk. Your creative title still drives the slug; you do not need to invent folder names.

**You do not** create project folders or invent a custom “how to save versions” system. Say you want a **new** project using the **Project Starter Pack**; the agent builds a **sibling folder** next to the starter pack (same **parent directory** as the folder that contains `Project-Starter-Pack`, unless you use `--dest`) whose name **starts with `psp-`**, and the project title in the UI shows **`PSP …`** so you can tell it came from this pack. **Saving versions** uses **Git** locally; see **[INDUSTRY_STANDARD_VERSIONING.md](INDUSTRY_STANDARD_VERSIONING.md)** for optional **remote** backup. After bootstrap, the same guide is copied into your new project as **`docs/INDUSTRY_STANDARD_VERSIONING.md`**.

After the project exists, jot inspiration in **`DESIGN.md`** (big picture) and/or **`ideas/INBOX.md`** (quick bullets) in **that new project** — the agent can type for you if you prefer talking.

**Git note:** the first bootstrap commit may list a placeholder author so the commit always succeeds; your agent or you can run **`git commit --amend --reset-author`** before pushing if you want your name on that commit.

**GitHub (optional):** right after your project is created, the agent should ask whether you want to **set up GitHub** for this project (**YES** / **NO**). If **YES**, they walk you through every step on **your** PC — you do not need to figure out the how yourself.

**First message after bootstrap:** your agent sends a polished **Beat A** screen (checklist, your folder path with one-click **Copy**, GitHub **YES** / **NO**) — templates live in **`docs/HANDOFF_MESSAGES.md`** in each new project.

**Trigger (example):**

> I’d like to start a new project — use the **Project Starter Pack**. Title: **“…”**. I only want to design; you handle the rest.

Read [README.md](README.md) if you want the one-screen summary.
