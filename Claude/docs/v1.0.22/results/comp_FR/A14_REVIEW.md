# A14_REVIEW — §2.6 (ch2_sec06_limits.tex) · §2.7 (ch2_sec07_revheat.tex) 심층 검토

- 검토 창: FR-A14 (v1.0.22 대공사) · BRIEF_FR_A.md 규율 준수(보고 전용 · 소스 수정 금지 · git 금지 · `Codex/` 접근 금지)
- 대상(전문 정독 완료):
  - `_sections/ch2_sec06_limits.tex` (§2.6 극한과 코너, 53행)
  - `_sections/ch2_sec07_revheat.tex` (§2.7 가역 발열 — Bernardi 출구, 103행)
  - ★명칭: 파일명은 `ch2_` 이나 두 파일 모두 **ch1_graphite_v1.0.22.tex 빌드의 Part T(열특성부)** 소속(역사적 파일명). LCO 챕터(ch2_lco_v1.0.22.tex)와 무관. sec07 말미 ∂_V↔∂_T 켤레 bgbox = [V22-SM2-C] 제거 용이 독립 블록 — 본 리뷰의 제안은 블록 내부 한정(독립성 유지).
- 참조 원문 확인(read-only): ch2_sec00_intro(범위 박스)·ch2_sec01_partition(eq:Vxi·eq:logistic·eq:BW·eq:Veq_BW·eq:slope_BW)·ch2_sec02_config(eq:Sconfig·eq:dSconfig·eq:dVdT_config·ssec:litverif·tab:ds)·ch2_sec03_vibel(eq:Se-ch2·ssec:elec·ssec:threedist)·ch2_sec05_mixing(eq:weighted·eq:single_config·eq:dxidT·ssec:weff·ssec:hys·eq:hys_rev·수치검증 srcbox)·ch2_sec08_synthesis(eq:complete·tab:worked·tab:qrev)·ch2_appA_traps(부록 C 함정표)·ch1_sec01_n0n1(σ_d 규약)·ch1_sec02a_part0(eq:sm-sint)·ch1_sec02b_part0(eq:sm-nernst)·ch1_graphite_v1.0.22.tex(조립 순서·부록 번호)·ch1v22_bib.tex(인용 키 실존)
- 상태: **진행 중(조기 저장)** — 발견 즉시 append. §서치(하이쿠 위임) 결과 대기 중.

## 진행 로그
- [x] BRIEF_FR_A.md 정독
- [x] 대상 2개 파일 전문 정독
- [x] 참조 라벨·인용 키 전수 대조(아래 무발견 축 참조)
- [x] §2.6 6코너 재유도·§2.7 부호 사슬 전체 재유도(아래 재계산 기록)
- [ ] 하이쿠 서브에이전트 문헌 검증(bernardi1985 항 구조·standardised2024 방법 성격) — 진행 중
- [ ] 4-tier 확정

---

## 발견 표

> 표기: 유형 = 보완/논리/설명/수식화. 여러 행에 걸친 현행·제안 원문은 표에는 `<br>`(개행 위치 표시)로 적고,
> 표 아래 **발견별 상세**의 fenced block 에 **개행 포함 축자 원문**을 그대로 둔다(기계 매칭용 원본 = fenced block).

