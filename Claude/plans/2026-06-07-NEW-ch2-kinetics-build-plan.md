# 신규 Chapter 2 (반응속도론) 작성 계획서 — Ch1 기반 백지 신규

> 재편 확정: old{1,3,4+2,5} → new{1,2,3,4}. 새 의존 트리 **1 → 2 → {3,4}**.
> 본 계획 = **new Ch2 = 흑연 음극 전이 반응속도론** (old Ch3 테마, Ch1만 기반). 발열(new3)·히스테리시스(new4)의 공통 keystone.
> ★ **기존 `graphite_ica_ch2.tex`(구 발열본) 제거·덮어쓰기 금지.** new Ch2 = **신규 파일**.
> 권위: 의존 트리 + Ch1(승인된 기반). **ver.N 포팅 금지, 발명 금지.**
> 방향 근거: `2026-06-07-ch2-recheck-ch3-direction-plan.md` PART B. 본 문서 = 그 PART B의 실행 계획.

---

## A. 작업 방식 (기존 방식 확인 — 박사님 sign-off 대상)

이번 신규 작성은 Ch1·구Ch2 에 적용했던 **검증된 작업 루프**를 그대로 따른다:

1. **계획서 우선 → GO 대기.** (본 문서가 그 계획서. GO 전 실행 0.)
2. **절 단위 실행 루프**: 절별 초안 → 자체 검수(물리·수학 무비약·Ch1 정합) → 직전 절·Ch1 정합 점검 → 저장. 문제 없을 때까지 반복.
3. **Codex foreground 적대 검수** (cross-model GPT, `--wait`, codex:codex-rescue): 핵심 gate 에서 부호 사슬·유도 정합·Ch1 정합·followability 검수, **MAJOR 0** 까지 정정. (Codex 판정도 source 직접 대조로 재확인 — 맹신 X.)
4. **Gate = 확인 가능 조건**(feedback_gate_design): 빌드 clean·undefined ref 0·overfull 0 / Ch2 본문 "Chapter 1 외 인용" 0(특히 구Ch2 발열 인용 0) / Ch1 환원식 명시 / followable(절별 ≤3단계) / 발명 0.
5. **Result ledger 저장**(anti-compaction 복구지점) — 매 단계 디스크에 박음.
6. **auto-commit+push** — 버전 바뀔 때마다(Anode_Fit 규칙). 내 산출물만 명시 스테이징(구Ch2·아카이브·zip 불혼입).
7. **소유권 보존**(P5): Ch1 식별자·라벨·식번호 불변, new Ch2 는 신규 라벨만(`eq:nch2_*` 또는 합의 prefix).
8. **빌드 검증**: xelatex 2-pass. 수식번호 `2.x`(new 기준), Ch1 인계식은 "식 (1.x)" 번호 지칭.
9. **cumulative step**: 본 계획 S100~ (이전 트랙과 충돌 회피용 신규 대역).
10. **멀티에이전트 필요 시 Agent 도구**(팝업 없음). Workflow 미사용(상시 지시).

→ **확인 요청**: 위 1~10 방식대로 진행하면 되겠습니까? (다르면 수정.)

---

## B. new Ch2 의 정체성·인계·산출물

- **정체성**: Ch1 이 진행률 완화를 \emph{단일 mobility $k$}로 거칠게 묶은 것을, 본 장이 **미시 forward/backward 반응속도론**으로 풀고 **전기화학(Butler--Volmer)으로 실현**한다. 발열(new3)·히스테리시스(new4)의 공통 기반.
- **인계 (Ch1만)**: $\mathcal A_j=s_{\phi,j}F(V-U_j)$ · $\Delta G_{\eff}=\Delta G_a-\chi\mathcal A_j$ · $k_j$ · 완화 $\dd\xi/\dd t=k_j(\xi_{\eq,j}-\xi_j)$ · $\xi_{\eq,j}$ logistic · $\dd\xi/\dd q$ · 세 전위($V_n/V_\app/V_{n,\OCV}$). **구Ch2(발열) 인용 0.**
- **하류가 받을 것(설계 제약)**:
  - new3(발열) ← forward/backward flux $J^\pm$ · 반응 과전압 $\eta_j$ · transition current $I_j$ (entropy production·소산열 기반).
  - new4(히스테리시스) ← 비평형 정상 target $\xi_\ss$ · 방향성 transfer coefficient $\beta$ · branch 비대칭 씨앗.
  → 이 둘이 **무엇을 본 장에 \emph{요구}하는지**가 내용 선정 기준. (ver.3 체크리스트 아님.)
