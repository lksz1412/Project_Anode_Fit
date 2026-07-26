# V1025_DOC_CASCADE_TODO — 문건(P2·P3) 연계 편집 체크리스트

> 작성: Fable 서브세션(2026-07-26). 코드+게이트(P0·P1)는 완결·전건 GREEN — 본 문서는 계획서
> P2(Step 13–20)·P3(Step 21–27)의 **LaTeX 편집을 파일·라벨·수정문 단위로 지시**하는 체크리스트다.
> 원칙(계획서 D-D): 기존 식 번호·`\label`·`\eqref/\ref` 키·변수명·한글 표현 불변. **추가만(additive)**,
> boxed 식 삭제 금지. 각 항 "원문 → 수정문" 초안 포함(집행자는 재빌드 3-pass 0-err 확인).
> 라인 번호는 `docs/v1.0.24.1/_sections/`(=v1.0.25 복제본 동일) 기준.

---

## T1. §5(sec:eqpeak) skew peak boxed 식 신설 — `eq:skewpeak` (계획서 Step 13, C1 cascade)

- **파일**: `_sections/ch1_sec06_eqpeak.tex`
- **위치**: `\label{eq:eqpeak}` 식 블록(line ~28)과 그 직후 문단("이 값이 전이별로 합산되어…") **사이**에 신규 소단락 삽입. 기존 `eq:eqpeak` 은 한 글자도 수정하지 않는다.
- **수정문(신규 삽입 초안)**:

```latex
\paragraph*{선택 확장 --- skew-logistic 비대칭 종(opt-in).}\label{par:skewpeak}
평형 진행률의 재모수화 $\xi_\eq=\sigma^{\alpha_j}$($\sigma=$ 식~\eqref{eq:xieq} 의 logistic,
$\alpha_j>0$)를 허용하면 전이 $j$ 의 평형 peak 이 다음의 비대칭 종으로 일반화된다:
\begin{equation}
\boxed{\;\Big(\frac{\dd Q}{\dd V}\Big)^\eq_j
=Q_j\,\frac{\alpha_j}{w_j}\,\sigma^{\alpha_j}\,(1-\sigma)\;,\qquad \xi_{\eq,j}=\sigma^{\alpha_j}\;.}
\label{eq:skewpeak}
\end{equation}
$\alpha_j=1$ 이면 $\sigma^{1}(1-\sigma)/w_j=\xi_\eq(1-\xi_\eq)/w_j$ 로 식~\eqref{eq:eqpeak} 를
\emph{정확히 회수}하고(코드도 이 경로가 bit-exact --- 부록 B), $\int_0^1\dd\xi_\eq=1$ 이라 면적
$Q_j$ 는 $\alpha_j$ 에 무관하게 보존되며 종은 $C^\infty$ 다. $\alpha_j$ 는 전류$\cdot$과전압과
무관한 \emph{평형} 형상 파라미터(현상학적$\cdot$tier C --- 새 물리$\cdot$새 상이 아님)로,
물리적 동기는 order--disorder 엔트로피 스텝$\cdot$조성 의존 $\Omega(x)$ 류의 조성 비대칭이다.
$\xi_\eq=\sigma^{\alpha}$ 는 여전히 단조 $0\!\to\!1$ 이라 \S\ref{sec:lag}--\S\ref{sec:tail} 의
인과 꼬리$\cdot$전하 보존 반전(식~\eqref{eq:implicit})이 그대로 성립한다. 기본값은 $\alpha_j=1$
(부재 시 현행과 동일 --- opt-in)이다.
```

- **연계**: `\S\ref{sec:width-w}`(ch1_sec05_width.tex:264 이하) 폭 이중지위 서술 끝에 1문장 병기 — "폭 $w_j$ 와 별개로 형상 지수 $\alpha_j$(식~\eqref{eq:skewpeak}, opt-in)가 좌우 비대칭을 담당한다(면적$\cdot$중심 정의 불변)."

## T2. §7(sec:broadening-sources) 에 α 축 추가 + ①과 구분 (Step 14, C1 cascade)

- **파일**: `_sections/ch1_sec07_broadening.tex`
- **위치**: line 40 `\emph{① 유한율속 비대칭 꼬리(동역학 몫).}` 문단 **끝**(…Fly 등\cite{fly2020}). 다음)에 이어 삽입(세 출처 열거 ①②③ 번호는 불변 — α 는 "추가 축"으로 별도 문단):
- **수정문(신규 삽입 초안)**:

