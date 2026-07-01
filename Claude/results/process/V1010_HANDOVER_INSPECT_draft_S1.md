# V1010 인계 무결성 검수 — draft S1 (초점: broadening 복원 보존)

> 검수자 = S1 (Sonnet 5). 초점 = v10이 6-30 핸드오버대로 복원한 broadening 절(전이별 SS/two-phase 2개·3기작 L_V/내재RT-F/집합통계역학=apparent-U=U_j+η 중심상수·w 이중지위·forward-only·역산금지·사이즈 전면배제·v10-11 D1 apparent-U 재정초)이 v1.0.10 Ch1에 온전·정확히 인계됐는가. ★검수 의견만 — 코드/문건 수정 0. v1.0.10 동결.
> 정독: 계획서(`Claude/plans/2026-07-06-v1010-handover-integrity-inspection-plan.md`) 전문·`results/research/broadening_w_design.md`·`results/builds/ch1v10/review1/R1_broadening.md`·`v10-00_spine/review2/A1_adv_broadening.md`·`v10-00_spine/FIX_LIST_v1011.md`·`v10-00_spine/review2/{A2,A3}_adv_*.md`·`review1/{R2,R3}_*.md`·`results/builds/v8/v8-00_spine/KNOWN_DEFECTS.md`·`results/builds/ch1v10/PHASE_CH1v10_RESULT.md`·`results/process/HANDOVER_2026-06-30_radius-dqdv-distribution-and-w-eff-bug.md`·`results/research/radius/CODE_w_check.md`·`docs/v1.0.10/HANDOVER_v1.0.11.md`·`docs/v1.0.10/V1010_PROBLEM_REPORT.md`·`results/process/GRAPH_VERIFY_RESULT.md`. line-by-line 대조 = `results/builds/ch1v10/v10-11/v10-11.tex`(1739줄, SPEC 최종본) vs `docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex`(1821줄, 현행) vs `old/Ch1_v10/graphite_ica_ch1_v10.tex`(v10-11과 동일 1739줄, 별도 사본 확인). 코드 = `docs/v1.0.10/Anode_Fit_v1.0.10.py` 직접 실행(Python 3.12) 검증. 서브에이전트 위임 = radius verdict·v8→v9 인계·old v3/v4/v5 회귀 사실관계·코드 42mV/90mV 쟁점 4개 항목(조사 결과 본문에 통합).

---

## 결함/무결 항목

### [무결 — PASS] broadening 절 본체(§sec:broadening) — 3기작 완전 보존
- 위치: 현행 `docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex:1218-1391` vs SPEC `results/builds/ch1v10/v10-11/v10-11.tex:1148-1317`.
- line-by-line 대조 결과 (a)전이별 출발(dilute·4L↔3L=SS / LiC₁₂·LiC₆ 2개만 two-phase) · (b)3기작(①L_V 비대칭꼬리 ②내재RT/F ③집합통계역학=Dreyer plateau(iii-a)+apparent-U=U_j+η 앙상블(iii-b), eq:ensavg, U_j=const·분포는 η) · (c)범위경고(사이즈 전면배제·forward-only ill-posed·PSD모델 미도입) · keybox · fig:broadening 캡션까지 **word-for-word 동일**.
- v10-11 D1 재정초(FIX_LIST_v1011의 "ρ(U_j)→ρ(U_app), U_j=입자무관상수, 분포는 η" 정정)가 그대로 인계됨 — "평형 중심 $U_j$는 입자 무관 상수"(1277)·"분포하는 것은 오직 η"(1303) 문구 확인.
- 사이즈 배제(τ∝r²·반경→U_j·PSD convolution 3항목 전부 배제, 1314-1325)·dahn1995 tier-C 강등 문구(1249-1251, FIX_LIST D2 반영)·LCO scope 분리(1264-1265, FIX_LIST D3 반영) 전부 확인.
- 차이 = 확장뿐(축소 0): (1) line 1228 "표~ref{tab:staging} 4→3·3→2L 행" 브리지 추가, (2) line 1234-1236 Maxwell 공통접선(값)↔Dreyer 순차전환(경로) 화해 문장 추가, (3) line 1255-1257 "현재 코드 n_j=1 고정→실폭 RT/F≈25.7mV, 'w' 폴백은 'n' 제거해야 활성" 코드대조 문장 추가. 전부 `docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex:2-8` 헤더 changelog가 예고한 "가독성 4-다리 보강"과 정확히 일치 — **훼손 아니라 명시된 확장**.
- 근거/렌즈: G-derive(비약 0 유지)·G-follow(다리 추가로 오히려 강화). 결론 — **broadening 3기작은 온전·정확 인계, P2 교과서화의 축약·훼손 없음**.

