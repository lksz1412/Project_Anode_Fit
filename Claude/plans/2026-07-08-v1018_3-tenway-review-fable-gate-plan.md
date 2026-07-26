# ★MASTER 계획서 — v1.0.18.3 종합 정련판: 10종 체리피킹(1 Fable 포함) + 별도 Fable 최종검수 게이트

> **이 문서 = v1.0.18.3 작업의 단일 마스터 진입점**(컴팩션 복구 시 여기부터). 페이즈 result·ledger = §8.
> **기획 단계 — Phase 1 착수 전 사용자 검토·GO 대기.** (팝업·플랜모드 X — 본 md 로 제시, GO 후 마지막 phase 까지 무중단.)
> **관계**: base = `docs/v1.0.18.2/`(물리판·제안1 vib Einstein 완결, 커밋 fbe2da6·b8c68bf) ← `docs/v1.0.18.1/`(이월판) ← v1.0.17 ← … 방법 = 우리가 써온 검토 방식(청킹·렌즈 로테이션·N회 가변청크·3-Pass·체리픽) **강화판**.
> **이번 세션 지시(2026-07-08)**: "우리 검토 방식을 제대로 사용. 이번엔 **다른(검토)건 10종**으로. **최종 검수는 Fable 모델**로." → 검토 다중에이전트 = 10, 최종 게이트 = Fable.

---

## 0. 배경 + 이번 정련의 성격
v1.0.18.2(물리판)는 P1~P8 + Fable 1차 검수(H-1/H-2 수정)까지 완결·push. **미해소 잔여** = Fable 경미/제안 6건(M-1~M-3·S-1~S-3, 당시 pre-existing/cosmetic로 기록·미수정) + 아직 10종급 전수 재검토를 안 거친 부분. 이번 v1.0.18.3 = **그 잔여 + 10종 다중에이전트 전수 검토**로 물리판을 최종 QA·정련하고, **Fable 을 닫는 게이트**로 확정한다. 물리·수식의 새 확장은 없다(정련·완결성·정합·서지·시각 — 결함 수정 중심). 코드 = matched bump(제안1 additive 무변경 = 회귀 bit-exact).

## 1. Summary
v1.0.18.3 = **10종 다중에이전트 검토 + Fable 최종게이트 정련 증판**(`docs/v1.0.18.3/`):
- **(A) Fable 1차검수 잔여 반영**: M-1(L_V 크기 단위-프레임 한정어)·M-2(G3 일련번호 forward-ref)·M-3(fig:reversal 1.00/1.01w 캡션 통일)·S-1(Ch2 라벨 노출 — 최종 게이트 판단)·S-2(tab:lco-staging 시연값 순서 note)·S-3(부호규약 재진술 압축) triage 후 타당분 반영.
- **(B) 10종 체리피킹 전수 검토**(렌즈×청크·N회 가변): **10 독립 에이전트 = 9 비-Fable(Sonnet/Opus) + 1 Fable**(체리피킹 10 중 1이 Fable). Ch1(~3540줄)·Ch2(~900줄)·appendix(~495줄)을 전담 창(청크×렌즈)으로 검토 → refute+가장약한1곳+빈통과금지 → master가 **union 체리픽·삼각검증·정밀 적용**.
- **(C) 별도 Fable 최종검수 게이트**: (A)(B) 반영·3대 무결 후 **별도 Fable 서브세션 1회** holistic 최종검수 → 통과(또는 잔결함 반영)까지. **★Fable 두 번 = ①체리피킹 10 중 1(B) + ②최종 게이트(C).** 나머지 9 = 비-Fable.
- **(불변)** 물리·수식·코드 = matched bump(제안1 additive·회귀 bit-exact). 공유 결함(Ch1 등)은 **18.1 에도 동반 반영**.

## 2. 품질 기준 (헌법 3종 + 검토 방식)
- **헌법 ①②③**: 교과서 register / 논문 깊이 / 수식-주도. v1.0.17~18.2 확립분 유지.
- **검토 렌즈(1급)**: 정확성 + **G-follow(따라가짐)·G-usable(사용성)** + register + 수식-주도 + 물리 적대검산 + 완결성 + 시각(그림/표) + 서지(`feedback_multiagent_review_chunking`).
- **청킹**: 파일당 ~500줄 여러 창 전담(큰 파일 통째/거친 청크 = "100% 정독" 과장 금지). N회 가변-청크: 매 라운드 청크 스킴·렌즈 전환 → coverage missing=0.
- **doc↔code**: 문서 식 = 코드 식(제안1 S_vib/_vib_dU/_vib_dS 등). 코드 참조는 구현 대응표만.

