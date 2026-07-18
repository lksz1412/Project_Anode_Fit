# MERGE_READINESS — v1.0.23 병합 준비 상태 (P5 마감 — 마스터 확정)

## 0. 요약 (한 눈)

- **정체성**: v1.0.23 = v1.0.22(완결·검증종료) + **사용자 JCP147 Fredholm-2종 ratio 방법의 정직 접목**. 신규 = 부록 E "자기일관 해법"(수학) + 코드 ratio/transfer 옵션(적용, 기본 off).
- **빌드**: 3장 분리 빌드 **err0·undef0** — ch1 **87p**(83+부록 E 4p)·ch2 25p·ch3 17p. 병합 빌드 금지(D22-8) 유지.
- **게이트**: 기존 `test_gates_v1023.py` **G1 bit-exact(max|d|=0.0)**·G2·G3·n(T)·R6 exit0. 신 `test_gates_v1023_selfconsistent.py` **G-E1~E5 5/5 PASS**.
- **검수**: 코드↔문건 정합 적대적 5창 — **치명 0**. 중대 2건(부록 E 수치 증거 과장)=정정 완료. 상세 = `comp_v23/AUD_REPORT_v23.md`.
- **parity**: v1.0.22 대비 **순수 additive**(공유 함수·47섹션 byte/sha256 동일). 병합 시 v1.0.22 물리·수치 무섭동.

## 1. 신규 자산 (v1.0.22 → v1.0.23 델타)

| 자산 | 파일 | 성격 |
|---|---|---|
| 부록 E "자기일관 해법" | `_sections/ch1_appE_selfconsistent.tex` | 신규 부록(letter E). ratio 닫힘·전달함수·P3-5 5항·타당성 부등식·warnbox·코드지도 |
| 부록 배선 | `ch1_graphite_v1.0.23.tex`(\input 1줄) | 부록군 말미(A·B·C·D·E 순) |
| 본문 포인터 | `ch1_sec08_lag.tex`(말미 1문장) | 부록 E 지시(코드 언급 0) |
| bib 3종 | `ch1v22_bib.tex` | lee2017jcp(사용자 JCP147)·lee2011jcp(Ref.6)·son2013jcp(Ref.7) |
| 코드 옵션 | `Anode_Fit_v1.0.23.py` | `_causal_memory_ratio`·`transfer_apparent_from_equilibrium`·`_lag_ratio_geff`·플래그 `lag_ratio_correction`(기본 False)·dqdv elif |
| 신 게이트 | `test_gates_v1023_selfconsistent.py` | G-E1~E5 |

## 2. 라벨 유일성 (병합 충돌)

- 신규 라벨(부록 E): `sec:appendix-selfconsistent`·`sec:sc-{volterra,ratio,p35,valid-sub,transfer,codemap}`·`eq:sc-{frozen,ref,true,volterra-eq,split,ratio,ratio-local,valid,transfer}`·`tab:sc-codemap` — 구조검사 **dup 0**. 부록 letter = **E**(`\setcounter{section}{4}` 로 수동 \section*(부록 C·D) 충돌 회피).
- 신규 bibkey 3종 cite-undef 0·bib-uncited 0.
- xr 미해소 19건 = ch2(lco) 외부참조(externaldocument) — **v1.0.22와 동일 baseline**(실빌드 undef0).

## 3. 서지

- 3종 추가, 장말 bib(ch1v22_bib) 편입. lee2017jcp = DOI 확정. Ref.6·7 = 원문 참고목록 서지 + 제목·DOI "원문 대조로 확정" 정직 유보(날조 0·AUD-4·5 웹 대조).

## 4. 병합 절차

1. v1.0.23 = v1.0.22 상위집합이므로, v1.0.22 병합 절차(MERGE_READINESS.md §4) 그대로 + 부록 E 파일·배선·bib 3종·코드 옵션 추가만.
2. 코드: `lag_ratio_correction` 기본 False → 기존 산출 bit-exact. ratio/transfer 는 선택 경로.
3. 재빌드 3장 분리·게이트 2본(기존+신) exit0 확인.

## 5. 알려진 주의점

- **(a) ratio 옵션 실이득창**: `0.1≲L_V/w≲0.6`(중간 전류). 기본 흑연(c_rate~1)은 L_V~1e-7 미해상 → 휴면(부록 E.4 warnbox·G-E5 정직 표기). ratio 는 결함 아닌 조건부 고정밀 경로.
- **(b) 부록 E 수치 증거**: 커밋 스크립트(`comp_v23/p1_ratio_check.py`·G-E4)의 재현값만 인용(P5 정정). scratchpad 스크립트(cond_audit_verify.py) 수치는 본문 미인용.
- **(c) AUD-2 F-1(config 상한 0.21)**: 결함 아님(원출처 정합·스팬 의존 hedge). 무수정.
- **(d) swiderska2019 multiply-defined**: v1.0.22 기지 의도적 중복(장말 bib 리뷰모음형)·빌드 경고 무해.
- **(e) 버전 라벨**: 코드 헤더·appB 코드파일명 v1.0.23 정정(P0 클론 누락분). 물리 lineage(1.0.21 확정본 승계) 주석 보존.

## 6. 검수 이력 포인터

- P1 조건검수: `PHASE_P1_RESULT.md`·`comp_v23/COND_AUDIT.md`·`comp_v23/p1_ratio_check.py`
- P2 부록 저작: `PHASE_P2_RESULT.md`
- P3 코드: `PHASE_P3_RESULT.md`
- P5 적대검수: `PHASE_P5_RESULT.md`·`comp_v23/AUD_REPORT_v23.md`
- 서베이: `comp_v23/SURV_SYNTHESIS.md`
