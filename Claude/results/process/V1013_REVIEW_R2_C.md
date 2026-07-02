# V1013 REVIEW — Round 2, 검수자 C (절 단위 청크: Ch2 전문 + 코드-문건 상호충실도)

- 대상: `Claude/docs/v1.0.13/graphite_ica_ch2_v1.0.13.tex`(791줄 전문) · `Anode_Fit_v1.0.13.py`(879줄 전문) · Ch1 facade/nodemap 신설 서술부(L130–219·L2770–2849) 대조.
- ★렌즈 ⑧(R1 수정 여파 전파) 최우선 수행. R1 원 지적 대조: `V1013_REVIEW_R1_C.md`(C-02 x/x̄·C-04 facade 전극 인지·C-06 MCMB·C-07 부동소수점·C-10 eq:muV σ_d·C-13 약자·C-14 라인 앵커).
- 수치 재계산: scratchpad `verify_derivA_r2c.py`·`verify_nj_r2c.py`(원본 코드 read-only import, 이분법 U_oc solver + 파생 A 완전식/단순식/config 독립 재구현).

---

## A. 렌즈 ⑧ — R1 수정 여파 전파 전수 (지정 5항목)

### ① eq:muV σ_d→s 치환 후 잔재 — **PASS (잔재·모순 0)** [확정]
- 근거: Ch2 내 `\sigma_d` 전수 3곳 — L149–150(각주: "방향 부호 σ_d(분극·분기·꼬리 세 작용처 전용)와 혼동하지 말 것"), L690(방향 라벨 대조 "σ_d=+1"), L745(procedurebox 분극 "$V_n=V_\mathrm{app}-\sigma_d|I|R_n$"). 셋 다 σ_d 의 정당 작용처(경고/라벨/분극)이며 평형식엔 재유입 없음.
- 재유도: eq:muV $\mu=\mu^0-sF(V-U_j)$, $s{=}+1$ → $\beta(\varepsilon_0-\mu)=+ (V-U_j)/w$ → eq:logistic 의 $\theta$ 감소형/$\xi$ 증가형 부호 정확. 각주의 여집합 함정 주장(σ_d=−1 대입 시 θ↔ξ 교환·종형 불변) 대수 검산 성립.
- Ch1 대조: L226($s$ = 유도 전용 고정 부호·코드 미대응)·L1963(σ_d 세 작용처) — 서술 일치.

### ② x̄≡1−x 도입 후 x/x̄ 혼용 잔재 — **2건 잔존 + 1건 경미**

**[HIGH] R2C-1 — L721–722 (sec:revheat keybox 종합식): eq:implicit 재진술이 "$=Q\,x$" 로 x̄ 미반영**
- 원문: "주어진 탈리튬화 분율 $\bar x$(식~\eqref{eq:implicit} 좌표)에서 $\xi_j$ 를 평가하려면 먼저 전하 보존 음함수~\eqref{eq:implicit} $\sum_j Q_j\xi_{\eq,j}(U_\oc,T)=Qx$ 를 풀어 $U_\oc(x,T)$ 를 얻고"
- 무엇이: 정의식 eq:implicit(L464)은 $\sum_j Q_j\xi_{\eq,j}=Q\,\bar x$ 인데 같은 식의 재진술이 $Qx$. 같은 문장 안에서 "탈리튬화 분율 $\bar x$" 라 선언하고 식은 $x$ — 직접 모순. $\sum Q_j\xi_j=Qx$ 를 문자 그대로 풀면 여집합 SOC 의 $U_\oc$ 가 나온다(ξ 는 탈리튬화 진행률이므로).
- 근거: R1 C-02 의 수정이 eq:implicit 본체(L462–464)·fig:blend 축(L535)에는 들어갔으나 keybox 재진술에 미전파.
- 수정안: "$\sum_j Q_j\xi_{\eq,j}(U_\oc,T)=Q\,\bar x$ 를 풀어 $U_\oc(\bar x,T)$ 를 얻고" (또는 $U_\oc$ 인자 표기는 L468 의 '고정 $\bar x$=고정 $x$' 관례를 재인용).

