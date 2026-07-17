# A07_REVIEW — §6 평형 peak `|I|→0` 기준선 (`ch1_sec06_eqpeak.tex`) 심층 검토 (FR-A07)

> 대상: `/home/user/Project_Anode_Fit/Claude/docs/v1.0.22/_sections/ch1_sec06_eqpeak.tex` (전문 정독 — bgbox [V22-SM2-A] 포함)
> 참조 원문 확인(read-only): `ch1_sec02a_part0.tex`(eq:fermifn·eq:sm-flucres·eq:sm-sint), `ch1_sec02b_part0.tex`(eq:sm-eqcond·eq:sm-logistic·eq:sm-mc-occ·eq:sm-mc-fluc·eq:sm-mc-balance), `ch1_sec03_center.tex`(eq:eqcond·eq:Uj), `ch1_sec04_hys.tex`(eq:dUhys·eq:Ubranch·eq:center), `ch1_sec05_width.tex`(eq:logisticsolve·eq:wbase·eq:xieq·이중지위·fig:logistic), `ch1_sec07_broadening.tex`(부류 분류·②잔여 폭·n_j<1), `ch1_sec08_lag.tex`(eq:Lq·eq:LV), `ch1_sec09_tail.tex`(eq:peakshape·eq:tail-limit·eq:reversal), `ch1_sec10_sum.tex`(eq:sum·tab:staging·L_V 수치), `ch1_sec01_n0n1.tex`(tab:notation·eq:vn), `ch1_sec00_intro.tex`(fig:spine), `ch1_appA_signcheck.tex`(S3·R3·R5), `results/comp_SM2/SM2_DRAFTS/SM2A_susceptibility.tex`(bgbox 독립성 계약 원본), `results/V1022_REFERENCE_LEDGER.md`(V1 원장 규칙).
> 규율: **보고 전용** — 소스 무수정·git 무조작·`Codex/` 미접근. bgbox [V22-SM2-A] 증축분은 제거 용이 독립 블록(무번호 전시식·신규 라벨 0·통삭제 시 §6 원상 복귀 — SM2A 초안 헤더 계약 확인) — 본 보고의 모든 bgbox 내 제안은 그 계약(무번호·라벨 신설 금지·외부가 박스에 의존 금지)을 유지한다. GS-1/GS-2(Ch3 Si 정직 공백)는 본 절 무관 — 메움 제안 없음.
> 상태: **작성 중 조기 저장본** — §서치(하이쿠 서브 doi 검증) 대기 중. (완료 시 이 줄 갱신)

---

## 0. 발견 색인 표 (BRIEF 양식 — 현행 축자·제안 전문은 각 ID 블록의 코드펜스가 원본)

| ID | 파일:행 | 유형 | 등급 | 요지 |
|---|---|---|---|---|
| A07-H1 | ch1_sec06_eqpeak.tex:43 · :57 · :69–72 | 논리(조건 오귀속·수식↔산문 불일치) | **H** | 감수율 항등 "정확" 조건을 `n_j=1` 로 귀속 — 필요한 조건은 `Ω_j=0`. 문서 기본 상태(n_j=1 균일 · Ω_j=6000–13000 J/mol>2RT)가 가드 이분법의 반례. "1/n_j 배 넓혀진 상"은 배율 오귀속(1/n_j는 높이, 폭은 n_j 배; n_j<1 이면 좁혀짐) |
| A07-M1 | ch1_sec06_eqpeak.tex:30–32 | 논리(조건 불완전) | M | 가역 기준선과의 일치를 "γ_j→0 에서만"으로 한정 — Ω_j≤2RT(ΔU^hys≡0)·h_η=0 에서도 일치(반례 존재) |
| A07-M2 | ch1_sec06_eqpeak.tex:8–10 | 보완+수식화 | M | (a) 유도의 암묵 3단(Q≡Q_cell q 식별 · C_bg≡dQ_bg/dV_n 정의 — 빌드 전체 미정의 · dV_n/dq 나눗셈 정당성) 명시 + 중심 단계의 무번호 전시식 승격 |
| A07-M3 | ch1_sec06_eqpeak.tex:53–58 | 보완(표기 정밀) | M | bgbox boxed 좌변 `(dQ/dV)^eq` 무첨자 — eq:sum 의 전곡선(C_bg 포함)과 혼독 위험, `Σ_j(...)^eq_j` 명시 |
| A07-M4 | ch1_sec06_eqpeak.tex:79–81 | 논리(적용 조건 과대) | M | "L_V 가 폭 w_j 보다 작으면" — L_V≲w_j 에선 꼬리 가시적. §10 과 같은 "무시될 만큼"(L_V≪w_j)으로 |
| A07-M5 | ch1_sec06_eqpeak.tex:33–35 | 보완 | M | 판독량에 폭 직접 판독 축(FWHM=3.53w_j) 부재 + 무모수 종-문법 검정 상수 높이×FWHM/면적=ln(1+√2)≈0.881 추가 제안 |
| A07-L1 | ch1_sec06_eqpeak.tex:5–6 | 설명 | L | "곡선이 이 종으로 직접 환원되는 항이다" — 비문 기미 재서술 |
| A07-L2 | ch1_sec06_eqpeak.tex:11 | 설명(P3-1) | L | (a)의 dV_n → (b)의 V 전환 무표시 — §5 평가 규약 승계 한 구절 |
| A07-L3 | ch1_sec06_eqpeak.tex:61–62 | 설명 | L | "몰당 F²/N_ART" — '몰당' 표기 안에 N_A 잔류로 어색, 두 환산 표기 정돈 |
| A07-L4 | ch1_sec06_eqpeak.tex:38–40 | 설명 | L | bgbox 도입의 '감수율' 독자용 정의 한 구절(선택) |

