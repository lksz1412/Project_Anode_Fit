# Phase P5 — Ch2 Result

## Summary
Ch2 전 절 전문 정독 결과 **D7 위반 없음 확정**(§2.1 은 정통 유도 선행 — bare Ξ₁ → μ–V → BW; q(T)/ε̃ 는 Ch1 §2 참조 서술로 기정합). 편집은 정밀 4건: U9 인용 부여(dahn1991·ohzuku1993 — ch2_bib +2종·C-017/C-018), U10 후방 참조, §2.3 서두에 Ch1 §2 페르미온/보손 배경 박스 후방 다리 1문장(F-1 분업 완성), eq:Svib_mode 도입부 D3 중간식 인라인 노출(B-005 — FD 측과 노출 수준 평행화). 수식 블록·라벨·자산 전부 불변. 부수 사건: 컨테이너 재생성으로 소실된 texlive-fonts-recommended 재설치(양 챕터 빌드 재검증 완료).

## Step Range
Steps 63–72.

## Inputs
ch2 전 절(sec00~10·appA·appB·bib — 잔여 8 신규 전문 + 4 재확인)·원장·baseline·ch1_bib(서지 원문)·ch1 절 지도(후방 정합).

## Files Created
plans/PLAN_P5_ch2.md·snapshot_v1020_p5.json·STEP_LOG_P5·본 RESULT.

## Files Updated
- ch2_sec05(각주 U9 인용 — 문장 다리)·ch2_sec02(U10 \S\ref{ssec:litverif} 병기 — 문장 다리)·ch2_sec03(배경 연결 1문장 + B-005 중간식 인라인)·ch2_bib(+dahn1991·ohzuku1993, 헤더 16)·CHANGE_LOG(C-017·C-018·B-005)·CITATION_BASELINE(U9·U10 ✅)·PLAN_P5(Correction — 환경 사건).

## Read Coverage
- 전문(신규): sec05(241)·sec06(53)·sec07(59)·sec08(145)·sec09(44)·sec10(26)·appA(75)·appB(70).
- 전문(재확인/계승): sec00(68)·sec01(145)·sec02(189)·sec03(96) 재확인·sec04(115) 컴팩션 직전 정독 계승. **Ch2 전 파일 커버 완료.**

## Execution Evidence
- 빌드: Ch2 **25p·err0·undef0**(v1.0.19 페이지수 동일)·Ch1 **65p·err0·undef0**(재검증).
- 구조 PASS: Ch2 cite 34/bib 16·미인용 0·미해소 0·자산 21·라벨 dup 0 / Ch1 전 수치 P4 동일.
- diff(P4→P5): Ch1 완전 불변(±0) / Ch2 eqblocks **+0/−0/~0**·라벨 ±0·bibitems **+2 = C-017·C-018 과 1:1**.

## Validation
- Gate "무인용 Ch2 소관 전건": PASS(U9·U10 ✅ — baseline 잔여 0).
- Gate "D7/D3": PASS(D7 위반 없음 확정[정독 근거]·D3 점프 1건 B-005 로 해소 — master 재유도 검산).
- Gate "배경 분업(F-1)": PASS(Ch1 §2 bgbox ↔ Ch2 §2.3 양방향 다리 완성 — Ch2 쪽은 서술형 참조로 컴파일 독립 유지).
- Gate "후방 정합": PASS(Ch2→Ch1 리터럴 참조 11종 23곳 전건 유효·appA 함정표 현행 정합·eq:Se/eq:Se-ch2 별개 공존·ε̃ 정의 문자 일치).
- Gate "불변·빌드": PASS(수식·라벨·자산 불변 + 양 챕터 GREEN).

## Gate
**PASS** (PASS_P5_CH2)

## Confirmed Non-Changes
sec04 무변경(Einstein (a)–(d) 완비·round-trip 정합·3온도점 식별 — 규율 완비 판정). sec06~10·appA·appB 무변경(극한표·Bernardi 수지·종합식·방법론·함정표·요구명세 — 인용·규율 완비). §2.3 S_e 사슬 무변경(Ch1 §15 상술 참조 구조 유지). appB 버전 표기는 P8 소관 유지.

## Open Issues / Decision Queue
- (기록) 컨테이너 재생성 시 texlive-fonts-recommended 소실 재발 가능 — P7/P8 빌드 전 `kpsewhich pzdr.tfm` 선확인 권장(STEP_LOG Step 69).

## Next
P6(전역 컨벤션·용어·어조 통일) — Step 73 부터.
