# SEAM_PLAN_R3 — 신 Ch2(LCO) 이음매 전환표 (v1.0.22 R3 · O-D 초안)

> 지위: `comp_R3/D_seams/` 신규 초안. 마스터 소스 미수정·git 무조작·`Codex/` 무접근.
> 대상 = 신 Chapter 2(LCO) 마스터 `ch2_lco_v1.0.22.tex` 의 \input 전량:
> `ch2v22_sec00_intro`·`ch2v22_notation`·`ch1_sec11~17`(lcointro/lcocenter/lcohys/lcodecomp/lcoelec/lcopeak/msmr)·`ch2v22_bib`.
> **명명 주의(P3-7)**: 파일명 `ch2_sec00~10*.tex` 는 신 Ch2 가 아니라 **신 Ch1 의 Part T(흑연 열특성, 구 Ch2 전량)** 다. 본 표의 xr 대상(Einstein·가역 발열·완전식)이 바로 그 Part T 이며, 신 Ch2 파일군과 구별한다.
> **현행 열 = 축자(verbatim) 인용** — R2 교훈 1(의역 매칭 불발). 아래 모든 "현행" 은 원문에서 복사, 라벨은 `ch1_graphite_v1.0.22.aux` 에서 실확인(추측 0).

---

## 0. 처분 구분과 xr 라벨 실확인

R3 이월 전환은 세 종류다.

| 종류 | 내용 | 처분 | 건수 |
|---|---|---|---|
| **W** | "본 문건" 어휘 스코프 명확화(장 단독 배포 유효, 병합 대비) | 어휘 치환(본 장/본서) — 라벨 무관 | 9 |
| **L1** | 신 Ch2 파일의 구 "Chapter 2"(열특성) 완전식 지칭 | xr 장 간 참조(→ Ch1 Part T live \eqref) | 1 |
| **N(신규)** | R1B 스윕 밖 — 축약형 `Ch2`(구 열특성 → Part T) 잔재 | xr 장 간 참조(→ Ch1 Part T live \S\ref) | 5 |

**xr 대상 라벨 실확인**(신 Ch2 는 `\externaldocument{ch1_graphite_v1.0.22}` 로 해소 — 아래는 `ch1_graphite_v1.0.22.aux` 의 `\newlabel` 실측):

| 라벨 | live 번호 | 정의 위치(Part T) | 용도 |
|---|---|---|---|
| `sec:einstein` | **§1.14** | ch2_sec04_einstein `\label{sec:einstein}` | Einstein 진동 보정 절 |
| `eq:complete` | **(1.125)** | ch2_sec08_synthesis `\label{eq:complete}` | 완전식(겹침 가중$+$config) |
| `sec:revheat` | **§1.17** | ch2_sec07_revheat `\label{sec:revheat}` | 가역 발열 절 |
| `sec:mixing` | **§1.15** | ch2_sec05_mixing `\label{sec:mixing}` | 섞임과 겹침(겹침 가중) 절 |
| `eq:qrev` | (1.124) | ch2_sec07_revheat | 가역 발열식(참고) |

`sec:einstein`=§1.14 라는 실측이 곧 축약형 "Ch2 \S2.4" 가 stale 임을 증명한다 — 그 절은 신 구조에서 신 Ch2 의 §2.4 가 아니라(신 Ch2 §2.4 = 본 삼분해 절 `sec:lco-decomp`) **신 Ch1 §1.14** 다.

---

## 1. W 9건 — 어휘 스코프 (W_RULE §2b 축자 확인판)

원칙(W_RULE 승계): 문장 논지·수식·자산 무변경, 조사만 정합. 기본값 **본 장**(장 스코프), 예외 **본서**(저작물 전체 스코프). 아래 현행은 원문 축자(grep 재확인). 신 Ch2 W 는 §제목·캡션·표 헤더에 걸리는 항 없음(전건 본문) — TOC/LoF/LoT 연동 무영향.

