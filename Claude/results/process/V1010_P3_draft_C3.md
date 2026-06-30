# V1010 P3 draft C3 — Ch2 발열 교과서화 supplement

## 0. 수행 범위와 판정 기준

본 supplement는 `docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex`를 직접 수정하지 않고, P3 경쟁 드래프트 C3로서 Ch2의 통계열역학 및 가역발열 이론을 코드 앵커와 Ch1에 대조한다. 출력 대상은 이 파일 하나이며, 발열 코드 구현은 P4 범위로 남긴다.

직접 확인한 원천은 다음이다.

| 구분 | 파일 | 직접 확인 범위 |
|---|---|---|
| 사용자 지시 | `scratchpad/p3_codex_C3.txt` | 전체 12행 |
| 프로젝트 지침 | `CLAUDE.md`, `Codex/AGENTS.md` | 전체 |
| Ch2 대상 | `Claude/docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex` | 전체 |
| 코드 앵커 | `Claude/results/process/V1010_P1_code-audit_RESULT.md` | 전체, 출력 잘림 구간 재확인 |
| Ch1 정합 | `Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex` | 전체, 출력 잘림 구간 재확인 |
| P3 계획 | `Claude/plans/2026-07-02-v1010-P3-ch2-heat-plan.md` | 전체 |
| v3 survey | `Claude/results/research/CH2_v3/PHASE_CH2v3_RESULT.md`, `50_report.md` | 전체 |
| v5/v4 검토 근거 | `REVIEW_RISK_PATTERNS.md`, `R2_mixing_weff_B.md`, `R3_qrev_depth.md`, `A2_adv_mixing.md` | 전체 |

판정 표기는 `확정`, `보정 필요`, `P4 예고`, `근거 미발견`으로 나눈다. `확정`은 위 원천에서 직접 대조된 항목만 가리킨다.

---

## 1. Ch2 ↔ 코드/Ch1 정합 매트릭스

### 1.1 핵심 정합표

| Ch2 항목 | Ch2 현재 내용 | 코드 앵커와의 정합 | Ch1과의 정합 | 판정 |
|---|---|---|---|---|
| 평형 중심 전위 | `U_j(T)=(-\Delta H_{\rxn,j}+T\Delta S_{\rxn,j})/F` 및 `\partial U_j/\partial T=\Delta S_{\rxn,j}/F` | 코드 `func_U_j`가 동일 식을 구현하고, P1 audit이 `dS_rxn`을 peak 위치의 온도 기울기 파라미터로 확정 | Ch1 N2가 같은 식과 같은 부호 사슬을 쓴다 | 확정 |
| 점유분포와 logistic | Ch2는 `Z_1 -> <n> -> \theta`, `\xi=1-\theta`로 Ch1 logistic의 통계역학 기원을 설명 | 코드 `func_ksi_eq`는 logistic 점유를 직접 구현 | Ch1 `\xi_\eq=1/(1+\exp[-\sigma_d(V-U^d)/w])`와 대응 | 확정 |
| configurational entropy | `S_\config=-R[\theta\ln\theta+(1-\theta)\ln(1-\theta)]`, 부분몰 항 `R\ln[\xi/(1-\xi)]` | 코드에는 `S_config` 계산 함수는 없지만 폭 `w=nRT/F`와 logistic 형이 해당 분포 항을 암묵적으로 만든다 | Ch1의 logistic 폭 및 `\xi=1-\theta` 규약과 정합 | 확정, 코드 내 명시 발열 계산은 부재 |
| vib/electronic entropy | Ch2는 vib(Bose--Einstein)와 electronic(Fermi--Dirac/Sommerfeld)을 분포 언어로 정리 | P1 audit은 코드에 전자엔트로피·발열 항이 없음을 확정 | Ch1 LCO electronic entropy 절과 같은 FD/Sommerfeld 언어를 공유한다. 흑연에서는 electronic이 소수로 취급된다 | 확정 |
| 겹침 가중 | Ch2는 음함수 미분으로 `\partial U_\oc/\partial T`의 전이별 `Q_j g_j` 가중 평균과 config 완전식을 제시 | 현재 코드는 `U_oc(x,T)`를 역으로 풀어 `q_rev`를 산출하지 않는다. 다만 `Q_j`, `g_j=\xi(1-\xi)/w`, logistic은 코드 구조와 같은 재료다 | Ch1의 전하 보존 합산식 `C_bg+\sum Q_j[...]`와 같은 가중 구조 | 이론 정합 확정, 코드 구현은 P4 |
| hysteresis 분리 | Ch2는 분기 평균을 reversible coefficient로, gap을 irreversible heat로 분리 | 코드에는 `func_dU_hys`, `func_U_branch`가 있으나 열분리 계산은 없다 | Ch1 N3의 히스 분기 중심과 정합 | 이론 정합 확정, 열계산은 P4 |
| 가역 발열 | `\dot Q_\rev=-IT\partial U_\oc/\partial T=-(IT/F)\Delta S(x)` | P1 audit은 `q_rev`, self-heating, `dT/dt`가 코드에 없음을 확정 | Ch1의 `dS_rxn`은 반응 엔트로피이고 `dS_a`는 활성화 엔트로피라 분리됨 | Ch2 이론 확정, 코드 과잉 없음, P4 예고 |
| 비가역 발열 | Ch2는 Bernardi의 `I(U_\oc-V)` 및 히스 gap/과전압 소산을 옵션으로 둔다 | 코드는 `Rn`, `L_V`, hysteresis, activation barrier로 비가역 동역학을 만들지만 열량으로 변환하지 않는다 | Ch1 N1/N7/N8의 분극·꼬리가 비가역 소산의 원천 | P4에서 `I^2R`, `I\eta`, `I\Delta U^\hys` 형태로 연결 가능 |

