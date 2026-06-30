# A1 adversarial review — broadening 절 · w 이중지위 (v10-10)

> 역할: adversarial A1 = broadening 물리 회의자(검수 sub). 대상 = `Claude/results/builds/ch1v10/v10-10/v10-10.tex` §sec:broadening(L1137–1272)·§sec:width 이중지위(L691–717)·LCO peak(L1123–1135).
> Ground truth: `results/research/broadening_w_design.md`(정정 설계)·`results/research/radius/ORIGIN_VERDICT.md`·`.../radius/43_structural_disorder_heterogeneity.md`(Dahn 카드).
> 판정: **반증 성공 — CRIT 1 + HIGH 2 + MED 2.** 파일 수정·commit 안 함.

---

## 결함표

| # | 식별자·위치 | 심각도 | 결함 | 반증근거 | 정정안 |
|---|---|---|---|---|---|
| D1 | ③ 정의(L1172–1177) ↔ (c) 경고(L1194·L1218–1219)·keybox(L1234) | **CRITICAL** | **ρ(U_j) 정의가 (c) 경고와 자기모순.** ③은 "입자마다 전이 전위·유효 배리어가 **분포 $\rho(U_j)$** 를 이룬다"(L1174–1176)·eq:ensavg 가 "중심 $U_j$ 가 분포한 앙상블 위로 forward 합성"(L1184). 그런데 (c)는 "평형 중심 $\bar U_j$ 는 GITT 입자 무관 **상수**…분포하는 것은 그 **중심이 아니라** 앙상블 폭 ρ와 η"(L1194·1218–1219), keybox 도 "단일 입자 평형 중심 $\bar U_j$ 는 입자 무관 상수"(L1234). **$\rho(U_j)$ = U_j(=중심)의 분포**인데 동시에 "중심은 분포 안 한다"고 못박음 = 정의상 모순. ρ가 *중심* 분포가 아니라면 eq:ensavg 의 적분변수 $\dd U_j$·"중심 $U_j$ 가 분포"(L1184) 가 무엇을 적분하는지 무정의. | 논리: ρ(U_j)dU_j 는 정의상 *중심 U_j 의 분포*. "중심은 입자 무관 상수"와 양립 불가. ORIGIN_VERDICT §3(L43–45): **참 평형 U_j 분포 ≈ 0**, 분포하는 건 η(과전압); "ρ(U_j) 가 평형 U_j 분포"라는 해석 자체를 ground truth 가 부정. | ③의 ρ를 *평형 전이 전위 U_j 의 분포*가 아니라 **유효 배리어·국소 sloping 폭(=plateau 가 sloping 으로 풀리는 정도)의 입자별 분산**으로 재정의하거나, "중심은 상수"를 철회하고 "중심이 ±수 mV 흩어진다(작게)"로 일관화. 둘 중 하나로 단일화 — 현재는 한 절 안에서 둘 다 주장. |
| D2 | ③ Dahn 인용(L1176·1188)·keybox·biblio dahn1995(L1803) | **HIGH** | **Dahn `x_max=1−P` 를 *전이전위 분포 ρ(U_j)* 의 1차 근거로 과대인용.** 본문은 dahn1995 를 "층간 배열 무질서가 평형 전위를 흩뜨린다는 통계역학"(L1176)·"같은 언어"(dreyer 포함)로 ③ ρ(U_j)의 직접 warrant 로 씀. 그러나 카드 43: `x_max=1−P`는 **가역 *용량 한계*·site-blocking** 식이고(card L19·58), "**입자 간** 결정질서 분산 → 전이전위 *중심* 분산 → ensemble 잔여폭"은 **직접 정량 1차논문 미발견 = 근거미발견 tier C(미검증)**(card L62·73–74·81). 또 Dahn 의 기작은 주로 *intra-particle* (P↑ → 한 입자 plateau 가 sloping 붕괴) = ②(내재 폭) 영역이지 *inter-particle* 앙상블 ρ 가 아님. | ground truth card 43 L62: "직접 정량 1차논문 미발견(근거 미발견 tier)"·L81 열린문제 (1)(2). 본문은 [추정/미검증]을 [확정]처럼 단정. tier 병기 의무(설계 L4) 위반. | dahn1995 인용에 tier 강등 명시: "P→dQ/dV 폭 변환식은 본 논문에 없음(외삽); 입자 간 중심분산 정량은 미검증". ②(intra-particle sloping)와 ③(inter-particle ensemble)을 Dahn 기작상 분리 — 현재 둘을 한 인용으로 묶어 과대주장. |
| D3 | LCO peak(L1128–1130) ↔ broadening ③ 물리기반(L1176) | **HIGH** | **③ 의 물리기반(흑연 turbostratic 무질서)이 LCO 로 전이 불가인데 LCO 3 전이에 같은 두-상 현상학적 w 지위를 부여.** L1128: "LCO 세 전이도 모두 $\Omega>2RT$ 두-상이라…현상학적 피팅 폭"(broadening 절 가리킴). 그러나 ③ ρ(U_j)의 물리는 전적으로 **흑연 결정성·흑연화도·turbostratic 무질서·$x_{\max}=1-P$**(L1175–1176) — 층상 산화물 LCO 엔 turbostratic gallery·흑연화도 개념이 부재. ∴ LCO 두-상 종폭을 broadening 절로 떠받칠 때 ③(앙상블 ρ)의 근거가 통째로 빠지는데 본문은 무차별 포인터. | 물리: $x_{\max}=1-P$·turbostratic = 탄소 전용. LCO order–disorder·MIT(L659–682)는 다른 기작. ③을 "보편"으로 쓴 뒤 LCO 에 그대로 적용 = 미정합. | LCO peak 절에서 "③(앙상블 비-크기 무질서)은 흑연 전용 근거 — LCO 두-상 종폭은 ①(η 꼬리)+②(MIT 양끝 폭)+LCO 고유 조성·도핑 이질로 떠받친다"로 분기. 또는 broadening 절 ③를 "흑연 한정"으로 스코프 명시. |
| D4 | eq:ensavg 적분 integrand(L1180–1184·1196) | **MEDIUM** | **eq:ensavg 의 single-particle kernel 에 ①(전류 의존 η 꼬리)을 넣어 평형 앙상블과 동역학을 한 적분에 혼입.** L1184: $(\dd Q/\dd V)^{single}$ = "①② 폭의 봉우리". 그런데 ρ(U_j)는 *평형* 구조 무질서 분포(L1175, 전류 무관). ①은 $L_V\propto|I|$ 로 **전류 켜야 생기고 $|I|\to0$ 소멸**(L1163–1164). 평형 ρ 적분 안에 전류 의존 kernel 을 넣으면 "이 종은 평형에서도 ③로 남는다"(L1186 $\rho\to\delta$ 환원 논리)와 충돌 — kernel 이 |I|에 의존하면 환원극한도 |I|에 의존. ①②③를 "한꺼번에 흡수"(L1196)하는 현상학적 정당화로는 무방하나, eq:ensavg 를 *닫힌 물리식*처럼 제시한 게 과함. | 물리: 평형 분포평균 ⊗ 비평형 kernel = 범주 혼합. forward "설명"이면 OK 지만 식 박스(eq:ensavg)는 평형 ③ 전용이어야. | eq:ensavg 의 kernel 을 "②(평형 잔여)만 포함한 near-delta", ①은 적분 밖 별도 convolution 으로 분리 기술. 또는 eq:ensavg 를 "현상학적 흡수 도식(닫힌 유도 아님)"으로 명시 강등. |
| D5 | 이중지위 Ω 초기값(L710–717)·"4 전이 전부>2RT" | **MEDIUM** | Ω 초기값 4개 전부>2RT = "거친 초기 추정·피팅 override"는 명시됨(L711–713, 설계 일치). 단 표 폭 폴백 0.020/0.016/0.014/0.012 V(L716)가 "초기값"이라면서 두-상 2개엔 현상학적 폭, 단상 2개엔 평형 예측으로 "각각 읽힌다"는데 — *어느 전이가 어느 폴백값을 갖는지* 매핑이 폭값↔전이 순서로만 암시되고 명시 표 참조 끊김. forward-only·ρ→δ·범위경고는 견고. | 경미: 설계 §1(a)·§2 와 일치하나 폭폴백↔전이 매핑이 독자에게 G-follow 약함. | 표 staging 에 "지위(단상/두-상)" 열 추가하거나 본문에 4값↔4전이 1:1 명시. |

