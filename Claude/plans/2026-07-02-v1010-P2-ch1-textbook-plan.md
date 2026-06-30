# P2 세부 스텝 계획 — 챕터1 교과서화 + LCO 이론 (9종 경쟁-체리픽)

> 마스터 §P2. result = `results/process/V1010_P2_ch1_RESULT.md`. 대상 문건 = `docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex`(34p). 앵커 = `results/process/V1010_P1_code-audit_RESULT.md`(P1 플로우차트 맵·파라미터). **순서 = 코드→문건→코드: LCO 코드 구현은 P4, P2는 이론 기술(문건이 코드보다 앞서는 것 정상).**

## P2 산출물
1. **Ch1 ↔ 코드 1:1 coverage 매트릭스**: P1 맵의 각 코드 step(equilibrium·dqdv 체인·각 파라미터)이 Ch1 어느 절·식으로 설명되나 → **누락(코드엔 있는데 문건 유도 빠진 것)**·**과잉(코드에 없는데 문건에만)** 식별.
2. **누락 유도·다리 보완**(물리화학 교재 형식·식→식): coverage 갭을 메우는 유도. v3~v9 교과서 요소 통합(이전 버전들의 좋은 유도).
3. **★LCO 이론 갈고닦기**: v9 LCO 검토분 타당성 반영 + LCO 양극 dQ/dV·전자 엔트로피(Sommerfeld) 이론을 교재급으로 정련(아직 미완성 인지 — 이번에 완성도↑). 코드 구현은 P4 예고로 명기.
4. 품질 = 마스터 §2(화학식·물리식 중심·유도 식→식·타 전공 자기완결·안정객관 어투·독자평가 0).

## 9종 경쟁-체리픽 단계
- **Step 1 — 9 드래프트**(3 Sonnet·3 Opus·3 Codex, 독립): 각자 Ch1.tex + P1 result + LCO 검토자료(`results/research/broadening_w_design.md`·radius `ORIGIN_VERDICT`) 정독 → 위 산출 1~3을 **supplement 문건**으로(coverage 매트릭스 + 보완 유도 초안 + LCO 이론 정련안) → `V1010_P2_draft_<id>.md`. **커밋①**.
- **Step 2 — 검토1(별도 세션)** + 보완: 9 supplement 교차검증(coverage 정확성·유도 물리 무결·LCO 이론 타당성·교재 형식·G-follow/G-usable). refute+가장약한1곳. **커밋②**.
- **Step 3 — master 체리픽**(vN-10): 9 supplement 장점 통합 → 통합 supplement. **커밋③**.
- **Step 4 — adversarial(별도 세션)** + finalizer: 통합 supplement를 코드·물리와 적대 검증 → master 가 **Ch1.tex에 실제 통합·재빌드**(PDF) → `V1010_P2_ch1_RESULT.md`. **커밋④**.

## Gate (P2 종료)
- coverage 0누락(코드 각 step ↔ Ch1 식)·**코드에 없는 서술은 P4 예고로 명기(또는 trim)**·LCO 이론 교재급 완성·유도 식→식 사슬 끊김 0·orphan 0·독자 자기완결·PDF 빌드 0-error.

## 주의
- 검수 = 작업/드래프트와 다른 세션. commit master 전용. 추정 금지(코드·P1 result 줄 근거). 원본 Ch1 정정은 통합 시 master 직접(전자엔트로피 절 등 byte-보존 확인). 사이즈/PSD 재도입 X.
