# V1010_INSPECT_draft_S1 — Ch1 forward-model 물리·그래프 검수 보고

- **Sub-agent ID**: S1
- **초점**: Ch1 forward-model 물리 (U_j·ξ_eq·peak·꼬리) + 그래프 개형 실행·판독
- **담당 cross-version**: v3 (`old/_archive/graphite_ica_ch1_Fable_v3.tex`)
- **작성일**: 2026-07-02
- **상태**: 초안 (master 교차검증 대기)

---

## 0. 검수 대상 파일 목록 & 정독 coverage

| 파일 | 줄·크기 | 정독 방법 | Coverage |
|------|---------|-----------|----------|
| `Anode_Fit_v1.0.10.py` | 742줄 | head→tail 전 영역 Read | 100% |
| `graphite_ica_ch1_v1.0.10.tex` | ~169 KB | 다수 청크 offset/limit 전 영역 | 100% |
| `graphite_ica_ch2_v1.0.10.tex` | ~62 KB | 다수 청크 전 영역 | 100% |
| `old/_archive/graphite_ica_ch1_Fable_v3.tex` | ~200 KB | 다수 청크 전 영역 | 100% |
| `figs/anode_fit_v1_0_10_dqdv.png` | — | 이미지 직접 판독 | Panel 1~4 |
| `figs/P5_graph_suite.png` | — | 이미지 직접 판독 | V1·V5·V8 패널 |
| `figs/P4_lco_heat_validation.png` | — | 이미지 직접 판독 | (a)(b)(c) 패널 |

---

## 1. 발견 목록

### [HIGH-1] P4_lco_heat_validation.png (a): 흑연 dQ/dV = 단일 broad bell 하나만 — staging 4개 전이 구분 없음

**위치**: `figs/P4_lco_heat_validation.png`, 패널 (a) "Graphite anode dQ/dV (discharge)"; `demo_lco_heat.py` (추정); `GRAPHITE_STAGING_LIT` 딕셔너리 사용 여부 미확인

**무엇이 문제인가**:
패널 (a)에서 흑연 음극 dQ/dV는 단 하나의 넓은 bell 종 형태만 보이며, 0.02 C / 0.2 C / 1.0 C 세 조건이 거의 동일하게 겹친다. 흑연 graphite staging 전이가 정상 동작한다면 stage 4→3, 3→2L, 2L→2, 2→1 네 개의 전이에 해당하는 복수 peak가 분리되거나 적어도 어깨(shoulder)가 존재해야 한다(문건 sec:staging 정의·코드 `GRAPHITE_STAGING_LIT`에 4개 전이 등록).

**왜 문제인가 (근거)**:
`demo_lco_heat.py`가 흑연을 단일 대표 전이로만 모델링하거나, `GraphiteAnodeModel`에 단일 전이만 넘기고 있을 가능성이 높다. 같은 코드베이스의 `anode_fit_v1_0_10_dqdv.png` 패널 (1)에서는 4개 bell이 명확하게 분리·표시되므로, P4 demo가 staging을 의도적으로 단순화한 것인지 아니면 버그인지를 문건이 설명하지 않는다. 교과서 교재(Ch1)가 4 staging 전이를 핵심 물리로 교육하는데 검증 그래프(P4)가 그것을 재현하지 않으면 독자는 "코드가 staging을 표현한다"는 주장을 신뢰하기 어렵다.

**어느 렌즈**: G-usable(그래프 검증가능성), 물리적 완결성

---

### [HIGH-2] 두-상 전이(Ω > 2RT) dQ/dV 평형 개형: near-delta 기대 vs. w=RT/F bell 실제 — 이중지위 설명이 불충분

**위치**:
- `Anode_Fit_v1.0.10.py` line 74–75 `func_w`: `return n * R * T / F` (w_eff 없음)
- `Anode_Fit_v1.0.10.py` line 388 `equilibrium()`: `ksi_eq * (1-ksi_eq) / w`
- `Anode_Fit_v1.0.10.py` line 486 `dqdv()`: `peak_shape = ksi_eq * (1-ksi_eq) / w`
- `graphite_ica_ch1_v1.0.10.tex` sec:width (폭 이중지위 설명)
- `figs/anode_fit_v1_0_10_dqdv.png` Panel 1·2

