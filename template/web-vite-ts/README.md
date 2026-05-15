# {{PROJECT_TITLE}}

Created from **Project Starter Pack** (`web-vite-ts` template).

## Commands

```bash
npm ci            # clean install from lockfile (matches CI; use after clone)
npm install       # when you change dependencies (then commit package-lock.json)
npm run dev       # local dev server (port {{DEV_PORT}} — unique per PSP project)
npm run build     # typecheck + production bundle
npm run preview   # preview production build
```

**Dev preview:** `npm run dev` uses port **{{DEV_PORT}}** (chosen at bootstrap so multiple PSP projects do not fight over `5173`). Vite tries to open **`http://127.0.0.1:{{DEV_PORT}}/`** in your browser or Cursor. If nothing opens (common on first Windows run — allow **Node.js** in the firewall, then paste the **Local:** URL from the terminal). On SSH-only machines, set **`server.open: false`** in **`vite.config.ts`**.

## For the user

Read [FOR_USER.md](FOR_USER.md). You focus on ideas; agents keep the folder and git healthy.

**Where to put inspiration (after the repo exists):**

- [`DESIGN.md`](DESIGN.md) — vision and design intent  
- [`ideas/INBOX.md`](ideas/INBOX.md) — quick bullets and links  
- [`docs/`](docs/) — longer notes  

You do not need to open `src/` unless you want to see the running app.

**Saving versions:** this template uses **Git** locally; an optional **remote** is for off-machine backup. After bootstrap, see **[`docs/INDUSTRY_STANDARD_VERSIONING.md`](docs/INDUSTRY_STANDARD_VERSIONING.md)**.