### 1.2 누락·과잉·중복

**누락(의도적, P4):**

- 코드에는 `q_rev`, `q_irr`, `heat_generation`, `dT/dt` 또는 thermal state가 없다. P1 audit §2-E가 `q_rev`, `발열`, `전자엔트로피` 검색 부재를 확정했다.
- Ch2 종합식은 `\partial U_\oc/\partial T`를 산출하기 위해 `U_\oc(x,T)` 음함수 해를 필요로 한다. 현재 코드의 public output은 `dQ/dV(V)` forward curve이며, `x -> U_\oc` 역문제/온도 미분 루틴은 없다.
- hysteresis gap의 열분리도 아직 코드화되지 않았다. Ch1/코드는 분기 중심을 계산하지만, 열항 `I\Delta U^\hys` 또는 cycle dissipation으로 변환하지 않는다.

**과잉 아님:**

- Ch2가 발열식을 서술하는 것은 코드 과잉 구현이 아니라 이론 예고다. P3 계획이 “발열 코드 구현은 P4, P3는 이론 갈고닦기”로 범위를 확정했다.
- Ch2의 LCO electronic entropy는 흑연 코드에 이미 있어야 하는 항이 아니다. Ch1이 LCO 확장 사례를 포함하므로, Ch2는 분포 언어의 사례로 정합시키면 된다.

**중복·모순 경계:**

- Ch1은 “한 곡선을 그리는 forward model”이고, Ch2는 그 같은 분포의 엔트로피·온도 기울기·가역열 해석이다. Ch2가 Ch1 logistic을 재유도하되, 코드 진행 전체를 다시 설명하면 중복이 된다. 따라서 Ch2의 재유도는 `Z -> 점유분포 -> S -> \partial U/\partial T -> q_rev` 사슬에 한정하는 것이 맞다.
- Ch1 `dS_a`는 활성화 엔트로피이고 Ch2 `\Delta S_{\rxn}`는 반응 엔트로피다. 둘은 단위가 같아도 열역학 위치가 다르다. 가역열에는 `dS_rxn`만 들어가고 `dS_a`는 비가역 속도/꼬리의 온도의존에만 들어간다.

---

## 2. 발열 이론 정련: 식에서 식으로

### 2.1 평형 전위와 반응 엔트로피

삽입 반응 1몰 Li 기준으로 평형 전위와 반응 Gibbs 자유에너지를

```tex
\Delta G_{\rxn}(T,x) = -F\,U_\oc(T,x)
```

로 둔다. Gibbs 항등식은 등압 조성 고정 조건에서

```tex
\Delta S_{\rxn}(x)
=-\left(\frac{\partial \Delta G_{\rxn}}{\partial T}\right)_x
=F\left(\frac{\partial U_\oc}{\partial T}\right)_x .
```

따라서

```tex
\left(\frac{\partial U_\oc}{\partial T}\right)_x
=\frac{\Delta S_{\rxn}(x)}{F}.
```