### [무결 — PASS] w 이중지위 절(§sec:width subsection) — 완전 보존 + 시제 명확화
- 위치: 현행 1218 이전 `:716-743` vs SPEC `:702-728`.
- eq:wbase(w_j=n_jRT/F)·단상(Ω≤2RT)=검증가능 평형예측/두-상(Ω>2RT)=현상학적 자유피팅폭 구분·Ω 초기값 4건 전부>2RT="거친 초기 추정" 명시·폭 폴백 0.020/0.016/0.014/0.012V="신뢰값 아니라 초기값" 전부 word-for-word 일치.
- 유일한 차이(현행 736-737) = "이 '전부 두-상'은 초기값 상태일 뿐 최종이 아니다"·"피팅 후" 삽입 — GRAPH_VERIFY_RESULT.md의 "master 삼각검증 보강 ③ w 초기값 시제 명확화" 항목과 정확히 일치하는 **의도된 확장**, 물리 내용 변경 0.
- 근거/렌즈: G-derive·G-usable(오독 차단 목적 명시 문구 추가로 사용성 개선).

### [경미 — LOW, 기록 오류] 전자엔트로피 절 "byte-identical" 주장이 실제로는 부정확 (단 물리 내용은 완전 보존)
- 위치: 현행 `:933-1165`(§sec:lco-electronic) vs SPEC `:914-1095`. 헤더 주석 `docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex:9,32`("전자엔트로피 절 불변(검수 byte-identical 확인)"·"byte-identical(SHA 불변)")과 `results/builds/ch1v10/PHASE_CH1v10_RESULT.md:20`("byte-identical(SHA 687ba7e6)")·`results/builds/ch1v10/v10-00_spine/review2/A2_adv_weff_preserve.md:26`("184줄/18504byte 동일, SHA-256 동일, 1바이트 변경도 없음") 세 기록 모두 "byte-identical"을 명문 주장.
- **직접 SHA-256 대조 결과 불일치**: v10-11 구간(914-1097, 184줄) hash=`ed246d9d…`, v1.0.10 구간(933-1167, 235줄) hash=`2488e68f…` — **동일하지 않음**(줄 수부터 184 vs 235로 상이).
- 실제 차이 = **삽입 2건**(삭제 0): (1) line 979-992 "★직접 엔트로피 경로(교차검증)" 신규 단락(eq:Sedirect, Fermi 적분 항등식 $\int s(\zeta)d\zeta=\pi^2/3$으로 eq:Se를 정보엔트로피 경로에서 재도출해 교차검증), (2) line 1123-1130 "★세 양의 구분(서로 다른 척도)" 신규 단락(S_e 절대량·부분몰 anchor·게이트 골 깊이 3수치 구분). 두 삽입 사이·이후 본문(Sommerfeld 유도·eq:dSe 부호규약·단위다리·MIT게이트·크기검산)은 완전 word-for-word 보존.
- 판정: **물리 내용 훼손 0**(핵심 유도·박스식·부호규약·tier 등급 전부 무손상, 오히려 교차검증 추가로 논증 강화 = G-derive 관점 개선) — 그러나 "byte-identical/SHA 불변"이라는 **기록 자체가 사실과 다름**. 3개 독립 문서(헤더 주석·PHASE_RESULT·A2 리뷰)가 동일하게 잘못된 주장을 반복한 것으로 보아, P2 교과서화 단계에서 삽입 후 "물리 불변 확인"을 "byte 불변"으로 과장 기록했을 가능성.
- 근거/렌즈: 인계 무결성(5)·기록 정확성. 심각도 = LOW(내용 무손상, 라벨 오류만) — 그러나 **N9 절에서도 동일 패턴 재발**(아래) 확인되어 반복적 기록관행 이슈로 격상.

