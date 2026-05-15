#!/usr/bin/env python3
"""Create a new sibling project from template/web-vite-ts. The user does not run this by hand — agents do."""

from __future__ import annotations

import argparse
import re
import shutil
import socket
import subprocess
import sys
import zlib
from pathlib import Path

STARTER_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = STARTER_ROOT / "template" / "web-vite-ts"


def _tool_exe(name: str) -> str:
    """Resolve a CLI on PATH (on Windows, ``npm`` is ``npm.cmd`` — needs ``shutil.which``)."""
    path = shutil.which(name)
    if not path:
        raise FileNotFoundError(
            f"{name!r} not found on PATH. Install it and try again "
            f"(bootstrap needs git and npm)."
        )
    return path


def _argv(tool: str, *args: str) -> list[str]:
    return [_tool_exe(tool), *args]

# Every PSP project is labeled so the user can spot them next to other folders and in the UI.
PSP_DISPLAY_PREFIX = "PSP "
PSP_SLUG_PREFIX = "psp-"
# npm package name rules (1–64 chars): alnum, single-char ok; multi-char cannot start/end with hyphen.
_SLUG_FULLMATCH = re.compile(r"[a-z0-9][a-z0-9-]{0,62}[a-z0-9]|[a-z0-9]")
_VITE_PORT_RE = re.compile(r"port:\s*(\d+)", re.MULTILINE)
_VITE_PORT_ASSIGN_RE = re.compile(r"(port:\s*)(\d+)(\s*,)")

# Dev ports for PSP children (avoid Vite default 5173 so multiple projects do not collide in Cursor).
DEV_PORT_MIN = 5200
DEV_PORT_MAX = 6099


def slug_is_valid(slug: str) -> bool:
    return bool(_SLUG_FULLMATCH.fullmatch(slug))


def strip_psp_marker(title: str) -> str:
    """Remove a leading PSP / (PSP) marker so we do not double-prefix."""
    s = title.strip()
    s = re.sub(r"^\(\s*PSP\s*\)\s*", "", s, flags=re.IGNORECASE).strip()
    s = re.sub(r"^PSP(?:\s+|[–—\-_:])\s*", "", s, flags=re.IGNORECASE).strip()
    if re.fullmatch(r"PSP", s, flags=re.IGNORECASE):
        return ""
    return s


def with_display_title(title: str) -> str:
    base = strip_psp_marker(title)
    if not base:
        return PSP_DISPLAY_PREFIX.strip()
    return PSP_DISPLAY_PREFIX + base


def with_slug_prefix(slug: str) -> str:
    slug = slug.strip().lower()
    if slug.startswith(PSP_SLUG_PREFIX):
        return slug
    return PSP_SLUG_PREFIX + slug


def trim_slug(slug: str, max_len: int = 64) -> str:
    if len(slug) <= max_len:
        return slug
    if slug.startswith(PSP_SLUG_PREFIX):
        rest = slug[len(PSP_SLUG_PREFIX) :]
        room = max_len - len(PSP_SLUG_PREFIX)
        if room < 1:
            return slug[:max_len].rstrip("-")
        rest = rest[:room].rstrip("-")
        if not rest:
            rest = "project"
        out = PSP_SLUG_PREFIX + rest
        if len(out) > max_len:
            return out[:max_len].rstrip("-")
        return out
    return slug[:max_len].rstrip("-")


def slugify(title: str) -> str:
    s = title.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[-\s]+", "-", s).strip("-")
    return s or "untitled-project"


def non_ascii_slug_help_suffix(slug: str, raw_title: str) -> str:
    """Extra help when slug/title contains non-ASCII (slugify can keep Unicode letters)."""
    if any(ord(c) > 127 for c in slug) or any(ord(c) > 127 for c in raw_title):
        return (
            " For titles with non-Latin characters or emoji, pass an ASCII `--slug` "
            "(e.g. `--slug my-neon-maze`)."
        )
    return ""


def exit_if_slug_invalid(slug: str, raw_title: str) -> None:
    if slug_is_valid(slug):
        return
    sys.exit(
        f"Invalid slug {slug!r}. Use lowercase letters, digits, hyphens only "
        f"(npm package name rules, 1–64 chars).{non_ascii_slug_help_suffix(slug, raw_title)}"
    )


def replace_placeholders(text: str, title: str, slug: str, dev_port: int) -> str:
    name = title
    port_s = str(dev_port)
    return (
        text.replace("{{PROJECT_TITLE}}", title)
        .replace("{{PROJECT_SLUG}}", slug)
        .replace("{{PROJECT_NAME}}", name)
        .replace("{{DEV_PORT}}", port_s)
    )


def dev_port_base_from_slug(slug: str) -> int:
    """Stable preferred port from slug (same slug → same port when free)."""
    span = DEV_PORT_MAX - DEV_PORT_MIN + 1
    h = zlib.crc32(slug.encode("utf-8")) & 0xFFFFFFFF
    return DEV_PORT_MIN + (h % span)