**[HIGH] R2C-2 — L502 (파생 A 본문): "측정 $dQ/dV$(=$Q\,\partial x/\partial U$)" — 좌표·부호 오류 잔재**
- 원문: "가중 분모 $\sum Q_jg_j$ 가 정확히 측정 $dQ/dV$(=$Q\,\partial x/\partial U$; $x$ 무차원이라 $Q$ 배)이므로"
- 무엇이: ★좌표 주의(L461–462)가 이 식의 좌표를 $\bar x\equiv1-x$ 로 못 박았고, $\xi_j$ 는 $U$ 에 증가하므로 $\sum_j Q_jg_j=Q\,\partial\bar x/\partial U>0$. 본 장 규약의 $x$(Li 함량)로는 $Q\,\partial x/\partial U=-\sum Q_jg_j<0$ — 부호가 뒤집힌 항등식. x̄ 도입 이전 문구의 잔재.
- 수정안: "(=$Q\,\partial\bar x/\partial U$; $\bar x$ 무차원이라 $Q$ 배)".

**[LOW] R2C-3 — L554 (fig:blend 캡션)·L500–501 (본문): 축은 $\bar x$ 인데 서술은 "$x$ 가 전이 $j$ 에서 $j{+}1$ 로"**
- 축 라벨(L535)은 "$\bar x$ (delithiation)". '고정 $\bar x$=고정 $x$'(L468)로 위치 서술은 방어되나, 진행 방향("$j$ 에서 $j{+}1$ 로 넘어갈 때")은 배향 의존이라 $\bar x$ 로 쓰는 것이 정합. 캡션·L500 두 곳 $x\to\bar x$ 권고.

### ③ eq:qrev 라벨 층위 문단 ↔ srcbox·SOC별 서술 정합 — **PASS** [확정]
- 라벨 판정 재검증: 흑연 하프셀(흑연 0.05–0.25 V vs Li ⇒ 양극 역할)의 전기화학적 셀 방전(자발 $V<U_\oc$) = 작동전극 리튬화 — 문단 서술(L688–691) 옳음. Ch1 라벨(방전=탈리튬화, L216–218·L814)과의 "같은 단어·반대 화학 방향" 지적도 정확.
- 부호 사슬 재검산: $\dot Q_\irr=I(U_\oc-V)$ 는 $I>0,V<U_\oc$ 및 $I<0,V>U_\oc$ 모두 $\ge0$ ✓. srcbox $\Delta G=-FU_\oc\Rightarrow\Delta S=+F\,\partial U_\oc/\partial T$ 대입 시 $\dot Q_\rev=-(IT/F)\Delta S$ ✓. 전셀 음극 몫 $+IT\,\partial U_\mathrm{an}/\partial T$ ($U_\mathrm{cell}=U_\mathrm{cat}-U_\mathrm{an}$ 전개) ✓.
- SOC별 서술(L699–705): 방전(=리튬화, $I>0$) 저-$x$ ΔS>0→흡열 / 고-$x$ ΔS<0→발열 / stage 2→1(ΔS⁰=−16)→발열 — 세 분기 전부 $\dot Q_\rev=-(IT/F)\Delta S$ 와 문헌 프로파일(+29@저-$x$, −16@$x>0.5$)에 정합. 모순 없음.
- procedurebox(L745)의 σ_d 사용은 분극 작용처라 문단의 "본 절 부호는 전류 부호 $I$ 로" 원칙과 충돌 없음.

### ④ "표시 정밀도" 완화 전파 — **2곳 반영·2곳 잔재**
- 반영 확인: L512–513(srcbox 1문단 "표시 정밀도($\lesssim10^{-2}$ mV/K)…잔차 수 $\mu$V/K 급은 이 표시 정밀도 아래") ✓ · L727–729(한계(1) "유한차분과 표시 정밀도로 일치") ✓.

**[HIGH] R2C-4 — L523 (같은 srcbox ★전제 명시 문단): "완전식의 부동소수점 일치는" — 완화 미전파, 같은 박스 안 자기모순**
- L512 가 "표시 정밀도 일치(잔차 μV/K 급)"로 완화됐는데 열 줄 아래 L523 이 "부동소수점 일치"를 재주장. μV/K 잔차는 float epsilon 급이 아니므로 두 서술은 같은 박스 안에서 양립 불가(R1 C-07 지적의 잔재).
- 수정안: "완전식의 표시-정밀도 일치는" (또는 "완전식-유한차분 일치는").

**[MED] R2C-5 — L787 (bibitem numverif2026): "[내부 자료 — 부동소수점 일치 PASS, …]" — 동일 잔재**
- 수정안: "표시 정밀도 일치 PASS" 로 동기화.

### ⑤ MCMB 미검증 괄호 문장 흐름 — **내용 정확·형식 규범 위반**