| # | 파일:행 | 현행(축자 인용) | 권고 개정 | 스코프 |
|---|---|---|---|---|
| W1 | `ch1_sec11_lcointro:27` | `본 문건이 다루는 범위는 \emph{코인 하프셀}(LCO vs Li metal) 단독이다` | `본 장이 다루는 범위는 \emph{코인 하프셀}(LCO vs Li metal) 단독이다` | 본 장 |
| W2 | `ch1_sec11_lcointro:37` | `주 진행 방향이다 --- 본 문건의` | `주 진행 방향이다 --- 본 장의` | 본 장 |
| W3 | `ch1_sec11_lcointro:45` | `등급 표기(본 문건 전역): tier A $=$ 1차 문헌의 정량 확정값` | `등급 표기(본서 전역): tier A $=$ 1차 문헌의 정량 확정값` | **본서**(§4 판정) |
| W4 | `ch1_sec12_lcocenter:93` | `\emph{LCO 단일전극}(vs Li) 값이고 본 문건(하프셀` | `\emph{LCO 단일전극}(vs Li) 값이고 본 장(하프셀` | 본 장 |
| W5 | `ch1_sec14_lcodecomp:90` | `본 문건이 추적하는 1차 문헌 공백은 셋이다` | `본 장이 추적하는 1차 문헌 공백은 셋이다` | 본 장 |
| W6 | `ch1_sec15_lcoelec:37` | `여기의 $U$ 와 $t$ 는 본 문건의 전극 전위 $U_j$ 와 별개인` | `여기의 $U$ 와 $t$ 는 본 장의 전극 전위 $U_j$ 와 별개인` | 본 장 |
| W7 | `ch1_sec15_lcoelec:125` | `갭 G2 --- 본 문건이 추적하는` | `갭 G2 --- 본 장이 추적하는` | 본 장 |
| W8 | `ch1_sec15_lcoelec:164` | `탈리튬화($x\!\downarrow$, 본 문건 LCO 충전 주 진행) 시` | `탈리튬화($x\!\downarrow$, 본 장 LCO 충전 주 진행) 시` | 본 장 |
| W9 | `ch1_sec17_msmr:19` | `무차원 폭 $\omega_j$ 를 본 문건은 $F/RT$ 를 폭에 흡수` | `무차원 폭 $\omega_j$ 를 본 장은 $F/RT$ 를 폭에 흡수` | 본 장 |

집계: 본 장 8 · **본서 1**(W3). 재현 선언·구조요소(§제목/캡션/헤더) 항은 신 Ch2 W 집합에 없음.

---

## 2. L1 1건 — 구 "Chapter 2" 완전식 지칭 → Ch1 Part T xr

`ch1_sec15_lcoelec:319`. 신 Ch2 한 점 시연에서 관측 계수를 평가하는 "완전식(겹침 가중$+$config)" 을 "Chapter 2 의 완전식" 으로 부르는데, 그 완전식은 구 열특성 장 = **신 Ch1 Part T** 의 `eq:complete`(=완전식, "겹침 가중(단순식)에 봉우리 내부 분포 config 를 더한" 식)다. 신 구조에서 자기 장 이름(Chapter 2)과 충돌 → live \eqref 로.

**현행(축자, 317–319행):**
```
\textbf{(b) 전하 보존 반전과 관측 계수.} 고정 $\bar x$ 에서 전하 보존
음함수~\eqref{eq:sm-mc-balance} 를 풀어 $U_\mathrm{oc}$ 를 얻고, 그 근에서 완전식(겹침 가중$+$config;
Chapter 2 의 완전식과 같은 구조)으로 $\partial U_\mathrm{oc}/\partial T$ 를 평가하면:
```
**전환 토큰:** `Chapter 2 의 완전식과 같은 구조)`
**권고 개정:** `Chapter 1 Part T 의 완전식~\eqref{eq:complete} 와 같은 구조)`
**라벨:** `eq:complete` → (1.125), Part T `sec:synthesis`(§1.18) 내 — 실확인.
**근거:** 시연 완전식은 "겹침 가중$+$config" 로, `eq:complete`("겹침 가중$+$봉우리 내부 config")와 문면·구조가 동일. `eq:sm-mc-balance`(전하 보존 반전)는 이미 신 Ch2 에서 live xr 로 인용 중(계승 정합).

