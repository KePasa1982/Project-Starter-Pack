# Handoff messages — premium first-run UX (for AI agents)

**Audience:** agents only. Send the **user-facing** blocks below in chat after bootstrap.  
**Do not** commit real usernames, tokens, or secrets into this file in the factory repo — fill placeholders from **bootstrap stdout** for **this** user only.

---

## Cursor chat constraints (read once)

| Can do | Cannot do |
|--------|-----------|
| Rich **Markdown**: headings, tables, dividers, emoji icons | Custom HTML or real **clickable buttons** |
| **One-click copy** for the user via **fenced code blocks** (Cursor shows **Copy** on the block) | Embed working UI widgets |
| Short, scannable **tables** for status and choices | Dump setup lectures in Beat A |

**Copy UX rule:** anything the user might paste (folder path, shell commands) goes in its **own** fenced block — **nothing else in that block**. Tell them once: *Use **Copy** on the code block.*

**Windows shell rule:** **Windows PowerShell 5** (default in Cursor on Windows) does **not** support `&&`. User-facing command blocks must use **one command per line** (works in PowerShell 5, PowerShell 7+, Git Bash, and macOS/Linux shells). On Windows, mention **`npm.cmd`** if the user hit script execution policy errors. Do **not** chain with `&&` unless you know the user is in **Git Bash** and you label it as such.

**Visual rule:** keep the **structure** below (icons, tables, dividers, numbered steps). Do not collapse to a plain paragraph. Premium = tidy, scannable, warm — not a wall of text.

**Tone:** confident, warm, premium product — not cheesy. Beat A = **one** message. Beat B = **one** message after GitHub YES or NO.

---

## Beat A — first reply (immediately after bootstrap)

**Fill placeholders:** `{{DISPLAY_TITLE}}` · `{{CHILD_FOLDER}}` · `{{PROJECT_KIND_LABEL}}` (from bootstrap: browser or desktop line)

**Do not include in Beat A:** `npm run dev` / `tauri:dev`, Local URLs, `DESIGN.md`, amend-author hints, versioning doc links.

### User message (copy structure; adapt only placeholders)

```markdown
# ✨ {{DISPLAY_TITLE}}

> **Project Starter Pack** · Your workspace is ready on this machine.

---

## 🧩 Setup status

|  | Step | Status |
|--|------|--------|
| 🏗️ | Project scaffold | ✅ Complete |
| 🧰 | Project type | ✅ {{PROJECT_KIND_LABEL}} |
| 📦 | Dependencies locked | ✅ `package-lock.json` |
| 🔨 | Production build | ✅ Passed |
| 📝 | Git history (local) | ✅ Initial commit |

---

## 📂 Open this project in Cursor

Open **this folder** — not `Project-Starter-Pack`:

```
{{CHILD_FOLDER}}
```

💡 **Copy tip:** use **Copy** on the block above for the full path in one step.

---

## 🔗 Optional — GitHub backup

Your work is already safe **on this PC** with Git.  
GitHub is optional cloud backup — your choice:

|  | Reply | What happens next |
|--|-------|-------------------|
| ☁️ | **YES** | Guided setup — you run commands, we walk each step |
| 💻 | **NO** | Skip for now — start building; connect GitHub anytime |

### 👉 Reply with one word: **YES** or **NO**

---

<sub>🎨 You bring ideas · We handle folders, git, and setup</sub>
```

---

## Beat B — after GitHub YES or NO

**Pick the Beat B block** that matches bootstrap **kind** (`browser` or `desktop`).

**Shared placeholders:** `{{DISPLAY_TITLE}}` · `{{CHILD_FOLDER}}` · `{{DEV_PORT}}` · `{{LOCAL_URL}}` (usually `http://localhost:{{DEV_PORT}}`)

**Pick exactly one GitHub status line** (first subsection under the title):

**If GitHub was set up (YES path):**

```markdown
> ☁️ **GitHub connected** — `https://github.com/<USERNAME>/<REPO>`
```

**If user declined (NO path):**

```markdown
> 💻 **GitHub skipped** — say when you want to connect; your project is safe on disk with Git.
```

---

### Beat B — browser (Vite in browser)

```markdown
# 🚀 Ready to build

## {{DISPLAY_TITLE}}

<PASTE ONE GITHUB STATUS LINE FROM ABOVE>

---

## ▶️ Run your project

### Step 1 · Open folder

```
{{CHILD_FOLDER}}
```

### Step 2 · Start dev server

Copy and run in your terminal *(one command per line)*:

```powershell
cd "{{CHILD_FOLDER}}"
npm run dev
```

*Windows PowerShell 5:* use `npm.cmd run dev` if `npm` is blocked by execution policy.

### Step 3 · Open preview

| 🌐 | URL |
|----|-----|
| **Primary** | {{LOCAL_URL}} |
| **Fallback** | http://127.0.0.1:{{DEV_PORT}} |

> **Windows note:** If the browser doesn’t open, allow **Node.js** through the firewall, then paste the **Local:** URL from the terminal.

---

## 💡 What should we build first?

Tell us in plain language — game, tool, screen, experiment.  
We implement · you design.

| 📌 | Where to capture ideas |
|----|-------------------------|
| 🎯 Big picture | `DESIGN.md` |
| ⚡ Quick notes | `ideas/INBOX.md` |

---

<sub>Project Starter Pack · Browser app · Git · lockfile · CI-ready</sub>
```

---

### Beat B — desktop (Tauri 2 native)

```markdown
# 🚀 Ready to build

## {{DISPLAY_TITLE}}

<PASTE ONE GITHUB STATUS LINE FROM ABOVE>

---

## 🖥️ Run your desktop app

### Step 1 · Open folder

```
{{CHILD_FOLDER}}
```

### Step 2 · Start native dev

Copy and run in your terminal *(one command per line)*:

```powershell
cd "{{CHILD_FOLDER}}"
npm run tauri:dev
```

*Windows PowerShell 5:* use `npm.cmd run tauri:dev` if `npm` is blocked.  
*First run* compiles Rust — may take a few minutes. Install [Rust](https://rustup.rs) if prompted.

### Step 3 · What you should see

| 🪟 | Expect |
|----|--------|
| **Window** | A native desktop app opens (not a browser tab) |
| **Port** | Vite runs behind the scenes on port **{{DEV_PORT}}** |

### Step 4 · Build installer (when ready)

```powershell
cd "{{CHILD_FOLDER}}"
npm run tauri:build
```

Produces a native installer (`.exe` on Windows) under `src-tauri/target/release/bundle/`.

---

## 💡 What should we build first?

Tell us in plain language — desktop tool, game, utility, experiment.  
We implement · you design.

| 📌 | Where to capture ideas |
|----|-------------------------|
| 🎯 Big picture | `DESIGN.md` |
| ⚡ Quick notes | `ideas/INBOX.md` |

---

<sub>Project Starter Pack · Desktop app (Tauri 2) · Git · lockfile · CI-ready</sub>
```

---

## Agent checklist

- [ ] User chose **BROWSER** or **DESKTOP** before bootstrap (unless they already specified in the request).
- [ ] Beat A sent **once**, using the Beat A template (placeholders filled).
- [ ] Wait for **YES** or **NO** before Beat B.
- [ ] Beat B sent **once** — **browser** or **desktop** block + correct GitHub line.
- [ ] Paths/commands only in **dedicated** copy-friendly code blocks.
- [ ] Never ask for tokens or passwords in chat.
