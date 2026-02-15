"""Tests for the two-stage matching engine (LingoLookup + TF-IDF)."""

import pytest

from emoji_generator.registry import load_registry, EmojiEntry, generate_yaml_snippet, append_entry_to_yaml
from emoji_generator.engine import (
    EmojiMatchingEngine,
    LingoLookup,
    TfidfEngine,
    MIN_CONFIDENCE,
    FUZZY_THRESHOLD,
)


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
        # Use a longer query that falls through to TF-IDF and returns
        # multiple results (short "deploy" hits lingo -> single result).
        results = engine.search("pull request code")
        assert len(results) >= 2, "Need multiple results to test sorting"
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


# ---------------------------------------------------------------------------
# Stage 1: LingoLookup tests
# ---------------------------------------------------------------------------


@pytest.fixture
def lingo_entries():
    """Small set of entries for focused lingo tests."""
    return [
        EmojiEntry(
            emoji="🫡",
            name="on_it",
            description="on it acknowledged working on it",
            aliases=["on it", "ack", "acknowledged", "got it", "roger that"],
        ),
        EmojiEntry(
            emoji="👍",
            name="lgtm",
            description="looks good to me approved",
            aliases=["lgtm", "looks good", "looks good to me", "ship it", "approved"],
        ),
        EmojiEntry(
            emoji="🏖️",
            name="out_of_office",
            description="out of office away vacation",
            aliases=["ooo", "out of office", "afk", "away"],
        ),
        EmojiEntry(
            emoji="🚧",
            name="wip",
            description="work in progress still working",
            aliases=["wip", "work in progress", "still working", "not done yet"],
        ),
    ]


@pytest.fixture
def lingo(lingo_entries):
    """Build a LingoLookup from the focused entries."""
    return LingoLookup(lingo_entries)


class TestLingoLookupExactMatch:
    """Test Stage 1 exact alias matching."""

    def test_exact_alias_match(self, lingo):
        """Exact alias text should produce a score of 1.0."""
        results = lingo.search("on it")
        assert len(results) == 1
        assert results[0].entry.name == "on_it"
        assert results[0].score == 1.0

    def test_exact_alias_case_insensitive(self, lingo):
        """Aliases should match case-insensitively."""
        results = lingo.search("LGTM")
        assert len(results) == 1
        assert results[0].entry.name == "lgtm"

    def test_exact_alias_whitespace_stripped(self, lingo):
        """Leading/trailing whitespace should be ignored."""
        results = lingo.search("  ooo  ")
        assert len(results) == 1
        assert results[0].entry.name == "out_of_office"

    def test_exact_multi_word_alias(self, lingo):
        """Multi-word aliases like 'looks good to me' should match exactly."""
        results = lingo.search("looks good to me")
        assert len(results) == 1
        assert results[0].entry.name == "lgtm"

    def test_exact_alias_short_abbreviation(self, lingo):
        """Short abbreviations like 'ack', 'wip', 'afk' should match."""
        for query, expected in [("ack", "on_it"), ("wip", "wip"), ("afk", "out_of_office")]:
            results = lingo.search(query)
            assert len(results) == 1, f"Expected 1 result for '{query}', got {len(results)}"
            assert results[0].entry.name == expected, f"'{query}' matched {results[0].entry.name}"

    def test_description_also_indexed(self, lingo):
        """Entry descriptions should also be searchable as aliases."""
        results = lingo.search("looks good to me approved")
        assert len(results) == 1
        assert results[0].entry.name == "lgtm"


class TestLingoLookupFuzzyMatch:
    """Test Stage 1 fuzzy (Levenshtein) matching for typos."""

    def test_typo_in_alias(self, lingo):
        """Close typos like 'roger tht' should fuzzy-match 'roger that'."""
        results = lingo.search("roger tht")
        assert len(results) >= 1
        assert results[0].entry.name == "on_it"
        assert results[0].score < 1.0  # fuzzy, not exact

    def test_typo_in_longer_alias(self, lingo):
        """Typos in longer aliases should still match if above threshold."""
        results = lingo.search("ship ti")  # typo for "ship it"
        assert len(results) >= 1
        assert results[0].entry.name == "lgtm"

    def test_no_match_for_distant_string(self, lingo):
        """A string very different from all aliases should return empty."""
        results = lingo.search("xyzzy foobar bazzle")
        assert len(results) == 0

    def test_fuzzy_scores_below_1(self, lingo):
        """Fuzzy match scores should be between 0 and 1, exclusive of 1.0."""
        # "roger tht" is close enough to "roger that" to trigger fuzzy match
        # but not identical, so score should be < 1.0
        results = lingo.search("roger tht")
        assert len(results) >= 1
        assert 0.0 < results[0].score < 1.0

    def test_fuzzy_deduplication(self, lingo):
        """An entry with multiple close-scoring aliases shouldn't appear twice."""
        # "looks good" and "looks good to me" could both fuzzy-match, but
        # only one result for the entry should appear.
        results = lingo.search("looks good")
        entry_names = [r.entry.name for r in results]
        assert len(entry_names) == len(set(entry_names)), "Duplicate entries in results"


class TestLingoLookupRebuild:
    """Test that LingoLookup can be rebuilt with new entries."""

    def test_rebuild_adds_new_aliases(self, lingo, lingo_entries):
        """After rebuild with additional entries, new aliases should match."""
        new_entries = lingo_entries + [
            EmojiEntry(
                emoji="🧹",
                name="cleanup",
                description="code cleanup refactoring",
                aliases=["cleanup", "refactor"],
            )
        ]
        lingo.rebuild(new_entries)
        results = lingo.search("cleanup")
        assert len(results) == 1
        assert results[0].entry.name == "cleanup"


# ---------------------------------------------------------------------------
# Two-stage pipeline integration tests
# ---------------------------------------------------------------------------


class TestTwoStagePipeline:
    """Test that the two-stage pipeline routes queries correctly."""

    def test_on_it_resolved_by_lingo(self, engine):
        """'on it' -- the original problem -- should now match via lingo."""
        results = engine.search("on it")
        assert len(results) > 0
        assert results[0].entry.name == "on_it"

    def test_lgtm_resolved_by_lingo(self, engine):
        """'lgtm' should match via exact alias lookup."""
        results = engine.search("lgtm")
        assert len(results) > 0
        # In the real YAML, "lgtm" is an alias of pr_approved
        assert results[0].entry.name == "pr_approved"

    def test_ooo_resolved_by_lingo(self, engine):
        """'ooo' should match via lingo."""
        results = engine.search("ooo")
        assert len(results) > 0
        assert results[0].entry.name == "out_of_office"

    def test_wip_resolved_by_lingo(self, engine):
        """'wip' should match via lingo."""
        results = engine.search("wip")
        assert len(results) > 0
        assert results[0].entry.name == "work_in_progress"

    def test_natural_language_falls_through_to_tfidf(self, engine):
        """Longer natural language should be handled by TF-IDF."""
        results = engine.search("the pull request was approved and merged")
        assert len(results) > 0
        assert results[0].entry.name == "pr_approved_merged"

    def test_kudos_resolved_by_lingo(self, engine):
        """'kudos' should match via exact alias."""
        results = engine.search("kudos")
        assert len(results) > 0
        assert results[0].entry.name == "kudos"

    def test_great_job_resolved_by_lingo(self, engine):
        """'great job' should match via exact alias."""
        results = engine.search("great job")
        assert len(results) > 0
        assert results[0].entry.name == "great_job"
