# GitHub setup walkthrough (for AI agents)

**Audience:** agents guiding **any** user after a Project Starter Pack bootstrap.  
**Not for:** pasting into chat with real usernames, tokens, or absolute paths from someone’s machine.

---

## Privacy and scope (non-negotiable)

| Where | What may appear |
|--------|------------------|
| **Project-Starter-Pack** (factory) | **Generic** instructions only. No real usernames, emails, tokens, PATs, or machine-specific absolute paths committed here. |
| **Child project** (`psp-…`) | After bootstrap, use **this user’s** folder path, GitHub username, and repo URL **only in chat or their local config** — never commit secrets or tokens into the repo. |

**Never ask the user to paste passwords or personal access tokens into AI chat.** They enter credentials only in **their** terminal or browser when Git prompts them.

---

## Mandatory prompt (right after bootstrap handoff)

When you have just finished bootstrap, send **Beat A** only — use the **Beat A** user template in **[HANDOFF_MESSAGES.md](HANDOFF_MESSAGES.md)** (premium layout: checklist table, folder path in a **copy-friendly** code block, GitHub **YES** / **NO**). Fill placeholders from bootstrap output; keep the structure — do not collapse to a plain paragraph.

**Do not put in Beat A:** `npm run dev`, browser/`Local:` instructions, `DESIGN.md` / `ideas/INBOX.md`, bootstrap author amend hints, or versioning doc links. GitHub first; local dev and “what to build” come in **Beat B** (Phase 5).

- **NO** — Say they can ask anytime; go to **Phase 5** (ready to build) without nagging.
- **YES** — Run the phases below **one phase at a time**. Wait for the user’s terminal output (or confirmation) before the next phase. You carry the checklist; they only run what you give them.

**Tone:** “I’ll tell you the next command; paste the output if something looks wrong.” The user should not plan *how* — you do.

### Windows shell (mandatory for agents)

| Shell | Chain commands? | What to give the user |
|-------|-----------------|------------------------|
| **PowerShell 5** (Windows default) | **No** — `&&` is a parse error | **One command per line** in a `powershell` fenced block |
| **PowerShell 7+** | Yes (`&&` works) | Still prefer **one command per line** (same block works everywhere) |
| **Git Bash** on Windows | Yes (`&&` works) | Multi-line is fine; `&&` only if you label the block `bash` |
| **macOS / Linux** | Yes | Multi-line is fine; `&&` optional |

**Never** paste `cd "…" && npm run …` or `… && git push` for a Windows user in PowerShell without splitting lines. See **[PLATFORMS.md](PLATFORMS.md)** — *Windows terminal commands*.

---

## Phase 0 — Discover current state (child project folder)

Resolve the child path from bootstrap output or `pwd` (e.g. `…/psp-my-game`). All commands assume:

```bash
cd <CHILD_PROJECT_FOLDER>
```

Run or ask the user to run and paste results:

```bash
git --version
git status -sb
git branch
git remote -v
git config --global user.name
git config --global user.email
git config --global credential.helper
```

**Interpret:**

| Signal | Meaning |
|--------|---------|
| `git: command not found` | → Phase 1A (install Git) |
| No `user.name` / `user.email` | → Phase 1B (identity) |
| `credential.helper` empty and they use HTTPS | → Phase 1C (credential helper) after first successful auth |
| `origin` already set | → Phase 3 may be “verify URL” only |
| Branch is `master` or `main` | Use **that** name for push (do not rename unless user asks) |

---

## Phase 1 — One-time machine setup (skip steps already OK)

### 1A — Install Git (only if missing)