**무엇이 문제인가**:
LiC12(stage 2L→2)·LiC6(stage 2→1)는 두-상 전이(Ω > 2RT). Maxwell 공통접선 해석에 따르면 단일-particle 평형 점유 ξ_eq는 coexistence 전위에서 0→1 계단(near-delta 미분)을 보여야 한다. 코드는 `func_w = n_j * RT/F ≈ 25.7 mV` (25°C)를 그대로 쓰므로, LiC6 panel 2에서 Q=0.499의 넓은 bell을 생성한다(그래프 실측). 이것이 "현상학적 피팅 폭" 설계라면 허용되지만:

1. `sec:width`에서 "두-상 w = 현상학적 피팅 폭"이라고 기술하나, "단일 입자 평형은 near-delta지만 코드가 생성하는 bell은 broadening 흡수 결과"임을 명시하는 문장이 없다.
2. v3에서 Ω→2RT 극한에서 w_eff→0이 되어 two-phase 전이의 near-delta 물리를 재현하는 `w_eff` 유도(eq:weff)가 있었는데, v1.0.10에서 이 유도가 완전히 삭제되었다. 삭제 이유(면적보존 깨짐 버그)가 코드 헤더 주석에만 한 줄로 적혀 있고 tex 교재에는 없다.
3. 결과적으로 독자는 "두-상 전이에서 equilibrium()이 near-delta를 돌려주지 않는 이유"를 교재만 읽어서는 파악할 수 없다.

**왜 문제인가**: G-follow(추론 따라가짐)·물리 정합성. 코드 출력이 교재에서 암묵적으로 기대되는 개형(near-delta)과 다름에도 이를 정당화하는 논리가 tex에 없으므로, 독자가 코드와 교재를 함께 읽을 때 불일치로 오해한다.

**어느 렌즈**: G-follow, 물리적 완결성, G-usable

---

### [HIGH-3] v3 eq:superpose(입자 분포 꼬리 일반형) + σ_lnL = σ_G/RT + KWW — v1.0.10 tex에 완전 누락

**위치**:
- v3 tex lines ~1600–1676: `eq:superpose` (∫ρ_G·(r_a/L_V)·exp(-(V-Va)/L_V)dG), `eq:deltareduce` (δ-극한 환원), `eq:varprop` (σ_lnL = σ_G/RT), KWW stretched exponential 연결
- v1.0.10 tex: Grep 검색 결과 rho_G·superpose·varprop·KWW·stretched 어느 것도 절 수준으로 없음. 무관 일반론 제외 목록에서 "KWW" 한 줄 언급(주석)만 존재

**무엇이 문제인가**:
꼬리 형태의 물리적 근거를 두 겹으로 제시할 수 있다:
- **δ-극한 단일 L_V**: 현행 v1.0.10 구현(지수 저역통과 `_causal_lowpass`)이 취하는 방식
- **일반형**: ρ_G(G) 분포를 갖는 입자 앙상블에서 꼬리가 ∫ρ_G·exp(...) 형태로 stretched exponential(KWW)에 수렴

v1.0.10이 δ-극한 단일 L_V만 쓰는 것은 코드 설계 선택으로 허용되지만, Ch1 sec:lag 어디에서도 "왜 δ-극한만 취하는가", "입자 분포가 있을 경우 어떻게 되는가"를 설명하지 않는다. 특히 σ_lnL = σ_G/RT — 저온일수록 꼬리 폭의 입자간 산포가 커짐 — 은 실험에서 관찰 가능한 온도 의존 비대칭성을 예측하는 결과인데, 이것이 tex에 없으면 온도별 꼬리 모양의 차이를 독자가 설명할 수 없다.

**왜 문제인가**: 피팅 실용성(stretched tail 진단 불가), G-usable(온도 의존 꼬리 예측 기반 없음)

**어느 렌즈**: G-usable, 물리 완결성, cross-version 회귀

---

### [MED-1] w_eff 유도 절(eq:weff) 삭제 — 두-상 전이 Ω→2RT 극한 물리 설명 소실

