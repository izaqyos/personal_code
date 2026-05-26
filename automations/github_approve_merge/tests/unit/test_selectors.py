import re

from github_approve_merge.pages import selectors as S


class TestSelectors:
    def test_constants_present(self):
        # Spec §9 selectors live in this module as named constants.
        for name in (
            "APPROVE_RADIO_VALUE",
            "SUBMIT_REVIEW_NAME",
            "MERGE_BUTTON_NAME",
            "CONFIRM_MERGE_NAME",
            "MERGE_WHEN_READY_NAME",
            "ENABLE_AUTO_MERGE_NAME",
            "USER_LOGIN_META",
            "STATE_BADGE_MERGED",
            "STATE_BADGE_CLOSED",
            "DRAFT_BADGE_TEXT",
            "LOCKED_NOTICE_TEXT",
            "CONFLICT_NOTICE_TEXT",
            "REQUIRED_STATUS_TEXT",
            "REVIEWERS_PANEL_APPROVED_LABEL",
            "PR_AUTHOR_LINK_CSS",
        ):
            assert hasattr(S, name), f"missing selector constant {name}"

    def test_merge_button_pattern_covers_all_methods(self):
        # GitHub renames the primary button based on merge method.
        for label in ("Merge pull request", "Squash and merge", "Rebase and merge",
                      "Create a merge commit"):
            assert S.MERGE_BUTTON_NAME.fullmatch(label), label

    def test_confirm_merge_pattern_covers_all_methods(self):
        for label in ("Confirm merge", "Confirm squash and merge", "Confirm rebase and merge"):
            assert S.CONFIRM_MERGE_NAME.fullmatch(label), label

    def test_merge_when_ready_exact(self):
        assert S.MERGE_WHEN_READY_NAME.fullmatch("Merge when ready")
        assert not S.MERGE_WHEN_READY_NAME.fullmatch("Merge pull request")

    def test_patterns_are_compiled_regex(self):
        for attr in (S.MERGE_BUTTON_NAME, S.CONFIRM_MERGE_NAME,
                     S.MERGE_WHEN_READY_NAME, S.ENABLE_AUTO_MERGE_NAME,
                     S.SUBMIT_REVIEW_NAME):
            assert isinstance(attr, re.Pattern), attr
