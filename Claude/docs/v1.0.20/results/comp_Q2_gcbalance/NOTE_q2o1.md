# NOTE_q2o1 — v1.0.21 Q2 대정준 전하 보존 유도 (경쟁 초안 q2o1)

> 독립·무통신 초안. 산출: `draft_q2o1.tex`(107행) + 본 NOTE. 문서 원본 무수정.
> 목적: 전하 보존 음함수 `Σ_j Q_j ξ_eq,j(U_oc,T)=Q x̄` 를 다클래스 격자기체의 대정준 구조에서
> 유도해 "중심식의 통계역학 1급 승격"을 완성하는 신설 소절 초안. 반영은 v1.0.21(본 창은 초안만).
> 근거: `DIRECTION_STATMECH_REPORT.md` 후보 (i)+축 A(1순위). 새 물리 주장 0 — 표준 통계역학 + 기존 문건 식의 식별.

---

## 1. 설계 근거

### 1.1 무엇을 승격하는가
- Part 0 §2.3(`sec:sm-lattice`)은 **단일 클래스** M 자리에서 `Ξ_M=Ξ_1^M`(eq:sm-factor)·`⟨N⟩=Mθ` 까지 닫았다.
- Chapter 2 `eq:implicit`(`Σ_j Q_j ξ_eq,j(U_oc,T)=Q x̄`)과 Ch1 §6(`sec:eqpeak`)의 전하 보존식
  (`Q_cell q=Q_bg(V_n)+Σ_j Q_j ξ_j`)은 **본론이 중심식으로 소비**하나, 그 통계역학적 기원이 Part 0 사다리에 없었다.
- 본 소절은 §2.3 을 **다클래스로 한 줄 확장**(`Ξ=Π_j Ξ_{1,j}^{M_j}` → `⟨N⟩=Σ_j M_j θ_j`)하고, 전하 보존식이
  그 대정준 구조의 **제약 반전**(대정준↔정준 Legendre)임을 **식별**해 승격을 완성한다.
- payoff(축 A): `∂⟨N⟩/∂μ=β·var(N)>0` 요동 양성이 반전 좌변의 U_oc 단조성 → **솔버 유일근의 통계역학
  존재·유일성 증명**. 단일 자리 요동–응답 `eq:sm-flucres`(`var(n)=θ(1-θ)`)의 거시판.

### 1.2 D7 정통 유도 선행 양식 준수(rubric B4)
- 원형(단일 클래스)은 §2.3 에 이미 있으므로 **재유도하지 않고 회수**((a)에서 eq:sm-factor 회수).
- (a)출발=§2.3 인수분해 회수 + "전이 j = 자리 클래스 M_j" 프레이밍 → (b)연산=클래스곱 `Π_j Ξ_{1,j}^{M_j}`
  (표준 인수분해 `\cite{hill1960}`) → (c)중간식=`⟨N⟩=Σ_j M_j θ_j`(eq:sm-gc 셋째 식 재사용) →
  (d)박스=`eq:implicit` 식별(eq:sm-mc-balance) → verifybox(요동 양성→유일근 + 확장 off 회수 + 부호).
- 확장 off 검산(rubric B3): `N_p=1` 에서 `Σ_j M_j θ_j → Mθ`(§2.3 eq:sm-factor 정확 회수). verifybox (ii).

### 1.3 규약·인용
- Ξ·β·θ/ξ(진행률 ξ=1-θ, §notation)·s=+1 규약 준수. 새 물리 도입 0.
- 인용: `hill1960`(대정준 lattice gas 표준 인수분해, (b))·`mcquarrie1976`(대정준 요동 정리, verifybox (i)) —
  둘 다 REFERENCE_LEDGER V1 등재 키(기존 §2.3·bgbox 에서 이미 사용). `callen1985` 등 신규 서지 불요.
- 라벨: 신규 `sec:sm-mc`·`eq:sm-mc-{factor,occ,vac,balance,fluc}`. 기존 라벨·식번호·수치 전부 불변.
- 매크로 유의: Ch1 preamble 에 `\oc` 미정의(Ch1 은 V_n, U_oc 는 Ch2). draft 는 `U_\mathrm{oc}` 로 표기 —
  렌더는 `U_\oc` 와 글자까지 동일. eq:implicit 과 시각적 완전 일치 유지.

---

## 2. 전 식 자체 재유도 검산 (task 규칙: 모든 식 재유도를 NOTE 에 기록)

