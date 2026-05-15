# Upgrading older `psp-…` child projects

The factory repo does **not** rewrite folders that already exist. Projects created from an **older** template stay as-is until you change them.

**When to read this:** you want your existing app folder to match current `template/web-vite-ts` behavior (CI, Vite defaults, docs).

**Practical options:**

1. **Light sync** — Compare your repo to the current template in `Project-Starter-Pack/template/web-vite-ts/` (especially `vite.config.ts`, `.github/workflows/ci.yml`, `.gitignore`, `package.json` / lockfile, and **`.cursor/rules/`** — e.g. add **`karpathy-guidelines.mdc`**, **`github-push-offer.mdc`**, or refresh **`github-setup-offer.mdc`**). Copy **`docs/HANDOFF_MESSAGES.md`** from the factory into your child’s **`docs/`** for the premium Beat A/B first-run messages. Copy diffs you care about, then run **`npm ci`** and **`npm run build`**. **Dev URLs:** add **`host: true`** under `server` in `vite.config.ts` if **`http://127.0.0.1:PORT`** fails but **`http://localhost:PORT`** works. **Port conflicts:** if several PSP apps all use `5173`, give each a unique `server.port` in `vite.config.ts` (new bootstraps get one automatically in the `5200–6099` range) and set **`strictPort: true`** so Vite does not silently switch ports.
2. **Re-bootstrap** — Create a **new** sibling with bootstrap and copy over `src/`, `DESIGN.md`, and `ideas/` if you prefer a clean tree.
3. **Do nothing** — Older children keep working if `npm run build` still passes; only adopt template changes when you need them.

Versioning and optional remotes: **`docs/INDUSTRY_STANDARD_VERSIONING.md`** in the child (same content as the starter pack’s **`INDUSTRY_STANDARD_VERSIONING.md`** before bootstrap).

If **`rmtree` / cleanup fails** (another program has files open, corporate antivirus, or disk full): close processes using that folder, fix disk space, then delete the `psp-…` path manually and run bootstrap again.
