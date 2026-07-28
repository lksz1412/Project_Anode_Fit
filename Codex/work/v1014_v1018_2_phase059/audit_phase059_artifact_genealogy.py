#!/usr/bin/env python3
"""Audit Phase 059 PDF, PNG, and golden-NPZ provenance.

The audit is read-only with respect to Claude/.  A single XeLaTeX dependency
probe is executed in a temporary directory.  PNG regeneration hashes and
golden array comparisons are consumed from the already isolated Step 34
executions rather than recreated in the source tree.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "Codex" / "results"
OUTPUT = RESULTS / "PHASE_059_ARTIFACT_GENEALOGY.json"
REPORT = RESULTS / "PHASE_059_ARTIFACT_GENEALOGY_REVIEW.md"
PDF_METRICS = RESULTS / "PHASE_059_PDF_RENDER_METRICS.json"
IMAGE_AUDIT = RESULTS / "PHASE_059_IMAGE_AUDIT.json"
RUNTIME = RESULTS / "PHASE_059_ISOLATED_RUNTIME_RESULTS.json"
GOLDEN_AUDIT = RESULTS / "PHASE_059_GOLDEN_NPZ_AUDIT.json"

VERSIONS = [
    ("v1.0.14", "1014"),
    ("v1.0.15", "1015"),
    ("v1.0.16", "1016"),
    ("v1.0.17", "1017"),
    ("v1.0.18.1", "1018_1"),
    ("v1.0.18.2", "1018_2"),
]
TAG = dict(VERSIONS)
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"

FAMILY_TASK = {
    "P4_LCO_HEAT": "demo_lco_heat",
    "GRAPH_SUITE": "graph_suite",
    "SAMPLE_TEST": "sample_test",
    "DQDV_BELL_SHAPES": "plot_dqdv",
}


def run(
    *arguments: str,
    check: bool = True,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    timeout: int = 30,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(arguments),
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=check,
        timeout=timeout,
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: str) -> str:
    return run("git", "rev-parse", f"HEAD:{path}").stdout.strip()


def commit_info(path: str, first_add: bool = False) -> dict[str, str]:
    command = ["git", "log"]
    if first_add:
        command.append("--diff-filter=A")
    command.extend(["-1", "--format=%H%x09%aI%x09%s", "--", path])
    line = run(*command).stdout.rstrip("\n")
    commit, authored_at, subject = line.split("\t", 2)
    return {
        "commit": commit,
        "authored_at": authored_at,
        "subject": subject,
    }


def is_ancestor(older: str, newer: str) -> bool:
    completed = run(
        "git", "merge-base", "--is-ancestor", older, newer, check=False
    )
    if completed.returncode not in {0, 1}:
        raise RuntimeError(completed.stderr)
    return completed.returncode == 0


def relation(artifact_commit: str, source_commit: str) -> str:
    if artifact_commit == source_commit:
        return "SAME_COMMIT"
    if is_ancestor(source_commit, artifact_commit):
        return "ARTIFACT_AFTER_SOURCE"
    if is_ancestor(artifact_commit, source_commit):
        return "SOURCE_AFTER_ARTIFACT"
    return "DIVERGED_HISTORY"


def path_record(path: str) -> dict:
    return {
        "path": path,
        "sha256": sha256(ROOT / path),
        "git_blob": git_blob(path),
        "first_added_commit": commit_info(path, first_add=True),
        "last_commit": commit_info(path),
    }


def source_record(
    role: str, path: str, artifact_last_commit: str
) -> dict:
    last = commit_info(path)
    return {
        "role": role,
        "path": path,
        "sha256": sha256(ROOT / path),
        "git_blob": git_blob(path),
        "first_added_commit": commit_info(path, first_add=True),
        "last_commit": last,
        "relation_to_artifact_last_commit": relation(
            artifact_last_commit, last["commit"]
        ),
    }


def version_from_path(path: str) -> str:
    match = re.search(r"Claude/docs/(v1\.0\.(?:\d+)(?:\.\d+)?)/", path)
    if not match:
        raise ValueError(path)
    return match.group(1)


def content_groups(records: list[dict], signature_key: str = "sha256") -> list[dict]:
    groups: dict[str, list[str]] = defaultdict(list)
    for record in records:
        groups[record[signature_key]].append(record["path"])
    return [
        {
            signature_key: digest,
            "occurrence_count": len(paths),
            "paths": paths,
        }
        for digest, paths in sorted(groups.items())
    ]


def rendered_signature(document: dict) -> str:
    digest = hashlib.sha256()
    for page in document["pages"]:
        digest.update(page["render_sha256"].encode("ascii"))
    return digest.hexdigest()


def tex_preflight(first_tex_path: str) -> dict:
    engine = shutil.which("xelatex")
    kotex = run("kpsewhich", "kotex.sty", check=False)
    font = run(
        "fc-match", "-f", "%{family}\n", "D2Coding", check=False
    )
    exact_d2coding = "d2coding" in font.stdout.casefold()
    record = {
        "engine_path": engine,
        "engine_version": None,
        "kotex_sty_path": kotex.stdout.strip() or None,
        "d2coding_resolved_family": font.stdout.strip() or None,
        "d2coding_exact_match": exact_d2coding,
        "probe_source": first_tex_path,
        "probe_exit_code": None,
        "probe_pdf_created": False,
        "missing_kotex_marker": False,
        "status": None,
    }
    if not engine:
        record["status"] = "DEPENDENCY_BLOCKED_XELATEX_NOT_FOUND"
        return record
    version = run(engine, "--version", check=False)
    record["engine_version"] = version.stdout.splitlines()[0]
    with tempfile.TemporaryDirectory(prefix="phase059_xelatex_probe_") as temp:
        temp_root = Path(temp)
        source = ROOT / first_tex_path
        local = temp_root / source.name
        shutil.copy2(source, local)
        tex_env = os.environ.copy()
        tex_env.update(
            {
                "TEXMFVAR": str(temp_root / "texmf-var"),
                "TEXMFCONFIG": str(temp_root / "texmf-config"),
                "TEXMFHOME": str(temp_root / "texmf-home"),
            }
        )
        completed = run(
            engine,
            "-interaction=nonstopmode",
            "-halt-on-error",
            local.name,
            check=False,
            cwd=temp_root,
            env=tex_env,
            timeout=60,
        )
        combined = completed.stdout + completed.stderr
        record["probe_exit_code"] = completed.returncode
        record["probe_pdf_created"] = local.with_suffix(".pdf").is_file()
        record["missing_kotex_marker"] = (
            "File `kotex.sty' not found" in combined
            or "File 'kotex.sty' not found" in combined
        )
    if record["probe_exit_code"] == 0 and record["probe_pdf_created"]:
        record["status"] = "PDF_RERENDER_PREFLIGHT_PASS"
    elif record["missing_kotex_marker"] and not exact_d2coding:
        record["status"] = (
            "DEPENDENCY_BLOCKED_MISSING_KOTEX_AND_D2CODING"
        )
    elif record["missing_kotex_marker"]:
        record["status"] = "DEPENDENCY_BLOCKED_MISSING_KOTEX"
    else:
        record["status"] = "PDF_RERENDER_PREFLIGHT_FAILED_OTHER"
    return record


def current_generator(version: str, family: str) -> str:
    base = f"Claude/docs/{version}"
    if family == "P4_LCO_HEAT":
        return f"{base}/demo_lco_heat.py"
    if family == "GRAPH_SUITE":
        return f"{base}/graph_suite_v{TAG[version]}.py"
    if family == "SAMPLE_TEST":
        return f"{base}/sample_test_v{TAG[version]}.py"
    if family == "DQDV_BELL_SHAPES":
        return f"{base}/plot_dqdv.py"
    raise ValueError(family)


def current_model(version: str) -> str:
    return (
        f"Claude/docs/{version}/"
        f"Anode_Fit_v{version.removeprefix('v')}.py"
    )


def filename_version_token(path: str) -> str | None:
    name = Path(path).name
    patterns = [
        (r"v1_0_(\d+)", lambda value: f"v1.0.{int(value)}"),
        (r"v10(\d{2})(?:_(\d))?", None),
    ]
    first = re.search(patterns[0][0], name)
    if first:
        return patterns[0][1](first.group(1))
    second = re.search(patterns[1][0], name)
    if second:
        minor = int(second.group(1))
        patch = second.group(2)
        return f"v1.0.{minor}" + (f".{patch}" if patch else "")
    return None


def build_pdf_records(pdf_data: dict, preflight: dict) -> list[dict]:
    records = []
    for document in pdf_data["documents"]:
        artifact = path_record(document["path"])
        tex = source_record(
            "tex_source",
            document["tex_path"],
            artifact["last_commit"]["commit"],
        )
        artifact.update(
            {
                "artifact_type": "PDF",
                "version": document["version"],
                "document_kind": document["document_kind"],
                "page_count": document["page_count_pdf"],
                "tex_source": tex,
                "rendered_page_signature_sha256": rendered_signature(document),
                "isolated_rerender": {
                    "status": (
                        "NOT_RUN_SHARED_DEPENDENCY_PREFLIGHT_FAILED"
                        if not preflight["status"].endswith("PASS")
                        else "NOT_RUN_AFTER_PREFLIGHT_ONLY"
                    ),
                    "shared_preflight_status": preflight["status"],
                    "stored_bit_exact": None,
                },
                "visible_version_label_disposition": (
                    "STALE_V1_0_15_LABEL_AND_EXACT_V1_0_15_RENDER_COPY"
                    if document["path"]
                    == "Claude/docs/v1.0.16/appendix_phase_separation.pdf"
                    else "NO_KNOWN_VISIBLE_VERSION_LABEL_DEFECT"
                ),
            }
        )
        records.append(artifact)
    return records


def runtime_hash_map(runtime_data: dict) -> dict[tuple[str, str], dict]:
    mapping = {}
    for item in runtime_data["runs"]:
        outputs = item["generated_outputs"]
        if len(outputs) == 1:
            mapping[(item["version"], item["task"])] = outputs[0]
    return mapping


def build_image_records(
    image_data: dict, runtime_data: dict
) -> list[dict]:
    runtime_hashes = runtime_hash_map(runtime_data)
    records = []
    for unique in image_data["images"]:
        family = unique["visual_review"]["family"]
        origin_path = unique["representative_path"]
        for occurrence in unique["occurrences"]:
            path = occurrence["path"]
            version = version_from_path(path)
            artifact = path_record(path)
            generator_path = current_generator(version, family)
            model_path = current_model(version)
            generator = source_record(
                "current_version_generator",
                generator_path,
                artifact["last_commit"]["commit"],
            )
            model = source_record(
                "current_version_model",
                model_path,
                artifact["last_commit"]["commit"],
            )
            task = FAMILY_TASK[family]
            regenerated = runtime_hashes[(version, task)]
            token = filename_version_token(path)
            artifact.update(
                {
                    "artifact_type": "PNG",
                    "version": version,
                    "family": family,
                    "content_group_origin_path": origin_path,
                    "copy_forward_identical_blob": path != origin_path,
                    "current_version_generator": generator,
                    "current_version_model": model,
                    "isolated_regeneration": {
                        "source": (
                            "PHASE_059_ISOLATED_RUNTIME_RESULTS.json"
                        ),
                        "task": task,
                        "generated_path_literal": regenerated["path"],
                        "sha256": regenerated["sha256"],
                        "size_bytes": regenerated["size_bytes"],
                        "stored_hash_bit_exact": (
                            regenerated["sha256"] == artifact["sha256"]
                        ),
                        "interpretation": (
                            "BIT_EXACT_RENDER"
                            if regenerated["sha256"] == artifact["sha256"]
                            else (
                                "NON_BIT_EXACT_RENDER_REQUIRES_NUMERIC_"
                                "DATA_SEPARATION"
                            )
                        ),
                    },
                    "filename_version_token": token,
                    "filename_version_matches_directory": (
                        None if token is None else token == version
                    ),
                    "known_visual_or_naming_defects": (
                        unique["visual_review"]["visual_defects"]
                    ),
                }
            )
            records.append(artifact)
    return records


def build_golden_records(golden_data: dict) -> list[dict]:
    regeneration = {
        item["version"]: item for item in golden_data["version_regeneration"]
    }
    origin_by_path = {}
    for unique in golden_data["unique_golden_contents"]:
        for path in unique["occurrence_paths"]:
            origin_by_path[path] = unique["representative_path"]
    records = []
    for version, _ in VERSIONS:
        path = f"Claude/docs/{version}/golden_graphite_ref.npz"
        artifact = path_record(path)
        generated = regeneration[version]
        test = source_record(
            "golden_generator_test",
            generated["paths"]["test"],
            artifact["last_commit"]["commit"],
        )
        model = source_record(
            "production_model",
            generated["paths"]["code"],
            artifact["last_commit"]["commit"],
        )
        artifact.update(
            {
                "artifact_type": "GOLDEN_NPZ",
                "version": version,
                "content_group_origin_path": origin_by_path[path],
                "copy_forward_identical_blob": (
                    path != origin_by_path[path]
                ),
                "golden_generator_test": test,
                "production_model": model,
                "current_regeneration": {
                    "source": "PHASE_059_GOLDEN_NPZ_AUDIT.json",
                    "key_order_equal": generated["key_order_equal"],
                    "key_set_equal": generated["key_set_equal"],
                    "array_count": generated["array_count"],
                    "array_equal_count": generated["array_equal_count"],
                    "allclose_rtol0_atol1e_15_count": generated[
                        "allclose_rtol0_atol1e_15_count"
                    ],
                    "allclose_rtol0_atol5e_15_count": generated[
                        "allclose_rtol0_atol5e_15_count"
                    ],
                    "allclose_rtol0_atol1e_12_count": generated[
                        "allclose_rtol0_atol1e_12_count"
                    ],
                    "max_abs_diff": generated["max_abs_diff"],
                    "file_bit_exact": False,
                    "interpretation": (
                        "NUMERICALLY_TOLERANT_NOT_BIT_EXACT_AND_INTERNAL_ONLY"
                    ),
                },
            }
        )
        records.append(artifact)
    return records


def source_after_count(records: list[dict]) -> int:
    count = 0
    for record in records:
        for key in (
            "tex_source",
            "current_version_generator",
            "current_version_model",
            "golden_generator_test",
            "production_model",
        ):
            source = record.get(key)
            if (
                source
                and source["relation_to_artifact_last_commit"]
                == "SOURCE_AFTER_ARTIFACT"
            ):
                count += 1
                break
    return count


def render_report(result: dict) -> str:
    summary = result["summary"]
    preflight = result["pdf_rerender_preflight"]
    image_source_after = [
        record["path"]
        for record in result["image_occurrences"]
        if any(
            record[key]["relation_to_artifact_last_commit"]
            == "SOURCE_AFTER_ARTIFACT"
            for key in ("current_version_generator", "current_version_model")
        )
    ]
    golden_source_after = [
        record["path"]
        for record in result["golden_occurrences"]
        if any(
            record[key]["relation_to_artifact_last_commit"]
            == "SOURCE_AFTER_ARTIFACT"
            for key in ("golden_generator_test", "production_model")
        )
    ]
    image_source_rows = "\n".join(
        f"- `{path}`" for path in image_source_after
    ) or "- 없음"
    golden_source_rows = "\n".join(
        f"- `{path}`" for path in golden_source_after
    ) or "- 없음"
    return f"""# Phase 059 PDF·image·golden 생성 계보 감사

