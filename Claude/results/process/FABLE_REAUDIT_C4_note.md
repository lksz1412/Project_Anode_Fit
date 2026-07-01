# FABLE 재검 챕터2 — 내용 감사 C-4

- **역할**: 감사 sub (파일 수정 없음, 노트 1개 산출)
- **대상**: `Claude/docs/v1.0.11/graphite_ica_ch2_v1.0.11.tex` (750줄, head→tail 전문 정독 완료)
- **방법**: 물리 독립 재유도(분배함수→점유분포→S_config·가중식·q_rev 부호 전부 손으로 재계산) + 파이썬 실행 실측(numpy/scipy, synthetic 4-전이 계·부호 대입 검산 2종) + `Anode_Fit_v1.0.11.py`의 `func_w`/`_width` 직접 대조(파생 A의 근거 확인용, 감사 범위는 .tex 유지·코드는 교차확인만)
- **판정 요약**: **CRITICAL 2건**(사인 오류 1건[국소적, 하류 전파 없음] + w 열적스케일링 지위 구조적 모순 1건[코드로 확증]), **MODERATE 1건**(히스 분기평균 근사가 항등식처럼 제시됨), **MINOR 1건**(극한표 고온 코너의 Sommerfeld 타당역 이탈). 나머지 전 도출 과정(분배함수→FD 동형성→S_config→S_vib(BE)→S_e(Sommerfeld)→겹침가중 완전식→q_rev)은 독립 재유도로 전부 정합 확인.

---

## 1. CRITICAL — eq(2.11)–(2.12) Bragg–Williams $V_\eq(\theta)$ 부호 오류 (국소적, 하류 오염 없음)

**재유도**: §ssec:BW 의 $g(\theta)=g_0+RT[\theta\ln\theta+(1-\theta)\ln(1-\theta)]+\Omega\theta(1-\theta)$ 에서 "평형 전위 = $\theta$ 1몰 삽입당 자유에너지 변화"로 $V_\eq=(1/F)\,dg/d\theta$ 를 취하면 문건 그대로 eq(2.11) $V_\eq(\theta)=U_j+(RT/F)\ln[\theta/(1-\theta)]+(\Omega/F)(1-2\theta)$ 가 나온다(이 스텝 자체는 재현됨).

문제는 이 부호 관례가 **같은 절 바로 앞 eq(2.5)/(2.6)/(2.7)과 충돌**한다는 것. eq(2.5) $\mu=\mu^0-\sigma_dF(V-U_j)$ ($\sigma_d{=}{+}1$)를 뒤집으면 $V=U_j-(\mu-\mu^0)/F$ 이고, $\mu=dg/d\theta$(化학퍼텐셜=자유에너지의 몰분율 미분, 표준 열역학 정의)를 대입하면
$$V_\eq(\theta) = U_j - \frac{RT}{F}\ln\frac{\theta}{1-\theta} - \frac{\Omega}{F}(1-2\theta)$$
로 **양쪽 항 모두 부호가 뒤집힌다**. 이 "정정형"이 맞다는 것은 두 가지로 확증했다:
1. $\Omega=0$ 극한에서 문건 eq(2.6)/(2.7)(logistic 로부터 직접 유도된 $V(\theta)=U_j+(RT/F)\ln[(1-\theta)/\theta]$, 즉 $-\ln[\theta/(1-\theta)]$)과 정확히 일치 — eq(2.11)-as-written 은 불일치.
2. 파이썬 수치 대입(`sign_check.py`): $\theta_\eq(V)$(eq 2.6)로 만든 참값 $V$ 5점에 대해 "정정형"은 모든 점에서 참값과 소수 4자리까지 정확히 일치(예: $V{=}0.05\to\theta{=}0.875\to$ 정정형 $0.0500$), "as-written"형은 $V_\text{true}$ 를 $U_j$ 기준으로 정확히 반사한 값(예: 같은 점에서 $0.1500$, 즉 $2U_j-V_\text{true}$)을 낸다 — 두 항이 정확히 mirror-flip 관계임을 확인.

**물리적 의미**: eq(2.11)을 문건 그대로 사용하면 $\theta$(점유)가 늘수록 $V_\eq$ 가 \emph{증가}하는 것으로 나와, 흑연 삽입 시 전위가 하강한다는 실측·문건 자신의 §2.1 서술과 정반대다.

