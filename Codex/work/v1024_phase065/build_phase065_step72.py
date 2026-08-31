#!/usr/bin/env python3
"""Build the deterministic Phase 065 Step 72 authority matrix.

Only immutable Git blobs are read.  Frozen Python is never imported or run.
External metadata recorded here was independently queried by the controller;
the builder performs no network access and grants metadata identity only.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import tempfile

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "5978da8626406879609b0dd5792f79143015e67f"
GATE = "PASS_P065_STEP72_AUTHORITY_WITH_CONCERNS"
DEFAULT_OUTPUT = Path("Codex/results/PHASE_065_SKEW_MATERIAL_AUTHORITY_MATRIX.json")
RESULT = Path("Codex/results/PHASE_065_STEP_072_SKEW_MATERIAL_AUTHORITY_RESULT.md")
VALIDATOR = Path("Codex/work/v1024_phase065/validate_phase065_step72.py")
CONTROL_PATHS = sorted([
    "Codex/work/v1024_phase065/build_phase065_step72.py",
    "Codex/work/v1024_phase065/validate_phase065_step72.py",
    "Codex/results/PHASE_065_STEP_072_SKEW_MATERIAL_AUTHORITY_RESULT.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
])


def run_process(argv: list[str], *, text: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(argv, check=True, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, text=text,
                        encoding="utf-8" if text else None)


def git(*args: str, text: bool = True) -> str | bytes:
    cp = run_process(["git", *args], text=text)
    return cp.stdout


def blob(path: str, rev: str = BASELINE) -> bytes:
    return git("show", f"{rev}:{path}", text=False)  # type: ignore[return-value]


def first_json_fence(path: str, rev: str) -> dict:
    text = blob(path, rev).decode("utf-8")
    marker = "```json"
    if marker not in text:
        raise SystemExit(f"missing JSON fence in {path}")
    payload = text.split(marker, 1)[1].split("```", 1)[0]
    return json.loads(payload)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strip_tex_comments(text: str) -> str:
    rows = []
    for line in text.splitlines():
        cut = len(line)
        for match in re.finditer(r"%", line):
            i = match.start(); n = 0; j = i - 1
            while j >= 0 and line[j] == "\\": n += 1; j -= 1
            if n % 2 == 0: cut = i; break
        rows.append(line[:cut])
    return "\n".join(rows)


def doi_values(text: str) -> list[str]:
    found = re.findall(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", text, re.I)
    return [x.rstrip(".,;:)}]\\").lower() for x in found]


def parse_tex(path: str, memberships: dict[str, list[str]]) -> tuple[dict, list[str], list[str], list[str]]:
    raw = blob(path); clean = strip_tex_comments(raw.decode("utf-8"))
    bib = re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}", clean)
    cite: list[str] = []
    for group in re.findall(r"\\cite\w*\s*(?:\[[^\]]*\]\s*)*\{([^}]+)\}", clean):
        cite.extend(k.strip() for k in group.split(",") if k.strip())
    dois = doi_values(clean)
    row = {
        "path": path,
        "git_blob": str(git("rev-parse", f"{BASELINE}:{path}")).strip(),
        "sha256": sha256(raw),
        "lines": len(raw.decode("utf-8").splitlines()),
        "closures": sorted(memberships.get(path, [])),
        "bibitem_occurrences": len(bib),
        "citation_occurrences": len(cite),
        "doi_occurrences": len(dois),
        "undefined_keys": sorted(set(cite) - set(bib)),
    }
    return row, bib, cite, dois


def stats_for(paths: list[str]) -> dict:
    bib: list[str] = []; cite: list[str] = []; dois: list[str] = []
    for path in paths:
        clean = strip_tex_comments(blob(path).decode("utf-8"))
        bib.extend(re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}", clean))
        for group in re.findall(r"\\cite\w*\s*(?:\[[^\]]*\]\s*)*\{([^}]+)\}", clean):
            cite.extend(k.strip() for k in group.split(",") if k.strip())
        dois.extend(doi_values(clean))
    return {
        "files": len(paths), "bibitem_occurrences": len(bib),
        "unique_bibitem_keys": len(set(bib)), "citation_occurrences": len(cite),
        "unique_citation_keys": len(set(cite)), "doi_occurrences": len(dois),
        "unique_doi_strings": len(set(dois)),
    }


def binding(path: str, role: str) -> dict:
    raw = blob(path)
    return {"path": path, "role": role,
            "git_blob": str(git("rev-parse", f"{BASELINE}:{path}")).strip(),
            "sha256": sha256(raw), "lines": len(raw.decode("utf-8").splitlines()),
            "read_status": "READ_FULL"}


def control_source_binding(path: Path, role: str) -> dict:
    path_text = str(path).replace("\\", "/")
    raw = git("show", f":{path_text}", text=False)
    return {"path": path_text, "role": role,
            "index_blob": str(git("rev-parse", f":{path_text}")).strip(),
            "sha256": sha256(raw), "size_bytes": len(raw)}


DERIVATION_BY_CLAIM = {
    "M72-GR-01":"D72-B2", "M72-GR-02":"D72-B1", "M72-GR-03":"D72-B1",
    "M72-GR-04":"D72-B2", "M72-GR-05":"D72-B2", "M72-GR-06":"D72-B1",
    "M72-GR-07":"D72-B1", "M72-GR-08":"D72-B3", "M72-GR-09":"D72-B1",
    "M72-LCO-01":"D72-B2", "M72-LCO-02":"D72-B1", "M72-LCO-03":"D72-B2",
    "M72-LCO-04":"D72-B2", "M72-LCO-05":"D72-B1", "M72-LCO-06":"D72-B1",
    "M72-LCO-07":"D72-B2", "M72-LCO-08":"D72-B1",
    "M72-SI-01":"D72-B1", "M72-SI-02":"D72-B1", "M72-SI-03":"D72-B1",
    "M72-SI-04":"D72-B2", "M72-SI-05":"D72-B1", "M72-SI-06":"D72-B3",
    "M72-BLEND-01":"D72-B4", "M72-BLEND-02":"D72-B4",
    "M72-BLEND-03":"D72-B4", "M72-BLEND-04":"D72-B4", "M72-BLEND-05":"D72-B4",
}


def scientific_claim_row(row: dict) -> dict:
    claim_id = row["id"]
    status = row["status"]
    refs = copy.deepcopy(row["source_refs"])
    suffixes = {Path(ref["path"]).suffix.lower() for ref in refs}
    source_tier = ("FROZEN_INTERNAL_MIXED" if ".py" in suffixes and len(suffixes) > 1
                   else "FROZEN_INTERNAL_CODE" if suffixes == {".py"}
                   else "FROZEN_INTERNAL_DOCUMENT")
    if status.startswith("GROUND_NOT_FOUND"):
        validation_state = "GROUND_NOT_FOUND"
    elif "UNVERIFIED" in status:
        validation_state = "EXTERNAL_UNVERIFIED"
    elif status.startswith("SUPERSEDED"):
        validation_state = "SUPERSEDED"
    elif status.startswith("CONTRADICTED") or status.startswith("REJECTED"):
        validation_state = "CONTRADICTED"
    else:
        validation_state = "INTERNAL_ONLY"
    if "ABSENT" in status or "UNIMPLEMENTED" in status:
        implementation_state = "ABSENT"
    elif "IMPLEMENT" in status or claim_id in {
            "M72-GR-01", "M72-GR-03", "M72-GR-07", "M72-LCO-02",
            "M72-LCO-08", "M72-SI-02", "M72-SI-03", "M72-BLEND-04"}:
        implementation_state = "IMPLEMENTED"
    else:
        implementation_state = "DOCUMENTED_ONLY"
    if claim_id == "M72-LCO-08":
        default_state = "DISABLED"
    elif claim_id in {"M72-GR-01", "M72-GR-03", "M72-GR-07", "M72-LCO-02",
                      "M72-SI-02", "M72-SI-03", "M72-BLEND-04"}:
        default_state = "PROFILE_DEPENDENT"
    else:
        default_state = "NOT_APPLICABLE"
    return {
        "claim_id": claim_id,
        "material": row["material"],
        "proposition": row["claim"],
        "derivation_id": DERIVATION_BY_CLAIM[claim_id],
        "source_tier": source_tier,
        "exact_anchor": refs,
        "implementation_state": implementation_state,
        "default_state": default_state,
        "validation_state": validation_state,
        "applicability": f"frozen-v1.0.24::{row['material']}",
        "status": status,
        "supersession": ("SUPERSEDED_BY_FINAL_V1024_RECORD"
                           if status.startswith("SUPERSEDED") else "ACTIVE_AUDIT_BOUNDARY"),
        "ceiling": row["ceiling"],
        "source_refs": refs,
    }


def guard_output(output: Path) -> None:
    resolved = output.resolve()
    default = DEFAULT_OUTPUT.resolve()
    if resolved == default:
        staged = sorted(x for x in str(git("diff", "--cached", "--name-only")).splitlines() if x)
        allowed = [CONTROL_PATHS, sorted(CONTROL_PATHS + [str(DEFAULT_OUTPUT).replace("\\", "/")])]
        if staged not in allowed:
            raise SystemExit(f"JSON-last requires exact staged controls (optionally prior matrix), got {staged}")
        result_path = str(RESULT).replace("\\", "/")
        if result_path not in staged:
            raise SystemExit("result document must be staged before JSON-last collection")
        unstaged = [x for x in str(git("diff", "--name-only", "--", *CONTROL_PATHS)).splitlines() if x]
        if unstaged:
            raise SystemExit(f"control files have unstaged changes: {unstaged}")
        staged_result = git("show", f":{result_path}", text=False)
        if staged_result != RESULT.read_bytes():
            raise SystemExit("staged result bytes differ from worktree result")
        return
    temp_root = Path(tempfile.gettempdir()).resolve()
    try:
        resolved.relative_to(temp_root)
    except ValueError:
        raise SystemExit("explicit output must remain below the system temporary directory")
    if not resolved.name.startswith("matrix-") or resolved.suffix != ".json":
        raise SystemExit("temporary output name must match matrix-*.json")
    if not resolved.parent.is_dir():
        raise SystemExit("temporary output parent must already exist")


def atomic_json_last_collect(output: Path, obj: dict) -> None:
    data = (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    fd, tmp_name = tempfile.mkstemp(prefix=".phase065-step72-", suffix=".json.tmp",
                                    dir=str(output.resolve().parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, output.resolve())
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def build() -> dict:
    if not RESULT.exists():
        raise SystemExit("result document must exist before JSON-last collection")
    topology = json.loads(blob("Codex/results/PHASE_065_SOURCE_PROCESS_TOPOLOGY.json", EXPECTED_PARENT))
    code_matrix = json.loads(blob("Codex/results/PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json", EXPECTED_PARENT))
    step70_result = first_json_fence(
        "Codex/results/PHASE_065_STEP_070_SOURCE_PROCESS_TOPOLOGY_RESULT.md",
        EXPECTED_PARENT,
    )
    tex = topology["tex"]
    closures = tex["adopted_closures"]
    adopted: list[str] = []
    memberships: dict[str, list[str]] = {}
    for name in ("graphite", "lco", "si_blend"):
        for path in closures[name]["paths"]:
            memberships.setdefault(path, []).append(name)
            if path not in adopted: adopted.append(path)
    paths = adopted + tex["non_master_paths"]
    file_rows = []; all_bib: list[str] = []; all_cite: list[str] = []; all_doi: list[str] = []
    for path in sorted(paths):
        row, bib, cite, dois = parse_tex(path, memberships)
        file_rows.append(row); all_bib += bib; all_cite += cite; all_doi += dois
    summary = {
        "files": len(file_rows), "bibitem_occurrences": len(all_bib),
        "unique_bibitem_keys": len(set(all_bib)), "citation_occurrences": len(all_cite),
        "unique_citation_keys": len(set(all_cite)), "doi_occurrences": len(all_doi),
        "unique_doi_strings": len(set(all_doi)),
        "globally_undefined_keys": sorted(set(all_cite) - set(all_bib)),
        "globally_unused_bibitem_keys": sorted(set(all_bib) - set(all_cite)),
    }
    closure_stats = {name: stats_for(closures[name]["paths"]) for name in ("graphite", "lco", "si_blend")}
    closure_stats["adopted_union"] = stats_for(adopted)
    closure_stats["non_master"] = stats_for(tex["non_master_paths"])

    sources = [
        ("Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py", "production implementation and profile values"),
        ("Claude/docs/v1.0.24/CODE_GUIDE_v24.md", "published route/default guide"),
        ("Claude/docs/v1.0.24/_sections/ch1_sec06_eqpeak.tex", "ideal logistic derivation"),
        ("Claude/docs/v1.0.24/_sections/ch1_sec07_broadening.tex", "graphite broadening claims"),
        ("Claude/docs/v1.0.24/_sections/ch1_sec10_sum.tex", "graphite seed status"),
        ("Claude/docs/v1.0.24/_sections/ch1_sec11_lcointro.tex", "ordinary LCO literature claims"),
        ("Claude/docs/v1.0.24/_sections/ch1_sec13_lcohys.tex", "LCO interaction and doping claims"),
        ("Claude/docs/v1.0.24/_sections/ch1_sec15_lcoelec.tex", "LCO electronic entropy claims"),
        ("Claude/docs/v1.0.24/_sections/ch1_sec16b_lcoomega.tex", "LCO per-peak Omega claim"),
        ("Claude/docs/v1.0.24/_sections/ch3v22_sec02_cases.tex", "Si material numerical claims"),
        ("Claude/docs/v1.0.24/_sections/ch3v22_sec02b_sifr.tex", "Si Frumkin and width claims"),
        ("Claude/docs/v1.0.24/_sections/ch3v22_sec03_blend.tex", "shared-voltage blend derivation"),
        ("Claude/docs/v1.0.24/_sections/ch2_sec05_mixing.tex", "regular-solution and entropy derivation"),
        ("Claude/results/comp_v24/v24_graphite_asym.py", "two-sided-width proposal experiment"),
        ("Claude/results/comp_v24/IMPROVEMENT_DIRECTIONS.md", "proposal chronology"),
        ("Claude/results/comp_v24/TAKE_VS_DISCARD.md", "later disposition and supersession"),
        ("Claude/results/comp_v24/VALIDATION_SYNTHESIS.md", "calibration claims and limitations"),
        ("Claude/results/comp_v24/FIT_CHECK_v1024.md", "in-sample and identifiability record"),
        ("Claude/docs/v1.0.24/results/PHASE_R1_RESULT.md", "competition adoption result"),
        ("Claude/docs/v1.0.24/results/comp_R1/CHERRYPICK_R1.md", "graft and non-graft decision"),
        ("Claude/docs/v1.0.24/results/comp_R1/W1/gr_2L.tex", "rejected candidate with undefined keys"),
        ("Claude/docs/v1.0.24/results/comp_R1/W5/NOTES.md", "blend article-number conflict"),
        ("Claude/docs/v1.0.24/results/HANDOVER_v24.md", "final v1024 supersession record"),
        ("Claude/docs/v1.0.24/_sections/ch1v22_bib.tex", "graphite bibliography"),
        ("Claude/docs/v1.0.24/_sections/ch2v22_bib.tex", "LCO bibliography"),
        ("Claude/docs/v1.0.24/_sections/ch3v22_bib.tex", "Si/blend bibliography"),
        ("Claude/docs/v1.0.25/Anode_Fit_v1.0.24.py", "first downstream static-skew implementation boundary"),
        ("Claude/docs/v1.0.25.1/ARCHIVE_NOTE.md", "later v1.0.25.1 touch-up boundary"),
    ]

    step70_ids = [f"F{i:02d}" for i in (6,7,8,12,13,14,15,16,17,18,19,20,23,25,27,28,29,30,31,32,33,35,36,38,41,42)]
    step71_ids = [f"F{i:02d}" for i in range(1,14)]
    step70_by_id = {row["id"]: row for row in step70_result["finding_routes"]}
    step71_by_id = {row["finding_id"]: row for row in code_matrix["findings"]}
    step71_nonruntime_owner = {
        "P065-S71-F12": "P065-STEP75-DISPOSITION",
        "P065-S71-F13": "PHASE-071-PRIMARY-SOURCE-ACQUISITION",
    }
    routes = []
    for fid in step70_ids:
        route_id = f"P065-S70-{fid}"
        origin = step70_by_id[route_id]
        routes.append({
            "route_id": route_id,
            "origin_step": 70,
            "origin_finding": fid,
            "origin_artifact": "Codex/results/PHASE_065_STEP_070_SOURCE_PROCESS_TOPOLOGY_RESULT.md",
            "origin_record": copy.deepcopy(origin),
            "disposition": "PRESERVE_EXACT_ORIGIN_RECORD",
            "owner": origin["owner"],
            "followup_targets": copy.deepcopy(origin["target_steps"]),
            "status": "OPEN_CARRIED",
        })
    for fid in step71_ids:
        route_id = f"P065-S71-{fid}"
        origin = step71_by_id[route_id]
        routes.append({
            "route_id": route_id,
            "origin_step": 71,
            "origin_finding": fid,
            "origin_artifact": "Codex/results/PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json",
            "origin_record": copy.deepcopy(origin),
            "disposition": "PRESERVE_EXACT_ORIGIN_RECORD",
            "owner": step71_nonruntime_owner.get(route_id, "P065-STEP73-RUNTIME"),
            "followup_targets": copy.deepcopy(origin["next_steps"]),
            "status": "OPEN_CARRIED",
        })

    obj = {
        "schema_version": "phase065-step72-v1",
        "generated_date": "2026-08-31",
        "artifact_kind": "skew-material-authority-matrix",
        "baseline_commit": BASELINE,
        "expected_parent": EXPECTED_PARENT,
        "branch": "codex/anode-fit-v1025_2-canonical-completion",
        "gate": GATE,
        "authority": {
            "internal_derivation": True, "internal_source_genealogy": True,
            "external_bibliographic_metadata_verified": False,
            "controller_metadata_observation_recorded": True,
            "external_primary_literature_truth": False,
            "external_proposition_support": False, "material_truth": False,
            "experimental_truth": False, "runtime_truth": False,
            "canonical_manuscript_ready": False, "publication_ready": False,
            "v1024_1_independent_corroboration": False,
            "ceiling": "Internal frozen-source genealogy and algebra only; controller metadata observations are not reproducible external authority in this artifact."
        },
        "source_policy": {
            "rules": [
                "Read immutable Git blobs at the pinned baseline and expected parent.",
                "Never import or execute frozen Python sources.",
                "Never write Claude/**.",
                "Do not back-import v1.0.25 skew behavior into v1.0.24.",
                "Bibliographic identity does not prove proposition, page, or equation support.",
                "Unavailable primary text remains GROUND_NOT_FOUND with an acquisition owner.",
                "Generate the machine JSON after the human result and controls are staged."
            ],
            "network_used_by_builder": False, "child_process_allowlist": ["git"],
            "frozen_source_execution": False, "claude_tree_written": False,
        },
        "control_source_bindings": [
            control_source_binding(Path("Codex/work/v1024_phase065/build_phase065_step72.py"),
                                   "JSON_LAST_BUILDER"),
            control_source_binding(VALIDATOR, "INDEPENDENT_VALIDATOR"),
            control_source_binding(RESULT, "RESULT_FIRST_RESULT"),
            control_source_binding(
                Path("Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"),
                "PARENT_EXECUTION_LEDGER"),
            control_source_binding(
                Path("Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"),
                "CANONICAL_EXECUTION_LEDGER"),
            control_source_binding(
                Path("Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"),
                "ACTIVE_HANDOVER"),
        ],
        "source_bindings": [binding(p, r) for p, r in sources],
        "tex_census": {"summary": summary, "files": file_rows, "closures": closure_stats},
        "non_graft": {
            "candidate": "Claude/docs/v1.0.24/results/comp_R1/W1/gr_2L.tex",
            "undefined_keys": ["fergusonbazant2014", "guo2016"],
            "decision_source": "Claude/docs/v1.0.24/results/comp_R1/CHERRYPICK_R1.md",
            "decision": "REJECTED_SOURCE_NOT_GRAFTED",
            "replacement_existing_key": "persson2010b",
            "authority_effect": "Non-blocking for adopted closures; still blocks any claim that all 90 TeX files are self-contained."
        },
        "bibliographic_conflicts": [
            {"id":"B72-C01","normalized_doi":"10.1149/2.0341708jes","status":"INTERNAL_BIBLIOGRAPHIC_IDENTITY_CONFLICT","locations":["Claude/docs/v1.0.24/_sections/ch1v22_bib.tex:49","Claude/docs/v1.0.24/_sections/ch2v22_bib.tex:17","Claude/docs/v1.0.24/_sections/ch3v22_bib.tex:43"],"issue":"The same DOI/article is bound to two incompatible titles.","owner":"PHASE-071-PRIMARY-SOURCE-ACQUISITION"},
            {"id":"B72-C02","normalized_doi":"10.1149/1945-7111/ad4823","status":"ARCHIVAL_ARTICLE_NUMBER_CONFLICT","adopted_value":"050539","historical_value":"050520","owner":"PHASE-071-PRIMARY-SOURCE-ACQUISITION"}
        ],
        "genealogy": [
            {"id":"G72-01","topic":"equilibrium static skew","v1024_state":"ABSENT_IN_FROZEN_SOURCE","later_state":"INTRODUCED_IN_V1025","first_later_commit":"edbc4a2c68cda0dd21662cb6dd68ba8bed699a76","first_later_parent":"2147abfac3fb6c82279aefb2b21c749a521112dc","first_later_source":"Claude/docs/v1.0.25/Anode_Fit_v1.0.24.py","v1025_1_role":"LATER_TOUCH_UP_NOT_FIRST_IMPLEMENTATION","back_imported":False},
            {"id":"G72-02","topic":"causal-memory tail asymmetry","v1024_state":"IMPLEMENTED_OPT_IN","default_state":"PROFILE_DEPENDENT_OR_ZERO","authority":"STATIC_SOURCE_ONLY_RUNTIME_PENDING_STEP73"},
            {"id":"G72-03","topic":"two-sided-width skew experiment","v1024_state":"PROPOSED_AND_IN_SAMPLE_FIT","adopted_in_final_v1024":False,"externally_validated":False},
            {"id":"G72-04","topic":"regular-solution kernel","v1024_state":"GRAPHITE_CUSTOM_ROUTE_ONLY","lco_document_claim":"OVERSTATES_EXECUTABLE_COVERAGE","runtime_pending":"STEP73"},
            {"id":"G72-05","topic":"material decomposition","v1024_state":"SHARED_VOLTAGE_ADDITIVE_MODEL","calibration_state":"IN_SAMPLE","phase_identity_proven":False,"finite_rate_independence_proven":False},
            {"id":"G72-06","topic":"v1.0.24.1","v1024_1_state":"MIRROR_ARCHIVE_ONLY","independent_corroboration":False},
        ],
        "derivations": [
            {"id":"D72-B1","name":"ideal lattice gas / logistic peak","coordinate":"x is inserted fraction; Q_insert=Q*x; V=U0+(RT/F)ln[(1-x)/x]","signed_derivative":"dQ_insert/dV=-(QF/RT)x(1-x)","reported_magnitude":"-dQ_insert/dV=QF/(4RT) sech^2(F(V-U0)/(2RT))","center_voltage":"U0","signed_area_over_increasing_V":"-Q","magnitude_area":"Q","dimensionless_fwhm":4.0*math.acosh(math.sqrt(2.0)),"fwhm":"4(RT/F) arcosh(sqrt(2))","test_temperature_K":298.15,"test_fwhm_V":4.0*8.31446261815324*298.15/96485.33212*math.acosh(math.sqrt(2.0)),"convention_note":"For an explicit n-electron exponent replace F by nF; v1.0.24 w=nRT/F instead uses n as a phenomenological broadening multiplier."},
            {"id":"D72-B2","name":"symmetric regular solution","free_energy":"g=RT[x ln x+(1-x)ln(1-x)]+Omega x(1-x)","chemical_potential":"mu=RT ln[x/(1-x)]+Omega(1-2x)","curvature":"g''=RT/[x(1-x)]-2Omega","critical_omega_over_rt":2.0,"critical_composition":0.5,"spinodal":"x_sp,+/-=(1 +/- sqrt(1-2RT/Omega))/2","spinodal_domain":"Omega>=2RT","binodal_common_tangent":"mu(xa)=mu(xb)=[g(xb)-g(xa)]/(xb-xa)=0","symmetric_binodal_constraints":"Omega>2RT; 0<xa<1/2; xb=1-xa>1/2","nontrivial_binodal_equation":"RT ln[xa/(1-xa)]+Omega(1-2xa)=0 with 0<xa<1/2","trivial_root_excluded":"x=1/2 is stationary but is not a coexistence endpoint for Omega>2RT","strictness":"Omega=2RT has zero finite gap; finite coexistence requires Omega>2RT","spinodal_test_omega_over_rt":3.0,"spinodal_test_endpoints":[(1.0-math.sqrt(1.0-2.0/3.0))/2.0,(1.0+math.sqrt(1.0-2.0/3.0))/2.0],"homogeneous_branch_limit":"QF/|g''| is valid only on a stable monotone homogeneous branch, diverges at spinodal, and cannot replace common-tangent/Maxwell convexification."},
            {"id":"D72-B3","name":"asymmetry requirements","base_response":"p0(V)=|dx/dV| is symmetric about U0 along the physical monotone path x=x(V)","weight_conditions":["A is measurable along x(V)","A>=0 almost everywhere","0<integral A(x(V),V)p0(V)dV<infinity"],"weighted_response":"p_hat(V)=Q A(x(V),V)p0(V)/integral[A(x(V),V)p0(V)dV]","symmetry_preserving_condition":"A(x(V),V)=A(1-x(V),2U0-V) almost everywhere in V","symmetry_break_condition":"The pathwise equality fails on a set of nonzero measure","barrier_closure_example":"A=exp[-DeltaG_dagger(x,V)/(RT)] only after direction/rate/history and observable closure are declared","required_separation":["equilibrium free-energy asymmetry","state-dependent observation weight or barrier","finite-rate lag/overpotential","overlapping symmetric transitions or heterogeneity convolution"],"claim_ceiling":"A fitted two-sided width is phenomenological until normalization, path, mechanism, rate/history, identifiability and independent validation are supplied."},
            {"id":"D72-B4","name":"shared-voltage material sum","selected_basis":"1 g total active solids","basis_constraints":"m_gr+m_Si=1; q*_gr and q*_Si must use the same reversible/accessible capacity kind, cycle and voltage window","equilibrium_specific_capacity":"q(V)=m_gr q*_gr theta_gr(V)+m_Si q*_Si theta_Si(V)","equilibrium_derivative":"dq/dV=sum_i m_i q*_i dtheta_i/dV","capacity_fraction_si":"f_Si=m_Si q*_Si/[m_Si q*_Si+m_gr q*_gr]","single_declared_basis_required":True,"finite_rate_current_balance":"I=I_gr+I_Si","finite_rate_requirement":"separate current-partition, exchange-current, transport, overpotential and state closures","non_implications":["phase identity","material identity from curve shape alone","independent current partition","finite-rate additivity","absence of mechanical/interfacial coupling"]},
        ],
        "material_claims": [
            {"id":"M72-GR-01","material":"graphite","claim":"Default four-transition U,Q,Omega,DeltaH,DeltaS,activation and width values are material constants.","status":"IMPLEMENTATION_FACT_PLACEHOLDER_NOT_MATERIAL_CONSTANT","ceiling":"Fitting starts only.","source_refs":[{"path":"Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py","lines":"1108-1141"},{"path":"Claude/docs/v1.0.24/_sections/ch1_sec10_sum.tex","lines":"16-59"}]},
            {"id":"M72-GR-02","material":"graphite","claim":"Literature-linked 0.085/0.120/0.210 V and entropy anchors have proposition support.","status":"UNVERIFIED_EXTERNAL","ceiling":"Local bibliography identity only; primary proposition not read here.","source_refs":[{"path":"Claude/docs/v1.0.24/_sections/ch1v22_bib.tex","lines":"6-7,29"}]},
            {"id":"M72-GR-03","material":"graphite","claim":"XRD5 implementation proves a five-phase physical assignment.","status":"IMPLEMENTED_OPT_IN_PHASE_IDENTITY_UNVERIFIED","ceiling":"Implementation seed/gallery count is not phase identity.","source_refs":[{"path":"Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py","lines":"1145-1183"},{"path":"Claude/docs/v1.0.24/results/PHASE_R1_RESULT.md","lines":"41-50"}]},
            {"id":"M72-GR-04","material":"graphite","claim":"Four two-phase plus one solid-solution assignment from competition drafts is canonical.","status":"SUPERSEDED","ceiling":"Final record delegates phase character to structural/plateau evidence and refuses gallery=phase inference.","source_refs":[{"path":"Claude/docs/v1.0.24/results/comp_R1/CHERRYPICK_R1.md","lines":"25-27"},{"path":"Claude/docs/v1.0.24/results/PHASE_R1_RESULT.md","lines":"41-50"}]},
            {"id":"M72-GR-05","material":"graphite","claim":"Fitted Omega>2RT independently confirms two-phase character when lower bound is 2.02RT.","status":"TAUTOLOGICAL_BOUND_INDUCED","ceiling":"Not independent phase validation.","source_refs":[{"path":"Claude/results/comp_v24/TAKE_VS_DISCARD.md","lines":"22-31"},{"path":"Claude/results/comp_v24/VALIDATION_SYNTHESIS.md","lines":"61-68"}]},
            {"id":"M72-GR-06","material":"graphite","claim":"Stage split 29 J mol^-1 K^-1 implies about 0.30 mV K^-1 and is externally validated.","status":"INTERNAL_DERIVATION_WITH_UNVERIFIED_PREMISE","ceiling":"Algebra is valid; numerical premise and multi-temperature validation are not closed.","source_refs":[{"path":"Claude/results/comp_v24/FIT_CHECK_v1024.md","lines":"53-65"}]},
            {"id":"M72-GR-07","material":"graphite","claim":"MSMR6 U0,omega,Q values are primary-source grounded material parameters.","status":"GROUND_NOT_FOUND","ceiling":"Code has an ad2061 suffix and tier-C seeds; primary table and X_j support not acquired.","source_refs":[{"path":"Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py","lines":"1187-1205"},{"path":"Claude/results/comp_v24/IMPROVEMENT_DIRECTIONS.md","lines":"38-45"}]},
            {"id":"M72-GR-08","material":"graphite","claim":"Two-sided widths improve the same two-cell fit and establish a transferable skew mechanism.","status":"INTERNAL_CALIBRATION_ONLY","ceiling":"About one-point in-sample improvement is not independent mechanism validation.","source_refs":[{"path":"Claude/results/comp_v24/v24_graphite_asym.py","lines":"1-58"},{"path":"Claude/results/comp_v24/IMPROVEMENT_DIRECTIONS.md","lines":"46-68"}]},
            {"id":"M72-GR-09","material":"graphite","claim":"Micron-particle size contribution is universally negligible.","status":"GROUND_NOT_FOUND_FOR_INPUT_RANGE","ceiling":"Conditional internal calculation only; density, expansion, size and surface-energy ranges need exact anchors.","source_refs":[{"path":"Claude/docs/v1.0.24/_sections/ch1_sec07_broadening.tex","lines":"231-286"}]},
            {"id":"M72-LCO-01","material":"LCO","claim":"Ordinary/pristine LCO transition windows have primary proposition support in this audit.","status":"UNVERIFIED_EXTERNAL","ceiling":"Local citations exist; primary text was not acquired here.","source_refs":[{"path":"Claude/docs/v1.0.24/_sections/ch1_sec11_lcointro.tex","lines":"40-75"},{"path":"Claude/docs/v1.0.24/_sections/ch2v22_bib.tex","lines":"6-15"}]},
            {"id":"M72-LCO-02","material":"LCO","claim":"Named 3.930/3.880/4.050 V, Q 0.55/0.30/0.15, gmax 13 and MIT gate are measured material constants.","status":"IMPLEMENTATION_FACT_TIER_C_DEMO","ceiling":"Executable demo values, not 1:1 phase mapping or measurement.","source_refs":[{"path":"Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py","lines":"1009-1032"}]},
            {"id":"M72-LCO-03","material":"LCO","claim":"Per-peak regular-solution/Omega behavior is executable for the named LCO profile.","status":"CONTRADICTED_BY_STATIC_ROUTE_AUDIT","ceiling":"No named-profile Omega or LCO regular-solution dispatch was found.","source_refs":[{"path":"Claude/docs/v1.0.24/_sections/ch1_sec16b_lcoomega.tex","lines":"1-160"},{"path":"Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py","lines":"1009-1105"}]},
            {"id":"M72-LCO-04","material":"LCO","claim":"Ordinary/pristine or O2 evidence supports doped high-voltage O3 LCO.","status":"GROUND_NOT_FOUND_REJECTED_SCOPE_TRANSFER","ceiling":"Dopant chemistry/site/concentration and high-voltage specimen evidence are absent; owner PHASE-071-PRIMARY-SOURCE-ACQUISITION.","source_refs":[{"path":"Claude/docs/v1.0.24/_sections/ch1_sec13_lcohys.tex","lines":"204-221"}]},
            {"id":"M72-LCO-05","material":"LCO","claim":"g(EF)=13 and continuous electronic entropy gate are externally validated across composition.","status":"UNVERIFIED_EXTERNAL_MODEL_ASSUMPTION","ceiling":"Sommerfeld algebra is conditional; scalar DOS premise and logistic gate are not composition-resolved validation.","source_refs":[{"path":"Claude/docs/v1.0.24/_sections/ch1_sec15_lcoelec.tex","lines":"113-179,236-283"}]},
            {"id":"M72-LCO-06","material":"LCO","claim":"-45.7 J mol^-1 K^-1, -0.411 mV K^-1 and sign shifts are measurements.","status":"INTERNAL_DEMO_CALCULATION","ceiling":"Not measured evidence.","source_refs":[{"path":"Claude/docs/v1.0.24/_sections/ch1_sec15_lcoelec.tex","lines":"285-390"}]},
            {"id":"M72-LCO-07","material":"LCO","claim":"Clean real O3 multi-temperature phase-shape validation exists.","status":"GROUND_NOT_FOUND","ceiling":"Analytic proxies and O2 data do not close real O3; owner PHASE-071-PRIMARY-SOURCE-ACQUISITION.","source_refs":[{"path":"Claude/results/comp_v24/TAKE_VS_DISCARD.md","lines":"61-78"},{"path":"Claude/results/comp_v24/VALIDATION_SYNTHESIS.md","lines":"73-78"}]},
            {"id":"M72-LCO-08","material":"LCO","claim":"Electronic entropy is enabled by default.","status":"SUPERSEDED_FINAL_DEFAULT_OFF","ceiling":"Frozen implementation fact only; runtime pending Step 73.","source_refs":[{"path":"Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py","lines":"1061-1084"},{"path":"Claude/docs/v1.0.24/results/PHASE_R1_RESULT.md","lines":"43-48"}]},
            {"id":"M72-SI-01","material":"Si","claim":"Elemental Si/SiO/Si-C capacities, ICE, voltages, stress and entropy numbers have verified primary proposition support.","status":"UNVERIFIED_EXTERNAL","ceiling":"Exact local citation keys only; no primary full-text proposition audit here.","source_refs":[{"path":"Claude/docs/v1.0.24/_sections/ch3v22_sec02_cases.tex","lines":"12-97"},{"path":"Claude/docs/v1.0.24/_sections/ch3v22_bib.tex","lines":"6-43"}]},
            {"id":"M72-SI-02","material":"Si","claim":"SiO absolute mean voltage and hysteresis are grounded.","status":"GROUND_NOT_FOUND","ceiling":"Frozen code retains warned placeholders.","source_refs":[{"path":"Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py","lines":"1242-1251,1273-1280"}]},
            {"id":"M72-SI-03","material":"Si","claim":"Frozen Si component centers, widths and Q fractions identify phases.","status":"IMPLEMENTATION_FACT_TIER_C_DEMO","ceiling":"Demo components only.","source_refs":[{"path":"Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py","lines":"1223-1264"}]},
            {"id":"M72-SI-04","material":"Si","claim":"Omega_Si point values are uniquely identified by static single-temperature data.","status":"GROUND_NOT_FOUND_NONIDENTIFIABLE","ceiling":"0.2RT lower seed is an internal choice.","source_refs":[{"path":"Claude/docs/v1.0.24/_sections/ch3v22_sec02b_sifr.tex","lines":"101-129"},{"path":"Claude/results/comp_v24/FIT_CHECK_v1024.md","lines":"41-55"}]},
            {"id":"M72-SI-05","material":"Si","claim":"Width ratios [1.45,2.74,1.09] alone prove single-phase solid solution.","status":"INTERNAL_FIT_PHASE_INFERENCE_UNVERIFIED","ceiling":"Kinetics, heterogeneity, overlap, processing and instrument convolution remain alternatives.","source_refs":[{"path":"Claude/docs/v1.0.24/_sections/ch3v22_sec02b_sifr.tex","lines":"27-41,116-120"}]},
            {"id":"M72-SI-06","material":"Si","claim":"One symmetric Frumkin component intrinsically creates skew.","status":"REJECTED_BY_INTERNAL_SYMMETRY","ceiling":"Skew needs multiple components or an explicit asymmetric mechanism.","source_refs":[{"path":"Claude/docs/v1.0.24/_sections/ch3v22_sec02b_sifr.tex","lines":"82-100,121-129"}]},
            {"id":"M72-BLEND-01","material":"blend","claim":"Common-voltage equilibrium sum and mass-to-capacity conversion are valid without assumptions.","status":"INTERNAL_DERIVATION_CONDITIONAL","ceiling":"Requires independent host free energies, common equilibrium voltage and one basis.","source_refs":[{"path":"Claude/docs/v1.0.24/_sections/ch3v22_sec03_blend.tex","lines":"17-133"}]},
            {"id":"M72-BLEND-02","material":"blend","claim":"Frozen graphite/Si capacity inputs share one reversible capacity kind.","status":"UNVERIFIED_INCOMPATIBLE_KINDS","ceiling":"372 theoretical, 1000 first-reversible, 1710 theoretical and 3117 first-charge cannot be mixed without a declared conversion.","source_refs":[{"path":"Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py","lines":"1283-1292"}]},
            {"id":"M72-BLEND-03","material":"blend","claim":"Tu article number is internally conflict-free.","status":"INTERNAL_BIBLIOGRAPHIC_IDENTITY_CONFLICT","ceiling":"Adopted 050539 conflicts with archival 050520; primary metadata owner must resolve.","source_refs":[{"path":"Claude/docs/v1.0.24/_sections/ch3v22_bib.tex","lines":"40-43"},{"path":"Claude/docs/v1.0.24/results/comp_R1/W5/NOTES.md","lines":"70-76"}]},
            {"id":"M72-BLEND-04","material":"blend","claim":"Equilibrium additivity proves finite-rate host independence.","status":"UNVERIFIED_CONTRADICTED_BY_ROUTE_SHAPE","ceiling":"Frozen route passes the same full I_abs and Q_cell to both hosts rather than enforcing I=I_gr+I_Si.","source_refs":[{"path":"Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py","lines":"1479-1501"},{"path":"Claude/docs/v1.0.24/_sections/ch3v22_sec03_blend.tex","lines":"229-273"}]},
            {"id":"M72-BLEND-05","material":"blend","claim":"Nonadditive correction is implemented.","status":"ABSENT_UNIMPLEMENTED_STUB","ceiling":"No finite-rate nonadditive validation.","source_refs":[{"path":"Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py","lines":"1543-1553"}]},
        ],
        "metadata_verifications": [
            {"doi":"10.1149/2754-2734/ad7d1c","controller_observation":"MSMR Part 1 MCMB graphite; ECS Advances 3(4), 042501 (2024)","source_label":"Crossref REST","artifact_authority":"UNVERIFIED_EXTERNAL_NO_RAW_RESPONSE"},
            {"doi":"10.1149/1945-7111/ad70d9","controller_observation":"MSMR Part II entropy coefficient; JES 171(10), 103505","source_label":"Crossref REST","artifact_authority":"UNVERIFIED_EXTERNAL_NO_RAW_RESPONSE"},
            {"doi":"10.1149/1945-7111/ad1d27","controller_observation":"Quantifying Entropy and Enthalpy; JES 171(2), 023502","source_label":"Crossref REST","artifact_authority":"UNVERIFIED_EXTERNAL_NO_RAW_RESPONSE"},
            {"doi":"10.1149/1945-7111/ad4823","controller_observation":"SiO/graphite reduced-order model; JES 171(5), 050539","source_label":"Crossref REST","artifact_authority":"UNVERIFIED_EXTERNAL_NO_RAW_RESPONSE","historical_article_number":"050520"},
            {"doi":"10.1016/S1359-6454(02)00514-1","controller_observation":"Limthongkul et al.; Acta Materialia 51(4), 1103-1113","source_label":"Crossref REST","artifact_authority":"UNVERIFIED_EXTERNAL_NO_RAW_RESPONSE","historical_nearby_doi":"10.1016/S1359-6454(02)00515-4"},
            {"doi":"10.1063/1.4802584","controller_observation":"diffusion-influenced bimolecular-reaction article","source_label":"Crossref REST","artifact_authority":"UNVERIFIED_EXTERNAL_NO_RAW_RESPONSE","primary_text":"GROUND_NOT_FOUND","owner":"PHASE-071-PRIMARY-SOURCE-ACQUISITION"},
            {"doi":"10.1063/1.4802005","controller_observation":"hard-helices article; apparently unrelated to asserted Ref. 7 method","source_label":"Crossref REST","artifact_authority":"UNVERIFIED_EXTERNAL_NO_RAW_RESPONSE"},
        ],
        "findings": [
            {"id":"S72-F01","severity":"P1","finding":"Static equilibrium alpha-skew is absent from v1.0.24 and first appears downstream; no backward import is allowed.","owner":"P066-LINEAGE"},
            {"id":"S72-F02","severity":"P1","finding":"LCO per-peak Omega prose exceeds the executable v1.0.24 route found in Step 71.","owner":"P065-STEP74-CONFORMANCE"},
            {"id":"S72-F03","severity":"P1","finding":"Several material conclusions are in-sample or bound-induced and do not establish external material truth.","owner":"P071-PRIMARY-SOURCE-ACQUISITION"},
            {"id":"S72-F04","severity":"P1","finding":"Blend additivity lacks one consistently declared denominator and finite-rate current-partition evidence.","owner":"P067-CODE-HISTORY"},
            {"id":"S72-F05","severity":"P1","finding":"Two undefined citation keys are isolated to a rejected W1 candidate and were explicitly not grafted.","owner":"P065-STEP74-CONFORMANCE"},
            {"id":"S72-F06","severity":"P1","finding":"Bibliographic metadata verification does not establish proposition/page/equation support; missing primary text remains GROUND_NOT_FOUND.","owner":"P071-PRIMARY-SOURCE-ACQUISITION"},
        ],
        "input_routes": routes,
        "consumed_parent_evidence": {
            "step70_content_gate": "PASS_P065_STEP70_PRECOMMIT",
            "step70_persistence_terminal": "PASS_P065_STEP70_PERSISTENCE",
            "step70_commit": "d6f680b26fb59c24098f44ed633873a2c6419a4e",
            "step70_findings_routed": len(step70_ids),
            "step71_gate": code_matrix["gate"],
            "step71_persistence_terminal": "PASS_P065_STEP71_PERSISTENCE",
            "step71_commit": EXPECTED_PARENT,
            "step71_findings_routed": len(step71_ids),
            "total_routes": len(routes),
        },
        "next_gate": "Step 73 must test fresh-import, explicit-profile, and legacy-restoration routes independently under Python 3.12 and 3.14.",
    }
    obj["material_claims"] = [scientific_claim_row(row) for row in obj["material_claims"]]
    clone = copy.deepcopy(obj)
    obj["semantic_sha256"] = sha256(json.dumps(clone, ensure_ascii=False, sort_keys=True,
                                                 separators=(",", ":")).encode("utf-8"))
    return obj


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = ap.parse_args(); guard_output(args.output); obj = build()
    atomic_json_last_collect(args.output, obj)
    print(GATE, json.dumps({"tex_files": obj["tex_census"]["summary"]["files"],
                            "routes": len(obj["input_routes"]),
                            "semantic_sha256": obj["semantic_sha256"]},
                           sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
