# INTRO_NOTATION_FINAL — 신 Ch2 장 서두·기호표 확정판 검토 (v1.0.22 R3 · O-D 초안)

> 지위: `comp_R3/D_seams/` 신규 초안. 마스터 소스 미수정. 대상 = `ch2v22_sec00_intro.tex`(R1 초판, S-005 신설)·`ch2v22_notation.tex`(R1 초판, S-005 신설).
> 목적(브리핑): "Chapter 1 의 식 번호를 그대로 인용" 문구가 xr live 참조 체계와 정합하는지, 계승 항목 라벨(eq:Uj 등)이 실존하는지 전수 확인 + 필요한 최소 개정문.
> 라벨 실측 = `ch1_graphite_v1.0.22.aux` `\newlabel`(추측 0).

---

## 1. `ch2v22_sec00_intro` — 장 서두

**현행(축자 전문):**
```
본 장은 Chapter 1 이 흑연에서 세운 골격을 두 번째 활물질 LCO(Li$_x$CoO$_2$ 양극)에 건다. 서술
방식은 처음부터 끝까지 하나다: \emph{새 유도를 반복하지 않고, 같은 식에서 바뀌는 파라미터와
추가되는 텀만 적는다.} 곡선 골격(전하 보존 반전$\cdot$평형 종$\cdot$히스테리시스$\cdot$폭)은 Chapter 1
의 식 번호를 그대로 인용하며, LCO 가 새로 요구하는 것 --- 방향 규약의 재배선, order--disorder 와
MIT 2상역, 그리고 흑연에 없는 전자 엔트로피 항 --- 이 본 장의 본문이다.
```
(뒤에 `\tableofcontents`·`\clearpage`.)

### 정합 판정

| 점검 | 결과 |
|---|---|
| "Chapter 1" 지칭 대상 | 흑연 장 = 신 Ch1 — **정확**(OK-NEW, R1B 25·26행) |
| "식 번호를 그대로 인용" ↔ xr live | **정합** — 본문 구현은 `\eqref{Ch1 라벨}`(§2 실측)이라 표시 번호가 곧 Ch1 live 번호. 하드코딩("(1.49)" 리터럴) 아님 → "그대로 인용" 이 실제로 성립 |
| "추가 텀만" 방식 선언 | 본문 절 구현과 정합(ADDTERM_CHECK 참조) |
| 명명 혼동(P3-7) | 없음 — "Chapter 1"(흑연)·"본 장"(LCO) 일관 |

**미세 관찰(비필수):** "그대로 인용" 은 정적 인용의 뉘앙스도 있으나, 실제 구현은 xr **live**(Ch1 재번호 시 자동 갱신)라 더 강한 성질이다. 오도는 아니므로 **개정 불요**. 명시를 원하면 아래 선택안.

- (선택) `Chapter 1 의 식 번호를 그대로 인용하며,` → `Chapter 1 의 식 번호를 (외부참조로) 그대로 인용하며,`
  — 문면 최소 변경. 강제 아님(마스터 재량).

**판정: 서두 확정 가능 — 필수 개정 0.**

---

## 2. `ch2v22_notation` — 계승·신규 2단 기호표

**현행(축자 전문):**
```
\subsection*{기호 --- 계승과 신규}
본 장의 기호는 두 단으로 관리한다. \textbf{계승}(Chapter 1 정의 그대로 --- 재정의 없음):
전이 지표 $j$·용량 $Q_j$·평형 중심 $U_j(T)$~\eqref{eq:Uj}·폭 $w_j=n_jRT/F$·평형 진행률
$\xi_{\eq,j}$~\eqref{eq:logisticsolve}·상호작용 $\Omega_j$ 와 히스 gap~\eqref{eq:dUhys}·분기 인자
$\gamma_j$~\eqref{eq:Ubranch}·방향 부호 $\sigma_d$·반응 엔트로피 $\Delta S_{\rxn,j}$·추출 분율
$\bar x$ 와 전하 보존 반전~\eqref{eq:sm-mc-balance}·합산식~\eqref{eq:sum}. \textbf{신규}(본 장
도입 --- 각 도입 절이 정의 기준): 탈리튬화$\cdot$충방전 재배선 $\sigma_d$ 슬롯 규약(\S\ref{sec:lco-direction}),
질서상$\cdot$MIT 2상역 파라미터(\S\ref{sec:lco-hys-od}), 전자 엔트로피 $\Delta S_e$$\cdot$상태밀도
게이트 $g(E_F,x)$$\cdot$게이트 중심 $x_\mathrm{MIT}$(\S\ref{sec:lco-electronic}), 슬롯 분해
$\Delta S^\mathrm{config/vib/e}_j$(\S\ref{sec:lco-decomp}).
```

### 2a. 계승단 — 인용 라벨 실존 전수 확인(6종, `\eqref`)