## 3. Current Ground Truth (전제 검증)
- **base = v1.0.18.2**(동결·커밋 b8c68bf). Ch1 59p·Ch2 17p·appendix 8p·코드 `Anode_Fit_v1.0.18.2.py`. 회귀 13/13 bit-exact. 3대 무결 green.
- **Fable 1차검수 결과**(반영 대상): 치명 0·HIGH 2(수정됨)·경미 4·제안 3. 잔여 = M-1~M-3·S-1~S-3(§1 A).
- **10종 미검토 영역**: 물리판 전체를 아직 10 전담창으로 안 돌림(1차 적대검증은 vib 절 집중). 이번이 전수.
- **⚠전제 재확인(실행 시)**: M-1 L_V 는 물리 결함 아님(결론 불변)·표기만. S-1 Ch2 라벨 노출은 다버전 anchor 관례라 최종판 정책 판단(Fable 게이트에서 확정). 공유 결함 = 18.1 동반.

## 4. Phase Range (순차 6-페이즈)
| Phase | 이름 | 성격 | Gate |
|---|---|---|---|
| P1 | 증판(18.2→18.3)·코드 matched + Fable 잔여 triage | 비파괴 | 3-tex 빌드·회귀 bit-exact·triage 확정 |
| P2 | 10종 다중에이전트 검토(렌즈 로테이션·N회 가변청크) | 검토 | 10창 커버리지 missing 0·refute·빈통과 0 |
| P3 | master 체리픽·삼각검증·정밀 적용(A 잔여 + B 발굴) | 적용 | 결함 반영·의미 왜곡 0·빌드 GREEN |
| P4 | 3대 무결(3-tex 빌드·회귀) + doc↔code + 공유분 18.1 동반 | 검증 | Ch1/Ch2/appendix 빌드·회귀·18.1 정합 |
| P5 | **Fable 최종검수 게이트**(holistic 1회) → 잔결함 반영 | 게이트 | Fable 통과(또는 반영 후 재확인)·물리 재검산 PASS |
| P6 | HANDOVER·INDEX·commit+push | 마감 | 최종·2-버전+정련판 정합 |

> N회 가변-청크: P2 는 기본 1라운드(10창). 미수렴(신규 결함) 시 P2b(청크 스킴 전환 재검토) 삽입, 연속 2R 0결함까지.

## 5. Phase 세부 + Gate
- **P1 증판·triage**: docs/v1.0.18.2 → v1.0.18.3 복제·버전 bump 1.0.18.3(계보 1.0.18.2)·코드 matched. Fable 경미/제안 6건 triage(반영/보류·근거). **Gate**: Ch1/Ch2/appendix xelatex 3-pass exit0/undef0/of>10 0·회귀 13/13·triage 표 확정.
- **P2 10종 체리피킹 검토**(9 비-Fable Sonnet/Opus + **1 Fable**): 창 배정(예) — Ch1 6창(Part0 L1-600 / N0-N3 / N4-N6 / N7-N9 꼬리 / LCO Part II / 부록·표), Ch2 2창(본문+vib 물리 적대검산 / 서지·표·완결), appendix 1창, cross-file 완결·Fable-flagged 검증 1창. **1 Fable 은 물리-critical 창(R7 vib) 또는 cross 창(R10) 배정.** 각 창 렌즈 로테이션. refute+가장약한1곳+빈통과금지 → master union 체리픽. **Gate**: 10창 head→tail 커버리지·각 창 결함 또는 clean 근거.
- **P3 체리픽·적용**: master 가 10종 결함 + A 잔여를 삼각검증(중복제거·타당성·물리 재검)·직접 정밀 적용(단위 루프). **Gate**: 반영 grep 확인·물리/식별자 불변·빌드 GREEN.
- **P4 3대 무결·18.1 동반**: 3-tex 빌드·회귀 bit-exact·문서식=코드식. 공유 결함(Ch1 register/정합 등)은 18.1 에도 동반 반영(document-protection: 별도 커밋). **Gate**: 3대 무결·18.1 정합.
- **P5 Fable 최종게이트**: `Agent(model:fable)` 1회 holistic 최종검수(물리 사슬 재검산 + register/정합/완결) → 발견 시 master 반영 → 재확인. Fable 미가용/미완 시 = Sonnet 적대검증 2라운드로 대체 명시(게이트 유지). **Gate**: Fable 통과 또는 반영 완료·회귀 PASS.
- **P6 마감**: HANDOVER_v1.0.18.3·INDEX(18.3 현행 물리판) + commit+push. **Gate**: 최종·정합.

