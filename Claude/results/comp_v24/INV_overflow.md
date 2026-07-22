# INV — overflow(넘침) 전수 인벤토리 (F-06 조판·F-07·F-09)

> FB0 산출. 원천: 3챕터 fresh 빌드 로그 `Overfull \hbox` 파싱(파일 귀속) + 렌더 시각 확인(E.3·식2.39).
> **★게이트 맹점 확증**: 과거 gate = "overfull \hbox >10pt = 0". 그런데 **F-07(E.3 좌측 `\item` 라벨 흘러넘침)·F-09(식2.39 `cases` 내부 텍스트 우측)는 둘 다 Overfull 경고를 안 냄** — ch2_lco 로그 텍스트 overfull 0건인데 식2.39 는 23쪽서 잘림. → **렌더 시각 게이트 신설**이 근본 교정(FB5).
> ★주의: **FB2(여백 22→26mm·microtype) 후 전 넘침 재스캔 필수**(여백 변경 = 리플로우 → 이 목록 변동). FB5 는 FB2 뒤에 집행.

## Tier ① — 렌더-only 넘침 (경고 無, 사용자 직접 지적) — 최우선
| ID | 위치 | 컴파일 | 원인 | 처리(FB5) |
|---|---|---|---|---|
| **F-07** | `ch1_appE_selfconsistent.tex:111·113·117·120·124`(§E.3) | ch1 85쪽 | `\item[\textbf{긴 라벨}]` 5건 → 라벨폭 초과 → **좌측 페이지 밖 잘림**(②③④⑤ 원문자 절단) | 볼드 리드인 or `description` 행걸이 |
| **F-09** | `ch1_sec16b_lcoomega.tex:98–106`(`\begin{cases}`) | ch2_lco 23쪽 | `include_electronic_entropy` 토글식 cases 내 **긴 국문 설명 우측 넘침**("보존"·"= v1."·"round" 절단) | 설명을 수식 밖으로 / `p{}` 열 (FB1 코드플래그 제거와 합류) |

## Tier ② — 경고-flagged 텍스트 overfull (로그)
### ch1_graphite 문서 (흑연 본론 + Part T[ch2_sec*])
| pt | 위치 | 비고 |
|---:|---|---|
| 46.0 | `ch1_appE_selfconsistent.tex:202` | E.6 구현대응지도 |
| 30.2 | `ch2_sec07_revheat.tex:75–81` | Part T 가역열 |
| 24.2 | `ch2_appA_traps.tex:63` | 부록(함정표) |
| 10.8 | `ch1_appE_selfconsistent.tex:204` | E.6 |
| 7.7×3 | `ch1_appE_selfconsistent.tex:196–206` | E.6 코드지도 |
| 6.6 | `ch1_sec01_n0n1.tex:59` | §1.1 |
| 6.2 | `ch2_sec00_intro.tex:6–15` | Part T 서 |
| 2.5 | `ch2_sec02_config.tex:156–166` | Part T config |
| **568×3** | `ch1_appB_codemap.tex:62–102` | **코드맵 longtable 내부**(넓은 `\code{}` 행) — 표 구조 처리 별도(FB1 코드정리 + 열폭 조정) |

### ch3_si 문서
| pt | 위치 | 비고 |
|---:|---|---|
| 17.0 | `ch3v22_sec02_cases.tex:34–35` | §3.2 |
| 12.5 | `ch3v22_sec02_cases.tex:32–33` | §3.2 |
| 5.6 | `ch3v22_sec02_cases.tex:33–34` | §3.2 |

### ch2_lco 문서
- 텍스트 overfull **0건**(단, F-09 식2.39 는 렌더-only라 여기 안 잡힘 → Tier①).

## F-06 조판 레버 (현행 → 목표, "약간씩")
| 항목 | 현행(`common_preamble_v1024.tex`) | 목표(기본값) |
|---|---|---|
| 여백 | `margin=22mm`(텍스트폭 166mm) | ~26mm |
| 줄간격 | `\setstretch{1.12}` | ~1.18 |
| 문단간격 | `\parskip 0.45em` | ~0.6em |
| microtype | 미로드 | 도입(protrusion) |
| 인라인→디스플레이 | — | 복잡도 기준 per-instance(분수중첩·합/적분·조건부 승격) |
- ★현행 조판값은 **v1.0.18.2 이래 동결 계승**(preamble 주석 "렌더 목표 v1.0.18.2") — F-06 이 처음 튜닝. 그림 규약(외부이미지 금지·TikZ 실계산)은 불변.

## 처리 순서(계획 정합)
FB2(preamble 전역 조판·리플로우) → **재빌드·재스캔** → FB5(F-07·F-09 렌더-only + Tier② 잔여 + 568pt 표). 각 수정 후 **렌더 crop 전/후 대조**.

## Read Coverage
3챕터 fresh 빌드 로그 overfull 파싱(파일 귀속 파서) + E.3(85쪽)·식2.39(23쪽) 렌더 확인(F-07/F-09 시). preamble 조판값 원문 확인. 표/tikz 내부(>200pt)는 별도 표시.
