# Ch2 v4 — 섞임/겹침·극한 수식 설계 (Phase C.2, master)

> C.1 분포 spine 위. 교과서용 *닫힌 유도*. 파생 A(겹침 가중·수치검증)·C(w_eff(Ω))·D(히스)·I(극한). 이중계산 B 명시.

## A. 봉우리 겹침 — dQ/dV-비중 가중 (계단 아님)
관측 평형 전위 $U_\oc(x,T)$: 음함수 $\sum_j Q_j\,\xi_{\eq,j}(U_\oc,T)=Q\,x$. 음함수 미분:
$$\frac{\partial U_\oc}{\partial T}\Big|_x=-\frac{\sum_j Q_j\,\partial\xi_j/\partial T|_U}{\sum_j Q_j\,\partial\xi_j/\partial U|_T}.$$
$\partial\xi_j/\partial U=g_j\equiv\xi_j(1-\xi_j)/w_j$(=dQ/dV 봉우리 모양). 선두차수 $\partial\xi_j/\partial T|_U\approx-g_j\,\partial U_j/\partial T$. ⇒
$$\boxed{\;\frac{\partial U_\oc}{\partial T}(x)=\frac{\sum_j Q_j\,g_j(x)\,(\partial U_j/\partial T)}{\sum_j Q_j\,g_j(x)}=\frac1F\,\frac{\sum_j Q_j g_j\,\Delta S_{\rxn,j}}{\sum_j Q_j g_j}\;}$$
= 각 전이 ΔS 를 *국소 dQ/dV 비중* $Q_jg_j/\sum Q_jg_j$ 로 가중한 평균. 겹침서 $g_j,g_{j+1}$ 둘 다 ≠0 → $\Delta S_{\rxn,j}/F$ 에서 $\Delta S_{\rxn,j+1}/F$ 로 *연속* 이동(계단 아님). ★**수치검증(A)**: Ch1 코드로 $\partial U/\partial T$(다온도 차분) = 위 식 비교 — `42_numerical_verification.md`(compute sub).

## 봉우리 내부 configurational (분포가 줌) — 이중계산 B
$V(\xi)=U_j+(RT/F)\ln[\xi/(1-\xi)]$ ⇒ $\partial V/\partial T|_\xi=\Delta S_{\rxn,j}/F+(R/F)\ln[\xi/(1-\xi)]$.
- ★**이중계산 B 금지**: $\Delta S_{\rxn,j}$ = *중심 표준값*(ξ=½, config=0). configurational $x$-의존은 logistic 폭 $w=RT/F$ 가 줌(C.1 §2). config 를 $\Delta S_{\rxn,j}$ 에 또 더하지 말 것. 측정 ΔS(x) = 중심 표준 + 분포 config + (vib·electronic 은 중심값 흡수).
- 부호: ξ=탈리튬화 진행률 → 희박 Li(ξ→1) +∞, 만충(ξ→0) −∞ (Ch1 부호 일관).

## C. w vs w_eff(Ω) — 상호작용의 폭·ΔS 변형
정규용액서 평형 등온선 기울기: $\dfrac{\dd V_\eq}{\dd\xi}=\dfrac{RT}{F}\Big[\dfrac{1}{\xi(1-\xi)}-\dfrac{2\Omega}{RT}\Big]$. ξ=½ 중심: $\dfrac{\dd V_\eq}{\dd\xi}\big|_{1/2}=\dfrac{4RT-2\Omega}{F}=4w\Big(1-\dfrac{\Omega}{2RT}\Big)$. 이상 logistic($V=U_j+w_\eff\ln[\xi/(1-\xi)]$)의 중심 기울기 $4w_\eff$ 와 정합:
$$\boxed{\;w_\eff=w\Big(1-\frac{\Omega}{2RT}\Big)\quad(\text{V-공간 폭, }\Omega<2RT).\;}$$
- ★**부호 주의**(역수 아님): Ω↑ → $w_\eff$ **감소**(V-폭 좁아짐) → Ω→2RT⁻ 서 $w_\eff\to0$(전위 plateau=상분리 임계, ξ 가 한 V 에서 급변). 곧 *V-공간* 폭은 줄고, **dQ/dV 봉우리 높이** $\dd\xi/\dd V|_{1/2}=1/(4w_\eff)=\dfrac{1}{4w(1-\Omega/2RT)}$ 는 **발산**(좁고 높은 peak). 둘은 역수 관계 — "좁힘"은 V-폭 기준.
- config 봉우리 내부 변동: 같은 x 폭에 V-폭이 줄어 $\ln[\xi/(1-\xi)]$ 가 더 가파름 → ∂U/∂T 봉우리 내부 변동 *증폭*(Ω→2RT 서 plateau·불연속).
- ★온도 의존: $\Omega$ 약한 T 의존이면 $\partial w_\eff/\partial T$ 가 ∂U/∂T 에 2차 기여(소수, 명시).

