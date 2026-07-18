# A16_REVIEW — §18 입력 규정 + 부록 A/B/C/D (ch1_graphite_v1.0.22 빌드)

- 검토 창: FR-A16 (BRIEF_FR_A.md 규율 준수 — 보고 전용·소스 수정 금지·git 조작 금지·Codex/ 접근 금지)
- 대상(전문 정독 완료):
  - `_sections/ch1_sec18_inputs.tex` (§18 전체 입력 인자와 피팅 준비, 69행)
  - `_sections/ch1_appA_signcheck.tex` (부록 A 곡선 부호 사슬 검산표, 89행)
  - `_sections/ch1_appB_codemap.tex` (부록 B 곡선 계산 구현 대응표, 157행)
  - `_sections/ch2_appA_traps.tex` (본 빌드 부록 C 열특성 기호·부호 함정 검산표[역사적 파일명], 75행)
  - `_sections/ch2_appB_codemap.tex` (본 빌드 부록 D 열특성 코드 요구명세[역사적 파일명], 75행)
- 코드 원본 대조: `Claude/docs/v1.0.21/Anode_Fit_v1.0.21.py` (1152행 전문 정독 — v22 코드 개정 R6 미착수 전제)
- 검토 4관점: ①내용 보완(빡세게) ②논리 오류(재계산·재유도 검증) ③더 쉬운 설명 ④산문→수식 간결화
- 상태: **완료** (조기 저장 원칙 준수 — 발견별 검증 즉시 append 후 말미 정리)
- 결산: **H 1 · M 8 · L 4 = 13건** + 무발견 축 명시

## 발견 표

