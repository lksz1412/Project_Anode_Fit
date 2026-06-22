# PHASE V5RR RESULT — Ch1 v5 전면 재검토 (v3 기준·수식별 루핑)

> 마스터 = `Claude/plans/2026-06-22-ch1-v5-comprehensive-rereview-MASTER.md` · baseline = `V5RR_baseline_map.md` · ledger = `PHASE_V5RR_EXECUTION_LEDGER.md`. 기존 `PHASE_V5_*` 불가침(본 문건은 별도 신설 — [[feedback_document_protection_addendum_pattern]]).

## 1. 목표·범위
v3(Fable, 동결 기준) 대비 v4·v5 변동을 물리·화학·수리적으로 빡세게 재검증하고 수식-구동 v5 의 완성도를 높인다. 검수 = **절별 루핑 + ★수식별 루핑**(식 N ↔ 관련 모든 선행식). §1.18 배제. 편집 = v5.tex 만(v3·v4 불가침).

---

## Phase R0 — Baseline & 식 의존 그래프 (완료)

### 수행
- master 직접: §1.1 기호표·§1.4 평형유도 spine(1.19~1.27)·overfull 2영역 정독.
- 매핑 sub(병렬 1, v5·v3 전문 217k tok): 식 대응표·★의존 그래프·변동 인벤토리 산출.
- master spot-check: §1.4 9개 의존 edge 전부 본문 \eqref 일치 ✓.

### Read Coverage
v5 §1.1(L233–285)·§1.4(L499–600)·§1.8 OF1(965–994)·§1.17 OF2(1825–1854) master 직접 + 매핑 sub v5/v3 전 범위.

### 산출
`V5RR_baseline_map.md`(빌드결함·누출점검·97식 대응·의존그래프·변동인벤토리·약점3), 본 RESULT, ledger, R0 plan.

### 확정 결과 (4-tier: 확정)
- **97/97 numbered 식 v3↔v5 verbatim 동일**(부호·항·계수·변수명·번호 차이 0). v5 변형 = 산문 압축(~32%)뿐.
- **§1.18 누출 0**(grep 2중 + 기호표 확인 — ψ/B/κ/ξ_c/stacking 행·토큰 부재).
- 누락(numbered 식·boxed·표·figure·코드) 0.
- **의존 그래프 97식 완성**(근본 정의식 9 + 준정의 2). R2 식별 단위 확보.
- **빌드 결함 = Overfull 2**(OF1 §1.8 L979–981, OF2 §1.17 L1836–1840) — R1 착수 시 봉합 예정. (직전 V5 "overfull 0 수렴" 주장이 R8 이후 거짓이 된 것 확정.)

### 약점 3곳 (완성도 제고 타깃, R2/R3)
(1.95)dHeff 고립 노드 · (1.75)xidecomp 정의 다리 무번호 · (1.83)Ifuse L_V 다리 무번호. 셋 다 v3≡v5 공통이나 수식-구동 표방을 깸 → 명시 다리식 승격 검토.

### 4-tier
- 근거 미발견(결함 아님): 식 변형·누락·§1.18 누출 — 0.
- 추정: 승격 "5개"의 정밀 매핑(②③ 등) — R2 확정 예정.
- 미검증: 식별 (i)~(iv) 물리·화학·수리 적대 재유도(R2 본작업).

### Gate R0 = PASS
97식 대응·선행식 배정 완료(미배정 0) · 빌드 결함 목록화 · §1.18 누출 0 · baseline_map 생성.

---

## Phase R1 — 절별 루핑 (완료)

### 수행
- master: overfull 2건 봉합(OF1 §1.8 긴 연쇄율 인라인식 분리·OF2 §1.17 — emergencystretch=2em + 분수 분리) → overfull 0.
- 검수 sub ×5 병렬: A(§1.1–1.3)·B(§1.4–1.5)·C(§1.6–1.8)·D(§1.9–1.12)·E(§1.13–1.17), 각 head→tail 정독, 렌즈=물리·화학·수리 건전성+v5↔v3 보존+절내 정합·G-follow. v3 대조.
- master 삼각검증 → 확정 수정만 직접 반영.

### Read Coverage
v5 §1.1~§1.17 전 범위(5 sub 분담 head→tail) + v3 동일 절 대조. master 직접: 봉합 영역·§1.5 Ω·§1.15 dHeff·§1.12 Ifuse.

### 확정 결과 (4-tier: 확정)
- **물리·화학·수리 오류 0** (5 sub 공통: 97식 verbatim 보존 덕, 부호·차원·극한·임계멱 3/2·수치 dU_hys 54.8mV 전부 재검산 통과). 손실은 전부 산문 다리(동기·인과절·forward-pointer)에 집중 — 대부분 v5 "수식-구동" 장르의 의도된 압축.
- **수정 4건 적용**:
  1. OF1/OF2 봉합 — 빌드 overfull 0 회복(직전 V5 R8 유입분).
  2. §1.8 L981 — 봉합 dash 중첩(`—...—`)을 괄호로(가독성, 의미·수식 불변).
  3. (1.95)dHeff L1547 — χ_d 정의에 `(식 eq:chisum 합-1)` cross-ref 추가(수식-follow 고립 해소).
  4. (1.83)Ifuse L1281 — L_V=|dV/dq|L_q 다리에 `(식 eq:tail)` cross-ref(번호 추적성).

### 삼각검증서 기각한 sub 지적 (빈 통과 방지)
- **§1.5 L607 "뒤집으므로 오타"(sub B 확정 주장) → 기각**: "뒤집-"+"-으므로"는 정문법, 해당 줄에 `+Ω(1−2θ)`·`−Ω(1−2ξ)` 부호전환 이미 둘 다 표기(보조식 소실 아님). master 직접 본문 확인.

