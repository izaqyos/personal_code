import pytest

from github_approve_merge.actions import (
    EXIT_CODE_FAILURE,
    EXIT_CODE_SUCCESS,
    STATUS_TO_EXIT_CLASS,
    ExitClass,
    aggregate_exit_code,
)
from github_approve_merge.pr_state import PRState, StateFlag


class TestPRStateEnum:
    def test_has_all_required_members(self):
        # Spec §9 detection table rows.
        expected = {
            "MERGED", "CLOSED", "DRAFT", "LOCKED", "SELF_AUTHORED",
            "CONFLICT", "REQUIRED_FAILING", "REQUIRED_PENDING",
            "OPEN_MERGEABLE", "OPEN_APPROVABLE",
        }
        assert {m.name for m in PRState} == expected


class TestStateFlagEnum:
    def test_already_approved_present(self):
        assert StateFlag.ALREADY_APPROVED.name == "ALREADY_APPROVED"


class TestStatusExitClassMap:
    @pytest.mark.parametrize("status,cls", [
        ("done", ExitClass.SUCCESS),
        ("skipped-merged", ExitClass.SUCCESS),
        ("skipped-closed", ExitClass.WARN),
        ("skipped-draft", ExitClass.WARN),
        ("skipped-self", ExitClass.WARN),
        ("skipped-needs-more-approvals", ExitClass.WARN),
        ("failed-conflict", ExitClass.ERROR),
        ("failed-required-check", ExitClass.ERROR),
        ("failed-locked", ExitClass.ERROR),
        ("failed-interrupted", ExitClass.ERROR),
        ("failed-exception", ExitClass.ERROR),
    ])
    def test_known_statuses(self, status: str, cls: ExitClass):
        assert STATUS_TO_EXIT_CLASS[status] is cls


class TestAggregateExitCode:
    def test_all_success(self):
        assert aggregate_exit_code(["done", "done", "skipped-merged"]) == EXIT_CODE_SUCCESS

    def test_any_warn_means_failure(self):
        assert aggregate_exit_code(["done", "skipped-closed"]) == EXIT_CODE_FAILURE

    def test_any_error_means_failure(self):
        assert aggregate_exit_code(["done", "failed-conflict"]) == EXIT_CODE_FAILURE

    def test_empty_means_failure(self):
        # No PRs processed (e.g. all filtered out): treat as failure so caller notices.
        assert aggregate_exit_code([]) == EXIT_CODE_FAILURE