| ID | 파일:행 | 유형 | 등급 | 현행(축자) | 제안(완성 LaTeX) | 근거 |
|----|---------|------|------|-----------|-----------------|------|
| A16-H1 | ch1_appB_codemap.tex:142,143-146 | 논리(코드맵 오귀속) | H | `\textbf{N2.} \code{if 'dH\_rxn' in tr and 'dS\_rxn' in tr: U\_j = func\_U\_j(T\_work, dH\_rxn, dS\_rxn)}`<br>…`실 호출의 $\Delta S$ 인자는 seam`<br>`\code{\_effective\_dS\_rxn(tr, T\_work)} 를 경유한다`…`vib 양자 보정 \code{\_vib\_dU(tr, T\_work)} 가`<br>`가산된다` | `\textbf{N2.} \code{if 'dH\_rxn' in tr and 'dS\_rxn' in tr: U\_j = func\_U\_j(T\_prog, dH\_rxn, dS\_rxn)}` (및 같은 codebox 의 `\code{\_effective\_dS\_rxn(tr, T\_prog)}`·`\code{\_vib\_dU(tr, T\_prog)}` 로 동반 치환; 문두 안내 "구현 스니펫 두 곳(본문 N2$\cdot$N7 에서 이관)을 원문 그대로 둔다" 는 유지하되 실 구현 식별자와 재정합) | 식별자 `T_work` 는 구현 어느 버전에도 없음 — v1.0.21(대조 코드)·v1.0.19(부록이 명시한 버전)·v1.0.15/16/17 전부 grep 0건. 실 코드 N2(dqdv 경로) = `U_j = func_U_j(T_prog, tr['dH_rxn'], self._effective_dS_rxn(tr, T_prog)) + self._vib_dU(tr, T_prog)` (v1.0.21:547; equilibrium·solve_U_oc 경로는 `T`). 부록 B 의 존재 목적이 "본 장과 구현 사이의 1:1 대조"인데 스니펫 식별자가 전 버전 부재 → 오귀속. tab:nodecode N1 행이 실코드 축자(`V_n = V_in - sigma_d * I_abs * self.Rn` v1.0.21:514 일치)인 것과 대비되어 독자가 N2 도 축자로 신뢰할 위험. v1.0.21 문건에서 이월된 기존 결함(v22 신규 아님) |
| A16-M1 | ch1_appB_codemap.tex:5 | 보완(버전 anchor) | M | `문건과 구현의 연계는 단방향이다 --- 구현(\code{Anode\_Fit\_v1.0.19.py})의 주석$\cdot$docstring 이 본 장의`<br>`식 번호를 참조한다.` | `문건과 구현의 연계는 단방향이다 --- 구현(\code{Anode\_Fit\_v1.0.21.py} --- v1.0.19 에서 물리$\cdot$수치 경로 무변경 이월)의 주석$\cdot$docstring 이 본 장의 식 번호를 참조한다.` (R6 코드 개정 착수 시 v1.0.22 로 재갱신) | 현행 matched 구현 = `docs/v1.0.21/Anode_Fit_v1.0.21.py`(코드 헤더 "release 버전 = 1.0.21 — 문건 Ch1/Ch2 1.0.21 와 동일 버전·matched"); `docs/v1.0.22/Anode_Fit_v1.0.22.py` 도 실재(v1.0.21 과 byte-identical). v1.0.19.py 는 실재하나 2세대 전 anchor — v1.0.22 문건이 이를 "구현"으로 지목하면 버전-matched 계보(코드 헤더 명시)와 불일치. 단 appB:134 "(v1.0.19 additive…)" 와 bib `numverif2026` 의 "Anode_Fit_v1.0.19" 은 역사 기록으로 정확하므로 유지 대상(치환 금지) |
| A16-M2 | ch2_appA_traps.tex:38-41 | 보완(명칭 정합 — P3-7) | M | `$g$ 4종 &`<br>`$g_j(x){=}\xi(1-\xi)/w$ 봉우리 가중[1/V] &`<br>`$g_j(\xi)$(Ch1 조성 자유에너지)$\cdot$$g(\theta)$(BW)$\cdot$$g(E_F)$(상태밀도)와 혼동 &`<br>`\S\ref{ssec:overlap} \\` | `$g$ 4종 &`<br>`$g_j(x){=}\xi(1-\xi)/w$ 봉우리 가중[1/V] &`<br>`$g_j(\xi)$(Part 0 조성 자유에너지, \S\ref{sec:sm-mf})$\cdot$$g(\theta)$(BW)$\cdot$$g(E_F)$(상태밀도)와 혼동 &`<br>`\S\ref{ssec:overlap} \\` | 병합 빌드에서 "Ch1" = 이 문서 전체라 지시 불명(v1.0.21 분권 시절 잔재). 원천 ssec:overlap(ch2_sec05_mixing:41-43) 자신이 "Part 0 의 조성 자유에너지 $g_j(\xi)$(\S\ref{sec:sm-mf})" 로 귀속 — 같은 표의 "u_j vs Ch1 u_j" 행은 이미 "앞 파트 \S\ref{sec:hys}…같은 문서 내" 로 정합화된 것과 비대칭. sec:sm-mf 라벨 실재(ch1_sec02b:5, 같은 빌드). 함정표의 존재 목적이 기호 지시 명확화이므로 지시어 자체의 모호성은 실질 개선 대상(P3-7 명칭 혼동 방지) |
| A16-M3 | ch2_appB_codemap.tex:10-11 | 논리(범위 주장 — 병합 후 실효) | M | `함수명은`<br>`이 부록에만 등장한다(본문은 교과서 register 로 물리$\cdot$모델 언어만 쓴다).` | `함수명은`<br>`부록(본 부록과 부록 B)에만 등장한다(본문은 교과서 register 로 물리$\cdot$모델 언어만 쓴다).` | 병합 빌드에서 부록 B(ch1_appB) 가 동일 함수명(`solve_U_oc`·`entropy_coefficient_x`·`reversible_heat_x` — tab:nodecode x̄ 진입점 행:132-135) 을 이미 수록 — "이 부록에만" 은 문서 전체 기준 문언상 거짓. Part T 본문(ch2_sec00~10) 의 `\code{}` 사용 0건은 grep 확인(괄호 절반은 참) — 분권 시절(구 Ch2 단독 문서) 참이던 주장이 병합으로 실효된 유형. 독자가 부록 B 의 함수명 수록을 규약 위반으로 오독할 여지 제거 |
| A16-M4 | ch1_sec18_inputs.tex:5-6 | 논리(과대 주장) | M | `곡선식의 모든 물리량이 사용자`<br>`조정 가능한 입력이며, 내부에 고정된 상수는 없다(전부 기본값$+$override).` | `곡선식의 모든 물리량이 사용자`<br>`조정 가능한 입력이며, 내부에 고정된 상수는 없다(전부 기본값$+$override --- 물리 상수 $R,F,k_B,h$ 와 수치 안전 가드 상수는 물리 인자가 아니므로 제외).` | 무한정 서술 "내부에 고정된 상수는 없다" 의 반례가 구현에 실재: `_LAG_RESOLVE_DECAY_CAP=40.0`(v1.0.21:77, 모듈 상수·override 불가), 기억 적분 조밀 구간 문턱 `a<1e-4`(:128), `eps=1e-12`(:669). 전부 수치 가드(물리 분기 아님 — 코드 주석 자인)이나, 문장을 감사 관점으로 읽는 독자(피팅 실무자)가 코드 대조 시 모순으로 오독할 수 있음. 한정어 1구로 주장 강도를 사실과 정합시키는 보강(자산 삭제 없음) |
| A16-M5 | ch1_sec18_inputs.tex:12-13 | 설명(압축 난해) | M | `반응 열역학($\Delta H_\rxn\cdot\Delta S_\rxn$)$\cdot$DFT 값은 신뢰 상한이 아니라`<br>`\emph{출발점}이므로 소폭 자유도를 권한다.` | `반응 열역학($\Delta H_\rxn\cdot\Delta S_\rxn$) 값과 DFT 활성화 값은 곧이 믿고 잠글 경계(상$\cdot$하한)가 아니라`<br>`\emph{출발점}이므로 소폭 자유도를 권한다.` | "신뢰 상한" 이 압축돼 두 갈래로 오독됨: (i) 직전 문장의 "좁은 상하한" 과 평행하게 '탐색 경계' 인지 (ii) '신뢰값' 의 오기인지. 본서 확립 어법은 "신뢰값이 아니라 초기값/출발점"(tab:staging 캡션·sec10:17·tab:lco-staging 캡션) — 여기서만 "신뢰 상한" 이라는 일회성 어구 사용. 또한 "DFT 값" 의 지시 대상(활성화 $\Delta H_a$, tab:staging의 persson anchor)이 명시되면 직전 문장의 $\Delta H_a$ 열거와의 관계도 풀림 |
| A16-M6 | ch1_appA_signcheck.tex:44-47,81 | 보완(꼬리 분기 수치 회귀 부재) | M | `R1--R3 은 독립 수기 재산출로 동일 양을 재확인한 것, R4 는 컷 규칙 정의 검사, R5 는 극한 논증,`<br>`R6 은 LCO 중심 부호의 문헌 역대입이다` | R6 뒤 추가 행 후보(R7 — 기존 행 무변경 append):<br>`R7 & 꼬리 방향 반전 수치: 단일 전이 $U{=}0.120$ V$\cdot$$w{=}0.014$ V$\cdot$$Q{=}0.5$$\cdot$$L_V{=}0.02$ V 직접 지정, $|I|{=}0.5$. & 방전 peak $V{=}0.134$/충전 peak $V{=}0.106$ --- 중점 $\tfrac12(V_\dis{+}V_\chg){=}0.120{=}U$(거울 대칭), 두 branch 최대값 동일$\cdot$전 구간 음수 없음, 꼬리가 진행상 나중 전위 쪽(방전 높은 $V$$\cdot$충전 낮은 $V$)으로 늘어짐 --- S7 의 수치 확인. & 식~\eqref{eq:reversal}$\cdot$ \eqref{eq:peakshape} & $\checkmark$ \\` (헤더 "R1--R5"·"여섯 행" 산문은 "R1--R6"(흑연)·"일곱 행" 으로 동반 갱신 필요) | R-표의 회귀 검산이 히스(R1$\cdot$R2)·평형 극한(R3$\cdot$R5)·컷(R4)·LCO(R6)를 덮으나 **유한 $L_V$ 의 꼬리 분기(S7 의 수치 대응)는 수치 행이 없음** — S7 만 정성. 부록 자기 규정("표의 각 행은 반증 가능한 조건")상 방향 반전은 부호 사슬의 최대 위험 항목(비인과 시 peak 번짐)인데 수치 고정이 빠짐. 제안 수치는 v1.0.21 코드 재현 검증 완료(방전 peak V=0.1336·충전 V=0.1063·중점 0.1200·최대 7.082 동일·음수 0건 — 코드 자체 데모와 동일 설정) |
| A16-M7 | ch1_appB_codemap.tex:93-94 | 보완(입력 표 완전성) | M | `\multicolumn{4}{l}{\emph{— 호출 인자(\code{curve}/\code{dqdv}) —}}\\`<br>`\code{V\_app},\code{T},\code{c\_rate}/\code{I\_abs},\code{Q\_cell},\code{direction} & 호출 & --- & 실험조건 (\eqref{eq:n0map}) \\` | 해당 그룹 아래 행 그룹 추가(기존 행 무변경):<br>`\multicolumn{4}{l}{\emph{— 호출 인자(발열$\cdot$$\bar x$ 진입점; 요구명세 = 열특성 부록 D) —}}\\`<br>`\code{V\_n}/\code{x\_bar},\code{T},\code{I},\code{return\_terms} & 호출 & --- $/\,298.15$,\,$1.0$,\,False & $\partial U_\oc/\partial T$$\cdot$$\dot Q_\rev$ (\eqref{eq:complete}\eqref{eq:qrev}); \code{return\_terms} 는 완전/단순/config 분리 반환 \\`<br>`\code{U\_lo},\code{U\_hi},\code{tol},\code{max\_iter} & 호출 & 자동/자동/$10^{-13}$/$200$ & 음함수~\eqref{eq:implicit} 이분법 괄호$\cdot$수렴(\code{solve\_U\_oc}) \\` | tab:inputs 캡션의 "전체 입력 인자" 주장 대비 발열$\cdot$$\bar x$ 진입점(`entropy_coefficient`/`_x`·`reversible_heat`/`_x`·`solve_U_oc`) 호출 인자가 전무 — 같은 부록 tab:nodecode 가 이 진입점들을 이미 수록(:132-135)하므로 표 간 비대칭. 기본값은 v1.0.21 시그니처 확인값(T=298.15·I=1.0·return_terms=False·tol=1e-13·max_iter=200·U_lo/U_hi=None 자동 괄호). Optuna 노출 관점(캡션 자인)에서 실질 이득 |
| A16-M8 | ch2_appB_codemap.tex:18-23 | 수식화(산문→표) | M | `이 타깃의 구현 진입점 명명(요구명세): 조성 $\bar x$ 를 직접 받는 세 진입점 ---`<br>`\code{solve\_U\_oc}$(\bar x,T)$ $=$ 음함수~\eqref{eq:implicit} 의 유일근 솔버,`<br>`\code{entropy\_coefficient\_x}$(\bar x,T)$ $=$ 그 근에서의 $\partial U_\oc/\partial T$(완전식~\eqref{eq:complete}),`<br>`\code{reversible\_heat\_x}$(\bar x,T,I)$ $=$ 출구~\eqref{eq:qrev} --- 를 두고, 기존 내부 전위 입력`<br>`\code{entropy\_coefficient}$(V_n,T)$ 경로는 그대로 유지한다(하위호환 --- 두 진입점의 입력 좌표가`<br>`$\bar x$ vs $V_n$ 으로 다르다는 것이 아래 D.2 첫 행의 함수명 구분 근거다).` | `이 타깃의 구현 진입점 명명(요구명세)은 다음 표와 같고, 기존 내부 전위 입력 \code{entropy\_coefficient}$(V_n,T)$ 경로는 그대로 유지한다(하위호환 --- 두 진입점의 입력 좌표가 $\bar x$ vs $V_n$ 으로 다르다는 것이 아래 D.2 첫 행의 함수명 구분 근거다).`<br>`\begin{center}\begin{tabular}{l l l}`<br>`\toprule 진입점(요구) & 입력 & 산출(=근거 식) \\ \midrule`<br>`\code{solve\_U\_oc} & $\bar x,\,T$ & $U_\oc$ --- 음함수~\eqref{eq:implicit} 유일근 \\`<br>`\code{entropy\_coefficient\_x} & $\bar x,\,T$ & $\partial U_\oc/\partial T$ --- 완전식~\eqref{eq:complete}, 그 근에서 평가 \\`<br>`\code{reversible\_heat\_x} & $\bar x,\,T,\,I$ & $\dot Q_\rev$ --- 출구~\eqref{eq:qrev} \\ \bottomrule`<br>`\end{tabular}\end{center}` | 5행에 걸친 3중 "---" 병렬 산문이 표 1개로 정확$\cdot$간결해짐(BRIEF ④). D.2 회귀표와 같은 표 어휘로 정렬돼 요구명세의 기계 적용성(함수명$\cdot$입력$\cdot$출력$\cdot$근거식 1:1) 향상. 내용 삭제 없음 — 하위호환 문장 전문 보존 |
| A16-L1 | ch1_sec18_inputs.tex:5 | 설명(선행사 없는 지시어) | L | `사용자 목표는 이 모든 인자를 입력으로 노출해 측정 데이터에 피팅하는 것이다.` | `사용자 목표는 여기까지의 곡선$\cdot$열특성 사슬에 등장한 모든 인자를 입력으로 노출해 측정 데이터에 피팅하는 것이다.` | 절 첫 문장의 "이 모든 인자" 는 선행사가 절 내부에 없음(직전 절은 Part T 마감 — 병합 재편으로 §18 이 문서 말미로 이동한 뒤 지시 범위가 더 멀어짐). 제목("전체 입력 인자")이 보완하나 본문 자체 완결이 나음 |
| A16-L2 | ch1_sec18_inputs.tex:18 | 설명(범주 정밀) | L | `(2) 실험조건 $\sigma_d$, $|I|=$ c-rate$\,\cdot Q_\cell$, $T$, $R_n$ 설정 → 분극 $V_n$(\eqref{eq:n0map}\eqref{eq:vn}); 이후 평가는 $V_n$ 에서 점별.` | `(2) 실험조건을 $\sigma_d$, $|I|=$ c-rate$\,\cdot Q_\cell$ 로 환산하고(\eqref{eq:n0map}) $T$$\cdot$모델 인자 $R_n$ 와 함께 분극 $V_n$(\eqref{eq:vn}); 이후 평가는 $V_n$ 에서 점별.` | $R_n$ 은 실험조건이 아니라 생성자 인자(모델 공통 — 같은 문서 tab:inputs "생성자 인자(모델 공통)" 분류·sec01:10 의 실험조건 5-튜플 $(V_\app,\mathrm{direction},\mathrm{c\_rate},Q_\cell,T)$ 정의와 상충). $\sigma_d\cdot|I|$ 도 raw 실험조건이 아니라 eq:n0map 환산 산출임을 문장 구조가 흐림 |
| A16-L3 | ch1_appA_signcheck.tex:23-24 | 설명(괄호 암호성) | L | `S1 & $U_j(T)=(-\Delta H_\rxn+T\Delta S_\rxn)/F$, $\Delta G_j=-sFU_j$ --- $\Delta H_\rxn<0$(발열)이면`<br>`$-\Delta H_\rxn>0$ 이 중심을 올린다(흡열 아님).` | `S1 & $U_j(T)=(-\Delta H_\rxn+T\Delta S_\rxn)/F$, $\Delta G_j=-sFU_j$ --- $\Delta H_\rxn<0$(발열)이면`<br>`$-\Delta H_\rxn>0$ 이 중심을 올린다(부호를 그대로 읽어 흡열 전이로 오독하지 않도록 --- 선행 음부호가 관건).` | 괄호 "(흡열 아님)" 의 부정 대상이 문면에 없음(중심 상승이 흡열이 아니라는 것인지, ΔH<0 이 흡열이 아니라는 것인지). 검산표는 오독 방지가 존재 이유이므로 함정의 방향을 명시하는 편이 안전. eq:Uj·eq:eqcond(ch1_sec03:35-41) 재확인 — 식 자체는 정확(무결) |
| A16-L4 | ch1_appB_codemap.tex:125 | 보완(구현 식별자 완결) | L | `N8 & 기억 적분 $\xi_\mathrm{lag}$(\eqref{eq:lag}) 의 점별 수치 적분(\code{ksi\_lag}); 충전 분기는 상한 반전(\eqref{eq:reversal}) \\` | `N8 & 기억 적분 $\xi_\mathrm{lag}$(\eqref{eq:lag}) 의 점별 수치 적분(\code{\_causal\_memory\_pointwise} $\to$ \code{ksi\_lag}); 충전 분기는 상한 반전(\eqref{eq:reversal}) \\` | tab:nodecode 의 다른 행은 산출 루틴명을 직접 들지만(N2 func_U_j·N5 func_ksi_eq·N7 func_L_q 등) N8 만 결과 변수명(`ksi_lag`, v1.0.21:580)만 들고 실제 적분 루틴 `_causal_memory_pointwise`(:107, eq:lag 구간별 정확 적분 구현)가 부록 전체에서 미등장(grep 0건) — 역방향 조회(노드→식별자) 목적상 루틴명이 조회 키 |

