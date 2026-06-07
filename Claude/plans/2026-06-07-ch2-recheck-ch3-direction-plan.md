# Ch2 재검토 + Ch3 작성 방향 계획서 — 의존 트리 단일 기준 (v4, 이전 Ch3 plan 전부 폐기)

> ★ 폐기: `...ch3-content-overhaul`(v1, 발명) · `...ch3-faithful-to-ver3`(v2) · `...ch3-rebuild-on-ch1`(v3, ver.3 anchor 잔존).
> **유일 권위 = 박사님이 직접 주신 의존 트리.** ver.3·ver.5·RB ledger·CLAUDE.md P1 의 적층서술은 **권위 아님**(박사님: "기존 ver.3도 내가 제시한 게 아니다, 지금 버전은 거기서 탈피해 완전히 새로 쓰는 중"). 따라서 **ver.N 내용을 가져오지 않는다.** 추론은 **의존 트리 + Ch1(승인된 기반)** 에서만.
> 본 문서 = \emph{방향성} 계획. 실행 전 박사님 확정(DG) 대기.

## 0. 의존 트리 (단일 진리)

```
            Ch1  (전하보존 → V_n · ξ_eq logistic · 유효배리어 ΔG_eff=ΔG_a−χ𝒜 · 완화 dξ/dt=k(ξ_eq−ξ) · dξ/dq · ICA/DVA · tail)
            ├── Ch2   (1기반2)
            └── Ch3   (1기반3)  ★keystone
                  ├── Ch4   (3기반4)
                  └── Ch5   (3기반5)
```
**해석 규칙(전 장 공통)**: 각 장은 \emph{자기 부모의 결과만} 인계한다. 형제 장(예: Ch2↔Ch3, Ch4↔Ch5)을 인계하지 않는다. 부모가 정의하지 않은 개념을 본문에서 쓰면 그건 \emph{그 개념을 정의하는 장의 자식}으로 가야 한다.
- Ch2 가 쓸 수 있는 것 = Ch1 결과뿐. **kinetics(forward/backward·detailed balance·entropy production·k_eff·BV) 사용 불가** — 그건 Ch3 소관.
- Ch3 가 쓸 수 있는 것 = Ch1 결과뿐. **Ch2(발열·heat-force) 인용 불가.**
- Ch4 = Ch3(kinetics) 기반 발열. Ch5 = Ch3(kinetics) 기반 히스테리시스.

---

# PART A. Ch2 재검토 (1기반2) — 방향성 맞는가?

## A1. Ch2 가 Ch1만으로 \emph{도출 가능}한 범위 (정당)
- **가역열**: 평형 전위 온도계수 $(\partial V_{n,\OCV}/\partial T)_q$ → Bernardi 가역열. (Ch1 전하보존식의 온도 미분만으로 닫힘. kinetics 불필요.)
- **reduced 비가역열**: $\dot{\mathcal Q}_\irr=|I|\eta$, 단 $\eta=V_\app-V_{n,\OCV}=s_I|I|R_n$ (Ch1 $R_n$). 즉 $I^2R_n$ 수준. (Ch1 $V_\app$ 정의만으로 닫힘.)
- **열원 분해 framework**: 가역(entropic)/비가역(dissipative)/배경 의 \emph{구조·차원·연결}만.
- **background heat** (Ch1 $Q_\bg$), **ICA 꼬리의 열적 신호**(Ch1 lag tail; 단 rate 의존부 점검).

## A2. 현재 Ch2 의 \emph{침범} (Ch3 kinetics 필요 → Ch4 소관인데 Ch2에 있음)
grep 증거: entropy production/flux-force **23회**, forward/backward $r^\pm$ **6회**, k_eff/Eyring **5회**, charge-transfer/BV **2회**.
| 현재 Ch2 위치 | 침범 내용 | 정당 소관 |
|---|---|---|
| §8.1 flux--force entropy production ($\sum J_jF\eta_j$, $r^\pm$) | forward/backward flux 필요 | **Ch4** (3기반) |
| §8.3 $\sigma_j=g''_jk_j^{\eff}r_j^2/T$ | k_eff·rate·국소평형 필요 | **Ch4** |
| §8.4 $R_n$ charge-transfer 분해 | BV/$R_\ct$ 필요 | **Ch3 정의 후 Ch4** |
| §3.2 Eyring activation entropy $\Delta S_{a,j}$ split | Eyring rate 필요 | **Ch3/Ch4** |
| "두 구동력 $\mathcal A_j$(중심) vs $\eta_j$(국소)" 프레이밍 | Ch3 가 정의할 개념 | **Ch3** |

