# INDEX — v1.0.25 산출물 색인 (MOC)

> 버전 성격 = **국소 수정판**(전문 재작성 아님): @2 skew opt-in · 인과 pad · 상수 SI opt-in ·
> @3 regsol **코드 삭제** · Si 7-gallery opt-in · $w_\eff$ 문장 정정 · $C_\bg$ 창-국소 명기 · 데이터 정직화.
> **시작점 = `results/HANDOVER_v25.md`** → `results/MERGE_READINESS_v25.md` → `results/V1025_CHANGE_LEDGER.md` → 본 색인.
> 작성 = 기계적 실무 서브세션(Opus 4.8), 2026-07-26. 상태·줄 수는 `docs/v1.0.24.1/` 원본 대비 **직접 대조분**.
> 규약: **파일명 유지(DG-2)** — 파일명·`\input` 경로·`\externaldocument` xr 키에 박힌 `v1.0.24`/`v1024` 토큰은 **개명 금지**.

**루트** = `Claude/docs/v1.0.25/` (아래 경로는 특별한 표기가 없으면 이 루트 기준 상대경로)

---

## 1. 코드 (1)

| 경로 | 종류 | 요약 | 상태 | 갱신일 |
|---|---|---|---|---|
| `Anode_Fit_v1.0.24.py` | Python 모듈 | 파일명 유지 · 내부 `release 버전 = 1.0.25`. **추가**(전부 additive · 미지정 시 bit-exact): `func_dxi_eq`(L148) · `_alpha_factor`(L511) · 전이키 `alpha`(부재=1.0) · `_causal_pad`(L199, `_LAG_PAD_NLV=5.0`·`_LAG_PAD_MAXPTS=4000`·간격 ≤ L_V/20) · `R_SI`(L106)/`F_SI`(L107)/`use_si_constants()`(L111) · `SI_MSMR7_LIT`(L1357). **삭제**: `_REGSOL_XG`·`_regsol_binodal_xa`·`_regsol_dqdv` + `equilibrium()` 의 `'kernel'` 분기 → 커널 계통 = 로지스틱 단일계. **보존**: Ω 코드 전량(`func_dU_hys` L312·`func_dH_a_eff` L330). 아카이브 1734 → **1917줄(+183)** · self-test `overall OK: True` | **수정** | 2026-07-26 |

## 2. 게이트 (4)

| 경로 | 종류 | 요약 | 상태 | 갱신일 |
|---|---|---|---|---|
| `test_gates_v1025.py` | 게이트(신규) | **8종** — G-α1(alpha 부재 == 현행 `array_equal`) · G-α2(면적) · G-α3(C¹) · G-α4(α·L_V 축퇴 경고) · G-창(평가창 불변, 74.31%→2.17e-04) · G-극단 · G-SI · G-si7. **ALL PASS (8/8)**. ★계획서의 `G-금지` 는 미구현(`MERGE_READINESS_v25.md` AMBER-3). G-α1(b)·G-창 은 `../v1.0.24.1/Anode_Fit_v1.0.24.py` 원본을 참조 | **신규** | 2026-07-26 |
| `test_gates_v1024_reflect.py` | 게이트 | **G-R3 을 "@3 regsol 커널 삭제 확인"으로 재작성**(심볼 부재 3/3 + `'kernel'` 키 무시 legacy dict `array_equal` + 면적=Q=0.999881). G-R1·G-R2·G-R4 불변 → **4/4 PASS**(분모 유지) | **수정** | 2026-07-26 |
| `test_gates_v1024.py` | 게이트 | 골든 회귀 — G1 module/golden **max\|d\| = 0.0e+00 · bit-exact True** · G2·G3·n(T)·R6 계열 전건 PASS. **파일 미수정** | **무변경** | — (v1.0.24.1 승계) |
| `test_gates_v1024_selfconsistent.py` | 게이트 | 부록 E 자기일관 5종 **5/5 PASS**. C2 pad 를 ratio 경로에도 넣어야 동결 극한 정확 회수가 유지됨을 노출한 게이트. **파일 미수정** | **무변경** | — |

