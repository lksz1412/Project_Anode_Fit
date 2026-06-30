# V1010 P2 드래프트 S3 — Ch1↔코드 coverage 매트릭스 + 누락 유도 보완 + LCO 이론 정련

> **역할**: Anode_Fit v1.0.10 P2 챕터1 9종 경쟁 드래프트 중 S3 (작업 sub). 드래프트만 — 수정 X. 범위 밖 자의 X. 허위 attribution X. 독립.
> **입력 근거**: `docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex` (1867줄) · `results/process/V1010_P1_code-audit_RESULT.md` · `results/research/broadening_w_design.md` · `results/research/radius/ORIGIN_VERDICT.md`
> **산출 위치**: `results/process/V1010_P2_draft_S3.md`
> **작성일**: 2026-07-01

---

## 산출 1. ★ Ch1↔코드 coverage 매트릭스

### P1 맵 step↔Ch1 식 전수 대조

아래 표는 P1 result(§1·§2-A)의 코드 맵 24심볼 + 12 closed-form 식을 Ch1 절·식 번호와 1:1 대조한 것이다. "Ch1 위치"는 tex 절 번호·식 레이블, "코드 줄"은 P1 result 줄근거다.

| 코드 노드(step) | 코드 식별자 (P1§1.0) | 코드 줄 | Ch1 절 | Ch1 식 | 대응 상태 |
|---|---|---|---|---|---|
| **N0** | `_direction_to_sigma`, `curve` | L483-524 | §1(sec:notation) | eq:n0map | ✔ 완전 대응 |
| **N1** | `dqdv` L408 `V_n` | L408 | §2(sec:pol) | eq:vn | ✔ 완전 대응 |
| 작업격자 | `dqdv` L410-425 | L412 | §2.2 | eq:vwork | ✔ 완전 대응(패딩·n_work 명시) |
| **N2** | `func_U_j` | L78-79 | §3(sec:center) | eq:Uj | ✔ 완전 대응(유도 포함) |
| N2 온도 의존 | `func_U_j` dS 항 | L79 | §3.2 | eq:lco-dUdT | ✔ (흑연·LCO 공용식) |
| **N3 히스 gap** | `func_dU_hys` | L133-140 | §4(sec:hys) | eq:dUhys | ✔ 완전 대응(artanh 유도 포함) |
| **N3 분기 중심** | `func_U_branch` | L143-148 | §4.3 | eq:Ubranch | ✔ 완전 대응 |
| N3 spinodal | `func_U_j_hys` (死코드) | L82-91 | §4.2 | eq:spinodal | ⚠ 死코드 — tex는 spinodal 유도 포함, 실제 분기는 `func_U_branch`(L447)가 담당 |
| **N4** | `_width`, `func_w` | L74-75, L281-284 | §5(sec:width) | eq:wbase | ✔ 완전 대응 |
| **N5** | `func_ksi_eq` | L94-97 | §5.2 | eq:xieq | ✔ 완전 대응(detailed balance 유도 포함) |
| N5+ 분포 관점 | (수식 only) | — | §5.3(sec:dist) | eq:partfn, eq:fermifn | ✔ Ch1에만 있음, 코드 구현 없음(설명 절) |
| **N6 평형 peak** | `equilibrium`, 인라인 | L350-367, L464 | §7(sec:eqpeak) | eq:eqpeak | ✔ 완전 대응(면적=Q 검산 §0 일치) |
| N6 broadening | (수식 eq:ensavg) | — | §7.3(sec:broadening) | eq:ensavg | ✔ Ch1에만 있음 — forward 설명; 코드 항 0(broadening_w_design.md §3 확정) |
| **N7 affinity** | `_resolve_lag_length` A산출 | L331 | §8.2(sec:lag) | eq:Acut | ✔ 완전 대응(z_cut 미분5% 컷 명시) |
| **N7 χ_d** | `func_chi_d` | L158-163 | §8.3 | eq:chid | ✔ 완전 대응 |
| **N7 ΔH_a^eff** | `func_dH_a_eff` | L152-155 | §8.3 | eq:dHeff | ✔ 완전 대응 |
| **N7 L_q** | `func_L_q` | L100-107 | §8.4 | eq:Lqfull | ✔ 완전 대응(Eyring·forward 지수·역방향 정규화 포함) |
| **N7 L_V** | `_resolve_lag_length` L347 | L347 | §8.4 | eq:LV | ✔ 완전 대응 |
| **N8 저역통과** | `_causal_lowpass` | L110-128 | §9(sec:tail) | eq:lowpass | ✔ 완전 대응(점화식·DC gain=1 언급) |
| **N8 peak_shape** | `dqdv` L475 | L462-475 | §9.2 | eq:peakshape, eq:branch | ✔ 완전 대응(0/0 불연속 스위치 명시) |
| **N8 충전 역전** | `dqdv` L473 | L473 | §9.3 | eq:reversal | ✔ 완전 대응 |
| **N9** | `dqdv` L477-480 | L477-480 | §10(sec:sum) | eq:sum | ✔ 완전 대응 |
| LCO 전자항 | (수식 eq:dSegate) | — | §6(sec:lco-electronic) | eq:dSe, eq:dSegate | **▲ Ch1에 있음 / 코드 구현 없음** — P1§2-E 확정(전자엔트로피 부재, `grep` no-match) |

### 누락·과잉 분류 요약

**코드에 있으나 Ch1에 없거나 약한 것(코드→Ch1 방향 누락)**