**[MED] R2C-6 — L335–337: ★단위 주의 괄호 보충(3.5줄·중첩 괄호·완결문 2개 내장)이 문단 흐름 절단 + 프로젝트 문체 규범(괄호 보충 금지) 저촉**
- 산술은 정확: $29/96485=0.30$ mV/K ✓, +3∼4 mV/K 와 자릿수 차 ✓, [미검증] 표기 적절 ✓ — R1 C-06 의 실질은 해소.
- 남은 문제: (a) 인용문("보고된다")과 문단 본론(표~tab:ds 정합) 사이에 괄호 안 완결 문장 2개("…자릿수가 다르다; …참고 인용이다")가 끼어 교과서 문체 규범(괄호 보충 전보체 금지 — 완결 문장으로) 위반, (b) 괄호 2중 중첩, (c) 단위 표기 "J/(mol\,K)" 가 같은 문단 L333 의 "J\,mol$^{-1}$K$^{-1}$" 와 불일치.
- 수정안: 괄호를 해체해 독립 문장으로 승격 — "다만 단위에 주의한다. 이 $+3\sim4$ mV/K 는 본 문서 스케일($\Delta S\approx+29$ J\,mol$^{-1}$K$^{-1}$, 곧 $+0.30$ mV/K)과 자릿수가 달라 보고 조건·단위 상이 가능성이 있고, 원문 재확인 대상[미검증]이며 본 문서 입력값과 무관한 참고 인용이다."

**[LOW] R2C-7 — SOC 약자 병기 위치: 첫 출현 L78("SOC 에 따라 부호를 바꾸고")이 아니라 L335 에 병기**
- R1 C-13 반영이 두 번째 출현에 들어감. 병기를 L78 로 이동(L335 는 약자만). OCV 는 첫 출현 L605 병기 ✓, MCMB L335 병기 ✓, "천이" 잔재 0 ✓.

---

## B. 코드-문건 상호충실도 (Ch2 서술 + Ch1 facade/nodemap 신설 서술 ↔ `Anode_Fit_v1.0.13.py` 실동작)

### facade/nodemap 신설 서술 대조 — **정합 (R1 C-04·C-14 정착 확인)** [확정]
- Ch1 L2790–2797 ↔ 코드: `curve` 가 `_direction_to_sigma`·$|I|=$`c_rate`$\cdot Q_\cell$(`I_abs` 우선, L537–541)로 환산 후 `dqdv` 재사용(새 물리 없음) ✓. **전극 인지 플래그** `_delith_is_discharge=False`(LCO, L682) → `curve()` 에서 `sigma_d=-sigma_d`(L531–535), 'charge'↦σ_d=+1 ✓, 저수준 `dqdv(s=...)` 무환산 ✓ — 신설 서술과 실동작 1:1. `equilibrium` = 히스 shift 미적용·σ_d 무인자(충방전 불변) ✓.
- tab:nodemap(L2799–2827) 전 행 대조: N0 `curve`,`_direction_to_sigma` ✓ / N1 "dqdv(분극 환산부)"(L437 `V_n=V_in-sigma_d*I_abs*Rn` — C-14 라인 앵커→식별자 교체 정착) ✓ / N2 `func_U_j`(L80) ✓ / N3 `func_dU_hys`,`func_U_branch`(L136–151) ✓ / N4 `func_w`,`_width` ✓(단 R2C-9 참조) / N5 `func_ksi_eq`(L97–100, dqdv 가 σ_d 를 s 슬롯에 전달 L484) ✓ / N6 `equilibrium`·인라인(L493) ✓ / N7 `_resolve_lag_length`,`func_L_q` ✓ / N8 `_causal_lowpass`·충전 격자 역전(L499–502) ✓ / N9 `dqdv_work`,`np.interp`(L508) ✓ / N0′ `LCO_MSMR_LIT` 3전이 ✓ / N2′ `func_U_j` 동일 ✓.
- fig:spine(L157–191) 노드 순서·per-transition loop(`for tr in transitions`, L460) ✓.

