# RB_LEDGER_CH1_REWORK — Ch1 §7+ 자기완결 재작업 Result (2026-06-01)

> 트리거: 사용자 검토 — Ch1 §7+ 부실(식 뜬금없이 등장·물리의미 불명·연결 부족·Ch1만으로 피팅 근사식 못 뽑음). 검수가 정확성만 보고 따라갈 수 있음/쓸 수 있음 못 봄. 계획서: `Claude/plans/2026-06-01-ch1-self-contained-rework-plan.md`.

## 1. 진단 (확정)
원천 consolidated_ch1 §7+(11절)의 실무·닫힌형 내용을 rebuilt 가 Ch6으로 이관·압축(4절) → Volterra 뜬금 등장(닫는 §closure 부재), fiteq 가 안 풀린 Volterra 의존, 심플 근사식 부재(0.2C 드롭). 단순 컴팩션 소실이 아니라 \*구조적 deferral\*.

## 2. 방법 (재발 방지)
절별 청크 작업 + **절별 청크 검수**(전체 tex 한 번에 검수 X — 이번 핵심 수정). 각 절 = 물리 동기 prose → display 식 + step → 변수·적분 의미 1줄 → 무비약 연결.

## 3. 재작성 (W1~W7, Ch1 662→795줄, 15p)
| W | 절 | 내용 |
|---|---|---|
| W1 | §kernel | A_L 물리 의미 명시("완화 길이별 꼬리 분해 분포") |
| W2 | §kernel/closure | Volterra 자기참조 동기(되먹임) + Θ_init 정의 + **Plan B(g-grid validator) + Plan A 닫힌형 eq:closed 복원**(선형화 b=−(Q_p/C_bg)∂Θ_eq/∂V_n → ratio ansatz → factor-out, 무결성 b→0 복귀). Fredholm↔Volterra 가정차 BOUNDED |
| W4 | §fiteq | S5 "Ch6" → 본 장 closure(Plan B/A)로 닫힘. dΘ/dQ=(1/Q_cell)dΘ/dq bridge 복원 |
| W5 | §ch1_simplefit(신설) | **single-mode 심플 근사식 eq:simplefit**(Θ=Θ_0(1−e^{−(q−q_a)/L}), L=|I|/(Q_cell k)) + **0.2C 기준식 eq:02c** + 데이터 피팅 절차(0단계 식별성 전제→L→유효엔탈피→χ) + EMG 초기값 |
| W6 | §falsify | 식별성 파라미터 제한 순서(저속OCV→펄스R_n→Arrhenius→전류χ→ρ_G독립) |
| W7 | §ch1_numeric(신설) | Ch6 수치 core 흡수(g-grid·index-1 DAE·근거기반 tolerance·ε_tol 검증·격자수렴). 전달노트 Ch6 해체 반영 |

## 4. 집중 적대검수 (§7+만 범위, 청크)
G-follow 대체로 PASS(원천보다 유도 동기 강화), **G-usable 초기 FAIL → 정정 후 PASS**. 발견·정정:
- **C1(CRITICAL)**: simplefit (2)"A_j→0 순수 ΔH_a" ↔ (3)"V_drive 흔들어 χ" 데이터영역 자기모순. → (2)는 \*유효\* 엔탈피 −(ΔH_a−χA)/R, 순수 ΔH_a는 A→0 외삽(별 영역), χ는 peak근방(유한 A) — 영역 분리 명시.
- **H1**: χ 추출 가로축 V_drive=V_n 은 비측정 내부전위 + R_n 공선형. → 0단계 식별성 전제(저속OCV·펄스R_n 선고정·V_app→V_n 환산) 박음. "본 장만으로"가 §falsify 식별성을 가리키게(여전히 Ch1 자족).
- **H2**: q_a 결정 절차 부재(L과 공선형). → q_a 먼저 고정(ICA peak/dξ_eq/dq 임계) 후 L 단일회귀 명시.
- **H3**: r(q_a) 공통값 흡수가 항등 아닌 가정. → L-의존 가능, BOUNDED 명시.
- **M2**: dΘ/dQ 좌표 bridge 복원.

## 5. 빌드·무결성
tex **795줄**, PDF **15p** → `Claude/results/graphite_ica_ch1_rebuilt.pdf`. env equation 29/29·begin-end 46/46. 진짜 undefined ref/cite 0, dup label 0, overfull 0, `!` 0. 신규 cite(jcp2017/lee2011/son2013) bibitem 추가·해소. 신규 label(eq:selfcoupling/eq:closed/eq:simplefit/eq:02c/sec:ch1_simplefit/sec:ch1_numeric) 충돌 0.

## 6. 결과
**Ch1 자기완결 달성**: §7+ 가 물리 동기+무비약으로 따라가지고, §ch1_simplefit 에서 실데이터에 바로 대입하는 single-mode 닫힌식 + 0.2C + {L,ΔH_a,χ} 추출 절차가 나온다. Ch6 수치·피팅 내용 Ch1 흡수.

## 7. Next (잔여)
Ch6 파일 해체(삭제) + full_rebuilt 재생성(Ch1 재작업본 반영, Ch6 제외) + refs 갱신 + Ch2~5 "Ch.6" 참조→"Ch.1 부록" 정리. (별도 단계)
