# Phase 059 PDF artifact render audit

정본일: 2026-07-28

판정: `CONDITIONAL_P059_PDF_RENDER_PASS_WITH_ACCESSIBILITY_AND_PROVENANCE_DEBTS`

## 범위와 경계

v1.0.14–v1.0.18.2의 18 PDF, 492 pages를 96 dpi로 전부 render했고 37 contact sheets를 모두 육안 검독했다. 기계적으로 선별한 고밀도·최소여백·수식추출·표·마지막 페이지 13쪽은 원해상도로 다시 확인했다.

이 판정은 artifact 가독성, 내부 link, 글꼴 embedding과 provenance에 대한 것이다. 식의 물리적 타당성, 문헌 진실성, 코드 정합 또는 실험 데이터 설명력을 이 결과만으로 승인하지 않는다.

전 페이지 PNG와 contact sheet는 검증 후 삭제하는 일시 중간물이다. 재현 가능한 script, source/render hash, 기계 metrics와 육안 판정만 repository에 보존한다.

## 결론

- 가시적 render는 통과했다. blank, 깨진 PNG, crop/media 불일치, page-boundary 밖 문자·단어, edge-touch, 잘린 식·표·그림을 찾지 못했다.

- 18 PDF의 모든 font는 embedded 상태다. 그러나 모든 PDF에 ToUnicode map이 없는 CMEX10이 있고 Chapter 1에는 CMSY10도 있어, pypdf 추출에서 NUL 3,117자가 발생한다. 화면 표시가 아니라 검색·복사·접근성 결함이다.

- v1.0.16 `appendix_phase_separation`은 v1.0.15 TeX와 exact-identical이고 8쪽 render도 전부 exact-identical이다. 표지에는 실제로 `버전 1.0.15 초안`이 남아 있으므로 v1.0.16 provenance를 주장할 수 없다.

- 등록된 named destination 자체는 모두 유효 page를 가리키고 본문의 `??` 표지는 0이다. 그러나 각주 복귀용 `Hfootnote.*` GoTo link 26개는 name tree에 목적지가 없어 끊겨 있다.

## 문서별 기계·링크 검사

| version | document | pages | contacts | NUL | fonts embedded | all ToUnicode | links | version label |
|---|---|---:|---:|---:|---|---|---:|---|
| v1.0.14 | appendix | 8 | 1 | 2 | yes | no | 38 | MATCH |
| v1.0.14 | chapter1 | 57 | 4 | 511 | yes | no | 790 | MATCH |
| v1.0.14 | chapter2 | 14 | 1 | 0 | yes | no | 138 | NOT_APPLICABLE_NO_TITLE_PAGE_VERSION |
| v1.0.15 | appendix | 8 | 1 | 2 | yes | no | 38 | MATCH |
| v1.0.15 | chapter1 | 58 | 4 | 521 | yes | no | 817 | MATCH |
| v1.0.15 | chapter2 | 16 | 1 | 0 | yes | no | 153 | NOT_APPLICABLE_NO_TITLE_PAGE_VERSION |
| v1.0.16 | appendix | 8 | 1 | 2 | yes | no | 38 | MISMATCH |
| v1.0.16 | chapter1 | 58 | 4 | 521 | yes | no | 817 | MATCH |
| v1.0.16 | chapter2 | 16 | 1 | 0 | yes | no | 156 | NOT_APPLICABLE_NO_TITLE_PAGE_VERSION |
| v1.0.17 | appendix | 8 | 1 | 2 | yes | no | 39 | MATCH |
| v1.0.17 | chapter1 | 58 | 4 | 521 | yes | no | 819 | MATCH |
| v1.0.17 | chapter2 | 16 | 1 | 0 | yes | no | 159 | NOT_APPLICABLE_NO_TITLE_PAGE_VERSION |
| v1.0.18.1 | appendix | 8 | 1 | 2 | yes | no | 42 | MATCH |
| v1.0.18.1 | chapter1 | 59 | 4 | 515 | yes | no | 822 | MATCH |
| v1.0.18.1 | chapter2 | 16 | 1 | 0 | yes | no | 159 | NOT_APPLICABLE_NO_TITLE_PAGE_VERSION |
| v1.0.18.2 | appendix | 8 | 1 | 2 | yes | no | 42 | MATCH |
| v1.0.18.2 | chapter1 | 59 | 4 | 515 | yes | no | 822 | MATCH |
| v1.0.18.2 | chapter2 | 17 | 2 | 1 | yes | no | 166 | NOT_APPLICABLE_NO_TITLE_PAGE_VERSION |

