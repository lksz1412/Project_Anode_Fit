# Anode_Fit v1.0.14 P4.1 R4 검수자 C(Sonnet) — 경계·일관성 검수 보고

- **렌즈**: 문건 밖 구성물과의 정합(경계·일관성) — FITTING_GUIDE.md ↔ tex 최신상태, py docstring eq 라벨 ↔ tex 라벨, tab:inputs/symcode/nodecode ↔ py 원문, graph_suite/sample_test/demo 스크립트 ↔ py 함수·상수, 버전 계보, v1.0.13 동결본 오염 여부.
- **대상**: `Claude\docs\v1.0.14\` 내 `graphite_ica_ch1_v1.0.14.tex`(3235행)·`graphite_ica_ch2_v1.0.14.tex`(782행)·`appendix_phase_separation.tex`(486행)·`Anode_Fit_v1.0.14.py`(905행)·`FITTING_GUIDE.md`(99행)·`test_regression_graphite.py` + 참조용 `graph_suite_v1014.py`·`sample_test_v1014.py`·`demo_lco_heat.py`·`plot_dqdv.py`.
- **수정 여부**: 파일 수정 없음(검토·보고서 작성만).

---

## 0. 수행 내역 요약(범주별 — 빈 통과 없음)

| 범주 | 방법 | 결과 |
|---|---|---|
| ① FITTING_GUIDE↔tex 최신상태 | FITTING_GUIDE.md 전문 정독(99행) + 인용 절/식/표 전건을 ch1/ch2 tex 본문과 대조 | 1건 HIGH(§7 그래프 suite 서술이 실제 이식 완료 상태와 불일치) |
| ② py eq 라벨 ↔ tex 라벨 실재·정합 | py 전문 정독(905행) 중 `eq:*` 참조 32건 전수 추출 → `\label{eq:*}` grep 전건(ch1 87건·ch2 21건·appendix 18건) 대조 + LaTeX 컴파일 로그(`*.log`)의 "undefined reference" 부재 교차확인 | 라벨 실재 32/32 · 내용 정합 확인, LOW 1건(N2 codebox 리터럴 단순화) |
| ③ tab:inputs·tab:symcode·tab:nodecode ↔ py 원문 | 부록 B(§sec:appendix-code, ch1 3066–3198행) 세 표 전 행을 `Anode_Fit_v1.0.14.py` `__init__` 시그니처·전이 dict 접근 코드와 1:1 대조. tab:staging(4행)·tab:lco-staging(3행)도 `GRAPHITE_STAGING_LIT`·`LCO_MSMR_LIT` 리터럴과 대조 | tab:inputs/symcode/nodecode 전건 일치(기본값·식별자·코드 스니펫 변수명까지 exact match). tab:staging 4행 전 필드 exact match. tab:lco-staging은 tier-C 시연값(3.930/3.880/4.050)과 물리 anchor(≈3.90/4.05/4.17–4.20)의 괴리를 캡션이 명시 disclose — 은폐된 불일치 아님 |
| ④ graph_suite_v1014.py·sample_test_v1014.py·demo_lco_heat.py·plot_dqdv.py ↔ py | 4개 스크립트 전문 정독, import 대상 클래스/함수/상수(`GraphiteAnodeDischargeDQDV`·`LCOCathodeDQDV`·`func_dSe_molar`·`GRAPHITE_STAGING_LIT`·`LCO_MSMR_LIT`·`curve`·`dqdv`·`equilibrium`·`entropy_coefficient`·`reversible_heat`) 전건이 py에 실재하는지 대조(실행은 회귀 스크립트만, 지시대로 나머지는 정적 대조만) | 전건 실재·시그니처 정합. graph_suite_v1014.py 자체 docstring이 "이식 유래/이식(P6.1)"을 명시 — 이 사실이 ①의 HIGH 근거 |
| 회귀 실행 | `python test_regression_graphite.py verify` 1회 실행 | 13/13 배열 `np.array_equal` bit-exact PASS, `=== GRAPHITE 0-DIFF: PASS ✓ ===` |
| ⑤ 버전 계보 잔재 | `1\.0\.13\|v1\.0\.13` grep 전 tex·md 대상 | ch1 2건·ch2 1건 모두 "계보 1.0.13 승계" 식 의도된 lineage 표기, FITTING_GUIDE.md 0건. 오기 없음 |
| ⑥ v1.0.13 동결본 오염 확인 | `git status --porcelain`/`git diff --stat` (Claude/docs/v1.0.13 한정) | 변경 0건, 마지막 touch = 기존 커밋(5995d64, P6.1 마감). 이번 세션 오염 없음 |
| 부가: 컴파일 로그 교차검증 | ch1/ch2/appendix 세 `.log` 파일에서 "Reference/Citation … undefined" 패턴 grep | 3개 파일 전부 0건 — 라벨·인용 실재를 LaTeX 엔진 자체가 이미 검증(폰트·Overfull·hyperref-unicode 경고만 존재, 무해) |
| 부가: 저장소 위생 | `Claude\docs\` 루트 직속 파일 존재 확인 | v1.0.14와 동일 이름의 0-byte 파일 9개 발견(§3) |

---

## 1. HIGH — FITTING_GUIDE.md §7 "그래프 suite" 서술이 실제 이식 완료 상태를 반영하지 못함

**위치**: `FITTING_GUIDE.md` 90행.

> "기존: `plot_dqdv.py`(흑연 4패널)·`demo_lco_heat.py`(흑연/LCO dQdV+q_rev)·`sample_test_v1014.py`(2×2 종합 데모) = PASS. 신규 validation suite `graph_suite_p5.py`(★현재 v1.0.10 폴더 소재·v1.0.10 코드 import — v1.0.14 이식 전):"

**불일치**: 이 문장은 (a) 파일명을 구판 `graph_suite_p5.py`로 지칭하고 (b) "v1.0.10 폴더 소재·v1.0.14 이식 전"이라 단언한다. 그러나 검수 대상 폴더에는 이미 `graph_suite_v1014.py`(128행)가 실재하며, 그 자체 docstring 1–17행이 "[이식 유래] docs/v1.0.10/graph_suite_p5.py(P5 산출)를 v1.0.14으로 이식(P6.1) … CODE/OUT 경로: v1.0.10 → v1.0.14 … V6 라벨 현행화(x_MIT=0.85 물리 anchor 반영) … V1 LCO 방향 라벨 정정"이라고 명시한다. 즉 이식은 이미 완료됐고, v1.0.14 전용 보정(경로·라벨·렌더링 4건)까지 반영된 상태다. FITTING_GUIDE.md §7의 V1–V9 패널 설명(91–99행)은 실제로 `graph_suite_v1014.py`의 9-패널 구현과 정확히 대응하므로(V1 흑연+LCO 나란히, V2 round-trip parity, V3 q_rev, V4 완전식 vs 단순식, V5 온도의존, V6 전자항 골 0.85 vs 0.50, V7 T² 곡률, V8 LCO q_rev, V9 면적보존 — 9개 전부 코드 패널과 1:1), 내용 자체는 최신인데 **도입부 상태 서술("이식 전"·구파일명)만 갱신되지 않아** 독자가 "이 validation suite는 아직 존재하지 않는다"고 오독하게 만든다.

**정정 제안**: §7 도입 문장을 "신규 validation suite `graph_suite_v1014.py`(P6.1 이식 완료 — docs/v1.0.10/graph_suite_p5.py 유래, 경로·V1 라벨·V6 라벨 v1.0.14 현행화 반영):"로 교체. "이식 전" 문구·구 파일명 `graph_suite_p5.py`를 현재 상태(완료)로 갱신.

---

## 2. MEDIUM — `Claude\docs\` 루트에 v1.0.14 폴더와 동명의 0-byte 잔재 파일 9개(경계 외 저장소 위생)

**발견**: `Claude\docs\v1.0.14\` 안이 아니라 그 **한 단계 위** `Claude\docs\`에 다음 9개 파일이 존재 — 전부 Git 미추적(`git status` untracked)이며 전부 **0 byte**, 동일 타임스탬프(2026-07-04 07:45:02):
`Anode_Fit_v1.0.14.py`·`FITTING_GUIDE.md`·`demo_lco_heat.py`·`graph_suite_v1014.py`·`graphite_ica_ch1_v1.0.14.tex`·`graphite_ica_ch2_v1.0.14.tex`·`plot_dqdv.py`·`sample_test_v1014.py`·`test_regression_graphite.py`.

이 항목은 지시된 검수 대상 폴더(`Claude\docs\v1.0.14\`) 밖에 있어 렌즈 ⑥(v1.0.13 오염)과는 다른 사안이지만, "문건 밖 구성물과의 정합"이라는 본 렌즈의 취지(외부 아티팩트와의 경계 정합)에 정확히 해당하고 실사용 리스크가 있어 보고한다 — 동일 파일명의 빈 사본이 상위 폴더에 있으면, 향후 세션이 `Claude/docs/*.py` 같은 얕은 glob이나 경로 오타로 이 빈 파일을 import/실행할 경우 **조용히 아무 클래스도 없는 빈 모듈**을 로드하는 silent-failure 위험이 있다(현재 `test_regression_graphite.py`·`graph_suite_v1014.py` 등은 절대경로로 `v1.0.14\` 하위를 명시 지정하므로 이번 회귀 실행 자체는 이 잔재에 영향받지 않았음을 확인함 — PASS는 유효).

**정정 제안**: 파일 수정 금지 지시에 따라 본 세션에서 직접 삭제하지 않음. Master 세션에서 `git status`로 재확인 후 `Remove-Item`으로 정리(또는 `git clean -n`으로 미리보기 후 처분) 권고. 삭제 전 0 byte임을 재확인해 데이터 손실 리스크가 없음을 재검증할 것.

---

## 3. LOW — 부록 B(구현 대응표) N2 codebox 리터럴 인용이 실제 seam 경유 호출을 축약

**위치**: `graphite_ica_ch1_v1.0.14.tex` 3186–3193행(codebox "N2").

인용문: `if 'dH_rxn' in tr and 'dS_rxn' in tr: U_j = func_U_j(T_work, dH_rxn, dS_rxn)` — 그러나 실제 `Anode_Fit_v1.0.14.py` 470행은 `U_j = func_U_j(T_work, tr['dH_rxn'], self._effective_dS_rxn(tr, T_work))`이다. codebox의 `dS_rxn`은 seam 함수 `_effective_dS_rxn(tr, T_work)` 호출을 거치지 않은 원값처럼 축약 표기됐다.

**refute(가장 약한 1곳 검증)**: 이것이 실질 결함인지 검토했다 — 바로 다음 문장(3188–3190행)이 "실 호출의 ΔS 인자는 seam `_effective_dS_rxn(tr, T_work)`를 경유한다(흑연 base는 항등으로 `tr['dS_rxn']` 그대로 — LCO 전자항 plug-in 자리: §sec:lco-code)"라고 명시적으로 정정·설명한다. 즉 codebox 자체는 축약(리터럴 정확도 미달)이나, 인접 산문이 즉시 정확한 경유 경로를 밝히므로 독자가 오도될 위험은 낮다. "코드 대응표는 구현 식별자와 1:1이어야 한다"는 부록 B의 목적(3068–3070행: "구현의 주석·docstring이 본 문건의 식 번호를 참조" + "역방향 조회 … 재현 가능성(1:1 대조) 보존")에 비추면 리터럴 불일치는 형식적으로는 흠이지만, 물리·동작 오도는 없다 — LOW로 유지.

**정정 제안(선택)**: codebox 인용을 `U_j = func_U_j(T_work, tr['dH_rxn'], self._effective_dS_rxn(tr, T_work))`로 교체해 완전 리터럴화하거나, 현행 유지 시 "축약(실제는 seam 경유)"라는 주석을 codebox 자체에 1줄 추가.

---

## 4. 검토했으나 결함 아님(refute 생존 — 잘못된 의심을 스스로 반증한 경로 포함)

1. **§1.13 이동 의심**: 현재 ch1.tex TOC(§1.1–§1.12 + 부록 A·B)에 §1.13은 존재하지 않는다. tex·md 전체에 "§1.13" 문자열 자체가 0건 — 과거 절 번호가 부록 A/B로 승격 이동한 뒤 잔존 참조가 없음을 확인(부록 A/B 신설은 커밋 6975870 P2.2). 결함 없음.
2. **Ξ₁ 표기 일관성**: ch1.tex(435·449·452·460·536·539·1331행)과 ch2.tex(127·133·141행) 전부 `\Xi_1` 사용, 병기 설명("자리 1개의 …")도 동형. 결함 없음.
3. **`appendix_phase_separation.tex`의 본문 절 텍스트 참조(§1.2·§1.5, 라벨 미사용·의도된 독립컴파일 설계)**: 헤더가 "본문 참조는 라벨이 아니라 절 번호 텍스트로만 적는다(독립 컴파일 유지)"라 명시. 실제 인용된 "Part 0(§1.2)"·"§1.5"를 현재 ch1.tex TOC와 대조하면 §1.2="통계역학 기초…(P0)", §1.5="히스테리시스 분기 중심"으로 문맥과 정확히 일치. 부록 A/B 신설(P2.2)·eq1.8 재유도(P2.1) 등 후속 개정이 §1.2/§1.5 번호 자체를 건드리지 않았음도 확인. 결함 없음. 단, 이 appendix는 "지위: 독립 초안 — 본문 편입 여부는 사용자 검토 후 결정(계획 Step 7)"로 ch1/ch2 어디서도 `\ref`·`\input`되지 않는 의도된 orphan 문서임(커밋 8cfe22a "Step 7 spinodal Appendix 초안(편입 보류)"와 정합) — 결함이 아니라 설계.
4. **"파생 C"/`ssec:weff` 유령 참조 의심(자기 반증 사례)**: ch2.tex 헤더(9–11행)가 "파생 C(w_eff(Ω)=w(1-Ω/2RT)) 절 완전 제거"라 적어, 175·448·525·649·716행의 `\S\ref{ssec:weff}`(현 "파생 C — 폭 w의 이중지위" 절)가 유령 라벨일 가능성을 의심했다. 그러나 570행에 `\subsection{파생 C — …}\label{ssec:weff}`가 실재 — 헤더의 "제거"는 구 v5(w_eff(Ω) 공식) 한정이고, 현재 "파생 C"는 같은 절 번호 자리에 다른 내용(w의 단상/두-상 이중지위)으로 대체된 것. `.log` 파일 전건에서 "undefined reference" 0건이라는 사실과도 정합. 최초 grep이 `ssec:` 접두를 놓쳐 생긴 오탐 — 컴파일 로그 교차검증으로 자체 반증함.
5. **tab:inputs 전체값 vs `__init__` 시그니처**: `x/chi`(0.5)·`Rn`(0.0)·`Cbg`(0.0)·`grid_pad_lo/hi`(0.15)·`n_work_min`(2048)·`min_lag_grid_steps`(2.0)·`v_span_floor`(1e-6)·`seed_T/I/Q_cell`(298.15/0.1/1.0)·`z_cut/A_cap_RT`(4.357/4.0)·`use_dH_eff`(True) 전 10항목 코드 기본값과 정확 일치. 전이 dict 키(U|dH_rxn·dS_rxn, w|n, Q, Omega/gamma, h_eta, dH_a/dS_a, dVdq_qa, L_V, electronic/x_center, g_max_eV/x_MIT/dx_MIT) 필수·선택 구분도 코드 `.get(...)` 기본값과 전건 일치. 결함 없음.
6. **tab:nodecode N1/N5/N6/N8/N9 코드 스니펫**: `V_n = V_in - sigma_d * I_abs * self.Rn`(N1)·`peak_shape = ksi_eq*(1-ksi_eq)/w`(N6)·`lowpass(ksi_arr[::-1])[::-1]`(N8) 등이 py 원문과 변수명까지 완전 일치. 결함 없음.
7. **tab:staging(흑연 4-전이)**: U/ΔH_rxn/ΔS_rxn/Q/Ω/ΔH_a/|dV/dq| 전 28개 셀 값이 `GRAPHITE_STAGING_LIT` 리터럴과 정확 일치. 결함 없음.
8. **§0 방향 규약(FITTING_GUIDE) vs eq:lco-sigmaslot(ch1 2081–2087행)**: "탈리튬화(산화) 진행 = +1", "LCO 하프셀 — 충전 ↦ +1"이 boxed 식과 문자 그대로 일치. 결함 없음.
9. **LCO Ω_j 지위(B-3, FITTING_GUIDE 30행) vs sec:lco-hys(ch1 2286–2290행)**: "LCO_MSMR_LIT 세 dict 전부 Omega 키 미배정 → Ω=0 폴백 → 히스 분기 비활성"이 tex 서술("표~tab:lco-staging는 LCO Ω_j^cat의 수치 열을 싣지 않으며 … 미배정 시 Ω=0으로 두어 히스 분기가 비활성")과 정확히 일치. 결함 없음.
10. **버전 계보 문자열**: ch1/ch2/appendix/py/FITTING_GUIDE 전부 "1.0.14"로 일관, "1.0.13" 언급은 전부 계보 승계 표기(오기 아님).
11. **"peak" 용어 변이("피크")**: `Anode_Fit_v1.0.14.py` 179행·`demo_lco_heat.py` 41행 단 2곳에서만 "피크"(음차) 사용, 나머지는 "peak"/"봉우리"로 형식 문건과 일치. 코드 주석·print문 수준의 경미한 표기 변이로 물리·해석 오도 없음 — 정정 불요(선택적 통일 권고만).

---

## 5. 회귀·오염 확인 결과 (지시된 실행·확인 항목)

- `python test_regression_graphite.py verify` → **13/13 배열 bit-exact PASS**, `=== GRAPHITE 0-DIFF: PASS ✓ ===`(면적비 0.936은 판정 기준 아닌 참고 출력).
- `git status`/`git diff --stat` (Claude/docs/v1.0.13 한정) → **변경 0건**, 이번 세션 오염 없음. 최종 touch는 기존 커밋 5995d64(P6.1 마감).

## 6. 심각도 집계

| 심각도 | 건수 | 항목 |
|---|---|---|
| HIGH | 1 | FITTING_GUIDE.md §7 이식 상태 서술 stale |
| MEDIUM | 1 | Claude/docs/ 루트 0-byte 잔재 9건(경계 외 위생) |
| LOW | 1 | 부록 B N2 codebox 리터럴 축약(산문이 즉시 정정 — refute 후 유지) |
| 결함 아님(확인·기록) | 11 | §4 목록 |

**결론**: 이번 렌즈에서 문건-코드-스크립트 간 식별자·기본값·라벨 정합은 거의 완벽(부록 B 세 표 전건 exact match, eq 라벨 32/32 실재+로그 무결함 확인)하며, 실질 결함은 FITTING_GUIDE.md의 그래프 suite 이식상태 서술 1건(HIGH)에 집중된다. 나머지는 검수 대상 폴더 경계 밖 저장소 위생(MEDIUM, 정보 제공 목적) 또는 낮은 리스크의 서술 축약(LOW)이다.