## 3. 마스터 `.tex` (3) + 장 밖 부록 (1)

| 경로 | 종류 | 요약 | 상태 | 갱신일 |
|---|---|---|---|---|
| `ch1_graphite_v1.0.24.tex` | 마스터(Ch1) | 표시 버전 3곳(pdftitle·lhead·`\date`) 1.0.24→**1.0.25** + 헤더 이력 주석 2줄. **60 → 62줄(+2)**. `\input` 34·xr 키 불변 | **수정** | 2026-07-26 |
| `ch2_lco_v1.0.24.tex` | 마스터(Ch2) | 동일 규약 — 표시 버전 3곳 + 주석 2줄. **32 → 34줄(+2)** | **수정** | 2026-07-26 |
| `ch3_si_v1.0.24.tex` | 마스터(Ch3) | 동일 규약 — 표시 버전 3곳 + 주석 2줄. **32 → 34줄(+2)** | **수정** | 2026-07-26 |
| `appendix_phase_separation.tex` | 독립 부록 | 라벨 30·ref 41·boxed 3 — 구조 검사 PASS. 편집 없음 | **무변경** | — |

## 4. 편집된 `_sections/*.tex` (14 — 각 파일이 무엇을 바꿨나)

> 줄 수는 `docs/v1.0.24.1/_sections/` 대비. **마스터 보고 합계 = +250**(02:06 시점),
> 본 서브세션 재계수 = **+257**(02:25 스냅샷 — 마감문서 작성 중에도 마스터 편집이 진행됐다).
> 아래 각 행의 `+n` 은 **02:25 실측**이고, 괄호의 `(보고 +m)` 은 그와 다른 경우의 마스터 보고값이다.
> 차이 근거·시각별 이력 = `MERGE_READINESS_v25.md` §4-A · `V1025_CHANGE_LEDGER.md` §4.

