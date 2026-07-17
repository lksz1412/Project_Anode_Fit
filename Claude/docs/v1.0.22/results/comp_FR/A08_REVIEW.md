# A08_REVIEW — FR-A08 심층 검토 (§7 두-상 broadening, `ch1_sec07_broadening.tex`)

- 검토 창: FR-A08 (v1.0.22 대공사, BRIEF_FR_A.md 준수 — **보고 전용**: 소스 무수정·git 무조작·`Codex/` 미접근)
- 대상: `Claude/docs/v1.0.22/_sections/ch1_sec07_broadening.tex` (358행, 전문 정독)
- 참조 원문(read-only 확인): `ch1_sec05_width.tex`(이중지위·eq:wbase·폴백)·`ch1_sec06_eqpeak.tex`(eq:eqpeak·eq:belliden)·`ch1_sec04_hys.tex`(eq:Veq·eq:spinodal·eq:dUhys)·`ch1_sec08_lag.tex`(L_V∝|I|)·`ch1_sec09_tail.tex`(eq:lag)·`ch1_sec10_sum.tex`(tab:staging)·`ch1_sec01_n0n1.tex`(fig:staging)·`ch1_sec11_lcointro.tex`(tier 각주 원본)·`ch2_sec05_mixing.tex`(ssec:weff 각주)·`ch1_graphite_v1.0.22.tex`(빌드·xr)·`ch1v22_bib.tex`·`results/V1022_REFERENCE_LEDGER.md`(V1 원장, v1.0.21 승계)
- 4관점 전부 수행: ①내용 보완(빡세게) ②논리 오류(재계산·재유도 검증 — §V 검증 로그) ③더 쉬운 설명 ④산문→수식 간결화
- 규율 확인: bgbox 증축분(CLT box·tier 범례 각주)은 제거 용이 독립 블록 — 본 보고의 해당 제안(M1·M2)은 box **내부 자구 대체**만이라 독립성 불변. GS-1/GS-2(Ch3 Si 정직 공백)는 본 절 무관 — 메움 제안 없음. 모든 제안은 대체·보강(삭제 없음).
- 상태: **최종본** (수치 검증 §V·문헌 서치 §S 통합 완료)

---

## 발견 총괄 표 (BRIEF 양식 — 현행 열은 원문 축자 부분열, 전문 축자는 아래 상세 절)

| ID | 파일:행 | 유형 | 등급 | 현행(축자 — 부분열) | 제안(요지 — 완성 LaTeX 는 상세 절) | 근거 |
|----|---------|------|------|-----------|-----------------|------|
| A08-H1 | ch1_sec07_broadening.tex:309 | 논리 | H | `셋을 한꺼번에 흡수하는 것이 \emph{현상학적 자유 피팅 폭}이며 ---` | `②$\otimes$③ 을 한꺼번에 흡수하는 것이 \emph{현상학적 자유 피팅 폭} $w_j$ 이고, ① 은 별도 축 $L_{V,j}$ 가 담당한다(합치면 이중계산 --- 식~\eqref{eq:widthbudget}) ---` | 본문 120–123행·157–164행의 이중계산 금지 규정과 keybox 자기모순 |
| A08-M1 | ch1_sec07_broadening.tex:135 | 논리 | M | `이고, 어느 하나도 총분산을 지배하지 않는다는 Lindeberg 조건 아래 중심극한정리(CLT)가` | Lindeberg 정의 gloss 를 "꼬리 몫 소멸(무지배를 함의)"로 정정 | 무지배(Feller)만으로 CLT 불성립 — 반례 재유도(§V-9) |
| A08-M2 | ch1_sec07_broadening.tex:141–142 | 논리 | M | `\emph{형상} 근거이자 그 분산` + `가법(현행은 ``모양과 무관한 합성곱 항등식'')의 CLT 재유도를 준다` | CLT 는 형상만 공급, 분산 가법은 독립성 항등으로 귀속 정정 | 가법은 CLT 의 전제·부산물이지 결과 아님(§V-10) |
| A08-M3 | ch1_sec07_broadening.tex:226–227 | 논리 | M | `세 척도($\sigma_\mathrm{int}$·$\sigma_\mathrm{sym}$·꼬리 길이 $L_V$)는` + `치수선 길이로 직접 대비된다.` | σ 치수선(±σ, 길이 2σ)과 L_V 치수선(길이 L_V)의 2배 눈금 차 명시 or 반스팬 통일 | 그림 좌표 재검증: 치수선 3.62/5.80/1.50 vs 척도 1.81/2.90/1.50(§V-4) |
| A08-M4 | ch1_sec07_broadening.tex:293–294 | 설명 | M | `(분포는 폭을` + `\emph{넓힐} 뿐 평형 중심 $U_j$ 를 옮기지 않는다 --- (iii-b) 의 GITT 한정과 동일\cite{park2021})` | "산포=폭, 평균 $\bar\eta$=관측 중심 이동 가능하되 $U_j$(파라미터) 불변" 구분 | CLT box 의 $\mathcal N(\bar\eta,\sigma_\eta^2)$ 평균과 표면 충돌로 읽힘 |
| A08-M5 | ch1_sec07_broadening.tex:46–48 | 설명 | M | `plateau` + `양끝이 첫째 부류와 같은 연속 등온선이라 그 경계가 무한히 날카롭지 않고 폭 $\sim RT/F$ 규모(수십 mV order)로 번진 데서` | binodal 접속 → "가지 몫까지 한 봉우리로 읽힌 유효 폭" 기작 한 절 보강 | 델타 자체는 델타로 남는데 왜 폭이 생기는지 독자 질문에 현행 미답 |
| A08-M6 | ch1_sec07_broadening.tex:175–176 | 보완 | M | `비대칭 꼬리는 $L_{V,j}$ 가 담당하며 $|I|\!\to\!0$ 에서 소멸해 두 축이 전류` + `의존성으로도 갈린다` | ③ 동역학 몫도 |I| 와 함께 줄되 대칭으로 줄고, 항등 소멸은 비대칭 축뿐임을 한정 | 125–127행(③ 의 동역학 몫 소멸)과의 정합 명시 필요 |
| A08-M7 | ch1_sec07_broadening.tex:119 뒤 | 보완 | M | `broadening 층이며, $\eta$ 의 \emph{입자간 산포}를 평균한다.` | $\rho(U_\app)$ 의 가중 규약(용량 가중; (i) 사이즈 소거로 수 가중과 일치) 1문장 | 앙상블 평균의 표준 사독 질문 — 현행 미규정 |
| A08-M8 | ch1_sec07_broadening.tex:107–109 | 보완 | M | `과전압$\cdot$국소 접촉 저항$\cdot$국소 환경(결정성$\cdot$흑연화도$\cdot$turbostratic 무질서가 \emph{유효 장벽$\cdot$국소` | η 의 입자 공통(평균) 몫은 §pol 의 lumped $R_n$ 에 계상, ③ 은 편차만 — 이중계산 경계 1문장 | $R_n$(eq:vn)과 접촉저항 η 의 회계 경계가 현행 미답 |
| A08-M9 | ch1_sec07_broadening.tex:32 뒤 | 수식화 | M | (§7.1 전체 산문 분류 — 12–32행) | 전이 분류 요약표(2행) 추가 | 산문 21행의 분류 결과를 표 1개로 고정 — ④관점 |
| A08-M10 | ch1_sec07_broadening.tex:117–119 | 수식화 | M | `곧 단일 입자 응답 $(\dd Q/\dd V)^\mathrm{single}_{U_\app}$(평형 델타에 ② 내재 폭이 얹힌 좁은 peak)을 \emph{겉보기 중심}` | $K(V-U_\app)$ 병진 커널 표기로 $(K\!\ast\!\rho)(V)$ 합성곱 구조 1줄 명시 | scope(ii) 의 "합성곱·Fredholm" 언급과 형식 연결 |
| A08-L1 | ch1_sec07_broadening.tex:223 | 논리(수치) | L | `$1.6w_j$'' 지름길로 재현한 logistic 종은 이 실제 합성곱보다 peak 가 약 $10\%$ 높다(분산은` | `약 $12\%$ 높다` (정밀 11.6%) 또는 방향 반전 "실제 합성곱이 약 10% 낮다"(10.4%) | 수치 재계산(§V-3): 비 1.1157 |
| A08-L2 | ch1_sec07_broadening.tex:40 | 설명 | L | `첫째는 본 장이 이미 모델로 담은 출처로, \emph{전류가 켜야} 생긴다` | `본 장 모델이 담는 출처로(\S\ref{sec:lag}--\S\ref{sec:tail} 이 뒤에서 세운다)` | §8·§9 는 본 절 뒤 — 선형 독자에게 "이미"가 시점 착오 |
| A08-L3 | ch1_sec07_broadening.tex:109 | 설명 | L | `\emph{비-크기$\cdot$비-사이즈} heterogeneity 다` | `\emph{비-크기(non-size)} heterogeneity 다` | 크기=사이즈 동어 중복 |
| A08-L4 | ch1_sec07_broadening.tex:168 | 설명(표시) | L | `298 K 에서 $\approx91$ mV)` | `$\approx90.5$ mV` (fig:logistic 캡션 표기와 통일) | 90.53 mV — 두 절이 91/90.5 로 갈림; 같은 문단 26 vs 25.7 mV 병존도 동류 |
| A08-L5 | ch1_sec07_broadening.tex:17–18 | 설명(참조) | L | `단일 입자 평형 dQ/dV 가 \S\ref{sec:width} 의 logistic 미분` + `종(식~\eqref{eq:belliden})으로` | `\S\ref{sec:width}$\cdot$\S\ref{sec:eqpeak} 의 logistic 미분 종(식~\eqref{eq:belliden})` | eq:belliden 정의 위치는 §6(sec:eqpeak) |
| A08-L6 | ch1_sec07_broadening.tex:267 | 보완 | L | `($r_{\min}/r_{\max}=3/15\,\mu$m 예시)` | 하한 1 μm 로 넓힌 값(0.70 mV, <3%) 병기 | 앞 문장 r=1–15 μm 와 예시 3–15 μm 의 어긋남 선제 차단(§V-6) |
| A08-L7 | ch1_sec07_broadening.tex:171–173 | 설명 | L | `성분비로 적으면` + `$\sigma_\mathrm{sym}/\sigma_\mathrm{int}=\sqrt{1+(\sigma_\eta/\sigma_\mathrm{int})^2}$ 이라 같은` + `비율이 scale 에도 그대로 적용된다` | "같은 logistic 족으로 분산 정합해 읽을 때" 한정 절 | scale 이월은 동족 가정 하에서만 — 캡션의 지름길 한계와 접속 |
| A08-L8 | ch1_sec07_broadening.tex:26 뒤 | 보완 | L | `(\S\ref{sec:width-w} 의 지위 구분$\cdot$Part T 파생 C(\S\ref{ssec:weff}) 각주와 같은 한정)` | 피팅이 첫째 부류 Ω_j 를 2RT 이하로 내리면 분류·문턱 자기정합된다는 반문장 | §5 post-fit 기준(307–311행)과 연결 — 독자 질문 차단 |
| A08-L9 | ch1_sec07_broadening.tex:52 | 수식화 | L | `③ 을 분리하지 않은 \emph{유효} 폭(그때의 $n_j$ 는 유효 다중도)으로 읽는다` | 유효 다중도 수치 병기: $n_j=w_jF/RT\approx0.55\cdot0.47$ | w=0.014/0.012 V ⇒ n=0.545/0.467(§V-7) |

