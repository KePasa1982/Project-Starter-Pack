# {{PROJECT_TITLE}}

Created from **Project Starter Pack** (`tauri-vite-ts` template) — **native desktop app**.

## Commands

```bash
npm ci                  # clean install from lockfile (matches CI; use after clone)
npm install             # when you change dependencies (then commit package-lock.json)
npm run build           # typecheck + frontend bundle (fast; used by CI)
npm run tauri:dev       # native app window + hot reload (requires Rust — see below)
npm run tauri:build     # native installer (.exe on Windows)
```

**Dev preview:** `npm run tauri:dev` opens a **desktop window** (not a browser tab). Vite runs on port **{{DEV_PORT}}** behind the scenes. First run compiles Rust and may take a few minutes.

**Rust (one-time):** install from [https://rustup.rs](https://rustup.rs). On Windows, also install [Microsoft C++ Build Tools](https://learn.microsoft.com/en-us/windows/dev-environment/rust/setup) when prompted.

**Windows PowerShell:** if `npm` fails with a script policy error, use `npm.cmd` instead (e.g. `npm.cmd run tauri:dev`).

## For the user

Read [FOR_USER.md](FOR_USER.md). You focus on ideas; agents keep the folder and git healthy.

**Where to put inspiration (after the repo exists):**

- [`DESIGN.md`](DESIGN.md) — vision and design intent  
- [`ideas/INBOX.md`](ideas/INBOX.md) — quick bullets and links  
- [`docs/`](docs/) — longer notes  

You do not need to open `src/` unless you want to see the running app.

**Saving versions:** this template uses **Git** locally; an optional **remote** is for off-machine backup. After bootstrap, see **[`docs/INDUSTRY_STANDARD_VERSIONING.md`](docs/INDUSTRY_STANDARD_VERSIONING.md)**.
