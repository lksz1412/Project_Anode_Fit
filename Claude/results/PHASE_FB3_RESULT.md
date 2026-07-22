# Phase FB3 — F-04 register + F-05 제목 + F-10 용어 전역 스윕 Result

## Summary
문서 전역 register(F-04 교과서 어투·수필/역사서 문체 제거)·제목 N-태그(F-05)·전문용어(F-10) 리비전. 4 서브 병렬(G1 흑연 본문·G2 LCO·G3 Part T 통계역학·G4 Ch3 Si+부록) + **master 통합·용어 running-form 전역 통일**. 물리·식·`\label`·코드 불변, 어투·용어 표기만. **핵심 결정: 사용자 직접 지목 일본식 calque(요동·양성)는 완전 영문화(병기 없음)·표준 학술어(음함수·섭동·준위)는 한글 유지+첫 병기 — G1/G4가 독립적으로 남긴 `음함수→implicit function` 영문 running 분기를 국문으로 통일.**

## Step Range
cumulative **FB step 15–24**. (Step15 제목 스윕·G2·G3 선행 커밋 → G1·G4·master 통합이 본 결과로 마감.)

## Inputs
- **지배 게이트 정독**: `CLOSING_v1.0.15.md`(헌법3종+D1-6)·`V1020_STYLE_RUBRIC.md`(A~G)·`V1013_TERMS_POLICY.md`(27+18)·`V1014_TONE_AUDIT.md`·`INV_register_titles_prose.md`·`TERM_DECISION_TABLE.md`.
- **편집 대상**: `_sections/` 25 tex(ch1 본문 sec00-10·LCO sec11-17·Part T ch2_sec00-10·Ch3 ch3v22_*·부록 ch1_appB/D/E·ch2_appA/B). 각 서브 head→tail 전문 정독 후 targeted edit.

## Files Created
- 없음(결정 기록 `TERM_DECISION_TABLE.md`는 FB0 생성분 갱신).

