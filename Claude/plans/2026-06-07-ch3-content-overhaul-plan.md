# Ch3 내용 전면 보완 계획서 (derivation·물리 심화)

> 대상: `Claude/docs/graphite_ica_ch3.tex` (전이 반응속도론). **형식(D2b)은 유지**, 부실한 **내용(유도·물리·워크드 예·dQ/dV 연결)**을 교과서 수준으로 보완.
> 진단 근거: 3-렌즈 멀티에이전트 감사(Ch2 기준 깊이격차 / 대학원 kinetics 완전성 / asserted-not-derived 전수). 44개 구체 보완점 도출.
> 경계: Ch4(일반 n_eff 발열)·Ch5(charge branch·ξ_ss≠ξ_eq)·Ch6(식별성·피팅)로의 기존 이연은 그대로 존중. 본 장은 그 forward 물리만 전개.

## 1. Summary

박사님 판정 "Ch3 내용 심각 부실(부실/skeleton)"은 정확하다. 진단 결과 Ch3는 **유도 결핍**이다: 23개 numbered 식 중 **완전 유도 8개**(3.5·3.6·3.7-8·3.9·3.12-13·3.14·3.18·3.19·3.26), **단언/미유도 12개**(3.2·3.4·3.10-11·3.15*·3.16·3.17·3.20·3.21·3.22·3.24·3.25). 분량은 Ch2와 줄당 식수가 비슷해 보이나, 그 분량의 ~40%가 "X≠Y≠Z" 구별·인계 정합 증명이라 **실제 유도 밀도는 붕괴**. 또 대학원 반응속도론 교과서가 갖춰야 할 핵심 물리(Marcus/λ·교환전류 물리·Tafel·농도 과전압·각 운동학 파라미터의 ICA/DVA 지문)와 **워크드 수치 예제(0개)·그림(0개)·계산순서·물리 capstone이 전무**. 본 장 서론이 약속한 "kinetics로 ICA 꼬리 설명"이 **본문에서 닫히지 않고** Ch5/Ch6로 떠넘겨져 있다. 보완 목표: Ch2 수준의 6-요소 전개(동기→단계 유도→검산→물리 해석→다리→유효범위) + 새 물리 + 워크드 예 + dQ/dV 회귀를 채워 **정합 증명서 → 교과서 章**으로 전환.

## 2. Scope / Targets

- 대상 1개: `graphite_ica_ch3.tex` (현 698줄, 14p). **Ch3 단독** (한 챕터씩 — 박사님 명시).
- 보존: 기존 D2b 형식(수식번호 3.x·기호규약 표·식 번호 지칭·박스 체계), 기존 8개 완전유도 식, 모든 라벨·기존 물리.
- 추가/심화: 아래 §5 target ToC. 정합 boilerplate(boundbox/verifybox 과잉)는 ~40%→~20%로 압축(삭제 아닌 응축).
- 불변 경계: charge branch·ξ_ss≠ξ_eq→Ch5 / 식별성·collinearity 해소→Ch6 / 일반 n_eff 발열 양정치→Ch4. 본 장은 각 주제의 forward 물리·극한·dQ/dV 신호만.

## 3. 진단 (무엇이 부실한가 — 3-에이전트 합의)

**3a. 유도 결핍 (asserted-not-derived) — 최우선 4종**
- (3.10-11) Eyring 비대칭 장벽 삽입: 장벽을 β_j𝒜 만큼 낮춘다를 유비로 단언, TST·지수 대수 안 보임. **본 장 미시 토대인데 미유도.**
- (3.15) n_eff=RT/(Fw_j): keystone인데 load-bearing 가정(C_j의 V_n-무의존)을 결과 뒤 boundbox로 강등. 물리 의미(n_eff<1 ⇔ 무질서) 1줄 단언.
- (3.16) 직렬 병목 1/r_obs=Σ1/r_k: "시간척도 합"으로 하완드, 왜 reciprocal이 더해지는지 정상상태 flux 논증 없음.
- (3.17) Butler-Volmer: "계면 변수로 옮기면"으로 r±→j_n 변환을 건너뜀. α_n=1-β_j가 그 안 보인 변환에 의존.

