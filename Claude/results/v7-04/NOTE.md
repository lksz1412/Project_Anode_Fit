# v7-04 자체검수 노트 (graphite_ica_ch1 v7, 코드-진행 어레인지)

산출물: `v7-04.tex` (자족, v5 계열 preamble) + `v7-04.pdf` (16쪽, xelatex 2-pass).
역할: v11_final.py 의 클래스 계산 진행(플로우차트 N0→N9)을 절 순서로, 그 순서를
이해하는 데 필요한 물리식만 그 순서대로 유도한 수식-주도 교과서(Chapter 1).

## 1. Read Coverage (전문 정독 행범위)

| 문건 | 경로 | 정독 범위 |
|---|---|---|
| AUTHOR_BRIEF | `v7-00_spine/AUTHOR_BRIEF.md` | 전문(1–76, head→tail) |
| 플로우차트(척추) | `v7-00_spine/v11_flowchart.md` | 전문(1–90) |
| v11_final 코드(정본) | `v7-00_spine/Anode_Fit_v11_final.py` | 전문(1–706, head→tail) |
| v5 형식 레퍼런스 | `Claude/docs/graphite_ica_ch1_Opus_v5.tex` | 전문(1–1883, 5청크 분할 정독) |

- v6 는 의도적으로 보지 않음(브리프 지시 — 이 단계 v5만).
- 코드 핵심 행 1:1 확인: dqdv [L374-484], _resolve_lag_length [L307], _causal_lowpass [L100],
  func_U_j [L68], func_ksi_eq [L84], func_L_q [L90], func_dU_hys [L123], func_U_branch [L133],
  func_chi_d [L155], func_dH_a_eff [L149], GRAPHITE_STAGING_LIT [L535-564].

## 2. 절 구성 (척추 N0→N9, 1:1)

| 절 | 노드 | 제목 | 핵심 식 |
|---|---|---|---|
| 서론 | — | N0–N9 진행 개요 + staging 도식 | — |
| §1.1 | N0 | 기호와 실험조건 매핑 | eq:setup |
| §1.2 | N1 | 분극 — 측정→내부 전위 | eq:vn, eq:vwork, eq:bgseed |
| §1.3 | N2 | 평형 중심 U_j(T) | eq:gibbsdef, eq:Uj |
| §1.4 | N3 | 히스테리시스 분기 중심 | eq:gxi, eq:spinodal, eq:Veq, eq:dUhys, eq:Ubranch |
| §1.5 | N4,N5 | 폭과 평형 점유(logistic) | eq:w, eq:weff, eq:relax, eq:logistic |
| §1.6 | N6 | 평형 peak(|I|→0 한계) | eq:belliden, eq:dxidV, eq:eqpeak, eq:equilibrium |
| §1.7 | N7 | 동역학 지연 길이 L_V | eq:Lq, eq:Lqclosed, eq:affcut, eq:chid, eq:dHeff, eq:LV |
| §1.8 | N8 | 인과 기억 꼬리·충전 역전 | eq:memory, eq:lowpass, eq:reversal, eq:peakshape |
| §1.9 | N9 | 합산·역보간 + STAGING 표 | eq:total |
| 맺음 | — | 진행·환원·무결성 요약 | — |

절 순서 = 플로우차트 N0→N9(코드 dqdv 실행 순서)와 1:1. 각 절에 도입(앞 절 인계)·
마무리(다음 절 다리)·코드 대응 박스 배치.

### Decision Queue (브리프 §3 vs 플로우차트 절 순서)
- 브리프 §3 권장 골격은 N4,N5→N6→N3(히스를 peak 뒤 "구조 선언"으로) 순서를 적시하나,
  같은 브리프가 "절 순서 = 플로우차트 N0→N9"를 최상위로 못박고, 플로우차트(공유 척추,
  코드 dqdv 실행 순서)는 N2→N3→N4→N5→N6 이다. 두 통제문서 충돌 시 **공유 척추(플로우차트
  = 코드 진행)를 채택**했다(N3 을 N2 직후에 둠). N3 절은 브리프 의도대로 "분기 위상 구조
  선언"으로 작성하고 γ=0/Ω≤2RT 환원을 명시해 방전 본론과 충돌 없게 했다. master 판단 사항.

## 3. 그림 목록 (전부 신규 TikZ, 내부 텍스트 영어 ASCII)

| 라벨 | 위치 | 동기(앞 식)·사용(본문 ref) | 왜 필요 |
|---|---|---|---|
| fig:staging | 서론 | staging 채움 → N9 합산 | 4전이 물리 직관(층·갤러리·채움 조밀화) |
| fig:hysbranch | §1.4 | eq:Veq loop → eq:dUhys/eq:Ubranch | 방·충 중심 ±분기, spinodal 극값 |
| fig:bell | §1.6 | eq:logistic → eq:eqpeak | logistic·미분 종(peak 1/4·중심 U_j^d) |
| fig:tail | §1.8 | eq:reversal → eq:peakshape | 충전 격자 역전(꼬리 거울 방향) |
| fig:sum | §1.9 | eq:total | 4전이 합산 → 한 ICA 곡선(융합) |

- 전 그림 \ref 됨(orphan 0). 내부 텍스트 한글 0(축·라벨·노드 전부 ASCII; subscript 는
  `Ujd`/`xi-s minus`/`dU-hys`/`sigma-d` 식으로 풀어 씀). 캡션만 한글. PDF 렌더 육안 확인 완료
  (5개 그림 전부 정상: staging 층/띠, 히스 loop, logistic+bell, 꼬리 거울, 4-peak 합산).

## 4. 부호 사슬 체크리스트 (브리프 §8, 전건 PASS)