## 검증 로그 (축별 — 완료 시마다 append)

### 축 0 — 기반 검증(빌드 소속·라벨 존재성·코드 대조 기반) [완료]
- 빌드 마스터 `ch1_graphite_v1.0.22.tex` 확인: 포함 순서 = sec00~10 → Part T(ch2_sec00~10) → sec18 → appA(`\appendix`, 부록 A) → appB(부록 B) → ch2_appA(`\section*` 부록 C) → ch2_appB(`\section*` 부록 D) → bib. LCO 장 라벨은 `\externaldocument{ch2_lco_v1.0.22}`(xr 전방 참조 22곳) 경유 — 대상 5본의 LCO 계열 참조(eq:lco-sigmaslot·eq:lco-dUdT·eq:lco-dUhys·eq:lco-Ubranch·eq:lco-decomp·eq:dSemolar·eq:ggate·tab:lco-staging·sec:lco-code·sec:lco-gate·sec:lco-direction·sec:lco-center) 전부 ch1_sec11~17(ch2_lco 빌드 소속 파일)에 실재 확인.
- 대상 5본이 참조하는 자체 빌드 라벨 전수 실재 확인(grep): eq:n0map·eq:vn·eq:Uj·eq:center·eq:wbase·eq:xieq·eq:Acut·eq:chid·eq:dHeff·eq:Lqfull·eq:LV·eq:lag·eq:reversal·eq:peakshape·eq:tail-limit·eq:eqpeak·eq:sum·eq:dUhys·eq:Ubranch·eq:implicit·eq:complete·eq:qrev·eq:logistic·eq:muV·eq:sm-mc-balance·eq:dxidT·eq:weighted·eq:Se-ch2(ch2_sec03)·tab:staging·tab:nodemap·tab:nodecode·tab:inputs·tab:symcode·tab:qrev·sec:signcheck·sec:appendix-code·sec:broadening·sec:eqpeak·sec:hys·sec:einstein·sec:mixing·sec:sm-mc·ssec:logistic·ssec:dvdt·ssec:overlap·ssec:einstein-roundtrip·ssec:einstein-closed·ssec:signlabel·ssec:threedist·ssec:elec·ssec:weff·ssec:synth·ssec:worked·ssec:blend — 전건 존재, 깨진 참조 0.
- §18 keybox(3) 의 `\eqref{eq:center}` 는 ch1_sec04_hys:269-276 의 분기 중심 case 식(γ≠0∧Ω>0 branch shift / 그 외 U_j)으로 실재 — "분기 중심 U_j^d" 귀속 정확(tab:nodemap N3 의 eq:dUhys·eq:Ubranch 와 상보, 충돌 아님). eq:center 의 T_rep 사용은 코드 `func_U_branch(T_rep, …)`(v1.0.21:556) 와 정합.
- appA S7 "적분 상한 +∞" = eq:reversal(ch1_sec09_tail:169-179) 충전 분기 `∫_V^{+∞} ξ_eq(u) e^{−(u−V)/L}du` 와 정확 일치.
- 코드 파일 계보: docs/v1.0.19/Anode_Fit_v1.0.19.py 실재, docs/v1.0.21/Anode_Fit_v1.0.21.py = matched 현행, docs/v1.0.22/Anode_Fit_v1.0.22.py = v1.0.21 과 byte-identical(diff 0) — R6 미착수 정합.