**[HIGH] R2C-8 — 완전식 config 항의 $n_j$ 누락: Ch2 파생 A·keybox 종합식·코드 `entropy_coefficient` 3자 공통 — $w_j=n_jRT/F$ 일반형에서 자기일관성 붕괴**
- 위치: Ch2 L480–489(eq:dxidT 둘째 조각 "$-g_j(R/F)z_j$", L482 "$\partial w/\partial T=R/F$")·L503–504("$+Rz_j/F$")·L713(keybox 종합식 "$(R/F)\ln(\xi_j/(1-\xi_j))$")·코드 L585(`config = (R/F)*np.log(...)`).
- 무엇이: 문건 스스로 L177·L521–522 에서 $\partial w_j/\partial T=n_jR/F$ 를 명시하는데, 음함수 미분의 $w(T)$ 조각은 $-g_j\,z_j\,\partial w_j/\partial T=-g_j z_j\,n_jR/F$ 이므로 완전식 config 항의 정확형은 $(n_jR/F)\ln[\xi_j/(1-\xi_j)]$ 다. 현행 유도(L480–482)는 $w=RT/F$($n{=}1$)로 진행하면서 결과식을 일반 $w_j$ 종합식에 그대로 얹었고, 코드도 $R/F$ 고정.
- 수치 확정(재계산, `verify_nj_r2c.py`): $n_j{=}1$(현 `GRAPHITE_STAGING_LIT` 전 전이 `'n':1.0`)에선 두 형이 동일해 무증상 — 완전식 vs FD $3\times10^{-7}$ mV/K(사실상 float 일치). 그러나 $n_j{=}0.5$ 로 두면 문건/코드형 완전식의 FD 대비 최대 오차 **0.103 mV/K**(config 몫의 100% 상대오차), 정정형 $(n_jR/F)$ 은 $4.5\times10^{-7}$ mV/K 로 float 일치 유지.
- 왜 치명: srcbox(L522–523)가 "자유 피팅되는 것은 진폭 $n_j$" 라 선언 — 두-상 전이의 실측 폭(12–20 mV)은 $RT/F{=}25.7$ mV 보다 좁아 피팅 시 $n_j\approx0.5$–$0.8$ 이 정상 귀결이고, 그 즉시 종합식·`entropy_coefficient`·`reversible_heat` 가 자기 모델의 FD 와 어긋난다(단순식/완전식 우열 논거 자체가 오염).
- 수정안: (i) eq:dxidT 둘째 조각과 keybox 종합식 config 를 $(n_jR/F)z_j$ 로 일반화(유도문에 $\partial w_j/\partial T=n_jR/F$ 사용 명시), (ii) 코드 `entropy_coefficient` 의 `config` 에 `n_j` 곱(단 `'w'` 키 T-동결 입력이면 0 — R2C-9 와 함께 처리), (iii) 당장 최소 조치로는 "본 유도·종합식·코드는 $n_j{=}1$ 기준" 한정 문구. — 검수 의견만, 수정은 master 소관.

**[MED] R2C-9 — srcbox ★전제 명시(L520–528)·keybox(L176–179)의 "코드가 모든 전이에 열적 서식을 강제 / $T$-의존 함수형 자유화는 코드 후속 과제" ↔ 코드에 이미 T-동결 폭 입력 경로 존재**
- 코드 실동작: `_n_factor`(L301–307)는 `'n'` 우선·없으면 `'w'` 에서 $n=wF/(RT)$ **역산** — 이 경로에서 `_width`$=n(T)RT/F=w$ 로 폭이 온도 무관 상수($\partial w_j/\partial T=0$)가 된다. 코드 헤더 L9–11 도 "'n' 우선→'w' 역산→n=1 / 피팅 핸들=n(또는 'n' 제거 시 'w')" 로 명시.
- 무엇이: (a) "현행 코드(func\_w/\_width)가 모든 전이에 강제하는 열적 서식" — `'w'` 단독 지정 시 강제되지 않음(사실 반대인 T-동결), (b) "실측 $w_j$ 가 T-동결에 가깝다면…함수형 자유화는 코드 후속 과제"(L525–528) — T-동결 옵션은 후속 과제가 아니라 현행 입력 모드로 이미 가능. `GRAPHITE_STAGING_LIT` 가 전 전이 `'n':1.0` 이라 파생 A 검증 자체는 유효(그 한정 서술은 참).
- 수정안: "기본 파라미터셋('n' 지정)이 강제하는 열적 서식" 으로 한정 + "코드는 `'w'` 단독 지정 시 T-동결 상수 폭을 이미 지원하므로, 남는 과제는 다온도 실데이터로 어느 함수형이 맞는지 판별" 로 재서술. (tab:nodemap N4 행의 이중 입력 모드 미언급도 동반 보완 후보.)