| ID | 파일:행 | 유형 | 등급 | 현행(축자) | 제안(완성 LaTeX) | 근거 |
|----|---------|------|------|-----------|-----------------|------|
| A14-01 | ch2_sec06_limits.tex:25 | 논리 | H | `단일 봉우리 (겹침 0) & $=\Delta S_{\rxn,j}/F+$ config & 가중식~\eqref{eq:weighted} 이 단일 전이로 환원 \\` | `단일 봉우리 (겹침 0) & $=\Delta S_{\rxn,j}/F+$ config & 완전식(가중식~\eqref{eq:weighted}$+$config, \S\ref{ssec:blend}; 후술 종합식~\eqref{eq:complete})이 단일 전이식~\eqref{eq:single_config} 으로 환원 \\` | eq:weighted 는 boxed **단순식**(중심값만, §2.5:75–79 `\Big|_{\text{단순식}}` 명기). 단일 봉우리 한계에서 eq:weighted → ΔS_rxn,j/F 뿐(재유도 확인) — config 항은 완전식(eq:dxidT 둘째 조각 포함)에서만 나옴. 거동 열의 "+config" 와 인용식이 불일치(오귀속) |
| A14-02 | ch2_sec06_limits.tex:35–36 | 논리 | H | `(ii) 단일 봉우리 한계에서 가중식이 단일 전이 $+$ config 로 환원되므로 \eqref{eq:weighted} 가`<br>`\eqref{eq:single_config} 를 포함한다;` | `(ii) 단일 봉우리 한계에서 가중 완전식(\eqref{eq:weighted} 에 config 항을 더한 것, \S\ref{ssec:blend}; 후술 종합식~\eqref{eq:complete})이 단일 전이식 \eqref{eq:single_config} 로 환원되므로 완전식이 \eqref{eq:single_config} 를 포함한다;` | A14-01 과 같은 뿌리. 축자 그대로면 "단순식 ⊇ eq:single_config" 라는 거짓 포함 관계가 됨(eq:single_config 의 둘째 항 $n_jR\ln[\xi/(1-\xi)]/F$ 가 eq:weighted 에 없음). "후술 + 전방 식 참조" 는 §2.2:49–50 의 기존 관행(`후술 \S\ref{ssec:overlap} 식~\eqref{eq:dxidT}`)과 동일 |
| A14-03 | ch2_sec06_limits.tex:42–43 | 보완 | M | `따라서 $\Delta S_{\rxn,j}(x)$ 를 임의 함수로 둘 필요가 \emph{없다}: 전이당 \emph{상수}`<br>`표준값 $+$ 분포만으로 측정급 곡선이 나온다.` | `따라서 $\Delta S_{\rxn,j}(x)$ 를 임의 함수로 둘 필요가 \emph{없다}: 전이당 \emph{상수} 표준값 $+$ 분포만으로 측정급 곡선이 나온다(분포 몫은 폭의 열적 서식 $w_j=n_jRT/F$ 를 전제한 것 --- 전제 명시 \S\ref{ssec:blend} srcbox; 실측 두-상 폭이 $T$-동결에 가까우면 중심값 단순식이 보수적 기준, \S\ref{ssec:weff}).` | "측정급 곡선" 근거인 §2.5 수치검증 [C-82]가 명시적으로 "자기일관성 검증이지 실측 검증 아님·~0.3 mV/K 우열 뒤집힘"을 한정. §2.8 [C-104]도 매 사용처에서 이 한정을 반복. 판정 keybox 만 무한정 단언 — 본 파트 내 일관성 공백 |
| A14-04 | ch2_sec06_limits.tex:22 | 보완/설명 | M | `$\xi=\tfrac12$ (봉우리 중심) & $=\Delta S_{\rxn,j}/F$ & config$=0$; 중심 표준값 정확 회수(파생 B 일관) \\` | `$\xi=\tfrac12$ (봉우리 중심) & $=\Delta S_{\rxn,j}/F$ & config$=0$; 중심 표준값 정확 회수(단일 전이 지배 시, 식~\eqref{eq:single_config}; 겹침에선 인접 전이 몫이 남음 --- 파생 B 일관) \\` | "정확 회수"는 eq:single_config(단일 전이 지배 근사) 기준. 겹침 가중에선 ξ_j=½ 라도 인접 g_k≠0 몫이 남음 — §2.8 tab:worked 실증: 2→1 이 75% 지배인 점에서도 가중값 −0.204 ≠ 수준 −0.166 mV/K. 독자가 표끼리 대조하면 모순으로 읽힘 |
| A14-05 | ch2_sec07_revheat.tex:43–44 | 보완 | M | `\emph{방법 요지} --- Bernardi 등은 셀 에너지 보존에서 전기화학 반응(가역 엔트로피 $+$ 과전압 소산)$\cdot$상변화`<br>`$\cdot$혼합(농도구배 완화열)$\cdot$joule 발열을 모두 담은 일반 에너지 수지를 세운다.` | 대응표에 1행 추가:<br>`$I(U_\oc-V)$ 에 포함 & joule(옴) 발열 & 유지(단자 $V$ 기준 첫 항이 옴$\cdot$전하이동$\cdot$물질전달 분극을 합산) \\`<br>+ 방법 요지 문장 뒤 보강: `원식의 평형 전위는 평균 조성 평가($U_\mathrm{avg}$)이며, 준평형 저율(농도 균일) 전제에서 표면/평균 구분이 소멸해 본문 $U_\oc$ 와 일치한다.` | srcbox 방법 요지는 Bernardi 원 수지의 발열원 4종(반응·상변화·혼합·joule)을 열거하는데 항별 대응표는 3종만 배치(유지 2·소거 2) — joule 의 행선지가 표에 없음. 단자 V 기준 첫 항이 옴 강하 포함(과전압 소산의 통상 정의)이므로 "유지(첫 항에 흡수)"로 닫힘. U_avg 주석은 혼합항 소거 전제와 맞물리는 원식 충실성 보강. [서지 확인은 §서치 — 하이쿠 검증 결과 반영 예정] |
| A14-06 | ch2_sec07_revheat.tex:63–65 | 보완 | M | `식~\eqref{eq:qrev} 의 $\Delta S(x)$ 는 본 장이 세운 세 분포의 합이므로(\S\ref{ssec:threedist} 핵심 박스),`<br>`가역 발열은 한 충전상태에서 다른 충전상태로 넘어갈 때 \emph{Li 배열 분포$\cdot$포논 분포$\cdot$전자 분포를`<br>`재배열하며 주고받는 열}이다.` | 문단에 1문장 삽입(첫 문장 뒤): `히스테리시스가 있는 실측 곡선에서는 식~\eqref{eq:qrev} 의 $\partial U_\oc/\partial T$ 로 분기 평균~\eqref{eq:hys_rev} 의 $\partial U_\oc^\rev/\partial T$ 를 쓴다(파생 D \S\ref{ssec:hys}); 이때 $U_\oc$ 를 분기 평균으로 두면 히스 gap 의 소산은 $\dot Q_\irr=I(U_\oc-V)\ge0$ 쪽에 자동 포함된다(각 가지에서 $\tfrac12|I|\,\Delta U^\hys$ 씩 --- 한 사이클 합이 파생 D warnbox 의 $Q_\mathrm{cycle}\,\Delta U^\hys$ 소산과 일치).` | Bernardi 출구 절이 파생 D 의 처방(가역 발열 = 분기 평균 eq:hys_rev [C-90 CRITICAL])을 인용하지 않음 — 한 분기 OCV 로 eq:qrev 를 쓰는 실수 경로가 열려 있음. ½|I|ΔU^hys/가지 는 재유도로 확인(재계산 기록 R7): 사이클 합 = Q·ΔU^hys 로 §2.5 warnbox 와 자기일관. 최소 수용안 = 첫 절(분기 평균 지정)만 삽입 |
| A14-07 | ch2_sec07_revheat.tex:51–52 | 논리 | M | `본 절의 부호는 라벨이 아니라 전류 부호 $I$ 로 읽는다(충전은 $I<0$ 으로 자동 처리 --- 식은 방향에 선형이라 부호`<br>`하나로 닫힌다).` | `본 절의 부호는 라벨이 아니라 전류 부호 $I$ 로 읽는다(충전은 $I<0$ 으로 자동 처리 --- 가역 항은 $I$ 에 선형이라 부호가 뒤집히고, 소산 항은 $U_\oc-V$ 가 함께 뒤집혀 $\ge0$ 이 유지된다).` | "식은 방향에 선형" 을 eq:qrev 전체에 적용하면 오독: 첫 항 $I(U_\oc-V)$ 는 $I$ 에 선형이 아니라 $I$ 와 $(U_\oc-V)$ 가 동시 반전(사실상 짝수)해 충전에서도 $\ge0$. 선형 반전은 $\dot Q_\rev$ 에만 해당(재계산 기록 R4). 축자 그대로면 "충전 시 $\dot Q_\irr$ 부호도 반전"으로 잘못 읽힐 수 있음 |
| A14-08 | ch2_sec07_revheat.tex:79–81 | 설명 | M | `평형 전위의 Nernst 배치 항 $(RT/F)\ln[\xi/(1-\xi)]$`<br>`(식~\eqref{eq:Vxi}; \S\ref{sec:sm-macro} 식~\eqref{eq:sm-nernst})을 두 축으로 미분하면` | `평형 전위의 Nernst 배치 항 $(RT/F)\ln[\xi/(1-\xi)]$`<br>`(식~\eqref{eq:Vxi}; \S\ref{sec:sm-macro} 식~\eqref{eq:sm-nernst})을 두 축으로 미분하면 --- 전위 축은 역함수 미분 $\dd\xi/\dd V=[\dd V/\dd\xi]^{-1}$, 온도 축은 고정 $\xi$ 편미분 ---` | bgbox 내부 display 의 왼쪽 조각($\dd\xi/\dd V$)은 Nernst 항을 "V 로 미분"한 것이 아니라 $V(\xi)$ 를 뒤집은 역함수 미분(재계산 기록 R6). 현행 산문 "두 축으로 미분"만으로는 독자가 좌우 조각의 미분 대상이 다른 점($\xi$ 를 미분 vs $V$ 를 미분)에서 막힘. 제안은 bgbox 내부 한 구절 삽입 — 블록 독립성 유지 |
| A14-09 | ch2_sec07_revheat.tex:65–67 | 수식화 | M | `부호는 식~\eqref{eq:qrev} 가 곧장 정한다 --- 방전($I>0$)에서 $\Delta S>0$ 이면`<br>`$\dot Q_\rev<0$ 으로 \emph{흡열}(endothermic, 셀이 열을 흡수), $\Delta S<0$ 이면 $\dot Q_\rev>0$ 으로`<br>`\emph{발열}(exothermic)이다($\Delta S$ 는 Li 1몰(전자 1몰) 삽입 기준 J\,mol$^{-1}$K$^{-1}$).` | 인용문 마지막 문장 뒤 1행 추가: `한 줄로는 $\operatorname{sgn}\dot Q_\rev=-\operatorname{sgn}(I)\operatorname{sgn}\Delta S(x)$ 라, 충전($I<0$)의 흡$\cdot$발열은 방전의 정반대로 자동 닫힌다.` | 현행 산문은 방전 사분면 2개만 열거 — 충전 쪽은 §2.7.2 의 "I<0 자동 처리"에 암시로만 존재. sgn 항등식 1줄이 사분면 4개를 전부 닫고(eq:qrev 에서 직독, 재계산 기록 R4) 산문 열거를 대체 아닌 보강으로 압축 |
| A14-10 | ch2_sec06_limits.tex:19–20 | 보완 | L | `$\xi\to1$ (희박, Li-poor) & config $\to+\infty$ & 삽입 자리 선택지 폭증; 저-$x$ 큰 양 $\Delta S$($+29$)에 분담`<br>`기여(귀속 한정 \S\ref{sec:config}) \\` | `$\xi\to1$ (희박, Li-poor) & config $\to+\infty$ & 삽입 자리 선택지 폭증; 저-$x$ 큰 양 $\Delta S$($+29$ J\,mol$^{-1}$K$^{-1}$)에 분담 기여(귀속 한정 \S\ref{ssec:litverif} 표~\ref{tab:ds} 도입 문단) \\` | 귀속 한정의 실제 위치는 §2.2.4(ssec:litverif) tab:ds 도입 문단("+29 끝점은 config 겹침 자리 — 구간 대표 수준") — 절 단위 참조(sec:config)보다 소절 직지정이 검증 경로를 단축. 단위 병기는 표 자체 완결성(+29 만 단위 없이 노출) |
| A14-11 | ch2_sec06_limits.tex:36–37 | 설명 | L | `(iii) $\Omega\to2RT$ 에서 평형 등온선이 비단조로 뒤집혀 상분리 plateau 가`<br>`발생하므로, 상호작용 모형이 상전이 임계를 스스로 짚는다.` | `(iii) $\Omega=2RT$ 를 지나 $\Omega>2RT$ 가 되면 평형 등온선이 비단조로 뒤집혀 상분리 plateau 가 발생하므로, 상호작용 모형이 상전이 임계를 스스로 짚는다.` | 재유도(eq:slope_BW): 중앙 기울기 $(2\Omega-4RT)/F$ 는 $\Omega=2RT$ 에서 0(임계·plateau 발생 직전), 비단조 뒤집힘은 엄밀히 $\Omega>2RT$ 측. 표 본체(행 4)는 "\emph{$\Omega>2RT$ 측에서}"로 정확 — 요약문만 "$\Omega\to2RT$ 에서 뒤집혀"로 완화되어 표와 미세 불일치 |
| A14-12 | ch2_sec06_limits.tex:26–28 | 보완 | L | `고온 ($\kB T\!\sim\!E_F$ 근접) & electronic $\propto T$ 우세화 & Fermi--Dirac--Sommerfeld~\eqref{eq:Se-ch2} 는`<br>`축퇴 극한 $\kB T\!\ll\!E_F$ 전용 --- \emph{정성적} 방향(전자 기여 증대)만 유효, $\kB T\!\sim\!E_F$ 에선 정량`<br>`부적용 \\` | 셀 말미 보강: `... 정량 부적용(실용상 이 코너는 멀거나 무해 --- 금속성 host 는 $E_F\gg\kB T$; 흑연은 준금속이라 여유가 작으나 그 항 자체가 소수, \S\ref{ssec:elec}) \\` | 독자 질문 "이 코너에 실제로 닿는 경우가 있는가"에 본문·표 모두 무응답. §2.3 의 기존 자산([C-68] 흑연 준금속 ΔS_e≈0)으로 답이 이미 문서 안에 있음 — 한 구절 소환이면 닫힘. [금속 host $E_F\gg\kB T$ 는 일반 고체물리 상식 수준 서술 — 추정 tier] |
| A14-13 | ch2_sec07_revheat.tex:52·57·58·63 | 문체 | L | `이 라벨 충돌이 본 장에서 부호가 가장 크게 어긋날 수 있는 자리이며` (52) / `본 장은 평형 전위 $U_\oc$ 기준` (57) / `본 장 범위 밖` (58) / `본 장이 세운 세 분포의 합이므로` (63) | 4곳 `본 장` → `본 파트` (예: `이 라벨 충돌이 본 파트에서 부호가 가장 크게 어긋날 수 있는 자리이며`) | v1.0.22 재편으로 구 Ch2 가 Ch1 의 Part T 가 됨 — "본 장"의 지시 대상이 Ch1 전체로 확장되어 정밀도 저하(내용상 거짓은 없음 — 4곳 모두 Ch1 전체로 읽어도 참임을 확인). 단 **문서 전반 공통 잔재**(ch2_sec01/02/03/04/05/08/09 에도 "본 장" 존재) — sec07 만 고치면 오히려 비일관. 일괄 치환 여부는 사용자 결정 경계(P5)로 이관 권고 |
| A14-14 | ch2_sec07_revheat.tex:86–87 | 문체 | L | `뒤 조각이 정확히 겹침 가중 완전식의 봉우리 내부 config 항 $+n_jR\ln[\xi/(1-\xi)]/F$`<br>`(식~\eqref{eq:single_config})이자 가역 발열 $\dot Q_\rev$ 의 배치 몫이다.` | `뒤 조각이 정확히 겹침 가중 완전식의 봉우리 내부 config 항 $+n_jR\ln[\xi/(1-\xi)]/F$`<br>`(식~\eqref{eq:single_config}; 위 전개는 $n_j{=}1$ 서식)이자 가역 발열 $\dot Q_\rev$ 의 배치 몫이다.` | bgbox display 는 eq:Vxi(폭 $RT/F$, $n_j{=}1$)에서 유도되어 $R/F$ 가 나오는데 직후 일반형 $n_jR/F$ 와 등치 — "정확히"가 성립하는 서식($n_j{=}1$)을 한 구절로 명시(§2.2:49 의 같은 처리와 정합). bgbox 내부 한정 — 독립성 유지 |
| A14-15 | ch2_sec07_revheat.tex:71–72 | 보완(서지) | 보류→§서치 | `이는 calorimetry 의 가역 발열 직접 관측과 정합한다 \cite{standardised2024}.` | (하이쿠 검증 후 확정 — standardised2024 가 potentiometric 방법 논문으로 확인되면 `이는 가역 발열 파라미터화의 표준화 측정과 정합한다 \cite{standardised2024}` 류로 성격 교정 필요) | bib 원문(ch1v22_bib.tex:42) 제목이 "A Standardised **Potentiometric** Method ..." — 전위법(∂U/∂T 측정)이지 열량계 직접 관측이 아닐 가능성. 논문이 calorimetry 교차검증을 포함하는지 하이쿠로 확인 중 — 확인 전 미검증 |

