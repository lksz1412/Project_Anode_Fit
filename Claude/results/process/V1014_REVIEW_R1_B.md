# V1014 REVIEW R1 — 검수자 B (Fable) 통독 보고서

- 대상: `Claude/docs/v1.0.14/graphite_ica_ch1_v1.0.14.tex` L1660(\section 동역학 지연 길이 $L_V$ (N7))–L3201(파일 끝)
- 렌즈: 통독(재배치·치환 편집 여파) + G-usable(부록 A/B 조회 가능성·포인터 무결·본문↔표 일치·이관 잔해) + 물리 정합(코드-주어문→물리 서술 치환의 의미 보존 — N7 사슬·N8 격자 역전·LCO σ_d 슬롯·부호)
- 수칙 준수: 전 지적 refute 시도 후 생존분만 기재. 파일 수정 0건(본 보고서 신규 작성만).

---

## 1. 결함 목록

### B-01 | HIGH | tab:staging 캡션 (L1936–1938)

- **원문**: "전위 anchor: $4\to3$($0.210$ V)$\cdot$$2\to1$($0.085$ V)는 Dahn\cite{dahn1991}, $3\to2\mathrm L$$\cdot$$2\mathrm L\to2$($0.120$ V)는 Ohzuku 등\cite{ohzuku1993} 의 보고값과 정합(2차 출처 경유 확인 — 문헌 간 $5$--$15$ mV 시료 의존 편차 존재)."
- **결함**: Dahn 쌍은 전이별 값이 각각 병기(0.210/0.085)되어 있는데 Ohzuku 쌍은 두 전이($3\to2\mathrm L$, $2\mathrm L\to2$)에 괄호 값이 하나(0.120 V)뿐이다. 병렬 구조상 자연스러운 독해("두 전이 모두 0.120 V anchor")로는 표 본체의 $3\to2\mathrm L$ 행 $U=0.140$ V(L1947)와 20 mV 어긋나 — 캡션 스스로 선언한 허용 편차 5–15 mV 를 초과한다. "(0.120 V) 가 $2\mathrm L\to2$ 에만 붙는다"는 대안 독해를 취해도, $3\to2\mathrm L$(0.140 V)의 "Ohzuku 보고값과 정합" 주장은 대응 값이 없어 검증 불가 진술이 된다. v1.0.14 ⑤(캡션 레퍼런스 병기)에서 신규 유입된 결함.
- **근거**: 표 본체 L1947 `$3\!\to\!2\mathrm L$ & 0.140`, L1948 `$2\mathrm L\!\to\!2$ & 0.120`. 어느 독해로도 0.140 행의 anchor 정합이 성립·검증되지 않음.
- **정정 제안**: Dahn 쌍과 같은 전이별 병기로 교체 — 예: "$2\mathrm L\to2$($0.120$ V)는 Ohzuku 등\cite{ohzuku1993} 과 정합; $3\to2\mathrm L$($0.140$ V)는 두 인접 plateau 사이 모델 배치값(직접 문헌 anchor 근거 미발견 — tier C)". 실제 Ohzuku 보고 plateau 에 0.140 V 대응이 있으면 그 값을 명기.

### B-02 | MED | 본문 잔존 구현-어투 9곳 (③ 코드-언급 제거의 편집 잔해)

- **원문**(각 위치):
  - L1758–1759: "지연 길이를 직접 지정하면 동역학 계산을 우회해 그 값을 쓰고, $I\le0$ 이거나 활성화 엔탈피 입력이 없으면 $L_V=0$ 이다."
  - L1797: "$L_V\le0$ 이거나 비유한이면 원신호를 그대로 돌린다."
  - L1841: "그 작은 $L_V$ 환원은 코드의 분기 스위치가 담당한다"
  - L1857–1858(각주): "v12 코드에서 기본 $\nu$ 상향($\gtrsim10$) 또는 문턱 근방 blend 를 검토한다"
  - L1859: "코드가 꼬리식으로 평가하지 않는 구간이다"
  - L1907(그림 캡션): "격자를 뒤집어 필터($\xi[::-1]\cdots[::-1]$)" — Python slice 표기
  - L1926: "스칼라 입력이면 첫 성분만 반환한다."
  - L2756–2757 및 L2829–2830: "코드는 전압 격자 위에서 돌므로" (동일 구 2회)
  - L2859–2863: "\emph{현행 구현}은 … 동결 구현은 순환이 없고"
