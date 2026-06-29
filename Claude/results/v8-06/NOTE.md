# v8-06 자체검수 NOTE — graphite_ica_ch1 v8 (유도 과정 포함 교과서 확장판)

> 독립 작업(9건 경쟁 중 v8-06). 무통신. 산출 = `v8-06.tex`(자족) + `v8-06.pdf`(21p) + 본 NOTE.
> 권위 사양 = `AUTHOR_BRIEF_v8.md`. 배치 보존 = `v7-11.tex`. 유도 원천 = `graphite_ica_ch1_Opus_v5.tex`. 결과·부호 정본 = `Anode_Fit_v11_final.py`.

## 1. Read Coverage (전문 정독)

| 문건 | 행 범위 | 정독 방식 |
|---|---|---|
| `AUTHOR_BRIEF_v8.md` | 1–64 (전문) | 1회 전문 — ★최우선 사양 |
| `v7-11.tex` | 1–890 (전문, 2페이지 분할 read) | head→tail 전 영역. 절 순서·결과 박스 11개·그림 5개·표 3개·부호 검산 절·R1–R4 회귀 |
| `graphite_ica_ch1_Opus_v5.tex` | 1–1883 (전문, 4페이지 분할 read) | head→tail. Boltzmann→Eyring(287–354)·G→μ→detailed balance(356–599)·spinodal/binodal/weff(601–748)·전하보존/관측미분(750–834)·평형peak 종(836–882)·지연 일반해(884–996)·유효장벽(998–1054)·Arrhenius(1056–1155)·합성/꼬리(1157–1318)·히스 gap 닫힌꼴(1320–1427)·master/code(1429–1883) |
| `Anode_Fit_v11_final.py` | 1–706 (전문) | 원형 보존 함수·resolver·dqdv·GRAPHITE_STAGING_LIT·__main__ self-test |
| `v11_flowchart.md` | 1–90 (전문) | 척추 N0→N9·v5 eq 라벨 매핑·부호 규약(2026-06-29 분극 정정 포함) |

## 2. 10R 검수 추이 (가변 청크·렌즈 로테이션, ★G-derive 1급)

| R | 청크 스킴 | 렌즈 | 결함 적발 | 조치 |
|---|---|---|---|---|
| 1 | 그림 라벨 전수 | orphan/G-usable | **2건**: `fig:flux`·`fig:relaxode` 본문 \ref 0 (신규 그림 orphan) | 두 곳에 본문 \ref + 동기 문장 삽입 |
| 2 | 빌드 로그 | 빌드 무결성 | 0 (3-pass 0-error·undefined 0·rerun 0; 폰트 italic 경고는 kotex 정상) | — |
| 3 | TikZ 블록 9개 | 그림 ASCII | 0 (9블록 모두 한글 0 — 내부 라벨 ASCII, 캡션만 한글) | — |
| 4 | 결과 박스 11개 | 코드 1:1 정합 | 0 (U_j·dU_hys·U_branch·ksi_eq·w_eff·A·dH_eff·ln_Lq·peak·reversal 전부 v11 verbatim 일치) | — |
| 5 | 유도 사슬 11식 | G-derive 완결성 | 0 ((a)→(b)→(c)→(d) 마커 14/13, 중간식 ≥1 전식 확인) | — |
| 6 | 부호 8항 | 부호 적대검산 | 0 (S1–S8·R1–R4 v7-11 보존, V_n 분극·logistic·히스 분기·컷상수·격자역전 전건) | — |
| 7 | 렌더 페이지(1·7·10·12·13·16) | 시각 | 0 (히스 gap·hysloop·logistic·barrier·flux·relaxode·eqpeak 정상 렌더, overflow 없음) | — |
| 8 | 본문 전수 | 범위(무관 재유입) | 0 (lever/chord/Marcus/KWW/적층/master S0–S5 본문 0; line 8 헤더 주석만 "재유입 안 함" 명시; Optuna 는 보존된 사용자 목표) | — |
| 9 | label↔ref 전수 | 완결성(dangling/orphan) | 0 (dangling eqref/figref/tabref 0; orphan fig/tab 0; 미참조 9 eq-label 은 의도된 (c) 중간식) | — |
| 10 | 통독 + 절 다리 | 구조·재빌드 | 0 (clean 3-pass·21p·절 순서 N0→N9 + signcheck 보존·절 도입/마무리 다리 존재) | — |

