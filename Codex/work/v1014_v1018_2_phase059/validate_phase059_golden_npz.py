#!/usr/bin/env python3
"""Validate Phase 059 Step 34.5 golden NPZ and rebaseline audit."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "Codex" / "results"
OUTPUT = RESULTS / "PHASE_059_GOLDEN_NPZ_AUDIT.json"
REVIEW = RESULTS / "PHASE_059_GOLDEN_NPZ_REVIEW.md"
RUNNER = (
    ROOT
    / "Codex"
    / "work"
    / "v1014_v1018_2_phase059"
    / "audit_phase059_golden_npz.py"
)
VERSIONS = [
    "v1.0.14",
    "v1.0.15",
    "v1.0.16",
    "v1.0.17",
    "v1.0.18.1",
    "v1.0.18.2",
]
EXPECTED_KEYS = [
    "V",
    "equilibrium_298",
    "dqdv_dis_I0.02",
    "dqdv_dis_I0.2",
    "dqdv_dis_I1.0",
    "dqdv_chg_I0.02",
    "dqdv_chg_I0.2",
    "dqdv_chg_I1.0",
    "dqdv_T258",
    "dqdv_T298",
    "dqdv_T318",
    "dqdv_TV",
    "curve_dis_02C",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    checks: list[tuple[str, bool]] = []
    checks.append(("result exists", OUTPUT.is_file()))
    checks.append(("review exists", REVIEW.is_file()))
    result = json.loads(OUTPUT.read_text(encoding="utf-8"))

    checks.append(
        (
            "status conditional",
            result["status"] == "CONDITIONAL_P059_GOLDEN_NPZ",
        )
    )
    checks.append(
        (
            "execution gate exact",
            result["execution_gate"]
            == "PASS_P059_GOLDEN_NPZ_AUDIT_EXECUTION",
        )
    )
    checks.append(("source unchanged", result["sources_unchanged"] is True))
    checks.append(
        (
            "source hashes stable",
            result["source_sha256_before"] == result["source_sha256_after"],
        )
    )
    checks.append(
        (
            "source hashes current",
            all(
                digest == sha256(ROOT / relative)
                for relative, digest in result["source_sha256_after"].items()
            ),
        )
    )
    checks.append(("version count", result["version_count"] == 6))
    checks.append(
        ("golden occurrence count", result["golden_occurrence_count"] == 6)
    )
    checks.append(
        (
            "two unique golden contents",
            result["unique_golden_content_count"] == 2
            and len(result["unique_golden_contents"]) == 2,
        )
    )
    unique = result["unique_golden_contents"]
    checks.append(
        (
            "occurrence multiplicities",
            sorted(item["occurrence_count"] for item in unique) == [1, 5],
        )
    )
    checks.append(
        (
            "unique content hashes current",
            all(
                item["file_sha256"]
                == sha256(ROOT / item["representative_path"])
                for item in unique
            ),
        )
    )
    checks.append(
        (
            "key orders exact",
            all(item["key_order"] == EXPECTED_KEYS for item in unique),
        )
    )
    checks.append(
        (
            "array/member counts",
            all(
                item["key_count"] == 13
                and len(item["arrays"]) == 13
                and len(item["zip_members"]) == 13
                for item in unique
            ),
        )
    )
    checks.append(
        (
            "array structure finite",
            all(
                array["shape"] == [1000]
                and array["dtype"] == "float64"
                and array["element_count"] == 1000
                and array["nbytes"] == 8000
                and array["finite_count"] == 1000
                and array["nan_count"] == 0
                and array["positive_inf_count"] == 0
                and array["negative_inf_count"] == 0
                for item in unique
                for array in item["arrays"]
            ),
        )
    )

    pair = result["golden_pair"]
    checks.append(
        (
            "pair key contract",
            pair["key_order_equal"] is True
            and pair["key_set_equal"] is True
            and pair["array_count"] == 13,
        )
    )
    checks.append(
        (
            "pair two unchanged eleven changed",
            pair["array_equal_count"] == 2
            and pair["changed_array_count"] == 11
            and [
                item["key"] for item in pair["arrays"] if item["array_equal"]
            ]
            == ["V", "equilibrium_298"],
        )
    )
    checks.append(
        (
            "pair architecture difference scale",
            3.9e-5 < pair["max_abs_diff"] < 4.0e-5,
        )
    )
    checks.append(
        (
            "all changed pair arrays differ at every element",
            all(
                item["unequal_element_count"] == 1000
                for item in pair["arrays"]
                if not item["array_equal"]
            ),
        )
    )

    regeneration = result["version_regeneration"]
    checks.append(
        (
            "regeneration versions exact",
            [item["version"] for item in regeneration] == VERSIONS,
        )
    )
    checks.append(
        (
            "regeneration key sets",
            all(
                item["key_order_equal"]
                and item["key_set_equal"]
                and item["generated_key_order"] == EXPECTED_KEYS
                and item["golden_key_order"] == EXPECTED_KEYS
                for item in regeneration
            ),
        )
    )
    checks.append(
        (
            "strict exact one per version",
            all(
                item["array_count"] == 13
                and item["array_equal_count"] == 1
                for item in regeneration
            ),
        )
    )
    checks.append(
        (
            "tolerance thirteen per version",
            all(
                item["allclose_rtol0_atol1e_12_count"] == 13
                for item in regeneration
            ),
        )
    )
    checks.append(
        (
            "runtime differences tiny nonzero",
            0.0
            < max(item["max_abs_diff"] for item in regeneration)
            < 5.0e-15,
        )
    )
    checks.append(
        (
            "regeneration arrays structurally equal",
            all(
                len(item["arrays"]) == 13
                and all(row["shape_equal"] for row in item["arrays"])
                and all(row["dtype_equal"] for row in item["arrays"])
                for item in regeneration
            ),
        )
    )

    rebaseline = result["v1015_rebaseline"]
    checks.append(
        (
            "rebaseline commit exact",
            rebaseline["commit"]
            == "03dab9221d9b017501a1a9d391ce8825dd440106"
            and rebaseline["parent"]
            == "da83d03efc536937089fa42fe42c3d52333e970a",
        )
    )
    checks.append(
        (
            "rebaseline changed code and golden only",
            rebaseline["selected_changed_paths"]
            == [
                "M\tClaude/docs/v1.0.15/Anode_Fit_v1.0.15.py",
                "M\tClaude/docs/v1.0.15/golden_graphite_ref.npz",
            ],
        )
    )
    checks.append(
        (
            "rebaseline mutation flags",
            rebaseline["code_changed_in_rebaseline_commit"] is True
            and rebaseline["golden_changed_in_rebaseline_commit"] is True
            and rebaseline["test_harness_changed_in_rebaseline_commit"] is False,
        )
    )
    checks.append(
        (
            "pre post golden lineage",
            rebaseline["pre_golden_equals_v1014_golden"] is True
            and rebaseline["post_golden_equals_v1015_current_file"] is True
            and rebaseline["golden_sha256_before"] == pair["left_sha256"]
            and rebaseline["golden_sha256_after"] == pair["right_sha256"],
        )
    )
    delta = result["rebaseline_delta_alignment"]
    checks.append(
        (
            "rebaseline delta alignment",
            delta["array_count"] == 13
            and 0.0 < delta["max_delta_mismatch"] < 5.0e-15,
        )
    )
    checks.append(
        (
            "zero deltas remain zero",
            all(
                item["golden_delta_max_abs"] == 0.0
                and item["current_delta_max_abs"] == 0.0
                and item["delta_max_abs_difference"] == 0.0
                for item in delta["arrays"][:2]
            ),
        )
    )
    checks.append(
        (
            "changed deltas aligned",
            all(
                item["golden_delta_max_abs"] > 1.0e-5
                and item["current_delta_max_abs"] > 1.0e-5
                and item["delta_max_abs_difference"] < 5.0e-15
                for item in delta["arrays"][2:]
            ),
        )
    )

    copy_forward = result["post_rebaseline_current_copy_forward"]
    checks.append(
        (
            "copy-forward comparisons exact",
            len(copy_forward) == 4
            and [item["right"] for item in copy_forward]
            == ["v1.0.16", "v1.0.17", "v1.0.18.1", "v1.0.18.2"]
            and all(
                item["array_equal_count"] == item["array_count"] == 13
                and item["max_abs_diff"] == 0.0
                for item in copy_forward
            ),
        )
    )

    coverage = result["coverage_and_authority"]
    checks.append(
        (
            "one normalized harness family",
            coverage["normalized_logic_family_count"] == 1
            and len(
                set(
                    coverage["normalized_harness_sha256_by_version"].values()
                )
            )
            == 1,
        )
    )
    checks.append(
        (
            "headline tokens absent",
            all(
                count == 0
                for count in coverage[
                    "token_occurrences_all_harnesses"
                ].values()
            ),
        )
    )
    checks.append(
        (
            "evidence class exact",
            coverage["evidence_class"] == "DERIVED_MODEL_OUTPUT_SNAPSHOT",
        )
    )
    checks.append(
        (
            "external authority absent",
            coverage["contains_experimental_observation"] is False
            and coverage["contains_optimizer_state"] is False
            and coverage[
                "contains_parameter_covariance_or_uncertainty"
            ]
            is False
            and coverage["contains_lco_output"] is False,
        )
    )
    checks.append(
        (
            "critical unit history coverage absent",
            coverage["contains_si_coulomb_capacity_case"] is False
            and coverage["contains_nonmonotone_or_reversal_history"] is False,
        )
    )
    checks.append(
        (
            "findings exact",
            [item["finding_id"] for item in result["findings"]]
            == [
                "GOLD-001",
                "GOLD-002",
                "GOLD-003",
                "GOLD-004",
                "GOLD-005",
                "GOLD-006",
            ],
        )
    )
    checks.append(
        (
            "next step exact",
            result["next_step"] == "35.1",
        )
    )

    review = REVIEW.read_text(encoding="utf-8")
    checks.append(
        (
            "review authority boundary",
            "독립 oracle이 아니다" in review
            and "DERIVED_MODEL_OUTPUT_SNAPSHOT" in review
            and "실험 데이터나 저장된 fit/optimizer" in review,
        )
    )
    checks.append(
        (
            "review records rebaseline",
            "pointwise-memory code 변경 commit" in review
            and "11개 curve가 새 pointwise architecture 출력으로 재정초" in review,
        )
    )

    before = (sha256(OUTPUT), sha256(REVIEW))
    completed = subprocess.run(
        [sys.executable, "-W", "error::SyntaxWarning", str(RUNNER)],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    after = (sha256(OUTPUT), sha256(REVIEW))
    checks.append(("runner rerun exits zero", completed.returncode == 0))
    checks.append(("runner rerun clean stderr", completed.stderr == ""))
    checks.append(("result and review deterministic", before == after))
    claude_status = subprocess.run(
        ["git", "status", "--porcelain", "--", "Claude"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    ).stdout
    checks.append(("Claude tree untouched", claude_status == ""))

    failures = [name for name, passed in checks if not passed]
    for name, passed in checks:
        print(f"{'PASS' if passed else 'FAIL'} {name}")
    if failures:
        raise SystemExit("FAIL_P059_GOLDEN_NPZ: " + ", ".join(failures))
    print(f"PASS_P059_GOLDEN_NPZ {len(checks)}/{len(checks)}")


if __name__ == "__main__":
    main()