```latex
\emph{(추가 축) 평형 비대칭 $\alpha_j$ --- ① 과의 구분.} v1.0.25 부터 선택 확장으로 평형 종
자체의 비대칭 $\alpha_j$(식~\eqref{eq:skewpeak}, opt-in)를 둘 수 있다. ① 의 비대칭 꼬리는
\emph{전류가 켜야} 생기고 $|I|\to0$ 에서 소멸($L_V\propto|I|$)하는 반면, $\alpha_j$ 는 전류$\cdot$
$\eta$ 와 무관한 \emph{평형 잔여} 비대칭이라 $|I|\to0$ 에서도 남는다 --- 두 몫을 같은 곡선에서
동시에 자유화하면 이중계산(축퇴)이 된다(\S\ref{sec:inputs} 가드). 분리는 율속 스윕만이 가른다
(① 만 $|I|$ 에 비례). ②$\otimes$③ 의 합성이 전제한 좌우 대칭은 $\alpha_j\ne1$ 에서 완화된다.
```

## T3. §18(sec:inputs) α↔L_V 식별 축퇴 가드 (Step 16, C1 cascade)

- **파일**: `_sections/ch1_sec18_inputs.tex` (`\label{sec:inputs}`, line 4 절 내 피팅 지침부)
- **수정문(신규 삽입 초안)**:

```latex
\emph{식별 가드($\alpha$--$L_V$--gallery 축퇴).} 정적 단일 온도 곡선에서 봉우리 비대칭은
$\alpha_j$(평형 skew, 식~\eqref{eq:skewpeak})$\cdot$$L_{V,j}$(유한율속 꼬리)$\cdot$gallery 세분
(폭 다른 종의 envelope) 세 손잡이가 서로 축퇴한다 --- 셋을 동시에 자유화하지 말 것.
권장: $\alpha$ 만 열 때는 $L_V$ 동결(코드는 같은 전이에 alpha$\ne$1 과 L\_V$>$0 동시 지정 시
경고를 낸다 --- G-$\alpha$4), gallery 세분과 $\alpha$ 의 동시 자유화 지양. 셋 중 ① 몫만 율속
스윕($\propto|I|$$\cdot$$|I|\to0$ 소멸)으로 분리 식별된다.
```

## T4. §5b:53–55 "$w_\mathrm{eff}\to0$ 델타 수렴/연속화" 정정 (Step 17 전반, C5/E)

- **파일**: `_sections/ch1_sec05b_gr2L.tex` lines 53–55
- **원문**:
  > 단일상($\Omega<2RT$) peak 의 유효 폭은 $w_\mathrm{eff}=(RT/F)(1-\Omega/2RT)$ 라(판정자~\eqref{eq:gr2l-disc} 의 $\theta{=}\tfrac12$ 강성에 반비례), $\Omega\!\to\!2RT$ 에서 $w_\mathrm{eff}\!\to\!0$ 으로 좁아져 두-상 델타로 수렴한다 --- 폭식~\eqref{eq:wbase} 의 이중지위가 이 한 식으로 연속화된다.
- **수정문(교체 초안)** (검수 E: FWHM 은 $\lambda\equiv1-\Omega/2RT$ 가 아니라 $\lambda^{3/2}$ 스케일 — 수치 확인, 최대 30배 과대; peak 높이 $1/(4w_\mathrm{eff})$ 는 정확. 코드의 binodal 불연속 전환과 "연속화" 서술 상충):
  > 단일상($\Omega<2RT$) peak 의 \emph{중심 높이}는 $w_\mathrm{eff}=(RT/F)(1-\Omega/2RT)$ 로 정확히 $1/(4w_\mathrm{eff})$ 스케일이다(판정자~\eqref{eq:gr2l-disc} 의 $\theta{=}\tfrac12$ 강성에 반비례). 다만 이 $w_\mathrm{eff}$ 를 \emph{반높이 폭}으로 읽으면 안 된다 --- $\lambda\equiv1-\Omega/2RT\to0$ 에서 FWHM 은 $\lambda$ 가 아니라 $\lambda^{3/2}$ 로 닫혀($\theta$ 4차항 지배; 수치 확인, $\lambda$ 읽기는 최대 $\sim$30배 과대) 높이와 폭의 스케일이 갈린다. 곧 이 식은 두-상 극한으로의 \emph{연속 보간이 아니라} 단일상 쪽 중심 높이의 국소 지표이며, 두-상($\Omega>2RT$)의 유한 폭은 \S\ref{sec:broadening} 대로 현상학적 피팅이 정한다.
