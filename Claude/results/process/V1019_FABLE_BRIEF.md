# Fable 브리핑 — Ch1 전면 재작성 (v1.0.19)

> 너(Fable)는 흑연 리튬이온 음극 dQ/dV(ICA)·DVA 물리 교재 **Chapter 1 을 전면 재작성**한다. 기존 절 구조는 버리되 **물리·화학 논리는 전부 보존**한다. 이 문서 = 네 브리핑(자료·방향성·규범·조건). 아래 §자산 체크리스트는 **완결성 앵커** — 신본이 이 자산을 모두(어디에 넣든) 담아야 한다.

## 0. 과제 한정
- **대상**: Ch1 문건만. Ch2·appendix·**코드는 이번 범위 밖**(고정 = v1.0.18.2). 코드가 구현한 모델과 **모순 없어야** 하고 **코드에 없는 새 물리 도입 X**(재작성 = 논리·구조·서술·유도의 재구성이지 새 물리 아님).
- **자유**: 세부 절 구조·순서·틀은 **자유롭게 재설계**(누적 증분으로 쌓인 구조 문제 해소가 재작성 목적). 
- **불변**: 물리·화학 논리 자산(§자산)·수치값·사용자 식별자(기호·라벨키는 재설계 가능하나 의미 보존)·코드 모델 정합.

## 1. 산출 방식 (한 세션·골격→절별→합치기)
1. **먼저 새 목차/골격** 산출: 신 절 구성 + **각 절이 어느 자산(§)을 담는지 매핑**. (master 조기 게이트: 골격이 자산 전부 덮나 확인 후 진행.)
2. **절별 개별 파일** write: `docs/v1.0.19/_sections/ch1_secNN.tex`(절별) + `ch1_preamble.tex`(preamble·매크로). 마스터 `graphite_ica_ch1_v1.0.19.tex` 는 `\input{_sections/...}` 로 조립 → **절마다 증분 빌드 확인**. (절별 파일 = checkpoint·resume 앵커.)
3. 전 절 완료 후 합본 빌드 통과. **각 절 끝에 담은 자산 번호 주석(% [A-nn])** 남겨 대조 가능케.
- xelatex/kotex, 3-pass. Ch2 참조는 별도 컴파일이므로 **리터럴 텍스트**(예 "Ch2 vibrational 절", "\S1.7")로(‑ \ref 로 Ch2 라벨 참조 금지).

## 2. 헌법 3종 + 문체 규범 (rubric)
- **① 교과서 register**: 본문은 물리·모델을 서술. "코드가 X 한다"·코드 함수명·내부 라벨·changelog 메타·방어 어투("~가 아니다") 금지. 코드 참조는 **구현 대응표(부록)** 에만.
- **② 논문 깊이**: 유도·엄밀·완결. 기호 충돌·미정의·gap 미태깅·서지 누락 = 결함.
- **③ 수식-주도**: 결과 박스 **(a)출발→(b)연산→(c)중간식(≥1)→(d)박스** 일관. assert-jump(출발→결론 비약) 금지.
- **문체 규범**(feedback_anode_fit_textbook_style): 완결 문장(괄호 전보체 X)·**보편식 먼저, 극한은 코너**·절 도입/마무리 다리·**피팅은 코드 작성 가능 수준(시뮬+round-trip 실증)**·**분량은 콘텐츠의 자연 결과**(억지 축소/팽창 X). 본문 한글 prose + 학술/기술 용어 영어 원어.

## 3. 버전 진화·방향성 (계획서 1.0.10~1.0.18 요지 — 왜 이렇게 왔나)
- **1.0.10** matched baseline: dQ/dV 정상 종개형 실증. broadening(집합 통계역학·사이즈 제외)·**w 이중지위**·w_eff 제거.
- **1.0.12** LCO 6절 줄글→수식화, 방향 규약 **f=+σ_d**(전극 중립 한정).
- **1.0.13** **Part 0 통계역학 기초 신설**(분배함수→lattice gas→정규용액→Nernst)·LCO 후방 **Part II** 통합·재구조화.
- **1.0.14** 어투·물리 엄밀성·**부록 A(부호 검산표)/B(구현 대응표)**·본문 코드-언급 0·레퍼런스 DOI 병기.
- **1.0.15** ★**이산 전압 격자 완전 퇴출 → 점별 연속 인과 기억 적분 아키텍처**(eq:memory/lag/tail-limit/reversal). 격자 잔재 금지.
- **1.0.16** **폭 다중도 n(T) 온도함수 피팅**(additive; 부재=상수 n bit-exact)·가역열 config 전파(∂w/∂T).
- **1.0.17** register/정합/완결성 정련: 본문 코드 참조 제거·서지 7 저자+DOI 2 정정·기호 정합·마스터표 caption.
- **1.0.18** ★**제안1 vib Einstein 양자보정**(additive; 동결 ΔS_vib → S_vib(T;θ_E), θ_E 부재=bit-exact). Ch2 유도·Ch1 eq:lco-slots vib 노트.
- **관통 방향**: 통계역학 first(분배함수→분포→관측) · 점별 연속(격자 X) · additive 확장(기본 bit-exact) · doc↔code · 코드 작성 가능한 피팅. **★백지 재작성 실패 전례**(Fable 감사): v4/v5 broadening 2771→894줄 후퇴·Eyring 척추·S0-S5 방향성 유실 — **반복 금지**(자산 전부 보존).