---

## H 등급 상세 (논리/물리 오류·오귀속) — 1건

### A08-H1 — keybox 가 본문의 이중계산 금지 규정과 자기모순 ("셋을 한꺼번에 흡수")
- 파일:행 = `ch1_sec07_broadening.tex:303–310` (문제 문장 309)
- 유형 = 논리(수식↔산문 불일치·절 내 자기모순) · 등급 = **H**
- 현행(축자, 303–310행):
```latex
두-상 전이($\mathrm{LiC_{12}}\cdot\mathrm{LiC_6}$)만 평형(plateau 내부) 델타가 유한 종이 된다 --- 그 폭은 \emph{세}
출처가 정한다: ① \emph{전류가 켜는} 유한율속 비대칭 꼬리($L_V$, $|I|\!\to\!0$ 소멸) ② plateau 양끝의 \emph{평형 잔여}
내재 폭($\sim RT/F$, 전류 무관) ③ \emph{입자 앙상블}의 집합 통계역학 --- 평형 층(Dreyer 순차 전환이 \emph{plateau 구조}를
만듦)과 broadening 층(그 평형 델타를 펴는 \emph{apparent-U $=U_j+\eta$} 의 입자간 $\eta$ 산포 $\rho(U_\app)$)으로 갈리며,
forward 평균 $\int\rho(U_\app)\,(\dd Q/\dd V)^\mathrm{single}\,\dd U_\app$(식~\eqref{eq:ensavg}; $\rho\!\to\!\delta$ 면
평형 중심 $U_j$ 의 단일 델타로 환원; 흑연-특정 구조 무질서 \emph{근거}는 흑연 두-상 한정 --- LCO 는 일반
$\eta$ 산포로만, 본문 ③). 셋을 한꺼번에 흡수하는 것이 \emph{현상학적 자유 피팅 폭}이며 ---
\emph{분포하는 것은 $\eta$(겉보기 중심 $U_\app$), 평형 중심 $U_j$ 는 입자 무관 상수로 움직이지 않는다}.
```
- 문제(재유도로 확인): 절 도입(8–9행)에서 "현상학적 자유 피팅 폭" = $w_j$ 로 정의된다. 본문은 (a) 120–123행 "식~\eqref{eq:ensavg} 가 담는 것은 ②(커널 내 내재 폭)$\otimes$③(앙상블 $\eta$ 산포)뿐", "두-상 \emph{총} broadening 은 $w_j(\text{②}\otimes\text{③})+L_V(\text{①})$ 로 묶인다(①의 전류 몫을 $w_j$ 가 다시 흡수하면 **이중계산**)"으로, (b) 식~\eqref{eq:widthbudget}(157–164행)의 대칭 폭(②③) vs 비대칭 꼬리 길이(①=$L_{V,j}$) 분리로, ① 을 $w_j$ 에서 두 번 명시 배제했다. keybox 의 "셋을 한꺼번에 흡수하는 것이 현상학적 자유 피팅 폭" 은 $w_j$ 가 ①까지 흡수한다는 문장이 되어 본문 규정과 정면 모순이고, keybox 자신도 같은 문장 안에서 ① 을 "$L_V$" 담당으로 이미 적고 있어 문장 내 충돌이다. 요약 박스는 마스터 피팅 지침으로 직접 읽히는 위치라 실害 있음.
- 제안(대체 LaTeX — 해당 문장만; 뒤의 "\emph{분포하는 것은 $\eta$…}" 문장은 그대로 접속):
```latex
②$\otimes$③ 을 한꺼번에 흡수하는 것이 \emph{현상학적 자유 피팅 폭} $w_j$ 이고, ① 은 별도 축
$L_{V,j}$ 가 담당한다(①의 전류 몫을 $w_j$ 가 다시 흡수하면 이중계산 --- 식~\eqref{eq:widthbudget}) ---
```
  대안(총 broadening 서술을 살리는 변형):
