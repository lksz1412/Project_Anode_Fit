# STEP_LOG P0 — 준비 phase 스텝 이력 (완료 즉시 기록)

## Step 1 — P0 세부 계획서 저장
- 대상: `plans/PLAN_P0_setup.md` 신규.
- 검증: 파일 존재. 다음: Step 2.

## Step 2 — v1.0.19→v1.0.20 복제 + 버전 태그
- 수행: 마스터 tex 2본(파일명 v1.0.20)·`_sections/` 41파일·`figs/` 5png·appendix 복제. 버전 문자열만 갱신(마스터 헤더 주석·\date 1.0.20·preamble pdftitle/lhead·appendix 승계 각주). 코드 참조 주석(Anode_Fit_v1.0.19.py)은 사실 기술이므로 유지(P8 에서 갱신).
- 검증: grep "1.0.19" 잔존 = 코드 참조·bib 내부검증 노트·역사 기술만. Step 5 스냅샷 diff 로 내용 무변경 교차 확인(labels/eq/asset/bib 4축 True).
- Read Coverage: (복제 작업 — 내용 정독은 담당 phase 소관.)

## Step 3 — TeX 환경 구축 + 기준선 빌드
- 수행: apt texlive-xetex/latex-recommended/latex-extra/pictures/lang-korean + fonts-unfonts-core/nanum/nanum-coding 설치. D2Coding 폰트: GitHub 릴리스는 프록시 차단(세션 범위 밖 저장소) → **npm registry `d2coding@1.3.2` tgz 로 확보**, full 계열 8종 설치(subset 제거).
- 기준선 빌드(xelatex 3-pass): **Ch1 62p·Ch2 25p·appendix 8p — v1.0.19 최종(R-P1 커밋 기준 62/25/8)과 일치. LaTeX Error 0·Undefined 0.** → 이 환경에서 빌드 게이트 유효(폴백 불요).
- 산출: `graphite_ica_ch1_v1.0.20.pdf`(807KB) 외 2본 + .log.

## Step 4 — pip + 회귀 기준선
- 수행: numpy 2.4.6·scipy 1.17.1·matplotlib 설치. `docs/v1.0.19/test_regression_v1019.py` 실행.
- 결과: 골든 대비 최대 편차 4.33e-15 (전 배열 1e-15 수준) = **플랫폼 부동소수 잡음**. bit-exact 판정은 원 캡처 머신 한정 → 이 환경의 코드 검증 기준 = 소스 diff(불변) + 수치 허용오차(≤1e-12). AREA/키 검사 정상.

## Step 5 — 구조 검증 스크립트 + 기준선 스냅샷
- 수행: `results/tools_check_structure.py`(check/snapshot/diff — 라벨 중복·미해소 ref/cite·환경 짝·수식블록 해시·자산 앵커; LastPage 화이트리스트). 기준선: v1.0.19 Ch1 = 라벨 219·refs 709·cite 50/bib 28 정합·환경짝 0·자산 336 유니크·수식블록 122(boxed 33) / Ch2 = 라벨 69·cite 32/bib 14 정합·자산 앵커 21태그·수식블록 32(boxed 10).
- 산출: `snapshot_v1019_baseline.json`·`snapshot_v1020_p0.json`. **복제 무결성: 두 스냅샷 labels/eqblocks/asset/bibitems 전부 동일(True×8).**

## Step 6 — rubric 원천 전문 정독
- Read Coverage: `_sections/ch1_sec02b_part0.tex` 1–329(전문) · `ch2_sec00_intro.tex` 1–68(전문) · `ch2_sec01_partition.tex` 1–144(전문) · `ch2_sec03_vibel.tex` 1–95(전문). (+기획 세션: ch1_sec02a 1–268·ch1_sec04 1–196·ch1_sec11 1–172 전문.)
- ★발견(P2 방향 확정): **Ch2 §2.1 은 이미 정통 유도 선행**(eq:Z1 = q(T) 없는 2-상태 → q(T)는 Part 0 참조로 흡수 언급). 교수 지적의 실체 = Ch1 Part 0 (sec02a eq:partfn)이 첫 유도부터 q(T) 포함형 → **Ch1 을 Ch2 와 같은 '정통 선행' 순서로 재배열하면 챕터 간 유도 순서도 정합**된다.
- 부수 발견: FD 동형 가드는 Ch1(sec02a verifybox)·Ch2(sec01 본문) 각각 존재. 페르미온/보손 배경은 양쪽 다 부재(ch2_sec01:36 "페르미온 전자가 아니라" 1회 언급뿐).

## Step 7 — STYLE_RUBRIC 작성
- 산출: `results/V1020_STYLE_RUBRIC.md` — A 어조 6항·B 수식 7항·C 용어 6항·D 박스 3항·E 인용 4항·F 편집통제 3항·G P6 후보 4항. bgbox 는 자족 블록 설계(사용자 D-2 유보 대응).

## Step 8 — CHANGE_LOG 초기화
- 산출: `results/V1020_CHANGE_LOG.md` — 보강/ERRATA 등재부(8컬럼) + ERRATA 요약(코드 영향 원장). 등재-후-편집 규칙 명문화.

## Step 9 — ledger 초기화 + RESULT_P0
- 산출: `results/V1020_EXECUTION_LEDGER.md`(P0 행 PASS) · `results/RESULT_P0_setup.md`.

## Step 10 — P0 커밋+푸시
- 커밋 대상: v1.0.20 골격(tex 복제+태그)·도구·rubric·CHANGE_LOG·ledger·STEP_LOG·RESULT·스냅샷 2본. PDF/log/aux 는 커밋 제외(빌드 산출물 — .gitignore 확인).