## 6. 검토 구조 (10종 = 렌즈×청크)
| 창 | 파일·범위 | 1차 렌즈 |
|---|---|---|
| R1 | Ch1 Part0(분배함수~Nernst) | 수식-주도·물리 적대검산 |
| R2 | Ch1 N0-N3(규약·중심·히스) | 기호·register |
| R3 | Ch1 N4-N6(폭·logistic·평형peak) | 정합·G-follow |
| R4 | Ch1 N7-N9(동역학·기억·합산) | 물리·완결(M-1 L_V 포함) |
| R5 | Ch1 Part II LCO(전자·분해·decomp) | 수식-주도·G-usable(M-2 G3 포함) |
| R6 | Ch1 부록(부호검산표·구현대응표·표) | 표·완결·시각 |
| R7 | Ch2 본문 + **vib Einstein 절** | 물리 적대검산·doc↔code |
| R8 | Ch2 서지·표·맺음(M-3 fig·S-2·S-3) | 서지·시각·register |
| R9 | appendix | 물리·단위·수식-주도 |
| R10 | 3파일 cross + Fable-flagged 6건 검증 | 완결·정합·교차참조 |

→ 10종 체리피킹 = **9 비-Fable(Sonnet/Opus) + 1 Fable**(1 Fable = 물리-critical R7 또는 cross R10). master union 체리픽. **별도 최종 게이트 = Fable(P5)**. ★Fable 두 번 = 체리피킹 10 중 1 + 최종 게이트 1(사용자 지시 정확 반영).

## 7. 검수 방법 (N회 가변-청크 + 게이트)
- P2 후 미수렴 시 청크 스킴 전환(통독/식별/도메인) 재검토, 연속 2R 0결함까지. Agent 병렬(공유 가변상태 X·목적적)·master 통합.
- P5 Fable = 닫는 게이트: 통과해야 확정. 잔결함이면 반영·재게이트.

## 8. 산출·위치
- 딜리버러블: `docs/v1.0.18.3/`(ch1/ch2/appendix tex+pdf·Anode_Fit_v1.0.18.3.py·FITTING_GUIDE·golden 불변·ROADMAP 승계·HANDOVER). 공유분 반영 시 `docs/v1.0.18.1/`·`docs/v1.0.18.2/` 별도 커밋.
- 레저·result: `results/process/V1018_3_EXECUTION_LEDGER.md`. INDEX 18.3 등재.
- 커밋: main·attribution 없음·phase별 명시 스테이징+push.

## 9. 정지 조건·결정 경계 (GO 후)
정지 5조건만(Decision Gate·새 의존성·FAIL gate·사용자 stop·두 통제문서 모순→더 제한적). **결정 대기 1건**: S-1(Ch2 라벨 노출) = 최종 합본 정책 — Fable 게이트 판단 + master 기본값(다버전 anchor 관례 유지, 최종 합본 시 재검토 note)으로 진행(사용자 대기 X). **Fable 미가용** = STOP 아님(Sonnet 2R 적대검증 대체).

## 10. 이월 (범위 밖)
- 제안 2~5(ROADMAP, 외부 위임)·v1.0.16 물리-데이터(실측 대기) — 이번 정련 대상 아님.
- 18.1 은 공유 결함만 동반(이월 [선택] 재개 X).

## 11. Correction History
- (초안, 2026-07-08) v1.0.18.2 Fable 1차검수 잔여 + 10종 전수 검토 → v1.0.18.3 정련판. 6-페이즈·N회 가변청크. GO 대기.
- (정정, 2026-07-08) 사용자 의도 재확인: **10종 체리피킹 중 1개 = Fable**(9 비-Fable + 1 Fable) + **별도 Fable 최종게이트** — Fable 두 번. 초안의 "10창 Sonnet + Fable 게이트" 단일 프레이밍 오류 정정. 우리 방식(분업·단위루프·N회 가변청크·체리피킹·3-Pass·doc↔code·GO후 무중단) 명시·정합 확인.