- **금지어 등록**: "이 한 식으로 연속화" 표현 재사용 금지(G-금지 grep 표).

## T5. Ch2 파생 C warnbox — "$w_\eff(\Omega)$ 금지" 를 두-상 한정으로 (Step 17 후반, C5)

- **파일**: `_sections/ch2_sec05_mixing.tex` warnbox lines 187–194
- **원문(핵심부)**:
  > "…본 장은 그런 유효-폭 축소식($w_\eff(\Omega)=w(1-\Omega/2RT)$ 류)을 쓰지 않는다(재도입 금지)."
- **수정문(교체 초안)** — 금지를 **두-상 폭**에 한정해 §5(sec:width-w)·§5b(위 T4 수정문)·Ch3 단상 해석과 공존시킨다:
  > "…\emph{두-상 봉우리의 폭}에 그런 유효-폭 축소식($w_\eff(\Omega)=w(1-\Omega/2RT)$ 류)을 쓰지 않는다(두-상 폭 한정 재도입 금지). \emph{단상}($\Omega<2RT$) 영역에서 같은 식이 중심 \emph{높이} $1/(4w_\eff)$ 의 국소 지표로 쓰이는 것(\S 5b, Ch3 \S 3.2b)은 별개다 --- 그 경우에도 FWHM 은 $\lambda^{3/2}$ 스케일이라 폭 읽기는 불가하다."
- **주의**: line 232 주석 `[C-2] ★v5 정정 구 w_eff(Ω) narrowing 식 완전 제거(재도입 금지)` 자산 행에 "(v1.0.25: 두-상 한정으로 조준 좁힘 — 단상 높이 지표는 허용)" 병기.

## T6. Ch3 §3.2b "비대칭=envelope 전용" 완화 (Step 15, C1 cascade)

- **파일**: `_sections/ch3v22_sec02b_sifr.tex` — **두 곳**(lines ~93–96, ~125–128) + 헤더 주석 line 12
- **원문 1(95)**: "…\emph{대칭}이라 그 자체로는 비대칭이 될 수 없고, 케이스별 개형의 \emph{비대칭}은 오직 폭이 다른 여러 종의 envelope 에서만 온다"
- **수정문 1**: "…\emph{대칭}이라 그 자체로는 비대칭이 될 수 없고, 케이스별 개형의 \emph{비대칭}은 폭이 다른 여러 종의 envelope \emph{또는} 단일 종의 skew 지수 $\alpha_j$(Ch1 식~\eqref{eq:skewpeak}, opt-in --- envelope 의 파라미터 효율 대안)에서 온다. 어느 쪽도 새 상(phase)이 아니며, 둘은 상호 대안이라 동시 자유화 시 축퇴한다(Ch1 \S 18 가드)"
- **원문 2(127)**: "그 자체로는 결코 비대칭이 아니며, 케이스별 개형의 \emph{비대칭}은 오직 폭이 다른 여러 종의 포갬(envelope)에서만 온다"
- **수정문 2**: "그 자체로는 결코 비대칭이 아니며, 케이스별 개형의 \emph{비대칭}은 폭이 다른 여러 종의 포갬(envelope) 또는 skew 지수 $\alpha_j$(Ch1 식~\eqref{eq:skewpeak} --- 상호 대안, 동시 자유화 지양)에서 온다"
- **주의**: line 12 헤더 주석("단일 종이 비대칭이라는 문장 제거·차단")에 "(v1.0.25: α opt-in 도입으로 '오직 envelope' 단정은 완화 — 본문 두 곳 수정)" 병기. cross-ref `eq:skewpeak` 는 Ch1 외부참조(xr) 키 확인.

## T7. Ch3 sifr(regsol) — **코드 삭제** 반영, 해석적 기록만 (Step 21, C6) ★사용자 결정으로 갱신

