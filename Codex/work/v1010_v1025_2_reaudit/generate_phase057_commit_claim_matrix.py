"""Map Phase 057 commit-subject scope claims to actual first-parent patches."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
REPO_ROOT = Path(__file__).resolve().parents[3]
GENEALOGY_PATH = (
    REPO_ROOT / "Codex/results/PHASE_057_GIT_DOCUMENT_GENEALOGY.json"
)
OUTPUT_PATH = REPO_ROOT / "Codex/results/PHASE_057_COMMIT_CLAIM_MATRIX.json"

CLAIM_PATTERNS = {
    "THEORY_TEXT": re.compile(
        r"(?i)(?:문건|본문|이론|수식|chapter|ch[123]|부록|저작|latex|tex)"
    ),
    "CODE": re.compile(r"(?i)(?:\bcode\b|코드|구현|backend|kernel|api)"),
    "TEST_OR_GATE": re.compile(
        r"(?i)(?:test|테스트|검증|게이트|회귀|PASS|GREEN|bit[- ]?exact)"
    ),
    "BUILD_OR_PDF": re.compile(r"(?i)(?:build|빌드|pdf|\d+p\b)"),
    "PLAN": re.compile(r"(?i)(?:plan|계획|기획|브리핑|brief)"),
    "HANDOVER": re.compile(r"(?i)(?:handover|인계)"),
    "INDEX": re.compile(r"(?i)(?:\bindex\b|색인)"),
    "LEDGER_OR_LOG": re.compile(r"(?i)(?:ledger|원장|log|로그)"),
    "DATA_OR_FIT": re.compile(r"(?i)(?:data|데이터|실측|fit|피팅|R²|BIC)"),
    "REFERENCE": re.compile(r"(?i)(?:reference|citation|인용|서지|문헌)"),
}


def run_git(*arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def path_scopes(path: str) -> set[str]:
    lowered = path.lower()
    name = Path(path).name.lower()
    suffix = Path(path).suffix.lower()
    scopes: set[str] = set()

    if suffix == ".tex":
        scopes.add("THEORY_TEXT")
    if suffix in {".md", ".txt", ".html"}:
        scopes.add("NARRATIVE_OR_REPORT")
    if suffix == ".py":
        scopes.add("CODE")
    if (
        "test" in name
        or "/tests/" in lowered
        or name.startswith("test_")
        or "gate" in name
    ):
        scopes.add("TEST_OR_GATE")
    if suffix == ".pdf":
        scopes.add("BUILD_OR_PDF")
    if "plan" in name or "/plans/" in lowered:
        scopes.add("PLAN")
    if "handover" in name:
        scopes.add("HANDOVER")
    if name.startswith("index") or name == "index.md":
        scopes.add("INDEX")
    if "ledger" in name or "change_log" in name or name.endswith(".log"):
        scopes.add("LEDGER_OR_LOG")
    if suffix in {".csv", ".parquet", ".bdf"} or "data" in lowered:
        scopes.add("DATA_OR_FIT")
    if (
        "reference" in name
        or "citation" in name
        or suffix == ".bib"
        or "literature" in lowered
    ):
        scopes.add("REFERENCE")
    if suffix in {".json", ".yaml", ".yml"}:
        scopes.add("MACHINE_RECORD")
    if suffix in {".png", ".jpg", ".jpeg", ".svg"}:
        scopes.add("IMAGE")
    if suffix in {".bat", ".ps1", ".sh"}:
        scopes.add("EXECUTION_SCRIPT")
    return scopes


def batch_changed_paths(
    wanted_commits: set[str],
) -> dict[str, list[dict[str, Any]]]:
    changes: dict[str, list[dict[str, Any]]] = {}
    for commit in sorted(wanted_commits):
        output = run_git(
            "diff-tree",
            "--root",
            "--first-parent",
            "--no-commit-id",
            "--name-status",
            "-r",
            "--no-renames",
            commit,
        )
        records: list[dict[str, Any]] = []
        for line in output.splitlines():
            if not line:
                continue
            fields = line.split("\t")
            status = fields[0]
            if status.startswith(("R", "C")):
                old_path, path = fields[1], fields[2]
            else:
                old_path, path = None, fields[1]
            records.append(
                {
                    "status": status,
                    "old_path": old_path,
                    "path": path,
                    "scopes": sorted(path_scopes(path)),
                }
            )
        changes[commit] = records
    return changes


def main() -> None:
    genealogy = json.loads(GENEALOGY_PATH.read_text(encoding="utf-8"))
    assert genealogy["baseline_commit"] == BASELINE
    baseline_ancestors = set(run_git("rev-list", BASELINE).splitlines())

    event_by_commit: dict[str, dict[str, Any]] = {}
    intent_documents_by_commit: dict[str, set[str]] = {}
    completion_markers_by_commit: dict[str, set[str]] = {}
    for document in genealogy["documents"]:
        for path_record in document["paths"]:
            for event in path_record["events"]:
                commit = event["commit"]
                event_by_commit[commit] = {
                    "commit": commit,
                    "date": event["date"],
                    "parents": event["parents"],
                    "subject": event["subject"],
                }
                intent_documents_by_commit.setdefault(commit, set()).add(
                    document["representative_path"]
                )
                completion_markers_by_commit.setdefault(commit, set()).update(
                    event["completion_markers_in_subject"]
                )

    records: list[dict[str, Any]] = []
    claimed_scope_counts: Counter[str] = Counter()
    actual_scope_counts: Counter[str] = Counter()
    no_patch_artifact_counts: Counter[str] = Counter()
    wanted_commits = set(event_by_commit)
    changes_by_commit = batch_changed_paths(wanted_commits)

    for commit, metadata in sorted(
        event_by_commit.items(), key=lambda item: (item[1]["date"], item[0])
    ):
        assert commit in baseline_ancestors
        changes = changes_by_commit[commit]
        claimed_scopes = sorted(
            scope
            for scope, pattern in CLAIM_PATTERNS.items()
            if pattern.search(metadata["subject"])
        )
        actual_scopes = sorted(
            {
                scope
                for change in changes
                for scope in change["scopes"]
            }
        )

        # A subject can report an executed check without changing a test file.
        # These are evidence gaps to inspect, not automatic falsehoods.
        claim_to_artifact = {
            "THEORY_TEXT": {"THEORY_TEXT"},
            "CODE": {"CODE"},
            "TEST_OR_GATE": {"TEST_OR_GATE", "MACHINE_RECORD", "LEDGER_OR_LOG"},
            "BUILD_OR_PDF": {"BUILD_OR_PDF", "MACHINE_RECORD", "LEDGER_OR_LOG"},
            "PLAN": {"PLAN"},
            "HANDOVER": {"HANDOVER"},
            "INDEX": {"INDEX"},
            "LEDGER_OR_LOG": {"LEDGER_OR_LOG"},
            "DATA_OR_FIT": {"DATA_OR_FIT", "MACHINE_RECORD", "IMAGE"},
            "REFERENCE": {"REFERENCE", "THEORY_TEXT", "NARRATIVE_OR_REPORT"},
        }
        claimed_scope_without_patch_artifact = sorted(
            scope
            for scope in claimed_scopes
            if not claim_to_artifact[scope].intersection(actual_scopes)
        )

        claimed_scope_counts.update(claimed_scopes)
        actual_scope_counts.update(actual_scopes)
        no_patch_artifact_counts.update(claimed_scope_without_patch_artifact)
        records.append(
            {
                **metadata,
                "completion_markers_in_subject": sorted(
                    completion_markers_by_commit[commit]
                ),
                "intent_document_count": len(
                    intent_documents_by_commit[commit]
                ),
                "intent_documents": sorted(intent_documents_by_commit[commit]),
                "claimed_scopes_from_subject": claimed_scopes,
                "actual_patch_scopes": actual_scopes,
                "claimed_scope_without_patch_artifact": (
                    claimed_scope_without_patch_artifact
                ),
                "changed_file_count": len(changes),
                "status_counts": dict(
                    sorted(
                        Counter(
                            change["status"][0] for change in changes
                        ).items()
                    )
                ),
                "changes": changes,
            }
        )

    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": BASELINE,
        "source_genealogy": str(GENEALOGY_PATH.relative_to(REPO_ROOT)),
        "commit_count": len(records),
        "completion_marker_commit_count": sum(
            bool(record["completion_markers_in_subject"]) for record in records
        ),
        "total_changed_file_events": sum(
            record["changed_file_count"] for record in records
        ),
        "claimed_scope_counts": dict(sorted(claimed_scope_counts.items())),
        "actual_scope_counts": dict(sorted(actual_scope_counts.items())),
        "claimed_scope_without_patch_artifact_counts": dict(
            sorted(no_patch_artifact_counts.items())
        ),
        "commits": records,
        "validation": {
            "all_genealogy_commits_present": len(records)
            == genealogy["unique_commit_count"],
            "all_commits_are_baseline_ancestors": True,
            "all_patches_are_first_parent_or_root": True,
            "no_patch_artifact_is_not_automatic_falsification": True,
        },
    }
    encoded = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    OUTPUT_PATH.write_text(encoded, encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "PASS",
                "output": str(OUTPUT_PATH.relative_to(REPO_ROOT)),
                "commits": payload["commit_count"],
                "completion_marker_commits": payload[
                    "completion_marker_commit_count"
                ],
                "changed_file_events": payload["total_changed_file_events"],
                "sha256": hashlib.sha256(encoded.encode()).hexdigest(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
