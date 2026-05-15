"""Unit tests for ``scripts/bootstrap_new_project.py`` helpers (no network, no subprocess)."""

from __future__ import annotations

import importlib.util
import inspect
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT = _ROOT / "scripts" / "bootstrap_new_project.py"


def _load_bootstrap():
    spec = importlib.util.spec_from_file_location("bootstrap_new_project", _SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


b = _load_bootstrap()


class TestToolResolution(unittest.TestCase):
    def test_tool_exe_resolves_npm_and_git(self) -> None:
        for name in ("npm", "git"):
            path = b._tool_exe(name)
            self.assertTrue(path)
            self.assertEqual(b._argv(name, "--version")[0], path)


class TestSlugAndTitle(unittest.TestCase):
    def test_slug_is_valid(self) -> None:
        self.assertTrue(b.slug_is_valid("a"))
        self.assertTrue(b.slug_is_valid("psp-foo"))
        self.assertTrue(b.slug_is_valid("psp-ci-smoke-test"))
        self.assertFalse(b.slug_is_valid(""))
        self.assertFalse(b.slug_is_valid("-a"))
        self.assertFalse(b.slug_is_valid("a-"))
        self.assertFalse(b.slug_is_valid("psp-"))

    def test_trim_then_valid(self) -> None:
        long_body = "x" * 80
        slug = b.trim_slug(b.with_slug_prefix(long_body))
        self.assertLessEqual(len(slug), 64)
        self.assertTrue(b.slug_is_valid(slug), slug)

    def test_slugify_strip_prefix_roundtrip_valid(self) -> None:
        slug = b.trim_slug(b.with_slug_prefix(b.slugify(b.strip_psp_marker("  Neon Maze  "))))
        self.assertEqual(slug, "psp-neon-maze")
        self.assertTrue(b.slug_is_valid(slug))

    def test_with_display_title(self) -> None:
        self.assertEqual(b.with_display_title("Neon"), "PSP Neon")
        self.assertEqual(b.with_display_title("PSP Neon"), "PSP Neon")
        self.assertEqual(b.with_display_title("(PSP) Neon"), "PSP Neon")

    def test_replace_placeholders(self) -> None:
        raw = "name={{PROJECT_SLUG}} title={{PROJECT_TITLE}} port={{DEV_PORT}}"
        self.assertEqual(
            b.replace_placeholders(raw, "PSP T", "psp-t", 5432),
            "name=psp-t title=PSP T port=5432",
        )


class TestDevPortAllocation(unittest.TestCase):
    def test_dev_port_base_stable(self) -> None:
        p1 = b.dev_port_base_from_slug("psp-cool-day")
        p2 = b.dev_port_base_from_slug("psp-cool-day")
        p3 = b.dev_port_base_from_slug("psp-tetris-loco")
        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)
        self.assertGreaterEqual(p1, b.DEV_PORT_MIN)
        self.assertLessEqual(p1, b.DEV_PORT_MAX)

    def test_collect_reserved_from_siblings(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            parent = Path(td)
            a = parent / "psp-a"
            a.mkdir()
            (a / "vite.config.ts").write_text("port: 5201,\n", encoding="utf-8")
            b_dir = parent / "psp-b"
            b_dir.mkdir()
            (b_dir / "vite.config.ts").write_text("port: 5202,\n", encoding="utf-8")
            reserved = b.collect_reserved_dev_ports(parent)
            self.assertEqual(reserved, {5201, 5202})

    def test_allocate_skips_sibling_port(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            parent = Path(td)
            other = parent / "psp-other"
            other.mkdir()
            base = b.dev_port_base_from_slug("psp-new")
            (other / "vite.config.ts").write_text(f"port: {base},\n", encoding="utf-8")
            port = b.allocate_dev_port("psp-new", parent)
            self.assertNotEqual(port, base)
            self.assertGreaterEqual(port, b.DEV_PORT_MIN)
            self.assertLessEqual(port, b.DEV_PORT_MAX)


class TestMaterializeCleanup(unittest.TestCase):
    def test_cleanup_when_copytree_blocked_by_existing_target(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "psp-clash"
            target.mkdir()
            (target / "marker").write_text("x", encoding="utf-8")
            self.assertFalse(b._materialize_with_cleanup(target, "PSP X", "psp-clash", 5200))
            self.assertFalse(target.exists())

    def test_cleanup_when_materialize_raises(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "psp-fail"
            target.mkdir()
            with patch.object(b, "_materialize_project_tree", side_effect=RuntimeError("fail")):
                self.assertFalse(b._materialize_with_cleanup(target, "PSP X", "psp-fail", 5200))
            self.assertFalse(target.exists())


class TestSlugHelpSuffix(unittest.TestCase):
    def test_ascii_only_no_extra_suffix(self) -> None:
        self.assertEqual(b.non_ascii_slug_help_suffix("psp-bad-", "Neon"), "")

    def test_non_ascii_slug_gets_suffix(self) -> None:
        self.assertIn("--slug", b.non_ascii_slug_help_suffix("psp-\u3042", "Neon"))

    def test_non_ascii_title_gets_suffix(self) -> None:
        self.assertIn("--slug", b.non_ascii_slug_help_suffix("psp-bad-", "Café"))


class TestViteDevServerHost(unittest.TestCase):
    def test_template_listens_on_all_local_interfaces(self) -> None:
        vite = (_ROOT / "template" / "web-vite-ts" / "vite.config.ts").read_text(encoding="utf-8")
        self.assertIn("host: true", vite)

    def test_template_opens_explicit_local_url(self) -> None:
        vite = (_ROOT / "template" / "web-vite-ts" / "vite.config.ts").read_text(encoding="utf-8")
        self.assertRegex(vite, r'open:\s*"http://127\.0\.0\.1:5200/"')

    def test_template_vite_config_is_valid_typescript_for_ci(self) -> None:
        vite = (_ROOT / "template" / "web-vite-ts" / "vite.config.ts").read_text(encoding="utf-8")
        self.assertNotIn("{{DEV_PORT}}", vite)
        self.assertRegex(vite, r"port:\s*\d+")

    def test_patch_vite_dev_server_updates_port_and_open(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            vite = target / "vite.config.ts"
            vite.write_text(
                (_ROOT / "template" / "web-vite-ts" / "vite.config.ts").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            b.patch_vite_dev_server(target, 5432)
            text = vite.read_text(encoding="utf-8")
            self.assertRegex(text, r"port:\s*5432")
            self.assertRegex(text, r'open:\s*"http://127\.0\.0\.1:5432/"')


class TestChildTemplateCursorRules(unittest.TestCase):
    """Template must ship both Cursor rules for every bootstrapped child."""

    def test_both_rules_exist_and_always_apply(self) -> None:
        rules = _ROOT / "template" / "web-vite-ts" / ".cursor" / "rules"
        k = rules / "karpathy-guidelines.mdc"
        u = rules / "user-project-standard.mdc"
        self.assertTrue(k.is_file(), k)
        self.assertTrue(u.is_file(), u)
        self.assertIn("alwaysApply: true", k.read_text(encoding="utf-8"))
        self.assertIn("alwaysApply: true", u.read_text(encoding="utf-8"))
        self.assertIn("Think Before Coding", k.read_text(encoding="utf-8"))

    def test_agents_template_documents_rules(self) -> None:
        agents = (_ROOT / "template" / "web-vite-ts" / "AGENTS.md.template").read_text(encoding="utf-8")
        self.assertIn("karpathy-guidelines.mdc", agents)
        self.assertIn("user-project-standard.mdc", agents)
        self.assertIn("github-setup-offer.mdc", agents)
        self.assertIn("github-push-offer.mdc", agents)
        self.assertIn("GITHUB_SETUP_WALKTHROUGH.md", agents)
        self.assertIn("Cursor rules", agents)

    def test_github_setup_offer_rule_exists(self) -> None:
        rule = _ROOT / "template" / "web-vite-ts" / ".cursor" / "rules" / "github-setup-offer.mdc"
        self.assertTrue(rule.is_file(), rule)
        text = rule.read_text(encoding="utf-8")
        self.assertIn("alwaysApply: true", text)
        self.assertIn("YES", text)
        self.assertIn("NO", text)

    def test_github_push_offer_rule_exists(self) -> None:
        rule = _ROOT / "template" / "web-vite-ts" / ".cursor" / "rules" / "github-push-offer.mdc"
        self.assertTrue(rule.is_file(), rule)
        text = rule.read_text(encoding="utf-8")
        self.assertIn("alwaysApply: true", text)
        self.assertIn("commit and push", text)
        self.assertIn("origin", text)


class TestIndustryVersioningGuide(unittest.TestCase):
    def test_factory_guide_exists(self) -> None:
        guide = _ROOT / "INDUSTRY_STANDARD_VERSIONING.md"
        self.assertTrue(guide.is_file(), guide)


class TestGithubSetupWalkthrough(unittest.TestCase):
    def test_factory_walkthrough_exists_and_is_generic(self) -> None:
        path = _ROOT / "docs" / "GITHUB_SETUP_WALKTHROUGH.md"
        self.assertTrue(path.is_file(), path)
        text = path.read_text(encoding="utf-8")
        self.assertIn("YES", text)
        self.assertIn("NO", text)
        self.assertNotIn("kepasa", text.lower())
        self.assertNotIn("/home/", text)


class TestHandoffMessages(unittest.TestCase):
    def test_factory_handoff_doc_exists(self) -> None:
        path = _ROOT / "docs" / "HANDOFF_MESSAGES.md"
        self.assertTrue(path.is_file(), path)
        text = path.read_text(encoding="utf-8")
        self.assertIn("Beat A", text)
        self.assertIn("Beat B", text)
        self.assertIn("{{CHILD_FOLDER}}", text)
        self.assertIn("Copy", text)

    def test_github_setup_offer_points_at_handoff_doc(self) -> None:
        rule = _ROOT / "template" / "web-vite-ts" / ".cursor" / "rules" / "github-setup-offer.mdc"
        text = rule.read_text(encoding="utf-8")
        self.assertIn("HANDOFF_MESSAGES.md", text)
        self.assertIn("premium", text.lower())

    def test_bootstrap_copies_handoff_to_child_docs(self) -> None:
        src = inspect.getsource(b._materialize_project_tree)
        self.assertIn("HANDOFF_MESSAGES.md", src)
        self.assertIn("THIRD_PARTY_NOTICES.md", src)


class TestCopytreeIgnore(unittest.TestCase):
    def test_ignore_drops_artifacts(self) -> None:
        names = ["src", "node_modules", "package.json", "dist", ".git", "README.md"]
        ignored = set(b._ignore_copytree_artifacts("/fake", names))
        self.assertEqual(ignored, {"node_modules", "dist", ".git"})
        # dist-ssr is skipped when present
        names2 = ["a", "dist-ssr"]
        self.assertEqual(set(b._ignore_copytree_artifacts("/fake", names2)), {"dist-ssr"})


_SKIP_DIR_NAMES = {"node_modules", "dist", "dist-ssr", ".git", "__pycache__", "tests"}
_SCAN_SUFFIXES = {".md", ".mdc", ".py", ".yml", ".yaml", ".json", ".template", ".ts", ".tsx", ".html", ".sh"}
# Substrings that must not appear in committed factory sources (personal / machine-specific).
_FORBIDDEN_SUBSTRINGS = ("kepasa", "/home/")


class TestFactoryRepoPrivacy(unittest.TestCase):
    """Committed factory tree must stay generic — no usernames or home paths."""

    def _iter_scannable_files(self):
        for path in _ROOT.rglob("*"):
            if not path.is_file():
                continue
            if any(part in _SKIP_DIR_NAMES for part in path.parts):
                continue
            if path.suffix.lower() not in _SCAN_SUFFIXES and path.name not in {
                "package.json",
                "package-lock.json",
            }:
                continue
            if path.name == "package-lock.json":
                continue  # third-party metadata only; skip bulk scan
            yield path

    def test_no_personal_paths_or_usernames_in_factory_sources(self) -> None:
        violations: list[str] = []
        for path in self._iter_scannable_files():
            try:
                text = path.read_text(encoding="utf-8").lower()
            except (UnicodeDecodeError, OSError):
                continue
            rel = path.relative_to(_ROOT)
            for needle in _FORBIDDEN_SUBSTRINGS:
                if needle in text:
                    violations.append(f"{rel}: contains {needle!r}")
        self.assertEqual(violations, [], "\n".join(violations))


if __name__ == "__main__":
    unittest.main()
