# V1025_T13_T14_REPORT — T13(데이터 정직화) · T14(버전 문자열) 집행 결과

> 집행: 기계적 실무 서브세션(2026-07-26). 지시 = `results/V1025_DOC_CASCADE_TODO.md` **T13·T14** + 마스터 브리프.
> 경계 준수: `_sections/*.tex`(마스터 동시 편집 중) **무편집** · `Claude/docs/v1.0.24.1/`·`Claude/docs/v1.0.24/`
> **무편집** · `Claude/results/comp_v24/` 기존 파일 **무편집**(addendum 방식). 질문·확인 팝업 0회.

---

## 0. 생성·수정 파일 (전체)

| 파일 | 종류 | 줄 수 변화 | 줄바꿈 |
|---|---|---|---|
| `Claude/docs/v1.0.25/results/V1025_DATA_ADDENDUM.md` | **신규 생성**(T13) | 0 → **291** | CRLF (291/291, bare LF 0) |
| `Claude/docs/v1.0.25/ARCHIVE_NOTE.md` | **수정**(T14, 추기만) | 40 → **109** (+69) | CRLF (109/109, bare LF 0) |
| `Claude/docs/v1.0.25/ch1_graphite_v1.0.24.tex` | **수정**(T14) | 60 → **62** (+2) | CRLF (62/62, bare LF 0) |
| `Claude/docs/v1.0.25/ch2_lco_v1.0.24.tex` | **수정**(T14) | 32 → **34** (+2) | CRLF (34/34, bare LF 0) |
| `Claude/docs/v1.0.25/ch3_si_v1.0.24.tex` | **수정**(T14) | 32 → **34** (+2) | CRLF (34/34, bare LF 0) |
| `Claude/docs/v1.0.25/results/V1025_T13_T14_REPORT.md` | **신규 생성**(본 문서) | 0 → **484** | CRLF (484/484, bare LF 0) |

**보호 경로 무변경 확인**(`git status --porcelain`, 출력 없음 = clean): `Claude/results/comp_v24/` ·
`Claude/docs/v1.0.24/` · `Claude/docs/v1.0.24.1/`. `_sections/` 는 마스터 편집 영역이라 **읽기만** 했다(편집 0).

그밖에 **수정한 파일 없음**. 편집 보조 스크립트 3종은 세션 스크래치에만 두었다(리포 미기입):
`t14_edit.py` · `archive_note_append.py` · `verify_protocol.py`.

**줄바꿈 보존 절차(지시대로 실행)**: 편집 전 원 파일의 CRLF/LF 개수를 세어 4파일 모두 **순수 CRLF(bare LF 0)**
임을 확인한 뒤, `open(p,'rb')` 로 읽어 **바이트 수준에서 CRLF 를 유지**하고 `open(p,'wb')` 로 되썼다.
(universal-newline 변환을 아예 거치지 않아 LF 혼입 여지 자체를 제거. 편집 후 재확인 결과 위 표의 "CRLF n/n".)
신규 md 2종은 주변 legacy 문서(`comp_v24/DATA_REGISTRY.md`·`REFLECT_SEED_TABLE.md`·`ARCHIVE_NOTE.md` 전부 CRLF)
관행에 맞춰 **CRLF** 로 통일했다.

---

## 1. T13 — 데이터 정직화 판정

**한 줄 판정: 완료.** `comp_v24/` 기존 파일을 **한 줄도 고치지 않고**, 신규 addendum
`results/V1025_DATA_ADDENDUM.md`(291줄) 에 A1~A7 을 등재했다. 각 항에 **supersede 대상(파일 + 절 이름)** 을 명기했다.

| 항 | 내용 | supersede 대상(파일·절) | 상태 |
|---|---|---|---|
| **A1** | 레포 프로토콜 혼용: `gr.csv`=gr_A=`p-ocv` / `si.csv`=si_Dhold=`p-ocvhold` | `sintef_data/SOURCES.md` §출처 "측정 조건"·§파일 표 / `DATA_REGISTRY.md` §2 SINTEF 행 / `FIT_CHECK_v1024.md` §"결과 — SINTEF … raw" R² 표("동일 데이터" 전제) | 등재 + **독립 확인** |
| **A2** | `p-ocvhold` 권고: 동일 7전이 R² 0.9770→0.9945 · 피크역 RMSE 4.708→2.701 | `DATA_REGISTRY.md` §5b 표 "SINTEF 흑연 … 잔차 원인 = 모델" 행 + 같은 절 "남는 잔차는 모델" 단정 / `FIT_CHECK_v1024.md` §정직한 한계 "…데이터 아님" | 등재(부분 supersede) |
| **A3** | 독립셀 재현성: gr_B 0.9770(레포 동일) · si_A/si_Chold 0.998~0.999 | **없음(신규 등재)**. 성격 한정 = `DATA_REGISTRY.md` §5 확장 프로토콜 **미경유**(레지스트리 셀 수 미합산·파이프라인 미증설) | 등재 |
| **A4** | @3(regsol) 채택 근거 철회 + 코드 삭제. 전이 고정 +0.97 %p → 승격 −0.53 %p 역전. **Ω 는 존치**(삭제 = dQ/dV 커널만) | `ABLATION_ANODE.md` §결과 표 @3 행("+0.67 %p·★유일 실효")·§한 줄 결론 / `REFLECT_SEED_TABLE.md` §1 "개선효과" 행·"코드 지점" 행 / `FIT_CHECK_v1024.md` §"@3 Si regsol Ω/RT …"·§"문건↔코드 정합 정정 — sifr Ω>2RT binodal" 의 재현 경로 | 등재 + 코드 상태 **독립 확인** |
| **A5** | `C_bg` 비상수 실측: 0.433→0.032(창 평균 ~230 %)·4셀·2프로토콜 전건 일치. 광폭 단독 대체는 악화(0.97702→0.97415), skew 동반 시 이득(0.98178) | **없음(신규 등재)** — comp_v24 에 `C_bg` 상수 단정 절 부재. 정정 대상은 문건 측(`V1025_DOC_CASCADE_TODO.md` **T10**, 마스터 소관) | 등재 |
| **A6** | @1~@5 조합 실측표(흑연 `gr.csv` 300점, R²·피크역·벨리역 3열) + Si 전이 수 스윕 | `ABLATION_ANODE.md` §결과 표 **순위 전체** + §한 줄 결론 4항(@2 "무의미"→최대 이득 / @4 "공짜"→−3.9 %p / @5 "해로움"→+0.61~0.80 %p) | 등재(조건 차이 명시) |
| **A7** | gallery ≠ 상: 7·9전이 중심 U 가 105/141/227 mV 에 ΔU<12 mV 근축퇴 / 검출 피크 3→4→5(prominence 의존) / Si 0.43–0.46 V feature 는 hold 전용 / XRD 상 수 불변(Dahn PRB **44**, 9170 (1991) — staging 전이 4·물리 두-상 2) | `GRAPHITE_STAGING_XRD.md` §2 말미 "6+ = 끼워맞추기"·§5 항 1 "6개는 물리 위반 — 폐기" / `REFLECT_SEED_TABLE.md` §2 "경계: … 6+ = curve-fitting(폐기 유지)" / `DATA_REGISTRY.md` §4 분포 표(피크 3개) | 등재(조준 정정) |