---

## 1. H 등급

### A07-H1 — bgbox 검산 (iii): 감수율 항등의 "정확" 조건 오귀속(`n_j=1` ≠ 충분조건; 필요한 것은 `Ω_j=0`) + "1/n_j 배 넓혀진 상"의 배율 오귀속
- 파일:행 = `ch1_sec06_eqpeak.tex:69–72` (주 locus) · `:43`(본문 병행 locus) · `:57`(boxed 병행 locus)
- 유형 = 논리(물리 조건 오귀속 · 수식↔산문 불일치) / 등급 = **H**
- 현행(축자 — 69–72행, verifybox 내):
```latex
(iii)
\emph{폭 이중지위 가드.} 이 감수율 항등은 통계 폭
$n_j=1$($w_j=RT/F$)에서 정확하다; 두-상 전이의 현상학적 자유 폭($w_j$ 가 broadening 을 흡수 ---
\S\ref{sec:width}$\cdot$\S\ref{sec:broadening})에서는 peak 이 그 감수율의 $1/n_j$ 배 넓혀진 상이라
문자 그대로의 감수율 \emph{크기}가 재척도된다(형상 근거는 유지되나 두-상 폭은 평형 예측이 아니다).
```
- 현행(축자 — 43행, 병행 locus):
```latex
잇는다. 이상 폭($w_j=RT/F$, 곧 $n_j=1$)에서 식~\eqref{eq:eqpeak} 의 전이 몫은 $Q_j=(F/N_A)M_j$ 와
```
- 문제(재유도로 확인):
  1. **조건 오귀속.** 항등 사슬의 마지막 등호(독립-자리 분산 `var(N)=Σ_j M_j θ_j(1-θ_j)`)와 logistic 종 형상·폭 `RT/F` 는 **이상 격자기체 `Ω_j=0`** 전용이다(§5 `sec:width-w`: "엄밀히 이 닫힌 폭은 이상 극한($\Omega_j=0$) 기준"; Part 0 eq:sm-mc-fluc 문장: 둘째 등호가 "독립 자리의 분산 가법"). `n_j=1` 은 폭 **값**일 뿐 폭의 **지위**(평형 예측 vs 현상학)를 정하지 않는다. **반례가 문서 자신의 기본 상태다**: tab:staging 은 네 전이 `n_j=1` 균일(§10: "실제 초기 폭은 네 전이 균일하게 w=RT/F")이면서 `Ω_j=6000–13000` J/mol `>2RT≈4958` J/mol 이고, §7 은 그중 `2L→2`·`2→1` 을 두-상 plateau 로 분류한다 — 이 두 전이는 "`n_j=1` 이라 정확"(가드 첫 가지)과 "두-상 현상학 폭이라 재척도"(가드 둘째 가지)에 **동시에 걸려** 가드의 이분법이 자기 기본값에서 판정 불능이다. 두-상의 평형 감수율은 Maxwell 델타(§7: "Maxwell 공통접선이 plateau 를 한 전위로 모으면 dq/dV→∞")이므로, `n_j=1` 이어도 그 종은 평형 감수율이 **아니다**.
  2. **배율 오귀속.** `(dQ/dV)_j = Q_j ξ(1-ξ)/w_j = [이상 감수율]×(RT/F)/w_j = [이상 감수율]/n_j` (점별) — 곧 `1/n_j` 는 **높이** 배율이고 **폭** 배율은 `n_j`(면적 `Q_j` 불변)다. "1/n_j 배 **넓혀진** 상"은 배율을 폭에 걸었고, 방향도 조건부로 틀린다 — §7 ② 대로 두-상 유효 다중도는 `n_j<1` 가능(폭 폴백 0.014/0.012 V `<RT/F=25.7 mV`, tab:staging)이며 그 경우 "**좁혀진**" 상이다.
  3. **강화 여지(같은 수정에서 공짜로 얻는 층 분리).** 결선 항등 `(dQ/dV)^eq = e²∂⟨N⟩/∂μ` 와 요동 읽기 `var(N)=k_BT∂⟨N⟩/∂μ` 자체는 **대정준 일반**(Part 0 eq:sm-mc-fluc: "대정준 일반 항등식의 특수형")이라 단상 평형이면 상호작용이 있어도 성립한다 — `Ω_j=0` 전용인 것은 독립-자리 분해와 종 형상뿐. 단상 `0<Ω_j<2RT` 에서는 유효 폭이 `(1-Ω_j/2RT)` 배로 좁아지고(§5 — `g''` 재유도로 확인: 중심 기울기 `F/[4RT(1-Ω/2RT)]`) 그만큼 참 `var(N)` 이 독립-자리 값을 넘는다. 현행 가드는 이 중간 창(단상 상호작용)을 통째로 건너뛴다.
