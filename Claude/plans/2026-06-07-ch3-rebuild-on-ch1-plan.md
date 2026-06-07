# Ch3 재구성 계획서 — Ch1 기반 전기화학 반응속도론 (v3, v1·v2 폐기)

> ★ v1(`...content-overhaul-plan.md`, Marcus 등 발명)·v2(`...faithful-to-ver3-plan.md`, ver.3 항목은 맞췄으나 의존구조 못 잡음) **모두 폐기**.
> **박사님 직접 지시 의존 구조**: `1기반2 · 1기반3 · 3기반4 · 3기반5`. 즉 **Ch3는 Ch1만 기반**(Ch2 아님). Ch4·Ch5가 Ch3 기반.
> 권위: 박사님 원천 ver.3(line 856–1118) + 의도 진단 `PHASE_DIAG_INTENT_GAP_RESULT.md`(8고리·장별 역할·N-1 서사·keystone).
> 원칙: ① Ch3는 Ch1만 인계(Ch2 의존 전면 제거). ② ver.3 전기화학 항목 충실. ③ **논리적으로 따라가지는 positive 서사**(disclaimer 적층 금지). ④ 발명 금지.

## 1. Summary

박사님 의도 의존 트리는 `Ch1 → {Ch2, Ch3}`, `Ch3 → {Ch4, Ch5}`. Ch3 = **Ch1의 진행률 동역학(ξ_j, dξ/dt=k(ξ_eq−ξ), 유효배리어 ΔG_eff=ΔG_a−χ𝒜)을 기반으로 전기화학 반응속도론(BV·i₀·Tafel·forward/backward·전류분배)으로 확장**하는 keystone 장이다. 그러나 현재 Ch3는 (a) **Ch2의 발열 framework에 기대고**(η_j를 Ch2 heat-force (2.29)로 import, reaction entropy (2.12)·R_{n,eff}·"두 구동력" 인용 12곳), (b) ver.3의 핵심 전기화학(Tafel·sinh/asinh·i₀(q,T)·모델선택)을 빠뜨리고, (c) Marcus 등 발명을 섞으려던 plan까지 더해, **박사님 의도와 의존구조부터 어긋났고 논리적으로 따라갈 수 없는** 상태다. 본 계획은 Ch3를 **Ch1 기반·ver.3 충실·followable**로 재구성한다.

## 2. 의존 구조 (박사님 직접 명시)

```
Ch1 (전하보존 V_n · ξ_eq logistic · 유효배리어 ΔG_eff=ΔG_a−χ𝒜 · 완화 dξ/dt=k(ξ_eq−ξ) · dξ/dq)
 ├─ Ch2  발열 확장성 검토        (1기반2)
 └─ Ch3  전기화학 반응속도론 ★    (1기반3)   ← 본 계획
      ├─ Ch4  반응속도론 기반 발열 (3기반4)
      └─ Ch5  충방전·히스테리시스  (3기반5)
```
- Ch3가 인계받는 것은 **오직 Ch1**: 𝒜_j=s_φF(V−U)·ΔG_eff·k_j·dξ/dt=k(ξ_eq−ξ)·dξ/dq·세 전위(V_n/V_app/V_OCV).
- Ch3는 **Ch2를 인계받지 않는다**. Ch2의 η_j(heat-force)·reaction entropy·R_{n,eff}·flux×force·"두 구동력" 인용 전면 제거.
- Ch3의 η_j = **반응 과전압**(ver.3: 𝒜_j=Fη_j, Butler-Volmer 입력). Ch2의 dissipation force와 무관하게 Ch1 𝒜_j + 전기화학으로 자체 정의.

## 3. 현재 Ch3의 문제 (3분류)