수렴: R9·R10 연속 2라운드 0결함(하한 10R 충족 + 수렴 조건 충족).

## 3. ★유도 사슬 복원 목록 (어느 식의 어느 단계를 메웠나 — v7 압축 → v8 단계 복원)

브리프 §3 의 11식. 각 결과 박스(v7-11 보존)로 가는 (a)출발→(b)연산→(c)중간식≥1→(d)박스 를 복원. 신규 라벨(`eq:*mid`/중간식)이 (c) 자리.

1. **U_j(T)** (`eq:Uj`): G≡H−TS(`eq:gibbsdef`)→μ≡∂G/∂n(`eq:mudef`)→전기화학 평형 균형 `eq:eqbalance`→상수덩이 sFU 흡수→`eq:eqcond`(ΔG=−sFU)→ΔH−TΔS 대입·이항 `eq:Ujmid`→박스. (v7 "넣어 풀면"을 G/μ 다리로 복원)
2. **w_j** (`eq:wbase`): logistic 중심 기울기 sF/(4RT)가 폭 RT/F 정의→n_j 다중도 일반화. w_eff(`eq:weff`)는 비단조 등온선 중심 기울기 4RT−2Ω 매칭으로 복원.
3. **ξ_eq logistic** (`eq:xieq`): Eyring 비대칭 장벽 r±(`eq:bv`)→비 취해 χ 상쇄 detailed balance `eq:db`→운동방정식 정지점→logit `eq:logisticsolve`→폭·σ_d 일반화 박스. (v7 "detailed balance 로부터"를 r± 비·정지점으로 복원)
4. **평형 peak** (`eq:eqpeak`): 보존식 q-미분→logistic 미분 종 항등식 `eq:belliden`(ξ(1−ξ) 분해 명시)→연쇄율 σ_d/w→박스. (v7 "종 항등식에 연쇄율 곱하면"을 e^{-z}/(1+e^{-z})² 분해로 복원)
5. **ΔU_hys** (`eq:dUhys`): 격자기체 μ(`eq:mu`)→ξ 자유에너지 `eq:gxi`→2계 미분 `eq:gpp`→근의공식 spinodal `eq:spinodal`→비단조 V_eq `eq:Veq`→spinodal 대입 `eq:hyssub`(logit 역수·(1−2ξ)=∓u)→극대−극소 `eq:hysdiff`(artanh 정리)→박스. (v7 "대입하면 닫힌다"의 전 단계 복원)
6. **분기 중심 U_j^d** (`eq:Ubranch`): 두 spinodal 끝점 평균=U_j 대칭 `eq:hyssym`(로그합·(1−2ξ)합 둘 다 0)→방향별 한 자유도 박스.
7. **L_q** (`eq:Lqfull`): 운동방정식 용량축 환산→지연 변수 r_j ODE 중간 `eq:Lqmid`→길이 정의 `eq:Lq`→정·역 합 k_j=r⁺(1+e^{−A/RT}) + Eyring r⁺ `eq:kuniv`→대입 `eq:Lqmid2`→T_* 묶기 박스. 전압축 L_V(`eq:LV`).
8. **컷 affinity 𝒜** (`eq:Acut`): 컷 정의(원천 5%)→z_cut·n RT 구동력→min 상한 박스. ∂lnL_q/∂V<0 은 컷 동기(운영 미분 0) — v7 系統 결함 회피 명시.
9. **ΔH_a^eff** (`eq:dHeff`): 합-1 χ_d(`eq:chid`)→꼬리 구동력 −Ω(1−2ξ) 깊은 꼬리 상수 +Ω 흡수→박스. χ_d 충전 1−χ.
10. **L_V·인과 꼬리** (`eq:peakshape`): 1계 선형 ODE→적분인자 `eq:intfactor`→일반해 합성곱 `eq:memory`→이산 저역통과 점화식 `eq:lowpass`→peak=(ξ_eq−ξ_lag)/L_V 박스. 충전 격자역전 `eq:reversal`.
11. **합산** (`eq:sum`): 보존식 선형 합(직접 미분이라 가정 아님)→C_bg+ΣQ_j[peak]→V_n 역보간.

## 4. 부호 사슬 체크리스트 8항 (브리프 §7, v11 코드 대조 — 전건 PASS)

