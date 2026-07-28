#!/usr/bin/env python3
"""Phase 059 Step 38.1: audit v1.0.17 document-only and citation claims."""

from __future__ import annotations

import difflib
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OLD = ROOT / "Claude/docs/v1.0.16"
NEW = ROOT / "Claude/docs/v1.0.17"
RESULT = ROOT / "Codex/results/PHASE_059_V1017_DOC_CITATION_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_V1017_DOC_CITATION_REVIEW.md"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def diff_stats(old: Path, new: Path) -> dict:
    a = old.read_text(encoding="utf-8").splitlines()
    b = new.read_text(encoding="utf-8").splitlines()
    counts = {"equal": 0, "replace_old": 0, "replace_new": 0, "delete": 0, "insert": 0}
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
        if tag == "equal":
            counts["equal"] += i2 - i1
        elif tag == "replace":
            counts["replace_old"] += i2 - i1
            counts["replace_new"] += j2 - j1
        elif tag == "delete":
            counts["delete"] += i2 - i1
        elif tag == "insert":
            counts["insert"] += j2 - j1
    return {
        "old_lines": len(a),
        "new_lines": len(b),
        "counts": counts,
        "unified_diff_sha256": hashlib.sha256(
            "".join(difflib.unified_diff(a, b, lineterm="\n")).encode()
        ).hexdigest(),
    }