| 경로 (`_sections/`) | 종류 | 무엇이 바뀌었나 | 상태 | 갱신일 |
|---|---|---|---|---|
| `ch1_sec06_eqpeak.tex` | Ch1 §6 | ★**신규 식 2개** — `eq:skewpeak`(**boxed**, skew-logistic 평형 peak · α=1 에서 `eq:eqpeak` 정확 회수) · `eq:skewapex`(정점이 중심에서 $\sigma_dw_j\ln\alpha_j$ 만큼 이동 · 높이 닫힌형). 기존 `eq:eqpeak` 은 한 글자도 미수정. 감수율 유도 서식이 α=1 기준임을 명기. `+39`(보고 +38) | **수정** | 2026-07-26 |
| `ch1_sec05b_gr2L.tex` | Ch1 §5b | ★**신규 식 `eq:gr2l-fwhm`** — FWHM 닫힌형 + 점근 $(16/3)(RT/F)\lambda^{3/2}$ · 과대율 실측(0.6/1.2/3.0/27%). "$w_\eff\to0$ 델타 수렴 / 이 한 식으로 연속화" **삭제**(중심 높이 $Q/(4w_\eff)$ 는 전 λ 정확 항등임은 유지) · $w_\eff$ 폭 오독 배수 6.6/21/30 · Ω>2RT 는 Maxwell 공존평탄으로 **불연속** 전환 · 해상도 사다리에 **7-gallery(Si, opt-in)** 추가 + "사다리를 올려도 상은 늘지 않는다". `+42`(보고 +39) | **수정** | 2026-07-26 |
| `ch1_sec07_broadening.tex` | Ch1 §7 | broadening 3출처(①②③) **번호 불변**, 세 출처·폭 예산이 끝난 뒤 `sec:broadening-scope` 직전에 **"(추가 축) 평형 비대칭 α"** 단락 신설. ① 과의 교란(정점 이동 방향까지 겹침)·분리(율속 스윕만 ① 을 가름)·"다율속 없이 α 로 얻은 비대칭을 평형 비대칭의 측정으로 읽지 말라". `+18` | **수정** | 2026-07-26 |
| `ch1_sec18_inputs.tex` | Ch1 §18 | **`warnbox` 신설** — 식별 가드를 3손잡이 → **4손잡이 축퇴**(α · $L_V$ · gallery 세분 · **$w_j$($n_j$)**)로 확장. 권장 스코프(α 열면 $L_V$ 동결 · gallery 세분과 동시 자유화 지양 · α 와 $n_j$ 중 하나만) · 원리적 분리(율속/다온도/XRD) · "손잡이 값은 곡선 표현 파라미터이지 상 개수·상 성격의 측정이 아니다". `+22` | **수정** | 2026-07-26 |
| `ch1_sec05_width.tex` | Ch1 §5 | 끝에 "폭과 형상 지수의 분업" 단락 — 폭식 `eq:wbase` 불변 · 비대칭은 진행률 좌표 재모수화에서 옴 · **α–$n_j$ 축퇴**. `+8` | **수정** | 2026-07-26 |
| `ch1_sec09_tail.tex` | Ch1 §9 | `eq:lag` 규격화 검산 직후 **각주** — "점별"은 *출력*이 점별이라는 뜻이고 하한은 $-\infty$ 인 이력 적분이므로 격자 시작점 이전 과거가 누락 → 진행방향 과거로 $5L_V$ pad(간격 ≤ $L_V/20$·상한 4000점) 후 원 격자만 절단. 게이트 실측 **74.3% → 0.02%** · pad 잔여 $e^{-5}\approx0.7\%$. `+8` | **수정** | 2026-07-26 |
| `ch1_sec10_sum.tex` | Ch1 §10 | `eq:sum` 직후 $C_\bg$ = **피팅 창-국소 상수 근사** 명기(실측 0.3–0.9 V 단조 감쇠 = 창 평균의 ~230%·4셀·2프로토콜 → 잡음 아님) · 광폭 종 이득은 **조건부**(단독 악화·skew α 동반 시 개선) · 세 조건 · 배경 출처 분해는 범위 밖. + $w=RT/F=25.693$ mV 가 **CODATA-2018**이고 구현 기본은 25.6912 mV(SI 는 opt-in)라는 각주. `+17` | **수정** | 2026-07-26 |
| `ch1_appB_codemap.tex` | Ch1 부록 B | `tab:symcode` 3행 추가($\alpha_j$↔`alpha`/`_alpha_factor` · $\xi^{(\alpha)}_{\eq,j}$↔`func_dxi_eq(...)[1]` · $R,F$↔`R_SI`/`F_SI`/`use_si_constants()`) · `tab:inputs` `alpha` 행(기본 부재=1.0·tier C·G-α4) · `tab:nodecode` N6 을 `peak_shape = dxi_eq` 로 갱신·N8 에 `_causal_pad` 사양 · 도입부 "v1.0.25 갱신 요지"(추가 4항 vs **삭제 1항** + 파일명 유지 규약). ★`longtable` 안 `\footnote` 는 취약하므로 각주 대신 셀 텍스트로 흡수. `+29` | **수정** | 2026-07-26 |
| `ch1_appE_selfconsistent.tex` | Ch1 부록 E | ratio 경로도 **같은** pad 를 쓴다는 것 + **한쪽만 pad 하면 동결극한 정확 회수가 깨진다**는 실제 경험(자기일관 게이트 실패 → 양 경로 적용으로 $\lVert r_1-r_0\rVert=0$ 복구) 기록. `+5` | **수정** | 2026-07-26 |
| `ch2_sec05_mixing.tex` | Ch2 Part T | warnbox 의 "쓰지 않는다(재도입 금지)" 를 **삭제하지 않고** 대상을 "\emph{두-상 봉우리의 폭}" 으로 좁힘 + "조준 좁힘(v1.0.25)" 단락(단상 중심 높이 지표 **허용** / 폭 읽기 여전히 **금지** / 두-상까지의 연속 보간 **금지**). `[C-2]` 자산 행에 조준 변경 병기. `+10` | **수정** | 2026-07-26 |
| `ch2_sec08_synthesis.tex` | Ch2 §8 | worked example 의 $U_\oc(\bar x{=}0.25)$ 를 "74.4 mV(raw 74.35 mV)" 로 병기 + 각주(레거시 raw 74.3511 / SI 74.3497 = −1.4 µV·2×10⁻⁵ 상대차인데 74.35 반올림 절벽에 걸려 `.1f` 표시가 74.4→74.3 으로 뒤집힘. 나머지 회귀 기준 −0.204/−0.134/−0.070 mV/K·+60.8 mV 는 두 상수계에서 표시 자리까지 동일 = G-SI). `+7` | **수정** | 2026-07-26 |
| `ch2_appB_codemap.tex` | Ch2 부록 B | B.2 회귀 기준표 $U_\oc$ 행에 "정합 판정은 **raw 값**으로" 명기. `+2` | **수정** | 2026-07-26 |
| `ch3v22_sec02b_sifr.tex` | Ch3 §3.2b | ★4건: ① 비대칭 = "오직 envelope" → "envelope **또는** skew 지수 $\alpha_j$(상호 대안·동시 자유화 시 축퇴)" 로 **두 곳 완화** ② 절 도입부 **지위 `warnbox` 신설** — "해석적 기록 · 미채택·**코드 미구현**"(이득 역전 +0.97 → −0.53 %p · 커널 계통 = 로지스틱 단일계 · **Ω 지위는 불변** · 재도입 시 새 게이트 필요), (v) 에 "재구현 시의 명세로 읽되 현행 코드 거동으로 읽지 말 것", `keybox` 의 "Ω=0 로지스틱 폴백(bit-exact)" → "로지스틱 회수"(코드 계약 표현 제거) ③ 지시서 밖 결함 정정 — (c) 가 $w_\eff$ 를 **폭으로** 읽던 것을 정량 주의로 교정 ④ ★**본 버전 유일한 문장 삭제** — "커널 분기가 … 로지스틱 폴백으로 bit-exact 회수" (코드 삭제로 거짓이 됨). `eq:sifr-kernel`·`eq:sifr-blend` **식·라벨·boxed 전부 보존**. `+39`(보고 +36) | **수정** | 2026-07-26 |
| `ch3v22_sec02_cases.tex` | Ch3 §3.2 | 원소 Si 절에 **프로토콜 의존 feature** 단락 신설(0.433/0.456 V 는 `p-ocvhold` 전용) + 7-gallery opt-in 병존. 기본 케이스 셋 무변경. `+11` | **수정** | 2026-07-26 |
| `_sections/` **그 외 42종** | 절 원본 | **무변경**(전체 56 .tex 중 14 편집 · 42 미편집). 미편집분에는 `common_preamble_v1024.tex`·`ch1_sec00_intro.tex`·`ch1_sec08_lag.tex`·`ch1v22_bib.tex`·`ch2v22_bib.tex`·`ch3v22_bib.tex` 등이 포함된다 — 개별 열거하지 않고 집계만 둔다 | **무변경** | — |

