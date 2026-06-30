# A1 — Adversarial 물리·유도 회의자 검수 (v9-10 LCO)

> 역할 = 물리·유도 **반증자**. 대상 `Claude/results/ch1v9/v9-10/v9-10.tex`(1608줄). GT = `research/CH1v9_LCO/35_electronic_entropy_design.md`, `base_v8-11.tex`.
> 방법 = 5 표적 각각 "틀렸다 가정"하고 적대 검증 + 독립 수치 재산출(Python). 결함은 식별자·심각도·반증 근거·정정안.

---

## 결함표

| # | 식별자/위치 | 심각도 | 반증 근거 | 정정안 |
|---|---|---|---|---|
| F1 | `eq:Se`/`eq:dSe` (L908–917) "Sommerfeld 전개로 $C_e$" — c_e→S_e 경로 | **MED** | 유도가 한 단계 점프한다. 본문은 ① Sommerfeld 적분 $\int(-\partial f/\partial E)(E-E_F)^2 dE=\tfrac{\pi^2}{3}(k_BT)^2$ 를 인용하고 ② "$U_e=\int E g f\,dE$ 의 $T$ 미분에 이 적분을 대입하면 $C_e$" 라고 적지만, **그 대입에서 $g(E)\approx g(E_F)$(상태밀도를 $E_F$ 에서 동결) 가정과 $\mu(T)\approx E_F$ 근사를 명시하지 않는다**. 사실 $\partial U_e/\partial T$ 를 닫으려면 (a) $g$ 의 $E_F$ 근방 Taylor 1차항이 $\mu(T)$ 의 $T^2$ 이동과 상쇄된다는 표준 논증, (b) $-\partial f/\partial E$ 가 $E_F$ 에 폭 $k_BT$ 로 국소(이건 "완만하면"으로만 언급)가 필요. 즉 "$\int(-\partial f/\partial E)(E-E_F)^2$" 가 곧 $C_e$ 가 되는 다리에 g-동결 가정이 숨어 있다. **단계 유도라 주장(서론 L108)하나 이 한 칸은 결과 인용**이다. | (b)단계 본문에 한 줄 추가: "$g(E)$ 를 $E_F$ 근방에서 상수 $g(E_F)$ 로 두면(Sommerfeld 1차, $\mu\!\approx\!E_F$ 보정은 $T^2$ 고차) $U_e\!-\!U_e(0)=g(E_F)\int(E-E_F)(-\partial f/\partial E)\cdots$" → $C_e$. **숨은 가정 = $g$ 동결**을 가시화하면 점프 해소. |
| F2 | `eq:Se`/`eq:dSe` (L915,927) tier 라벨 모순 | **MED** | GT(35_…md L7)는 $S_e$ 식을 **"tier A 식, Reynier·Motohashi"** 로 명기. v9-10 L916 캡션은 **"$g(E_F)$ anchor 는 tier B–A"** 로 적어 식 자체의 tier 와 anchor 의 tier 를 뭉갠다. 실제로 **식 형태(Sommerfeld)는 tier A(교과서), $g_{\max}=13$ anchor 는 tier A 단일점(L990), 연속 $g(x)$ 곡선은 부재(G2)** — 세 층위가 다른데 한 라벨로 묶임. 반증: 독자가 "이 닫힌식 전체가 tier B" 로 오독 가능. | "식형 tier A(Sommerfeld) · $g_{\max}$ anchor tier A 단일점 · 연속 $g(x)$ 부재→logistic 게이트(피팅)" 3층 분리 표기. GT 의 "tier A 식" 과 일치시킴. |
| F3 | `eq:dSe` L927 박스 부호주석 vs `eq:dSemolar` 차원 | **MED→LOW** | `eq:dSe` 박스는 **자리당**($k_B^2$ 차원)인데 박스 안 부호주석에 "($<0$ at MIT, **삽입 기준**)" 을 달고, 바로 아래(L930) "이 박스는 자리당 양이라 forward 슬롯(몰당)에 **그대로 넣으면 단위가 어긋난다**" 고 자인. 즉 **박스 식 자체는 forward 에 plug-in 불가**인데 `tab:nodemap` N5+ 행(L1528)은 `eq:dSe` 를 그대로 코드 plug-in 식으로 가리킨다(몰당 `eq:dSemolar` 가 아니라). 반증: 코드 구현자가 박스(`eq:dSe`)를 그대로 쓰면 $N_A$ 배 틀림. | `tab:nodemap` N5+ 와 L1437 plug-in 지시의 참조를 `eq:dSe`→**`eq:dSemolar`(몰당)** 로 교체. 자리당 박스는 "유도용, 코드엔 몰당" 명시. |
| F4 | `eq:dSegate` L976–982 게이트 닫힌식의 leading-minus | **반증 실패(견고)** | 표적 2 핵심. 검증: $g=g_{\max}[1-\sigma(z)]$, $z=(x-x_{MIT})/\Delta x$. $\partial g/\partial x=-g_{\max}\sigma'(z)/\Delta x=-\tfrac{g_{\max}}{\Delta x}\sigma(1-\sigma)<0$. `eq:dSe` 에 대입 → $\Delta S_e=\tfrac{\pi^2}{3}k_B^2T\partial g/\partial x=-\tfrac{\pi^2}{3}k_B^2T\tfrac{g_{\max}}{\Delta x}\sigma(1-\sigma)$. **leading-minus 가 실제로 $\Delta S_e<0$ 을 강제함이 대수적으로 확인**($g_{\max},\Delta x,\sigma(1-\sigma)$ 모두 양). 부호 사슬: `eq:dSe`(L927)·`eq:dSegate`(L979)·`eq:lco-decomp`(L1400)·`fig:lco-electronic`(L1036)·`tab:nodemap` N5+ — **5곳 모두 "삽입 기준 $\Delta S_e<0$, 탈리튬화 방출 $|\Delta S_e|>0$" 로 1:1 일관**. 제거-positive 잔존 없음. | — |
| F5 | `eq:ggate`/`eq:dSegate` $\sigma$ 기호 충돌 | **LOW** | `eq:ggate`·`eq:dSegate` 의 logistic 을 $\sigma(\cdot)$ 로 쓰는데, 같은 문건이 방향 부호를 $\sigma_d$ 로 쓰고 전 절(L487)에서 **상호작용 평균장 초과에너지 $c\theta^2$ 의 계수**를 다룬다. $\sigma$(logistic)와 $\sigma_d$(방향)는 첨자로 구분되나 인접 식에서 인지부하. 물리 결함은 아님(반증 실패). | logistic 을 $\mathrm{logit}^{-1}$ 또는 $\ell(\cdot)$ 로 표기하거나 "$\sigma$=logistic(방향 $\sigma_d$ 와 무관)" 각주. |
| F6 | `tab:lco-staging` T1 $x$범위 vs `eq:ggate` 중심 | **반증 실패(견고)** | MIT 발현 $x\approx0.75$–$0.94$(tab L302, L893, L992)와 게이트 중심 $x_{MIT}\approx0.85$(L964)=구간 중앙 ✓, 폭 $\Delta x\approx0.05$ 를 $\pm2\Delta x\approx0.2\approx(0.94-0.75)$ 에 맞춤(L994) ✓. 자기일관. step→logistic 정당화(결함농도 분산·매끄러운 $\partial U/\partial T$, L996–999)도 물리적. | — |
| F7 | `verifybox` L1005–1007 크기검산 + `+0.83 mV/K` 부호 서술(L462) | **반증 실패(견고)** | 독립 수치: $S_e/k_B=\tfrac{\pi^2}{3}(0.0259\,\mathrm{eV})(13/\mathrm{eV})=$ **1.108** ✓(본문 1.1). $0.18\,k_B$/atom(Reynier B)과 같은 자릿수 ✓. **$+0.83$ mV/K 가 $\Delta S_e$ 부호를 제약 안 한다는 서술 정확**: $+0.83$ mV/K 는 $\Delta S_{rxn}^{cat}$ **전체**(config+vib+elec 합)의 단전극 sanity 스케일(L462–466)이고, $\Delta S_e$ 는 그 안의 작은 MIT-국소 성분이라 부호 독립 — 문건이 정확히 이렇게 분리(L1413 "부호 뒤집기 없음"). 단전극 vs 전셀 혼동 경고(L462–464)도 정확. | — |

