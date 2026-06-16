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

**Windows shell rule:** **Windows PowerShell 5** (default in Cursor on Windows) does **not** support `&&`. User-facing command blocks must use **one command per line** (works in PowerShell 5, PowerShell 7+, Git Bash, and macOS/Linux shells). Do **not** chain with `&&` unless you know the user is in **Git Bash** and you label it as such.

**Tone:** confident, warm, premium product — not cheesy, not a wall of text. Beat A = **one** message. Beat B = **one** message after GitHub YES or NO.

---

## Beat A — first reply (immediately after bootstrap)

**Fill placeholders:** `{{DISPLAY_TITLE}}` · `{{CHILD_FOLDER}}` (absolute path from bootstrap)

**Do not include in Beat A:** `npm run dev`, Local URLs, `DESIGN.md`, amend-author hints, versioning doc links.

### User message (copy structure; adapt only placeholders)

```markdown
# ✨ {{DISPLAY_TITLE}}

**Project Starter Pack** — your project is live on this machine.

---

### ✅ Ready checklist

| Step | Status |
|------|--------|
| Scaffold (Vite + TypeScript) | ✓ Done |
| Git history (local) | ✓ Initial commit |
| Locked dependencies | ✓ `package-lock.json` |
| Production build | ✓ Passed |

---

### 📁 Open in Cursor

When you start building, open **this folder** (not Project-Starter-Pack):

```
{{CHILD_FOLDER}}
```

*Tip: click **Copy** on the block above — the full path is selected in one step.*

---

### 🔗 Next: GitHub backup (optional)

Your work is already saved **locally with Git**.  
**GitHub** is optional off-machine backup — you choose:

| Reply | What we do next |
|-------|-----------------|
| **YES** | Step-by-step GitHub setup — you run commands; we guide each step |
| **NO** | Skip for now — jump to building; connect GitHub anytime later |

**Reply with one word:** **YES** or **NO**

---

*You focus on ideas — we handle layout, git hygiene, and the boring setup.*
```

---

## Beat B — after GitHub YES or NO

**Fill placeholders:** `{{DISPLAY_TITLE}}` · `{{CHILD_FOLDER}}` · `{{DEV_PORT}}` · `{{LOCAL_URL}}` (usually `http://localhost:{{DEV_PORT}}`)

**Pick exactly one GitHub status line** (first subsection under the title):

**If GitHub was set up (YES path):**

```markdown
> **GitHub connected** — `https://github.com/<USERNAME>/<REPO>`
```

**If user declined (NO path):**

```markdown
> **GitHub skipped** — say when you want to connect; your project is safe on disk with Git.
```

### User message (copy structure; adapt placeholders + one GitHub line)

```markdown
# 🚀 You're ready to build

## {{DISPLAY_TITLE}}

<PASTE ONE GITHUB STATUS LINE FROM ABOVE>

---

### ▶️ Run locally

**1.** In Cursor, open folder:

```
{{CHILD_FOLDER}}
```

**2.** Start the dev server — **Copy** and run in your terminal (one command per line):

```powershell
cd "{{CHILD_FOLDER}}"
npm run dev
```

*Works in **PowerShell** (including Windows PowerShell 5). Do not use `&&` on Windows — it errors in the default shell.*

**3.** Open the preview:

| | |
|---|---|
| **Primary** | {{LOCAL_URL}} |
| **Alternate** | http://127.0.0.1:{{DEV_PORT}} |

*Vite tries to open **`http://127.0.0.1:{{DEV_PORT}}/`** automatically. Each PSP project uses its own port so nothing fights over `5173`. **Windows:** if nothing opens, allow **Node.js** in the firewall when prompted, then paste the **Local:** URL from the terminal.*

---

### 💡 What should we make first?

Describe it in plain language — screens, game, tool, experiment.  
We'll implement; you design.

| Where ideas live | |
|------------------|---|
| Big picture | `DESIGN.md` |
| Quick jots | `ideas/INBOX.md` |

---

*Project Starter Pack · Git · lockfile · CI-ready · optional GitHub when you want it*
```

---

## Agent checklist

- [ ] Beat A sent **once**, using the Beat A template (placeholders filled).
- [ ] Wait for **YES** or **NO** before Beat B.
- [ ] Beat B sent **once**, using the Beat B template + correct GitHub line.
- [ ] Paths/commands only in **dedicated** copy-friendly code blocks.
- [ ] Never ask for tokens or passwords in chat.
