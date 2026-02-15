"""Tests for the TF-IDF matching engine."""

import pytest

from emoji_generator.registry import load_registry, EmojiEntry, generate_yaml_snippet, append_entry_to_yaml
from emoji_generator.engine import EmojiMatchingEngine, MIN_CONFIDENCE


@pytest.fixture
def engine():
    """Build an engine from the default registry."""
    entries = load_registry()
    return EmojiMatchingEngine(entries)


@pytest.fixture
def entries():
    """Load the default registry."""
    return load_registry()


# ---------------------------------------------------------------------------
# Registry tests
# ---------------------------------------------------------------------------


class TestRegistry:
    def test_loads_entries(self, entries):
        """Registry should load a non-empty list of entries."""
        assert len(entries) > 0

    def test_entries_have_required_fields(self, entries):
        """Every entry must have emoji, name, description."""
        for entry in entries:
            assert entry.emoji, f"Entry {entry.name} has no emoji"
            assert entry.name, "Entry has no name"
            assert entry.description, f"Entry {entry.name} has no description"

    def test_searchable_text_includes_description(self, entries):
        """Searchable text should contain the description."""
        for entry in entries:
            assert entry.description in entry.searchable_text

    def test_searchable_text_includes_aliases(self, entries):
        """Searchable text should contain all aliases."""
        for entry in entries:
            for alias in entry.aliases:
                assert alias in entry.searchable_text

    def test_generate_yaml_snippet(self):
        """YAML snippet generator should produce valid output."""
        snippet = generate_yaml_snippet("deploy canary to staging")
        assert "PUT_EMOJI_HERE" in snippet
        assert "deploy_canary_to_staging" in snippet
        assert "deploy canary to staging" in snippet

    def test_load_empty_yaml(self, tmp_path):
        """Loading an empty YAML file should return empty list."""
        empty_yaml = tmp_path / "empty.yaml"
        empty_yaml.write_text("")
        result = load_registry(empty_yaml)
        assert result == []

    def test_append_entry_to_yaml(self, tmp_path):
        """append_entry_to_yaml should add a valid entry to the file."""
        yaml_file = tmp_path / "emojis.yaml"
        yaml_file.write_text(
            '- emoji: "✅🔀"\n'
            '  name: "test"\n'
            '  description: "test entry"\n'
            '  aliases:\n'
            '    - "test"\n'
        )
        append_entry_to_yaml(yaml_file, "🎯🔥", "new custom concept")
        content = yaml_file.read_text()
        assert "🎯🔥" in content
        assert "new_custom_concept" in content
        assert "new custom concept" in content

        # Verify it's still valid YAML that can be loaded
        entries = load_registry(yaml_file)
        assert len(entries) == 2
        assert entries[1].emoji == "🎯🔥"


# ---------------------------------------------------------------------------
# Engine matching tests
# ---------------------------------------------------------------------------


class TestEngineMatching:
    """Test that known queries match expected emoji entries."""

    def test_pr_merged_matches(self, engine):
        """'pr merged' should match the pr_approved_merged entry."""
        results = engine.search("pr merged")
        assert len(results) > 0
        assert results[0].entry.name == "pr_approved_merged"

    def test_merge_queue_matches(self, engine):
        """'merge queue' should match the in_merge_queue entry."""
        results = engine.search("merge queue")
        assert len(results) > 0
        assert results[0].entry.name == "in_merge_queue"

    def test_looking_at_it_matches(self, engine):
        """'looking at this issue' should match the looking_at_it entry."""
        results = engine.search("looking at this issue")
        assert len(results) > 0
        assert results[0].entry.name == "looking_at_it"

    def test_will_get_back_matches(self, engine):
        """'will get back to you' should match the will_get_back entry."""
        results = engine.search("will get back to you asap")
        assert len(results) > 0
        assert results[0].entry.name == "will_get_back"

    def test_deploying_matches(self, engine):
        """'deploying to prod' should match deploying entry."""
        results = engine.search("deploying to prod")
        assert len(results) > 0
        assert results[0].entry.name == "deploying"

    def test_hotfix_matches(self, engine):
        """'emergency hotfix' should match hotfix entry."""
        results = engine.search("emergency hotfix")
        assert len(results) > 0
        assert results[0].entry.name == "hotfix"

    def test_rollback_matches(self, engine):
        """'rolling back deployment' should match rollback entry."""
        results = engine.search("rolling back deployment")
        assert len(results) > 0
        assert results[0].entry.name == "rollback"

    def test_bug_found_matches(self, engine):
        """'found a bug' should match bug_found entry."""
        results = engine.search("found a bug")
        assert len(results) > 0
        assert results[0].entry.name == "bug_found"

    def test_ooo_matches(self, engine):
        """'out of office' should match out_of_office entry."""
        results = engine.search("out of office")
        assert len(results) > 0
        assert results[0].entry.name == "out_of_office"

    def test_changes_requested_matches(self, engine):
        """'changes requested' should match changes_requested entry."""
        results = engine.search("changes requested on my pr")
        assert len(results) > 0
        assert results[0].entry.name == "changes_requested"


# ---------------------------------------------------------------------------
# Engine behavior tests
# ---------------------------------------------------------------------------


class TestEngineBehavior:
    def test_returns_top_k_results(self, engine):
        """Should return at most top_k results."""
        results = engine.search("merge", top_k=3)
        assert len(results) <= 3

    def test_results_sorted_by_score(self, engine):
        """Results should be sorted by descending score."""
        results = engine.search("deploy")
        for i in range(len(results) - 1):
            assert results[i].score >= results[i + 1].score

    def test_scores_between_0_and_1(self, engine):
        """All scores should be between 0.0 and 1.0."""
        results = engine.search("pull request review")
        for result in results:
            assert 0.0 <= result.score <= 1.0

    def test_no_match_returns_empty(self, engine):
        """Gibberish query should return empty results."""
        results = engine.search("xyzzy foobar bazzle")
        assert len(results) == 0

    def test_rebuild_works(self, engine):
        """Engine should work after rebuild with new entries."""
        custom_entries = [
            EmojiEntry(
                emoji="🎯🔥",
                name="custom_test",
                description="custom test entry for validation",
                aliases=["test validation"],
            )
        ]
        engine.rebuild(custom_entries)
        results = engine.search("custom test validation")
        assert len(results) > 0
        assert results[0].entry.name == "custom_test"