## A3. 판정 (4-tier)
- **확정**: Ch2 의 \emph{가역열}(OCV 온도계수·Bernardi·background·decomposition framework)은 Ch1만으로 도출 = 방향 맞음.
- **확정(이탈)**: Ch2 의 \emph{미시 비가역열}(flux-force·$\sigma_j$·rate 기반, 23회)은 Ch1로 도출 불가 = **Ch4 영역 침범**. 의도(Ch2=Ch1 상태변수로 가역/비가역열 \emph{차원·연결만}, 확정은 Ch3-4)와 어긋남.
- **추정**: 현재 Ch2 가 "교과서 양식상 충분"해 보였던 건 \emph{Ch4 내용을 당겨와 채웠기} 때문 — 즉 부피는 찼으나 \emph{의존 트리 위반}.

## A4. Ch2 수정 방향 (DG-A 확정 시)
1. **유지·강화**: 가역열 라인(§2 OCV 온도계수 → §5 가역열 OCV → §6 가역열 ξ → §7 background). 이건 Ch1 기반 정당.
2. **scoping 으로 축소**: 비가역열은 **reduced $I^2R_n=|I|\eta_{\mathrm{red}}$ 수준 + 차원·연결 진술**까지만. 미시 전개(flux-force·$\sigma_j$·entropy production·rate 기반 §8.1/8.3/8.4)는 **Ch4 로 이관**.
3. **Ch3 개념 제거**: "두 구동력 중심/국소", Eyring activation entropy split, charge-transfer 분해 — Ch2 에서 빼고 해당 장으로.
4. **재명명 점검**: §11 열적거울이 Ch1 lag tail 기반이면 유지, kinetic rate 의존이면 Ch4 표지.
→ 결과: Ch2 = "Ch1 상태변수로 \emph{가역열을 확정}하고 \emph{비가역열은 scoping}하는 장" (의도 정합).

---

# PART B. Ch3 작성 방향 (1기반3) — 어떻게 써야 하나

## B1. 인계 (Ch1만)
$\mathcal A_j=s_{\phi,j}F(V-U_j)$ · $\Delta G_{\eff}=\Delta G_a-\chi\mathcal A_j$ · $k_j$ · 완화 $\dd\xi/\dd t=k_j(\xi_{\eq,j}-\xi_j)$ · $\xi_{\eq,j}$ logistic · $\dd\xi/\dd q$ · 세 전위($V_n/V_\app/V_{n,\OCV}$). **Ch2 인용 0.**

## B2. Ch3 의 역할 (keystone)
Ch1 은 완화를 \emph{단일 mobility $k$}로 거칠게 묶었다. Ch3 = 그 $k$ 를 \textbf{미시 반응속도론으로 풀어}, Ch4(발열)와 Ch5(히스테리시스)가 동시에 쓸 기반을 만든다.
- Ch4 가 받을 것: forward/backward flux + 구동력(반응 과전압) → entropy production 발열.
- Ch5 가 받을 것: 비평형 정상 target $\xi_\ss(\ne\xi_\eq)$ + 방향성 배리어 $\beta$ → branch 비대칭.

## B3. 작성 서사 (Ch1에서 출발, \emph{따라가지는} positive 흐름)
의도 진단(N-1)의 핵심: 현재 장들은 "X≠Y≠Z" disclaimer 적층(hygiene manual)이라 \emph{따라갈 수 없다}. Ch3 는 다음 한 줄 서사로 쓴다:

1. **질문 제기**: Ch1 의 $k$ 는 무엇으로 이루어졌나? (완화 = 평형으로 가는 단일 속도 — 그 내부를 본다.)
2. **정/역 분해**: $\dd\xi/\dd t=r^+(1-\xi)-r^-\xi$. → $k=r^++r^-$, $\xi_\eq=r^+/(r^++r^-)$. \textbf{Ch1 완화식이 이 축약형임을 보임}(환원 = 정합 검산).
3. **detailed balance**: $r^+/r^-$ 를 Ch1 logistic $\xi_\eq$ 에서. ($\ln(r^+/r^-)=(V_n-U_j)/w_j$.)
4. **방향성 배리어(Level B)**: $\mathcal A_j$ 가 $r^\pm$ 에 \emph{비대칭} 진입(transfer coefficient $\beta=\chi$). Ch1 의 $\chi\mathcal A$ 유효배리어와 연결. → mobility 의 $\mathcal A$-응답.
5. **비평형 정상 target** $\xi_\ss=r^+/(r^++r^-)$ ($\ne\xi_\eq$ 일반): Ch5 분기의 씨앗.
6. **전기화학 실현**: 계면 charge-transfer 를 Butler-Volmer 로 — 정/역 kinetics 의 계면 형태. $R_\ct$ = 소신호 한계. (반응 과전압 $\eta_j$ 를 \emph{여기서} 자체 정의 — $\mathcal A_j=F\eta_j$, Ch2 heat-force 아님.)
7. **전류 분배**: $I_j=Q_j\,\dd\xi/\dd t$, $I=I_\bg+\sum I_j$ — Ch4 가 쓸 transition current. (Ch1 전하보존 직접 미분.)
8. **인계 명시**: Ch4(forward/backward + $\eta$ → entropy production), Ch5($\xi_\ss$ + $\beta$ → branch).

## B4. 작성 원칙 (제약)
- **Ch2 인용 0**(grep gate). $\eta_j$=반응 과전압(Ch1 $\mathcal A_j$ 기반), heat-force 아님.
- **ver.N 식 강제 안 함**: Tafel·sinh/asinh·$i_0(q,T)$ 등을 "ver.3에 있으니" 넣지 않는다. **Ch1에서 자연히 따라오고 Ch4/Ch5가 실제로 필요로 하는 것만** 포함. (필요 판단은 B2 의 "Ch4·Ch5가 받을 것"으로.)
- **발명 0**: Marcus/λ·dQ/dV 지문 표·nucleation·그림 등 추가 안 함.
- **followable gate**: 각 절 "직전식/관찰 → 왜 → 식 → 환원·검산". disclaimer 는 boundbox 종속.
- **소유권 보존**(P5): 기존 식별자·라벨 유지, 신규만 add.

## B5. Ch3 작성 = 재작성 vs 교정 (DG-B)
현재 Ch3 는 (a) Ch2 의존 12곳, (b) "두 구동력" 등 Ch2 프레이밍이 \emph{뼈대}에 박혀 있어 부분 제거가 어렵다. 두 길:
- ① **Ch1 기반 백지 재작성**(권장): B3 서사로 새로 써내려감. 현 Ch3 의 Ch1-기반 검증식(정/역·환원·BV·전류보존)은 재료로 재사용.
- ② surgical 교정: Ch2 의존만 들어내고 서사 보강.

---

# PART C. Decision Gates (박사님 확정 — 실행 전)

- **DG-A (Ch2 방향)**: A3 판정 수용 시 — Ch2 를 "가역열 확정 + 비가역열 scoping(미시는 Ch4 이관)"으로 축소하는 방향이 박사님 의도와 맞는가? ① 맞음(Ch2 축소·Ch4로 이관) / ② Ch2 가 비가역열까지 다뤄야 함(그렇다면 Ch2 의 kinetics 의존은 어디서 정당화? — 트리 재논의).
- **DG-B (Ch3 작성)**: ① Ch1 기반 백지 재작성(권장) / ② surgical 교정.
- **DG-C (테마 확인)**: 장 테마 — Ch2=발열·Ch3=반응속도론·Ch4=반응속도론 기반 발열·Ch5=히스테리시스 — 이 유지가 맞는가? (트리는 의존만 규정, 테마는 별개 — 박사님 확인.)
- **DG-D (순서)**: Ch2 재검토와 Ch3 작성 중 무엇 먼저? (Ch4·Ch5 의존 교정은 Ch3 확정 후.)

## D. 다음 (DG 확정 후 별도 실행 계획)
- DG 확정 → Ch2 수정 실행계획 / Ch3 작성 실행계획 각각 11-section 으로 분리 작성 → GO → 실행.
- Ch4(←Ch3)·Ch5(←Ch3) 의존 교정은 후속 phase.

## Correction History
- 2026-06-07 v4: v1~v3 폐기. 계기 = 박사님 "ver.3 내 것 아님·현 버전은 탈피해 새로 씀·의존 트리만 진짜·Ch2도 의도 반영 의심" + "Ch2 재검토 방향 + Ch3 작성 방향 세세히". ver.N anchor 완전 제거, 의존 트리+Ch1 단독 추론. Ch2 = Ch4 영역 침범(flux-force 23회) 적발. 방향성 문서이며 DG-A~D 확정 전 실행 안 함.