> **갱신(2026-07-26, 사용자 결정 "regsol 삭제")**: 계획서 DG-1 은 (a) 강등이 아니라 **(b) 삭제**로
> 확정되었다. 코드에서 `_REGSOL_XG`·`_regsol_binodal_xa`·`_regsol_dqdv`·`equilibrium` 의
> `'kernel'` 분기가 **전부 제거**되었고, reflect 게이트 G-R3 은 "삭제 확인"(심볼 부재 + `'kernel'`
> 키가 남은 legacy dict 이 로지스틱과 `array_equal`) 게이트로 대체되었다. 따라서 아래 warnbox 는
> "코드 경로 존치" 가 아니라 **"코드 미구현·해석적 기록"** 으로 써야 한다.

- **파일**: `_sections/ch3v22_sec02b_sifr.tex` — `\label{eq:sifr-kernel}`(61)·`\label{eq:sifr-blend}`(108) **식·라벨은 불변**(문건 자산 삭제 금지 — 해석적 유도는 그대로 유효한 물리다), 절 도입부에 지위 warnbox 1개 삽입.
- **수정문(절 도입부 삽입 초안)**:

```latex
\begin{warnbox}
\textbf{지위(v1.0.25): 해석적 기록 --- 미채택$\cdot$코드 미구현.} 본 절의 Frumkin/정칙용액 커널
(식~\eqref{eq:sifr-kernel}$\cdot$\eqref{eq:sifr-blend})은 유도 자체가 유효한 통계열역학이지만,
v1.0.25 실측 재검증에서 \emph{채택 경로에서 제외}되고 구현 코드가 \emph{삭제}되었다: 전이 수
고정(흑연4+Si3) 조건의 이득 $+0.97$\,\%p 가 전이 수 승격(흑연7+Si7 gallery) 시 $-0.53$\,\%p 로
역전되기 때문이다 --- 이득의 실체는 전이 수 부족의 우회였고, gallery 세분과 중복이며 gallery 가
같은 개형을 더 적은 가정으로 설명한다. 그러므로 v1.0.25 커널 계통은 \emph{로지스틱 단일계}이며,
비대칭은 skew 지수 $\alpha_j$(Ch1 식~\eqref{eq:skewpeak})와 gallery envelope 이 담당한다.
$\Omega$ 파라미터 자체의 지위는 \emph{불변}이다 --- 히스테리시스 gap$\cdot$$\Delta H_a^\eff$
$\cdot$\S 7 상성격 판정($\Omega/RT\gtrless2$)에 계속 쓰인다(삭제된 것은 dQ/dV \emph{커널}뿐).
본 절의 두 식을 코드로 되살리려면 새 게이트 없이 재도입하지 말 것(reflect G-R3 이 부재를 증빙).
\end{warnbox}
```

- **연계**: `results/REFLECT_SEED_TABLE.md`·`results/comp_v24/FIT_CHECK_v1024.md` 의 @3 채택 근거 행에 "v1.0.25 철회 + 코드 삭제(전이세분 우위 — ablation 재실측)" 추기.
- **금지**: `eq:sifr-kernel`·`eq:sifr-blend` 식/라벨/boxed 삭제 금지. Ch3 §3.2b 의 $\Omega$ 논의 자체도 삭제 금지(위 warnbox 로 지위만 명시).

## T8. 부록 B 코드맵 — alpha·func_dxi_eq·_causal_pad·use_si_constants 행 (Step 22, C1/C2/C3 cascade)

- **파일**: `_sections/ch1_appB_codemap.tex`
- **`tab:symcode`(line 18~)**: 행 추가 —
  - `$\alpha_j$ (skew 지수, 식~\eqref{eq:skewpeak})` ↔ `전이 dict 'alpha'(부재=1.0=bit-exact) / func_dxi_eq`
  - `$\xi_\eq=\sigma^{\alpha}$ 진행좌표` ↔ `func_dxi_eq(...)[1]`
- **`tab:inputs`**: 입력 행 추가 — `'alpha'`: 선택, 기본 1.0, tier C(피팅), α↔L_V 동시 자유화 경고(G-α4).
- **`tab:nodecode`(line 107~)**: 꼬리 노드 행에 `_causal_pad`(eq:lag 하한 −∞ 실현 — 진행방향 5·L_V pad 후 절단) 추가.
- **각주**: `func_ksi_eq`↔`func_dxi_eq` 관계 — "func_dxi_eq 는 func_ksi_eq 의 σ 를 재사용하며 α=1 에서 기존 종을 연산 순서까지 동일하게 반환(bit-exact 계약)".
- **상수 행**: `R·F`(레거시 기본) 옆에 `R_SI·F_SI + use_si_constants()`(opt-in, C3) 행 추가 — "기본 미적용: 골든 bit-exact 계약(G1) 보존" 명기.