### 축 1 — 수치 재계산(부록 A R1~R6·부록 D D.2 전건) [완료 — 전건 PASS]
- 실행 환경: v1.0.21 코드 직접 로드(파일 무변경·bytecode 미생성) + 수기 병행 재산출.
- appA R1: u=√(1−2RT/Ω)=0.7661 (본문 0.766 ✓), ΔU_hys=(2/F)[Ωu−2RT·artanh u]=86.69 mV (본문 86.7 ✓ — `func_dU_hys` 동일값). 분기 갈림 V_dis−V_chg=γ·ΔU_hys=+86.7 mV>0 부호 ✓.
- appA R2: 2RT(298.15 K)=4957.6 J/mol (본문 4958 = 반올림 ✓), ΔU_hys=0.0000 ✓ (Ω≤2RT 분기 연속).
- appA R3: func_L_q 구조상 L_q∝|I| (T_attempt=(I/Q_cell)h/k_B 가 log 안 선형) ✓ — L_V∝|I|→0 ✓.
- appA R4: 코드 v1.0.21:432 `A = float(min(z_cut*n_safe*R*T, A_cap*R*T))` — 전이당 상수 ✓, 실현 미분 0 ✓.
- appA R5: 치환 t=(V−u)/L 의 항등식 재유도 — ξ_lag=∫₀^∞ξ_eq(V−Lt)e^{−t}dt 에서 부분적분으로 (ξ_eq−ξ_lag)/L=∫₀^∞e^{−t}ξ'_eq(V−Lt)dt 정확 성립(경계항 t→∞ 서 0, t=0 서 ξ_eq(V)). 지배함수 |dξ/dV|≤1/(4w) → e^{−t}/(4w) 적분가능 ✓ DCT 로 극한·적분 교환 ✓ → ξ(1−ξ)/w ✓. 차원 [1/V] 양변 ✓. 본문 sec09_tail:142 "지배함수 e^{−t}/(4w_j)" 와 동일 논거 ✓.
- appA R6: F×0.83e-3=80.1 J/(mol K) (본문 ~+80 ✓); 30 K×0.83 mV/K=24.9 mV (본문 ~+25 ✓); bib `swiderska2019` 실재(PCCP 21, 2115 (2019), DOI 10.1039/c8cp06638h, "+0.83 mV/K, tier B" 주석 포함) ✓.
- appB tab:inputs z_cut 기본 4.357 검산: ξ(1−ξ)=0.05×0.25 근 ξ=0.98734/0.01266, z=ln[ξ/(1−ξ)]=4.3565 ✓.
- appD D.2 전건 코드 실행 재검증: U_oc(0.25)=74.35 mV(→74.4 표시 ✓); 완전식 −0.2039/단순식 −0.1340/config −0.0700 mV/K ✓; ΔS=−19.68→−19.7 ✓; Q̇_rev/I=+60.81→+60.8 ✓; 5점 (−0.307/−0.204/−0.089/+0.044/+0.218 · +91.5/+60.8/+26.6/−13.2/−64.9) 전건 match ✓; U_oc 5점 열(43.5/74.4/109.0/148.8/195.2 mV) ✓; round-trip |FD−해석|=1.1×10⁻⁵ µV/K < 0.001 ✓.
- appD D.2 (c) 몫 수기 독립 재산출(코드 불사용): ξ_j=0.0049/0.0724/0.1434/0.3956, g_j=0.190/2.615/4.78/9.31, 비중 0.003/0.051/0.193/0.753, config=−0.4577/−0.2198/−0.1540/−0.0365 mV/K, 단순식 −0.1339, config 몫 −0.0698, 완전식 −0.2038 — ssec:worked tab:worked·(c) 표시값과 전건 일치 ✓ (완전식 괄호값 −0.157/−0.220/−0.206/−0.203 도 재산출 일치).
- appD D.2 "전 범위 파생 A" 행 ↔ ssec:blend srcbox: "175 점 전 범위 표시 정밀도(≲10⁻² mV/K) 일치·내부 전이 경계 3 곳 연속 블렌드" 축자 대응 ✓; `numverif2026` bib 실재([내부 자료] Anode_Fit_v1.0.19 명시) ✓.
- appD D.1 유일근 논거 재확인: 좌변 Σ_jQ_jξ_eq,j 는 s=+1 에서 각 항이 U_oc 단조증가 → 유일근 ✓; eq:sm-mc-balance(ch1_sec02b:343)·sec:sm-mc(:280) 라벨 실재 ✓. 완전식이 음함수 전미분과 동치임을 재유도(dU/dT=Σ Q_jg_j[U_j'+z_j w_j']/Σ Q_jg_j, U_j'=ΔS_j/F, w_j'=n_jR/F, z_j=ln[ξ/(1−ξ)]) — eq:complete 형태와 정확 일치 ✓.