### eq:sm-mc-factor  `Ξ=Π_j Ξ_{1,j}^{M_j}, lnΞ=Σ_j M_j lnΞ_{1,j}`
- 대정준 합 `Ξ=Σ_{배열} exp[-β Σ_k (ε̃_{c(k)}-μ) n_k]`, c(k)=자리 k 의 클래스, n_k∈{0,1}(가정 1).
- 자리 독립(가정 2) ⇒ 합이 자리별 곱: `Ξ=Π_{k=1}^{M_tot}[Σ_{n_k} e^{-β(ε̃_{c(k)}-μ)n_k}]=Π_k Ξ_{1,c(k)}`.
- 클래스별로 묶으면 클래스 j 의 M_j 자리가 각각 Ξ_{1,j} ⇒ `Ξ=Π_j Ξ_{1,j}^{M_j}`, `lnΞ=Σ_j M_j lnΞ_{1,j}`. ✓
- `Ξ_{1,j}=1+e^{-β(ε̃_j-μ)}`(eq:partfn 을 ε̃_j 로; 이상 극한). Ω_j≠0 이면 자기무모순 평균장형(§2.4). ✓
- §2.3 eq:sm-factor(`Ξ_M=Ξ_1^M`)의 클래스별 반복 — 자명한 다클래스 확장. **근사 경계 명시**: 평균장 수준,
  클래스 간 staging 상관은 곱에서 빠짐(DIRECTION 위험 노트 정합).

### eq:sm-mc-occ  `⟨N⟩=k_BT ∂lnΞ/∂μ=Σ_j M_j θ_j`
- `∂lnΞ/∂μ=Σ_j M_j ∂lnΞ_{1,j}/∂μ`.
- `∂lnΞ_{1,j}/∂μ=(1/Ξ_{1,j})·β e^{-β(ε̃_j-μ)}=β·e^{-β(ε̃_j-μ)}/(1+e^{-β(ε̃_j-μ)})=β θ_j`,
  `θ_j=1/(1+e^{β(ε̃_j-μ)})`.
- `⟨N⟩=k_BT·Σ_j M_j β θ_j=Σ_j M_j θ_j`(k_BT·β=1). ✓ = §2.3 `⟨N⟩=Mθ` 의 클래스 합. eq:sm-gc 셋째 식 재사용.

### eq:sm-mc-vac  `Σ_j M_j ξ_j=M_tot-⟨N⟩`
- ξ_j=1-θ_j(§notation θ_j=1-ξ_j; §2.5 ξ_eq=1-θ_eq).
- `⟨N⟩=Σ M_j θ_j=Σ M_j(1-ξ_j)=M_tot-Σ M_j ξ_j` ⇒ `Σ M_j ξ_j=M_tot-⟨N⟩`. ✓ (중간식 노출 — rubric B2 점프 금지)

### eq:sm-mc-balance  `Σ_j Q_j ξ_eq,j(U_oc,T)=Q x̄`  [★박스]
- eq:sm-mc-vac 를 M_tot 로 나눔: `Σ (M_j/M_tot) ξ_j = 1-⟨N⟩/M_tot ≡ x̄`(추출 전하 분율).
- 자리마다 단위 전하 공통 ⇒ `Q_j=q_s M_j`, `Q=Σ Q_j=q_s M_tot` ⇒ `Q_j/Q=M_j/M_tot`.
- 양변 ×Q: `Σ Q_j ξ_j = Q x̄`. 평형(V=U_oc)에서 θ_j→θ_eq,j, ξ_j→ξ_eq,j; μ↔V 결선 = eq:sm-eqcond. ✓
- **eq:implicit 과 글자 일치 검산**: eq:implicit(ch2_sec05 line 16–19) = `\sum_j Q_j\,\xi_{\eq,j}(U_\oc,T) = Q\,\bar x`.
  박스 = `\sum_j Q_j\,\xi_{\eq,j}(U_\mathrm{oc},T)=Q\,\bar x`. 완전 일치. ✓
- x̄ 정합 검산: x̄=1-⟨N⟩/M_tot = 추출 분율 = 1-x(Li 함량 x=⟨N⟩/M_tot). Ch2 `x̄≡1-x`(ch2_sec05 line 14)와 일치. ✓
- §6 기원 검산: §6 은 `Q_cell q=Q_bg(V_n)+Σ_j Q_j ξ_j`. 박스는 faradaic 합 `Σ_j Q_j ξ_j`(=Q_cell q-Q_bg)의
  대정준 기원 — 배경 축전 몫 Q_bg 는 격자 삽입 밖이라 박스가 그 **faradaic 몫**의 기원임을 정확히 서술(과대주장 회피). ✓