- **Linux (Debian/Ubuntu):** `sudo apt update && sudo apt install -y git`
- **macOS:** Xcode Command Line Tools or Homebrew `git`
- **Windows:** [https://git-scm.com/download/win](https://git-scm.com/download/win)

Re-check: `git --version`.

### 1B — Git identity (recommended)

Ask for the name and email they use on GitHub, then:

```bash
git config --global user.name "THEIR_NAME"
git config --global user.email "THEIR_EMAIL"
```

Optional: fix bootstrap placeholder author on first commit only:

```bash
cd <CHILD_PROJECT_FOLDER>
git commit --amend --reset-author --no-edit
```

### 1C — Remember HTTPS login (recommended for HTTPS remotes)

After explaining that GitHub uses a **token** as the password (not account password):

```bash
git config --global credential.helper store
```

First successful `git push` saves credentials in `~/.git-credentials` on their machine (plain text — only on a PC they trust).

**Alternatives** (if user prefers): SSH keys + `git@github.com:USER/REPO.git`, or `gh auth login`. Do not mix three methods without reason.

---

## Phase 2 — Create empty GitHub repository (user in browser)

Walk them through:

1. Log in to GitHub in the browser.
2. **New repository** → name matches project slug if possible (e.g. `psp-my-game`).
3. **Do not** initialize with README, `.gitignore`, or license (bootstrap already committed files).
4. Copy the **HTTPS** clone URL: `https://github.com/<USERNAME>/<REPO>.git`

Confirm they have the URL before Phase 3.

---

## Phase 3 — Link local project to GitHub

In the child folder:

```bash
cd <CHILD_PROJECT_FOLDER>
git remote add origin https://github.com/<USERNAME>/<REPO>.git
```

If `origin` exists:

```bash
git remote set-url origin https://github.com/<USERNAME>/<REPO>.git
git remote -v
```

Detect branch:

```bash
git branch --show-current
```

Set upstream and push (replace `BRANCH` with `master` or `main` from above):

```bash
git push -u origin BRANCH
```

**User enters in terminal (not in chat):**

- Username: GitHub username  
- Password: **Personal access token** with `repo` scope  

---

## Phase 4 — Test push (proves the loop)

1. Make a tiny visible change (e.g. one line in `src/main.ts` or README).
2. `npm run build` (template standard).
3. Commit and push (one command per line — required on **Windows PowerShell 5**):

```powershell
cd <CHILD_PROJECT_FOLDER>
npm run build
git add -A
git commit -m "Test: verify GitHub push from local dev"
git push
```

Success: remote shows new commit. If push fails, → Troubleshooting.

**PowerShell 5:** if the user pasted a one-liner with `&&`, they see `The token '&&' is not a valid statement separator` — give them the multi-line block above.

---

## Phase 5 — Ready to build (Beat B — user-facing)

Send this **after** GitHub setup completes (**YES** path) **or** the user declines (**NO**). This is the **only** place to mention local dev in the bootstrap flow.

Use the **Beat B** user template in **[HANDOFF_MESSAGES.md](HANDOFF_MESSAGES.md)** — fill placeholders; paste the correct **GitHub status** line (connected vs skipped). Keep tables, dividers, and **copy-friendly** code blocks (folder path; `cd` + `npm run dev` as **separate lines** in a `powershell` block — never `&&` for Windows users).

Do **not** repeat bootstrap author / amend instructions unless they ask.

**After GitHub works:** ongoing work uses **`.cursor/rules/github-push-offer.mdc`** — agents offer *commit and push* / *commit only* / *skip* after meaningful tasks; they do not push without consent.

**Per new PSP project:** repeat Phase 2–3 only (new empty repo + `remote` + first push). Phase 1 is **once per PC**.

---

## Troubleshooting (agent quick reference)

| Symptom | Action |
|---------|--------|
| `The token '&&' is not a valid statement separator` | User is on **PowerShell 5** — replace any `&&` chain with **separate lines** (block above). |
| `could not read Username` / auth failed | PAT expired or wrong; create new token; ensure `credential.helper store` if they want HTTPS remembered |
| `remote origin already exists` | `git remote set-url origin …` |
| `rejected (fetch first)` | `git pull --rebase` then `git push` |
| `Permission denied (publickey)` | They use SSH URL but no key — switch to HTTPS or set up SSH |
| Pushed to wrong repo | `git remote set-url origin` correct URL |
| Agent cannot push from cloud | User runs `git push` locally; agent may commit locally if workspace is their machine |

---

## What the agent must not do

- Commit `.env`, tokens, or `~/.git-credentials` into any repo.
- Store the user’s GitHub username or home path in **Project-Starter-Pack** source files.
- Ask for token/password in chat.
- Run `git config --global` on the user’s machine **without** explaining it is one-time (prefer giving them the command to run).

---

## Checklist (agent internal — tick as you go)

- [ ] Phase 0: state discovered  
- [ ] Phase 1: Git installed / identity / credential helper (as needed)  
- [ ] Phase 2: empty GitHub repo created; URL confirmed  
- [ ] Phase 3: `origin` set; first `git push -u` succeeded  
- [ ] Phase 4: test commit pushed  
- [ ] Phase 5: Beat B sent (GitHub line if applicable, local dev, invite what to build)  