**[MED] R2C-10 — L513–515 (srcbox)·L567–568 (파생 B): "단순식 절대오차 최대 $0.18$ mV/K" vs "config 항 $[-0.21,+0.14]$ mV/K" — 같은 프로토콜에서 양립 불가한 수치 쌍**
- 근거: 완전식$=$FD(표시 정밀도)이고 완전식$-$단순식$=$config 항(대수 항등)이므로 단순식 최대 절대오차 $=\max|{\rm config}|=0.21$ 이어야 함. 재계산: 문건의 config 범위를 재현하는 그리드($\bar x\in[0.06,0.94]$, 175점)에서 config $[-0.211,+0.130]$·max|단순식−FD|$=0.211$ mV/K — $0.18$ 과 불일치(어느 그리드에서도 두 수는 pointwise 같은 양의 max 라 분리 불가).
- 수정안: numverif 원자료 재확인 후 한쪽 수치 정정(0.18→0.21 또는 범위 재보고). 파생 B 의 재인용(L568)도 동반 수정. [원자료 미열람 — 모순 판정은 항등식 기반 확정, 어느 쪽이 오기인지는 미검증]

**[MED] R2C-11 — L515–516 (srcbox)·L554 (fig:blend 캡션): "전이 경계 4 곳 모두 계단 없이 연속" — 4-전이 사슬의 인접 경계는 3곳**
- 근거: 4 전이(4→3, 3→2L, 2L→2, 2→1)의 인접 경계는 $x=0.16,0.25,0.50$(↔$\bar x=0.84,0.75,0.50$) 3곳. 재계산으로 3곳 모두 단순식이 인접 $\Delta S^0/F$ 사이 값을 연속으로 취함을 확인(0.001 간격 스캔 최대 계단 $0.002$ mV/K — 블렌드 자체는 참). "4 곳"은 전이 수(4)와 경계 수(3)의 혼동 오기 의심 — numverif 원자료 대조 필요. [미검증 원자료]
- 수정안: "전이 경계 3 곳" 또는 "4 전이의 인접 경계 전부" 로 정정(캡션 동기화).

**[NOTE] R2C-12 — srcbox 가 175점 그리드의 $\bar x$ 범위를 명시하지 않음**
- config 항이 양끝에서 발산하므로 끝점 선택이 "최대 오차·config 범위"를 좌우(재계산: $[0.01,0.99]$ 이면 $[-0.37,+0.26]$, $[0.06,0.94]$ 이면 $[-0.21,+0.13]$). 재현성 위해 그리드 범위 1구절 명시 권고.

**[LOW] R2C-13 — tab:nodemap N5$+$·N9$'$ 행의 "코드 식별자" 열이 식별자가 아님**
- "$\Delta S_e$ plug-in(전자항)"·"MSMR 동형 \eqref{eq:msmr}" — 실제 심볼은 `func_dSe_molar`·`_effective_dS_rxn`·`entropy_coefficient`. 표 캡션("코드 식별자로 닫는다") 목적 대비 미완.

### 기타 정합 확인(이상 없음) [확정]
- Ch2 수치 대조: tab:ds $\Delta S^0_j=+29/0/-5/-16$ ↔ 코드 `dS_rxn` ✓ · $x$ 범위 ✓ · $\Delta H^0_{2\to1}=-FU_j+T\Delta S=-13.0$ kJ/mol(U=0.0853 V 재계산) ✓ · L182 검산값 $-45.7$(코드 `func_dSe_molar` docstring)·Ch2 MIT 서술 방향 ✓.
- `entropy_coefficient`(L556–590) = keybox 종합식 구조($\sum Q_jg_j[\Delta S^0_j/F+{\rm config}]/\sum Q_jg_j$) ✓ · `reversible_heat` $=-IT\,\partial U/\partial T$(T 한 번) = eq:qrev ✓ · `irreversible_heat` $=I(U_\oc-V)$ = eq:qrev 첫 항 ✓ · 히스 분기평균의 "γ 대칭 전제 근사" 서술(코드 docstring L564–566) ↔ Ch2 파생 D 의 1차 정확 선형화(L620–623) 정합 ✓ · 평형 경로 `func_ksi_eq` 기본 $s{=}+1$ ↔ Ch2 "평형 관계엔 항상 $s{=}+1$" ✓.
- TikZ 좌표 검산: fig:occ_config — logistic 중점 $\tfrac12$@0·포화 1·$S/R$ 최대 $\ln2$@$\theta{=}\tfrac12$·발산 화살 부호 ✓. fig:blend — 블렌드 곡선 끝값 $\pm1.5$ 레벨 일치·중점 0·step 대비 ✓. (NOTE: L544 빈 TikZ 노드 `\node[blue,above] at (2.0,1.6) {};` — 죽은 코드, 제거 권고. L461·L501 의 fig:blend 참조는 float 소스 위치보다 앞이나 [t] 배치·2-pass 해석으로 실렌더 무해 — 관찰만.)