- 제안(완성 LaTeX — (iii) 전문 대체; bgbox 독립성 유지 — 무번호·신규 라벨 0·참조는 기존 것만):
```latex
(iii)
\emph{폭 이중지위 가드.} 이 감수율 항등이 문자 그대로 정확한 곳은 이상 극한($\Omega_j{=}0$ --- 이때
통계 폭 $w_j{=}RT/F$, $n_j{=}1$)이다. 항등의 층은 갈라 읽는다 --- 위 박스의 결선$\cdot$요동 층
($e^2\,\partial\langle N\rangle/\partial\mu$ 와 $\mathrm{var}(N)=\kB T\,\partial\langle N\rangle/\partial\mu$,
식~\eqref{eq:sm-mc-fluc})은 대정준 일반이라 단상 평형이면 상호작용이 있어도 성립하나, 독립-자리 분해
$\mathrm{var}(N)=\sum_jM_j\theta_j(1-\theta_j)$ 와 logistic 종 형상$\cdot$폭 $RT/F$ 는 $\Omega_j{=}0$
전용이다(단상 $0{<}\Omega_j{<}2RT$ 는 유효 폭이 $(1{-}\Omega_j/2RT)$ 배로 좁아지고 그만큼
$\mathrm{var}(N)$ 이 독립-자리 값을 넘는다 --- \S\ref{sec:width}). 두-상 전이($\Omega_j{>}2RT$)의
현상학적 자유 폭($w_j$ 가 broadening 을 흡수 --- \S\ref{sec:width}$\cdot$\S\ref{sec:broadening})에서는
평형 감수율이 Maxwell 델타라, 실측 peak 은 이상 감수율을 폭 $n_j$ 배$\cdot$높이 $1/n_j$ 배로 재척도한
상으로만 읽는다($n_j{<}1$ 이면 좁혀진 상 --- \S\ref{sec:broadening} ②) --- 문자 그대로의 감수율
\emph{크기}는 평형 예측이 아니며, 합규칙 (i) 의 면적 $=Q_j$ 만 폭 무관으로 생존한다.
```
- 병행 locus 제안(43행 — 한 구절 교체):
```latex
잇는다. 이상 극한($\Omega_j{=}0$ --- 이때 통계 폭 $w_j=RT/F$, 곧 $n_j=1$)에서 식~\eqref{eq:eqpeak} 의 전이 몫은 $Q_j=(F/N_A)M_j$ 와
```
- 병행 locus(57행 boxed 꼬리 괄호)는 A07-M3 제안 코드에 포함(`이상 폭` → `이상 극한 $\Omega_j{=}0$`).
- 근거: §5 `sec:width-w`(이상 극한 Ω=0 기준·(1-Ω/2RT) 유효 폭·이중지위) · §7 `sec:broadening-class`/② (두-상 분류·Maxwell 델타·n_j<1 허용) · §10 tab:staging+"네 전이 균일 w=RT/F" · Part 0 eq:sm-mc-fluc 본문("독립 자리의 분산 가법"·"대정준 일반 항등식") · 재유도: `(dQ/dV)_j=[F²M_jθ(1-θ)/(N_ART)]·(RT/F)/w_j = 감수율/n_j`(높이), 폭 스케일 `w_j=n_j·RT/F`(폭 n_j 배), 면적 `Q_j` 불변.

---

## 2. M 등급

### A07-M1 — 히스 잔존 극한과 가역 기준선의 일치 조건 "γ_j→0 에서만" — 불완전(반례: γ_j≠0·Ω_j≤2RT)
- 파일:행 = `ch1_sec06_eqpeak.tex:30–32` / 유형 = 논리(조건 불완전) / 등급 = M
- 현행(축자):
```latex
이 값이 전이별로 합산되어 배경과 함께 $|I|\to0$ 극한을 이룬다 --- 단 $\gamma_j\ne0$ 이면 이 극한은 분기
중심 $U_j^{\,d}$ 에 남는 히스테리시스 잔존 극한이고, 분기 없는 가역 기준선($U_j$ 중심)과는
$\gamma_j\to0$ 에서만 일치한다(히스테리시스는 열역학적 --- \S\ref{sec:hys}).
```
- 문제(재유도): 분기 shift 는 `U_j^d − U_j = ½σ_d h_{η,j} γ_j ΔU_j^hys`(eq:Ubranch)이고 `ΔU_j^hys` 는 `Ω_j≤2RT` 에서 **항등적으로 0**(eq:dUhys 명시 분기)이다. 따라서 `γ_j≠0` 이어도 `Ω_j≤2RT`(단상) 또는 `h_{η,j}=0` 이면 두 기준선은 일치한다 — "γ_j→0 에서**만**"의 '만'이 반례를 가진다(전제 `γ_j≠0` 아래에서 문장 자체가 γ_j→0 극한을 말하는 것도 논리적으로 어색).
- 제안(완성 LaTeX):
```latex
이 값이 전이별로 합산되어 배경과 함께 $|I|\to0$ 극한을 이룬다 --- 단 $\gamma_j\ne0$ 이면 이 극한은 분기
중심 $U_j^{\,d}$ 에 남는 히스테리시스 잔존 극한이고, 분기 없는 가역 기준선($U_j$ 중심)과는 분기 shift
$\tfrac12h_{\eta,j}\gamma_j\Delta U_j^\hys$ 가 $0$ 으로 가는 곳 --- $\gamma_j\to0$, 또는 애초에
$\Omega_j\le2RT$ 라 $\Delta U_j^\hys=0$(식~\eqref{eq:dUhys}) --- 에서만 일치한다(히스테리시스는 열역학적
--- \S\ref{sec:hys}).
```
- 근거: eq:Ubranch·eq:center(분기 적용 조건)·eq:dUhys("Ω_j≤2RT 면 gap 은 정확히 0") · appB "equilibrium 메서드 = U_j 중심 가역 기준선" 구분과도 정합.

