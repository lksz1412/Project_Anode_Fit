# Phase P6 — 전역 컨벤션·용어·어조 통일 Result

## Summary
rubric 전 항목 스윕(grep 근거 STEP_LOG 기록) 결과 위반 실건 3묶음만 적발·정정: ①C2 금지어 "가역열" 1건(ch1_appB) ②C4 MSMR 첫 출현 병기 대소문자(ch1_sec00 — 명명 원전·Ch2 와 통일) ③appendix 붙임 표기 8건(정규용액 7·격자기체 1). 그 외 전건 무위반 확인 또는 근거 있는 유지 판정(2상역/두-상 의미 분업·청유형 관용·fig 캡션·G1 유지·G3 추가 후보·G4 기각·tab:notation 소관 밖). diff P5→P6 완전 ±0 — 수식·라벨·서지·자산 불닿음 실증.

## Step Range
Steps 73–80.

## Inputs
전 tex(Ch1 24 + Ch2 15 + appendix 전문 정독)·V1020_STYLE_RUBRIC·마스터플랜 P6 절.

## Files Created
plans/PLAN_P6_convention.md·snapshot_v1020_p6.json·STEP_LOG_P6·본 RESULT.

## Files Updated
- ch1_appB_codemap(가역열→가역 발열)·ch1_sec00_intro(MSMR 병기 대문자 통일)·appendix_phase_separation(정규용액 ×7·격자기체 ×1 붙임).
- (전건 표면·문장 수준 — D11′ CHANGE_LOG 등재 대상 없음: 수식·수치·부호 불닿음, diff ±0 이 증빙.)

## Read Coverage
- 전문: appendix_phase_separation(1–497, P6 소관 신규).
- 스윕: 전 tex 파일 grep(용어별 명령·매치 수 STEP_LOG 기록) + 매치 문맥 정독(2상/두-상 전 출현 16곳 포함).

## Execution Evidence
- 빌드 3본 GREEN: Ch1 65p·Ch2 25p·appendix 8p — err0·참조/인용 undef0.
- 구조 PASS(P5 와 동일 수치). diff(P5→P6): 라벨·eqblocks·자산·bibitems 전 항목 ±0.

## Validation
- Gate "rubric 항목별 전 파일 스윕 기록": PASS(STEP_LOG Steps 74–78 — grep 근거·판정·처리 전건).
- Gate "tab:notation 신설 기호 전건": PASS — 신설 기호 전건(Ξ₁⁰·⟨n⟩⁰·U·t)이 [등장부 부연 정의·충돌 가드] 완비, 표는 N0 실험조건 매핑 전용 소관 판정(등재 0 — 판정 기록).
- Gate "불변 가드": PASS(diff ±0·자산 336/21).
- Gate "빌드/구조검증": PASS.

## Gate
**PASS** (PASS_P6_CONVENTION)

## Confirmed Non-Changes
"2상역·2상 공존"(상도표 영역) vs "두-상"(전이 유형) 의미 분업 유지. appendix "혼합 X" 내부 일관 체계 유지(본문도 혼합 엔탈피 병용 — P7 재론 가능 기록). 청유형 "~고 하자"(본문 관용 존재). fig:occ_config 캡션. `% 자산` 주석 내 축약 표기. G1 부록 번호 방식(위험>이득). G4 bib 키(기각). 표지 버전 스탬프(헤더 보존 지시).

## Open Issues / Decision Queue
- **(P7 서지 큐) appendix 참고문헌 [A1]~[A5] 5건이 REFERENCE_LEDGER 검증 범위 밖** — P7 서지 최종 정합에서 온라인 전수 검증 필요(F-6).
- **(추가 후보 — 사용자 결정)** G3: Ch1 제목 꼬리 "— 유도 확장 (재작성)" 는 D1(자기 이력) 관점 제거 후보이나 제목 보존 원칙상 무변경 유지 — P8 HANDOVER 로 전달.

## Next
P7(통합 검수 — 4창 union·triage·최종 Fable 패스 + 서지 3자 정합) — Step 81 부터.
