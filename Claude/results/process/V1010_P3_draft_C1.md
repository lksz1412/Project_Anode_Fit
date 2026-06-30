# V1010 P3 Draft C1 — Ch2 발열 교과서화 Supplement

## 0. Read coverage and scope

역할: Anode_Fit v1.0.10 P3 챕터2(발열) 9종 경쟁 드래프트 C1(Codex).

직접 읽은 범위:

| 구분 | 파일 | 실제 확인 범위 | 용도 |
|---|---|---:|---|
| P3 지시 | `C:/Users/lksz1/AppData/Local/Temp/claude/d--Projects/f45f576c-1efc-4f50-8591-1f84bb7d7f39/scratchpad/p3_codex_C1.txt` | 1-12 | 본 작업 지시 원문 |
| 프로젝트 지침 | `CLAUDE.md`, `Codex/AGENTS.md` | 전문 | 작업 경계, 원본 수정 금지, full-read 규칙 |
| 대상 Ch2 | `Claude/docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex` | 1-750 | 통계열역학·가역발열 본문 |
| 코드 anchor | `Claude/results/process/V1010_P1_code-audit_RESULT.md` | 1-445 | 코드 엔트로피항·q_rev 부재·피팅 파라미터 |
| Ch1 정합 | `Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex` | 1-1932 | U_j(T), electronic entropy, broadening, sign chain |
| v3 survey | `Claude/plans/2026-06-30-ch2-reversible-heat-entropy-survey-plan.md`; `Claude/results/research/CH2_v3/{50_report.md,PHASE_CH2v3_RESULT.md,22_ch1_vs_literature.md,30_synthesis_gap.md,20_extraction/_SUMMARY.md}` | 전문 | Bernardi 사슬, 부호, 문헌 anchor, 공백 |
| v5 review | `Claude/results/process/PHASE_V5_RESULT.md`, `PHASE_V5RR_ROUNDS_RESULT.md` | 전문 | v5 검토 원칙과 수식-follow 검증 방식 |

산출 범위: supplement 초안만 작성한다. 원본 `.tex`, 코드, 기존 result/ledger는 수정하지 않았다.

---

## 1. Ch2 ↔ code / Ch1 정합 매트릭스