---

## 발견별 상세 (축자 원문 — 기계 매칭용)

### A14-01 · A14-02 (H) — eq:weighted(단순식) 오귀속
현행 축자 (ch2_sec06_limits.tex:25):
```latex
단일 봉우리 (겹침 0) & $=\Delta S_{\rxn,j}/F+$ config & 가중식~\eqref{eq:weighted} 이 단일 전이로 환원 \\
```
현행 축자 (ch2_sec06_limits.tex:33–37 — (ii) 부분):
```latex
(ii) 단일 봉우리 한계에서 가중식이 단일 전이 $+$ config 로 환원되므로 \eqref{eq:weighted} 가
\eqref{eq:single_config} 를 포함한다;
```
재유도: eq:weighted(§2.5:74–79)는 `\boxed{\;\frac{\partial U_\oc}{\partial T}(x)\Big|_{\text{단순식}} = \frac{\sum_j Q_j\,g_j(x)\,(\partial U_j/\partial T)}{\sum_j Q_j\,g_j(x)} = ...}` — **단순식 라벨이 박스 안에 명기**되어 있고, 단일 봉우리($g_{k\ne j}\to0$) 대입 시 분자·분모의 $Q_jg_j$ 상쇄로 $\Delta S_{\rxn,j}/F$ **만** 남는다. config 항 $n_jR\ln[\xi_j/(1-\xi_j)]/F$ 는 eq:dxidT 둘째 조각을 마저 넣은 **완전식**(§2.5 ssec:blend 산문 정의, 라벨은 §2.8 eq:complete)에서만 발생. 따라서 표 행 5 의 거동값("+config")과 검증 열의 인용식(eq:weighted), 그리고 (ii) 의 포함 주장("eq:weighted ⊇ eq:single_config")이 성립하지 않는다. eq:single_config 의 둘째 항이 eq:weighted 에 없으므로 "포함"은 거짓 — 인용 대상을 완전식(eq:complete 전방 참조 또는 §ssec:blend)으로 교정해야 함. 전방 식 참조는 §2.2:49–50 `(후술 \S\ref{ssec:overlap} 식~\eqref{eq:dxidT})` 로 기존 관행.