### eq:sm-mc-fluc  `∂⟨N⟩/∂μ=β Σ_j M_j θ_j(1-θ_j)=β var(N)>0`  [payoff]
- `∂θ_j/∂μ`: θ_j=1/(1+e^{β(ε̃_j-μ)}); `∂θ_j/∂μ=β θ_j(1-θ_j)`(eq:sm-flucres `∂θ/∂(βμ)=θ(1-θ)` ⇒ ∂/∂μ 는 ×β). ✓
- `∂⟨N⟩/∂μ=Σ M_j β θ_j(1-θ_j)=β Σ M_j θ_j(1-θ_j)`.
- var(N): N=Σ_k n_k(전 자리). 자리 독립(평균장) ⇒ `var(N)=Σ_k var(n_k)=Σ_j M_j θ_j(1-θ_j)`
  (자리당 var(n)=θ(1-θ), eq:sm-flucres). ⇒ `∂⟨N⟩/∂μ=β var(N)>0`(0<θ_j<1). ✓
- **eq:sm-flucres 거시판임 검산**: 단일 자리 `var(n)=θ(1-θ)`(eq:sm-flucres)를 클래스마다 M_j 배 합한 것. ✓

### 유일근(솔버 존재·유일성) 통계 증명
- `∂⟨N⟩/∂μ>0` ⇒ ⟨N⟩(μ) 순증가. eq:sm-eqcond(`μ_Li=μ^0-sF(V-U)`, s=1) ⇒ μ_Li 는 V 에 순감소.
- 합성 ⇒ ⟨N⟩(V) 순감소 ⇒ 박스 좌변 `Σ Q_j ξ_eq,j=Q(1-⟨N⟩/M_tot)` 는 **U_oc 에 순증가**.
- ⇒ 고정 x̄∈(0,1) 에 U_oc 유일근. ✓ = ch2_sec08 line 51 "좌변이 U_oc 에 단조라 유일근" +
  ch2_appB `solve_U_oc` "유일근 솔버"에 통계역학 존재·유일성 근거 부여.

### verifybox 부호 읽기
- x̄↑(탈리튬화↑) ⇒ ⟨N⟩↓ ⇒ (eq:sm-mc-fluc 단조) μ↓ ⇒ (eq:sm-eqcond, s=1) V=U_oc↑. "추출↑ ⇒ 전위↑".
  §2.5 signbox(`V↑⇒ξ_eq↑`)와 합치. ✓

**전 식 재유도 무결 — 모순 0. 기존 수치·라벨·식 불변.**

---

## 3. 배치

- **파일**: `_sections/ch1_sec02b_part0.tex` 내부.
- **삽입점**: `sec:sm-electro`(§2.5)의 끝(signbox line 217–222 + fig:sm-occ line 224–278) **뒤**,
  `sec:sm-macro`(§2.6, line 280 `\subsection{거시 열역학으로...}`) **앞**.
  → 즉 현행 line 278(그림 끝) 과 line 280(§2.6 시작) 사이에 draft_q2o1.tex 전체를 삽입.
- **근거**: DIRECTION 후보 (i) 1순위("§2.6 sec:sm-macro 직전 신설 소절"). 단일 클래스 §2.3 →
  거시 §2.6 다리에 앉으며, μ↔V(§2.5 eq:sm-eqcond)를 받아 U_oc 반전을 읽어야 하므로 §2.5 **뒤**가 필수.
- **번호**: 새 `\subsection` → §2.6 이 §2.7 로 자동 밀림(LaTeX 자동 번호; 라벨 참조만 관리, rubric F1).
  기존 `\S\ref{sec:sm-macro}` 참조는 라벨 불변이라 자동 정합.