**수치 창작 0**: A1~A7 의 피팅 수치는 **마스터 브리프에 제공된 값만** 사용했다. 제공되지 않은 값은 addendum 에
**"미측정"** 으로 남겼다(`sigr.csv` 프로토콜 등 — §미해결 M1~M6). 측정 주체는 addendum §0 에 "마스터 세션 측정 ·
본 서브세션 미재실행(「독립 확인」 표기 항목 제외)" 로 **명시 고지**했다.

**본 서브세션이 브리프를 넘어 추가한 것**(전부 직접 실행한 확인, 창작 아님): A1 의 프로토콜 매핑 독립 검증,
A4 의 코드 상태 독립 검증, A6 의 순위 역전에 대한 **조건 차이 명시**(v1.0.24 ABLATION = 블렌드 `sigr_aq1`·기준
R² 0.987 vs v1.0.25 = 흑연 `gr.csv` 300점·기준 R² 0.97090 — 같은 실험이 아님), A7 의 선행 불일치 등재(아래 미해결 M4).

---

## 2. T14 — 버전 문자열 판정

**한 줄 판정: 완료. 파일명·식별자 문자열 개명 0건.** 3개 마스터 `.tex` 에서 **사람이 읽는 표시 버전 3곳**(각 파일당)
만 교체하고, 상단 주석 블록에 v1.0.25 이력 2줄을 추가했다(기존 주석 줄 삭제 0). `ARCHIVE_NOTE.md` 는 기존 40줄을
**보존**한 채 v1.0.25 절(S1~S6)을 **추기**했다.

### 2.1 파일별 변경 (v1.0.24.1 원본 대비 diff — 아래 §3.3 원문 출력)

| 파일 | pdftitle | lhead | `\date` | 주석 추가 |
|---|---|---|---|---|
| `ch1_graphite_v1.0.24.tex` | 1회 | 1회 | 1회 | 2줄(line 7–8) |
| `ch2_lco_v1.0.24.tex` | 1회 | 1회 | 1회 | 2줄(line 5–6) |
| `ch3_si_v1.0.24.tex` | 1회 | 1회 | 1회 | 2줄(line 5–6) |

각 파일 총 변경 = **치환 3행 + 삽입 2행**. 그 외 행 무변경(diff 로 증빙).

### 2.2 손대지 않은 것 (지시대로)

`_sections/common_preamble_v1024.tex` · `appendix_phase_separation.tex` · `_sections/` 전체(56 .tex) ·
`Anode_Fit_v1.0.24.py` · `test_gates_*.py` · `CODE_GUIDE_v24.{md,html}` · `FITTING_GUIDE.md`.

### 2.3 `1.0.24` 잔존 12곳 — 전건 "남겨야 함" 판정

| # | 위치 | 문자열 | 판정 근거 |
|--:|---|---|---|
| 1 | ch1:2 | `% ch1_graphite_v1.0.24.tex — …` | **파일명** 자기기술 주석 — 파일명 불변이므로 불변 |
| 2 | ch1:3 | `%   (v1.0.24 활물질별 재편 …` | **이력 주석**(v1.0.24 시점 재편 사실) |
| 3 | ch1:6 | `%   v1.0.24 신규: §5 폭 뒤 stage-2L …` | **이력 주석**(v1.0.24 신규 항목 기록) |
| 4 | ch1:11 | `\externaldocument{ch2_lco_v1.0.24}` | **xr 키 = 파일명 식별자** — 바꾸면 외부 참조 파손 |
| 5 | ch1:32 | `\input{_sections/ch1_sec05b_gr2L}% v1.0.24 신규 …` | **이력 주석**(경로 자체는 v1024 토큰 없음) |
| 6 | ch2:2 | `% ch2_lco_v1.0.24.tex — …` | **파일명** 자기기술 주석 |
| 7 | ch2:9 | `\externaldocument{ch1_graphite_v1.0.24}` | **xr 키 = 파일명 식별자** |
| 8 | ch2:30 | `\input{…ch1_sec16b_lcoomega}% v1.0.24 신규 …` | **이력 주석** |
| 9 | ch3:2 | `% ch3_si_v1.0.24.tex — …` | **파일명** 자기기술 주석 |
| 10 | ch3:9 | `\externaldocument{ch1_graphite_v1.0.24}` | **xr 키 = 파일명 식별자** |
| 11 | ch3:10 | `\externaldocument{ch2_lco_v1.0.24}` | **xr 키 = 파일명 식별자** |
| 12 | ch3:27 | `\input{…ch3v22_sec02b_sifr}% v1.0.24 신규 …` | **이력 주석** |

분류 집계: **파일명 자기기술 3 · 이력 주석 5 · `\externaldocument` xr 키 4**. **표시 버전 잔존 0**.
(`\input{_sections/common_preamble_v1024}` 는 `1.0.24` 패턴에 걸리지 않는 `v1024` 토큰 — 마찬가지로 파일명 식별자,
지시대로 불변. `\code{Anode\_Fit\_v1.0.24.py}` 류 코드 식별자는 이 3개 마스터 파일에 **출현하지 않는다**(grep 0 —
§3.1 출력에 `Anode_Fit` 히트 없음). 그 문자열은 `_sections/` 쪽 자산이며 마스터 소관.)