### A14-03 (M) — "상수+분포" 판정 keybox 의 전제 한정 누락
현행 축자 (ch2_sec06_limits.tex:39–47 keybox 중 42–43):
```latex
따라서 $\Delta S_{\rxn,j}(x)$ 를 임의 함수로 둘 필요가 \emph{없다}: 전이당 \emph{상수}
표준값 $+$ 분포만으로 측정급 곡선이 나온다. 이 근사는 \emph{중심 표준값(vib$+$electronic 중심)이 전이 폭 안에서
천천히 변할 때} 타당하다.
```
근거: 이 판정의 수치 근거(§2.5 srcbox [C-81])는 스스로 "★전제 명시 — ... 해석 미분 사슬의 자기일관성 검증이지 ... 실측 검증이 아니다. 만일 실측 $w_j$ 가 $T$-동결에 가깝다면 단순식/완전식의 우열이 뒤집히는 $\sim$0.3 mV/K 급 차이"([C-82])라고 한정했고, §2.8 도 종합식 keybox 아래·worked (e)·tab:qrev 캡션에서 세 차례 반복 한정([C-104]·[C-113]). 유일하게 **판정 그 자체를 선언하는 §2.6 keybox 에만** 이 한정이 없다 — keybox 만 읽는 독자(요약 소비자)가 "측정급"을 무조건부로 수용할 경로. 타당 조건 문장("중심 표준값이 천천히 변할 때")은 **다른** 전제(중심 흡수)만 다루므로 대체가 안 됨. 제안은 keybox 문장에 괄호 한정 1구 추가(발견 표 참조) — 기존 문장 삭제 없음.