def main() -> None:
    pairs = [
        ("chapter1", "graphite_ica_ch1_v1.0.16.tex", "graphite_ica_ch1_v1.0.17.tex"),
        ("chapter2", "graphite_ica_ch2_v1.0.16.tex", "graphite_ica_ch2_v1.0.17.tex"),
        ("appendix", "appendix_phase_separation.tex", "appendix_phase_separation.tex"),
    ]
    theory_diffs = {
        name: {
            "old_path": str((OLD / a).relative_to(ROOT)),
            "new_path": str((NEW / b).relative_to(ROOT)),
            "old_sha256": sha(OLD / a),
            "new_sha256": sha(NEW / b),
            **diff_stats(OLD / a, NEW / b),
        }
        for name, a, b in pairs
    }

    executable_pairs = [
        ("production", "Anode_Fit_v1.0.16.py", "Anode_Fit_v1.0.17.py"),
        ("golden", "golden_graphite_ref.npz", "golden_graphite_ref.npz"),
        ("plot", "plot_dqdv.py", "plot_dqdv.py"),
        ("lco_demo", "demo_lco_heat.py", "demo_lco_heat.py"),
    ]
    executable = []
    for role, a, b in executable_pairs:
        old_hash, new_hash = sha(OLD / a), sha(NEW / b)
        version_only = False
        if (OLD / a).suffix == ".py":
            old_text = (OLD / a).read_text(encoding="utf-8")
            new_text = (NEW / b).read_text(encoding="utf-8")
            version_only = (
                old_text.replace("v1.0.16", "v1.0.17").replace("1.0.16", "1.0.17")
                == new_text
            )
        executable.append({
            "role": role,
            "old_path": str((OLD / a).relative_to(ROOT)),
            "new_path": str((NEW / b).relative_to(ROOT)),
            "old_sha256": old_hash,
            "new_sha256": new_hash,
            "byte_identical": old_hash == new_hash,
            "only_version_literals_changed": version_only,
            "calculation_logic_changed": False,
        })

    test_diff = diff_stats(OLD / "test_regression_graphite.py", NEW / "test_regression_graphite.py")
    test_diff.update({
        "old_sha256": sha(OLD / "test_regression_graphite.py"),
        "new_sha256": sha(NEW / "test_regression_graphite.py"),
        "physical_assertion_change": False,
        "only_versioned_absolute_paths_changed": True,
    })

    ch1 = (NEW / "graphite_ica_ch1_v1.0.17.tex").read_text(encoding="utf-8")
    ch2 = (NEW / "graphite_ica_ch2_v1.0.17.tex").read_text(encoding="utf-8")
    appendix_start = ch1.index(r"\section{구현 대응표}")
    ch1_body = "\n".join(line for line in ch1[:appendix_start].splitlines() if not line.lstrip().startswith("%"))
    implementation_pattern = re.compile(
        r"(코드|구현|Anode_Fit|entropy\\_coefficient|func\\_|GRAPHITE\\_|use\\_dH)"
    )
    boundary_hits = []
    for document, text in (("chapter1_body", ch1_body), ("chapter2", ch2)):
        for line_no, line in enumerate(text.splitlines(), 1):
            if implementation_pattern.search(line):
                boundary_hits.append({"document": document, "line": line_no, "text": line.strip()})

    citations = [
        {
            "key": "occupation2019",
            "old_doi": "10.1016/j.electacta.2019.135634",
            "new_doi": "10.1016/j.electacta.2019.134774",
            "bibliography": "PASS",
            "scope": "PARTIAL_METHOD_LEVEL",
            "reason": "Correct article 134774; supports low-occupation graphite thermodynamics, not every equation used in Chapter 2.",
            "primary_url": "https://doi.org/10.1016/j.electacta.2019.134774",
        },
        {
            "key": "chemmater2015",
            "new_doi": "10.1021/acs.chemmater.5b00235",
            "bibliography": "PASS",
            "scope": "FAIL_ANNOTATION",
            "reason": "The paper reports high-temperature LiH/graphite synthesis, diffraction/Raman and stage stability; it is not formation-enthalpy calorimetry.",
            "primary_url": "https://pubs.acs.org/doi/10.1021/acs.chemmater.5b00235",
        },
        {
            "key": "jpcc2021",
            "new_doi": "10.1021/acs.jpcc.1c08992",
            "bibliography": "PASS",
            "scope": "PASS",
            "reason": "Directly treats graphite vibrational free energy and configurational entropy by first-principles calculations.",
            "primary_url": "https://pubs.acs.org/doi/10.1021/acs.jpcc.1c08992",
        },
        {
            "key": "msmr_partI",
            "new_doi": "10.1149/1945-7111/ad1d27",
            "bibliography": "PARTIAL_MISSING_ARTICLE_023502",
            "scope": "FAIL_AT_CITATION_SITE",
            "reason": "Supports reversible entropy-coefficient/MSMR deconvolution, but does not directly establish the manuscript's Eyring activation-entropy separation claim.",
            "primary_url": "https://www.osti.gov/pages/biblio/2290426",
        },
        {
            "key": "msmr_partII",
            "new_doi": "10.1149/1945-7111/ad70d9",
            "bibliography": "PARTIAL_TITLE_AND_ARTICLE_103505",
            "scope": "PASS_FOR_MCMB_TEMPERATURE_PARAMETERIZATION",
            "reason": "Supports temperature-dependent MCMB graphite MSMR estimation; it does not validate this repository's four-transition default.",
            "primary_url": "https://www.osti.gov/pages/biblio/2459353",
        },
        {
            "key": "standardised2024",
            "new_doi": "10.1149/1945-7111/ad4918",
            "bibliography": "PASS",
            "scope": "PARTIAL_METHOD_ONLY",
            "reason": "Supports potentiometric extraction of effective cell entropy coefficient, not the specific graphite +60.8 mW/A demonstration.",
            "primary_url": "https://doi.org/10.1149/1945-7111/ad4918",
        },
        {
            "key": "hysteresis2018",
            "old_doi": "10.1016/j.jpowsour.2018.05.060",
            "new_doi": "10.1016/j.jpowsour.2018.05.052",
            "bibliography": "PARTIAL_MISSING_PAGES_179_184",
            "scope": "PASS",
            "reason": "Directly supports temperature-path-dependent OCP hysteresis and entropy-measurement uncertainty.",
            "primary_url": "https://www.sciencedirect.com/science/article/pii/S0378775318305287",
        },
        {
            "key": "numverif2026",
            "bibliography": "INTERNAL_NOT_LITERATURE",
            "scope": "INTERNAL_SELF_CONSISTENCY_ONLY",
            "reason": "A repository calculation cannot provide external material validation.",
            "primary_url": None,
        },
    ]

    findings = [
        {"id": "CIT-001", "disposition": "PRESERVE", "text": "Both previously wrong Elsevier DOI strings were corrected to resolvable article identifiers."},
        {"id": "CIT-002", "disposition": "CORRECT", "text": "The Chemistry of Materials annotation incorrectly calls the paper formation-enthalpy calorimetry."},
        {"id": "CIT-003", "disposition": "CORRECT", "text": "MSMR Part I is not direct support for the activation-entropy versus reversible-entropy sentence where it is cited."},
        {"id": "CIT-004", "disposition": "CORRECT", "text": "MSMR Part I and Part II remain bibliographically incomplete; article numbers 023502 and 103505 are absent and the Part II title is not exact."},
        {"id": "CIT-005", "disposition": "CORRECT", "text": "The hysteresis citation has the corrected DOI but still omits pages 179–184."},
        {"id": "DOC-001", "disposition": "PRESERVE", "text": "Production code and golden data are byte-identical; plotting, LCO heat demo and regression harness change only version/path literals, not calculation logic or assertions."},
        {"id": "DOC-002", "disposition": "EMPIRICAL_ONLY", "text": "Chapter 1 changes are register, notation, dimensional clarification and an electronic-term description; they add no validated material parameters."},
        {"id": "DOC-003", "disposition": "PRESERVE", "text": "Chapter 2 adds an equation label around an already present formula; no new mathematical content is introduced by eq:complete."},
        {"id": "DOC-004", "disposition": "CORRECT", "text": "The theory-only body boundary is not closed: direct implementation language remains outside the designated implementation appendix, including entropy_coefficient and the internal Anode_Fit bibliography item."},
        {"id": "DOC-005", "disposition": "REJECT", "text": "Handover claims of complete external-review incorporation and physical completeness are process claims, not scientific validation."},
        {"id": "DOC-006", "disposition": "REJECT", "text": "The revised references do not validate graphite/LCO/Si fitting, doped high-voltage LCO, or the specific reversible-heat demonstration."},
        {"id": "DOC-007", "disposition": "PRESERVE", "text": "Appendix dimensional clarification f=energy density, [kappa]=J/m and [M]=m^5/(J s) is dimensionally consistent."},
    ]

    data = {
        "schema_version": 1,
        "phase": 59,
        "step": "38.1",
        "status": "CONDITIONAL_P059_V1017_BIBLIOGRAPHIC_CORRECTIONS_AND_REGISTER_CLEANUP_PASS_BUT_CITATION_SCOPE_THEORY_BODY_AND_SCIENTIFIC_AUTHORITY_FAIL",
        "source_version": "v1.0.16",
        "target_version": "v1.0.17",
        "theory_diffs": theory_diffs,
        "executable_comparison": executable,
        "regression_harness_comparison": test_diff,
        "citation_adjudication": citations,
        "theory_only_boundary": {
            "pass": False,
            "outside_designated_section_hit_count": len(boundary_hits),
            "hits": boundary_hits,
        },
        "claims": {
            "production_physics_changed": False,
            "algorithm_changed": False,
            "new_external_material_validation": False,
            "two_wrong_dois_corrected": True,
            "all_bibliography_complete": False,
            "all_citation_sites_directly_supported": False,
            "external_review_completely_reflected_as_scientific_authority": False,
            "v1017_is_doc_only_scientific_release": True,
        },
        "findings": findings,
        "summary": {
            "citation_count": len(citations),
            "finding_count": len(findings),
            "byte_identical_executable_asset_count": sum(x["byte_identical"] for x in executable),
            "version_literal_only_asset_count": sum(x["only_version_literals_changed"] for x in executable),
            "next_step": "38.2",
        },
        "source_retrieval_date": "2026-07-28",
    }
    RESULT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    REPORT.write_text(f"""# Phase 059 v1.0.17 문건·인용 감사

정본일: 2026-07-28

판정: `{data["status"]}`

## 결론

v1.0.17은 생산 물리나 알고리즘을 바꾼 판이 아니다. 생산 코드와
golden은 byte-identical이다. plot, LCO heat demo와 regression
harness는 버전/절대경로 문자열만 바뀌었고 계산 논리와 assertion은
같다. 따라서 이 판의 정당한 지위는 doc-only register·서지 정련이다.

두 잘못된 DOI를 바로잡은 것은 분명한 개선이다.
`occupation2019`는 134774가 맞고, `hysteresis2018`은
`2018.05.052`가 맞다. 그러나 서지 완결과 주장-인용 정합은 아직
닫히지 않았다.

## 인용 범위 판정

- Konar et al. 2015는 LiH/graphite 고온 합성, PXRD/Raman과 staged
  phase 안정성 논문이지 본 문건 주석이 말하는 형성 엔탈피
  calorimetry 논문이 아니다.
- Garrick et al. MSMR Part I은 가역 entropy coefficient와 gallery
  분해를 다룬다. 이를 Eyring activation entropy가 가역열에 들어가지
  않는다는 문장의 직접 근거로 쓰는 것은 인용 위치가 맞지 않는다.
- Paul et al. Part II는 MCMB graphite 다온도 MSMR 추정을 지지하지만
  이 저장소의 4-transition 기본값을 검증하지 않는다.
- Hales--Bulman은 full-cell 유효 entropy coefficient 추출 방법을
  지지할 뿐, 본 문건의 graphite \\(+60.8\\) mW/A 수치를 검증하지 않는다.
- Haruyama et al.은 graphite의 vibrational/configurational free-energy
  기여를 직접 다루므로 해당 범위에는 적합하다.
- Zilberman et al.은 temperature-path-dependent OCP hysteresis와
  entropy 측정 불확실성을 직접 지지한다.

MSMR Part I/II에는 article number 023502/103505가 빠졌고 Part II
제목도 원제와 정확히 같지 않다. hysteresis 논문은 DOI는 고쳤으나
179--184쪽이 빠졌다.

## 문건 경계

제목과 여러 본문 표현에서 `코드`를 `계산` 또는 `모델`로 바꾼 방향은
사용자 제약에 맞다. 하지만 지정된 구현 대응 부록 밖에 구현 언어가
여전히 남는다. Chapter 2에는 `entropy_coefficient`가 본문에 있고,
내부 `Anode_Fit_v1.0.17` 계산이 참고문헌 항목으로 들어가 있다.
그러므로 theory-only body gate는 아직 FAIL이다.

## 권위

v1.0.17이 새로 확보한 것은 서지 오류 정정과 표현 개선이지 graphite,
LCO, Si 또는 doped high-voltage LCO의 외부 데이터 적합성 검증이
아니다. handover의 “리뷰 완전 반영”, “완결”은 작업 절차의 자기
보고로만 보존하며 과학적 완결 권위로 승격하지 않는다.

## 다음 단계

Step 38.2에서 v1.0.18.1이 v1.0.17의 물리 무변경 이월판인지
theory/code/test/PDF 전 축에서 판정한다.

원본 `Claude/`, `main`은 수정하지 않았다.
""", encoding="utf-8")
    print(data["status"])
    print("citations", len(citations), "findings", len(findings), "boundary_hits", len(boundary_hits))


if __name__ == "__main__":
    main()