전이 중심만 보면 Ch1의 `U_j(T)=(-\Delta H_{\rxn,j}+T\Delta S_{\rxn,j})/F`에서 곧바로

```tex
\frac{\partial U_j}{\partial T}=\frac{\Delta S_{\rxn,j}}{F}
```

가 나온다. 겹친 전이에서는 `U_j(T)` 중심 이동만 평균하면 중심 근사이고, Ch2의 완전식은 여기에 logistic 폭의 명시적 온도 의존이 만드는 config 항을 더한다.

### 2.2 통계열역학에서 `\Delta S(x)`까지

단일 삽입 자리의 대정준 분배함수는

```tex
Z_1=1+\exp[-\beta(\varepsilon_0-\mu)].
```

평균 점유는

```tex
\theta=\langle n\rangle
=\frac{1}{1+\exp[\beta(\varepsilon_0-\mu)]},
\qquad \xi=1-\theta .
```

이 0/1 점유 분포의 configurational entropy는

```tex
S_\config=-R[\theta\ln\theta+(1-\theta)\ln(1-\theta)].
```

부분몰 configurational entropy는

```tex
\frac{\partial S_\config}{\partial \theta}
=-R\ln\frac{\theta}{1-\theta}.
```

`\theta=1-\xi`를 실제로 대입하면

```tex
\left.\frac{\partial S_\config}{\partial \theta}\right|_{\theta=1-\xi}
=R\ln\frac{\xi}{1-\xi}.
```

따라서 Ch2의 config 항 정답은

```tex
\Delta S_\config(\xi)=R\ln\frac{\xi}{1-\xi}
```

이다. 여기서 `\xi`는 Ch1과 같은 탈리튬화 진행률이다. 이 부호가 바뀌면 저-Li 희박 한계와 만충 한계가 뒤집혀 Ch1 및 Allart/Reynier 계열 흑연 엔트로피 프로파일과 충돌한다.

vibrational entropy와 electronic entropy는 같은 구조 위의 추가 자유도다. 포논 모드에 대해

```tex
S_{\vib,k}=k_B[(1+n_k)\ln(1+n_k)-n_k\ln n_k]
```

이며, 전자 준위에 대해

```tex
S_e=-k_B\int g(E)[f\ln f+(1-f)\ln(1-f)]\,dE
\simeq \frac{\pi^2}{3}k_B^2Tg(E_F)
```

가 된다. Ch1 LCO electronic entropy 절과 Ch2 electronic entropy 절은 이 FD/Sommerfeld 구조에서 정합한다. 흑연 주모델에서는 electronic 항을 소수로 두고, LCO MIT는 예외적 사례로 남긴다.

### 2.3 `\Delta S(x)`에서 Bernardi 가역열까지

전기화학 반응의 molar rate를 방전 전류 규약 `I>0`에서

```tex
\dot n=\frac{I}{F}
```

로 둔다. 가역 entropy heat generation을 “셀 내부에서 생성되는 열률”의 부호로 쓰면

```tex
\dot Q_\rev
=-\dot n\,T\,\Delta S_{\rxn}(x)
=-\frac{I\,T}{F}\Delta S_{\rxn}(x).
```

위 2.1의 `\Delta S_{\rxn}=F(\partial U_\oc/\partial T)`를 넣으면

```tex
\boxed{\dot Q_\rev=-I\,T\left(\frac{\partial U_\oc}{\partial T}\right)_x
=-\frac{I\,T}{F}\Delta S_{\rxn}(x)}.
```

이것이 Ch2와 v3 survey가 공통으로 쓰는 Bernardi 출구다. 총 열생성은 단일 활물질 단순형에서

```tex
\dot Q
=I(U_\oc-V)-I\,T\left(\frac{\partial U_\oc}{\partial T}\right)_x
=\dot Q_\irr+\dot Q_\rev .
```

여기서 `I(U_\oc-V)`는 discharge에서 `V<U_\oc`이면 양수인 비가역 소산이고, 두 번째 항은 부호가 바뀌는 가역열이다.

### 2.4 부호 검산

현재 Ch2 규약은 `I>0` 방전, `\Delta S=F\partial U/\partial T`, `\dot Q>0` 열생성이다. 따라서:

| 조건 | 수식 | 열 해석 |
|---|---|---|
| `\Delta S>0`, `\partial U/\partial T>0` | `\dot Q_\rev=-(IT/F)\Delta S<0` | 방전에서 흡열 |
| `\Delta S<0`, `\partial U/\partial T<0` | `\dot Q_\rev>0` | 방전에서 발열 |
| 전류 반전 | `I -> -I` | 가역열 부호 반전 |
| `I=0` | `\dot Q_\rev=0`, `\dot Q_\irr=0` | 열률 0 |
| `T -> 0` | `\dot Q_\rev -> 0` | 엔트로피 열률 소멸 |
| `\Delta S=0` | `\dot Q_\rev=0` | 중심 표준 entropy 0이면 해당 항 없음 |

따라서 저-Li 희박 영역에서 config 항이 양이면 방전 가역열은 흡열이고, 고-Li 또는 stage `2->1`처럼 `\Delta S<0`인 영역은 방전 가역 발열이다. 이 판정은 `R3_qrev_depth.md`의 ground truth와 정합한다.

### 2.5 차원 검산

```tex
I\,T\,\frac{\partial U}{\partial T}
=[C\,s^{-1}]\,[K]\,[V\,K^{-1}]
=C\,V\,s^{-1}
=J\,s^{-1}
=W.
```

또는

```tex
\frac{I\,T}{F}\Delta S
=\frac{C\,s^{-1}\,K}{C\,mol^{-1}}\frac{J}{mol\,K}
=J\,s^{-1}.
```

비가역 항도

```tex
I(U_\oc-V)=[C\,s^{-1}][J\,C^{-1}]=J\,s^{-1}.
```

히스테리시스 gap을 소산 항으로 볼 때 `I\Delta U^\hys`도 같은 차원이다.

### 2.6 비가역 옵션의 위치

P4에서 열 모델을 구현한다면 다음 항들을 분리해야 한다.

```tex
\dot Q_\irr
=I(U_\oc-V)
\simeq I^2R_n + I\eta_{\kin} + I\Delta U^\hys_{\mathrm{loss}} + \cdots .
```

단 `\Delta U^\hys` 전체를 `\partial U/\partial T`에 섞으면 안 된다. Ch2의 현재 파생 D처럼 reversible coefficient는 분기 평균으로 두고, gap 자체는 path-dependent entropy production으로 분리한다. Ch1의 `Rn`, `L_V`, `dH_a`, `dS_a`, `Omega`, `gamma`는 비가역 소산의 원천을 만든다. 그러나 P1 audit 기준 현재 코드에는 그 원천을 W 단위 열률로 바꾸는 함수가 없다.

---

## 3. v5/v4 검토분 타당성 반영

### 3.1 확정 채택할 검토 판단

| 검토 판단 | 타당성 | Ch2 v1.0.10 반영 상태 |
|---|---|---|
| config 항은 `+R ln[\xi/(1-\xi)]`, `\xi`는 탈리튬화 진행률 | 타당. Ch1의 `\xi` 규약과 Ch2 수식 전개가 이 방향을 요구한다 | 현재 Ch2가 이 방향으로 정리되어 있음 |
| 방전 `I>0`에서 `\Delta S>0`은 흡열, `\Delta S<0`은 발열 | 타당. `\dot Q_\rev=-(IT/F)\Delta S`의 직접 귀결 | 현재 Ch2 §revheat가 이 판정으로 정리되어 있음 |
| `w_eff=w/(1-\Omega/2RT)`는 오류이고, V-폭 기준 정정은 `w_eff=w(1-\Omega/2RT)` | v4 검토 당시에는 타당한 정정. 다만 v5는 이 전체 `w_eff` 절을 제거하고, 두-상 폭을 현상학적 피팅 폭으로 재정의했으므로 더 안정적 | 현재 Ch2는 `w_eff` narrowing 식을 제거하고 Ch1 broadening으로 넘김 |
| 완전식은 logistic 가정 하 음함수 미분의 정확식이지 “선두차수”가 아니다 | 타당. A2 독립 강겹침 테스트가 완전식 exact를 확인 | 현재 Ch2의 한계·갭 서술은 “logistic 전이형과 파라미터 집합의 실데이터 검증”을 남은 공백으로 두어 더 적절함 |
| 하프셀 범위와 전셀 합성 금지 | 타당 | 현재 Ch2는 코인 하프셀 단독 warnbox를 둠 |
| v4-05의 섞임/극한 구조는 좋지만 exo/endo 문단은 오염원 | 타당 | 현재 Ch2는 구조적 장점을 보존하고 exo/endo는 정정된 판정으로 씀 |