### A14-04 (M) — ξ=½ 코너의 "정확 회수" 적용 조건
현행 축자 (ch2_sec06_limits.tex:22):
```latex
$\xi=\tfrac12$ (봉우리 중심) & $=\Delta S_{\rxn,j}/F$ & config$=0$; 중심 표준값 정확 회수(파생 B 일관) \\
```
근거: config$=0$ 은 $\ln1=0$ 으로 무조건 성립(재계산 확인). 그러나 "$=\Delta S_{\rxn,j}/F$ 정확 회수"는 단일 전이 지배(eq:single_config)에서만 등식 — 겹침 가중 완전식에서는 $\xi_j=\tfrac12$ 인 지점에도 인접 전이의 $Q_kg_k\ne0$ 몫이 남는다. 문서 내 실증: §2.8 tab:worked 의 $\bar x{=}0.25$ 는 2→1 이 75% 지배임에도 가중값 $-0.204$ mV/K ≠ 수준 $-0.166$ mV/K. 독자가 tab:limits 행 3 과 tab:worked 를 대조하면 모순으로 읽을 수 있는 자리 — "단일 전이 지배 시" 한정 1구가 닫는다. (행 1·2 의 ±∞ 발산은 전 SOC 창 양끝에서 발생 — 그 자리에선 인접 가중이 지수적으로 소멸해 한정 불요, §2.5 srcbox "그리드 양끝 스팬-의존"과 정합.)

### A14-05 (M) — Bernardi 다리 srcbox: joule 행 부재 + $U_\mathrm{avg}$ 주석
현행 축자 (ch2_sec07_revheat.tex:43–44):
```latex
\emph{방법 요지} --- Bernardi 등은 셀 에너지 보존에서 전기화학 반응(가역 엔트로피 $+$ 과전압 소산)$\cdot$상변화
$\cdot$혼합(농도구배 완화열)$\cdot$joule 발열을 모두 담은 일반 에너지 수지를 세운다.
```
현행 축자 (같은 srcbox 대응표, ch2_sec07_revheat.tex:32–41):
```latex
\begin{tabular}{@{}lll@{}}
\hline
본문(식~\eqref{eq:qrev}) & Bernardi\cite{bernardi1985} 항 & 본문 처리 \\
\hline
$I(U_\oc-V)$ & 과전압 소산(반응 비가역) & 유지 \\
$-IT\,\partial U_\oc/\partial T$ & 반응 가역 엔트로피 & 유지 \\
--- & 혼합 엔탈피(농도구배 완화) & 소거(준평형 저율) \\
--- & 상변화 항 & 소거($U_\oc(x)$ 에 흡수) \\
\hline
\end{tabular}
```
근거: srcbox 의 선언된 용도가 "항별 대응"인데, 방법 요지가 열거한 발열원 4종 중 **joule 발열만 대응표에 행이 없다**(유지 2·소거 2 로 3종만 처리). 독자 즉문 "joule 은 어디로 갔나"에 답이 없음. 물리적 답: 본문 $V$ 가 **단자 전압**이므로 첫 항 $I(U_\oc-V)$ 의 총 분극이 옴 강하를 포함(과전압 소산 항에 흡수 — "Part I 의 동역학 꼬리·분극" 서술과 정합). 제안 = 대응표 1행 추가 + $U_\mathrm{avg}$(평균 조성 평가) 주석 1문장(혼합항 소거 전제와 맞물림). 원 논문의 항 구조·표현은 §서치의 하이쿠 검증 결과로 확정(검증 전 "유지(첫 항에 흡수)" 문구는 추정 tier).