---

## 3. 신규 전수 재스윕 — R1B 밖 5건(축약형 `Ch2` stale) + 정당 지칭

R1B 스윕 패턴은 `Chapter[~\s]*[12]|그 문건|별도 컴파일|본 문건|이 문건` 으로 **축약형 `Ch1`·`Ch2` 를 포함하지 않았다**. 브리핑 확장 패턴(`…|Ch1|Ch2`)으로 신 Ch2 \input 전량을 재스윕(주석 행 제외)한 결과, R1B 밖 축약형 잔재가 검출된다.

### 3a. 전환 대상 — 축약형 `Ch2`(구 열특성 → Part T), 5건

전건 stale: 축약형 "Ch2" 가 구 v1.0.21 의 열특성 "Chapter 2" 를 뜻하나, 그 내용은 신 구조에서 **Ch1 Part T** 다(Einstein·가역 발열·겹침 가중 — 신 Ch2 에는 없는 절). L1 과 동종의 장 간 xr 전환 대상.

| # | 파일:행 | 현행(축자 인용) | 전환 토큰 | 권고 개정 | 라벨(실측) |
|---|---|---|---|---|---|
| N1 | `ch1_sec14_lcodecomp:47` | `T\text{-의존 Einstein 보정 --- Ch2 \S2.4 Einstein 절}` | `Ch2 \S2.4 Einstein 절` | `T\text{-의존 Einstein 보정 --- Chapter 1 Part T Einstein 절 \S\ref{sec:einstein}}` | sec:einstein→§1.14 |
| N2 | `ch1_sec14_lcodecomp:54` | `그 유도는 Ch2 \S2.4 Einstein 절), elec 는` | `Ch2 \S2.4 Einstein 절` | `그 유도는 Chapter 1 Part T Einstein 절 \S\ref{sec:einstein}), elec 는` | sec:einstein→§1.14 |
| N3 | `ch1_sec15_lcoelec:176` | `이 $T$ 의존을 보이며, Ch2 의 가역\n발열로 확장할 때 중요하다.` | `Ch2 의 가역 발열로 확장할 때` | `이 $T$ 의존을 보이며, Chapter 1 Part T 의 가역 발열(\S\ref{sec:revheat})로 확장할 때 중요하다.` | sec:revheat→§1.17 |
| N4 | `ch1_sec15_lcoelec:193` | `모델링한다(Ch2 Einstein 절 --- 강제 $T_\mathrm{ref}$ 영점` | `(Ch2 Einstein 절 ---` | `모델링한다(Chapter 1 Part T Einstein 절 \S\ref{sec:einstein} --- 강제 $T_\mathrm{ref}$ 영점` | sec:einstein→§1.14 |
| N5 | `ch1_sec15_lcoelec:237` | `$\partial U_j/\partial T$ 를 주어 Ch2 의 겹침 가중과 일관되고,` | `Ch2 의 겹침 가중과 일관되고` | `$\partial U_j/\partial T$ 를 주어 Chapter 1 Part T 의 겹침 가중(\S\ref{sec:mixing})과 일관되고,` | sec:mixing→§1.15 |

주의(집행 시):
- **N1 은 수식 내부**(`eq:lco-slots` 의 `\text{}`). `\S\ref` 는 텍스트 모드(`\text{}` 안)에서 안전하나, 개정 후 3-pass 재빌드로 슬롯 정렬·박스 폭 무붕괴 확인.
- N3 은 176–177 행에 걸침("Ch2 의 가역"→"발열"). 개정 시 줄바꿈 위치는 마스터 재량(문면 무변경).
- N2·N4 는 기존 닫는 괄호 유지 — `\S\ref` 에 중복 괄호 붙이지 말 것(위 개정안대로).
- 조사·괄호 스타일(예 "절(\S\ref…)" vs "절 \S\ref…")은 마스터 재량. 논지·수식·라벨 대상은 위 고정.

### 3b. 정당 지칭 — 대상 정상(전환 불요), 12건