```latex
셋이 함께 실측 종을 정하되, 그중 ②$\otimes$③ 을 흡수하는 것이 \emph{현상학적 자유 피팅 폭} $w_j$
(① 은 $L_{V,j}$ --- 합치면 이중계산, 식~\eqref{eq:widthbudget})이며 ---
```
- 근거: 같은 파일 8–10·120–124·157–178행; `ch1_sec05_width.tex:296–305`(이중지위 — $w_j$ 정의); `ch1_sec09_tail.tex` eq:lag(①의 별도 축 실현). 재계산 §V-2·§V-5 로 두 축 분리가 수치로도 정확함을 확인.

---

## M 등급 상세 (의미·이해 실질 개선) — 10건

### A08-M1 — CLT bgbox: Lindeberg 조건의 gloss 가 무지배(Feller) 조건과 동일시됨
- 파일:행 = `ch1_sec07_broadening.tex:134–135` · 유형 = 논리 · 등급 = M
- 현행(축자, 133–135행):
```latex
없다(비-Gaussian 가능). 그러나 (iii-b) 의 실제 기원(국소 접촉 저항$\cdot$결정성$\cdot$흑연화도$\cdot$%
turbostratic 무질서$\cdot$국소 과전압)은 성격이 다른 \emph{다수 독립} 기여의 합 $\eta=\sum_{k=1}^{m}\eta_k$
이고, 어느 하나도 총분산을 지배하지 않는다는 Lindeberg 조건 아래 중심극한정리(CLT)가
```
- 문제(반례 재유도 — §V-9): "어느 하나도 총분산을 지배하지 않는다" 는 Feller(무지배) 조건이고, Lindeberg 조건은 그보다 **엄격히 강한** "임계 초과 꼬리 2차 모멘트 몫의 소멸" 이다(Lindeberg ⇒ Feller, 역은 불성립). 무지배만으로는 CLT 가 성립하지 않는 반례가 존재한다(§V-9: $\eta_k=\pm k$ w.p. $1/2k^2$ — 분산 1 균일·무지배인데 합/√n → 0 퇴화). 반면 같은 box 의 회수 문구 "한 원천 지배면(Lindeberg 붕괴)"(149행)는 방향이 옳다(지배 ⇒ Feller 붕괴 ⇒ Lindeberg 붕괴) — 정정 불요.
- 제안(대체 LaTeX — box 내부 자구만, 독립성 불변):
```latex
이고, 임계 초과 꼬리 몫이 총분산에서 소멸한다는 Lindeberg 조건 --- 어느 한 원천도 총분산을
지배하지 않음을 함의한다 --- 아래 중심극한정리(CLT)가
```
- 근거: Lindeberg–Feller CLT 의 표준 진술(수학적 사실 — 문헌 인용 불요의 교과서 수준); 반례 재유도 §V-9.

### A08-M2 — CLT bgbox: "분산 가법의 CLT 재유도" — 귀속 방향 오류
- 파일:행 = `ch1_sec07_broadening.tex:141–142` · 유형 = 논리(인과/귀속) · 등급 = M
- 현행(축자, 141–142행):
```latex
로 몰아 --- 식~\eqref{eq:widthbudget} ③ 항 $\sigma_\eta^{\,2}$ 의 \emph{형상} 근거이자 그 분산
가법(현행은 ``모양과 무관한 합성곱 항등식'')의 CLT 재유도를 준다.
```
- 문제(재유도 — §V-10): 분산 가법($\sigma_\eta^2=\sum_k\sigma_{\eta_k}^2$, 그리고 식~\eqref{eq:widthbudget} 의 ②$+$③ 가법)은 **독립성만으로** 성립하는 항등(합성곱의 2차 모멘트 가법)이며, CLT 의 결과가 아니라 CLT 가 규격화에 **쓰는 전제 수준의 사실**이다. CLT 가 새로 공급하는 것은 $\rho(\eta)$ 의 **형상(Gaussian)** 뿐이다. "CLT 재유도" 는 인과를 뒤집어, 본문(153–155행)이 옳게 세운 "모양과 무관한 항등식" 지위를 도리어 약화시킨다.
- 제안(대체 LaTeX — box 내부 자구만):
```latex
로 몰아 --- 식~\eqref{eq:widthbudget} ③ 항 $\sigma_\eta^{\,2}$ 의 \emph{형상}(Gaussian) 근거를 준다
(분산 가법 자체는 독립성만으로 성립하는 합성곱 항등식 --- 본문의 ``모양과 무관'' 규정 그대로이고,
CLT 는 그 위에 형상만 얹는다).
```
- 근거: Var(합)=Σ Var (독립) 은 CLT 무관 항등; 본문 153–155행과의 정합.

### A08-M3 — fig:widthbudget 캡션 "치수선 길이로 직접 대비" — σ 치수선(±σ=2σ)과 L_V 치수선(1·L_V)의 2배 눈금 불일치
- 파일:행 = `ch1_sec07_broadening.tex:226–227` (치수선 좌표 197·202·209행) · 유형 = 논리(그림↔캡션) · 등급 = M
- 현행(축자, 226–227행):
```latex
peak 위치가 중심에서 이동한다. 세 척도($\sigma_\mathrm{int}$·$\sigma_\mathrm{sym}$·꼬리 길이 $L_V$)는
치수선 길이로 직접 대비된다.}
```
- 문제(좌표 재검증 — §V-4): 치수선 실측 길이는 $\sigma_\mathrm{int}$ 바 $=3.62w$ ($-1.81\to1.81$, 197행), $\sigma_\mathrm{sym}$ 바 $=5.80w$ ($-2.90\to2.90$, 202행), $L_V$ 바 $=1.50w$ ($1.24\to2.74$, 209행). 곧 σ 두 바는 $\pm\sigma$ 스팬(길이 $2\sigma$)이고 $L_V$ 바만 길이 $L_V$ 그 자체라, "길이로 직접 대비"를 문자대로 읽으면 $L_V$ 대비 σ 척도가 2배 과대로 보인다(실제 $\sigma_\mathrm{int}{=}1.81w$ vs $L_V{=}1.5w$ 는 비슷한 크기인데, 바 길이는 3.62 vs 1.50).
- 제안(1안 — 캡션 자구 보강, 그림 불변):
```latex
peak 위치가 중심에서 이동한다. 세 척도($\sigma_\mathrm{int}$·$\sigma_\mathrm{sym}$·꼬리 길이 $L_V$)가
치수선으로 대비된다 --- 단 $\sigma$ 치수선은 $\pm\sigma$ 스팬(길이 $2\sigma$)이고 $L_V$ 치수선은 길이
$L_V$ 그 자체라, 길이를 맞비교할 때는 $2$ 배 눈금 차를 감안한다.}
```
  (2안 — 그림 통일: σ 바를 $0\to\sigma$ 반스팬으로 교체 `\draw[{Bar...}] (0,0.37) -- (1.81,0.37)` 류 — 자산 수정 폭이 커서 1안 우선.)