## 원해상도 표적 검수

| PDF | page | 선별 이유 | 판정 |
|---|---:|---|---|
| `v1_0_16__appendix_phase_separation` | 1 | version-label provenance check | Rendered cleanly, but the visible title says version 1.0.15 inside the v1.0.16 directory. |
| `v1_0_18_2__appendix_phase_separation` | 5 | densest appendix page with two figures | Both figures, axes, captions, and following heading are intact. |
| `v1_0_14__graphite_ica_ch1_v1.0.14` | 20 | densest v1.0.14 Chapter 1 page | Figure, caption, equations, and body remain inside the page. |
| `v1_0_17__graphite_ica_ch1_v1.0.17` | 25 | densest v1.0.17 Chapter 1 page | Dense prose and inline mathematics remain legible and unclipped. |
| `v1_0_18_2__graphite_ica_ch1_v1.0.18.2` | 25 | densest latest Chapter 1 page | Dense prose and inline mathematics remain legible and unclipped. |
| `v1_0_18_2__graphite_ica_ch1_v1.0.18.2` | 50 | high NUL-extraction count and boxed equations | All visible mathematical delimiters and boxed equations render; the defect is extraction, not display. |
| `v1_0_18_2__graphite_ica_ch1_v1.0.18.2` | 55 | smallest measured right margin and two wide tables | Both tables remain within the page; no right-edge clipping is visible. |
| `v1_0_14__graphite_ica_ch1_v1.0.14` | 49 | high NUL-extraction count and equation-flow diagram | Integral delimiters, arrows, equations, and flow diagram render visibly. |
| `v1_0_14__graphite_ica_ch2_v1.0.14` | 12 | densest v1.0.14 Chapter 2 page | Boxed heat equations and body text remain intact. |
| `v1_0_16__graphite_ica_ch2_v1.0.16` | 10 | densest v1.0.16 Chapter 2 page | Bullets, equations, and headings remain intact. |
| `v1_0_18_2__graphite_ica_ch2_v1.0.18.2` | 7 | latest Chapter 2 page containing an extracted NUL | Large mathematical brackets and equations render visibly; the single NUL is a text-extraction defect. |
| `v1_0_18_2__graphite_ica_ch2_v1.0.18.2` | 11 | densest latest Chapter 2 page | Dense bullets and equations remain legible and unclipped. |
| `v1_0_18_2__graphite_ica_ch2_v1.0.18.2` | 17 | new final reference page | References are intact; the lower-page whitespace is intentional, not blank loss. |

## Finding register

| ID | 판정 | 내용 | 후속 처리 |
|---|---|---|---|
| PDF-059-01 | PASS | 492/492 pages와 37/37 contact sheets의 가시적 layout 이상 없음 | Phase 35.3에서 생성 계보 연결 |
| PDF-059-02 | EVIDENCE_DEBT | 18/18 PDF에 non-ToUnicode math font; 추출 NUL 3,117 | 최종 문건 build에서 Unicode math 또는 actual-text layer 검증 gate 추가 |
| PDF-059-03 | PROVENANCE_DEFECT | v1.0.16 appendix가 v1.0.15 source/render copy이고 표지도 v1.0.15 | v1.0.16의 새 appendix 증거로 계수 금지 |
| PDF-059-04 | LINK_DEFECT | 등록된 named destination은 유효하고 `??`는 0이나 `Hfootnote.*` 목적지 26개가 누락 | 최종 build에서 각주 복귀 link target 검증 gate 추가 |

## 다음 단계

Step 35.2에서 10 standalone image의 원해상도 축·단위·legend·조건·peak morphology와 생성 source를 감사한다.