### A14-06 (M) — 히스테리시스 시 eq:qrev 의 입력 지정(분기 평균) 부재
현행 축자 (ch2_sec07_revheat.tex:63–65):
```latex
식~\eqref{eq:qrev} 의 $\Delta S(x)$ 는 본 장이 세운 세 분포의 합이므로(\S\ref{ssec:threedist} 핵심 박스),
가역 발열은 한 충전상태에서 다른 충전상태로 넘어갈 때 \emph{Li 배열 분포$\cdot$포논 분포$\cdot$전자 분포를
재배열하며 주고받는 열}이다.
```
근거: §2.5 파생 D 가 "가역 발열에 들어가는 것은 두 분기의 평균"(eq:hys_rev, [C-90] CRITICAL)을 세웠는데, 정작 가역 발열 출구 절(§2.7)은 eq:qrev 의 $\partial U_\oc/\partial T$ 가 어느 곡선(분기/평균)인지 지정하지 않는다. 실측 OCV 는 분기별로만 존재하므로, 한 분기 $\partial U^{(d)}/\partial T$ 를 그대로 넣는 실수 경로가 열려 있음(파생 D warnbox 가 경고한 "가역/비가역 섞기"의 실행 지점이 바로 여기). 재유도(재계산 기록 R7): $U_\oc:=U^\rev$(분기 평균)로 두면 리튬화 가지 $V\approx U^\rev-\tfrac12\Delta U^\hys-\eta$ 에서 $\dot Q_\irr=I(U^\rev-V)=I\eta+\tfrac12 I\,\Delta U^\hys\ge0$, 탈리튬화 가지($I<0$)에서도 동형 — 사이클 합 $Q_\mathrm{cycle}\Delta U^\hys$ 로 §2.5 warnbox 의 소산율과 정확히 일치. 곧 분기 평균 지정 하나로 (i) 가역 몫은 eq:hys_rev, (ii) 히스 소산은 $\dot Q_\irr$ 슬롯 자동 포함이 동시에 닫힌다. 최소 수용안 = 제안문 첫 절(분기 평균 지정)만.

### A14-07 (M) — "식은 방향에 선형" 의 적용 범위
현행 축자 (ch2_sec07_revheat.tex:51–53):
```latex
본 절의 부호는 라벨이 아니라 전류 부호 $I$ 로 읽는다(충전은 $I<0$ 으로 자동 처리 --- 식은 방향에 선형이라 부호
하나로 닫힌다).
```
근거(재계산 기록 R4): eq:qrev 두 항 중 $\dot Q_\rev=-IT\,\partial U_\oc/\partial T$ 만 $I$-선형(방향 반전 시 부호 반전). $\dot Q_\irr=I(U_\oc-V)$ 는 방향 반전 시 $(U_\oc-V)$ 도 함께 반전해 **부호 불변**($\ge0$ 유지) — "선형이라 부호 하나로 닫힌다"를 식 전체에 적용해 읽으면 충전 시 $\dot Q_\irr<0$(2법칙 위반)로 오독 가능. 제안은 두 항의 닫힘 기제를 각각 명시(발견 표 참조).

### A14-08 (M) — bgbox "두 축으로 미분" 의 역함수 미분 명시
현행 축자 (ch2_sec07_revheat.tex:79–84):
```latex
평형 전위의 Nernst 배치 항 $(RT/F)\ln[\xi/(1-\xi)]$
(식~\eqref{eq:Vxi}; \S\ref{sec:sm-macro} 식~\eqref{eq:sm-nernst})을 두 축으로 미분하면
\[
\frac{\partial}{\partial V}:\ \ \frac{\dd\xi}{\dd V}=\frac{\xi(1-\xi)}{w}\quad(\text{peak},\ \propto\mathrm{var});
\qquad
\frac{\partial}{\partial T}:\ \ \frac{R}{F}\ln\frac{\xi}{1-\xi}\quad(\text{부분몰 배치 엔트로피}/F),
\]
```
근거(재계산 기록 R6): 좌 조각은 $V(\xi)$ 를 $\xi$ 로 미분한 뒤 **뒤집은** 역함수 미분($\dd V/\dd\xi=w/[\xi(1-\xi)]$ 의 역수), 우 조각은 고정 $\xi$ 의 $T$-편미분 — 두 "미분"의 피연산이 다르다($\xi$ 를 얻는 미분 vs 계수 $RT/F$ 를 훑는 미분). 수식 자체는 둘 다 정확(재유도 일치)하나 산문 "두 축으로 미분하면"이 이 비대칭을 감춰 독자가 "$\ln$ 항을 $V$ 로 미분했는데 왜 $\xi(1-\xi)/w$ 인가"에서 막힌다. 제안 = 산문에 짧은 삽입구(발견 표) — bgbox 내부 한정, 블록 독립성 유지.

### A14-09 (M) — 흡·발열 사분면의 sgn 1줄 닫음
현행 축자 (ch2_sec07_revheat.tex:65–67):
```latex
부호는 식~\eqref{eq:qrev} 가 곧장 정한다 --- 방전($I>0$)에서 $\Delta S>0$ 이면
$\dot Q_\rev<0$ 으로 \emph{흡열}(endothermic, 셀이 열을 흡수), $\Delta S<0$ 이면 $\dot Q_\rev>0$ 으로
\emph{발열}(exothermic)이다($\Delta S$ 는 Li 1몰(전자 1몰) 삽입 기준 J\,mol$^{-1}$K$^{-1}$).
```
제안(완성 LaTeX — 인용 구절 뒤 문장 추가):
```latex
한 줄로는 $\operatorname{sgn}\dot Q_\rev=-\operatorname{sgn}(I)\,\operatorname{sgn}\Delta S(x)$ 라,
충전($I<0$)의 흡$\cdot$발열은 방전의 정반대로 자동 닫힌다.
```
근거: 현행은 사분면 4개 중 방전 2개만 산문 열거 — 충전 2개는 §2.7.2 의 "$I<0$ 자동 처리"에서 독자가 스스로 조합해야 함. eq:qrev 에서 직독되는 sgn 항등식(재계산 기록 R4)이 4사분면을 1줄로 닫음. 산문→수식 간결화(보강 — 기존 문장 유지).

---

## 재계산 기록 (검증 완료분 — 전부 독립 재유도)