### 2.4 ARCHIVE_NOTE.md 갱신 — 스테일 주장 처리

기존 40줄 **무삭제**. 추기 절 S1~S6 신설(+69줄):
- **S1** = 스테일 판정 표. 위 본문의 "코드(.py) 무변경" · "sha256 f230f59b…" · "문건 한정 리비전" ·
  "빌드 GREEN 97/30/21 페이지" · "빌드본 PDF 3종" 을 **v1.0.25 에 대해 스테일**로 표시하고,
  "`diff -rq v1.0.24 v1.0.24.1` = IDENTICAL"(원본 두 폴더에 대해 **여전히 참**)·"파일명 v1.0.24 유지"(**유효·재확인**)
  는 유효로 남겼다 — 무차별 무효화 금지.
- **S2** = 코드 변경(파일명 유지·내부 release 버전 1.0.25 / 추가 4종 / 삭제 regsol 3종 + `'kernel'` 분기 /
  **Ω 존치** / 줄 수 / 골든 G1 max|d| = 0.0).
- **S3** = 문건 변경 = 표시 버전만(DG-2) + 개명 금지 목록.
- **S4** = 원본 아카이브 무변경 확인(LF-sha256 `f230f59bb10bcc49` 두 폴더 동일 · git clean · diff 차이 = ARCHIVE_NOTE 뿐).
- **S5** = 게이트·빌드 상태(마스터 실행 인용분 / 서브세션 직접 확인분 / **빌드 미수행** 을 3구분).
- **S6** = 데이터 정정은 `V1025_DATA_ADDENDUM.md` 로 처리했음을 연결.

**★줄 수 수치 정정(브리프 대비)**: 브리프는 "1957 → **1917** 줄" 로 지시했다. 실측은 아래와 같다 — 두 수를 모두
살려 S2 에 **명시적으로 구분**해 적었다.
- `docs/v1.0.24`·`docs/v1.0.24.1` 아카이브 코드 = **1734 줄**(LF 기준, 111823 바이트) → `docs/v1.0.25` = **1917 줄**(124501 바이트).
- 곧 **1957 은 v1.0.24 아카이브 줄 수가 아니다.** 1957 → 1917(−40)은 **v1.0.25 개발 중 regsol 삭제 그 단계**의
  변화로 읽어야 정합하며(`V1025_DOC_CASCADE_TODO.md` 참고표 C6 항 "**−40줄**" 과 일치), 아카이브→v1.0.25 의
  총 변화는 **1734 → 1917(+183)** 이다. "v1.0.24 대비 1957→1917" 로 쓰면 스테일 수치가 된다.

---

## 3. 실행한 검증 — 명령과 원문 출력

> **빌드는 하지 않았다.** 본 PC 에 TeX 배포판이 없음을 직접 확인했다(§3.4). "빌드 GREEN" 류 주장은 어디에도 쓰지 않았다.

### 3.1 V1 — 파일명·`\input`·`\externaldocument` 문자열 불변 증빙