### 축 2 — §18 본문·keybox·tab:nodemap [완료]
- keybox 6단계 사슬의 라벨 17건 전수 실재·귀속 정합(eq:center = 분기 중심 case 식 — 오귀속 아님을 sec04 원문으로 확정). 단계 순서 = 코드 dqdv 실행 순서(분극→중심→폭→ξ_eq→지연 상수→기억 적분→합산)와 1:1.
- tab:nodemap N0~N9 노드↔식 귀속 전수 정합: N0(eq:n0map — sec01:13-19 원문 대조 ✓)·N1(eq:vn)·N2(eq:Uj)·N3(eq:dUhys·eq:Ubranch)·N4(eq:wbase — sec05:265-270 ✓·"이중지위" 용어 sec05 자체 사용 ✓)·N5(eq:xieq — z=σ_d(V−U^d)/w ✓)·N6(eq:eqpeak — sec06:22-30 ✓)·N7(eq:Acut~eq:LV — sec08 라벨 순서가 실제로 이 구간을 이룸 ✓)·N8(eq:peakshape·eq:reversal)·N9(eq:sum).
- N5+ 행 수식 재유도: N_A(π²/3)k_B²T ∂g/∂x = (π²/3)R k_B T ∂g/∂x (N_A k_B²=R k_B) — eq:dSemolar(ch1_sec15:184-189) 와 동치 확정. "<0 (삽입)" 부호도 원문 부호 규약(삽입 시 ∂g/∂x<0)과 일치. 게이트 σ(1−σ) 닫힌식(eq:dSegate)이 코드 `func_dSe_molar` 와 축자 일치(골 깊이 −45.7 J/(mol K) 재계산 일치).
- §18.1 "출력이 입력 전위 $V_n$ 좌표" 표현 검토 — sec10:14 의 확립 관행("모든 평가가 입력 전위 $V_n$ 위에서 점별로 닫혀 출력 좌표가 곧 입력 좌표다")과 동일 어법으로 확인 → 무발견 처리(V_app→V_n 환산은 N1 이 명시).
- 발견: M4(고정 상수 과대주장)·M5(신뢰 상한 압축)·L1(지시어)·L2(R_n 범주).