축약형 `Ch1`·정식 "Chapter 1"·"Chapter 1 Part T" 지칭으로, **대상이 신 구조에서 정확**(흑연=Ch1, 열특성=Ch1 Part T). 전환 불요. 축약형 `Ch1`(8건)은 표기 정규화 후보로 §5 에 별기(선택·비강제).

| 파일:행 | 현행 핵심 | 지칭 대상 | 판정 |
|---|---|---|---|
| `ch1_sec11_lcointro:166` | `Part II 종반에서 Ch1 곡선 클래스와 1:1 대응표` | Ch1(흑연) | 정당(축약형) |
| `ch1_sec14_lcodecomp:57` | `흑연 장의 열특성 파트(Chapter 1 Part T)가 같은 기호` | Ch1 Part T | 정당(S-008 ⑤ 결과) |
| `ch1_sec14_lcodecomp:70` | `기존 Ch1 logistic 이 … peak 내부 항을 자동 생성` | Ch1(흑연) | 정당(축약형) |
| `ch1_sec14_lcodecomp:79` | `phonon 음의 baseline 으로 Ch1 흑연과 동형이며` | Ch1(흑연) | 정당(축약형) |
| `ch1_sec17_msmr:33` | `Ch1 logistic 서식은 여집합에 대해 닫혀 있다` | Ch1(흑연) | 정당(축약형) |
| `ch1_sec17_msmr:42` | `MSMR 점유율 … 는 Ch1 의 점유 $\theta_{\eq,j}$ 와` | Ch1(흑연) | 정당(축약형) |
| `ch1_sec17_msmr:43` | `여집합 … 는 Ch1 의 진행률 $\xi_{\eq,j}$(식~\eqref{eq:xieq})와` | Ch1(흑연) | 정당(축약형) |
| `ch1_sec17_msmr:62` | `MSMR 종별 미분용량과 Ch1 평형 peak 은 같은 식이다` | Ch1(흑연) | 정당(축약형) |
| `ch1_sec17_msmr:73` | `따라서 Ch1 의 곡선 골격 … 은 구조 변경 없이 LCO 에 적용` | Ch1(흑연) | 정당(축약형) |
| `ch2v22_sec00_intro:4` | `본 장은 Chapter 1 이 흑연에서 세운 골격을 …` | Ch1(흑연) | 정당(OK-NEW) |
| `ch2v22_sec00_intro:6` | `… 은 Chapter 1 의 식 번호를 그대로 인용하며` | Ch1(흑연) | 정당(OK-NEW) |
| `ch2v22_notation:6` | `\textbf{계승}(Chapter 1 정의 그대로 --- 재정의 없음)` | Ch1(흑연) | 정당(OK-NEW) |

(주석 행 hit 3건 — `ch2v22_bib:2`·`ch2v22_sec00_intro:2`·`ch2v22_notation:2,3` — 은 스윕 규약대로 제외.)

---

## 4. W3 판정 — "본 문건 전역" → **본서** (3장 공통 규약 확인)

W_RULE §2b 가 본서 후보로 표류시킨 `ch1_sec11:45`(tier 등급 정의). 판정 근거(실측):
1. tier A/B/C **정의는 신 Ch2 `ch1_sec11:45` 한 곳에서만** 이뤄진다("등급 표기(본 문건 전역): tier A=…, B=…, C=…").
2. **신 Ch1(흑연)이 이 정의를 역참조**한다 — `ch1_sec07_broadening:64`: "tier C 추정이며(신뢰 등급 범례는 \S\ref{sec:lco-map} 각주)". `sec:lco-map` 은 `ch1_sec11:11`(신 Ch2)의 라벨이므로, Ch1→Ch2 xr 로 tier 범례를 끌어 쓴다.
3. tier 표기는 신 Ch1(`ch1_sec01:91,245,247`·`ch1_sec07:64,257,269,285`)·신 Ch2 양쪽에서 사용된다.

∴ tier 등급은 **저작물 전체(3장+코드) 공통 규약**이고, 그 "전역" 스코프는 병합 문건 전체를 가리킨다 → **본서 전역** 이 정확(본 장 아님). W_RULE 본서 후보 확정.

