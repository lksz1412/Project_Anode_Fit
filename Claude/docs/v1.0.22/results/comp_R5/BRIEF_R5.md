# BRIEF R5 공통 — Ch3(Si·혼합음극) 경쟁 저작 (v1.0.22 — 오푸스 3창)

## 공통 규칙 (위반 시 기각)
1. **초안 전용**: 기존 파일 수정 금지 — 산출물은 자기 창 폴더(`comp_R5/W{n}/`)에만. git 조작·`Codex/` 접근 금지.
2. 서지: `results/V1022_REFERENCE_LEDGER.md` V1 키 + **comp_R4 검증 후보 키**(`comp_R4/SI_CASES.md`·`comp_R4/upgraded/` 4본의 표에 있는 키만 — 전건 doi 실검증 완료 상태)만 \cite 가능. 기억 서지 절대 금지. **수치는 그 표들에 있는 원문 확인분만** — 그 외는 "확인 필요" 표기.
3. 기존 기호·라벨 재정의 금지(ch3v22_notation 계승 2단 규약). 신규 기호·라벨은 도입 절 명시(라벨 제안 = `eq:si-*`/`eq:blend-*`/`sec:si-*` 형).
4. Ch1/Ch2 결과식 인용 = xr live 참조(\S\ref/\eqref) — **라벨은 해당 소스에서 실확인한 것만**(추측 금지). 핵심 계승: `eq:sm-mc-balance`(전하 보존 반전)·`eq:logisticsolve`·`eq:dUhys`·`sec:sm-mc`.
5. 어조 = 기존 본문 동일(한국어 수식-구동 교과서체·`---` 강조·`$\cdot$` 나열·keybox/bgbox/verifybox/srcbox 관행·절 말미 `% 자산:` 앵커 신설[`[V22-R5-##]` 형]).
6. **조기 저장**: 절 하나 완성될 때마다 즉시 파일 저장. 표는 열 구조 고정(셀 내 개행·6열 혼용 금지 — R3 교훈).

## 과제 패키지 (전 절 저작 — PLAN_R5 §과제 패키지가 정본, 정독: `plans/PLAN_R5_ch3_authoring.md`)
산출 파일(자기 창 폴더에): `s31_map.tex`(생존 지도 본문화)·`s32_cases.tex`(Si/SiOₓ/Si–C 케이스별)·`s33_blend.tex`(공통-μ 대정준+GS-2 비가산 공백)·`s34_mech.tex`(Larché–Cahn 시도+GS-1)·`s35_code.tex`(R6 요구명세 예고)·`notation.tex`(기호표 확정안)·`DESIGN_NOTE.md`(설계 근거·공백 4분류 표·서지 채택 목록).

## 필수 정독 (저작 전)
- `plans/PLAN_R5_ch3_authoring.md`(과제·게이트·중단 경계 전문)
- `_sections/ch1_appD_si.tex`(현행 생존 지도 — §3.1 원천)·`_sections/ch3v22_sec00_intro.tex`·`ch3v22_notation.tex`
- `comp_R4/SI_CASES.md` + `comp_R4/upgraded/{SIOX_CASES,SIC_CASES,SI_ENTROPY_UP,BLEND_UP}.md`(문헌·수치 원천 — 이 표 밖 수치 금지)
- `Claude/plans/2026-07-17-v1022-master-plan.md` §7(R5 블렌드 이론 핵심·R6 코드 설계)
- `_sections/ch1_sec02b_part0.tex`의 sec:sm-mc 소절(대정준 반전 — §3.3 이 일반화할 원형)
- 흑연 케이스 표 관행: `_sections/ch1_sec10_sum.tex`의 tab:staging·`ch1_sec11_lcointro.tex`의 tab:lco-staging(tier 표기 양식)

## 물리 핵심(마스터 지정 — 전 창 공통 준수)
- §3.3 중심식: $\sum_{\mathrm{host}\in\{\mathrm{gr},\mathrm{Si}\}}\sum_j Q_j^{\mathrm{host}}\,\xi_{\eq,j}^{\mathrm{host}}(U_\mathrm{oc},T)=Q\,\bar x$ — eq:sm-mc-balance 의 클래스곱→host 곱 **한 줄 일반화**(요동 양성 유일근 논증 그대로 이월 — 재유도 말고 xr 인용). $f_\mathrm{Si}=Q_\mathrm{Si}/Q\in[0,0.3]$.
- **GS-2(신설 공백)**: 블렌드 실측(BLEND_UP 의 Ai2022·Chatzogiannakis2025)이 SoC 구간별 host 교대·비가산 거동을 보임 → 공통-μ 완전 동시반응은 **1차 근사** — 공백 4분류(물리 가정 충돌 계열)로 정직 명시. 구간별 전환 모델링은 범위 밖 선언.
- **GS-1**: Larché–Cahn(larchecahn1973) 응력-화학퍼텐셜 결합 유도는 닫히는 데까지만 — 1~2 스텝 내 안 닫히면 중단·공백 4분류 선언(유사 유도 날조 금지).
- Si 합금화는 삽입 아님 — 격자기체 ξ 의 재해석 한계(생존 지도 N4~N6 재해석 행)를 케이스 절이 존중.

## 창별 강조축 (전 절을 쓰되 강조가 다름 — 체리픽 다양성용)
- (기동 프롬프트에서 창별 지정: W1 이론 우선 / W2 실측·데이터 우선 / W3 교육·서사 우선)

## 완료 보고(마지막 텍스트)
절별 행수·신규 식/라벨 수·인용 키 목록(V1/후보 구분)·공백 4분류 표 요약·"확인 필요" 건수.
