# REVIEW2 — v8-04b 검토2 (체리픽 강후보·엄격)

대상: `Claude/results/v8-04/v8-04b.tex` (1183행, v8-04.tex 의 정정 4건 증분판)
기준: `v7-00_spine/Anode_Fit_v11_final.py`(706줄)·`v7-11/v7-11.tex`(879행)·`v8-00_spine/AUTHOR_BRIEF_v8.md`
방식: 식·유도 단위 청크 전문 정독(1183행 전수) + 직접 수치 검산(Python) + 적대 sub 2 (refute·빈통과금지) 삼각검증
Read coverage: v8-04b 전 1183행 / v8-04.tex 비교 영역(L404-462, L895-929) / py L100-130·L455-484 / v7-11 L404-431.

---

## ① 보완 4건 반영 검증 (★D-PEAK 수학 직접 검산 포함)

### (1) ★D-PEAK 정정 (N8, L924-932) — **CORRECT (코드·수학 직접 검산 통과)**
원본 v8-04.tex L905-907 결함: "작은 L_V → ρ=e^{−Δgrid/L_V}→0 → ξ_lag→**한 칸 뒤처진** ξ_eq → 이산미분 → 평형 종으로 **환원**".
- 점화식(eq:lowpass) `ξ_lag,i = ρ·ξ_lag,i−1 + (1−ρ)·ξ_eq,i`. **ρ→0 직접 검산**: `ξ_lag,i = 0·ξ_lag,i−1 + 1·ξ_eq,i = ξ_eq,i` = **같은 칸**(한 칸 뒤가 아님). 따라서 `(ξ_eq−ξ_lag)/L_V → 0/L_V = 0` (퇴화, peak 소멸). 원본의 "한 칸 뒤처짐"·"환원" 둘 다 거짓.
- **코드 1:1 대조** (py L114-117 스칼라 fallback): `lagged[i]=decay·lagged[i−1]+(1−decay)·source[i]`, decay→0 시 `lagged[i]=source[i]` 동일칸. lfilter 경로(L108-111, zi=decay·src[0])도 `lagged[0]=src[0]` 로 일치.
- **환원 담당 = 명시 분기 스위치** (py L466 `if lag_len_V < min_lag_grid_steps*grid_step: peak_shape = ksi_eq*(1−ksi_eq)/w`). 저역통과 ρ→0 극한이 **아님**.
- v8-04b 정정문(L924-932)이 위를 정확히 진술: 큰 L_V(ρ→1)=매끄러운 저역통과→이산미분→평형 종 접근 / 작은 L_V(ρ→0)=같은 칸으로 퇴화(0/L_V) / 환원은 명시 분기 스위치 담당. **수학·코드 양쪽 정합. 정정 완료.**

### (2) fig:overshoot 정정 — **3항 모두 CORRECT**
- **\eqref 식번호**(L447): 원본 하드코딩 `Eq.~(1.18)$=$(1.16)` → `Eq.~\eqref{eq:Veq}\,⇒\,Eq.~\eqref{eq:gpp}`. fig 블록(L431-459) 전수 스캔: 잔존 하드코딩 식번호 0(숫자는 전부 좌표/spinodal 값). 캡션도 \eqref/\ref 만.
- **분기 라벨 상하 정정**(L448-450): 원본 "rising(delithiation)"@(0.30,**−0.55**)·"falling(lithiation)"@(0.70,**+0.55**) = fig:hysloop 규약과 **상하 반전**(방전=상단 max 인데 하단에 배치). 정정판 = "rising(delithiation)"@(0.34,**+0.70**)=상단 max 로브, "falling(lithiation)"@(0.66,**−0.70**)=하단 min 로브. **fig:hysloop(L558-569: 방전 좌상 max xi_s^−, 충전 우하 min xi_s^+)·본문 prose(L427-428)와 정합.**
- **곡선 차별화 Ω=3RT**(L433-440): 원본 Ω=4RT(0.1464/0.8536) → Ω=3RT(0.2113/0.7887). **17개 좌표 전부 `g'(ξ)/RT=ln[ξ/(1−ξ)]+3(1−2ξ)` 로 직접 검산 — 오차 ≤±0.0005**(반올림 수준). 단순 복사가 아니라 실제 재계산. extrema ±0.415 정확. fig:hysloop(Ω=4RT)와의 중복(브리프 §5 후보경쟁 맥락) 해소, fig:doublewell(Ω=3RT)과 spinodal 공유.