**3b. 누락/과소 물리 (대학원 교과서 기준) — P1~P10**
- P1 Marcus-Hush + 재구성에너지 λ: β의 물리적 기원(β=½(1+𝒜/λ))·역전영역·작동창 RT≲𝒜≪λ 정량화 — 현재 4줄 caveat.
- P2 교환전류 j₀(T,θ) 유도: r⁺=r⁻에서 j₀, θ≈½ 극대·plateau 끝 소멸 → R_ct(SOC) U자(관측 가능) — 현재 기호만.
- P3 BV 전 영역: Tafel b=2.303RT/(αF)≈118 mV/dec, linear→Tafel→transport 3영역, 데이터서 β 읽기 — 현재 linear만.
- P4 농도/수송 과전압: η_conc=(RT/F)ln(c_b/c_s)·한계전류 j_lim·Cottrell √t — 병목(transport/site/diffusion)을 4번 원칙으로 외치고 식 0개.
- P5 워크드 수치 예제: R_ct, n_eff←w_j, Tafel→α, Eyring ΔH‡ 등 ≥4-6개 — 현재 0개(Ch1은 25.7mV 등 다수).
- P6 ★ 각 kinetic 파라미터의 ICA/DVA 지문(j₀·β_j·n_eff·ΔH‡·R_ct → peak 높이/너비/꼬리/DVA 골) — **책의 핵심인데 Ch3는 dQ/dV에서 떠 있음.** Ch1 3×3 표의 운동학 판.
- P7 w_j 물리 기원: 사이트 에너지 분포 ⊗ logistic → w_eff>RT/F → n_eff<1 (Ch1 ρ_G 재사용).
- P8 nucleation/Avrami(staging 2상): logistic-완화 유효 범위 vs nucleation 필요 경계 명시 — 현재 종속절 1개.
- P9 극한영역 taxonomy: 가역/forward-dominated/Marcus inverted/transport-limited/instant 각 dQ/dV.
- P10 그림 6종(이중우물·BV·Tafel·Marcus 포물선·R_ct(SOC) U자·Eyring plot) — 현재 0개.

**3c. 구조 결함**
- 계산순서 section 없음 + 물리 capstone 없음 → 서론이 약속한 ICA 꼬리 closure가 §11에서 그냥 멈춤(Ch2는 §12 6-step loop + §13 thermal mirror로 닫음).
- (3.37) C-rate 꼬리 = 이름만 있고 정의 없는 함수 𝓕(·) — 가장 노골적 skeleton.
- Ch5/Ch6 forward-ref 과의존(≥5회 branch, ≥2회 식별성)으로 핵심 결과를 본문서 안 닫음.

## 4. 보완 접근 / 원칙

1. **Ch2 6-요소 전개**를 모든 신규/심화 항목에 적용: 동기(왜) → 단계 유도(중간 대수 명시) → 차원·극한 검산 → 물리 해석(말로) → 이전식 다리 → 유효범위 boundbox.
2. **asserted→derived**: 12개 미유도 식 중 본 장 소관(3.10-11·3.15·3.16·3.17·3.4·3.22·3.21)을 실제 유도로 채움. (Ch4/5/6 소관 deferral은 1줄 preview만 추가.)
3. **새 물리는 forward만**: 식별성·역피팅은 Ch6 경계 존중. Marcus·j₀·Tafel·농도과전압·dQ/dV 지문은 "정방향 예측 물리"라 본 장 소관.
4. **워크드 예·그림**: 수치는 search-first로 실측/문헌값 확인 후 삽입(λ·j₀·w_j 등 — 박사님 확인 대상). 그림은 TikZ(문서 내 렌더) 기본.
5. **boilerplate 응축**: §4 정합 증명·중복 boundbox(특히 §11이 §5 boundbox 3회 반복)를 압축, 그 자리를 새 물리로.
6. **소유권 보존**(P5): 기존 식별자·라벨·식번호·한글 표현 불변. 신규만 추가. 부분수정 시 원본 의미 보존.

## 5. Target ToC (보완 후 구조) + 항목별 작업

(기존=유지, [심화]=확장, [신규]=추가. Ch4/5/6 deferral 불변.)

