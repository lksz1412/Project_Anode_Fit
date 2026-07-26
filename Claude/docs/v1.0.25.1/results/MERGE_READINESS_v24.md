# MERGE_READINESS — v1.0.24 (9항 게이트)

> 반영: @3 Si Frumkin·@5 stage-2L·LCO 전자항 토글·#7·#1. 판정 = 각 항 확인가능 증빙 첨부.

| # | 항목 | 판정 | 증빙 |
|---|---|---|---|
| 1 | **빌드 GREEN** (3장 컴파일) | **PASS** | xelatex 3-pass×2R: ch1 0-err **91p**·ch2 0-err **28p**·ch3 0-err **20p**. 'undefined' 로그 = 한글폰트 italic shape 경고뿐(benign). |
| 2 | **구조 검증** (labels·refs·cites·env) | **PASS** | `tools_check_structure.py check` 3장: dup **0**·unresolved **0**·cite-undef **0**·bib-uncited **0**·env-pairing **0**. |
| 3 | **코드 게이트** (회귀+신규) | **PASS** | G1 bit-exact max\|d\|=**0**·selfconsistent **5/5**·R6 블렌드 4종·반영게이트 **4/4**(@5 0.301mV/℃·토글 ON=OFF@298·regsol 단일봉·#1 값무변경). |
| 4 | **doc↔code 정합** | **PASS** | AUD-1(인라인) 4/4: 토글 기본 **False**(코드 L1052·시드/브리프 사양)·XRD 상수 ΔS+15/−14·regsol 분기 L588·func_L_q 주석만 L144. |
| 5 | **물리 유도 건전성** | **PASS** | AUD-2(손유도) 5/5: 판정자 4RT−2Ω·split Δ(ΔS)/F·Frumkin 연쇄·T_ref 동결 U불변 대수·#7 곡률. 코드상수 U(298) 자기정합. |
| 6 | **장간 정합** (모순 0) | **PASS** | AUD-3: gr_2L 이 §7 분류 **위임**(뒤집지 X)·§7 자체 "Ω 네전이>2RT·분류는 plateau" 논리와 정합·tab:staging 미편집·#7 guard 계승·gate-7 명칭대응. |
| 7 | **정직 한계 공개** (tier·warnbox) | **PASS** | 3 소절 전부 warnbox: stage-2L 다온도 미검증(tier B)·Ω_Si 범위시드·O3 전자항 미검증·ΔS 피팅대상. HANDOVER §5 집약. |
| 8 | **이름·구조 보존** (P5) | **PASS** | tab:staging·GRAPHITE_STAGING_LIT·기존 라벨/기호/식번호 **무변경**. 신규 = additive(신규 소절·별도 상수·별도 플래그). 역사적 stage 명칭 보존(gate-7). |
| 9 | **P3 7항 프로젝트 게이트** | **PASS** | V_n 구분 유지·전하보존 중심식 유지·순환의존 표기 계승·ref6,7 완료(bib)·Chapter1↔2~5 전달식 무충돌·ver.N/Chapter 혼동 가드 명시. |

| 10 | **공개 실측 피팅 + 전수 정합 감사** (R4 후 강화) | **PASS** | (a) SINTEF Zenodo 20086298 실측을 @3/@5 실경로로 피팅: 흑연 **0.9731**·Si **0.9944**·블렌드 **0.9848**(`FIT_CHECK_v1024.md`). (b) 6-에이전트 전수 doc↔code 감사: **곡선·피팅 BUG 0**, 잠재 코드버그 1(regsol 용량 +0.063%) 수정·주석/문서 다수 정정(`AUDIT_v1024_DOC_CODE.md`). 재검증 게이트 전건 GREEN. |

## 종합 판정
**MERGE-READY = YES (10/10 PASS).** (R4 마감 후 공개 실측 검증 + 전수 정합 감사로 강화, 최종 커밋 709d9e9.)

## 잔여(비-차단 · 회사 데이터/차기 위임)
- stage-2L 0.30 mV/℃·병합 10℃ 정량, Ω 점값, O3 전자항 온도의존 = **다온도 반쪽셀 데이터로 확정**(Task #38 미완, warnbox 명시분).
- Schmitt 2022 저자 전체·권쪽 = 사용 시 Crossref 최종 대조(제목·저널·연도·DOI 웹 확인 완료).
- 유한율속 dqdv() regsol 확장·AUD 별창 재검 = 차기 옵션.

## 부수
- `ch1_graphite_v1.0.24.tex` 마스터 손상(R0 구조검증 JSON 덮어씀) **복구 완료** — 재빌드로 89p PDF 재확인.

---

## Addendum — 1차 정독 피드백 리비전 (FB0~FB7, 2026-07-22)

> R4 마감 후 사용자 1차 정독 피드백(F-01~F-11)을 리비전. 본 addendum은 R4 본표를 **덮어쓰지 않고**(문건 보호 원칙) 변경분만 기록. 상세 = `Claude/results/V1024_FEEDBACK_EXECUTION_LEDGER.md` + `PHASE_FB0~FB7_RESULT.md`.

### 리비전 요약 (F-01~F-11 → FB0~FB6)
- **F-11**(FB1) 코드=부록: 본문 코드 함수명 → 부록 전용(본문 코드토큰 grep **0**). §3.5 코드절 부록 이전. → CLAUDE.md P3-8 게이트 명문화(FB7).
- **F-06**(FB2) 조판: 여백 22→25mm·줄간 1.12→1.16·문단 0.45→0.55em·microtype.
- **F-04·F-05·F-10**(FB3) register+제목+용어: 수필체·survival 술어·판번호·자기-diff·정직 형용사 평서화; 제목 N-태그 제거(~33); 요동/양성→영문(body **0**)·음함수/섭동/준위→국문+첫 병기·유일근→"유일한 근".
- **F-02·F-03·F-05**(FB4) 노테이션: 확률 P→소문자 p(압력 P 유지)·f_int 자리당 vs Helmholtz F 가드·잔여 제목 N-태그.
- **F-07·F-09**(FB5) overflow: E.3 서지 리스트 off-page(itemize 전환)·식2.39 재확인·**전역 픽셀-스캔 149쪽**으로 실 overflow 3건 추가 수정(Table11 `l l l l`→p{}·식2.18 주석·식2.36 multline).
- **F-01·F-08**(FB6) 내용: §1.1.4 배경 박스 압축(~50%↓·인용 보존)·LCO장 서두+제목 차이-선도 재균형(σ_d·order-disorder·전자항).

### 게이트 재확인 (FB7)
| 항목 | 판정 | 증빙 |
|---|---|---|
| 빌드 GREEN | **PASS** | ch1 0-err **97p**·ch2 0-err **30p**·ch3 0-err **21p**. (R4 91/28/20 → FB2 조판 후 98/30/21 → FB6 §1.1.4 압축 후 **97/30/21**.) undefined ref/cite **0**(한글 italic fallback만). |
| 코드 bit-exact | **PASS** | `Anode_Fit_v1.0.24.py` sha256 **f230f59b** 무변경(FB는 문건 한정). |
| 물리·식·label 불변 | **PASS** | full-diff invariant: equation env·`\label` 정의·식번호·`\eqref/\ref/\cite` 키·`%`주석 불변(P→p 개명·식2.36 multline은 식번호 보존). |
| 본문 코드토큰 | **PASS** | grep **0**(F-11 재발 게이트 = CLAUDE.md P3-8). |
| 용어 running-form | **PASS** | 요동/양성/유일근 body **0**·음함수 병기 앵커 4(문서별 1). |
| 적대 검수(N창) | **PASS(triage 완료)** | FB7 3창 병렬 — C 물리/label/빌드 **CLEAN**·A 피드백 10/11 해소(F-04 부록E 공백 발견)·B 용어 CLEAN+register 잔여. **FB3 스윕 누락분 triage 수정 16+건**(부록E 제목 참문제/안전증명서·keybox·구어 진짜×6·"원전 재확인 중"×4·process 라벨·서사/자기-diff) → 재빌드 GREEN·물리/label 불변. 상세 `PHASE_FB7_RESULT.md`. |

**판정**: FB 리비전은 표면/additive(register·용어·조판·overflow·배경압축)이며 **물리·코드·식번호 불변**. 적대검수 3창 + triage 완료 → **MERGE-READY 유지 = YES**.

### 추가 후보 (미집행 flag — 사용자 판단)
- Ch3 defined term "생존 지도"·"정직 공백 GS" 중립화(의도적 유지).
- LCO §2.1 도입 소절 제목 공유점 표현 추가 완화(내용 정합상 미개작).
- orphan `ch1_appD_si`(마스터 미입력)·레거시 preamble(`ch1/ch2_preamble`) 정리.