- 근거: 197·202·209행 좌표 산술; §V-4.

### A08-M4 — scope(ii) "분포는 폭을 넓힐 뿐 평형 중심 U_j 를 옮기지 않는다" — 산포/평균 구분 미비
- 파일:행 = `ch1_sec07_broadening.tex:293–294` · 유형 = 설명 · 등급 = M
- 현행(축자, 292–294행):
```latex
증폭한다는 것이다. 따라서 $\eta$ heterogeneity 는
\emph{현상학적 폭 $w_j$ 에 흡수되는 것으로만} 두고 식~\eqref{eq:ensavg} 를 forward 로만 쓴다(분포는 폭을
\emph{넓힐} 뿐 평형 중심 $U_j$ 를 옮기지 않는다 --- (iii-b) 의 GITT 한정과 동일\cite{park2021}).
```
- 문제: CLT bgbox 는 $\rho(\eta)\to\mathcal N(\bar\eta,\sigma_\eta^2)$ 로 **평균 $\bar\eta$ 를 명시적으로 허용**한다(137행). $\bar\eta\ne0$ 이면 관측 peak 중심은 $U_j+\bar\eta$ 로 이동하므로, "분포는 …옮기지 않는다"를 "관측 중심 불변"으로 읽으면 box 와 충돌한다. 진의(평형 파라미터 $U_j$ 는 불변)와 관측 중심 이동을 갈라 적으면 충돌이 사라진다.
- 제안(대체 LaTeX — 괄호 절만):
```latex
(분포의 \emph{산포}는 폭을 \emph{넓힐} 뿐이고, 그 \emph{평균} $\bar\eta$ 가 관측 peak 중심을 옮기더라도
그것은 평형 파라미터 $U_j$ 의 이동이 아니다 --- $U_j$ 는 입자 무관 상수로 불변, (iii-b) 의 GITT 한정과
동일\cite{park2021})
```
- 근거: 137행($\bar\eta$)·125–127행(잔여 몫 처리)과의 정합; ① 의 평균 이동($+L_V$, §V-5)과의 회계 일관.

### A08-M5 — ② 내재 폭: "델타가 델타로 남는데 왜 폭이 생기나"에 기작 반 걸음 보강 (binodal 접속)
- 파일:행 = `ch1_sec07_broadening.tex:46–48` · 유형 = 설명 · 등급 = M
- 현행(축자, 46–48행):
```latex
\emph{② 내재 $RT/F$ 폭(평형 잔여 몫).} 둘째는 plateau 양끝의 단상(solid-solution) 꼬리가 까는 내재 폭으로, plateau
양끝이 첫째 부류와 같은 연속 등온선이라 그 경계가 무한히 날카롭지 않고 폭 $\sim RT/F$ 규모(수십 mV order)로 번진 데서
온다(Levi--Aurbach\cite{leviaurbach1999}) --- 이 몫은 전류와 무관한 \emph{평형 자체의 잔여 폭}이라 $|I|\!\to\!0$ 에서도
```
- 문제: 엄밀한 독자는 "plateau 내부 델타는 여전히 델타인데, 양끝 단상 꼬리가 있다고 **델타의 폭**이 왜 생기나"에서 막힌다. 답은 "평형 등온선이 plateau 밖 양끝(binodal)에서 단상 가지로 연속 접속하고, 실측·피팅은 델타$+$그 가지 몫을 **한 봉우리로** 읽으므로 그 유효 폭이 $\sim RT/F$ 규모"인데 현행은 이 연결 고리를 생략했다.
- 제안(보강 LaTeX — 47행 `온다(Levi--Aurbach\cite{leviaurbach1999})` 직후 삽입):
```latex
--- 평형 등온선이 plateau 밖 양끝(binodal)에서 단상 가지로 \emph{연속} 접속하므로, plateau 내부 델타에
그 가지 몫이 붙어 \emph{한 봉우리로} 읽히는 유효 폭이 이 규모다
```
- 근거: `ch1_sec04_hys.tex` eq:Veq(단상 가지의 연속 곡선)·fig:broadening (b) 캡션 "양끝 단상 꼬리 탓에 폭이 정확히 0 은 아님" 과 동일 물리의 본문 명문화.

### A08-M6 — "두 축이 전류 의존성으로도 갈린다" — ③ 동역학 몫의 |I| 의존과의 한정 접속
- 파일:행 = `ch1_sec07_broadening.tex:173–176` · 유형 = 보완 · 등급 = M
- 현행(축자, 173–176행):
```latex
실측 종에서 조작적으로 분리되는 것도 이 두 축이다: 대칭 폭은 피팅 폭 $w_j$ 가
②$\otimes$③ 을 한꺼번에 흡수하고(두 몫의 분리는 $\sigma_\eta$ 의 독립 측정 없이는 비유일 --- \S\ref{sec:broadening-scope} 의 (ii)
ill-posed 성질과 같은 뿌리), 비대칭 꼬리는 $L_{V,j}$ 가 담당하며 $|I|\!\to\!0$ 에서 소멸해 두 축이 전류
의존성으로도 갈린다.
```
- 문제: 같은 절 125–127행이 "③($\eta$) 중 순수 동역학 몫도 $|I|\to0$ 에서 소멸"을 이미 인정했으므로, "전류 의존성으로 갈린다"는 문자대로는 성립 반경이 좁다(대칭 폭의 일부도 전류를 따라 준다). 살아남는 구분은 "비대칭 축은 **항등 소멸**·대칭 축은 ② 의 평형 잔여가 **바닥으로 남음**"이다.
- 제안(보강 LaTeX — 176행 `의존성으로도 갈린다.` 를 다음으로 대체):
```latex
의존성으로도 갈린다(③ 의 동역학 몫 역시 $|I|$ 와 함께 줄지만 \emph{대칭}으로 줄어 왜도를 남기지
않는다 --- $|I|\!\to\!0$ 에서 \emph{항등 소멸}하는 것은 비대칭 축뿐이고, 대칭 축은 ② 의 평형 잔여가
바닥으로 남는다).
```
- 근거: 125–127행과의 자기정합; ②"전류 무관"(48행)·①"소멸"(44행) 규정의 3원 회계 완결.

### A08-M7 — eq:ensavg 의 가중 규약(수 가중 vs 용량 가중) 미규정
- 파일:행 = `ch1_sec07_broadening.tex:117–119` (식 111–116) · 유형 = 보완 · 등급 = M
- 현행(축자, 117–119행):
```latex
곧 단일 입자 응답 $(\dd Q/\dd V)^\mathrm{single}_{U_\app}$(평형 델타에 ② 내재 폭이 얹힌 좁은 peak)을 \emph{겉보기 중심}
$U_\app$ 이 $\eta$ 만큼 분포한 앙상블 위로 \emph{forward} 합성한 것이다 --- (iii-a) 평형 층 위에 얹힌
broadening 층이며, $\eta$ 의 \emph{입자간 산포}를 평균한다.
```
- 문제: 앙상블 $\dd Q/\dd V$ 는 입자별 **전하 기여의 합**이므로 $\rho(U_\app)$ 는 엄밀히 용량 가중 밀도여야 한다(수 가중이면 대입자 편향 누락). (i) 의 사이즈 소거 결과로 본 절에서는 두 가중이 일치하지만, 그 논리 고리가 무명시라 사독 질문 지점이다.
- 제안(보강 LaTeX — 119행 `입자간 산포}를 평균한다.` 직후 1문장):
```latex
$\rho(U_\app)$ 는 입자 수가 아니라 \emph{용량 가중} 밀도로 읽는다 --- \S\ref{sec:broadening-scope}(i) 의
사이즈 소거로 입자 용량이 사실상 균일해 두 가중이 일치하므로, 이 규약은 본 절 범위에서 자동 충족된다.
```
- 근거: 앙상블 평균의 표준 회계; eq:psdconv(238–242행)의 $p(r)$ 에도 같은 규약이 함의됨(그쪽은 반경 소거로 항등이라 실무 영향 없음).