### 축 3 — 부록 A 정성 사슬(S1~S8) [완료]
- S1: eq:Uj·eq:eqcond(ch1_sec03:35-41, ΔG_j=−sFU_j) 원문 대조 ✓. ΔH<0→−ΔH>0→중심 상승 논리 ✓ (발견 L3 = 괄호 표현만).
- S2·S3: logistic 미분 재유도 dξ/dV=σ_dξ(1−ξ)/w ✓ 절댓값 종 ✓.
- S4: eq:dUhys 의 "극대>극소라 ΔU≥0"·Ω≤2RT 명시 분기·u_j→0 연속(sec04:106-112 의 (8RT/3F)u³ 소멸 전개까지 확인) ✓.
- S5: 코드 func_chi_d(χ/1−χ 합-1)·func_dH_a_eff(ΔH_a−χ_dΩ) ✓.
- S6: sec08 "실현되는 미분 ∂lnL_q/∂V=0·부등식은 물리적 동기" 원문과 동일 register — 자기모순 없음 판정 타당 ✓.
- S7: eq:reversal 충전 분기 상한 +∞ 축자 확인 ✓ (발견 M6 = 수치 회귀행 부재 보완).
- S8: V_n=V_app−σ_d|I|R_n, 방전 시 V_app>V_n ✓ 코드 :514 축자 일치.