- **결함**: 부록 B 서두(L3036–3037)가 "본문을 코드 언급 없이 물리로만 읽을 수 있게 하면서"라고 이관 목적을 선언하는데, 위 9곳이 본문(그림 캡션 포함)에 구현-주어 문장·API 반환 의미론·slice 표기로 남아 그 선언과 모순된다. 특히 L1926("반환한다")·L1907("[::-1]")은 물리 문장으로 위장되지 않은 노출 잔해다.
- **근거**: 내용 자체는 전부 코드와 일치함을 확인(오류 아님 — `_resolve_lag_length`: `if I <= 0 or transition.get('dH_a') is None: return 0.0`; `_causal_lowpass`: `if lag_length <= 0 or not np.isfinite(...): return source_signal.copy()`). 곧 정확성 문제가 아니라 v1.0.14 자체 편집 목표(③)와 부록 B 선언에 대한 자기일관성 결함.
- **정정 제안**: L1926 → "스칼라 전위 입력은 한 점의 값으로 축약된다" 류 물리 서술 또는 부록 B 이관. L1907 → "역순 필터 후 재역순" 물리 서술(slice 표기는 tab:nodecode N8 에 이미 있음). 나머지는 "코드/구현" 주어를 "모델의 수치 처방" 류로 치환하거나, 의도적 잔존이면 부록 B 서두 선언을 "본문 수치-처방 서술 최소 잔존" 으로 완화.

### B-03 | MED | Motohashi config 값의 T2/T3 슬롯 배정 — 근접성 역전 + tier 플래그 비대칭 (L2032–2033, L2339–2342, L2757–2758)

- **원문**: 표 L2032 "T2 … config 주도($\approx$0.47 J/(mol\,K))", L2033 "T3 … config($\approx$1.49 J/(mol\,K); 배정 tier C)"; 본문 L2340–2342 "($\approx0.47$ J/(mol\,K)@$x{=}\tfrac12$, $\approx1.49$ J/(mol\,K)@$x{=}\tfrac23$ [값은 tier A, Motohashi; 단 $x{=}\tfrac23$ anchor 는 T2/T3 조성 창($x\approx0.55/0.48$) 밖이라 슬롯 배정은 tier C — 최종 귀속은 피팅 위임])"; L2758 "$\approx0.47/1.49$ J/(mol\,K), T2/T3".
- **결함**: 조성 근접성으로는 배정이 역방향이다 — $x{=}\tfrac12$ anchor(0.47)는 T3 창($x\approx0.48$, $|\Delta x|=0.02$)에 가깝고 T2 창($x\approx0.55$, $|\Delta x|=0.05$)에서 멀며, $x{=}\tfrac23$ anchor(1.49)는 오히려 T2 쪽에 가깝다($|\Delta x|=0.117$ vs $0.187$). 그런데 (i) 0.47→T2 배정의 근거가 어디에도 서술되지 않고, (ii) 두 anchor 모두 배정 창 밖임에도 tier C 플래그·사유는 $x{=}\tfrac23$/T3 행에만 붙어 T2 행("config 주도(≈0.47)")은 무유보로 읽힌다.
- **근거**: 위 3개 위치의 수치 대조(0.5 vs 0.55/0.48; 0.667 vs 0.55/0.48). refute 시도 — "$x{=}\tfrac12$ 질서상이 T2 경계 형성"류의 물리 사유가 있을 수 있으나 문건 내에 그 근거 서술이 없어, 문건만으로는 배정이 정당화되지 않음(추정 배제, 문건 내 근거 부재로 판정).
- **정정 제안**: T2 행에도 "배정 tier C" 병기 + 본문 괄호를 "두 anchor($x{=}\tfrac12,\tfrac23$) 모두 T2/T3 조성 창과 정확히 일치하지 않아 슬롯 배정은 양쪽 다 tier C(값은 tier A) — 귀속은 피팅 위임"으로 대칭화. 0.47→T2 선택에 물리 사유가 있으면 한 줄 명기.

### B-04 | LOW | 컷-동결 동기 부등식의 방향 한정 누락 (L1753–1757; 부록 S6 L2976–2979 동형)