### 3.2 현재 Ch2에서 남는 보정 후보

1. `\partial U_\oc/\partial T` 완전식은 `g_j` 가중 평균의 분모가 `\sum Q_j g_j`이므로, 정규화 SOC `x`를 쓰면 측정 `dQ/dV`와는 비례상수 `Q` 차이가 있다. 본문에서 “정확히 측정 dQ/dV”라고 쓰는 위치는 `Q\partial x/\partial U` 또는 “비례”로 정밀화하는 것이 좋다.
2. Ch2 §revheat의 source box에는 `-(IT/F)\,T\,\Delta S/T`처럼 중간 표현이 길게 들어가 있다. 수식 자체는 결과가 맞지만, 교과서식 전개에서는 `\Delta S=F\partial U/\partial T`를 바로 대입해 `-IT\partial U/\partial T=-(IT/F)\Delta S`로 쓰는 편이 더 깨끗하다.
3. `occupation2019`, `chemmater2015`, `jpcc2021` 등 일부 인용은 Ch2 bib에 tier가 낮다고 명시되어 있다. 본문 근거 강도를 주장할 때 “방법 수준”, “abstract tier”를 유지해야 한다.

위 1-3은 supplement의 후속 체리픽 후보이며, 본 C3 드래프트에서는 원문 파일을 수정하지 않는다.

---

## 4. v3 가역발열 survey 통합

### 4.1 좋은 요소

v3 survey에서 유지할 요소는 다음이다.

- `U_j(T) -> \partial U_j/\partial T -> \Delta S_{\rxn,j} -> \dot Q_\rev` 사슬을 Ch1에서 Ch2로 직접 연결한 점.
- Bernardi, Newman, MSMR, Allart/Reynier, hysteresis uncertainty, standardised potentiometric protocol을 tier와 함께 모은 점.
- Ch1의 흑연 전이별 `\Delta S_{\rxn,j}=+29,0,-5,-16` J mol^-1 K^-1가 Allart 계열 측정 엔트로피 프로파일의 양 끝과 정량 대응한다고 확인한 점.
- 반응 엔트로피와 활성화 엔트로피를 분리한 점.
- 다온도 `dQ/dV` 동시 피팅으로 `U_j(T)`의 기울기를 추정하려는 신규 경로를 “실데이터 round-trip 필요”로 정직하게 남긴 점.

### 4.2 보정해서만 가져올 요소

`CH2_v3/50_report.md`는 `\dot Q_\rev=-IT\partial U/\partial T`와 `\Delta S=+F\partial U/\partial T`를 올바르게 확정하면서도, 핵심 결과 3에서 “저-x 양 `\Delta S`(방전 발열) ↔ 고-x 음 `\Delta S`(흡열)”이라고 적었다. 이는 같은 문서의 수식과 v4/v5 검토 ground truth에 반한다.

따라서 v3의 해당 문장은 다음처럼 보정해야 한다.

```tex
\Delta S>0 \quad\Rightarrow\quad \dot Q_\rev<0 \quad(\text{방전 흡열}),
```

```tex
\Delta S<0 \quad\Rightarrow\quad \dot Q_\rev>0 \quad(\text{방전 발열}).
```

v3에서 가져올 것은 문헌 사슬과 Ch1 정량 앵커이며, exo/endo 라벨은 v4/v5 검토 기준으로 정정해 가져와야 한다.

---

## 5. Ch2 본문에 넣을 수 있는 supplement 문단 후보

### 5.1 Bernardi 항의 부호를 닫는 짧은 유도

```tex
\Delta G_{\rxn}=-FU_\oc,\qquad
\Delta S_{\rxn}=-\left(\frac{\partial \Delta G_{\rxn}}{\partial T}\right)_x
=F\left(\frac{\partial U_\oc}{\partial T}\right)_x .
```

전류 `I>0`를 방전 molar reaction rate `\dot n=I/F`로 두면, reversible entropy heat generation은

```tex
\dot Q_\rev=-\dot n\,T\Delta S_{\rxn}
=-\frac{I\,T}{F}\Delta S_{\rxn}
=-I\,T\left(\frac{\partial U_\oc}{\partial T}\right)_x .
```