def _read_vite_port(path: Path) -> int | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    m = _VITE_PORT_RE.search(text)
    return int(m.group(1)) if m else None


def collect_reserved_dev_ports(parent: Path, *, exclude: Path | None = None) -> set[int]:
    """Ports already claimed by sibling ``psp-*`` projects under ``parent``."""
    reserved: set[int] = set()
    if not parent.is_dir():
        return reserved
    for child in parent.iterdir():
        if not child.is_dir() or not child.name.startswith(PSP_SLUG_PREFIX):
            continue
        if exclude is not None and child.resolve() == exclude.resolve():
            continue
        port = _read_vite_port(child / "vite.config.ts")
        if port is not None:
            reserved.add(port)
    return reserved


def is_tcp_port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


def allocate_dev_port(slug: str, parent: Path, *, exclude: Path | None = None) -> int:
    """Pick a dev port unique among siblings and free on this machine."""
    reserved = collect_reserved_dev_ports(parent, exclude=exclude)
    span = DEV_PORT_MAX - DEV_PORT_MIN + 1
    start = dev_port_base_from_slug(slug)
    for offset in range(span):
        port = DEV_PORT_MIN + ((start - DEV_PORT_MIN + offset) % span)
        if port in reserved:
            continue
        if is_tcp_port_free(port):
            return port
    sys.exit(
        f"No free dev port in range {DEV_PORT_MIN}–{DEV_PORT_MAX} "
        f"(sibling PSP projects or running servers may be using them)."
    )


def _ignore_copytree_artifacts(_src: str, names: list[str]) -> list[str]:
    """Do not copy install/build outputs — a copied ``node_modules`` breaks ``npm install`` in the child."""
    skip = {"node_modules", "dist", "dist-ssr", ".git"}
    return [n for n in names if n in skip]


def under_skipped_dir(p: Path, target: Path) -> bool:
    skip_dirs = {"node_modules", "dist", "dist-ssr", ".git"}
    try:
        rel = p.relative_to(target)
    except ValueError:
        return True
    return any(part in skip_dirs for part in rel.parts)


def _cleanup_failed_bootstrap(target: Path) -> None:
    """Remove the project folder so bootstrap can be retried after a failure."""
    print(
        "[bootstrap] removing incomplete project folder (fix the error above, then run bootstrap again).",
        file=sys.stderr,
        flush=True,
    )
    try:
        shutil.rmtree(target)
    except OSError as e:
        print(
            f"[bootstrap] warning: could not remove {target} ({e}). Delete it manually before retrying.",
            file=sys.stderr,
            flush=True,
        )


def _materialize_project_tree(target: Path, title: str, slug: str, dev_port: int) -> None:
    """Copy template, rename AGENTS, replace placeholders, add industry guide. No git yet."""
    shutil.copytree(TEMPLATE, target, ignore=_ignore_copytree_artifacts)
    agents_tpl = target / "AGENTS.md.template"
    if agents_tpl.is_file():
        agents_tpl.rename(target / "AGENTS.md")
    apply_placeholders(target, title, slug, dev_port)
    patch_vite_dev_port(target, dev_port)
    dest_docs = target / "docs"
    dest_docs.mkdir(parents=True, exist_ok=True)
    for name in (
        "INDUSTRY_STANDARD_VERSIONING.md",
        "GITHUB_SETUP_WALKTHROUGH.md",
        "HANDOFF_MESSAGES.md",
        "THIRD_PARTY_NOTICES.md",
    ):
        src = STARTER_ROOT / name if name == "INDUSTRY_STANDARD_VERSIONING.md" else STARTER_ROOT / "docs" / name
        if src.is_file():
            shutil.copy2(src, dest_docs / name)


def _materialize_with_cleanup(target: Path, title: str, slug: str, dev_port: int) -> bool:
    """Create tree under ``target``; on failure remove ``target`` if it exists. Returns True on success."""
    try:
        _materialize_project_tree(target, title, slug, dev_port)
    except Exception as e:
        print(
            f"[bootstrap] error: failed while preparing project folder ({e}).",
            file=sys.stderr,
            flush=True,
        )
        if target.exists():
            try:
                shutil.rmtree(target)
            except OSError:
                pass
        return False
    return True


def patch_vite_dev_port(target: Path, dev_port: int) -> None:
    """Set the Vite dev server port in the child ``vite.config.ts``."""
    vite = target / "vite.config.ts"
    if not vite.is_file():
        return
    raw = vite.read_text(encoding="utf-8")
    new, count = _VITE_PORT_ASSIGN_RE.subn(rf"\g<1>{dev_port}\g<3>", raw, count=1)
    if count != 1:
        sys.exit(f"Could not patch dev port in {vite}")
    vite.write_text(new, encoding="utf-8")


