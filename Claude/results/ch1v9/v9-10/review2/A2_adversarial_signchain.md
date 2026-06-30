# A2 Adversarial 검수 — 부호 사슬 · 흑연 보존 · graft 정합 회의자

- **대상**: `Claude/results/ch1v9/v9-10/v9-10.tex` (체리픽본, 1608줄)
- **비교 원본**: `Claude/results/ch1v9/v9-00_spine/base_v8-11.tex` (흑연 원본, 1208줄, md5 `ff5cee5a…`)
- **방법**: `diff -u` byte-level 대조(전수) + 부호 사슬 손-검산(반증 시도) + ref/cite 정합 스크립트(PowerShell 정규식)
- **역할**: 반증 시도자(흑연 VERBATIM·부호 사슬·graft 봉합·단/전셀 분리)

---

## ★ 핵심 결론 (반환 요약 박스)

| 표적 | 판정 | 근거 |
|---|---|---|
| ① 흑연 VERBATIM 보존 | **PASS (byte-동일)** | diff 상 흑연 본문 lines 제거 0, 순수 삽입 12 hunk, 헤더 4줄만 1:1 치환 |
| ② 부호 사슬 전수 정합 | **PASS** | 흑연 anchor(eq:eqcond·Uj·xieq·db) 와 LCO 삽입(eq:lco-dUdT·fermifn·dSe·dSegate) 1:1, 봉합 join 부호 무모순 |
| ③ graft 봉합 | **PASS (LOW 1건)** | dangling ref 0·dangling cite 0·orphan eq-label 0; MSMR `f`↔`−σ_d` 명시 생략(LOW) |
| ④ 단/전셀 분리 | **PASS** | 전셀 혼동 명시 차단, 하프셀 단독 범위 유지 |

---

## 표적 ① — 흑연 VERBATIM 보존 (★diff 기반)

**PASS / 흑연 영역 byte-동일.** `diff -u base v9-10` 전수 결과:

- **라인 수 정합**: base 1208 → v9-10 1608, 정확히 **+400줄**. 이 400은 12개 삽입 hunk의 `+`줄 합과 일치(누락·이중계산 없음).
- **흑연 본문에서 제거된 줄 = 0.** diff `-`줄(`---` 제외)은 **단 4줄**이며 전부 헤더/라벨이고 모두 1:1 치환(line-balanced):
  1. `pdftitle={… (v8)}` → `… + LCO 양극 … (v9)}`
  2. `\lhead{… (v8 …)}` → `… + LCO 양극 … (v9 …)}`
  3. `\title{… 흑연 음극 dQ/dV …}` → `… 흑연 음극 + LCO 양극 dQ/dV …}`
  4. `\begin{thebibliography}{9}` → `{99}` (라벨 폭만 9→99, 흑연 bibitem 7건 전부 보존)
- **graft가 흑연 영역 침범 안 함**: 모든 LCO 추가는 흑연 절·식 **사이에 순수 insert**(@@ −264,+56 / −384,+39 / −557,+30 / −696,+50 / −723,+177 / −759,+18 / −1056,+57 / −1136,+12 / −1203,+15). 흑연 절 내부를 가르고 들어간 in-place 치환 없음.

**흑연 정본 요소 보존 확인(diff-untouched 영역, lines 1372–1586):**

- **흑연 ΔS/U 표(tab:staging, line 1381–1384)**: `4→3` U=0.210 ΔH=−11700 **ΔS=+29.0**; `3→2L` 0.140 −13500 **0.0**; `2L→2` 0.120 −13100 **−5.0**; `2→1` 0.085 −13000 **−16.0**. 표적 명세(U 0.210/0.140/0.120/0.085·ΔS +29/0/−5/−16)와 **완전 일치, 훼손 0**.
- **부호 검산 S1–S8(sec:signcheck, line 1535–1559)**: 8항 전건 `✓`, "부호 결함 0" 선언. 모두 base와 byte-동일.
- **자가검증 R1–R5(verifybox, line 1561–1586)**: 5항(히스 분기 +86.7 mV·문턱 0·|I|→0 환원·Lq 동결·D-PEAK 회귀) 전부 보존, "self-test PASS".
- **그림 9개**: spine·staging·doublewell·hysloop·barrier·flux·logistic·reversal·relaxode — 흑연 9 fig 모두 diff-untouched(새 fig:lco-electronic은 +1 추가일 뿐 흑연 fig 대체 아님).
- **코드 대응 박스(codebox/func_U_j 등)**: 훼손 흔적 없음.

> **흑연 보존 PASS — diff로 확정.** 흑연 식·부호·표·코드·그림은 base 대비 byte 단위로 불변이며, v9는 흑연 위에 LCO를 *순수 첨가*한 것이다.

---

## 표적 ② — 부호 사슬 전수 (반증 시도)

흑연 anchor와 LCO 삽입을 1:1 대조하여 **반증 시도**. 결과: 사슬 무모순.