**하류 전파 여부**: 다행히 국소적이다 — (a) $\partial V_\eq/\partial\theta=0$ 이 되는 임계값은 부호가 반전돼도 두 항이 함께 뒤집히므로 영점 위치 자체는 불변(파이썬으로 재확인: $\theta{=}1/2$ 에서 $4RT-2\Omega=0\Rightarrow\Omega=2RT$, 부호와 무관), 그래서 §sec:limits·§ssec:weff 등에서 반복 인용되는 "$\Omega=2RT$" 임계값은 살아있다. (b) 이후 §sec:config 이후의 모든 실제 계산(부분몰 config, 겹침가중, q_rev)은 eq(2.11)이 아니라 eq(2.7)의 $V(\xi)$ 를 재사용하므로, 이 사인 오류가 챕터의 나머지 정량 기계장치를 오염시키지 않는다. 그래도 eq(2.11)–(2.12) 자체는 문건에 boxed 결과식으로 인쇄돼 있어 독자가 그대로 구현하면 정성적으로 뒤집힌 등온선을 얻는다 — 수정 필요.

## 2. CRITICAL — $w_j$ 열적 스케일링 지위의 구조적 자기모순 (코드로 확증)

세 지점이 서로 충돌한다:
- **§ssec:logistic keybox(162행)**: "logistic 폭 $w=RT/F$ 는(...전이별 유효 폭 $w_j=n_jRT/F$ 는 §sec:revheat·코드 \texttt{func\_w}) **임의 모수가 아니라** 단일 자리 2-상태 분배함수가 정하는 분포의 열적 폭이다." — $w_j=n_jRT/F$ 를 **물리적으로 확정된 형태**라고 단정, 근거로 §sec:revheat·코드 func_w 를 지목.
- **§ssec:weff/파생 C(546–556행) 및 §sec:revheat 종합식(676–680행)**: "두-상($\Omega>2RT$, **흑연 staging 전이가 여기 속함**): ...실측 폭은 평형이 정하는 양이 **아니라**, (i) 유한 율속 비대칭 꼬리 (ii) 평탄역 내재 단상 폭 (iii) 집합 다입자 통계역학 $\rho(U_\app)$ 이 정하는 **현상학적 자유 피팅 파라미터**다... 평형 예측 $nRT/F$ 가 **아니라** 다온도 $dQ/dV$ 로 피팅하는 현상학적 자유 폭이다." — 정확히 같은 흑연 staging 전이에 대해 $n_jRT/F$ 형태를 **명시적으로 부정**.

두 서술 모두 "§sec:revheat·코드 func_w"를 근거로 인용하는데, 서로 반대 결론을 내린다. 그리고 **파생 A(484–495행)의 "부동소수점 정밀도 일치" 수치검증**은 "Chapter 1 코드의 4-전이 흑연 staging 파라미터"로 수행됐다고 명시하는데, 그 검증이 성립하려면 $w_j(T)$가 정확히 $n_jRT/F$ 로(즉 $\partial w_j/\partial T=n_jR/F$ 로) 스케일해야 한다 — 이는 §ssec:weff가 같은 전이들에 대해 부정한 바로 그 형태다.

**재유도 + 시뮬레이션(파이썬, synthetic 4-전이계, $R,F$ 실제값, $T_1{=}292.15,T_2{=}298.15$K, 175점)**:
- Case 1 ($w_j(T)=n_jRT/F$, 열적 스케일): 완전식 vs FD 최대오차 $3.6\times10^{-9}$ V/K(부동소수점) / 단순식 오차 최대 $0.309$ mV/K — 문건이 보고한 패턴(완전식 PASS, 단순식 최대 $0.18$ mV/K)과 정성적으로 일치(크기는 synthetic 파라미터 차이로 다름, 메커니즘은 동일).
- Case 2 ($w_j$ 를 $T_\mathrm{ref}$ 에서 동결, T-무관 — §ssec:weff 가 주장하는 phenomenological 폭에 가까운 가정): **정확히 뒤집힌다** — 단순식이 FD와 $1.0\times10^{-8}$ V/K로 일치하고, 문건이 "정답"으로 제시하는 완전식(R/F 계수 그대로 적용)이 오히려 $0.310$ mV/K 오차를 낸다.

즉 어느 공식이 "옳은" 공식인지는 전적으로 $w_j$가 실제로 $T$에 선형 비례하는지에 달려 있고, 이는 무시할 수 없는 크기(두 formula 오차가 정확히 자리를 바꿈)다.