| Ch2 요소 | Ch2 근거 | 코드 anchor | Ch1 근거 | 판정 | P3 supplement 반영 |
|---|---|---|---|---|---|
| `U_j(T)=(-Delta H_rxn + T Delta S_rxn)/F` | Ch2 L69-73, L636-646 | `func_U_j`는 동일식, P1 L174-177; `Delta S_rxn`은 보조 파라미터, P1 L393-394 | Ch1 L437-456, L1831-1834 | 확정 정합 | `Delta S_rxn`은 코드에 이미 있는 평형/반응 엔트로피 항이다. |
| `partial U_j/partial T = Delta S_rxn/F` | Ch2 L240-243, L645-653 | 코드는 `U_j(T)`를 계산하므로 다온도 입력에서 기울기 추정 가능하나 `q_rev`는 없음 | Ch1 L453-456, L1858-1860 | 확정 정합 | Ch2는 코드의 열역학 입력을 발열 이론으로 해석하는 장이다. |
| `xi_eq` logistic / 점유 분포 | Ch2 L119-175, L151-158 | `func_ksi_eq`, `func_w`, peak `Q xi(1-xi)/w`, P1 L106-109, L185-189, L293-295 | Ch1 L740-780, L853-899 | 확정 정합 | Ch2의 `Z -> <n> -> xi_eq`는 Ch1 logistic의 통계역학적 해설이다. |
| configurational entropy | Ch2 L210-309, L524-537 | 코드에는 별도 `S_config(x)` 함수 없음. 단 `w=nRT/F`와 logistic 미분이 config 항의 수학적 자리다. | Ch1 L1695-1701은 config 내부 조성 의존을 logistic이 이미 담는다고 명시 | 정합, 구현은 간접 | P4 코드 구현 시 config를 `Delta S^0_j`에 중복 가산하면 안 된다. |
| vibrational entropy | Ch2 L359-380 | 코드에는 vib 분해 함수 없음. `Delta S_rxn` 중심값에 흡수됨. | Ch1 L1711-1712에서 vib baseline을 `Delta S_rxn` 내부 성분으로 처리 | 정합, 구현은 lumped | Ch2는 vib를 물리 해석으로 보존하되 현재 코드는 lumped `Delta S_rxn`만 가진다고 명시한다. |
| electronic entropy | Ch2 L381-409 | P1 L351-356: `dS_e`/전자 엔트로피 구현 없음 | Ch1 L927-1160, L1685-1759: LCO MIT 전자항 이론, P4 plug-in 예고 | Ch1과 정합, 현재 코드에는 과잉 | Ch2의 electronic 항은 흑연에서는 보정/사례, LCO/P4 확장 예고로 분리해야 한다. |
| 반응 entropy vs 활성화 entropy | Ch2 L423-427 | 코드에는 `dS_rxn`과 `dS_a`가 둘 다 있으나 물리 역할 분리, P1 L393-397 | Ch1 L244-245, L1456-1476 | 확정 정합 | `dS_a`는 Eyring 꼬리의 prefactor/activation 항이고 `q_rev`에 직접 넣지 않는다. |
| 겹침 가중식 | Ch2 L439-495, L669-684 | 코드의 `dQ/dV` 가중 구조는 `sum Q_j peak_shape`, P1 L287-300, L371-422 | Ch1 L1641-1655, L1822-1841 | 개념 정합 | Ch2의 `sum Q_j g_j` 분모는 Ch1의 전하 보존 미분 구조와 같은 spine이다. |
| 폭 `w_j` 이중지위 / `w_eff` 제거 | Ch2 L539-568, L676-683 | P1 L120, L237-240, L347: `use_w_eff` 제거, 면적 보존 회복 | Ch1 L711-738, L1213-1347, L1835-1838 | 확정 정합 | v5의 핵심 타당 요소. 두-상 흑연 폭은 평형 narrowing이 아니라 broadening을 흡수한 현상학적 폭이다. |
| 히스테리시스 평균과 비가역 분리 | Ch2 L570-593 | 코드에는 히스 분기와 꼬리 구현은 있으나 열 생성 없음, P1 L289-300 | Ch1 L620-649, L1853-1904 | 방향은 정합, 발열 부호는 재검토 필요 | 히스 gap은 비가역 소산으로 분리한다. 단 `q_rev` 단전극 부호 convention을 본문에서 고정해야 한다. |
| `q_rev` / self-heating | Ch2 L637-666 | P1 L351-356: `q_rev`, 열생성, `dT/dt` 결합 없음 | Ch1은 P4 예고만 보유, Ch1 L1724-1733 | 코드 대비 과잉이 아니라 P4 예고 | Ch2는 이론 chapter이고 P4에서 구현해야 한다고 명시한다. |

결론: Ch2의 통계열역학 본체는 Ch1/코드 spine과 대체로 정합한다. 코드와의 유일한 큰 경계는 `q_rev` 계산과 전자 엔트로피가 아직 구현되지 않았다는 점이다. 물리적으로 가장 위험한 미결점은 `q_rev`의 단전극/하프셀 부호 convention이다.

---

## 2. 발열 이론 갈고닦기: 식 -> 식 유도

### 2.1 평형 전위의 온도 기울기와 반응 엔트로피

삽입 반응 1몰당 Gibbs 자유에너지를

```math
\Delta G = \Delta H - T\Delta S
```

로 둔다. 전극 평형 전위 `U`와 반응 자유에너지의 연결을 Ch1/Ch2 convention처럼

```math
\Delta G = -F U
```

로 두면

```math
-F U = \Delta H - T\Delta S,
\qquad
U(T)=\frac{-\Delta H+T\Delta S}{F}.
```

따라서 같은 반응 좌표와 같은 표준상태에서

```math
\frac{\partial U}{\partial T}=\frac{\Delta S}{F},
\qquad
\Delta S = F\frac{\partial U}{\partial T}.
```

이 부호는 v3 survey의 정전 결론과 일치한다: MSMR Part I/Newman 계열에서 `Delta S = + n F dU/dT`, `n=1`일 때 `Delta S = F dU/dT`다. Ch1의 `GRAPHITE_STAGING_LIT`도 이 convention으로 `+29 -> 0 -> -5 -> -16 J mol^-1 K^-1`를 가진다.