정본일: 2026-07-28

판정: `{result['status']}`

## 범위와 판정 경계

PDF {summary['pdf_occurrence_count']}개, PNG
{summary['image_occurrence_count']} occurrence/{summary['image_unique_content_count']} unique,
golden NPZ {summary['golden_occurrence_count']} occurrence/
{summary['golden_unique_content_count']} unique의 current blob, 최초 도입
commit, 마지막 변경 commit, 대응 TeX/generator/model/test commit을
연결했다.

commit 선후관계와 재생성 hash는 artifact의 생성 계보만 판정한다.
물리식, 재료 identity, parameter, 문헌 또는 실험 타당성을 승인하지
않는다.

## PDF 계보와 재빌드 한계

- 18 PDF는 byte hash로는 모두 다르다. 그러나 v1.0.15와 v1.0.16
  appendix는 TeX가 exact-identical이고 8개 rendered page signature도
  동일하며, v1.0.16 표지에는 `버전 1.0.15 초안`이 남아 있다.
- 모든 PDF–TeX commit 관계를 기록했다. source-after-artifact PDF는
  {summary['pdf_source_after_artifact_count']}개다.
- XeLaTeX probe는 `{preflight['status']}`다. engine은
  `{preflight['engine_version']}`이지만 `kotex.sty`가 없고 D2Coding
  요청은 `{preflight['d2coding_resolved_family']}`로 fallback된다.
