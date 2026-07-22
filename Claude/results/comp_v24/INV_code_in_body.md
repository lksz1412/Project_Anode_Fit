# INV — 본문(비부록) 코드 언급 전수 인벤토리 (F-11)

> FB0 산출. 규칙 근거: 헌법①(교과서 register)·rubric **A5**("코드 함수명 본문 노출 0 — 부록 B 전용")·`V1014_CODE_MENTION_AUDIT`(1차 집행 83행). F-11 = 2차 재발.
> 스캔: `_sections/*.tex` 에서 렌더 코드토큰(`\code`/`\texttt`/클래스·함수·플래그·상수·`.py`) grep, **부록 6파일 제외**(허용 구역), **`%` 주석·`\code` 매크로 정의 제외**. 결과 = **본문 17행 + 구조적 §3.5 전체(D5)**.
> 허용 구역(부록): `ch1_appA_signcheck`·`ch1_appB_codemap`·`ch1_appD_si`·`ch1_appE_selfconsistent`·`ch2_appA_traps`·`ch2_appB_codemap`.
> 처리 원칙: **삭제→물리 언어 치환**(코드명 불필요) 또는 **부록 코드맵(appB `tab:nodecode`)로 이전**. 캡션·제목·표는 코드명 0.

## Tier ① — 사용자 직접 지적: Ch3 Fig 2 캡션 (명백 위반)
| file:line | 현재 문구(발췌) | 코드 토큰 | 처리 |
|---|---|---|---|
| `ch3v22_sec03_blend.tex:204` | `\texttt{BlendedAnodeDQDV.from_wt}$(m_Si, \texttt{si_case='elemental'})$ 의 실계산이다` | 클래스·메서드·인자 | 캡션에서 제거 → "평형 dQ/dV 가족($f_\mathrm{Si}$ wt% 스윕, elemental Si-host)"(물리만) |
| `ch3v22_sec03_blend.tex:217` | `그 Si host 몫만 떼어(코드 \texttt{host_contributions}) 확대` | 메서드 | "(코드 …)" 삭제 → "Si-host 기여만 분리" |
| `ch3v22_sec03_blend.tex:220` | `\texttt{elemental} 케이스는 SiO_x 절대전위 …` | 케이스명 | `\texttt{elemental}`→"원소 Si(elemental) 케이스" 물리어 |

## Tier ② — 본문 산문 코드명 (v1.0.24 신규 절 집중)
| file:line | 현재 문구(발췌) | 코드 토큰 | 처리 |
|---|---|---|---|
| `ch1_sec05b_gr2L.tex:128` | `(\code{GRAPHITE_STAGING_XRD_v1024}, §ref 4-전이 기준과 병존)` | 상수 | 상수명 삭제 → "5-feature staging 시드(§7 4-전이 기준과 병존)"; 코드 대응은 부록 |
| `ch1_sec05b_gr2L.tex:135` | `…(코드 \code{GRAPHITE_STAGING_LIT}, 무변경)이고` | 상수 | "(문헌 4-전이 기준선, 무변경)" |
| `ch1_sec05b_gr2L.tex:136·143·148·188` | `\code{GRAPHITE_STAGING_*}` 재등장 | 상수 | 동일 — 물리어("4-전이 기준선"/"5-feature 시드"), 코드명 부록 |
| `ch1_sec16b_lcoomega.tex:97` | `\textbf{(d) 박스 --- \code{include_electronic_entropy} 토글(기본 False).} 이를 코드 플래그 한 개로 고정한다` | 플래그·"코드 플래그" | "전자항 on/off 옵션(기본 off)" 물리어, "코드 플래그" 삭제 |
| `ch1_sec16b_lcoomega.tex:100·154` | `\code{include_electronic_entropy} 는 기본 False…` | 플래그 | "전자항 옵션은 기본 off(…)·on 옵션(…)" |
| `ch3v22_notation.tex:32` | `\code{si_case} & … & 케이스 선택자 \code{'elemental'/'siox'/'sic'}` | 표기표 코드 열 | 물리 케이스 3종(원소 Si·SiO_x·SiC) 서술로; 코드 선택자명은 부록 |
| `ch3v22_sec02_cases.tex:139` | `\texttt{BlendedAnodeDQDV.host_contributions} 의 Si-host 기여` | 클래스·메서드 | "블렌드 모델의 Si-host 기여(식 eq:blend-dqdv)" |
| `ch3v22_sec02b_sifr.tex:147` | `이 커널의 구현(\code{_regsol_dqdv})은 …` | 함수 | "(구현: Maxwell 공존 구성)" 코드명 삭제 |

## Tier ③ — 구조적 (D5 사용자 결정)
| 대상 | 현황 | 처리(D5 기본값) |
|---|---|---|
| `ch3v22_sec05_code.tex` §3.5 전체 | **본문 절 전체가 코드 확장 요구명세** — 절 제목에 `\code{BlendedAnodeDQDV(f_Si, si_case)}` | **부록으로 이전**(본문서 코드 명세 절 제거, 요구명세는 부록/`docs/`로) |
| `ch1v22_bib.tex:44` | `\bibitem{numverif2026} … \code{Anode_Fit_v1.0.19} 4-전이 흑연 staging …` | **`\code` 제거 평문화**(내부 데이터 출처로 서지 유지, 코드 서식만 제거) |

## 카운트
- 본문 산문/캡션 코드 언급: **17행**(gr2L 6·lcoomega 3·blend 3·notation 1·cases 1·sifr 2·bib 1).
- 구조적: §3.5 절 1(전체).
- **재발 게이트(FB1 신설)**: 부록 6파일 제외 grep 에서 위 토큰 = **0** 이어야 PASS. bib `\code` 예외 여부는 D5 확정 후 게이트에 반영.

## Read Coverage
`_sections/` 전체 grep(코드토큰, 주석·매크로정의 제외) + 위 12행 원문 sed 확인 + 부록 6파일·§3.5 식별. F-11 원 스캔(USER_FEEDBACK_v1024_READING.md)과 17행 완전 일치 = 안정.