**3a. 의존구조 오류 (최우선 — Ch2 의존 제거)**
| 위치 | Ch2 의존 | 조치 |
|---|---|---|
| §1 포인터 L101-102 | reaction entropy (2.12)·flux×force (2.29)·(2.31) 인계 | 삭제(Ch1만 인계로) |
| §1 L105 + §2 L176 + §3 L249-253 | "Chapter 2 두 구동력 / heat-force η_j (2.29)" | 삭제·η_j를 반응 과전압으로 재정의 |
| 표 L126·L134 + §6 L508 | $\tilde\eta_j$ vs Ch2 η_j / R_{n,eff}(Ch2) | Ch2 비교 제거 |
| §7 L540 | double counting "Chapter 2 𝒜_j/F 분해" | Ch1/자체 근거로 |
| §8 L549·L569 | 시간미분 "식 (2.26) Ch2 동형" / coordinate shift | Ch1 전하보존 직접 미분으로 |

**3b. ver.3 항목 누락/부실 (복원)** — Tafel·대칭 BV sinh/asinh 역함수·교환전류 i₀(q,T) 조성의존 f_{i,j}(q)·reduced/reaction-resolved/Hybrid 모델선택. (v2 plan 대조표와 동일.)

**3c. 논리 followability (N-1 서사)** — 현재는 "X≠Y≠Z 구별" disclaimer 적층(hygiene manual). 필요한 것은 **Ch1 완화식 → 전기화학 일반화 → BV/Tafel/i₀/forward-backward → ξ_eq=k⁺/(k⁺+k⁻)로 Ch1 환원**의 한 줄 서사로 따라가짐. (PHASE_DIAG N-1.)

**3d. 발명물 폐기** — Marcus/λ·dQ/dV 지문 표·nucleation·극한 taxonomy·그림(v1). 추가 안 함. rebuild-bloat(generalized affinity 𝒜_resid·R_n 5분해·C-rate 𝓕)는 Ch2 의존 정리와 함께 축소/제거 검토(DG).

## 4. 접근

- **재구성 기준**: Ch1 인계식 + ver.3 전기화학 항목. 현재 Ch3에서 Ch1 기반으로 살아있는 부분(forward/backward·relaxation 환원·BV→R_ct·전류보존)은 유지, Ch2 의존부는 들어냄, ver.3 누락분 복원.
- **서사 우선**: 각 절이 "관찰/직전식 → 왜 이게 필요 → 식 → 환원/검산"으로 따라가지게. disclaimer는 boundbox로 종속.
- **Ch1만 인계**: η_j·𝒜_j·detailed balance를 Ch1 𝒜_j와 BV로 자체 정의. Ch2 언급 0.

## 5. Ch3 target 구조 (Ch1→전기화학, ver.3 순서)

```
서론        Ch1 완화 동역학에서 출발, 전기화학 반응속도론으로 확장하는 한 줄 서사
1. 기호와 규약   Ch1 인계식만(𝒜_j, ΔG_eff, k_j, dξ/dt, dξ/dq, 세 전위). Ch2 인계 0.
2. 평형/속도 분리 + 전위 보조 구동력 일반화   ξ_eq=ξ_eq(V_OCV) vs k_j(𝒜_j); 𝒜_j=s_φF(V_app−U) → 𝒜_j=Fη_j(반응 과전압); ΔG_eff=ΔG_a−χFη_j; 중복반영(reduced vs reaction-resolved) note
3. Butler–Volmer식과 η_j        i_j=i₀[exp(αFη/RT)−exp(−(1−α)Fη/RT)]
   3a 저과전압 선형 → R_ct=RT/(Fi₀)      (현행 유지·Ch1근거)
   3b [복원] 대칭 BV 역함수 sinh/asinh    η=(2RT/F)asinh(i/2i₀), ΔG_eff=ΔG_a−2χRT·asinh
   3c [복원] Tafel 근사                  η≈(RT/αF)ln(i/i₀), ±branch 부호
4. [복원] 교환전류밀도 i₀(q,T)           i₀=i₀,ref f_{i,j}(q)exp[−E_i/R(1/T−1/T_ref)]; ν_j(T); 상관 경고
5. forward/backward rate              dξ/dt=k⁺(1−ξ)−k⁻ξ; k±=ν±exp[−(ΔG_a±∓χ±𝒜)/RT]; relaxation 환원 → ξ_eq=k⁺/(k⁺+k⁻)=Ch1, k_relax=k⁺+k⁻ (★Ch1 환원이 keystone)
6. 전류 분배                          I_j=Q_jdξ/dt, I=I_bg+ΣI_j (Ch1 전하보존 직접 미분)
7. [복원] 모델 선택                    reduced/reaction-resolved/Hybrid 3-모델 표
8. 온도 의존(Eyring ΔH‡/ΔS‡)          현행 유지(Ch1 Eyring 근거)
(식별성·피팅절차 = DG2 / detailed balance·Level A·B·n_eff = DG3)
```