**코드 교차확인**(`Anode_Fit_v1.0.11.py`): `func_w(T,n)=n*R*T/F`(L74-75), `_width`(L303-306, "폭 w: 자유 피팅 파라미터: w|n 직접 지정, 없으면 n=1")는 **모든 전이**(graphite staging 포함)에 대해 이 열적 스케일 형태를 그대로 쓴다 — 자유롭게 피팅되는 것은 진폭 $n_j$(또는 기준온도의 $w$)뿐이고, $T$-의존의 \emph{함수형}(선형, 기울기 $n_jR/F$)은 고정돼 있다. C-6 감사가 이미 확인한 대로 앙상블 $\rho(U_\app)$ convolution도 별도 구현되지 않고 이 $w$에 흡수되므로(forward-only), 코드에는 §ssec:weff가 묘사하는 "$RT/F$ 스케일을 따르지 않는 phenomenological 폭"을 실현할 경로가 **존재하지 않는다**. 결론: §ssec:weff/파생 C가 "두-상 전이는 $nRT/F$ 가 아니다"라고 명시적으로 선언한 바로 그 물리가 실제 구현·수치검증(파생 A)에는 반영되지 않았고, 이는 §ssec:logistic keybox의 (반대되는) 주장과만 일치한다 — 챕터 내부에서 결론이 두 갈래로 갈리고, 실제 코드/수치검증은 그중 한쪽(§ssec:logistic 편)만 구현한 채 다른 쪽(§ssec:weff)이 "성립"한다고 텍스트로 계속 주장하는 상태.

## 3. MODERATE — 파생 D 히스테리시스 분기평균이 근사를 항등식처럼 제시

eq(2.35) $\partial U^\rev_\oc/\partial T=\tfrac12(\partial U^\mathrm{ch}/\partial T+\partial U^\mathrm{dis}/\partial T)$ 뒤의 근거 문장("충방전을 한 사이클 돌면 히스 중심이 상쇄되고 열역학적 $\Delta S$만 남기 때문이다")은 두 분기의 봉우리 형태 $g_j^{(d)}(x)$가 동일하다는 가정 하에서만 정확하다. 그러나 $g_j^{(d)}=\xi_j^{(d)}(1-\xi_j^{(d)})/w_j$ 는 분기 중심 $U_j^{(d)}=U_j\pm\Delta U_j^\hys/2$ 자체가 다르므로 같은 $x$에서 $g_j^{(\mathrm{ch})}\ne g_j^{(\mathrm{dis})}$ 이고, 겹침가중식(eq 2.22-type)의 비선형 때문에 두 분기 가중평균이 정확히 "$\Delta S_{\rxn,j}/F$"로 떨어진다는 보장은 없다(config 항의 곡률 때문에 1차 근사에서만 상쇄). 문건은 이를 정확한 결과처럼 boxed로 제시하는데, 적어도 "$\Delta U^\hys \ll w_j$(선형화 유효 영역)에서" 라는 조건절이 필요하다.

## 4. MINOR — 극한표의 "고온($k_BT\sim E_F$)" 코너가 Sommerfeld 타당역 밖 인용

§ssec:elec은 eq(2.29) $S_e=(\pi^2/3)k_B^2Tg(E_F)$ 를 "축퇴 극한($k_BT\ll E_F$)"에서만 유도한다고 명시한다. 그런데 표 tab:limits 마지막 행은 "고온($k_BT\sim E_F$ 근접)"코너에서 "electronic $\propto T$ 우세화, FD Sommerfeld eq(2.29); $S_e$ 선형 증가"라고 **같은 식을 타당역 경계 밖(퇴화 붕괴 직전)에 그대로 인용**한다. 정성적 방향(전자 기여가 커진다)은 맞을 수 있으나, eq(2.29)이 그 극한에서 정량적으로 성립한다고 읽히는 서술은 근사의 유효범위를 넘는 코너케이스 과일반화다.

---

## 5. 독립 재유도로 검증 완료(정합, 오류 없음) — 커버리지 확인용