---

## 말미 종합

**가장 약한 1곳**: **R2C-8 (완전식 config 항 $n_j$ 누락 — 문건 유도·keybox 종합식·코드 `entropy_coefficient` 3자 공통)**. 유일하게 "미래의 정상 사용(두-상 폭 피팅 $n_j\neq1$)에서 조용히 정량 오류(≈0.1 mV/K, config 몫 100%)를 내는 결함이며, 문건이 스스로 세운 전제($\partial w_j/\partial T=n_jR/F$)와 자기 식이 어긋난다.

**물리 불변 확인**: **PASS** — f$=+\sigma_d$(Ch2 무접촉)·$\Delta\mu=+sF(V-U)$(eq:muV $s$ 치환 후 대수 동치 유지, 재유도 일치)·H-1 BW 부호(eq:BW→eq:Veq_BW→eq:slope_BW 재유도, 임계 $\Omega=2RT$ ✓)·eq:qrev 부호 사슬(방전=리튬화 라벨 포함) ✓. 단 R2C-8 은 $n_j\neq1$ 일반화 시점의 파생식 결함으로, 현행 boxed 확정 판정($n{=}1$ 기준) 자체는 훼손하지 않는다.

**Coverage 선언**:
- `graphite_ica_ch2_v1.0.13.tex` L1–791 **전문**(1–461·462–791 분할 정독, 누락 0).
- `Anode_Fit_v1.0.13.py` L1–879 **전문**(1–732·733–879 분할 정독, 누락 0).
- `graphite_ica_ch1_v1.0.13.tex` — 담당 범위 한정 부분 정독: L130–219(spine·N0·부호 규약)·L2770–2849(6단계 keybox·facade 절·tab:nodemap·부호 검산 S1–S6) + 대조 grep(σ_d/s 정의 행 218·226·651–652·693–696·782·814·884·896·1015·1151·1963·1999·2783·2809).
- 수치 재계산 2본(scratchpad, 원본 무수정): 파생 A 완전식/단순식/config 독립 재구현 + $n_j$ 판별 실험.

**5줄 요약**:
1. R1 수정 5항목 전파 검사 — ① σ_d 잔재 0(PASS)·③ eq:qrev 라벨 문단 정합(PASS)은 확정, ② x̄ 는 keybox "$=Qx$"(R2C-1)·"$Q\partial x/\partial U$"(R2C-2) 2곳 미전파, ④ "부동소수점" 잔재 2곳(L523·L787), ⑤ MCMB 는 내용 정확·괄호 문체만 규범 저촉.
2. 최대 적발 = 완전식 config 항 $n_j$ 누락(R2C-8): 문건·코드 동시 결함, $n_j{=}0.5$ 수치 실험으로 0.103 mV/K 불일치 확정(정정형은 float 일치) — 두-상 폭 피팅 즉시 발현.
3. 수치 주장 재계산으로 "0.18 vs [−0.21,+0.14]" 자기모순(R2C-10)·"전이 경계 4곳"(실제 3곳, R2C-11) 적발 — 단 numverif 원자료 미열람이라 어느 쪽이 오기인지는 [미검증]으로 한정(오적발 자기표시: 모순 판정 자체는 대수 항등식 기반이라 그리드 선택으로 해소 불가).
4. facade/nodemap 신설 서술은 코드 실동작과 전 행 정합(C-04·C-14 정착) — 유일 잔여는 srcbox 의 "코드가 열적 서식 강제" 과일반화(R2C-9: `'w'` 키 T-동결 경로 실존; 'w' 를 하위호환 폴백으로만 보는 반론 여지 있어 MED 한정 — 오적발 자기표시).
5. 합계: HIGH 4(R2C-1·2·4·8) · MED 5(R2C-5·6·9·10·11) · LOW 3(R2C-3·7·13) · NOTE 2(R2C-12·빈 TikZ 노드 등) — tex/코드 무수정(검수 의견만).
