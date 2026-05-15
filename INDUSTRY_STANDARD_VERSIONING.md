# Git and industry-standard versioning (Project Starter Pack)

This starter pack keeps **history in Git** on your machine. **Off-machine backup** is optional: you add a **remote** on whatever git hosting you use. It does **not** use custom “save every edit to a special folder” workflows.

**What the bootstrap script does *not* do:** `bootstrap_new_project.py` does **not** create a remote repository, set `git remote`, or push. It only prepares a **local** git repo with an initial commit.

The first commit may show a **placeholder git author** (`Project Starter Pack bootstrap`) so the commit succeeds without global `git user.name`; run **`git commit --amend --reset-author`** before pushing if you want your name on that commit.

---

## Part 1: Local Git (every day)

Work inside your project folder (the one that contains `package.json`).

### Check status

```bash
git status
```

### Record changes

```bash
git add -A
git commit -m "Describe what changed in plain language"
```

Use short, honest commit messages. Commit **`package-lock.json`** whenever dependencies change.

---

## Part 2: Optional remote (one-time per project)

When you want backups off this computer, create an **empty** repository using your host’s website or tools, then connect this folder.

### Step 1 — Copy the clone URL from your host

Your provider shows an **HTTPS** or **SSH** URL for the empty repo (often ending in `.git` for HTTPS). Keep it for the next step.

### Step 2 — Link this folder to the remote

Replace the URL with **yours** (HTTPS example):

```bash
git remote add origin https://YOUR-HOST/YOUR-USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

- **`git remote add origin …`** stores the remote under the name `origin`.
- **`git branch -M main`** names your default branch `main` (common convention).
- **`git push -u origin main`** uploads your existing commits.

### If `git remote add` says “remote origin already exists”

```bash
git remote -v
```

Fix a wrong URL:

```bash
git remote set-url origin https://YOUR-HOST/YOUR-USERNAME/YOUR_REPO.git
```

Then run `git push -u origin main` again.

### If the remote was created with an initial README or license

The remote has commits you do not have locally yet. Sync once, then push:

```bash
git pull origin main --rebase
git push -u origin main
```

Ask your agent for help if this step feels confusing.

---

## Part 3: Sign-in and HTTPS pushes

Many hosts **do not** accept your normal website login password for `git push` over HTTPS. Use what your provider documents instead: **personal access token**, **credential helper**, **SSH keys**, or a **CLI login** tool they support.

**Safety:** treat tokens like passwords. Do **not** paste them into AI chat or commit them into the repo. If one leaks, revoke it at the host and create a new one.

---

## Part 4: What you get when a remote works

| Piece | What it does for you |
|--------|-------------------------|
| **Git commits** | History on your machine: what changed, when, with messages. |
| **`git push`** | Copies commits to the remote so they survive a lost laptop. |
| **`package-lock.json`** | Same dependencies everywhere; keep it committed. |
| **CI** | On supported hosts, the template can run **`npm ci`** + **`npm run build`** automatically on pushes to `main` (see the workflow file bundled with the template). |
| **Tags / releases** | Optional later when you ship — not required on day one. |

---

## What this starter pack does *not* do

- No **`code-history/`** folders maintained by a custom script.  
- No hooks that bump **`package.json`** on every save.  
- No second “version diary” beside Git.

Other repos may use different patterns; **Project Starter Pack projects use Git + lockfile + build (+ optional remote + CI) only.**

---

## For AI agents helping the user

When off-machine backup matters, help them create an **empty** remote repo (per their host’s UI), then **Part 2** in the terminal. Use **Part 3** only if `git push` fails with an authentication error. Do **not** ask them to paste tokens or passwords into chat.

In **PSP child projects**, after meaningful work and when **`origin`** is configured, follow **`.cursor/rules/github-push-offer.mdc`**: one short line offering **commit and push**, **commit only**, or **skip** — do not push without the user agreeing in that turn.

Official Git reference: **[https://git-scm.com/doc](https://git-scm.com/doc)**