```
$ grep -n "input{_sections\|externaldocument\|Anode_Fit" ch1_graphite_v1.0.24.tex ch2_lco_v1.0.24.tex ch3_si_v1.0.24.tex
ch1_graphite_v1.0.24.tex:8:%   (파일명·input 경로·externaldocument 키는 불변 — 사람이 읽는 표시 버전만 갱신: DG-2 사용자 확정.)
ch1_graphite_v1.0.24.tex:10:\input{_sections/common_preamble_v1024}
ch1_graphite_v1.0.24.tex:11:\externaldocument{ch2_lco_v1.0.24}% 전방 참조(LCO 장 22곳 — 교과서 관행) — 첫 빌드에서는 ?? 후 ch2 빌드 뒤 재패스로 해소
ch1_graphite_v1.0.24.tex:25:\input{_sections/ch1_sec00_intro}
ch1_graphite_v1.0.24.tex:26:\input{_sections/ch1_sec01_n0n1}
ch1_graphite_v1.0.24.tex:27:\input{_sections/ch1_sec02a_part0}
ch1_graphite_v1.0.24.tex:28:\input{_sections/ch1_sec02b_part0}
ch1_graphite_v1.0.24.tex:29:\input{_sections/ch1_sec03_center}
ch1_graphite_v1.0.24.tex:30:\input{_sections/ch1_sec04_hys}
ch1_graphite_v1.0.24.tex:31:\input{_sections/ch1_sec05_width}
ch1_graphite_v1.0.24.tex:32:\input{_sections/ch1_sec05b_gr2L}% v1.0.24 신규 — stage-2L 엔트로피 T-분리(@5)
ch1_graphite_v1.0.24.tex:33:\input{_sections/ch1_sec06_eqpeak}
ch1_graphite_v1.0.24.tex:34:\input{_sections/ch1_sec07_broadening}
ch1_graphite_v1.0.24.tex:35:\input{_sections/ch1_sec08_lag}
ch1_graphite_v1.0.24.tex:36:\input{_sections/ch1_sec09_tail}
ch1_graphite_v1.0.24.tex:37:\input{_sections/ch1_sec10_sum}
ch1_graphite_v1.0.24.tex:39:\input{_sections/ch1v22_partT_divider}
ch1_graphite_v1.0.24.tex:40:\input{_sections/ch2_sec00_intro}
ch1_graphite_v1.0.24.tex:41:\input{_sections/ch2_sec01_partition}
ch1_graphite_v1.0.24.tex:42:\input{_sections/ch2_sec02_config}
ch1_graphite_v1.0.24.tex:43:\input{_sections/ch2_sec03_vibel}
ch1_graphite_v1.0.24.tex:44:\input{_sections/ch2_sec04_einstein}
ch1_graphite_v1.0.24.tex:45:\input{_sections/ch2_sec05_mixing}
ch1_graphite_v1.0.24.tex:46:\input{_sections/ch2_sec06_limits}
ch1_graphite_v1.0.24.tex:47:\input{_sections/ch2_sec07_revheat}
ch1_graphite_v1.0.24.tex:48:\input{_sections/ch2_sec08_synthesis}
ch1_graphite_v1.0.24.tex:49:\input{_sections/ch2_sec09_method}
ch1_graphite_v1.0.24.tex:50:\input{_sections/ch2_sec10_closing}
ch1_graphite_v1.0.24.tex:52:\input{_sections/ch1_sec18_inputs}
ch1_graphite_v1.0.24.tex:54:\input{_sections/ch1_appA_signcheck}
ch1_graphite_v1.0.24.tex:55:\input{_sections/ch1_appB_codemap}
ch1_graphite_v1.0.24.tex:56:\input{_sections/ch2_appA_traps}
ch1_graphite_v1.0.24.tex:57:\input{_sections/ch2_appB_codemap}
ch1_graphite_v1.0.24.tex:58:\input{_sections/ch1_appE_selfconsistent}
ch1_graphite_v1.0.24.tex:60:\input{_sections/ch1v22_bib}
ch2_lco_v1.0.24.tex:6:%   (파일명·input 경로·externaldocument 키는 불변 — 사람이 읽는 표시 버전만 갱신: DG-2 사용자 확정.)
ch2_lco_v1.0.24.tex:8:\input{_sections/common_preamble_v1024}
ch2_lco_v1.0.24.tex:9:\externaldocument{ch1_graphite_v1.0.24}
ch2_lco_v1.0.24.tex:22:\input{_sections/ch2v22_sec00_intro}
ch2_lco_v1.0.24.tex:23:\input{_sections/ch2v22_notation}
ch2_lco_v1.0.24.tex:24:\input{_sections/ch1_sec11_lcointro}
ch2_lco_v1.0.24.tex:25:\input{_sections/ch1_sec12_lcocenter}
ch2_lco_v1.0.24.tex:26:\input{_sections/ch1_sec13_lcohys}
ch2_lco_v1.0.24.tex:27:\input{_sections/ch1_sec14_lcodecomp}
ch2_lco_v1.0.24.tex:28:\input{_sections/ch1_sec15_lcoelec}
ch2_lco_v1.0.24.tex:29:\input{_sections/ch1_sec16_lcopeak}
ch2_lco_v1.0.24.tex:30:\input{_sections/ch1_sec16b_lcoomega}% v1.0.24 신규 — per-peak Ω·#7 정정·전자항 토글(@3)
ch2_lco_v1.0.24.tex:31:\input{_sections/ch1_sec17_msmr}
ch2_lco_v1.0.24.tex:32:\input{_sections/ch2v22_bib}
ch3_si_v1.0.24.tex:6:%   (파일명·input 경로·externaldocument 키는 불변 — 사람이 읽는 표시 버전만 갱신: DG-2 사용자 확정.)
ch3_si_v1.0.24.tex:8:\input{_sections/common_preamble_v1024}
ch3_si_v1.0.24.tex:9:\externaldocument{ch1_graphite_v1.0.24}
ch3_si_v1.0.24.tex:10:\externaldocument{ch2_lco_v1.0.24}
ch3_si_v1.0.24.tex:23:\input{_sections/ch3v22_sec00_intro}
ch3_si_v1.0.24.tex:24:\input{_sections/ch3v22_notation}
ch3_si_v1.0.24.tex:25:\input{_sections/ch3v22_sec01_map}
ch3_si_v1.0.24.tex:26:\input{_sections/ch3v22_sec02_cases}
ch3_si_v1.0.24.tex:27:\input{_sections/ch3v22_sec02b_sifr}% v1.0.24 신규 — Si-host Frumkin 커널(@3)
ch3_si_v1.0.24.tex:28:\input{_sections/ch3v22_sec03_blend}
ch3_si_v1.0.24.tex:29:\input{_sections/ch3v22_sec04_mech}
ch3_si_v1.0.24.tex:31:\input{_sections/ch3v22_sec05_code}
ch3_si_v1.0.24.tex:32:\input{_sections/ch3v22_bib}
```

판정: `\input` 46개(preamble 3 + 절 43) · `\externaldocument` 4개 = **전부 v1.0.24.1 원본과 동일**(§3.3 diff 가
이 행들을 변경분으로 잡지 않음). `Anode_Fit` 히트 **0** — 이 3파일에는 코드 식별자 문자열이 없다.
line 8/6/6 히트는 **이번에 추가한 주석**(불변 원칙을 명문화한 줄)이다.

### 3.2 V2 — `1.0.24` 잔존 위치 전량 열거

```
$ grep -rn "1\.0\.24" ch1_graphite_v1.0.24.tex ch2_lco_v1.0.24.tex ch3_si_v1.0.24.tex
ch1_graphite_v1.0.24.tex:2:% ch1_graphite_v1.0.24.tex — Chapter 1 마스터: 흑연 음극 — dQ/dV 이론 + 열특성
ch1_graphite_v1.0.24.tex:3:%   (v1.0.24 활물질별 재편 — 원천 = v1.0.21 구 Ch1 §0~10 + 구 Ch2 전량[Part T].
ch1_graphite_v1.0.24.tex:6:%   v1.0.24 신규: §5 폭 뒤 stage-2L 소절(ch1_sec05b_gr2L) — @5 반영(엔트로피 T-분리).
ch1_graphite_v1.0.24.tex:11:\externaldocument{ch2_lco_v1.0.24}% 전방 참조(LCO 장 22곳 — 교과서 관행) — 첫 빌드에서는 ?? 후 ch2 빌드 뒤 재패스로 해소
ch1_graphite_v1.0.24.tex:32:\input{_sections/ch1_sec05b_gr2L}% v1.0.24 신규 — stage-2L 엔트로피 T-분리(@5)
ch2_lco_v1.0.24.tex:2:% ch2_lco_v1.0.24.tex — Chapter 2 마스터: LCO 양극 — 추가 텀 방식 (v1.0.24 재편)
ch2_lco_v1.0.24.tex:9:\externaldocument{ch1_graphite_v1.0.24}
ch2_lco_v1.0.24.tex:30:\input{_sections/ch1_sec16b_lcoomega}% v1.0.24 신규 — per-peak Ω·#7 정정·전자항 토글(@3)
ch3_si_v1.0.24.tex:2:% ch3_si_v1.0.24.tex — Chapter 3 마스터: Si·혼합음극 (v1.0.24 재편 골격)
ch3_si_v1.0.24.tex:9:\externaldocument{ch1_graphite_v1.0.24}
ch3_si_v1.0.24.tex:10:\externaldocument{ch2_lco_v1.0.24}
ch3_si_v1.0.24.tex:27:\input{_sections/ch3v22_sec02b_sifr}% v1.0.24 신규 — Si-host Frumkin 커널(@3)
```