부수 관찰(판단 보류 §6-c): 책 전역 규약(tier 범례)이 **Chapter 2 안에서 정의되고 Chapter 1 이 역참조**하는 구조는 정합하나(xr 로 해소), 규약의 자연 위치는 아니다 — 향후 공통 서두/부록 이설 후보(구조 재편이라 본 R3 범위 밖·미집행).

---

## 5. 축약형 `Ch1` 표기 정규화 — 선택(비강제)

§3b 의 축약형 `Ch1` 8건은 **대상이 정상**이라 전환 대상이 아니다. 다만 신 Ch2 는 `ch2v22_sec00_intro`·`ch2v22_notation` 및 다수 본문에서 정식 "Chapter 1" 을 쓰므로, 축약형 `Ch1` 은 병합 문건에서 표기 불일치다(오독은 아님 — `Ch1`≡Chapter 1 로 일의적).

- 권고(선택): `Ch1` → `Chapter 1`(조사 정합만; 논지·수식·라벨 무변경). 예 `ch1_sec17:73` `따라서 Ch1 의 곡선 골격` → `따라서 Chapter 1 의 곡선 골격`.
- **P5(이름·표현 보존)·게이트("무변경") 준수**를 위해 **강제하지 않고 마스터 결정에 위임**. W(어휘 스코프 뭉갬)·L1/N(대상 stale)과 달리 정규화는 정합성 개선일 뿐 정정이 아니다.
- 일괄 대상: `ch1_sec11:166`·`ch1_sec14:70,79`·`ch1_sec17:33,42,43,62,73`(8건).

---

## 6. 통계·판단 보류

### 건수 통계

| 구분 | 건수 | 세부 |
|---|---|---|
| **전환 대상** | **15** | W 9(본 장 8·본서 1) + L1 1(→eq:complete) + 신규 Ch2-stale 5(→sec:einstein×3·sec:revheat 1·sec:mixing 1) |
| **정당 지칭** | **12** | 축약형 Ch1 8 + Chapter 1/Part T 정식 4(OK-S8 1·OK-NEW 3) |
| **정상(비지칭)** | **0** | 스윕 hit 전건이 장 지칭류 |
| 재스윕 본문 hit 계 | **27** | (주석 행 3 별도 제외) |

라벨 실확인: 전환 대상 xr 6종(eq:complete·sec:einstein·sec:revheat·sec:mixing + 참고 eq:qrev) 전건 `ch1_graphite_v1.0.22.aux` `\newlabel` 실측(추측 0).

### 판단 보류

- **(a) W3 본서 스코프**: §4 근거로 "본서" 확정 권고이나, 최종은 마스터 판단(브리핑 "본서 후보 → R3 판정"). Ch1→Ch2 역참조(`ch1_sec07:64`)라는 실증 제시.
- **(b) 축약형 `Ch1` 정규화(§5)**: 대상 정상이라 전환 불요. 정규화 실행/보류는 마스터 결정(P5 보존 원칙상 O-D 는 미집행·권고만).
- **(c) tier 범례 위치(§4 부수)**: 책 전역 규약이 Ch2 내 정의 — 구조 재편 후보이나 본 R3 범위 밖.
- **(d) N1 수식 내 \S\ref**: `\text{}` 내부 삽입은 문법상 안전하나, 집행 후 `eq:lco-slots` 슬롯 정렬 3-pass 재확인을 게이트로.
- **(e) 조사·괄호 미세 문체**: N3~N5·L1 의 "절(\S\ref…)"/"절 \S\ref…" 등은 마스터 재량(대상 라벨·논지 고정, 문체만 위임).

### 집행 후 게이트(권고)
동일 확장 패턴(`Chapter[~\s]*[12]|그 문건|본 문건|이 문건|별도 컴파일|Ch1|Ch2`) 재스윕 → 잔존이 §3b 정당 지칭(+ 정규화 미집행 시 축약형 Ch1)만이면 PASS. Ch1→Ch2 3-pass 재빌드로 xr 6종 live 해소(?? 무잔존) 확인.