## D. 히스테리시스 — 충/방전 분기별 ∂U/∂T
분기 중심 $U_j^d=U_j\pm\tfrac12\Delta U_j^\hys$(방향 $d$). 각 분기:
$$\frac{\partial U_\oc^{(d)}}{\partial T}=\frac1F\frac{\sum_j Q_j g_j^{(d)}\,\Delta S_{\rxn,j}}{\sum_j Q_j g_j^{(d)}}\quad(g_j^{(d)}=\text{분기 봉우리}).$$
- **가역(평균)**: $\partial U^\mathrm{rev}/\partial T=\tfrac12(\partial U^\mathrm{ch}/\partial T+\partial U^\mathrm{dis}/\partial T)$ — 가역 발열의 열역학적 ΔS.
- **비가역(히스 gap)**: $\Delta U^\hys$ 자체는 entropy 생성(비가역열 $\propto I\Delta U^\hys$), ∂/∂T 와 분리. ★가역 발열은 평균 분기로, 히스 gap 은 비가역으로 분리 계산(혼동 금지).

## I. 극한·코너 검산 → "ΔS_rxn,j 상수" 근사 타당성
| 극한 | ∂U/∂T 거동 | 검증 |
|---|---|---|
| ξ→0(만충) | config −∞ | 부분몰 발산(분포), 물리적(만충 정렬) |
| ξ→1(희박) | config +∞ | 희박 큰 양 ΔS(저-x +29 주원천) |
| ξ=½(중심) | =Δ S_{rxn,j}/F | config=0, 표준값 회수 |
| Ω→2RT⁻ | w_eff(V-폭)→0·dQ/dV peak→∞, plateau | 상분리 임계(∂U/∂T 평탄·불연속) |
| 단일 봉우리(겹침 0) | =Δ S_{rxn,j}/F + config | 가중식이 단일 전이로 환원 |
| 고온 | electronic ∝T 우세화 | FD 분포 Sommerfeld |
★**파생 I 판정**: "$\Delta S_{\rxn,j}$ 전이당 상수" 근사는 **중심 표준값(vib+electronic 중심)이 전이 폭 내 천천히 변할 때 타당**. 봉우리 내부 *급변*은 config 분포가 담음(상수 아님). ⇒ 측정 ∂U/∂T(x) 비선형은 (i) 겹침 가중 (ii) 봉우리 내부 config 두 출처로 *자동 생성*, $\Delta S_{\rxn,j}(x)$ 함수화 불요(전이별 상수 + 분포로 충분). 단 vib/electronic 이 전이 폭 내 급변하면(예: MIT 게이트가 한 전이 안에서) 그 항만 x-의존 유지(LCO T1).

## C.2 Gate
A 닫힌식+수치검증(sub)·B 이중계산 분리·C w_eff(Ω)·D 히스 가역/비가역 분리·I 극한 6건+근사 판정. → AUTHOR_BRIEF(Ch2 v4) → Phase D 9종.
