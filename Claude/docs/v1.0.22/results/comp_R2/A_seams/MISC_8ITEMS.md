# MISC_8ITEMS — Step 14 이음매 8항 잔여 검토 (v1.0.22 R2 · O-A 초안)

> 지위: `comp_R2/A_seams/` 신규 초안. 마스터 소스 미수정. 권고·문안 제시(집행은 마스터).
> 근거: `plans/PLAN_R1_reorg.md` Step 14 의 8항.

## 0. Step 14 8항 상태 맵

| # | 항목 | 처리 위치 | 상태 |
|---|---|---|---|
| 1 | `ch2_sec00_intro` 장→파트 개작 | `A_seams/ch2_sec00_intro_partT.tex` | 초안 완료 |
| 2 | `ch2_sec10_closing` 장 마감→파트 마감 | `A_seams/ch2_sec10_closing_partT.tex` | 초안 완료 |
| 3 | `ch1v22_partT_divider` 다리 문단 확정 | **본 문서 §C** | 확정안(현행 유지+미세 옵션) |
| 4 | 서술형↔live 참조 전환 스윕(T1/T2/T3) | `A_seams/SEAM_PLAN.md`(78행) | 초안 완료 |
| 5 | `ch1_sec18_inputs` LCO 행 분리 검토 | **본 문서 §A** | 권고: 현행 유지 |
| 6 | `ch1_appB`·`ch2_appB` 코드맵 제목 분업 | **본 문서 §B** | 권고: Option 2(C/D 재번호) |
| 7 | `ch1_sec00_intro` 3챕터 안내 | R1/S-008 반영 완료(OK-S8) — 잔여 W 는 `A_seams/W_RULE.md` | W 처리로 이관 |
| 8 | 인용 다리 12곳(흑연분) | **O-B 소관**(본 O-A 범위 밖) | — |

---

## A. `ch1_sec18_inputs` LCO 행 지위 (권고: **현행 유지**)

**현황**: `tab:nodemap`(§18, 진행 요약 표)에 LCO 확장 행 N0$'$~N9$'$(54~60행)이 있고, 65행이 "여기까지가 본 장(흑연)의 결과 사슬이다 --- 표의 LCO 행(N$'$ 계열)은 Chapter 2 가 같은 forward 골격을 재사용하는 지점의 통합 대응 참조다" 로 프레이밍(= S-008 정정 결과, OK-S8).

**LCO 행이 참조하는 식**: `eq:lco-dUdT`·`eq:lco-dUhys`·`eq:lco-Ubranch`·`eq:dSemolar`·`eq:ggate`·`eq:lco-decomp` — 전부 신 Ch2(`ch1_sec12~17`)로 이동. `ch1_graphite` 의 `\externaldocument{ch2_lco_v1.0.22}` 가 이들을 forward xr("2.x")로 해소(설계4 의 전방 참조 22곳 중 일부).

**권고 = 현행 유지.** 근거:
1. 65행이 이미 LCO 행을 "Chapter 2 가 재사용하는 지점의 **통합 대응 참조**" 로 정확히 규정 — LCO 가 Ch1 소속이라 주장하지 않음(OK-S8). 스코프 오류 없음.
2. §18 은 "진행 요약"(facade) — 흑연 골격이 LCO 로 어떻게 확장되는지의 노드 지도를 한자리에 보이는 것이 "같은 골격, 추가 텀만" 이라는 재편 서사의 교육적 핵심. 분리하면 이 forward 지도가 끊긴다.
3. LCO 행의 `\eqref{eq:lco-*}` 는 xr 로 live 해소되므로 기술적으로 건재(집행 후 재빌드에서 `??` 잔존 0 확인이 게이트).

**분리(대안)의 조건**: 만약 사용자가 "Ch1 §18 은 순수 흑연 입력만" 을 원하면 → N0$'$~N9$'$ 행을 신 Ch2 의 대응 요약표로 이관하고, §18 에는 "LCO 확장은 Chapter 2 \S… 참조" 한 줄만 남김. 단 이는 재편 서사 약화·xr 재배선 부담이 있어 **권고하지 않음**. 최종 마스터 판단.