### 2.2 Bernardi cell-level energy balance

균일 온도, 단일 cell OCV `E`, 방전 전류 `I>0`, 단자 전압 `V` convention에서는 Bernardi 축약형을

```math
\dot Q = I(E-V) - I T\frac{\partial E}{\partial T}
```

로 쓴다. 첫 항은

```math
\dot Q_{\mathrm{irr}} = I(E-V)=I\eta_{\mathrm{cell}}\ge 0
```

이고, 둘째 항은

```math
\dot Q_{\mathrm{rev,cell}}
= -I T\frac{\partial E}{\partial T}
= -\frac{I T}{F}\Delta S_{\mathrm{cell}}.
```

차원 검산:

```math
[I T \partial E/\partial T]
= [C\,s^{-1}]\,[K]\,[J\,C^{-1}\,K^{-1}]
= J\,s^{-1}=W.
```

부호 검산:

```math
\Delta S_{\mathrm{cell}}>0
\Rightarrow
\partial E/\partial T>0
\Rightarrow
\dot Q_{\mathrm{rev,cell}}<0
```

즉 방전 중 cell은 가역적으로 열을 흡수한다. `Delta S_cell<0`이면 가역 발열이다.

### 2.3 단전극/하프셀 convention 경고

Ch2는 “코인 하프셀 단독”과 `I>0 방전`을 동시에 둔다. 여기서 `U`를 어느 quantity로 쓰는지에 따라 부호가 달라진다.

1. **cell-level half-cell convention**: Li metal 상대극을 포함한 하프셀의 OCV를 `E_half = U_working - U_Li = U_working`로 보고, 그 하프셀의 방전 전류 `I>0`을 Bernardi cell convention에 맞추면

```math
\dot Q_{\mathrm{rev,half}}
= -I T\frac{\partial U_{\mathrm{working}}}{\partial T}.
```

이것이 현재 Ch2 L643-646의 식이다.

2. **full-cell negative-electrode contribution convention**: full-cell OCV를

```math
E = U_p - U_n
```

으로 두면 negative electrode contribution은

```math
\dot Q_{\mathrm{rev},n}
= -I T\frac{\partial(-U_n)}{\partial T}
= +I T\frac{\partial U_n}{\partial T}.
```

과거 FRR 결과에는 “전극 단독형은 `q_rev=+IT partial V^rev/partial T`, full cell에서는 `E=U_cat-U_an` 때문에 음극 몫 부호가 반전되어 표준 Bernardi가 복원된다”는 부호 정정 이력이 있다.

따라서 P3 master가 Ch2에 실제 삽입할 때는 다음 박스를 추가하는 것이 안전하다.

```math
\boxed{
\text{본 장의 } \dot Q_{\mathrm{rev}}=-IT\,\partial U/\partial T
\text{ 는 }U\text{ 를 하프셀 OCV로 보고 }I>0\text{ 를 그 하프셀 discharge convention으로 정의한 식이다.}
}
```

그리고 full-cell 음극 기여를 계산할 때는

```math
\dot Q_{\mathrm{rev},n}^{\mathrm{full-cell}}
= +I T\frac{\partial U_n}{\partial T}
```

로 전환해야 한다. 이 convention box가 없으면 Ch2 L656-665의 “`Delta S>0`이면 방전 흡열” 해석과 v3 `50_report.md`의 “저-x 양 `Delta S`(방전 발열)” 문장이 충돌한다.

### 2.4 통계열역학 `Delta S(x)`에서 `q_rev`로 가는 사슬

Ch2의 점유 분포는

```math
Z_1=1+\exp[-\beta(\epsilon_0-\mu)],
\qquad
\theta=\frac{1}{1+\exp[\beta(\epsilon_0-\mu)]},
\qquad
\xi=1-\theta.
```

configurational entropy는

```math
S_{\mathrm{config}}
=-R[\theta\ln\theta+(1-\theta)\ln(1-\theta)].
```

부분몰 config 항은

```math
\frac{\partial S_{\mathrm{config}}}{\partial \theta}
=-R\ln\frac{\theta}{1-\theta}
=R\ln\frac{\xi}{1-\xi}.
```

