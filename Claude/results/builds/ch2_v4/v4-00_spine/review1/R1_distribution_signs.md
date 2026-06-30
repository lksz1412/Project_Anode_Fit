# R1 — 분포 유도(G-derive) + 부호 규약 전담 검토 (Ch2 v4, 9빌드)

> 검토1 R1 (검수 sub). 렌즈: ★위험1(config 부호)·위험2(ξ/θ)·위험4(μ(V) logistic)·위험5(단위다리) + G-derive 점프.
> 방법: master 직접 grep 전수(config 인자·logistic) + 3 sub-agent 전문 정독(파일당 3종) 삼각검증. 9종 모두 head→tail full read coverage.
> Ground truth: `41_statmech_spine.md`·`40_mixing_term_design.md`·`42_numerical_verification.md`·`REVIEW_RISK_PATTERNS.md`.
> **★주의**: spine 설계 doc(`41` line 27)의 박스 총엔트로피식 자체가 역수 `ln[(1-ξ)/ξ]`로 오기됨 → 일부 빌드가 상속. 정답 = `+(R/F)·ln[ξ/(1-ξ)]`, ξ=탈리튬화 진행률, ξ→1(희박 Li-poor)→**+∞**, ξ→0(만충)→−∞.

---

## (a) 9종 PASS/FAIL 표

| 빌드 | config 부호 (위험1) | ξ/θ 규약 (위험2) | μ(V) logistic (위험4) | 단위다리 N_A (위험5) | G-derive 점프 | LaTeX 무결성 | 종합 |
|---|---|---|---|---|---|---|---|
| **v4-01** | **PASS** 전식 `ξ/(1-ξ)` 일관 | PASS (θ→ξ 치환 무명시, MED) | PASS | PASS (w=RT/F, N_A 암시) | 2 (MED: 선두차수·V(ξ) 미반전) | OK | **PASS** |
| **v4-02** | **FAIL ★CRIT** L319 박스 `(1-ξ)/ξ` 역수 (L265·537·z_j와 모순) | PASS 규약 (역수가 결함 경로) | PASS | PASS | 2 (MED) | L319/408/413 역수 | **FAIL** |
| **v4-03** | **PASS** 전식 `ξ/(1-ξ)` 일관 (역수 트랩 선제 차단) | **PASS (최상·명시)** | PASS (eq2.5 σ_d 생략 MED) | **PASS (명시 N_A 라인)** | 1–2 (최소·⟨n⟩ 완전유도) | OK | **PASS** |
| **v4-04** | **FAIL ★CRIT** L473·605·793 박스 `(1-ξ)/ξ` 역수 (극한표 L705와 모순) | PASS 규약이나 L388 "상쇄" 말로 때움 | **FAIL ★CRIT** prose +σ_d(L181) vs 박스 −σ_d(L184) 반대 (C1) | PASS (k_BT/e=RT/F) | 3 (μ(V)·S_vib·S_el) | 역수 3곳 | **FAIL (2 CRIT)** |
| **v4-05** | **PASS** 전식 `ξ/(1-ξ)` 일관 | **PASS (명시 치환)** | PASS (θ_eq·ξ_eq 둘 다) | **PASS (N_A 명시 L147)** | 2 (LOW: S_vib·S_e 인용) | OK | **PASS** |
| **v4-06** | **PASS** 전식 `ξ/(1-ξ)` 일관 | **PASS (명시 치환)** | PASS (+σ_d 일관) | **PASS (N_A 명시 L137)** | 2 (LOW: S_vib·S_el 인용) | OK (ξ_eq glyph 재사용 LOW) | **PASS** |
| **v4-07** | **PASS** 전식 `ξ/(1-ξ)` 일관 | **PASS (명시 θ=1-ξ 치환)** | PASS (−σ_j 일관) | **PASS (명시 k_B N_A=R L230)** | **0 (W/Stirling 완전유도)** | OK | **PASS (최상)** |
| **v4-08** | **FAIL ★CRIT** L199-202 박스 `+` 누락(합→곱) + L143 역수 `(1-ξ)/ξ` | **FAIL (말로 때움 L159-163)** | PASS | **FAIL (silent N_A)** | 1 (p₀,p₁·W/Stirling 생략) | `+` 누락 1식 | **FAIL** |
| **v4-09** | **FAIL ★CRIT** L249·315-317·370 박스 `+` 3곳 누락(합→곱) | PASS (좌표 재정의, 일관) | PASS (σ_d 명시) | **FAIL (silent N_A)** | 0 (W/Stirling 생략 LOW) | `+` 누락 3식 | **FAIL** |

**config 부호 PASS 초안 (개념·인자 정답)**: v4-01·v4-03·v4-05·v4-06·v4-07 (5종). 이 중 LaTeX·μ(V)·ξ/θ 까지 전부 깨끗 = **v4-03·v4-05·v4-06·v4-07** (v4-01은 PASS이나 θ→ξ 치환 무명시 MED).
**개념상 인자는 정답이나 LaTeX `+` 누락으로 FAIL**: v4-08·v4-09 (역수가 아니라 식별자 사이 연산자 탈락 — 합이 곱으로 렌더).
**진성 역수(위험1 상속) FAIL**: v4-02(L319)·v4-04(L473/605/793).