- **산출물**: 신규 파일(파일명 = DG-1). 제목 "Chapter 2 — 흑연 음극 전이 반응속도론".

## C. new Ch2 구성 (절별 — 무엇을 세우고 왜)

> 서사 원칙: 각 절 "직전식/관찰 → 왜 필요 → 식(중간 대수 명시) → Ch1 환원·검산". disclaimer 는 boundbox 종속. followable.

| 절 | 내용 | Ch1 근거 / 하류 필요 |
|---|---|---|
| **서론** | "Ch1 은 $k$ 로 거칠게 묶었다 → $k$ 는 무엇인가? 본 장이 미시로 풀어 발열·히스테리시스의 기반을 만든다"는 한 줄 서사 + 전개 줄기 | — |
| **§1 기호와 규약** | Ch1 인계식 식번호 지칭 + 신규 기호($r^\pm$, $\beta$, $\xi_\ss$, $\eta_j$, $i_0$, $R_\ct$, $I_j$). 구Ch2 인계 0 | Ch1 |
| **§2 평형 위치 vs 동역학 속도의 분리** | $\xi_{\eq}=\xi_{\eq}(V_{\OCV})$(열역학)와 $k_j(\mathcal A_j)$(동역학)를 분리. 섞으면 중복 반영(reduced vs reaction-resolved 원칙) | Ch1 / 장 조직 원리 |
| **§3 forward/backward 분해 + Ch1 환원** | $\dd\xi/\dd t=r^+(1-\xi)-r^-\xi$ → $k=r^++r^-$, $\xi_\eq=r^+/(r^++r^-)$. **Ch1 완화식이 축약형임을 대수로 환원**(정합 검산). $k$=mobility(정·역 합) | Ch1 완화식 / 핵심 환원 |
| **§4 detailed balance** | 평형 net flux 0 → $r^+/r^-=\xi_\eq/(1-\xi_\eq)$. Ch1 logistic 대입 → $\ln(r^+/r^-)=(V_n-U_j)/w_j$ | Ch1 logistic |
| **§5 방향성 배리어(Level B)** | Eyring $r^\pm=\nu^\pm\exp[-(\Delta G_a^\pm\mp\beta\mathcal A)/RT]$. $\beta$=transfer coef=Ch1 $\chi$. ratio 가 $\mathcal A$ 의존, mobility 가 $\mathcal A$ 에 비대칭 응답. Ch1 $\chi\mathcal A$ 유효배리어와 연결 | Ch1 유효배리어 / new4 필요(β) |
| **§6 비평형 정상 target $\xi_\ss$** | $\dot\xi=0$ 일반해 $\xi_\ss=r^+/(r^++r^-)$. detailed balance 면 $\xi_\ss=\xi_\eq$ 환원; 이탈이 강구동·branch 씨앗 | new4 필요(ξ_ss) |
| **§7 전기화학 실현 — Butler--Volmer·반응 과전압** | 계면 charge-transfer 를 BV 로. **반응 과전압 $\eta_j$ 자체 정의**($\mathcal A_j=F\eta_j$ — 구Ch2 heat-force 아님). $i_j=i_0[\exp(\alpha F\eta/RT)-\exp(-(1-\alpha)F\eta/RT)]$. 저과전압→$R_\ct=RT/(Fi_0)$ | Ch1 𝒜_j / new3 필요(η, 소산) |
| **§8 교환전류 $i_0$·온도 의존** | $i_0(q,T)$, Eyring/Arrhenius rate prefactor. rate scale·온도 tail 의 기반 | new3 필요(T-tail) |
| **§9 전류 분배** | $I_j=Q_j\,\dd\xi/\dd t$, $I=I_\bg+\sum I_j$ (Ch1 전하보존 직접 미분) | Ch1 전하보존 / new3 필요(I_j) |
| **§10 하류 인계 명시** | new3 ← $J^\pm,\eta_j,I_j$ / new4 ← $\xi_\ss,\beta$. (forward-ref 1줄, 적층 disclaimer 아님) | — |

