# A12_REVIEW — FR-A12 심층 검토 (Part T §2.2 config + §2.3 vib·electronic)

- 검토 창: FR-A12 (v1.0.22 대공사 재기동, BRIEF_FR_A.md 규율 준수 — 보고 전용·소스 불변·git 불변·`Codex/` 미접근)
- 대상 (전문 정독):
  - `Claude/docs/v1.0.22/_sections/ch2_sec02_config.tex` (§2.2 configurational 엔트로피, 191행 전문)
  - `Claude/docs/v1.0.22/_sections/ch2_sec03_vibel.tex` (§2.3 vibrational·electronic 엔트로피, 115행 전문)
- 소속 확인: 두 파일은 **ch1_graphite_v1.0.22.tex 빌드의 Part T(흑연 열특성부)** 소속(마스터 :38–39 input 확인). 파일명 `ch2_` 는 역사적 명칭 — ch2_lco 빌드(LCO 챕터)와 무관.
- 참조 원문 확인(read-only): ch2_sec01_partition(전문 — eq:Z1·eq:occ·eq:muV·eq:logistic·eq:Vxi·eq:BW·eq:Veq_BW·eq:slope_BW) · ch2_sec00_intro(전문) · ch2_sec04_einstein(도입 — 핸드오프) · ch2_sec05_mixing(전문 — eq:dxidT·eq:single_config·파생 B·파생 C warnbox) · ch2_sec06_limits(전문 — tab:limits·keybox) · ch2_sec07_revheat(도입 — eq:qrev) · ch1_sec02a/02b_part0(sm-site 페르미온 bgbox·eq:sm-sint·sm-lattice 단위환산·eq:sm-Smix) · ch1_sec03_center(eq:Uj·fig:UjT·수치 예시) · ch1_sec10_sum(tab:staging 전문) · ch1_sec07_broadening(분리 식별 한정) · ch1_sec18_inputs · ch1_sec14_lcodecomp(삼분해·슬롯·스코프 주의) · ch1_sec15_lcoelec(Sommerfeld 유도부) · ch1v22_bib · common_preamble_v1022(매크로·박스 환경) · ch1/ch2_lco aux(라벨 전수) · V1022→V1021→V1020 서지 원장 체인 · v1.0.21 동일 절 diff(증축분 식별)
- 검토 4관점: ①내용 보완(빡세게) ②논리 오류(재계산·재유도) ③더 쉬운 설명 ④산문→수식 간결화 — 전부 수행
- 표기 규약: 총괄표 셀 안 개행은 `<br>`. **기계 매칭용 축자 정본은 §2 등급별 상세의 코드펜스**(개행 원형 보존).

---

## 1. 발견 총괄표

