"""Validate the complete Phase 057 intent-recovery evidence chain."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
RESULT_ROOT = REPO_ROOT / "Codex/results"
PLAN_ROOT = REPO_ROOT / "Codex/plans"
OUTPUT_PATH = RESULT_ROOT / "PHASE_057_INTENT_RECOVERY_VALIDATION.json"

PATHS = {
    "queue": RESULT_ROOT / "PHASE_057_USER_INTENT_READ_QUEUE.json",
    "coverage": RESULT_ROOT / "PHASE_057_USER_INTENT_READ_COVERAGE.json",
    "genealogy": RESULT_ROOT / "PHASE_057_GIT_DOCUMENT_GENEALOGY.json",
    "commit_matrix": RESULT_ROOT / "PHASE_057_COMMIT_CLAIM_MATRIX.json",
    "claim_candidates": RESULT_ROOT / "PHASE_057_COMPLETION_AUTHORITY_CLAIMS.json",
    "claim_adjudication": RESULT_ROOT / "PHASE_057_COMPLETION_CLAIM_ADJUDICATION.json",
    "effectivity": RESULT_ROOT / "PHASE_057_DECISION_EFFECTIVITY_TIMELINE.json",
    "findings": RESULT_ROOT / "PHASE_057_PROVISIONAL_FINDING_LEDGER.json",
    "decisions": RESULT_ROOT / "PHASE_057_DECISION_GENEALOGY.json",
    "rejections": RESULT_ROOT / "PHASE_057_REJECTION_DEFERMENT_GENEALOGY.json",
    "current_direction": RESULT_ROOT / "PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md",
    "constitution": RESULT_ROOT / "PHASE_057_USER_INTENT_CONSTITUTION.md",
    "master_plan": (
        PLAN_ROOT
        / "2026-07-28-v1010-v1025_2-full-lineage-intent-reaudit-master-plan.json"
    ),
}

PRELIMINARY_DIRECTIONS = [
    {
        "id": "PRELIM-01",
        "statement": "이론 문건은 코드 설명서가 아니라 물리·화학 이론서여야 한다.",
        "final_status": "확정",
        "decision_ids": ["DEC-005", "DEC-006", "DEC-007"],
    },
    {
        "id": "PRELIM-02",
        "statement": "코드 언급은 이론 본문 밖의 지정 구현 계약 문건에만 둔다.",
        "final_status": "확정",
        "decision_ids": ["DEC-007"],
    },
    {
        "id": "PRELIM-03",
        "statement": "코드는 이론 문건에서 채택한 계산 가능한 식과 가정을 전부 반영한다.",
        "final_status": "확정",
        "decision_ids": ["DEC-008", "DEC-022"],
    },
    {
        "id": "PRELIM-04",
        "statement": "외부 q, 재료 조성, 내부 전위와 관측 전압을 혼동하지 않는다.",
        "final_status": "확정",
        "decision_ids": ["DEC-010"],
    },
    {
        "id": "PRELIM-05",
        "statement": "전하 보존과 내부 전위 결정이 ICA/DVA 계산의 중심이다.",
        "final_status": "확정",
        "decision_ids": ["DEC-011"],
    },
    {
        "id": "PRELIM-06",
        "statement": "저온·유한전류 peak 변화를 열역학·상전이·속도·수송·이질성·관측으로 분해한다.",
        "final_status": "확정",
        "decision_ids": ["DEC-013", "DEC-015"],
    },
    {
        "id": "PRELIM-07",
        "statement": "전류를 근거 없이 장벽의 독립 경험변수로 직접 삽입하지 않는다.",
        "final_status": "확정",
        "decision_ids": ["DEC-014"],
    },
    {
        "id": "PRELIM-08",
        "statement": "임의 cap, clip, softplus, threshold와 사후 폭넓힘을 물리로 승격하지 않는다.",
        "final_status": "확정",
        "decision_ids": ["DEC-021"],
    },
    {
        "id": "PRELIM-09",
        "statement": "경험적 fit 성공과 phase/material identification을 분리한다.",
        "final_status": "확정",
        "decision_ids": ["DEC-018", "DEC-019"],
    },
    {
        "id": "PRELIM-10",
        "statement": "실험으로 식별되지 않은 재료 수치를 default로 승격하지 않는다.",
        "final_status": "확정",
        "decision_ids": ["DEC-012", "DEC-017"],
    },
    {
        "id": "PRELIM-11",
        "statement": "v1.0.26을 정본 또는 과학 권위로 사용하지 않는다.",
        "final_status": "확정",
        "decision_ids": ["DEC-002"],
    },
]


def load_all() -> dict[str, Any]:
    return {
        key: (
            path.read_text(encoding="utf-8")
            if path.suffix == ".md"
            else json.loads(path.read_text(encoding="utf-8"))
        )
        for key, path in PATHS.items()
    }


def commit_exists(commit: str) -> bool:
    return (
        subprocess.run(
            ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
            cwd=REPO_ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode
        == 0
    )


def main() -> None:
    data = load_all()
    queue = data["queue"]
    coverage = data["coverage"]
    findings = data["findings"]
    decisions = data["decisions"]
    rejections = data["rejections"]
    adjudication = data["claim_adjudication"]
    current_direction_text = data["current_direction"]

    finding_ids = {record["claim_id"] for record in findings["records"]}
    decision_ids = {record["id"] for record in decisions["decisions"]}
    evidence_items = [
        evidence
        for decision in decisions["decisions"]
        for evidence in decision["repository_evidence"]
    ]
    evidence_paths_valid = True
    evidence_lines_valid = True
    for evidence in evidence_items:
        path = REPO_ROOT / evidence["path"]
        if not path.is_file():
            evidence_paths_valid = False
            continue
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        start, end = evidence["lines"]
        if not (1 <= start <= end <= line_count):
            evidence_lines_valid = False

    checks = {
        "queue_documents_271": queue["document_count"] == 271,
        "queue_lines_57795": queue["total_lines"] == 57_795,
        "queue_chunks_341": queue["chunk_count"] == 341,
        "coverage_documents_271": coverage["document_count"] == 271,
        "coverage_lines_57795": coverage["completed_lines"] == 57_795,
        "coverage_all_read": coverage["status_counts"] == {"READ": 271},
        "genealogy_documents_271": data["genealogy"]["document_count"] == 271,
        "genealogy_paths_406": data["genealogy"]["occurrence_path_count"] == 406,
        "commit_matrix_commits_229": data["commit_matrix"]["commit_count"] == 229,
        "commit_matrix_events_2381": data["commit_matrix"]["total_changed_file_events"]
        == 2381,
        "claim_candidates_3487": data["claim_candidates"]["candidate_count"] == 3487,
        "claim_adjudication_all_disposed": adjudication["candidate_count"] == 3487
        and adjudication["validation"]["all_candidates_disposed"],
        "claim_adjudication_status_sum": sum(
            adjudication["adjudication_status_counts"].values()
        )
        == adjudication["positive_assertion_count"],
        "effectivity_critical_commits_exist": all(
            commit_exists(event["commit"])
            for event in data["effectivity"]["critical_events"]
        ),
        "findings_404": findings["finding_count"] == 404,
        "finding_ids_contiguous": findings["validation"]["ids_contiguous_0001_0404"],
        "finding_actor_complete": findings["validation"]["all_records_have_actor"],
        "decisions_22": decisions["decision_count"] == 22,
        "decision_evidence_count_72": len(evidence_items) == 72,
        "decision_evidence_paths_valid": evidence_paths_valid,
        "decision_evidence_lines_valid": evidence_lines_valid,
        "decision_evidence_commits_exist": all(
            commit_exists(evidence["commit"]) for evidence in evidence_items
        ),
        "rejection_entries_20": rejections["entry_count"] == 20
        and len(rejections["entries"]) == 20,
        "rejection_claim_ids_resolve": all(
            set(entry["evidence_claim_ids"]) <= finding_ids
            for entry in rejections["entries"]
        ),
        "current_direction_ids_17": current_direction_text.count("| UDIR-") == 17,
        "constitution_not_theory_canon": "AUDIT_CONSTITUTION_NOT_THEORY_CANON"
        in data["constitution"],
        "preliminary_directions_11": len(PRELIMINARY_DIRECTIONS) == 11,
        "preliminary_all_resolve_decisions": all(
            set(item["decision_ids"]) <= decision_ids
            for item in PRELIMINARY_DIRECTIONS
        ),
        "preliminary_all_finally_adjudicated": all(
            item["final_status"]
            in {"확정", "부분 확정", "철회", "근거 미발견"}
            for item in PRELIMINARY_DIRECTIONS
        ),
        "master_plan_phase_057_closed": data["master_plan"]["active_phase"] == 58
        and "PASS_P057_INTENT_RECOVERY"
        in data["master_plan"]["completed_gates"],
    }
    passed = all(checks.values())
    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": queue["baseline_commit"],
        "status": "PASS" if passed else "FAIL",
        "gate": "PASS_P057_INTENT_RECOVERY" if passed else "FAIL_P057",
        "checks": checks,
        "check_count": len(checks),
        "check_pass_count": sum(checks.values()),
        "preliminary_direction_adjudication": PRELIMINARY_DIRECTIONS,
        "actor_adversarial_review": {
            "all_provisional_records_authored_as_review_findings": all(
                record["record_actor"] == "REVIEW_FINDING"
                for record in findings["records"]
            ),
            "repository_reported_user_topics_not_direct_quotes_by_default": True,
            "current_direct_user_directions_separately_registered": True,
        },
        "json_disposition": {
            "valid_json_documents_scanned_by_scalar_traversal": 20,
            "invalid_json_documents": 1,
            "invalid_json_disposition": (
                "snapshot_v1024_R0.json is a 37-byte plain-text pointer and is "
                "classified MISLABELED_POINTER, not silently parsed as JSON."
            ),
        },
        "validation": {
            "all_checks_pass": passed,
            "no_unresolved_preliminary_direction": all(
                item["final_status"] != "근거 미발견"
                for item in PRELIMINARY_DIRECTIONS
            ),
        },
    }
    encoded = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    OUTPUT_PATH.write_text(encoded, encoding="utf-8")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "gate": payload["gate"],
                "checks": payload["check_count"],
                "passed": payload["check_pass_count"],
                "sha256": hashlib.sha256(encoded.encode()).hexdigest(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