- **원문**: "부등식 $\partial\ln L_q/\partial V<0$ 은 \emph{물리적 동기}로 읽어야 한다 — 만일 $\mathcal A$ 를 컷에 동결하지 않고 국소 구동력 $\mathcal A=\sigma_dF(V_n-U)$ 로 두면 $V\!\uparrow\Rightarrow\mathcal A\!\uparrow\Rightarrow$ 유효 장벽$\downarrow\Rightarrow L_q\downarrow$"
- **결함**: 구동력을 방향 일반형 $\sigma_dF(V_n-U)$ 로 적어 놓고 화살표 사슬은 $\sigma_d$ 를 떨군다 — $V\!\uparrow\Rightarrow\mathcal A\!\uparrow$ 및 $\partial\ln L_q/\partial V<0$ 은 $\sigma_d=+1$(방전)에서만 성립하고 충전($\sigma_d=-1$)에서는 $V$-미분 부호가 뒤집힌다(진행 좌표를 따라가면 양방향 동일 단조성). 부록 표는 기준 명제가 방전-프레임(L2949–2950)이라 방어되나, 본문 이 문단에는 그 한정이 없다.
- **근거**: $\mathcal A=\sigma_dF(V_n-U)$ 에 $\sigma_d=-1$ 대입 시 $\partial\mathcal A/\partial V=-F<0$.
- **정정 제안**: "방전 기준($\sigma_d=+1$; 충전은 진행 방향 $V\!\downarrow$ 를 따라 같은 단조성)" 한 구 삽입, 또는 부등식을 진행 좌표로 서술("진행이 깊어질수록 $L_q$ 감소").

### B-05 | LOW | 절 도입문 편집 이음새 — 문장 개시구 중복 (L1662–1663)

- **원문**: "유한 전류에서는 평형 목표 $\xi_\eq$ 를 점유가 즉시 따라가지 못하고 뒤처진다 — 그 지연이 peak 의 꼬리다. 유한 전류에서는 전이당 하나의 지연 길이 $L_{V,j}$ 를 구한다"
- **결함**: 연속 두 문장이 같은 개시구 "유한 전류에서는"으로 시작 — P4 재작성의 접합 잔해로 읽힌다(어투 정련 ④ 대상 누락).
- **근거**: 원문 그대로.
- **정정 제안**: 둘째 문장을 "이 절은 그 지연을 전이당 하나의 길이 $L_{V,j}$ 로 닫는다" 류로 접합.

### B-06 | LOW | 동일 표 연속 재지시 (L1929–1930)

- **원문**: "네 전이의 초기값이 표~\ref{tab:staging} 에 있다(신뢰값이 아닌 \emph{초기값} — …). 표~\ref{tab:staging} 가 각 인자의 의미와 출발값이다 — 이 표가 있어 …"
- **결함**: 연속 두 문장이 같은 표를 거의 같은 술어("초기값이 있다"/"의미와 출발값이다")로 재지시 — 치환 편집의 잔해성 중복.
- **근거**: 원문 그대로.
- **정정 제안**: 한 문장으로 병합 — "표~\ref{tab:staging} 가 네 전이 각 인자의 의미와 출발값(신뢰값 아닌 초기값, 피팅 override 전제)이며, 이 표가 있어 '이 문건만으로 곡선 재현 코드를 짤 수 있다'."

### B-07 | LOW | tab:nodemap N9$'$ 행의 (MSMR eq:msmr) 병기 — 색인 정밀도 (L2940)

- **원문**: "N9$'$ & $\Delta S^\mathrm{cat}=$config$+$vib$+$elec (MSMR \eqref{eq:msmr}) & \eqref{eq:lco-decomp}"
- **결함**: $\Delta S$ 분해(eq:lco-decomp)와 MSMR 점유식(eq:msmr)은 무관한 두 결과인데 한 행에 병기됐다. tab:nodecode(L3146)의 N9$'$ 는 `\_effective\_dS\_rxn`(분해 seam)만 가리키므로, 노드 표로 MSMR 을 추적하는 독자는 MSMR 내용이 없는 식별자에 착지한다. MSMR 사전(eq:lco-msmrmap)·변환 폐쇄(eq:lco-msmrpeak)는 노드 행이 없다.
- **근거**: eq:msmr(L2768–2771)=MSMR 종별 점유식, eq:lco-decomp(L2725–2730)=$\Delta S$ 3-성분 분해 — 서로 다른 내용.
- **정정 제안**: N9$'$ 물리식 열에서 "(MSMR \eqref{eq:msmr})" 제거, 필요 시 별도 행 "N5$'$(또는 각주): MSMR 동형 사전 \eqref{eq:lco-msmrmap}" 신설.

### B-08 | LOW | "진행 방향 뒤쪽" 공간 독해 모호 (L1874–1876)

