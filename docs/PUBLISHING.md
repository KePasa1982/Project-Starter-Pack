# Publishing this repo to GitHub

Use this checklist **once** when you turn your local **Project Starter Pack** into a public (or private) GitHub repository. It is for **maintainers**, not for end users bootstrapping `psp-…` apps.

## Before the first push

1. **Remove local-only artifacts** (should already be ignored; delete if present):
   - `template/**/node_modules/`
   - `template/**/dist/`, `template/**/dist-ssr/`
2. **Third-party notices** — **[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)** is included for the Karpathy-style Cursor rule (MIT upstream).
3. **Scan for personal data** — factory docs must stay generic (no home paths, usernames, tokens, or machine names). Unit tests include a privacy scan; run:

   ```bash
   python3 -m unittest discover -s tests -p "test_*.py" -v
   ```

4. **Verify the template builds** (from repo root):

   ```bash
   cd template/web-vite-ts && npm ci && npm run build && cd ../..
   ```

## Initialize git (if not already)

From the **Project-Starter-Pack** folder:

```bash
git init
git add -A
git status   # confirm node_modules/ and dist/ are NOT listed
git commit -m "Initial public release of Project Starter Pack"
```

## Create the GitHub repository

1. On GitHub: **New repository** → name e.g. `Project-Starter-Pack` → **do not** add a README if you already have one locally.
2. Add the remote and push (replace `YOUR_USER`):

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USER/Project-Starter-Pack.git
git push -u origin main
```

Use SSH (`git@github.com:YOUR_USER/Project-Starter-Pack.git`) if you prefer SSH keys.

## After push

- Enable **Actions** on the repo so [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) runs on `main` (Linux + Windows).
- Optional: add a repo description and topics (`cursor`, `vite`, `starter-template`).
- Share [README.md](../README.md) and [FOR_USER.md](../FOR_USER.md) with anyone cloning the pack.

**Privacy:** never commit `.env` files, PATs, or `~/.git-credentials`. Child-project GitHub setup stays in each user’s session — see [GITHUB_SETUP_WALKTHROUGH.md](GITHUB_SETUP_WALKTHROUGH.md).