따라서 단일 전이 지배 영역에서는

```math
\frac{\partial U}{\partial T}
=\frac{1}{F}
\left[
\Delta S^0_j
R\ln\frac{\xi_j}{1-\xi_j}
\delta S_{\mathrm{vib/e}}(\xi_j)
\right].
```

여러 전이가 겹치면 Ch2의 전하보존 음함수 미분으로

```math
\frac{\partial U_{\mathrm{oc}}}{\partial T}(x)
=
\frac{
\sum_j Q_j g_j(x)
\left[
\Delta S^0_j/F+(R/F)\ln(\xi_j/(1-\xi_j))
\right]
}{
\sum_j Q_j g_j(x)
},
\qquad
g_j=\frac{\xi_j(1-\xi_j)}{w_j}.
```

마지막에

```math
\dot Q_{\mathrm{rev}}
= -I T\frac{\partial U_{\mathrm{oc}}}{\partial T}
```

을 붙인다. 단, 위 마지막 부호는 2.3의 convention box에 종속된다.

### 2.5 비가역 옵션

P4 열모델로 확장할 때 비가역항은 Ch1의 동역학과 분극에서 온다.

```math
\dot Q_{\mathrm{irr}}
= I\eta_{\mathrm{cell}}
```

cell-level로는 `eta_cell=E-V >= 0`이다. 음극 half-cell 내부에서는 Ch1의 `V_n=V_app-sigma_d |I| R_n`, 분기 중심, `L_V` 꼬리, 히스 gap이 비가역 energy loss로 들어가며, entropy production 조건은

```math
\dot S_{\mathrm{irr}}=\frac{\dot Q_{\mathrm{irr}}}{T}\ge 0
```

을 만족해야 한다. 히스 gap `Delta U_hys`는 `partial U/partial T`에 섞는 값이 아니라 loop area 또는 effective overpotential로 분리해야 한다.

---

## 3. 부호·차원·극한 적대검산

### 3.1 차원

| 식 | 차원 |
|---|---|
| `Delta S = F partial U/partial T` | `[C/mol][J/C/K]=J/mol/K` |
| `q_rev = -I T partial U/partial T` | `[C/s][K][J/C/K]=W` |
| `Delta S_config = R ln(xi/(1-xi))` | `J/mol/K` |
| `g_j=xi(1-xi)/w_j` | `1/V`, `Q_j g_j = C/V` |
| `I(E-V)` | `[C/s][J/C]=W` |

### 3.2 부호

| 상황 | cell-level `q_rev=-IT dE/dT` | 해석 |
|---|---|---|
| `Delta S_cell>0` | `q_rev<0` | 방전 중 가역 흡열 |
| `Delta S_cell<0` | `q_rev>0` | 방전 중 가역 발열 |
| full-cell 음극 몫 `E=U_p-U_n` | `q_rev,n=+IT dU_n/dT` | cell-level 분해 시 음극 부호 반전 |
| Ch2 half-cell 식 | convention 명시 전까지 미결 | 현재 본문에는 충돌 가능성 |

### 3.3 극한

1. `I -> 0`: `q_rev -> 0`, `q_irr -> 0`. 열률은 0으로 간다. 단 `partial U/partial T` 자체는 남는다.
2. `Delta S -> 0`: `partial U/partial T -> 0`, 가역열 0. Ch1/Ch2의 `3->2L` 중심값이 이 극한 anchor다.
3. `xi -> 1`: `R ln[xi/(1-xi)] -> +infty`. 실제 계산에서는 전이 꼬리/측정 window/피팅 폭이 이 발산을 자른다.
4. `xi -> 0`: config 항은 음의 발산. 마지막 Li를 넣는 쪽의 배열 선택지 소멸과 정합한다.
5. `Omega -> 2RT^-`: 단상 평형 폭 지위. `Omega -> 2RT^+`: plateau/델타가 생기고 실측 폭은 broadening 지위로 넘어간다.
6. `rho(U_app)->delta(U_app-U_j)`: Ch1 ensemble broadening이 사라져 두-상 폭의 앙상블 몫이 0으로 환원된다.

---

## 4. v3 survey 좋은 요소 통합