**12곳 · 전건 판정 = 남겨야 함.** 사유 한 줄씩 = §2.3 표. **표시 버전 잔존 0.**

### 3.3 v1.0.24.1 원본 대비 diff (변경 최소성 증빙)

```
$ cd Claude/docs && for f in ch1_graphite_v1.0.24.tex ch2_lco_v1.0.24.tex ch3_si_v1.0.24.tex; do diff -u "v1.0.24.1/$f" "v1.0.25/$f"; done

--- v1.0.24.1/ch1_graphite_v1.0.24.tex
+++ v1.0.25/ch1_graphite_v1.0.24.tex
@@ -4,17 +4,19 @@
 %   v1.0.24 신규: §5 폭 뒤 stage-2L 소절(ch1_sec05b_gr2L) — @5 반영(엔트로피 T-분리).
+%   v1.0.25 국소 수정: @2 skew(eq:skewpeak) opt-in · 인과 pad(_causal_pad) · C_bg 창-국소 명기 · @3 regsol 코드 삭제 · 상수 SI opt-in.
+%   (파일명·input 경로·externaldocument 키는 불변 — 사람이 읽는 표시 버전만 갱신: DG-2 사용자 확정.)
 % ====================================================================
-\hypersetup{pdftitle={흑연 음극 dQ/dV 이론과 열특성 — Chapter 1 (v1.0.24)}}
-\lhead{흑연 음극 $dQ/dV$ 이론과 열특성 — Ch.1 (v1.0.24)}
+\hypersetup{pdftitle={흑연 음극 dQ/dV 이론과 열특성 — Chapter 1 (v1.0.25)}}
+\lhead{흑연 음극 $dQ/dV$ 이론과 열특성 — Ch.1 (v1.0.25)}
-\date{\normalsize 버전 1.0.24}
+\date{\normalsize 버전 1.0.25}

--- v1.0.24.1/ch2_lco_v1.0.24.tex
+++ v1.0.25/ch2_lco_v1.0.24.tex
@@ -2,17 +2,19 @@
 %   빌드 순서 주의: ch1 을 먼저 3-pass 빌드해야 외부 참조가 해소된다(ch1→ch2→(ch1 갱신 시 반복)).
+%   v1.0.25 국소 수정: w_eff(Ω) 금지 조준을 두-상 폭 한정으로 좁힘 · 상수 SI opt-in(use_si_constants) worked-example 표시값 각주.
+%   (파일명·input 경로·externaldocument 키는 불변 — 사람이 읽는 표시 버전만 갱신: DG-2 사용자 확정.)
 % ====================================================================
-\hypersetup{pdftitle={LCO 양극 dQ/dV 와 열특성 — Chapter 2 (v1.0.24)}}
-\lhead{LCO 양극 $dQ/dV$ 와 열특성 — Ch.2 (v1.0.24)}
+\hypersetup{pdftitle={LCO 양극 dQ/dV 와 열특성 — Chapter 2 (v1.0.25)}}
+\lhead{LCO 양극 $dQ/dV$ 와 열특성 — Ch.2 (v1.0.25)}
-\date{\normalsize 버전 1.0.24}
+\date{\normalsize 버전 1.0.25}

--- v1.0.24.1/ch3_si_v1.0.24.tex
+++ v1.0.25/ch3_si_v1.0.24.tex
@@ -2,18 +2,20 @@
 %   본문은 R4 조사 → R5 저작 소관. Ch1/Ch2 결과식은 xr 외부 참조.
+%   v1.0.25 국소 수정: 비대칭 = envelope 전용 서술 완화(skew 지수 alpha_j opt-in 병기) · @3 regsol 코드 삭제 반영(해석적 기록만) · Si 7-gallery(SI_MSMR7_LIT) opt-in 병기.
+%   (파일명·input 경로·externaldocument 키는 불변 — 사람이 읽는 표시 버전만 갱신: DG-2 사용자 확정.)
 % ====================================================================
-\hypersetup{pdftitle={Si·혼합음극 — Chapter 3 (v1.0.24)}}
-\lhead{Si·혼합음극 — Ch.3 (v1.0.24)}
+\hypersetup{pdftitle={Si·혼합음극 — Chapter 3 (v1.0.25)}}
+\lhead{Si·혼합음극 — Ch.3 (v1.0.25)}
-\date{\normalsize 버전 1.0.24}
+\date{\normalsize 버전 1.0.25}
```

(문맥행은 지면상 축약. 각 파일 hunk 는 **1개**이며 그 안의 변경은 위 5행뿐 — `\input`·`\externaldocument`·`\title`·
`\renewcommand`·`\begin{document}` 이하 전부 무변경.)

### 3.4 TeX 배포판 부재 확인 (빌드 미수행 근거)

```
$ for c in xelatex pdflatex latexmk lualatex tex; do printf "%s: " "$c"; command -v $c || echo "NOT FOUND"; done
xelatex: NOT FOUND
pdflatex: NOT FOUND
latexmk: NOT FOUND
lualatex: NOT FOUND
tex: NOT FOUND
$ ls -d /c/texlive
ls: cannot access '/c/texlive': No such file or directory
```

판정: **빌드 불가 · 빌드 미수행.** PDF 페이지 수·0-error·undefined ref 0 은 **본 세션에서 검증되지 않았다.**
`docs/v1.0.25/*.pdf` 도 부재(존재하는 PDF 3종은 `docs/v1.0.24.1/` 뿐).

### 3.5 구조 검사 (빌드 대체 · 지시대로 1회 실행 · 실패 시 재시도 금지 규칙 적용)