### 비수정 (4-tier: 추정/의도 — D2)
- §1.3 keybox 절-마무리 다리 제거(sub A) — v5 "산문 다리 DROP" 장르의 의도된 압축. 복원 시 장르 위배 → 비수정.
- §1.2 fig:barrier caption 𝒜=0.39 vs TikZ 주석 A=0.35(sub A) — v3 계승·비렌더(PDF엔 caption 0.39만 표시) → 추정, 사용자 보고. v3 동결이라 v5 단독수정 부적절.
- §1.9 line~1005 무번호 equation* 승격(sub D) — v5 설계의 "산문-only 유도단계 명시 승격"(의도). 수치 정확.
- 다수 forward-pointer·인과절 압축(sub B/C) — 수식 사슬 자체는 닫힘, 의도된 압축.

### Gate R1 = PASS
build_gate Opus_v5 0/0/0 40p · comment_gate 15/15 · overfull 0 회복 · 절별 보존 감사 PASS(물리오류 0).

---

## Phase R2 — ★수식별 루핑 (완료, 사용자 핵심)

### 수행
- 식 97개를 의존 클러스터 7로 분담. Wave A(C1 1.1–1.18·C2 1.19–1.32·C3 1.33–1.51·C4 1.52–1.63) + Wave B(C5 1.64–1.74·C6 1.75–1.83·C7 1.84–1.97) = 검수 sub 7 병렬. 각 식을 **의존집합 전체에 대해 (i)물리 (ii)화학 (iii)수리(대수 한 단계·부호·차원·극한) (iv)선행식 정합** 적대 재유도(다수 sub가 SymPy/Python 독립 검산 동반).
- 교차모델 Codex(codex:rescue, 히스 1.84–1.97 부호) 시도 → **Windows 샌드박스 오류(740 CreateProcessAsUserW)로 파일 접근 실패**. C7 Claude sub가 수치+해석 양면 재유도로 동일 범위 커버 → in-model 삼각으로 대체(교차모델은 이번 미가동, 정직 기록).

### 확정 결과 (4-tier: 확정) — ★유도 오류 0
- **식 (1.1)~(1.97) 전부 (i)~(iv) 4축 PASS. 물리·화학·수리 유도 오류 0건.** 핵심 재검산 통과:
  - 과거 codex 의심처 **전자 일 −FV 부호(1.14→1.18 eqcond)** — s=+1·z=−1 규약서 flip 없이 정합(C1, SymPy).
  - 평형 심장부(BV→detailed balance χ 상쇄→정지점→logistic) round-trip 닫힘(C2, SymPy).
  - g(ξ)·공통접선·spinodal ξ_s±=½±½√(1−2RT/Ω)·Ω/2RT 3-case(C3, 수치 binodal 0.0707/spinodal 0.2113).
  - 꼬리 사슬 기억적분·연쇄율 다리(1.62→1.63 prefactor Q_j r_a/L_V 정확 폐합, master overfull 수정 의미 보존)(C4).
  - Arrhenius y(T) χ𝒜 상쇄가 𝒜(T) 온도의존 무관하게 정확(C5, SymPy), 입자분포 σ_lnL=σ_G/RT.
  - 합성 면적보존·kinshift ⟨Δq⟩=L_q·Ifuse round-trip(0.07/0.035C)(C6).
  - **히스 임계멱: ΔU_hys 닫힌꼴·계수 8RT/3·멱 (T_c−T)^{3/2}·dU_hys 54.8mV, σ_d⊥s=+1 직교**(C7, 수치+해석).
- **수정 3건 적용**(수식-follow 완성도):
  1. (1.21)chisum — (1.20)의 (1−χ)를 독립 χ'로 푸는 재파라미터화 다리 1구 추가(C2 G-follow 갭 해소).
  2. (1.67)LqV — ≤0 부등호에 `(s=+1)` scope 명시(s 노출된 채 s=+1 가정 숨던 것).
  3. (1.51)eqpeak — 순높이에 "방전 s=+1 크기, 충전 부호반전·통합형 §1.15" note(s-인자 테마 정본 해소).

### 삼각검증서 정리한 sub 지적 (빈 통과/과잉수정 방지)
- **(1.47)dQdV "dV_n/dq<0" 가정(R1 sub C)** → **거짓 확정**: 방전 s=+1 탈리튬화에서 V_n↑(q↑), dV_n/dq>0 → (1.47)(1.48)(1.51) 전부 양수 정합(C3 삼각).
- **(1.75)xidecomp "선행 없는 뿌리"(baseline·C6 HIGH)** → **충분 판정**: 정의 ξ_j=ξ_eq−r̄ 가 (1.75) 직전 display equation*(line 1165)로 명시 → 다리 present. 비수정.

### 비수정 (4-tier: 추정 — D2, v3 계승·규약 내 정합)
- (1.63)tail 지수 방향 일반성·(1.60)risefollow O(L²) 부호 — O(·) 크기/σ_d 이연 안에서 정합, numbered 식 본문(verbatim v3) 수정 회피.
- (1.9) site 개수 N vs (1.11) N_s 표기 분열 — verbatim v3 식 본문, 수치 무영향. 추정 보고.
- (1.93) 기울기 2R_n에 L_V kinetic 이동 합산 가능(C7) — 본문 산문에 이미 단서, v3 계승.

### Gate R2 = PASS
97식 전부 (i)~(iv) 판정 완료(미판정 0) · 유도 오류 0 · 수정 3건 재빌드 0/0/0 40p · comment 15/15 · 약점3(1.95 R1해소/1.75 충분/1.83 R1해소) 처리 완료.