- **R1 (§2.6 표 행 1–3)**: eq:dVdT_config 의 config 항 $(n_jR/F)\ln[\xi/(1-\xi)]$ — $\xi\to1$ ⇒ $+\infty$ ✓, $\xi\to0$ ⇒ $-\infty$ ✓, $\xi=\tfrac12$ ⇒ $\ln1=0$ ✓ (규약 $\xi$=탈리튬화 진행률, §2.2 부호 3분기와 배향 일치 ✓). 가중식에서도 전 SOC 창 양끝 발산은 생존(끝 전이의 가중이 분자·분모에서 상쇄) ✓.
- **R2 (§2.6 표 행 4)**: eq:Veq_BW 미분 → $\dd V_\eq/\dd\theta=-\tfrac{RT}{F}\tfrac1{\theta(1-\theta)}+\tfrac{2\Omega}F$; $\theta=\tfrac12$ 에서 $(2\Omega-4RT)/F$ — $\Omega=2RT$ 임계 ✓, 비단조(중앙 양 기울기)는 $\Omega>2RT$ 측 ✓ (→ A14-11 의 요약문 미세 불일치만 지적).
- **R3 (§2.6 표 행 5)**: eq:weighted 단일 봉우리 대입 → $\Delta S_{\rxn,j}/F$ **만**(config 무) — 표·산문의 "+config·포함" 주장은 완전식(eq:complete) 몫 (→ A14-01·02, H).
- **R4 (§2.7 부호 사슬 전체)**: $\Delta G=-FU_\oc$, $\Delta S=-\partial\Delta G/\partial T=+F\,\partial U_\oc/\partial T$ ✓ → $\dot Q_\rev=-IT\,\partial U_\oc/\partial T=-(IT/F)\Delta S$ ✓. 1법칙 재유도: 방전 $I>0$ 에서 반응 진행률 $I/F$, $\dot H=(I/F)(-FU_\oc+TF\,\partial U_\oc/\partial T)$, $\dot Q_\mathrm{gen}=-\dot Q_\mathrm{in}=I(U_\oc-V)-IT\,\partial U_\oc/\partial T$ — eq:qrev 와 항·부호 완전 일치 ✓. 흡·발열 판정(방전 ΔS>0 → 흡열 등) ✓ §2.8 tab:qrev 5점의 부호와 전부 정합 ✓. $\dot Q_\irr=I(U_\oc-V)$: 방전 $(+)(+)$, 충전 $(-)(-)$ → 항상 $\ge0$ ✓(단 $I$-선형 아님 → A14-07). 전셀 음극 몫: $\partial U_\cell/\partial T=\partial U_\mathrm{cat}/\partial T-\partial U_\mathrm{an}/\partial T$ ⇒ $+IT\,\partial U_\mathrm{an}/\partial T$ ✓.
- **R5 (§2.7 라벨 층위)**: 흑연 하프셀(흑연 vs Li 금속)에서 흑연이 양극(전위 $>0$ vs Li/Li⁺) → 전기화학적 셀 방전 = 흑연 환원 = **리튬화** ✓. Part I 규약 원문 확인(ch1_sec01_n0n1.tex:14 `\sigma_d=+1` 방전 · :29–30 "방전($\sigma_d=+1$)은 $V\uparrow\Rightarrow\xi_\eq\uparrow$(전위를 올리면 탈리튬화)") — 같은 단어 반대 화학 방향 주장 ✓ 사실.
- **R6 (bgbox 수학)**: $V(\xi)=U_j+(RT/F)\ln\tfrac{\xi}{1-\xi}$ ⇒ $\dd V/\dd\xi=w/[\xi(1-\xi)]$ ⇒ 역수 $\dd\xi/\dd V=\xi(1-\xi)/w=g_j$ ✓ = eq:gj ✓ = var$(n)/w$ (eq:sm-flucres $\mathrm{var}=\theta(1-\theta)=\xi(1-\xi)$) ✓. $T$-편미분(고정 $\xi$) = $(R/F)\ln[\xi/(1-\xi)]$ ✓ = $(1/F)\,\partial S_\config/\partial\theta|_{\theta=1-\xi}$ (eq:dSconfig 부호 포함) ✓ = eq:single_config 둘째 항($n_j{=}1$) ✓. eq:sm-sint 원문 대조(ch1_sec02a_part0.tex:321–325) ✓ · eq:sm-nernst 원문 대조(ch1_sec02b_part0.tex:439–446, $s{=}+1$) ✓. 가드(가역 한정·히스 소산 별개)는 §2.5 파생 D warnbox 와 정합 ✓.
- **R7 (분기 평균 → Bernardi 슬롯 배정, A14-06 제안 검증)**: 리튬화 가지 중심 $U^\mathrm{lith}=U^\rev-\tfrac12\Delta U^\hys$(σ_d 규약: dis=탈리튬화 $+\tfrac12$ 위 가지 — §2.5 파생 D), $V=U^\mathrm{lith}-\eta$ ⇒ $I(U^\rev-V)=I\eta+\tfrac12I\Delta U^\hys$; 탈리튬화 가지 $I<0$, $V=U^\mathrm{delith}+\eta'$ ⇒ $I(U^\rev-V)=|I|\eta'+\tfrac12|I|\Delta U^\hys$. 사이클 합(히스 몫) $=Q_\mathrm{cycle}\Delta U^\hys$ — §2.5 파생 D warnbox 의 소산율 표현과 일치 ✓.
- **R8 (차원·단위)**: $[IT/F\cdot\Delta S]$ = A·K·(C/mol)⁻¹·J mol⁻¹K⁻¹ = W ✓. $R/F=0.0862$ mV/K 스케일 ✓(±0.21/0.35 mV/K 급 config 항과 정합).
- **R9 (구조 참조)**: "부록 C 의 함정표" — 마스터 조립(ch1_graphite_v1.0.22.tex:50–53) 순서상 ch2_appA_traps = 세 번째 부록, 그 표제 원문 "부록 C --- 열특성 기호·부호 함정 검산표" ✓ 번호 정합. "상단 범위 박스" = ch2_sec00_intro warnbox(범위 — 코인 하프셀 단독) ✓ 실존. "다음 절 = 종합식+수치 예제" = §2.8 ✓.

