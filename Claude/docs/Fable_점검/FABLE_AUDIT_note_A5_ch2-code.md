# Fable 재검 — 이력 감사 노트 A5: Ch2 트랙(v3→v4→v5→v1.0.10) + 코드 트랙(v11_final→v1.0.10)

> 역할: 분석 sub(파일 수정 없음). 담당 = Ch2 챕터 이력 + 코드 이력. 모든 판단은 줄 근거(파일 경로+줄) 동반. 추정은 "추정"으로 명시.

---

## 0. 정독 대상 확인

- Ch2 tex 4종: `Claude/old/Ch2_v3/graphite_ica_ch2_v3.tex`(266행)·`Claude/old/Ch2_v4/graphite_ica_ch2_v4.tex`(760행, 헤더는 "v4-11")·`Claude/results/builds/ch2v5/v5-draft.tex`(751행)·`Claude/docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex`(751행).
- Ch2 기록: `2026-06-30-ch2-reversible-heat-entropy-survey-plan.md`(v3 계획)·`PHASE_CH2v3_RESULT.md`(v3 결과)·`2026-06-30-ch1v9-LCO-ch2v4-mixing-2track-9x9x1x1-plan.md`(v4 계획)·`ch2_v4/v4-00_spine/{AUTHOR_BRIEF,CHERRYPICK_PLAN,FIX_LIST_v411,REVIEW_RISK_PATTERNS}.md`·`review1/{R1..R4}.md`·`review2/{A1,A2}.md`·`2026-07-02-v1010-P3-ch2-heat-plan.md`(v1.0.10 편입 계획).
- 코드: `Claude/results/code/Anode_Fit_v11_final.py`(617행)·`Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py`(742행)·`Claude/results/code/Anode_Fit_v12.py`(607행, 참고용)·`Claude/results/research/radius/CODE_w_check.md`·`Claude/results/process/V1010_P4_code-revision_RESULT.md`·`Claude/results/code/v12_roundtrip_check.md`(참고용).
- review1 5차원(R1~R5) 중 R1·R2·R3 전문 정독, R4·R5 는 `CHERRYPICK_PLAN.md` 인용을 통해 결론 확인(원문 grep 교차 — 아래 §2 각주). review2 A1·A2 전문 정독, A3 는 `FIX_LIST_v411.md` 인용으로 결론 확인.

---

## 1. v3 — 백지 조사·초안 (기준점)

**이전 문제.** Ch2(가역 발열·엔트로피 계수) 마지막 작업물은 v2(2026-05-29)였고, 이후 6-07~6-09 작업은 반응속도론·히스테리시스로 재편되어 전부 Ch1(v8-11)에 흡수됐다 — 즉 이 주제는 "v2 이후 진행 이력 없음"(`2026-06-30-ch2-reversible-heat-entropy-survey-plan.md` L13). 가역 발열이라는 주제 자체가 미진했다(사용자 명시, 같은 파일 L8).

**개선 의도.** v2/rebuilt/old/roadmap_v1 을 명시적으로 미참고 처리하고(백지, 같은 파일 L3, L37), Ch1 v8-11 의 $U_j(T)=(-\Delta H_{\rxn,j}+T\Delta S_{\rxn,j})/F$ 를 토대로 사슬 `다온도 dQ/dV → U_j(T) → ∂U_j/∂T=ΔS_rxn,j/F → Q̇_rev=-IT·∂U/∂T(Bernardi)` 를 1차 문헌으로 근거화하는 조사+초안(완본 아님).

**달성 여부.** `PHASE_CH2v3_RESULT.md` 에 따르면 부호 규약을 Bernardi·Newman·MSMR Part I 삼각 확인(L24), Ch1 `Δ​S_{rxn,j}=+29→0→-5→-16` J/mol/K 이 Allart 2018 문헌값과 정량 일치(양 끝 정확, L25) — `graphite_ica_ch2_v3.tex` 표 1(L148-169)에 반영. xelatex 0-error·cite 11/11 검수 PASS(L27-30). **완주 확인.** 단, 산출물 자체는 저자 서문에서도 "5p" 스켈레톤(`CHERRYPICK_PLAN.md`에서 이후 v4 base 로 재확인, "base_ch2_v3.tex(265줄·6절, ... 얇은 출발 skeleton)" — `AUTHOR_BRIEF.md` L3)으로 규정 — 스스로 "Ch1+ΔS 한 절 수준"이라 인정(`AUTHOR_BRIEF.md` L3, L6).