**주의(현행 유지 시)**: 65행 "Chapter 2 가" 는 설계 의도 지칭(OK-S8) — 전환 대상 아님. 유지.

---

## B. 코드맵 2본 제목 "곡선/열특성" 분업 (+ 4부록 letter 충돌)

### B.1 문제 — letter 충돌(실질 오도)

조립된 Chapter 1 의 부록 4본:

| 파일 | 선언 | 표시 | 라벨 | 내용 |
|---|---|---|---|---|
| `ch1_appA_signcheck` | `\appendix\section{…}` | 부록 A(자동번호) | `sec:signcheck` | 곡선 부호 사슬 검산 |
| `ch1_appB_codemap` | `\section{…}` | 부록 B(자동번호) | `sec:appendix-code` | 곡선 계산 구현 대응 |
| `ch2_appA_traps` | `\section*{부록 A --- …}` | **부록 A(하드코딩)** | **없음** | 열특성 기호·부호 함정 |
| `ch2_appB_codemap` | `\section*{부록 B --- …}` | **부록 B(하드코딩)** | **없음** | 열특성 코드 요구명세 |

→ **부록 A 두 번·부록 B 두 번**. `\section*`(비번호) 하드코딩이라 자동 C/D 로 밀려나지 않음. 게다가 프로세 참조가 오도:
- `ch2_sec04:22` "부록 A 함정표 참조"·`ch2_sec07:32` "부록 A 의 함정표" → 의도는 `ch2_appA`(열특성 함정표)이나 독자는 `ch1_appA`(곡선 부호검산)로 감.
- `ch2_sec04:96`·`ch2_sec08:95` "부록 B" → 의도는 `ch2_appB`(요구명세).
- `ch1_appB:135`(SEAM T1-02) "Chapter 2 부록 B" → `ch2_appB`, live 라벨 없어 전환 보류.

### B.2 Option 1 (최소 — 제목 분업만)

4 제목에 곡선/열특성만 명시, letter 유지:
- `ch1_appA`: `\section{부호 사슬 검산표}` → `\section{곡선 부호 사슬 검산표}`
- `ch1_appB`: `\section{구현 대응표}` → `\section{곡선 계산 구현 대응표}`
- `ch2_appA`: `\section*{부록 A --- 기호·부호 함정 검산표}` → `\section*{부록 A --- 열특성 기호·부호 함정 검산표}`
- `ch2_appB`: `\section*{부록 B --- 코드 구현 요구명세…}` → `\section*{부록 B --- 열특성 코드 구현 요구명세…}`

→ PLAN 14.6(곡선/열특성 분업)은 충족. **한계**: 부록 A/B letter 중복 잔존, T1-02 live 참조 여전히 불가.

### B.3 Option 2 (근본 — C/D 재번호 + 라벨 신설) — **권고**

열특성 부록을 부록 C/D 로 밀고 라벨 신설:

| 파일 | 개정 `\section*` 표시(+addcontentsline) | 신설 라벨(제안) |
|---|---|---|
| `ch1_appA` | `부호 사슬 검산표`(곡선; 유지 또는 "곡선 " 접두) | `sec:signcheck`(기존) |
| `ch1_appB` | `구현 대응표` → `곡선 계산 구현 대응표` | `sec:appendix-code`(기존) |
| `ch2_appA` | `부록 A --- 기호·부호 함정 검산표` → **`부록 C --- 열특성 기호·부호 함정 검산표`** | **`\label{sec:traps-thermal}`** |
| `ch2_appB` | `부록 B --- 코드 구현 요구명세…` → **`부록 D --- 열특성 코드 구현 요구명세(회귀 기준·하위호환)`** | **`\label{sec:codemap-thermal}`** |

**파급(재번호 시 동반 갱신 — 전수)**:

| 위치 | 현행 | 개정 |
|---|---|---|
| `ch2_sec04:22`(각주) | `(부록 A 함정표 참조)` | `(부록 C 함정표 참조)` 또는 `(부록~\ref{sec:traps-thermal} 함정표 참조)` |
| `ch2_sec07:32` | `부록 A 의 함정표가` | `부록 C 의 함정표가` |
| `ch2_sec04:96` | `부록 B가 명세한다` | `부록 D가 명세한다` |
| `ch2_sec08:95` | `대응은 부록 B).` | `대응은 부록 D).` 또는 `부록~\ref{sec:codemap-thermal})` |
| `ch1_appB:135`(SEAM T1-02) | `요구명세는 Chapter 2 부록 B)` | `요구명세는 부록~\ref{sec:codemap-thermal})`(부록 D) — **SEAM 판단 보류 #1 해소** |
| `ch1_sec18:66-67` | `부록 A 가 부호 사슬을…부록 B 가 구현과의…` | **무변경**(ch1_appA=A·ch1_appB=B 그대로) |

**권고 = Option 2**: (a) letter 충돌·프로세 오도를 근본 해소, (b) T1-02 를 live `\ref{sec:codemap-thermal}` 로 전환해 SEAM 보류 제거, (c) 곡선/열특성 분업 동시 달성. 비용 = 프로세 참조 5곳 + 라벨 2곳 신설(마스터 집행). Option 1 은 분업만 필요하고 letter 충돌을 감내할 때의 폴백.

**주의**: `ch2_appA/appB` 는 `\section*`(비번호)이므로 "부록 C/D" 는 자동번호가 아니라 표시 텍스트를 직접 바꾸는 것. addcontentsline 문자열도 동일하게 바꿔야 TOC 정합. 라벨은 `\section*` 다음 줄 `\label{...}` 로 부여(비번호 섹션이라 `\ref` 는 상위 절 번호를 잡으니, 필요 시 `\phantomsection` 선행 권고).

---

## C. `ch1v22_partT_divider` 다리 문단 확정안 (권고: **현행 유지 + 미세 옵션**)

**현행 다리 문단**(11~15행):
> 여기까지가 흑연 $\dd Q/\dd V$ 한 곡선을 그리는 계산 사슬이었다. 이제 같은 전극$\cdot$같은 입력에서 곡선 대신 \emph{열}을 뽑는다 --- 전이별 반응 엔트로피 $\Delta S_{\rxn,j}$ 가 어디서 오는지(배치$\cdot$진동$\cdot$전자 세 분포), 그리고 그것이 가역 발열 $\dot Q_\rev=-IT\,\partial U_\oc/\partial T$ 로 어떻게 조립되는지다. 앞 파트의 전하 보존 반전~\eqref{eq:sm-mc-balance}$\cdot$평형 종~\eqref{eq:eqpeak}$\cdot$폭 서식이 그대로 입력으로 들어온다.

**판정 = 확정(현행 유지).** 근거:
1. 지칭 정합 완비 — "앞 파트" 호칭이 본 O-A 규약(및 S-008 정정문 `ch2_appA:51`)과 일치. "Chapter" 구지칭 없음.
2. 라벨 실존 — `\eqref{eq:sm-mc-balance}`(`ch1_sec02b:343`)·`\eqref{eq:eqpeak}`(`ch1_sec06:28`) 둘 다 live. 같은 마스터 내 참조.
3. Part T 표제면의 다리로서 길이·어조 적정(교과서 파트 divider 관행).

**미세 옵션(선택 — 마스터 재량)**: "폭 서식" 이 유일하게 무참조 → live 참조 부여 가능:
> …$\cdot$평형 종~\eqref{eq:eqpeak}$\cdot$폭 서식(\S\ref{sec:width})이 그대로 입력으로 들어온다.

`sec:width`=`ch1_sec05:4` 실존. 논지 무변경, 참조 1개 추가일 뿐이라 넣어도 무방하나 필수는 아님.

**중복 점검**: `ch1_sec10:167`(Part I 말미)이 "이어지는 Part T 는 곡선 대신 열…" 을, `ch2_sec00_intro_partT`(서) 도입이 같은 취지를 서술 → divider 다리와 3중 근접. 파트 표제면의 짧은 재진술은 관행상 허용 범위(제거 불요). 단 divider 는 "한 문장 다리" 로 최단 유지가 좋아 현행 길이 적정.
