# V1.0.19 최종 검수 UNION (R-P1) — 3종 정합성(Ch1↔Ch2↔code)+완결성, G-follow·논문깊이·G-usable

> 5창(RW1 Ch1↔code·RW2 Ch2↔code·RW3 Ch1↔Ch2·완결·RW4 G-follow·RW5 G-usable) → master union·삼각검증. R-P1 fix로 정정.

## ★ 종합 판정
- **물리·정합·완결 핵심 무결**: Ch1↔Ch2 모순 0(교차참조·공유기호·tab:worked 재계산 전항)·Ch1↔code bit-exact 고충실도·Ch2↔code 회귀값 bit-exact·자산 336+133 커버·CRITICAL 물리오류 0.
- 결함 = (A)버전 staleness(내 K-P1 후 메타문서 미갱신) (B)appendix/guide 미갱신 (C)★G-usable 피팅 round-trip 실증 부재 (D)부록B doc↔code API (E)물리 honesty caveat (F)G-follow/수식주도 폴리시. 물리 골격 무관.

## Cluster A — 버전 staleness (HIGH, master 직접 fix)
- **A1** [RW3-1] HANDOVER §②-1/§③ + `graphite_ica_ch1/ch2_v1.0.19.tex:7` 헤더가 "코드=Anode_Fit_v1.0.18.2.py 미변경·개정 차기 이월"이라 주장 → **코드 이미 v1.0.19(K-P1 완료)**. HANDOVER·2 마스터 헤더를 "코드 v1.0.19 개정 완료(x̄ 진입점·회귀 bit-exact)"로 갱신.
- **A2** [RW3-10] appendix PDF 표지 "1.0.18.2 초안" → "v1.0.19 승계·미개정" 각주.

## Cluster B — appendix Ch1 절번호 stale (HIGH, Fable)
- **B1** [RW3-2] `appendix_phase_separation.tex` L42-43/381-382/476-477: "§1.2"→§2(Part0)·"§1.5"→§4.2(sec:hys-gap)·"§1.7"→§7(sec:broadening). [RW3-12] 연결절에 Ch2 ssec:BW 언급(선택).

## Cluster C — ★G-usable 피팅 round-trip + 스크립트 (CRITICAL/HIGH, Fable 코드+가이드)
- **C1** [RW5-1 CRITICAL] **역방향(피팅) round-trip 실증 예제 부재** — forward 자기일관성만 있고 합성곡선→피팅→파라미터 회복 실행 예제·optimizer·손실함수 0. 사용자 #3 기준("피팅=코드 작성 가능 수준(시뮬+round-trip 실증)") 미충족. → **피팅 round-trip 데모 스크립트 추가**: 알려진 θ*로 합성 dQ/dV(+잡음) → 정규화 residual 손실 → tier 개방 회복 → 회복오차·수렴 제시. v1.0.19 폴더 동봉.
- **C2** [RW5-2/RW3-3/4] FITTING_GUIDE §6/§7이 v1.0.19 폴더에 없는 구버전 스크립트(test_regression_graphite.py·graph_suite_v1016 등) "본 폴더 소재"라 지칭 → **골든 13/13 대조 + 그래프 suite를 v1.0.19 import로 재작성·동봉**(또는 명시적 경로). __main__이 golden 미로드 → 골든 대조 추가.
- **C3** [RW3-5] samples/(K-P3 fig_*_x.png·continuity_scan) FITTING_GUIDE 미언급 → §7에 반영.
- **C4** [RW5-6] §6 수렴 게이트 "잔차<1e-4(정규화 dQ/dV)" 정규화 미정의(gate 확인불가) → 정규화 정의(예 peak max=1 스케일 점별 잔차 제곱평균).
- **C5** [RW5-7] S3 dVdq_qa 산출 절차(컷점 q_a·기울기) 닫힌 식 부재 → 절차 명시.
- **C6** [RW5-3] Phase D 다온도 LCO 전자항 T-복원을 코드 미구현(T_ref 동결)인데 가이드가 지시(과약속) → 가이드 Phase D에 "현 코드 T_ref 동결·T-복원은 사용자 구현/차기" 명시(scope 정직).
- **C7** [RW5-11] LCO tier-2/3 초기값(Ω_j·dH_a 문헌 범위) 부재로 LCO 피팅 미착수 가능 → 초기값 가이드(선택·갭 명시 강화).