### A08-M8 — ③ 의 접촉 저항 η 와 §pol 의 lumped R_n — 평균/편차 계상 경계 미명시
- 파일:행 = `ch1_sec07_broadening.tex:107–109` · 유형 = 보완 · 등급 = M
- 현행(축자, 107–109행):
```latex
전극 수준 OCP 는 이를 시사할 뿐 단일입자 산포를 직접 분해하진 못한다), \emph{분포하는 것은 $\eta$}다 ---
과전압$\cdot$국소 접촉 저항$\cdot$국소 환경(결정성$\cdot$흑연화도$\cdot$turbostratic 무질서가 \emph{유효 장벽$\cdot$국소
$\eta$} 를 입자별로 흩뜨림)에서 오는 \emph{비-크기$\cdot$비-사이즈} heterogeneity 다.
```
- 문제: "국소 접촉 저항" 몫은 $|I|R$ 형이라 독자는 곧장 \S\ref{sec:pol} 의 lumped $R_n$(식~\eqref{eq:vn})과의 이중계산을 묻게 된다. 회계 경계(입자 공통 평균 몫 = $R_n$ 분극으로 기계상, ③ 에 드는 것은 그 **입자간 편차**뿐)가 본 절에 없다.
- 제안(보강 LaTeX — 109행 `heterogeneity 다.` 직후 1문장):
```latex
$\eta$ 의 입자 \emph{공통}(평균) 몫은 \S\ref{sec:pol} 의 lumped $R_n$ 분극(식~\eqref{eq:vn})이 이미
계상하므로, ③ 에 드는 것은 그 \emph{입자간 편차}뿐이다 --- 같은 저항을 두 번 세지 않는다.
```
- 근거: `ch1_sec10_sum.tex` §pol(159–184행) 과의 회계 정합; M4 의 평균/산포 구분과 한 몸.

### A08-M9 — [④수식화] §7.1 분류 결론의 요약표 부재
- 파일:행 = `ch1_sec07_broadening.tex:12–32` (삽입 위치 32행 뒤) · 유형 = 수식화 · 등급 = M
- 현행: §7.1 전체가 산문 21행(분류·명명 규약·근거·한정이 문단 하나에 직렬). 축자 대표행(20–21행):
```latex
예측 그 자체라 ``왜 종이냐''는 물음이 생기지 않는다. 둘째 부류는 \emph{두-상 평탄역(plateau)} 전이다 ---
$2\mathrm L\!\to\!2$($\mathrm{LiC_{12}}$)와 $2\!\to\!1$($\mathrm{LiC_6}$)은 $\Omega_j>2RT$ 의 상분리(\S\ref{sec:hys}
```
- 제안(보강 LaTeX — 32행 뒤, 소절 말미에 추가; 기존 산문 삭제 없음):
```latex
\begin{center}\footnotesize
\begin{tabular}{@{}llll@{}}
\hline
전이 & 평형 단일 입자 모양 & 폭 $w_j$ 의 지위 & 분류 근거 \\
\hline
dilute$\to$4 영역$\cdot$$4\!\to\!3$$\cdot$$3\!\to\!2\mathrm L$ & 연속 등온선 --- 이미 종($\sim n_jRT/F$) &
평형 예측(식~\eqref{eq:wbase}) & plateau 없음\cite{rsc2021,leviaurbach1999} \\
$2\mathrm L\!\to\!2$($\mathrm{LiC_{12}}$)$\cdot$$2\!\to\!1$($\mathrm{LiC_6}$) & plateau 내부 델타(Maxwell) &
broadening 이 정하는 현상학적 자유 피팅 폭 & 실측 plateau$\cdot$상도표\cite{dahn1991,ohzuku1993} \\
\hline
\end{tabular}
\end{center}
```
- 근거: ④관점 — 분류 결과가 이후 절 전체의 분기 조건인데 산문에만 있음; 표 라벨은 본문 용어 그대로(P5 보존).

### A08-M10 — [④수식화] eq:ensavg 의 합성곱 구조(병진 커널) 1줄 명시
- 파일:행 = `ch1_sec07_broadening.tex:117–119` · 유형 = 수식화 · 등급 = M
- 현행(축자): A08-M7 과 동일 구간(117–119행).
- 문제/이득: scope(ii)(288행)는 eq:ensavg 를 "1종 Fredholm(DRT 동형)·합성곱"이라 부르지만, 식 자체(111–116행)에는 평가 전위 $V$ 와 커널의 병진 구조가 암묵이다. 한 줄이면 ②$\otimes$③ 표기·분산 가법·ill-posed 논증이 전부 같은 형식 위에 선다.
- 제안(보강 LaTeX — 119행 직후, M7 문장과 병합 가능):
```latex
커널이 중심의 병진으로만 들어가므로($K(V-U_\app)\equiv(\dd Q/\dd V)^\mathrm{single}_{U_\app}(V)$)
식~\eqref{eq:ensavg} 는 표준 합성곱
$\big\langle\dd Q/\dd V\big\rangle_\mathrm{ens}(V)=(K\!\ast\!\rho)(V)$ 다 ---
\S\ref{sec:broadening-scope}(ii) 의 1종 Fredholm/DRT 동형이 이 형태에서 바로 읽힌다.
```
- 근거: 120행 "②$\otimes$③" 과 288–289행 "합성곱" 서술의 형식적 접지; 신규 기호 $K$ 는 제안 표기(P5 — 채택 시 국소 정의로 무충돌).

---

## L 등급 상세 (문체·표시) — 9건

### A08-L1 — fig:widthbudget 캡션 "약 10% 높다" — 정밀값 11.6%
- 파일:행 = `ch1_sec07_broadening.tex:222–224` · 유형 = 논리(수치 표시) · 등급 = L
- 현행(축자, 222–224행):
```latex
$=2.90w_j$ 의 피타고라스 형태로, 본문 식~\eqref{eq:widthbudget} 과 일치한다. 다만 본문이 쓰는 ``같은 함수족이면 유효 scale
$1.6w_j$'' 지름길로 재현한 logistic 종은 이 실제 합성곱보다 peak 가 약 $10\%$ 높다(분산은
정확해도 \emph{모양}까지 같은 logistic 족은 아님 --- 근사의 한계를 명시해 둔다).
```
- 재계산(§V-3): 지름길 peak $=1/(4\times1.6008w)=0.15617/w$, 실제 합성곱 peak $=0.13998/w$ → 지름길이 **11.6% 높음**(비 1.1157). "약 10%"는 "실제가 지름길보다 10.4% 낮다" 방향에서만 맞는다(주석 196행의 "~10% lower" 는 그 방향이라 정확).
- 제안: `peak 가 약 $12\%$ 높다` 로 교체, 또는 방향 반전 `이 실제 합성곱은 지름길 종보다 peak 가 약 $10\%$ 낮다`.

