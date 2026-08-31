#!/usr/bin/env python3
"""Build the deterministic Phase 065 Step 74 conformance matrix.

Only immutable Git blobs and staged Codex controls are read.  Frozen Python is
never imported or executed.  The output is an audit/disposition interface, not
a production repair or a scientific-truth promotion.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
from typing import Any


BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "5c5c555462f1dbf0603eedda6a1d5b62684cffdf"
EXPECTED_SUBJECT = "audit(phase065): adjudicate v1024 doc code guide"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
GATE = "PASS_P065_STEP74_CONFORMANCE_WITH_CONCERNS"
EXPECTED_VALIDATOR_MODULE_AST = "02dd0ca5bd1ced4a9dc927756cc891ccee8d78202dd45264bd6dd72586164f9a"
DEFAULT_OUTPUT = Path("Codex/results/PHASE_065_DOC_CODE_GUIDE_CONFORMANCE_MATRIX.json")
RESULT = Path("Codex/results/PHASE_065_STEP_074_DOC_CODE_GUIDE_RESULT.md")
VALIDATOR = Path("Codex/work/v1024_phase065/validate_phase065_step74.py")
CONTROL_PATHS = sorted([
    "Codex/work/v1024_phase065/build_phase065_step74.py",
    "Codex/work/v1024_phase065/validate_phase065_step74.py",
    "Codex/results/PHASE_065_STEP_074_DOC_CODE_GUIDE_RESULT.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
])


def run_process(argv: list[str], *, text: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        argv, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=text, encoding="utf-8" if text else None,
    )


def git(*args: str, text: bool = True) -> str | bytes:
    return run_process(["git", *args], text=text).stdout


def blob(path: str, rev: str = BASELINE) -> bytes:
    return git("show", f"{rev}:{path}", text=False)  # type: ignore[return-value]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")


def binding(path: str, role: str, status: str, rev: str = BASELINE) -> dict[str, Any]:
    raw = blob(path, rev); lines = len(raw.decode("utf-8").splitlines())
    return {
        "path": path, "role": role, "revision": rev,
        "git_blob": str(git("rev-parse", f"{rev}:{path}")).strip(),
        "sha256": sha256(raw), "size_bytes": len(raw), "lines": lines,
        "read_status": status, "read_ranges": [[1, lines]] if lines else [],
    }


def control_binding(path: str, role: str) -> dict[str, Any]:
    raw = git("show", f":{path}", text=False)
    return {
        "path": path, "role": role,
        "git_blob": str(git("rev-parse", f":{path}")).strip(),
        "sha256": sha256(raw), "size_bytes": len(raw),
    }


def anchor(path: str, lines: str, role: str) -> dict[str, str]:
    return {"path": path, "lines": lines, "role": role}


def authority(status: str, path: str = "NOT_APPLICABLE", lines: str = "NOT_APPLICABLE") -> dict[str, str]:
    return {"status": status, "path": path, "lines": lines}


def runtime(status: str, route: str = "NOT_APPLICABLE") -> dict[str, str]:
    return {
        "status": status,
        "artifact": "Codex/results/PHASE_065_RUNTIME_ATTESTATION.json" if route != "NOT_APPLICABLE" else "NOT_APPLICABLE",
        "route": route,
    }


def row(
    number: int, claim_class: str, claim: str, surfaces: list[dict[str, str]],
    source: dict[str, str], code: dict[str, str], run_auth: dict[str, str],
    artifact_class: str, verdict: str, severity: str, status: str, owner: str,
    acceptance: str, target: str, routes: list[str], ceiling: str,
) -> dict[str, Any]:
    return {
        "row_id": f"D74-{number:03d}", "claim_class": claim_class,
        "claim": claim, "claim_surface": surfaces,
        "source_authority": source, "code_authority": code,
        "runtime_authority": run_auth, "artifact_class": artifact_class,
        "verdict": verdict, "severity": severity, "status": status,
        "owner": owner, "acceptance_criterion": acceptance,
        "target_phase": target, "origin_routes": routes,
        "authority_ceiling": ceiling,
    }


def rows() -> list[dict[str, Any]]:
    code = "Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py"
    guide = "Claude/docs/v1.0.24/CODE_GUIDE_v24.md"
    html = "Claude/docs/v1.0.24/CODE_GUIDE_v24.html"
    fit = "Claude/docs/v1.0.24/FITTING_GUIDE.md"
    return [
        row(1,"behavior","The guide's blanket statement that the code implements the document equations exactly exceeds route-specific conformance.",[anchor(guide,"1-5","blanket conformance claim")],authority("ROUTE_SPECIFIC_ONLY",guide,"200-218"),authority("MIXED_ROUTE_THERMODYNAMICS",code,"582-602,679-726,813-834,884-931"),runtime("MIXED_ROUTE_CONFIRMED","explicit_profile.scope_boundaries"),"SOURCE","MISMATCH","P1","OPEN_ROUTED","PHASE-083-IMPLEMENTATION-CONTRACT","Replace the blanket claim with equation-ID and endpoint-specific conformance states, including explicit nonconforming paths.","Phase 083",["P065-S70-F08","P065-S71-F01"],"Internal source/runtime conformance only."),
        row(2,"behavior","The Markdown guide correctly discloses that regsol is restricted to equilibrium while dqdv, entropy and solve_U_oc remain logistic.",[anchor(guide,"200-218","scope disclosure")],authority("DISCLOSURE_CONFORMS",guide,"200-218"),authority("EQUILIBRIUM_ONLY",code,"582-602,679-726,813-834,884-931"),runtime("CONFIRMED","explicit_profile.scope_boundaries"),"SOURCE","CONFORMS","NONE","PRESERVE_BOUNDARY","P065-STEP75-DISPOSITION","Preserve the disclosure as historical behavior evidence without promoting it to thermodynamic closure.","NOT_APPLICABLE",["P065-S70-F08","P065-S71-F01"],"Behavior disclosure, not scientific acceptance."),
        row(3,"behavior","The reflect seed table says the regular-solution branch applies to equilibrium and derivative paths.",[anchor("Claude/docs/v1.0.24/results/REFLECT_SEED_TABLE.md","14","seed contract")],authority("CONTRADICTED_BY_EXECUTABLE",guide,"200-218"),authority("DYNAMIC_DERIVATIVE_LOGISTIC",code,"582-602,679-726"),runtime("CONTRADICTED","explicit_profile.scope_boundaries"),"SOURCE","MISMATCH","P1","OPEN_ROUTED","PHASE-083-IMPLEMENTATION-CONTRACT","Either implement one declared free-energy route for every listed consumer or revise the seed contract to equilibrium-only.","Phase 083",["P065-S70-F08","P065-S71-F01"],"Frozen behavior only."),
        row(4,"science","The silicon text combines w=nRT/F with an Omega-dependent direct kernel without deriving the generalized denominator and critical threshold.",[anchor("Claude/docs/v1.0.24/_sections/ch3v22_sec02b_sifr.tex","82-129","silicon regular-solution discussion")],authority("DERIVATION_INCOMPLETE","Claude/docs/v1.0.24/_sections/ch2_sec05_mixing.tex","1-EOF"),authority("N_EQUALS_ONE_KERNEL_FORM",code,"132-146"),runtime("NOT_SCIENTIFIC_AUTHORITY"),"SOURCE","PARTIAL","P1","OPEN_ROUTED","PHASE-075-EQUILIBRIUM-PHASE","Derive the n-generalized chemical-potential derivative and critical condition or remove n from the asserted constitutive interpretation.","Phase 075",["P065-S70-F06"],"Internal algebra; no material truth."),
        row(5,"science","Per-peak LCO Omega prose is not an executable named-profile route in v1.0.24.",[anchor("Claude/docs/v1.0.24/_sections/ch1_sec16b_lcoomega.tex","10-16,46-57,119-125,143-152","LCO Omega prose")],authority("THEORY_ONLY_UNVERIFIED","Claude/docs/v1.0.24/_sections/ch1_sec16b_lcoomega.tex","1-160"),authority("NAMED_PROFILE_KEYS_ABSENT",code,"1009-1055"),runtime("ABSENT_FROM_NAMED_PROFILE","explicit_profile.lco_electronic_entropy"),"SOURCE","MISMATCH","P1","OPEN_ROUTED","PHASE-078-LCO-CLOSURE","Ground the per-peak interaction in primary evidence and a declared model route, or label the section as unimplemented theory only.","Phase 078",["P065-S72-F02"],"No LCO material or proposition truth."),
        row(6,"science","Ref. 7 proposition/equation support remains unavailable in the Step 74 evidence and cannot be filled from repository self-report.",[anchor("Codex/results/PHASE_065_STEP_072_SKEW_MATERIAL_AUTHORITY_RESULT.md","1-EOF","bounded primary-source status")],authority("GROUND_NOT_FOUND","Codex/results/PHASE_065_SKEW_MATERIAL_AUTHORITY_MATRIX.json","metadata and findings"),authority("NOT_APPLICABLE"),runtime("NOT_SCIENTIFIC_AUTHORITY"),"MIXED","GROUND_NOT_FOUND","P2","OPEN_ROUTED","PHASE-071-PRIMARY-SOURCE-ACQUISITION","Acquire, hash and fully read the primary source, then bind exact proposition/page/equation support; otherwise retain GROUND_NOT_FOUND.","Phase 071",[],"No external proposition or scientific authority."),
        row(7,"record","The current guide correctly says LCO electronic entropy defaults off, while Phase R2/R3 retain mutually inconsistent default-ON/default-True statements.",[anchor(guide,"239-242,294-298","current default-false guide"),anchor("Claude/docs/v1.0.24/results/PHASE_R2_RESULT.md","30-44","R2 default claims"),anchor("Claude/docs/v1.0.24/results/PHASE_R3_RESULT.md","20-25","R3 contradictory claims")],authority("GIT_CHRONOLOGY_SUPERSEDES_STALE_RECORD","Claude/docs/v1.0.24/results/PHASE_R3_RESULT.md","1-39"),authority("DEFAULT_FALSE",code,"1061-1084"),runtime("CONFIRMED_DEFAULT_FALSE","explicit_profile.lco_electronic_entropy"),"SOURCE","MISMATCH","P1","OPEN_ROUTED","P065-STEP75-DISPOSITION","Preserve the current guide default-false statement; mark default-ON/default-True record clauses superseded by the R5 correction and final source.","Phase 065 Step 75.1",["P065-S70-F34","P065-S71-F06"],"Adoption chronology and current behavior only."),
        row(8,"behavior","The guide calls solve_U_oc a unique-root solver without disclosing silent max_iter exhaustion.",[anchor(guide,"52,114-119,319-323","unique-root claims")],authority("MATHEMATICAL_CONDITIONS_NOT_ENFORCED",guide,"114-119"),authority("SILENT_LAST_ITERATE_RETURN",code,"884-931"),runtime("CONFIRMED_SILENT_EXHAUSTION","explicit_profile.root_behavior"),"SOURCE","MISMATCH","P1","OPEN_ROUTED","PHASE-083-IMPLEMENTATION-CONTRACT","Specify bracketing, monotonicity, tolerance and iteration failure; return success only after a checked residual/convergence condition.","Phase 083",[],"Internal algorithm boundary."),
        row(9,"units","The R4 unit-contract record does not migrate the C-rate/Eyring path from per-hour to per-second.",[anchor("Claude/docs/v1.0.24/results/REFLECT_SEED_TABLE.md","38-43","unit contract"),anchor("Claude/docs/v1.0.24/results/PHASE_R2_RESULT.md","12-16,30-44","value-unchanged record")],authority("COMMENT_ONLY",code,"148-164"),authority("FACTOR_3600_RETAINED",code,"148-164,733-763"),runtime("CONFIRMED_FACTOR_3600","explicit_profile.seconds_hour"),"SOURCE","MISMATCH","P1","OPEN_ROUTED","PHASE-074-FOUNDATION","Separate current in amperes from normalized capacity rate in s^-1 and derive the conversion without absorbing it into a material parameter.","Phase 074",[],"Dimensional/runtime finding, not material truth."),
        row(10,"behavior","The guides omit the no-n/no-w and n_T1=None width/temperature-derivative inconsistency.",[anchor(guide,"170-173,250-261,351-359","width options"),anchor(fit,"36-53","width fitting ladder")],authority("CAVEAT_MISSING",fit,"36-53"),authority("ASYMMETRIC_NONE_HANDLING",code,"421-458"),runtime("CONFIRMED","explicit_profile.width_derivative"),"SOURCE","PARTIAL","P1","OPEN_ROUTED","PHASE-083-IMPLEMENTATION-CONTRACT","Define one total width schema and make value/derivative behavior consistent for absent and explicit-None keys.","Phase 083",[],"Behavioral schema only."),
        row(11,"behavior","The blend capacity-conservation claim covers equilibrium area but not finite-rate current partition or host-specific denominators.",[anchor("Claude/docs/v1.0.24/test_gates_v1024.py","535-570","equilibrium area gate"),anchor("Claude/docs/v1.0.24/results/MERGE_READINESS_v24.md","1-25","readiness claim")],authority("EQUILIBRIUM_ONLY",guide,"299-306"),authority("FULL_INPUT_TO_BOTH_HOSTS",code,"1479-1501"),runtime("CONFIRMED_FULL_HOST_ARGUMENTS","explicit_profile.blend_host_arguments"),"SOURCE","MISMATCH","P1","OPEN_ROUTED","PHASE-080-BLEND-CLOSURE","Derive I=I_gr+I_Si and host capacity bases, then test finite-rate conservation separately from equilibrium weighted area.","Phase 080",[],"No finite-rate blend truth."),
        row(12,"science","An analytic PyBaMM LCO proxy is labeled as the first real-data fit although no LCO-specific measured raw data were available.",[anchor("Claude/results/comp_v24/VALIDATION_SYNTHESIS.md","15,24","real-fit headline"),anchor("Claude/results/comp_v24/LCO_DIAGNOSIS.md","5-16","proxy limitation"),anchor("Claude/results/comp_v24/TAKE_VS_DISCARD.md","61-78","later correction")],authority("ANALYTIC_PROXY_ONLY","Claude/results/comp_v24/LCO_DIAGNOSIS.md","5-16"),authority("NOT_APPLICABLE"),runtime("NOT_APPLICABLE"),"SOURCE","MISMATCH","P1","OPEN_ROUTED","PHASE-086-CALIBRATION-VALIDATION","Relabel the result as an analytic proxy and require independently registered measured LCO data for any real-fit or validation claim.","Phase 086",["P065-S70-F14"],"No experimental validation."),
        row(13,"record","Two undefined citation keys occur only in a rejected W1 candidate that was explicitly not grafted.",[anchor("Claude/docs/v1.0.24/results/comp_R1/W1/gr_2L.tex","73-97","undefined keys"),anchor("Claude/docs/v1.0.24/results/comp_R1/CHERRYPICK_R1.md","23-28,34-41","non-graft decision")],authority("REJECTED_SOURCE_NOT_GRAFTED","Claude/docs/v1.0.24/results/comp_R1/CHERRYPICK_R1.md","23-28,34-41"),authority("NOT_APPLICABLE"),runtime("NOT_APPLICABLE"),"SOURCE","CLOSED_NON_GRAFT","NONE","CLOSED","P065-STEP75-DISPOSITION","Keep the candidate marked rejected and exclude it from adopted-closure citation completeness denominators.","NOT_APPLICABLE",["P065-S72-F05"],"Adoption/citation topology only."),
        row(14,"science","Fixed graphite/Si specific-capacity values are used for mass-to-capacity conversion without one measured capacity-kind contract.",[anchor(guide,"327-340","constant table"),anchor(fit,"1-137","fitting assumptions")],authority("EMPIRICAL_INPUT_REQUIRED",guide,"327-340"),authority("FIXED_TABLE_FALLBACK",code,"1283-1292,1437-1468"),runtime("CONFIRMED","explicit_profile.profile_surfaces"),"SOURCE","PARTIAL","P1","OPEN_ROUTED","PHASE-080-BLEND-CLOSURE","Require cycle/window/rate-matched accessible capacities and uncertainty or label each fixed value as an explicit prior/example.","Phase 080",[],"No universal material constant authority."),
        row(15,"version","FITTING_GUIDE identifies itself and its implementation target as v1.0.20 inside the v1.0.24 release surface.",[anchor(fit,"1-5","stale title and target")],authority("STALE_VERSION_METADATA",fit,"1-5"),authority("CURRENT_FILE_IS_V1024",code,"1-12"),runtime("NOT_APPLICABLE"),"SOURCE","MISMATCH","P2","OPEN_ROUTED","PHASE-087-MANUSCRIPT-ASSEMBLY","Issue a version-bound companion or explicitly state the preserved older procedure and enumerate v1.0.24 deltas.","Phase 087",["P065-S70-F43"],"Documentation versioning only."),
        row(16,"version","The fitting guide's reproduction suite points to v1.0.19 paths and scripts rather than a self-contained v1.0.24 command set.",[anchor(fit,"114-137","v1.0.19 suite")],authority("STALE_REPRODUCTION_SURFACE",fit,"114-137"),authority("CURRENT_TESTS_DIFFER",code,"NOT_APPLICABLE"),runtime("NOT_REPLAYED_BY_GUIDE"),"SOURCE","PARTIAL","P2","OPEN_ROUTED","PHASE-087-MANUSCRIPT-ASSEMBLY","Provide version-local commands, exact input hashes and expected terminals, or label the section historical.","Phase 087",["P065-S70-F43"],"Reproduction instructions only."),
        row(17,"artifact","CODE_GUIDE_v24.html is a generated copy of the Markdown guide and adds no independent scientific support.",[anchor(html,"1-219","authored wrapper"),anchor(html,"220-3807","vendor payload"),anchor(html,"3808-3812","initialization footer")],authority("MARKDOWN_IS_AUTHORING_SOURCE",guide,"1-374"),authority("NOT_APPLICABLE"),runtime("NOT_APPLICABLE"),"GENERATED","DERIVED_ONLY","NONE","PRESERVE_BOUNDARY","P065-STEP75-DISPOSITION","Preserve the source/generated edge and never count HTML repetition as a second authority.","NOT_APPLICABLE",[],"Generated presentation only."),
        row(18,"artifact","The generated HTML equilibrium table row is split into five cells by literal pipe delimiters.",[anchor(html,"142","damaged equilibrium row"),anchor(guide,"176","correct Markdown source")],authority("MARKDOWN_SOURCE_CORRECT",guide,"176"),authority("NOT_APPLICABLE"),runtime("NOT_APPLICABLE"),"GENERATED","MISMATCH","P2","OPEN_ROUTED","PHASE-089-RELEASE-QA","Escape absolute-value pipes and verify the regenerated three-column table with an HTML parser.","Phase 089",["P065-S70-F10"],"Generated rendering defect."),
        row(19,"artifact","The generated HTML R_n option row is split into five cells by literal pipe delimiters.",[anchor(html,"166","damaged R_n row"),anchor(guide,"228","correct Markdown source")],authority("MARKDOWN_SOURCE_CORRECT",guide,"228"),authority("NOT_APPLICABLE"),runtime("NOT_APPLICABLE"),"GENERATED","MISMATCH","P2","OPEN_ROUTED","PHASE-089-RELEASE-QA","Escape absolute-value pipes and verify the regenerated three-column table with an HTML parser.","Phase 089",["P065-S70-F10"],"Generated rendering defect."),
        row(20,"artifact","The generated HTML V_n symbol row is split into six cells by literal pipe delimiters.",[anchor(html,"214","damaged V_n row"),anchor(guide,"350","correct Markdown source")],authority("MARKDOWN_SOURCE_CORRECT",guide,"350"),authority("NOT_APPLICABLE"),runtime("NOT_APPLICABLE"),"GENERATED","MISMATCH","P2","OPEN_ROUTED","PHASE-089-RELEASE-QA","Escape absolute-value pipes and verify the regenerated four-column table with an HTML parser.","Phase 089",["P065-S70-F10"],"Generated rendering defect."),
        row(21,"artifact","The exact Markdown-to-HTML generator command and pinned renderer dependency are not recoverable.",[anchor(html,"1-219,3808-3812","generated artifact declarations")],authority("GROUND_NOT_FOUND",guide,"1-374"),authority("NOT_APPLICABLE"),runtime("NOT_APPLICABLE"),"GENERATED","GROUND_NOT_FOUND","P2","OPEN_ROUTED","PHASE-089-RELEASE-QA","Record a deterministic generator command, renderer version/hash, trusted-input boundary and structural post-generation checks.","Phase 089",["P065-S70-F11"],"Generation provenance only."),
        row(22,"record","The reflect test reports a single peak but its predicate accepts any count greater than or equal to one.",[anchor("Claude/docs/v1.0.24/test_gates_v1024_reflect.py","48-52","single-peak predicate"),anchor("Claude/docs/v1.0.24/results/PHASE_R2_RESULT.md","30-39","single-peak promotion"),anchor("Claude/docs/v1.0.24/results/PHASE_R3_RESULT.md","15-20","single-peak promotion")],authority("PREDICATE_SCOPE_ONLY","Claude/docs/v1.0.24/test_gates_v1024_reflect.py","48-52"),authority("AT_LEAST_ONE_LOCAL_MAXIMUM",code,"NOT_APPLICABLE"),runtime("INTERNAL_SYNTHETIC_FIXTURE","explicit_profile.regsol"),"SOURCE","MISMATCH","P1","OPEN_ROUTED","PHASE-083-IMPLEMENTATION-CONTRACT","Relabel the result as at least one approximate local maximum or require exactly one under a defined prominence and boundary rule.","Phase 083",[],"Internal numerical fixture only."),
        row(23,"artifact","Step 70 reported seventeen comp_v24 PNGs with missing-glyph boxes, but a fresh decode and original-image visual pass directly observed fifteen named PNGs and found no durable identity for the other two claimed members.",[anchor("Codex/results/PHASE_065_STEP_070_SOURCE_PROCESS_TOPOLOGY_RESULT.md","388-390,1432-1441","inherited seventeen-image finding"),anchor("Codex/results/PHASE_065_STEP_074_DOC_CODE_GUIDE_RESULT.md","182-190","fresh fifteen-path visual numerator")],authority("FRESH_VISUAL_COUNT_15_AND_REMAINDER_GROUND_NOT_FOUND","Codex/results/PHASE_065_STEP_074_DOC_CODE_GUIDE_RESULT.md","182-190"),authority("NOT_APPLICABLE"),runtime("NOT_APPLICABLE"),"GENERATED","MISMATCH","P2","OPEN_ROUTED","PHASE-089-RELEASE-QA","Persist the fifteen directly observed paths (bdd_vs_savgol.png, cathode_fit.png, consistency.png, gr_4vs6_transitions.png, gr_angular_diag.png, gr_sym_vs_asym.png, model_vs_data.png, new_materials.png, param_distributions.png, quality_vs_r2.png, rate_broadening.png, rate_quant.png, regsol_proto.png, temperature_entropy.png, wavelet_denoise_check.png), keep the remaining two as GROUND_NOT_FOUND, regenerate with a verified font stack, and visually verify every affected image at original resolution.","Phase 089",["P065-S70-F41"],"Visual presentation evidence only; fifteen observed is not silently reconciled to the inherited seventeen."),
        row(24,"artifact","Four named visual artifacts contain clipping, scalar-representation or label-overlap defects.",[anchor("Codex/results/PHASE_065_STEP_070_SOURCE_PROCESS_TOPOLOGY_RESULT.md","391-393,1444-1452","named visual defects")],authority("VISUAL_AUDIT_ONLY","Codex/results/PHASE_065_SOURCE_PROCESS_TOPOLOGY.json","finding P065-S70-F42"),authority("NOT_APPLICABLE"),runtime("NOT_APPLICABLE"),"GENERATED","MISMATCH","P2","OPEN_ROUTED","PHASE-089-RELEASE-QA","Regenerate gr_dva_Mremoval.png, lco_phase.png, param_distributions.png and quality_vs_r2.png and inspect at original resolution.","Phase 089",["P065-S70-F42"],"Visual presentation evidence only."),
        row(25,"units","The graphite first-look helper labels cumulative capacity as mAh and later multiplies it by 1000 while retaining that label.",[anchor("Claude/results/comp_v24/v24_graphite_firstlook.py","12,72","capacity conversion")],authority("UNIT_NOT_CLOSED","Claude/results/comp_v24/v24_graphite_firstlook.py","12,72"),authority("NOT_PRODUCTION_CODE"),runtime("NOT_REEXECUTED"),"SOURCE","MISMATCH","P2","OPEN_ROUTED","PHASE-074-FOUNDATION","Declare the raw capacity unit and apply exactly one verified conversion before labeling the axis/output.","Phase 074",["P065-S70-F35"],"Historical helper output only."),
        row(26,"units","The rate-broadening helper multiplies a V/mA slope by 1000 to ohms but labels a later output as Omega per mA.",[anchor("Claude/results/comp_v24/v24_rate_broadening.py","67-70","resistance/current unit output")],authority("DERIVED_UNIT_INCOHERENT","Claude/results/comp_v24/v24_rate_broadening.py","67-70"),authority("NOT_PRODUCTION_CODE"),runtime("NOT_REEXECUTED"),"SOURCE","MISMATCH","P2","OPEN_ROUTED","PHASE-074-FOUNDATION","Derive and label every reported quantity dimensionally; do not interpret the current-divided output as a material parameter.","Phase 074",["P065-S70-F36"],"Historical helper output only."),
        row(27,"artifact","Historical sample/plot helpers contain absolute local paths that are provenance rather than portable commands.",[anchor("Claude/docs/v1.0.24/results/v1024_final_sample.py","9-12,68,102","absolute paths"),anchor("Claude/docs/v1.0.24/results/v1024_reflect_curves.py","7,9,40","absolute paths")],authority("NONPORTABLE_PROVENANCE","Claude/docs/v1.0.24/results/v1024_final_sample.py","9-12"),authority("NOT_PRODUCTION_CODE"),runtime("NOT_PORTABLE"),"SOURCE","MISMATCH","P2","OPEN_ROUTED","PHASE-087-MANUSCRIPT-ASSEMBLY","Replace reproduction instructions with repository-relative inputs and exact hashes while retaining historical paths only as provenance.","Phase 087",["P065-S70-F39"],"Historical helper provenance only."),
        row(28,"artifact","Two Markdown records lack a final line feed.",[anchor("Claude/results/comp_v24/fit_registry.md","1-25","no final LF"),anchor("Claude/results/comp_v24/param_dist_stats.md","1-8","no final LF")],authority("EXACT_BYTE_DEFECT","Claude/results/comp_v24/fit_registry.md","EOF"),authority("NOT_APPLICABLE"),runtime("NOT_APPLICABLE"),"SOURCE","MISMATCH","P2","OPEN_ROUTED","PHASE-089-RELEASE-QA","Normalize both records to UTF-8 LF with one final LF and verify byte hashes in the release build.","Phase 089",["P065-S70-F44"],"Formatting only; scientific content unchanged."),
        row(29,"scope","Legacy restoration and saved-state key compatibility are absent from the frozen source and cannot receive a behavioral PASS.",[anchor("Codex/results/PHASE_065_STEP_073_INITIALIZATION_RUNTIME_RESULT.md","88-105","absence boundary")],authority("STATIC_ABSENCE_PRIMARY","Codex/results/PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json","profile/default census"),authority("ABSENT_IN_FROZEN_SOURCE",code,"1-1734"),runtime("ABSENCE_CORROBORATION_ONLY","legacy_restoration"),"MIXED","ABSENT_NOT_A_PASS","NONE","PRESERVE_BOUNDARY","P065-STEP75-DISPOSITION","Preserve ABSENT_IN_FROZEN_SOURCE and do not relabel absence-corroboration runs as route success.","NOT_APPLICABLE",[],"Absence boundary only."),
        row(30,"scope","Plastic hysteresis and nonadditive blend correction are explicit unimplemented stubs rather than supported features.",[anchor(guide,"190-197","stub disclosure")],authority("DISCLOSED_UNSUPPORTED",guide,"190-197"),authority("UNIMPLEMENTED_STUB",code,"1543-1553"),runtime("NOT_IMPLEMENTED","explicit_profile.scope_boundaries"),"SOURCE","CONFORMS","NONE","PRESERVE_BOUNDARY","P065-STEP75-DISPOSITION","Preserve the unsupported status until a later canonical contract and implementation exist.","NOT_APPLICABLE",[],"No feature or production authority."),
        row(31,"behavior","XRD profile Omega values do not activate regsol without the kernel key, a caveat not explicit at the profile-selection surface.",[anchor(guide,"279-292,327-340","profile examples and constants")],authority("CAVEAT_INCOMPLETE",guide,"200-218"),authority("LOGISTIC_WITHOUT_KERNEL",code,"1145-1183"),runtime("CONFIRMED_LOGISTIC","explicit_profile.xrd_omega"),"SOURCE","PARTIAL","P2","OPEN_ROUTED","PHASE-083-IMPLEMENTATION-CONTRACT","State that Omega alone affects other routes but does not select the equilibrium regsol kernel; require explicit model-family selection.","Phase 083",[],"Frozen behavior only."),
        row(32,"behavior","The MSMR6 profile is available only through direct explicit injection, and the guide example reflects that route.",[anchor(guide,"279-286,327-340","explicit MSMR6 injection")],authority("EXPLICIT_ROUTE_DISCLOSED",guide,"279-286"),authority("DIRECT_PROFILE_CONSTANT",code,"1187-1205"),runtime("CONFIRMED_DIRECT_INJECTION","explicit_profile.msmr6"),"SOURCE","CONFORMS","NONE","PRESERVE_BOUNDARY","P065-STEP75-DISPOSITION","Preserve explicit injection and do not claim automatic endpoint/profile selection.","NOT_APPLICABLE",[],"Frozen profile availability only."),
        row(33,"behavior","Unknown, None and false-like kernel values silently fall back to logistic, but the guide documents only regsol versus absent.",[anchor(guide,"200-218,250-261","kernel option")],authority("FALLBACK_UNDOCUMENTED",guide,"250-261"),authority("STRING_EQUALITY_FALLBACK",code,"596-602"),runtime("CONFIRMED","explicit_profile.kernel_fallback"),"SOURCE","PARTIAL","P2","OPEN_ROUTED","PHASE-083-IMPLEMENTATION-CONTRACT","Validate kernel against an explicit enum and fail on unsupported values, or document every accepted fallback with tests.","Phase 083",[],"Input-contract behavior only."),
        row(34,"behavior","The regsol delta fallback/clamp behavior is not fully disclosed by the guide's optional-delta description.",[anchor(guide,"250-261,287-292","delta option")],authority("CAVEAT_INCOMPLETE",guide,"250-261"),authority("FALLBACK_AND_CLAMP",code,"132-146"),runtime("CONFIRMED","explicit_profile.delta_fallback"),"SOURCE","PARTIAL","P2","OPEN_ROUTED","PHASE-083-IMPLEMENTATION-CONTRACT","Define delta's physical role, unit, admissible domain and failure behavior; expose any numerical clamp as a diagnostic.","Phase 083",[],"Numerical observation parameter only."),
        row(35,"behavior","Explicit zero current and numeric direction zero have edge semantics not stated in the guide.",[anchor(guide,"264-306,343-362","curve usage and symbols")],authority("EDGE_CASE_UNDOCUMENTED",guide,"264-306"),authority("ZERO_OVERRIDES_RATE_AND_DIRECTION_NONNEGATIVE",code,"733-763"),runtime("CONFIRMED","explicit_profile.zero_current_direction"),"SOURCE","PARTIAL","P2","OPEN_ROUTED","PHASE-083-IMPLEMENTATION-CONTRACT","Specify that I_abs=0 overrides c_rate and define or reject direction=0 consistently across facades.","Phase 083",[],"API behavior only."),
        row(36,"behavior","Transition dictionaries are retained by alias, so caller mutation can alter later behavior without a documented state contract.",[anchor(guide,"40-70,248-261","transition state surface")],authority("MUTABILITY_UNDOCUMENTED",guide,"248-261"),authority("ALIAS_RETAINED",code,"368-401"),runtime("CONFIRMED_ALIAS_MUTATION","explicit_profile.transition_alias"),"SOURCE","PARTIAL","P2","OPEN_ROUTED","PHASE-085-STRUCTURE-FREEZE","Choose immutable copied configuration or explicitly version and test mutable state/serialization behavior.","Phase 085",[],"Initialization/state behavior only."),
        row(37,"record","Self-consistency and merge-ready/BUG0 records overstate validation because the fixed-point check uses the same implementation and open conformance gaps remain.",[anchor("Claude/docs/v1.0.24/test_gates_v1024_selfconsistent.py","1-EOF","same-code fixed-point check"),anchor("Claude/docs/v1.0.24/results/MERGE_READINESS_v24.md","1-25","merge-ready claim"),anchor("Claude/docs/v1.0.24/results/HANDOVER_v24.md","66-74","full-conformance claim")],authority("INTERNAL_REGRESSION_ONLY","Claude/docs/v1.0.24/test_gates_v1024_selfconsistent.py","1-EOF"),authority("SAME_IMPLEMENTATION_ORACLE",code,"1-1734"),runtime("INTERNAL_REGRESSION_ONLY","explicit_profile.selfconsistent"),"SOURCE","MISMATCH","P1","OPEN_ROUTED","PHASE-088-SCIENTIFIC-REDTEAM","Reclassify same-code checks as regression evidence and require independent equations/data for scientific or correctness claims.","Phase 088",[],"Internal regression, not external correctness."),
        row(38,"scope","Visible scientific main text contains implementation names and work-history language beyond the narrow 17-line literal-token inventory, contradicting the archive statement that code is appendix-only.",[anchor("Claude/results/comp_v24/INV_code_in_body.md","1-39","narrow literal-token inventory"),anchor("Claude/docs/v1.0.24/ch1_graphite_v1.0.24.tex","23-56","Part-T main-body versus appendix topology"),anchor("Claude/docs/v1.0.24/ch2_lco_v1.0.24.tex","20-29","LCO main-body inclusion topology"),anchor("Claude/docs/v1.0.24/ch3_si_v1.0.24.tex","23-29","Si main-body versus appendix topology"),anchor("Claude/docs/v1.0.24/_sections/ch1_sec00_intro.tex","14-20","code-construction promise"),anchor("Claude/docs/v1.0.24/_sections/ch1_sec18_inputs.tex","30-37,66-68","implementation identifiers and one-to-one mapping"),anchor("Claude/docs/v1.0.24/_sections/ch1_sec15_lcoelec.tex","340-390","current implementation and reproduction language"),anchor("Claude/docs/v1.0.24/_sections/ch3v22_sec02_cases.tex","138-153","code/blend execution caption"),anchor("Claude/docs/v1.0.24/_sections/ch3v22_sec03_blend.tex","84-110,203-222,257-272","toggle, bit-exact and implementation-status prose"),anchor("Claude/docs/v1.0.24/_sections/ch3v22_sec05_code.tex","1-EOF","designated implementation section"),anchor("Claude/docs/v1.0.24.1/ARCHIVE_NOTE.md","16","appendix-only archive claim")],authority("MAIN_BODY_RELOCATION_REQUIRED","Claude/results/comp_v24/INV_code_in_body.md","1-39"),authority("NOT_APPLICABLE"),runtime("NOT_APPLICABLE"),"SOURCE","MISMATCH","P1","OPEN_ROUTED","PHASE-087-MANUSCRIPT-ASSEMBLY","Preserve the full-read main-body topology manifest; reduce rendered pre-appendix prose and captions containing implementation identifiers/defaults/override/fallback/toggle/placeholder warnings/bit-exact/regression/backward-compatibility/current implementation status to zero; keep mathematical limits, numerical checks and physical uncertainty as code-independent science; move implementation detail to the designated appendix or guide; verify rendered prose rather than raw grep comments or label keys.","Phase 087",[],"Manuscript register and topology only; the old 17-line count is not a complete denominator."),
        row(39,"science","The graphite regular-solution helper treats Omega greater than 2RT as a phase confirmation even though the optimizer enforces Omega at or above 2.02RT.",[anchor("Claude/results/comp_v24/v24_regsol2.py","74-85","bound-enforced Omega and conclusion"),anchor("Claude/results/comp_v24/TAKE_VS_DISCARD.md","12,28-31","two-phase confirmation claim"),anchor("Claude/results/comp_v24/VALIDATION_SYNTHESIS.md","58-66","promoted regular-solution conclusion")],authority("BOUND_CONSTRAINED_IN_SAMPLE_DIAGNOSTIC","Codex/results/PHASE_065_STEP_072_SKEW_MATERIAL_AUTHORITY_RESULT.md","223-225,299-300"),authority("HISTORICAL_HELPER_ONLY","Claude/results/comp_v24/v24_regsol2.py","74-85"),runtime("NOT_REEXECUTED"),"SOURCE","MISMATCH","P1","OPEN_ROUTED","PHASE-075-EQUILIBRIUM-PHASE","Downgrade the result to a bound-constrained in-sample diagnostic and require an unconstrained or independently justified inference with uncertainty before any phase-identity claim.","Phase 075",[],"No independent phase identity or experimental validation."),
        row(40,"science","Finite fitted Si width ratios are presented as direct single-phase evidence although the same manuscript identifies them as fit-tier diagnostics.",[anchor("Claude/docs/v1.0.24/_sections/ch3v22_sec02b_sifr.tex","27-41,115-120","single-phase evidence language"),anchor("Claude/docs/v1.0.24/_sections/ch3v22_sec02b_sifr.tex","131-142","fit-tier and identification limits")],authority("INTERNAL_WIDTH_DIAGNOSTIC_ONLY","Codex/results/PHASE_065_STEP_072_SKEW_MATERIAL_AUTHORITY_RESULT.md","313-320"),authority("NOT_APPLICABLE"),runtime("NOT_APPLICABLE"),"SOURCE","MISMATCH","P1","OPEN_ROUTED","PHASE-079-SILICON-CLOSURE","Limit the statement to single-phase-consistent behavior under the stated fit and extraction assumptions, and test kinetic, disorder and extraction alternatives before a material phase conclusion.","Phase 079",[],"No external material or phase truth."),
        row(41,"science","A roughly one-percentage-point in-sample two-sided-width improvement is treated as transferable physical skew evidence although the prototype adds flexibility and does not preserve the production capacity normalization.",[anchor("Claude/results/comp_v24/IMPROVEMENT_DIRECTIONS.md","46-68","physical-skew promotion"),anchor("Claude/results/comp_v24/v24_graphite_asym.py","1-58","same-data flexible asymmetric fit")],authority("IN_SAMPLE_SHAPE_DIAGNOSTIC_ONLY","Codex/results/PHASE_065_STEP_072_SKEW_MATERIAL_AUTHORITY_RESULT.md","297-300"),authority("NON_PARITY_PROTOTYPE","Claude/results/comp_v24/v24_graphite_asym.py","18-55"),runtime("NOT_REEXECUTED"),"SOURCE","MISMATCH","P1","OPEN_ROUTED","PHASE-077-GRAPHITE-CLOSURE","Report the gain as an in-sample flexibility diagnostic; require capacity-normalized parity, held-out comparison and uncertainty before transferring skew into a physical production model.","Phase 077",[],"No transferable physical-skew or predictive authority."),
    ]


def is_link_like(path: Path) -> bool:
    return path.is_symlink() or path.is_junction()


def guard_output(output: Path) -> None:
    lexical = Path(os.path.abspath(output)); default = Path(os.path.abspath(DEFAULT_OUTPUT))
    if is_link_like(output) or lexical.exists() and lexical.resolve() != lexical:
        raise SystemExit("output cannot be a symlink, junction, or reparse escape")
    if lexical == default:
        if lexical.parent.resolve() != lexical.parent:
            raise SystemExit("default output parent cannot traverse a link or junction")
        staged = sorted(x for x in str(git("diff", "--cached", "--name-only")).splitlines() if x)
        allowed = [CONTROL_PATHS, sorted(CONTROL_PATHS + [str(DEFAULT_OUTPUT).replace("\\", "/")])]
        if staged not in allowed:
            raise SystemExit(f"JSON-last requires exact staged controls (optionally prior matrix), got {staged}")
        if str(RESULT).replace("\\", "/") not in staged:
            raise SystemExit("result document must be staged before JSON-last collection")
        checked = CONTROL_PATHS + [str(DEFAULT_OUTPUT).replace("\\", "/")]
        unstaged = [x for x in str(git("diff", "--name-only", "--", *checked)).splitlines() if x]
        if unstaged:
            raise SystemExit(f"control files have unstaged changes: {unstaged}")
        return
    temp_root = Path(tempfile.gettempdir()).resolve(); parent = lexical.parent.resolve()
    try:
        parent.relative_to(temp_root)
    except ValueError as exc:
        raise SystemExit("explicit output must remain below the system temporary directory") from exc
    if not lexical.name.startswith("matrix-") or lexical.suffix != ".json":
        raise SystemExit("temporary output name must match matrix-*.json")
    if not parent.is_dir() or is_link_like(lexical.parent):
        raise SystemExit("temporary output parent must be a real directory")


def atomic_write(output: Path, obj: dict[str, Any]) -> None:
    guard_output(output)
    data = (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    destination = Path(os.path.abspath(output)); parent = destination.parent.resolve()
    fd, tmp_name = tempfile.mkstemp(prefix=".phase065-step74-", suffix=".json.tmp", dir=str(parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data); handle.flush(); os.fsync(handle.fileno())
        if is_link_like(destination) or destination.exists() and destination.resolve() != destination:
            raise SystemExit("output became a link-like escape before replace")
        os.replace(tmp_name, destination)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def build() -> dict[str, Any]:
    topology = json.loads(blob("Codex/results/PHASE_065_SOURCE_PROCESS_TOPOLOGY.json", EXPECTED_PARENT))
    code_matrix = json.loads(blob("Codex/results/PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json", EXPECTED_PARENT))
    skew_matrix = json.loads(blob("Codex/results/PHASE_065_SKEW_MATERIAL_AUTHORITY_MATRIX.json", EXPECTED_PARENT))
    runtime_matrix = json.loads(blob("Codex/results/PHASE_065_INITIALIZATION_ROUTE_MATRIX.json", EXPECTED_PARENT))

    source_specs = [
        ("Claude/docs/v1.0.24/CODE_GUIDE_v24.md","implementation guide source","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/CODE_GUIDE_v24.html","generated guide full wrapper/vendor/footer","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/FITTING_GUIDE.md","fitting guide","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py","frozen executable source","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/test_gates_v1024.py","release test","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/test_gates_v1024_reflect.py","reflect test","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/test_gates_v1024_selfconsistent.py","same-code self-consistency test","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/results/REFLECT_SEED_TABLE.md","reflect seed contract","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/results/PHASE_R2_RESULT.md","R2 record","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/results/PHASE_R3_RESULT.md","R3 record","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/results/MERGE_READINESS_v24.md","merge-readiness record","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/results/HANDOVER_v24.md","release handover","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/results/comp_R1/CHERRYPICK_R1.md","adoption decision","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/results/comp_R1/W1/gr_2L.tex","rejected candidate","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/_sections/ch1_sec16b_lcoomega.tex","LCO Omega theory","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/_sections/ch2_sec05_mixing.tex","regular-solution derivation","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/_sections/ch3v22_sec02b_sifr.tex","Si regular-solution theory","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/_sections/ch3v22_sec05_code.tex","main-tree implementation section","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/_sections/ch1_sec05b_gr2L.tex","main-text profile identifiers","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/ch1_graphite_v1.0.24.tex","graphite master main-body topology","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/ch2_lco_v1.0.24.tex","LCO master main-body topology","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/ch3_si_v1.0.24.tex","Si master main-body topology","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/_sections/ch1_sec00_intro.tex","graphite introduction prose","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/_sections/ch1_sec01_n0n1.tex","graphite transition implementation prose","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/_sections/ch1_sec03_center.tex","graphite center implementation prose","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/_sections/ch2_sec04_einstein.tex","LCO regression prose","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/_sections/ch2_sec08_synthesis.tex","LCO synthesis regression prose","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/_sections/ch1_sec18_inputs.tex","Part-T implementation mapping prose","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/_sections/ch1_sec12_lcocenter.tex","LCO center implementation prose","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/_sections/ch1_sec15_lcoelec.tex","LCO current implementation prose","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/_sections/ch3v22_sec01_map.tex","Si code synthesis prose","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/_sections/ch3v22_sec02_cases.tex","Si case code captions","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/_sections/ch3v22_sec03_blend.tex","Si blend implementation prose","AGENT_FULL_READ",BASELINE),
        ("Claude/results/comp_v24/VALIDATION_SYNTHESIS.md","validation synthesis","AGENT_FULL_READ",BASELINE),
        ("Claude/results/comp_v24/LCO_DIAGNOSIS.md","LCO proxy diagnosis","AGENT_FULL_READ",BASELINE),
        ("Claude/results/comp_v24/TAKE_VS_DISCARD.md","later disposition","AGENT_FULL_READ",BASELINE),
        ("Claude/results/comp_v24/v24_regsol2.py","bound-constrained regular-solution helper","AGENT_FULL_READ",BASELINE),
        ("Claude/results/comp_v24/IMPROVEMENT_DIRECTIONS.md","candidate improvement directions","AGENT_FULL_READ",BASELINE),
        ("Claude/results/comp_v24/v24_graphite_asym.py","asymmetric graphite prototype","AGENT_FULL_READ",BASELINE),
        ("Claude/results/comp_v24/INV_code_in_body.md","main-body code inventory","DIRECT_READ",BASELINE),
        ("Claude/results/comp_v24/v24_graphite_firstlook.py","capacity helper","AGENT_FULL_READ",BASELINE),
        ("Claude/results/comp_v24/v24_rate_broadening.py","rate helper","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/results/v1024_final_sample.py","nonportable sample helper","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24/results/v1024_reflect_curves.py","nonportable plot helper","AGENT_FULL_READ",BASELINE),
        ("Claude/results/comp_v24/fit_registry.md","no-final-LF record","AGENT_FULL_READ",BASELINE),
        ("Claude/results/comp_v24/param_dist_stats.md","no-final-LF record","AGENT_FULL_READ",BASELINE),
        ("Claude/docs/v1.0.24.1/ARCHIVE_NOTE.md","mirror/archive note","AGENT_FULL_READ",BASELINE),
        ("Codex/results/PHASE_065_SOURCE_PROCESS_TOPOLOGY.json","Step 70 topology","MACHINE_FULL_TRAVERSAL",EXPECTED_PARENT),
        ("Codex/results/PHASE_065_STEP_070_SOURCE_PROCESS_TOPOLOGY_RESULT.md","Step 70 result","DIRECT_READ",EXPECTED_PARENT),
        ("Codex/results/PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json","Step 71 matrix","MACHINE_FULL_TRAVERSAL",EXPECTED_PARENT),
        ("Codex/results/PHASE_065_STEP_071_CODE_PROFILE_DEFAULT_RESULT.md","Step 71 result","AGENT_FULL_READ",EXPECTED_PARENT),
        ("Codex/results/PHASE_065_SKEW_MATERIAL_AUTHORITY_MATRIX.json","Step 72 matrix","MACHINE_FULL_TRAVERSAL",EXPECTED_PARENT),
        ("Codex/results/PHASE_065_STEP_072_SKEW_MATERIAL_AUTHORITY_RESULT.md","Step 72 result","DIRECT_READ",EXPECTED_PARENT),
        ("Codex/results/PHASE_065_INITIALIZATION_ROUTE_MATRIX.json","Step 73 route matrix","MACHINE_FULL_TRAVERSAL",EXPECTED_PARENT),
        ("Codex/results/PHASE_065_RUNTIME_ATTESTATION.json","Step 73 runtime attestation","MACHINE_FULL_TRAVERSAL",EXPECTED_PARENT),
        ("Codex/results/PHASE_065_STEP_073_INITIALIZATION_RUNTIME_RESULT.md","Step 73 result","DIRECT_READ",EXPECTED_PARENT),
    ]
    bindings = [binding(*spec) for spec in source_specs]

    s70_ids = [f"P065-S70-F{n:02d}" for n in (6,8,10,11,14,34,35,36,39,41,42,43,44)]
    s71_ids = ["P065-S71-F01", "P065-S71-F06"]
    s72_ids = ["P065-S72-F02", "P065-S72-F05"]
    s70 = {x["id"]: x for x in topology["findings"]}
    s71 = {x["finding_id"]: x for x in code_matrix["findings"]}
    s72 = {f"P065-{x['id']}": x for x in skew_matrix["findings"]}
    routes = []
    for route_id in s70_ids:
        routes.append({"route_id":route_id,"origin_step":70,"origin_artifact":"Codex/results/PHASE_065_SOURCE_PROCESS_TOPOLOGY.json","origin_record":copy.deepcopy(s70[route_id]),"disposition":"PRESERVE_EXACT_ORIGIN_RECORD"})
    for route_id in s71_ids:
        routes.append({"route_id":route_id,"origin_step":71,"origin_artifact":"Codex/results/PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json","origin_record":copy.deepcopy(s71[route_id]),"disposition":"PRESERVE_EXACT_ORIGIN_RECORD"})
    for route_id in s72_ids:
        routes.append({"route_id":route_id,"origin_step":72,"origin_artifact":"Codex/results/PHASE_065_SKEW_MATERIAL_AUTHORITY_MATRIX.json","origin_record":copy.deepcopy(s72[route_id]),"disposition":"PRESERVE_EXACT_ORIGIN_RECORD"})

    matrix_rows = rows()
    obj: dict[str, Any] = {
        "schema_version":"phase065-step74-v1", "generated_date":"2026-08-31",
        "artifact_kind":"document-code-guide-conformance-matrix",
        "baseline_commit":BASELINE, "expected_parent":EXPECTED_PARENT,
        "expected_subject":EXPECTED_SUBJECT, "branch":BRANCH, "gate":GATE,
        "authority":{
            "internal_conformance_audit":True, "external_scientific_truth":False,
            "external_material_truth":False, "external_experimental_truth":False,
            "external_proposition_support":False, "canonical_model_selected":False,
            "production_repair_complete":False, "publication_ready":False,
            "generated_artifact_independent_support":False,
            "ceiling":"Exact frozen-source/guide/result/runtime conformance and downstream routing only.",
        },
        "source_policy":{
            "behavior_authority":"isolated Step 73 runtime plus frozen executable source",
            "science_authority":"primary source text only; proposition support remains separately bounded",
            "adoption_authority":"Git chronology and explicit disposition records",
            "generated_artifact_rule":"HTML/PDF/image repetition does not multiply source support",
            "external_scientific_evidence_network_used":False,
            "git_remote_reference_network_used":True, "frozen_source_execution":False,
            "claude_tree_written":False, "child_process_allowlist":["git"],
            "json_last":True,
        },
        "control_source_bindings":[
            control_binding("Codex/work/v1024_phase065/build_phase065_step74.py","JSON_LAST_BUILDER"),
            control_binding("Codex/work/v1024_phase065/validate_phase065_step74.py","INDEPENDENT_VALIDATOR"),
            control_binding("Codex/results/PHASE_065_STEP_074_DOC_CODE_GUIDE_RESULT.md","RESULT_FIRST_RESULT"),
            control_binding("Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md","PARENT_LEDGER"),
            control_binding("Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md","CANONICAL_LEDGER"),
            control_binding("Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md","ACTIVE_HANDOVER"),
        ],
        "source_bindings":bindings,
        "artifact_genealogy":[
            {"source":"Claude/docs/v1.0.24/CODE_GUIDE_v24.md","derived":"Claude/docs/v1.0.24/CODE_GUIDE_v24.html","relation":"GENERATED_FROM","generator_command":"GROUND_NOT_FOUND","independent_support":False},
            {"source":"Claude/docs/v1.0.24/ch1_graphite_v1.0.24.tex","derived":"Claude/docs/v1.0.24/ch1_graphite_v1.0.24.pdf","relation":"GENERATED_FROM_CLOSURE","generator_command":"GROUND_NOT_FOUND","independent_support":False},
            {"source":"Claude/docs/v1.0.24/ch2_lco_v1.0.24.tex","derived":"Claude/docs/v1.0.24/ch2_lco_v1.0.24.pdf","relation":"GENERATED_FROM_CLOSURE","generator_command":"GROUND_NOT_FOUND","independent_support":False},
            {"source":"Claude/docs/v1.0.24/ch3_si_v1.0.24.tex","derived":"Claude/docs/v1.0.24/ch3_si_v1.0.24.pdf","relation":"GENERATED_FROM_CLOSURE","generator_command":"GROUND_NOT_FOUND","independent_support":False},
            {"source":"Claude/docs/v1.0.24","derived":"Claude/docs/v1.0.24.1","relation":"130_BYTE_IDENTICAL_MIRROR_PAIRS_PLUS_ARCHIVE_NOTE","generator_command":"NOT_APPLICABLE","independent_support":False},
        ],
        "authority_precedence":[
            {"claim_class":"behavior","authority":"isolated runtime, then frozen executable source","cannot_overrule":"scientific proposition or adoption"},
            {"claim_class":"science","authority":"primary full text and explicit derivation","cannot_overrule":"runtime behavior or Git adoption"},
            {"claim_class":"adoption","authority":"Git chronology and explicit disposition","cannot_overrule":"scientific truth or runtime behavior"},
            {"claim_class":"artifact","authority":"authoring source plus reproducible generator","cannot_overrule":"source content"},
        ],
        "input_routes":routes, "conformance_rows":matrix_rows,
        "findings":[
            {"id":"S74-F01","severity":"P1","finding":"Route-specific regular-solution, root, unit, width and blend behavior conflicts with blanket/full-conformance records.","owner":"PHASE-083-IMPLEMENTATION-CONTRACT"},
            {"id":"S74-F02","severity":"P1","finding":"LCO per-peak Omega, analytic real-fit, capacity-basis and main-body implementation claims exceed their authority.","owner":"PHASE-078-LCO-CLOSURE"},
            {"id":"S74-F03","severity":"P2","finding":"HTML generation, versioning, unit labels, portability, visual defects and exact output require repair.","owner":"PHASE-089-RELEASE-QA"},
            {"id":"S74-F04","severity":"P2","finding":"The inherited 17-image missing-glyph count conflicts with the fresh 15-path visual numerator; the remaining two identities are GROUND_NOT_FOUND.","owner":"PHASE-089-RELEASE-QA"},
        ],
        "counts":{
            "conformance_rows":len(matrix_rows),
            "severity_p1":sum(x["severity"] == "P1" for x in matrix_rows),
            "severity_p2":sum(x["severity"] == "P2" for x in matrix_rows),
            "severity_none":sum(x["severity"] == "NONE" for x in matrix_rows),
            "open_routed":sum(x["status"] == "OPEN_ROUTED" for x in matrix_rows),
            "input_routes":len(routes), "source_bindings":len(bindings),
            "step73_runtime_routes":len(runtime_matrix["routes"]),
        },
        "next_gate":"Step 75.1 must disposition all 261 occurrences and route every open Step 70-74 obligation to exactly one canonical owner without rewriting Claude/**.",
    }
    clone = copy.deepcopy(obj)
    obj["semantic_sha256"] = sha256(canonical(clone))
    return obj


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(); guard_output(args.output)
    if not RESULT.exists():
        raise SystemExit("result document must exist before JSON-last collection")
    obj = build(); atomic_write(args.output, obj)
    print(GATE, json.dumps({"rows":len(obj["conformance_rows"]),"routes":len(obj["input_routes"]),"semantic_sha256":obj["semantic_sha256"]},sort_keys=True,separators=(",",":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
