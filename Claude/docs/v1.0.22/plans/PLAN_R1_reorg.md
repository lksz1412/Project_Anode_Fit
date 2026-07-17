# PLAN R0/R1 — v1.0.22 구조 재편 설계서 + 집행 계획 (Steps 1–14)

## Summary
v1.0.21(원천)을 활물질별 3챕터로 재편한다: Ch1 흑연+열특성 / Ch2 LCO+열특성(추가 텀 방식) / Ch3 Si·혼합음극. 원칙 = **이동이지 재작성 아님**(자산 무유실), 장별 기호표(계승 2단)·장별 참고문헌, 항법판 제거, 병합 대비(라벨 전역 유일·번호 장 prefix — 병합 빌드는 사용자 별도 세션).

## Current Ground Truth
v1.0.21 Q0~Q8 완료(76/26p err0·서지 54종·코드 matched)·HANDOVER_v1.0.21 마감. D22 전건 확정(마스터플랜 v2). 섹션 파일 39본(_sections/)·마스터 2본+항법 2본·부록 1본·코드 2본.

## 설계 1 — 파일 전략
- **섹션 파일 이름 불변**(ch1_sec*·ch2_sec* 그대로) — git 이력·자산 주석·diff 추적 보존. 재편은 **마스터의 \input 재조립**로 구현.
- 신규 마스터 3본: `ch1_graphite_v1.0.22.tex` / `ch2_lco_v1.0.22.tex` / `ch3_si_v1.0.22.tex`. (구 명명 graphite_ica_* 는 v1.0.21 까지의 역사 명칭 — P3-⑦ 명칭 대응표를 §설계 7 에 둔다.)
- 항법 제거: `ch1_appC_navaid.tex`·`*_nav.tex` 드라이버·nav PDF 는 v1.0.22 로 **복사하지 않음**(v1.0.21 에 이력 보존). `\ifnavaid` 인프라는 preamble 에서 제거.
- `appendix_phase_separation.tex` = 공통 독립 부록 유지(4번째 산출물).

## 설계 2 — 절 이동 매핑표 (원천 → 신 구조)
| 신 위치 | 원천 파일 | 처리 |
|---|---|---|
| **Ch1** §1.0 서론 | ch1_sec00_intro | 이동 + 서론 개정(3챕터 구조 안내 1문단 — R2) |
| Ch1 §1.1 규약·측정 원리 | ch1_sec01_n0n1 | 그대로 |
| Ch1 §1.2 Part 0 통계역학 기초 | ch1_sec02a·02b | 그대로(전 장 공통 뿌리 — sec:sm-mc 포함) |
| Ch1 §1.3~1.10 흑연 결과 사슬 | ch1_sec03~sec10 | 그대로(fig:UjT·hysgap·sumcurve·sec:sum-worked 포함) |
| Ch1 **Part T 흑연 열특성** | ch2_sec00~sec10 (구 Ch2 전량) | 이동. sec00(서론)·sec10(closing)은 "장→파트" 격 개작(R2 이음매), sec01~09 본문 그대로 |
| Ch1 부록 | ch1_appA(부호)·ch1_appB(코드맵)·ch2_appA(함정표)·ch2_appB(코드 요구명세) | 이동(부록 4본 병렬 — appB 2본은 "곡선/열특성 코드맵"으로 제목 구분) |
| **Ch2** §2.0 서론 | 신규 소절(짧게 — "Ch1 식 기반, 추가 텀만" 선언) + ch1_sec11_lcointro | sec11 이 사실상 서론 — 앞에 방식 선언 문단만 추가 |
| Ch2 §2.1~2.7 LCO 본체 | ch1_sec12~sec17 | 그대로(sec:lco-worked = §15 내 유지) |
| Ch2 기호표·bib | 신규(계승 2단)·ch1_bib 에서 LCO 그룹 분리+공통 재수록 | 신규 파일 ch2v22_notation.tex·ch2v22_bib.tex |
| **Ch3** §3.0 개관·케이스 | ch1_appD_si 승격(본문화) + 신규(R5) | appD → ch3 본문 골격으로 이동 |
| Ch3 §3.x 블렌드 | 신규(R5 — 공통-μ 대정준·f_Si 합성) | R5 저작 |
| Ch3 기호표·bib | 신규(계승 2단)·Si 14종+공통 재수록 | 신규 파일 |
| 코드 | Anode_Fit_v1.0.22.py(복사)·test_gates_v1022.py | R6 에서 블렌드 확장 |