**조건부(서사/하류 필요 시에만, ver.3이라서가 아님)**: §7 의 Tafel 근사·대칭 BV sinh/asinh 역함수 — high-overpotential 영역이 new3 발열·new4 강구동에서 실제 필요하면 추가, 아니면 생략. (DG-2)

**의도적 배제(발명·범위 밖)**: Marcus/λ 정식 전개, dQ/dV 지문 표, nucleation/Avrami, generalized affinity $\mathcal A_{\resid}$, R_n 5-항 분해, C-rate 𝓕(·). (Ch1·하류가 본 장에 요구하지 않음.)

## D. 검증 Gate (확인 가능)

- **G-ch1-only**: new Ch2 본문 "Chapter 2(구 발열)/heat-force/reaction entropy/flux-force/entropy production" 인용 0. Ch1 외 인계 0. (grep)
- **G-reduction**: §3 에 Ch1 완화식 환원($k=r^++r^-$, $\xi_\eq=r^+/(r^++r^-)$)이 대수로 명시.
- **G-followable**: 각 절 직전식→식 ≤3단계, disclaimer boundbox 종속.
- **G-handoff**: §10 에 new3·new4 가 받을 양($J^\pm,\eta,I_j$ / $\xi_\ss,\beta$) 명시.
- **G-no-invent**: Marcus/dQ-지문/nucleation/𝓕 본문 0. (grep)
- **G-build**: xelatex 2-pass exit 0, undefined ref 0, overfull 0.
- **G-preserve**: 구Ch2.tex 무수정(mtime 불변), Ch1.tex 무수정.
- **G-codex**: Codex foreground 검수 MAJOR 0(부호·Ch1 정합·followability).

## E. Steps (cumulative S100~)

- S100: DG-1·DG-2 확정 + 작업방식(A) sign-off.
- S101: 신규 파일 골격(preamble·박스·수식번호 2.x·제목) + §1 기호와규약(Ch1 인계).
- S102: §2 분리 원리 + §3 forward/backward + Ch1 환원(핵심).
- S103: §4 detailed balance + §5 방향성 배리어(β=χ, Ch1 연결).
- S104: §6 ξ_ss + §7 BV·반응 과전압·R_ct.
- S105: §8 i_0·온도 + §9 전류 분배(Ch1 미분).
- S106: §10 하류 인계 + 서론 + 서사 패스(followable).
- S107: 빌드 + Codex foreground 검수 until MAJOR 0 + Gate 전수.
- S108: 커밋·푸쉬 + result ledger.

## F. Decision Gates (박사님 확정 — 실행 전)

- **DG-1 (신규 파일명)**: 구 `graphite_ica_ch2.tex`(발열) 보존 전제. new Ch2 파일명 — ① `graphite_ica_ch2_kinetics.tex`(권장, 명확) / ② 신규 트랙 폴더 `Claude/docs/new/graphite_ica_ch2.tex` / ③ 박사님 지정. (제목·수식번호는 "Chapter 2"·2.x 동일.)
- **DG-2 (전기화학 깊이)**: §7 에 Tafel·sinh/asinh 역함수 — ① 핵심(BV·R_ct·i_0)만, 나머지는 하류가 부르면 추가(권장) / ② 처음부터 포함.
- **DG-3 (작업방식 A)**: A 1~10 방식 그대로 / 수정.

## G. Risks
- R1(또 ver.3/구Ch2 유입): G-ch1-only·G-no-invent grep 으로 차단. R2(η_j 혼동): η_j=반응 과전압으로 §7서 자체 정의, 구Ch2 heat-force 절대 인용 X. R3(환원 누락): §3 Ch1 환원이 keystone gate. R4(구Ch2 훼손): G-preserve mtime 점검, 신규 파일만 작성.

## H. Correction History
- 2026-06-07: 최초. 재편 확정(old2→old4 통합, new{1,2,3,4}, 트리 1→2→{3,4}) 후 new Ch2(반응속도론) 신규 작성 계획. 작업방식 sign-off + 절별 구성/내용 상세. 구Ch2.tex 보존. DG-1~3 + 방식 확인 후 GO. 실행 안 함.