### A07-M2 — (a) 전하 보존식 미분의 암묵 3단 명시 + 중심 단계의 전시식 승격 (보완·수식화 겸용)
- 파일:행 = `ch1_sec06_eqpeak.tex:8–10` / 유형 = 보완+수식화 / 등급 = M
- 현행(축자):
```latex
\textbf{(a) 출발 --- 전하 보존식.} 관측 $\dd Q/\dd V$ 는 전하 보존식 $Q_\cell q=Q_\bg(V_n)+\sum_jQ_j\xi_j$ 를 궤적
$q$ 로 미분해 닫힌다 --- 양변을 $q$ 로 미분하면 $Q_\cell=C_\bg\,\dd V_n/\dd q+\sum_jQ_j\,\dd\xi_j/\dd q$ 이고,
$\dd V_n/\dd q$ 로 나누면 $\dd Q/\dd V_n=C_\bg+\sum_jQ_j\,\dd\xi_j/\dd V_n$ 이다.
```
- 문제(빠진 논증 3건 — 독자가 물을 곳):
  1. 좌변 식별 `Q ≡ Q_cell q` 가 무표시(관측 `dQ/dV` 와 좌변 `Q_cell·dq/dV_n` 의 연결 고리 — tab:notation 의 `q=Q/Q_cell` 를 역방향으로 써야 보임).
  2. `C_bg ≡ dQ_bg/dV_n` 연쇄율이 무표시 — **이 정의식은 빌드 어디에도 없다**(grep 전수: tab:notation 은 "배경 미분용량"이라는 말 정의뿐; `Q_bg` 와 `C_bg` 를 잇는 식은 §6 (a) 의 이 행이 유일한 사용처인데 정의 없이 대입됨). 전하 보존식이 중심식(P3-2)인 문서에서 그 미분의 첫 항 정의가 공백.
  3. `dV_n/dq` 나눗셈의 정당성(궤적 단조) — 평형 추종에서 `q(V_n)` 은 배경(`C_bg≥0`)과 강단조 logistic 들의 합이라 강단조: 바로 Part 0 요동 양성(eq:sm-mc-fluc)의 결과-사슬 판인데, 그 연결이 bgbox("유일근을 보증한 바로 그 var(N)")에만 있고 본문 유도에는 없다.
- 제안(완성 LaTeX — (a) 전문 대체; 전시식은 **무번호** `\[...\]` 로 두어 기존 식 번호 무이동(P5); 문장 전부 보존·보강만):
```latex
\textbf{(a) 출발 --- 전하 보존식.} 관측 $\dd Q/\dd V$($Q\equiv Q_\cell q$ --- 표~\ref{tab:notation} 의
용량 좌표)는 전하 보존식 $Q_\cell q=Q_\bg(V_n)+\sum_jQ_j\xi_j$ 를 궤적 $q$ 로 미분해 닫힌다 --- 양변을
$q$ 로 미분하고(배경 몫은 연쇄율 $\dd Q_\bg/\dd q=C_\bg\,\dd V_n/\dd q$, $C_\bg\equiv\dd Q_\bg/\dd V_n$
--- 표~\ref{tab:notation} 의 배경 미분용량), $\dd V_n/\dd q$ 로 나누면
\[
Q_\cell=C_\bg\,\frac{\dd V_n}{\dd q}+\sum_jQ_j\,\frac{\dd\xi_j}{\dd q}
\quad\Longrightarrow\quad
\frac{\dd Q}{\dd V_n}=C_\bg+\sum_jQ_j\,\frac{\dd\xi_j}{\dd V_n}
\]
이다. 나눗셈은 $\dd V_n/\dd q\ne0$ 인 단조 구간에서 정의되는데, 평형 추종에서는 $q(V_n)$ 이 배경
($C_\bg\ge0$)과 강단조 logistic 들의 합이라 항상 성립한다 --- Part 0 요동 양성(식~\eqref{eq:sm-mc-fluc})
의 결과-사슬 판이다.
```
- 근거: tab:notation(`q=Q/Q_cell`·`C_bg` 말 정의) · grep 전수(`C_\bg` 정의식 부재) · eq:sm-mc-fluc(강단조 보증) · P3-2(보존식 중심 유지 — 현행은 중심 단계가 인라인, 일반 항등식 eq:belliden 만 번호 전시라 시각 비중 역전; 무번호 전시로 교정하면 번호 재배열 0).