- **원문**: "peak\_shape $=(\xi_\eq-\xi_\mathrm{lag})/L_V$ 는 양수를 유지한다(꼬리가 진행 방향 뒤쪽 — 시간상 나중에 지나는 전위 쪽 — 곧 충전에서는 $V$ 가 낮은 쪽으로 늘어진다)."
- **결함**: "진행 방향 뒤쪽"의 공간 독해(진행 방향의 후미 = 방전에서 낮은 $V$)는 뒤따르는 올바른 주석("시간상 나중에 지나는 전위 쪽" = 방전에서 높은 $V$, 그림 (a) "tail $\to$ higher $V$")과 정반대다. 시간 독해("뒤"=나중)로만 성립하는 표현이 부호-민감 지점(★충전 격자 역전 절)에 있다.
- **근거**: 그림~\ref{fig:reversal}(a) L1890 "tail $\to$ higher $V$" — 방전 꼬리는 진행 방향 앞(높은 $V$) 쪽.
- **정정 제안**: "꼬리는 진행상 나중에 지나는 전위 쪽으로(방전은 높은 $V$, 충전은 낮은 $V$)"로 공간 중의성 제거.

### B-09 | LOW | $n_j$ 부호 전제의 두 서술 간 미세 긴장 (L1703 vs L1761)

- **원문**: L1702–1703 "컷 affinity 의 크기는 충$\cdot$방전 동일($n_j>0$ 라 항상 양수)" vs L1761 "다중도의 크기 $|n_j|$(부호 제거)에서 컷 affinity $\mathcal A$ … 로".
- **결함**: 전자는 $n_j>0$ 를 전제로 양수성을 주장하고, 후자(및 부록 codebox N7 의 `n\_safe=|n\_j|`)는 부호 제거가 필요한 듯 서술 — 같은 절 안에서 전제(항상 양)와 처방(절댓값)이 미세하게 어긋난다. 물리 왜곡은 없음(코드 가드 `abs` 는 방어적 처리).
- **근거**: 두 원문 병치; 코드 `n_safe = abs(_finite("n_j", n_j))` 확인.
- **정정 제안**: L1761 을 "$n_j$(입력 가드로 크기만 취함)" 류로, 혹은 L1703 에 "(입력 이상치는 크기로 정규화)" 병기해 정합.

---

## 2. 구획별 0-결함 근거 (빈 통과 금지 이행)

