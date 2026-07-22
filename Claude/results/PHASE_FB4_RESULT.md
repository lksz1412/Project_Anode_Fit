# Phase FB4 — F-02 확률/압력 P 충돌 + F-03 식1.21 f 명료화 + F-05 잔여 제목 N-태그 Result

## Summary
§1.2.1 기호 충돌·명료화. **F-02**: 식1.6(eq:sm-fund)의 압력 $P$ 와 식1.7(eq:sm-resv)의 확률 $P_i$ 가 인접식에서 같은 대문자 P → 확률을 **소문자 $p$** 로 개명(압력 $P$ 유지). **F-03**: 식1.21(eq:sm-sint)의 자리당 내부 자유에너지 $f_\mathrm{int}$ 를 계 전체 Helmholtz $F$ 로 오독 방지 가드 추가. **F-05**: Step15가 놓친 제목 N-태그 2건 제거. 식번호·`\label`·물리 불변.

## Step Range
cumulative **FB step 25–28**.

## Inputs
- `_sections/ch1_sec02a_part0.tex`(§1.2.1 sec:sm-ensemble·sec:sm-site 소절; 식1.6/1.7/1.21 소재).
- `_sections/ch1_sec01_n0n1.tex`(제목 N0·N1 잔여).
- 매핑 근거: `ch1_graphite_v1.0.24.aux`(식1.6=eq:sm-fund·1.7=eq:sm-resv·1.21=eq:sm-sint·§1.2.1=sec:sm-ensemble 확정).
- 게이트: V1020 B5(기호 충돌=각주 가드 우선)·F1(식번호·label 불변).

## Files Created
- 없음.

## Files Updated
- `ch1_sec02a_part0.tex`:
  - **F-02** 확률 $P_i{\to}p_i$·$P_0{\to}p_0$·$P_1{\to}p_1$(11곳). 압력 $P$(식~eq:sm-fund $-P\dd V$·$\mu{=}\partial G/\partial n|_{T,P}$) 불변.
  - **F-03** 식1.21 도입부: "내부 자유도의 \emph{자리당} 자유에너지 $f_\mathrm{int}$(소문자 $f$ --- 계 전체 Helmholtz $F{=}-k_BT\ln Z$ 가 아니라 자리당 양)" 가드 삽입.
- `ch1_sec01_n0n1.tex`: **F-05** 소절 제목 N-태그 제거 2건(`실험조건 매핑과 방향 부호 --- $\mathrm N0$`→`실험조건 매핑과 방향 부호`·`분극 --- 측정 전위에서 내부 전위로 ($\mathrm N1$)`→`분극 --- 측정 전위에서 내부 전위로`). `\label`(sec:n0map·sec:pol) 불변.

## Read Coverage
- 전문 정독: ch1_sec02a_part0 §1.2.1 전개(식1.5–1.8·1.20–1.22 문맥)·ch1_sec01_n0n1 제목.
- grep 전수: 확률 $P$ 소재(단일 파일 ch1_sec02a 한정 확인)·압력 $P$·$f_\mathrm{int}$/$f_k$(자리당·모드당 소문자 f 규약 확인 = ch2_sec01·ch2_sec03)·Part T 확률 소문자 $p$ 규약(ch2_sec00:36/50·ch2_sec02:15) 확인·제목 N-태그 전수.

## Execution Evidence
```
F-02 검증: p_i/p_0/p_1 = 11 · 잔여 P_i/P_0/P_1 = 0 · 압력 P(식30/32/70) 불변
근거: 확률 P 단일 파일(ch1_sec02a) 국한 → 개명 무-교차영향. Part T 는 이미 소문자 p(−R∑p ln p) → 개명이 Part0↔PartT 정합↑
F-03: f_int 가드 삽입(자리당 vs Helmholtz F 구분) — f_int/f_k 소문자=자리당·모드당 규약 확정
F-05: 제목 N-태그 잔여 = 0(전수 grep)
빌드(3챕터): ch1 0-err/98p · ch2 0-err/30p · ch3 0-err/21p · undefined ref/cite 0
invariant: \label 키·\eqref/\ref/\cite 키 변경 0 · 식번호(식1.6/1.7/1.21) 불변(기호 개명은 식번호 무관)
```

## Validation (게이트별)
- **F-02 충돌 해소** — PASS(확률→p·압력 P 유지; 대문자 중복 소거). B5(각주 가드 우선) **의도적 divergence**: 확률 P가 단일 파일 국한 + Part T가 이미 소문자 p → 개명이 정합 증가(가드보다 우월). 1회 flag.
- **F-03 명료화** — PASS(자리당 vs 계 Helmholtz 가드; 문서 기존 F/Faraday 가드 패턴과 정합).
- **F-05 제목 N-태그** — PASS(잔여 0).
- **빌드 GREEN** — PASS(98/30/21·undefined ref/cite 0).
- **F1 식번호·label 불변** — PASS(개명은 식번호·label 무영향; invariant 확인).

## Gate
**PASS_FB4_NOTATION** (P/p·f 명료화 + 제목 N-태그 소거 + 빌드 GREEN + label/식번호 불변).

## Confirmed Non-Changes
- 코드 `.py` 무변경(sha256 f230f59b). 식번호·`\label`·`\eqref/\ref/\cite` 키·`%` 주석 불변.
- 압력 $P$·Helmholtz/Faraday $F$·자리당 $f_\mathrm{int}$/$f_k$ 규약 유지(F-02는 확률만 개명).

## 비고 (거버넌스)
- **B5 divergence 기록**: 본 프로젝트 rubric B5 = "기호 충돌은 각주 가드(개명 아님)". F-02는 **개명**(확률 $P{\to}p$) 채택. 근거 = (1) 사용자 F-02 직접 지목(임의변경 아님) (2) 확률 P 단일 파일 국한(교차영향 0) (3) Part T 소문자 $p$ 기존 사용 → 개명이 문서 내 정합 증가. F(Helmholtz/Faraday)처럼 다-파일·양방 표준이라 개명 불가한 경우와 상황 상이 → 가드 유지. 방법론(개명 가능 시 개명·불가 시 가드)은 일관.
