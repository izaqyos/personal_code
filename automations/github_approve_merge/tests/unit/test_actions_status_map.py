from github_approve_merge.actions import (
    STATUS_TO_EXIT_CLASS, ExitClass, aggregate_exit_code,
    EXIT_CODE_SUCCESS, EXIT_CODE_FAILURE,
)


def test_new_statuses_have_exit_classes():
    assert STATUS_TO_EXIT_CLASS["done"] is ExitClass.SUCCESS
    assert STATUS_TO_EXIT_CLASS["queued"] is ExitClass.SUCCESS
    assert STATUS_TO_EXIT_CLASS["would-merge"] is ExitClass.SUCCESS
    assert STATUS_TO_EXIT_CLASS["skipped-merged"] is ExitClass.SUCCESS
    assert STATUS_TO_EXIT_CLASS["cancelled"] is ExitClass.WARN
    assert STATUS_TO_EXIT_CLASS["failed-auth"] is ExitClass.ERROR
    assert STATUS_TO_EXIT_CLASS["failed-not-found"] is ExitClass.ERROR


def test_aggregate_success_only_when_all_success():
    assert aggregate_exit_code(["done", "queued", "skipped-merged"]) == EXIT_CODE_SUCCESS
    assert aggregate_exit_code(["done", "cancelled"]) == EXIT_CODE_FAILURE
