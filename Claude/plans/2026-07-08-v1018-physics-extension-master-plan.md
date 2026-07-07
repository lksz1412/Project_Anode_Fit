# ★MASTER 계획서 — v1.0.18 물리 심화(vib Einstein) + v1.0.17 이월 완결 + 연구 로드맵 (신규 발전 제안서 반영)

> **이 문서 = v1.0.18 작업의 단일 마스터 진입점**(컴팩션 복구 시 여기부터). 페이즈 result·ledger = §8.
> **기획 단계 — Phase 1 착수 전 사용자 검토·GO 대기.** 특히 **§9 Decision Gate(물리 스코프)는 사용자 결정 필수.** (팝업·플랜모드 X — 본 md 로 제시.)
> **근거**: 신규 `S_AnodeFit_v1017_review.md`("논리 발전 방향·개선 제안서" 5개 물리 확장, 원본 프레임·표준식 교차검증 완료) + `docs/v1.0.17/HANDOVER_v1.0.17.md` ③이월 + `V1017_FIXLIST_CONSOLIDATED.md` + 누적 이력(INDEX·CLOSING_v1.0.15 헌법·feedback_anode_fit_textbook_style). 방법 = v1.0.16/17 방식(증판·9종 체리피킹·doc↔code sync·phase별 commit+push·master+sonnet).

---

## 0. 배경 + 신규 리뷰 성격 + 추출 검증

**신규 리뷰의 성격(중요)**: `S_AnodeFit_v1017_review.md` 는 v1.0.17 처럼 라인별 register 검토가 **아니라**, `V1017_Physics_Logic_Review` 심도검토를 바탕으로 한 **"논리 발전 방향·개선 제안서"**. **"물리적 오류 0건, 모든 한계는 명시적 선언됨"** 전제 하에 한계를 넘는 **5개 물리 확장 제안**(각각 "외부 AI 연구에 위임 가능한 발전 과제"로 명시). 즉 결함 수정이 아니라 **연구-급 물리 심화 방향**이다.

**추출 검증(7-07·7-08 교훈 적용)**: 이번 v2 추출은 stitch 를 문서화(코드화면=가로스크롤 절단→연속 프레임 stitch, markdown=완전). master 직접 검증: **원본 프레임 #5(212117)로 S_vib 우측 = `[ln(1/(1-e^{-ℏω/kT}))+(ℏω/kT)/(e^{ℏω/kT}-1)]` 확인** = doc stitch·표준 Einstein 식과 정합. `_LEDGER.md` = Anode #1~17 완결(세그먼트 재매핑 정정). **절단/미포착/오류 없음.**

**누적 이력 궤적**: v1.0.10(matched baseline) → v1.0.12(LCO 수식화) → v1.0.13(Part 0·재구조화) → v1.0.14(어투·엄밀성·부록) → v1.0.15(격자 퇴출·점별) → v1.0.16(**n(T) 폭 피팅·additive**) → v1.0.17(register 정련) → **v1.0.18(물리 심화 + 이월 완결 + 로드맵)**. 궤적상 v1.0.16(다온도 n(T)) 다음의 자연 심화 = **다온도 T-의존 성분의 물리적 분리**(vib vs electronic) = 제안 1.

## 1. Summary

v1.0.18 = **세 트랙 증판**(`docs/v1.0.18/`):
- **(A) v1.0.17 register 이월 완결**: [선택] cosmetic/정합 폴백(verifybox·longtable·signcheck ✓·N3 재배열·N/n·ω 다리·z 각주·Appendix 단위). v1.0.17 정련 pass 를 닫는다. doc-only·저위험.
- **(B) 물리 심화 — 제안 1 (vib 엔트로피 Einstein 양자 보정)**: 동결 상수 ΔS_vib → **S_vib(T;θ_E)=R[−ln(1−e^{−θ_E/T})+(θ_E/T)/(e^{θ_E/T}−1)]**(전이별 Einstein 온도 θ_E). doc(Ch2 vib 유도 + Ch1 eq:lco-decomp) + code(entropy_coefficient vib 항 + ∂S_vib/∂T 발열 전파) + verify. **v1.0.16 n(T) 와 동일 additive 패턴**(θ_E 부재/고온극한 = 현 동결값 = bit-exact). 목적 = 다온도 피팅에서 전자항(∝T)과 vib 잔여 T-의존 분리 식별(v1.0.16 방향 심화).
- **(C) 연구 로드맵 문서화**: 제안 2~5(Ω(ξ)·Cahn-Hilliard·Butler-Volmer·PSD) + v1.0.16 물리-데이터 이월(per-T n 진단·two-phase 폭 T-의존·LCO 실값)을 **구조화된 "향후 발전 방향·외부 연구 위임 과제"**(문건 절 또는 별도 ROADMAP)로. 리뷰의 "외부 AI 위임" 취지 + 누적 이력 캡처.