| ID | 내용 | 코드 근거 | Ch1 현황 |
|---|---|---|---|
| M1 | **n_factor 우선순위 — `'n'` 있으면 `'w'` inert** | `_n_factor` L272-278, P1§2-D | Ch1 §5.1 "폭 폴백값…`'n'`을 제거해야 활성화" 주석 있음 — 기술 수준 OK, 코드박스 문장화 가능 |
| M2 | **equilibrium은 T 스칼라 전용** — dqdv의 배열 T(V) 비지원 | L352 `_finite_pos("T",T)` P1§4-보완2 | Ch1 미언급 — §2.2 작업격자 절에 서술 가능(P4 코드개정 전까지 주의 항) |
| M3 | **꼬리 활성/비활성 경계 해상도 의존** — n_work=max(n_work_min, V_n.size×2) → lag_len_V 경계가 입력 V 점수에 종속 | L412, P1§4-보완3 | Ch1 미언급 |
| M4 | **면적=Q assert 부재** — self-test(L567-703)에 면적 회귀 가드 없음 | P1§4-보완4 | Ch1 미언급(P4 후보) |

**Ch1에 있으나 코드에 없는 것(Ch1→코드 방향, 의도적 배제)**

| ID | 내용 | Ch1 위치 | 코드 현황 |
|---|---|---|---|
| E1 | **LCO 전자 엔트로피 항** $\Delta S_{e,j}^{\mathrm{mol}}$ | §6 전체, eq:dSe, eq:dSegate | P1§2-E 확정: `grep "LCO|dS_e"` no-match. 코드 P4 구현 예정 |
| E2 | **broadening 설명 절** (eq:ensavg forward 통계 평균) | §7.3(sec:broadening) | 의도적 — broadening_w_design.md §3 "모델 항 0, 설명만" |
| E3 | **분포 관점 절** (eq:partfn·eq:fermifn) | §5.3(sec:dist) | 교육 설명용, 코드 항 없음 |
| E4 | **LCO order-disorder·MIT 2상역** Ω 적용 논의 | §4.4(sec:lco-hys) | 코드 E1과 연동, P4 대상 |

**coverage 결론**: P1 맵 12 closed-form 식 전부 Ch1에 대응(누락 0). Ch1에만 있는 항 3건(E1·E2·E3)은 의도적 미구현(P4 대상·설명용). 코드에만 있는 항 4건(M1-M4)은 Ch1 주석 수준으로 회수 가능 또는 P4 후보.

---

## 산출 2. ★ 누락 유도 보완 (물리화학 교재급, v3~v9 통합)

이 절은 Ch1 현행본에서 식→식 유도 단계가 약하거나 누락된 4개 자리를 보완한다. 각 보완은 (a) 출발→(b) 연산→(c) 중간식→(d) 박스 형식을 따르고, 코드 줄 근거를 병기한다.

---

### 2-1. 격자기체 $\mu(\theta)$ → $\bar{g}(\xi)$ 유도의 상호작용 몫 전개

**배경**: Ch1 §4(sec:hys) 식 (eq:mu)의 상호작용 항 $\Omega_j(1-2\theta)$가 $\bar{g}(\xi)$에서 어떻게 나오는지, 미분 전개를 한 단계씩 명시하지 않는다. 다음 유도가 그 틈을 채운다.

**(a) 출발** — 자리 1몰당 자유에너지(Ch1 eq:gxi):
$$\bar{g}(\xi)=g_j^0+RT\bigl[\xi\ln\xi+(1-\xi)\ln(1-\xi)\bigr]+\Omega_j\,\xi(1-\xi).$$
$g_j^0$은 선형·상수 항의 기준(공통접선 판정에 불변이라 떼어냄), $\Omega>0$이면 가운데를 위로 미는 이중우물의 씨앗이다.

**(b) 연산** — $\bar{g}$를 $\xi$로 1계 미분. 로그 몫의 미분은 $\partial/\partial\xi[\xi\ln\xi+(1-\xi)\ln(1-\xi)]=\ln\xi-\ln(1-\xi)=\ln[\xi/(1-\xi)]$이고, 상호작용 몫의 미분은 $\partial/\partial\xi[\Omega\xi(1-\xi)]=\Omega(1-2\xi)$이다(곱법칙: $\Omega[(1-\xi)+\xi\cdot(-1)]=\Omega(1-2\xi)$).

**(c) 중간식** — 평형 조건 $g_j'(\xi)=sF(V_\mathrm{eq}-U_j)$(Ch1 eq:Veq 바로 앞)에 대입:
$$\bar{g}'(\xi)=RT\ln\frac{\xi}{1-\xi}+\Omega_j(1-2\xi)=sF(V_\mathrm{eq}-U_j).$$

**(d) 박스** — $V_\mathrm{eq}(\xi)$로 이항:
$$\boxed{V_{\mathrm{eq},j}(\xi)=U_j+\frac{RT}{sF}\ln\frac{\xi}{1-\xi}+\frac{\Omega_j}{sF}(1-2\xi).}$$
이것이 Ch1 eq:Veq이며, $\Omega_j>2RT$에서 비단조($dV/d\xi=g''/sF$가 $0$을 지남)라 spinodal에서 극값이 생긴다. 코드에서 이 비단조성은 `func_dU_hys`(L133-140)의 $\Omega\le2RT$ 분기가 처리한다.

**검산**: $\Omega=0$이면 $V_\mathrm{eq}=U_j+(RT/F)\ln[\xi/(1-\xi)]$, $\xi=\frac12$에서 $V=U_j$ — 이상 격자기체의 Nernst 식. $\Omega>0$이면 상호작용 항이 $\xi=\frac12$ 부근을 0으로 눌러($1-2\xi=0$) logit 항만 남기지만, 좌우 양쪽에서 $|1-2\xi|>0$이라 추가 기울기가 붙어 비단조가 켜진다.

---