- S1 U_j=(−ΔH+TΔS)/F, ΔG=−FU ✓ (발열 ΔH<0 → 중심 ↑)
- S2 ξ_eq=logistic[σ_d(V−U)/w], 방전 V↑→ξ↑ ✓
- S3 dξ/dV peak=|ξ(1−ξ)/w|≥0 방향 불변 ✓
- S4 ΔU_hys≥0, Ω≤2RT→0, 분기 ±½σ_d → U^dis>U^chg ✓
- S5 χ_d 충전 1−χ, ΔH_a^eff=ΔH_a−χ_dΩ (합-1 거울) ✓
- S6 ∂lnL_q/∂V: 컷 상수라 운영 실현 미분 0, 부등식<0 은 동기 (자기모순 0) ✓
- S7 꼬리 충전 격자역전 ξ[::-1]…[::-1], 충전 dQ/dV 방전 거울(양수) ✓
- S8 분극 V_n=V_app−σ_d|I|R_n, 방전 측정 V_app>내부 V_n ✓

R1–R4 수치 회귀(ΔU_hys=86.7mV@Ω=12000·문턱 0·|I|→0 환원·L_q 동결) 전건 보존. 부호 결함 0.

## 5. 그림 목록 (v7-11 유래 / 신규)

| fig | 내용 | 출처 | 본문 \ref |
|---|---|---|---|
| fig:spine | 코드 진행 spine N0→N9 | v7-11 유래(그대로) | ✓ |
| fig:staging | 흑연 staging 갤러리 채움 | v7-11 유래(그대로) | ✓ |
| fig:doublewell | g(ξ) 이중웰·spinodal 띠 | **신규** | ✓ |
| fig:hysloop | 비단조 V_eq(ξ) 과주행 | v7-11 유래(캡션 식참조 보강) | ✓ |
| fig:barrier | 활성화 장벽 (a)평형/(b)구동 | **신규** | ✓ |
| fig:flux | 정·역 플럭스 교점 정지점 | **신규** | ✓ |
| fig:logistic | ξ_eq S-curve + 종 미분 | v7-11 유래(그대로) | ✓ |
| fig:relaxode | 지연 ODE 완화 ξ_eq vs ξ_lag | **신규** | ✓ |
| fig:reversal | 인과 꼬리 방전/충전 격자역전 | v7-11 유래(그대로) | ✓ |

합계 9개 = v7-11 유래 5 + 신규 4. 전 TikZ 내부 텍스트 ASCII 만(한글 0, 스크립트 검증). orphan 0(전 그림 본문 \ref·캡션 동기·앞 식 참조).

## 6. 빌드 결과

- 엔진: xelatex (MiKTeX, `C:\Users\lksz1\AppData\Local\Programs\MiKTeX\...\xelatex`).
- 명령: `xelatex -interaction=nonstopmode -halt-on-error v8-06.tex` × 3-pass(clean .aux/.toc/.out 후).
- 결과: **3-pass 전부 exit 0, 0 TeX error, undefined ref/cite 0, "Rerun" 경고 0**.
- 산출: `v8-06.pdf` **21페이지**, 394 KB.
- 잔여 경고(무해, v7-11 동일): kotex 폰트 italic shape 자동 대체(`TU/UnBatang/m/it` 등), "Infinite glue shrinkage"(longtable 분할 1건, 렌더 정상).
- preamble = v7-11 계열(kotex/D2Coding/amsmath/tikz, 자족) + `derivbox` theorem 추가.

## 7. 보존·확장 요약

- **보존(불가침)**: 절 순서 N0→N9 + signcheck, 결과 박스 11개(식 형태 v11 1:1), 코드 식별자, 부호 8항·R1–R4, 표 3종(staging/inputs/nodemap), v7-11 그림 5개, bibliography 7건. v7-11 의 식 라벨(eq:vn·eq:Uj·… eq:sum) 동일 유지.
- **확장(유도 추가만)**: 각 박스 위 (a)→(b)→(c)→(d) 단계, 신규 중간식 9개 라벨, 신규 그림 4개. .tex 890→1181행(+291, 유도의 자연 결과). 분량 21p(브리프 28–40p 예상 대비 — v7-11 preamble 의 조밀 조판; 패딩 없이 유도만 추가한 결과).

## 8. Decision Queue

- 없음. 모든 사양 충족(빌드 통과·orphan 0·부호 8/8·코드 1:1·유도 11식 복원·그림 9개[유래 5/신규 4]·10R 수렴).