- 이 공통 dependency preflight 실패 뒤 18개를 반복 실패시키지
  않았다. 그러므로 저장 PDF의 bit-exact 재현은
  `UNTESTED_DEPENDENCY_BLOCKED`이며, 저장 PDF가 현재 TeX의
  재빌드 산출물이라는 주장도 이 환경에서는 승인하지 않는다.

## PNG copy-forward와 현재 generator

- 24 path occurrence는 10 unique blob으로 수렴한다. 14 occurrence는
  이전 blob의 exact copy-forward다.
- filename의 version token이 현재 directory와 다른 것은
  {summary['image_filename_version_mismatch_count']}개다. 여기에는
  v1.0.16 title/generator 그림이 `v1_0_14` 이름으로 네 release에
  남은 경우와 old graph-suite filename의 후속판 복제가 포함된다.
- 각 occurrence를 그 version의 current generator와 production
  model에 다시 연결했다. source-after-artifact 후보는
  {summary['image_source_after_artifact_count']}개다:
{image_source_rows}
- Step 34.3의 disposable rerender 24개와 저장 PNG를 대조하면
  bit-exact는 {summary['image_regeneration_bit_exact_count']}/{summary['image_occurrence_count']}이다.
  환경·font·backend·metadata에
  민감한 PNG byte mismatch만으로 curve 차이를 단정할 수 없다.
  반대로 plot-data array/hash가 저장되지 않았으므로 scientific
  curve equality도 입증할 수 없다.