## 설계 3 — preamble 통합
- `common_preamble_v1022.tex` 신설 = 현 ch1_preamble ∪ ch2_preamble 매크로 합집합(\oc·\rev·\vib·\avg·\code 등 ch2 전용을 공통 승격 — 충돌 사전 검사: 동명 매크로 정의 diff 0 확인 후 병합). box 환경(keybox·bgbox·verifybox·signbox·srcbox) 통합.
- 장별 얇은 드라이버 preamble: 장 번호(\thesection=N.x·\theequation=N.x — Ch1=1.x·Ch2=2.x·Ch3=3.x)·pdftitle·헤더만. **구 Ch2 의 \theequation=2.x 재정의는 신 Ch1 열특성 파트에서 제거**(신 Ch1 은 1.x 연속 — 병합 시에도 유일).

## 설계 4 — 장 간 교차 참조 (별도 컴파일 유지)
- **xr-hyper**: Ch2/Ch3 preamble 에 `\externaldocument{ch1_graphite_v1.0.22}` — 구 Part II 가 쓰던 Ch1 라벨(\eqref{eq:Uj}·\S\ref{sec:center} 등 다수)이 **별도 컴파일에서도 live 번호로 해소**. 이것이 재편의 최대 기술 리스크 해소책(라벨 깨짐 방지) — R1 step 5 에서 시험 필수(실패 시 폴백 = 서술형 참조 일괄 전환, 분량 큼).
- 병합 세션 주의(MERGE_READINESS 에 기록): 병합 빌드에서는 externaldocument 줄 제거(라벨이 내부화).
- Ch1→Ch2/Ch3 방향 참조는 서술형 유지(앞 장은 뒷 장에 의존하지 않음 — 교과서 순서 원칙).

## 설계 5 — 장별 기호표(계승 2단)·장별 bib
- 각 장 §N.0 직후 기호표: [**계승** — 기호·뜻·정의 장·"재정의 없음" | **신규** — 이 장 도입]. Ch1 기호표 = 현 tab:notation 승계+열특성 기호(구 ch2 도입분) 통합.
- 장별 bib: Ch1 = 흑연·통계역학·TST·측정·열특성(구 ch2_bib 16종 흡수) / Ch2 = LCO 그룹+공통 재수록 / Ch3 = Si 14종+공통 재수록. 같은 키가 여러 장에 실리는 것은 의도(리뷰 모음형·장 자기완결). 원장은 공통 1본(`results/V1022_REFERENCE_LEDGER.md` 승계 개설).

## 설계 6 — 검증·자산
- 자산: 파일 불이동이므로 자산 주석 자동 보존 — 게이트 = 장별 스캔 합계가 원천 합계(336+21+V21 신규 주석)와 일치.
- tools_check_structure: 마스터 3본 대상으로 재기준 스냅샷(r1). cite/bib 정합은 장별.
- 빌드: 3장+부록 = 4본 3-pass err0/undef0.

## 설계 7 — 명칭 대응표 (P3-⑦ 혼동 가드)
| 역사 명칭 | v1.0.22 신 명칭 |
|---|---|
| 구 Ch1(graphite_ica_ch1, 흑연+LCO) | 신 Ch1(흑연+열특성) + 신 Ch2(LCO) 로 분할 |
| 구 Ch1 Part 0 | 신 Ch1 §1.2(위치 불변) |
| 구 Ch1 Part II(§11~17) | 신 Ch2 본체 |
| 구 Ch2(가역 발열) | 신 Ch1 Part T(열특성 파트) |
| 구 부록 D(Si 예비 지도) | 신 Ch3 골격 |
| ver.1~5·Chapter 1~5(v1.0.19 이전 역사 구조) | 본 재편과 무관(문서 자립 원칙 — 본문 언급 없음 유지) |

