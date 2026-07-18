# HANDOVER — v1.0.23 (사용자 JCP147 ratio 방법 접목 + 고등수학) — P5 마감

## 1. 무엇을 했나 (P0~P5)

v1.0.22(완결 문건)를 승계해 **사용자 논문 JCP 147(14) 144111 (2017)의 Fredholm-2종 ratio 닫힘 기법을 흑연 dQ/dV 문건의 동역학 지연(lag) 자기일관 구조에 정직하게 접목**했다. 수학은 부록 E, 적용은 코드(선택·기본 off).

| Phase | Steps | 내용 | 결과 |
|---|---|---|---|
| P0 | 1–3 | v1.0.23 골격 복제·GREEN baseline | PASS |
| P1 | 4–8 | 조건검수: lag=비선형 Volterra(Markov) 자기일관 → 1차 ratio 닫힘 재유도·타당성 부등식·마스터 검산 | COND-PASS |
| P2 | 9–15 | 부록 E 저작(E.1~E.6)·bib 3종·본문 포인터 | PASS |
| P3 | 16–20 | 코드 ratio/transfer 옵션(동결 bit-exact 보존)·게이트 | PASS |
| P5 | 25–28 | 코드↔문건 정합 적대적 5창·정정·마감 문서 | PASS |

(P4 Tier2 Fisher 정보기하 = 사용자 결정 D3 로 **미실행**·차기 옵션.)

## 2. 핵심 결과 (정직)

- **접목 성립 지점 = 동역학 lag(II) 하나뿐.** 전하보존 U_oc 반전(I)·배경 자기일관(III)은 적분핵 없는 대수근이라 이 기법 대상 아님(부록 E 서두 warnbox 명시). Fredholm 리터럴 이식 불가(문건엔 Volterra만).
- **가치 = 계산 절감이 아님.** lag 참 문제가 이미 O(N) 전진 ODE(Markov). 실가치 = (a) 동결 0차 위 **분석적 1차 닫힌형**, (b) 동결 근사가 언제 옳은지의 **타당성 증명서** `ε=2χ_d(Ω/RT)Δξ_supp≪1`, (c) 사용자 방법 시연.
- **동결 경로 완전 보존.** `lag_ratio_correction=False`(기본) → 기존 dQ/dV bit-exact(G1 max|d|=0.0). ratio/transfer 는 선택.
- **실이득창 = 중간 전류** `0.1≲L_V/w≲0.6`(2–10× 오차감축). 기본 흑연은 휴면(warnbox·G-E5 정직).

## 3. 검수 상태 (사용자 "양 버전 빡세게 코드↔문건" 요청 반영)

- 코드↔문건 정합 **적대적 5창**(AUD-1~5) — **치명 0**. 물리·수식·코드·게이트·서지·버전 parity·검수7항 전부 정합.
- 중대 2건(부록 E 수치 증거 문장 과장/오귀속) = **커밋·재현 수치로 정정 완료**(밑바탕 주장 참).
- 상세·트리아지·마스터 검산 = `comp_v23/AUD_REPORT_v23.md`.
- **v1.0.22 parity**: 순수 additive(공유 함수·47섹션 byte/sha256 동일) — v1.0.22 검수 결론 그대로 승계, 두 버전 공통.

## 4. 다음 작업 (열린 항목)

- **[진행 예정] 양 버전 샘플 이미지 QA** (사용자 요청): dQ/dV·DVA 곡선을 대표 조건에서 렌더링 → 물리 타당성 + **연속·매끄러움·미분가능성** 점검(전이 경계·미해상 가드 전환점 line 574·ratio 경로 kink 여부).
- **[D3 보류] P4 Fisher 정보기하**(Tier2·피팅 식별성) — 사용자 GO 시.
- **[근거 미발견] Ref.6·7 원문 제목·DOI** — 사용자 원문 제공 시 확정(현재 정직 유보).
- **[차기 버전 후보] v1.0.24 역문제**(Tikhonov/Bayes deconvolution) — forward 문건과 스코프 분리.

## 5. 재개 지침

- master roadmap = 계획서 `Claude/plans/2026-07-18-v1023-ratio-and-advanced-methods-plan.md`(11-section).
- Phase 결과 = `results/PHASE_P{1,2,3,5}_RESULT.md`(11항)·`results/V1023_EXECUTION_LEDGER.md`(12-col).
- 재개 시 추정 금지: 해당 Phase result 직접 Read 후 작업.
- 빌드: `xelatex -interaction=nonstopmode ch1_graphite_v1.0.23.tex` 3-pass(ch2 aux 선존). 게이트: `python3 test_gates_v1023.py` + `test_gates_v1023_selfconsistent.py`.