### A07-M3 — bgbox boxed 좌변 `(dQ/dV)^eq` 무첨자 — eq:sum 전곡선(C_bg 포함)과 혼독 위험
- 파일:행 = `ch1_sec06_eqpeak.tex:53–58` / 유형 = 보완(표기 정밀) / 등급 = M
- 현행(축자):
```latex
\[
\boxed{\;\Big(\frac{\dd Q}{\dd V}\Big)^\eq
=\frac{F^2}{N_A RT}\,\mathrm{var}(N)
=e^2\,\frac{\partial\langle N\rangle}{\partial\mu}\;}
\qquad(e\equiv F/N_A,\ \text{이상 폭}),
\]
```
- 문제: 본문이 정의한 표기는 `(dQ/dV)^eq_j`(첨자형, eq:eqpeak)뿐이고, 무첨자 `(dQ/dV)^eq` 는 이 박스가 새로 만든 표기다. 그런데 §6 본문의 "|I|→0 극한"과 eq:sum 의 관측 `dQ/dV` 는 **배경 `C_bg` 포함**이라, 박스 헤드라인만 인용하는 독자가 "평형 dQ/dV(전곡선) = e²∂⟨N⟩/∂μ"로 오독할 수 있다(검산 (iv)가 뒤에서 바로잡지만 boxed 식 자체가 자족적이어야 함). 꼬리 괄호 "(이상 폭)"의 조건 오귀속은 A07-H1 과 동일 사안.
- 제안(완성 LaTeX):
```latex
\[
\boxed{\;\sum_j\Big(\frac{\dd Q}{\dd V}\Big)^\eq_j
=\frac{F^2}{N_A RT}\,\mathrm{var}(N)
=e^2\,\frac{\partial\langle N\rangle}{\partial\mu}\;}
\qquad(e\equiv F/N_A,\ \text{이상 극한 }\Omega_j{=}0),
\]
```
  (뒤따르는 "곧 \emph{평형 $\dd Q/\dd V$ 는 저장 전하의 요동 스펙트럼}이다" 문장은 그대로 접속 — 필요하면 "곧 \emph{평형 $\dd Q/\dd V$ 의 전이 몫은 …}"로 한 단어 보강.)
- 근거: eq:sum(`dQ/dV = C_bg + Σ…`) · 검산 (iv) 자체가 배경 제외를 별도로 말해야 했다는 사실이 표기 공백의 방증 · 대수 재검증(아래 §V — 등호 사슬 자체는 정확).

### A07-M4 — 닫는 문단의 적용 조건 "L_V 가 폭 w_j 보다 작으면" — 과대(경계 사례 L_V≲w_j 에서 꼬리 가시적)
- 파일:행 = `ch1_sec06_eqpeak.tex:79–81` / 유형 = 논리(적용 조건 과대) / 등급 = M
- 현행(축자):
```latex
이 식이 쓰이는 조건은 지연 길이가 peak 폭에 비해 작을 때다 --- \S\ref{sec:lag}(N7)이 그 지연 길이 $L_V$ 를
세우고, $L_V$ 가 폭 $w_j$
보다 작으면(또는 동역학 입력이 없으면) 식~\eqref{eq:eqpeak} 의 평형 종으로 매끈히 환원된다(식~\eqref{eq:tail-limit} 의 $L_V\to0$ 극한). 이것이 $|I|\to0$ 환원이다.
```
- 문제: eq:tail-limit 은 `L_V→0` **극한**이고, `L_V<w_j` 이기만 하면(예 `L_V=0.5w_j`) 꼬리는 여전히 폭과 같은 자릿수로 가시적이다. §6 도입부(6행)와 §10(55행 "폭 $w_j$(수십 mV)에 비해 무시할 만큼 작아")은 이미 "무시될 만큼"으로 옳게 말한다 — 이 문단만 조건이 풀렸다.
- 제안(완성 LaTeX):
```latex
이 식이 쓰이는 조건은 지연 길이가 peak 폭에 비해 무시될 만큼 작을 때다 --- \S\ref{sec:lag}(N7)이 그 지연
길이 $L_V$ 를 세우고, $L_{V,j}\ll w_j$ 면(또는 동역학 입력이 없으면) 식~\eqref{eq:eqpeak} 의 평형 종으로
매끈히 환원된다(식~\eqref{eq:tail-limit} 의 $L_V\to0$ 극한 --- 초기 상태 수치로는 $L_{V,j}\sim10^{-10}$--$10^{-8}$ V
대 $w_j$ 수십 mV, \S\ref{sec:sum}). 이것이 $|I|\to0$ 환원이다.
```
- 근거: eq:tail-limit(극한 명제) · §10 55행(수치·"무시할 만큼" 어법) · §6 6행(같은 어법) — 문서 내 자기정합 회복.