### 2-2. spinodal 점 → $\Delta U_j^\mathrm{hys}$ 닫힌 꼴 유도의 중간 단계 보강

**배경**: Ch1 §4.2(eq:hysdiff) 전개에서 "두 끝점의 logit 인자가 서로 역수"(eq:hyssub)를 쓰는 이유가 본문 한 줄로 지나간다. 아래는 그 대입을 명시적으로 밟는다.

**(a) 출발** — spinodal 값(Ch1 eq:spinodal):
$$\xi_{s,j}^\pm=\tfrac12(1\pm u_j),\quad u_j=\sqrt{1-2RT/\Omega_j}\quad(\Omega_j>2RT).$$

**(b) 연산** — logit 인자와 $(1-2\xi)$ 인자를 두 끝점에 각각 대입.

$$\frac{\xi}{1-\xi}\bigg|_{\xi_s^+}=\frac{\frac12(1+u)}{\frac12(1-u)}=\frac{1+u}{1-u},\quad
\frac{\xi}{1-\xi}\bigg|_{\xi_s^-}=\frac{\frac12(1-u)}{\frac12(1+u)}=\frac{1-u}{1+u}.$$

두 값이 서로 역수임을 확인한다: $(1+u)/(1-u)\times(1-u)/(1+u)=1$ $(\checkmark)$.

$(1-2\xi)$ 인자:
$$(1-2\xi)\big|_{\xi_s^\pm}=1-2\cdot\tfrac12(1\pm u)=\mp u.$$

**(c) 중간식** — 극대($\xi_s^-$)에서 극소($\xi_s^+$)의 전위 차, 상수항 $U_j$ 상쇄:
$$\Delta U_j^\mathrm{hys}=\frac{RT}{sF}\left[\ln\frac{1-u}{1+u}-\ln\frac{1+u}{1-u}\right]+\frac{\Omega_j}{sF}\bigl[u-(-u)\bigr].$$

첫째 괄호: $\ln[(1-u)/(1+u)]-\ln[(1+u)/(1-u)]=2\ln[(1-u)/(1+u)]=-4\,\mathrm{artanh}\,u$
($\mathrm{artanh}\,u=\frac12\ln[(1+u)/(1-u)]$ 사용). 둘째 항: $2\Omega u/sF$.

**(d) 박스** — $s=+1$ 대입:
$$\boxed{\Delta U_j^\mathrm{hys}=\frac{2}{F}\bigl[\Omega_j u_j-2RT\,\mathrm{artanh}\,u_j\bigr].}$$
이것이 Ch1 eq:dUhys이며, 코드 `func_dU_hys`(L133-140)의 `(2/F)*(Omega*u - 2*R*T*arctanh(u))` 와 1:1 대응한다.

**연속성 검산**: $\Omega_j\to2RT^+$에서 $u_j\to0^+$. $\mathrm{artanh}\,u=u+u^3/3+\cdots$이므로
$$\Omega u-2RT\,\mathrm{artanh}\,u\to2RT\cdot u-2RT\cdot(u+u^3/3+\cdots)=-\frac{2RT}{3}u^3+O(u^5)\to0.$$
$\Delta U^\mathrm{hys}\to0$이라 경계에서 연속이다($u^3\propto(T_{c,j}-T)^{3/2}$, $T_{c,j}=\Omega_j/(2R)$).

---

### 2-3. logistic 에서 equilibrium peak 로 — 연쇄율과 면적 보존

**배경**: Ch1 §7(sec:eqpeak) eq:belliden에서 종 항등식 $d\xi_\mathrm{eq}/dz=\xi_\mathrm{eq}(1-\xi_\mathrm{eq})$이 나오고 연쇄율로 peak 식이 닫히는 부분이 한 단락이다. 아래는 면적 보존이 왜 $\int=Q_j$인지를 적분변수 치환으로 유도한다.

**(a) 출발** — 평형 peak 면적(전하 보존식에서):
$$\int_{V_\mathrm{lo}}^{V_\mathrm{hi}}\left(\frac{dQ}{dV}\right)^\mathrm{eq}_j\,dV=Q_j\int_{V_\mathrm{lo}}^{V_\mathrm{hi}}\frac{\xi_{\mathrm{eq},j}(1-\xi_{\mathrm{eq},j})}{w_j}\,dV.$$

**(b) 연산** — 치환: $d\xi_\mathrm{eq}=(\sigma_d/w_j)\xi_\mathrm{eq}(1-\xi_\mathrm{eq})\,dV$이므로
$$\frac{\xi_\mathrm{eq}(1-\xi_\mathrm{eq})}{w_j}\,dV=\sigma_d\,d\xi_\mathrm{eq}.$$

전위 $V_\mathrm{lo}\to V_\mathrm{hi}$에 걸쳐 방전($\sigma_d=+1$)에서 $\xi_\mathrm{eq}$는 $0$에서 $1$로 단조 증가한다.

**(c) 중간식** — 적분변수를 $V$에서 $\xi_\mathrm{eq}$로 전환:
$$Q_j\int_0^1 d\xi_\mathrm{eq}=Q_j\cdot1=Q_j.$$

**(d) 박스** — 면적 보존:
$$\boxed{\int\left(\frac{dQ}{dV}\right)^\mathrm{eq}_j\,dV=Q_j.}$$
이것이 P1§0의 독립 수치적분 1.000000과 일치한다. `use_w_eff` 제거(L7)의 근거 — 분모 $w$와 $\xi_\mathrm{eq}$ 폭이 같은 $w_j$여야 치환이 성립하고 면적이 보존된다. `w_eff`가 있으면 분모 폭이 달라져 적분값이 $Q_j$에서 이탈한다(v1.0.9 이전 버그). `_causal_lowpass`의 DC gain=1(검토1 확정)이 꼬리의 면적 보존에도 같은 원리를 적용한다.