### 축 4 — 부록 B 코드맵 전수 대조 [완료]
- tab:symcode 28행 전수: 전 식별자가 v1.0.21 에 실재하고 역할 서술 정합(σ_d/s 이중 슬롯 해설·w↔n 역산 `_n_factor`·χ 생성자 인자 `x` 역사 명칭·MSMR ω→w=ωRT/F 환산[sec17 eq:lco-msmrmap 의 계수비교 f/ω=σ_d/w 와 동치 확인]). 결함 = H1(T_work — 전 버전 grep 0)·M1(v1.0.19 anchor) 뿐.
- tab:inputs 기본값 전수: n 부재=1·n_T1 부재=0/T_ref 298.15·Omega/gamma 0/0·h_eta 1.0·dS_a 0·dVdq_qa 0·z_cut 4.357(5% 컷 재계산 4.3565 ✓)·A_cap_RT 4.0·use_dH_eff True·x/chi 0.5·chi_split func_chi_d·Rn 0.0·Cbg 0.0·seed 298.15/0.1/1.0·LCO 게이트 13/0.85/0.05·_delith_is_discharge True/False·theta_E —/298.15 — 코드 시그니처·dict 접근 전건 일치. per-transition override(z_cut·A_cap_RT·use_dH_eff) 도 코드 tr.get(…, self.…) 구조와 일치.
- tab:nodecode: N1 스니펫 코드 :514 와 축자 일치 ✓; N5 np.where 이분 ✓ :94; N6 인라인 평형 종 ✓ :577; x̄ 진입점 3종 실재 ✓ :711/791/820 (발견 L4 = N8 루틴명 미등장). codebox N7 진행 사슬(:429→:432→:439→:443→:448) 전수 일치, U(298)=0.08529 재계산 ✓.
- LCO_MSMR_LIT "전이 구성·순서가 표의 물리 anchor 와 다른 tier-C 데모" 문구 — tab:lco-staging(ch1_sec11:51-78) 캡션의 동일 취지 문구와 축자 정합(코드 리스트 {3.930, 3.880, 4.050} vs 표 anchor {~3.90, ~4.05, ~4.17} 실제 상이 확인) → 무발견.
- equilibrium 서술("eq:eqpeak 만 U_j 중심 합산 — 분기 미반영 γ_j 무관 가역 기준선") — 코드 equilibrium(:451-468, 분기 shift 미적용) 및 sec06 의 γ≠0 잔존 극한 구분과 정합 ✓.

### 축 5 — 부록 C 함정표 12행 전수 원문 대조 [완료]
- s vs σ_d(ssec:logistic 각주 축자 정합 ✓)·θ/ξ(keybox ★표기 + ssec:dvdt 발산 부호 경고 축자 정합 ✓)·θ vs θ_E(ssec:einstein-closed 정의 ✓)·x̄≡1−x(ssec:overlap ★좌표 주의 축자 ✓)·g 4종(ssec:overlap ★기호 주의 — 발견 M2: "Ch1"→"Part 0" 지시 정합화)·F_vib(ssec:einstein-roundtrip ★구별 문구 축자 ✓·ΔF_vib=RT ln(1−e^{−θ_E/T}) 코드 :373 일치)·u_j vs x(정의 괄호 축자 ✓)·u_j vs Ch1 u_j(각주 "동명 별개·절-국소" 축자 ✓)·방전(I>0)(ssec:signlabel ★라벨 층위 축자 ✓·코드 reversible_heat docstring 일치)·ΔS(x) vs ΔS_a(ssec:threedist 경계 문단 축자 ✓)·ΔS_vib(T) vs ∂S_vib/∂x(eq:dSvib 직후 괄호 문장 축자 ✓)·S_e 라벨(eq:Se-ch2=ch2_sec03:74[본 빌드]·eq:Se=ch1_sec15:134[LCO 빌드] 라벨 배치 실확인 ✓).
- 표 서문 "새 내용을 도입하지 않는다" — 전 행이 본문 실재 문구의 재수록임을 확인(재수록 전용 charter 준수) ✓.

### 축 6 — 부록 D 요구명세 [완료]
- D.1: 타깃 사슬(eq:complete←eq:logistic·eq:implicit·eq:qrev) 라벨·구조 정합 ✓; 진입점 시그니처 3종 코드 일치 ✓; 유일근 보증 재유도(각 ξ_j 가 U_oc 단조증가 → 좌변 단조) + sec:sm-mc·eq:sm-mc-balance 라벨 실재 ✓ (발견 M3 = "이 부록에만"·M8 = 산문→표).
- D.2: 6행 전건 수치 재현(축 1 로그) + 근거 포인터(ssec:worked (a)(c)(d)(e)·tab:qrev·ssec:blend) 원문 값과 축자 일치 ✓.
- D.3: θ_E 미지정 bit-exact — 코드 `_vib_theta` None→0 경로(:344-385) 일치 ✓.
- D.4: s=+1·평형 중심(분기 無) — solve_U_oc `_charge`(:763-768)·entropy_coefficient(:680) 일치 ✓; "표시 반올림 전위 입력 금지" — 반올림 U 대입 시 U_oc 74.07 vs 74.35 mV(차 0.28 mV) 실측 = ssec:worked "0.3 mV 급" 정합 ✓; 두-상 자유 폭 규정 = ssec:synth keybox·ssec:weff 와 정합 ✓.

## 서치 (하이쿠 서브 위임 — doi 실검증분만)

대상 5본의 외부 인용은 **swiderska2019 단 1건**(appA R6). 나머지 인용(numverif2026)은 내부 자료(V1 원장 [C-133] 관할)라 위임 대상 아님. 신규 문헌 도입이 필요한 공백은 발견되지 않음(appB MSMR 행·appC Bernardi 행의 근거 문헌 msmr_partI/II·bernardi1985·newman 은 ch1v22_bib 에 기존재 — 본 창 무추가).

| 키 | DOI | 실재 | 메타데이터 일치 | 불일치/불가 | 비고 |
|---|---|---|---|---|---|
| swiderska2019 | 10.1039/c8cp06638h | ✓ (crossref 조회) | 저자 3인(Swiderska-Mocek·Rudnicka·Lewandowski)·저널 PCCP·권 21·시작쪽 2115·연도 2019 전건 일치 | 본문 수치 +0.83 mV/K 는 메타데이터로 검증 불가(기존 tier B 분류 타당) | crossref 제목 대시 "–" vs 본문 "—" 표기 차뿐. 페이지 전체 범위 2115-2120 |

## 등급별 정리