### A07-M5 — 판독량 확장: 폭의 직접 판독 축(FWHM) 부재 + 무모수 종-문법 검정 상수(보완)
- 파일:행 = `ch1_sec06_eqpeak.tex:33–35` / 유형 = 보완 / 등급 = M
- 현행(축자):
```latex
세 양 --- 위치 $=$ 중심
$U_j^{\,d}$, 순높이 $=Q_j/(4w_j)$($\xi=\tfrac12$ 에서 $\xi(1-\xi)=\tfrac14$), 배경 차감 면적 $=Q_j$
($\int_0^1\dd\xi=1$, 식~\eqref{eq:belliden} 의 종이 $\dd\xi_\eq$ 의 치환적분이라 면적 $1$) --- 가 이 한 식에서 읽힌다.
```
- 문제/이득: 피팅 실무의 4대 판독량 중 **폭**만 직접 판독 축이 없다(높이·면적에서 `w_j=면적/(4×높이)` 로 역산은 되나 배경 차감 오차에 이중 노출). fig:logistic 캡션에는 이미 `FWHM=3.53w`(298 K, 90.5 mV)가 있는데 판독 절인 §6 본문에 없다. 덤으로 세 판독량은 독립이 아니어서 — 재유도: 반높이 `ξ(1-ξ)=1/8` 의 두 근 `ξ=(1±1/√2)/2` 에서 `z=±ln(3+2√2)` → `FWHM=2ln(3+2√2)w_j≈3.5255w_j`; `높이×FWHM/면적 = ln(3+2√2)/2 = ln(1+√2) ≈ 0.8814` — **모수와 무관한 상수**가 나와, 측정 종이 정말 logistic 미분인지(Gauss `2√(ln2/π)≈0.939`·Lorentz `2/π≈0.637` 과 구별) 배경 차감 뒤 무모수로 검정하는 한 줄이 된다.
- 제안(완성 LaTeX — 해당 문장 대체):
```latex
네 양 --- 위치 $=$ 중심
$U_j^{\,d}$, 순높이 $=Q_j/(4w_j)$($\xi=\tfrac12$ 에서 $\xi(1-\xi)=\tfrac14$), 반높이 전폭
$=2\ln(3{+}2\sqrt2)\,w_j\approx3.53\,w_j$($\xi(1-\xi)=\tfrac18$ 의 두 근 --- 폭의 직접 판독 축,
그림~\ref{fig:logistic}), 배경 차감 면적 $=Q_j$
($\int_0^1\dd\xi=1$, 식~\eqref{eq:belliden} 의 종이 $\dd\xi_\eq$ 의 치환적분이라 면적 $1$) --- 가 이 한 식에서 읽힌다.
높이$\cdot$폭$\cdot$면적은 독립이 아니다 --- 종이 logistic 미분이면 순높이$\times$반높이
전폭$/$면적$=\ln(1{+}\sqrt2)\approx0.881$ 로 모수 무관 상수라(Gauss 종 $0.939$$\cdot$Lorentz 종 $0.637$ 과
구별), 배경 차감 뒤 종 문법 자체를 무모수로 검정하는 한 줄이 된다.
```
- 근거: 재유도(위 수치 전부 본 검토에서 독립 계산 — §V) · fig:logistic 캡션의 `3.53w` 와 정합 · "세 양→네 양"은 명칭 변경이라 P5 상 **제안**으로만 둔다.

---

## 3. L 등급

### A07-L1 — 도입 문장 재서술
- 파일:행 = `ch1_sec06_eqpeak.tex:5–6` / 유형 = 설명 / 등급 = L
- 현행(축자):
```latex
평형 진행률에서 곧바로 얻어지는 것이 평형 peak 모양 $\xi_\eq(1-\xi_\eq)/w$ 이다. 이것이 전류가 없을 때($|I|\to0$)의
기준선이며, 동역학 꼬리가 무시될 만큼 작을 때 곡선이 이 종으로 직접 환원되는 항이다.
```
- 문제: "곡선이 … 환원되는 **항**이다" — 주어(곡선)와 술어(항)가 어긋나는 비문 기미.
- 제안:
```latex
평형 진행률에서 곧바로 얻어지는 것이 평형 peak 모양 $\xi_\eq(1-\xi_\eq)/w$ 이다. 이것이 전류가 없을 때($|I|\to0$)의
기준선이며, 동역학 꼬리가 무시될 만큼 작을 때 곡선이 직접 환원되는 종이다.
```

### A07-L2 — (a)→(b) 의 `V_n`→`V` 표기 전환 무표시 (P3-1 위계 한 구절)
- 파일:행 = `ch1_sec06_eqpeak.tex:11` / 유형 = 설명(P3-1) / 등급 = L
- 현행(축자 — 11행 중):
```latex
미분의 종 항등식.} 평형 추종이면 $\dd\xi_j/\dd V_n$ 에 평형 기울기가 들어가고, $z\equiv\sigma_d(V-U_j^{\,d})/w_j$ 로
```
- 문제: (a) 는 `dQ/dV_n`, (b) 부터는 맨 `V`(z 정의·eq:eqpeak 좌변) — §5 의 평가 규약("여기서 평가 전위는 §pol 의 내부 전위 V_n")을 승계하는 전환인데 §6 안에는 무표시. `|I|→0` 에서 `V_n=V_app` 라 실해는 없으나(eq:vn), 절 제목이 그 극한을 다루는 만큼 한 구절이면 위계가 닫힌다.
- 제안:
```latex
미분의 종 항등식.} 평형 추종이면 $\dd\xi_j/\dd V_n$ 에 평형 기울기가 들어가고, $z\equiv\sigma_d(V-U_j^{\,d})/w_j$
($V$ 는 이하 내부 전위 $V_n$ --- \S\ref{sec:width} 의 평가 규약; $|I|\to0$ 에서 $V_n=V_\app$, 식~\eqref{eq:vn}) 로
```