## T9. §1.4·§9 "점별 평가" pad 각주 (C2 cascade)

- **파일**: `_sections/ch1_sec00_intro.tex`(line ~85, 점별 서술)·`_sections/ch1_sec09_tail.tex`(eq:lag 사용부)·`_sections/ch1_sec08_lag.tex`(eq:lag 정의부)
- **수정문(각주 초안)**: "구현 각주(v1.0.25): 꼬리 항의 인과 기억 적분(식~\eqref{eq:lag})은 하한이 $-\infty$ 인 이력 적분이므로, 점별 평가라도 \emph{진행방향 과거로} $5L_V$ 만큼 pad 확장 후 원 격자만 절단 반환한다(`_causal_pad`) --- 평가창 시작점이 peak 안에 있어도 결과가 창에 의존하지 않는다(≤1\%; 종전 구현은 창 시작 $\xi_\eq$ 상수 근사라 최대 100\% 의존). 평형 종$\cdot$기본 데이터셋 경로는 무변경."
- **부록 E**(`ch1_appE_selfconsistent.tex`): ratio 경로도 같은 pad 를 쓴다는 1문장(G-E2 동결회수 불변).

## T10. C_bg 창-국소 상수 근사 명기 (Step 18, C8)

- **파일**: `_sections/ch1_sec10_sum.tex`(eq:sum·배경 서술 lines 7·14·108·114·128 부근)·§6/§7 의 배경 언급부
- **수정문(삽입 초안)**: "$C_\bg$ 는 \emph{피팅 창-국소 상수 근사}다 --- 실측(4셀$\cdot$2프로토콜)에서 배경은 0.3--0.9 V 에 걸쳐 단조 감쇠(창 평균의 $\sim$230\%)하므로 상수$\cdot$선형 모두 전역으로는 부족하고, 좁은 피팅 창 안에서만 상수가 실용적이다. 창을 넓히면 광폭 종 1개가 추가로 필요하며, 그 이득은 skew $\alpha$(식~\eqref{eq:skewpeak})와 동반될 때만 확인되었다(단독 대체는 악화)."

## T11. C3 상수 — worked-example 표시값 각주 (C3 cascade)

- **파일**: `_sections/ch2_sec08_synthesis.tex`·`ch2_appB_codemap.tex`(B.2 회귀 기준표)·열척도 25.7 mV 언급부(ch1_sec05_width.tex:302 등)
- **내용**: 코드 기본은 레거시 상수(R=8.314·F=96485.0 — 골든 bit-exact 계약), SI 는 `use_si_constants()` opt-in 임을 각주로. SI 발효 시 회귀 기준 표시값: −0.204/−0.134/−0.070 mV/K·+60.8 mV·25.693 mV **불변**, 단 $U_\oc(\bar x{=}0.25)$ 는 raw 74.3511→74.3497 mV(−1.4 µV, 표시양자 50 µV 의 3%)로 물리 불변이나 `.1f` 표시가 74.4→74.3 으로 뒤집힌다(반올림 절벽 74.35 인공물) — worked-example 에 "74.35 mV(표시 74.4; SI 상수 시 74.3)" 형태로 병기 권고. LCO `dH_rxn` 역산 상수 주석(코드 line ~1018 "역산 상수 = 본 모듈 F=96485.0")도 SI opt-in 시 +13 µV 어긋남 각주 유지.
- **근거**: `test_gates_v1025.py` G-SI 출력.

## T12. §5b 해상도 사다리 — Si 7-gallery 병기 + gallery≠상 재강조 (Step 23, C7)

- **파일**: `_sections/ch1_sec05b_gr2L.tex`(해상도 사다리 서술)·`_sections/ch3v22_sec02_cases.tex`(Si 케이스)
- **수정문(삽입 초안)**: "Si 쪽 최고 해상도 옵션으로 7-gallery(`SI_MSMR7_LIT`, opt-in)가 추가되었다 — p-ocvhold 프로토콜에서만 검출되는 0.433/0.456 V c-Li$_{15}$Si$_4$ 결정화 쌍 feature 포함. gallery 세분은 곡선 표현 해상도이지 상(phase)이 아니다 — XRD 상 수(흑연 4 staging·두-상 2)는 불변(§7 위임). 검출 피크 수는 프로토콜·prominence 의존(흑연 3→4→5, Si 0.43–0.46 V feature 는 p-ocv 부재/hold 존재)."