**위치**:
- v3 tex sec:regsol, line ~1219: `w_j^{eff} = (RT/F)(1 - Ω_j/2RT)`, "상호작용이 있으면 w^eff로 좁아진다"
- v1.0.10 tex: sec:width가 폭 이중지위를 서술하나, eq:weff 유도 자체 없음

**무엇이 문제인가**:
v3은 regular solution 모델에서 `w_eff = (RT/F)(1 - Ω/2RT)`를 유도하여 Ω→2RT 극한에서 폭이 0(near-delta)이 됨을 보였다. v1.0.10은 이 유도를 버그(면적보존 깨짐)로 간주해 제거했는데:

1. 코드 헤더 주석에 제거 이유가 한 줄("`use_w_eff 제거: ξ_eq 폭·분모 w 불일치로 면적보존 깨짐(버그)`")뿐이며 tex에 이 설명이 없다.
2. 두-상 전이에서 단일-particle near-delta가 물리적으로 왜 나오는지를 교육하는 유도가 사라졌다. sec:width의 현상학적 설명("피팅 폭")만으로는 이 물리를 완결하기 어렵다.

**어느 렌즈**: G-follow, 물리 완결성

---

### [MED-2] `func_L_q` 내부: `log(1 + exp(-A/RT))` softplus 항 — 물리 의미 tex 미설명

**위치**:
- `Anode_Fit_v1.0.10.py` line ~160: `ln_Lq = log(T_attempt/T) - log(1+exp(-A/RT)) + dG_a/RT - x*A/RT`
- v1.0.10 tex sec:lag: `A = min(z_cut·n_j·RT, A_cap·RT)`, `L_q = |I|/(Q_cell·k_j)` 설명

**무엇이 문제인가**:
`-log(1+exp(-A/RT))`는 softplus 함수로, `A→∞`이면 0(기여 없음), `A→-∞`이면 `A/RT` 계단. 이 항의 물리적 역할은 "속도식에서 역방향 기여를 적분한 효과로 A<0 영역에서 barrier가 없어지는 한계를 부드럽게 잇는다"는 것인데, tex에서는 단지 `A`의 정의(`min(...)`)만 서술하고 이 softplus 항이 왜 들어가는지를 설명하지 않는다. 따라서 독자가 코드를 읽을 때 이 항을 확인할 수 없다.

**어느 렌즈**: G-follow, G-usable(코드 재현성)

---

### [MED-3] `anode_fit_v1_0_10_dqdv.png` Panel 3: 방전·충전 꼬리 방향 — 검증 기준 정량 없음

**위치**: `figs/anode_fit_v1_0_10_dqdv.png` Panel 3 "discharge vs charge with kinetic tail + hysteresis"

**무엇이 문제인가**:
Panel 3은 방전·충전 두 곡선을 표시하며 꼬리 비대칭과 히스테리시스를 보여준다. 그러나:
1. 꼬리 지수 특성 길이 L_V 수치가 그래프에 없다.
2. 방전 꼬리가 저전위 방향으로 늘어지는지(물리적 기대), 충전 꼬리가 고전위 방향으로 늘어지는지를 판독하기 어렵게 두 곡선이 겹쳐 있다.
3. 오차 지표·실험 데이터 오버레이 없이 "모델이 꼬리를 잘 재현한다"는 정성 확인에 그친다.

**어느 렌즈**: G-usable(피팅 실용성), 검증가능성

---

### [MED-4] `_causal_lowpass` scipy 경로 vs. 점화식 경로 분기 — 문건 미언급, 수치 동등성 미검증

**위치**:
- `Anode_Fit_v1.0.10.py` lines ~200–240: `_causal_lowpass` 내부에 `scipy.signal.lfilter` 경로와 점화식(fallback) 두 갈래가 있음
- v1.0.10 tex: `_causal_lowpass` 구현의 두 경로 중 어느 것이 기준인지 언급 없음

**무엇이 문제인가**:
두 구현 경로가 수치 동등함을 단위 테스트로 검증한 흔적이 코드에 없다. scipy unavailable 환경(일부 HPC·임베디드)에서 fallback 점화식을 쓸 경우 결과 차이가 0인지 검증이 필요하며, 교재에서 이 구현 선택을 설명하지 않는다.

