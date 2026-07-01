# Fable 재검 — 챕터 4(v1.0.12 작성) 세부 계획서 + ★Decision Gate

> 마스터 = `2026-07-02-fable-reaudit-v12-master-plan.md`(Steps 25+). 입력 = 세 감사(`docs/Fable_점검/FABLE_AUDIT_01·02·03`) + v10→v11 핸드오버·v11 마스터플랜(고가중) + 과거 사용자 지침(두 축·교과서 문체·수식-주도·보편식 먼저). 방식 = 개정 스킬 **N=10**(3S+3O+3C+**1F**, Fable 가중 3)·**체리픽 통합·최종본 = Fable(master)**·검수 union+10차. ★Step 26 = 사용자 GO 대기(Decision Gate).

## v12 개정 목록 (감사 확정분 — GO 시 즉시 착수)
**A. 물리 주장 정정 (HIGH·물리 논리 집중의 본체)**
1. Ch2 eq(2.11)-(2.12) BW V_eq 부호 반전 정정 [H-1].
2. w_j 지위 일원화 — Ch2 §logistic 단정에 "단상 한정" 한정어·파생A 검증 전제 명시·Ch1 이중지위와 챕터 간 정합 [H-2].

**B. 서술·귀속·한정 정정 (MED 11 — 물리 골격 불변)**
3. fig:staging ξ_j→θ_j 라벨 [M-1] · 0.18 k_B 재귀속+검산문장 교체 [M-2] · broadening ①이중귀속/③과결정 정합화 [M-3] · ν=2 점프 정직 서술 [M-4] · 꼬리 수렴 대상 정정 3곳 [M-5] · 우함수 대칭 한 줄 [M-6] · park2021 완화 [M-7] · 파생D "선형화 근사" 명시 [M-8] · 고온 코너 타당역 한정 [M-9] · supplement T² 가드 유지 편입 [M-10] · 규약표 s 행 [M-11] + LOW/NOTE 5.

**C. LCO 6절 수식화 + P1.1 supplement 편입** (기왕 GO 계승 — center·hys·peak·decomp·plug-in·MSMR, 물리 불변·G-derive 사슬).

**D. 코드 위생 (물리 불변)**: 버전 라벨 현행화 [P-1] · 헤더 w^eff 잔재 제거 [P-4] · default 표시(그래프 라벨 or 초기값) [P-3] + 인계 minor(byte-claim·forward-ref·동반개정 제약·ρ_G 예고 — v11 핸드오버 계승).

**E. 산출 정리**: `docs/v1.0.12/`에 Ch1/Ch2 tex·코드(`Anode_Fit_v1.0.12.py` — results/code/구 v12.py와 구분)·figs·샘플 이미지(글자깨짐 0)·FITTING_GUIDE. INDEX 현행화.

## ★Decision Gate — 사용자 승인 항목 (Step 26)
| # | 항목 | 배경 | master 권고 |
|---|---|---|---|
| D1 | **Eyring 구조 재배열 여부** | 6-11 지시 "모든 것이 Eyring서 뻗어야" — 서사는 서론에 계승됨(M-4 확인), 미계승은 구조 배열(현행 코드-순 N0→N9 vs Fable_v2 식-first) | (a) 현행 구조 유지 + Eyring 서사 강화(각 절 도입에 근본식 가지 명시) — 저위험·물리 불변 정합. 식-first 대개편은 (b) 별도 결정 시만 |
| D2 | §1.18 적층 준안정·athermal 훅(v4 자산) 재개방 | v5부터 park | v12 범위 밖(코너를 메인으로 안 끌기) — 후속 |
| D3 | S0-S5 역방향 식별 사슬·울타리(v5/v6 자산) 복원 | v7 절삭·G-usable(피팅 식별성) 가치 | FITTING_GUIDE 확장으로 **선별 복원**(문건 본체 아님) |
| D4 | HIGH 2 정정(A항) 승인 | 물리 주장 정정이라 명시 승인 | 승인 요청(근거 = C-4 재유도+수치) |
| D5 | ν(min_lag_grid_steps) 기본값 상향(≈8-10) | ~23% 점프 완화(코드 기본값 층·모델식 불변·흑연 회귀는 의도적 변화로 ledger) | 서술 정정(M-4)은 무조건, 기본값 변경은 승인 시 |

## Phase 구성 (GO 후, cumulative Steps 27+)
- **4.2**: `docs/v1.0.12/` 증판 + B·D항(서술·위생 — master 직접, 저위험 일괄) → 빌드·회귀 → 커밋+푸쉬.
- **4.3**: A항 HIGH 2 + C항 LCO 수식화 — **N=10 작성 경쟁**(3S+3O+3C+1F, Fable 가중 3) → Fable 체리픽 → **검수 N종 union + 10차** → Fable finalizer(편입·재빌드) → 커밋+푸쉬(단계별).
- **4.4**: 코드 위생·샘플 이미지(글자깨짐 0)·최종 점검(두 축 gate·상호충실도) → result·ledger·커밋+푸쉬.
- gate: 두 축(G-derive 비약0·G-follow)·물리 결과식 diff=승인분만·xelatex 0-error·코드 실측 회귀·union 수렴(연속 2R 0확정결함).

## 주의
- 원본(v1.0.10/v1.0.11 이하 전부) 불가침 — v12는 별도 폴더. 코너케이스 검토는 하되 메인 승격 금지. 신규 개념 무근거 도입 금지(검증은 지속). Codex 단계구동+지속 관찰.