---

## (b) ★분포 유도 best 랭킹 + 체리픽 추천

분포 유도 G-derive 품질 + 부호 4렌즈 전부 통과 기준 랭킹:

1. **v4-07 (BEST·체리픽 base 추천)** — config·ξ/θ·μ(V)·단위다리 **4렌즈 전부 PASS, G-derive 점프 0**. 유일하게 S_config 를 다중도 W→Stirling→k_B N_A=R 로 *완전 유도*(나머지는 Boltzmann-Shannon 단정). θ=1−ξ 명시 대수 치환(L240-244), 박스 logistic Ch1 형 −σ_j(V−U)/w 일관, **유일 명시 N_A 단위다리(L230)**. 745줄 최장·전 섹션 완비, LaTeX 무결. 결함 = 미인용 bib 4건(LOW)뿐.
2. **v4-05 / v4-06 (공동 2위)** — 둘 다 4렌즈 PASS, config 전식 `ξ/(1-ξ)` 일관, **N_A 명시**(v4-05 L147 R=N_A k_B·F=N_A e / v4-06 L137). v4-05는 θ_eq·ξ_eq 두 logistic 명시+가장 상세, v4-06은 ⟨n⟩=∂lnZ/∂μ 로그미분·전용 §부호규약. S_vib·S_e 만 인용(점프 2, LOW). v4-06 ξ_eq glyph 재사용(LOW). **v4-07 부적격 시 대체 base.**
3. **v4-03 (3위)** — config·ξ/θ·단위다리 PASS(**명시 N_A 라인** L340-341 g_mol). ⟨n⟩ derivebox 완전유도. 단 eq2.5 logistic 지수 σ_d 생략·ξ를 점유⟨n⟩와 탈리튬화에 이중 사용(MED 봉합). 역수 트랩을 본문서 선제 차단(L246-247)한 유일 빌드.
4. **v4-01 (4위)** — config 전식 일관 PASS이나 θ→ξ 치환 1줄 무명시(MED)·V(ξ) Ch1서 단정(미반전).

**체리픽 권고**: **base = v4-07** (분포 유도·부호·단위다리·LaTeX 전부 최상). 보완 소스: 수치검증 round-trip 표가 필요하면 **v4-09 §2.4.2 표**(가장 구체적 mV/K), ξ/θ 명시 치환 문구가 더 풍부한 곳은 **v4-05 L233 / v4-06 L259**(`−R ln[θ/(1-θ)]|_{θ=1-ξ}=+R ln[ξ/(1-ξ)]` 완전 대수). v4-04·v4-02 는 config-부호 CRITICAL 보유 → **base 부적격**.

---

## (c) 결함표 (초안·식별자·심각도·정정)

### CRITICAL (체리픽 전 반드시 교정)

| 빌드 | 식별자 | 줄 | 심각도 | 잘못된 텍스트 (verbatim) | 정정 |
|---|---|---|---|---|---|
| v4-02 | eq:Stotal (박스 총ΔS) | 319 | CRIT | `+\underbrace{R\ln\frac{1-\xi}{\xi}}_{config(분포)}` | `+R\ln\frac{\xi}{1-\xi}` (L265·537·538·eq2.24 z_j와 일치시킴) |
| v4-02 | 이중계산 prose | 408 | HIGH | `배위 항 R\ln[(1-\xi)/\xi] 이다` | `R\ln[\xi/(1-\xi)]` |
| v4-02 | warnbox | 413 | HIGH | `R\ln[(1-\xi)/\xi] 를 별도로` | `R\ln[\xi/(1-\xi)]` |
| v4-04 | eq:dS_total (박스 총ΔS) | 473 | CRIT | `+\underbrace{R\ln\frac{1-\xi}{\xi}}` | `R\ln\frac{\xi}{1-\xi}` |
| v4-04 | §5B 이중계산 박스 | 605 | CRIT | `+R\ln[(1-\xi)/\xi]` | `R\ln[\xi/(1-\xi)]` |
| v4-04 | Part7 Q_rev 박스 | 793 | CRIT | `+R\ln\tfrac{1-\xi}{\xi}` | `R\ln\tfrac{\xi}{1-\xi}` |
| v4-04 | μ(V) logistic 지수 (C1) | 181 vs 184 | CRIT | prose `+σ_d(V−U)/w` vs 박스 `e^{−σ_d(V−U)/w}` 반대 | ε₀−μ=+σ_d F(V−U), FD형 1/(1+e^{+β(ε₀−μ)}) → 박스 `1/(1+e^{+σ_d(V−U)/w})` 로, 또는 prose 부호 수정 — 둘 일치 |
| v4-08 | eq:decomp (박스 총ΔS) | 199-202 | CRIT | `\Delta S^0_{\rxn,j} R\ln\frac{\xi}{1-\xi} \Delta S_{\vib,j} \Delta S_{\elec,j}` (연산자 전무 → 합이 곱) | `R\ln` 앞·`\Delta S_{\vib,j}` 앞·`\Delta S_{\elec,j}` 앞에 `+` 삽입 |
| v4-09 | eq:config_in_dudt (중간식) | 248-249 | CRIT | `=\frac{\partial U_j}{\partial T} \frac{R}{F}\ln\frac{\xi}{1-\xi}` (`+` 누락 → 연쇄등식 깨짐) | L249 `\frac{R}{F}\ln` 앞 `+` |
| v4-09 | eq:decomp (박스 총ΔS) | 314-317 | CRIT | `\Delta S^0_{\rxn,j} R\ln… \Delta S_{\vib}^{slow} \Delta S_{\el}^{slow}` (연산자 전무) | 세 항 앞 `+` 삽입 |
| v4-09 | eq:overlap_full (박스 완전식) | 369-370 | CRIT | `\left[\Delta S^0_{\rxn,j} Rz_j(x)\right]` (`+` 누락) | `Rz_j(x)` 앞 `+` |

