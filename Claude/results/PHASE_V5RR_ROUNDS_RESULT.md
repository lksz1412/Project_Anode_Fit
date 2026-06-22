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