### A07-L3 — bgbox "자리당 e² 과 몰당 F²/N_ART" — '몰당' 표기 정돈
- 파일:행 = `ch1_sec06_eqpeak.tex:61–62` / 유형 = 설명 / 등급 = L
- 현행(축자):
```latex
$\partial Q/\partial V$ 로 옮긴 것이 이 항등식 --- 요동--소산 관계의 전기화학판이며, 자리당 $e^2$ 과 몰당
$F^2/N_ART$ 는 같은 환산의 두 표기다($e$ 는 자리당 전하, $F=N_Ae$).
```
- 문제: '몰당' 이라 부른 표기 `F²/N_ART` 안에 `N_A` 가 잔류해 명명이 스스로 어긋난다(순수 몰당 형이 아니라 몰 상수로 쓴 자리-량 표기).
- 제안:
```latex
$\partial Q/\partial V$ 로 옮긴 것이 이 항등식 --- 요동--소산 관계의 전기화학판이며, 자리당 표기
$e^2\,\partial\langle N\rangle/\partial\mu$ 와 몰 상수 표기 $F^2\,\mathrm{var}(N)/(N_ART)$ 는 같은 양의 두
환산이다($e$ 는 자리당 전하, $F=N_Ae$, $R=N_A\kB$).
```

### A07-L4 — bgbox 도입의 '감수율' 독자용 한 구절(선택)
- 파일:행 = `ch1_sec06_eqpeak.tex:38–40` / 유형 = 설명 / 등급 = L
- 현행(축자):
```latex
\textbf{평형 peak 은 등온 감수율 --- 요동--소산 읽기.} 식~\eqref{eq:eqpeak} 의 평형 peak 은 곡선맞춤 종이
아니라 전극에 저장된 전하의 \emph{등온 입자수 감수율}(isothermal particle-number susceptibility) 그
자체다.
```
- 제안(문장 뒤에 한 구절 —):
```latex
자체다 --- 저장조 손잡이($\mu$, 결선하면 $V$)를 미소하게 틀 때 저장 입자수(전하)가 얼마나 응답하는지를
재는 평형 응답계수라는 뜻이다.
```

---

## V. 재계산·재유도 검증 기록 (관점 ② 전수 — 문제 없던 것 포함)