| 기호 | 인용 라벨 | live 번호(aux 실측) | 정의 위치(Ch1) | 실존 |
|---|---|---|---|---|
| 평형 중심 $U_j(T)$ | `eq:Uj` | (1.49) | sec:center(§1.3) $U_j(T)$ 온도 환산 | ✅ |
| 평형 진행률 $\xi_{\eq,j}$ | `eq:logisticsolve` | (1.61) | sec:width(§1.5) logistic 유도 | ✅ |
| 히스 gap($\Omega_j$) | `eq:dUhys` | (1.55) | sec:hys(§1.4) gap 닫힌 꼴 | ✅ |
| 분기 인자 $\gamma_j$ | `eq:Ubranch` | (1.57) | sec:hys(§1.4) 방향별 분기 중심 | ✅ |
| 전하 보존 반전 | `eq:sm-mc-balance` | (1.40) | Part 0(§1.2) 다클래스 대정준 반전 | ✅ |
| 합산식 | `eq:sum` | (1.97) | §1.10 합산·staging 초기값 | ✅ |

**6종 전건 `ch1_graphite_v1.0.22.aux` 에 `\newlabel` 실존 → xr 로 live 해소.** 추측 0.
무-eqref 계승 기호(전이 지표 $j$·용량 $Q_j$·폭 $w_j{=}n_jRT/F$·$\sigma_d$·$\Delta S_{\rxn,j}$·$\bar x$·$\Omega_j$)는 기호 나열(정의는 Ch1 소관)이라 라벨 불요 — 정합.

### 2b. 신규단 — 도입 절 라벨 실존(4종, `\S\ref`, 신 Ch2 내부)

| 신규 항 | 라벨 | 정의 위치(신 Ch2) | 실존 |
|---|---|---|---|
| $\sigma_d$ 슬롯 규약 | `sec:lco-direction` | ch1_sec11:83 `\subsection{방향 규약…}` | ✅ |
| 질서상·MIT 2상역 | `sec:lco-hys-od` | ch1_sec13:105 `\subsection{T2·T3 order--disorder…}` | ✅ |
| 전자 엔트로피·게이트 | `sec:lco-electronic` | ch1_sec15:4 `\section{LCO 전자 엔트로피 항…}` | ✅ |
| 슬롯 분해 | `sec:lco-decomp` | ch1_sec14:4 `\section{반응 엔트로피 삼분해…}` | ✅ |

4종 전건 신 Ch2 파일에 정의(장 내부 해소 — xr 불요). "각 도입 절이 정의 기준" 규약과 정합.

### 정합 판정

- "Chapter 1 정의 그대로 --- 재정의 없음" 규약(D22 계승) ↔ 계승단이 Ch1 라벨만 인용하고 재정의 식 없음 → **정합**.
- 명명 혼동(P3-7) 없음. 계승=Ch1(흑연), 신규=본 장(LCO) 구획 명확.

**판정: 기호표 확정 가능 — 필수 개정 0.**

---

## 3. 확정 결론

| 파일 | 확정 여부 | 필수 개정 | 선택 개정 |
|---|---|---|---|
| `ch2v22_sec00_intro` | **확정 가** | 0 | "(외부참조로)" 삽입 1(선택·§1) |
| `ch2v22_notation` | **확정 가** | 0 | ξ_eq 라벨 조화 1(선택·§4) |

두 R1 초판은 라벨 실존·xr 정합·명명 정합이 모두 성립하여 **필수 개정 없이 확정**할 수 있다. 아래 선택 개정은 정합성 미세 개선일 뿐 정정이 아니다(P5 보존·게이트 "무변경" 준수 — 강제 X).

---

## 4. 판단 보류

- **(a) ξ_eq 인용 라벨 조화(선택):** 기호표는 평형 진행률 $\xi_{\eq,j}$ 를 `eq:logisticsolve`(1.61)로 인용하나, 본문(예 `ch1_sec16:17`·`ch1_sec17:43`)은 같은 양을 `eq:xieq`(1.69)로 인용한다. 둘 다 Ch1 평형-logistic 라벨로 **실존·정확**(오류 아님)이나, 계승 기호표가 정본 인용처라면 본문과 라벨을 하나로 맞추는 것이 독자 혼선을 줄인다. 어느 쪽으로 통일할지는 마스터 결정(대상 물리량 동일 — 문서 인용 정책 문제).
- **(b) "그대로 인용" 문구(선택, §1):** 개정 불요. xr live 명시 원할 때만 삽입.
- **(c) 무-eqref 폭 $w_j{=}n_jRT/F$(선택):** 다른 계승 항은 eqref 병기이나 폭은 식만 인라인. 필요 시 `eq:wbase`(1.68)/`eq:xieq`(1.69) 병기 가능 — 현행도 정합(정의 인라인). 강제 X.
- 위 셋 모두 정정이 아닌 정합성 선택이라 O-D 는 **미집행·권고만**.