### [경미 — LOW, 기록 오류 반복] §sec:sum(N9) 절에도 "byte-identical" 미기록 삽입 1건 + 정당한 코드대조 수정 1건
- 위치: 현행 `:1655-1739`(§sec:lco-code 전후) vs SPEC `:1573-1773` 구간(N9, sec:sum).
- 삽입: line 1729-1738 "★Ch2/P4 코드 구현 예고(두 설계 항목)" 신규 단락 — (i)좌표매핑 x↔ξ_eq,1(V), (ii)round-trip 가드(config 중심값 Motohashi 0.47/1.49 J/mol·K을 신뢰값으로 승격하기 전 self-test 필요) — §sec:lco-code 직전 삽입, 물리 내용 추가이지 삭제 아님.
- **정당한 수정 1건 발견**: line 1755 `\code{LCO\_STAGING\_LIT}` (v10-11) → `\code{LCO\_MSMR\_LIT}` (v1.0.10). 코드 실측 결과 실제 딕셔너리명은 `LCO_MSMR_LIT`(`docs/v1.0.10/Anode_Fit_v1.0.10.py:623`) — v10-11의 `LCO_STAGING_LIT`는 코드와 불일치하는 오기였고, v1.0.10이 이를 코드 대조로 바로잡음. **개선이지 훼손 아님**.
- N7(sec:lag, 1320-1432/1394-1506)·N8(sec:tail, 1432-1573/1506-1647) 두 절은 완전 byte-identical(diff 0건, PowerShell Compare-Object 직접 검증). tab:staging 표(Ω 6000/8000/10000/13000 J/mol)·부호사슬 절(sec:signcheck) 모두 완전 보존.

### [무결 — PASS] KNOWN_DEFECTS 정정 인계 (D-PEAK/D-PEAK2/D-VEQ/D-DHEFF/D-UBR/D-WEFF)
- `results/builds/v8/v8-00_spine/KNOWN_DEFECTS.md` 전문 대조 결과, v1.0.10에 다음과 같이 정정된 형태로 인계됨을 확인:
  - D-PEAK/D-PEAK2(branch-switch 문턱 ν=2·진폭 불연속 정직기술): 현행 line 1580 `eq:branch`(`L_V<\nu\Delta_grid`)·1557-1587 근처에 "매끈한 극한 아니라 이산 모드 스위치"·"작은 진폭 점프" 정직 서술 확인.
  - D-VEQ(eq:Veq 다리 가시화): line 589 근처 eq:Veq 및 도입 다리 존재.
  - D-DHEFF(χ_d Ω 중간식): line 1455-1456 `eq:dHeff = ΔH_a − χ_d Ω` 박스식 확인.
  - D-UBR(γ 보간 명시): line 636 `eq:Ubranch` + 본문 γ 인자 명시.
  - D-WEFF: `use_w_eff`/`func_w_eff`/`w_eff_floor_frac` 등 식별자가 본문에 전혀 없음(grep 0건, 헤더 changelog에만 이력 언급) — defect 자체가 소멸(제거).
- 근거/렌즈: 인계 판정(2) — v8→v9→v10→v1.0.10 전 구간 정정 형태 유지.

### [정보 — 인계 대상 밖이나 중대 사실관계] "코드 회귀" 쟁점 = 진짜 회귀 아님, 단 6-30 CODE_w_check.md 측정이 부정확했던 것으로 확정
- 계획서 §4("코드 회귀?")·base 프롬프트 서술("v11_final 42mV 정상→v1.0.10 'n':1.0로 w inert→90mV 병합bell = 의도된 기본값") 검증을 위해 `docs/v1.0.10/Anode_Fit_v1.0.10.py`를 직접 로드·실행:
  - 실제 `GRAPHITE_STAGING_LIT`(코드가 출고 시 실제로 쓰는 초기값, 'n':1.0 보유) 그대로 단일 LiC₆ 전이 평형 dQ/dV 계산 → **FWHM = 80.00mV**(V1010_PROBLEM_REPORT.md의 90.57mV와 근사, grid/window 차이).
  - 'n' 키를 인위로 제거하고 'w'=0.012V 폴백을 강제 활성화(코드가 실제로는 이 상태로 절대 안 씀) → **FWHM = 42.30mV** — 이 값이 6-30 `CODE_w_check.md`가 측정한 값과 정확히 일치.
  - 4전이 합산 실제 dQ/dV → **local maxima = 1개**(완전 병합 bell).
  - `results/code/Anode_Fit_v11_final.py:538-559`의 `GRAPHITE_STAGING_LIT`도 4전이 전부 `'n':1.0` 보유 확인(v1.0.10과 동일) — 즉 **'n':1.0 우선 로직과 병합 bell은 v11_final부터 이미 있었고 v1.0.10에서 새로 생긴 게 아님**.
  - `results/process/GRAPH_VERIFY_RESULT.md:20-26`(2026-07-01, v1.0.10 확정 검수)가 이미 이 정확한 사실("radius CODE_w_check.md의 42mV는 'n' 키 없는 반사실 테스트였다")을 자체 발견·기록하고 "실제 폭은 RT/F≈25.7mV(≈84mV), 두 그래프 다 정상 종, 코드·문건 모순 0"으로 결론지음.