## 5. `results/` — v1.0.25 신규 문서 (4 + 3)

| 경로 (`results/`) | 종류 | 요약 | 상태 | 갱신일 |
|---|---|---|---|---|
| `HANDOVER_v25.md` | 인계(★시작점) | 4부 구성 — ① 사용자 지시 11건 시간순 + 실제 한 일 + **모델 배분 이력 표** + 핵심 결과(정직) ② 미완료 N1~N13 ③ 다음 세션 주의 11항 ④ Chain 헤더. 파일명은 v1.0.24 선례(`HANDOVER_v24.md`) 승계 | **신규** | 2026-07-26 |
| `MERGE_READINESS_v25.md` | 머지 판정 | GREEN 14항 / **AMBER 3항**(빌드 미수행·정적 검사 시점 불일치·G-금지 미구현) / RED 0. **미해결 통합 표 X1~X14**(addendum M1~M6 + T13/T14 U1~U11 + 마스터 1건 중복 제거) · **최종 판정 = 조건부 YES "빌드 확인 후 머지"** · 머지 차단 = **1건**(X1) | **신규** | 2026-07-26 |
| `V1025_CHANGE_LEDGER.md` | 변경 원장 | C1~C9·G0 을 실집행으로 확정(코드 지점·문건 지점·게이트·판정) · ★**계획 이탈 3건 별도 표**(C3 opt-in · C6 완전 삭제 · 신규 라벨 1→3) · 부수 이탈 5건 · 게이트 원장 · 계수 대조(+250 vs +254) | **신규** | 2026-07-26 |
| `INDEX_v25.md` | 색인(본 문서) | v1.0.25 산출물 MOC | **신규** | 2026-07-26 |
| `V1025_DOC_EDIT_REPORT.md` | 집행 보고(마스터) | T1~T12 항목별 판정 · **마스터 반결 3건** · 미해결 물리 판단 1건(두-상 4 vs 2) · 검증 원문 출력(STRUCTURE/STRICT/doc↔code 30/30/게이트) · §5 한계(빌드 미수행) | **신규** | 2026-07-26 |
| `V1025_T13_T14_REPORT.md` | 집행 보고(서브) | T13(데이터 addendum)·T14(버전 문자열·ARCHIVE_NOTE) 결과 · `1.0.24` 잔존 12곳 전건 "남겨야 함" 판정 · 가정 G1~G8 · 미해결 U1~U11 · ★줄 수 정정(1957 은 아카이브 값이 아니다) | **신규** | 2026-07-26 |
| `V1025_DATA_ADDENDUM.md` | 데이터 정정(addendum) | comp_v24 **원본 무수정** 전제의 supersede 문서 — **A1**(프로토콜 혼용: `gr.csv`=gr_A=`p-ocv` / `si.csv`=si_Dhold=`p-ocvhold`) · **A2**(`p-ocvhold` 권고 0.9770→0.9945) · **A3**(독립셀 재현성) · **A4**(@3 근거 철회 + 코드 삭제 · Ω 존치) · **A5**($C_\bg$ 비상수) · **A6**(@1~@5 조합 실측표) · **A7**(gallery ≠ 상) + 미해결 M1~M6. 291줄 | **신규** | 2026-07-26 |