| ID | 파일:행 | 유형 | 등급 | 현행(축자) | 제안(완성 LaTeX) | 근거 |
|---|---|---|---|---|---|---|
| A12-02 | ch2_sec02_config.tex:50–52 | 보완(독자 질문 선제 — 상호작용 항 무기여) | M | 곧 \textbf{Part I 의 logistic 폭 $w=RT/F$ 가 이미 부분몰<br>configurational 엔트로피를 담고 있었다}. 봉우리 내부 $\partial U_\oc/\partial T(x)$ 의 $x$-의존(비선형 모양)은<br>새 물리가 아니라, 점유 분포의 엔트로피가 $w$ 의 온도 의존을 통해 자동으로 들어온 것이다. | §2-M1 참조 | §2.1 이 직전에 상호작용식 eq:Veq_BW 를 세웠는데 §2.2 는 이상식 eq:Vxi 만 미분 — "Ω 항은 왜 빠지나"가 자연 질문. 재유도: $V_\eq$ 에 $-\Omega(1-2\theta)/F$ 를 더해도 고정 $\xi$ 의 $T$-미분 기여는 $-(\partial\Omega/\partial T)(1-2\theta)/F$ 뿐 — Part I 의 Ω 상수 취급에서 정확히 0. §2.5 파생 C warnbox("상호작용 엔트로피 ∝∂Ω/∂T … 범위 밖")와 접속하는 다리 한 문장 부재 |
| A12-03 | ch2_sec02_config.tex:54–68 | 보완(발산↔유한 실측의 다리) | M | (부호 3분기 itemize 종료 직후) 이 세 분기의 부호는 \S\ref{ssec:logistic} 의 규약 $\xi=1-\theta$ 에 매여 있다 --- … | §2-M2 참조 | 독자 질문 "측정 $\partial U_\oc/\partial T$ 는 ±∞ 가 아니다" 미답. 재계산: 겹침 가중(eq:implicit_diff·eq:dxidT)에서 발산 인자 $z_j$ 는 가중 $g_j\propto\xi_j(1-\xi_j)$ 와 곱으로만 등장, $\lim_{\xi_j\to0,1}\xi_j(1-\xi_j)\ln[\xi_j/(1-\xi_j)]=0$ — 내부 경계는 이웃이 이어받아 유한 블렌드(§2.5 수치 검증의 "연속 블렌드 3 경계"와 정합), 전역 양끝만 로그 발산 잔존 |
| A12-04 | ch2_sec02_config.tex:138–139 ↔ :163 | 보완/논리(문헌값 서술 상호 긴장) | M | $\Delta S\approx+29$ J\,mol$^{-1}$K$^{-1}$ @\,$x=0.08$, $-5\sim-16$ J\,mol$^{-1}$K$^{-1}$ @\,$x>0.5$ 이고<br>\cite{allart2018}, ↔ 표 4행: $-16$ @\,$x{>}0.5$ (양 끝, 정확) | §2-M3 참조 | 같은 문헌·같은 구간($x>0.5$)에 본문은 "−5∼−16(범위)", 표는 "−16(정확)" — 독자에겐 상충으로 읽힘. 범위 중 평탄역 대표값과의 일치라는 관계를 한쪽에 명시해야 정합. Allart 프로파일 세부는 [미검증-원문] |
| A12-05 | ch2_sec02_config.tex:143–145 | 보완(검증 성격 한정 — 순환 차단) | M | 표~\ref{tab:ds} 는 Part I 의 전이별 중심 표준값 $\Delta S^0_j=+29\to0\to-5\to-16$ J\,mol$^{-1}$K$^{-1}$ 가<br>이 문헌 프로파일과 부호$\cdot$규모에서 정합함을 보인다 --- 곧 분포 spine 의 입력 표준값이 임의값이 아니라<br>측정에 닿아 있다. | §2-M4 참조 | tab:staging 캡션이 명시하듯 $\Delta S_\rxn$ 초기값 자체가 실측(reynier2003 계열) 스케일에 맞춘 배치값 — 양 끝 +29·−16 의 수치 일치는 구성상 따라오는 것이라 "정합함을 보인다"는 독립 검증으로 오독될 여지. 비-자명분(중간 전이의 구간 정합·부호 반전 위치)과 계보 확인을 분리 서술하면 절 제목 "문헌 검증"의 하중이 정직해짐 |
| A12-06 | ch2_sec02_config.tex:175–178 | 보완(환산 결과 미제시 — 독자 검산 실패 지점) | M | calorimetry 의 형성 엔탈피(LiC$_6$ $-13.9$, LiC$_{12}$ $-24.8$<br>kJ/mol\,Li \cite{chemmater2015})는 \emph{누적}(formation, graphite$+$Li 금속 기준)이라 직접 등치할 수 없다 ---<br>비교하려면 형성 엔탈피의 $x$-미분으로 환산해야 한다. | §2-M5 참조 | 권유된 환산을 실제로 하면 stage 2→1: $2(-13.9)-(-24.8)=-3.0$ kJ/mol Li ≠ 본 문서 $-13.0$ — 환산해도 10 kJ/mol 급 간극 잔존(재계산 확정). 독자가 이 검산을 하면 미해명 모순으로 읽힘. 서브 검증: 두 수치·per mol Li 기준은 원문 abstract 계열에서 확인(LiH 경로·고온 열량계 맥락) — "기준 차이 경고 전용, 정량 anchor 아님"을 수치와 함께 못박는 문장 필요 |
| A12-07 | ch2_sec03_vibel.tex:27 | 설명(직관 서술의 엄밀 대체) | M | 가 된다 --- 여기서 첫 항은 빈 들뜸을 채우는 경우의 수, 둘째 항은 이미 들뜬 양자의 가짓수에서 온다. | §2-M6 참조 | 현행 두-항 귀속은 유도 불가능한 직관 서술(단일 모드에서 "경우의 수" 분리는 성립 안 함). 재유도로 뒷받침되는 두 독법 존재: (i) 들뜸수 기하분포의 Shannon 엔트로피(−Σ P_m ln P_m = −ln(1−e^{−x})+x n — 본문 자신이 언급한 "정보 엔트로피" 경로와 동일), (ii) 보손 셈 W=(N+g−1)!/(N!(g−1)!) 의 Stirling 두 항. 둘 중 하나로 대체하면 주장 전체가 검산 가능 |
| A12-08 | ch2_sec03_vibel.tex:29–31 | 수식화(산문 부호 서술→닫힌 항등식) | M | 삽입에 따른 부분몰 변화 $\Delta S_\vib=\partial<br>S_\vib/\partial x$ 는 모드 연화/경화에 따라 부호가 갈리는데, 흑연에서는 고-$x$(만충에 가까운) 영역에서<br>\emph{음의 baseline}을 만든다(Reynier 의 ``second contribution'') \cite{reynier2003}. | §2-M7 참조 | 산문 "연화/경화에 따라 부호"는 한 줄 항등식 $\Delta S_\vib=-\sum_k\bar c_k(T)\,\partial\ln\omega_k/\partial x$ ($\bar c_k$=모드 비열)로 정확·간결화 가능(재유도: $\partial S_k/\partial\ln\omega_k=-\bar c_k$ ✓). 부수 이득 둘: 고전 극한 $\bar c_k\to R$ 에서 "$T$-무관 상수"(:49–50 의 중심 흡수 전제)가 식으로 명시되고, 준양자 잔여 $T$-의존(§2.4 동기)이 같은 식의 $\bar c_k(T)$ 로 이어짐 |
| A12-12 | ch2_sec03_vibel.tex:81–82(·84–85) | 논리(과대 일반화 — 주 사례가 반례 방향) | M | 본 장의 규약대로, 삽입(리튬화)은 일반적으로<br>$\Delta S_e<0$ 이다 --- 밴드 채움으로 $E_F$ 부근 상태밀도가 줄어드는 호스트가 많기 때문이다. | §2-M8 참조 | 부호는 $\partial g(E_F)/\partial x$ 가 정하는 것이지 리튬화 일반의 성질이 아님. 본 장 주 사례 흑연이 방향 반례: 삽입 전자가 $E_F$ 를 준금속 최소점 위로 올려 $g(E_F)$ 는 커짐(LiC$_6$ 금속성 — Holzwarth 1978 계열, 서브 확인: "Fermi level … near a saddle point in the $\pi$ bands"; 전문 미접근 [추정]). 흑연 결론 $\Delta S_e\approx0$ 은 규모 논거로 살아남으나 "$g(E_F)$ 가 작아"는 저-$x$ 한정 — 일반화 문장·흑연 bullet 논거를 부호↔규모 분리로 대체 필요 |
| A12-15 | ch2_sec03_vibel.tex:101–104 | 논리(인용 하중 배분 — 오귀속 위험) | M | 활성화 엔트로피는 \emph{비가역} 동역학을 지배하고 가역 발열에는 들어가지 않으므로 \cite{msmr_partI}, | §2-M9 참조 | 서브 검증(abstract 축자): msmr_partI 는 "The entropy coefficient … governs the amount of reversible heat"(가역 발열↔평형 엔트로피 계수)를 지지하나, 활성화 엔트로피 배제 명제는 abstract 에 부재(전문 미접근). 현행 cite 위치는 배제 명제까지 문헌에 귀속 — 지지되는 반쪽으로 cite 를 옮기고 배제 명제는 본 문서 TST 몫(\S\ref{sec:lag})으로 앵커하는 재배치 필요 [추정] |
| A12-01 | ch2_sec02_config.tex:23–24 | 보완(부분몰=자리미분 등치 근거 한 줄) | L | 가역 발열에 들어가는 것은 $S_\config$ 자체가 아니라 \emph{Li 1몰 삽입당} 엔트로피 변화, 곧 부분몰량이다.<br>식~\eqref{eq:Sconfig} 를 $\theta$ 로 미분하면, | §2-L1 참조 | $S_\config$ 는 자리 1몰당인데 $\theta$-미분이 곧 Li 1몰당이 되는 근거($\dd n_\mathrm{Li}=n_\mathrm{site}\dd\theta$ 로 $n_\mathrm{site}$ 약분)가 무언급 — 단위에 엄밀한 본 장 관행(§2.3 C-66)과 비대칭 |
| A12-09 | ch2_sec03_vibel.tex:42–44(srcbox) | 설명("제일원리" 한 문장 내 이중 어의) | L | 본문은 vib 항을 포논 BE 분포에서<br>제일원리적으로 세워(식~\eqref{eq:Svib_mode}) … 모드별 정량은 제일원리 포논(\cite{jpcc2021}) 소관으로 넘긴다. | §2-L2 참조 | 같은 문장에서 "제일원리"가 (i) 통계역학 원리로부터의 유도, (ii) DFT(제일원리 포논)의 두 뜻으로 연속 사용 — 첫째를 "통계 원리로부터"로 바꾸면 어의 충돌 해소 |
| A12-10 | ch2_sec03_vibel.tex:27–29 | 보완(몰 기준 명시) | L | 전<br>모드에 대해 합하고 1몰당으로 환산하면($R=N_A\kB$ 를 써서) 격자의 vibrational 엔트로피는 | §2-L3 참조 | "1몰당"의 기준(호스트 formula C$_6$ 1몰당 — 그래야 $\partial/\partial x$ 가 Li 1몰당 부분몰량)이 무명시. §2.3 전자항은 자리당/몰당을 명시(C-66)하는 것과 비대칭 |
| A12-11 | ch2_sec03_vibel.tex:50–52 | 설명(지시 대상 불명 포인터) | L | 다온도 곡률 피팅에서 이 vib 잔여가 electronic($\propto T$,<br>\S\ref{ssec:elec}) 신호에 소량 섞일 수 있다(Part I 의 대응 한정과 동급). | §2-L4 참조 | "Part I 의 대응 한정"에 \S\ref 부재 — Part I 전수 검색 결과 가장 가까운 대응은 ch1_sec07_broadening:156 의 "$L_V\propto|I|$ 라 대칭 폭 $w_j$ 와 분리 식별" 한정(함수형 차이로 두 형상 기여를 가르는 같은 논리). 명시 앵커 필요(대상 확정은 저자 몫) |
| A12-13 | ch2_sec03_vibel.tex:68–71 | 설명(유도 사슬 한 고리 괄호 보충) | L | 를 닫고($g$ 를 창 안에서 $g(E_F)$ 로 동결), 이를 $S_e=\int_0^T (C_e/T')\,\dd T'$ 로 적분하면 | §2-L5 참조 | Sommerfeld 적분→$C_e$ 사이 다리($C_e=(1/T)\int g(E-E_F)^2(-\partial f/\partial E)\dd E$)가 생략 — 전 단계는 Chapter 2 위임으로 정당하나 괄호 한 줄이면 본문만으로 검산 가능(LCO §lco-Se 원문의 사슬과 동일함 확인) |
| A12-14 | ch2_sec03_vibel.tex:76–78 | 문체(전방 참조 시제 불일치) | L | 는 Chapter 2 \S\ref{sec:lco-electronic}(LCO 전자 엔트로피)의 전자<br>엔트로피 유도가 상술했고, 본 파트는 그 결과를 분포 언어로 확장해 받는다. | §2-L6 참조 | v1.0.22 재편으로 LCO 는 뒤 장(Chapter 2) — 과거형 "상술했고"는 독자가 이미 읽었다는 함의(구판 잔재: v1.0.21 은 같은 문서 앞 절 "Chapter 1 §15" 였음, diff 확인). 같은 파일 :89 는 현재형 "상술한다" — 시제 통일 |

---

## 2. 등급별 상세 (축자 정본 + 완성 LaTeX 제안)

### H (0건)

H(논리/물리 오류·오귀속 확정) 없음 — §2.2·§2.3 의 수식·유도·부호·수치는 재계산에서 전건 통과(§3 검증 로그). 오귀속 *위험* 2건(A12-12·A12-15)은 전문 미접근 한도에서 M 로 분류.

### M (9건)

#### §2-M1 = A12-02 — 상호작용(Ω) 항이 $\partial V/\partial T|_\xi$ 에 안 들어가는 이유의 다리 문장

현행 축자 (ch2_sec02_config.tex:50–52):
```latex
(후술 \S\ref{ssec:overlap} 식~\eqref{eq:dxidT}). 곧 \textbf{Part I 의 logistic 폭 $w=RT/F$ 가 이미 부분몰
configurational 엔트로피를 담고 있었다}. 봉우리 내부 $\partial U_\oc/\partial T(x)$ 의 $x$-의존(비선형 모양)은
새 물리가 아니라, 점유 분포의 엔트로피가 $w$ 의 온도 의존을 통해 자동으로 들어온 것이다.
```
제안 (직후에 추가 — 삭제 없음):
```latex
이 결과는 이상 격자기체 서식~\eqref{eq:Vxi} 를 미분한 것이지만, 상호작용을 켠 식~\eqref{eq:Veq_BW} 로
시작해도 달라지지 않는다 --- 추가 항 $-\Omega(1-2\theta)/F$ 는 $\Omega$ 가 $T$-무관인 한(Part I 의 상수
취급) 고정 $\xi$ 의 온도 미분에 기여하지 않기 때문이다. $\partial\Omega/\partial T\ne0$ 의 상호작용
엔트로피는 본 장 범위 밖의 2차 항이다(\S\ref{ssec:weff} 끝 warnbox 의 같은 한정).
```
근거: 재유도 — $V_\eq(\theta)=U_j-(RT/F)\ln[\theta/(1-\theta)]-(\Omega/F)(1-2\theta)$ 를 고정 $\theta(=1-\xi)$ 에서 $T$-미분하면 로그 항 몫은 eq:dVdT_config 와 동일하고 잔여는 $-(\partial\Omega/\partial T)(1-2\theta)/F$ 뿐. §2.1 독자가 방금 eq:Veq_BW 를 봤으므로 이 질문은 필연적. §2.5 파생 C warnbox 끝 문장("상호작용 엔트로피 $\propto\partial\Omega/\partial T$ 같은 2차 항 … 본 장 범위 밖")과 정확히 접속.

#### §2-M2 = A12-03 — 단일 전이 발산 vs 유한 실측 프로파일의 다리(겹침 자기 억제)

현행 축자 (ch2_sec02_config.tex:66–68 — 3분기 itemize 직후 문단 첫 문장):
```latex
이 세 분기의 부호는 \S\ref{ssec:logistic} 의 규약 $\xi=1-\theta$ 에 매여 있다 --- 만약 점유율 $\theta$ 와
진행률 $\xi$ 를 뒤섞으면 $\ln[\xi/(1-\xi)]$ 의 인자가 뒤집혀 희박$\cdot$만충 극한의 발산 부호($\pm\infty$)가
반대로 읽히므로, 두 이름을 끝까지 구분해야 한다.
```
제안 (이 문단 앞에 한 문장 삽입 — 삭제 없음):
```latex
덧붙여 이 $\pm\infty$ 는 \emph{단일 전이 시야}의 극한이다 --- 겹침 관측(\S\ref{ssec:overlap})에서는 발산
인자 $z_j=\ln[\xi_j/(1-\xi_j)]$ 가 그 전이의 국소 가중 $g_j\propto\xi_j(1-\xi_j)$ 와 곱으로만 들어와
$g_jz_j\to0$ ($\xi_j\to0,1$)으로 스스로 꺼지고 이웃 전이가 가중을 이어받으므로, 내부 전이 경계의 실측
프로파일은 유한한 봉우리$\cdot$골로 남는다. 로그 항이 그대로 드러나는 곳은 이어받을 이웃이 없는 전역
양끝(희박$\cdot$만충 끝)뿐이다.
```
근거: 재계산 — $\lim_{\xi\to0,1}\xi(1-\xi)\ln[\xi/(1-\xi)]=0$; eq:implicit_diff 의 분자·분모 비에서 내부 경계는 인접 $\Delta S^0/F$ 사이 값으로 수렴(§2.5 수치 검증 "내부 전이 경계 3 곳 모두 계단 없이 연속 블렌드" 문면과 정합), 전역 끝은 가중비가 최근접 전이 하나로 수렴해 $\Delta S^0_{j^*}/F+n_{j^*}Rz_{j^*}/F$ 의 로그 발산이 잔존(배경항 없는 Part T 음함수 기준). §2.0 서두의 "발산에 가깝게 치솟는다"(전역 저-$x$)와도 정합.

#### §2-M3 = A12-04 — 같은 구간 문헌값의 "범위" vs "정확" 서술 정합

현행 축자 a (ch2_sec02_config.tex:137–139):
```latex
$2\to1$($x\approx0.5$)에서 급변을 보인다고 보고한다 \cite{reynier2003,allart2018}. 정량으로는 전극
$\Delta S\approx+29$ J\,mol$^{-1}$K$^{-1}$ @\,$x=0.08$, $-5\sim-16$ J\,mol$^{-1}$K$^{-1}$ @\,$x>0.5$ 이고
\cite{allart2018},
```
현행 축자 b (ch2_sec02_config.tex:163 — tab:ds 4행):
```latex
$2\!\to\!1$ & 0.50–1.00 & $-16.0$ & $-16$ @\,$x{>}0.5$ (양 끝, 정확) \\
```
제안 (표 4행 괄호 보강 — 본문은 불변):
```latex
$2\!\to\!1$ & 0.50–1.00 & $-16.0$ & $-16$ @\,$x{>}0.5$ (양 끝 --- 문헌 $x{>}0.5$ 변동 범위 $-5\sim-16$ 중 평탄역 값과 일치) \\
```
근거: 본문(범위 $-5\sim-16$)과 표("정확")가 같은 구간·같은 문헌에 대해 다른 정밀도 주장으로 읽힘 — 관계(범위 내 평탄역 대표값) 명시로 해소. "(정확)" 낱말은 표 각주의 "$-16$@$x>0.5$ 쪽은 평탄역 내부 대조라 이 한정이 필요 없다"(:146–147)와는 정합하나 본문 범위 서술과의 연결 고리가 없음. Allart 프로파일 세부 수치는 원문 전문 미접근 [미검증-원문] — 제안은 두 서술의 내부 정합만 복구.

#### §2-M4 = A12-05 — tab:ds 대조의 성격(계보 확인 vs 독립 검증) 한정

현행 축자 (ch2_sec02_config.tex:143–145):
```latex
표~\ref{tab:ds} 는 Part I 의 전이별 중심 표준값 $\Delta S^0_j=+29\to0\to-5\to-16$ J\,mol$^{-1}$K$^{-1}$ 가
이 문헌 프로파일과 부호$\cdot$규모에서 정합함을 보인다 --- 곧 분포 spine 의 입력 표준값이 임의값이 아니라
측정에 닿아 있다.
```
제안 (직후에 추가 — 삭제 없음):
```latex
이 대조의 성격을 한정한다 --- $\Delta S^0_j$ 초기값 자체가 실측 스케일에 맞춰 놓인 출발값이므로
(표~\ref{tab:staging} 캡션의 reynier2003 정합 주석), 양 끝 값의 수치 일치는 독립 검증이 아니라 입력
\emph{계보}(traceability) 확인이다. 이 표의 비-자명한 내용은 (i) 중간 두 전이가 문헌 하강 \emph{구간
안}에 놓인다는 범위 정합과 (ii) 양$\to$음 전환 위치가 문헌 보고 저-$x$ 창($x\approx0.2$--$0.25$)과 겹친다는
위치 정합이다.
```
근거: tab:staging 캡션 원문 "$\Delta S_\rxn$ 의 부호·수십 J/(mol K) 스케일은 흑연 삽입 엔트로피 실측\cite{reynier2003} 과 정합(전이별 정밀값 아님 --- tier B)" — 입력이 문헌 계열에서 온 이상 +29·−16 끝값 일치는 구성상 결과. 절 제목("문헌 검증")의 하중을 이 한정이 정직하게 만들며, 기존 도입 문단의 "+29 끝점 구간 대표" 한정과 결이 같다(보강·비삭제).

#### §2-M5 = A12-06 — 형성→미분 환산의 실제 결과(−3.0 vs −13.0) 제시

현행 축자 (ch2_sec02_config.tex:175–178):
```latex
엔탈피 쪽 표준값 $\Delta H^0_j$ 는 \emph{기준 차이}에 주의해야 한다: Part I 의 $\Delta H_{\rxn,j}$ 는
\emph{전이별}(differential) 반응 엔탈피이고, calorimetry 의 형성 엔탈피(LiC$_6$ $-13.9$, LiC$_{12}$ $-24.8$
kJ/mol\,Li \cite{chemmater2015})는 \emph{누적}(formation, graphite$+$Li 금속 기준)이라 직접 등치할 수 없다 ---
비교하려면 형성 엔탈피의 $x$-미분으로 환산해야 한다.
```
제안 ("환산해야 한다." 직후에 추가 — 삭제 없음):
```latex
실제로 환산해 보면 간극이 남는다 --- stage $2\to1$(Li$+$LiC$_{12}\to2\,$LiC$_6$)의 형성값 유한차분은
$2\Delta H_f(\mathrm{LiC_6})-\Delta H_f(\mathrm{LiC_{12}})=2(-13.9)-(-24.8)=-3.0$ kJ/mol\,Li 로, 본 문서
전이값 $-13.0$ kJ/mol 과 $10$ kJ/mol 급 차이가 환산 후에도 남는다. 이 문헌값은 LiH 경로 고온 합성의
준안정 stage 상대안정성 맥락(abstract tier)이라 전기화학 formation 과 절대 기준이 같다는 보장이 없으므로,
여기서는 \emph{기준 차이 경고}로만 쓰고 정량 anchor 로 쓰지 않는다.
```
근거: 재계산 확정 — $2(-13.9)-(-24.8)=-3.0$; 전기화학 쪽은 $U=0.085$ V·$\Delta S=-16$ 에서 $\Delta H=-13.0$ kJ/mol(§3 축 A 검산). 환산 권유만 있고 결과가 없으면 독자 검산이 미해명 모순으로 끝남 — 결과와 해석 한정을 함께 제시해야 인용 목적(기준 차이 경고)이 완결. 서브 검증(§4): 두 수치·per mol Li·직접 열량계·LiH 경로는 원문 abstract 계열 스니펫에서 확인(전문 미접근 — 455 K 세부는 스니펫 수준).

#### §2-M6 = A12-07 — BE 닫힌형 두 항의 직관 귀속을 유도 가능한 서술로 대체

현행 축자 (ch2_sec03_vibel.tex:27):
```latex
가 된다 --- 여기서 첫 항은 빈 들뜸을 채우는 경우의 수, 둘째 항은 이미 들뜬 양자의 가짓수에서 온다. 전
```
제안 (해당 구절 대체):
```latex
가 된다 --- 이 닫힌형은 모드 들뜸수의 열적 분포(기하분포 $P_m=(1-e^{-\beta\hbar\omega_k})e^{-m\beta\hbar\omega_k}$)의
정보 엔트로피 그 자체이고, 보손 미시상태 셈 $W=\binom{N+g-1}{N}$ 의 Stirling 전개에서 $(N{+}g)!$ 몫이
첫 항, $N!$ 몫이 둘째 항으로 남는 셈으로도 같은 식이 나온다. 전
```
근거: 재유도 두 건 통과 — (i) $-\sum_mP_m\ln P_m=-\ln(1-e^{-x})+x\,n$ (기하분포 Shannon 엔트로피 = 본문 자신이 병기한 "정보 엔트로피" 경로의 실체) ✓; (ii) $\ln W\approx(N{+}g)\ln(N{+}g)-N\ln N-g\ln g$, $n=N/g$ 대입 시 모드당 $(1+n)\ln(1+n)-n\ln n$ — 첫/둘째 항이 각각 $(N{+}g)!$·$N!$ 몫 ✓. 현행 문구("빈 들뜸을 채우는 경우의 수"/"이미 들뜬 양자의 가짓수")는 단일 모드에서 조합적으로 성립하지 않는 귀속이라 이 문서의 검산 가능성 기준에 미달.

#### §2-M7 = A12-08 — $\Delta S_\vib$ 부호·$T$-의존을 닫는 한 줄 항등식 (산문→수식)

현행 축자 (ch2_sec03_vibel.tex:29–31):
```latex
$S_\vib=R\sum_k[(1+n_k)\ln(1+n_k)-n_k\ln n_k]$ 가 된다. 삽입에 따른 부분몰 변화 $\Delta S_\vib=\partial
S_\vib/\partial x$ 는 모드 연화/경화에 따라 부호가 갈리는데, 흑연에서는 고-$x$(만충에 가까운) 영역에서
\emph{음의 baseline}을 만든다(Reynier 의 ``second contribution'') \cite{reynier2003}.
```
제안 ("부호가 갈리는데" 문장을 다음으로 보강 — 기존 문장 유지 후 식 삽입; 라벨은 제안 표기):
```latex
$S_\vib=R\sum_k[(1+n_k)\ln(1+n_k)-n_k\ln n_k]$ 가 된다. 삽입에 따른 부분몰 변화는 모드별 진동수 이동으로
닫힌다 --- $S_{\vib,k}$ 가 $\omega_k$ 와 $T$ 에 $\beta\hbar\omega_k$ 로만 의존하므로
\begin{equation}
\Delta S_\vib \;=\; \frac{\partial S_\vib}{\partial x}
\;=\; -\sum_k \bar c_k(T)\,\frac{\partial\ln\omega_k}{\partial x},
\qquad
\bar c_k(T)\;=\;R\,\frac{(\beta\hbar\omega_k)^2 e^{\beta\hbar\omega_k}}{(e^{\beta\hbar\omega_k}-1)^2},
\label{eq:dSvib-x}% 제안 라벨(기존 eq:dSvib 와 별개)
\end{equation}
이다($\bar c_k$ = 모드 비열의 몰 환산). 경화($\partial\ln\omega_k/\partial x>0$)면 음, 연화면 양이고,
흑연에서는 고-$x$(만충에 가까운) 영역에서 \emph{음의 baseline}을 만든다(Reynier 의 ``second
contribution'') \cite{reynier2003}. 고전 극한에서 $\bar c_k\to R$ 이라 $\Delta S_\vib$ 는 $T$-무관 상수로
닫히고(아래 ``중심 흡수''의 전제가 이 극한이다), 준양자 모드는 $\bar c_k(T)$ 의 잔여 $T$-의존을 남긴다
(\S\ref{sec:einstein} 의 대상).
```
근거: 재유도 — $u\equiv\beta\hbar\omega$ 로 $\partial S/\partial\ln\omega=u\,S'(u)$, $T\,\partial S/\partial T=-u\,S'(u)=\bar c$ (모드 비열) ⇒ $\partial S/\partial\ln\omega=-\bar c$ ✓; 고전 극한 $\bar c\to R$ 에서 $\Delta S_\vib=-R\sum_k\partial\ln\omega_k/\partial x$ 는 $T$-무관 ✓ — :49–50 의 "고전 극한 … $T$-무관 상수" 주장과 :50–52 의 준양자 잔여 서술이 이 한 식의 두 극한으로 통합됨(관점 ④의 정확·간결화 + §2.4 동기 접속). 기호는 절 내 기존 표기($\beta\hbar\omega_k$)만 사용, 신규 라벨은 제안 표기.

#### §2-M8 = A12-12 — "$\Delta S_e<0$ 일반" 과대 일반화 정정(부호↔규모 분리)

현행 축자 a (ch2_sec03_vibel.tex:80–82):
```latex
는 삽입이 $g(E_F)$ 와 $E_F$ 를 바꾸는 방식에 달려 있다. 본 장의 규약대로, 삽입(리튬화)은 일반적으로
$\Delta S_e<0$ 이다 --- 밴드 채움으로 $E_F$ 부근 상태밀도가 줄어드는 호스트가 많기 때문이다.
```
현행 축자 b (ch2_sec03_vibel.tex:84–85):
```latex
\item \textbf{흑연 하프셀}: 흑연은 준금속이라 $g(E_F)$ 가 작아 $\Delta S_e\approx0$ --- 전자 항은 소수이고
config$+$vib 가 지배한다. 본 장 주 사례에서 electronic 은 보정항이다.
```
제안 a (해당 구절 대체):
```latex
는 삽입이 $g(E_F)$ 와 $E_F$ 를 바꾸는 방식에 달려 있다 --- 부호를 정하는 것은 리튬화 일반이 아니라
$\partial g(E_F)/\partial x$ 다. 밴드 채움으로 $E_F$ 부근 상태밀도가 줄어드는 호스트는 $\Delta S_e<0$
이고(아래 LCO 가 대표), 반대 방향의 호스트도 있다(아래 흑연).
```
제안 b (bullet 대체):
```latex
\item \textbf{흑연 하프셀}: 부호와 규모가 갈린다 --- 삽입 전자가 $E_F$ 를 준금속 최소점 위로 올려
$g(E_F)$ 는 오히려 커지지만($\partial g/\partial x>0$ 방향), $S_e\sim(\pi^2/3)\kB^2T\,g(E_F)$ 의 몰 환산
규모 자체가 config$\cdot$vib 의 수십 J\,mol$^{-1}$K$^{-1}$ 에 크게 못 미쳐 $\Delta S_e\approx0$ --- 전자
항은 부호와 무관하게 소수이고 config$+$vib 가 지배한다. 본 장 주 사례에서 electronic 은 보정항이다.
```
근거: (논리) 부호는 $\partial g(E_F)/\partial x$ 의 성질 — "일반적으로 <0" 은 주 사례 흑연이 방향 반례가 되는 과대 일반화. 흑연 방향(π* 상승·$g$ 증가·LiC$_6$ 금속성)은 표준 밴드구조 결과 — 서브 검증에서 Holzwarth 1978(PRB 18, 5190, DOI 10.1103/PhysRevB.18.5190) 서지 확정 + "Fermi level of LiC$_6$ … near a saddle point in the $\pi$ bands" 스니펫 확인(전문 미접근 [추정] — 인용하려면 원장 등재 절차 필요, §4 후보 표). 기존 결론($\Delta S_e\approx0$·보정항·LCO 음 부호)은 전부 보존 — 논거만 부호↔규모로 분리.

#### §2-M9 = A12-15 — msmr_partI 인용 하중 재배치(지지되는 반쪽에만)

현행 축자 (ch2_sec03_vibel.tex:101–105):
```latex
한 가지 경계를 못박고 절을 닫는다. 가역 발열에 들어가는 것은 위 세 분포가 주는 \emph{반응(평형) 엔트로피}
$\Delta S(x)$ 뿐이다. 이는 \S\ref{sec:lag}$\cdot$\S\ref{sec:tail} 동역학 꼬리의 \emph{활성화 엔트로피} $\Delta S_{a,j}$(Eyring
속도 $k_j\propto\exp[-(\Delta H_a-T\Delta S_a)/RT]$ 의 prefactor 몫)와 \emph{차원은 같으나 물리가 다른
양}이다. 활성화 엔트로피는 \emph{비가역} 동역학을 지배하고 가역 발열에는 들어가지 않으므로 \cite{msmr_partI},
둘을 혼동하면 가역 발열을 동역학 lag 와 섞게 된다.
```
제안 (마지막 두 문장 대체):
```latex
활성화 엔트로피는 \emph{비가역} 동역학을 지배하고 가역 발열에는 들어가지 않는다 --- 가역 발열을 지배하는
것이 (평형) 엔트로피 계수라는 틀은 \cite{msmr_partI} 그대로이고, 반응/활성화의 구분 자체는 Part I 의
TST 유도(\S\ref{sec:lag})가 닫는다. 둘을 혼동하면 가역 발열을 동역학 lag 와 섞게 된다.
```
근거: 서브 검증(abstract 축자, §4) — msmr_partI abstract 는 "The entropy coefficient of a battery cell is the property that governs the amount of reversible heat" 로 전반(가역 발열↔평형 엔트로피 계수)을 명시 지지하나, "활성화 엔트로피 배제" 명제는 abstract 에 없음(전문 미접근). 현행 cite 위치는 미확인 반쪽까지 문헌에 지움 — 오귀속 위험 [추정]. 재배치는 문헌 하중을 지지 확인분에 한정하고 배제 명제를 본 문서 자산(§sec:lag TST)에 앵커.

### L (6건)

#### §2-L1 = A12-01 — 부분몰=자리미분 등치의 한 줄 근거

현행 축자 (ch2_sec02_config.tex:23–24):
```latex
가역 발열에 들어가는 것은 $S_\config$ 자체가 아니라 \emph{Li 1몰 삽입당} 엔트로피 변화, 곧 부분몰량이다.
식~\eqref{eq:Sconfig} 를 $\theta$ 로 미분하면, $\theta\ln\theta$ 항이 $\ln\theta+1$ 을, $(1-\theta)\ln(1-\theta)$
```
제안 (첫 문장 뒤 괄호 추가):
```latex
가역 발열에 들어가는 것은 $S_\config$ 자체가 아니라 \emph{Li 1몰 삽입당} 엔트로피 변화, 곧 부분몰량이다
(전체 엔트로피는 자리 몰수 $n_\mathrm{site}$ 배, 삽입량은 $\dd n_\mathrm{Li}=n_\mathrm{site}\,\dd\theta$
이므로 $n_\mathrm{site}$ 가 약분되어 자리 1몰당 식의 $\theta$-미분이 그대로 Li 1몰 삽입당이다).
```

#### §2-L2 = A12-09 — srcbox "제일원리" 이중 어의 해소

현행 축자 (ch2_sec03_vibel.tex:42–44):
```latex
$\cdot$추세를 두 기여로 정성 분해하나(전이별 정밀값 아님, tier B), 본문은 vib 항을 포논 BE 분포에서
제일원리적으로 세워(식~\eqref{eq:Svib_mode}) 봉우리 폭 안 $T$-무관 상수로 중심 흡수하므로, Reynier 는 고-$x$
음 baseline 의 부호$\cdot$스케일 앵커로만 쓰고 모드별 정량은 제일원리 포논(\cite{jpcc2021}) 소관으로 넘긴다.
```
제안 ("제일원리적으로 세워" → "통계 원리로부터 세워"):
```latex
$\cdot$추세를 두 기여로 정성 분해하나(전이별 정밀값 아님, tier B), 본문은 vib 항을 포논 BE 분포에서
통계 원리로부터 세워(식~\eqref{eq:Svib_mode}) 봉우리 폭 안 $T$-무관 상수로 중심 흡수하므로, Reynier 는 고-$x$
음 baseline 의 부호$\cdot$스케일 앵커로만 쓰고 모드별 정량은 제일원리 포논(\cite{jpcc2021}) 소관으로 넘긴다.
```

#### §2-L3 = A12-10 — $S_\vib$ "1몰당" 기준 명시

현행 축자 (ch2_sec03_vibel.tex:27–29):
```latex
모드에 대해 합하고 1몰당으로 환산하면($R=N_A\kB$ 를 써서) 격자의 vibrational 엔트로피는
```
제안:
```latex
모드에 대해 합하고 호스트 formula 단위(C$_6$) 1몰당으로 환산하면($R=N_A\kB$ 를 써서 --- 그래야
$x$-미분이 Li 1몰 삽입당 부분몰량이 된다) 격자의 vibrational 엔트로피는
```

#### §2-L4 = A12-11 — "Part I 의 대응 한정" 명시 앵커

현행 축자 (ch2_sec03_vibel.tex:50–52):
```latex
관련 포논 모드가 고전 극한 $\kB T\gg\hbar\omega$ 에 있을 때의 근사다. 준양자 영역($\kB T\!\sim\!\hbar\omega$)의
모드는 작은 잔여 $T$-의존을 남기며, 다온도 곡률 피팅에서 이 vib 잔여가 electronic($\propto T$,
\S\ref{ssec:elec}) 신호에 소량 섞일 수 있다(Part I 의 대응 한정과 동급).
```
제안 (괄호 구체화 — 지시 대상 최종 확정은 저자 몫):
```latex
\S\ref{ssec:elec}) 신호에 소량 섞일 수 있다(두 형상 기여를 함수형 차이로 분리 식별하던 Part I 의
한정 --- 꼬리 길이 $L_V\propto|I|$ vs 전류 무관 폭 $w_j$, \S\ref{sec:broadening} --- 과 동급).
```
근거: Part I 전수 검색에서 "대응 한정"의 유일 근접 후보 = ch1_sec07_broadening:156 "전류에 비례해 소멸하여($L_V\propto|I|$) 대칭 폭 $w_j$ 와 분리 식별되기 때문이다".

#### §2-L5 = A12-13 — Sommerfeld 사슬 한 고리 괄호 보충

현행 축자 (ch2_sec03_vibel.tex:70–71):
```latex
를 닫고($g$ 를 창 안에서 $g(E_F)$ 로 동결), 이를 $S_e=\int_0^T (C_e/T')\,\dd T'$ 로 적분하면($C_e/T'$ 가
$T'$-무관 상수이므로 곧바로 닫혀)
```
제안 (첫 괄호 보강):
```latex
를 닫고($g$ 를 창 안에서 $g(E_F)$ 로 동결 --- 중간 사슬은 $C_e=(1/T)\int g(E)\,(E-E_F)^2(-\partial f/\partial
E)\,\dd E$, 전 단계는 Chapter 2 \S\ref{sec:lco-electronic}), 이를 $S_e=\int_0^T (C_e/T')\,\dd T'$ 로
적분하면($C_e/T'$ 가 $T'$-무관 상수이므로 곧바로 닫혀)
```

#### §2-L6 = A12-14 — 전방 참조 시제 통일("상술했고" → 현재형)

현행 축자 (ch2_sec03_vibel.tex:76–78):
```latex
가 되어 온도에 \emph{선형}이고 Fermi 준위 상태밀도 $g(E_F)$ 에 비례한다. 이 Fermi--Dirac$\to$Sommerfeld
유도의 전 단계 --- 정보 엔트로피 합에서 비열을 거쳐 $S_e$ 까지 --- 는 Chapter 2 \S\ref{sec:lco-electronic}(LCO 전자 엔트로피)의 전자
엔트로피 유도가 상술했고, 본 파트는 그 결과를 분포 언어로 확장해 받는다.
```
제안:
```latex
가 되어 온도에 \emph{선형}이고 Fermi 준위 상태밀도 $g(E_F)$ 에 비례한다. 이 Fermi--Dirac$\to$Sommerfeld
유도의 전 단계 --- 정보 엔트로피 합에서 비열을 거쳐 $S_e$ 까지 --- 는 Chapter 2 \S\ref{sec:lco-electronic}(LCO 전자 엔트로피)의 전자
엔트로피 유도가 상술한다(전방 참조). 본 파트는 그 결과를 분포 언어로 확장해 받는다.
```
근거: 같은 파일 :89 "Chapter 2 \S\ref{sec:lco-hys}$\cdot$\S\ref{sec:lco-electronic} 가 상술한다"(현재형)와 통일. v1.0.21 diff 로 확인 — 구판에서는 같은 문서 앞 절("Chapter 1 §15")이라 과거형이 참이었으나, 재편 후 LCO 는 뒤 장.

---

## 3. 검증 로그 (재계산·재유도 — 축별)

### [축 A] §2.2 수식 재유도 — 전건 재계산 완료 (2026-07-17)

| 항목 | 재계산 | 판정 |
|---|---|---|
| eq:Sconfig ↔ eq:BW 둘째 항 | BW 둘째 항 $RT[\theta\ln\theta+(1-\theta)\ln(1-\theta)]$ ÷ $(-T)$ = $-R[\theta\ln\theta+(1-\theta)\ln(1-\theta)]$ = eq:Sconfig | 일치 ✓ |
| eq:dSconfig | $d/d\theta[\theta\ln\theta]=\ln\theta+1$, $d/d\theta[(1-\theta)\ln(1-\theta)]=-\ln(1-\theta)-1$, ±1 상쇄 → $-R\ln[\theta/(1-\theta)]$ | 재유도 일치 ✓ |
| eq:dVdT_config | eq:Vxi(§2.1 원문 확인: $V=U_j+(RT/F)\ln[\xi/(1-\xi)]$)를 $T$-미분: $\partial U_j/\partial T+(R/F)\ln[\xi/(1-\xi)]$; $\partial S_\config/\partial\theta\vert_{\theta=1-\xi}=-R\ln[(1-\xi)/\xi]=+R\ln[\xi/(1-\xi)]$ → $(1/F)$ 배가 둘째 항과 정확 일치 | 재유도 일치 ✓ |
| BW 확장 불변성(A12-02 근거) | $V_\eq(\theta)$ 의 $-\Omega(1-2\theta)/F$ 는 고정 $\xi$ 에서 $-(\partial\Omega/\partial T)(1-2\theta)/F$ 만 기여 — $\Omega$ 상수면 0 | 확정 ✓ |
| 부호 3분기 | $\xi\to1$: $+\infty$ / $\xi\to0$: $-\infty$ / $\xi=1/2$: $0$ (θ=1−ξ 규약 하) | 일치 ✓ |
| 발산 자기 억제(A12-03 근거) | $\lim_{\xi\to0,1}\xi(1-\xi)\ln[\xi/(1-\xi)]=0$; 가중비는 내부 경계에서 인접 $\Delta S^0/F$ 블렌드, 전역 끝에서 단일 전이 로그 발산 | 확정 ✓ |
| n_jR/F 일반형 | §2.5 eq:dxidT 원문 — 둘째 조각 계수 $n_jR/F$; eq:single_config $n_jR\ln[\xi_j/(1-\xi_j)]/F$ | 전달 정합 ✓ |
| 단위 각주 | $29/96485=3.006\times10^{-4}$ V/K $=0.30$ mV/K; "3–4 mV/K"와 1자릿수 차 — 각주의 [미검증] 태그 타당 | 일치 ✓ |
| ΔH⁰ 검산(2→1) | $U_j(298.15)=(13000-298.15\times16)/96485=0.08529$ V; 역산 $-F(0.08529)+298.15(-16)=-8229.6-4770.4=-13000$ J/mol = **−13.0 kJ/mol** — tab:staging ΔH_rxn=−13000 일치("표값 일치" 검증) | 일치 ✓ |
| 형성값 유한차분(A12-06 근거) | $2(-13.9)-(-24.8)=-3.0$ kJ/mol Li ≠ $-13.0$ (간극 10 kJ/mol) | 확정 ✓ |
| tab:ds ↔ tab:staging | ΔS⁰ 4행(+29.0/0.0/−5.0/−16.0) 동일; 4행 전부 $U(298)$ 재계산 0.21088/0.13992/0.12032/0.08529 V — 표 U 와 ±1 mV 정합 | 일치 ✓ |
| fig:occ_config | (a) $\langle n\rangle=1/(1+e^{-(\mu-\varepsilon_0)/\kB T})$ = eq:occ 동형; (b) max $\ln2$@θ=1/2(플롯 수식 검산 2.5 스케일 정확), 양끝 ±∞ 라벨 방향 정확(θ→0 에서 +∞). "→−∞" 라벨 x-위치(θ≈0.78)는 우단(θ→1)보다 안쪽 — 장식적 배치로 판단, 스킵 | 일치 ✓ |

### [축 B] §2.2·§2.3 참조·라벨·서지 — 전건 확인 완료 (2026-07-17)

- ch1 빌드 aux 라벨 해소: eq:BW·eq:Vxi·eq:occ·eq:dxidT·ssec:BW·ssec:logistic·sec:width·ssec:overlap·ssec:derivB·sec:einstein·sec:mixing·sec:limits·sec:lag·sec:tail·sec:sm-site·sec:sm-lattice — **전건 존재** ✓
- LCO 외부 라벨(\externaldocument): sec:lco-decomp·sec:lco-electronic·sec:lco-hys — ch2_lco aux 에 **전건 존재** ✓
- Part 0 실물 확인: 페르미온·보손 bgbox = ch1_sec02a:198(sec:sm-site :106 이하 소속 — §2.3:9 지시 정확) ✓; eq:sm-sint = :324 ✓; $R=N_A\kB$ 단위 환산 = :378(sec:sm-lattice :342 이하 소속 — §2.3:80 지시 정확) ✓
- 매크로·환경: \avg·\config·\oc·\rxn·\vib·\kB·\dd·\eq·\rev·\app 정의 확인(common_preamble :43–63) ✓; warnbox·keybox·srcbox·bgbox = newtheorem* 정의 확인(:32–39) ✓
- 서지 7키(reynier2003·allart2018·occupation2019·chemmater2015·jpcc2021·msmr_partI·msmr_partII): ch1v22_bib.tex 전건 수록 ✓ · V1022→V1021→V1020 원장 승계 체인에서 **전건 V1**(msmr_partI=C-005 보완·msmr_partII=C-006 정정 후) ✓ · 본문 한정문(occupation2019 "방법 수준·dilute 격자기체 한정" / reynier2003 tier B "전이별 정밀값 아님")이 bib 비고와 정합 ✓

### [축 C] §2.3 수식 재유도 + 앞뒤 절 핸드오프 — 전건 완료 (2026-07-17)

| 항목 | 재계산/대조 | 판정 |
|---|---|---|
| eq:Svib_mode 유도 | $f_k=\kB T\ln(1-e^{-\beta\hbar\omega_k})$, $S=-\partial f/\partial T=-\kB\ln(1-e^{-\beta\hbar\omega})+\kB\beta\hbar\omega\,n$ (본문 중간식과 일치); 항등식 $1-e^{-x}=1/(1+n)$·$x=\ln[(1+n)/n]$ 대입 → $\kB[(1+n)\ln(1+n)-n\ln n]$ | 재유도 일치 ✓ |
| 기하분포 검산(A12-07 근거) | $-\sum_m P_m\ln P_m=-\ln(1-e^{-x})+x\langle m\rangle$ = 위 중간식; Stirling: $\ln\binom{N+g-1}{N}\to g[(1+n)\ln(1+n)-n\ln n]$ | 확정 ✓ |
| $\partial S/\partial\ln\omega=-\bar c$ (A12-08 근거) | $u=\beta\hbar\omega$: $\partial S/\partial\ln\omega=uS'(u)$; $\bar c=T\,\partial S/\partial T=-uS'(u)$ ⇒ 항등; 고전 극한 $\bar c\to R$ ⇒ $\Delta S_\vib$ $T$-무관(본문 :49–50 의 "고전 극한 근사" 주장 재유도 확정) | 재유도 일치 ✓ |
| 영점 에너지 생략 | $\hbar\omega/2$ 는 $T$-무관 → $-\partial/\partial T$ 에서 0 — 본문 근거 정확 | 일치 ✓ |
| eq:Se_start·Sommerfeld | $\int(-\partial f/\partial E)(E-E_F)^2\dd E=(\kB T)^2\int x^2e^x/(e^x+1)^2\dd x=(\pi^2/3)(\kB T)^2$ ✓; $C_e=(1/T)\int g(E-E_F)^2(-\partial f/\partial E)\dd E\to(\pi^2/3)\kB^2Tg(E_F)$ ✓; $S_e=\int_0^T(C_e/T')\dd T'=\gamma T$ ✓ | 재유도 일치 ✓ |
| $S_e$ 차원 | $[\kB^2Tg]=(\mathrm{J/K})^2\cdot\mathrm K\cdot\mathrm J^{-1}=\mathrm{J/K}$ = $\kB$ 차원 — 본문 서술 정확 | 일치 ✓ |
| Eyring 형 | $k=(\kB T/h)\exp[-(\Delta H_a-T\Delta S_a)/RT]$ — prefactor 몫 $e^{\Delta S_a/R}$ 서술 정확 | 일치 ✓ |
| 핸드오프 §2.4 | einstein 도입부 원문 "앞 절은 … 온도 편차는 미결로 남겼다" — §2.3 의 "그 문제만 세워 둔다"와 정확 맞물림 | 정합 ✓ |
| 핸드오프 §2.6 | limits keybox "예외는 … LCO 의 MIT" — §2.3 "(중심 흡수 근사의 예외 코너, §sec:limits)" 지시 정확 | 정합 ✓ |
| 핸드오프 §2.7 | revheat 제목·§ssec:revinterp "분포 재배열의 열" — §2.3 keybox "세 분포를 재배열하는 열" 정합 | 정합 ✓ |
| 교차 특성화(LCO) | §2.2 warnbox 의 "그 절의 $\Delta S_j^0$=config 슬롯 중심값 / 본 장=전체 중심값" ↔ lco-decomp:56–58 "★스코프 주의"(같은 경계를 거울로 명시) — 상호 정합 | 정합 ✓ |
| 명칭 규약(P3-7) | 두 파일 전체에서 Part 0/Part I/Part T/Chapter 2 사용 전건 정합(v1.0.21→22 diff 로 재편 확인) — ver.N 역사 명칭 혼입 없음 | 정합 ✓ |
| keybox 분해식 | $\Delta S(x)=\Delta S^0_j+R\ln[\xi/(1-\xi)]+\delta S_{\vib/e}(x)$ — warnbox 원식과 동일($n_j{=}1$ 서식, :49–50 의 일반형 주석이 절 전체를 커버) | 일치 ✓ |

---

## 4. 서치 절 (haiku 서브 위임 결과 — DOI 실검증분만)

서브에이전트(model: haiku)가 Crossref/출판사 랜딩에서 검증한 결과. **기억 서지 없음** — 전건 확인 경로 보고됨.

### 4.1 기존 인용 키의 주장 검증

| 키 | 질의 | 결과 | 판정 |
|---|---|---|---|
| msmr_partII (10.1149/1945-7111/ad70d9) | MCMB 저-SOC 엔트로피 계수 수치·단위(+3~4 mV/K?) | abstract 에 수치 없음(Figure 본문 소관). 웹 검색에 0.3 mV/K 급 언급 존재하나 원문 귀속 미확정 | **미결** — 본문 각주의 [미검증] 태그 유지가 타당(발견 없음) |
| msmr_partI (10.1149/1945-7111/ad1d27) | 활성화 vs 반응 엔트로피 구분 명시 여부 | abstract 축자 "The entropy coefficient of a battery cell is the property that governs the amount of reversible heat …" — 가역 발열↔평형 엔트로피 계수는 명시, 활성화 엔트로피 구분은 부재(전문 미접근) | A12-15 근거(반쪽 지지) |
| chemmater2015 (10.1021/acs.chemmater.5b00235) | LiC$_6$ −13.9 / LiC$_{12}$ −24.8 kJ/mol Li 수치·기준 | **확인**: −13.9±1.2 / −24.8±1 kJ/mol Li, per mol Li, 직접 열량계(스니펫 상 455 K), LiH+graphite 경로·준안정 stage 맥락(abstract 축자 확보) | 본문 인용 수치 정확 — A12-06 은 수치 정정이 아니라 환산 결과 보완 |

### 4.2 신규 후보 표 (A12-12 보강용 — **원장 미등재**: 인용하려면 V1 절차[검증→등재→인용] 필요)

| 후보 키(제안) | 확정 서지(Crossref) | DOI | 지지 범위 | 한계 |
|---|---|---|---|---|
| holzwarth1978 | N. A. W. Holzwarth, S. Rabii, L. A. Girifalco, "Theoretical study of lithium graphite. I. Band structure, density of states, and Fermi-surface properties," Phys. Rev. B **18**(10), 5190–5205 (1978) | 10.1103/PhysRevB.18.5190 | LiC$_6$ 밴드구조·DOS·Fermi 면 — "Fermi level … near a saddle point in the $\pi$ bands" 스니펫 확인 | 전문 미접근 — $g(E_F)$ 증가의 정량은 본문 필요 [추정] |
| dresselhaus1981 | M. S. Dresselhaus, G. Dresselhaus, "Intercalation Compounds of Graphite," Adv. Phys. **30**(2), 139–326 (1981); 재판 **51**(1), 1–186 (2002) | 10.1080/00018738100101367 (1981) / 10.1080/00018730110113644 (2002) | GIC 전자구조 표준 리뷰(tier B 용도) | 전문 미접근 — 내용 수준 미확인 |

(A12-12 의 제안 문안은 신규 인용 없이 성립하도록 작성했다 — 후보는 저자가 보강 인용을 원할 때의 검증 출발점.)

---

## 5. 등급별 정리

- **H: 0건** — 재계산·재유도에서 물리/논리 오류 미발견. (§2.2·§2.3 의 유도 사슬은 전건 통과 — 축 A·C.)
- **M: 9건** — 보완 5(A12-02 Ω 다리 · A12-03 발산↔유한 다리 · A12-04 문헌값 서술 정합 · A12-05 검증 성격 한정 · A12-06 환산 결과 제시), 설명 1(A12-07 BE 두 항 귀속), 수식화 1(A12-08 $\Delta S_\vib$ 항등식), 논리 2(A12-12 $\Delta S_e$ 과대 일반화 · A12-15 인용 하중 재배치)
- **L: 6건** — A12-01(부분몰 근거) · A12-09(제일원리 어의) · A12-10(몰 기준) · A12-11(포인터 앵커) · A12-13(사슬 괄호) · A12-14(시제)

## 6. 4-tier

- **확정**(재계산·문면 대조 완료): 축 A·B·C 전건; A12-02·03 의 수학(Ω 무기여·$g_jz_j\to0$); A12-05 의 계보 논거(tab:staging 캡션 문면); A12-06 의 $-3.0$ vs $-13.0$ 산술; A12-07·08 의 항등식; A12-14 의 diff 근거; chemmater2015 수치 일치(서브 abstract 계열 확인)
- **추정**(방향 타당·전문 미접근): A12-12 의 흑연 $g(E_F)$ 증가 방향(스니펫+표준 밴드구조 수준 — holzwarth1978 전문 필요); A12-15 의 "msmr_partI 전문에도 활성화 구분 없음"(abstract 수준 판단)
- **미검증**(원문 전문 필요): A12-04 의 Allart $x>0.5$ 프로파일 세부; msmr_partII 의 +3~4 mV/K 수치 귀속(본문 각주의 기존 [미검증] 유지); dresselhaus1981 내용 수준
- (제안 채택 여부는 전건 마스터/사용자 결정 사항 — 본 창은 보고 전용, 소스 무수정)

## 7. 무발견 축 (검토했으나 문제 없음)

1. **수식 재유도 축(§2.2 전건 + §2.3 전건)**: eq:Sconfig·eq:dSconfig·eq:dVdT_config·eq:Svib_mode·eq:Se_start·eq:Se-ch2 및 모든 산술(단위 환산 0.30 mV/K·ΔH −13.0·U(298) 4행·fig 좌표) — **오류 0건**
2. **라벨·참조 해소 축**: 내부 16종 + LCO 외부 3종 + Part 0 실물 3건 — 전건 해소, 깨진 참조 0건
3. **서지-원장 정합 축**: 7키 전건 V1 승계 확인·본문 한정문↔bib 비고 정합 — 위반 0건
4. **명칭 규약 축(P3-7)**: Part 0/I/T·Chapter 2 사용 전건 정합(ver.N 혼입 없음), §2.2 warnbox 의 두-기호 비등치 경계는 LCO 측 "스코프 주의"와 거울 정합 — 위반 0건
5. **§2.2 산문→수식화 축**: 실질 후보 없음 — 본 절은 이미 수식-구동이고 산문은 검산 gloss 역할(3분기 bullet 포함). §2.3 쪽 후보는 A12-08·A12-13 로 보고
6. **이중계산 경계 축(P3-2·파생 B)**: warnbox 삼분해↔§2.5 파생 B↔§2.6 keybox↔LCO 슬롯 규칙 — 4문서 교차 문면 충돌 0건
7. **제거 용이 블록 독립성**: v22 증축분(srcbox Reynier 다리)은 자기완결 박스로 본문 사슬 비의존 — 유지 시/제거 시 모두 본문 성립(문제 없음)
8. **부호 규약 축**: θ/ξ 구분·s=+1·탈리튬화 배향 — 두 파일 내 혼용 0건(§2.2 는 오히려 경계 문단 보유)

— 이상. FR-A12 검토 완료(발견 15건: H0·M9·L6 + 서치 3건 검증·2건 후보).
