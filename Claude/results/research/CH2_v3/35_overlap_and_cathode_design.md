# Ch2 — 봉우리 겹침 구간의 ∂U/∂T 와 양극(LCO) 확장 (설계 노트)

> 사용자 질문(2026-06-30)에서 파생. Ch2 v3 초안의 eq:qrev_sum 을 *왜 매끄러운가*로 정밀화 + 양극 확장 scope. tier: 모델로 유도되는 부분=확정준함, 문헌/데이터 확인 필요=flag.

## Q1 — 겹침 구간: 합·계단이 아니라 dQ/dV-비중 가중 블렌드
관측 평형 전위 $U_\oc(x,T)$ 는 음함수로 정의: $\sum_j Q_j\,\xi_{\eq,j}(U_\oc,T)=Q\,x$. 음함수 미분(implicit function theorem):
$$\frac{\partial U_\oc}{\partial T}\Big|_x=-\frac{\sum_j Q_j\,\partial\xi_j/\partial T|_U}{\sum_j Q_j\,\partial\xi_j/\partial U|_T}.$$
$\partial\xi_j/\partial U=g_j\equiv\xi_j(1-\xi_j)/w_j$ (= dQ/dV 봉우리 모양). 선두차수($w$ 의 $T$ 의존 무시) $\partial\xi_j/\partial T|_U\approx-g_j\,\partial U_j/\partial T$. ⇒
$$\boxed{\;\frac{\partial U_\oc}{\partial T}(x)=\frac{\sum_j Q_j\,g_j(x)\,(\partial U_j/\partial T)}{\sum_j Q_j\,g_j(x)}=\frac1F\,\frac{\sum_j Q_j g_j\,\Delta S_{\rxn,j}}{\sum_j Q_j g_j}\;}$$
= **각 전이의 ΔS 를 그 전이의 *국소 dQ/dV 비중* $Q_jg_j/\sum Q_jg_j$ 로 가중한 평균.** 사용자 직관("비율적으로 적용")이 정확히 맞다.

**왜 계단이 아니라 매끄러운가 — 두 출처:**
1. **봉우리간 겹침**: 가중치 $g_j(V)$ 가 logistic-종이라 겹침 구간서 $g_j,g_{j+1}$ 둘 다 0이 아님 → $\partial U/\partial T$ 가 $\Delta S_{\rxn,j}/F$ 에서 $\Delta S_{\rxn,j+1}/F$ 로 *연속* 이동(지시함수 합 아님 ⇒ 계단 아님).
2. **봉우리 내부 configurational 엔트로피**: 한 전이 안에서도 $V(\xi)=U_j+(RT/F)\ln[\xi/(1-\xi)]$ 라 $\partial V/\partial T|_\xi=\Delta S_{\rxn,j}/F+(R/F)\ln[\xi/(1-\xi)]$. 둘째 항이 **섞임(configurational) 엔트로피** — $\xi\to0$(희박) 발산 양수(저-$x$ 큰 양 ΔS·+29 의 주원천), $\xi=\tfrac12$ 에서 0, $\xi\to1$ 발산 음수. 곧 Ch1 의 logistic 폭 $w=RT/F$ 가 *이미* 봉우리 내부 비선형 ΔS(x) 를 담고 있다.

⇒ Ch1 의 *같은 모델*이 매끄러운 비선형 $\partial U/\partial T(x)$ 를 자동 생성(임시 계단·ad hoc 분리 불요). 가역 발열 $\dot Q_\rev=-IT\,\partial U/\partial T$ 가 비선형으로 나오는 게 자연스러움.

**★확인 필요(flag)**: (a) $\Delta S_{\rxn,j}$(상수)가 ΔS 의 *표준/vibrational* 부분이고 configurational 은 logistic 이 주는 것 — **이중계산 주의**(Allart 의 config/vib 분해와 매핑 검증). (b) $w$ 대신 $w_\eff(\Omega)$ 쓰면 configurational 기여 변형 — Ω-narrowing 의 ΔS 영향. (c) 위 가중식을 Ch1 코드로 수치 검증(매끄러움·실측 비선형 재현).