### H (1건)
- **A16-H1** appB codebox N2 의 `T_work` — 구현 전 버전(v1.0.15~v1.0.21) 부재 식별자를 "구현 스니펫"으로 제시(오귀속). 실 식별자 `T_prog`(dqdv)/`T`(equilibrium·발열 경로). v1.0.21 문건 이월 결함.

### M (8건)
- **A16-M1** appB 구현 버전 anchor v1.0.19.py → 현행 matched v1.0.21(또는 v22 사본) 재지정(역사 기록 2곳은 보존).
- **A16-M2** appC g 4종 행 "Ch1 조성 자유에너지" → "Part 0 …(\S\ref{sec:sm-mf})" (병합 빌드 지시 정합·P3-7).
- **A16-M3** appD "함수명은 이 부록에만 등장" — 병합 후 부록 B 와 중복이라 문언 실효 → "부록(본 부록과 부록 B)에만".
- **A16-M4** §18 "내부에 고정된 상수는 없다" 과대 주장 — 수치 가드 상수(_LAG_RESOLVE_DECAY_CAP 등) 예외 한정어.
- **A16-M5** §18 "신뢰 상한" 압축 난해 — 본서 확립 어법("신뢰값…출발점")으로 재서술.
- **A16-M6** appA 꼬리 방향 반전의 수치 회귀행(R7) 부재 — 검증 완료 수치로 행 추가 후보 제시.
- **A16-M7** appB tab:inputs 에 발열·x̄ 진입점 호출 인자 행 부재("전체 입력 인자" 주장 대비) — 행 그룹 추가 후보.
- **A16-M8** appD D.1 진입점 명세 5행 산문 → 3행 표(④ 간결화).

### L (4건)
- **A16-L1** §18 첫 문장 선행사 없는 "이 모든 인자".
- **A16-L2** §18 keybox(2) R_n 의 실험조건 오분류(문서 내 분류 체계와 상충).
- **A16-L3** appA S1 "(흡열 아님)" 괄호의 부정 대상 불명.
- **A16-L4** appB tab:nodecode N8 에 적분 루틴명 `_causal_memory_pointwise` 미등장.

## 4-tier (확정/추정/미검증)

- **확정(문면·코드·재계산으로 종결)**: A16-H1(전 버전 grep 0건)·M1(파일 계보 실확인)·M2(원천 절 원문 대조)·M3(grep 전수)·M4(코드 상수 실재)·L2(문서 내 분류 상충 문면)·L3(문면)·L4(grep 0건). 그리고 무발견 판정 전건(수치 재계산·라벨 전수·원문 대조에 근거).
- **추정(개선 제안 — 채택은 사용자/마스터 몫)**: M5(원문 의도의 최종 확정은 저자 몫 — 두 독해 모두 제시)·M6·M7(보강 행 추가는 증축 판단 사안)·M8(표 전환은 문체 정책 사안)·L1(재서술 강도).
- **미검증(본 창 범위 밖)**: ①PDF 렌더 층위(표 폭·줄바꿈·xr 해소 후 표시 번호 — 빌드 산출물 미검사, 마스터 GREEN 보고 의존) ②swiderska2019 의 본문 수치 +0.83 mV/K(crossref 메타데이터 검증 불가 — 기존 tier B 유지 타당) ③ch2_lco 빌드 쪽 LCO 절 내용 자체(A17~A20 소관 — 본 창은 라벨 실재·인용 정합만 확인).

## 무발견 축 (검토했으나 문제 없음)

1. **appA R1~R6 수치 전건**: 재계산 전건 일치(u=0.766·86.7 mV·4958·80 J/(mol K)·25 mV·L_V∝|I|·R5 항등식 재유도) — 결함 0.
2. **appD D.2 회귀 기준 전건**: 코드 실행 + 수기 병행 재산출 전건 일치(74.4 mV·−0.204/−0.134/−0.070·−19.7·+60.8·5점 표·round-trip 1.1×10⁻⁵ µV/K) — 결함 0.
3. **§18 tab:nodemap 노드↔식 귀속(N0~N9·N0′~N9′·N5+)**: 전수 정합 — eq:center 귀속 포함 오귀속 0. N5+ 수식은 eq:dSemolar 와 동치 확정.
4. **라벨·참조 무결성**: 대상 5본이 참조하는 라벨(자체 빌드 + xr 상대 장) 전수 실재 — 깨진 참조 0.
5. **appC 12행 재수록 정확성**: M2(지시어) 외 전 행이 원천 절 문구와 정합 — 부호·정의 왜곡 0. "재수록 전용·신규 내용 없음" charter 준수 확인.
6. **appB LCO_MSMR_LIT 데모 불일치 고지**: tab:lco-staging 캡션과 축자 정합(실제 값 상이도 코드로 확인) — 과대/과소 주장 없음.
7. **부호 사슬 ↔ 코드 부호 정합**: σ_d 슬롯(탈리튬화=+1)·LCO 라벨 자동 환산('charge'↦+1)·Bernardi I>0 라벨 층위 — 문건·코드·appC 3자 일관.
8. **P3 게이트 관점**: V_n 위계(S8·N1) 유지·전하 보존식이 U_oc 결정 중심식으로 유지(appD D.1)·x̄→U_oc→ξ 되먹임 순환이 "정의상 implicit formulation + 수치해법(이분법)" 으로 명시 분류돼 있음(논리 공백 아님)·ver.N 표기 미사용(명칭 혼동 무) — 위반 0. GS-1/GS-2 는 본 창 대상 밖(메우기 제안 없음 준수).
9. **서지**: 유일 외부 인용 swiderska2019 crossref 실검증 통과 — 서지 결함 0, 신규 문헌 필요 공백 0.

— 이상. (FR-A16 완료: H 1 · M 8 · L 4. 본 창 제안은 전건 대체·보강형 — 자산 삭제 제안 없음.)
