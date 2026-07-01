# Fable 재검 챕터1(Ch1) 내용 감사 C-1 — L1~683

- 대상: `Claude/docs/v1.0.11/graphite_ica_ch1_v1.0.11.tex` L1~683 (서론·기호·eq:n0map·N1 분극·N2 평형중심·N3 히스/spinodal + sec:lco-map·sec:lco-center, sec:hys 본문 끝(fig:hysloop)까지).
- 방법: head→tail 전문 정독(부분 read 3회, 1-250·251-500·501-683, 빈틈 없음) + **물리 독립 재유도**(문건 서술을 그대로 베끼지 않고 Gibbs 자유에너지 정의부터 손으로 재전개) + **실행 기반 검산**(Python/SymPy 스크립트로 모든 boxed 식·수치 예시·그림 내 좌표값을 독립 재계산). 검증 스크립트:
  - `C:\Users\lksz1\AppData\Local\Temp\claude\d--Projects\f45f576c-1efc-4f50-8591-1f84bb7d7f39\scratchpad\fable_c1_audit.py` (SymPy 기호 재유도)
  - `C:\Users\lksz1\AppData\Local\Temp\claude\d--Projects\f45f576c-1efc-4f50-8591-1f84bb7d7f39\scratchpad\fable_c1_audit2.py` (수치 재계산 — branch-cut 문제 없는 real-valued 버전)
- 등급 스케일: CRITICAL(치명, 물리·부호 오류로 결과 왜곡) / HIGH(중대, 재유도 실패·논리 단절) / MEDIUM(중간, G-follow·표기 불완전·논리 다리 생략이나 최종식은 옳음) / LOW(경미, 표기 중의성) / PASS(독립 재유도로 무결 확인).

---

## 결함 목록

### [MEDIUM-1] 위치: L216–255(기호표) vs L432, L438, L444, L585–609(사용처) — 기호 "$s$" 가 규약표에 없음
**무엇이.** N2(§평형 중심, eq:eqcond)부터 등장하는 고정 부호 상수 $s$($s$는 항상 $+1$, "방전 규약"으로 텍스트에 산문 설명만 있음)가 L216–255 의 마스터 "기호와 규약" longtable 에 행이 없다. 반면 방향에 따라 실제로 $\pm1$ 로 바뀌는 $\sigma_d$ 는 표에 등재돼 있다(L219). $s$ 는 이후 eq:Veq, eq:hysdiff, eq:dUhys 전체(그리고 범위 밖이지만 N4–N6 의 eq:width, eq:branch 등)에서 계속 재사용되는 문건 전역 상수인데, 신규 기호가 나올 때마다 지키기로 한 규약표 원칙(L216 "기호(코드 식별자)" 표)에서 이 심볼만 누락됐다.
**왜(재유도/근거).** $s$ 와 $\sigma_d$ 는 둘 다 "$V-U$" 꼴 인자 앞에 붙는 부호라는 점에서 시각적으로 거의 같은 역할처럼 보이지만, $\sigma_d$ 는 실행시 방향에 따라 $\pm1$ 로 바뀌는 코드 변수이고 $s$ 는 $U_j$ 정의 관례상 **항상 고정된 $+1$**(코드에는 아예 나타나지 않고, boxed 식 단계에서 이미 $s=1$ 대입돼 사라진다 — 실제로 \code{func\_dU\_hys}, \code{func\_U\_branch} 코드박스(L620, L638)에는 $s$ 가 전혀 없다). 두 기호가 표기상 구분되지 않은 채 산문 각주 하나로만 갈리는 것은 "부호 규약(★최우선 결함 클래스)"라고 문건 스스로 L210 에서 선언한 항목과 정확히 같은 종류의 리스크다. 코드까지 내려가면 소멸하는 심볼이라 물리적 오류는 아니지만(PASS 항목 참조), G-follow(독자가 따라가기)·G-usable("이 문건만으로 코드 재현" 목표, L138) 관점에서 실제 걸림돌이 된다.
**수정 방향.** L216–255 표에 "$s$ (내부 유도 전용, 코드 미대응) — 항상 $+1$; $U_j$ 정의의 부호 관례, 실행시 바뀌는 $\sigma_d$ 와 별개" 행 1개 추가. 또는 L432 최초 등장 시 "이 $s$ 는 §\ref{sec:notation} 의 $\sigma_d$ 와 다른 고정 상수다" 를 명시적으로 1문장 추가.
**4-tier.** 확정(표 vs 본문 대조로 직접 확인 가능한 누락).