이 부호는 heat generation convention이다. `\dot Q_\rev<0`은 셀이 열을 흡수하는 endothermic reversible term이고, `\dot Q_\rev>0`은 셀 내부에서 방출되는 exothermic reversible term이다.

### 5.2 통계열역학 항과 발열 항의 연결 문단

```tex
The statistical-mechanical calculation supplies \Delta S_{\rxn}(x), not a separate heat source. Once the lattice, phonon, and electronic distributions have been reduced to the partial molar entropy, the thermal step is purely thermodynamic:
\Delta S_{\rxn}(x)\mapsto \partial U_\oc/\partial T=\Delta S_{\rxn}(x)/F \mapsto \dot Q_\rev=-(IT/F)\Delta S_{\rxn}(x).
```

한글 본문에서는 다음처럼 둘 수 있다.

```tex
통계열역학은 직접 열률을 만들지 않는다. 통계열역학이 주는 것은 한 SOC에서 다음 SOC로 갈 때 재배열되는 미시상태 분포의 부분몰 엔트로피 \Delta S_{\rxn}(x)이다. 이 값이 평형 전위의 온도계수 \partial U_\oc/\partial T=\Delta S_{\rxn}/F 로 바뀌고, Bernardi 에너지 수지에서 \dot Q_\rev=-(IT/F)\Delta S_{\rxn} 로 열률이 된다.
```

### 5.3 P4 구현 경계 문단

```tex
현재 Anode_Fit v1.0.10 코드는 \Delta S_{\rxn,j}를 U_j(T)의 온도 기울기 파라미터로 보유하고, \Delta S_{a,j}를 동역학 지연의 활성화 엔트로피로 보유한다. 그러나 q_rev, q_irr 또는 thermal state equation은 없다. 따라서 본 장의 열식은 P4 구현의 사양이며, 현 코드의 출력과 동일시하지 않는다.
```

---

## 6. P4 전달 사양

P4에서 실제 열 계산을 추가한다면 최소 인터페이스는 다음 순서가 되어야 한다.

1. 주어진 `x` 또는 `V`에서 Ch1 logistic 전이들을 평가한다.
2. `\sum_j Q_j\xi_j(U,T)=Qx`를 풀어 `U_\oc(x,T)`와 각 `\xi_j`를 얻는다.
3. 완전식으로 `\partial U_\oc/\partial T`를 계산한다.
4. `q_rev=-I*T*dUdT`를 계산한다.
5. `q_irr=I*(U_oc-V)` 또는 분해형 `I^2R_n + I\eta + I\Delta U^\hys_loss`를 선택적으로 계산한다.
6. `dS_rxn`과 `dS_a`를 절대 섞지 않는다. `dS_a`는 kinetic temperature dependence에만 쓰고 reversible heat에는 넣지 않는다.

검증 gate는 다음이어야 한다.

| Gate | 기대 결과 |
|---|---|
| `I=0` | `q_rev=q_irr=0` |
| `T=0` | `q_rev=0` |
| `dUdT=0` | `q_rev=0` |
| `I` 반전 | `q_rev` 부호 반전 |
| `\Delta S>0`, 방전 | `q_rev<0` |
| `\Delta S<0`, 방전 | `q_rev>0` |
| `V=U_oc` | overpotential part `I(U_oc-V)=0` |
| `R_n>0`, `I!=0` | ohmic heat positive |

---

## 7. 결론

Ch2 v1.0.10의 큰 구조는 코드와 Ch1에 정합한다. Ch1/코드는 `U_j(T)`, `dS_rxn`, logistic 점유, 폭, 히스, 동역학 꼬리를 제공하고, Ch2는 같은 재료를 엔트로피와 가역발열로 해석한다. 단 현재 코드에는 발열 산출 함수가 없으므로 Ch2의 `q_rev`는 이론 사양이며 P4 구현 대상이다.

가장 중요한 교정점은 부호다. 현재 채택해야 할 정본은

```tex
\Delta S=F\partial U/\partial T,\qquad
\dot Q_\rev=-IT\partial U/\partial T=-(IT/F)\Delta S.
```

따라서 방전에서 `\Delta S>0`은 흡열, `\Delta S<0`은 발열이다. v3 survey의 문헌 사슬과 Ch1 정량 앵커는 유효하지만, v3 요약의 exo/endo 라벨은 이 규약으로 보정해야 한다.