---

### 2-4. Lq 전압축 환산 $L_V$ — 이산 미분과 연속해의 연결

**배경**: Ch1 §8.4(eq:LV)에서 $L_V=|\mathrm{d}V/\mathrm{d}q|_{q_a}\cdot L_q$로 정의되지만, 이 환산이 이산 격자에서 peak_shape $=(\xi_\mathrm{eq}-\xi_\mathrm{lag})/L_V$를 물리적으로 왜 쓰는지의 유도가 빠져 있다. 아래는 연속 ODE 해 → 이산 차분 → peak 식의 사슬을 밟는다.

**(a) 출발** — 연속 지연 방정식(Ch1 eq:Lq):
$$\frac{d\xi_j}{dt}=k_j(\xi_{\mathrm{eq},j}-\xi_j),\quad L_{q,j}=\frac{|I|}{Q_\mathrm{cell}\,k_j}.$$
정전류에서 $q=|I|t/Q_\mathrm{cell}$이므로 $t$ 대신 용량 좌표 $q$를 쓰면
$$\frac{d\xi_j}{dq}=\frac{1}{L_{q,j}}(\xi_{\mathrm{eq},j}-\xi_j).$$

**(b) 연산** — $\mathrm{d}V/\mathrm{d}q$를 곱해 전압축으로:
$$\frac{d\xi_j}{dV}=\frac{d\xi_j}{dq}\cdot\frac{dq}{dV}=\frac{1}{L_{q,j}}\cdot\frac{1}{|\mathrm{d}V/\mathrm{d}q|}\cdot(\xi_\mathrm{eq}-\xi)=\frac{\xi_\mathrm{eq}-\xi}{L_V},\quad L_V\equiv\Big|\frac{dV}{dq}\Big|_{q_a}L_{q,j}.$$

**(c) 중간식** — 보존식 $\mathrm{d}Q/\mathrm{d}V=C_\mathrm{bg}+\sum_j Q_j\,\mathrm{d}\xi_j/\mathrm{d}V$에 대입하면 전이 $j$의 기여가
$$Q_j\frac{d\xi_j}{dV}=Q_j\frac{\xi_\mathrm{eq}-\xi}{L_V}.$$

이산 격자에서 지수 커널 점화식(Ch1 eq:lowpass)이 $\xi_j\approx\xi_\mathrm{lag}$이므로

**(d) 박스** — peak_shape:
$$\boxed{\mathrm{peak\_shape}=\frac{\xi_\mathrm{eq}-\xi_\mathrm{lag}}{L_{V,j}}}$$
이것이 Ch1 eq:peakshape이며 코드 L475이다. **$L_V$가 컷점 상수임에 주의**: $\mathrm{d}V/\mathrm{d}q|_{q_a}$는 컷점 $q_a$에서 한 번 동결되므로(코드 `dVdq_qa`, L347), $L_V$는 전이당 한 스칼라다. 이것이 P1§2-B S6의 "운영상 실현 미분 $\partial\ln L_q/\partial V=0$"의 의미다 — 컷점에서 동결하지 않으면 격자마다 $L_V$를 재평가해야 하고 전이당 한 길이라는 구조가 깨진다.

**면적 검산**: $L_V$로 나눈 peak_shape의 적분이 $Q_j$에 얼마나 근접하는지는 P1§0 수치적분 결과 — $L_V=0.02$서 0.4997($\approx0.50$, 두 전이 가중 각 0.25+0.25), 큰 $L_V$서 격자 경계 손실. `_causal_lowpass` DC gain=1 원리와 일관.

---

### 2-5. v3~v9 통합 — 폭 $w_j$ 이중지위의 물리적 전개

**배경**: broadening_w_design.md §2의 "단상/두-상 이중지위"와 Ch1 §5.1·§7.3의 서술을 v3~v9의 발전 맥락에서 물리 교재 수준으로 정련한다.

#### 단상($\Omega_j\le2RT$)에서 $w_j$의 의미 — 평형 예측

등온선의 기울기 $\mathrm{d}\xi_\mathrm{eq}/\mathrm{d}V$를 중심 $V=U_j^d$에서 평가하면(Ch1 eq:belliden·연쇄율):
$$\left.\frac{d\xi_\mathrm{eq}}{dV}\right|_{V=U_j^d}=\frac{\sigma_d}{w_j}\xi_\mathrm{eq}(1-\xi_\mathrm{eq})\bigg|_{\xi=1/2}=\frac{\sigma_d}{4w_j}.$$

따라서 중심에서의 기울기가 $1/(4w_j)$이고, 그 역수 $4w_j$가 "반치폭" 척도(logistic의 $\pm\ln 3$ 점에서 폭 $\approx 2.2\,w_j$)다. **단상에서는 이 $w_j=n_jRT/F$가 실측 등온선 폭을 예측하는 검증 가능한 양이다** — Levi–Aurbach 1999(DOI 10.1016/S0013-4686(99)00202-9)의 Frumkin/정규용액 등온선 결과와 같다.

#### 두-상($\Omega_j>2RT$)에서 $w_j$의 의미 — 현상학적 피팅 폭

평형 단일 입자의 자유에너지가 이중우물($g_j''>0$ 구간 없음)이면, Maxwell 공통접선이 plateau 전위 $U_j^\mathrm{flat}$을 한 값으로 수렴시키고, 이상적 단일 입자의 $\mathrm{d}q/\mathrm{d}V\to\infty$ (delta 함수에 근접)다. **그러나 실측은 유한 폭의 종**이며, 그 종을 만드는 세 출처가 §7.3(sec:broadening)에 정리된다:

1. **유한율속 비대칭 꼬리** — 단일 입자 유한 전류에서 과전압 $\eta(t)$가 변하며 peak을 한쪽으로 밀고 꼬리를 늘인다. 이것이 코드 N7/N8의 $(\xi_\mathrm{eq}-\xi_\mathrm{lag})/L_V$이며 $|I|\to0$에서 소멸한다(Fly·Chen 2020, DOI 10.1016/j.est.2020.101329).
2. **내재 $RT/F$ 폭** — plateau 양끝 단상 꼬리가 까는 $\sim RT/F$ floor. 전류 무관.
3. **앙상블 통계역학** — $N$-입자 계에서 (iii-a) Dreyer 순차전환이 plateau 구조(공통 전위)를 만들고, (iii-b) apparent-$U=U_j+\eta$의 입자간 $\eta$ 산포 $\rho(U_\mathrm{app})$가 그 평형 delta를 종으로 펼친다. **평형 중심 $U_j$는 입자 무관 상수**이고(Park 2021 GITT, DOI 10.3390/ma14164683), 분포하는 것은 $\eta$다.

이 세 출처가 합쳐 만드는 종의 폭을 $w_j$ 하나로 흡수하는 것이 **현상학적 피팅 폭** 지위다. 수식으로는 식 eq:wbase $w_j=n_jRT/F$가 그대로이지만, 두-상에서는 그 $n_j$가 평형이 정하는 값이 아니라 데이터가 정하는 값이다 — $n_j$를 피팅 자유변수로 두고 측정 폭에 맞춘다.

**같은 식 eq:wbase, 다른 지위**: 코드는 분기 없이 항상 `func_w(T,n)*n=nRT/F`를 쓴다(`_width`, L281-284). 지위 전환은 코드 분기가 아니라 $\Omega_j$ 값이 $2RT$ 기준으로 정한다 — 이것이 Ch1 §5.1의 "이중지위" 선언의 핵심이다.

---

## 산출 3. ★ LCO 이론 정련 (교재급, 코드 P4 예고)

이 절은 Ch1에 이미 있는 LCO 이론(§1.2·§3.2·§4.4·§5+·§6·§7.4·§9.2·§9.3 H)을 P4 코드 구현을 위한 교재급 정련으로 압축한다. 초점은 (i) LCO dQ/dV의 세 봉우리 평형 구조, (ii) 전자 엔트로피 $\Delta S_e$의 물리·식·단위·코드 구현 경로, (iii) 흑연과의 대조다.

---

### 3-1. LCO dQ/dV — 세 봉우리의 평형 구조 (코드 P4 예고)

흑연의 staging 전이 4건이 코드 `GRAPHITE_STAGING_LIT`에 대응하듯, LCO 하프셀(coin, $\le4.2$–$4.5$ V vs Li)은 세 전이를 남긴다. 이 세 봉우리는 **같은 forward 골격**(N0–N9)으로 그린다 — 파라미터만 교체하고 N5+ 전자항 하나를 더한다.

**LCO 전이 초기값** (Ch1 tab:lco-staging, P4 `LCO_STAGING_LIT` 구현 대상):

| 전이 | $U_j$ [V vs Li] | $x$ 범위 | 성격 | $\Delta S_{\mathrm{rxn},j}^\mathrm{cat}$ 특징 |
|---|---|---|---|---|
| T1 (MIT) | $\sim3.90$ | 0.94–0.75 | insulator→metal | config + $\Delta S_e$ 게이트 ON |
| T2 (OD-a) | $\sim4.05$ | $\approx0.55$ | hex→monoclinic | config 주도($\approx0.47$ J/K·mol) |
| T3 (OD-b) | $\sim4.17$–4.20 | $\approx0.48$ | monoclinic→hex | config($\approx1.49$ J/K·mol) |

흑연이 $U\approx0.085$–0.21 V(음극 vs Li)에 있는 것과 달리, LCO는 $\sim3.9$–4.2 V (양극 vs Li)이다. **양극 부호 규약**: 방전($\sigma_d=+1$)이 LCO 입장에서 리튬화($x\uparrow$, Co$^{4+}$→Co$^{3+}$)이고, 충전($\sigma_d=-1$)이 탈리튬화($x\downarrow$)다. 이 방향 정의가 흑연과 $\sigma_d$ 기호를 공유한다.

**평형 peak 식(전극 불변)**: Ch1 eq:eqpeak
$$\left(\frac{dQ}{dV}\right)^\mathrm{eq}_j=Q_j\frac{\xi_{\mathrm{eq},j}(1-\xi_{\mathrm{eq},j})}{w_j}$$
에서 LCO도 위치=$U_j^d$, 높이=$Q_j/(4w_j)$, 면적=$Q_j$의 세 양이 똑같이 읽힌다. LCO의 세 전이는 모두 $\Omega_j>2RT$의 두-상이라 폭은 §2-5의 현상학적 피팅 폭이다.

**MSMR 동형**(Ch1 eq:msmr): Paul et al. 2024(DOI 10.1149/2754-2734/ad7d1c)의 양극 logistic 합 구조 $x_j=X_j/[1+\exp(f(U-U_j^0)/\omega_j)]$가 Ch1 eq:xieq와 구조 동형이다 — 대응: $X_j\leftrightarrow Q_j$, $U_j^0\leftrightarrow U_j^d$, $\omega_j\leftrightarrow w_j$, $f\leftrightarrow-\sigma_d$. 곧 코드 구조 변경 0으로 LCO에 적용된다.

---

### 3-2. 전자 엔트로피 $\Delta S_{e,j}$ — Sommerfeld 유도에서 코드 plug-in 경로까지 (교재급)

