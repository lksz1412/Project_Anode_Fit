# STEP_LOG P5 — Ch2 phase 스텝 이력

## Step 63 — 계획서 저장
- PLAN_P5_ch2.md.

## Steps 64–66 — 전문 정독 + 보강 지도
- Read Coverage(잔여 8 + 재확인 4): sec05(1–241)·sec06(1–53)·sec07(1–59)·sec08(1–145)·sec09(1–44)·sec10(1–26)·appA(1–75)·appB(1–70) 신규 전문 + sec00(68)·sec01(145)·sec02(189)·sec03(96) 재확인(컴팩션 후 상세 복원). sec04(115)는 컴팩션 직전 전문 정독분 계승.
- 판정: **Ch2 는 D7 위반 없음** — §2.1 이 이미 정통 선행(eq:Z1 bare 대정준 → μ–V 연결 → BW)이고, q(T)/ε̃ 흡수는 Ch1 §2 참조 서술로 이미 정합(sec01:39–49, ε̃=ε₀−k_BT ln q(T) 문자 일치). sec04~10·appA·appB 는 인용·규율 완비로 무변경. 편집 소요 4건만 확정: ①U9(sec05 각주 — 인용 0) ②U10(sec02:9, low) ③sec03 서두 배경 연결(Ch1 §2 bgbox 후방 다리 부재 — P2 에서 Ch1 쪽 forward 다리만 생김) ④sec03 eq:Svib_mode 도입부 D3 중간식 점프("어느 경로든 …닫힌형" — −∂f/∂T 에서 닫힌형까지 대수 생략; FD 측 eq:Se_start→eq:Se-ch2 사슬은 노출 완비로 비대칭).

## Step 67 — 보강 지도 확정 + CHANGE_LOG 사전 등재
- C-017(ch2_bib:dahn1991)·C-018(ch2_bib:ohzuku1993)·B-005(sec03 D3 중간식 인라인 노출). 배경 연결 문장·U10 포인터는 D11′ 규칙상 문장 다리 → RESULT Files Updated 갈음.

## Step 68 — 편집 (4건 + 결 다듬기 1)
- sec05 각주: "\cite{dahn1991,ohzuku1993}" 부여(U9 — U3 처리와 동일 패턴).
- ch2_bib: 2종 등재(ch1_bib 검증 표기 문자 동일 — 3자 정합)·헤더 카운트 14→16.
- sec03 서두: 배경 연결 1문장("왜 BE/FD 를 따르는가 — 교환 대칭성·스핀–통계 — 는 Chapter 1 §2 의 배경 박스가 정리").
- sec03 ssec:vib: B-005 인라인 중간식(곱규칙 로그 항 + β 연쇄율 점유 항 → S=−k_B ln(1−e^{−βℏω})+k_B βℏω n_k → BE 항등식 2개 대입) — master 재유도 검산 완료, 표시 수식 블록·라벨 불변.
- sec02:9: "(\S\ref{ssec:litverif})" 병기(U10).

## Step 69 — 빌드·변경 통제 (환경 사건 1건 포함)
- 구조 PASS: Ch1 라벨 222(dup0)·refs 732(미해소 0)·cite 96/bib 36·미인용 0·자산 336 / Ch2 라벨 69(dup0)·refs 200(미해소 0)·**cite 34/bib 16**·미인용 0·자산 21·수식블록 32(boxed 10).
- diff(P4→P5): Ch1 전 항목 ±0(완전 불변) / Ch2 라벨 ±0·**eqblocks +0/−0/~0**·자산 21 유지·**bibitems +2(dahn1991·ohzuku1993) = C-017·C-018 과 1:1**.
- **환경 사건**: 컨테이너 재생성으로 texlive-fonts-recommended 소실 → hyperref(xetex) pzdr.tfm 실패("No pages of output") → apt 재설치로 복구(PLAN_P5 Correction 기록). 재빌드: **Ch2 25p·err0·undef0**(v1.0.19 기준 페이지수 동일) + **Ch1 65p·err0·undef0**(P4 증거 재현 — 현 환경 유효 확인).

## Step 70 — 후방 정합 (Ch1↔Ch2)
- Ch2→Ch1 리터럴 참조 전수 대조(11종 23곳): §1(V_n·σ_d 분극)·§2(Part 0 — Ξ₁ 표기·q(T)→ε̃ 흡수 문자 일치·bgbox·섞임 엔트로피)·§3(평형 중심)·§4(γ_j·spinodal u_j=√(1−2RT/Ω) 잔존 확인)·§5(평형 진행률 제목 일치)·§7(broadening 제목 일치)·§8(Eyring/활성화 확인)·§13·§14(삼분해 제목 일치)·§15(eq:Se 라벨 잔존 — eq:Se-ch2 와 별개 공존)·§17(MSMR) — **전건 유효**(P2~P4 가 Ch1 절 번호·라벨을 불변 유지했으므로 리터럴 참조 파손 0).
- 신설 후방 다리로 P2 의 Ch1→Ch2 forward 다리(bgbox 말미 "포논 BE·전자 FD 실사용처")와 양방향 분업 완성.
- appA 함정표 행(u_j 동명 별개·eq:Se 라벨 구분·방전 라벨 층위) 전부 현행과 정합 — 무변경 유지.

## Steps 71–72 — 기록·커밋
- baseline U9·U10 ✅ 기입. PLAN_P5 Correction(환경 사건). 본 STEP_LOG·RESULT_P5·ledger·커밋.