- $Z_1$(eq 2.1)→$\langle n\rangle$(eq 2.2): 대수 재계산 정확 일치, Fermi–Dirac 동형성 확인.
- eq(2.6)–(2.8): $\mu$–$V$ 선형관계(eq 2.5, $\sigma_d{=}{+}1$)로부터 logistic 역함수 재유도 → 문건과 정확 일치(§1의 대조군으로 사용).
- $S_\config$(eq 2.13)과 부분몰 발산(eq 2.14–2.16): $\partial S_\config/\partial\theta=-R\ln[\theta/(1-\theta)]$ 재미분 정확 일치; $\partial V/\partial T=\Delta S_{\rxn,j}/F+(R/F)\ln[\xi/(1-\xi)]$ 도 $w=RT/F$ 명시 $T$-의존으로부터 재도출 일치.
- BW 임계 $\Omega=2RT$(eq 2.9–2.12): 위 §1의 부호 오류에도 불구하고 임계값 자체(양변 동시 반전으로 불변)는 재계산으로 확인.
- $S_{\vib,k}$ Bose–Einstein 닫힌식(eq 2.17): $F_k=\hbar\omega/2+k_BT\ln(1-e^{-\beta\hbar\omega})$ 로부터 $S_k=-\partial F_k/\partial T$ 를 처음부터 재유도해 $k_B[(1+n)\ln(1+n)-n\ln n]$ 과 정확 일치(교재 표준식과도 일치).
- $S_e$ Sommerfeld(eq 2.29): 표준 자유전자 열용량 $\gamma=(\pi^2/3)k_B^2g(E_F)$, $S_e=\gamma T$ 형태와 일치(단 §4의 타당역 예외 있음).
- 겹침가중 완전식(eq 2.18–2.26, "계산용 종합식"): 음함수 미분(implicit function theorem)으로 처음부터 재유도 — $\partial\xi_j/\partial U=g_j$, $\partial\xi_j/\partial T=-g_j\partial U_j/\partial T-g_j z_j(R/F)$ 까지 부호 하나까지 정확히 일치. 파이썬 시뮬레이션(§2 Case 1)으로 "완전식=FD to 부동소수점" 재현 확인.
- $\dot Q_\rev$ 부호규약(eq 2.30–2.32): $\Delta G=-FU_\oc$, $\Delta S=+F\,\partial U_\oc/\partial T$ 대입 경로 재확인, Bernardi–Pawlikowski–Newman 표준형과 일치.
- 파생 B(이중계산 금지, warnbox): $\Delta S^0_j$(중심 표준값, config=0)와 분포 config 항이 겹치지 않는다는 주장은 정의상 self-consistent, 실제 이중계산 버그는 발견되지 않음(파생 B 자체가 이미 가드).

## 6. 4-tier 분류 — 리터러처 수치 (미검증)

표 tab:ds의 $\Delta S^0_j=+29.0/0.0/-5.0/-16.0$ J/mol/K, LiC$_6$/LiC$_{12}$ 형성엔탈피, stage $2\to1$ $\Delta H^0_j=-13.0$ kJ/mol 등은 **근거 미발견**(외부 1차 문헌 원문 대조 없이는 확정 불가) — 다만 방향·자리수는 흑연 엔트로피 문헌의 널리 알려진 정성적 추세(저-$x$ 큰 양, 고-$x$ 음, stage $2\to1$ 부근 급변)와 부합하며 내적 일관성은 확인됨.

---

**요약(5줄)**: eq(2.11)–(2.12) Bragg–Williams $V_\eq(\theta)$에서 부호가 eq(2.5)–(2.7)과 반대로 뒤집힌 오류를 재유도+수치대입으로 확정(임계 $\Omega{=}2RT$ 자체는 불변, 하류 오염 없음). 더 심각한 것은 $w_j$의 열적 스케일링 지위 — §ssec:logistic이 "$w_j=n_jRT/F$, 임의모수 아님"이라 단정한 것을 §ssec:weff/파생C가 그래파이트 두-상 전이에 대해 명시적으로 부정하는데, 파생 A의 "완전식=FD 부동소수점 일치" 검증과 실제 코드(`func_w`/`_width`, 모든 전이에 $n_jRT/F$ 강제)는 §ssec:weff 아닌 §ssec:logistic 편을 실현하고 있어 챕터 내부 물리 주장과 구현이 어긋난다(파이썬 시뮬레이션으로 두 스케일링 가정 사이 오차가 정확히 자리바꿈함을 확인, ~0.3 mV/K급). 파생 D의 히스 분기평균은 엄밀한 항등식이 아니라 선형화 근사(leading-order)를 결과박스로 제시한 것이 비약. 극한표의 고온 코너는 Sommerfeld 축퇴극한 공식을 타당역 밖에 재사용. 나머지 분배함수→점유분포→config/vib/electronic 엔트로피→겹침가중→q_rev 사슬은 전부 독립 재유도·수치 재현으로 정합 확인됨.