#### 3-2-1. 왜 흑연엔 없고 LCO엔 있나

삽입 반응의 전체 엔트로피 변화 = config + vib + electronic 세 자유도의 합이다. **흑연**은 반금속·전도성이 충방전 중 크게 변하지 않아($g(E_F)$ 변화 미미) 전자항을 무시할 수 있다. **LCO**는 $x=1$(LiCoO$_2$, Co$^{3+}$, $t_{2g}^6$ low-spin, 닫힌 껍질 → **절연체**, $g(E_F)\approx0$)에서 $x<0.94$로 내려가면 Co$^{4+}$ 정공이 $t_{2g}$ 띠에 생겨 **금속**($g(E_F)\to$유한)으로 전환한다 — 이 절연체→금속 전이(MIT)가 $x\approx0.75$–$0.94$의 2상역에서 일어나며, 그 구간에서만 전자 분포 변화가 엔트로피에 들어온다(Ménétrier et al. 1999, DOI 10.1039/a900016j; Motohashi et al. 2009, DOI 10.1103/PhysRevB.80.165114).

#### 3-2-2. Fermi–Dirac에서 Sommerfeld 전자 엔트로피로 — 단계별 유도

**(a) 출발** — 전도 전자의 Fermi–Dirac 분포:
$$f(E)=\frac{1}{1+e^{(E-E_F)/k_BT}}.$$
구조: §5.3(sec:dist)의 리튬 자리 점유 eq:fermifn과 **동형**이다 — 입자 0/1 배타 점유가 공통이고, 자리만 "흡착 자리"에서 "전자 에너지 준위"로 바뀐다.

**(b) 연산** — 분포의 엔트로피. 모든 준위의 점유 정보 엔트로피는
$$S_e=-k_B\sum_E [f(E)\ln f(E)+(1-f(E))\ln(1-f(E))].$$
축퇴 전자기체($k_BT\ll E_F$)에서 적분에 기여하는 범위는 $E_F$ 근방 열폭 $\sim k_BT$에 한정된다. **Sommerfeld 근사**: 이 좁은 창에서 $g(E)\approx g(E_F)$(상태밀도를 $E_F$ 값으로 동결). 이 동결의 정당성은 창 폭($\sim k_BT$)이 $E_F$에 비해 작고(축퇴 조건) 그 안에서 $g(E)$의 에너지 의존이 선도 차수로 무시되기 때문이다.

**(c) 중간식 1** — 전자 비열. 내부에너지 $U_e=\int E\,g(E)f(E)\,dE$를 $T$로 미분하고 Sommerfeld 표준 적분 $\int(-\partial f/\partial E)(E-E_F)^2\,dE=(\pi^2/3)(k_BT)^2$을 대입하면:
$$C_e=\frac{\partial U_e}{\partial T}=\frac{\pi^2}{3}k_B^2T\,g(E_F)\quad[T\text{-선형 전자 비열, 금속 표준 결과}].$$