```
$ cd Claude/docs/v1.0.25 && PYTHONIOENCODING=utf-8 python results/tools_check_structure.py check . \
    ch1_graphite_v1.0.24.tex ch2_lco_v1.0.24.tex ch3_si_v1.0.24.tex appendix_phase_separation.tex
=== ch1_graphite_v1.0.24.tex (34 files) ===
labels: 265 (dup: 0) []
refs: 1090 (unresolved: 0) []
cites: 138 keys, bibitems: 44 (cite-undef: [], bib-uncited: [])
env pairing errors: 0
asset anchors: 265 tags, unique 265
math env blocks: 145 (boxed: 39)
=== ch2_lco_v1.0.24.tex (13 files) ===
labels: 82 (dup: 0) []
refs: 355 (unresolved: 0) []
cites: 77 keys, bibitems: 15 (cite-undef: [], bib-uncited: [])
env pairing errors: 0
asset anchors: 92 tags, unique 92
math env blocks: 49 (boxed: 16)
=== ch3_si_v1.0.24.tex (11 files) ===
labels: 44 (dup: 0) []
refs: 190 (unresolved: 0) []
cites: 86 keys, bibitems: 36 (cite-undef: [], bib-uncited: [])
env pairing errors: 0
asset anchors: 0 tags, unique 0
math env blocks: 16 (boxed: 4)
=== appendix_phase_separation.tex (1 files) ===
labels: 30 (dup: 0) []
refs: 41 (unresolved: 0) []
cites: 0 keys, bibitems: 0 (cite-undef: [], bib-uncited: [])
env pairing errors: 0
asset anchors: 0 tags, unique 0
math env blocks: 19 (boxed: 3)
STRUCTURE_CHECK: PASS
```

**PASS** — 실패하지 않았으므로 재시도·수정 없음. **시각 = 2026-07-26 01:52:10**(마스터가 `_sections` 를 계속
편집 중이므로 이 결과는 **그 시점 스냅샷**이다. 마스터 편집이 끝난 뒤 재실행 권고 — 특히 신규 `eq:skewpeak`
라벨 정의 1회·참조 무결(T14 지시의 Step 19)은 이 시점에는 아직 검사 대상이 아니었다).

### 3.6 줄바꿈 방식 확인 (편집 전 → 편집 후)

```
$ python -c "... CRLF / bare-LF 계수 ..."
[편집 전]
ch1_graphite_v1.0.24.tex CRLF= 60 LF_total= 60 bare_LF= 0 bytes= 2745 lines= 60
ch2_lco_v1.0.24.tex      CRLF= 32 LF_total= 32 bare_LF= 0 bytes= 1509 lines= 32
ch3_si_v1.0.24.tex       CRLF= 32 LF_total= 32 bare_LF= 0 bytes= 1374 lines= 32
ARCHIVE_NOTE.md          CRLF= 40 LF_total= 40 bare_LF= 0 bytes= 2966 lines= 40
[편집 후]
ch1_graphite_v1.0.24.tex CRLF 62 bareLF 0
ch2_lco_v1.0.24.tex      CRLF 34 bareLF 0
ch3_si_v1.0.24.tex       CRLF 34 bareLF 0
ARCHIVE_NOTE.md          CRLF 109 bareLF 0
V1025_DATA_ADDENDUM.md   CRLF 291 bareLF 0   (신규 · 주변 legacy md 관행에 맞춰 CRLF)
```

전 파일 **순수 CRLF 유지 · LF 혼입 0 · BOM 없음(편집 전 assert 로 확인)**.

### 3.7 A1 독립 검증 — 레포 CSV 의 원자료 대응

```
$ python verify_protocol.py
==== gr.csv : 16827 points, V=[0.086459, 1.000010] Q=[0.0000, 2.1173]
   gr_A       n=16827   max|dV|=4.755e-06  max|dQ|=5.000e-06  differs
   gr_B       n=16501   LENGTH MISMATCH -> not the source
   gr_Chold   n=19955   LENGTH MISMATCH -> not the source
   gr_Dhold   n=19588   LENGTH MISMATCH -> not the source
==== si.csv : 10831 points, V=[0.047719, 1.000010] Q=[0.0000, 1.8953]
   si_A       n=8372    LENGTH MISMATCH -> not the source
   si_B       n=9771    LENGTH MISMATCH -> not the source
   si_Chold   n=11199   LENGTH MISMATCH -> not the source
   si_Dhold   n=10831   max|dV|=4.663e-06  max|dQ|=5.000e-06  differs
```

**해석(스크립트 라벨 정정)**: `differs` 는 스크립트의 판정 공차(1e-6)가 과하게 좁아서 붙은 라벨이다.
관측된 편차 max|dV| ≈ 4.7e−6 V · max|dQ| = 5.0e−6 mAh 는 **레포 CSV 의 저장 반올림 폭 그 자체**다
(레포 `gr.csv` 첫 행 `0.0864586,0` vs 원자료 `0.0864586383,0.0` — 유효숫자 7자리 반올림, 반올림 오차 상한 5e−6).
점수까지 완전 일치하는 후보가 **각각 단 하나**이고 나머지는 점수 자체가 다르므로 판정은 명확하다:
**`gr.csv` = gr_A** · **`si.csv` = si_Dhold**.

```
$ python -c "Zenodo record json 확인"
record id: 20086298
title: Half-Cell Open-Circuit Voltage of Several Lithium-Ion Battery Active Materials Measured under Various Electrochemical Pr…
n files: 96
$ grep -o "p-ocvhold\|p-ocv" alt/r20086298.json | sort | uniq -c
     48 p-ocv
     48 p-ocvhold
$ (파일 키 발췌)
sintef__sintef-graphite-R2032-intelligent-1d5628__20250528__p-ocv__RT.bdf.parquet
sintef__sintef-graphite-R2032-intelligent-4ccc47__20250514__p-ocv__RT.bdf.parquet
sintef__sintef-graphite-R2032-intelligent-677295__20250514__p-ocvhold__RT.bdf.parquet
sintef__sintef-graphite-R2032-intelligent-a29c1f__20250528__p-ocvhold__RT.bdf.parquet
sintef__sintef-silicon-R2032-intelligent1-2c4b6a__20250405__p-ocv__RT.bdf.parquet
sintef__sintef-silicon-R2032-intelligent1-931301__20250405__p-ocv__RT.bdf.parquet
sintef__sintef-silicon-R2032-intelligent1-5f45a8__20250405__p-ocvhold__RT.bdf.parquet
sintef__sintef-silicon-R2032-intelligent1-882755__20250405__p-ocvhold__RT.bdf.parquet
```