## 4. 자료 경로 (필요 시 정독)
- **계획서 1.0.10~1.0.18**: `Claude/plans/` — v1010(2026-07-01~06 다수)·v1013 restructure·v1014 tone-rigor·v1015 code-doc-sync·v1016 은 v1018-physics-extension 안·v1017 register·v1018 physics-extension. (진화·11-section·N종 체리피킹 방법.)
- **이력 1.0.18**: `Claude/results/process/V1018_EXECUTION_LEDGER.md` · `Claude/docs/v1.0.18.1/HANDOVER_v1.0.18.1.md` · `Claude/docs/v1.0.18.2/HANDOVER_v1.0.18.2.md`.
- **작업물 1.0.18(이전본 = 재작성 원본)**: `Claude/docs/v1.0.18.2/graphite_ica_ch1_v1.0.18.2.tex` (58p·~3540줄). **전문 정독 후 재작성** — 담긴 물리·화학 논리를 모두 신본에 옮기되 틀은 새로.
- **코드 모델(정합 기준)**: `Claude/docs/v1.0.19/Anode_Fit_v1.0.18.2.py` (미변경). 신본 식 = 이 코드 거동.

## 5. 자산 체크리스트 (완결성 앵커 — 신본이 전부 담아야)
> **전수 목록 = `Claude/results/process/V1019_ASSET_CHECKLIST.md`(336 항목, 반드시 정독).** 이전본 Ch1 전수 추출(A-001~159 전반부 + B2-001~177 후반부, head→tail 갭 0). 신본은 각 자산을 **어느 절에든 반드시 포함**하고, 담은 절에 `% [A-nn]`/`% [B2-nn]` 주석을 남긴다. 10종 검수(P3)가 이 목록으로 유실(regression)을 잡는다. **틀은 버려도 이 336 자산의 물리·논리는 전부 살아 있어야 한다.**

**★★ 최우선 보존 — CRITICAL 오독방지 앵커 12종(반드시 명시 문장으로 재현)**:
A-035 Fermi-Dirac 함수형 가드 · A-094 Taylor 함정(Ωu·artanh 함께 전개) · A-105 폭 이중지위(단상 평형예측/두-상 자유폭) · A-132 Maxwell–Dreyer 화해(값/경로) · A-137~139 기작③ iii-a 평형층(공통전위·순차)·iii-b broadening층(U_app=U_j+η, U_j 상수) · B2-054 Kirchhoff(∫ΔS dT') · B2-069 Ω≠config ΔS · B2-084/085/121 단위(몰당 N_A·eV→J) · B2-105 슬롯규칙(config/vib/elec, 이중계산 방지) · B2-107 가산성≠무이중계산 · B2-116 함수형 동형≠물리량 동일 · B2-094 세 척도 구분.

**중심 공식·닫힌식(반드시 유도-완결로)**: eq:Uj(A-081)·eq:spinodal(A-088)·eq:dUhys(A-093)·eq:Ubranch(A-096)·eq:xieq(A-112)·eq:eqpeak(A-126)·eq:lag(B2-019)·eq:reversal(B2-027)·eq:sum(B2-030)·eq:dSegate(B2-091)·eq:lco-decomp(B2-106)·eq:lco-msmrmap(B2-115). Part 0 사다리(A-015~069) 전 유도 사슬 보존.

**표·그림(논리 나름)**: tab:notation·tab:staging·tab:lco-staging·tab:inputs(θ_E 행 포함)·tab:symcode·tab:nodemap / fig:spine·fig:hysloop·fig:logistic·fig:broadening·fig:reversal·fig:lco-electronic 등. 서지 24종(B2-154~177, tier 등급·과인용 가드 포함).