## T13. 데이터 정직화 (Step 24, C9)

- **파일**: `results/comp_v24/DATA_REGISTRY.md`·`results/comp_v24/FIT_CHECK_v1024.md`·(있으면) `SOURCES.md` — v1.0.25 사본에 추기
- **내용**:
  1. 레포 프로토콜 혼용 정정: `gr.csv` = gr_A(**p-ocv**), `si.csv` = si_Dhold(**p-ocvhold**) — 라벨 명기.
  2. p-ocvhold 권고: 같은 7전이로 p-ocv R² 0.9770 → p-ocvhold 0.9945·피크역 RMSE 4.708→2.701 (불일치 상당분 = 비평형 잔여).
  3. 독립셀 재현성 등재: gr_B 0.9770(레포 동일)·si_A/si_Chold 0.998–0.999 — `FIT_CHECK` 근거로만(상시 파이프라인 증설 아님).
  4. @3(regsol) 근거 철회 행: 전이세분 시 +0.97%p→−0.53%p 역전(T7 과 동일 근거) + **코드 삭제 완료** 명기.

## T14. 버전 문자열·마감문서 (Step 25 연계)

- ch1/ch2/ch3 `.tex` 표제·`common_preamble_v1024.tex` 버전 표기 1.0.24→1.0.25. **DG-2 확정(사용자 결정 "파일명을 왜 바꿔? 버전명만 바꿔주면 되는거 아니냐"): 파일명·`\input` 경로·`\externaldocument` 키는 전부 불변 — 문서 내 버전 문자열만 교체.** 파일명에 박힌 `_v1.0.24`/`v1024` 토큰은 그대로 둔다(개명 금지).
- `ARCHIVE_NOTE.md`(v1.0.25 사본): "v1.0.24 와 byte-identical" 주장 스테일 — v1.0.25 변경 요지로 갱신 필요.
- 마감문서 신설: `results/V1025_CHANGE_LEDGER.md`·`HANDOVER_v25.md`·`MERGE_READINESS_v25.md`·`INDEX_v25.md`.
- 신규 라벨 grep 확인: `eq:skewpeak` 정의 1회·참조 무결, 기존 라벨 무변경(Step 19). 빌드 3-pass 0-err(Step 20·26·27).

---

## 참고 — 코드 측 이미 완결(문건이 정합해야 할 코드 거동)

| 항목 | 코드 사실 |
|---|---|
| C1 | `func_dxi_eq(T,V,U,n,s,alpha)` → `(dξ/dV, ξ_eq=σ^α)`; `alpha` 부재=1.0=bit-exact(G-α1 array_equal, 골든 max\|d\|=0) |
| C2 | `_causal_pad(V,L)`: 5·L_V·간격≤L/20·상한 4000점; dqdv 동결·ratio 두 인과 경로 적용; 창 의존 74%→0.02%(G-창) |
| C3 | 기본 R=8.314·F=96485.0(레거시) + `R_SI/F_SI/use_si_constants()` opt-in — **계획서 원안(즉시 교체)은 골든 bit-exact 게이트와 양립 불가**하여 opt-in 으로 집행(G-SI 증빙). 문건은 이 opt-in 지위를 그대로 서술할 것 |
| C6 | **regsol 코드 완전 삭제**(사용자 결정 DG-1(b)) — `_REGSOL_XG`·`_regsol_binodal_xa`·`_regsol_dqdv`·`equilibrium` 의 `'kernel'` 분기 제거(−40줄). 커널 계통 = 로지스틱 단일계. reflect **G-R3 = 삭제 확인 게이트**(심볼 부재 3/3 + `'kernel'` 키 무시 `array_equal` + 면적=Q). **Ω 코드는 전량 보존**(`func_dU_hys`·`func_dH_a_eff`·§7 상성격 판정 — regsol 무관). 데이터셋 전량 보존 |
| C7 | `SI_MSMR7_LIT` 7전이(0.433/0.456 포함, 로지스틱) additive — 기본 셋 동일(G-si7) |