def apply_placeholders(target: Path, title: str, slug: str, dev_port: int) -> None:
    for path in target.rglob("*"):
        if not path.is_file() or under_skipped_dir(path, target):
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".woff2"}:
            continue
        try:
            raw = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if "{{PROJECT_" not in raw and "{{DEV_PORT}}" not in raw:
            continue
        path.write_text(replace_placeholders(raw, title, slug, dev_port), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap a new PSP project from web-vite-ts template.")
    parser.add_argument("--title", required=True, help='Idea name (e.g. "Neon Maze"). "PSP " is added automatically to the display title.')
    parser.add_argument(
        "--slug",
        help="Folder + npm name (letters, digits, hyphens). Default: psp- + slug from title. "
        "`psp-` is added if missing so every PSP project is easy to spot on disk.",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        help="Parent directory for the new folder (default: parent directory of Project-Starter-Pack)",
    )
    args = parser.parse_args()

    raw_title = args.title.strip()
    if not raw_title:
        sys.exit("Empty --title")

    title = with_display_title(raw_title)

    if args.slug:
        slug = trim_slug(with_slug_prefix(args.slug.strip().lower()))
    else:
        slug = trim_slug(with_slug_prefix(slugify(strip_psp_marker(raw_title))))

    exit_if_slug_invalid(slug, raw_title)

    parent = args.dest.resolve() if args.dest else STARTER_ROOT.parent
    parent.mkdir(parents=True, exist_ok=True)
    target = parent / slug

    if target.exists():
        sys.exit(f"Refusing to overwrite existing path: {target}")

    if not TEMPLATE.is_dir():
        sys.exit(f"Missing template directory: {TEMPLATE}")

    dev_port = allocate_dev_port(slug, parent, exclude=target)

    if not _materialize_with_cleanup(target, title, slug, dev_port):
        return 1

    print(f"[bootstrap] created: {target}", flush=True)
    print(f"[bootstrap] title: {title!r} slug: {slug!r}", flush=True)
    print(
        f"[bootstrap] dev server: http://localhost:{dev_port} "
        f"(also http://127.0.0.1:{dev_port}; unique port for this project)",
        flush=True,
    )

    try:
        subprocess.run(_argv("git", "init"), cwd=target, check=True, capture_output=True, text=True)
        print("[bootstrap] git init: ok", flush=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"[bootstrap] error: git init failed ({e}). Install git and retry.", file=sys.stderr)
        try:
            shutil.rmtree(target)
        except OSError:
            pass
        return 1

    try:
        subprocess.run(_argv("npm", "install"), cwd=target, check=True)
        print("[bootstrap] npm install: ok", flush=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"[bootstrap] error: npm install failed ({e}).", file=sys.stderr)
        _cleanup_failed_bootstrap(target)
        return 1

    try:
        subprocess.run(_argv("npm", "run", "build"), cwd=target, check=True)
        print("[bootstrap] npm run build: ok", flush=True)
    except subprocess.CalledProcessError as e:
        print(f"[bootstrap] error: npm run build failed ({e}). Fix the template before handoff.", file=sys.stderr)
        _cleanup_failed_bootstrap(target)
        return 1

    try:
        subprocess.run(_argv("git", "add", "-A"), cwd=target, check=True, capture_output=True, text=True)
        # One-shot author so the first commit succeeds even when global git user.name/email is unset.
        commit = subprocess.run(
            _argv(
                "git",
                "-c",
                "user.name=Project Starter Pack bootstrap",
                "-c",
                "user.email=noreply@project-starter-pack.invalid",
                "commit",
                "-m",
                "chore: initial project from Project Starter Pack",
            ),
            cwd=target,
            capture_output=True,
            text=True,
            check=False,
        )
        if commit.returncode == 0:
            print("[bootstrap] git commit (initial): ok", flush=True)
            print(
                "[bootstrap] note: first commit uses a bootstrap-only git author; "
                "`git commit --amend --reset-author` if you want your name on it.",
                flush=True,
            )
        else:
            err = (commit.stderr or commit.stdout or "").strip()
            print(f"[bootstrap] error: initial git commit failed. {err}", file=sys.stderr)
            _cleanup_failed_bootstrap(target)
            return 1
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"[bootstrap] error: git commit step failed ({e}).", file=sys.stderr)
        _cleanup_failed_bootstrap(target)
        return 1

    print()
    print("[bootstrap] agent handoff (do not dump the old multi-step checklist on the user)")
    print(f"  Child folder: {target}")
    print(f"  Display title: {title}")
    print(
        f"  Dev URL (after Beat B): http://localhost:{dev_port} "
        f"(http://127.0.0.1:{dev_port} works too) — npm run dev opens in Cursor when server.open is true"
    )
    print("  First reply (Beat A): docs/HANDOFF_MESSAGES.md — premium template + GitHub YES/NO only.")
    print("  After GitHub YES or NO (Beat B): docs/HANDOFF_MESSAGES.md — then invite to build.")
    print(f"  Walkthrough: {target / 'docs' / 'GITHUB_SETUP_WALKTHROUGH.md'}")
    print(f"  Handoff UX: {target / 'docs' / 'HANDOFF_MESSAGES.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