```
서론                         [심화] ICA 꼬리=lag 비대칭 1문단 + j₀/Tafel/Marcus/dQ-dV arc preview
1. 기호와 규약               유지 (a_j^±·C_j·λ에 물리 1줄 부여)
2. 전위·과전압·구동력 계층화  [심화] (3.1)η_n 동기·검산, (3.2)n_eff "잠정 placeholder→§5.3서 고정" 명시,
                                   η̃-η split 인라인 유도(현재 forward-ref)
3. forward/backward·detailed balance  유지(강) + [신규]3.3 a_j^±=(1-ξ,ξ) 질량작용 인자 유도
4. Ch1 완화 ODE 정합          유지 but boundbox ~40% 응축
5. Level B                    유지 핵심
   5.1 방향성 장벽·rate ratio  [심화] (3.10-11) TST/BEP 지수 대수 명시 + 이중우물 그림
   5.2 [신규] Marcus-Hush·λ    ← P1: ΔG‡=(λ+𝒜)²/4λ, β=½(1+𝒜/λ), 역전·작동창, MHC vs BV, 워크드(λ≈?)
   5.3 n_eff=RT/(Fw_j)        [심화] C_j-독립 가정을 유도 본류로, V_n-미분 명시
   5.4 [신규] w_j 물리 기원    ← P7: 분포⊗logistic→n_eff<1, 워크드(w_j=?mV→n_eff)
   5.5 강구동 병목            [심화] (3.16) 정상상태 flux로 reciprocal 합 유도 + 2-병목 극한
6. 교환전류·BV 전 영역        ← P2,P3 (현 §6 확장)
   6.1 [신규] j₀(T,θ) 유도     ← P2: r⁺=r⁻→j₀, θ≈½ 극대→R_ct(SOC) U자
   6.2 small-signal·R_ct      유지(강)
   6.3 [신규] Tafel·전달계수 읽기 ← P3: b=2.303RT/αF, 워크드(118 vs 60 mV/dec)
   6.4 [신규] 3영역 종합·BV 유도 ← P3: (3.17)을 Level B서 유도(r±→j_n 변환 명시)+Tafel plot 그림
   6.5 R_n≠R_ct≠R_{n,eff}      유지(강)
   6.6 [신규] R_ct 워크드 예    ← P5
7. [신규] 농도·수송 과전압·한계전류  ← P4: η_conc·j_lim·Cottrell√t·병목 구성식
8. 전류 보존·transition current   유지(강) + r_curr 구성식을 §7과 연결
9. generalized affinity         유지 압축
10. R_n 전기화학 분해           유지 (η_conc/η_film에 §7 식 부여)
11. C-rate 재분해              [심화] (3.37) 𝓕(·) → §6/§7 식으로 ≥1개 정량 꼬리 유도(dominant balance)
12. 온도 의존 kinetics         유지(강) + [신규]12.2 ΔH‡ 워크드(2온도)
13. [신규] ★ 운동학 파라미터의 ICA/DVA 지문  ← P6 (책의 잃어버린 keystone): 표(features×params)+각 신호
14. [신규] 극한영역 taxonomy    ← P9: 각 극한의 dQ/dV
15. [신규] 계산순서·물리 capstone  ← 구조결함: kinetics→ICA 꼬리 closure(서론 약속 이행, Ch2 §12-13 판)
(그림 6종 P10은 해당 절에 분산)
```

## 6. Steps (cumulative; 이전 plan S53 이후)

- S54: 서론·§1·§2 심화(arc preview·η_n 동기·η̃-η 인라인·placeholder 명시) + §3.3 a_j 유도
- S55: §5.1 TST 지수 대수 + 이중우물 그림 / §5.3 n_eff 유도 본류화
- S56: §5.2 [신규] Marcus-Hush·λ (+워크드, +포물선 그림)
- S57: §5.4 [신규] w_j 물리 기원(+워크드) / §5.5 직렬병목 유도
- S58: §6 재편 — 6.1 j₀(θ) [신규] / 6.3 Tafel [신규] / 6.4 BV 유도+3영역(+Tafel·BV 그림) / 6.6 R_ct 워크드
- S59: §7 [신규] 농도·수송 과전압·한계전류 / §8·§10 병목 구성식 연결
- S60: §11 (3.37) 정량 꼬리 유도 / §12.2 Eyring 워크드
- S61: §13 [신규] ICA/DVA 지문 표 + §14 극한 taxonomy + §15 계산순서·capstone
- S62: boilerplate 응축(§4·중복 boundbox) / 전체 다리·register 정리
- S63: 빌드 + Codex foreground 검수(물리 정확성·부호·유도 정합) until clean
- S64: 커밋·푸쉬 + result ledger