v3 survey에서 P3에 유지해야 할 요소:

1. **정전 사슬**: `Delta S=+nF partial U/partial T`, `q_rev=-IT partial U/partial T`는 Newman/MSMR/Bernardi 축으로 삼각검증됐다. Ch2 v1.0.10도 이 사슬을 이미 쓴다.
2. **문헌 anchor**: Allart 2018 full-text 기준 흑연 전극 `Delta S(x)`의 양 끝 `+29 J mol^-1 K^-1 @ x=0.08`, `-16 J mol^-1 K^-1 @ x>0.5`가 Ch1 `+29 -> ... -> -16`과 정량 대응한다.
3. **신규성/공백의 정직한 위치**: MSMR은 `OCV(T)`/reaction별 `dU_j^0/dT` template를 제공하지만, Ch1식 다온도 `dQ/dV` peak shift에서 직접 `partial U_j/partial T`를 뽑는 경로는 명시 선례가 약하다. 이것은 결함이 아니라 P3/P4의 기여 지점이다.
4. **반응 entropy vs activation entropy**: `Delta S_rxn`은 가역열 원천, `Delta S_a`는 Eyring 꼬리의 prefactor/kinetic 항이다. Ch2 L423-427은 이 구분을 이미 잘 반영한다.
5. **히스테리시스 경계**: 히스 경로의존은 `Delta S` 측정 불확실도의 source다. Ch2 파생 D처럼 충/방전 평균 또는 평형 기준을 명시하고, 히스 gap은 비가역열로 분리해야 한다.

v3에서 그대로 가져오면 안 되는 요소:

1. `50_report.md`의 “저-x 양 `Delta S`(방전 발열)” 문장은 현재 Ch2의 `q_rev=-IT dU/dT` 해석과 반대다. convention이 다른 문장으로 보이며, Ch2 본문에 무비판적으로 재유입하면 안 된다.
2. Bernardi 원전은 v3 survey에서 snippet/2차 tier였고, 부호는 MSMR/Newman으로 보강해 확정준함 처리했다. supplement는 “Bernardi 원문 직접 page 확인 완료”처럼 쓰면 안 된다.
3. Electrochim. Acta 2019는 dQ/dV -> partial `Delta S/Delta H` prototype 후보이나 full text 미확보다. Ch2 본문에 식까지 확정된 선례처럼 쓰면 안 된다.

---

## 5. v5 검토분 타당성 판정

### 5.1 Ch1 v5/v5RR에서 가져올 작업 원칙

`PHASE_V5_RESULT.md`와 `PHASE_V5RR_ROUNDS_RESULT.md`는 Ch1 v5 검토 자료라 Ch2 발열 물리의 직접 원천은 아니다. 그러나 다음 원칙은 P3 supplement 작성에 유효하다.

1. 식을 보존하고 산문을 압축하더라도, 수식 사이의 인과 다리가 끊기면 보강 대상이다.
2. `식 N -> 선행식 전체 -> 부호/차원/극한` 루핑으로 검증한다.
3. 물리 오류 0과 “산문 다리 손실”은 구분한다.
4. 기존 식·기호·명칭은 임의 변경하지 않는다.

### 5.2 Ch2 v5 본체의 타당한 핵심

Ch2 v5의 가장 중요한 정정은 `w_eff(Ω)=w(1-Ω/2RT)` 식의 제거다. 이 정정은 타당하다.

근거:

1. 코드 v1.0.10도 `use_w_eff` 제거로 면적 보존을 회복했다(P1 audit L347).
2. Ch1 broadening 절은 두-상 흑연 peak 폭이 평형 narrowing이 아니라 `U_app=U_j+eta` broadening을 흡수한 현상학적 폭이라고 확정한다.
3. Ch2 L539-568, L676-683도 같은 결론을 반복한다.

판정:

```text
v5의 w_eff 제거와 두-상 폭 지위 정정은 확정 채택.
```

### 5.3 Ch2 v5에서 보강해야 할 핵심

1. `q_rev` 부호 convention box가 필요하다.
2. Ch2 L651-653의 부호 설명은 수식상 맞더라도 문장 구조가 흐릿하다. 아래처럼 정리하는 편이 낫다.