**(c) 중간식 2** — 엔트로피. $C_e$를 $S_e=\int_0^T(C_e/T')\,dT'$로 적분:
$$\frac{C_e}{T'}=\frac{\pi^2}{3}k_B^2\,g(E_F)=\text{const},\quad \Rightarrow\quad S_e=\int_0^T\frac{\pi^2}{3}k_B^2\,g(E_F)\,dT'.$$

**(d) 박스** — 자리당 전자 엔트로피:
$$\boxed{S_e(T,x)=\frac{\pi^2}{3}k_B^2\,T\,g(E_F,x).}$$
세 구성요소의 신뢰 등급:
- **식의 함수형** $S_e=(\pi^2/3)k_B^2T\,g(E_F)$: 교과서 Sommerfeld 표준 결과 — **tier A**.
- **완전 metal($x=0$) 단일 anchor** $g(E_F)\approx13$ e/eV/atom: 측정된 끝점(Motohashi 2009) — **tier A(한 점만)**.
- **MIT 천이 연속 곡선** $g(E_F,x)$: 1차 문헌 부재(갭 G2) — **tier 없음, 모델 가정 필요**(§3-2-4).

**★온도 의존**: $S_e\propto T$라 삽입당 전자 엔트로피 $\Delta S_{e,j}\propto T$이다. 이것이 config·vib(상수 $\Delta S_\mathrm{rxn}$)와 구분되는 전자항의 **식별 신호**다 — 다온도 피팅에서 $\partial U_j/\partial T$의 기울기 자체가 $T$에 선형이면(위치 이동은 $\propto T^2$) 전자항이 있는 것이다.

#### 3-2-3. 삽입 기준 전이당 전자 엔트로피 — 부호·단위 규약

forward 슬롯 $\Delta S_{\mathrm{rxn},j}$는 **삽입 기준**($x\uparrow$ 당 변화)의 몰당[J/(mol·K)] 양이다 — 흑연 stage $2\to1$에 $\Delta S_\mathrm{rxn}=-16$ J/(mol·K)이 들어가는 바로 그 슬롯이다.

**자리당→몰당 환산**: 식 eq:Se는 자리당($k_B^2$ 차원). Avogadro 수를 곱해 몰당으로:
$$\Delta S_{e,j}^{\,\mathrm{mol}}(x,T)=N_A\frac{\partial S_e}{\partial x}\bigg|_T=\frac{\pi^2}{3}Rk_BT\frac{\partial g(E_F,x)}{\partial x}\quad[\text{J/(mol·K)};\;N_Ak_B^2=Rk_B].$$
$g$의 단위가 e/eV이면 eV→J 환산($1.602\times10^{-19}$)도 함께.

**부호 규약** — 삽입($x\uparrow$)으로 금속→절연체라 $g(E_F)$가 $g_\mathrm{max}\to0$으로 **감소**하므로 $\partial g/\partial x<0$, 따라서 $\Delta S_{e,j}=N_A(\pi^2/3)k_B^2T\,\partial g/\partial x<0$이다. 즉 MIT 구간에서 전이당(삽입당) 전자 엔트로피는 **음의 골**이고, 탈리튬화 시 방출되는 봉우리는 $|\Delta S_{e,j}|=-\partial S_e/\partial x>0$이다.

이것이 흑연 $\Delta S_\mathrm{rxn}<0$(stage $2\to1$)과 **같은 부호 관례**로 슬롯에 들어가는 이유다.

**★이중계산 금지**: 봉우리 내부의 config 조성 의존 $R\ln[(1-\xi)/\xi]$는 logistic eq:xieq이 이미 자동 생성한다 — 식 eq:lco-decomp의 $\Delta S_j^\mathrm{config}$ 슬롯에는 봉우리 **중심 표준값**만 넣어야 하고, MIT 구간의 전자 기여는 $\Delta S_{e,j}^\mathrm{mol}$ 슬롯이 별도로 담는다. 두 항이 서로 다른 자유도(리튬 배열 vs 전자 밴드점유)라 통계역학적으로 근사 직교하여 단순 가산이 허용된다(직교 가정의 한계는 MIT 근방 리튬-전자 결합 잔차로, 선도 차수에서 무시).

#### 3-2-4. $g(E_F,x)$의 MIT-logistic 게이트 — 코드 P4 구현 형식

연속 곡선 $g(E_F,x)$가 1차 문헌에 없으므로(갭 G2) **logistic 게이트로 근사**한다:

$$\boxed{g(E_F,x)\approx g_\mathrm{max}\left[1-\sigma\!\left(\frac{x-x_\mathrm{MIT}}{\Delta x_\mathrm{MIT}}\right)\right],\quad g_\mathrm{max}=13\text{ e/eV},\;x_\mathrm{MIT}\approx0.85,\;\Delta x_\mathrm{MIT}\approx0.05.}$$

게이트 미분($\sigma'(z)=\sigma(z)(1-\sigma(z))$, 연쇄율)을 eq:dSemolar에 대입하면:

$$\boxed{\Delta S_{e,j}^{\,\mathrm{mol}}(x,T)=-\frac{\pi^2}{3}Rk_BT\frac{g_\mathrm{max}}{\Delta x_\mathrm{MIT}}\sigma\!\left(\frac{x-x_\mathrm{MIT}}{\Delta x_\mathrm{MIT}}\right)\!\left[1-\sigma\!\left(\frac{x-x_\mathrm{MIT}}{\Delta x_\mathrm{MIT}}\right)\right]\;<0.}$$

(앞의 음부호가 삽입 기준 $\Delta S_{e,j}<0$을 식 자체로 못박는다. $\sigma(1-\sigma)\le1/4$라 $x_\mathrm{MIT}$에서 골이 가장 깊다.)

**P4 코드 plug-in 경로**:
```python
# P4 구현 예시 (T1 전이에서만 활성)
def func_dS_e_mol(x, T, g_max=13.0, x_mit=0.85, dx_mit=0.05,
                  R=8.314, kB=1.38e-23, eV_to_J=1.602e-19):
    """삽입 기준 전이당 전자 엔트로피 [J/(mol K)], MIT-logistic 게이트.
    반환값 < 0 (MIT 구간 삽입 기준 음의 골).
    g_max 단위 e/eV → eV_to_J 환산 포함."""
    z = (x - x_mit) / dx_mit
    sig = 1.0 / (1.0 + np.exp(-z))
    dg_dx = -(g_max / dx_mit) * sig * (1.0 - sig)  # e/eV, <0
    dg_dx_J = dg_dx * eV_to_J  # J/atom
    # 자리당: (pi^2/3)*kB^2*T*dg_dx_J; 몰당: ×N_A = ×R/kB
    return (np.pi**2 / 3.0) * R * kB * T * dg_dx_J / kB  # = (pi^2/3)*R*kB*T*dg_dx_J/kB
    # = (pi^2/3)*R*T*dg_dx_J [J/(mol K)]
```
이 함수의 반환값이 T1 전이의 $\Delta S_{\mathrm{rxn},1}^\mathrm{cat}$ 슬롯에 더해진다 — T2·T3는 이 항 없이 config+vib만.

**크기 검산**: 완전 metal 한계에서 $S_e/k_B=(\pi^2/3)(k_BT)g(E_F)\approx3.29\times0.0259\text{ eV}\times13/\text{eV}\approx1.1\,k_B$/atom($T=300$ K). O3 부분몰 차 $\approx0.18\,k_B$/atom(Reynier 2004, DOI 10.1103/PhysRevB.70.174304, tier B) — 같은 자릿수($\checkmark$). config의 O3 $\Delta S(>1/2$ 지배, tier A)보다 **작지만**, MIT 2상역에서만 켜지는 **게이트** 신호라 config 단독으로 대체 불가(Teichert et al. 2024, DOI 10.1016/j.jmps.2024.105727, tier A).

**★단위 주의(P4 구현 필수)**: forward 슬롯 $\Delta S_{\mathrm{rxn},j}$는 J/(mol·K)이다. 자리당 식 eq:dSe의 $k_B^2$ 차원($k_B^2\approx1.9\times10^{-46}$ J²/K²)을 그대로 쓰면 $\sim10^{23}$배 과소가 된다 — **반드시 $N_A$ 배 환산**(eq:dSemolar)이 필요하다. 위 구현 예시에서 `R*kB*T*dg_dx_J/kB = R*T*dg_dx_J`이 몰당 환산을 자동으로 포함한다($N_Ak_B^2=Rk_B$이므로 $k_B$가 약분).

---

### 3-3. LCO $\Delta S_{\mathrm{rxn},j}^\mathrm{cat}$ 분해 — config + vib + electronic 정합

식 eq:lco-decomp:
$$\Delta S_{\mathrm{rxn},j}^\mathrm{cat}(x,T)=\Delta S_j^\mathrm{config}+\Delta S_j^\mathrm{vib}+\Delta S_{e,j}^{\,\mathrm{mol}}(x,T).$$

| 성분 | 물리 기원 | T 의존 | 코드 슬롯 | 이중계산 방지 |
|---|---|---|---|---|
| config | 리튬 자리 배열 엔트로피 | 상수($x$만) | $\Delta S_{\mathrm{rxn},j}$ 중심 표준값만 | logistic이 내부 조성 의존 자동 생성 — 중복 금지 |
| vib | phonon baseline | 상수 | 동일 슬롯 | 흑연과 동형 |
| electronic | MIT 게이트($g(E_F)$ 변화) | $\propto T$ | T1만 추가 | config와 직교(다른 자유도), 별도 슬롯 |

흑연에서 $\Delta S_{e,j}^\mathrm{mol}=0$이고 슬롯이 config+vib만이었던 것이 LCO T1에서 세 번째 성분이 켜지는 것이다. T2·T3는 전자항 미발현(전도 전자 변화 없음) — config+vib만.

$\partial U_j/\partial T=\Delta S_{\mathrm{rxn},j}^\mathrm{cat}/F$의 경로(eq:lco-dUdT)는 흑연과 동일하다:

$$U_j(T)=\frac{-\Delta H_{\mathrm{rxn},j}+T\,\Delta S_{\mathrm{rxn},j}^\mathrm{cat}(x,T)}{F}.$$

T1의 경우 $\Delta S_{\mathrm{rxn},1}^\mathrm{cat}$에 전자항이 $\propto T$로 들어오므로 $U_1(T)$ 이동이 $\propto T^2$다 — 다온도 dQ/dV에서 T1 봉우리 위치의 **이동률 $\partial U_1/\partial T$가 $T$에 선형**으로 커지는 것이 전자항의 직접 관측 신호다.

---

### 3-4. 흑연↔LCO 대조 요약 — "같은 골격, 다른 전극"

| 항목 | 흑연 음극 | LCO 양극 |
|---|---|---|
| 전위 범위 | $\sim0.085$–0.21 V vs Li | $\sim3.90$–4.20 V vs Li |
| 방전 방향 | 탈리튬화($x\downarrow$) | 리튬화($x\uparrow$) |
| staging 전이 수 | 4 (LiC$_6$·LiC$_{12}$·2L·3L) | 3 (MIT·OD-a·OD-b) |
| 두-상 전이 | LiC$_{12}$(2L→2), LiC$_6$(2→1) | T1·T2·T3 전부 |
| 전자 엔트로피 | 없음($g(E_F)$ 변화 미미) | T1 MIT 구간에서 필수(MIT 게이트) |
| $\Delta S_\mathrm{rxn}$ 성분 | config + vib | config + vib + electronic(T1만) |
| $\partial U_j/\partial T$ 의존 | 선형($\Delta S$ 상수) | T1은 비선형($\propto T^2$ — 전자항) |
| 코드 변경 | ground truth | **파라미터 교체 + 전자항 plug-in 1건** |
| 구조 변경 | — | 0 (MSMR 동형 eq:msmr) |
| 초기값 출처 | lit(dahn·ohzuku) | Xia 2007·Reynier 2004·Motohashi 2009 |

**코드 P4 작업 목록** (Ch1 범위 내, 확정):
1. `LCO_STAGING_LIT` dict 생성 — tab:lco-staging 3 전이, 동일 키 구조.
2. `func_dS_e_mol(x, T, ...)` 구현 — eq:dSemolar·eq:dSegate 기반.
3. T1 전이에서 `dS_rxn = dS_config + dS_vib + func_dS_e_mol(x, T)` plug-in.
4. `LCO_STAGING_LIT` self-test — T1 위치 $U_1(298)$가 $\sim3.90$ V 근방, $\partial U_1/\partial T$ 부호 양수(swiderska-mocek 2019 +0.83 mV/K 스케일).
5. P1§4 보완2(equilibrium T 스칼라 전용) 확인 — LCO 다온도 피팅은 dqdv 경로 전용.

---

## 품질 메모 (추정·근거 분류)

- [확정] 코드 줄 근거 있는 모든 대응 (P1 result §1·§2-A·§0)
- [확정] LCO $g(E_F)\approx13$ e/eV anchor (Motohashi 2009, tier A)
- [확정] $\Delta S_{e,j}<0$ 부호 (삽입 기준 $\partial g/\partial x<0$)
- [확정] Sommerfeld 함수형 (교과서 tier A)
- [추정] $x_\mathrm{MIT}\approx0.85$, $\Delta x_\mathrm{MIT}\approx0.05$ 초기값 (MIT 2상역 중앙·폭 읽음, 데이터 override 전제)
- [추정] LCO apparent-U 절대 mV 분산 (ORIGIN_VERDICT §2 "추정", 직접 실측표 미발견)
- [근거 미발견] $g(E_F,x)$ 연속 곡선 (갭 G2, logistic 게이트는 모델 가정)
- [추정] 흑연 4L↔3L solid-solution 판단 (rsc2021 tier B 비교인용)

---

*작성: 2026-07-01 | S3 드래프트 | 드래프트만 — 수정 X, 범위 밖 자의 X, 허위 attribution X*