| # | 검증 대상 | 방법 | 결과 |
|---|---|---|---|
| V1 | (a) 보존식 미분 사슬 | `Q_cell=C_bg V_n'+ΣQ_jξ_j'` 을 `dV_n/dq` 로 나눔 → `Q_cell dq/dV_n = d(Q_cell q)/dV_n` 식별 | ✓ 정확(암묵 3단은 A07-M2) |
| V2 | eq:belliden | `d/dz (1+e^{-z})^{-1} = e^{-z}/(1+e^{-z})² = [1/(1+e^{-z})]·[e^{-z}/(1+e^{-z})] = ξ(1-ξ)`; 최대 `1/4`@`ξ=½` | ✓ 항등·언더브레이스 대응 정확 |
| V3 | (c) 연쇄율 | `dz/dV=σ_d/w_j` → `dξ/dV=σ_dξ(1-ξ)/w_j` | ✓ |
| V4 | eq:eqpeak 부호 처리 | `|σ_d|=1` → `Q_j|dξ/dV|=Q_jξ(1-ξ)/w_j` — 절댓값 정의 채택, S3(appA)와 동일 | ✓ 자기정합(방향 불변은 `ξ↔1-ξ` relabel 불변과도 정합, §2b(i)) |
| V5 | 세 판독량 | 위치 z=0 → `V=U_j^d`; 높이 `Q_j/(4w_j)`; 면적 `∫ξ(1-ξ)/w dV=∫₀¹dξ=1` 치환적분 | ✓ |
| V6 | bgbox 전이별 식 | `Q_j/w_j=(FM_j/N_A)(F/RT)=F²M_j/(N_ART)`; `ξ(1-ξ)=θ(1-θ)`; `var_j=M_jθ_j(1-θ_j)`(독립 자리) | ✓ (이상 극한 조건은 A07-H1) |
| V7 | bgbox 합산 boxed | `F²var/(N_ART) = F²k_B·(∂N/∂μ)/(N_AR) = (F/N_A)²∂N/∂μ = e²∂N/∂μ` (k_B/R=1/N_A) | ✓ |
| V8 | 같은 식의 1원리 독립 재유도 | `Q_ext=e(M−⟨N⟩)`, 결선 `dμ=−e dV`(s=+1) → `dQ_ext/dV=+e²∂⟨N⟩/∂μ>0` — 부호·양수성 포함 | ✓ 부호까지 일치 |
| V9 | 차원 | `e²∂N/∂μ`: C²/J=C/V; `F²var/(N_ART)`: (C²/mol²)/(J/mol²)=C/V | ✓ |
| V10 | 검산 (i) 합규칙·(ii) 정점 | `∫(dQ/dV)_j dV=Q_j`; `var` 최대@`θ=½` | ✓ (합규칙은 폭 무관 — H1 제안에 반영) |
| V11 | 검산 (iv) 배경 제외 | eq:sum 의 `C_bg` 가법·Part 0 "클래스 밖 가법 항" 문구 대조 | ✓ 정합 |
| V12 | 검산 (iii) | `(dQ/dV)_j = 이상 감수율/n_j`(점별·높이), 폭 `×n_j`, 면적 불변; 기본 상태 `n_j=1`∧`Ω_j>2RT` 반례 | ✗ → **A07-H1** |
| V13 | 히스 잔존 문장 | `U_j^d−U_j=½σ_dh_ηγ_jΔU^hys`; `ΔU^hys≡0`@`Ω≤2RT` | ✗(조건 불완전) → **A07-M1** |
| V14 | 닫는 문단 조건 | `L_V<w_j` vs `≪`; §10 수치 `10⁻¹⁰–10⁻⁸ V` | ✗(과대) → **A07-M4** |
| V15 | Part 0 라벨 4건 인용 정확성 | eq:sm-flucres·eq:sm-mc-occ·eq:sm-mc-fluc·eq:sm-eqcond 원문 축자 대조 | ✓ 오귀속 없음 |
| V16 | eq:tail-limit 인용 | §9 지배수렴 유도(치환 `t=(V−u)/L_V`·지배함수 `e^{-t}/(4w)`) 재확인 | ✓ |
| V17 | FWHM·형상 상수 | `ξ(1-ξ)=1/8`→`z=±ln(3+2√2)`; `½ln(3+2√2)=ln(1+√2)=0.8814`; Gauss `0.9394`·Lorentz `0.6366` | ✓ (A07-M5 제안 수치) |
| V18 | bgbox 독립성 | 무번호 전시식 2·라벨 신설 0·외부 의존 0(SM2A 초안 계약) — 본 보고 제안 전부 계약 유지 | ✓ |

## 무발견 축 (검토했으나 문제 없음 — 명시)

- **수식 대수 전층**: eq:belliden·연쇄율·eq:eqpeak·bgbox 두 전시식·검산 (i)(ii)(iv) — 재유도·차원·부호 전부 통과(V1–V11). bgbox 의 핵심 물리 주장(평형 종 = 입자수 요동, `μ↔V` 결선이 감수율을 `∂Q/∂V` 로 옮김)은 1원리 독립 재유도(V8)로 **부호까지 확인** — 건전.
- **부호 사슬**: `σ_d` 처리(절댓값·방향 불변)는 appA S3·R3·R5 와 정합 — 신규 부호 결함 0.
- **교차 참조 정확성**: §6 이 인용하는 외부 라벨 전건(eq:sum·eq:tail-limit·Part 0 4건·§hys·§lag·§width·§broadening) 원문 대조 — 오귀속 0 (V15·V16).
- **P3 준수**: P3-2(전하 보존식이 중심식 — (a) 가 보존식에서 출발, 유지 ✓; A07-M2 는 강화 제안) · P3-7(ver.N/Chapter 혼동 — 해당 표기 없음 ✓) · P3-1(V_n 위계 — 실오류 없음, L2 한 구절 제안만).
- **bgbox 독립성**: 계약 준수 확인(V18) — 본 보고의 어떤 제안도 본문이 bgbox 에 의존하게 만들지 않는다.

---

## S. 문헌 서치 (하이쿠 서브에이전트 — doi 실검증분만)

**배경**: bgbox [V22-SM2-A] 는 현재 `\cite` 0건이다. "요동--소산 관계의 전기화학판"이라는 자리매김 주장(61행)에 (i) 일반 항등의 교과서 근거, (ii) 선행 문헌 앵커가 붙으면 주장 지위가 명확해진다(선행이 있으면 오귀속 방지, 없으면 자리매김 강화 — 어느 쪽이든 이득).

**즉시 가능 옵션(원장 무접촉·신규 등재 0)**: 대정준 일반 항등 `∂⟨N⟩/∂μ=β[⟨N²⟩−⟨N⟩²]` 는 Part 0 이 이미 `\cite{mcquarrie1976}` 로 앵커(eq:sm-mc-fluc 문장). bgbox 의 결선·요동 층 문장에 같은 키를 병기하는 것은 ch1 bib 기존 키(확인: `ch1v22_bib.tex:14`) 재사용이라 [검증→등재→인용] 파이프라인 비용이 0 이다. bgbox 독립성(제거 용이)도 불변 — `\cite` 는 참조일 뿐.

**신규 후보(하이쿠 서브 doi 검증)**: *(서브에이전트 결과 대기 중 — 완료 시 본 절에 통합)*

---

## 4-tier 최종 분류

*(서치 통합 후 확정)*