| 구획 | 범위 | 결함 | 검증 내용(적대 검산 수행분) |
|---|---|---|---|
| N7 사슬 | L1660–1766 | B-04·B-05·B-02 일부 | $z_\mathrm{cut}=4.357$ 을 독립 재계산 — $\sigma(1-\sigma)=0.0125$ 의 해 $z=4.3565$ 로 "5% 컷 대응 선택값" 정확. eq:kuniv 의 $r^-=r^+e^{-\mathcal A/RT}$ ↔ eq:db(L1210–1213) 정합. $\Delta H_a^\eff$ 흡수: 방전 $\xi\to1$ 에서 $-\Omega(1-2\xi)\to+\Omega$, 충전 $\xi\to0$ 에서 $+\Omega(1-2\xi)\to+\Omega$ — 양방향 $+\Omega$ 대수 확인, eq:mu(L598–599)의 $\theta\to\xi$ 부호 반전 서술 정확. eq:Lqmid2→eq:Lqfull 인자 분해 대수 확인 |
| N8 꼬리·역전 | L1768–1910 | B-02·B-08 | 점프 닫힌식 $1-(1/\nu)/(e^{1/\nu}-1)$ 을 이산 점화식에서 독립 재유도($\sum e_i=\rho/(1-\rho)$ → 꼬리 면적 $(1/\nu)/(e^{1/\nu}-1)$): $\nu{=}2\to23.0\%$, $8\to6.1\%$, $10\to4.9\%$, "$\approx50\%/\nu$" 전개 모두 본문 수치와 일치. "높이도 같은 인자" 주장( $L_V\!\ll\!w$ 완만 극한에서 비 $(1/\nu)\rho/(1-\rho)$ ) 재유도 일치. 저역통과 초기값 $\xi_{\mathrm{lag},0}=\xi_{\eq,0}$ ↔ 코드 `zi=[ρ·s[0]]`(첫 출력 $=s[0]$) 일치. $L_V\to0$ 이 $0/0$ 이라 종으로 환원 안 됨 — 논증 유효 |
| N9·표 | L1913–1960 | B-01·B-06·B-02 일부 | 표 4행 $U(298)$ round-trip 전건 재계산: 0.21088/0.13992/0.12032/0.08529 — "±1 mV 정합, $4\to3$ 만 0.2109 자리수 경계" 서술 정확 |
| Part II 도입·방향 | L1962–2133 | 없음 | eq:lco-sigmaslot ↔ Part I 부호 규약(L217–219 "방전 $\sigma_d{=}+1$ … 전위를 올리면 탈리튬화") ↔ 코드 `_delith_is_discharge`(흑연 True/LCO False)·docstring 3중 일치. T2/T3 조성-전위 단조성(0.55@4.05 < … 아니, $x$ 감소 방향으로 4.05→4.17 ✓). fig:lco-dirmap 배선(충전→delith→$+1$) 확인. 층위 구분 문단(L2074–2077)이 lco-map 의 "셀 방전=리튬화"와의 외견 모순을 선제 해소 |
| LCO 중심 N2$'$ | L2135–2226 | 없음 | 이중 경로(직접 미분/Gibbs 항등식) 대수 확인; Kirchhoff 논증($T\partial_T\Delta S=\Delta C_p$ ↔ $\Delta H$ 고정 모순) 물리 정확; verifybox 수치 전건 재계산 — $96485\times0.83\times10^{-3}=80.1$, $30$ K$\times0.83$ mV/K$=24.9$ mV, $+80-46=+34$ |
| LCO 히스 | L2228–2386 | B-03 | spinodal $\xi_s^\pm=\tfrac12(1\pm u)$ 근 재유도; gap $\tfrac2F[\Omega u-2RT\,\mathrm{artanh}\,u]$ 를 eq:lco-Veq 두 끝점 대입으로 독립 재유도(eq:hyssub L1076–1080 대조); 도핑 극한 $\tfrac{8RT}{3F}u^3$ Taylor 재유도 — 흑연 L1101–1103 과 동일식 확인. "표에 $\Omega^\mathrm{cat}$ 열 없음" 진술 ↔ 실제 표 열 구성 ↔ Part 0 L587("표 밖 — 피팅 배정 전제") 3중 일치 |
| LCO 전자항 N5$+$ | L2388–2619 | 없음 | Sommerfeld 이중 경로($C_e$ 적분/직접 엔트로피 $\int s\,\dd\zeta=\pi^2/3$) 표준 결과 확인; 단위 사슬 $N_Ak_B^2=Rk_B$·$1/e_V^2\approx3.9\times10^{37}$ 재계산; 골 깊이 $-\tfrac{\pi^2}{3}R\tfrac{k_BT}{e_V}\tfrac{13}{0.05}\cdot\tfrac14=-45.96$ J/(mol K)@300 K(코드 주석 $-45.678$@298.15 와 온도비로 정합); $S_e=1.108\,k_B$/atom 재계산; 게이트 적분=끝점 $S_e$ 항등 확인; $g_{\max}{=}13$ ↔ $\gamma\approx30$ mJ/(mol K$^2$) 역산 정합; eq:U1T2 의 $\tfrac12$ 계수 — $\Delta H(T)$ Kirchhoff 보정 포함 재유도로 열역학 자기일관 확인; 그림 fig:lco-electronic 좌표(logistic 0.2688@$z{=}-1$) 수치 일치 |
| LCO peak·분해·MSMR | L2621–2883 | B-02 일부 | eq:lco-belliden·peakobs($Q/4w$·면적 $Q$) 재유도; config 혼합항 $+R\ln\tfrac{\xi}{1-\xi}$ 부호를 $S_\mathrm{mix}$ 부분몰로 재유도(삽입 기준 ✓); MSMR $f=+\sigma_d$ — 진행률/점유 두 pairing 모두 동일 해, 직접 등치 시 $f=-\sigma_d$ 재현 확인; 되먹임 상한 $46/96485\times30=14.3$ mV 재계산; 고정점 서술(L2863–2865)의 참조 방향(xmap←$\xi$←$U$←$\Delta S_e$←xmap) 순환 정확 |
| 입력 인자·facade | L2885–2943 | B-07 | keybox 6단계 포인터 전건 해소 — 특히 \eqref{eq:center} 는 분기 중심 평가식(L1124–1130) 실재로 올바른 참조(오지시 아님). nodemap N5$+$ 식 $N_A\tfrac{\pi^2}{3}k_B^2T\,\partial g/\partial x\equiv\tfrac{\pi^2}{3}Rk_BT\,\partial g/\partial x$ 항등 확인 |
| 부록 A | L2946–3030 | 없음 | S1–S8 근거식 전건 원문 대조(eq:Uj L982–985·eq:eqcond L963–967·eq:xieq L1229–1232·eq:eqpeak L1391–1398·eq:dUhys L1094–1099·eq:Ubranch L1114–1117·eq:chid·eq:dHeff·eq:Lqfull·eq:LV·eq:reversal·eq:vn L900–903·eq:Acut) — 각 행 명제가 근거식 내용과 일치. R1 재계산 $u=0.7661$, $\Delta U^\hys=86.68$ mV ✓; R2 $2RT=4957.8\approx4958$ ✓; R6 $+80.1$·$+25$ mV ✓; R3·R4·R5 논증 본문(L1753–1757·L1836–1859)과 정합. S6 방향 프레임은 표 기준 명제(L2949, 방전-프레임)로 방어됨 — 본문 측만 B-04 |
| 부록 B | L3032–3165 | 없음 | 표 3종 식별자 53종 전수 grep — 전부 `Anode_Fit_v1.0.14.py` 에 실재. 생성자 기본값 12종(x=0.5·Rn=0·Cbg=0·use_dH_eff=True·z_cut=4.357·A_cap_RT=4.0·pad 0.15/0.15·2048·2.0·1e-6·seed 298.15/0.1/1.0) 코드 L251–261 과 전건 일치. nodecode N8 lfilter 계수 $[1{-}\rho]/[1,-\rho]$·충전 `[::-1]…[::-1]` ↔ `_causal_lowpass` 일치. codebox N2 수치 $0.0853$ 재계산 일치. tab:lco-staging 캡션 시연값 3.930/3.880/4.050·electronic=T1·x_MIT=0.85 ↔ `LCO_MSMR_LIT` 일치 |
| 참고문헌 | L3167–3199 | 없음 | 신규 5건(reynier2003·persson2010·persson2010b·cogswell2012·park2021) 모두 본문 인용 실재(1/1/1/1/4회) — orphan 0. cogswell2012 는 L1568(broadening, 범위 밖)에서 인용되며 bibitem 주석("γ 수치 출처 아님")과 역할 일치. LaTeX log 미해결 참조 0(폰트 shape 경고 3건만) |