**방법** = v1.0.16/17(증판→이월→코드→문건→로드맵→마감, 9종 체리피킹은 (B) 물리 유도 authoring 에 실제 적용, doc↔code sync·verify, phase별 commit). 헌법 3종 + 문체 규범 상위 권위.

## 2. 품질 기준 (헌법 3종 + 문체 규범 + doc↔code)

- **헌법 ① 교과서 register** / **② 논문 깊이** / **③ 수식-주도**(결과 박스 (a)출발→(b)연산→(c)중간식≥1→(d)박스). v1.0.17 에서 확립한 register(본문 물리·모델 서술, 코드는 구현 대응표만) 유지.
- **문체 규범**(`feedback_anode_fit_textbook_style`): 완결 문장(전보체 X)·보편식 먼저 극한은 코너·절 도입/마무리 다리·**피팅은 코드 작성 가능 수준(시뮬+round-trip 실증)**·분량은 콘텐츠의 자연 결과.
- **doc↔code sync(불가침)**: "코드에 없는 내용 X + 문건 내용은 코드에 반영". 제안 1 = 문건 유도 ↔ 코드 구현 ↔ 검증 3자 동기.
- **additive 보존**: 제안 1 은 θ_E 부재 시 현 동결 vib = **v1.0.17 bit-exact**(골든 불변). n(T) 선례 준수.

## 3. Current Ground Truth (전제 검증)