(각 step = Ch2 6-요소 전개 준수. 신규 물리 식은 부호·차원·극한 검산 의무.)

## 7. Gates (확인 가능 조건)

- G-build: xelatex 2-pass exit 0, undefined ref/citation 0, Overfull hbox 0.
- G-derive: 본 장 소관 미유도 식(3.10-11·3.15·3.16·3.17·3.4·3.21·3.22)이 중간 대수 명시된 유도로 전환됨 — 식별자별 체크.
- G-physics-new: P1~P9 각 신규 항목이 (동기+유도+검산+물리해석+유효범위) 5요소 충족 — 항목별 체크리스트.
- G-numeric: 워크드 수치 예제 ≥4개, 각 출처(문헌/실측) 병기.
- G-dQdV: §13 지문 표 존재(features×params 부호/방향), 각 파라미터→peak 신호 1:1 매핑.
- G-figure: 핵심 그림 ≥4종 렌더(TikZ 또는 합의된 대체).
- G-closure: §15 capstone이 서론 약속(kinetics→ICA 꼬리)을 본문서 닫음(Ch5/Ch6 미루지 않음).
- G-preserve: 기존 라벨·식번호·완전유도 8식 불변, 신규만 추가.
- G-codex: Codex foreground 물리/부호 검수 MAJOR 0.

## 8. Decision Gates (박사님 결정 필요 — 실행 전)

- **DG1 (보완 범위)**: ① 전체(P1~P10 전부, 章 분량 대략 2배·그림 6·워크드 6 — 권장) / ② 핵심만(P1 Marcus·P2 j₀·P3 Tafel·P6 dQ/dV 지문 + 미유도 4종 + capstone) / ③ 최소(미유도 식만 채우고 신규 물리 없음). **권장 ①** — 박사님이 "전면 보완" 명시하셨으므로. 단 분량/시간 큰 차이라 확정 요청.
- **DG2 (그림)**: TikZ 소스(문서 내 렌더, 권장) / 서술형 placeholder / 생략.
- **DG3 (워크드 수치 출처)**: λ·j₀·w_j·Tafel slope 등 실값을 search-first로 문헌 확인 후 삽입(권장) vs 박사님 지정값 사용. 어느 쪽이든 본문엔 출처 병기.
- **DG4 (Marcus 깊이)**: β=½(1+𝒜/λ) 유도 + 역전영역까지(권장) vs λ 정의·작동창만.
- **DG5 (nucleation P8)**: 유효범위 경계 1개 subsection만(권장) vs Avrami 전개 포함 vs 전면 Ch staging으로 이연.

## 9. Risks

- R1(내용 추가가 부정확): 신규 물리 식의 부호·차원 오류 → 매 식 검산 의무 + Codex 물리 검수(S63).
- R2(과확장으로 register 이탈): 분량 2배 시 Ch2 톤 일탈 → 6-요소 템플릿 강제, boilerplate 응축으로 상쇄.
- R3(소유권 침해): 기존 식 변형 → 신규는 add-only, 기존 수정은 의미 보존·필요 시 GO 확인.
- R4(경계 침범): Ch4/5/6 소관을 본 장서 닫으려 함 → forward 물리만, deferral 1줄 preview 유지.
- R5(수치 환각): 워크드 값을 학습 기반 추정 → search-first 실값 확인, 미확인 시 "예시값(출처 필요)" 명시.

## 10. Validation

각 step 산출 직후 G-build·G-derive·G-physics-new 부분 점검. S63서 전 Gate 전수 + Codex MAJOR 0. 통과 전 커밋 금지. 보완 전후 diff로 기존 8 완전유도 식·라벨 불변 확인.

## 11. Correction History

- 2026-06-07 v0: 최초 작성. 계기 = 박사님 "Ch3 내용 심각 부실, 전면 보완" 지시 + 내 선행 오판("Ch3 rigorous→M7 skip") 정정. 3-렌즈 멀티에이전트 진단(깊이격차/완전성/asserted-not-derived 44항) 기반. 범위는 DG1서 박사님 확정 대기. **본 계획은 GO 전이며 실행하지 않음.**