- 판정: 계획서/base 프롬프트의 "42mV→90mV 회귀" 이항 대비 서술 자체가 **비교 대상이 다른(반사실 vs 실측) 것을 회귀처럼 표현한 부정확한 프레이밍**이나, 결론("회귀 아님, 병합 bell이 코드의 실제 정상 기본 출력")은 GRAPH_VERIFY_RESULT.md의 실측·제 직접 재실행 둘 다로 **확정**됨. broadening 절 인계 무결성 판정 자체에는 영향 없음(코드가 원래 그랬으므로 "인계 중 훼손"이 아니라 "처음부터 그 상태").
- ★단, 이 사실은 아래 항목과 직결되므로 별도 표시.

### [★가장 중대 — 인계 무결성 관점 CRIT 아니나 프로젝트 전체 관점 최우선 경고] 별도 세션(V1010_PROBLEM_REPORT/HANDOVER_v1.0.11)이 동일 bell 현상을 "R1 CRIT 구조 결함"으로 재규정 — base 프롬프트가 지목한 바로 그 오판 사건 확인
- `docs/v1.0.10/V1010_PROBLEM_REPORT.md:11-17`·`docs/v1.0.10/HANDOVER_v1.0.11.md` 전문 정독 결과, 이 두 문건은 **9종 병렬 검수 + 10차 재검**을 거쳐 "단일전이 FWHM=90.57mV·4전이 병합 bell 1개·Ω 무관 폭 동일"이라는 동일 실측 사실을 근거로 **"[CRIT] R1 — 폭 모델 구조 결함(두-상 near-delta 생성 불가)"**이라 명명하고, v1.0.11에서 "물리 모델 변경(폭 재설계)"을 요구하는 Phase 1.1-1.3을 편성함.
- 이는 `GRAPH_VERIFY_RESULT.md`(2026-07-01, 같은 실측값을 근거로 "정상 종·면적보존·확정 오류 0"으로 결론)·`results/research/broadening_w_design.md`(사용자 결정으로 "bell = 두-상 broadening이 정하는 현상학적 자유 피팅 폭"이 의도된 물리)·본 검수의 base 프롬프트("★bell은 결함 아님, 오적발 주의")와 **정면 충돌**.
- 사실관계 확인: bell 병합의 원인은 4 staging 전이 간격(71/20/35mV)이 각 전이 폭(RT/F≈25.7mV 이상)보다 좁아서 발생하는 **기하학적 필연**이며, broadening_w_design.md §1(b)가 이미 "two-phase 폭 = 평형 예측 아니라 현상학적 자유 피팅 폭"이라 정의했으므로 Ω 무관성·병합 자체는 **설계된 거동**이지 "생성 불가" 결함이 아님. FITTING_GUIDE Ω 하한 문구가 애매해 오독 유발 가능성(R4)은 별도 저비용 실 결함으로 타당하나, R1을 "CRIT·모델 재설계 필요"로 격상한 것은 SPEC(broadening_w_design.md·FIX_LIST_v1011·6-30 핸드오버 사용자 명시 "size 전면배제, w=자유피팅파라미터") 대조 없이 그래프 개형만 보고 내린 **오판으로 판단**.
- 이 오판은 **v1.0.10 Ch1 tex 인계 자체를 훼손하지 않았음**(V1010_PROBLEM_REPORT는 진단 문서일 뿐 v1.0.10 파일을 수정하지 않았고, v1.0.11 착수는 Decision Gate 대기 중으로 확인 — `HANDOVER_v1.0.11.md:31` "Phase 1.2 Decision Gate 전 R1 물리 모델 변경 착수 금지"). 따라서 **broadening 절 인계 무결성 판정에는 영향 없음** — 그러나 **차기 세션이 이 오판 위에서 v1.0.11 물리 모델을 실제로 재설계하면 v10/v1.0.10이 애써 복원·정초한 broadening 물리(3기작·w 이중지위·apparent-U)가 v1.0.11에서 파괴될 위험**이 있어 최우선 경고로 표시.

