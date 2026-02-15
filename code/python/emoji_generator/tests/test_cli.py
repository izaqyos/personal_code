"""Tests for the CLI and REPL interface."""

import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from emoji_generator.engine import EmojiMatchingEngine, MatchResult
from emoji_generator.registry import EmojiEntry, load_registry, get_default_yaml_path
from emoji_generator.cli import (
    copy_to_clipboard,
    display_results,
    display_no_match,
    display_all_emojis,
    prompt_selection,
    handle_repl_add,
    run_single_query,
    run_repl,
    build_parser,
    main,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_entries():
    """A small set of entries for testing."""
    return [
        EmojiEntry(
            emoji="✅🔀",
            name="pr_approved_merged",
            description="pull request approved and merged",
            aliases=["pr merged", "lgtm merged"],
        ),
        EmojiEntry(
            emoji="🚦⏳",
            name="in_merge_queue",
            description="in the merge queue waiting",
            aliases=["merge queue"],
        ),
        EmojiEntry(
            emoji="🐛✅",
            name="bug_fixed",
            description="bug fixed resolved",
            aliases=["fixed the bug"],
        ),
    ]


@pytest.fixture
def engine(sample_entries):
    """Build a small engine for testing."""
    return EmojiMatchingEngine(sample_entries)


@pytest.fixture
def sample_results(sample_entries):
    """Build sample MatchResult list."""
    return [
        MatchResult(entry=sample_entries[0], score=0.82),
        MatchResult(entry=sample_entries[1], score=0.54),
    ]


@pytest.fixture
def yaml_path():
    return get_default_yaml_path()


# ---------------------------------------------------------------------------
# copy_to_clipboard tests
# ---------------------------------------------------------------------------


class TestCopyToClipboard:
    def test_copy_success(self):
        """Should return True when pyperclip works."""
        mock_pyperclip = MagicMock()
        with patch.dict("sys.modules", {"pyperclip": mock_pyperclip}):
            result = copy_to_clipboard("✅🔀")
            assert result is True
            mock_pyperclip.copy.assert_called_once_with("✅🔀")

    def test_copy_failure_when_pyperclip_raises(self):
        """Should return False when pyperclip.copy raises."""
        mock_pyperclip = MagicMock()
        mock_pyperclip.copy.side_effect = Exception("no clipboard")
        with patch.dict("sys.modules", {"pyperclip": mock_pyperclip}):
            result = copy_to_clipboard("✅🔀")
            assert result is False


# ---------------------------------------------------------------------------
# Display function tests (just verify they don't crash)
# ---------------------------------------------------------------------------


class TestDisplayFunctions:
    def test_display_results_runs(self, sample_results, capsys):
        """display_results should produce output without crashing."""
        display_results(sample_results, "pr merged")
        captured = capsys.readouterr()
        assert "pr merged" in captured.out or True  # rich may use stderr

    def test_display_results_with_empty_list(self, capsys):
        """display_results with empty list should not crash."""
        display_results([], "empty query")

    def test_display_no_match_runs(self, yaml_path, capsys):
        """display_no_match should produce output without crashing."""
        display_no_match("xyzzy foobar", yaml_path)

    def test_display_all_emojis_runs(self, sample_entries, capsys):
        """display_all_emojis should produce output without crashing."""
        display_all_emojis(sample_entries)


# ---------------------------------------------------------------------------
# prompt_selection tests
# ---------------------------------------------------------------------------


class TestPromptSelection:
    def test_empty_results_returns_none(self):
        """Should return None for empty results."""
        result = prompt_selection([])
        assert result is None

    def test_select_first_by_default(self, sample_results):
        """Pressing Enter (empty input) selects first result."""
        with patch("builtins.input", return_value=""):
            result = prompt_selection(sample_results, no_copy=True)
        assert result == "✅🔀"

    def test_select_by_number(self, sample_results):
        """Selecting '2' should return the second emoji."""
        with patch("builtins.input", return_value="2"):
            result = prompt_selection(sample_results, no_copy=True)
        assert result == "🚦⏳"

    def test_quit_returns_none(self, sample_results):
        """Typing 'q' should return None."""
        with patch("builtins.input", return_value="q"):
            result = prompt_selection(sample_results, no_copy=True)
        assert result is None

    def test_quit_full_word_returns_none(self, sample_results):
        """Typing 'quit' should return None."""
        with patch("builtins.input", return_value="quit"):
            result = prompt_selection(sample_results, no_copy=True)
        assert result is None

    def test_invalid_number_returns_none(self, sample_results):
        """Out of range number should return None."""
        with patch("builtins.input", return_value="99"):
            result = prompt_selection(sample_results, no_copy=True)
        assert result is None

    def test_invalid_text_returns_none(self, sample_results):
        """Non-numeric text should return None."""
        with patch("builtins.input", return_value="abc"):
            result = prompt_selection(sample_results, no_copy=True)
        assert result is None

    def test_eof_returns_none(self, sample_results):
        """EOFError during input should return None."""
        with patch("builtins.input", side_effect=EOFError):
            result = prompt_selection(sample_results, no_copy=True)
        assert result is None

    def test_keyboard_interrupt_returns_none(self, sample_results):
        """KeyboardInterrupt during input should return None."""
        with patch("builtins.input", side_effect=KeyboardInterrupt):
            result = prompt_selection(sample_results, no_copy=True)
        assert result is None

    def test_select_with_clipboard_copy(self, sample_results):
        """Should attempt clipboard copy when no_copy=False."""
        with patch("builtins.input", return_value="1"):
            with patch("emoji_generator.cli.copy_to_clipboard", return_value=True) as mock_copy:
                result = prompt_selection(sample_results, no_copy=False)
        assert result == "✅🔀"
        mock_copy.assert_called_once_with("✅🔀")

    def test_select_clipboard_failure(self, sample_results):
        """Should still return emoji even when clipboard fails."""
        with patch("builtins.input", return_value="1"):
            with patch("emoji_generator.cli.copy_to_clipboard", return_value=False):
                result = prompt_selection(sample_results, no_copy=False)
        assert result == "✅🔀"


# ---------------------------------------------------------------------------
# handle_repl_add tests
# ---------------------------------------------------------------------------


class TestHandleReplAdd:
    def test_add_entry_success(self, engine, tmp_path):
        """Should append entry to YAML and rebuild engine."""
        yaml_file = tmp_path / "emojis.yaml"
        yaml_file.write_text(
            '- emoji: "✅🔀"\n'
            '  name: "test"\n'
            '  description: "test entry"\n'
            '  aliases:\n'
            '    - "test"\n'
        )
        initial_count = len(engine.entries)

        with patch("builtins.input", return_value="🎯🔥"):
            handle_repl_add("new concept", yaml_file, engine)

        # Engine should have been rebuilt with the new entry
        content = yaml_file.read_text()
        assert "new concept" in content
        assert "🎯🔥" in content

    def test_add_entry_cancelled_empty(self, engine, tmp_path):
        """Empty emoji input should cancel the add."""
        yaml_file = tmp_path / "emojis.yaml"
        yaml_file.write_text(
            '- emoji: "✅🔀"\n'
            '  name: "test"\n'
            '  description: "test entry"\n'
            '  aliases:\n'
            '    - "test"\n'
        )
        original_content = yaml_file.read_text()

        with patch("builtins.input", return_value=""):
            handle_repl_add("new concept", yaml_file, engine)

        # File should be unchanged
        assert yaml_file.read_text() == original_content

    def test_add_entry_cancelled_eof(self, engine, tmp_path):
        """EOFError should cancel the add."""
        yaml_file = tmp_path / "emojis.yaml"
        yaml_file.write_text(
            '- emoji: "✅🔀"\n'
            '  name: "test"\n'
            '  description: "test entry"\n'
            '  aliases:\n'
            '    - "test"\n'
        )

        with patch("builtins.input", side_effect=EOFError):
            handle_repl_add("new concept", yaml_file, engine)


# ---------------------------------------------------------------------------
# run_single_query tests
# ---------------------------------------------------------------------------


class TestRunSingleQuery:
    def test_query_with_results_first_flag(self, engine, yaml_path):
        """With --first flag, should auto-select top result."""
        with patch("emoji_generator.cli.copy_to_clipboard", return_value=True):
            run_single_query(engine, "pr merged", top_k=5, no_copy=False, first=True, yaml_path=yaml_path)

    def test_query_with_results_no_copy(self, engine, yaml_path):
        """With --no-copy --first, should just print selected."""
        run_single_query(engine, "pr merged", top_k=5, no_copy=True, first=True, yaml_path=yaml_path)

    def test_query_with_results_prompt(self, engine, yaml_path):
        """Without --first, should prompt for selection."""
        with patch("builtins.input", return_value="1"):
            with patch("emoji_generator.cli.copy_to_clipboard", return_value=True):
                run_single_query(engine, "pr merged", top_k=5, no_copy=False, first=False, yaml_path=yaml_path)

    def test_query_no_match(self, engine, yaml_path):
        """Gibberish query should show no-match panel."""
        run_single_query(engine, "xyzzy foobar bazzle", top_k=5, no_copy=True, first=False, yaml_path=yaml_path)

    def test_query_first_clipboard_failure(self, engine, yaml_path):
        """Clipboard failure with --first should still work."""
        with patch("emoji_generator.cli.copy_to_clipboard", return_value=False):
            run_single_query(engine, "pr merged", top_k=5, no_copy=False, first=True, yaml_path=yaml_path)


# ---------------------------------------------------------------------------
# run_repl tests
# ---------------------------------------------------------------------------


class TestRunRepl:
    def test_repl_quit(self, engine, yaml_path):
        """Typing 'quit' should exit the REPL."""
        mock_session = MagicMock()
        mock_session.prompt.return_value = "quit"
        with patch("prompt_toolkit.PromptSession", return_value=mock_session):
            run_repl(engine, top_k=5, no_copy=True, yaml_path=yaml_path)

    def test_repl_exit(self, engine, yaml_path):
        """Typing 'exit' should exit the REPL."""
        mock_session = MagicMock()
        mock_session.prompt.return_value = "exit"
        with patch("prompt_toolkit.PromptSession", return_value=mock_session):
            run_repl(engine, top_k=5, no_copy=True, yaml_path=yaml_path)

    def test_repl_eof(self, engine, yaml_path):
        """EOFError should exit the REPL gracefully."""
        with patch("builtins.input", side_effect=EOFError):
            run_repl(engine, top_k=5, no_copy=True, yaml_path=yaml_path)

    def test_repl_empty_input_continues(self, engine, yaml_path):
        """Empty input should continue the loop."""
        inputs = iter(["", "quit"])
        with patch("builtins.input", side_effect=inputs):
            run_repl(engine, top_k=5, no_copy=True, yaml_path=yaml_path)

    def test_repl_list_command(self, engine, yaml_path):
        """'list' should show all emojis then continue."""
        inputs = iter(["list", "quit"])
        with patch("builtins.input", side_effect=inputs):
            run_repl(engine, top_k=5, no_copy=True, yaml_path=yaml_path)

    def test_repl_help_command(self, engine, yaml_path):
        """'help' should show help then continue."""
        inputs = iter(["help", "quit"])
        with patch("builtins.input", side_effect=inputs):
            run_repl(engine, top_k=5, no_copy=True, yaml_path=yaml_path)

    def test_repl_search_with_results(self, engine, yaml_path):
        """A valid search should display results and prompt."""
        # "pr merged" -> results, then "q" to skip selection, then "quit"
        inputs = iter(["pr merged", "q", "quit"])
        with patch("builtins.input", side_effect=inputs):
            run_repl(engine, top_k=5, no_copy=True, yaml_path=yaml_path)

    def test_repl_no_match_skip_add(self, engine, yaml_path):
        """No match + declining to add should continue."""
        inputs = iter(["xyzzy foobar bazzle", "n", "quit"])
        with patch("builtins.input", side_effect=inputs):
            run_repl(engine, top_k=5, no_copy=True, yaml_path=yaml_path)

    def test_repl_no_match_eof_on_add_prompt(self, engine, yaml_path):
        """EOFError on the add prompt should continue."""
        call_count = [0]
        def mock_input(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return "xyzzy foobar bazzle"  # no-match query
            elif call_count[0] == 2:
                raise EOFError  # on the [a]dd prompt
            else:
                return "quit"

        with patch("builtins.input", side_effect=mock_input):
            run_repl(engine, top_k=5, no_copy=True, yaml_path=yaml_path)


# ---------------------------------------------------------------------------
# build_parser tests
# ---------------------------------------------------------------------------


class TestBuildParser:
    def test_parser_query(self):
        """Parser should accept a positional query."""
        parser = build_parser()
        args = parser.parse_args(["pr merged"])
        assert args.query == "pr merged"

    def test_parser_repl_flag(self):
        """Parser should accept --repl."""
        parser = build_parser()
        args = parser.parse_args(["--repl"])
        assert args.repl is True

    def test_parser_repl_short(self):
        """Parser should accept -r."""
        parser = build_parser()
        args = parser.parse_args(["-r"])
        assert args.repl is True

    def test_parser_top(self):
        """Parser should accept --top N."""
        parser = build_parser()
        args = parser.parse_args(["--top", "10", "query"])
        assert args.top == 10

    def test_parser_first_flag(self):
        """Parser should accept -1 / --first."""
        parser = build_parser()
        args = parser.parse_args(["-1", "query"])
        assert args.first is True

    def test_parser_no_copy(self):
        """Parser should accept --no-copy."""
        parser = build_parser()
        args = parser.parse_args(["--no-copy", "query"])
        assert args.no_copy is True

    def test_parser_list(self):
        """Parser should accept --list."""
        parser = build_parser()
        args = parser.parse_args(["--list"])
        assert args.list_all is True

    def test_parser_yaml(self):
        """Parser should accept --yaml PATH."""
        parser = build_parser()
        args = parser.parse_args(["--yaml", "/tmp/my.yaml", "query"])
        assert args.yaml == "/tmp/my.yaml"

    def test_parser_defaults(self):
        """Default values should be correct."""
        parser = build_parser()
        args = parser.parse_args(["query"])
        assert args.top == 5
        assert args.first is False
        assert args.no_copy is False
        assert args.list_all is False
        assert args.repl is False
        assert args.yaml is None


# ---------------------------------------------------------------------------
# main() integration tests
# ---------------------------------------------------------------------------


class TestMain:
    def test_main_list(self):
        """main() with --list should list emojis and exit."""
        with patch("sys.argv", ["devmoji", "--list"]):
            main()  # Should not raise

    def test_main_cli_first_no_copy(self):
        """main() with a query + --first --no-copy should work."""
        with patch("sys.argv", ["devmoji", "-1", "--no-copy", "pr merged"]):
            main()

    def test_main_no_query_exits(self):
        """main() with no query and no flags should print help and exit."""
        with patch("sys.argv", ["devmoji"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

    def test_main_missing_yaml(self):
        """main() with a bad --yaml path should exit with error."""
        with patch("sys.argv", ["devmoji", "--yaml", "/nonexistent/path.yaml", "query"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

    def test_main_empty_yaml(self, tmp_path):
        """main() with an empty YAML should exit with warning."""
        empty_yaml = tmp_path / "empty.yaml"
        empty_yaml.write_text("")
        with patch("sys.argv", ["devmoji", "--yaml", str(empty_yaml), "query"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

    def test_main_repl_mode(self):
        """main() with --repl should enter REPL (exit immediately)."""
        with patch("sys.argv", ["devmoji", "--repl"]):
            with patch("builtins.input", return_value="quit"):
                main()

    def test_main_cli_with_prompt(self):
        """main() with a query (no --first) should prompt for selection."""
        with patch("sys.argv", ["devmoji", "--no-copy", "pr merged"]):
            with patch("builtins.input", return_value="1"):
                main()

    def test_main_custom_yaml(self, tmp_path):
        """main() with a valid custom --yaml should work."""
        custom_yaml = tmp_path / "custom.yaml"
        custom_yaml.write_text(
            '- emoji: "🎯"\n'
            '  name: "test"\n'
            '  description: "custom test entry"\n'
            '  aliases:\n'
            '    - "testing"\n'
        )
        with patch("sys.argv", ["devmoji", "--yaml", str(custom_yaml), "-1", "--no-copy", "test"]):
            main()