---

## 견고했던 부분 (반증 실패 — 설계 정합 확인)

- **사이즈(반경) 제외 일관성: 견고.** (c)-(i)(L1205–1212)·keybox(L1234–1235)·fig 캡션(L1270) 에서 τ∝r²·반경→U_j·PSD convolution 전면 배제, ρ를 "크기 아니라 구조 무질서"로 못박음. 유도·사용 0, 크기분포 잔재 0. 설계 §1(c)·D3 와 일치.
- **forward-only·역산 금지: 견고.** (c)-(ii)(L1213–1219)·L1188 "역산 안 한다"·ill-posed 1종 Fredholm 명시. 설계 §1(b)·(c) 일치.
- **two-phase = LiC₁₂·LiC₆ 2개만(흑연): 견고.** (a)(L1150–1154)·이중지위(L714) 에서 전이별 구분 명확. *단 LCO 로 넘어가면 깨짐 = D3.*
- **w 이중지위 골격·w_eff 제거: 견고.** 단상=평형예측/두-상=현상학적, 같은 eq:wbase 한 식, w_eff 자취 0(헤더 L11).

---

## 반환 요약
기작③(앙상블 ρ(U_j)) **견고도 = 낮음**: ρ 정의가 "중심 분포"인데 (c)·keybox 는 "중심은 상수"라 **자기모순(D1=CRIT)**, Dahn `x_max=1−P`(용량식·미검증 inter-particle)을 ρ(U_j) 1차근거로 **과대인용(D2=HIGH)**. **사이즈 제외 일관 = 견고**(유도·사용 0, 크기잔재 0). **Ω 2개(흑연 two-phase)=견고**하나 **LCO 3 전이엔 ③ 물리기반(turbostratic) 전이 불가인데 같은 두-상 w 부여(D3=HIGH)**. CRIT=D1(ρ 중심분포 vs 상수 모순), HIGH=D2·D3. **가장 약한 1곳 = D1**: ρ(U_j)를 "전이전위(=중심) 분포"로 도입하고 같은 절에서 "중심은 입자 무관 상수"라 부정 — ground truth(ORIGIN §3, 참 U_j 분포≈0)와도 충돌.