- **base = v1.0.17**(완결·동결). Ch1 58p·Ch2 16p·appendix 8p·코드 `Anode_Fit_v1.0.17.py`(matched, v1.0.16 bit-identical). 회귀 13/13 PASS. 커밋 ee4ff96.
- **vib 엔트로피 현 위치**(제안 1 적용점): Ch2 통계열역학 config/vib/electronic 분해의 vib(포논 BE) 항 = "음의 baseline" 동결 · Ch1 eq:lco-decomp(ΔS_config+ΔS_vib+ΔS_e) 의 ΔS_vib 슬롯 · 코드 entropy_coefficient 의 vib 기여. → S_vib(T;θ_E) 로 승격 시 세 곳 + ∂/∂T 발열 전파(v1.0.16 config ∂w/∂T 와 동형).
- **5 제안 tractability**(§6 상세): 제안 1=자기완결·표준식·additive(구현 적합) / 제안 2=정규용액 코어 침습(중간) / 제안 3=부록→본문 승격+γ_j 유도(연구급, 내 v1.0.17 부록 κ/M 기반) / 제안 4=농도분극 신규 layer(연구급) / 제안 5=데이터 의존 나노(연구급).
- **이월 인벤토리**(실재 확인됨, `V1017_FIXLIST_CONSOLIDATED.md`): Ch1 register [선택](#11 verifybox·#25 longtable·#24 signcheck ✓·#26 표서식·#5 N3 재배열·#8 z·#9 ω·N/n·L1017/1159) + Appendix [선택](N_A 각주·γ/v_m 단위·(c)분류표·kinetics 박스). v1.0.16 물리-데이터 이월(다온도 실측 소관).
- **⚠ 전제 재확인(실행 시)**: θ_E 값(전이별 포논 에너지 50–80 meV — 문헌값 실조회, 날조 X) · S_vib 식 원본 프레임(검증 완료) · 제안 1 적용이 v1.0.16 n(T) config 항과 이중계산 안 되게 경계(vib·config·electronic 삼분 유지).

## 4. Phase Range (순차, Decision Gate 후 확정)

| Phase | 이름 | 성격 | Gate |
|---|---|---|---|
| P1 | 증판(v1.0.17→v1.0.18)·코드 matched bump | 비파괴 | 3-tex 빌드·회귀 bit-exact |
| P2 | v1.0.17 register 이월 완결(Ch1/Ch2/Appendix [선택]) | doc | 이월 전건 반영·빌드 GREEN |
| P3 | 제안 1 코드(S_vib(T;θ_E) additive + ∂S_vib/∂T 전파) | code | θ_E 부재=bit-exact·고온극한=현 동결·round-trip·골든 |
| P4 | 제안 1 문건(Ch2 vib Einstein 유도[9종 체리피킹]+Ch1 decomp+GUIDE) | doc | 수식-주도·doc↔code 정합·빌드 |
| P5 | 연구 로드맵(제안 2~5 + 물리-데이터 이월 구조화) | doc | 5 제안·이월 완전 캡처·외부위임 형식 |
| P6 | 적대검수 + 3대 무결 + HANDOVER·INDEX | 마감 | 3대 무결·수렴·commit+push |

> Decision Gate(§9)에서 **Option 2**(제안 1 미구현·로드맵만) 선택 시 P3/P4 생략, **Option 3**(제안 2 추가) 선택 시 P3b/P4b 삽입.

## 5. Phase 세부 + Gate (확인 가능 조건)

- **P1 증판**: docs/v1.0.17 소스 14개 → v1.0.18 복제·버전태그 rename 1.0.18(현행 선언·매칭코드; 이력·temporal·"계산 진행" 유지)·코드 matched bump. **Gate**: Ch1/Ch2/appendix xelatex 3-pass exit0/참조·인용 undef0/of>10 0 · 회귀 13/13 PASS.
- **P2 register 이월**: `V1017_FIXLIST` [선택] 전건 반영(단위 루프). #11 verifybox 감쌈(극한검산 5곳, 정의된 derivbox/verifybox 활성)·#25 longtable(tab:inputs·nodecode)·#24 signcheck-R ✓열·#26 표서식 통일·#5 N3 그룹 재배열(헤더 분할)·#8 z 각주·#9 ω 다리·N/n 통일·Appendix(N_A 각주·γ/v_m 단위·(c)분류표·kinetics 박스 라벨). **Gate**: 이월 항목 grep 확인·빌드 GREEN·의미 왜곡 0.
- **P3 제안 1 코드**: entropy_coefficient 에 vib 항 = S_vib(T;θ_E) additive(dict 키 `θ_E`/전이별, 부재=현 동결 상수 = bit-exact) + 발열 ∂S_vib/∂T = (R θ_E/T²)·[Einstein 미분]을 config ∂w/∂T·전자항과 병렬 전파(삼분 이중계산 가드). **Gate**: θ_E 부재 회귀 bit-exact(골든 불변) · 고온극한 kT≫ℏω → 현 동결값 수렴(해석 검산) · θ_E round-trip(∂U/∂T 유한차분 = 해석, μV/K) · 다운스트림 exit0.
- **P4 제안 1 문건**: Ch2 vib 절 = 고전 동결 → **Einstein 양자 유도**(분배함수 → S_vib(T;θ_E), 고온극한 환원 코너, 수식-주도 (a-d)) **9종 체리피킹**(sonnet 유도 draft 9 → master 체리픽·물리 검증) · Ch1 eq:lco-decomp ΔS_vib 슬롯 T-의존 명시(config·electronic 과 삼분) · FITTING_GUIDE vib-θ_E 규약(문헌 θ_E·다온도 분리 식별·이중계산 경계). **Gate**: 빌드·헌법 3종·doc↔code(문건 식 = 코드 식) 정합·고온극한 문건=코드.
- **P5 로드맵**: 제안 2(Ω(ξ))·3(Cahn-Hilliard γ_j)·4(Butler-Volmer 농도분극)·5(PSD 나노) + v1.0.16 물리-데이터 이월을 **"향후 발전 방향" 구조화 문서**(과제·현상태·문제·개선방향·난이도·외부위임 적합성·선행 데이터 — 리뷰 우선순위표 계승). 위치 = `docs/v1.0.18/ROADMAP_future_physics.md` 또는 부록 절(Decision). **Gate**: 5 제안·이월 완전 캡처·각 과제 자기완결(외부 AI 위임 가능 수준).
- **P6 마감**: 적대검수(물리·register·수식-주도·doc↔code 렌즈, sonnet 병렬 refute+빈통과금지 → master 삼각검증) → 3대 무결(3-tex 빌드·회귀) → HANDOVER_v1.0.18·INDEX(v1.0.18 현행). **Gate**: 3대 무결·수렴(연속 0결함)·문건↔코드 정합.

## 6. 5개 물리 제안 triage (구현 vs 로드맵 · 근거)

| # | 제안 | 자기완결성 | 침습도 | 선행 데이터 | 리뷰 등급 | **v1.0.18 판정** |
|---|---|---|---|---|---|---|
| 1 | vib Einstein 양자 보정 | 높음(표준식·검증됨) | 낮음(additive) | 문헌 θ_E(50-80meV, 有) | ★★★ | **구현(B 트랙)** — v1.0.16 방향 심화·bit-exact 보존 |
| 2 | Ω(ξ)=Ω₀+Ω₁(2ξ-1) | 중간 | **높음**(g(ξ)·spinodal·N2/N3 코어) | Ω₁ 물리기원 | ★★★ | 로드맵(옵션 구현 = Option 3) |
| 3 | Cahn-Hilliard→γ_j 유도 | 낮음(연구급) | 높음(부록→본문 승격) | — (내 v1.0.17 κ/M 기반) | ★★☆ | 로드맵 |
| 4 | Butler-Volmer+Nernst-Planck | 낮음(신규 layer) | 높음(N1 확장) | 임피던스 데이터 | ★★☆ | 로드맵 |
| 5 | PSD 컨볼루션 나노 | 낮음(데이터 의존) | 중간 | PSD 실측 | ★☆☆ | 로드맵 |

→ **구현 = 제안 1**(자기완결·저침습·additive·데이터 有·v1.0.16 연속). **나머지 4 = 로드맵**(연구급·침습·데이터 의존 → 외부 위임이 리뷰 취지). Option 3 시 제안 2 추가 구현.

## 7. 검수 방법 (9종 체리피킹 + 적대검증)

- **P4 물리 유도 authoring = 9종 체리피킹**(v1.0.15 §1.9 선례): sonnet 9 독립 유도 draft(Einstein S_vib 유도·고온극한·발열 전파·삼분 경계) → master 체리픽·물리 삼각검증·정밀 적용. 물리 유도는 다수 접근 존재 → 체리픽 실효.
- **P6 적대검수**: 물리(Einstein·이중계산·차원)·register·수식-주도·doc↔code 렌즈, sonnet 병렬(refute+가장약한1곳+빈통과금지) → master 직접 수정 → 수렴. DOI/문헌 θ_E CrossRef 재확인.
- **하위 서칭·master 고등작업**(사용자 상시 지침): 문헌 θ_E 조회·이월 mechanical·유도 draft = sonnet, 체리픽·물리 판단·정밀 적용·통합 = master.

## 8. 산출·위치

- 딜리버러블: `docs/v1.0.18/graphite_ica_ch1_v1.0.18.tex(+pdf)·ch2·appendix·Anode_Fit_v1.0.18.py·FITTING_GUIDE.md·golden(제안1 additive면 불변)·ROADMAP_future_physics.md`.
- Phase 결과·ledger: `results/process/V1018_EXECUTION_LEDGER.md`·`V1018_*_RESULT.md`.
- 인계·INDEX: `docs/v1.0.18/HANDOVER_v1.0.18.md`·`docs/INDEX.md` v1.0.18 현행.
- 커밋: main·attribution 없음·phase별 명시 스테이징+push(회사 실시간 pull).

## 9. 정지 조건·Decision Gate (GO 전 결정)

**★Decision Gate — 물리 스코프(사용자 결정 필수, 실행 전)**:
- **Option 1(권장 default)**: A(register 이월) + **B(제안 1 vib Einstein 구현)** + C(제안 2~5 로드맵). = 폴백 완결 + 1 물리 심화 + 연구 로드맵. 균형·연속성 최적.
- **Option 2(보수)**: A + C만(제안 1도 로드맵). 물리 신규 X, 폴백+연구 준비. v1.0.18 경량.
- **Option 3(확장)**: A + B(제안 1) + 제안 2(Ω(ξ)) 구현 + 3~5 로드맵. 물리 2건(제안 2 = 정규용액 코어 침습, 검증 부담 큼).

GO 후 정지 5조건만(Decision Gate·새 의존성·FAIL gate·사용자 stop·두 통제문서 모순→더 제한적). 문헌 θ_E 미확보 시 = 로드맵 이관(날조 X, STOP 아님).

## 10. 이월 (로드맵으로 이관 — P5 캡처)

- 제안 2~5(Option 1 기준) — 외부 연구 위임 과제.
- v1.0.16 물리-데이터: 다온도 실측 per-T n 상수성 진단 → two-phase 폭 T-의존 확정(4단 사다리 (2)~(4)) · LCO Ω/dH_a 실값 · 다온도 T² 실측 · 서지 재확인.
- v1.0.17 [선택] 중 P2 미완분(있으면).

## 11. Correction History

- (초안, 2026-07-08) 신규 발전 제안서(5 물리 확장) 추출 검증(원본 프레임·표준식 정합, 오류 0) + 이월 인벤토리 + 누적 이력 → 3-트랙 v1.0.18(register 이월 완결 + 제안 1 vib Einstein 구현 + 제안 2~5 로드맵), 6-페이즈, 9종 체리피킹. **§9 Decision Gate(물리 스코프) GO 대기.**
- **(2026-07-08 GO·스코프 확정) 사용자 결정 = 2-버전 제작**: **v1.0.18.1**(이월 완결만 = §9 Option 2 의 A 트랙) + **v1.0.18.2**(= 18.1 기반 + 제안 1 vib Einstein 구현 + 제안 2~5 로드맵 = A+B+C). 18.2 는 18.1 을 증판 base 로 삼는 superset(회사가 안전 폴백판 18.1 / 물리판 18.2 선택 가능). 실행 구조(8-페이즈) = `../results/process/V1018_EXECUTION_LEDGER.md`. 물리 스코프 Decision Gate 해소.