## R1 Steps (1–14)
| Step | 작업 | Gate |
|---|---|---|
| 1 | 본 설계서 저장·v22 ledger/CHANGE_LOG/원장 개설 | 파일 |
| 2 | v1.0.22 골격 복사(섹션·부록·코드 — 항법 3파일 제외)·매크로 충돌 검사 | 충돌 0 |
| 3 | common_preamble 통합 + 장별 드라이버 preamble 3본 | 파일 |
| 4 | 마스터 3본 조립(설계 2 매핑 그대로)·구 마스터 미복사 | 파일 |
| 5 | **xr-hyper 시험**(Ch2 가 Ch1 라벨 해소) — 실패 시 폴백 결정 보고 | 시험 |
| 6 | Ch1 빌드 GREEN(흑연+열특성 — 이음매 개작 전이라 sec00/10 은 임시 헤더 처리) | err0 |
| 7 | Ch2 빌드 GREEN | err0·xr 해소 |
| 8 | Ch3 빌드 GREEN(appD 승격 골격) | err0 |
| 9 | 장별 기호표 2단 초판·장별 bib 분리 | cite-undef 0 |
| 10 | 구조 검증·자산 합계 게이트·스냅샷 r1 | PASS·자산 전수 |
| 11 | 코드 복사·게이트 이월 실행 | exit 0 |
| 12 | INDEX 갱신·ledger R1 행 | 갱신 |
| 13 | 커밋·푸시 | 해시 |
| 14 | (R2 준비) 이음매 개작 대상 목록 확정(sec00·sec10·서술형↔live 참조 전환 후보) | 목록 |

## Non-goals(R1)
본문 산문 개작 X(R2 소관 — R1 은 조립·빌드만). 병합 빌드 X(금지 — D22-8). B급 그림 X(취소).

## 중단 조건
xr 시험 실패 + 서술형 폴백 분량이 과대(>100곳)로 판정되면 중단·사용자 보고(라벨 재설계 결정 필요).

## Correction History
(초판 — R0 산출)

## Step 14 — R2 이음매 개작 대상 목록 (R1 마감 시 확정)
1. ch2_sec00_intro(구 Ch2 서론) — "본 장/chapter" 자기 지칭을 "본 파트"로, 문서 범위 서술을 Ch1 통합 문맥으로(분량 ~6문장).
2. ch2_sec10_closing — 장 마감 어조를 파트 마감으로.
3. ch1v22_partT_divider 다리 문단 확정(현 초판).
4. 서술형↔live 참조 전환 스윕: 구 "Chapter 2 의 식 (eq:...)" 식 서술형(같은 문서가 된 열특성 방향, ~15곳)과 구 "Chapter 1 의 ..." (Ch2 LCO 문건 내, xr live 전환 후보 ~20곳) — 전수 목록은 grep "그 문건\|Chapter [12] 의" 로 산출.
5. ch1_sec18_inputs — LCO 행 분리 검토(입력 사양의 장 귀속).
6. ch1_appB·ch2_appB 코드맵 2본 — 제목·서두에 "곡선/열특성" 분업 명시.
7. ch1_sec00_intro 서론 — 3챕터 체제 안내 1문단 + 구 "본 문서 = 흑연+LCO" 서술 갱신.
8. 인용 다리 12곳(D22-5)은 R2(흑연분)/R3(LCO분) 본안.

## Correction History
- (R1 마감) Step 6 누락 발견 1건: ch1_sec18_inputs 조립 누락(tab:nodemap 미해소로 검출) → 편입. 자산 27 앵커(구 bib 주석) 복원. xr 양방향 채택(설계 4 개정 — 전방 참조 22곳 산문 무손상 우선).