---

## 추가 정밀 점검 (반증 시도했으나 견고)

- **단위 다리 $N_A k_B^2=R k_B$ (L932,937)**: 독립 검증 → $N_A k_B=8.3145=R$ ✓. "자리당 $k_B$ 한 몫이 몰당 $R$ 로 올라간다" 정확. **차원 정합 PASS.**
- **이중계산 B (L1407–1409)**: config 슬롯=중심 표준값 $\Delta S_j^0$ 만, 봉우리 내부 $R\ln[(1-\xi)/\xi]$ 는 logistic 이 담음 → 두 번 안 더함. **config 가 logistic 폭과 분해식에서 이중계산 안 됨** ✓. 단 **전자항-config 간 이중계산은 별도 논증 없음**(아래 F8 참조).
- **$\propto T$ (전자) vs 상수($\Delta S_{rxn}$) 구분 (L950–954, L1415)**: $\Delta S_e\propto T$ → $\partial U/\partial T|_e\propto T$ → peak 이동 $\propto T^2$. "$\partial U/\partial T$ 가 $T$-선형이지 peak 위치가 $T$-선형 아님" 식별신호 구분 정확 ✓.
- **artanh 히스 R1 (L1567)**: $\Omega=12000,\gamma=1$ → 독립 수치 $u=0.766$, $\Delta U^\hys=86.68$ mV ✓(본문 86.7). 임계 Taylor $\tfrac{8RT}{3F}u^3$ 는 $u\to0$ 극한 계수로만 정확(본문이 "Taylor 전개·$\to0$" 로 한정, 오용 아님).

