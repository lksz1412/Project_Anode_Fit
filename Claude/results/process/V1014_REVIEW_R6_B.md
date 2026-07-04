# V1014 REVIEW R6 — 검수자 B (Fable) · 경계·코너 케이스 적대 검산

- 대상: `Claude/docs/v1.0.14/graphite_ica_ch1_v1.0.14.tex`(전문 L1–3251, 8분할 Read, 갭 0) · `graphite_ica_ch2_v1.0.14.tex`(전문 L1–793, 2분할 Read, 갭 0). ※두 파일 모두 R5 이후 P4.1 정정이 반영된 현행본 기준 줄번호(R1–R5 보고서의 구 줄번호와 다름).
- 렌즈: 문건이 주장하는 **모든 극한·경계·특수값·부등식·단정("정확히 0"/"연속"/"불변")·차원 환산** 서술의 전수 목록화 + 독립 재검산. 이전 라운드(R1~R5, 15개 보고서 전문 정독)가 이미 검산한 항목은 [기검산 R#] 표시만 하고 재보고하지 않음 — 미검산 잔여의 사냥이 임무.
- 방법: 손 재유도 + Python 독립 재계산(`scratchpad/r6b_verify.py` — SciPy `brentq` 포함, 세션 임시). 전 지적 refute 시도 후 생존분만 결함으로 기재. ★파일 수정 0건(본 보고서 1건만 신규).
- 판정: **CRIT 0 · HIGH 0 · MED 0 · LOW 2 · INFO(경계 관찰) 2**. 전수 목록의 FAIL 0.

---

## 1. 극한·경계·특수값 주장 전수 목록 (판정 표)

> 형식: [위치 | 주장 | 재검산 방법 | 판정]. "기검산"은 R1~R5 보고서가 동일 내용을 이미 독립 검산했음을 뜻하며 근거 라운드를 병기한다. 신규 검산 상세는 §2.

### 1.1 Ch1 Part 0 (L311–885)

| # | 위치 | 주장 | 재검산 방법 | 판정 |
|---|---|---|---|---|
| P1 | L352–353 | 입자 교환 시 $dS_\mathrm{tot}\ge0$ → 입자는 높은 $\mu$→낮은 $\mu$; 정지 조건 $\mu_1=\mu_2$ | 부호 대수 재유도(1계 전개) | PASS [기검산 R5-B] |
| P2 | L394–395 | $\beta\to0$: 등확률 / $\beta\to\infty$: $E_i-\mu N_i$ 최소 상태만 | Gibbs 인자 극한 | PASS [기검산 R2-A] |
| P3 | L481–484 | eq:fermifn $T\to0$: 계단; 고전 $k_BT\ln q\to0$→$\varepsilon_0$, 양자 $\varepsilon_0+\tfrac32\hbar\omega_0$ | 극한 재유도 | PASS [기검산 R2-A·R2-C] |
| P4 | L485–488 | $T\to\infty$: $q\equiv1$ 기준 $\theta\to\tfrac12$, 실제 조화 우물 $\theta\to1$ | $\beta\Delta\mu\to-\ln q$ 추적 | PASS [기검산 R2-A D1 정정분 — R5-B 이식 확인] |
| P5 | L487–488 | $\mu\to\pm\infty$: $\theta\to1/0$; $q\to1$: $\tilde\varepsilon\to\varepsilon_0$ | 지수 극한 | PASS [기검산 R2-A] |
| P6 | L494–500 | $n^2=n$ → var$(n)=\theta(1-\theta)=\partial\theta/\partial(\beta\mu)$ | 미분 재유도 | PASS [기검산 R2-A] |
| P7 | L518–522 | 영점 인자 $e^{-\beta\hbar\omega/2}$ 의 $T\ln q$ 기여 = 온도 무관 상수 $-\hbar\omega/(2k_B)$ → 엔트로피 동일 | 항등식 재유도 | PASS [기검산 R1-A #1 정정분·R2-C] |
| P8 | L567–569 | $\theta\to0$: $\mu\to-\infty$ / $\theta\to1$: $+\infty$ / $\theta=\tfrac12$: $\mu=\mu^0$·$S_\mathrm{mix}$ 최대 $k_B\ln2$ | 로그 극한 | PASS [기검산 R2-A] |
| P9 | L592–593 | $u<0$(인력) ⟺ $\Omega>0$(상분리 경향) | 정의 대입 | PASS [기검산 R2-A] |
| P10 | L620–628 | $g''\ge0\ \forall\xi \Leftrightarrow \Omega\le2RT$; **등호는 $\Omega=2RT,\ \xi=\tfrac12$ 한 점** | §2-[K] 수치 스캔: $g''$ 최솟값 0 은 $\xi=0.5$ 유일 | PASS (등호-한-점은 신규 확인) |
| P11 | L631–633 | $\Omega\to0$: $g''\ge4RT>0$ 한 웰 / $\Omega\to2RT^-$: 바닥 평탄·한 웰 / $\Omega\to2RT^+$: 이중웰, $T_c=\Omega/2R$ 아래서만 상분리 | 극한 대입($T<T_c\Leftrightarrow\Omega>2RT$ 자기일관) | PASS [기검산 R2-A] |
| P12 | fig:sm-gxi (L643–667) | spinodal $\xi_s^\pm=0.2113/0.7887$·$f/RT=-0.0157$·$\xi{=}\tfrac12$ 5값 | — | PASS [기검산 R1-A·R2-A·R4-B 전좌표] |
| P13 | fig:sm-mu (L679–697) | $\Omega=4RT$: $\theta_s^\pm=0.146/0.854$, 값 $\pm1.066$; §hys 거울 대응 | — | PASS [기검산 R2-A·R4-B] |
| P14 | L780–783 | $V=U\Rightarrow\theta_\eq=\xi_\eq=\tfrac12$; $T\to0$ 계단($w\to0$); $w\propto T$ | 대입 | PASS [기검산 R1-A signbox] |
| P15 | fig:sm-occ (L834–838) | $w=23.1/25.7/28.3$ mV @268/298/328 K; (a) $\varepsilon=\mu$ 에서 $\tfrac12$ | — | PASS [기검산 R2-A·R5-B] |
| P16 | L874–876 | Nernst: $\xi=\tfrac12\Rightarrow V=U_j$; $T\uparrow$ 기울기 $\propto T$; $\Delta S>0$→중심 상승 | $\partial U/\partial T=\Delta S/F$ | PASS [기검산 R2-A] |
| P17 | L756–758·L1338–1340 | 자리당$(k_BT,e)$↔몰당$(RT,F)$ 환산 — 지수비 불변; $\beta F=N_A/w$ | 차원 사슬 | PASS [기검산 R2-A ⑧] |

### 1.2 Ch1 N1–N3 (L887–1173)

| # | 위치 | 주장 | 재검산 방법 | 판정 |
|---|---|---|---|---|
| N1 | L913–915 | 방전 $V_n<V_\app$·충전 $V_n>V_\app$; $|I|\to0$ 또는 $R_n=0$ ⇒ $V_n=V_\app$ | 대입 | PASS [기검산 R1-A] |
| N2 | L927–928 | 스팬 하한 $10^{-6}$ V·$n_\work=\max(2048,2\,\mathrm{len})$ | 코드 기본값 대조 | PASS [기검산 R4-C tab:inputs] |
| N3 | L995–999 | $\Delta H<0$→중심 상승; $|\Delta S|\sim$수십 J/(mol K)→30 K 창 수 mV | $-0.166$ mV/K×30 | PASS [기검산 R1-A·S1] |
| N4 | L1006–1007 | $U(298)=(13000-298.15{\times}16)/96485\approx0.0853$ V | — | PASS [기검산 R1-A·R2-C] |
| N5 | L1036–1041 | $u_j$ 실수 조건 $\Omega>2RT$; $\Omega\le2RT$ 면 gap **정확히 0** | — | PASS [기검산 R2-C S4·R2] |
| N6 | L1109–1115 | $\Delta U^\hys\ge0$; $\Omega\to2RT^+$ Taylor(동시 전개) $\to\tfrac{8RT}{3F}u^3\to0$ 연속; 소박 대입 함정 $-\tfrac{4RT}{3F}u^3$; $u^3\propto(T_c-T)^{3/2}$ | — | PASS [기검산 R1-A #2·R2-C] |
| N7 | L1118–1123 | 두 spinodal 끝점 평균 $=U_j$ (분기 $U_j$ 대칭) | — | PASS [기검산 R1-A·R2-C] |
| N8 | L1130–1132 | $U^{\dis}>U^{\chg}$; $\gamma=1$ spinodal 상한·$\gamma\to0$ 히스 소멸 | — | PASS [기검산 S4·R3행] |
| N9 | fig:hysloop (L1154–1171) | $\pm1.0657$ 좌표; $\gamma\to0$: $y=0$ plateau 합류 | — | PASS [기검산 R1-A·R4-B·R5-B] |

### 1.3 Ch1 N4–N6·broadening (L1176–1688)

| # | 위치 | 주장 | 재검산 방법 | 판정 |
|---|---|---|---|---|
| W1 | L1184–1185 | 중심 기울기 $\dd\xi_\eq/\dd V|_{1/2}=sF/(4RT)$ | §2-[A]: $9.7304$ V$^{-1}$ 재계산 | PASS (신규 확인) |
| W2 | **L1197–1199** | **$0<\Omega<2RT$ 에서 유효 폭이 $(1-\Omega/2RT)$ 배로 좁아짐**(P4.1 신설 — O2-G 복원 문안) | §2-[A]: $\dd V/\dd\xi|_{1/2}=(4RT-2\Omega)/F$ → $w_\eff/w=1-\Omega/2RT$, 2점 수치 일치; $\Omega\to2RT^-$ 에서 $w_\eff\to0$ 로 두-상 델타와 연속 접속 | **PASS (신규 — 유일한 미검산 신설 물리식)** |
| W3 | L1203–1204 | 네 전이 초기 $\Omega$ 전부 $>2RT\approx4958$ J/mol@298 K | $2RT=4957.9$ | PASS [기검산 R2-C] |
| W4 | L1210–1211 | 폭 폴백 0.020/0.016/0.014/0.012 V — $n_j$ 입력 배제 시만 활성, 현 출발 $n_j{=}1$ | 역산 $n=0.778/0.623/0.545/0.467$ | PASS [기검산 R1-A #8 정정분; §2-[J] $n$ 재계산] |
| W5 | L1224–1230 | $\chi+(1-\chi)=1$ ⇒ 평형비 $\chi$-무관(detailed balance) | — | PASS [기검산 R2-A·R1-B] |
| W6 | fig:flux (L1313–1315) | $r^+=2r^-$⇒$\xi_\eq=2/3$; $\mathcal A=0$⇒$\tfrac12$ | — | PASS [기검산 R1-A·R5-B] |
| W7 | L1319–1323 | $V\gg U$⇒$\xi_\eq\to1$·$V\ll U$⇒0·$V=U$⇒$\tfrac12$; $w=25.7$ mV@25$^\circ$C | — | PASS [기검산; §2-[J] RT/F=25.69] |
| W8 | L1338–1343 | $\Delta\mu=+sF(V-U_j)$·여집합 관계 부호 일치 | — | PASS [기검산 R2-A ⑧] |
| W9 | L1349–1351 | $\Omega=0$: 정확히 Fermi-함수형 / $\Omega>0$: $\Delta\mu$ 에 $-\Omega(1-2\xi)$ | $\theta\to\xi$ 부호 반전 | PASS [기검산 R2-A·R1-A] |
| W10 | eq:belliden·fig:logistic | $\xi(1-\xi)$ 최대 $\tfrac14$@$\xi{=}\tfrac12$; 스케일 3배→0.75 | — | PASS [기검산 R4-B] |
| W11 | L1415–1417 | $|I|\to0$ 극한: $\gamma_j\ne0$ 이면 $U_j^{\,d}$ 잔존 극한, $\gamma_j\to0$ 에서만 가역 기준선과 일치 | — | PASS [기검산 R1-A #3 정정분] |
| W12 | L1417–1420 | peak 모양 $\ge0$·방향 불변; 순높이 $Q_j/(4w)$; 면적 $Q_j$($\int_0^1\dd\xi=1$) | — | PASS [기검산 S3·R1-B] |
| W13 | L1442–1443 | Maxwell 공통접선 → plateau 한 전위 → $\dd q/\dd V\to\infty$(델타) | 정성 극한 | PASS [기검산 R1-A (a)항] |
| W14 | L1456–1457·L1461 | ① $|I|\to0$ 소멸($L_V\propto|I|$) / ② 평형 잔여 폭은 $|I|\to0$ 에도 잔존 | — | PASS [기검산 R2-B #23] |
| W15 | L1462–1466 | $RT/F\approx26$ mV 는 하한 아님; $n_j<1$ 이면 잔여 폭 축소; 현 출발 $n_j{=}1$→25.7 mV | — | PASS [기검산 R2-B #28] |
| W16 | L1506–1507 | $\rho\to\delta(U_\app-U_j)$ ⇒ 단일 델타 환원(③ 소멸) | — | PASS [기검산 R1-A·R2-B] |
| W17 | L1513–1516 | 합성곱 분산 가법 = 모양 무관 항등식; ① 단측 지수도 총분산에 $L_V^2$ 가법 | — | PASS [기검산 R2-B #15/F2 정정분] |
| W18 | L1525–1527 | logistic 분산 $\pi^2w^2/3$; FWHM $=2\ln(3+2\sqrt2)w\approx3.53w$ ($n{=}1$,298 K ≈91 mV) | §2-[J] 상수 3.5255 재계산 | PASS [기검산 R2-B #12·13] |
| W19 | L1528–1533 | $\sigma_\mathrm{int}\equiv\pi n_jRT/(\sqrt3 F)$; $\sigma=\pi w/\sqrt3$; $\sigma_\mathrm{sym}/\sigma_\mathrm{int}=\sqrt{1+(\sigma_\eta/\sigma_\mathrm{int})^2}$ | — | PASS [기검산 R3-A A3 정정분·R5-A ⑦] |
| W20 | fig:widthbudget (L1550–1566) | $\sigma_\eta=1.25\sigma_\mathrm{int}$→유효 scale 1.6; ① 곡선 = 실제 수치 합성곱 | — | PASS [기검산 R4-B §3] |
| W21 | eq:gibbsthomson 사슬 (L1583–1620) | 차원 V; $V_m$ 31.9→36 cm³/mol; $\Delta U(1\mu m)\le0.75$ mV; $\delta U_\mathrm{PSD}\approx0.20$ mV; $<1\%$; $3\%$ 못 넘음; $\gamma{=}5$→$\approx1.0$ mV; $\tau=6{\times}10^2$–$2.5{\times}10^4$ s; 30 nm→$\approx25$ mV·$\gamma{\sim}0.1$ 십분의 일 | §2-[J] $\gamma{=}5$: 0.99 mV = 3.85% 재확인 | PASS [기검산 R2-B 전항·R5-B 정정 후 값] |
| W22 | L1614–1616 | 반경 의존 커널 소거 → PSD 적분 항등 → 비-크기 $\eta$ 만 잔존 | — | PASS [기검산 R2-B F5 정정분] |

### 1.4 Ch1 N7–N8 (L1691–1946)

| # | 위치 | 주장 | 재검산 방법 | 판정 |
|---|---|---|---|---|
| K1 | **L1719** | 역방향 몫 $(1+e^{-\mathcal A/RT})$ — "$\mathcal A\gtrsim3RT$ 면 1로 수렴" | §2-[D]: 3RT 에서 1.0498(편차 4.98%), 4RT 1.018, 4.357RT 1.013 | **PASS (신규)** — 문턱 3RT 의 잔차 ≈5% 는 문건 자신의 5% 컷 관례와 동급, "수렴" 서술 성립 |
| K2 | L1725–1727 | 종 5% 지점 $z_\mathrm{cut}=4.357$; 컷 구동력 $\mathcal A=z_\mathrm{cut}n_jRT$ | §2-[J]: $\sigma(1-\sigma)/\tfrac14=0.05$ 근 $z=4.3565$ | PASS [기검산 R1-B·R2-C R4] |
| K3 | **L1733–1735** | (P4.1 신설) $n_j{=}1$ 기본에서 $\min$ 은 상한: 실효 컷 $z=4.0$(정점의 **약 7%**); 5% 분기 활성 조건 $n_j<A_\mathrm{cap}/z_\mathrm{cut}\approx0.92$ | §2-[C]: $z{=}4.0$→7.07%; $4.0/4.357=0.9181$ | **PASS (신규 — R5-B B5-1 정정 문안의 수치 일치 확인)** |
| K4 | L1753–1756 | 방전 $\xi\to1$: $-\Omega(1-2\xi)\to+\Omega$ / 충전 $\xi\to0$: $+\Omega(1-2\xi)\to+\Omega$ — 양방향 동일 $+\Omega$ | — | PASS [기검산 R1-B] |
| K5 | L1787–1792 | 실현 미분 $\partial\ln L_q/\partial V=0$(컷 동결); 부등식 $<0$ 은 방전 기준 동기 | — | PASS [기검산 R1-B B-04 정정분·R2-C F-3·S6] |
| K6 | L1792–1793 | $L_q\propto|I|$($T_*\propto|I|$) ⇒ $|I|\to0$: $L_V\to0$ → 평형 peak 환원 | — | PASS [기검산 R2-B #23·R3행] |
| K7 | L1793–1795 | $L_V=0$ 침묵 3채널($I\le0$·$\Delta H_a$ 무·$|\dd V/\dd q|_{q_a}=0$ 기본) | 코드 `_resolve_lag_length` 경로 | PASS [기검산 R5-B B5-3 정정분] |
| K8 | L1832–1833 | 초기값 $\xi_{\mathrm{lag},0}=\xi_{\eq,0}$ ⇔ $r(q_0)=0$ 첫 항 소거; $L_V\le0$/비유한→항등 | — | PASS [기검산 R1-B] |
| K9 | L1872–1878 | $L_V\gg\Delta$: $\rho\to1$ 매끈한 미분(단 평형 종 환원엔 $L_V\ll w$ 별도 필요) / $L_V\to0$: $\rho\to0$, $0/0$ — 식으로는 환원 안 됨, 분기 스위치 소관 | — | PASS [기검산 R1-B·R2-C R5] |
| K10 | L1887–1894 | 점프 닫힌꼴 $1-(1/\nu)/(e^{1/\nu}-1)$; $\nu{=}2$: ~23%(면적 0.77); $\approx50\%/\nu$; $\nu{=}8$: 6.1%·$\nu{=}10$: 4.9%; **$\nu\gtrsim10$ 필요** | §2-[J]: $\nu{=}9$→5.45%·$\nu{=}10$→4.92% — "$\gtrsim10$" 경계 정확 | PASS [기검산 R1-B·R5-C; $\nu{=}9$ 경계는 신규 확인] |
| K11 | L1893–1894 각주 | 문턱 통과 시 "모델 곡선의 해당 전이 기여 ~23% 점프" | — | PASS [기검산 R5-B B5-4 정정분] |
| K12 | L1909–1912 | 충전 역전: peak 양수 유지; 꼬리 = 진행상 나중 전위 쪽(방전 高$V$/충전 低$V$) | — | PASS [기검산 R1-B B-08 정정분·S7] |

### 1.5 Ch1 N9·표 (L1948–2004)

| # | 위치 | 주장 | 재검산 방법 | 판정 |
|---|---|---|---|---|
| T1 | L1992–1993 | $U(298)$ round-trip ±1 mV(4→3 만 0.2109 자리수 경계) | — | PASS [기검산 R1-B·R5-B] |
| T2 | **L1974–1976** | $3\to2\mathrm L$ 0.140 V vs Ohzuku $\approx0.125$ V — "**15 mV** 시료 의존 편차 **안**"(통상 5–15 mV) | §2-[J]: 편차 정확히 15.0 mV = 선언 범위의 상단 **끝점** | PASS-경계 (INFO-2 — §3) |
| T3 | **L1998–2003** | (P4.1 신설) 초기 $L_V=10^{-10}$–$10^{-8}$ V ≪ 문턱 $\nu\Delta\sim10^{-4}$ V → 초기 곡선 = 평형 종 전용; 가시적 꼬리 $\Delta H_a\gtrsim7$–$8{\times}10^4$ J/mol | §2-[H] **완전 독립 재유도**: 4전이 $L_V=4.91{\times}10^{-8}/1.46{\times}10^{-8}/4.36{\times}10^{-9}/4.75{\times}10^{-10}$ V; 문턱 도달 $\Delta H_a=73.1$ kJ/mol·가시(10 mV) $81.8$ kJ/mol | **PASS (신규 — R5-B B5-2 정정 문안의 수치를 코드 없이 식만으로 재현)** |
| T4 | L1992 | $w$ 폴백 + $n{=}1$·$\Delta S_a{=}0$ 병행 | — | PASS [기검산 R4-C tab:staging 전건] |

### 1.6 Ch1 Part II (L2012–2930)

| # | 위치 | 주장 | 재검산 방법 | 판정 |
|---|---|---|---|---|
| L1 | L2102–2103 | 흑연 0.08→0.21 V·LCO 3.9→4.2 V — 탈리튬화에서 전위 상승(규약의 전극-중립 근거) | 표 단조성 | PASS [기검산 R1-B·R5-B] |
| L2 | eq:lco-dUdT (L2206–2231) | 이중 경로(직접/Gibbs 항등식) 일치; host 항 부재 | — | PASS [기검산 R1-B] |
| L3 | verifybox (L2252–2270) | $F{\times}0.83$ mV/K$\approx+80$; 30 K→$+25$ mV; 골 $-46$; $+80-46\approx+34>0$; 게이트 적분 $\approx1.1\,k_B$/atom | §2-[J] 80.08/24.9/45.96/34 재계산 | PASS [기검산 R1-B·R5-B] |
| L4 | L2318–2319 | $\Omega^\mathrm{cat}<2RT$: $u$ 허수 / 등호: $u=0$ / gap 0 연속 | — | PASS [기검산 R2행 동형] |
| L5 | L2335–2338 | LCO 대칭점 검산(평균 $=U^\mathrm{cat}$, host-무관) | — | PASS [기검산 R1-B] |
| L6 | eq:lco-dope (L2419–2426) | $\Omega^\mathrm{dop}\to2RT^+$: $u\to0$, gap $\to\tfrac{8RT}{3F}u^3\to0$; $T_c=\Omega/2R$ | — | PASS [기검산 R1-B·R2-C] |
| L7 | **L2712–2714** | "order–disorder 의 큰 $\Omega^\mathrm{cat}$ 는 … **분기 gap 도 흑연보다 키운다**" — gap 의 $\Omega$-단조 증가 암묵 주장 | §2-[B] **신규 해석 유도**: $\dd(\Delta U^\hys)/\dd\Omega=2u/F>0$ (수치 4점에서 해석식과 소수 6자리 일치) | **PASS (신규 — 단조성이 처음으로 명시 검산됨)** |
| L8 | L2447–2450 | $x{=}1$ 절연체 $g(E_F)\approx0$ → $x<0.94$ 금속 | 물리 서술 | PASS(물리); 단 게이트 모델의 $x{=}1$ 잔차는 §3 LOW-1 |
| L9 | L2487–2488 | $s(\zeta)\ge0,g\ge0$⇒$S_e\ge0$; $T\to0$ 또는 $g\to0$⇒$S_e\to0$ | 부호 대수 | PASS (신규-자명) |
| L10 | **L2489–2493** | Sommerfeld 동결 보정(Mott 항) $\mathcal O[(k_BT/E_F)^2]$; $k_BT/E_F\sim0.03$@300 K → 무시 | §2-[G]: $k_BT$=0.0259 eV, 비 0.026, 제곱 $6.7{\times}10^{-4}$ | **PASS (신규)** |
| L11 | eq:dSegate (L2584–2593) | 전인자 음성 고정; $\sigma(1-\sigma)$ 최대 $\tfrac14$@$x_\mathrm{MIT}$; 양쪽 지수 감쇠 | — | PASS [기검산 R1-B·R4-B 곡선 전좌표] |
| L12 | **L2600–2603** | $x_\mathrm{MIT}\approx0.85$ = 2상역(0.75–0.94) **중앙**; $\Delta x\approx0.05$ — $\pm2\Delta x$ 유효폭 $\approx0.2$ ↔ 창 0.19 | §2-[E]: 중앙 0.845; $4\Delta x=0.2$ vs 0.19 | **PASS (신규-산술)** |
| L13 | L2613–2615 | $S_e/k_B=3.29{\times}0.0259{\times}13\approx1.1$@300 K = 게이트 적분 방출과 항등 | §2-[J]: 1.1056 | PASS [기검산 R1-B·R5-B] |
| L14 | L2625–2629 | 골 깊이 $-\tfrac{\pi^2}{3}R(k_BT/e_V)(g_{\max}/\Delta x)\tfrac14\approx-46$ J/(mol K); 증폭 $1/\Delta x\approx20$ | §2-[J]: $-45.96$; $1/0.05=20$ | PASS [기검산 R1-B] |
| L15 | L2529–2534 | $e_V$ 를 곱하면 $1/e_V^2\approx4{\times}10^{37}$ 배 어긋남; 부호는 환산 불변($N_A,e_V>0$) | §2-[J]: $3.896{\times}10^{37}$ | PASS [기검산 R1-B] |
| L16 | L2544–2548·eq:U1T2 | $\Delta S_e\propto T$→$\partial U/\partial T|_e\propto T$·$U$-이동 $\propto T^2$($\tfrac12$ 인자); $a_e<0$→고온 외삽이 선형보다 낮음 | 적분 재유도 | PASS [기검산 R1-B eq:U1T2] |
| L17 | eq:lco-xmap (L2879–2883) | $\xi{=}0\leftrightarrow x_\mathrm{hi}$·$\xi{=}1\leftrightarrow x_\mathrm{lo}$; $x_\mathrm{MIT}$ 창 내부 | §2-[J]: $\xi(0.85)=0.4737\in(0,1)$ | PASS [기검산 R5-B 0.474] |
| L18 | L2895–2897 | $N_A$ 누락 시 전자항 $\sim10^{23}$ 배 과소 | $N_A=6.022{\times}10^{23}$ | PASS (자명) |
| L19 | L2906–2915 | 동결 근사 → 선형 $U(T)$; 되먹임 상한 $0.47$ mV/K${\times}30$ K$\approx14$ mV $\lesssim w_1$ | §2-[J]: 14.3 mV vs 25.7 mV | PASS [기검산 R1-B·R5-B] |
| L20 | eq:lco-msmrmap·L2853–2858 | $f=+\sigma_d$ 유일해(pairing 하); 직접 등치 시 $f=-\sigma_d$; $\theta(1-\theta)=\xi(1-\xi)$ 여집합 불변; $|f|=1$ | — | PASS [기검산 R1-B] |
| L21 | L2385–2388 | Motohashi anchor $x{=}\tfrac12,\tfrac23$ 모두 T2/T3 창(0.55/0.48) 밖 — 배정 양쪽 tier C | §2-[L] 거리 재계산 | PASS [기검산 R1-B B-03 정정분] |
| L22 | eq:lco-configsplit (L2752–2758) | $[R\ln\tfrac{\xi}{1-\xi}]_{\xi=1/2}=0$ | $\ln1=0$ | PASS (자명) |

### 1.7 Ch1 부호검산표·부록 (L2994–3214)

| # | 위치 | 주장 | 판정 |
|---|---|---|---|
| S1–S8 | tab:signcheck-S | 정성 부호 8행 | PASS [기검산 R2-C 전행·R4-A] |
| R1–R6 | tab:signcheck-R | $u{=}0.766$·86.7 mV·$2RT{=}4958$·$|I|\to0$·컷 동결·$0/0$·$+80$/$+25$ mV | PASS [기검산 R2-C·R4-A/B 재계산] |
| C1 | codebox N2 (L3205–3207) | $U(298)\approx0.0853$ V | PASS [기검산] |

### 1.8 Ch2 전수 (L1–793)

| # | 위치 | 주장 | 재검산 방법 | 판정 |
|---|---|---|---|---|
| C2-1 | L85·eq:qrev | $\dot Q_\rev=-IT\,\partial U_\oc/\partial T=-(IT/F)\Delta S$; $\dot Q_\irr\ge0$ | — | PASS [기검산 R5-C 4-사분면·F-3 정정분 반영 확인(L692–695 두 전제 명시)] |
| C2-2 | eq:occ·eq:logistic | FD 동형; $w=RT/F$; $\beta F=N_A/w$ | — | PASS [기검산 R2-A ⑧·R1-C] |
| C2-3 | keybox L175–185 | 단상 폭 = 평형 예측(이상 극한 eq:Z1 의 $RT/F$, 상호작용 시 $\Omega$ 가 바꾸되 평형이 결정) | — | PASS [기검산 R5-C F-7 정정분 반영 확인] |
| C2-4 | eq:Veq_BW·eq:slope_BW (L210–224) | $\dd V_\eq/\dd\theta|_{1/2}=(2\Omega-4RT)/F$; 임계 $\Omega=2RT$(등호 중심 기울기 0); $\Omega>2RT$ 중앙 기울기 양(불안정) | 재미분 | PASS [기검산 R5-C·H-1 정정 계보] |
| C2-5 | eq:dSconfig·L268–277 | $\partial S_\config/\partial\theta=-R\ln[\theta/(1-\theta)]$; $\xi\to1$: $+\infty$ / $\xi\to0$: $-\infty$ / $\xi=\tfrac12$: 0 | 로그 극한 | PASS [기검산 R5-C·tab:limits R4-B] |
| C2-6 | eq:dVdT_config (L252–262) | 둘째 항 부호 $+$ 맞물림($\theta=1-\xi$); 계수 $R/F$($n_j$ 일반형 $n_jR/F$) | — | PASS [기검산 R5-C 부호 맞물림] |
| C2-7 | fig:occ_config | $S$ 최대 $\ln2$@$\tfrac12$; 축 $(\mu-\varepsilon_0)/k_BT$ | — | PASS [기검산 R1-C C-4 정정분 확인] |
| C2-8 | L338–339 각주 | $+29$ J/(mol K) ⇒ $+0.30$ mV/K — 문헌 $+3$–4 mV/K 와 자릿수 상이[미검증 플래그 유지] | §2-[J]: 0.301 mV/K | PASS (신규-산술; 원문 재확인 대상 표기는 문건 자신이 유지) |
| C2-9 | tab:ds·L342–344 | $+29$@$x{=}0.08$ 창 끝 — config 겹침이라 "구간 대표값 수준" 한정 | — | PASS [기검산 R5-C F-2 정정분 반영 확인] |
| C2-10 | L369–374 | 형성(누적) vs 전이별 기준 구분; $\Delta H^0=-FU+FT\partial U/\partial T$: stage 2→1 $-13.0$ kJ/mol 표값 일치 | §2-[J]: $-12.97$ | PASS [기검산 R1-C] |
| C2-11 | eq:Svib_mode | 보손 닫힌형 | — | PASS [기검산 R2-A ⑤] |
| C2-12 | eq:Se·L419–421 | Sommerfeld $T$-선형; $g$[1/에너지]→$k_B^2Tg$ 알짜 차원 $k_B$; 몰당 $N_Ak_B=R$ | 차원 사슬 | PASS [기검산 R1-B·R5-C] |
| C2-13 | eq:gj·eq:dxidT·eq:weighted | $\partial\xi/\partial T|_U=-g_j\partial U_j/\partial T-g_j(n_jR/F)z_j$; 가중 분모 $\sum Q_jg_j=Q\,\partial\bar x/\partial U$ = 측정 $dQ/dV$ | 재미분(본 라운드 재확인) | PASS [기검산 R1-C·R5-C] |
| C2-14 | srcbox (L510–522) | 175점 표시 정밀도 일치; 단순식 오차 최대 0.18(해석 상한 0.21); config 항 $[-0.21,+0.14]$ mV/K — 스팬 의존 | §2-[I] $R/F{\times}z$ 재계산 | PASS [기검산 R5-C config 스케일] |
| C2-15 | **L529–530** | "실측 $w_j$ 가 $T$-동결이면 단순식/완전식 우열이 뒤집히는 **~0.3 mV/K 급** 차이" | §2-[I]: 검증 그리드 실측 범위는 $[-0.21,+0.14]$ (peak-to-peak **0.35**); $(R/F)z$ 는 $z{=}3.5$ 에서 0.302·컷 $z{=}4.357$ 에서 0.375 | **PASS-주의 (LOW-2, ★가장 약한 1곳 — §3)** |
| C2-16 | eq:hys_branch·eq:hys_rev (L607–629) | 분기 평균 상쇄는 $g^{(\mathrm{ch})}=g^{(\mathrm{dis})}$ 선형화($\Delta U^\hys\ll w$)에서 정확 — 1차까지, 유한 gap 고차 보정(대칭 이동 $\pm\tfrac12\delta$ 평균 = $f(U)+\mathcal O(\delta^2)$) | 대칭 전개 재확인 | PASS [기검산 R5-C·M-8 정정 계보] |
| C2-17 | L628–629 | 히스 소산 사이클당 $\propto Q_\mathrm{cycle}\Delta U^\hys$ (차원 C·V=J) | — | PASS [기검산 R5-C] |
| C2-18 | tab:limits (L643–660) | 6코너: $\xi\to1$/$\xi\to0$/$\xi{=}\tfrac12$/$\Omega\to2RT$/단일 봉우리/고온($k_BT\sim E_F$ 정량 부적용) + L662 "다섯 환원·여섯째 한계" | — | PASS [기검산 R4-B·R5-C F-6 정정분 반영 확인] |
| C2-19 | L692–699 | Bernardi 두 전제(혼합열·상변화) 명시; 라벨 층위(셀 방전=리튬화, $I$ 부호로 읽음, 식은 방향 선형) | — | PASS [기검산 R5-C F-3 정정분 반영 확인] |
| C2-20 | L707–713 | 방전 $\Delta S>0$→흡열/$\Delta S<0$→발열; stage 2→1 큰 음 $\Delta S$→$\dot Q_\rev>0$ | — | PASS [기검산 R5-C 4-사분면] |
| C2-21 | use-this·procedurebox | 종합식 환원(단일 전이→eq:single_config); $\Delta S^0_j=F\dd U_j/\dd T$ | — | PASS [기검산 R5-C] |
| C2-22 | fig:blend 캡션 | 모식(부호·순서 임의) 선언; 실제 프로파일 $-16\to-5\to0\to+29$ 상승 | 표 순서 대조 | PASS [기검산 R4-B §5] |

**전수 판정: FAIL 0.** 극한·경계·특수값·부등식·차원 환산 주장 가운데 수학·물리적으로 반증되는 항목은 없다.

---

## 2. 신규(미검산 잔여) 독립 재검산 상세 — `r6b_verify.py` 출력 근거

| ID | 대상 | 재검산 결과 |
|---|---|---|
| [A] | W1·W2 유효 폭 좁힘 | $\dd V/\dd\xi|_{1/2}=(4RT-2\Omega)/F$ 재미분 → $w_\eff/w$ 가 $\Omega/2RT=0.5/0.9$ 에서 정확히 $0.5000/0.1000=(1-\Omega/2RT)$. 이상 중심 기울기 $sF/4RT=9.7304$ V$^{-1}$. $\Omega\to2RT^-$ 에서 $w_\eff\to0$ — 두-상 "평형 델타" 서술과 연속 접속. Ch2 파생 C·keybox 문안("$\Omega$ 가 중심 기울기를 비틀어 폭을 바꾼다")과 정합 |
| [B] | L7 gap 단조성 | 해석 유도: $u^2=1-2RT/\Omega$, $\mathrm{artanh}'u=\Omega/2RT$ ⇒ $\dd[\Omega u-2RT\,\mathrm{artanh}u]/\dd\Omega=u$ ⇒ $\dd(\Delta U^\hys)/\dd\Omega=2u/F>0$. 수치 4점($\Omega=6000$–20000)에서 중앙차분과 소수 6자리 일치. "큰 $\Omega$ → 큰 gap" 성립 |
| [C] | K3 실효 컷 | $z{=}4.0$: $\sigma(1-\sigma)/\tfrac14=7.07\%$("약 7%" ✓); $z{=}4.357$: 4.998%("5% 컷" ✓); $A_\mathrm{cap}/z_\mathrm{cut}=0.9181$("≈0.92" ✓) |
| [D] | K1 역방향 몫 | $A/RT=2/3/4/4.357$ → 인자 1.1353/1.0498/1.0183/1.0128. 문턱 3RT 잔차 4.98% |
| [E] | L12 게이트 파라미터 | $(0.75+0.94)/2=0.845\approx0.85$ ✓; $\pm2\Delta x=0.2$ vs 창 0.19 ✓ |
| [F] | 게이트 $x{=}1$ 잔차 | $z=3.0$, $1-\sigma=0.0474$ → $g(x{=}1)=0.617$ e/eV/atom = $g_{\max}$ 의 4.7%. 그림 좌표 $0.123/2.6=0.0473$ — **좌표는 식 그대로 정확**, "$g\to0$" 주석만 근사(§3 LOW-1) |
| [G] | L10 Mott 비 | $k_BT@300$ K$=0.0259$ eV; $E_F\sim1$ eV 기준 비 0.026("~0.03" ✓); 제곱 $6.7\times10^{-4}$ — 무시 정당 |
| [H] | T3 초기 $L_V$ | eq:Acut→eq:dHeff→eq:Lqfull→eq:LV 를 식만으로 재구성(코드 미참조): $L_V=4.91{\times}10^{-8}/1.46{\times}10^{-8}/4.36{\times}10^{-9}/4.75{\times}10^{-10}$ V (4전이, 298.15 K·C/10·$\chi{=}0.5$) — 본문 "$10^{-10}$–$10^{-8}$ V 규모" ✓, R5-B 코드 실행값과 독립 일치. 문턱 $L_V=3{\times}10^{-4}$ V 도달 $\Delta H_a=73.1$ kJ/mol·가시(10 mV) 81.8 kJ/mol — 본문 "$\gtrsim7$–$8\times10^4$ J/mol" ✓ |
| [I] | C2-15 "~0.3 mV/K" | config 항 $(R/F)z$: $z{=}1.6$→0.138 / $z{=}2.4$→0.207 / $z{=}3.5$→0.302 / 컷 $z{=}4.357$→0.375 mV/K; 검증 그리드 서명 범위 $[-0.21,+0.14]$ 의 peak-to-peak $=0.35$ mV/K |
| [J] | 산술 일괄 | §1 표에 병기(0.30 mV/K·1.1056 $k_B$·$-45.96$·$-12.97$ kJ/mol·14.3 mV·$3.896{\times}10^{37}$·$\nu{=}9/10$ 점프 5.45/4.92%·$z_\mathrm{cut}$ 근 4.3565·폴백 $n$ 0.778/0.623/0.545/0.467·FWHM 상수 3.5255·$\gamma{=}5$ PSD 0.99 mV) |
| [K] | P10 등호-한-점 | $\Omega=2RT$ 에서 $g''$ 의 전역 최솟값 0 이 $\xi=0.5$ 에서만 도달(수치 스캔 99999점) — "등호는 한 점" 정확 |
| [L] | L21 anchor 거리 | $|0.5-0.48|=0.02<|0.5-0.55|=0.05$; $|0.667-0.55|=0.117<|0.667-0.48|=0.187$ — 근접성 역전 사실 재확인(양쪽 tier C 처리로 이미 닫힘, 신규 결함 아님) |

---

## 3. refute 생존 지적 (심각도순 — CRIT/HIGH/MED 0)

### LOW-1 | ch1 fig:lco-electronic 주석 (L2644·L2652–2653) — "$x\to1$ 좌측 끝: $g\to0$" 주석과 게이트 곡선 시작값(4.7% $g_{\max}$)의 불일치
- **원문**: 그림 내 주석 "insulator ($x\!\to\!1$ 좌측 끝: $g\!\to\!0$)"·캡션 "$x\!\approx\!1$ 절연체에서 $\approx0$".
- **결함**: 게이트 식~eq:ggate 그대로 평가하면 $x{=}1$(축 좌측 끝)에서 $g=g_{\max}[1-\sigma(3)]=0.617$ e/eV/atom — $g_{\max}$ 의 **4.7%로 0 이 아니며**, 그림 좌표 자체(0.123, 높이 2.6 스케일)가 그 값을 정직하게 그리고 있어(§2-[F]) 주석 "$\to0$"과 곡선 시작 높이가 지면에서 눈에 띄게 어긋난다. 물리(실제 LiCoO$_2$ $x{=}1$ 은 진짜 절연체 $g{=}0$)와 모델(logistic 꼬리 잔차)의 차이가 주석에 뭉개졌다.
- **refute 시도**: "≈0/→0 은 $g_{\max}$ 대비 소수라는 뜻" — 4.7%를 "≈0"으로 읽는 관례는 가능하나, "$\to$"(극한 화살표)는 축 좌측 끝에서 실제로 0 에 도달하지 않는 곡선에 대해 문자 그대로 성립하지 않고, 같은 문건이 "좌표는 식 그대로의 수치 평가"를 그림 규율로 삼는다 — 생존(경미).
- **정정 제안**: 주석을 "insulator ($x\!\to\!1$: $g\!\approx\!0.05\,g_{\max}$ — 게이트 꼬리 잔차)" 로, 또는 캡션에 "(게이트 근사라 $x{=}1$ 에서 정확히 0 은 아님)" 1구.

### LOW-2 | ch2 L529–530 — "~0.3 mV/K 급" 의 문건 내 도출 근거 부재 (★가장 약한 1곳)
- **원문**: "만일 실측 $w_j$ 가 $T$-동결에 가깝다면 단순식/완전식의 우열이 뒤집히는 $\sim$0.3 mV/K 급 차이가 남는다."
- **결함**: 이 차이 = config 항 크기인데, 문건 자신이 제시하는 검증 수치는 "그리드 실측 최대 0.18·해석 상한 0.21·서명 범위 $[-0.21,+0.14]$ mV/K"(L516–518)뿐이다. "~0.3" 은 그 어느 값과도 직접 일치하지 않으며 도출이 본문에 없다. 재검산(§2-[I])으로는 두 독해에서만 성립한다 — (i) 서명 범위의 peak-to-peak $0.35\approx0.3$ 급, (ii) 그리드 밖 꼬리($|z|\approx3.5$, 컷 4.357 에서 0.375)까지의 스팬-의존 성장. 어느 쪽이든 "급" 서술로는 방어되나(refute 부분 성공 — MED 이하로 강등), 독자가 같은 절의 0.18/0.21 과 대조하면 출처 불명의 세 번째 수가 된다.
- **정정 제안**: "$\sim$0.2–0.4 mV/K 급(검증 그리드의 서명 범위 peak-to-peak 0.35; 스팬을 꼬리 컷까지 넓히면 0.38)" 처럼 기존 수치와 잇거나, 괄호로 근거 1구 병기.

### INFO-1 | ch1 L1719 — "$\mathcal A\gtrsim3RT$ 면 1로 수렴한다" 의 문턱 잔차 5%
- $A{=}3RT$ 에서 인자 1.0498(편차 4.98%) — "수렴"의 경계값이 문건의 5% 컷 관례와 동급이라 서술은 성립하나, 기본 실효 컷($4RT$, 잔차 1.8%)을 쓰면 더 여유가 있음을 병기할 여지. 결함 아님(기록).

### INFO-2 | ch1 L1974–1976 — $3\to2\mathrm L$ anchor 편차 15 mV = 선언 범위 "5–15 mV" 의 상단 끝점
- $0.140-0.125=15.0$ mV 로 "편차 **안**"이 경계 포함 독해에서만 참(초과가 아니라 정확히 끝점). tier C 명기로 이미 보수 처리되어 있어 결함으로 세지 않음(기록). 문안을 "편차 상한과 같은 배치값"으로 하면 중의성이 사라진다.

---

## 4. 가장 약한 1곳 (필수 지목)

**LOW-2 — ch2 L529–530 의 "~0.3 mV/K 급".** 이유: 본 라운드 전수 목록(약 90항)에서 수학적으로 반증되는 주장은 없었고, 유일하게 **문건 내 도출 사슬이 끊긴 정량 주장**이 이것이다 — 같은 srcbox 가 세 개의 정밀 수치(0.18/0.21/$[-0.21,+0.14]$)를 제시한 직후에 근거 없는 네 번째 수(0.3)가 등장하며, 그 수는 검증 그리드의 최대값을 1.4배 초과한다. 재검산으로 "급" 독해(peak-to-peak 0.35 또는 꼬리 스팬 0.30–0.38)의 방어가 가능해 FAIL 은 아니지만, 이 문장은 단순식/완전식 선택이라는 실무 판단의 스케일 기준이라 하중이 있고, 수정은 괄호 1구로 닫힌다.

---

## 5. 요약

- **전수 목록 약 90항(Ch1 ~68 · Ch2 ~22) 중 FAIL 0.** 기검산 승계 약 75항 + 신규 독립 검산 15항(§2 [A]–[L]) 전건 성립.
- 신규 검산의 수확: ① P4.1 신설 문안 3건(W2 유효 폭 $(1-\Omega/2RT)$·K3 실효 컷 7%·T3 초기 $L_V$/문턱 $\Delta H_a$)이 전부 독립 재계산과 일치 — 특히 T3 은 코드 미참조 식-단독 재유도로 R5-B 의 코드 실행값을 재현. ② 이전 라운드가 안 본 두 단정 — gap 의 $\Omega$-단조 증가($\dd\Delta U^\hys/\dd\Omega=2u/F>0$)와 $g''$ 등호-한-점 — 을 해석적으로 확정. ③ $\nu\gtrsim10$ 경계의 $\nu{=}9$(5.45%) 확인.
- 생존 지적: **LOW 2**(fig:lco-electronic "$g\to0$" 주석 vs 4.7% 잔차 / ch2 "~0.3 mV/K" 근거 공백) · **INFO 2**(3RT 수렴 잔차 5% / 15 mV 경계 끝점). CRIT·HIGH·MED 0.

*검수자 B (Fable) · V1.0.14 P4.1 R6 · 파일 수정 0건(본 보고서 1건 신규). 수치 스크립트: scratchpad/r6b_verify.py(세션 임시).*