### (3) eq:Veq inline 다리(eq:isotherm 추가, L416-424) — **CORRECT (cosmetic 흠 1)**
- eq:isotherm(L416-418)·eq:Veq(L421-423)는 **독립 라벨 2식**, 사이에 다리 prose(L420). g'(ξ)(L412-414)=`RT ln[ξ/(1−ξ)]+Ω(1−2ξ)` = eq:isotherm RHS 동일(순환 아님). 대수(÷sF→U_j 이항→전개)가 eq:Veq 정확 재현. "대입하면 박스" 점프 해소(브리프 §3 G-derive 충족).
- cosmetic(LOW): L420 "U_j 좌변으로 이항해 우변으로 옮김"은 자기모순 표현, "sF로 나누고…각각 sF로 나누면" 중복 진술. 결과는 정확.

### (4) orphan bib 정정 — **CORRECT (잔여 orphan 0)**
- \cite 전수: bloom2005+dubarry2012(L100)·dahn1991+ohzuku1993(L101)·dreyer2010(L376, "히스테리시스 열역학적 기원" 정맥락)·bazant2013(L382, "비평형 열역학 기반 반응속도론" 정맥락)·eyring1935(L608). **7개 bibitem 전부 본문 인용 ≥1. orphan 0.**

---

## ② ★신규 회귀 검증 (곡선 차별화가 doublewell/hysloop 정합 깼나)

- **fig:doublewell(Ω=3RT, L524-549)**: g(ξ)/RT 25개 좌표 직접 검산(`xi ln xi+(1−xi)ln(1−xi)+3 xi(1−xi)`, g0 상수 drop) — **오차 ≤±0.0001**. spinodal 0.2113/0.7887 일치. v8-04 에서 이미 Ω=3RT 였고 **무변경** → fig:overshoot 가 Ω=3RT 로 와서 **두 그림이 같은 spinodal 공유**(내부 정합 ↑, 회귀 아님).
- **fig:hysloop(Ω=4RT, L551-577)**: v7-11 에서 **verbatim 보존**(좌표·라벨·구조 동일). overshoot 캡션(L454-456)이 hysloop 을 "Ω=4RT, 과주행이 더 깊은 정성적 예"로 명시 — 두 Ω 의 의도적 분리를 캡션이 정확히 해설. 회귀 0.
- **부호 8항(S1-S8)·self-test 4항(R1-R4)**: 차별화와 무관(Ω 수치 예시 불변). R1 직접 검산 u=0.766·ΔU_hys=86.7 mV / R2 2RT=4958 J/mol / RT/F=25.7 mV 전부 정확. 회귀 0.
- **상호참조 무결성**: 8 figure·3 table·48 equation·7 bibitem 전부 label↔ref 정합, dangling/orphan ref 0. 환경 begin/end 17종 전부 균형. **신규 회귀 0건.**

---

## ③ 재점수 /35 (7차원 × 5점)

| 차원 | 점수 | 근거 |
|---|---|---|
| 유도 완결성(G-derive) | 5 | eq:isotherm 다리로 eq:Veq 점프 해소, D-PEAK 두 극한 정확 분리. 브리프 §3 충족 |
| 수식 정확성 | 5 | D-PEAK ρ-극한 코드 검산 통과·fig 17+25 좌표 직접 검산·R1/R2 수치 정확 |
| 코드 정합 | 5 | py L114-117·L466 분기·func_* 1:1. 환원=명시 스위치 정확 반영 |
| 부호 사슬 | 5 | S1-S8·R1-R4 기준명제 정합, 회귀 0 |
| 그림(완결·정합) | 4 | 라벨 상하·Ω 차별화·\eqref 정정 모두 통과. −1: overshoot "rising" 라벨 x=0.34 가 apex 직후 하강부 위(로브는 정확, x 배치 미세 흠) |
| G-follow/G-usable | 5 | 6단계 재현 박스·nodemap·inputs 표 완비, 다리 prose 추가로 추적성 ↑ |
| 완결성·빌드 | 4 | 환경 균형·참조 무결. −1: xelatex 부재로 실 PDF 빌드 미검(환경 한계, 결함 아님) |
| **합계** | **33/35** | 정정 4건 전부 검증 통과, 신규 회귀 0 |

