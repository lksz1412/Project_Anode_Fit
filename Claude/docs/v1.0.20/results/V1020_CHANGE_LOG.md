# V1020 변경 통제 로그 — 물리적 변경(보강·ERRATA) 전수 등재부

> 규칙([D11′], 마스터플랜 §2): **물리 내용에 닿는 모든 변경은 편집 전 여기 등재.** 스냅샷 diff(eqblocks ±~)의 전 항목이 본 로그와 1:1 대응해야 gate PASS. 표현·문장 다리·인용 부여는 phase RESULT 의 Files Updated 로 갈음(여기 등재 X — 단 수식·수치·부호에 닿으면 등재).
> 종류: **보강**(신규 식·유도·배경 추가 — 기존 물리 불변) / **ERRATA**(기존 물리 오류 정정 — 코드 영향 판정 필수) / **서지정정**(bibliography 필드 정정 — 물리 무관).

## 등재부

| ID | 종류 | 위치(파일:라벨) | 구판 요지 | 신판 요지 | 근거(재유도/문헌) | 코드 영향 | Phase |
|---|---|---|---|---|---|---|---|
| C-001 | 서지정정 | ch1_bib:ml2024 | JMPS 190, **105727**·DOI …105727·Teichert 제1저자(arXiv판 순서) | **105726**·DOI 10.1016/j.jmps.2024.105726·출판판 저자 순서(Faghih Shojaei 제1) — 기재 DOI 는 실재하는 타 논문을 가리키던 위험 유형 | Crossref 105726/105727 대조 + master 독립 재검증(WebSearch) | 무 | P1 |
| C-002 | 서지정정 | ch1_bib:leviaurbach1999 | 제목이 별개 논문(JEAC 421, 79, 1997)의 것과 혼합 | 제목을 실제 1999 리뷰("Frumkin intercalation isotherm — a tool …: a review")로 교체·쪽 167–185 보완(서지·DOI 는 원래 리뷰 것 유지 — 인용 취지[내재 평형 폭·Frumkin] 부합 정정안 a) | Crossref + master 독립 재검증 | 무 | P1 |
| C-003 | 서지정정 | ch1_bib:ohzuku1993 | 제목 무표시 절단 | 출판 제목 전문 복원("…and Their Application as a Negative Electrode for a Lithium Ion (Shuttlecock) Cell") | Crossref | 무 | P1 |
| C-004 | 서지정정 | ch1_bib:msmr2024 | 제목 "(MSMR)" 삽입·Part I 표기 | 출판 표기 복원(Part 1·삽입어구 제거)·병기 Part II 권·아티클 103505 보완 | Crossref | 무 | P1 |
| C-005 | 서지정정 | ch2_bib:msmr_partI | 아티클번호 미기재 | 023502 보완 | Crossref | 무 | P1 |
| C-006 | 서지정정 | ch2_bib:msmr_partII | 제목 "MSMR" 축약·구두점 상이·아티클 미기재 | 출판 제목 전문·103505 보완 | Crossref | 무 | P1 |
| C-007 | 서지정정 | ch2_bib:hysteresis2018 | 쪽 미기재 | 179–184 보완 | Crossref | 무 | P1 |
| C-008 | 서지정정 | ch1_bib 헤더 주석 | "서지 — 24종"(stale) | "28종" + 검증 원장 참조 | 실측 카운트 | 무 | P1 |
| B-001 | 보강 | ch1_sec02a:§2.2(eq:partfn 주변) | 첫 유도부터 q(T) 포함(Ξ₁=1+q e^{-βΔ}) | **D7 2단 재배열**: [원형 — 내부 자유도 없는 2-상태 Ξ₁⁰=1+e^{-β(ε₀-μ)}·⟨n⟩ 박스(신규 라벨)] → [확장 — q(T) 도입·기존 eq:partfn~eq:fermifn 사슬] → [q≡1 원형 회수 검산]. **최종식·기존 라벨·수치 전부 불변**(재배열+중간식 노출) | 교수 감수 F-2·Ch2 §2.1 기존 순서와 정합·hill1960/mckinnon1983 | 무(물리 불변) | P2 |
| B-002 | 보강 | ch1_sec02a:§2.2(원형 박스 직후) | 페르미온/보손 배경 부재 | 배경 bgbox 신설: 동일입자·교환대칭 → 페르미온(Pauli 배타·FD)/보손(BE) 최소 배경 → 본 문건 0/1 은 기하적 배타(양자 아님) 명시 → Ch2 실사용처(포논 BE·전자 FD) forward 다리 | F-1·mcquarrie1976 | 무 | P2 |
| B-003 | 보강 | ch1_preamble·ch2_preamble | bgbox 환경 없음 | `\newtheorem*{bgbox}{배경}` 신설(자족 블록 — 부록 이동 가능 설계, 사용자 D-2 유보 대응) | 렌더 체계 기존 박스 5종과 정합 | 무 | P2 |
| C-009 | 서지추가 | ch1_bib:ashcroftmermin1976 | 미등재(Ch2 소관도 아님 — 원장 V1 만) | ch1_bib 등재(Solid State Physics, 1976 — Ch.2·Appendix C 장 수준) — §2.2 bgbox 인용 + P4 §15 Sommerfeld 예정 | 원장 V1(P1 검증) | 무 | P2 |
| (B-001 확정 기록) | — | ch1_sec02a | — | 신규 라벨 3종 = eq:sm-baresum·eq:sm-baremid·eq:sm-bare. 스냅샷 diff: +3/−0/~0·자산 336 보존 — 기존 수식 해시 전부 불변 실증 | tools_check_structure diff(P2) | 무 | P2 |
| C-010 | 서지추가 | ch1_bib:dreyer2011 | 미등재 | 등재(CMT 23, 211–231, 2011 — many-particle 준안정성 동반 논문) — §4 계보 다리·§7(iii-a) 병기 | 원장 V1(P1 검증) | 무 | P3 |
| B-004 | 보강 | ch1_sec15:§15.1 | MIT 배경(밴드/Mott 절연체 구분·1차 전이 기작) 부재 — 개념이 전제로 사용됨 | MIT 배경 bgbox 신설(경쟁 저작): 밴드 절연체 vs Mott 절연체 → LiCoO₂(x=1)=밴드 절연체 → 탈리튬화 정공의 1차 MIT = 불순물 준위 Mott 전이(Marianetti) → 게이트 현상학화 다리. **기존 식·라벨 불변** | F-4·mott1968/imada1998/marianetti2004/menetrier1999 | 무 | P4 |
| C-011 | 서지추가 | ch1_bib:mott1968 | 미등재 | RMP 40, 677–683 (1968) — Mott 원전 | 원장 V1 | 무 | P4 |
| C-012 | 서지추가 | ch1_bib:imada1998 | 미등재 | RMP 70, 1039–1263 (1998) — MIT 리뷰 앵커 | 원장 V1 | 무 | P4 |
| C-013 | 서지추가 | ch1_bib:marianetti2004 | 미등재 | Nat. Mater. 3, 627–631 (2004) — LCO 불순물 Mott 전이 기작 | 원장 V1 | 무 | P4 |
| C-014 | 서지추가 | ch1_bib:vanderven1998 | 미등재 | PRB 58, 2975–2987 (1998) — LCO 제일원리 상도표·order–disorder | 원장 V1 | 무 | P4 |
| C-015 | 서지추가 | ch1_bib:msmr_origin2017 | 미등재 | JES 164(11), E3243–E3253 (2017) — MSMR 열역학 원전(Verbrugge 외 5인·byline 이니셜 없음) | 원장 V1 | 무 | P4 |
| C-016 | 서지추가 | ch1_bib:bakerverbrugge2018 | 미등재 | JES 165(16), A3952–A3964 (2018) — "Multi-Species, Multi-Reaction" 명명 원전 | 원장 V1 | 무 | P4 |
| C-017 | 서지추가 | ch2_bib:dahn1991 | 미등재(ch1_bib 에만 존재) | ch2_bib 등재(PRB 44, 9170, 1991 — Li_xC6 상도표) — §2.5 파생 C 각주 U9 인용용. ch1_bib 표기와 동일(3자 정합) | 원장 V1(P1 검증) | 무 | P5 |
| C-018 | 서지추가 | ch2_bib:ohzuku1993 | 미등재(ch1_bib 에만 존재) | ch2_bib 등재(JES 140, 2490, 1993 — 흑연 삽입 화합물 형성·C-003 정정 제목 전문) — §2.5 파생 C 각주 U9 인용용 | 원장 V1(P1 검증) | 무 | P5 |
| C-019 | 서지정정 | appendix_phase_separation:[A5] | 장 귀속 "Ch.~17--18 (Cahn--Hilliard 선형화·핵생성 이론)" | "Ch.~18--19" — 실제 목차: Ch.18 Spinodal and Order-Disorder Transformations(p.433)·Ch.19 Nucleation(p.459). 본문 [A5] 언급 3곳(L57 서두 원천 나열·L403·L439 — P7 검수 C2F1/C2F2 교차 실측으로 집계 정정, 구 기재 "2곳")은 전부 장 번호 무표기라 무변경 | Wiley TOC·서지 레코드(P7 Step 84 온라인 검증) | 무 | P7 |
| E-001 | **ERRATA** | ch2_sec00:20–21 | 서두 대비 수사: "전이마다 상수 ΔS_rxn,j 를 가정하는 평형 정전 식만으로는 재현되지 않는다 — 상수 엔트로피는 SOC 축 위에서 봉우리·골·**부호 반전**을 만들 자유도 자체가 없기 때문이다" | 과일반화 정정: 상수 ΔS_j 도 겹침 가중(단순식·tab:qrev)만으로 SOC 축 부호 교차를 냄 — 상수가 못 만드는 것은 봉우리·골(경계 발산형 구조)이고 부호 교차도 매끄러운 블렌드가 아닌 계단형에 그친다는 것. 불명 용어 "평형 정전 식" 제거(문서 유일 용례·무정의 — C2F3-02) | P7 검수 C2F3-01/02 + master 재유도(문서 자체 §2.5 단순식·tab:qrev 가 상수 가중으로 부호 교차 산출 — 자기모순 확인) | **무**(서두 수사 문장 — 코드 미구현 대상; 물리 골격·수식·수치 불변) | P7 |
| B-006 | 보강 | ch2_sec08:§2.8.2 도입 + ch2_appB:B.4 | 계산 예제·회귀 기준 U_oc=74.4 mV 의 입력 U_j 평가 규약 무명세 — 표시 반올림 전위(85 mV 등) 입력 시 74.07 mV 로 기준 미달(재현 규약 결손) | **U_j 평가 규약 명시**: U_j 는 (−ΔH_rxn,j+TΔS_rxn,j)/F 환산값으로 평가(표시 반올림값 아님) — 본문 1문장 + B.4 규약 1문. 수식·수치·기준값 자체는 불변 | P7 검수 C2F3-07(M) + C2F1·C2F2 동일 관찰(3창) + v1.0.19 코드 func_U_j 대조·독립 재계산 2종 | 무(v1.0.19 코드가 이미 이 규약으로 구현 — 스트림 2 G2 게이트 PASS 로 재확인; 명세 문서화만) | P7 |
| B-005 | 보강 | ch2_sec03:eq:Svib_mode 도입부 | "어느 경로든 보손 통계의 닫힌형" — S=−∂f/∂T 에서 닫힌형까지 중간식 생략(점프) | **D3 중간식 인라인 노출**: −∂f_k/∂T 평가 결과(S=−k_B ln(1−e^{−βℏω})+k_B βℏω n_k)와 BE 항등식 2개(1−e^{−βℏω}=1/(1+n_k)·βℏω=ln[(1+n_k)/n_k]) 대입 경로를 본문 인라인으로 명시. **표시 수식 블록·라벨·최종식 불변**(FD 측 eq:Se_start→eq:Se-ch2 사슬과 노출 수준 평행화) | 교수 감수 F-2/D3·master 재유도 검산 | 무(물리 불변) | P5 |
| B-007 | 보강 | ch1_sec14:47(eq 슬롯 규칙 내 \text)·:54·ch1_appB:100 | θ_E 온도 보정 상술처를 "Ch2 vibrational 절"로 지칭(실제 상술 = Ch2 §2.4 Einstein 절; Ch1 §15 는 이미 정확 지칭 — Ch1 내부 불일치) | 3곳 "Ch2 §2.4 Einstein 절"로 통일. **47행은 align 환경 내 \text 주석이라 eqblock 해시 변경 발생 — 수식 기호·구조·물리 전부 불변**(참조 문자열만) | P7 스트림 3 L-5(교차 대조: Ch2 §2.3 은 문제 제기만·§2.4 가 상술) | 무 | P7 |

## ERRATA 요약 (P8 코드 영향 판정 원장)
- **E-001** (P7): ch2_sec00 서두 수사 과일반화 정정 — **코드 영향 무**(서두 대비 문장, 코드 미구현 대상·물리 골격 불변). matched bump 판정 유지.