판정: 레코드 표제가 **"under Various Electrochemical Protocols"** 로 복수 프로토콜 수록을 명시하고, 프로토콜이
**파일명 토큰**(`p-ocv`/`p-ocvhold`/`gitt`/`gitthold`)으로 박혀 있다. 재료당 p-ocv 2 + p-ocvhold 2 → 마스터의
라벨 규약 **A·B = `p-ocv`, Chold·Dhold = `p-ocvhold`** 가 파일 키와 정합. **A1 은 독립 확인됨.**

### 3.8 A4 독립 검증 — 코드 상태(regsol 삭제 · Ω 존치)

```
$ grep -c "_REGSOL_XG\|_regsol_binodal_xa\|_regsol_dqdv" v1.0.25/Anode_Fit_v1.0.24.py
2
$ grep -n "_REGSOL_XG\|_regsol_binodal_xa\|_regsol_dqdv" v1.0.25/Anode_Fit_v1.0.24.py
12:#      C6 @3 정칙용액(Frumkin) 커널 삭제(DG-1): 커널 함수 3종(_REGSOL_XG·_regsol_binodal_xa·
13:#         _regsol_dqdv)·equilibrium 의 'kernel' 분기 전부 제거 → 커널 계통 = 로지스틱 단일계.
$ grep -c "_REGSOL_XG\|_regsol_binodal_xa\|_regsol_dqdv" v1.0.24/Anode_Fit_v1.0.24.py
6
$ grep -n "kernel'" v1.0.25/Anode_Fit_v1.0.24.py
13:#         _regsol_dqdv)·equilibrium 의 'kernel' 분기 전부 제거 → 커널 계통 = 로지스틱 단일계.
16:#         'kernel' 키가 남아 있어도 무시된다(=로지스틱) — 하위호환 무해·reflect G-R3 이 증빙.
683:            #   'kernel' 키가 남은 legacy 전이 dict 도 이 경로를 탄다(키 무시 — reflect G-R3).
$ grep -n "^def func_dxi_eq\|^def _causal_pad\|^R_SI\|^F_SI\|^def use_si_constants\|^SI_MSMR7_LIT" v1.0.25/Anode_Fit_v1.0.24.py
106:R_SI = 8.314462618      # [J/(mol·K)] CODATA-2018
107:F_SI = 96485.33212      # [C/mol]     CODATA-2018
111:def use_si_constants(enable: bool = True) -> None:
148:def func_dxi_eq(T: ScalarOrArray, V_n: ScalarOrArray, U: ScalarOrArray,
199:def _causal_pad(V_prog: np.ndarray, lag_length: float):
1357:SI_MSMR7_LIT: List[Dict[str, Any]] = [
$ grep -n "^def func_dU_hys\|^def func_dH_a_eff" v1.0.25/Anode_Fit_v1.0.24.py
312:def func_dU_hys(T: float, Omega: float) -> float:
330:def func_dH_a_eff(dH_a: float, Omega: float, chi_d: float) -> float:
```

판정: regsol 심볼 = **주석 2행뿐**(정의·호출 0). `'kernel'` = **주석 3행뿐**(디스패치 분기 0).
신규 심볼 6종 **전부 존재**. Ω 소비 함수 2종 **존치**. 코드 헤더 line 3 = `release 버전 = 1.0.25`.

### 3.9 S2/S4 독립 검증 — 줄 수 · LF-sha256 · 아카이브 무변경

```
$ python -c "LF 정규화 후 줄 수·sha256"
v1.0.24    lines= 1734 bytes= 111823 lf-sha256[:16]= f230f59bb10bcc49
v1.0.24.1  lines= 1734 bytes= 111823 lf-sha256[:16]= f230f59bb10bcc49
v1.0.25    lines= 1917 bytes= 124501 lf-sha256[:16]= 36b21a1c52af7764
$ git ls-files -- Claude/docs/v1.0.24 Claude/docs/v1.0.24.1 | wc -l
261
$ git status --porcelain -- Claude/docs/v1.0.24 Claude/docs/v1.0.24.1
(출력 없음 = 변경 0)
$ diff -rq --exclude='*.aux' --exclude='*.log' --exclude='*.out' --exclude='*.toc' \
      --exclude='__pycache__' --exclude='*.pdf' v1.0.24 v1.0.24.1
Only in v1.0.24.1: ARCHIVE_NOTE.md
```

판정: 아카이브 2폴더 **무변경**(git clean, 추적 261파일) · 코드 LF-sha256 앞 16 = `f230f59bb10bcc49` **두 폴더 동일**
(브리프와 일치) · 빌드산물 제외 두 폴더 차이 = `ARCHIVE_NOTE.md` 하나뿐. **v1.0.25 는 1917 줄**(브리프와 일치)이나
**1957 은 v1.0.24 아카이브 줄 수가 아니다**(§2.4 정정).

### 3.10 게이트 — 정의 대조만(재실행 X)

게이트 스크립트를 **실행하지 않았다**(실행 시 그림·산출물 파일이 생겨 "명시된 파일만 생성" 경계를 벗어날 수 있고,
브리프가 이미 마스터 실행분으로 값을 제공했다). 대신 **정의 존재·개수·이름을 grep 으로 대조**했다:

| 파일 | 정의된 게이트 | 마스터 보고 |
|---|---|---|
| `test_gates_v1024_reflect.py` | G-R1(@5 5-feature) · G-R2(LCO 토글) · **G-R3 = "@3 regsol 커널 삭제 확인"**(심볼 부재 3/3 + `'kernel'` 키 무시 `array_equal` + 면적=Q) · G-R4(#1 단위계약) = **4종** | 4/4 PASS |
| `test_gates_v1024_selfconsistent.py` | G-E1~G-E5 = **5종** | 5/5 PASS |
| `test_gates_v1025.py` | G-α1·G-α2·G-α3·G-α4·G-창·G-극단·G-SI·G-si7 = **8종** | 8/8 PASS |
| `test_gates_v1024.py` | (G1 골든 포함) | 전건 PASS · G1 golden max|d| = **0.0** |

**정의 개수는 마스터 보고 분모(4·5·8)와 일치**한다. **PASS/FAIL 자체는 마스터 실행분 인용**이며 본 서브세션이
재확인한 사실이 아니다 — ARCHIVE_NOTE S5 와 addendum §0·M5 에 그렇게 구분해 적었다.

---

## 4. 가정 (질문 없이 채택한 기본값 — 전부 명시)

| # | 가정 | 근거·영향 |
|--:|---|---|
| G1 | 신규 md 2종의 줄바꿈 = **CRLF** | 주변 legacy md(`DATA_REGISTRY.md`·`REFLECT_SEED_TABLE.md`·`ARCHIVE_NOTE.md`) 전부 CRLF. 단 같은 폴더의 `V1025_DOC_CASCADE_TODO.md` 는 LF(Fable 세션 산출) — 리포에 두 관행이 공존한다. 필요 시 일괄 정규화는 마스터 판단 |
| G2 | 상단 주석 추가 위치 = 헤더 주석 블록의 **닫는 `% ====` 줄 바로 앞** | 기존 이력 주석 계열의 끝에 시간순으로 붙음. 기존 주석 줄 삭제·재배열 0 |
| G3 | 추가 주석은 **챕터별로 내용을 달리** 씀(브리프 예시문은 ch1 에 거의 그대로 사용) | 각 장에 실제 해당하는 v1.0.25 변경만 적어야 오해가 없음. ch2 = w_eff 조준·SI 상수 / ch3 = 비대칭 완화·regsol 삭제·Si 7-gallery (출처 = `V1025_DOC_CASCADE_TODO.md` T5·T6·T7·T11·T12) |
| G4 | 주석 안에서는 백슬래시 명령 대신 **`input 경로`·`externaldocument 키`** 로 표기 | LaTeX 주석이라 무해하지만, 후속 grep(`input{`·`externaldocument`) 이 주석을 실 코드로 오인 집계하는 것을 줄이려 함. §3.1 에서 그 3줄이 히트하는 이유를 명기 |
| G5 | ARCHIVE_NOTE 는 **표제·기존 40줄을 건드리지 않고** 하단에 추기 | 표제가 "v1.0.24.1 … 동결 아카이브" 라 v1.0.25 폴더에는 어긋나지만, "삭제하지 말고 정정을 덧붙여라" 지시가 표제 개정보다 우선. S1 첫 줄에 "위 본문은 v1.0.24.1 기준" 을 명시해 오독을 막음 |
| G6 | addendum 은 **comp_v24 안이 아니라 `docs/v1.0.25/results/`** 에 둔다 | 브리프 지정 경로. comp_v24 는 무수정 원칙 |
| G7 | A6 순위 역전을 **"조건 차이 실증"** 으로 서술(ABLATION 을 오류로 규정하지 않음) | 두 측정의 셀·기준 구성·점수가 다름을 직접 확인. ABLATION 자신의 정직 단서가 순위 변동을 예고했음 |
| G8 | 게이트 **미재실행** | 산출물 생성이 경계를 넘을 위험 + 브리프가 마스터 실행분으로 값 제공. 대신 정의 대조로 분모 검증 |

---

## 5. 미해결 (마스터·사용자 판단 필요)

| # | 항목 | 왜 여기서 못 닫았나 |
|--:|---|---|
| U1 | **LaTeX 빌드 3-pass 0-error·페이지 수** | TeX 배포판 부재(§3.4). 구조 검사 PASS 로 대체했을 뿐 **빌드 증빙이 아니다** |
| U2 | `eq:skewpeak` 라벨 정의 1회·참조 무결 확인(T14 지시의 Step 19) | 그 라벨은 `_sections/ch1_sec06_eqpeak.tex`(마스터 편집 중)에 신설된다 — §3.5 스냅샷 시점에는 검사 대상 아님. **마스터 편집 종료 후 구조 검사 재실행 필요** |
| U3 | ARCHIVE_NOTE **표제** 가 여전히 "v1.0.24.1 … 동결 아카이브" | 표제 개정은 삭제·개작이라 지시 범위 밖(G5). 폴더 지위 문서를 v1.0.25 명의로 새로 세울지 = 마스터 결정 |
| U4 | 마감문서 `V1025_CHANGE_LEDGER.md`·`HANDOVER_v25.md`·`MERGE_READINESS_v25.md`·`INDEX_v25.md` | T14 항목이지만 **본 브리프 범위 밖**(브리프는 3개 tex + ARCHIVE_NOTE 만 지정) — 미착수 |
| U5 | `sigr.csv`(블렌드)의 원자료 키·프로토콜 | **미측정**. A1 은 gr/si 만 확정 |
| U6 | 신규 CSV 8종의 리포 영구보존·`DATASETS` 편입 | 세션 스크래치에만 존재. `SOURCES.md` 의 "스크래치는 휘발" 교훈이 아직 미적용(addendum M2) |
| U7 | A2·A4·A5·A6·A7(1–3) 수치의 **재현 스크립트** 리포 등재 | comp_v24 의 `v24_*.py` 관행에 대응하는 v1.0.25 스크립트가 리포에 없음 → 현재 수치는 재현 경로 없이 인용 상태(addendum M3) |
| U8 | "흑연 물리 두-상 = **4** vs **2**" 표기 불일치 | `GRAPHITE_STAGING_XRD.md` §1 = 4 / §7·`FIT_CHECK` §추가 후보 = 2. v1.0.24 에서 후보 보고만 되고 미수정, v1.0.25 도 미해소. **물리 서술 판단이라 마스터 소관**(addendum M4) |
| U9 | 게이트 PASS/FAIL 독립 재확인 | 미재실행(G8·addendum M5) |
| U10 | @3 철회의 **다중 셀 통계** 확정 | ABLATION 정직 단서("@3 는 이 셀 하나")가 요구한 반복이 v1.0.25 에서도 미수행(addendum M6) |
| U11 | 리포 md 줄바꿈 관행 이원화(CRLF legacy vs LF 신규) | 정규화 여부 = 마스터 결정(G1) |