| # | 항목 | 식 | 코드 | 결과 |
|---|---|---|---|---|
| 1 | U_j=(−ΔH+TΔS)/F, ΔG=−FU | eq:Uj/eq:gibbsdef | func_U_j L68 | ✓ |
| 2 | ξ_eq=logistic[σ_d(V−U)/w], 방전 V↑→ξ↑ | eq:logistic | func_ksi_eq L84 | ✓ |
| 3 | dξ/dV=σ_d ξ(1−ξ)/w, peak 양수(방향 불변) | eq:dxidV/eq:eqpeak | L468/L370 | ✓ |
| 4 | ΔU_hys≥0, Ω≤2RT→0, 분기 ±½σ_d | eq:dUhys/eq:Ubranch | func_dU_hys L123, func_U_branch L133 | ✓ |
| 5 | χ_d(방전 χ/충전 1−χ), ΔH_a^eff=ΔH_a−χ_d Ω | eq:chid/eq:dHeff | func_chi_d L155, func_dH_a_eff L149 | ✓ |
| 6 | ∂lnL_q/∂V<0 (V↑→장벽↓→꼬리↓) | §1.7 본문/verifybox | func_L_q L90 | ✓ |
| 7 | 충전 격자 역전 ξ[::-1]…[::-1], 충전=방전 거울·양수 | eq:reversal | L474-477 | ✓ |
| 8 | V_n=V_app−σ_d|I|R_n | eq:vn | L412 | ✓ |

전건 정합: 방전 V↑→탈리튬화↑, 충전 dQ/dV=방전 거울. 환원 검산 둘 — |I|→0 → equilibrium(γ=0
한정), γ=0/Ω≤2RT → 단일 중심 — 식으로 확인.

## 5. 10R 가변-청크·렌즈 검수 결함 추이

병렬 adversarial Agent(세션 분리 cross-check) + master 직접 삼각검증·수정·재유도.

| R | 청크 스킴 | 렌즈 | 결함 수 | 주요 적발·조치 |
|---|---|---|---|---|
| 1a | 절별 부호 | 물리·부호 적대검산 | 9 | z_cut≈2.94/n 부호/배치 오류, L_q 유도 "역항 사멸" 모순(인자 미정당), q=Q/Q_cell 사용처, ΔU/∂T 규모(0.1→0.2-0.3), 단위 c-rate·Q_cell·|I| 불일치, U(298)=0.211 vs 0.210 자기모순, 체크7 라벨오류, k_j 정의 선행 |
| 1b | 절·노드 | spine·G-follow·form | 11 | V_eq(ξ) 무유도 등장(최약), w 이상극한 먼저(보편식 X 완화), 괄호 전보체(χ 약분), N7→N8 다리 부재, eq:bgseed/dxidV/lowpass orphan, 5번째 그림(N9 합산) 부재, A 의미 이중 |
| 1c | 식별자·LaTeX | G-usable·완결성 | 17 | n_work=2|V_app|(→2·len), 기본상수 5종 누락(min_lag=2.0·pad=0.15·n_min=2048·floor=0.05·χ=0.5), L_q(I≤0)=−inf 가드, T_rep·|n| 평가점, 'w' 폴백 미설명, equilibrium vs dqdv(γ>0) 캐비엇, $그리고$ math 위험 |
| 2 | 수정영역+전역 | new-defect·삼각 | 3 | **Q_cell 단위 [A·h]↔[C] 모순(최약, 3600× 위험)**, charge-conservation 단위, orphan eq 2종(figure-scope 아님·LOW) |
| 3 | 단위사슬+부호+전역 | 수렴 확인 | 0 | 단위 전역 정합·8 부호 전건·44/44 label·ASCII·코드행 전부 PASS. weakest=∂lnL_q/∂V 개념 vs 동결(LOW, 캐비엇 기존재) → 한 줄 명료화 |

- 수렴: R3 = 0 결함(앞 R2 의 단위 모순 수정 후). R3 명명 weakest(LOW, 결함 아님)는 verifybox
  한 줄 명료화로 닫음(식·참조 불변 → 추가 결함 무).
- 청크 스킴 매 라운드 전환(절→절·노드→식별자→수정영역→단위사슬), 렌즈 로테이션(부호·spine·
  G-follow·G-usable·완결성·시각·new-defect). 빈 통과 금지(매 라운드 weakest 강제 적발).

## 6. 빌드 결과

- `xelatex -interaction=nonstopmode` 2-pass (MiKTeX, D2Coding 폰트 설치 확인).
- **에러 0, undefined cross-reference 0, Missing $ 0, 큰 overfull box 0.**
- PDF: 16쪽, 328 KB. 식 번호 1.x, 절 1.x, 그림 1–5 정상.
- 잔여 경고 = 폰트 italic 대체 3건(UnBatang/D2Coding italic shape 미정의 → upright 대체) —
  v5 레퍼런스와 동일한 무해 경고(한글·mono 폰트가 true italic 부재). 에러 아님.
- label 감사: 정의 44 = 참조 44, orphan 0(PowerShell regex 확인).

## 7. 특징

- v5 수식-주도 형식을 v11_final 코드 진행(N0→N9)에 어레인지: 곡선에 필요한 식만 코드 순서대로
  유도. 각 절 코드 대응 박스(식↔식별자↔행번호 1:1)로 G-usable 봉인.
- G-usable: §1.9 에 "이 문건만으로 곡선 재현" 6-step 진행 + 전 기본상수(z_cut=4.357·A_cap=4·
  m=2.0·pad=0.15·n_min=2048·floor=0.05·χ=0.5·ΔS_a=0) + STAGING 4전이 값표(코드 L535-564 와
  value-for-value 일치 검증).
- 신규 그림 5개(전부 TikZ·ASCII 내부텍스트), 기존 v5/v6 그림 재사용 0.