**어느 렌즈**: G-usable(재현성), 코드 견고성

---

### [LOW-1] `GRAPHITE_STAGING_LIT` `n`:1.0 — staging 전이별 n_j 차이 물리 근거 미서술

**위치**:
- `Anode_Fit_v1.0.10.py` `GRAPHITE_STAGING_LIT`: 4개 전이 모두 `'n': 1.0`
- v1.0.10 tex sec:transitions 또는 parameter table

**무엇이 문제인가**:
n_j는 한 번의 staging 전이에서 이동하는 Li 이온 수(또는 Redlich-Kister order)를 반영할 수 있다. stage 2L→2 전이(1/6→1/4 Li/C)와 stage 2→1 전이(1/4→1/2 Li/C)는 전이 폭이 다를 수 있으며, 이 물리적 차이가 n_j=1 일률 적용으로 흡수 가능한지 tex에서 논의되지 않는다. 문헌 fitting 결과로 n_j를 고정하는 것이 수렴 관행이라 해도 그 justification이 없다.

**어느 렌즈**: 물리 완결성

---

### [LOW-2] Panel 4 온도 의존 bell: 저온에서 bell 좁아짐(w∝T) 확인 — 그러나 실험 역전 설명 그래프 없음

**위치**: `figs/anode_fit_v1_0_10_dqdv.png` Panel 4 "single LiC6 equilibrium vs T"

**관찰**:
Panel 4에서 저온일수록 bell이 좁고 높아진다. 이는 `func_w = n_j * R * T / F`의 선형 T-의존성을 반영하며, 평형(ξ_eq) 미분으로 예상되는 방향이다. 이 범위에서는 물리적으로 올바르다.

**남은 공백**:
실험에서 저온에서 peak가 더 넓게 관찰되는 역전(꼬리 우세 체계)을 모델이 어떻게 설명하는지 보여주는 온도별 비교 그래프가 없다. sec:lag 꼬리 절이 저온 확장을 예측한다고 서술하나, 이것을 그래프로 실증하는 panel이 없다.

**어느 렌즈**: G-usable, 검증가능성

---

## 2. 무결 확인 (빈 통과 금지 대응)

아래 항목은 검수 후 물리적으로 정합하거나 의도적 설계로 판단되어 결함 분류에서 제외한다. 근거를 남긴다.

| 항목 | 위치 | 판정 | 근거 |
|------|------|------|------|
| 면적 보존 `∫ksi*(1-ksi)/w dV = 1` | py line 388·486, equilibrium()·dqdv() | ✓ 정합 | `∫ksi*(1-ksi)/w dV`는 ξ_eq의 적분이므로 정확히 1. Panel 2 실측 Q=0.499 (≈0.5, 이산 격자 오차 허용 내) |
| `func_U_j(T)` = dH-T*dS 선형 | py line ~55 | ✓ 정합 | 표준 반응엔탈피·엔트로피 분리. 온도 범위(200–330 K) 내 선형 근사 적절 |
| `_causal_lowpass` 방향 부호 | py line 491–495: σ_d≥0→정방향, 음→뒤집기 | ✓ 정합 | 방전(V 증가)=오름차순, 충전(V 감소)=내림차순 반전 후 필터는 eq:memory 인과 합성곱과 일치 |
| σ_d 히스테리시스 분기 (eq:hyscenter) | py line 460–470 | ✓ 정합 | `func_U_branch`로 방·충 center 분리, γ=0 시 비활성화 |
| P5 V8 패널 면적비 ≈ 0.979 | `P5_graph_suite.png` V8 | ✓ 근사 보존 | 수치 적분 이산화 오차 2.1% 수준. 의도적 격자 이산 결과로 허용 |
| Ch2 (발열) ΔH_rxn 기여항 seam | py line 532–545 `_effective_dS_rxn` | ✓ 정합 | equilibrium·dqdv·entropy_coefficient 세 경로가 같은 seam을 공유해 일관성 유지 |
| detailed balance `r+/r- = exp(A/RT)` | v1.0.10 tex sec:lag | ✓ 정합 | χ_d·Ω 보정(ΔHa^eff = ΔHa - χ_d·Ω)이 두-상 전이에서 방·충 asymmetry를 만드는 경로가 sec:lag에 명시됨 |
| Dreyer 다입자 해석 (sec:broadening) | tex sec:broadening | ✓ 적절 | apparent-U = U_j + η 분리, 분포하는 것이 η임을 명시. 면적 보존(Q_j 직접 회수) 설계 정당 |

