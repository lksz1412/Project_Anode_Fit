"""Conservatively adjudicate Phase 057 completion/authority claim candidates."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
CLAIMS_PATH = (
    REPO_ROOT / "Codex/results/PHASE_057_COMPLETION_AUTHORITY_CLAIMS.json"
)
MATRIX_PATH = REPO_ROOT / "Codex/results/PHASE_057_COMMIT_CLAIM_MATRIX.json"
OUTPUT_PATH = (
    REPO_ROOT / "Codex/results/PHASE_057_COMPLETION_CLAIM_ADJUDICATION.json"
)

LIMITATION_PATTERN = re.compile(
    r"(?i)(?:미완료|미수행|미실행|미검증|미해소|불완료|검증되지|"
    r"증거가\s*아니|증빙이\s*아니|범위\s*밖|차단|대기|잔여|남았다|"
    r"부재|불가|하지\s*않았|못\s*했|not\s+(?:performed|verified|complete)|"
    r"incomplete|pending|unverified)"
)
FUTURE_OR_CRITERION_PATTERN = re.compile(
    r"(?i)(?:해야\s*한다|해야\s*함|할\s*것|예정|계획|목표|acceptance|"
    r"통과\s*조건|gate|검증\s*기준|확인\s*후|수행\s*후|재실행\s*필요)"
)
QUOTED_OR_META_PATTERN = re.compile(
    r"(?i)(?:라고\s*(?:쓰|말|주장|보고)|주장을?\s*(?:인용|반박)|"
    r"스테일|stale|요지\s*인용|실행분\s*인용|자기보고)"
)


def manual_override(path: str, line: int | None, text: str) -> dict[str, str] | None:
    """Return high-risk claims that were independently resolved during the re-audit."""

    if path.endswith("v1.0.25.2/ARCHIVE_NOTE.md") and line == 1:
        return {
            "status": "OVERCLAIMED",
            "reason_code": "STALE_AUTHORITY_LABEL",
            "basis": (
                "v1.0.25.2 경로에 복제된 제목이 v1.0.25.1을 현행 최신으로 "
                "부른다. 같은 파일 후반과 사용자 확인은 v1.0.25.2를 최신으로 둔다."
            ),
        }
    if path.endswith("v1.0.25.2/ARCHIVE_NOTE.md") and line == 200:
        return {
            "status": "CONFIRMED",
            "reason_code": "CURRENT_BASELINE_AUTHORITY_CONFIRMED",
            "basis": (
                "현재 감사 기준선, Git tree와 사용자 재확인이 모두 "
                "v1.0.25.2를 최신 과학 기준선으로 지정한다."
            ),
        }
    if path.endswith("v1.0.25.2/results/HANDOVER_v1025_2.md") and line in {
        3,
        171,
    }:
        return {
            "status": "CONFIRMED",
            "reason_code": "CURRENT_BASELINE_AUTHORITY_CONFIRMED",
            "basis": (
                "현재 감사 기준선, Git tree와 사용자 재확인이 모두 "
                "v1.0.25.2를 최신 과학 기준선으로 지정한다."
            ),
        }
    if path.endswith("v1.0.25.2/results/HANDOVER_v1025_2.md") and line == 25:
        return {
            "status": "OVERCLAIMED",
            "reason_code": "THEORY_CODE_BOUNDARY_VIOLATED",
            "basis": (
                "최종 이론 계열의 본문·부록·각주에 함수명, key, gate, "
                "bit-exact 및 code map이 남아 있어 '코드 이야기 배제 완료'와 충돌한다."
            ),
        }
    if path.endswith("v1.0.25.2/ARCHIVE_NOTE.md") and line == 230:
        return {
            "status": "OVERCLAIMED",
            "reason_code": "IMPLEMENTATION_COMPLETION_TOO_BROAD",
            "basis": (
                "최종 기본 경로는 legacy4이고 skew7은 opt-in isothermal 표현이며, "
                "정칙용액 이론과 logistic 평형 구현도 단절돼 '코드 반영 완결'은 성립하지 않는다."
            ),
        }
    if path.endswith("KERNEL_COMPARISON_REPORT_v1025_2.html") and line == 228:
        return {
            "status": "OVERCLAIMED",
            "reason_code": "LOSING_FIT_TRANSFERRED_TO_PHASE_CLAIM",
            "basis": (
                "패배한 regsol 적합의 Ω/RT 중 하나는 임계값 아래이고 불확도·대응 "
                "전이가 검증되지 않았다. 이를 winning basis나 독립 상 판정으로 이전할 수 없다."
            ),
        }
    if path.endswith("v1.0.25.2/ARCHIVE_NOTE.md") and line == 270:
        return {
            "status": "PARTIAL",
            "reason_code": "GREEN_SCOPE_NARROWER_THAN_SCIENTIFIC_CLAIM",
            "basis": (
                "나열된 gate 실행은 기록됐지만 legacy 복원 때문에 당시 결함 기본 경로를 "
                "검사하지 못했다. GREEN은 실제 검사한 경로에만 유효하다."
            ),
        }
    if (
        path.endswith("v1.0.25.1/results/HANDOVER_v25.md")
        and line == 56
        and "30/30" in text
    ):
        return {
            "status": "PARTIAL",
            "reason_code": "CONFORMANCE_NOT_PHYSICAL_VALIDITY",
            "basis": (
                "30/30은 문건 식과 코드 계산의 복제를 보이지만 같은 물리 오류의 "
                "양쪽 복제, 외부 데이터 타당성 및 후속 편집 뒤 stale 상태를 배제하지 못한다."
            ),
        }
    return None


def evidence_tier(categories: list[str], scopes: set[str]) -> tuple[str, str]:
    if "CONFORMANCE" in categories:
        required = {"CODE", "THEORY_TEXT", "TEST_OR_GATE"}
        if required.issubset(scopes):
            return (
                "PARTIAL",
                "SAME_COMMIT_CODE_THEORY_TEST_NOT_INDEPENDENT_VALIDATION",
            )
        if scopes & required:
            return "UNVERIFIED", "CONFORMANCE_EVIDENCE_INCOMPLETE"
        return "UNVERIFIED", "TEXT_ONLY_CONFORMANCE_ASSERTION"
    if "INVARIANCE" in categories:
        if scopes & {"MACHINE_RECORD", "TEST_OR_GATE"}:
            return "PARTIAL", "MACHINE_OR_TEST_ARTIFACT_NOT_RERUN"
        return "UNVERIFIED", "NO_INDEPENDENT_INVARIANCE_EVIDENCE"
    if "COMPLETION" in categories:
        if scopes & {"BUILD_OR_PDF", "MACHINE_RECORD", "TEST_OR_GATE"}:
            return "PARTIAL", "EXECUTION_ARTIFACT_PRESENT_SCOPE_NOT_FULLY_PROVEN"
        return "UNVERIFIED", "COMPLETION_SELF_REPORT_ONLY"
    return "UNVERIFIED", "AUTHORITY_NOT_INDEPENDENTLY_ESTABLISHED"


def main() -> None:
    claims = json.loads(CLAIMS_PATH.read_text(encoding="utf-8"))
    matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    documents = {
        document["document_id"]: document
        for document in claims["document_summaries"]
    }
    commits = {record["commit"]: record for record in matrix["commits"]}

    records: list[dict[str, Any]] = []
    disposition_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    reason_counts: Counter[str] = Counter()

    for candidate in claims["candidates"]:
        document = documents[candidate["document_id"]]
        path = document["representative_path"]
        text = candidate["excerpt"]
        line = candidate["line"]
        override = manual_override(path, line, text)

        if override is not None:
            disposition = "POSITIVE_ASSERTION"
            status = override["status"]
            reason_code = override["reason_code"]
            basis = override["basis"]
            rule = "MANUAL_REAUDIT_OVERRIDE"
        elif LIMITATION_PATTERN.search(text):
            disposition = "NON_POSITIVE_LIMITATION"
            status = None
            reason_code = "NEGATED_OR_LIMITED_CONTEXT"
            basis = (
                "후보 literal이 미완료·미검증·잔여·부재 등 제한 또는 부정 "
                "문맥에 있어 긍정적 완료 주장으로 판정하지 않는다."
            )
            rule = "CONTEXT_FILTER"
        elif (
            document["document_category"] == "PLAN"
            and FUTURE_OR_CRITERION_PATTERN.search(text)
        ):
            disposition = "NON_POSITIVE_PLAN_OR_CRITERION"
            status = None
            reason_code = "FUTURE_ACTION_OR_GATE_DEFINITION"
            basis = (
                "계획서의 향후 행동·통과 조건을 실제 완료 결과로 세지 않는다."
            )
            rule = "CONTEXT_FILTER"
        elif QUOTED_OR_META_PATTERN.search(text):
            disposition = "NON_POSITIVE_QUOTED_OR_META"
            status = None
            reason_code = "QUOTED_STALE_OR_SELF_REPORT_DISCUSSION"
            basis = (
                "다른 선언의 인용·비판·stale 표기 또는 자기보고 논평이며 "
                "이 위치 자체를 독립 긍정 주장으로 세지 않는다."
            )
            rule = "CONTEXT_FILTER"
        else:
            disposition = "POSITIVE_ASSERTION"
            commit = commits.get(document["first_exact_blob_commit"])
            scopes = set(commit["actual_patch_scopes"]) if commit else set()
            status, reason_code = evidence_tier(candidate["categories"], scopes)
            basis = (
                "exact-blob 최초 commit의 실제 patch scope를 연결했다. 같은 commit의 "
                "산출물은 실행 흔적이지만 독립적인 물리·과학 검증으로 승격하지 않는다."
            )
            rule = "CONSERVATIVE_PATCH_EVIDENCE_RULE"

        disposition_counts[disposition] += 1
        reason_counts[reason_code] += 1
        if status is not None:
            status_counts[status] += 1
        commit = commits.get(document["first_exact_blob_commit"])
        records.append(
            {
                **candidate,
                "representative_path": path,
                "first_exact_blob_commit": document["first_exact_blob_commit"],
                "commit_actual_patch_scopes": (
                    commit["actual_patch_scopes"] if commit else []
                ),
                "linked_provisional_claim_ids": document[
                    "provisional_claim_ids"
                ],
                "disposition": disposition,
                "adjudication_status": status,
                "reason_code": reason_code,
                "adjudication_basis": basis,
                "adjudication_rule": rule,
            }
        )

    positive_count = disposition_counts["POSITIVE_ASSERTION"]
    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": claims["baseline_commit"],
        "source_claim_candidates": str(CLAIMS_PATH.relative_to(REPO_ROOT)),
        "source_commit_matrix": str(MATRIX_PATH.relative_to(REPO_ROOT)),
        "candidate_count": len(records),
        "positive_assertion_count": positive_count,
        "non_positive_candidate_count": len(records) - positive_count,
        "disposition_counts": dict(sorted(disposition_counts.items())),
        "adjudication_status_counts": dict(sorted(status_counts.items())),
        "reason_code_counts": dict(sorted(reason_counts.items())),
        "policy": {
            "same_commit_artifact_maximum_status": "PARTIAL",
            "default_without_independent_evidence": "UNVERIFIED",
            "manual_overrides_require_saved_reaudit_basis": True,
            "non_positive_candidates_excluded_from_four_status_denominator": True,
        },
        "records": records,
        "validation": {
            "all_candidates_disposed": len(records) == claims["candidate_count"],
            "all_positive_assertions_have_four_way_status": all(
                record["adjudication_status"]
                in {"CONFIRMED", "OVERCLAIMED", "PARTIAL", "UNVERIFIED"}
                for record in records
                if record["disposition"] == "POSITIVE_ASSERTION"
            ),
            "non_positive_candidates_have_null_status": all(
                record["adjudication_status"] is None
                for record in records
                if record["disposition"] != "POSITIVE_ASSERTION"
            ),
            "status_sum_matches_positive_assertions": sum(
                status_counts.values()
            )
            == positive_count,
            "source_candidate_ids_preserved": [
                record["candidate_id"] for record in records
            ]
            == [candidate["candidate_id"] for candidate in claims["candidates"]],
        },
    }
    encoded = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    OUTPUT_PATH.write_text(encoded, encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "PASS",
                "output": str(OUTPUT_PATH.relative_to(REPO_ROOT)),
                "candidates": payload["candidate_count"],
                "positive_assertions": positive_count,
                "non_positive_candidates": payload[
                    "non_positive_candidate_count"
                ],
                "adjudication_status_counts": payload[
                    "adjudication_status_counts"
                ],
                "sha256": hashlib.sha256(encoded.encode()).hexdigest(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