## 6. `results/` — 지시서·승계 문서

| 경로 (`results/`) | 종류 | 요약 | 상태 | 갱신일 |
|---|---|---|---|---|
| `V1025_DOC_CASCADE_TODO.md` | 지시서(Fable 산출) | 문건 P2·P3 의 **T1~T14** 편집 체크리스트("원문 → 수정문" 초안 포함) + "코드 측 이미 완결" 참고표. ★줄바꿈 **LF**(다른 md 는 CRLF — `MERGE_READINESS_v25.md` X11) | **신규** | 2026-07-26 |
| `HANDOVER_v24.md` | 인계(승계) | v1.0.24 인계문서 + FB0~FB7 리비전 절. **본 버전 Chain 의 직전 항** | **무변경** | — |
| `MERGE_READINESS_v24.md` | 머지 판정(승계) | v1.0.24 10항 게이트(10/10) + FB Addendum. **v1.0.25 는 이 문서를 덮어쓰지 않는다** | **무변경** | — |
| `INDEX_v24.md` | 색인(승계) | v1.0.24 산출물 색인 | **무변경** | — |
| `V1024_REFLECT_EXECUTION_LEDGER.md` | 실행 원장(승계) | 12-col R0~R5. `V1025_CHANGE_LEDGER.md` 의 열 구성 참조 원본 | **무변경** | — |
| `REFLECT_SEED_TABLE.md` | 사양 원천(승계) | @3/@5/토글/#1/#7 확정물리·값·서지. ★§1 "@3 개선효과"·"코드 지점" 행과 §2 "6+ = curve-fitting" 행은 addendum **A4·A7 이 supersede** | **무변경** | — |
| `PHASE_R0/R1/R2/R3_RESULT.md` | 단계 Result(승계) | v1.0.24 반영 스트림 단계별 결과 | **무변경** | — |
| `tools_check_structure.py` | 검사 도구 | 라벨·ref·cite·env 정적 검사(`check` 서브커맨드). v1.0.25 판정의 G7 근거. ★JSON 스냅샷 모드는 과거 마스터 `.tex` 덮어쓰기 사고를 낸 적이 있으므로 `check` 로만 쓸 것 | **무변경** | — |
| `snapshot_v1024_R0.json` · `reflect_curves.png` · `v1024_reflect_curves.py` · `final_sample_core.png` · `final_sample_reflect.png` · `v1024_final_sample.py` | 산출물(승계) | v1.0.24 곡선·스냅샷·샘플 스크립트 | **무변경** | — |
| `comp_R1/` (W1~W9 + `AUTHOR_BRIEF.md` + `CHERRYPICK_R1.md`) | 경쟁 저작(승계) | v1.0.24 R1 9창 경쟁 저작·체리픽 기록 | **무변경** | — |