**(a) ∂U_j/∂T 관계 — 흑연↔LCO 1:1**
- 흑연 eq:Uj 미분(line 425): `∂U_j/∂T = ΔS_rxn,j/F`.
- LCO eq:lco-dUdT(line 446): `∂U_j/∂T = ΔS_rxn,j^cat/F`, 명시적으로 "식 eq:Uj의 T 미분, 전극 불문".
- **판정**: 동일 관계식, 부호까지 일치. 첨자 `^cat`만 추가 — 충돌 없음. ✓

**(b) eq:eqcond 합류 — Δμ 부호 정합 (★graft 봉합 핵심 join)**
- 흑연 eq:eqcond(line 401): `μ_Li = μ⁰ − sF(V−U)`, `ΔG_j = −sFU_j`, s=+1.
- LCO dist절 eq:fermifn(line 824): `⟨n⟩ = 1/(1+e^{+βΔμ})`, 대입 `Δμ = −sF(V−U_j)` (line 829, "eq:eqcond를 단일 자리 점유에 적용") → `⟨n⟩ = 1/(1+e^{−s(V−U_j)/w_j})`.
- 이는 흑연 eq:logisticsolve/eq:xieq(line 717·723) `ξ_eq = 1/(1+e^{−σ_d(V−U)/w})` 와 **항등 일치**.
- **반증 시도**: grand-canonical Δμ 정의가 흑연 eq:eqcond와 부호 반대였다면 logistic이 뒤집혀야 함 → 확인 결과 `Δμ = −sF(V−U)`로 **정확히 정합**, s=σ_d=+1로 흑연 logistic 재현. **사슬 안 깨짐.** ✓

**(c) LCO 양극 부호 — 흑연과 모순 없이 합류**
- 양극 부호 규약(line 276): 방전 σ_d=+1 = LCO 리튬화(x↑·전위 하강), 충전 σ_d=−1 = 탈리튬화(x↑ 진행). 흑연 "V↑⇒탈리튬화"와 *골격 동일, 값만 다름*(전위 ~3.9–4.2 V 높음).
- **반증 시도(T1 부호 공존)**: 같은 T1 전이에 두 부호 주장 공존 —
  - LCO center verifybox(line 458–460): 대표 `ΔS_rxn^cat ≈ +80 J/(mol·K) > 0` (dφ/dT≈+0.83 mV/K).
  - 전자항(line 945–949): `ΔS_e,j < 0` (삽입 기준, MIT 음의 골).
  - **모순인가?** 아님. eq:lco-decomp(line ~1396): `ΔS_rxn^cat = config + vib + electronic`. 전자항은 `|ΔS_e|≈0.18 k_B/atom ≈ 1.5 J/mol·K` 규모(line 943·946)로 config 주도 양수 총합(+80 대표 스케일)을 **뒤집지 못하는 작은 음의 보정**. 문서가 +80을 "tier B 대표 스케일·x 의존·전이별 정밀값 아님"(line 942)으로, ΔS_e를 "작지만 게이트라 필수"(line 339)로 명시. **공존 내부 정합.** ✓

**(d) ΔS_e 부호 유도 자기일관**
- eq:dSe(line 926): `ΔS_e,j ≡ ∂S_e/∂x = (π²/3)k_B²T·∂g/∂x` (<0 at MIT, 삽입 기준).
- 닫는 논리(line 944–945): 삽입(x↑)→금속→절연체→`g(E_F): g_max→0` 감소→`∂g/∂x<0`→`ΔS_e<0`. eq:dSegate(line ~1090)의 leading `−`부호가 이를 식 자체로 못박음.
- 흑연 `ΔS_rxn=−16<0` 삽입 음수 슬롯과 **부호 규약 일관**(둘 다 삽입 기준 음수). ✓
- **단위 다리** eq:dSemolar: `N_A k_B² = R k_B`, 자리당→몰당, "부호는 환산 불변(N_A>0)" — 차원·부호 모두 정합. ✓

> **부호 사슬 PASS.** 흑연 8/8 검산이 byte-보존된 채, LCO 4개 신규 부호 주장이 모두 흑연 anchor에 무모순으로 합류. 반증 시도(T1 ±부호 공존·Δμ join·logistic 재현)에서 깨지는 곳 없음.

---

## 표적 ③ — graft 봉합 (서로 다른 초안 합성)

**스크립트 검증(PowerShell 정규식, 전수):**
- labels 92 / refs 79 / cites 15 / bibitems 15.
- **Dangling ref(정의 없는 참조) = 0.** (`\eqref`/`\ref` 79개 전부 label로 해소; `LastPage`는 hyperref 내장.)
- **Dangling cite(bibitem 없는 인용) = 0.** 신규 LCO cite 8건(reimers1992·menetrier1999·motohashi2009·xia2007·reynier2004·swiderska2019·msmr2024·ml2024) 모두 bibitem 존재.
- **Unused bibitem = 0.** 흑연 7 + LCO 8 = 15건 전부 인용됨.
- **Orphan eq-label = 0.** 신규 식 라벨(eq:Se·dSe·dSegate·dSemolar·fd·ggate·partfn·fermifn·msmr·lco-decomp·lco-dUdT) 전부 본문 참조됨.