---

## 가장 약한 1곳
**V1010_PROBLEM_REPORT.md의 R1 CRIT 판정**(위 항목) — v1.0.10 자체의 broadening 절 인계는 완전 무결하나, 그 직후 별도 세션이 SPEC(broadening_w_design.md·6-30 핸드오버·FIX_LIST_v1011의 사용자 결정)을 대조하지 않고 동일 bell 현상을 "구조 결함"으로 재규정해 v1.0.11 착수 계획(물리 모델 변경)을 세워둔 상태. 이것이 실행되면 v1.0.10까지 3세대(v8→v9→v10)에 걸쳐 어렵게 복원한 broadening 물리가 v1.0.11에서 되돌아갈 위험이 가장 크다. 사용자가 지시문에서 "이전 문제검수가 이력을 참조하지 않고 bell을 구조 결함으로 오판"이라 지적한 대상이 바로 이 문건임을 사실관계로 확인.

## 버전전환별 인계 판정
| 전환 | 판정 | 근거 |
|---|---|---|
| v3/v4/v5 → v8 | **훼손(회귀)** | ρ_G 배리어분포·두 broadening·현상학적 w 절 전부 제거(서브에이전트 확인: v8-11 grep 결과 "broaden" 문자열 그림주석 2건만 잔존) |
| v8 → v9 | **보존**(신규 결함 0) | v8 KNOWN_DEFECTS(D-PEAK 등)는 v8-11에서 이미 정정 완료, v9는 이를 verbatim 이월 + LCO 전자엔트로피(Sommerfeld·MIT게이트·x_MIT≈0.85·T1/T2/T3) 신규 추가 확인 |
| v9 → v10 | **개선(복원)** | 6-30 핸드오버 지시대로 broadening 3기작·w 이중지위·w_eff 제거를 v9 보존 위에 신규 저작, 9종 competition-cherrypick + adversarial(A1 CRIT 재정초) 거쳐 v10-11 확정 |
| v10(v10-11) → v1.0.10 | **보존+확장**(훼손 0) | broadening·w이중지위·N7/N8/tab:staging·부호사슬 word-for-word 또는 완전 byte-identical. 전자엔트로피·N9 절은 "byte-identical" 기록과 달리 실제로는 검증·설명 강화용 신규 단락 2+1건 삽입되었으나 전부 확장이며 삭제 0. LCO_STAGING_LIT→LCO_MSMR_LIT 코드대조 정정 1건은 개선 |

## 5줄 요약
- 초점: v10 broadening 복원(3기작·w이중지위·forward-only·사이즈배제·D1 apparent-U 재정초)의 v1.0.10 인계 무결성.
- 인계결함 수: 인계 자체의 실질 결함 0건. 기록 정확성 결함 2건(LOW) — "전자엔트로피 byte-identical" 및 "N9 일부 byte-identical" 주장이 실제로는 부정확(내용은 무손상, 신규 단락 삽입으로 줄 수 증가).
- 최중대: v1.0.10 자체가 아니라 **후속 검수(V1010_PROBLEM_REPORT.md R1 CRIT)가 SPEC 미대조 상태로 bell을 구조 결함 오판**해 v1.0.11 물리 재설계 계획을 세운 것 — 실행 시 broadening 복원 전체가 위협받음.
- 두 축 유지 판정: 축1(G-derive, 비약 0)·축2(G-follow, 교과서 따라오기) 모두 v1.0.10에서 유지·오히려 4개 가독성 다리 추가로 강화. P2 교과서화의 축약·훼손 없음 — 사용자 우려("내 P2 교과서화가 축약/훼손했는지")는 **근거 없음(기각)**.
- 오적발 자기표시: 본 검수는 "bell=결함"으로 오적발하지 않았음(base 지침 준수) — 대신 코드 직접 실행으로 42mV/90mV 쟁점을 실측 재현·확정했고, 그 실측이 오히려 별도 문건(V1010_PROBLEM_REPORT)의 오판을 사실관계로 재확인하는 데 사용됨.