---

## 등급별 정리

### H (논리/물리 오류·오귀속) — 2건 (한 뿌리)
- **A14-01·A14-02**: §2.6 이 단일 봉우리 코너의 "+config 환원"을 **단순식 eq:weighted** 에 귀속 — eq:weighted 는 박스에 "단순식" 명기된 중심값 식이라 config 항이 없고, "eq:weighted 가 eq:single_config 를 포함한다"는 축자 그대로는 거짓 포함 관계. 인용 대상을 완전식(§ssec:blend / 후술 eq:complete)로 교정하는 2곳 수정이면 닫힘(물리 주장 자체는 옳음 — 인용식 오귀속).

### M (의미·이해 실질 개선) — 7건
- **A14-03**: 판정 keybox 에만 $w_j(T)$ 열적 서식 전제 한정 부재(§2.5 [C-82]·§2.8 [C-104]와 비일관).
- **A14-04**: ξ=½ "정확 회수"에 단일 전이 지배 한정 필요(tab:worked 와 대조 시 겉보기 모순).
- **A14-05**: Bernardi 다리 srcbox — joule 행 부재(방법 요지 4종 vs 대응표 3종) + $U_\mathrm{avg}$ 주석.
- **A14-06**: 히스테리시스 실측에서 eq:qrev 입력 = 분기 평균(eq:hys_rev) 지정 부재 — 파생 D CRITICAL 자산의 출구 연결 공백.
- **A14-07**: "식은 방향에 선형" — 가역 항 한정으로 정밀화($\dot Q_\irr$ 는 짝수).
- **A14-08**: bgbox "두 축으로 미분" — 역함수 미분/고정-ξ 편미분 비대칭 명시.
- **A14-09**: 흡·발열 사분면 sgn 항등식 1줄 보강(충전 쪽 자동 닫음).

### L (문체) — 5건
- **A14-10**: 귀속 한정 참조를 §ssec:litverif(표 도입 문단)로 직지정 + $+29$ 단위 병기.
- **A14-11**: 골격 (iii) "$\Omega\to2RT$ 에서 뒤집혀" → "$\Omega>2RT$" (표 본체와 표현 통일).
- **A14-12**: 고온 코너의 실효성 1구(멀거나 무해 — [C-68] 소환).
- **A14-13**: "본 장" 4곳 → "본 파트" — 단 문서 전반 공통 잔재라 일괄 결정 사안(사용자 결정 경계로 이관).
- **A14-14**: bgbox $n_j{=}1$ 서식 명시 1구.

### 보류(§서치 결과 대기) — 1건
- **A14-15**: standardised2024 를 "calorimetry 의 가역 발열 직접 관측"으로 성격 규정한 문장 — bib 제목은 "Potentiometric Method". 하이쿠 검증 후 H(오귀속)/무발견 판정.

---

## §서치 (하이쿠 서브에이전트 위임 — 진행 중)

(결과 수신 후 이 절에 통합: bernardi1985 원 수지의 항 구조·joule 처리·$U_\mathrm{avg}$ 표기, standardised2024 의 방법 성격. doi 실검증분만 표로.)

---

## 4-tier (작성 중 — §서치 통합 후 확정)

## 무발견 축 (검토했으나 문제 없음)

- **eq:qrev 부호 사슬 전체**(ΔG→ΔS→Q̇_rev→흡·발열 사분면→전셀 음극 부호 반전→Q̇_irr≥0 양방향): 독립 재유도로 전부 일치 — 무발견 (R4).
- **라벨 층위 경고(§2.7.2) 자체의 사실성**: 하프셀 방전=리튬화 vs Part I σ_d=+1 방전=탈리튬화 — 원문 대조·전기화학 재확인 결과 경고 내용 정확 (R5).
- **§2.6 표 행 1·2·3·4 의 수학**(발산 부호·임계 Ω=2RT·config=0): 재유도 일치 (R1·R2). 행 6 의 축퇴 극한 한정 서술도 Sommerfeld 유도(§2.3)와 정합.
- **bgbox [V22-SM2-C] 의 수식 전부**(두 미분 조각·var 동일시·eq:sm-sint/eq:sm-nernst 원문 대조·가드): 재유도·대조 일치 (R6) — 발견은 설명(A14-08)·문체(A14-14)뿐. 블록 독립성 훼손 발견 없음(외부에서 이 블록을 참조하는 라벨 없음 확인).
- **참조 무결성**: tab:limits·eq:weighted·eq:single_config·eq:Se-ch2·eq:Vxi·eq:sm-nernst·eq:sm-sint·ssec:weff·ssec:overlap·ssec:elec·ssec:threedist·ssec:hys·sec:eqpeak·sec:sm-macro·sec:config 라벨 전부 실존(대상: A14-01 의 인용 '대상 선택' 오류 1건 외 끊어진 참조 없음). 인용 키 bernardi1985·newman·msmr_partI·standardised2024·hysteresis2018 모두 ch1v22_bib.tex 실존.
- **구조 참조**: "부록 C 함정표"(조립 순서상 세 번째 부록, 표제 일치)·"상단 범위 박스"(§2.0 warnbox)·"다음 절 종합식+예제"(§2.8) 전부 정합 (R9).
- **P3-2(전하 보존 중심식)**: §2.7 이 U_oc 를 OCV 읽기로 회귀시키지 않음 — eq:qrev 의 U_oc 는 §2.5 음함수(eq:implicit)·§2.8 계산 순서(음함수 풀이→되먹임)와 정합 유지.
- **P3-7(명칭)**: 두 파일 내 ver.N/Chapter 혼동 없음("본 장" 정밀도 저하는 A14-13 별도).
- **GS-1/GS-2**: 본 두 절과 무관(Ch3 소속 정직 공백) — 메우기 제안 없음.