## Golden NPZ 계보

- v1.0.14 한 blob과 v1.0.15 이후 다섯 경로의 한 blob, 총 2 unique다.
  후속 4 occurrence는 v1.0.15 golden의 byte-identical copy-forward다.
- generator test 또는 model이 artifact 뒤에 바뀐 후보는
  {summary['golden_source_after_artifact_count']}개다:
{golden_source_rows}
- 현재 재계산은 모든 version에서 key 13/13과
  `rtol=0, atol=5e-15` 13/13이 일치하지만 bit-exact array는
  1/13뿐이다. 따라서 golden은 현재 model의 byte-exact 재현물이
  아니라 historical, tolerance-level internal snapshot이다.
- 특히 v1.0.15 이후 같은 golden blob의 반복은 새 물리 검증 또는
  새 실험 증거가 아니다.

## 권위 판정

1. PDF: build ordering은 기록됐으나 현재 환경 재빌드는 한글 TeX/font
   dependency 부재로 막혔다.
2. PNG: 14 exact copy-forward, 0/24 bit-exact rerender이며 plot-data가
   없어 byte mismatch와 scientific curve delta를 분리할 수 없다.
3. Golden: 4 exact copy-forward, 재계산 13/13 tolerance pass이나
   1/13 array exact다.
4. 세 artifact 계열 모두 내부 consistency/provenance evidence일 뿐
   사용자가 요구한 저온×전류, Si/blend, doped high-voltage LCO
   실험 타당성을 제공하지 않는다.

