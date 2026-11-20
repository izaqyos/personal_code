import pytest

from aireview.globs import match, match_any


@pytest.mark.parametrize(
    "path,pattern,expected",
    [
        ("src/routes/a.ts", "src/routes/**", True),
        ("src/routes/deep/a.ts", "src/routes/**", True),
        ("src/router.ts", "src/routes/**", False),
        ("src/a.ts", "**/*.ts", True),
        ("a.ts", "**/*.ts", True),
        ("a.tsx", "**/*.{ts,tsx}", True),
        ("a.js", "**/*.{ts,tsx}", False),
        ("migrations/002.sql", "migrations/**", True),
        ("db/migrations/002.sql", "**/migrations/**", True),
        ("src/app.ts", "src/app.ts", True),
        ("src/app.tsx", "src/app.ts", False),
        ("x/y/package-lock.json", "package-lock.json", True),  # no slash => any depth
        ("src/a.test.ts", "**/*.test.*", True),
        ("src/a.ts", "src/*.ts", True),
        ("src/x/a.ts", "src/*.ts", False),
        ("src/a1.ts", "src/a?.ts", True),
        ("anything/at/all", "*", True),
    ],
)
def test_match(path, pattern, expected):
    assert match(path, pattern) is expected


def test_match_any():
    assert match_any("tests/a.ts", ["src/**", "tests/**"])
    assert not match_any("docs/a.md", ["src/**", "tests/**"])
