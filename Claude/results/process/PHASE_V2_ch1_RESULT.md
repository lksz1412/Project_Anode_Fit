# PHASE V2 Result — Ch1 백지 재작성 v2 (V.0–V.2)

작성: 2026-06-10 (V.2 챕터 게이트 통과 시점) · plan: `Claude/plans/2026-06-10-ch1-blank-rewrite-v2-plan.md`

## 1. Phase 목표
박사님 2차 /goal 피드백 6건 기준 Ch1 **백지 재작성** — Eyring 속도식 k≃k₀exp(−ΔG_a/RT) 를 식 (1.1) 근본식으로 세우고 온도·전위·C-rate 세 영향 + 평형 열역학(정지점 회수)을 전부 그 식에서 가지 치는 새 구성. 작성·검수 전수 Fable, Codex 는 검수 시 적대 의견만.

## 2. 산출물
- `Claude/docs/graphite_ica_ch1_Fable_v2.tex` (+pdf) — **32 페이지, 1,550 행, 식 (1.1)–(1.34), 그림 10, 참고문헌 19**
- 본 RESULT · `PHASE_V2_EXECUTION_LEDGER.md` (steps 117–136)
- 직전 판 `graphite_ica_ch1_Fable.tex`(50p)·원본 `graphite_ica_ch1.tex` — 불가침 보존 확인

## 3. 새 구성 실행 결과 (절 지도 17단위 → 전부 작성)
서론(척추 선언+stagebox) → §1 기호 → §2 근본식(eq:eyring=**1.1**, fig:barrier 신규) → §3 열역학 다리(G→μ→격자기체→전기화학) → §4 정·역과 평형 회수(BV→detailed balance→logistic **유도**) → §5 상호작용·상분리(현 작도→binodal·spinodal 단계 명명, fig:isofamily·doublewell) → §6 관측축(보존식·세 전위·worked example) → §7 평형 peak 기준선(FWHM 닫힌꼴 없음) → §8 C-rate 가지(보편 ODE→기억 커널→두 극한) → §9 전위 가지(ΔG_eff, 직렬 율속) → §10 온도 가지(Arrhenius 회귀·분포 전파) → §11 합성(eq:closed·simplefit·3×3 표·비순환 원칙) → §12 합산·겹침(forward 원칙) → §13 [확장] 분기(eq:hysdU 유도) → §14 [확장] 관측 gap(절편/기울기·gap-T 표·부분 cycle 소절 흡수) → §15 통합식·알고리즘((1)–(8), M1–M6, S0–S5, 참조표, 가정 울타리 ①–⑩) → §16 검증과 반증(경쟁 꼬리원 표·히스 세 칼날).

## 4. 게이트 결과 (전부 확인 가능 조건)
| Gate | 조건 | 결과 |
|---|---|---|
| 빌드 | xelatex 2-pass err/of/undef | **0 / 0 / 0**, 32p (commit 23f3efe) |
| 피드백① | §3 다리 존재 + μ 무근거 등장 0 | PASS — eq:mudef 1.3, eq:mu(1.5) 인용 3건 전부 §3 정의 이후 (행 367·389·475) |
| 피드백② | FWHM 닫힌꼴 유도 0 | PASS — grep `FWHM\|3\.53` = **0** |
| 피드백③ | binodal/spinodal 첫 등장 전 그림+단계 전개 | PASS — 본문 전개: 현 작도(행 531)→binodal 명명(536)→spinodal 명명(542), fig:doublewell 동반. §1 기호표 2행은 사전(辭典) 성격의 괄호 병기 |
| 피드백④ | 식 1.1=Eyring, 인용 빈도 최다 | PASS — eq:eyring=(1.1), eqref 9회(차순위 weff·logistic 6회) |
| 피드백⑤ | 신규 개념 도식 ≥2 | PASS — fig:barrier(신규)·fig:doublewell(현-작도 재설계)·fig:kernel(기억 커널) 외 총 10개, 좌표 전부 실함수 계산값 |
| 피드백⑥ | 연습문제 절 0 | PASS — grep `연습문제` = 0, 자연 분량 32p(50p 채움 강박 제거) |

## 5. 통독(전문 정독) 검증
- **Read Coverage**: 1–520 / 520–1029 / 1029–1308 / 1308–1550 — 전 구간, 생략 없음.
- 척추 일관: 매 절 도입·keybox 가 식 1.1 과의 연결을 명시("근본식의 가지" 추적 가능). eq:master 의 각 항 출처를 (1.1) 가지로 명기.
- orphan 0: 그림 10개 전부 본문 \ref 인용, box·표 전부 앞 도입·뒤 사용 확인.
- 수치 검산(재계산 일치): ΔU^hys(4RT)=2.13RT/F≈55mV · 임계 멱 (8RT/3sF)u³ · w_eff=(RT/F)(1−Ω/2RT) · spinodal ξ=½±½u · binodal(Ω=3RT)=0.0707 · fig:gapT 28.1mV(3RT₀,270K) · 절편 표 33.2mV(4RT₀,23°C,γ=0.6) · σ_lnL=2.0/2.3 · L_q=0.028(0.1C) · worked example 0.471+0.029.

## 6. 결함·수정 이력 (V.1 중)
- step 134 overfull 1건(모듈 골격 인라인) → tt quote 블록 승격(aea5362).
- V.1 말 undef 1건: 기호표 `sec:dist`(직전 판 잔재) → `sec:tempbranch`(23f3efe).

## 7. 직전 판 자산의 재작성 활용 (복붙-완료 금지 준수)
그림 좌표(검증 완료 함수값)·알고리즘 사양(round-trip 실증)·유도 골격은 전부 새 흐름(Eyring 척추)에 맞춰 절별 재작성. 인과 방향 역전(평형→속도 ⇒ 속도→평형 회수)에 따라 §3–§5 는 전면 신작.

## 8. 식번호 재매핑 의무 (post-confirmation)
v2 는 전면 새 번호( (1.1)–(1.34) ). ch3/ch4 의 (1.x) 하드코딩 인용 재매핑은 **v2 확정 후 별도 phase** — plan·핸드오버에 기록, 이번 작업에서 ch3/ch4 무수정.

## 9. 검수 체계 (이후 V.R)
Fable 자체 렌즈 로테이션 + **Codex 적대 검수 병행**(의견만, 파일 수정 금지, Codex/ 불가침) — V.2 게이트 직후와 주요 라운드에 투입, master 삼각검증 후 직접 수정.

## 10. 미해결·이월
- V.R 보완 10회+ (렌즈: prose 패턴·흐름 통독·코드 작성 시뮬레이션·물리 재유도 적대·완결성/orphan·PDF 시각 판독·round-trip 사양 대조).
- 사용자 확인 후: ch3/ch4 재매핑 phase.

## 11. 다음 단계
V.R Round 1 부터 — 라운드당 [검수→수정→빌드 0/0/0→ROUNDS_RESULT 기록→커밋+푸쉬].