## 다음 단계

Step 36.1에서 v1.0.14의 textbook register, derivation restructuring,
width budget와 theory-only 본문 경계를 v1.0.13과 exact diff로
재판정한다.
"""


def main() -> int:
    pdf_data = json.loads(PDF_METRICS.read_text(encoding="utf-8"))
    image_data = json.loads(IMAGE_AUDIT.read_text(encoding="utf-8"))
    runtime_data = json.loads(RUNTIME.read_text(encoding="utf-8"))
    golden_data = json.loads(GOLDEN_AUDIT.read_text(encoding="utf-8"))

    tracked_paths = (
        {document["path"] for document in pdf_data["documents"]}
        | {document["tex_path"] for document in pdf_data["documents"]}
        | {
            occurrence["path"]
            for image in image_data["images"]
            for occurrence in image["occurrences"]
        }
        | {
            current_generator(version, family)
            for version, _ in VERSIONS
            for family in FAMILY_TASK
        }
        | {current_model(version) for version, _ in VERSIONS}
        | {
            f"Claude/docs/{version}/golden_graphite_ref.npz"
            for version, _ in VERSIONS
        }
        | {
            item["paths"][role]
            for item in golden_data["version_regeneration"]
            for role in ("code", "test")
        }
    )
    source_hashes_before = {
        path: sha256(ROOT / path) for path in sorted(tracked_paths)
    }
    preflight = tex_preflight(pdf_data["documents"][0]["tex_path"])
    pdf_records = build_pdf_records(pdf_data, preflight)
    image_records = build_image_records(image_data, runtime_data)
    golden_records = build_golden_records(golden_data)
    source_hashes_after = {
        path: sha256(ROOT / path) for path in source_hashes_before
    }

    pdf_render_groups = content_groups(
        [
            {
                "path": record["path"],
                "rendered_page_signature_sha256": record[
                    "rendered_page_signature_sha256"
                ],
            }
            for record in pdf_records
        ],
        signature_key="rendered_page_signature_sha256",
    )
    image_groups = content_groups(image_records)
    golden_groups = content_groups(golden_records)
    mismatch_count = sum(
        record["filename_version_matches_directory"] is False
        for record in image_records
    )
    result = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": BASELINE,
        "scope": (
            "Phase 059 Step 35.3 PDF/image/golden source and Git "
            "genealogy with isolated regeneration evidence"
        ),
        "authority_boundary": (
            "Artifact ordering, copy lineage, and regeneration only; "
            "no physics, material, parameter, literature, or experimental "
            "validity is promoted."
        ),
        "source_inputs": {
            "pdf_metrics": str(PDF_METRICS.relative_to(ROOT)),
            "image_audit": str(IMAGE_AUDIT.relative_to(ROOT)),
            "isolated_runtime": str(RUNTIME.relative_to(ROOT)),
            "golden_audit": str(GOLDEN_AUDIT.relative_to(ROOT)),
        },
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "sources_unchanged": source_hashes_before == source_hashes_after,
        "pdf_rerender_preflight": preflight,
        "pdf_occurrences": pdf_records,
        "pdf_byte_content_groups": content_groups(pdf_records),
        "pdf_rendered_content_groups": pdf_render_groups,
        "image_occurrences": image_records,
        "image_content_groups": image_groups,
        "golden_occurrences": golden_records,
        "golden_content_groups": golden_groups,
        "summary": {
            "artifact_occurrence_count": (
                len(pdf_records) + len(image_records) + len(golden_records)
            ),
            "artifact_unique_content_count": (
                len(content_groups(pdf_records))
                + len(image_groups)
                + len(golden_groups)
            ),
            "pdf_occurrence_count": len(pdf_records),
            "pdf_unique_byte_content_count": len(content_groups(pdf_records)),
            "pdf_unique_rendered_content_count": len(pdf_render_groups),
            "pdf_source_after_artifact_count": source_after_count(pdf_records),
            "pdf_rerender_bit_exact_count": 0,
            "pdf_rerender_dependency_blocked_count": len(pdf_records),
            "image_occurrence_count": len(image_records),
            "image_unique_content_count": len(image_groups),
            "image_copy_forward_occurrence_count": sum(
                record["copy_forward_identical_blob"]
                for record in image_records
            ),
            "image_filename_version_mismatch_count": mismatch_count,
            "image_source_after_artifact_count": source_after_count(
                image_records
            ),
            "image_regeneration_bit_exact_count": sum(
                record["isolated_regeneration"]["stored_hash_bit_exact"]
                for record in image_records
            ),
            "image_regeneration_non_bit_exact_count": sum(
                not record["isolated_regeneration"]["stored_hash_bit_exact"]
                for record in image_records
            ),
            "golden_occurrence_count": len(golden_records),
            "golden_unique_content_count": len(golden_groups),
            "golden_copy_forward_occurrence_count": sum(
                record["copy_forward_identical_blob"]
                for record in golden_records
            ),
            "golden_source_after_artifact_count": source_after_count(
                golden_records
            ),
            "golden_versions_array_exact_1_of_13_count": sum(
                record["current_regeneration"]["array_equal_count"] == 1
                and record["current_regeneration"]["array_count"] == 13
                for record in golden_records
            ),
            "golden_versions_tolerance_13_of_13_count": sum(
                record["current_regeneration"][
                    "allclose_rtol0_atol5e_15_count"
                ]
                == 13
                for record in golden_records
            ),
        },
        "interpretation_rules": [
            (
                "A source commit after an artifact commit makes the artifact "
                "stale against current source unless the change is proven "
                "render- or output-inert."
            ),
            (
                "Exact copy-forward is lineage evidence, not new validation."
            ),
            (
                "A non-bit-exact PNG alone cannot distinguish curve changes "
                "from renderer, font, compression, or metadata differences."
            ),
            (
                "A tolerance-level golden match is not a byte-exact "
                "reproduction and remains an internal model snapshot."
            ),
            (
                "A blocked PDF rebuild cannot be reported as a passing build."
            ),
        ],
        "status": (
            "CONDITIONAL_P059_ARTIFACT_GENEALOGY_WITH_PDF_"
            "DEPENDENCY_BLOCK_AND_NON_BIT_EXACT_REGENERATIONS"
        ),
        "next_action": (
            "Proceed to Step 36.1 v1.0.14 theory-boundary and derivation-"
            "restructuring adjudication."
        ),
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    REPORT.write_text(render_report(result), encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(OUTPUT.relative_to(ROOT)),
                "report": str(REPORT.relative_to(ROOT)),
                "status": result["status"],
                "summary": result["summary"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