## 7. 폴더 지위·가이드 문서

| 경로 | 종류 | 요약 | 상태 | 갱신일 |
|---|---|---|---|---|
| `ARCHIVE_NOTE.md` | 폴더 지위 | 기존 40줄 **무삭제** + v1.0.25 절 **S1~S6 추기**(+69 → **109줄**): S1 스테일 판정 표(무차별 무효화 금지 — "두 아카이브 폴더 IDENTICAL"·"파일명 v1.0.24 유지" 는 **유효 유지**) · S2 코드 변경 · S3 문건 = 표시 버전만(DG-2) · S4 원본 아카이브 무변경(LF-sha256 `f230f59bb10bcc49`) · S5 게이트·빌드 상태 3구분(마스터 실행 인용 / 서브 직접 확인 / **빌드 미수행**) · S6 데이터 정정 연결. ★표제는 여전히 "v1.0.24.1 … 동결 아카이브"(`MERGE_READINESS_v25.md` X5) | **수정** | 2026-07-26 |
| `CODE_GUIDE_v24.md` | 코드 가이드 | 구조도·플로우차트·커널 분기·옵션 전수·상수·기호 사전. ★**v1.0.25 미갱신** — 서술된 `'kernel':'regsol'` 경로는 **더 이상 존재하지 않는다**(차기 갱신 대상) | **무변경** | — |
| `CODE_GUIDE_v24.html` | 코드 가이드(HTML) | 위 가이드의 self-contained 판(mermaid 내장). 동일 주의 | **무변경** | — |
| `FITTING_GUIDE.md` | 피팅 가이드 | 파라미터 tier·초기값·경계·수렴·역식별 사슬. ★`alpha`(tier C)·`use_si_constants()` 미반영(차기 갱신 대상) | **무변경** | — |

## 8. 리포 상위 참조 (루트 밖)