## Files Updated (그룹)
- **제목(Step15, 선행)**: ch1_sec00-16b·ch2_sec00/02/09·ch3v22_sec01_map/sec03·ch1_appD ~31개(N0-N9' 태그 제거·수필형→명사구·물음형 6개 명사화).
- **G2 LCO**: ch1_sec15_lcoelec·ch1_sec16b_lcoomega(수사문답 정리·판번호 제거).
- **G3 Part T**: ch2_sec00-08(못박다→규정/명시·TOC `\addcontentsline` 정합).
- **G1 흑연 본문**: ch1_sec00-08(survival 술어→남는다/유지·요동→fluctuation·양성→positivity).
- **G4 Ch3 Si+부록**: ch3v22_sec00-05·notation·ch1_appB/D/E·ch2_appA/B(survival 은유·못박다·갈아끼우다·손잡이·정직 형용사→평서·요동/양성/유일근 영문화·suite 코드식별자 유지).
- **master 통합(용어 running-form 통일)**:
  - **음함수 국문 복원**(표준 수학어): ch1_sec02b(4)·ch1_appB·ch1_appD·ch2_appA·ch2_appB(4)·ch3v22_sec03_blend `implicit function`→`음함수`(running). 첫 병기 앵커 4개 유지(sec02b:286·sec15:365·sec05:13·map:97 = 문서별 1회 `음함수(implicit function)`).
  - **요동 완전 영문화**(사용자 지목 calque·병기까지 제거): ch1_sec02a(소절명+running)·ch2_sec05·ch2_sec07·ch3v22_notation `요동`→`fluctuation`.
  - **정직한 한계→적용 한계**(D2 방어어투·G4 Ch3 선례 전역화): ch1_sec05b·ch1_sec16b(2)·ch2_sec08·ch2_sec09(정직하게→명시적으로).
  - **sec04_mech warnbox self-diff 평서화**(D1): "본 절이 예비 지도에서 나아간 지점···한 단계 좁혔다"→결과 직진술(식·GS-1·이연 사유 보존).
  - ch1_appD:77 `유도 미착수`→`유도 범위 밖`(D1 공정어).
- **결정 기록**: `comp_v24/TERM_DECISION_TABLE.md` B절 6개어 "사용자 결정" 열 집행 확정 기입.

## Read Coverage
- **전문 정독**: 지배 게이트 6종 + 편집 대상 25 tex(각 서브 head→tail).
- **grep 전수 검증**: `implicit function`/`음함수`·`요동`·`양성`·`유일근`·`정직`·survival 술어·판번호·process label 전 파일.
- **미열람(범위 밖)**: 컴파일 제외 orphan 3개(ch1_appD_si·ch1_preamble·ch2_preamble)의 빌드 반영(파일 자체는 편집/정독함) · Codex 산출물(P2 경계).

## Execution Evidence
```
빌드(3챕터, FB3 통합 후): ch1 0-err/98p · ch2 0-err/30p · ch3 0-err/21p
undefined: 전부 "Font shape ... undefined"(한글-italic fallback) — undefined ref/cite = 0
용어 running-form 전수(body):
  implicit function = 4(문서별 첫 병기 앵커만) · 음함수 running = 국문 통일
  요동 = 0(body) / 3(주석 forbidden-zone) · 양성 = 0(body) / 2(주석) · 유일근 = 0(body)
  정직 = '정직 공백'(GS 정의어) 8곳만 잔존 · 정직한/정직하게/정직 한계 = 0
물리 불변(full diff): equation env 증감 0 · \label 키 변경 0 · % 주석 변경 0 · \eqref/\ref/\cite 키 변경 0
TOC: \section*↔\addcontentsline 5쌍 검사 — 실질 불일치 0(appA/B의 $\cdot$↔· 2건은 동일 렌더·FB3 미변경)
```

## Validation (P3 프로젝트 7항 게이트별)
1. **V_n 표기 일관** — N/A(본 phase 전위 기호 미접촉; FB4 F-02/F-03 소관).
2. **전하 보존식=중심식 유지** — PASS(음함수 국문 복원이 `전하 보존 음함수` 중심식 지위 강화; 식 불변).
3. **순환 의존 표시** — N/A(dependency graph 미접촉).
4. **순환 4분류** — 유지(`정의상 implicit formulation` P3 카테고리명 불변 — 음함수 국문화와 분리 보존).
5. **ref.6,7 방법론 4항** — N/A(본 phase 서지 방법론 미접촉).
6. **Ch1 기준식↔Ch2-5 전달식 충돌** — PASS(식·label 불변, 전달 정합 유지).
7. **ver.N↔Chapter N 혼동** — PASS(파일명 역사적 구조 확인: ch1_graphite=Ch1[Part0+흑연+Part T]·ch2_lco=Ch2[LCO]·ch3_si=Ch3[Si]; 보고에 매핑 명시).

### 추가 게이트
- **빌드 GREEN** — PASS(3챕터 0-err·undefined ref/cite 0·페이지 98/30/21 baseline 동일).
- **물리·식·label 불변** — PASS(full-diff invariant 4종 empty).
- **용어 정책 정합** — PASS(요동/양성 영문·음함수/섭동/준위 국문+병기·유일근 풀어쓰기 grep 확인).
- **register 전역** — PASS(survival 술어·판번호·process label·정직 형용사·self-diff warnbox 제거 grep 확인).

## Gate
**PASS_FB3_REGISTER_TERM** (빌드 GREEN + 물리 불변 4종 + 용어 running-form 전역 통일 grep 확인 + register offender 소거 확인).

## Confirmed Non-Changes
- 코드 `.py` 무변경(sha256 f230f59b). 식·`\label`·식번호·`\eqref/\ref/\cite` 키·`%` 주석(자산 앵커) 불변.
- 유지 확정 defined term: **정직 공백(GS-1/GS-2)**·**생존 지도**(Ch3 골격 판정 구조어) — 의도적 보존(아래 추가 후보 참조).

## 추가 후보 (실제 미수정 — 사용자 결정 대기, P5)
1. **`생존 지도`/`생존 판정`(Ch3, ~13곳)** — survival 은유이나 골격 노드 판정 구조를 정하는 defined term. 술어형 survival은 전량 평서화했으나 명사 구조어는 보존. 중립화 원하면 `노드 이행 지도`/`골격 대응 지도` 등 후보(라벨 키 `sec:si-map`·`ssec:si-verdicts`는 이미 중립 — 표시어만 교체).
2. **`정직 공백 GS-1/GS-2`(Ch3, 8곳)** — 형식 개념명(정직하게 선언한 미유도 공백). `정직한 한계`(형용사·자기과시)는 평서화했으나 GS 정의어는 보존. 중립화 원하면 `미결 공백 GS-1`/`선언 공백` 등 후보(제목·라벨 연동 대규모 rename).
3. **orphan `ch1_appD_si`(Si 노드 판정 부록)** — 어느 마스터에도 `\input` 안 됨(컴파일 제외). register/용어 편집은 반영돼 있으나 미출간. Ch3에 포함 여부는 구조 결정(FB3 범위 밖).
4. **레거시 preamble `ch1_preamble`·`ch2_preamble`(v1.0.21 잔재)** — 마스터 미입력·미컴파일. 삭제 여부 사용자 판단(원본 불가침 하 미접촉).
5. **`swiderska2019`(3챕터)·`verbrugge2017`(ch3) `Label multiply defined`** — 서지 중복(FB3 이전부터 존재). F-07(E.3 서지) FB5에서 함께 점검.