## Cluster D — 부록B doc↔code API (MED, Fable)
- **D1** [RW2-1/RW5-9] `ch2_appB_codemap.tex` B.2 `entropy_coefficient(x̄=0.25)=−0.204` → 코드 `entropy_coefficient`는 V_n 입력(−0.204는 `entropy_coefficient_x(x̄)`) → **`entropy_coefficient_x(x̄=0.25)`로 정정**.
- **D2** [RW2-2/RW5-8/RW3-6] 신규 x̄ 진입점(solve_U_oc·entropy_coefficient_x·reversible_heat_x) 부록B·tab:nodecode·가이드 미명명 → 요구명세·nodecode `solve_U_oc`(eq:implicit) 행·가이드 x̄ 사용 시점 추가.
- **D3** [RW5-4] `ch1_appB_codemap.tex` tab:inputs에 n(T) 키(`n_T1`/`n_T_ref`) 누락(θ_E는 있음) → 행 추가(기본 부재=0/298.15·eq:dwdT-nT).
- **D4** [RW1-1] Ch1 codebox N2가 U_j에 `_vib_dU` 가산 누락 → "(+ _vib_dU; θ_E 부재=0 bit-exact)" 한 절.
- **D5** [RW1-2] tab:symcode `s` "코드 미대응" → 코드 `s` 파라미터(σ_d 받는 자리)와 유도-전용 s 구분 비고.
- **D6** [RW5-5] MSMR "ω_j↔w_j" — 재모수화([V] 흡수) 여부 §17 확인 후 codemap/주석에 "ω_j(문헌 무차원, w=ω·RT/F)↔w_j 또는 ↔n_j" 명확화(문헌 ω 직접 'w' 대입 오류 방지).

## Cluster E — 물리 honesty caveat (MED, Fable)
- **E1** [RW2-3] tab:qrev 캡션에 "행별 흡/발열 판정은 완전식(열적 폭) 전제·두-상 T-동결 시 단순식 기준으로 이동(x̄≈0.75 부호반전)" caveat.
- **E2** [RW1-3] Ch1 §15 eq:U1T2 "곡률은 전자항 단독" → "(본 절 config·vib 고전근사 전제 하)·잔여 vib 양자곡률은 θ_E(Ch2)" caveat.
- **E3** [RW3-7] Ch1 §7 broadening 분류에 "Ω>2RT는 4전이 모두 만족·실제 분류 근거는 문헌 상평형"(§5/Ch2와 동일) 한 문장.
- **E4** [RW3-8] Ch1 §10 "w 폴백+n=1 함께" → "n=1 우선 적용·실초기폭 균일 RT/F·w폴백은 n제거 시 대안" 명시.

## Cluster F — G-follow / 수식-주도 (MED, Fable)
- **F1** [RW4-8] Ch2 §2.4 u_j(θ_E/T)가 Ch1 §4 spinodal u_j와 충돌 → 각주 "Ch1 §4 spinodal u_j와 무관"·부록A 함정표 행 추가.
- **F2** [RW4-9] Ch2 θ(점유율) vs θ_E(Einstein 온도 K) 충돌 → §2.4 도입 명시·부록A 행 추가.
- **F3** [RW4-10] Ch2 §2.4.2 eq:dUvib 적분 중간식 삽입((a)(b)(c)(d) 관행 복원).
- **F4** [RW4-11] Ch2 §2.5.1 eq:implicit_diff 전미분 연쇄율 중간식 삽입.
- **F5** [RW4-5] Ch1 §15.2 Sommerfeld 고차보정(홀×짝·Mott) 각주/부록로 이동, 본문은 결론만.
- **F6** [RW4-3] Ch1 §8.3 eq:dHeff 방전/충전 부호 미니표. [RW4-4] §7.3 Fredholm "불안정" 잡음증폭 직관 한 줄. [RW4-7] §17 f=+σ_d 유일해 계수비교 한 줄. [RW4-6] §7.2 괄호 남발 분리. [RW4-1] tab:notation 참조용 안내. [RW4-2] §2.2 q(T) 각주 선행안내.

## Cluster G — LOW/NOTE (선택·기록)
- RW2-4 파생A 스팬 기재·RW2-5 eq:Svib-einstein 참조 1회·RW3-9 θ_E Ch1→Ch2 위임 명시·RW3-13 "4 plateau"→"4-전이"·RW3-14 Z1 q≡1 단서·RW3-15 z 배위수/전하수 각주·RW3-16 h 정의·RW3-17 appB v1.0.18.2 provenance·RW3-18 broadening 문장·RW3-19 γ 충돌(현행 각주 충분).
- RW3-11 appendix 미편입 = 사용자 결정 대기(조치 없음). RW1-4/RW2 LCO 시연 loose = doc-leads 정직 hedge(결함 아님).

## fix 배정
- **master 직접**: A1·A2(버전 staleness 메타문서).
- **Fable(코드+문건)**: C1 피팅 round-trip 데모·C2 검증 스크립트 v1.0.19 이관 + B·D·E·F 문건 정정 + C3~C6 가이드. G는 선택 반영.