### A08-L2 — ① "본 장이 이미 모델로 담은 출처" — 선형 독자 시점 착오
- 파일:행 = `ch1_sec07_broadening.tex:40` · 유형 = 설명 · 등급 = L
- 현행(축자, 40행):
```latex
\emph{① 유한율속 비대칭 꼬리(동역학 몫).} 첫째는 본 장이 이미 모델로 담은 출처로, \emph{전류가 켜야} 생긴다 --- 유한
```
- 문제: $L_V$ 를 세우는 \S\ref{sec:lag}--\S\ref{sec:tail} 는 본 절 **뒤**다(빌드 순서 §7→§8→§9; 말미 354–355행도 "다음 절이 세운다"). "이미"는 판 이력 기준이라 선형 독자에게 어긋난다.
- 제안: `첫째는 본 장 모델이 담는 출처로(\S\ref{sec:lag}--\S\ref{sec:tail} 이 뒤에서 세운다), \emph{전류가 켜야} 생긴다`

### A08-L3 — "비-크기·비-사이즈" 동어 중복
- 파일:행 = `ch1_sec07_broadening.tex:109` · 유형 = 설명 · 등급 = L
- 현행(축자): `$\eta$} 를 입자별로 흩뜨림)에서 오는 \emph{비-크기$\cdot$비-사이즈} heterogeneity 다.`
- 제안: `...에서 오는 \emph{비-크기(non-size)} heterogeneity 다.` (같은 뜻의 국·영 중복 제거 — 본문 다른 곳 표기 "비-크기" 와 통일)

### A08-L4 — FWHM 표시 자리수: 본문 "≈91 mV" vs fig:logistic 캡션 "90.5 mV"
- 파일:행 = `ch1_sec07_broadening.tex:165–168` · 유형 = 설명(표시) · 등급 = L
- 현행(축자, 165–168행):
```latex
(logistic 미분 종~\eqref{eq:belliden} 은 규격화하면 scale $w_j$ 의 logistic 분포 그 자체라 분산이
$\pi^2w_j^2/3$, 반높이 전폭(full width at half maximum, FWHM)은
$2\ln(3+2\sqrt2)\,w_j\approx3.53\,w_j$ 다 --- $n_j{=}1$,
298 K 에서 $\approx91$ mV).
```
- 재계산(§V-1): $3.5255\times25.68=90.53$ mV — "≈91" 은 정수 반올림으로 참이나, `ch1_sec05_width.tex` fig:logistic 캡션은 "90.5 mV". 표시 통일 권고: `$\approx90.5$ mV`. (같은 문단 49행 "≈26 mV" vs 54행 "≈25.7 mV" 병존도 동류 — 앞은 "척도" 서술이라 관용 가능하나 통일하면 더 깔끔.)

### A08-L5 — eq:belliden 의 절 포인터: "\S\ref{sec:width} 의 logistic 미분 종"
- 파일:행 = `ch1_sec07_broadening.tex:17–18` · 유형 = 설명(참조) · 등급 = L
- 현행(축자, 17–18행):
```latex
이들은 plateau 가 없는 연속 등온선이라\cite{rsc2021}, 단일 입자 평형 dQ/dV 가 \S\ref{sec:width} 의 logistic 미분
종(식~\eqref{eq:belliden})으로 \emph{이미} 폭 $\sim n_jRT/F$ 의 종이다
```
- 문제: eq:belliden 은 `ch1_sec06_eqpeak.tex:17`(\S sec:eqpeak) 정의다(§5 는 logistic $\xi_\eq$·폭). 하이퍼링크는 옳게 가지만 산문 포인터가 어긋난다.
- 제안: `\S\ref{sec:width}$\cdot$\S\ref{sec:eqpeak} 의 logistic 미분 종(식~\eqref{eq:belliden})으로`

### A08-L6 — PSD 산포 예시(3/15 μm)와 앞 문장 범위(1–15 μm)의 하한 어긋남 선제 차단
- 파일:행 = `ch1_sec07_broadening.tex:264–267` · 유형 = 보완 · 등급 = L
- 현행(축자, 267행): `($r_{\min}/r_{\max}=3/15\,\mu$m 예시). 폭에 기여하는 것은 이동의 절대값이 아니라 PSD 위 이동의`
- 재계산(§V-6): 하한을 앞 문장의 $1\,\mu$m 까지 넓혀도 $\delta U_\mathrm{PSD}=0.70$ mV(= 실측 폭의 2.7%) — 결론 불변.
- 제안: `($r_{\min}/r_{\max}=3/15\,\mu$m 예시; 하한을 앞의 $1\,\mu$m 까지 넓혀도 $\delta U_\mathrm{PSD}\approx0.70$ mV --- 실측 폭의 $3\%$ 미만으로 결론 불변).`

### A08-L7 — "같은 비율이 scale 에도 그대로 적용된다" — 동족 가정 한정 절
- 파일:행 = `ch1_sec07_broadening.tex:171–173` · 유형 = 설명 · 등급 = L
- 현행(축자, 171–173행):
```latex
$\sigma=\pi w_j/\sqrt3$ 으로 환산된다. 성분비로 적으면
$\sigma_\mathrm{sym}/\sigma_\mathrm{int}=\sqrt{1+(\sigma_\eta/\sigma_\mathrm{int})^2}$ 이라 같은
비율이 scale 에도 그대로 적용된다.
```
- 문제: σ-비 항등은 무조건 정확하나, 그것을 "scale"(logistic $w$)로 이월하는 것은 합성 종을 **같은 logistic 족으로 분산 정합**해 읽을 때만이다(캡션의 지름길 한계와 같은 뿌리 — 본문에는 한정이 없음).
- 제안: `...이라, 합성 종을 같은 logistic 족으로 분산 정합해 읽으면 같은 비율이 scale 에도 그대로 적용된다(모양까지 같지는 않다 --- 그림~\ref{fig:widthbudget} 캡션의 지름길 한계).`

### A08-L8 — 분류↔문턱의 post-fit 자기정합 반문장
- 파일:행 = `ch1_sec07_broadening.tex:23–26` (26행 뒤 보강) · 유형 = 보완 · 등급 = L
- 현행(축자, 23–26행):
```latex
다만 이 두-부류 분류를 $\Omega>2RT$ 문턱 자체가 가르는 것은 아니다 ---
표~\ref{tab:staging} 의 \emph{초기값} $\Omega_j$ 로는 네 전이가 모두 문턱을 넘으므로, 두 전이만 두-상
plateau 로 지목하는 실제 근거는 실측 plateau$\cdot$staging 상도표의 상평형이다\cite{dahn1991,ohzuku1993}
(\S\ref{sec:width-w} 의 지위 구분$\cdot$Part T 파생 C(\S\ref{ssec:weff}) 각주와 같은 한정).
```
- 문제/이득: "그러면 첫째 부류의 초기 $\Omega_j>2RT$ 는 언제 해소되나" 라는 독자 질문에 §5(309–311행 post-fit 기준)가 답을 갖고 있으나 본 절에는 접속이 없다.
- 제안(26행 뒤 반문장): ` 피팅이 첫째 부류 두 전이의 $\Omega_j$ 를 $2RT$ 이하로 내리면 분류와 문턱이 자기정합된다(\S\ref{sec:width-w} 의 post-fit 기준).`