(v8-04 대비: D-PEAK 결함(−2급)·fig 라벨 반전(−1급)·하드코딩 식번호·orphan bib 해소 → 약 +4~5 상승)

---

## ④ 부호 8항 (S1-S8, 기준명제: 방전 V↑⇒탈리튬화↑, 충전 dQ/dV=방전 거울 양수)

| | 항목 | 식 | 판정 |
|---|---|---|---|
| S1 | U_j=(−ΔH+TΔS)/F, ΔG=−FU | eq:Uj·eq:eqcond | ✓ ΔH<0→중심↑ |
| S2 | ξ_eq=logistic[σ_d(V−U)/w] | eq:xieq | ✓ 방전 V↑→ξ↑ |
| S3 | dξ/dV=σ_d ξ(1−ξ)/w, peak 양수 | eq:dxidV·eq:eqpeak | ✓ |dξ/dV| 방향불변 |
| S4 | ΔU_hys≥0, Ω≤2RT→0, 분기 ±½σ_d | eq:dUhys·eq:Ubranch | ✓ U^dis>U^chg |
| S5 | χ_d 충전 1−χ, ΔH_a^eff=ΔH_a−χ_dΩ | eq:chid·eq:dHeff | ✓ 합-1 거울 |
| S6 | ∂lnL_q/∂V: 컷상수라 운영 0, 부등식=동기 | eq:lnLq·eq:LV | ✓ 자기모순 0 |
| S7 | 꼬리 충전 격자역전, 충전 dQ/dV 방전 거울 양수 | eq:reversal | ✓ py L477 [::-1]…[::-1] 정합 |
| S8 | 분극 V_n=V_app−σ_d|I|R_n | eq:vn | ✓ 방전 측정>내부 |

**부호 결함 0.** self-test R1-R4(L1154-1167) 수치 전부 재산출 통과(R1 86.7mV·R2 0.0mV·R3 |I|→0 환원·R4 동결 vs 부등식).

---

## ⑤ 체리픽 적합도 + 잔여

**적합도: 강후보 (33/35).** 보완 4건이 전부 실질·정확하게 반영됐고(특히 D-PEAK 는 수학·코드 양면 검산 통과), 신규 회귀 0. v8-04b 는 v8-04 의 알려진 결함 4건을 모두 닫은 상위 버전 — v8-04 대신 채택 가능.

**잔여(전부 LOW, 채택 차단 아님):**
1. (LOW) fig:overshoot "rising branch" 라벨 x=0.34 가 max apex(0.2113) 직후 하강 구간 위 — 로브(상단 양수)는 정확하나 x 위치가 약간 apex 뒤. 대칭 라벨(falling@0.66)은 깔끔. 미세 가독 흠.
2. (LOW) eq:Veq 다리 prose L420 자기모순 표현("좌변 이항…우변 옮김")·중복 진술. 결과식은 정확.
3. (LOW) eq:isotherm→sec:width forward-ref: sec:width 의 detailed balance(eq:stationary L639)는 **이상혼합(Ω=0)** 만 명시 유도, Ω 항은 w^eff(L596-599)로 따로 처리. "g'(ξ)=sF(V_eq−U)" 의 비이상 일반화는 정당하나 참조 도착지에서 재유도 아닌 **단언**. 한 절(비이상에서 A 가 Ω(1−2ξ) 흡수) 보완하면 닫힘.
4. (LOW·환경) xelatex 부재로 실 PDF 빌드 미검 — 구문(환경 균형·참조 무결)은 정적 통과.

**결함 미발견(확정 PASS):** D-PEAK 수학·orphan bib·fig Ω 좌표·부호 8항·self-test 4항·상호참조·환경 균형.