## 6. Steps (cumulative; S65~)

- S65: DG1~DG3 박사님 확정.
- S66: §1·§2 재정의 — Ch1만 인계, η_j=반응 과전압, Ch2 인계 12곳 제거.
- S67: §3 BV 골격 + 3a(R_ct) Ch1 근거로 재서술.
- S68: 3b sinh/asinh + 3c Tafel 복원(ver.3 원식).
- S69: §4 i₀(q,T) 복원, §5 forward/backward + Ch1 환원 서사 강화.
- S70: §6 전류분배(Ch1 직접 미분), §7 모델선택 표 복원.
- S71: 서사 패스(절별 positive 흐름), (DG 결과) 식별성·rebuild-bloat 정리.
- S72: 빌드 + Codex(Ch1 정합·ver.3 정합·부호·followability) until clean.
- S73: 커밋·푸쉬 + ledger.

## 7. Gates

- **G-ch1-only**: Ch3 본문 "Chapter 2 / (2.x) / ch2_" 인용 0 (grep). η_j가 반응 과전압으로 자체 정의됨.
- **G-ver3-fidelity**: Tafel·sinh/asinh·i₀(q,T) f_{i,j}(q)·3-모델 표 복원(grep + 식 대조).
- **G-followable**: 각 절이 직전식/관찰에서 ≤3단계로 이어짐(Observation Anchor); disclaimer는 boundbox 종속.
- **G-ch1-reduction**: forward/backward → ξ_eq=k⁺/(k⁺+k⁻)=Ch1 환원이 본문 명시(keystone).
- G-no-invent: Marcus/dQ-지문/nucleation 부재.
- G-build: exit 0, undefined ref 0, overfull 0.
- G-codex: MAJOR 0.

## 8. Decision Gates (박사님 결정 — 실행 전)

- **DG1 (재구성 vs 외과수술)**: Ch3의 Ch2 의존·누락·서사 문제가 깊어 ① **Ch1+ver.3 기반 재구성**(권장, 깔끔) / ② 현행 surgical 수정(Ch2 의존만 들어내고 복원). 박사님 선택.
- **DG2 (식별성·피팅, ver.3 §8·§9)**: Ch3 복귀(ver.3 원안) / Ch6 유지(현재).
- **DG3 (rebuild-bloat 거취)**: detailed balance·Level A/B·n_eff = CHARTER 합의(유지 기본). generalized affinity 𝒜_resid·R_n 5분해·C-rate 𝓕 = 유지/축소/제거.
- **DG4 (Ch4·Ch5 의존 수정)**: Ch3 확정 후 Ch5(현재 Ch4 기반)를 **Ch3 기반**으로, Ch4를 **Ch3 기반**으로 동일 교정. (별도 phase)

## 9. Risks
- R1(Ch2 제거가 Ch1 근거 공백 유발): η_j·전류미분을 Ch1 𝒜_j·전하보존으로 자체 유도해 메움. R2(식 이식 오류): ver.3 대조+Codex. R3(또 발명): G-no-invent. R4(서사 과욕으로 내용 손실): 식·물리 보존, prose만.

## 10. Validation
각 step G-ch1-only·G-ver3-fidelity 부분점검. S72 전 Gate + Codex MAJOR 0 + Ch1/ver.3 대조 전수. 통과 전 커밋 금지.

## 11. Correction History
- 2026-06-07 v3: v1·v2 폐기. 계기 = 박사님 직접 의존구조 명시(`1기반2·1기반3·3기반4·3기반5`) + "Ch3가 Ch2 기반으로 잘못 구현됨, 논리 못 따라감" 지적. 의존구조·ver.3·서사 3중 교정. DG1~DG4 박사님 확정 대기. 실행하지 않음.