**표기 일관(σ_d·ξ·w·Ω):** LCO 절들이 흑연 매크로(`\sigma_d`·`\xi`·`w_j`·`\Omega_j`·`\code{}`)를 그대로 재사용. 신규 기호 충돌 없음(`g(E_F)`·`x_MIT`·`Δx_MIT`·`ΔS_e`는 흑연에 없던 자리라 충돌 불가). 전이 인덱스 `j`·진행률 `ξ_j` 흑연과 공유.

**[LOW-1] MSMR 방향 인자 `f`↔`−σ_d` 명시 생략.** eq:msmr `x_j = X_j/(1+exp[f(U−U_j^0)/ω_j])`를 흑연 eq:xieq `ξ=1/(1+exp[−σ_d(V−U_j^d)/w_j])`와 "구조 동형"으로 매핑(X_j↔Q_j·U_j^0↔U_j^d·ω_j↔w_j)하나, 부호 인자 `f ↔ −σ_d` 대응만 명시 안 됨. *구조 isomorphism* 주장이라 결함은 아니나, 부호 사슬 엄밀성 기준에선 한 줄 보강 여지(severity LOW, 봉합 깨짐 아님). — 유일하게 발견된 graft-seam 미세 흠.

**서론/spine 그림(fig:spine):** v9에서 pdftitle·lhead·title만 "+ LCO 양극"으로 갱신, spine 그림 노드(N0–N9)는 base와 byte-동일. 즉 spine은 여전히 흑연 9-노드 — LCO가 별도 절로 첨가되고 spine 그림 자체엔 LCO 노드 미반영(tab:nodemap에는 "LCO 추가" 행 4개 삽입됨, line 1525–1528). spine 그림 미갱신은 의도된 보존(흑연 정본 불가침)으로 해석 가능, 결함 아님.

> **graft 봉합 PASS (LOW 1).** 서로 다른 초안(v9-06 base + v9-04/03/05/02 graft)에서 온 절·식이 기호·번호·참조 충돌 0으로 봉합. 끊긴 참조·중복 정의·orphan 없음.

---

## 표적 ④ — 단/전셀 분리

**PASS.** 전셀 합성이 끼어든 흔적 없음, 하프셀 단독 범위 명시 유지:
- sec:lco-map(line 271–273): "본 문건 범위 = **코인 하프셀(LCO vs Li metal) 단독** … 전셀 합성(∂U_cell=∂U_cat−∂U_an)은 **범위 밖**(후속) … 단전극 부호와 전셀 부호를 섞지 않는다."
- LCO center verifybox(line 462–464, ★단전극 대 전셀 혼동 금지): "+0.83 mV/K는 **LCO 단일전극**(vs Li) 값 … **전셀**(LCO−graphite) 엔트로피 계수는 SOC 따라 부호 전환(−0.37~+0.1 mV/K)이며 흑연 항 합산된 다른 양 … 본 문건은 하프셀 범위라 단전극 LCO 부호만 쓴다."
- **반증 시도**: 전셀 부호(−0.37~+0.1 mV/K)가 단전극 계산에 잘못 합성됐나? → 확인 결과 명시적으로 *격리*되어 인용되며 계산에는 단전극 +0.83만 사용. 혼입 없음. ✓

---

## 결함표

| # | 식별자/위치 | 심각도 | 반증 근거 | 정정 |
|---|---|---|---|---|
| L1 | eq:msmr ↔ eq:xieq 동형(line ~1429–1433) | LOW | 방향 인자 `f ↔ −σ_d` 대응이 명시 안 됨(X·U·ω 3쌍만 명시); *구조* 동형 주장이라 봉합은 안 깨지나 부호 엄밀성 한 줄 부족 | "`f`는 MSMR의 외부 방향 부호로 `−σ_d`에 대응" 한 구절 추가 권고(비차단) |

CRIT/HIGH/MED **0건**. LOW 1건(graft-seam 미세 표기, 비차단).

---

## 가장 약한 1곳 (refute 1급 표적)

**T1(MIT) 전이의 부호 공존 — `ΔS_rxn^cat ≈ +80 > 0` (center verifybox) vs `ΔS_e < 0` (전자항).** 같은 전이에 양·음 두 ΔS 주장이 공존해 표면상 가장 모순처럼 보이는 지점. 정밀 검산 결과: eq:lco-decomp의 합 분해(config+vib+electronic)에서 전자항은 ~1.5 J/mol·K 규모의 *작은 음의 골*이고 총합은 config 주도 양수라 **부호 뒤집힘 없음** — 문서가 +80을 "대표 스케일·정밀값 아님", ΔS_e를 "작지만 게이트라 필수"로 이중 단서를 달아 내부 정합을 유지. **반증 실패(= 문서가 견딤).** 다만 독자가 "+80과 −는 모순"으로 오독할 여지가 사슬 중 최대이므로, decomp 절에서 "전자항은 총 ΔS_rxn^cat의 부호를 바꾸지 않는 소수 보정"을 한 줄 더 못박으면 G-usable 향상(권고, 비차단).