### A08-L9 — [④수식화] 폴백 유효 다중도 수치 병기
- 파일:행 = `ch1_sec07_broadening.tex:51–53` · 유형 = 수식화 · 등급 = L
- 현행(축자, 51–53행):
```latex
0.014 V($2\mathrm L\!\to\!2$)$\cdot$0.012 V($2\!\to\!1$)와 모순되지 않는다. 다만 그 폴백 값 자체는 ② 와
③ 을 분리하지 않은 \emph{유효} 폭(그때의 $n_j$ 는 유효 다중도)으로 읽는다 --- 두 몫의 분리가
$\sigma_\eta$ 독립 측정 없이는 비유일하다는 아래 폭 예산의 규정과 같은 이유다.
```
- 제안: `...\emph{유효} 폭(그때의 $n_j$ 는 유효 다중도 --- $n_j=w_jF/RT\approx0.55\cdot0.47$)으로 읽는다` (재계산 §V-7: 0.545·0.467. "n_j<1 은 피팅이 내려갈 수 있는 여지" 주장이 수치로 즉시 구체화됨)

---

## §V — 검증 로그 (재계산·재유도 전건; 수치는 Python 재현, 스크립트 = 세션 스크래치 `verify_fig.py`)

1. **logistic 상수 재유도** — pdf $e^{-x/s}/[s(1+e^{-x/s})^2]$ 의 반높이: $u^2-6u+1=0\Rightarrow u=3\pm2\sqrt2$ ⇒ FWHM $=2\ln(3+2\sqrt2)s=3.5255s$ ✓(본문 3.53). 분산 $\pi^2s^2/3$ ✓, $\sigma_\mathrm{int}=\pi w/\sqrt3=1.8138w$ ✓(그림 1.81). $RT/F=25.68$ mV(298 K)·FWHM $=90.53$ mV(본문 ≈91 — L4).
2. **폭 예산 피타고라스** — $\sigma_\eta=1.25\sigma_\mathrm{int}$ ⇒ $\sigma_\mathrm{sym}=1.8138\sqrt{1+1.5625}\,w=2.9035w$ ✓(그림·캡션 2.90); 유효 scale $=\sigma_\mathrm{sym}\sqrt3/\pi=1.6008w$ ✓(본문 1.6).
3. **지름길 vs 실제 합성곱 peak** — FFT 수치 합성곱(격자 $2^{16}$, $|x|\le60$): 실제 peak $0.13998/w$ @ $x=0.00$, 지름길 logistic(scale 1.6008) peak $0.15617/w$ ⇒ 지름길/실제 $=1.1157$(**11.6% 높음**; 실제는 10.4% 낮음). 캡션 "약 10% 높다" → L1. 합성곱 분산 수치 $=8.4303w^2=\sigma_\mathrm{sym}^2$ 정확 ✓.
4. **fig:widthbudget 좌표 진위** — 24개 표본점 전건 대조: stage2(=logistic, 오차 $\le10^{-4}$)·stage3(=logistic$\otimes$Gaussian 실제 합성곱, 오차 $\le10^{-4}$)·stage4(=stage3$\otimes$단측 지수 $L{=}1.5w$, 오차 $\le5\times10^{-4}$) — **캡션의 "실제 수치 합성곱" 주장 사실로 확인**. stage4 평균 이동 $1.498w\approx L_V$ ✓, 총분산 $10.680w^2=\sigma_\mathrm{sym}^2+L_V^2$ 정확 ✓. 치수선 길이 산술(197·202·209행): $3.62/5.80/1.50w$ → M3.
5. **①=단측 지수 커널 합성곱 재유도** — `ch1_sec09_tail.tex` eq:lag→eq:tail-limit-start 로 peak shape $=(\dd\xi_\eq/\dd V)\ast\mathrm{Exp}(L_V)$ 정확 합성곱 확인 ⇒ 분산 $+L_{V,j}^2$ 가법·평균 이동 $+\sigma_dL_V$·왜도 동반·$L_V\propto|I|$(`ch1_sec08_lag.tex:120–121`) — 본문 155–156행·162행 주장 전건 ✓. 방전 꼬리 고전위 방향 ✓(fig:reversal 정점 $+1.01w$ 와 정합).
6. **Gibbs–Thomson·PSD 수치** — $V_m$: $6\times12.011/2.26=31.89$ ✓(본문 31.9)·$\times1.13\approx36.0$ ✓. $\Delta U(1\,\mu m;\gamma{=}1)=0.746$ mV ✓(0.75)·$=2.90\%$ of $25.68$ mV ✓("3% 를 넘지 못한다" 성립). $\delta U_\mathrm{PSD}(3/15\,\mu m)=0.199$ mV ✓(0.20; 0.78% <1% ✓)·$\gamma{=}5$: 0.995 mV ✓(1.0). $r=30$ nm: 24.9 mV ✓(≈25). 하한 1 μm 확장: 0.70 mV(2.7%) — L6 병기 근거.
7. **문턱·폴백 수치** — $2RT@298.15$ K $=4957.9$ J/mol ✓(≈4958); tab:staging $\Omega$ 초기값 6000/8000/10000/13000 모두 초과 ✓("네 전이 모두 문턱"). 폴백 폭 0.020/0.016/0.014/0.012 V ⇒ $n_j=0.778/0.623/0.545/0.467$ — ② 의 "$n_j<1$" 서술과 정합 ✓(두-상 두 건 0.55·0.47 — L9).
8. **τ 수치** — $\tau(5\,\mu m)=r^2/D$: $D=4\times10^{-10}$ cm²/s ⇒ 625 s(≈6×10²) ✓·$D=10^{-11}$ ⇒ $2.5\times10^4$ s ✓(park2021 의 D 범위 그대로).
9. **Lindeberg 반례 재유도(M1)** — $\eta_k=\pm k$ w.p. $1/2k^2$, 그 외 0: $\mathrm{Var}=1$ 균일, $\max_k\sigma_k^2/s_n^2=1/n\to0$(무지배 성립)인데 $\sum P(\eta_k\ne0)=\sum1/k^2<\infty$ ⇒ Borel–Cantelli 로 합이 a.s. 유한 ⇒ $S_n/\sqrt n\to0$(퇴화, 정규 아님) — 무지배⇏CLT. 역방향(지배⇒Lindeberg 붕괴)은 참 — 149행 회수 문구는 무수정.
10. **CLT 귀속(M2)** — 독립 합의 분산 가법은 2차 모멘트 항등(형상 무관)·CLT 진술의 전제 측 사실 — "CLT 재유도" 는 귀속 역전. 본문 153–155행의 규정("모양과 무관한 항등식")이 옳고, box 는 형상만 보태는 것이 정합.
11. **교차참조 정합 전수(대상 절 기준)** — eq:eqpeak·eq:belliden·eq:wbase·eq:Veq·eq:spinodal·eq:dUhys·eq:lag·tab:staging(행 라벨 4→3/3→2L/2L→2/2→1)·fig:staging(stage 2L 옅은 표시)·\S width-w 폴백 규정("n 우선·w 폴백" — §10 45–48행 동일)·ssec:weff 각주(169–173행 — "문턱이 가르지 않는다" 동일 한정)·tier 각주 쌍둥이(`ch1_sec11_lcointro.tex:44–47` 자구 동일)·xr 전방참조(sec:lco-map — ch2 빌드, \externaldocument 선언 확인) — 전건 정합, 불일치 무발견(단 L5 의 산문 포인터 1건).
12. **서지 대조** — §7 인용 10키(rsc2021·leviaurbach1999·dahn1991·ohzuku1993·fly2020·park2021·dreyer2010·dreyer2011·cogswell2012·dahn1995) 전건 `ch1v22_bib.tex` 수록·V1 원장(v1.0.21 승계) 관할·주석 정합: rsc2021(K-graphite 비교 인용 tier B — §7 의 "연속 등온선" 용법 범위 내), dahn1995(용량-한계 예시 한정 — §7 283–286행의 과대인용 방지 문구와 자구 정합), cogswell2012("γ 수치 출처 아님" — §7 의 tier C 상정 문구와 정합), park2021(GITT OCP·D 범위 — §7 사용처 2건 정합). 서지 신규 제안 없음(아래 §S 는 후보만).