### HIGH / MED (위험2·5 보강)

| 빌드 | 식별자 | 줄 | 심각도 | 내용 | 정정 |
|---|---|---|---|---|---|
| v4-08 | ξ/θ 재조정 | 159-163 | HIGH | "로그 부호가 반대로 보이는 것은 …방향 차이다" — 말로 때움(위험2 정확 위반) | v4-07 L240-244 식 명시 θ=1−ξ 대수 치환으로 교체 |
| v4-08 | eq:partialconfig | 142-144 | MED | `\partial S_config/\partial\xi=R\ln\frac{1-\xi}{\xi}` (역수형이 +ln[ξ/(1-ξ)] 옆에) | 좌표상 수학적으론 OK이나 말 아닌 대수로 봉합, 또는 좌표 각주 |
| v4-08 | 단위다리 | — | MED | `k_B N_A=R` 라인 부재(silent N_A) | per-site→per-mole N_A 명시 1줄 추가 |
| v4-09 | 단위다리 | — | MED | silent N_A | 동상 |
| v4-04 | ξ/θ 상쇄 | 388 | MED | "부호 반전이 정확히 상쇄" 말로 때움 | 명시 치환으로 |
| v4-03 | eq2.5 지수 σ_d 생략·ξ 이중역할 | 142 vs 241 | MED | ξ=점유⟨n⟩(eq2.5) vs ξ=탈리튬화(V(ξ)) | σ_d형 정렬 또는 역할전환 1줄 명시 |
| v4-01 | θ→ξ 치환·V(ξ) 미반전 | 229→240 | MED | θ-form↔ξ-form 사이 θ=1−ξ 1줄·V(ξ) 역산 무명시 | 1줄 추가 |
| v4-01/02/03 | 선두차수 ∂ξ/∂T | 364/352/412 | MED | `≈−g_j ΔS/F` 단정 | chain rule 명시 |

### 공통 LOW (전 빌드, 위험 외)

- 모든 빌드: S_vib(Bose-Einstein 단일모드)·S_e(Sommerfeld FD)는 분포서 *인용*(닫힌형만), 적분 전개 생략 — 교과서 표준 단축, 허용. 단 **config 사슬 Z₁→⟨n⟩→S_config→부분몰은 전 빌드 완전 전개**. 예외: v4-07만 S_config 까지 W/Stirling 완전 유도(나머지 단정).

---

## 핵심 결론

1. **진성 config-부호 역수(위험1 상속) = v4-02·v4-04 둘뿐** — spine doc `41` L27 의 `(1-ξ)/ξ` 오기를 박스 총엔트로피식에 상속. 둘 다 *자기 모순*(같은 파일 ∂V/∂T·극한표는 정답 `ξ/(1-ξ)`). v4-04는 추가로 μ(V) 지수 반대(C1) — **2 CRITICAL, base 부적격**.
2. **v4-08·v4-09 는 개념상 인자 정답이나 박스식 `+` 연산자 탈락**(합이 곱으로 렌더) — 기계적 LaTeX 결함이나 챕터 중심식 손상. v4-09 3곳·v4-08 1곳.
3. **부호 4렌즈 + LaTeX 전부 PASS = v4-03·v4-05·v4-06·v4-07** (v4-01 PASS이나 MED 봉합). **v4-07 이 G-derive 점프 0·N_A 명시·W/Stirling 완전유도로 단독 최상 → 체리픽 base 추천.**
4. ξ/θ 명시 대수 치환(위험2 정답)은 **v4-05·v4-06·v4-07** 가 모범, **v4-08 만 진성 FAIL(말로 때움)**, v4-04 일부 때움(MED).

*검토자: R1 (master grep 전수 + 3 sub-agent 전문 정독 삼각검증). 파일 수정 없음 — 검토 의견 only.*