## 잠재 결함 — 표적 4 심화 (F8)

- **F8 (MED): config–electronic 이중계산 미논증.** L1407 "이중계산 금지(B)" 는 **config 내부**(중심값 vs 봉우리 logistic)만 다룬다. 그러나 MIT T1 에서 **config $\Delta S$ 와 electronic $\Delta S_e$ 가 같은 물리(절연체→금속 = 전자구조 변화 = 동시에 정렬/무질서 변화)를 부분 중복 계상**할 위험은 논증 없음. GT(L21–23)도 "config=O3 지배, $\Delta S_e$=신규" 로 병렬 나열만. MIT 2상역의 전체 $\Delta S$ 를 config(격자기체 점유)+elec(밴드 켜짐)로 **가법 분리 가능**하다는 전제가 암묵. 반증 근거: Reynier 측정 $\Delta S(x)$ 는 **합**이라, config 를 logistic 으로 자동생성 + $\Delta S_e$ 를 또 더하면 T1 에서 측정값 초과 가능. **정정안**: L1407 부근에 "config(자리 점유)와 elec(밴드 점유)는 직교 자유도라 가법 — 단 피팅 시 T1 의 $\Delta S_j^0$ 는 elec 제외 잔차로 잡아 이중계상 방지" 한 줄 명시.

---

## 종합 물리 견고도

**5 표적 중 핵심(표적 2 부호·표적 3 게이트·표적 5 sanity)은 견고(F4·F6·F7 반증 실패).** 부호 사슬은 자리당·몰당·5개 식/그림/표 전수 1:1 일관. 결함은 모두 **유도 가시성·tier 표기·참조 정합·이중계산 논증** 층(CRIT 0, HIGH 0, MED 4: F1·F2·F3·F8, LOW 2: F5·F8경계). 물리 자체가 틀린 곳은 없으나 **"단계 유도"를 표방하는 문건 기준 F1(c_e→S_e g-동결 점프)·F3(코드 plug-in 식이 자리당 박스를 가리킴)·F8(config-elec 이중계상 미논증)** 은 실질 보강 가치가 있다.