### [MEDIUM-2] 위치: L535–540(eq:gxi) → L585–588(eq:Veq) — $\theta\to\xi$ 치환에서 1차항 제거가 1계 미분(V_eq)에도 그대로 넘어가는 다리가 생략
**무엇이.** L535 "1차(직선) 몫과 상수는 공통 접선 판정에 불변이라 떼어내고" 라는 근거로 $\mu^0\theta$ 선형항을 $g_j^0$(상수로 서술)에 흡수해 eq:gxi 를 얻는다. 이 근거는 **2계 미분**(eq:gpp, spinodal 판정)에는 완전히 타당하다 — 아핀항의 2계 미분은 항상 0이므로. 그런데 바로 다음 절(L585–588)에서 똑같이 선형항이 빠진 $g_j(\xi)$ 를 **1계 미분**($g_j'(\xi)$)에 재사용해 곧장 $sF(V_\eq-U_j)$ 와 등치시킨다. 1계 미분에서는 선형항을 지우는 게 공짜가 아니다 — $\mu^0\theta$ 를 $\xi=1-\theta$ 로 바꾸면 $\mu^0(1-\xi)=\mu^0-\mu^0\xi$ 가 되어 **$\xi$ 에 대해 선형인 항($-\mu^0\xi$)이 실제로 남는다**. 문건은 이 항이 사라지는 이유(왜 1계 미분 결과에 영향을 주지 않는지)를 명시하지 않는다.
**왜(재유도/근거, 독립 재유도로 확인).** 손으로 직접 다시 유도했다: $f(\theta)\equiv RT[\theta\ln\theta+(1-\theta)\ln(1-\theta)]+\Omega\theta(1-\theta)$(선형항 제외한 부분)는 $\theta\leftrightarrow1-\theta$ 치환에 대해 **우함수**다($f(1-\theta)=f(\theta)$, 두 항 모두 자리바꿈에 대칭). 이로부터 $f'(1-\xi)=-f'(\xi)$(우함수의 도함수는 기함수) 라는 **비자명한 항등식**이 성립한다. eq:mu 로부터 $\mu_\mathrm{Li}(\theta)-\mu^0=f'(\theta)$ 이므로, $\xi=1-\theta$ 대입 시 $\mu_\mathrm{Li}(\theta_\eq)-\mu^0=f'(1-\xi)=-f'(\xi)$. 이를 eq:eqcond($\mu_\mathrm{Li}(\theta_\eq)=\mu^0-sF(V_\eq-U_j)$)와 결합하면 $-f'(\xi)=-sF(V_\eq-U_j)$, 곧 $V_\eq=U_j+f'(\xi)/(sF)$ — **정확히 eq:Veq 그대로**, 선형항 기여가 정확히 상쇄돼 사라진다. 즉 **최종 결과(eq:Veq)는 옳다** — 다만 이 상쇄가 $f$ 의 대칭성이라는 한 단계를 더 거쳐야 성립하는데, 문건은 이 단계를 보이지 않고 "1차 몫은 공통접선에 불변"이라는, 2계 미분에만 해당하는 근거를 1계 미분 결과에도 암묵적으로 재사용한다. Python(SymPy + 수치) 재검산 결과 boxed 식 자체는 기계정밀도(≈$10^{-11}$)까지 일치했다(아래 PASS 목록). 이것은 "설계문건 순응 검수가 오류를 통과시킨 전례"의 반대 사례 — 서술은 논리적으로 한 칸 비약(비약이 있는데도)하지만 도착한 최종식은 검증상 옳다.
**수정 방향.** L584–588 사이에 한 문장 추가: "이 $g_j(\xi)$ 는 $\theta\leftrightarrow1-\theta$ 대칭이라(로그·상호작용 몫 모두 자리바꿈 불변) $g_j'(\xi)=-g_j'(\theta)|_{\theta=1-\xi}$ 를 만족하며, 이 부호반전이 eq:eqcond 의 $\mu^0$ 항과 정확히 상쇄돼 선형항 없이도 $g_j'(\xi)=sF(V_\eq-U_j)$ 가 성립한다." 정도로 다리를 명시하면 G-derive 완결.
**4-tier.** 확정(수치·기호 결과는 정확 — 스크립트로 재확인) + 추정 아님, 논리 다리 생략은 직접 대조로 확인된 사실.

### [LOW-1] 위치: L390(eq:vwork) — $n_\work=\max(2048,\,2\,|V_n|)$ 의 $|V_n|$ 표기 중의성
**무엇이.** $|I|,|\Delta S_e|$ 등 이 문건에서 $|\cdot|$ 는 전 구간 "물리량의 절대값(크기)"만을 뜻하는데, 이 자리의 $|V_n|$ 은 문맥상(격자 점 개수 $n_\work$ 를 정하는 식) **$V_n$ 배열의 원소 개수(길이)** 를 뜻할 수밖에 없다 — 전위 값의 절대값을 그대로 정수 점 개수로 쓰는 것은 물리적으로 무의미하다. 같은 기호 $|\cdot|$ 를 "크기"와 "배열 길이"라는 서로 다른 뜻으로 겹쳐 쓴 것으로 보인다.
**왜.** "이 문건만 보고 코드를 재현" 목표(L138, G-usable)에 실제로 걸리는 지점 — 순수하게 식만 보고 구현하면 $|V_n|$ 을 전위 크기로 오해해 격자 점 수를 잘못 계산할 위험이 있다.
**수정 방향.** $n_\work=\max(2048,\,2\,\mathrm{len}(V_n))$ 또는 $2N_{V_n}$ 처럼 카디널리티 전용 표기로 교체.
**4-tier.** 추정(코드 원문 대조 없이 문맥상 유일하게 말이 되는 해석; .py 코드는 이번 감사 범위 밖이라 확정은 아님).

---

## 독립 재유도로 무결 확인된 항목 (PASS)

L1–683 범위의 boxed 식·수치 예시·그림 내 정량 좌표를 전부 Python 으로 재계산해 문건 값과 대조했다. **전부 일치**(오차는 부동소수 수준, 최대 $10^{-11}$):

| 대상 | 문건 값/식 | 독립 재계산 |
|---|---|---|
| eq:vn 부호 체인 | $V_n=V_\app-\sigma_d|I|R_n$, 방전 $\eta>0$/충전 $\eta<0$ | Butler–Volmer 부호규약과 정합(산화=+η, 환원=−η) 확인 |
| eq:Uj 수치예 (stage 2→1) | $U(298)\approx0.0853$ V | $0.085294$ V (일치) |
| eq:mu | $\mu_\mathrm{Li}(\theta)=\mu^0+RT\ln\frac{\theta}{1-\theta}+\Omega(1-2\theta)$ | SymPy $\partial\bar g/\partial\theta$ 로 재도출, 완전 일치 |
| eq:gpp | $g_j''=RT/[\xi(1-\xi)]-2\Omega$ | SymPy 2계미분 재도출, 차이 0 |
| eq:spinodal | $\xi_s^\pm=\tfrac12(1\pm u)$, $u=\sqrt{1-2RT/\Omega}$ | 2차방정식 근 재계산, 완전 일치. $\Omega_c=2RT$ 임계값도 regular-solution 표준 결과와 정합 |
| fig:doublewell 좌표($\Omega=3RT$) | $\xi_s^\pm=0.2113/0.7887$ | 재계산 $0.21132/0.78868$ (일치) |
| fig:hysloop 좌표($\Omega=4RT$) | $\xi_s^\pm=0.1464/0.8536$, $y=1.066$ | 재계산 $0.14645/0.85355$, $y=1.0653$ (일치) |
| eq:Veq, eq:hysdiff, eq:dUhys | $\Delta U_\hys=\frac2F[\Omega u-2RT\,\mathrm{artanh}\,u]$ | 극값 직접대입(logit/1-2ξ)과 boxed 식이 $10^{-11}$ 수준까지 일치 |
| 임계점 근방 극한 | $\Delta U_\hys\to\frac{8RT}{3F}u^3$, $u^3\propto(T_c-T)^{3/2}$ | Taylor 전개 재계산 일치, 멱지수 회귀로 $1.497\approx1.5$ 확인(mean-field 임계지수와 정합) |
| eq:hyssym | $\tfrac12[V_\eq(\xi_s^-)+V_\eq(\xi_s^+)]=U_j$ | 임의 $U_j=0.12345$ 대입 시 오차 $1.4\times10^{-17}$ (수치 0) |
| eq:Ubranch | $U_j^d=U_j+\tfrac12\sigma_d h_\eta\gamma\Delta U_\hys$, $\gamma\to0\Rightarrow U_j^d\to U_j$ | 수치 재확인, $U^\dis>U^\chg$ 도 확인 |
| eq:lco-dUdT + verifybox 수치 | $\Delta S_\rxn^\mathrm{cat}\approx+80$ J/(mol K), 30K 창 $\approx+25$ mV | 재계산 $80.08$ J/(mol K), $24.90$ mV (일치) |
| 전자항 크기 비교 | $0.18\,k_B$/atom$\times N_A\approx1.5$ J/(mol K) | 재계산 $1.4966$ J/(mol K) (일치, $k_B N_A=R$ 도 확인) |

이 결과로, 이전 챕터1 검수에서 문건 서술에 순응해 물리 오류(w_eff)를 통과시킨 전례와 달리, 이번 v1.0.11 N2/N3 코어 물리(Gibbs 자유에너지 → 화학퍼텐셜 → regular-solution 격자기체 → spinodal → 히스테리시스 gap)는 **문건 서술을 따라가지 않고 처음부터 손으로 재유도**해도 동일한 결과에 도달한다 — 물리 자체는 건전하다.

## 미검증 항목 (외부 문헌, 이 샌드박스에서 인터넷 접근 불가)
- tab:lco-staging 의 T1/T2/T3 전위값($\sim$3.90/4.05/4.17–4.20 V), $x$ 범위, config $\Delta S$ 값(0.47/1.49 J/mol K) — xia2007·reynier2004·motohashi2009 원문 대조 불가. 문건 스스로 "tier, 신뢰값 아니라 초기값" 으로 이미 헤지하고 있어 과잉주장은 아님.
- $\dd\phi/\dd T\approx+0.83$ mV/K(swiderska2019, tier B) — 원문 대조 불가, 문건이 "대표 스케일"로 이미 헤지.

## 범위 경계 보고
`sec:lco-hys`(LCO order–disorder/MIT 두 상태를 같은 regular-solution 틀에 매핑하는 절)는 **L684 에서 시작** — 지정 범위 L1–683 바로 다음 줄이다. 이 절은 이번 감사에서 다루지 않았으므로, 인접 청크(다음 절 담당)가 L684 부터 빠짐없이 이어받는지 확인 필요(coverage gap 방지).

## 정독 근거
L1–683 를 3회 분할 Read(1–250, 251–500, 501–683)로 head→tail 빈틈 없이 정독. grep 으로 `\label{sec:` 전수 확인해 sec:lco-hys 경계(L684)를 정확히 특정. 수식은 전부 손 재유도 + Python(SymPy/수치) 이중 검산.
