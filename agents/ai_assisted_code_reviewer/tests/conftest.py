from __future__ import annotations

import importlib.util
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "demo"
PAYLOAD = ROOT / "src" / "aireview" / "payload"


def _load_setup():
    spec = importlib.util.spec_from_file_location("setup_demo_repo", DEMO / "setup_demo_repo.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="session")
def demo_repo_template(tmp_path_factory) -> Path:
    if shutil.which("git") is None:
        pytest.skip("git not installed")
    return _load_setup().setup(tmp_path_factory.mktemp("demo") / "repo")


@pytest.fixture
def demo_repo(demo_repo_template, tmp_path) -> Path:
    """A fresh copy per test so tests may mutate it."""
    dst = tmp_path / "repo"
    shutil.copytree(demo_repo_template, dst, symlinks=True)
    return dst


@pytest.fixture
def git_repo(tmp_path) -> Path:
    repo = tmp_path / "g"
    repo.mkdir()
    for args in (
        ["init", "-q", "-b", "main"],
        ["config", "user.email", "t@t"],
        ["config", "user.name", "t"],
        ["config", "commit.gpgsign", "false"],
    ):
        subprocess.run(["git", *args], cwd=repo, check=True)
    return repo


def commit(repo: Path, msg: str = "c") -> None:
    subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "add", "-A"], cwd=repo, check=True)
    subprocess.run(
        ["git", "-c", "core.hooksPath=/dev/null", "commit", "-q", "-m", msg],
        cwd=repo,
        check=True,
    )


# Key-shaped fixtures are assembled at runtime so secret scanners on this repo stay quiet.
FAKE_STRIPE = "sk_" + "live_abcdefghijklmnopqrstuv"
FAKE_AWS = "AKIA" + "ABCDEFGHIJKLMNOP"
FAKE_GH = "ghp" + "_abcdefghijklmnopqrstuvwxyz0123456789"
FAKE_PEM = "-----BEGIN RSA " + "PRIVATE KEY-----"

SAMPLE_DIFF = """\
diff --git a/src/app.ts b/src/app.ts
index 1111111..2222222 100644
--- a/src/app.ts
+++ b/src/app.ts
@@ -10,4 +10,5 @@ app.get("/healthz", (_req, res) => res.json({ ok: true }));

 app.use("/users", requireAuth, usersRouter);
+app.use("/invoices", invoicesRouter);

 app.use(errorHandler);
diff --git a/src/routes/invoices.ts b/src/routes/invoices.ts
new file mode 100644
index 0000000..3333333
--- /dev/null
+++ b/src/routes/invoices.ts
@@ -0,0 +1,3 @@
+import { Router } from "express";
+export const r = Router();
+const key = "__FAKE_STRIPE__";
diff --git a/old.txt b/old.txt
deleted file mode 100644
index 4444444..0000000
--- a/old.txt
+++ /dev/null
@@ -1,2 +0,0 @@
-gone
-gone too
diff --git a/src/a.ts b/src/b.ts
similarity index 90%
rename from src/a.ts
rename to src/b.ts
index 5555555..6666666 100644
--- a/src/a.ts
+++ b/src/b.ts
@@ -1,3 +1,3 @@
 const a = 1;
-const b = 2;
+const b = 3;
 const c = 4;
diff --git a/logo.png b/logo.png
new file mode 100644
index 0000000..7777777
Binary files /dev/null and b/logo.png differ
""".replace("__FAKE_STRIPE__", FAKE_STRIPE)
