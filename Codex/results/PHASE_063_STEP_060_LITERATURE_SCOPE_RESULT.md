# Phase 063 Step 060 — v1.0.22 Literature, Quantity and Scope Authority Result

상태: `PASS_WITH_CONCERNS`

Precommit Gate: `PASS_P063_STEP60_LITERATURE_SCOPE_WITH_CONCERNS`

Postcommit terminal: `PENDING_AT_PRECOMMIT_BY_DESIGN`

Gate 의미: frozen v1.0.22의 bibliography/citation/DOI occurrence, 정량·재료 claim의 현재 권위 상한, 충돌과 후속 원문 검증 조건을 inventory했다. 이 Gate는 외부 논문의 실재, full-text proposition, material truth, canonical equation 또는 최종 원고 채택을 승인하지 않는다.

정본일: 2026-08-29

Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`

예정 parent: `07a0f3ead16a072550919b86d1d41580682fd92d`

## 1. 목적과 권위 경계

Step 60은 Task 60A–60C에 따라 final release와 process/candidate surface의 bibliography key, DOI-like string, equation/numeric/material candidate를 occurrence 단위로 보존하고, bibliographic existence·full-text method·exact equation·exact value/unit/basis·sample/material/protocol·current-model mapping·external experiment의 권위 축을 분리한다. Frozen repository의 `tier A/B/C`, `Crossref 확인`, `원문 확인`, `실측` 문구는 자기보고이며 원천 증거를 대신하지 않는다.

외부 네트워크와 resolver를 이 Step에서 사용하지 않았다. Primary-literature truth는 Phase 071 owner 전까지 모두 `UNVERIFIED_EXTERNAL` 또는 `GROUND_NOT_FOUND`다. DOI/abstract/title은 full-text proposition으로 승격하지 않았고, `Claude/**`는 수정하지 않는다.

## 2. 복구와 진입 조건

- `Codex/AGENTS.md` 1–180, master plan 1–665, Phase 063 detailed plan 1–681을 현재 HEAD에서 전문 재확인했다.
- Step 59 result 1–488, 두 execution ledger와 active handover를 현재본 기준으로 다시 읽었다.
- Step 59 commit `07a0f3ead16a072550919b86d1d41580682fd92d`은 local HEAD/upstream/live origin과 일치했고 status는 clean이었다.
- frozen baseline은 `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`이다.
- Step 58의 204 manifest occurrences는 `200 FULL_TEXT + 4 FULL_PDF`다. 별도 supplemental process-control source 1개는 manifest 분모에 합치지 않는다.
- Validator-first RED는 artifact 부재 상태에서 `FAIL_P063_STEP60: E_ARTIFACT_MISSING: Codex/results/PHASE_063_V1022_LITERATURE_SCOPE_MATRIX.json`을 반환했다.

## 3. 독립 검독 범위

- final-release audit: 63 identities 전부를 frozen Git object로 재대조했다. 59 text/10,462행/847,155 bytes와 4 PDF/133쪽/2,137,917 bytes의 blob/hash/extent 불일치가 0이었다. PDF 133쪽은 text traversal했지만 새 visual-layout 판정으로 승격하지 않는다.
- process/candidate audit: VERSION_PLAN 6, STATUS_MACHINE_PROCESS 10, COMPETING_REVIEW_CANDIDATE 125와 supplemental 1, 합계 142 text/19,856행/2,005,191 bytes를 1–EOF 재검독하고 identity mismatch 0을 확인했다.
- material/quantity audit: final 및 candidate 핵심 source 33개 4,134행을 전문 의미 검독했고, 그 밖의 수동 판정 근거 11개 interval/10개 source/409개 고유 행을 명시적 의미 검독했으며, production code 535개 고유 행은 부분 검독했다. 수동 literature/material 근거 52개 전부가 이 semantic attestation에 포함된다. 이 검독은 Step 61 runtime/code 검증을 대신하지 않는다.
- topology/read-attestation JSON은 strict parse와 full traversal로 각각 18,715/4,408 nodes, duplicate key와 nonfinite 값 0을 확인했다.

## 4. Citation과 bibliography closure

- 활성 root: `210 cite commands / 258 expanded key occurrences / 88 root-local routes`이며 missing cited key, keyed unused bibliography, root 내부 duplicate key는 모두 0이다.
- root별 ch1/ch2/ch3는 각각 `87/114/39`, `53/68/15`, `70/76/34`이다. Appendix root는 citation 0이다.
- `P063-SRC-0005 ch1_appD_si.tex`는 별도 manifest orphan으로 `17 commands / 20 key occurrences / 14 unique keys`; root/build adoption은 `GROUND_NOT_FOUND`다.
- keyed bibliography는 88 physical definitions/87 unique keys다. `swiderska2019`은 ch1/ch2에 동일 metadata로 두 번 정의되며 root별 정상, merged duplicate다.
- `P063-SRC-0056:483–495`의 수동 A1–A5 다섯 참고문헌은 key도 `\cite` route도 없는 별도 occurrence다. 따라서 전체 bibliography record는 `88 keyed + 5 manual = 93`이다.
- final text DOI-like string은 84 occurrences/80 unique normalized strings다. Rendered PDF reference pages에서 84/84 alphanumeric sequence를 찾았지만 URI annotation은 0이고 exact in-text cite→PDF page mapping은 GNF다.
- `numverif2026`은 외부 문헌이 아니라 내부 numerical regression record다. 본문 citation이 존재해도 권위는 `INTERNAL_REGRESSION_ONLY`다.
- process/candidate/supplemental의 `414 commands / 492 key occurrences`는 lexical parser가 찾은 전 occurrence를 그대로 센 값이다(`COMPETING_REVIEW_CANDIDATE 487 + STATUS_MACHINE_PROCESS 5`; VERSION_PLAN과 supplemental은 0). malformed·quoted 예시도 provenance 보존을 위해 분모에서 임의 제외하지 않는다.
- 201개 text source 전수에서 display-environment/bracket equation 339건, TeX-syntax delimiter-math 14,958건, numeric/unit/material/citation/bibliography/DOI lexical claim-candidate line 8,751건 각각에는 7개 권위축을 모두 `NOT_ESTABLISHED_BY_LEXICAL_OCCURRENCE`로 배정했다. Delimiter parser는 TeX 등 비-Markdown source의 합법적 다중행과 `$…$$…$` 인접 close/open 경계를 statefully 보존한다. Markdown에서는 state-free `$`의 right-flank로 open 가능성을 판정하고 열린 state의 다음 `$`를 close endpoint로 사용해 일반 문단·fenced LaTeX의 다중행을 보존하되, 빈 행·표 행·heading·fence marker 같은 구조 경계에서는 state를 회복한다. 그 결과 `INLINE_DOLLAR` lexical candidates 14,953건과 display dollar 1건 외에 Markdown에서 방향을 확정할 수 없는 unpaired token 3건을 `UNPAIRED_INLINE_DOLLAR`, 비-Markdown의 파일 말단 미종료 state 1건을 `UNTERMINATED_INLINE_DOLLAR`로 보존한다. All-text raw unescaped dollar 29,914개(`.md` subset 14,075개, `.tex` 15,838개, `.py` 1개)는 candidate delimiter endpoint에 중복·누락 없이 정확히 한 번 대응한다. 모든 raw display opener 339개도 path/line/column/environment candidate에 일대일 대응하며, embedded same-line `\[...\]`와 한 행의 복수 environment를 standalone/multiline display와 함께 inventory한다. 모든 row에는 path/start–end line/ordinal/column/body hash를 남긴다. 이는 전수 lexical occurrence의 권위 상한을 봉인한 것이며 각 delimiter body가 실제 수식 proposition이라고 의미 정규화했다는 주장이 아니다. 별도 수동 의미 판정은 load-bearing literature 12건과 material 12건에 한정된다.

## 5. Result-first manual authority evidence

아래 JSON object는 builder가 그대로 strict parse해 machine matrix에 봉인한다. `source_evidence`는 frozen source occurrence이고, repository 문구의 tier와 Step 60 audit state를 분리한다.

<!-- P063_STEP60_LITERATURE_EVIDENCE_BEGIN -->
```json
{
  "evidence_id": "P063-STEP60-LITERATURE-QUANTITY-SCOPE-AUTHORITY",
  "evidence_date": "2026-08-29",
  "authority_ceiling": "STATIC_FROZEN_OCCURRENCE_AND_INTERNAL_ARITHMETIC_ONLY",
  "external_truth_state": "UNVERIFIED_EXTERNAL",
  "primary_literature_truth_validated": false,
  "inventory_summary": {
    "manifest_sources": 204,
    "manifest_full_text": 200,
    "manifest_full_pdf": 4,
    "supplemental_process_control": 1,
    "all_reviewed_text_sources": 201,
    "all_reviewed_text_physical_lines": 30318,
    "final_root_citation_commands": 210,
    "final_root_citation_key_occurrences": 258,
    "final_root_routes": 88,
    "final_keyed_bibliography_definitions": 88,
    "final_unique_bibliography_keys": 87,
    "manual_unkeyed_references": 5,
    "final_doi_occurrences": 84,
    "final_unique_normalized_dois": 80,
    "process_candidate_supplemental_citation_commands": 414,
    "process_candidate_supplemental_citation_key_occurrences": 492,
    "process_candidate_supplemental_doi_occurrences": 244,
    "process_candidate_supplemental_unique_normalized_dois": 107,
    "all_text_display_equation_candidates": 339,
    "all_text_tex_delimited_math_candidates": 14958,
    "all_text_claim_candidate_lines": 8751
  },
  "authority_axes": [
    "BIBLIOGRAPHIC_EXISTENCE",
    "FULLTEXT_METHOD",
    "EXACT_EQUATION",
    "EXACT_VALUE_UNIT_BASIS",
    "SAMPLE_MATERIAL_COMPOSITION_PROTOCOL",
    "CURRENT_MODEL_MAPPING",
    "EXTERNAL_EXPERIMENTAL_SUPPORT"
  ],
  "semantic_review_attestation": {
    "authority": "INTERNAL_SEMANTIC_REVIEW_ATTESTATION_ONLY",
    "full_text_source_count": 33,
    "full_text_physical_lines": 4134,
    "full_text_rows": [
      {"source_id":"P063-SRC-0002","path":"Claude/docs/v1.0.22/FITTING_GUIDE.md","git_blob":"f097793b69237d6f63705cc07708f8a1adbe7192","read_interval":[1,137],"physical_lines":137,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0003","path":"Claude/docs/v1.0.22/_sections/ch1_appA_signcheck.tex","git_blob":"4583cf94bb25c118702a5a9235562bcc6bbf3db9","read_interval":[1,89],"physical_lines":89,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0019","path":"Claude/docs/v1.0.22/_sections/ch1_sec11_lcointro.tex","git_blob":"68420103dacba4e7f0b2ffbb72a4b57a802c1fb0","read_interval":[1,175],"physical_lines":175,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0020","path":"Claude/docs/v1.0.22/_sections/ch1_sec12_lcocenter.tex","git_blob":"f4a1d85c06d28b254901914f52568707f5115c35","read_interval":[1,112],"physical_lines":112,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0021","path":"Claude/docs/v1.0.22/_sections/ch1_sec13_lcohys.tex","git_blob":"9eac9dc326aaea977867a7f263e8f7458543e34d","read_interval":[1,223],"physical_lines":223,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0022","path":"Claude/docs/v1.0.22/_sections/ch1_sec14_lcodecomp.tex","git_blob":"8ab4d9fde06ae3920b3d02281d984556fb474249","read_interval":[1,143],"physical_lines":143,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0023","path":"Claude/docs/v1.0.22/_sections/ch1_sec15_lcoelec.tex","git_blob":"2a41d8aaf965b18131eea68e5a77d8b7f536f44a","read_interval":[1,396],"physical_lines":396,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0024","path":"Claude/docs/v1.0.22/_sections/ch1_sec16_lcopeak.tex","git_blob":"9e6625f1cca1ac7ab5083fbef746bec29855ee8d","read_interval":[1,70],"physical_lines":70,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0025","path":"Claude/docs/v1.0.22/_sections/ch1_sec17_msmr.tex","git_blob":"90bc83050a0ea7f707e015a20cb441289d0d0e9c","read_interval":[1,176],"physical_lines":176,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0026","path":"Claude/docs/v1.0.22/_sections/ch1_sec18_inputs.tex","git_blob":"2c4e61dd04a4fd81ee56d0f9d4a6649d39f9a955","read_interval":[1,70],"physical_lines":70,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0027","path":"Claude/docs/v1.0.22/_sections/ch1v22_bib.tex","git_blob":"f16cb4c709967f1e57a9b0a6f0ccece8e3b45b4f","read_interval":[1,51],"physical_lines":51,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0043","path":"Claude/docs/v1.0.22/_sections/ch2v22_bib.tex","git_blob":"9884af52a4be61c8695371c8a1c91d68669e7a34","read_interval":[1,21],"physical_lines":21,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0046","path":"Claude/docs/v1.0.22/_sections/ch3v22_bib.tex","git_blob":"33a212799b83e47df84fe890aa9d5ceb7023dfd4","read_interval":[1,42],"physical_lines":42,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0047","path":"Claude/docs/v1.0.22/_sections/ch3v22_notation.tex","git_blob":"87aa209d66ec2a71b165a58d6e25819eeb7ba80a","read_interval":[1,46],"physical_lines":46,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0048","path":"Claude/docs/v1.0.22/_sections/ch3v22_sec00_intro.tex","git_blob":"7e2720e03280b07765a32104521d51ca198bbe02","read_interval":[1,12],"physical_lines":12,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0049","path":"Claude/docs/v1.0.22/_sections/ch3v22_sec01_map.tex","git_blob":"84c2a45e9dbe26e70ab1582520a568ba2823f530","read_interval":[1,132],"physical_lines":132,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0050","path":"Claude/docs/v1.0.22/_sections/ch3v22_sec02_cases.tex","git_blob":"ea88ed0730bb8cbc5f48cd3cacc42fab93f88ded","read_interval":[1,162],"physical_lines":162,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0051","path":"Claude/docs/v1.0.22/_sections/ch3v22_sec03_blend.tex","git_blob":"4966fa1ffbe31364b3b87ba387cd4d439cf658a5","read_interval":[1,278],"physical_lines":278,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0052","path":"Claude/docs/v1.0.22/_sections/ch3v22_sec04_mech.tex","git_blob":"b4c331374a7c03f5de26353cb0655e2c7c21f1dc","read_interval":[1,111],"physical_lines":111,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0053","path":"Claude/docs/v1.0.22/_sections/ch3v22_sec05_code.tex","git_blob":"96b95d9bee7b717a75bf3e128903fb6f4a6c20f3","read_interval":[1,70],"physical_lines":70,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0098","path":"Claude/docs/v1.0.22/results/comp_FR/A18_REVIEW.md","git_blob":"45a78d29478a17a5e48ae13dd4aeda492502de52","read_interval":[1,456],"physical_lines":456,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0143","path":"Claude/docs/v1.0.22/results/comp_R3/E_bridges/L2_TIER_CANDIDATES.md","git_blob":"fe6c16148ddb7190b7e992013d1a4beef58c5038","read_interval":[1,32],"physical_lines":32,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0144","path":"Claude/docs/v1.0.22/results/comp_R3/E_bridges/L5_CHARGEORDER_CHECK.md","git_blob":"c3cfe682acf2c59eb6d27278c9d56ae432407bca","read_interval":[1,40],"physical_lines":40,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0149","path":"Claude/docs/v1.0.22/results/comp_R4/BLEND_ALIGN.md","git_blob":"9f6452fab6d9f133d859683f43ea33083b52b421","read_interval":[1,122],"physical_lines":122,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0151","path":"Claude/docs/v1.0.22/results/comp_R4/L2_REGISTER_PREP.md","git_blob":"6f3cd3925bf1bb6c415e6ebeecd12e07ce7a11f7","read_interval":[1,176],"physical_lines":176,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0152","path":"Claude/docs/v1.0.22/results/comp_R4/L5_RESOURCE.md","git_blob":"6ab95951cbdc2be3a76b7e80cd02febe97130b7b","read_interval":[1,169],"physical_lines":169,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0154","path":"Claude/docs/v1.0.22/results/comp_R4/SI_CASES.md","git_blob":"047ca0b3f6954e7cc1c0817a32fb9ece810e0aaa","read_interval":[1,122],"physical_lines":122,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0155","path":"Claude/docs/v1.0.22/results/comp_R4/SI_ENTROPY.md","git_blob":"97bcf26b1c06ff7fbb152f070d3a3b8115c4eb1c","read_interval":[1,110],"physical_lines":110,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0156","path":"Claude/docs/v1.0.22/results/comp_R4/upgraded/BLEND_UP.md","git_blob":"5d7fdd8031a730726bd7d7fdc7b3b2ddaaaec13f","read_interval":[1,48],"physical_lines":48,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0157","path":"Claude/docs/v1.0.22/results/comp_R4/upgraded/SIC_CASES.md","git_blob":"4e33b805c1fc0e368fd1d8f3c53a021b595f41f5","read_interval":[1,33],"physical_lines":33,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0158","path":"Claude/docs/v1.0.22/results/comp_R4/upgraded/SIOX_CASES.md","git_blob":"439956249129fcee7757ec97c278aed02c63f96b","read_interval":[1,37],"physical_lines":37,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0159","path":"Claude/docs/v1.0.22/results/comp_R4/upgraded/SI_ENTROPY_UP.md","git_blob":"ed206f2b3938c04e8dcc3d519c78c72eddeb42ed","read_interval":[1,38],"physical_lines":38,"read_state":"READ_FULL_SEMANTIC"},
      {"source_id":"P063-SRC-0183","path":"Claude/docs/v1.0.22/results/comp_R6/R6_REPORT.md","git_blob":"0ac20304a19b0f90b62ccde5893b1958fe4e3aaf","read_interval":[1,235],"physical_lines":235,"read_state":"READ_FULL_SEMANTIC"}
    ],
    "additional_semantic_interval_count": 11,
    "additional_semantic_source_count": 10,
    "additional_semantic_unique_physical_lines": 409,
    "additional_semantic_intervals": [
      {"source_id":"P063-SRC-0034","path":"Claude/docs/v1.0.22/_sections/ch2_sec02_config.tex","git_blob":"e5aec92f5cc650c2a1d22c38cd4542f43092fdb2","read_interval":[175,179],"read_state":"READ_SEMANTIC_EXPLICIT_INTERVAL"},
      {"source_id":"P063-SRC-0035","path":"Claude/docs/v1.0.22/_sections/ch2_sec03_vibel.tex","git_blob":"ced1d9fda1c33d7a789045a96959c5bed31c852b","read_interval":[31,44],"read_state":"READ_SEMANTIC_EXPLICIT_INTERVAL"},
      {"source_id":"P063-SRC-0036","path":"Claude/docs/v1.0.22/_sections/ch2_sec04_einstein.tex","git_blob":"a80fd3226a474f4c2e235896607488966d813d53","read_interval":[22,25],"read_state":"READ_SEMANTIC_EXPLICIT_INTERVAL"},
      {"source_id":"P063-SRC-0037","path":"Claude/docs/v1.0.22/_sections/ch2_sec05_mixing.tex","git_blob":"b7d1650418c2734854378e0a1ca5cac8fc5790d3","read_interval":[94,141],"read_state":"READ_SEMANTIC_EXPLICIT_INTERVAL"},
      {"source_id":"P063-SRC-0005","path":"Claude/docs/v1.0.22/_sections/ch1_appD_si.tex","git_blob":"c658d67d6e06f0325f6165ff8f08e6eda749b6ef","read_interval":[15,74],"read_state":"READ_SEMANTIC_EXPLICIT_INTERVAL"},
      {"source_id":"P063-SRC-0190","path":"Claude/docs/v1.0.22/results/comp_RV/RV2_CH2_REPORT.md","git_blob":"34a33243580e6354cc0e2ca1520315ad1f0017ba","read_interval":[33,139],"read_state":"READ_SEMANTIC_EXPLICIT_INTERVAL"},
      {"source_id":"P063-SRC-0189","path":"Claude/docs/v1.0.22/results/comp_RV/RV1_CH1_REPORT.md","git_blob":"0e974624904e549830d8abaff7d81778da66588a","read_interval":[18,115],"read_state":"READ_SEMANTIC_EXPLICIT_INTERVAL"},
      {"source_id":"P063-SRC-0197","path":"Claude/docs/v1.0.22/results/comp_v23/SURV1_integral_transform.md","git_blob":"36c3ad6c6eee72dfbb30be6e917ca65714ad2711","read_interval":[118,176],"read_state":"READ_SEMANTIC_EXPLICIT_INTERVAL"},
      {"source_id":"P063-SRC-0062","path":"Claude/docs/v1.0.22/ch3_si_v1.0.22.tex","git_blob":"5810298ed59229f2b2410bc98da6be8e2a873b73","read_interval":[27,27],"read_state":"READ_SEMANTIC_EXPLICIT_INTERVAL"},
      {"source_id":"P063-SRC-0101","path":"Claude/docs/v1.0.22/results/comp_FR/A21_REVIEW.md","git_blob":"b1876aeb03502b53149201380571748eef788647","read_interval":[90,90],"read_state":"READ_SEMANTIC_EXPLICIT_INTERVAL"},
      {"source_id":"P063-SRC-0101","path":"Claude/docs/v1.0.22/results/comp_FR/A21_REVIEW.md","git_blob":"b1876aeb03502b53149201380571748eef788647","read_interval":[308,319],"read_state":"READ_SEMANTIC_EXPLICIT_INTERVAL"}
    ],
    "manual_evidence_anchor_count": 52,
    "manual_evidence_anchor_path_count": 30,
    "manual_evidence_coverage_state": "ALL_52_ANCHORS_COVERED_BY_SEMANTIC_ATTESTATION",
    "partial_code_review": {"source_id":"P063-SRC-0001","path":"Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py","git_blob":"c822c4e7ef9b8676e3a9bde675a718169ce79d5b","physical_lines":1500,"read_intervals":[[160,198],[855,1350]],"unique_physical_lines":535,"read_state":"PARTIAL_SEMANTIC_CODE_SCOPE"}
  },
  "literature_claims": [
    {
      "claim_id": "P063-S60-LIT-001",
      "family": "final-root citation closure",
      "source_evidence": [{"source_id":"P063-SRC-0027","path":"Claude/docs/v1.0.22/_sections/ch1v22_bib.tex","lines":[1,51]},{"source_id":"P063-SRC-0043","path":"Claude/docs/v1.0.22/_sections/ch2v22_bib.tex","lines":[1,21]},{"source_id":"P063-SRC-0046","path":"Claude/docs/v1.0.22/_sections/ch3v22_bib.tex","lines":[1,42]}],
      "current_state": "CONFIRMED_INTERNAL_STRUCTURE_ONLY",
      "axis_states": {"bibliographic_existence":"UNVERIFIED_EXTERNAL","fulltext_method":"UNVERIFIED_EXTERNAL","exact_equation":"UNVERIFIED_EXTERNAL","exact_value_unit_basis":"UNVERIFIED_EXTERNAL","sample_material_composition_protocol":"UNVERIFIED_EXTERNAL","current_model_mapping":"UNVERIFIED_EXTERNAL","external_experimental_support":"UNVERIFIED_EXTERNAL"},
      "disposition": "PRESERVE_OCCURRENCES_AND_ROOT_LOCAL_CLOSURE",
      "owner": "Phase 071",
      "acceptance": "resolver metadata plus primary full text and exact proposition/page mapping",
      "external_truth_promoted": false
    },
    {
      "claim_id": "P063-S60-LIT-002",
      "family": "Swiderska LCO entropy coefficient +0.83 mV/K",
      "source_evidence": [{"source_id":"P063-SRC-0027","path":"Claude/docs/v1.0.22/_sections/ch1v22_bib.tex","lines":[23,23]},{"source_id":"P063-SRC-0020","path":"Claude/docs/v1.0.22/_sections/ch1_sec12_lcocenter.tex","lines":[64,109]},{"source_id":"P063-SRC-0003","path":"Claude/docs/v1.0.22/_sections/ch1_appA_signcheck.tex","lines":[82,85]}],
      "current_state": "UNVERIFIED_EXTERNAL",
      "axis_states": {"bibliographic_existence":"UNVERIFIED_EXTERNAL","fulltext_method":"UNVERIFIED_EXTERNAL","exact_equation":"INTERNAL_ARITHMETIC_ONLY","exact_value_unit_basis":"REACTION_SIGN_SOC_PROTOCOL_UNVERIFIED","sample_material_composition_protocol":"UNVERIFIED_EXTERNAL","current_model_mapping":"UNVERIFIED_EXTERNAL","external_experimental_support":"UNVERIFIED_EXTERNAL"},
      "disposition": "DO_NOT_USE_AS_LOAD_BEARING_UNTIL_BASIS_FIXED",
      "owner": "Phase 071/074",
      "acceptance": "primary full-text table/figure, electrode and reaction direction, SOC, temperature and protocol",
      "external_truth_promoted": false
    },
    {
      "claim_id": "P063-S60-LIT-003",
      "family": "LCO charge-order entropy values 0.47 and 1.49 J mol^-1 K^-1",
      "source_evidence": [{"source_id":"P063-SRC-0019","path":"Claude/docs/v1.0.22/_sections/ch1_sec11_lcointro.tex","lines":[54,75]},{"source_id":"P063-SRC-0021","path":"Claude/docs/v1.0.22/_sections/ch1_sec13_lcohys.tex","lines":[169,178]},{"source_id":"P063-SRC-0144","path":"Claude/docs/v1.0.22/results/comp_R3/E_bridges/L5_CHARGEORDER_CHECK.md","lines":[1,40]}],
      "current_state": "GROUND_NOT_FOUND",
      "axis_states": {"bibliographic_existence":"GROUND_NOT_FOUND_FOR_VALUE_SOURCE","fulltext_method":"GROUND_NOT_FOUND","exact_equation":"NOT_APPLICABLE","exact_value_unit_basis":"GROUND_NOT_FOUND_ENTROPY_CATEGORY_AND_COMPOSITION","sample_material_composition_protocol":"GROUND_NOT_FOUND","current_model_mapping":"REJECT_DELTA_S_TO_OMEGA_COLLAPSE","external_experimental_support":"GROUND_NOT_FOUND"},
      "disposition": "QUARANTINE_VALUES_AND_ASSIGNMENTS",
      "owner": "Phase 071/078",
      "acceptance": "primary page/table with composition, entropy category, molar basis and transition assignment",
      "external_truth_promoted": false
    },
    {
      "claim_id": "P063-S60-LIT-004",
      "family": "chemmater2015 exact formation enthalpy values",
      "source_evidence": [{"source_id":"P063-SRC-0027","path":"Claude/docs/v1.0.22/_sections/ch1v22_bib.tex","lines":[38,38]},{"source_id":"P063-SRC-0034","path":"Claude/docs/v1.0.22/_sections/ch2_sec02_config.tex","lines":[175,179]}],
      "current_state": "UNVERIFIED_EXTERNAL_ABSTRACT_TIER",
      "axis_states": {"bibliographic_existence":"UNVERIFIED_EXTERNAL","fulltext_method":"UNVERIFIED_EXTERNAL","exact_equation":"UNVERIFIED_EXTERNAL","exact_value_unit_basis":"UNVERIFIED_EXTERNAL","sample_material_composition_protocol":"UNVERIFIED_EXTERNAL","current_model_mapping":"UNVERIFIED_EXTERNAL","external_experimental_support":"UNVERIFIED_EXTERNAL"},
      "disposition": "REJECT_ABSTRACT_TO_EXACT_QUANTITY_PROMOTION",
      "owner": "Phase 071/078",
      "acceptance": "primary full-text exact values, basis and calculation method",
      "external_truth_promoted": false
    },
    {
      "claim_id": "P063-S60-LIT-005",
      "family": "jpcc2021 vibrational/configurational decomposition and phonon method",
      "source_evidence": [{"source_id":"P063-SRC-0027","path":"Claude/docs/v1.0.22/_sections/ch1v22_bib.tex","lines":[39,39]},{"source_id":"P063-SRC-0035","path":"Claude/docs/v1.0.22/_sections/ch2_sec03_vibel.tex","lines":[31,44]},{"source_id":"P063-SRC-0036","path":"Claude/docs/v1.0.22/_sections/ch2_sec04_einstein.tex","lines":[22,25]}],
      "current_state": "UNVERIFIED_EXTERNAL_ABSTRACT_TIER",
      "axis_states": {"bibliographic_existence":"UNVERIFIED_EXTERNAL","fulltext_method":"UNVERIFIED_EXTERNAL","exact_equation":"UNVERIFIED_EXTERNAL","exact_value_unit_basis":"UNVERIFIED_EXTERNAL","sample_material_composition_protocol":"UNVERIFIED_EXTERNAL","current_model_mapping":"UNVERIFIED_EXTERNAL","external_experimental_support":"UNVERIFIED_EXTERNAL"},
      "disposition": "REJECT_ABSTRACT_TO_METHOD_PROMOTION",
      "owner": "Phase 071/076",
      "acceptance": "primary full text, equations, computational method and phase mapping",
      "external_truth_promoted": false
    },
    {
      "claim_id": "P063-S60-LIT-006",
      "family": "MSMR cite-key to multiple DOI identities",
      "source_evidence": [{"source_id":"P063-SRC-0027","path":"Claude/docs/v1.0.22/_sections/ch1v22_bib.tex","lines":[40,41]},{"source_id":"P063-SRC-0043","path":"Claude/docs/v1.0.22/_sections/ch2v22_bib.tex","lines":[19,19]}],
      "current_state": "CONFLICTING_IDENTITY_SCOPE",
      "axis_states": {"bibliographic_existence":"UNVERIFIED_EXTERNAL","fulltext_method":"UNVERIFIED_EXTERNAL","exact_equation":"UNVERIFIED_EXTERNAL","exact_value_unit_basis":"UNVERIFIED_EXTERNAL","sample_material_composition_protocol":"UNVERIFIED_EXTERNAL","current_model_mapping":"UNVERIFIED_EXTERNAL","external_experimental_support":"UNVERIFIED_EXTERNAL"},
      "disposition": "SPLIT_PRIMARY_AND_RELATED_WORK_IDENTITIES",
      "owner": "Phase 071",
      "acceptance": "one proposition routed to one exact bibliographic identity and page",
      "external_truth_promoted": false
    },
    {
      "claim_id": "P063-S60-LIT-007",
      "family": "numverif2026 internal numerical record",
      "source_evidence": [{"source_id":"P063-SRC-0027","path":"Claude/docs/v1.0.22/_sections/ch1v22_bib.tex","lines":[44,44]},{"source_id":"P063-SRC-0037","path":"Claude/docs/v1.0.22/_sections/ch2_sec05_mixing.tex","lines":[94,141]}],
      "current_state": "INTERNAL_REGRESSION_ONLY",
      "axis_states": {"bibliographic_existence":"NOT_EXTERNAL_SOURCE","fulltext_method":"NOT_EXTERNAL_SOURCE","exact_equation":"INTERNAL_REGRESSION_ONLY","exact_value_unit_basis":"INTERNAL_REGRESSION_ONLY","sample_material_composition_protocol":"NOT_EXTERNAL_SOURCE","current_model_mapping":"INTERNAL_ONLY","external_experimental_support":"FALSE"},
      "disposition": "MOVE_OUT_OF_EXTERNAL_LITERATURE_AUTHORITY_CHAIN",
      "owner": "Phase 083/086",
      "acceptance": "retain only as labeled reproducibility or implementation appendix evidence",
      "external_truth_promoted": false
    },
    {
      "claim_id": "P063-S60-LIT-008",
      "family": "orphan ch1_appD_si citation surface",
      "source_evidence": [{"source_id":"P063-SRC-0005","path":"Claude/docs/v1.0.22/_sections/ch1_appD_si.tex","lines":[15,74]}],
      "current_state": "GROUND_NOT_FOUND_FOR_RELEASE_ADOPTION",
      "axis_states": {"bibliographic_existence":"UNVERIFIED_EXTERNAL","fulltext_method":"UNVERIFIED_EXTERNAL","exact_equation":"UNVERIFIED_EXTERNAL","exact_value_unit_basis":"UNVERIFIED_EXTERNAL","sample_material_composition_protocol":"UNVERIFIED_EXTERNAL","current_model_mapping":"GROUND_NOT_FOUND","external_experimental_support":"UNVERIFIED_EXTERNAL"},
      "disposition": "PRESERVE_AS_ORPHAN_OCCURRENCES",
      "owner": "Phase 083",
      "acceptance": "explicit root/include/adoption edge or explicit rejection",
      "external_truth_promoted": false
    },
    {
      "claim_id": "P063-S60-LIT-009",
      "family": "Limthongkul and other stale/current metadata variants",
      "source_evidence": [{"source_id":"P063-SRC-0046","path":"Claude/docs/v1.0.22/_sections/ch3v22_bib.tex","lines":[7,7]},{"source_id":"P063-SRC-0046","path":"Claude/docs/v1.0.22/_sections/ch3v22_bib.tex","lines":[17,17]},{"source_id":"P063-SRC-0046","path":"Claude/docs/v1.0.22/_sections/ch3v22_bib.tex","lines":[24,24]},{"source_id":"P063-SRC-0046","path":"Claude/docs/v1.0.22/_sections/ch3v22_bib.tex","lines":[33,33]},{"source_id":"P063-SRC-0154","path":"Claude/docs/v1.0.22/results/comp_R4/SI_CASES.md","lines":[13,63]},{"source_id":"P063-SRC-0159","path":"Claude/docs/v1.0.22/results/comp_R4/upgraded/SI_ENTROPY_UP.md","lines":[13,38]}],
      "current_state": "CONFLICTING_REPOSITORY_METADATA",
      "axis_states": {"bibliographic_existence":"UNVERIFIED_EXTERNAL","fulltext_method":"UNVERIFIED_EXTERNAL","exact_equation":"NOT_APPLICABLE","exact_value_unit_basis":"UNVERIFIED_EXTERNAL","sample_material_composition_protocol":"UNVERIFIED_EXTERNAL","current_model_mapping":"UNVERIFIED_EXTERNAL","external_experimental_support":"UNVERIFIED_EXTERNAL"},
      "disposition": "PRESERVE_STALE_AND_CURRENT_VARIANTS_UNTIL_EXTERNAL_ADJUDICATION",
      "owner": "Phase 071",
      "acceptance": "resolver and publisher record with exact title/authors/year/article or pages",
      "external_truth_promoted": false
    },
    {
      "claim_id": "P063-S60-LIT-010",
      "family": "LCO g(E_F)=13 endpoint and continuous logistic gate",
      "source_evidence": [{"source_id":"P063-SRC-0023","path":"Claude/docs/v1.0.22/_sections/ch1_sec15_lcoelec.tex","lines":[160,303]},{"source_id":"P063-SRC-0190","path":"Claude/docs/v1.0.22/results/comp_RV/RV2_CH2_REPORT.md","lines":[33,139]}],
      "current_state": "ENDPOINT_UNVERIFIED_AND_CONTINUOUS_CURVE_GROUND_NOT_FOUND",
      "axis_states": {"bibliographic_existence":"UNVERIFIED_EXTERNAL","fulltext_method":"UNVERIFIED_EXTERNAL","exact_equation":"INTERNAL_MODEL_ONLY","exact_value_unit_basis":"UNVERIFIED_ENDPOINT","sample_material_composition_protocol":"UNVERIFIED_EXTERNAL","current_model_mapping":"DEMO_INTERNAL","external_experimental_support":"UNVERIFIED_EXTERNAL"},
      "disposition": "SEPARATE_ENDPOINT_OCCURRENCE_FROM_LOCAL_GATE_MODEL",
      "owner": "Phase 071/078/082",
      "acceptance": "primary endpoint units/basis and independent evidence for composition dependence",
      "external_truth_promoted": false
    },
    {
      "claim_id": "P063-S60-LIT-011",
      "family": "JCP 147(14) 144111 reference 6/7 transform method",
      "source_evidence": [{"source_id":"P063-SRC-0189","path":"Claude/docs/v1.0.22/results/comp_RV/RV1_CH1_REPORT.md","lines":[18,115]},{"source_id":"P063-SRC-0197","path":"Claude/docs/v1.0.22/results/comp_v23/SURV1_integral_transform.md","lines":[118,176]}],
      "current_state": "UNVERIFIED_EXTERNAL_PROPOSAL_ONLY",
      "axis_states": {"bibliographic_existence":"UNVERIFIED_EXTERNAL","fulltext_method":"UNVERIFIED_EXTERNAL","exact_equation":"UNVERIFIED_EXTERNAL","exact_value_unit_basis":"NOT_APPLICABLE","sample_material_composition_protocol":"UNVERIFIED_EXTERNAL","current_model_mapping":"UNVERIFIED_EXTERNAL","external_experimental_support":"UNVERIFIED_EXTERNAL"},
      "disposition": "DO_NOT_ADOPT_FREDHOLM_NEUMANN_EXTENSION",
      "owner": "Phase 071/075",
      "acceptance": "exact references, equations, assumptions and current-variable mapping",
      "external_truth_promoted": false
    },
    {
      "claim_id": "P063-S60-LIT-012",
      "family": "code/API section inside main Chapter 3 body",
      "source_evidence": [{"source_id":"P063-SRC-0062","path":"Claude/docs/v1.0.22/ch3_si_v1.0.22.tex","lines":[27,27]},{"source_id":"P063-SRC-0053","path":"Claude/docs/v1.0.22/_sections/ch3v22_sec05_code.tex","lines":[4,66]}],
      "current_state": "VIOLATES_CODE_FREE_PHYSICS_BODY_SCOPE",
      "axis_states": {"bibliographic_existence":"UNVERIFIED_EXTERNAL","fulltext_method":"UNVERIFIED_EXTERNAL","exact_equation":"NOT_ESTABLISHED_BY_API","exact_value_unit_basis":"NOT_ESTABLISHED_BY_DEFAULTS","sample_material_composition_protocol":"NOT_ESTABLISHED_BY_CODE","current_model_mapping":"INTERNAL_STATIC_ONLY","external_experimental_support":"FALSE"},
      "disposition": "RELOCATE_TO_EXPLICIT_IMPLEMENTATION_APPENDIX_OR_REMOVE",
      "owner": "Phase 083/087",
      "acceptance": "no code/API/default discussion outside the explicitly permitted implementation appendix",
      "external_truth_promoted": false
    }
  ],
  "material_scope_ledger": [
    {
      "material_id": "P063-S60-MAT-001",
      "material": "pristine LCO",
      "scope": "general half-cell transition map up to approximately 4.2–4.5 V; T4 near 4.55 V is explicitly out of current scope",
      "source_evidence": [{"source_id":"P063-SRC-0019","path":"Claude/docs/v1.0.22/_sections/ch1_sec11_lcointro.tex","lines":[38,75]}],
      "quantity_basis": "transition labels and source-reported entropy anchors; primary values unverified",
      "state": "UNVERIFIED_EXTERNAL",
      "axis_states": {"bibliographic_existence":"UNVERIFIED_EXTERNAL","fulltext_method":"UNVERIFIED_EXTERNAL","exact_equation":"UNVERIFIED_EXTERNAL","exact_value_unit_basis":"UNVERIFIED_EXTERNAL","sample_material_composition_protocol":"UNVERIFIED_EXTERNAL","current_model_mapping":"UNVERIFIED_EXTERNAL","external_experimental_support":"UNVERIFIED_EXTERNAL"},
      "forbidden_join": "doped or high-voltage sample",
      "owner": "Phase 071/078",
      "external_truth_promoted": false
    },
    {
      "material_id": "P063-S60-MAT-002",
      "material": "Al/Mg-doped high-voltage LCO",
      "scope": "dopant identity, fraction, crystallographic site, charge compensation, synthesis, voltage window, cycle and dQ/dV protocol",
      "source_evidence": [{"source_id":"P063-SRC-0021","path":"Claude/docs/v1.0.22/_sections/ch1_sec13_lcohys.tex","lines":[204,221]},{"source_id":"P063-SRC-0098","path":"Claude/docs/v1.0.22/results/comp_FR/A18_REVIEW.md","lines":[97,114]}],
      "quantity_basis": "no exact joint record",
      "state": "GROUND_NOT_FOUND",
      "axis_states": {"bibliographic_existence":"UNVERIFIED_EXTERNAL","fulltext_method":"GROUND_NOT_FOUND_FOR_EXACT_JOINT_SCOPE","exact_equation":"GROUND_NOT_FOUND","exact_value_unit_basis":"GROUND_NOT_FOUND","sample_material_composition_protocol":"GROUND_NOT_FOUND","current_model_mapping":"GROUND_NOT_FOUND","external_experimental_support":"GROUND_NOT_FOUND"},
      "forbidden_join": "pristine LCO phase map or generic dopant prose",
      "owner": "Phase 071/078",
      "external_truth_promoted": false
    },
    {
      "material_id": "P063-S60-MAT-003",
      "material": "elemental crystalline/amorphous silicon",
      "scope": "first lithiation c-Si to a-LixSi, low-potential terminal phase, later amorphous cycling and delithiation range",
      "source_evidence": [{"source_id":"P063-SRC-0050","path":"Claude/docs/v1.0.22/_sections/ch3v22_sec02_cases.tex","lines":[15,52]},{"source_id":"P063-SRC-0154","path":"Claude/docs/v1.0.22/results/comp_R4/SI_CASES.md","lines":[9,50]}],
      "quantity_basis": "theoretical, first-lithiation, first-delithiation/reversible and cycle-specific values must remain separate",
      "state": "CONFLICTING_STOICHIOMETRY_AND_UNVERIFIED_EXTERNAL",
      "axis_states": {"bibliographic_existence":"UNVERIFIED_EXTERNAL","fulltext_method":"UNVERIFIED_EXTERNAL","exact_equation":"INTERNAL_STOICHIOMETRIC_CHECK_ONLY","exact_value_unit_basis":"CONFLICTING_INTERNAL_AND_UNVERIFIED_EXTERNAL","sample_material_composition_protocol":"UNVERIFIED_EXTERNAL","current_model_mapping":"UNVERIFIED_EXTERNAL","external_experimental_support":"UNVERIFIED_EXTERNAL"},
      "forbidden_join": "Li15Si4 with 4200 mAh/g or 1000 measured reversible with theoretical capacity",
      "owner": "Phase 071/079/082",
      "external_truth_promoted": false
    },
    {
      "material_id": "P063-S60-MAT-004",
      "material": "Li15Si4 theoretical capacity",
      "scope": "3.75 electrons per Si and per-g-Si denominator",
      "source_evidence": [{"source_id":"P063-SRC-0154","path":"Claude/docs/v1.0.22/results/comp_R4/SI_CASES.md","lines":[33,36]},{"source_id":"P063-SRC-0101","path":"Claude/docs/v1.0.22/results/comp_FR/A21_REVIEW.md","lines":[90,90]}],
      "quantity_basis": "Faraday-law internal calculation gives 3578.5567 mAh/g-Si; 4198.8399 corresponds to Li4.4Si",
      "state": "CONFIRMED_INTERNAL_CONFLICT",
      "axis_states": {"bibliographic_existence":"UNVERIFIED_EXTERNAL","fulltext_method":"UNVERIFIED_EXTERNAL","exact_equation":"INTERNAL_FARADAY_LAW_ONLY","exact_value_unit_basis":"INTERNAL_ARITHMETIC_CONFIRMED_PER_G_SI","sample_material_composition_protocol":"NOT_APPLICABLE_TO_THEORETICAL_LIMIT","current_model_mapping":"INTERNAL_CONFLICT","external_experimental_support":"UNVERIFIED_EXTERNAL"},
      "forbidden_join": "Li15Si4 label with approximately 4200 mAh/g",
      "owner": "Phase 079/082",
      "external_truth_promoted": false
    },
    {
      "material_id": "P063-S60-MAT-005",
      "material": "SiO and general SiOx",
      "scope": "stoichiometry x, treatment, formation state, ICE, reversible capacity, average potential and absolute hysteresis",
      "source_evidence": [{"source_id":"P063-SRC-0158","path":"Claude/docs/v1.0.22/results/comp_R4/upgraded/SIOX_CASES.md","lines":[14,37]},{"source_id":"P063-SRC-0183","path":"Claude/docs/v1.0.22/results/comp_R6/R6_REPORT.md","lines":[180,187]}],
      "quantity_basis": "1710 mAh/g theory and 58.52/82.12 percent ICE are different axes; U=0.300 V is a demo placeholder",
      "state": "UNVERIFIED_EXTERNAL_WITH_PLACEHOLDER",
      "axis_states": {"bibliographic_existence":"UNVERIFIED_EXTERNAL","fulltext_method":"UNVERIFIED_EXTERNAL","exact_equation":"INTERNAL_STOICHIOMETRIC_CHECK_ONLY","exact_value_unit_basis":"PLACEHOLDER_OR_UNVERIFIED_EXTERNAL","sample_material_composition_protocol":"UNVERIFIED_EXTERNAL","current_model_mapping":"DEMO_INTERNAL","external_experimental_support":"UNVERIFIED_EXTERNAL"},
      "forbidden_join": "SiO to arbitrary SiOx or demo potential to verified average/hysteresis",
      "owner": "Phase 071/079/080",
      "external_truth_promoted": false
    },
    {
      "material_id": "P063-S60-MAT-006",
      "material": "Si-C composite",
      "scope": "60:15:10:15 Si:graphite:CMC:carbon-black recipe, first discharge/charge, ICE and long-cycle protocol",
      "source_evidence": [{"source_id":"P063-SRC-0157","path":"Claude/docs/v1.0.22/results/comp_R4/upgraded/SIC_CASES.md","lines":[12,33]},{"source_id":"P063-SRC-0050","path":"Claude/docs/v1.0.22/_sections/ch3v22_sec02_cases.tex","lines":[67,78]}],
      "quantity_basis": "3117/3801=82.0047 percent internally; mass denominator is not established in frozen evidence",
      "state": "BASIS_GROUND_NOT_FOUND",
      "axis_states": {"bibliographic_existence":"UNVERIFIED_EXTERNAL","fulltext_method":"UNVERIFIED_EXTERNAL","exact_equation":"INTERNAL_RATIO_ONLY","exact_value_unit_basis":"MASS_DENOMINATOR_GROUND_NOT_FOUND","sample_material_composition_protocol":"PARTIAL_REPOSITORY_RECORD_ONLY","current_model_mapping":"INVALID_PURE_HOST_JOIN","external_experimental_support":"UNVERIFIED_EXTERNAL"},
      "forbidden_join": "3117 mAh/g composite occurrence to pure elemental-Si host q_Si",
      "owner": "Phase 071/079/080",
      "external_truth_promoted": false
    },
    {
      "material_id": "P063-S60-MAT-007",
      "material": "graphite-Si blend",
      "scope": "mass fraction, active/capacity fraction, capacity kind, utilization, ICE, formation/cycle and common denominator",
      "source_evidence": [{"source_id":"P063-SRC-0051","path":"Claude/docs/v1.0.22/_sections/ch3v22_sec03_blend.tex","lines":[193,222]},{"source_id":"P063-SRC-0183","path":"Claude/docs/v1.0.22/results/comp_R6/R6_REPORT.md","lines":[18,25]}],
      "quantity_basis": "conversion arithmetic is conditional on common q/u/cycle/mass basis and correction exactly once",
      "state": "DEMO_INTERNAL_BASIS_UNVERIFIED",
      "axis_states": {"bibliographic_existence":"UNVERIFIED_EXTERNAL","fulltext_method":"UNVERIFIED_EXTERNAL","exact_equation":"INTERNAL_CONDITIONAL_ARITHMETIC_ONLY","exact_value_unit_basis":"COMMON_BASIS_UNVERIFIED","sample_material_composition_protocol":"UNVERIFIED_EXTERNAL","current_model_mapping":"DEMO_INTERNAL","external_experimental_support":"UNVERIFIED_EXTERNAL"},
      "forbidden_join": "mixed theoretical, first-charge, reversible and composite-specific capacities",
      "owner": "Phase 079/080/082",
      "external_truth_promoted": false
    },
    {
      "material_id": "P063-S60-MAT-008",
      "material": "Si mechanics GS-1",
      "scope": "sample geometry, particle size, stress sign, partial molar volume, lithiation direction, plastic/path history and cycle",
      "source_evidence": [{"source_id":"P063-SRC-0052","path":"Claude/docs/v1.0.22/_sections/ch3v22_sec04_mech.tex","lines":[15,105]},{"source_id":"P063-SRC-0101","path":"Claude/docs/v1.0.22/results/comp_FR/A21_REVIEW.md","lines":[308,319]}],
      "quantity_basis": "reversible stress shift only; predictive plastic hysteresis closure absent",
      "state": "GROUND_NOT_FOUND_FOR_PREDICTIVE_CLOSURE",
      "axis_states": {"bibliographic_existence":"UNVERIFIED_EXTERNAL","fulltext_method":"UNVERIFIED_EXTERNAL","exact_equation":"REVERSIBLE_INTERNAL_RELATION_ONLY","exact_value_unit_basis":"PROTOCOL_JOIN_GROUND_NOT_FOUND","sample_material_composition_protocol":"GROUND_NOT_FOUND_FOR_JOINT_RECORD","current_model_mapping":"PREDICTIVE_CLOSURE_GROUND_NOT_FOUND","external_experimental_support":"UNVERIFIED_EXTERNAL"},
      "forbidden_join": "100–120 mV/GPa, -1.75 GPa, 150 nm and 300 percent from different protocols into one parameter set",
      "owner": "Phase 071/079/082",
      "external_truth_promoted": false
    },
    {
      "material_id": "P063-S60-MAT-009",
      "material": "finite-rate graphite-Si blend GS-2",
      "scope": "host-current allocation, overpotential, kinetic state and finite-rate nonadditivity",
      "source_evidence": [{"source_id":"P063-SRC-0051","path":"Claude/docs/v1.0.22/_sections/ch3v22_sec03_blend.tex","lines":[229,273]}],
      "quantity_basis": "common-potential equilibrium balance does not determine finite-rate current split",
      "state": "GROUND_NOT_FOUND_FOR_PRODUCTION_FINITE_RATE",
      "axis_states": {"bibliographic_existence":"UNVERIFIED_EXTERNAL","fulltext_method":"UNVERIFIED_EXTERNAL","exact_equation":"FINITE_RATE_ALLOCATION_GROUND_NOT_FOUND","exact_value_unit_basis":"GROUND_NOT_FOUND","sample_material_composition_protocol":"GROUND_NOT_FOUND","current_model_mapping":"PRODUCTION_MAPPING_GROUND_NOT_FOUND","external_experimental_support":"GROUND_NOT_FOUND"},
      "forbidden_join": "passing full applied current to both hosts and adding them as physical allocation",
      "owner": "Phase 080/082",
      "external_truth_promoted": false
    },
    {
      "material_id": "P063-S60-MAT-010",
      "material": "Si/Si-C entropy and calorimetry",
      "scope": "material identity, SoH, cycle index, temperature, rate, loading, electrode type and protocol",
      "source_evidence": [{"source_id":"P063-SRC-0159","path":"Claude/docs/v1.0.22/results/comp_R4/upgraded/SI_ENTROPY_UP.md","lines":[13,38]},{"source_id":"P063-SRC-0050","path":"Claude/docs/v1.0.22/_sections/ch3v22_sec02_cases.tex","lines":[80,96]}],
      "quantity_basis": "-40 to -105 microV/K ranges and heat-component claims are source-reported exact quantities",
      "state": "UNVERIFIED_EXTERNAL_PROTOCOL_SPECIFIC",
      "axis_states": {"bibliographic_existence":"UNVERIFIED_EXTERNAL","fulltext_method":"UNVERIFIED_EXTERNAL","exact_equation":"UNVERIFIED_EXTERNAL","exact_value_unit_basis":"PROTOCOL_SPECIFIC_UNVERIFIED_EXTERNAL","sample_material_composition_protocol":"PROTOCOL_SPECIFIC_UNVERIFIED_EXTERNAL","current_model_mapping":"UNVERIFIED_EXTERNAL","external_experimental_support":"UNVERIFIED_EXTERNAL"},
      "forbidden_join": "aged Si-C to elemental Si or full-cell component attribution to half-cell coefficient",
      "owner": "Phase 071/076/079",
      "external_truth_promoted": false
    },
    {
      "material_id": "P063-S60-MAT-011",
      "material": "demo transition sets",
      "scope": "elemental, SiOx and SiC synthetic U/w/Q values plus LCO demonstration anchors",
      "source_evidence": [{"source_id":"P063-SRC-0050","path":"Claude/docs/v1.0.22/_sections/ch3v22_sec02_cases.tex","lines":[138,153]},{"source_id":"P063-SRC-0023","path":"Claude/docs/v1.0.22/_sections/ch1_sec15_lcoelec.tex","lines":[236,283]}],
      "quantity_basis": "tier-C/demo structure only",
      "state": "DEMO_INTERNAL",
      "axis_states": {"bibliographic_existence":"NOT_APPLICABLE_TO_DEMO","fulltext_method":"NOT_APPLICABLE_TO_DEMO","exact_equation":"DEMO_INTERNAL","exact_value_unit_basis":"DEMO_INTERNAL","sample_material_composition_protocol":"SYNTHETIC_DEMO_ONLY","current_model_mapping":"DEMO_INTERNAL","external_experimental_support":"FALSE"},
      "forbidden_join": "demo default to trusted material parameter or literature transition",
      "owner": "Phase 082/083",
      "external_truth_promoted": false
    },
    {
      "material_id": "P063-S60-MAT-012",
      "material": "mixed blend literature families",
      "scope": "commercial graphite-Si, Si15Gr75, dilatometry, 30 wt percent decoupled blend, SiOx/graphite and 150-Ah full cell",
      "source_evidence": [{"source_id":"P063-SRC-0156","path":"Claude/docs/v1.0.22/results/comp_R4/upgraded/BLEND_UP.md","lines":[20,44]}],
      "quantity_basis": "distinct materials and protocols; no single overlay source",
      "state": "UNVERIFIED_EXTERNAL_NONJOINABLE_PROTOCOLS",
      "axis_states": {"bibliographic_existence":"UNVERIFIED_EXTERNAL","fulltext_method":"UNVERIFIED_EXTERNAL","exact_equation":"NOT_APPLICABLE_TO_NONJOINABILITY","exact_value_unit_basis":"NONJOINABLE_PROTOCOLS","sample_material_composition_protocol":"NONJOINABLE_PROTOCOLS","current_model_mapping":"NO_SINGLE_COMMON_MAPPING","external_experimental_support":"UNVERIFIED_EXTERNAL"},
      "forbidden_join": "single common curve, f_Si authority or morphology from distinct studies",
      "owner": "Phase 071/080",
      "external_truth_promoted": false
    }
  ],
  "findings": [
    {"finding_id":"P063-S60-F001","priority":"P0","summary":"Li15Si4 is paired with about 4200 mAh/g although Faraday-law Li15Si4 is 3578.5567 mAh/g-Si and about 4200 corresponds to Li4.4Si.","status":"CONFIRMED_INTERNAL_CONFLICT","evidence_refs":["P063-S60-MAT-004"],"disposition":"BLOCK_CANONICAL_PROMOTION","downstream_owner":"Phase 079/082","external_truth_promoted":false},
    {"finding_id":"P063-S60-F002","priority":"P0","summary":"Si-C 3117 mAh/g is promoted to pure-host q_Si without a proven mass denominator, collapsing composite recipe, capacity kind and cycle basis.","status":"BASIS_GROUND_NOT_FOUND","evidence_refs":["P063-S60-MAT-006","P063-S60-MAT-007"],"disposition":"BLOCK_CAPACITY_FRACTION_AUTHORITY","downstream_owner":"Phase 071/079/080","external_truth_promoted":false},
    {"finding_id":"P063-S60-F003","priority":"P0","summary":"Pristine LCO evidence cannot be joined to Al/Mg-doped high-voltage LCO without dopant, site, charge compensation, voltage-window and protocol evidence.","status":"GROUND_NOT_FOUND","evidence_refs":["P063-S60-MAT-001","P063-S60-MAT-002"],"disposition":"BLOCK_SCOPE_PROMOTION","downstream_owner":"Phase 071/078","external_truth_promoted":false},
    {"finding_id":"P063-S60-F004","priority":"P0","summary":"GS-1 predictive plastic hysteresis and GS-2 production finite-rate host allocation remain unclosed and cannot be presented as implemented physics.","status":"GROUND_NOT_FOUND","evidence_refs":["P063-S60-MAT-008","P063-S60-MAT-009"],"disposition":"BLOCK_PRODUCTION_CLAIM","downstream_owner":"Phase 079/080/082","external_truth_promoted":false},
    {"finding_id":"P063-S60-F005","priority":"P0","summary":"Chapter 3 includes an API/default/code section in the ordinary physics body, violating the required code-free main-text boundary.","status":"SCOPE_VIOLATION","evidence_refs":["P063-S60-LIT-012"],"disposition":"RELOCATE_OR_REMOVE","downstream_owner":"Phase 083/087","external_truth_promoted":false},
    {"finding_id":"P063-S60-F006","priority":"P0","summary":"Repository claims of original-text or tier-A verification conflict with later audit records that exact Si mechanical and electrochemical quantities were not checked in full text.","status":"AUTHORITY_CONFLICT","evidence_refs":["P063-S60-MAT-003","P063-S60-MAT-008"],"disposition":"DOWNGRADE_TO_UNVERIFIED_EXTERNAL","downstream_owner":"Phase 071","external_truth_promoted":false},
    {"finding_id":"P063-S60-F007","priority":"P1","summary":"The +0.83 mV/K LCO coefficient has reproducible arithmetic but unresolved electrode, reaction-sign, SOC and protocol basis.","status":"UNVERIFIED_EXTERNAL","evidence_refs":["P063-S60-LIT-002"],"disposition":"QUARANTINE_LOAD_BEARING_USE","downstream_owner":"Phase 071/074","external_truth_promoted":false},
    {"finding_id":"P063-S60-F008","priority":"P1","summary":"The 0.47 and 1.49 J mol^-1 K^-1 charge-order values lack a primary source and have unresolved composition and entropy-category assignments.","status":"GROUND_NOT_FOUND","evidence_refs":["P063-S60-LIT-003"],"disposition":"QUARANTINE_VALUES","downstream_owner":"Phase 071/078","external_truth_promoted":false},
    {"finding_id":"P063-S60-F009","priority":"P1","summary":"Abstract-tier chemmater2015 metadata is used for exact formation enthalpy quantities.","status":"TIER_COLLAPSE","evidence_refs":["P063-S60-LIT-004"],"disposition":"REJECT_PROMOTION","downstream_owner":"Phase 071/078","external_truth_promoted":false},
    {"finding_id":"P063-S60-F010","priority":"P1","summary":"Abstract-tier jpcc2021 metadata is used for full-text phonon and entropy-decomposition method claims.","status":"TIER_COLLAPSE","evidence_refs":["P063-S60-LIT-005"],"disposition":"REJECT_PROMOTION","downstream_owner":"Phase 071/076","external_truth_promoted":false},
    {"finding_id":"P063-S60-F011","priority":"P1","summary":"MSMR bibliography entries bind one cite key to multiple primary and related-work DOI identities.","status":"IDENTITY_SCOPE_CONFLICT","evidence_refs":["P063-S60-LIT-006"],"disposition":"SPLIT_IDENTITIES","downstream_owner":"Phase 071","external_truth_promoted":false},
    {"finding_id":"P063-S60-F012","priority":"P1","summary":"The orphan ch1_appD_si citation surface has no frozen root or PDF adoption edge.","status":"GROUND_NOT_FOUND","evidence_refs":["P063-S60-LIT-008"],"disposition":"PRESERVE_ORPHAN_STATE","downstream_owner":"Phase 083","external_truth_promoted":false},
    {"finding_id":"P063-S60-F013","priority":"P1","summary":"numverif2026 is an internal numerical record cited in scholarly body text and must not count as external literature support.","status":"INTERNAL_ONLY","evidence_refs":["P063-S60-LIT-007"],"disposition":"REMOVE_FROM_EXTERNAL_AUTHORITY_CHAIN","downstream_owner":"Phase 083/086","external_truth_promoted":false},
    {"finding_id":"P063-S60-F014","priority":"P1","summary":"Limthongkul, Ogata, Arnot and Jiang metadata variants remain internally conflicting despite correction self-reports.","status":"CONFLICTING_REPOSITORY_METADATA","evidence_refs":["P063-S60-LIT-009"],"disposition":"PRESERVE_VARIANTS_AND_EXTERNALLY_ADJUDICATE","downstream_owner":"Phase 071","external_truth_promoted":false},
    {"finding_id":"P063-S60-F015","priority":"P1","summary":"Crossref and resolver verification claims have no frozen raw response or full-text/page evidence and cannot establish proposition authority.","status":"SELF_REPORT_ONLY","evidence_refs":["P063-S60-LIT-001","P063-S60-LIT-009"],"disposition":"DO_NOT_PROMOTE","downstream_owner":"Phase 071","external_truth_promoted":false},
    {"finding_id":"P063-S60-F016","priority":"P1","summary":"SiOx U=0.300 V is an explicit demo placeholder while absolute average potential and hysteresis remain ungrounded.","status":"PLACEHOLDER_AND_GROUND_NOT_FOUND","evidence_refs":["P063-S60-MAT-005"],"disposition":"BLOCK_MATERIAL_AUTHORITY","downstream_owner":"Phase 071/079/080","external_truth_promoted":false},
    {"finding_id":"P063-S60-F017","priority":"P1","summary":"JCP reference 6/7 transform-method mapping is proposal-only and lacks exact references, equations and assumptions.","status":"UNVERIFIED_EXTERNAL","evidence_refs":["P063-S60-LIT-011"],"disposition":"DO_NOT_ADOPT","downstream_owner":"Phase 071/075","external_truth_promoted":false},
    {"finding_id":"P063-S60-F018","priority":"P1","summary":"Si and Si-C entropy/calorimetry values are protocol-specific and cannot be transferred across elemental, composite, aged or full-cell scopes.","status":"UNVERIFIED_EXTERNAL","evidence_refs":["P063-S60-MAT-010"],"disposition":"PRESERVE_PROTOCOL_SCOPE","downstream_owner":"Phase 071/076/079","external_truth_promoted":false},
    {"finding_id":"P063-S60-F019","priority":"P1","summary":"g(E_F)=13 is an unverified endpoint while the continuous logistic gate is an internal model with conflicting free-versus-fixed parameter language.","status":"MODEL_AUTHORITY_CONFLICT","evidence_refs":["P063-S60-LIT-010"],"disposition":"SEPARATE_ENDPOINT_AND_MODEL","downstream_owner":"Phase 071/078/082","external_truth_promoted":false},
    {"finding_id":"P063-S60-F020","priority":"P2","summary":"Five manually enumerated appendix references lie outside cite-key closure.","status":"UNCITED_UNKEYED_MANUAL_REFERENCE","evidence_refs":["P063-S60-MANREF-00001","P063-S60-MANREF-00002","P063-S60-MANREF-00003","P063-S60-MANREF-00004","P063-S60-MANREF-00005"],"disposition":"KEY_OR_EXPLICITLY_LABEL","downstream_owner":"Phase 083","external_truth_promoted":false},
    {"finding_id":"P063-S60-F021","priority":"P2","summary":"Chapter 2 and Chapter 3 bibliography header counts are stale relative to 15 and 34 actual bibitems.","status":"COUNT_LABEL_DRIFT","evidence_refs":["P063-S60-LIT-001"],"disposition":"CORRECT_LABELS","downstream_owner":"Phase 083","external_truth_promoted":false},
    {"finding_id":"P063-S60-F022","priority":"P2","summary":"sethuraman_stresspot2010 page range and koebbing2024 volume/issue remain self-declared Crossref follow-ups.","status":"METADATA_GROUND_NOT_FOUND","evidence_refs":["P063-S60-LIT-001"],"disposition":"EXTERNALLY_VERIFY","downstream_owner":"Phase 071","external_truth_promoted":false},
    {"finding_id":"P063-S60-F023","priority":"P2","summary":"Rendered PDF DOI text repeats source strings but has no URI annotations and can be fragmented by line-break hyphenation.","status":"RENDERED_REPETITION_ONLY","evidence_refs":["P063-S60-LIT-001"],"disposition":"DO_NOT_TREAT_AS_METADATA_AUTHORITY","downstream_owner":"Phase 087","external_truth_promoted":false},
    {"finding_id":"P063-S60-F024","priority":"P2","summary":"Malformed lexical keys <br>bazant2013 and ... must not be normalized into adopted citation keys.","status":"MALFORMED_QUOTED_OCCURRENCES","evidence_refs":["P063-S60-LIT-001"],"disposition":"PRESERVE_RAW_CONTEXT","downstream_owner":"Phase 083","external_truth_promoted":false},
    {"finding_id":"P063-S60-F025","priority":"P2","summary":"Repeated equation, citation and DOI occurrences must remain separate from normalized families to prevent proposal-to-adoption fabrication.","status":"PROVENANCE_BOUNDARY","evidence_refs":["P063-S60-LIT-001"],"disposition":"PRESERVE_OCCURRENCE_COUNTS","downstream_owner":"Phase 071/083","external_truth_promoted":false},
    {"finding_id":"P063-S60-F026","priority":"P2","summary":"Average-potential ranges, representative values and uniquely defined averages are not interchangeable quantity types.","status":"QUANTITY_SEMANTICS","evidence_refs":["P063-S60-MAT-003","P063-S60-MAT-005","P063-S60-MAT-006"],"disposition":"KEEP_DISTINCT_FIELDS","downstream_owner":"Phase 071/079","external_truth_promoted":false}
  ]
}
```
<!-- P063_STEP60_LITERATURE_EVIDENCE_END -->

## 6. 독립 수치 판정

- `F × 0.83 mV/K = 80.0828 J mol^-1 K^-1`, `30 K × 0.83 mV/K = 24.9 mV`. 산술만 맞으며 reaction/electrode sign과 SOC/protocol은 미확정이다.
- `0.47/F = 4.871 microV/K`, `1.49/F = 15.443 microV/K`이다. 이 환산은 해당 값이 올바른 partial molar reaction entropy라는 조건부 산술이며 원천 authority를 만들지 않는다.
- `Li15Si4 = 3578.5567 mAh/g-Si`, `Li4.4Si = 4198.8399 mAh/g-Si`, `LiC6 = 371.9019 mAh/g-graphite`다. 따라서 `Li15Si4 ≈ 4200`은 내부 화학량론 모순이다.
- SiO에 2.8125 e/SiO를 가정하면 `1709.86 mAh/g-SiO`지만, 일반 SiOx/formation/reversible capacity로 자동 확장할 수 없다.
- Si–C의 `3117/3801 = 82.0047%`는 산술적으로 맞지만 g-Si/g-active composite/g-electrode denominator가 frozen evidence에서 결정되지 않았다.

## 7. Finding 요약과 Gate 판정

- P0/P1/P2: `6/13/7`.
- P0는 내부 모순과 권위·범위 위반을 숨기지 않고 downstream repair에 전달한다는 조건에서 `PASS_WITH_CONCERNS`와 양립한다. P0 claim 자체를 채택한다는 의미가 아니다.
- 이 Step이 확정하는 것은 occurrence 보존, 내부 구조 closure, 산술 재현, conflict/GNF 판정과 acceptance criteria뿐이다.
- `bibliographic_existence_externally_validated`, `fulltext_method_validated`, `exact_equation_externally_validated`, `exact_quantity_basis_externally_validated`, `material_protocol_externally_validated`, `model_mapping_externally_validated`, `external_experimental_truth_validated`, `primary_literature_truth_validated`, `canonical_equation_accepted`, `final_manuscript_ready`는 모두 false다.

## 8. Exact-seven 산출물과 예정 checkpoint

1. `Codex/work/v1022_phase063/build_phase063_step60_literature_scope.py`.
2. `Codex/work/v1022_phase063/validate_phase063_step60.py`.
3. `Codex/results/PHASE_063_V1022_LITERATURE_SCOPE_MATRIX.json`.
4. 이 result.
5. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`.
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`.
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`.

예정 subject: `audit(phase063): bound v1022 literature scope`

Result-first sentinel: `P063_STEP60_RESULT_FIRST_PRECOMMIT`

Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN` — persistence는 주장하지 않는다.

## 9. 실행 명령과 검증 결과

- Validator-first RED: artifact 부재 상태의 Python 3.12 실행은 exit 1과 전용 `E_ARTIFACT_MISSING` 진단을 반환했다.
- Builder: Python 3.12에서 `PASS_P063_STEP60_BUILD sources=201 bib=91 cites=770 doi=328 equations=339 texmath=14958 claims=8751`.
- Python 3.12/3.14 compile: builder와 validator 모두 exit 0.
- Python 3.12 content/negative/determinism: `PASS_P063_STEP60_CONTENT sources=201 claims=8751 negative=60/60 strict=5/5 determinism=2/2 nodes=882275`.
- Python 3.14 content/negative/determinism: 동일한 `60/60`, `5/5`, `2/2`, `882275` 결과.
- Artifact raw SHA-256: `77fa60e9ceeea086f8a6dde2cb3719a82357d01669e8c126e013c126e9725efd`.
- Artifact semantic SHA-256: `895b2279f87c15383b01293266ddb4f71c0a56be22207ecaa1ad214c67a16452` (top-level self-field를 제외한 builder/validator `semantic_projection`의 compact sorted JSON).
- 현재 검증은 content gate다. Staged exact-seven과 postcommit persistence는 각각 stage와 push 이후 별도로 실행해야 하며 아직 주장하지 않는다.

## 10. 다음 단계 조건

Step 61은 이 exact-seven이 staged content Gate를 통과한 뒤 atomic commit/push되고, local HEAD/upstream/live origin이 같은 full 40-character commit이며 status clean인 `PASS_P063_STEP60_PERSISTENCE`가 성립한 후에만 열린다. Phase 071은 외부 원문과 metadata의 실제 권위 검증을 소유하며, 그 전까지 이 Step의 GNF/UNVERIFIED/CONFLICTING 상태를 해제할 수 없다.