---

## §S — 문헌 서치 (BRIEF 규정대로 haiku 서브에이전트 위임 — doi 실검증분만, 기억 서지 배제)

**주제 1 — 흑연 리튬화 상경계 계면 에너지 γ 정량 문헌: 발견 못함.** (순수 흑연 cleavage energy ~0.37 J/m² 류만 발견 — 상경계 γ 아님, 제외.) ⇒ 본문 256–257행의 "수치의 전용 문헌 anchor 는 근거 미발견 --- tier C" 정직 표기가 **독립 서치로도 지지됨**. 메우기 제안 없음 — 현행 유지가 옳다(상한 논증 구조도 γ 정밀값에 둔감하게 이미 설계됨).

**주제 2·3 — 후보 표(서브에이전트 doi 검증분).** 채택은 원장 절차(검증→등재→인용, D22-4) 전제의 **후보**일 뿐이며, 본 보고는 등재를 요구하지 않는다:

| # | 주제 | 서지 | DOI | 검증 | 관련성(본 검토자 한정 주석 포함) |
|---|------|------|-----|------|------|
| S-1 | 입자간 이질성 | Merryweather et al., "Operando monitoring of single-particle kinetic state-of-charge heterogeneities and cracking in high-rate Li-ion anodes," *Nat. Mater.* **21**(11), 1306–1313 (2022) | 10.1038/s41563-022-01324-z | DOI·서지 실검증(서브) | 단일 입자 SoC 이질성 operando 직접 관측 — **단, 활물질이 흑연인지 원문 미확인(고율 음극 — 흑연 아닐 가능성). 흑연 한정 인용으로는 부적합 소지 — 방법론 앵커 후보로만** |
| S-2 | 입자간 이질성 | Gao et al., "Interplay of Lithium Intercalation and Plating on a Single Graphite Particle," *Joule* **5**(2), 393–414 (2021) | 10.1016/j.joule.2020.12.020 | DOI·서지 실검증(서브) | 단일 **흑연** 입자의 리튬화 상태 operando 광학 추적 — (iii-b) "전극 수준 OCP 는 단일입자 산포를 직접 분해하진 못한다"(106–107행) 보강용 최유력 후보 |
| S-3 | 입자간 이질성 | Guo et al., "Li Intercalation into Graphite: Direct Optical Imaging and Cahn–Hilliard Reaction Dynamics," *J. Phys. Chem. Lett.* **7**(11), 2151–2156 (2016) | 10.1021/acs.jpclett.6b00625 | DOI·서지 실검증(서브) | 흑연 리튬화 직접 광학 관측 — 단일 결정(입자간 분포 아님) — 보조 후보 |
| S-4 | 크기 의존성 | Holland et al., "Ab initio study of lithium intercalation into a graphite nanoparticle," *Mater. Adv.* **3**(23), 8469–8484 (2022) | 10.1039/d2ma00857b | DOI·서지 실검증(서브) | 나노 흑연 staging·OCP 제일원리 — scope(i) 의 "나노 영역은 범위 밖"(280–283행) 경계 서술의 보조 후보 |

서브 제외 목록: arXiv 1211.0027(크기별 OCP 정량 미제시 — 제외). **주제 3 의 실측(마이크론 vs 나노 OCP 비교) 1차 문헌은 미발견** — (iii-b) 의 park2021 전극 수준 한정 서술이 현재로선 최선임을 방증.

---

## 무발견 축 (검토했으나 문제 없음 — 명시)

1. **그림 수치 진위**: fig:widthbudget 3곡선 전건이 선언대로의 실제 수치 합성곱(§V-4) — "지름길 좌표를 실측인 척" 류 문제 없음. fig:broadening 은 도식 선언과 용법 일치.
2. **폭 예산 식~eq:widthbudget**: 계수(π²/3)·가법·왜도/평균이동 회계·$\ell_\mathrm{tail}=L_{V,j}\propto|I|$ — 재유도·수치 전건 정합(§V-2·3·5).
3. **① 의 물리**: eq:lag 재유도로 "대칭 합성곱으로 표현되지 않음·별도 축·$|I|\to0$ 소멸" 전건 확인(§V-5). fly2020 용법 정합.
4. **(iii-a)/(iii-b) 층 분리**: Dreyer 평탄역(값/경로 양립 서술 포함)과 η-산포 broadening 의 분리 논증 — 순환·비약 무발견. srcbox 대응표·가정 차 기재는 원장 주석과 정합.
5. **scope(i) 수치 유도**: Gibbs–Thomson·PSD 산포·동역학 채널 소거 논증 — 전 수치 재현(§V-6·8), 상한 논증 구조 견고(γ 5배 강건성 포함). "비-크기 전용은 선언이 아니라 따름 결과" 주장 성립.
6. **scope(ii) ill-posed**: 1종 Fredholm/DRT 동형·고주파 지수 억압 서술 — 표준 사실과 정합(smooth 커널의 스펙트럼 감쇠).
7. **교차참조·명칭**: tab:staging 행 라벨↔L 접미 명명 매핑, 폴백 4값, tier 각주 쌍둥이, ssec:weff 각주 한정, ver.N/Chapter 혼동 없음(P3-7), 전하 보존 중심식 흐름 훼손 없음(P3-2 — eq:ensavg 는 보조 forward 층), GS-1/GS-2 무관 — 전건 이상 없음(§V-11).
8. **서지**: §7 인용 10키 전건 원장 관할·주석 범위 내 사용(§V-12) — 과대인용·오귀속 무발견.
9. **bgbox 증축분 독립성**: CLT box 는 무번호 display·자체 한정·회수 문구로 제거 용이 구조 유지 — 훼손 요인 무발견(M1·M2 제안도 내부 자구 대체만).

## 4-tier 분류

- **확정**(재계산·원문 대조로 검증 완료): A08-H1(자기모순 — 원문 대조), M1·M2(수학적 사실+반례 재유도), M3(좌표 산술), L1(수치 11.6%), L4(90.53 mV), L5(라벨 정의 위치) — 및 §V 검증 로그 전건.
- **추정**(물리·논리 확인했으나 채택 여부는 저자 판단 — 보강 제안): M4·M5·M6·M7·M8·M9·M10, L2·L3·L6·L7·L8·L9.
- **미검증**(본 검토 범위에서 원문 전문 미접근 — 원장/서브 검증 수준까지만): park2021 원문 세부(입자 크기·형상 무관 보고의 실측 범위 — 원장 주석 신뢰), dreyer2010/2011 원 논문 내부 구조(원장·srcbox 주석 신뢰), §S 후보 4건의 본문 세부(특히 S-1 활물질 정체 — DOI·서지만 실검증).
- **범위 밖/제안 억제**: γ anchor 공백(tier C)·η 분포 형상 근거 공백(dahn1995 주석) — 본문이 정직 표기한 공백이며 서치로도 미발견 재확인 — 메우기 제안 없음. GS-1/GS-2 무관 확인.