## 3. Coverage 선언

- 대상 범위 L1660–3201: Read 4회(1655–2114 / 2115–2574 / 2575–3033 / 3034–3201)로 전 라인 통독 — **missing 0**.
- 범위 밖 대조 정독(참조 무결 검증 목적): L196–235(N0·부호 규약), L468–483(eq:fermifn), L563–622(eq:mu·eq:gxi·문턱), L879–1002(eq:vn·eq:vwork·eq:eqcond·eq:Uj), L1069–1243(eq:dUhys·eq:Ubranch·eq:center·fig:hysloop·eq:db·eq:xieq), L1372–1411(eq:belliden·eq:eqpeak). `\label` 전수 추출로 범위 내 `\eqref`/`\ref` 표적 전건 해소 확인 — 깨진 참조 0.
- 코드 대조: `Anode_Fit_v1.0.14.py` — 식별자 53종 grep, 생성자 기본값 블록, `_causal_lowpass`·`_resolve_lag_length`·`func_dSe_molar` 본문, `LCO_MSMR_LIT` 정독.

## 4. 가장 약한 1곳

**B-03(Motohashi config 슬롯 배정, L2032–2033·L2339–2342)** 를 지목한다. 이유 — 이 범위에서 tier-A 실측값이 물리 슬롯에 매달리는 유일한 자리인데, (i) 배정의 조성 근접성이 실제로는 역방향이고, (ii) 그 사실이 표·본문 어디에도 서술되지 않으며, (iii) tier-C 유보가 T3 에만 비대칭으로 붙어 T2 값("config 주도")이 무유보 tier-A 처럼 읽힌다. 적대적 검토자가 "값은 맞는데 자리가 왜 거기냐"로 가장 먼저 찌를 수 있는, 문건 내 근거가 비어 있는 지점이다(B-01 은 더 명백하나 국소 수정으로 닫히는 반면, B-03 은 배정 논거 자체의 공백).

---
*검수자 B (Fable) — v1.0.14 P4.1 R1. 본 보고서 외 파일 수정 0건.*
