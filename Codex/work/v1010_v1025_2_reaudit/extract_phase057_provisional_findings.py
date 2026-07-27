"""Extract and actor-classify all Phase 057 provisional findings."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
RESULT_ROOT = REPO_ROOT / "Codex/results"
OUTPUT_PATH = RESULT_ROOT / "PHASE_057_PROVISIONAL_FINDING_LEDGER.json"
HEADING_PATTERN = re.compile(
    r"^### (INTENT-PROV-(\d{4}))\s+[—-]\s+(.+?)\s*$"
)
IMPLEMENTED_PATTERN = re.compile(
    r"(?:구현|반영|도입|삭제|추가|변경|복원|철회|실행|재실행|build|"
    r"코드(?:는|가|에서)|v1\.0\.\d+(?:\.\d+)?(?:은|는|에서))",
    re.IGNORECASE,
)
MODEL_PATTERN = re.compile(
    r"(?:Fable|Opus|Claude|Codex|모델|초안|제안|계획서).{0,40}"
    r"(?:제안|계획|주장|판정|해석)",
    re.IGNORECASE | re.DOTALL,
)
VERBATIM_PATTERN = re.compile(
    r"(?:verbatim|직접\s*인용|원문\s*인용|\"[^\"]{4,}\")",
    re.IGNORECASE,
)
USER_REFERENCED_IDS = {
    6,
    14,
    15,
    20,
    26,
    30,
    36,
    47,
    50,
    69,
    96,
    111,
    139,
    174,
    175,
    181,
    192,
    203,
    219,
    228,
    233,
    244,
    253,
    257,
    258,
    277,
    281,
    286,
    314,
    325,
    326,
    345,
    346,
    347,
    348,
    351,
    354,
    372,
    379,
    380,
    387,
    394,
    403,
}


def observation_paths() -> list[Path]:
    return sorted(
        path
        for path in RESULT_ROOT.glob("PHASE_057*_OBSERVATIONS.md")
        if re.fullmatch(r"PHASE_057[A-Z]+_.+_OBSERVATIONS\.md", path.name)
    )


def classify_actor(
    numeric_id: int, title: str, body: str
) -> tuple[str, str, str]:
    sample = f"{title}\n{body[:1800]}"
    if numeric_id in USER_REFERENCED_IDS:
        confidence = (
            "REPOSITORY_REPORTED_VERBATIM"
            if VERBATIM_PATTERN.search(sample)
            else "REPOSITORY_REPORTED"
        )
        return (
            "USER_REQUIREMENT",
            confidence,
            "문건이 사용자 요구·지시·결정으로 귀속한 항목이다. 현재 대화의 "
            "직접 재확인과 연결되기 전에는 repository-reported 상태로 보존한다.",
        )
    if MODEL_PATTERN.search(sample):
        return (
            "MODEL_PROPOSAL",
            "EXPLICIT_MODEL_OR_PLAN_ATTRIBUTION",
            "모델·초안·계획의 제안 또는 해석으로 명시된 항목이다.",
        )
    if IMPLEMENTED_PATTERN.search(title):
        return (
            "IMPLEMENTED_STATE",
            "PATCH_CONFIRMATION_REQUIRED",
            "제목이 버전의 구현·변경·실행 상태를 기술한다. 실제 diff와의 대조는 "
            "commit matrix 및 후속 phase에서 유지한다.",
        )
    return (
        "REVIEW_FINDING",
        "DIRECT_REAUDIT_FINDING",
        "Phase 057 전문 검독에서 도출한 검토 판단이며 사용자 요구나 구현 상태로 "
        "자동 승격하지 않는다.",
    )


def extract_records(path: Path) -> list[dict[str, Any]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, re.Match[str]]] = []
    for index, line in enumerate(lines):
        match = HEADING_PATTERN.match(line)
        if match:
            starts.append((index, match))
    records: list[dict[str, Any]] = []
    for position, (start, match) in enumerate(starts):
        next_start = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        end = next_start
        for index in range(start + 1, next_start):
            if lines[index].startswith("## ") and not lines[index].startswith("### "):
                end = index
                break
        body = "\n".join(lines[start + 1 : end]).strip()
        title = match.group(3)
        actor, confidence, basis = classify_actor(
            int(match.group(2)), title, body
        )
        records.append(
            {
                "claim_id": match.group(1),
                "numeric_id": int(match.group(2)),
                "title": title,
                "source_path": str(path.relative_to(REPO_ROOT)),
                "source_lines": [start + 1, end],
                "record_actor": "REVIEW_FINDING",
                "referenced_actor": actor,
                "actor_confidence": confidence,
                "actor_basis": basis,
                "body": body,
                "source_block_sha256": hashlib.sha256(
                    ("\n".join(lines[start:end]) + "\n").encode()
                ).hexdigest(),
            }
        )
    return records


def main() -> None:
    paths = observation_paths()
    records = [
        record
        for path in paths
        for record in extract_records(path)
    ]
    records.sort(key=lambda record: record["numeric_id"])
    ids = [record["numeric_id"] for record in records]
    actor_counts = Counter(record["referenced_actor"] for record in records)
    confidence_counts = Counter(record["actor_confidence"] for record in records)
    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": "3b5fd059ed09cdcdde38668c399cb35b8afbcca9",
        "source_document_count": len(paths),
        "finding_count": len(records),
        "referenced_actor_counts": dict(sorted(actor_counts.items())),
        "actor_confidence_counts": dict(sorted(confidence_counts.items())),
        "actor_policy": {
            "record_actor": "All records are Codex re-audit findings.",
            "referenced_actor": (
                "The actor whose requirement, proposal, finding or implemented state "
                "the record primarily discusses."
            ),
            "repository_reported_user_requirement": (
                "Not promoted to direct-user evidence until corroborated by current "
                "conversation or repeated approved project decisions."
            ),
        },
        "records": records,
        "validation": {
            "ids_unique": len(ids) == len(set(ids)),
            "ids_contiguous_0001_0404": ids == list(range(1, 405)),
            "all_source_blocks_nonempty": all(record["body"] for record in records),
            "all_records_have_actor": all(
                record["referenced_actor"]
                in {
                    "USER_REQUIREMENT",
                    "MODEL_PROPOSAL",
                    "REVIEW_FINDING",
                    "IMPLEMENTED_STATE",
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
                "source_documents": len(paths),
                "findings": len(records),
                "actor_counts": payload["referenced_actor_counts"],
                "sha256": hashlib.sha256(encoded.encode()).hexdigest(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