**우수 구조 보존·장단점.**
- 장점: 문헌 삼각검증 방식(seed 문헌 명시적 tier 구분·확정/미확인 분리)이 이후 v4/v5/v1.0.10 전체에 그대로 유지되는 인용 마스터의 출발점이 됐다(참고문헌 11종이 v4~v1.0.10 까지 거의 변경 없이 이어짐 — `graphite_ica_ch2_v3.tex` L251-263 vs `graphite_ica_ch2_v1.0.10.tex` L734-747, bernardi1985·newman·reynier2003·allart2018·occupation2019·chemmater2015·jpcc2021·msmr_partI/II·standardised2024·hysteresis2018 11종 중 10종 그대로 승계, huggins2009·bazant2013 는 v4 에서 추가).
- 단점: 표 1(L148-169)의 "중간 두 전이는 범위 정합(점-대-점 아님)"이라는 각주 처리 방식이 정직하지만, staging 전이 4개와 Allart region 세분 간의 $x$-경계 불일치를 "해상도 차이"로만 뭉뚱그려 — 이 미봉합은 v4/v5/v1.0.10 까지 표 그대로 상속됨(동일 각주 문구가 4개 버전 모두에 존재, 예: `graphite_ica_ch2_v1.0.10.tex` L338-341).
- 문제점: "다온도 dQ/dV 직접 추출"(사슬 가운데 고리)은 "MSMR template 위 신규 각"으로만 표시하고 실증 없음(`PHASE_CH2v3_RESULT.md` Open Issues #4) — 이 갭은 v4/v5/v1.0.10 까지 미해결로 이월(§4 참조).

---

## 2. v3 → v4 — 통계열역학 챕터화 (9종 competition-cherrypick)

**이전 문제.** v3 는 "Ch1 결과값 + ΔS 한 절" 수준 — 분포(distribution)를 결론으로만 인용하고, 겹침 봉우리의 비선형 $\partial U_\oc/\partial T(x)$ 모양이나 configurational/vibrational/electronic 분해가 없었다(`AUTHOR_BRIEF.md` L3: "v3 의 'Ch1+ΔS 한 절' 수준 탈피"가 목표로 명문화 — 즉 이전 문제를 v4 계획서 자신이 특정).

**개선 의도.** `2026-06-30-ch1v9-LCO-ch2v4-mixing-2track-9x9x1x1-plan.md`(L6): 격자기체 분배함수 → 점유 분포 → $S_\mathrm{config}=-R\sum p\ln p$(Ch1 logistic 의 통계역학적 기원) → vibrational(Bose-Einstein)·electronic(Fermi-Dirac, LCO MIT) 분해 → 겹침/이중계산/$w_\eff(\Omega)$/히스테리시스 닫힌식(파생 A·B·C·D) → 극한 검산(파생 I) → 가역 발열, 을 "고유 챕터"로 세운다. 방법 = 9종 병렬 competition-cherrypick(Sonnet 3·Opus 3·Codex 3, 무통신) → 검토1(R1-R5, 5차원) → 체리픽 → 검토2(A1-A3, adversarial) → v4-11.

**달성 여부(분포 전개 자체).** 달성. v4-11(`graphite_ica_ch2_v4.tex`)은 §2.1 분배함수 $Z_1=1+e^{-\beta(\varepsilon_0-\mu)}$(L116)→점유 $\langle n\rangle$(L122-124, Ch1 logistic 기원과 등가 확인 L154-158)→§2.2 configurational $S_\config=-R[\theta\ln\theta+(1-\theta)\ln(1-\theta)]$(L206-208)→부분몰 발산 항 $-R\ln[\theta/(1-\theta)]$(L219-221)→§2.3 vibrational Bose-Einstein(L358)·electronic Fermi-Dirac/Sommerfeld(L383-391)까지 무비약 유도. review1 R1(전 9종 head→tail 정독)에서 이 config 사슬만은 "전 빌드 완전 전개"로 확인(`R1_distribution_signs.md` L76). review2 A1은 vib/elec 두 항만 "라벨 후 결과 직착"(HIGH, 공식은 정확)으로 지적(`A1_adv_physics.md` L21, L41) — v4-11 FIX_LIST 에서 "Ch1 v9 §전자엔트로피 참조로 해소 가능"으로 처리(`FIX_LIST_v411.md` L7, L22).

**달성 여부(파생 C w_eff) — ★핵심 결함, v5 에서 전면 취소.**
9종 빌드 단계에서 마스터 자신의 설계 문서(`40_mixing_term_design.md`)가 $w_\eff=w/(1-\Omega/2RT)$(역수형)로 **틀렸고 9작가 전원이 그대로 상속**했다 — 마스터 본인이 이를 `REVIEW_RISK_PATTERNS.md` ★위험7 에서 인정: "내 원 설계 doc 이 ... 틀렸고 9 작가 전부 상속"(L34-35). 체리픽 단계에서 이를 $w_\eff=w(1-\Omega/2RT)$(정답형, "V-폭 좁아짐·$\Omega\to2RT^-$ 서 $w_\eff\to0$·dQ/dV peak 발산")로 정정하고, 이 정정형이 review1 R2(`R2_mixing_weff_B.md` L17: "유일 전체 정합")·review2 A1(`A1_adv_physics.md` L28-32: "반증 실패(견고)")·A2(`A2_adv_mixing.md` L33: "정확 → $w_\eff=w(1-\Omega/2RT)$ 정확")를 **모두 통과**해 v4-11 확정본에 박혔다(`graphite_ica_ch2_v4.tex` L531-556, eq:weff L544-546).

그런데 이 "정정형"조차 물리적으로 거꾸로였다. v5 changelog(`v5-draft.tex` L8-9): "파생 C($w_\eff(\Omega)=w(1-\Omega/2RT)$ '상호작용이 종을 좁힘') 절 완전 제거 — two-phase 실측은 *종*이지 델타가 아니라 narrowing 그림이 틀림." 즉 강한 1차상전이(흑연 staging, $\Omega>2RT$)의 실측 dQ/dV 봉우리는 좁아지는 델타가 아니라 넓은 종 모양이며, $\Omega$ 는 상분리 개시 임계를 정할 뿐 실측 봉우리 폭을 정하지 않는다 — 폭은 (i) 유한 율속 비대칭 꼬리 (ii) 내재 단상 폭 $RT/F$ (iii) 앙상블 heterogeneity 로 정해지는 **현상학적 자유 피팅 파라미터**다(`v5-draft.tex` L548-556).

**이 결함이 두 라운드 적대 검수를 통과한 이유(감사 핵심 발견).** review1(R1-R5, 5명 독립)과 review2(A1-A3, adversarial 재검수, 독립 수치 재현 스크립트 `check_a2.py`/`check_overlap.py` 포함, `A2_adv_mixing.md` L5-15)는 전부 "$w_\eff=w(1-\Omega/2RT)$" 를 **설계 문서(ground truth)와의 내적 정합성**으로만 검증했다 — 즉 "이 식이 Bragg-Williams 자유에너지의 중심 기울기 조건과 대수적으로 맞는가"만 확인했고, 이 물리적 그림(narrowing) 자체가 실측 이상거동(broad two-phase 종)과 맞는지는 어느 검수 라운드도 묻지 않았다. A2 의 "독립 수치 재현"조차 $dV_\eq/d\theta|_{1/2}=(4RT-2\Omega)/F$ 라는 대수식의 재도출이었지(`A2_adv_mixing.md` L33: "이상 logistic 중심 기울기 ... 정합 → $w_\eff=w(1-\Omega/2RT)$ 정확"), 실측/시뮬레이션 곡선 모양과의 대조는 아니었다. 이 물리 오류는 이후(v1.0.10 P1 코드감사 단계) **실제 코드를 돌려 그래프를 뽑아보는 별개의 실행 기반 검증**(`CODE_w_check.md`)에서야 발견됐다 — 상세는 §3.

**우수 구조 보존(파생 B 이중계산).** v3 에는 없던 이중계산 경고가 v4 에서 신설되고("파생 B", `graphite_ica_ch2_v4.tex` L286-302: $\Delta S^0_j$=중심 표준값·config=봉우리 내부 분포항·둘은 별개 항이라 이중가산 금지) 이후 v5·v1.0.10 까지 문구 변경 없이 보존됨(§4 확인). review1 R1(L76)·R2(L23: "이중계산 B '분리 논리'는 9종 모두 substance PASS")가 이 부분은 견고하다고 재확인.

**우수 구조 보존(exo/endo 부호).** v4-04 의 자체(지시 위반) 검토 sub 가 발견한 exo/endo 역매핑(희박 +ΔS 를 방전 발열로 오기, 정답=흡열)이 `REVIEW_RISK_PATTERNS.md` ★위험3 으로 등재되어 9종 전수 재확인 — 9종 중 5종(01·03·07·08·09) PASS·4종(02·04·05·06, 전부 Opus 계열 다수) CRITICAL FAIL(`R3_qrev_depth.md` L8-23). 체리픽 base 로 채택된 v4-05 도 이 결함을 갖고 있어("v4-05 는 R2 mixing/w_eff 최강이나 R3 exo/endo FAIL" — `CHERRYPICK_PLAN.md` L20, L33) v4-10 조립 시 "exo/endo 라벨 반전" 국소 fix 로 교정됨(같은 파일 L37, L43).

**장단점 종합.**
- 장점: 9종 경쟁 + 5차원 검토1 + 3차원 adversarial 검토2 의 다층 구조가 실제로 다수의 CRITICAL 결함(config 부호 역수 2종·μ(V) 부호 반대 1종·LaTeX `+` 탈락 2종·exo/endo 역매핑 4종)을 잡아냈다 — 이 정도 규모의 결함 매트릭스가 사전에 존재했다는 것 자체가 단일 저자 초안이었다면 훨씬 위험했을 것을 시사.
- 단점: 검수 라운드 전부가 "설계 문서 대비 정합"을 최종 기준(ground truth)으로 삼았고, 그 설계 문서 자체의 물리적 타당성(narrowing vs broadening)을 재검증하는 렌즈가 없었다 — 이는 다수 에이전트 교차검증도 상위 스펙이 틀리면 하나의 오답으로 수렴시킬 수 있음을 보여주는 사례.
- 문제점: `FIX_LIST_v411.md`(v4-11 확정 직전 fix list)는 A1-H1(vib/elec 유도 점프)·A1-L1/A2-D1(선두차수 오칭)·A3-D1(TikZ 한글)·A3-D2(dangling "파생 I")만 다루고 w_eff 는 "★4대 부호 ... 전부 견고"(L6)로 명문화 — 즉 v4-11 확정 시점에는 이 물리 오류가 **완전히 미인지 상태**였다.

---

## 3. v4 → v5 — w_eff 정정 (단일 pass, 코드 실행 기반 재검증)

**이전 문제.** §2 에서 확인한 파생 C(w_eff narrowing) 의 물리 오류.

**개선 의도.** v5 changelog(`v5-draft.tex` L1-13): 파생 C 절을 완전 제거하고, "$w$(logistic 폭)는 두-상($\Omega>2RT$)에서 *현상학적 자유 피팅 파라미터*이며, 실측 종 폭의 기원은 Chapter 1 의 broadening 절 참조"로 대체. 통계열역학 본체(A·B·D, 분배함수→점유분포→$S_\config$·vib·elec·히스)는 보존 명시.

**이 정정을 촉발한 근거 — 코드 실행 기반 falsification.** `CODE_w_check.md`(`Claude/results/research/radius/`)는 v11_final.py 를 실제로 실행해 세 경우(기본 w=12mV·코드 `use_w_eff`(Ω=13000)·"의도된" w_eff)의 peak 높이·FWHM·면적을 비교했다(L5-11): 기본 경로는 FWHM 42.3mV 의 정상 종(면적 0.499≈Q=0.5), 코드의 `use_w_eff` 경로는 FWHM 90.6mV·면적 9.294(18.6배 부푼 깨진 종), "의도된"(설계대로 n=0.05 일관 적용) w_eff 는 FWHM 4.5mV 의 진짜 뾰족이. 결론(L18-20): "$w_\eff$ 를 '상호작용이 종을 좁힘'으로 유도해 두었으나, 코드는 그렇게 구현하지 않고(불일치) 물리적으로도 거꾸로다." 이 문건이 소속된 `research/radius/`(입자 크기·앙상블 broadening 조사 트랙, `RADIUS_VERDICT.md`·`ORIGIN_VERDICT.md`·`BAND_VERDICT.md` 등)가 v5 가 참조하는 "Chapter 1 broadening 절"과 동일 계열임이 확인됨(`v5-draft.tex` L11-12 의 "단일입자 율속 꼬리+내재 RT/F+집합 다입자 통계역학 apparent-U 앙상블 분포"가 `CODE_w_check.md` L18 의 "w는 강한 1차 전이에서 자유 피팅 파라미터" 결론과 문구·논리 모두 일치).

**달성 여부.** 완전 취소·대체 확인. v5 §mixing(L430-437)·§limits 표(L613, "$\Omega\to2RT^-$: 상분리 임계(plateau); 실측 두-상 폭은 현상학적 피팅")·§revheat 종합식(L678-680, "$w_j$ 는 ... 단상 전이에서는 평형 예측 ... 흑연 staging 의 두-상 전이에서는 ... 현상학적 자유 폭")까지 일관되게 재작성됐다. 잔존 "narrowing" 문구 재확인 — v5 전문에서 $w_\eff$ 라는 라벨은 절 제목(L539, "폭 $w$ 의 지위")에만 남고 본문 수식에서는 완전히 사라짐(grep 결과 §sec:revheat 종합식은 `w_j` 만 사용, `w_eff(Ω)` 수식 없음).

**우수 구조 보존(사용자 질의 직접 답변).**
- **w_eff 제거가 Ch1 과 coordinated 였는가 — 예.** v5 는 폭의 *지위*(단상=평형 예측 vs 두-상=현상학적 피팅)만 Ch2 종합식에 못박고, 폭의 *기원*(broadening 물리)은 "Chapter 1 의 broadening 절"로 명시 위임한다(`v5-draft.tex` L554-555, L560, L680). 즉 고립된 삭제가 아니라 챕터 간 경계를 재조정한 coordinated 수정.
- **이중계산 B — 불변 보존.** `\S 2.2` 파생 B 박스(경고문 포함)는 v4-11 과 v5 사이 바이트 수준 동일(양쪽 L286-309 vs L293-309 문구 대조, ΔS 분해식 3항 동일). w_eff 삭제가 이중계산 논리를 건드리지 않았다는 뜻 — 국소 수정 원칙 준수.
- **극한 취급 — 물리 내용 보존, 서술만 정정.** 극한표(`tab:limits`) 의 $\Omega\to2RT^-$ 행이 v4 "w_eff→0, plateau"(상분리 임계 자체는 유지)에서 v5 "상분리 임계(plateau); 실측 두-상 폭은 현상학적 피팅"으로 바뀜(v4 L625 vs v5 L613) — **상분리 임계 조건($\Omega=2RT$) 자체는 변경 없이 유지**, 오직 "그 임계에서 폭이 어떻게 되는가"라는 잘못된 결론만 제거. 여섯 코너 중 나머지 다섯(config 발산 2·중심 표준값 회수·단일봉우리 환원·고온 electronic)은 완전 동일 유지.

**장단점.**
- 장점: 단일 pass 정정임에도 삭제 범위가 정확했다(파생 C 하나만, A·B·D·I 는 무변) — "그림만 틀렸지 문서의 나머지 골격은 옳다"는 정확한 진단.
- 단점: v5 자체에는 이 재검증을 수행한 별도 review1/review2 리뷰 파일이 없다(`ch2v5/` 빌드 디렉터리에는 tex/pdf/log 만 존재, 검수 문서 부재) — v4 수준의 다층 적대 검수 없이 "Opus 단일 build"(tex 헤더 L2-3)로 확정됐다. 즉 이번엔 검증 방법이 (다수 텍스트 검수 → 코드실행 검증)으로 바뀌었으나, 그 교정 자체를 재검수하는 절차는 생략됨 — 절차상 비대칭.

---

## 4. v5 → v1.0.10 — 문건 동결 편입 (코드-문건 동시 버전 통일)

**이전 문제.** v5-draft 는 `Claude/results/builds/ch2v5/` 에 산재한 빌드 산출물로, 정식 `docs/` 배포본이 아니었다. 또한 코드(`Anode_Fit_v11_final.py`)는 여전히 흑연 음극 전용이라 Ch1(LCO 확장)·Ch2(발열 q_rev) 이론과 코드가 어긋나 있었다(`2026-07-02-v1010-P3-ch2-heat-plan.md` L3: "P1 result — 발열 함수 q_rev 부재 확정").

**개선 의도.** P3 계획(`2026-07-02-v1010-P3-ch2-heat-plan.md`): Ch2 를 코드/Ch1 과 정합 매트릭스로 대조하고, v5 검토분(위 §3 의 정정)을 반영해 `docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex` 로 동결한다("순서 코드→문건→코드: 발열 코드 구현은 P4, P3는 이론", L3).

**달성 여부.** v1.0.10 ch2 tex 는 v5-draft 와 **본문 수식·절 구조가 사실상 동일**(entity-level diff 확인: L1-751 대응 문단 전부 일치, 차이는 4곳뿐 — ① L162 각주에 코드 심볼 `func_w` 교차참조 추가 ② L251 각주에 "방법 수준·dilute 격자기체 한정 참조" 명확화 추가 ③ L479 겹침 가중 분모 설명에 "$Q\,\partial x/\partial U$" 정규화 상수 명시(review2 A2-D3 LOW 결함 정정과 일치, `A2_adv_mixing.md` L25) ④ L653 부호규약 srcbox 에 "전셀 조립 시 음극 몫 부호반전" 범위 각주 추가). 즉 **이론적으로는 v5 확정본이 그대로 동결**됐고, v1.0.10 고유의 추가 작업은 코드 트랙(§5)에 집중됐다.

**우수 구조 보존.** v5 에서 확정된 파생 A·B·D·I·"현상학적 폭" 재정의가 전부 무변경 승계(참고문헌 목록도 `numverif2026` bibitem 의 코드명만 `Anode_Fit_v11`→`Anode_Fit_v1.0.10` 으로 갱신, L747). Ch2 이론 골격 자체의 "달성 여부" 판정은 §3 과 동일.

**장단점.**
- 장점: 문서-코드 버전 동기화 규율이 실제로 지켜짐(파일명·내부 참조 문자열까지 일치) — 이는 사용자 프로젝트 관례(코드-문건 동기화 대업무)에 부합.
- 단점: P3 계획이 "Ch2 ↔ 코드/Ch1 정합 매트릭스" 산출물을 요구했으나(계획 L6), 정독한 v1.0.10 tex 본문에는 그 매트릭스가 별도로 보이지 않는다 — 있다면 `V1010_P3_ch2_RESULT.md`(본 감사 범위 밖, 미정독)에 있을 가능성. **미검증(추정 아님, 단순 범위 밖 명시).**

---

## 5. 코드 트랙 — v11_final.py → v1.0.10.py (LCO seam·q_rev·use_w_eff 제거)

**이전 문제.** v11_final.py(617행)는 흑연 음극 전용 forward dQ/dV 모델로, (a) LCO(양극) 확장이 없고 (b) 가역 발열 함수 `q_rev` 가 없으며(`V1010_P4_code-revision_RESULT.md` 표제 인용 "P1 result 앵커 — 발열 함수 q_rev 부재 확정") (c) `use_w_eff` 경로가 §2-3 에서 밝힌 물리·구현 이중 버그를 안고 있었다.

**개선 의도.** 이론(Ch1 LCO 확장·Ch2 발열)을 코드에 1:1 반영 — "순서 코드→문건→코드: 이론(Ch1·Ch2) 확정 후 그 이론 1:1 코드화"(`V1010_P4_code-revision_RESULT.md` L3). 방법 = 9종 설계 드래프트(3S·3O·3C) → 검토1 → 체리픽 설계 → master(Serena)가 단독 실편입(단일 .py 는 공유 가변상태라 9종 동시편집 불가, L6) → adversarial.

**달성 여부.**
- **LCO seam**: School B(dqdv 항등 seam) 채택, 9종 전원이 놓친 "가장 약한 1곳"(equilibrium·q_rev 경로에서 LCO 전자항 누락)을 검토1 이 적발해 3경로 공유 헬퍼(`_effective_dS_rxn`)로 해소(L20-21). Serena 실편입 결과: `func_dSe_molar`(전자엔트로피 게이트)·`entropy_coefficient`·`reversible_heat`·`irreversible_heat`·`LCO_MSMR_LIT`/`LCOCathodeDQDV` 클래스 신설(L28-34).
- **q_rev**: $\dot Q_\rev=-IT\partial U_\oc/\partial T$ 구현, adversarial 검증에서 "T 한 번"($q-(-I\cdot T\cdot dUdT)=0.0$) 확인(L39) — Ch2 의 $\Delta S=+F\partial U/\partial T$ 규약과 T 중복곱 없이 일관.
- **use_w_eff 제거**: v1.0.10.py 헤더에 명문화("[1.0.10 변경] use_w_eff 경로 제거: ξ_eq 폭·분모 w 불일치로 면적보존 깨짐(버그) — w=자유 피팅 파라미터만", L7). 실제 코드 확인: `func_w_eff` 함수·`use_w_eff`/`w_eff_floor_frac` 생성자 인자·`self.use_w_eff` 속성이 전부 제거됨(`_width()` 메서드 L302-306, 분기 없이 `func_w(T, self._n_factor(tr,T))` 단일 반환).
- **회귀 검증**: 흑연 0-diff(13/13 배열 bit 완전일치, L45)·면적 ratio 불변(0.936308, L45)·LCO dQ/dV finite·피크 3.92/4.04(연속 블렌드 정합, L46)·전자엔트로피 $-45.68$(Ch1 $-46$ 대조, L47)·q_rev 범위(흑연 $[-0.216,0.105]$W, LCO $[-0.099,0.258]$W, L48) 전부 PASS.
- **항목 7(가장 약한 1곳, adversarial 최종 발견)**: LCO 전자엔트로피 $dS_e(T)\propto T$ 를 `func_U_j` 의 $T\Delta S$ 항에 그대로 넣으면 평형 peak $U_j(T)$ 와 `entropy_coefficient` 계산 사이에 **factor-2 불일치**(eq:U1T2 의 $a_e/2F$ vs $a_e/F$) 발생 — 단일온도 정합엔 무해하나 다온도 피팅에서 조용히 틀림(L39-40). Master 가 마감 시 LCO override 의 $dS_e$ 를 $T_\mathrm{ref}=298.15$K 동결 상수 오프셋으로 바꿔 해소(L40) — 이는 **일반해가 아니라 단일-기준 근사**이며, 다온도 T² 곡률 구현은 P5 로 명시 이월(L54-55).

**우수 구조 보존.**
- `func_w`·`func_U_j`·`func_U_j_hys`·`func_ksi_eq`·`func_L_q`·`_causal_lowpass`·`GRAPHITE_STAGING_LIT` 는 "1바이트도 변조 X" 원칙이 v11_final→v1.0.10 에서도 재확인됨(`Anode_Fit_v1.0.10.py` L34-36 원칙 명시 계승, 실제 `func_w` 정의 L74-75 는 v11_final L64-65 와 문자 그대로 동일).
- 死코드 `func_U_j_hys`·통계열역학 본체 불가침 원칙도 유지(`V1010_P4_code-revision_RESULT.md` L36).

**장단점·문제점.**
- 장점: use_w_eff 제거가 "코드 버그 보고"(§2-3)에서 시작해 실제 삭제까지 문서(CODE_w_check.md)·코드 헤더 주석(변경 이력)·회귀 테스트(v12_roundtrip_check.md 의 "0.00e+00 완전 동일" 확인) 3단으로 추적 가능하게 남아있다.
- 단점(경미): `Anode_Fit_v1.0.10.py` L305 의 `_width()` 독스트링이 "use_w_eff 경로는 ... v12에서 제거"라고 적어 두었는데, 실제로는 이미 **v1.0.10 자체에서** 이 경로가 완전히 제거된 상태다(L7 헤더와 모순). 별도로 `Claude/results/code/Anode_Fit_v12.py`(2026-07-01) 라는 파일이 이미 존재하며 이 파일이 `func_w_eff`·`use_w_eff` 등을 완전 삭제한 버전으로 `v12_roundtrip_check.md` 에서 회귀 검증까지 마쳤다(v11 대비 equilibrium/dqdv 출력 0.00e+00 동일) — 즉 "v12" 라는 이름이 이미 한 번(실험적 정리본으로) 소비됐다. 공식 차기 릴리스를 "v12"로 명명할 경우 이 선점 파일과 이름이 충돌하거나 오인될 위험이 있다(추정: 실제 충돌 여부는 두 파일의 병합 계획 문서를 확인해야 하며 본 감사 범위 밖).

---

## 6. v12 교훈 (cross-track 종합)

1. **적대 검수(adversarial review)는 "설계 문서 대비 내적 정합성"과 "물리적/실측적 타당성"을 별개 렌즈로 분리해야 한다.** v4 의 w_eff 사례는 5차원 검토1 + 3차원 검토2(독립 수치 재현 스크립트 포함)가 전부 마스터 자신의 설계 문서(`40_mixing_term_design.md`)를 기준(ground truth)으로 삼았기 때문에, 그 설계 문서 자체의 물리 오류(narrowing 그림)를 한 라운드도 걸러내지 못했다. 반대로 이를 잡아낸 것은 텍스트 재검수가 아니라 **실제 코드를 실행해 그래프·면적·FWHM 을 재는 실행 기반 검증**(`CODE_w_check.md`)이었다. → v12 이후 물리 모델을 다루는 모든 챕터 검수 루프에는 "이 닫힌식이 실제 코드 실행 결과(또는 실측/시뮬레이션 곡선)와 정성적으로 맞는가"를 묻는 최소 1개의 실행 기반(non-symbolic) 검증 단계를 의무화할 것.
2. **마스터 자신의 설계 단계 산출물도 무오류로 가정하지 말 것.** `REVIEW_RISK_PATTERNS.md` 가 스스로 인정했듯("내 원 설계 doc 이 틀렸고 9 작가 전부 상속") 설계자(마스터)의 오류는 하위 9개 독립 빌드 전원에 무비판적으로 전파된다 — 병렬 다양성(9종 무통신)은 "같은 잘못된 입력에서 출발한 다양한 서술"만 만들 뿐, 입력 자체의 오류에는 눈멀다. 설계 문서(spine/design doc) 확정 직후에도 최소 1회 "이 설계가 실측과 반대 방향일 가능성"을 묻는 역방향(counter-hypothesis) 체크를 넣을 것.
3. **국소 수정(local fix)의 파급 범위를 명시 문서화하는 습관은 유지할 가치가 있다.** v4→v5 전환은 파생 C 하나만 정확히 도려내고 A·B·D·I 는 그대로 뒀다(§3) — 이는 "문제 하나 고치려다 전체 재작성"을 피한 좋은 사례. 다만 이 교정 자체에 대한 재검수 절차(review1/review2 급)가 생략된 것은 절차적 비대칭이었다 — 향후에는 "치명적 오류 발견 시 국소 수정 + 최소 1회 독립 재검수"를 표준 절차로 삼을 것(교정도 검수 대상이다).
4. **코드 버전 명명 충돌을 피하기 위해 실험적 정리본에는 공식 버전 번호를 쓰지 말 것.** `Anode_Fit_v12.py` 가 정식 v12 릴리스 이전에 실험적 회귀검증 스크립트 이름으로 이미 소비됐다 — 다음 공식 버전이 "v12"가 될 경우 파일 관계(이 실험본을 흡수하는지, 폐기하는지)를 v12 착수 시점에 명시적으로 정리할 것.
5. **코드 주석의 "제거 시점" 서술은 실제 상태와 어긋나면 즉시 갱신할 것.** v1.0.10.py L7(헤더, "이미 제거")과 L305(독스트링, "v12에서 제거") 사이의 문구 불일치처럼, 같은 파일 안에서도 변경이력 서술이 시제 불일치를 일으킬 수 있다 — 커밋 시 grep 으로 "제거 예정" 류 표현이 실제로 남아있는 코드 경로를 가리키는지 자체 점검할 것.

---

## 7. 4-tier 분류 요약

- **확정**: v3 문헌 삼각검증·부호 규약(§1); v4 9종 경쟁 구조와 다수 CRITICAL 결함 적발(§2); v4→v5 w_eff 전면 취소 및 그 근거(CODE_w_check.md 실측치, §3); 이중계산 B·극한표 대부분 코너의 무변경 보존(§2-3); v1.0.10 코드의 LCO seam·q_rev·use_w_eff 제거와 회귀 0-diff(§5).
- **근거 미발견**: P3 계획이 요구한 "Ch2↔코드/Ch1 정합 매트릭스"의 tex 본문 내 소재(§4) — `V1010_P3_ch2_RESULT.md` 미정독으로 확인 불가.
- **추정**: `Anode_Fit_v12.py`(results/code) 와 차기 공식 v12 릴리스 사이의 이름 충돌 실질 위험도(§5) — 병합/폐기 계획 문서 미확인.
- **미검증**: review1 R4·R5, review2 A3 원문(요약은 `CHERRYPICK_PLAN.md`/`FIX_LIST_v411.md` 인용으로 교차 확인했으나 원문 전문 정독은 본 노트 작성 범위 내 수행하지 않음 — 결론 자체는 R1-R3·A1-A2 와 정합적이라 신뢰도 높음).
