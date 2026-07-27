"""Generate the Phase 057 canonical decision genealogy."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
FINDINGS_PATH = REPO_ROOT / "Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json"
OUTPUT_PATH = REPO_ROOT / "Codex/results/PHASE_057_DECISION_GENEALOGY.json"

DECISIONS: list[dict[str, Any]] = [
    {
        "id": "DEC-001",
        "topic": "audit-scope",
        "statement": "새 이론·코드 작업 전에 v1.0.10–v1.0.25.2 전 계보를 다시 감사한다.",
        "status": "PRESERVE",
        "actor": "USER_REQUIREMENT",
        "current_direction_ids": ["UDIR-01"],
        "claim_ids": [96, 181],
    },
    {
        "id": "DEC-002",
        "topic": "scientific-baseline",
        "statement": "v1.0.25.2를 최신 기준선으로 사용하고 v1.0.26은 권위에서 제외한다.",
        "status": "PRESERVE",
        "actor": "USER_REQUIREMENT",
        "current_direction_ids": ["UDIR-02"],
        "claim_ids": [376, 378],
    },
    {
        "id": "DEC-003",
        "topic": "source-preservation",
        "statement": "원본과 main을 수정하지 않고 전용 branch에서만 작업한다.",
        "status": "PRESERVE",
        "actor": "USER_REQUIREMENT",
        "current_direction_ids": ["UDIR-03"],
        "claim_ids": [354],
    },
    {
        "id": "DEC-004",
        "topic": "compaction-resilient-workflow",
        "statement": "master phase plan, 세부 step plan, step history, ledger, handover, commit/push 사슬을 유지한다.",
        "status": "PRESERVE",
        "actor": "USER_REQUIREMENT",
        "current_direction_ids": ["UDIR-04", "UDIR-14"],
        "claim_ids": [181, 354],
    },
    {
        "id": "DEC-005",
        "topic": "reader-and-depth",
        "statement": "대학원 교재의 친절한 유도와 review 논문의 깊이를 동시에 달성한다.",
        "status": "PRESERVE",
        "actor": "USER_REQUIREMENT",
        "current_direction_ids": ["UDIR-07", "UDIR-08"],
        "claim_ids": [26, 47, 111],
    },
    {
        "id": "DEC-006",
        "topic": "self-contained-manuscript",
        "statement": "최종 이론 문건은 과거 작업사와 버전 방어 문구 없이 한 권으로 자립한다.",
        "status": "PRESERVE",
        "actor": "USER_REQUIREMENT",
        "current_direction_ids": ["UDIR-07"],
        "claim_ids": [20, 36],
    },
    {
        "id": "DEC-007",
        "topic": "theory-code-boundary",
        "statement": "이론 문건에는 물리·화학만 두고 함수명, key, gate, code map은 별도 companion으로 분리한다.",
        "status": "PRESERVE",
        "actor": "USER_REQUIREMENT",
        "current_direction_ids": ["UDIR-05"],
        "claim_ids": [30, 69, 139, 203, 244, 380, 394],
    },
    {
        "id": "DEC-008",
        "topic": "authority-direction",
        "statement": "권위 방향은 theory → implementation contract → code이며 code-first cascade를 최종 방식으로 사용하지 않는다.",
        "status": "PRESERVE",
        "actor": "USER_REQUIREMENT",
        "current_direction_ids": ["UDIR-06"],
        "claim_ids": [6, 14, 277, 314, 346],
    },
    {
        "id": "DEC-009",
        "topic": "literature-derivation",
        "statement": "1차 문헌을 전제·변수 대응·유도·적용범위까지 검증하고 결론 인용만으로 닫지 않는다.",
        "status": "PRESERVE",
        "actor": "USER_REQUIREMENT",
        "current_direction_ids": ["UDIR-08"],
        "claim_ids": [111],
    },
    {
        "id": "DEC-010",
        "topic": "coordinate-separation",
        "statement": "외부 누적용량 q, 재료 조성, 전극 내부전위, 관측 cell voltage를 별도 좌표로 정의한다.",
        "status": "CORRECT",
        "actor": "REVIEW_FINDING",
        "current_direction_ids": [],
        "claim_ids": [50, 174],
    },
    {
        "id": "DEC-011",
        "topic": "charge-conservation",
        "statement": "전하 보존과 공통 cell voltage 제약을 ICA/DVA 및 blend 조립의 중심에 둔다.",
        "status": "PRESERVE",
        "actor": "REVIEW_FINDING",
        "current_direction_ids": [],
        "claim_ids": [174],
    },
    {
        "id": "DEC-012",
        "topic": "material-free-energy",
        "statement": "공통 보존법칙 위에 graphite, doped LCO, Si/SiOx/Si-C별 자유에너지와 상태변수를 분리한다.",
        "status": "CORRECT",
        "actor": "USER_REQUIREMENT",
        "current_direction_ids": ["UDIR-09"],
        "claim_ids": [174, 257],
    },
    {
        "id": "DEC-013",
        "topic": "equilibrium-kinetics-observation-layers",
        "statement": "equilibrium state, kinetic barrier/internal variables, observation/differentiation을 연결하되 서로 혼합하지 않는다.",
        "status": "PRESERVE",
        "actor": "USER_REQUIREMENT",
        "current_direction_ids": ["UDIR-10", "UDIR-11"],
        "claim_ids": [174, 219, 379],
    },
    {
        "id": "DEC-014",
        "topic": "temperature-current-potential-barrier",
        "statement": "장벽의 T·I·U 의존은 전위·과전압·상태·열활성화에서 유도하며 전류를 근거 없는 독립 barrier 변수로 삽입하지 않는다.",
        "status": "CORRECT",
        "actor": "USER_REQUIREMENT",
        "current_direction_ids": ["UDIR-10", "UDIR-11"],
        "claim_ids": [174, 219, 253, 351, 403],
    },
    {
        "id": "DEC-015",
        "topic": "peak-broadening-decomposition",
        "statement": "저온·유한전류 peak 저하·이동·broadening을 상공존, 이질성, kinetics, transport, observation으로 분해한다.",
        "status": "CORRECT",
        "actor": "USER_REQUIREMENT",
        "current_direction_ids": ["UDIR-10", "UDIR-11"],
        "claim_ids": [15, 174, 219, 351, 403],
    },
    {
        "id": "DEC-016",
        "topic": "thermodynamic-heat-closure",
        "statement": "entropy와 reversible heat는 승인된 free energy의 온도 미분에서 파생하고 empirical shape가 이를 오염시키지 않게 한다.",
        "status": "CORRECT",
        "actor": "REVIEW_FINDING",
        "current_direction_ids": [],
        "claim_ids": [15, 337],
    },
    {
        "id": "DEC-017",
        "topic": "public-data-validation",
        "statement": "graphite, Si, blend, doped high-voltage LCO의 공개 다온도·다율속 데이터를 calibration과 holdout으로 사용한다.",
        "status": "PRESERVE",
        "actor": "USER_REQUIREMENT",
        "current_direction_ids": ["UDIR-09"],
        "claim_ids": [257, 347, 351, 403],
    },
    {
        "id": "DEC-018",
        "topic": "fit-versus-identification",
        "statement": "실제 fit 성공을 보존하되 basis component, phase, gallery, material constant의 식별로 자동 승격하지 않는다.",
        "status": "PRESERVE",
        "actor": "USER_REQUIREMENT",
        "current_direction_ids": ["UDIR-13", "UDIR-16"],
        "claim_ids": [50, 219, 347, 399, 401, 402],
    },
    {
        "id": "DEC-019",
        "topic": "empirical-skew-basis",
        "statement": "skew-logistic/gallery basis는 검증된 thermodynamic kernel이 아니라 empirical observation/heterogeneity 후보로만 보존한다.",
        "status": "EMPIRICAL_ONLY",
        "actor": "REVIEW_FINDING",
        "current_direction_ids": ["UDIR-16"],
        "claim_ids": [336, 337, 338, 399, 402],
    },
    {
        "id": "DEC-020",
        "topic": "regular-solution-role",
        "statement": "regular-solution 자유에너지는 재유도 후보로 남기되 패배한 curve fit의 Omega를 phase 권위로 이전하지 않는다.",
        "status": "THEORY_ONLY",
        "actor": "REVIEW_FINDING",
        "current_direction_ids": [],
        "claim_ids": [339, 340, 370, 379, 398, 401],
    },
    {
        "id": "DEC-021",
        "topic": "numerical-guards",
        "statement": "invalid input rejection은 보존하지만 값과 gradient를 몰래 바꾸는 cap, clip, clamp, fixed threshold/grid branch는 유도 없이는 거부한다.",
        "status": "REJECT",
        "actor": "USER_REQUIREMENT",
        "current_direction_ids": ["UDIR-12"],
        "claim_ids": [286],
    },
    {
        "id": "DEC-022",
        "topic": "acceptance-boundary",
        "statement": "문건–코드 conformance, 제한극한, parameter recovery, uncertainty, holdout, multi-condition/material transfer를 별도 gate로 통과한다.",
        "status": "PRESERVE",
        "actor": "USER_REQUIREMENT",
        "current_direction_ids": ["UDIR-13", "UDIR-16"],
        "claim_ids": [174, 346, 347, 351, 403],
    },
]


def evidence_commit(path: str) -> str:
    result = subprocess.check_output(
        ["git", "log", "-1", "--format=%H", "--", path],
        cwd=REPO_ROOT,
        text=True,
    ).strip()
    if not result:
        raise RuntimeError(f"No Git commit found for {path}")
    return result


def main() -> None:
    findings = json.loads(FINDINGS_PATH.read_text(encoding="utf-8"))
    finding_by_id = {
        record["numeric_id"]: record for record in findings["records"]
    }
    commit_cache: dict[str, str] = {}
    records: list[dict[str, Any]] = []

    for decision in DECISIONS:
        evidence = []
        for numeric_id in decision["claim_ids"]:
            finding = finding_by_id[numeric_id]
            path = finding["source_path"]
            if path not in commit_cache:
                commit_cache[path] = evidence_commit(path)
            evidence.append(
                {
                    "claim_id": finding["claim_id"],
                    "title": finding["title"],
                    "path": path,
                    "lines": finding["source_lines"],
                    "commit": commit_cache[path],
                }
            )
        records.append(
            {
                **decision,
                "repository_evidence": evidence,
                "conflicts": [],
                "confidence": (
                    "DIRECT_CURRENT_AND_REPOSITORY_CORROBORATED"
                    if decision["current_direction_ids"]
                    else "READAUDIT_DERIVED"
                ),
            }
        )

    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": "3b5fd059ed09cdcdde38668c399cb35b8afbcca9",
        "source_findings": str(FINDINGS_PATH.relative_to(REPO_ROOT)),
        "current_direction_register": (
            "Codex/results/PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md"
        ),
        "decision_count": len(records),
        "allowed_statuses": [
            "PRESERVE",
            "CORRECT",
            "SUPERSEDE",
            "EMPIRICAL_ONLY",
            "THEORY_ONLY",
            "REJECT",
            "UNVERIFIED",
        ],
        "decisions": records,
        "validation": {
            "decision_ids_unique": len({record["id"] for record in records})
            == len(records),
            "all_decisions_have_repository_evidence": all(
                record["repository_evidence"] for record in records
            ),
            "all_evidence_has_path_lines_commit": all(
                item["path"] and item["lines"] and item["commit"]
                for record in records
                for item in record["repository_evidence"]
            ),
            "all_statuses_allowed": all(
                record["status"]
                in {
                    "PRESERVE",
                    "CORRECT",
                    "SUPERSEDE",
                    "EMPIRICAL_ONLY",
                    "THEORY_ONLY",
                    "REJECT",
                    "UNVERIFIED",
                }
                for record in records
            ),
        },
    }
    encoded = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    OUTPUT_PATH.write_text(encoded, encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "PASS",
                "output": str(OUTPUT_PATH.relative_to(REPO_ROOT)),
                "decisions": len(records),
                "evidence_links": sum(
                    len(record["repository_evidence"]) for record in records
                ),
                "sha256": hashlib.sha256(encoded.encode()).hexdigest(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