```math
\Delta G=-FU,\qquad
\Delta S=-\frac{\partial\Delta G}{\partial T}
=F\frac{\partial U}{\partial T},
\qquad
\dot Q_{\mathrm{rev}}=-IT\frac{\partial U}{\partial T}
=-\frac{IT}{F}\Delta S.
```

3. full-cell 음극 기여와 half-cell OCV 기여의 부호가 다른 이유를 분리해야 한다.
4. electronic 항은 Ch1의 LCO MIT 이론과 맞지만, 현재 코드에는 없다. “Ch2가 코드와 정합”이라고만 쓰면 과잉이다. 정확한 판정은 “이론은 Ch1과 정합, 구현은 P4”다.

---

## 6. 본문 삽입 후보

### 6.1 `sec:revheat` 앞 부호 convention box

```latex
\begin{warnbox}
\textbf{부호 convention.}
본 절의 $\dot Q_\rev=-IT\,\partial U_\oc/\partial T$ 는
$U_\oc$ 를 \emph{하프셀 OCV} 로 보고, $I>0$ 를 그 하프셀의
방전 convention 으로 정의한 Bernardi cell-level 식이다.
full cell 로 조립해 $E=U_p-U_n$ 를 쓰면 음극 몫은
$-IT\,\partial(-U_n)/\partial T=+IT\,\partial U_n/\partial T$
로 부호가 반전된다. 따라서 하프셀 발열, full-cell total, full-cell
음극 contribution 을 같은 기호 $U$ 로 섞지 않는다.
\end{warnbox}
```

### 6.2 `eq:qrev` 직후 식->식 다리

```latex
\[
\Delta G=-FU_\oc,\qquad
\Delta S=-\left(\frac{\partial \Delta G}{\partial T}\right)_x
=F\left(\frac{\partial U_\oc}{\partial T}\right)_x,
\]
\[
\dot Q_\rev=-IT\left(\frac{\partial U_\oc}{\partial T}\right)_x
=-\frac{IT}{F}\Delta S(x).
\]
```

### 6.3 코드 경계 문장

```latex
현재 \texttt{Anode\_Fit\_v1.0.10.py} 는
$U_j(T)=(-\Delta H_{\rxn,j}+T\Delta S_{\rxn,j})/F$ 와
$\Delta S_a$ 를 각각 평형 중심과 동역학 꼬리에 사용하지만,
$\dot Q_\rev$, self-heating, $dT/dt$ 는 계산하지 않는다.
따라서 본 장의 발열식은 P4 코드 구현의 이론 사양이며,
현재 코드 검증 항목으로 완료 보고하지 않는다.
```

---

## 7. 확정 / 미결 / 근거 미발견

확정:

- Ch2의 `Z -> occupation -> S_config/vib/electronic -> partial U/partial T -> q_rev` 큰 사슬은 Ch1/코드 입력 구조와 정합한다.
- 코드에는 `dS_rxn`과 `dS_a`가 있지만 `q_rev`, self-heating, `dS_e` 구현은 없다.
- `w_eff` 제거와 두-상 폭의 현상학적 지위는 Ch1 broadening 및 P1 code audit와 정합한다.
- `Delta S_rxn`과 `Delta S_a`는 구분해야 하며 가역열에는 `Delta S_rxn`만 들어간다.

미결:

- Ch2 본문에서 `I>0 방전`과 `U_oc`가 half-cell OCV인지 full-cell 음극 contribution인지 명시되어야 한다. 명시 전에는 저-`x` 양 `Delta S`의 흡열/발열 해석이 충돌한다.
- 다온도 `dQ/dV` peak shift로 `partial U_j/partial T`를 직접 추정하는 정확도는 후속 round-trip 검증이 필요하다.
- 히스테리시스 하 `partial U_oc/partial T`의 불확실도 정량은 아직 문헌 수치가 미확보다.

근거 미발견:

- 현재 코드에서 `q_rev` 또는 열방정식 `dT/dt`를 계산한다는 근거.
- 현재 코드에서 LCO MIT electronic entropy `dS_e`가 구현됐다는 근거.
- Ch2 v5의 `q_rev` 부호가 full-cell 음극 contribution convention까지 자동으로 커버한다는 근거.