| 경로 | 종류 | 요약 | 상태 | 갱신일 |
|---|---|---|---|---|
| `Claude/plans/2026-07-26-v1025-surgical-skew-consistency-plan.md` | 계획서(11-section) | 확정 D-A~D-D · DG-1(b)/DG-2(a) · Summary · Current Ground Truth(실측) · Phase P0~P4(Step 1~31) · Non-goals · **변경대장 C1~C9·G0** · Implementation Interfaces · Test Plan · Assumptions · Decision Gate · Correction History | **신규** | 2026-07-26 |
| `Claude/results/comp_v24/` | v1.0.24 근거(원본) | `FIT_CHECK_v1024.md` · `DATA_REGISTRY.md` · `ABLATION_ANODE.md` · `GRAPHITE_STAGING_XRD.md` · `AUDIT_v1024_DOC_CODE.md` · `sintef_data/{gr,si,sigr}.csv`+`SOURCES.md` 등. ★**무수정**(git clean) — v1.0.25 정정은 `V1025_DATA_ADDENDUM.md` 가 **supersede**. **읽는 순서 = 원본 → addendum(충돌 시 addendum 우선)** | **무수정** | — |
| `Claude/docs/v1.0.24.1/` · `Claude/docs/v1.0.24/` | 동결 아카이브 | **무변경**(git clean · 추적 261파일 · 코드 LF-sha256 앞 16 `f230f59bb10bcc49` 두 폴더 동일). 빌드본 PDF 3종은 v1.0.24.1 에만 존재. 비교 기준으로만 사용 | **무변경** | — |

---

## 9. 재현 명령

```
# 코드 게이트 (마스터 실행분 = 전건 PASS)
cd Claude/docs/v1.0.25
python test_gates_v1024.py                 # G1 골든 bit-exact max|d|=0.0
python test_gates_v1024_reflect.py         # 4/4  (G-R3 = regsol 삭제 확인)
python test_gates_v1024_selfconsistent.py  # 5/5
python test_gates_v1025.py                 # 8/8  (G-α1~4·G-창·G-극단·G-SI·G-si7)
python Anode_Fit_v1.0.24.py                # >>> overall OK: True

# 정적 구조 검사 (빌드 대체 — 부분 대체일 뿐이다)
PYTHONIOENCODING=utf-8 python results/tools_check_structure.py check . \
  ch1_graphite_v1.0.24.tex ch2_lco_v1.0.24.tex ch3_si_v1.0.24.tex appendix_phase_separation.tex

# ★LaTeX 빌드 (이 PC 에서는 불가 — TeX 배포판 부재. 머지 전 필수 잔여 게이트)
xelatex -interaction=nonstopmode ch1_graphite_v1.0.24.tex   # 3-pass, ch1 먼저(xr)
xelatex -interaction=nonstopmode ch2_lco_v1.0.24.tex        # 3-pass
xelatex -interaction=nonstopmode ch3_si_v1.0.24.tex         # 3-pass
```

## 10. 이 색인을 읽을 때의 주의

1. **줄 수 3개를 구분할 것**: 아카이브 코드 **1734** → v1.0.25 **1917**(**+183**)이 총 변화이고,
   **1957 → 1917(−40)** 은 *v1.0.25 개발 중 regsol 삭제 그 단계*의 변화다.
2. **삭제된 것은 dQ/dV 커널뿐**이고 **Ω 파라미터·Ω 물리는 전량 유효·코드 존치**다.
3. **문건 자산은 삭제되지 않았다** — 삭제 라벨 0 · `\boxed` 38→39 순증 · 문장 삭제는 전 버전에서 **1건**뿐
   (`ch3v22_sec02b_sifr.tex`, 코드 삭제로 거짓이 된 서술).
4. ★**빌드 미수행**이 유일한 머지 차단 항목이다(`MERGE_READINESS_v25.md` X1/AMBER-1).
   "빌드 GREEN"·"페이지 수" 류 주장은 v1.0.25 문서 어디에도 쓰여 있지 않다 — 쓰지 말 것.
5. **게이트 PASS/FAIL 은 마스터 실행분 인용**이다. 두 실무 서브세션은 게이트를 재실행하지 않았다.