## Q2 — 양극(LCO): 전셀 = 양극 − 음극, 같은 프레임 가능하나 LCO 고유 항
- **전셀 엔트로피 계수 = 두 전극의 차**: $U_\mathrm{cell}=U_\mathrm{cat}-U_\mathrm{an}$ ⇒ $\partial U_\mathrm{cell}/\partial T=\partial U_\mathrm{cat}/\partial T-\partial U_\mathrm{an}/\partial T$. 가역 발열 $\dot Q_\rev=-IT\,\partial U_\mathrm{cell}/\partial T$ 는 *두 전극 합*이라 **음극만으로는 전셀 가역열 불가**.
- **같은 Ch1 프레임 적용 가능(개념)**: LCO 도 intercalation 상전이(다봉우리 dQ/dV)라 전이별 logistic + $U_j(T)=(-\Delta H+T\Delta S)/F$ + $\Delta S_{\rxn,j}$ 의 *동일 forward 모델*이 적용된다 — 프레임은 전극-불문(일반 격자기체 열역학). 곧 "양극용 Chapter 1" 을 같은 코드/구조로 세워 양극 $\partial U/\partial T$ 산출 가능.
- **★LCO 고유 주의(음극과 다른 점)**:
  1. $x\approx0.5$ 의 order–disorder(육방↔단사) + **insulator–metal 전이** → graphite 의 config/vib 외에 **전자(electronic) 엔트로피** 기여 추가(LCO ∂U/∂T 의 특징적 봉우리). 이 항은 Ch1 프레임에 *새 성분*으로 들어가야 할 수 있음.
  2. LCO ∂U/∂T 프로파일 모양이 graphite 와 다름(문헌 pure-LCO 값 = 출발점).
  3. 도핑·첨가제로 봉우리 smear/shift → pure-LCO 문헌값을 *초기값*으로 약간 피팅(Ch1 의 GRAPHITE_STAGING_LIT 가 초기값이었던 철학과 동일).
  4. 부호/기준: 양극 U 높음(~3.9–4.2V vs Li), 전셀선 음극과 반대 부호로 합류.
- **권고 경로**: 같은 forward 모델로 "cathode-Ch1(LCO)" 별도 구축 → 양극 $\Delta S_{\rxn,j}^\mathrm{cat}$ → 음극과 합쳐 전셀 $\partial U_\mathrm{cell}/\partial T$ → 전셀 가역열. (LCO 전자 엔트로피 항은 조사로 근거화.)

## 파생 확인 항목 (A–I)
- **A** 겹침 가중식(위 boxed)을 Ch1 코드로 수치 검증 — 매끄러움·실측 비선형 재현, 계단 부재.
- **B** Ch1 $\Delta S_{\rxn,j}$ = 표준/vibrational? configurational 은 logistic 폭이 주는가 → **이중계산 점검**(Allart config/vib 분해 대조). +29@저-x 가 config 발산인지.
- **C** $w$ vs $w_\eff(\Omega)$ 가 ΔS(x) 모양에 주는 차이(Ω-narrowing).
- **D** 히스 하 겹침: 충/방전 경로별 $\partial U/\partial T$ 차이(가역/비가역 분리, JPS 2018).
- **E** 전셀 합성 부호·기준 정합($\partial U_\mathrm{cell}=\partial U_\mathrm{cat}-\partial U_\mathrm{an}$), 반쪽 vs 전셀 측정 분해.
- **F** ★LCO 전자 엔트로피(metal–insulator @x≈0.5) — Ch1 프레임에 추가 항 필요성·문헌값.
- **G** 검증: 측정 전셀 가역열(calorimetry/entropy spectroscopy) = (음극+양극) 예측 — 비선형 재현 round-trip.
- **H** Ch1 forward 코드(클래스)의 LCO 일반화 가능성(전이 파라미터 교체만으로?).
- **I** "$\Delta S_{\rxn,j}$ 전이당 상수" 근사의 타당성 — 봉우리 내부 ΔS(x) 가 logistic config 로 충분한가, 아니면 $\Delta S_{\rxn,j}(x)$ 필요한가.

## 함의
- Ch2 의 가역 발열은 *Ch1 모델의 자연 귀결*(겹침 가중 + 봉우리 내부 config) — 별도 계단/분리 모델 불요. 이게 "실측 비선형"의 물리적 이유.
- 양극(LCO)은 **같은 프레임 + 전자 엔트로피 항 + 전셀 합성**으로 확장 — 별도 "cathode-Ch1" 조사·구축이 새 scope(교수님 검토 후 v9/양극 트랙).