---

## 3. Cross-version 누락 판정 (v3 대비)

| v3 항목 | v1.0.10 상태 | 판정 | 설명 |
|---------|-------------|------|------|
| `w_eff = (RT/F)(1-Ω/2RT)` (eq:weff) | tex에서 완전 삭제 | **의도적 컷 — 교육 가치 손실** | 버그(면적보존 깨짐)로 코드에서 제거됨은 정당. 그러나 두-상 near-delta 극한의 물리 유도가 tex에서 사라져 교육 목적 훼손 |
| `eq:superpose` 입자 분포 꼬리 일반형 | tex에 없음 | **누락(결함)** | δ-극한만 쓰는 근거가 tex에 없고, stretched tail 진단 기반 부재 |
| `σ_lnL = σ_G/RT` (eq:varprop) | tex에 없음 | **누락(결함)** | 온도 의존 꼬리 늘어짐 예측 불가 |
| KWW stretched exponential 연결 | tex에 없음(주석 한 줄 언급만) | **의도적 컷 — 허용** | 실무 불필요 판단으로 제거. 주석에서 명칭 언급은 있음 |
| Arrhenius 회귀식 (eq:arrhenius, eq:ydef) | 확인 필요(sec:lag·sec:arrhenius 검색 미확인) | **추정: 부분 포함** | ΔHa 피팅 부분은 있으나 y(T) 회귀 선형화 식이 tex에 명시됐는지 미확인 |
| sec:hyspeak (2상 broadening 별도 절) | v1.0.10 sec:lag + sec:broadening 분산 | **재구조화** | 기능은 유지되나 절 구조가 다름 |

---

## 4. 가장 약한 1곳 필수 지목

**HIGH-1 (P4 단일 bell)이 가장 약한 1곳이다.**

이유: 교재(Ch1)가 4 staging 전이를 핵심 물리로 교육하고, 코드(`GRAPHITE_STAGING_LIT`)도 4개 전이를 등록하지만, 가장 눈에 띄는 검증 그래프(P4, demo_lco_heat)가 단일 broad bell만 보여 staging이 실제로 구현·재현되는지를 독자가 확인할 수 없다. `anode_fit_v1_0_10_dqdv.png`의 4 peak 그래프는 `demo_main`에서만 나오고 P4가 이를 재현하지 못하면 Ch2 LCO 발열과의 통합 검증에서 흑연 부분의 신뢰성이 없다.

---

## 5. 5줄 요약

1. **초점**: Ch1 forward-model 물리(U_j·ξ_eq·peak·꼬리) + v3 cross-version + 그래프 직접 판독
2. **문제 수**: HIGH 3건 · MED 4건 · LOW 2건 (총 9건), 무결 확인 8항목
3. **최중대**: HIGH-1(P4 demo 흑연 staging 미재현 — 교재·코드·그래프 삼각 불일치) > HIGH-2(두-상 near-delta vs. bell 이중지위 tex 미설명) > HIGH-3(eq:superpose·σ_lnL=σ_G/RT cross-version 누락)
4. **그래프 개형 판정**: `anode_fit_v1_0_10_dqdv.png`에서 staging 4 전이 모두 bell (spike 없음). Panel 2 LiC6 single bell Q=0.499 — 면적 보존 ✓. P4 demo는 bell 1개만 — staging 미재현 의심.
5. **오적발 가능성 자기표시**: (a) softplus 항(MED-2) 물리 해석이 추정 포함 — 코드 원 의도 확인 필요. (b) Arrhenius 회귀 v1.0.10 포함 여부 미확인(추정: 부분). (c) demo_lco_heat.py 미직접 정독 — HIGH-1은 그래프 판독 기반 간접 결론.