- **keybox 정책**: 본 소절은 keybox 0(Part 0 keybox 는 §2.6 말미 1개 유지 — 절당 keybox≤1, D1'). 박스=boxed 1 + verifybox 1.
- **그림**: 신규 그림 불요(fig:sm-occ 재사용 — §2.5 의 ξ_eq(V) 곡선이 반전의 시각).

### tab:notation 등재 필요(v1.0.21 반영 시)
- `M_j` 자리 클래스 크기 · `M_tot=Σ_j M_j` 총 자리수 · `ε̃_j` 클래스 j 유효 자리 자유에너지 ·
  `Ξ_{1,j}` 클래스 j 단일 자리 대정준 분배함수. (θ_j·ξ_j·N_p·x̄ 는 기존 등재/정의 — 재정의 일치.)
- `\oc` 매크로: 반영 시 `\newcommand{\oc}{\mathrm{oc}}` 를 ch1_preamble 에 추가하거나 `\mathrm{oc}` 유지.
- 신규 자산: `[V20-mc-01..04]`(draft 말미 주석).

### P3 검수 7항 대응
- 2항(전하 보존식=내부 전위 결정 중심식): 본 소절이 전하 보존식을 **대정준 제약 반전**으로 세워 중심식 지위 강화. OCV 읽기 회귀 아님.
- 3·4항(순환 의존성): 이 반전을 **"정의상 implicit formulation"(대정준↔정준 Legendre 반전)**으로 명확 분류 —
  self-consistent loop 진단에 기여(수치해법·논리공백·가정충돌 아님).
- 6항(Ch1↔Ch2 정합): 박스 = Ch2 eq:implicit 글자 일치, §6 faradaic 합 기원 — 충돌 0.
- 7항(ver↔Chapter): "Part 0"·"Chapter 1/2"·"§N6" 새 구조명만 사용, ver.N 역사명 미사용.

---

## 4. B — "Part 0 사다리" keybox 에 추가할 1항 문구

현행 keybox(ch1_sec02b_part0.tex line 320–327) 사슬의 `logistic~\eqref{eq:sm-logistic}` 와
`Nernst~\eqref{eq:sm-nernst}` **사이**에 다음 rung 1개를 삽입:

```
$\to$ 다클래스 전하 보존 반전~\eqref{eq:sm-mc-balance}
($\sum_j M_j\theta_j{=}\langle N\rangle$ 을 고정한 대정준 제약; 유일근 $\Leftarrow$ 요동 양성~\eqref{eq:sm-mc-fluc})
```

- 위치 근거: 반전이 logistic(§2.5)을 받아 U_oc 를 결정하고, 그 위에서 §2.6 Nernst 가 닫히므로 사슬 순서상 그 사이.
- 사슬 마지막 문장("본론이 결과로 쓰는 평형식의 전 유도가 이 사다리에 있다")은 전하 보존식까지 포함되도록
  자동 강화됨(별도 수정 불요).

---

## 5. C — 연결 참조 각 1문장 (재유도 금지·참조만; v1.0.21 반영 초안)

### C1 — Ch2 §2.5(`ch2_sec05_mixing.tex`, `ssec:overlap`, eq:implicit line 19 직후)
```
식~\eqref{eq:implicit} 의 통계역학적 기원은 Chapter 1 Part 0 의 다클래스 대정준 유도로, 거기서 이 음함수는
평균 입자수 $\langle N\rangle=\sum_j M_j\theta_j$ 를 고정한 대정준 제약의 정준 반전이며, 좌변이 $U_\oc$ 에
단조여서 유일근을 갖는 것도 입자수 요동 양성 $\partial\langle N\rangle/\partial\mu=\beta\,\mathrm{var}(N)>0$
으로 보증된다.
```
- Ch2 는 U_\oc 매크로 사용 가능(ch2_preamble). Ch1 은 이름 참조("Chapter 1 Part 0"), 분리 컴파일이라 \eqref 교차 금지.
- 재유도 아님 — 결과 관계만 명시(문건 관례 = ch1 line 313 "Chapter 2 의 식 (eq:Vxi)가 ... 재사용" 형식).

### C2 — ch2_appB(`ch2_appB_codemap.tex`, B.1 `solve\_U\_oc` 정의 line 18 또는 B.2 U_oc 기준행)
```
\code{solve\_U\_oc} 가 전제하는 유일근의 존재$\cdot$유일성은 Chapter 1 Part 0(다클래스 대정준 소절)이 입자수
요동 양성 $\partial\langle N\rangle/\partial\mu=\beta\,\mathrm{var}(N)>0$ 에서 음함수~\eqref{eq:implicit} 좌변의
$U_\oc$ 단조성으로 증명하므로, 솔버는 근 분리(bracketing) 없이도 단일근 수렴을 전제할 수 있다.
```
- 부록 B 는 함수명 노출 허용(codemap 전용). \eqref{eq:implicit} 은 Ch2 로컬이라 유효.
- 구현 함의(bracketing 불요)까지 명시해 codemap register("요구명세") 정합. 재유도 아님.

---

## 6. 자족 점검
- 분량 107행(60–110 준수). boxed 1 + verifybox 1. 인용 hill1960·mcquarrie1976 만.
- 새 물리 주장 0 — §2.3 확장 + eq:implicit/§6 식별 + eq:sm-flucres 거시화(전부 표준 통계역학·기존 문건 식).
- 근사 경계(클래스 간 staging 상관 배제 = 평균장 수준) 명시 — 과대주장 방지.
- 무통신 준수: comp_Q2_gcbalance/ 의 타 draft·NOTE 미열람.
