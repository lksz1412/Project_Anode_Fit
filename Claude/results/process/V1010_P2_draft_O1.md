# V1010 P2 Ch1 정련 supplement — 드래프트 O1 (작업 sub)

> **역할·범위**: Anode_Fit v1.0.10 P2 챕터1 9종 경쟁 드래프트 O1(작업 sub). 본 문서는 *드래프트*다 — 문건(`graphite_ica_ch1_v1.0.10.tex`)·코드(`Anode_Fit_v1.0.10.py`)를 수정하지 않는다(통합은 master). 범위 밖 자의 X. 허위 attribution X. 독립 작성.
> **목표**: Ch1 을 "코드 플로우차트(P1 맵 N0→N9)를 충실히 설명하는 물리화학 교과서"로 정련하는 supplement. 산출 = ① Ch1↔코드 1:1 coverage 매트릭스 ② 누락 유도·다리 보완 초안 ③ ★LCO 이론 정련안(중점).
> **입력 정독 범위**: tex 전문(1847줄, 절·식·표·그림 라벨 전수 grep cross-check) · `V1010_P1_code-audit_RESULT.md`(11항목 result + §1 맵 24심볼 + §2 audit 12식 + §3 인벤토리) · `broadening_w_design.md`(P2 설계) · `ORIGIN_VERDICT.md`(broadening 원인 4-tier).
> **표기(4-tier)**: [확정]=코드·식 직접 줄근거 / [근거 미발견]=코드·문헌으로 못 짚음 / [추정]=설계 의도 추론(근거 명시) / [미검증]=수치 미실행.
> **물리 적대검산 규약**: 각 보완·정련 초안은 부호·차원·극한 셋을 자체 검산한다(아래 각 항 "적대검산" 줄).

---

## §A. Ch1 ↔ 코드 1:1 coverage 매트릭스 (P1 맵 각 step ↔ Ch1 절·식, 누락·과잉 식별)

### A-0. 매트릭스 구성 원칙
P1 맵(`V1010_P1_map_v10.md` §1)의 노드 N0→N9 + 24심볼 + 12 closed-form 식을, Ch1 tex 의 절(`sec:`)·식(`eq:`)·표(`tab:`)에 1:1 로 건다. 한 행 = 하나의 코드 step. 열 = [코드 step·줄] / [물리식(P1)] / [Ch1 절] / [Ch1 식] / [coverage 판정]. coverage 판정 5등급: **충족**(코드 step ↔ Ch1 식 1:1) / **과잉-A**(Ch1 이 코드에 없는 항을 추가 — 단 후속 chapter·plug-in 예고로 정당) / **과잉-B**(Ch1 이 코드에 없는 항을 추가 — 정당성 미확인) / **누락**(코드 step 에 대응 Ch1 식 부재) / **부분**(대응은 있으나 다리·유도 끊김).

### A-1. 노드 매트릭스 (N0→N9, 코드 forward 골격)

| # | 코드 step (P1 줄) | 물리식 (P1 맵) | Ch1 절 | Ch1 식 | 판정 |
|---|---|---|---|---|---|
| N0 | `curve`→`_direction_to_sigma`, `\|I\|=c_rate·Q_cell` (L483-524) | σ_d 매핑·전류 환산 | sec:notation | eq:n0map | **충족** |
| N1 | `V_n=V_app−σ_d\|I\|R_n` (dqdv L408) | 분극 | sec:pol | eq:vn (유도 eq:vapppol→eq:vnmid) | **충족** |
| N1b | 작업격자 `V_work`·`T_work` (L410-425) | 패딩 linspace·비등온 보간 | sec:pol §작업격자 | eq:vwork | **충족** |
| N2 | `func_U_j=(−ΔH+TΔS)/F` (L78, dqdv L434) | 평형 중심 | sec:center | eq:Uj (유도 eq:gibbsdef→eq:eqcond→eq:Ujmid) | **충족** |
| N3 | `func_U_branch=U_j+½σ_d h_η γ ΔU_hys` (L143-148, dqdv L447) | 분기 중심 | sec:hys | eq:Ubranch·eq:center (유도 eq:mu→eq:spinodal→eq:dUhys) | **충족** |
| N3-gap | `func_dU_hys` (L133-140) | spinodal gap | sec:hys §gap | eq:dUhys (유도 eq:Veq→eq:hyssub→eq:hysdiff) | **충족** |
| N4 | `_width`→`func_w=nRT/F` (L74-75, L281-284); `_n_factor`(L272-278) | 폭 (이중지위) | sec:width §폭 | eq:wbase | **충족**(+이중지위 설명 sec:width·sec:broadening) |
| N5 | `func_ksi_eq=logistic[σ_d(V−U)/w]` (L94-97, dqdv L455) | 평형 점유 | sec:width §logistic | eq:xieq (유도 eq:bv→eq:db→eq:logisticsolve) | **충족** |
| N6 | `peak_shape=ξ_eq(1−ξ_eq)/w` (L464; equilibrium L366) | 평형 peak | sec:eqpeak | eq:eqpeak (유도 eq:belliden) | **충족** |
| N7-A | `A=min(z_cut·n·RT, A_cap·RT)` (L331) | 컷 affinity | sec:lag §컷 | eq:Acut | **충족** |
| N7-χ | `func_chi_d` (L158-163); `func_dH_a_eff=ΔH_a−χ_d Ω` (L152-155) | 방향별 χ_d·유효장벽 | sec:lag §전달계수 | eq:chid·eq:dHeff | **충족** |
| N7-Lq | `func_L_q` (L100-107, dqdv L342) | 지연 길이(전하축) | sec:lag §L_q | eq:Lq·eq:kuniv·eq:Lqfull (유도 eq:Lqmid→eq:Lqmid2) | **충족** |
| N7-LV | `L_V=\|dVdq_qa\|·L_q` (L347) | 전압축 환산 | sec:lag §L_V | eq:LV | **충족** |
| N8-mem | `_causal_lowpass` IIR `y=ρy+(1−ρ)x` (L110-128) | 인과 저역통과 | sec:tail §지수기억 | eq:lowpass (유도 eq:intfactor→eq:memory) | **충족** |
| N8-peak | `peak_shape=(ξ_eq−ξ_lag)/L_V` (L475) | 지연 꼬리 | sec:tail §peak모양 | eq:peakshape | **충족** |
| N8-branch | `L_V<ν·Δ_grid → 평형종 else 꼬리` (L462-475) | 분기 스위치 | sec:tail §peak모양 | eq:branch | **충족** |
| N8-rev | 충전 격자역전 `lowpass(ξ[::-1])[::-1]` (L470-473) | 인과 방향 | sec:tail §격자역전 | eq:reversal | **충족** |
| N9 | `dqdv_work += Q·peak_shape`; `np.interp(V_n←V_work)` (L477-480) | 합산·역보간 | sec:sum | eq:sum | **충족** |

### A-2. equilibrium 메서드(별도 진입점) 매트릭스

| 코드 step (P1 줄) | 물리식 | Ch1 절·식 | 판정 |
|---|---|---|---|
| `equilibrium` `dQ/dV=C_bg+ΣQ_j ξ_eq(1−ξ_eq)/w` (L350-367) | |I|→0 평형 peak (히스·동역학 없음, 방향 불변) | sec:eqpeak eq:eqpeak; sec:sum facade 언급(L1750-1754) | **충족** — 단 A-4 누락①(T 스칼라 전용 미서술) 참조 |

### A-3. LCO plug-in 매트릭스 (코드에 **없는** 항 — 과잉-A 판정 = 후속 plug-in 예고로 정당)

P1 §2-E 가 코드의 LCO·발열·전자엔트로피 부재를 [확정](`grep "LCO|cathode|발열|dS_e"`→No matches)했다. Ch1 의 LCO 절들은 **코드에 대응 step 이 없는 추가 이론**이다. 이 행들은 "코드를 설명"하지 않고 "같은 골격을 LCO 로 확장"하므로, coverage 매트릭스에서 별도 분류한다.

| Ch1 절 | Ch1 식 | 코드 대응 | 판정 | 정당성 근거 |
|---|---|---|---|---|
| sec:lco-map (LCO 전이표) | tab:lco-staging | 없음 (코드 GRAPHITE 전용) | **과잉-A** | "파라미터 교체"로 같은 dict 키 구조 재사용(sec:lco-code (i)); MSMR 동형 eq:msmr 근거 |
| sec:lco-center (∂U/∂T) | eq:lco-dUdT | `func_U_j` 동일식 재사용 | **충족(식)+과잉-A(값)** | 식·부호는 eq:Uj 미분으로 전극 불문 1:1; 값만 LCO 입력 |
| sec:lco-hys (order-disorder·MIT 2상) | eq:dUhys·eq:Ubranch 재사용 | `func_dU_hys` 동일식 | **충족(식)+과잉-A(적용처)** | 격자기체 틀이 "동등 자리 차고 빔" 가정만 쓰므로 LCO Ω-값만 교체 |
| sec:lco-electronic (전자 엔트로피) | eq:dSe·eq:dSemolar·eq:dSegate | **없음** (코드 0) | **과잉-A** | sec:lco-code (ii) "한 줄 plug-in" 예고 = P4 코드개정 후보. **★중점 §C 가 이 정당성을 교재급으로 갈고닦음** |
| sec:lco-decomp (ΔS 삼분해) | eq:lco-decomp | `func_U_j` 의 ΔS 슬롯 내부 분해 | **과잉-A** | 식·코드 경로 불변, ΔS *내부 분해*만 추가 |
| sec:lco-code (MSMR 동형) | eq:msmr | 없음(구조 논증) | **과잉-A** | 구조 변경 0 논증 = P4 plug-in 설계 근거 |
| sec:lco-peak (LCO 세 봉우리) | eq:eqpeak 재사용 | 없음(파라미터) | **충족(식)+과잉-A(적용)** | 평형 peak 식 전극 불문 |

→ **A-3 결론**: LCO 절 7개는 전부 **과잉-A**(코드 미구현이나 후속 plug-in 예고로 정당). **과잉-B(부당한 과잉)는 0건.** Ch1 헤더·P1 §2-E·P1 Open Issues 가 "LCO = 후속 develop, 코드 P4 후보"로 일관 선언하므로 self-consistent. 단 §C 가 그 plug-in 의 물리 무결성을 강화할 여지를 갖는다(아래).

### A-4. ★ 누락·과잉 식별 (coverage 결손)

P1 §4 가 "9 드래프트 전부 놓친 보완 4건"을 명시했다. 이 중 **Ch1 본문에 서술이 없거나 약한 것**을 누락으로 분류한다(코드 거동 ↔ Ch1 설명의 비대칭).

**누락 (코드 거동인데 Ch1 본문 미서술/약함):**

- **누락① [확정] — `equilibrium` 의 T 스칼라 전용성**. 코드: `equilibrium`은 L352 `T=_finite_pos("T",T)`로 **배열 T(V) 미지원**(dqdv 는 L402-424 `T_is_array` 분기로 비등온 지원). Ch1: sec:pol(L386-387)이 dqdv 의 비등온 보간(`T_work`·`T_rep`)은 서술하나, **equilibrium 이 그 능력을 갖지 않는다는 비대칭은 어디에도 없다**. facade 절(L1750-1754)도 equilibrium 을 "|I|→0 한계"로만 적고 온도 제약 무언급. → **보완 §B-1 초안** 제공.
- **누락② [확정] — 꼬리 활성/비활성 경계의 해상도 의존**. 코드: `n_work=max(n_work_min, V_n.size*2)`(L412) → 분기 문턱 `L_V<ν·Δ_grid`의 `Δ_grid=v_span/n_work`가 **사용자 V 점수에 종속**. 같은 물리 L_V 라도 입력 V 해상도에 따라 평형종/꼬리종이 갈린다. Ch1: eq:branch(sec:tail)는 문턱 `ν Δ_grid`를 적으나 **Δ_grid 가 사용자 입력에 의존한다는 사실**은 미서술 — 독자가 "ν=2 칸"을 절대 물리 문턱으로 오독할 위험. → **보완 §B-2 초안** 제공.
- **누락③ [부분] — `_resolve_lag_length` 우선순위 사다리**. 코드(L303-347): ① `'L_V'` 직접지정(L313-318, 동역학 전부 우회) → ② `I≤0 or 'dH_a' 부재 → 0`(L319-320) → ③ 동역학 산출. Ch1: sec:lag(L1435-1436)이 "직접 L_V 우회·I≤0·dH_a 부재→0"을 *한 문장*으로 언급하나, **세 단계 사다리의 우선순위 구조와 "L_V 직접지정이 dH_a/chi/Omega/z_cut/dVdq_qa 를 전부 우회"(P1 §2-C silent-off)는 미명시**. 피팅 시 과식별 함정. → **보완 §B-3 초안** 제공.

**과잉 (Ch1 식인데 코드 미구현 — A-3 외 추가):**

- **과잉-A② [확정] — `func_U_j_hys` 死코드의 Ch1 비대응**. 코드(L82-91): `func_U_j_hys`는 **미호출 死코드**(P1 §2-D, grep 호출 0; 실 분기중심은 `func_U_branch` L447). Ch1: sec:hys 는 분기중심을 `func_U_branch`/eq:Ubranch 로만 서술하고 死코드 `func_U_j_hys`는 *언급조차 안 함* — 이는 **올바른 누락**(死코드를 교과서에 넣지 않음)이라 과잉 아님. P1 §1.2 가 死코드로 [확정] → Ch1 의 미언급은 정합. **판정: 과잉 아님, 정합.**
- **과잉-A③ [확정] — z_cut docstring 부정확의 Ch1 정확성**. P1 §2-D C1: 코드 docstring(L217) "ξ_eq 5%"는 부정확(실제=정규화 미분 ξ(1−ξ)/0.25 의 5%, ξ_eq 자체 98.73%). Ch1: sec:lag(L1368-1370, eq:Acut 직전)은 **"점유 ξ_eq 자체가 아니라 미분 기준"으로 정확히 적음**. → **Ch1 이 코드 docstring 보다 정확**(코드가 Ch1 에 맞춰야 = P4 docstring 정정 후보). 과잉 아님, Ch1 우위 정합.

**과잉-B(부당) 식별 결과: 0건.** Ch1 의 모든 추가 항(LCO·전자엔트로피·broadening 설명)은 후속 chapter·plug-in 예고 또는 코드 거동의 정확한 물리 해설로 정당. 코드에 있는데 Ch1 에 없는 *물리식*도 0(死코드·docstring 부정확 2건은 Ch1 의 *올바른* 비대응).

### A-5. 매트릭스 한 줄 결론
**N0→N9 forward 골격 17 step + equilibrium 1 step = 18 코드 step 전부 Ch1 식에 1:1 충족.** 12 closed-form 식(P1 §2-A) 0 누락. **누락 3건**(equilibrium T 스칼라·해상도 의존·resolver 사다리)은 코드 *거동*의 설명 결손이지 *식* 결손이 아니다 → §B 가 본문 다리로 보완. **과잉-A 9건**(LCO plug-in)은 후속 예고로 정당, **과잉-B 0건**. 死코드·docstring 2건은 Ch1 의 올바른 비대응.

---

## §B. 누락 유도·다리 보완 초안 (물리화학 교재·식→식 사슬 끊김 0)

> 본 절의 초안은 Ch1 본문에 *삽입 후보*인 다리 단락이다. 어투·식 번호는 tex 양식에 맞춰 작성하되, 실제 삽입·식번호 배정은 master. 각 초안은 출발 전제→연산→중간식→결론 4단계와 자체 적대검산을 단다.

### B-1. equilibrium 의 T 스칼라 전용성 — facade 절 다리 초안 (누락①)

**삽입 위치 후보**: sec:sum 의 "facade 와 전체 진행 한눈에"(L1750 부근), `equilibrium` 을 "|I|→0 한계"로 적은 문장 뒤.

> **초안.** 기준선 `equilibrium` 은 식~eq:eqpeak 의 평형 종만 합산한 충방전 불변·히스 미반영 곡선이며, 그 입력 온도는 **스칼라(등온)에 한한다** — 코드가 진입 즉시 `T=_finite_pos("T",T)`로 온도를 양의 스칼라로 강제하기 때문이다. 이는 dqdv 와의 의도적 비대칭이다: dqdv 는 작업 격자 위에서 배열 온도 $T_\work(V)$ 를 보간해 비등온 $U_j(T_\work)$ 를 배열로 평가(식~eq:Uj 가 격자별)하지만, equilibrium 은 그 작업-격자·보간 기계장치를 거치지 않고 입력 전위에 직접 평형 종을 얹으므로 온도가 전위에 따라 변할 자리가 없다. 따라서 비등온 기준선이 필요하면 equilibrium 이 아니라 $|I|\to0$ 극한의 dqdv 를 써야 한다(같은 평형 종을 배열 $T$ 로 얻는다). 두 진입점의 평형 종 *식*은 동일(eq:eqpeak)하고, 갈리는 것은 *온도 정의역*뿐이다.

**적대검산(B-1)**: 부호 — 무관(서술적 제약). 차원 — 무관. 극한 — dqdv 의 $|I|\to0$ 이 equilibrium 과 같은 식 eq:eqpeak 로 수렴함은 Ch1 R3(L1824-1826, $L_V\propto|I|\to0$→평형종)이 이미 [확정]. **정합.** 근거: P1 §1.3 보완 2·§1.4 7축표 "격자/온도 — equilibrium T 스칼라 전용"[확정].

### B-2. 분기 문턱의 해상도 의존 — sec:tail eq:branch 다리 초안 (누락②)

**삽입 위치 후보**: eq:branch 직후, "ν=2 다(지연이 격자 두 칸보다 짧으면...)" 문장(L1529) 뒤.

> **초안.** 이 문턱이 절대 전위 폭이 아니라 *격자 칸 수* $\nu$ 로 적힌 것은 의도적이지만, 한 가지 종속성을 명시해야 오독을 막는다 — 격자 간격 $\Delta_\mathrm{grid}=\Delta v/n_\work$ 의 점 수 $n_\work=\max(n_{\work,\min},\,2|V_n|)$ 가 *사용자 입력 전위 격자의 점 수* $|V_n|$ 에 의존하므로(식~eq:vwork), 같은 물리 지연 $L_{V,j}$ 라도 입력 해상도가 높아 $\Delta_\mathrm{grid}$ 가 줄면 $L_V/\Delta_\mathrm{grid}$ 가 커져 꼬리 분기로, 낮으면 평형 분기로 갈릴 수 있다. 곧 문턱 $\nu\,\Delta_\mathrm{grid}$ 는 *물리 상수가 아니라 수치 해상도에 묶인 양*이다. 실용 함의 — 동역학 꼬리를 피팅으로 관측하려면 입력 $V_\app$ 격자를 충분히 조밀하게(또는 $n_{\work,\min}$ 을 키워) $\Delta_\mathrm{grid}\ll L_V$ 가 되게 해야 하며, 그러지 않으면 작은 seed $L_V$ 가 평형 종으로 접혀 꼬리가 *수치적으로* 사라진다(물리적 소멸 $|I|\to0$ 과 구별).

**적대검산(B-2)**: 부호 — $n_\work\uparrow\Rightarrow\Delta_\mathrm{grid}\downarrow\Rightarrow L_V/\Delta_\mathrm{grid}\uparrow$(단조, 정합). 차원 — $\Delta_\mathrm{grid}$[V]·$L_V$[V]·비 무차원(정합). 극한 — $n_\work\to\infty\Rightarrow\Delta_\mathrm{grid}\to0\Rightarrow$ 모든 유한 $L_V$ 가 꼬리 분기(평형종 접힘 소멸); 반대로 거친 격자는 평형종 다수. **정합.** 근거: P1 §1.3 보완 3·§2-F[확정]. **주의**: 이 다리는 "버그"가 아니라 "수치 해상도 종속성"으로 적어야 한다(P1 도 보고만, 코드 정정 X).

### B-3. resolver 우선순위 사다리 — sec:lag 다리 초안 (누락③)

**삽입 위치 후보**: sec:lag 의 "직접 지정 `'L_V'` 가 있으면 동역학을 우회..."(L1435) 문장을 확장.

> **초안.** 코드의 `_resolve_lag_length` 는 세 단계 우선순위로 $L_{V,j}$ 를 정한다. **(1) 직접 지정 우회** — 전이 dict 에 `'L_V'` 가 있으면 그 값을 그대로 쓰고 동역학 사슬 전부($\mathcal A,\chi_d,\Delta H_a^\eff,L_q,\code{dVdq\_qa}$)를 *우회*한다. 따라서 `'L_V'` 와 $(\Delta H_a,\Omega,\chi,z_\mathrm{cut},\code{dVdq\_qa})$ 를 *동시에* 지정하면 후자들은 꼬리에 반영되지 않으므로(과식별), 피팅에서 둘을 함께 자유화하면 안 된다. **(2) 평형 종 sentinel** — `'L_V'` 가 없고 $|I|\le0$ 이거나 동역학 키 $\Delta H_a$ 가 *부재*하면 $L_V=0$ 을 돌려 평형 종으로 떨어뜨린다(꼬리 끄기 신호). 단 $\Delta H_a=0.0$ 은 *부재가 아니므로*(키 존재) 이 분기에 걸리지 않고 동역학을 계산한다 — "꼬리를 끄려면 키를 빼야지 $0$ 을 넣으면 안 된다". **(3) 동역학 산출** — 위 둘에 안 걸리면 식~eq:Acut→eq:LV 의 사슬을 전이당 상수로 평가한다. 이 사다리가 "직접 지정 > sentinel > 동역학"의 순서임을 명시해 두면, 피팅 스코프 설계에서 어떤 키를 동시에 풀면 식별성이 붕괴하는지가 분명해진다.

**적대검산(B-3)**: 부호·차원 — 무관(제어 흐름 서술). 극한 — $|I|\to0\Rightarrow$ (2) sentinel 진입($L_V=0$, 평형종) = R3 환원과 정합; `'L_V'` 직접지정 시 (1) 이 (2)(3) 선행 → $|I|\to0$ 이어도 직접 $L_V$ 유지(테스트 우회 경로, P1 §2-C "L_V 직접 = dH_a 등 우회"[확정]). **정합.** 근거: P1 §1.3 `_resolve_lag_length`·§2-C silent-off[확정].

### B-4. (점검) 기존 본문 유도 사슬 — 끊김 0 확인 [확정]

P1 §2-A 가 12 closed-form 식의 코드 매핑을 [확정]했고, Ch1 각 식은 (a)출발→(b)연산→(c)중간식→(d)박스 4단계로 유도된다. 본 드래프트가 전수 정독한 결과, **본문 유도 사슬의 식→식 끊김은 0**이다. 대표 검증 3건:
- **eq:Uj** (sec:center): eq:gibbsdef($G=H-TS$)→eq:mudef($\mu=\partial G/\partial n$)→eq:eqcond(전기화학 평형 $\Delta G=-sFU$)→eq:Ujmid(ΔG 대입·이항)→eq:Uj. 끊김 0, 부호 일관(발열 $\Delta H<0$→중심 상승, L451-452 명시).
- **eq:xieq** (sec:width): eq:bv(Eyring 정·역 속도)→eq:db(비→detailed balance, χ 상쇄)→eq:logisticsolve(정지점 logit)→eq:xieq(폭 다중도·방향 일반화). 끊김 0, χ 합-1 제약이 detailed balance 강제(L756)로 명시.
- **eq:dUhys** (sec:hys): eq:mu(격자기체 μ)→eq:gxi(진행률 자유에너지)→eq:gpp(2계 미분)→eq:spinodal(g''=0 근)→eq:Veq(비단조 평형 전위)→eq:hyssub(spinodal 대입)→eq:hysdiff(극대−극소)→eq:dUhys. 끊김 0, artanh 항등식 명시(L607).

→ **본문 유도는 보완 불요**(끊김 0). §B 의 보완은 *유도 사슬*이 아니라 *코드 거동 설명*의 다리(누락①②③)에 한정된다.

---

## §C. ★ LCO 이론 정련안 (중점) — 양극 dQ/dV·전자 엔트로피의 교재급 정련

> P1 Open Issues·Next 가 "P2 = LCO·발열 이론 갈고닦기"를 명시. 본 절은 Ch1 의 LCO 절(sec:lco-electronic 중심)을 **물리 무결·유도 완결·비약 0**의 교재급으로 정련하는 초안이다. 코드 구현은 P4 예고(sec:lco-code (ii) 한 줄 plug-in). 각 정련 항은 [현 Ch1 진술]→[정련 초안]→[적대검산] 3단으로 적는다.

### C-1. v9 LCO 타당성 게이트 점검 — "왜 LCO 가 흑연 forward 틀에 들어오는가"의 무결성

**[현 Ch1 진술]** sec:lco-map·sec:lco-code 가 "MSMR 동형"(eq:msmr)으로 LCO 를 같은 logistic 합으로 적고, 부호 인자 $f=-\sigma_d$ 대응(L1678-1681)으로 흑연 eq:xieq 와 1:1 매핑. P1 §2-E 가 코드 LCO 부재를 [확정]하므로, 이 동형은 *코드 정합*이 아니라 *이론 확장의 타당성 논증*이다.

**[정련 초안 — 타당성을 세 전제로 분해]** LCO 가 흑연 forward 틀에 들어오는 정당성은 *암묵 가정 셋*에 달려 있고, 교재급 정련은 이 셋을 명시해 "어디까지 같고 어디서 갈리는가"를 못박는 데 있다.

1. **자리-등가 가정 (격자기체 보편성).** 흑연 eq:gxi 의 격자기체 자유에너지는 "동등한 자리에 리튬이 차고 빈다"는 가정만 쓴다(L519-520). LCO $\mathrm{Li}_x\mathrm{CoO_2}$ 의 리튬 층도 같은 2D 자리 격자이므로 *자리 등가*가 성립 → eq:mu→eq:dUhys 사슬이 Ω-값 교체만으로 LCO 에 이식된다. **이 가정의 한계**: order-disorder 초격자($x\approx0.5$ monoclinic)는 자리가 *비등가*(점유·빈자리 교대 정렬)가 되는 구간이라, 거기서는 격자기체 평균장이 1차 근사다 — 정련은 "T2·T3 의 $\Omega$ 는 평균장 유효값"임을 명시해야 한다(허위 정밀 차단).
2. **평형 조건의 전극 불문성.** eq:eqcond($\Delta G_j=-sFU_j$)는 *전극 가정 없이* 전기화학 평형에서 나오므로(L466-467), eq:Uj·eq:lco-dUdT 가 LCO 에 부호까지 1:1 (L482-483). **이것은 가정이 아니라 유도 결과** — 정련은 "LCO 중심식은 *새 가정 없이* 흑연 식의 입력 교체"임을 강조(tier A).
3. **전자 자유도의 추가성.** 흑연이 닫히는 두 몫(config+vib)에 LCO 는 전자 몫이 *더해진다*(eq:lco-decomp). 이 "추가성"이 §C-3 의 핵심이며, 그 정당성(직교성)이 LCO 타당성의 *유일한 비자명 가정*이다.

**[적대검산 C-1]** 부호 — eq:msmr 의 $f=-\sigma_d$: MSMR 지수 $+f(U-U_j^0)$ vs Ch1 지수 $-\sigma_d(V-U_j^d)$, 같은 자리 → $f=-\sigma_d$(L1680). 방전 $\sigma_d=+1\Rightarrow f=-1$: LCO 방전=리튬화($x\uparrow$, 전위 하강), eq:msmr 에서 $f=-1$ 이 $x_j$ 를 $U\downarrow$ 에 증가시킴 → 리튬화 시 점유 증가, 정합. 차원 — eq:msmr·eq:xieq 둘 다 지수 무차원(전위/폭). 극한 — $\Omega\to0$(이상 격자기체)면 LCO·흑연 둘 다 단일 Fermi 종으로 환원(eq:fermifn). **정합.** [확정](식 유도)+[추정](자리-등가 한계는 설계 판단, 근거=order-disorder 비등가성).

### C-2. LCO 양극 dQ/dV 세 봉우리 — 평형 peak 의 양극 적용 무결성

**[현 Ch1 진술]** sec:lco-peak: 평형 peak eq:eqpeak 가 전극 불문이므로 LCO 하프셀에 세 봉우리(T1 ~3.90V MIT·T2 ~4.05V·T3 ~4.17-4.20V). 폭 $w_j=n_jRT/F$, 세 전이 모두 $\Omega>2RT$ 두-상 → 폭은 sec:broadening 의 *두-상* 측(현상학적 피팅 폭).

**[정련 초안 — 세 봉우리의 물리 성격을 peak 3양으로 분해]** 평형 peak 의 세 양(위치=$U_j^d$, 순높이=$Q_j/(4w_j)$, 면적=$Q_j$, L1137-1139)을 LCO 세 전이에 *물리 성격과 함께* 적으면 교재급 자기완결이 선다.

| 전이 | 위치 $U_j^d$ | 폭 $w_j$ 지위 | 순높이 결정 | 면적 $Q_j$ | 전자항 |
|---|---|---|---|---|---|
| T1 (MIT, ~3.90V) | $U_1+½σ_d γ ΔU_hys^{(1)}$; **$\partial U_1/\partial T$ 가 $T$-선형**(전자항) | 두-상(MIT 2상역) → 현상학적 | $Q_1/(4w_1)$ | $x$=0.94→0.75 구간 용량 | **ON** (eq:dSegate 골) |
| T2 (o-d a, ~4.05V) | $U_2+½σ_d γ ΔU_hys^{(2)}$; 큰 $\Omega$→좁은 분기 | 두-상(order) → 현상학적·좁음 | $Q_2/(4w_2)$ 높음(작은 $w_2$) | $x$≈0.55 부근 | off |
| T3 (o-d b, ~4.17V) | $U_3+½σ_d γ ΔU_hys^{(3)}$; T2 와 한 쌍 | 두-상(order) → 현상학적·좁음 | $Q_3/(4w_3)$ | $x$≈0.48 부근 | off |

핵심 정련 두 가지: **(가)** order-disorder 의 큰 $\Omega$ 가 spinodal gap $\Delta U_j^\hys$(eq:dUhys)를 키워 T2·T3 분기를 흑연보다 *날카롭게*(좁은 한 쌍 peak) 만든다 — 이는 eq:dUhys 의 $\Omega\uparrow\Rightarrow u\to1\Rightarrow\Delta U^\hys\uparrow$ 단조성의 직접 귀결(아래 적대검산). **(나)** T1 의 관측 신호는 *위치 자체*가 아니라 *온도 이동률* $\partial U_1/\partial T$ 가 $T$-선형으로 커지는 것(전자항 $\Delta S_{e,1}\propto T$) — 위치 이동은 $\propto T^2$(L1153-1156). 이 "이동률 $T$-선형 ≠ 위치 $T$-선형" 구분이 교재급 정밀의 핵이며, §C-4 가 깊이 판다.

**[적대검산 C-2]** 부호 — $\Omega\uparrow\Rightarrow u=\sqrt{1-2RT/\Omega}\to1\Rightarrow\Delta U^\hys=\frac2F[\Omega u-2RT\,\mathrm{artanh}\,u]$: 큰 $\Omega$ 에서 $\Omega u$ 항이 $\mathrm{artanh}$ 발산보다 빠르게 커져 $\Delta U^\hys\uparrow$(단조 증가, 정합 — order 의 좁은 한 쌍 peak). 차원 — eq:eqpeak 순높이 $Q_j/(4w_j)$: [C]/[V]=C/V(dQ/dV, 정합). 극한 — $w_j\to0$(델타 극한)이면 순높이$\to\infty$·면적 보존 $Q_j$(P1 §0 면적적분=1.000 [확정]); order 의 좁은 peak 가 이 극한에 가까움. **정합.**

### C-3. ★★ 전자 엔트로피 정련 (최중점) — Fermi-Dirac→Sommerfeld→삽입당 ΔS_e

이 절이 본 supplement 의 물리적 핵이다. Ch1 sec:lco-electronic 의 유도(eq:fd→eq:Se→eq:dSe→eq:dSemolar→eq:dSegate)를 교재급으로 *재검*하고, 비약·부호·단위·이중계산 네 축에서 무결성을 강화한다.

#### C-3-a. 유도 사슬 재검 — 비약 0 점검

**[현 Ch1 유도]** (a) eq:fd Fermi-Dirac → (b) 정보 엔트로피 합 $-k_B\sum[f\ln f+(1-f)\ln(1-f)]$ → (c) Sommerfeld 전개로 $C_e=\frac{\pi^2}3 k_B^2 T g(E_F)$ → 적분 $S_e=\int_0^T(C_e/T')dT'$ → eq:Se $S_e=\frac{\pi^2}3 k_B^2 T g(E_F)$ → (d) eq:dSe 삽입당 $\Delta S_{e,j}=\partial S_e/\partial x$.

**[정련 점검 — 각 단계 비약 검사]**
1. **(a)→(b) [확정·무결]**: 입자 0/1 배타 점유라 자리당 2-state 정보 엔트로피. 흑연 $S_\mathrm{mix}$(eq:partfn 부근, sec:hys)와 *같은 꼴*임을 sec:dist 가 이미 다리 놓음(keybox L890-895). 비약 0.
2. **(b)→(c) Sommerfeld [정련 여지]**: 현 Ch1(L955-965)이 $g(E)\approx g(E_F)$ 동결을 명시하고 그 정당성(좁은 열폭 $\sim k_BT$·축퇴 $k_BT\ll E_F$)을 적음 — **무결**. 단 교재급 강화 여지: **표준 Sommerfeld 적분 $\int(-\partial f/\partial E)(E-E_F)^2 dE=\frac{\pi^2}3(k_BT)^2$ 의 *출처*를 한 줄 명시**하면 자기완결이 완성된다(아래 C-3-b 초안). 현 Ch1 은 적분값을 *주어진 것*으로 쓰는데, 타 전공 석박 독자에겐 이 적분이 "어디서 $\pi^2/3$ 가 오는가"의 비약으로 읽힐 수 있다 → C-3-b 가 메운다.
3. **(c) $C_e\to S_e$ 적분 [확정·무결]**: $C_e/T'=\frac{\pi^2}3 k_B^2 g(E_F)$ 가 $T'$ 무관 상수라 적분이 곧바로 닫힘(L963-965). 비약 0.
4. **(c)→(d) eq:dSe [확정·무결]**: $S_e$ 의 $x$ 미분(삽입당). $g(E_F,x)$ 의 $x$ 의존이 유일한 조성 의존. 비약 0.

→ **유도 사슬 무결, 단 (b)→(c) Sommerfeld 적분 출처 한 줄이 교재급 자기완결의 마지막 다리.**

#### C-3-b. Sommerfeld 적분 출처 다리 — 삽입 초안 (C-3-a 점검 2 보완)

**삽입 위치 후보**: sec:lco-Se (c) 의 "표준 Sommerfeld 적분 $\int(-\partial f/\partial E)(E-E_F)^2 dE=\frac{\pi^2}3(k_BT)^2$" 문장 앞.

> **초안.** 이 적분이 $\frac{\pi^2}3(k_BT)^2$ 로 닫히는 것은 Sommerfeld 전개의 표준 결과다 — 축퇴 극한에서 $-\partial f/\partial E$ 는 $E_F$ 에 중심을 둔 폭 $\sim k_BT$ 의 종(우함수)이고, 무차원 변수 $\eta=(E-E_F)/k_BT$ 로 바꾸면 적분이 $(k_BT)^2\int_{-\infty}^{\infty}\frac{\eta^2 e^\eta}{(1+e^\eta)^2}d\eta$ 가 되며, 이 표준 적분이 $\pi^2/3$ 다($\int_{-\infty}^{\infty}\eta^2\,(-\partial f/\partial\eta)\,d\eta=\pi^2/3$; 하한 $0\to-\infty$ 연장은 축퇴 극한에서 지수적으로 작은 오차). 곧 $\pi^2/3$ 는 자유전자 비열의 보편 상수이지 LCO 고유 값이 아니다 — LCO 가 정하는 것은 오직 $g(E_F,x)$ 한 인자다.

**적대검산(C-3-b)**: 부호 — 피적분 $\eta^2(-\partial f/\partial\eta)\ge0$(우함수·양), 적분 양수 → $C_e>0$(정합). 차원 — $(k_BT)^2$[J²]·$g$[1/J] → $C_e=\frac{\pi^2}3 k_B^2 T g$ 차원 $k_B^2 T g$=[J/K]²·[K]·[1/J]=[J/K](엔트로피·비열 차원, 정합). 극한 — $T\to0\Rightarrow C_e\to0$(3법칙 정합), $S_e\to0$. **정합.** [확정](교과서 표준 적분).

#### C-3-c. ★ 부호 규약 정련 — 삽입 기준 ΔS_e<0 의 무결성 (★최우선 결함 클래스)

**[현 Ch1 진술]** eq:dSe·L1002-1009: 삽입 기준 $\Delta S_{e,j}<0$, 탈리튬화 시 $|\Delta S_e|\approx0.18 k_B$/atom *방출*. 닫는 논리: 삽입($x\uparrow$)→금속→절연체→$g(E_F)$ $g_\max\to0$ 감소→$\partial g/\partial x<0$→eq:dSe $\Delta S_e=\frac{\pi^2}3 k_B^2 T\,\partial g/\partial x<0$.

**[정련 — 부호 사슬을 다섯 고리로 명시]** 이 부호가 교재급으로 falsifiable 하려면 다섯 고리가 *각각* 검증돼야 한다(P1 식 "★최우선 결함 클래스" 규율):
1. **물리 끝점**: $x=1$($\mathrm{LiCoO_2}$) Co³⁺ low-spin 닫힌 껍질 = 절연체 $g(E_F)\approx0$; $x=0$($\mathrm{CoO_2}$) metal $g(E_F)=g_\max\approx13$ e/eV (L938-940, L975 anchor [tier A 단일점]).
2. **조성 미분 부호**: 삽입 방향 $x\uparrow$ 로 metal→insulator 라 $g(E_F)$ *감소* → $\partial g/\partial x<0$ [확정, 끝점에서 직접].
3. **식 부호**: eq:dSe $\Delta S_{e,j}=\frac{\pi^2}3 k_B^2 T\cdot(\partial g/\partial x)$, 앞 인자 양수 → $\Delta S_{e,j}<0$ [확정].
4. **슬롯 일관**: 흑연 $2\to1$ 삽입 $\Delta S_\rxn=-16$ J/(mol·K)<0 슬롯과 *같은 삽입 기준 음수* → 부호 뒤집기 없이 plug-in (L1002-1009) [확정].
5. **방출 해석**: 삽입이 음이면 역과정(탈리튬화 $x\downarrow$, LCO 충전 주 진행)이 양 → $|\Delta S_e|>0$ 방출 [확정].

**핵심 정련 지적**: 현 Ch1 은 다섯 고리를 *서술로* 담으나, eq:dSegate 의 *leading 음부호*가 이 부호를 식 자체로 못박는다(L1042). 교재급 강화 = **다섯 고리를 한 검산 박스로 묶어** "끝점→미분부호→식부호→슬롯→방출"이 한 줄로 따라가지게(G-follow) 만드는 것. 이는 흑연 sec:signcheck(S1-S8) 와 같은 격의 *LCO 전자항 전용 부호 검산 박스* 신설 제안이다(아래 C-3-d).

**[적대검산 C-3-c]** 부호 — 다섯 고리 전부 음의 삽입 기준으로 일관(교차 모순 0). 차원 — eq:dSe 자리당 $k_B^2 T g$=[J/K], eq:dSemolar $N_A$ 곱해 몰당 [J/(mol·K)](C-3-e 단위 다리). 극한 — $x\to x_\mathrm{MIT}$ 에서 $\sigma(1-\sigma)$ 최대 $\frac14$→골 가장 깊음; $x$ 멀어지면 지수적 소멸(T1 국소화). **정합.**

#### C-3-d. LCO 전자항 부호 검산 박스 — 신설 초안 (C-3-c 정련)

**삽입 위치 후보**: sec:signcheck(S1-S8 흑연 부호 사슬) 뒤 또는 sec:lco-electronic 말미에 verifybox 로.

> **초안 (verifybox: LCO 전자 엔트로피 부호 사슬).** 흑연 부호 사슬(S1-S8)과 같은 격으로, LCO 전자항의 삽입-기준 부호를 전건 검산한다 — 기준 명제 = *삽입($x\uparrow$, LCO 방전) 시 전자 엔트로피 음의 골, 탈리튬화($x\downarrow$, LCO 충전) 시 $|\Delta S_e|>0$ 방출*.
> - **E1. 끝점.** $g(E_F)\!: 0\,(x{=}1,\text{절연체})\to13\,\text{e/eV}\,(x{=}0,\text{metal})$. anchor tier A 단일점.[motohashi2009]
> - **E2. 미분.** 삽입 $x\uparrow$ 로 metal→insulator → $\partial g/\partial x<0$. $\checkmark$
> - **E3. 식.** eq:dSe $\Delta S_{e}=\frac{\pi^2}3 k_B^2 T\,\partial g/\partial x<0$(앞 인자 양). $\checkmark$
> - **E4. 게이트.** eq:dSegate leading $-$ 가 $\Delta S_e<0$ 을 식으로 못박음($g_\max,\Delta x_\mathrm{MIT},\sigma(1-\sigma)$ 모두 양). $\checkmark$
> - **E5. 슬롯.** 흑연 $2\to1$ 삽입 $-16$ J/(mol·K)<0 과 같은 삽입-기준 음수 → 부호 뒤집기 0. $\checkmark$
> - **E6. 단위.** 자리당 $\to$ 몰당 $N_A$ 곱(eq:dSemolar, $N_A k_B^2=R k_B$); 부호 $N_A>0$ 불변. $\checkmark$
> - **E7. 크기.** $|\Delta S_e|\approx0.18 k_B$/atom = O3 부분몰과 동자릿수(L1067 [tier B]); config(>½ 지배 [tier A])보다 작으나 MIT 게이트로 필수. $\checkmark$
> 일곱 고리 전건 정합 — LCO 전자항 부호 사슬 PASS.

**적대검산(C-3-d)**: 박스 자체가 적대검산. 모든 고리 음의 삽입 기준 일관, 교차 모순 0. [확정](식)+[tier A/B 병기](anchor·크기).

#### C-3-e. 단위 다리 무결성 — 자리당 k_B → 몰당 R 재검

**[현 Ch1 진술]** eq:dSe 는 자리당($k_B^2$ 차원), forward 슬롯 $\Delta S_{\rxn,j}$ 는 몰당(J/(mol·K)). eq:dSemolar 가 $N_A$ 곱: $\Delta S_e^\mathrm{mol}=\frac{\pi^2}3 R k_B T\,\partial g/\partial x$ ($N_A k_B^2=R k_B$, L990-998). 단위 주의 경고(L1687-1689): $N_A$ 누락 시 $\sim10^{23}$ 배 과소.

**[정련 — 환산 항등식 명시 검산]** $N_A k_B^2=R k_B$ 는 $N_A k_B=R$(기체상수 정의)에서 양변 $k_B$ 곱. 곧 *자리당 $k_B$ 한 몫이 몰당 $R$ 로 올라가고 나머지 $k_B$ 한 몫은 자리당으로 남는다* — 그래서 eq:dSemolar 가 $R k_B$(혼합 차원)을 갖는다. 이는 오타가 아니라 **올바른 혼합 차원**: $S_e$ 의 두 $k_B$ 중 하나(엔트로피의 $k_B$)만 몰당 $R$ 로 환산되고, 다른 하나($g(E_F)$ 의 에너지 스케일 $k_BT$ 안의 $k_B$)는 자리당 에너지 스케일로 남기 때문이다. **교재급 정련 = 이 "왜 $R k_B$ 이고 $R^2$ 도 $k_B^2$ 도 아닌가"를 한 줄로 명시**(타 전공 독자의 가장 흔한 오독 지점).

> **초안.** $N_A k_B^2=R k_B$ 의 혼합 차원은 의도된 것이다 — $S_e=\frac{\pi^2}3 k_B^2 T g$ 의 두 $k_B$ 는 *역할이 다르다*: 하나는 엔트로피의 단위 $k_B$(정보 엔트로피 $-k_B\sum f\ln f$ 에서 온 것)이고, 다른 하나는 비열 적분의 열에너지 스케일 $k_BT$ 안의 $k_B$ 다. 몰당 환산은 *입자 수를 세는* 첫째 $k_B$ 만 $R=N_A k_B$ 로 올리고, *에너지 스케일*인 둘째는 자리당으로 남긴다 → $\frac{\pi^2}3 R k_B T g$. 따라서 $g(E_F)$ 가 e/eV 단위면 eV→J 환산($1.602\times10^{-19}$)을 함께 적용해야 최종 J/(mol·K) 가 닫힌다.

**[적대검산 C-3-e]** 차원 — $\frac{\pi^2}3 R k_B T g$: [J/(mol·K)]·[J/K]·[K]·[1/J]=[J/(mol·K)](정합, 슬롯 단위 일치). 부호 — $N_A>0$ 불변. 극한 — $N_A$ 누락 → $10^{23}$ 배 과소(L1689 경고와 정합). **정합.** [확정](항등식)+교재급 다리(혼합 차원 해설).

#### C-3-f. ★ 가법성·이중계산 정련 — 직교성 vs 무초과의 2층 논증

**[현 Ch1 진술]** eq:lco-decomp $\Delta S^\mathrm{cat}=\Delta S^\mathrm{config}+\Delta S^\mathrm{vib}+\Delta S_e^\mathrm{mol}$. L1647-1655 가 *(가) 가산성*(config·elec 직교 자유도 → $Z=Z_\mathrm{config}Z_\mathrm{elec}$ → $S=S_\mathrm{config}+S_\mathrm{elec}$)과 *(나) 무이중계산*(config 슬롯=봉우리 중심값만, elec 슬롯=MIT 게이트 골만)을 분리.

**[정련 — 2층 논증의 무결성 강화]** 이 분리는 교재급으로 매우 정밀하나, *직교성 근사의 한계*를 한 단계 더 명시하면 비약이 0 이 된다.
- **(가) 직교성 = "더해도 되는가"**: config(리튬 자리 배열 자유도)와 elec(전도 전자 밴드 점유 자유도)는 *서로 다른 힐베르트 공간*이라 독립 극한에서 $Z$ 인수분해 → $S$ 가산. **한계 명시 필요**: MIT 부근에서 리튬 정렬↔전자 밴드채움이 *결합*(Co 산화수가 리튬 점유와 전자 모두에 연결)하므로 교차항이 정확히 0 은 아니다. 현 Ch1(L1650-1652)이 "선도 차수에서 성립, 결합 몫은 (나)의 슬롯 분리로 통제"로 적음 — **무결, 단 "선도 차수"의 의미를 한 줄 보강**하면 완벽: 교차항은 $O(\partial^2 S/\partial(\text{config})\partial(\text{elec}))$ 크기로, MIT 게이트 폭 $\Delta x_\mathrm{MIT}$ 안에서만 비0 이고 그 적분 기여가 게이트 골의 고차 보정이라 forward 피팅의 $w_j$·$\gamma_j$ 자유도에 흡수된다.
- **(나) 무초과 = "과대 계상 없는가"**: 직교성이 *아니라* 슬롯 분리 규칙이 보장. config 슬롯에 봉우리 *중심 표준값* $\Delta S_j^0$ 만(봉우리 내부 조성 의존 $R\ln[(1-\xi)/\xi]$ 는 logistic 이 이미 자동 생성, L1642-1646), elec 슬롯에 MIT 게이트 골만. **이중계산 금지의 핵**: 같은 엔트로피를 logistic(config 내부)과 명시 항(config 중심값)이 두 번 세지 않게 하는 것 → "표~tab:lco-staging 의 config 값 = 중심 표준값으로 읽음"(L1646).

**[정련 결론]** 직교성(가산성)과 슬롯 분리(무초과)는 *논리적으로 독립한 두 보장*이다 — 전자는 "합이 의미 있는가", 후자는 "합이 측정값을 안 넘는가". 이 2층 구조를 명시하는 것이 교재급 정밀의 핵이며, 현 Ch1 이 이미 갖춘 구조다(L1655 명시). **정련 제안 = "선도 차수" 한 줄 보강만**(교차항 크기·흡수처).

**[적대검산 C-3-f]** 부호 — config 중심값(O3 양 [reynier2004])·elec 골(음, eq:dSegate)이 합산; 총 ΔS^cat 부호는 §C-4 verifybox(L496-503)가 "$+80$ 전체 vs T1 전자항 $-1.5$ J/(mol·K) 소수 보정 → 총 부호 불변"으로 [확정]. 차원 — 세 몫 전부 J/(mol·K)(슬롯 일치). 극한 — elec 골이 $\Delta x_\mathrm{MIT}$ 밖에서 소멸 → T1 외 전이는 config+vib 만(흑연과 동형). **정합.** [확정]+[추정](교차항 크기는 설계 논증, 근거=직교성 고차 보정).

### C-4. ★ 전자항의 T-선형성 — 식별 신호의 교재급 정밀

**[현 Ch1 진술]** L1010-1015·L1153-1156·fig:lco-electronic 캡션: $\Delta S_{e,j}\propto T$ 이므로 전자 기여 $\partial U_1/\partial T|_e=\Delta S_{e,1}/F\propto T$ 가 *T-선형*. 곧 *$\partial U_1/\partial T$ 의 기울기 자체가 $T$ 비례*이며, 적분한 위치 이동 $U_1$ 은 $\propto T^2$. "식별 신호는 *$\partial U/\partial T$ 가 $T$-선형*이지 *peak 위치가 $T$-선형*이 아니다."

**[정련 — 세 항의 T-의존 분리표]** 이 구분이 다온도 피팅의 식별성을 떠받치므로, 세 ΔS 성분의 T-의존을 *한 표*로 분리하면 교재급 자기완결이 선다.

| 성분 | $\Delta S(T)$ | $\partial U_j/\partial T=\Delta S/F$ | $U_j(T)$ 적분형 | 다온도 식별 신호 |
|---|---|---|---|---|
| config | $\Delta S^0$ (T-무관 상수) | 상수 | $U_j^0+(\Delta S^0/F)T$ (T-선형) | 위치가 $T$-선형 |
| vib | $\Delta S^\mathrm{vib}$ (T-무관 상수) | 상수 | T-선형 | config 와 합쳐 식별 |
| **electronic** | $\Delta S_e\propto T$ (T-선형) | $\propto T$ (기울기가 $T$-비례) | $\propto T^2$ | **$\partial U/\partial T$ 가 $T$-선형 (위치는 $T^2$)** |

핵심 정련: config·vib 는 $\Delta S$ 가 상수라 위치가 $T$-선형이지만, electronic 은 $\Delta S_e\propto T$ 라 *$\partial U/\partial T$ 가 $T$-선형이고 위치는 $T^2$*. 따라서 다온도 dQ/dV 에서 **T1 봉우리의 온도 이동률을 $T$ 에 대해 plot 했을 때 직선(기울기 비0)이면 전자항의 직접 증거**다 — config·vib 만이면 이동률이 $T$-무관 상수(수평선). 이 "이동률 기울기" 검사가 세 항을 분리 식별하는 1급 lever 이며, sec:lco-Se 의 "셋 중 유일하게 $\propto T$ 라 분리 식별"(L1661)을 정량화한다.

**[적대검산 C-4]** 부호 — $\Delta S_e<0$(삽입 기준) 이고 $\propto T$: $\partial U_1/\partial T|_e=\Delta S_e/F<0$ 이고 $|\partial U_1/\partial T|_e|$ 가 $T\uparrow$ 로 증가(이동률 음의 기울기 직선). 차원 — $\partial U/\partial T$[V/K]=$\Delta S$[J/(mol·K)]/$F$[C/mol]=[V/K](정합); $T$-선형 이동률 → $U\propto T^2$ 적분 차원 정합. 극한 — $T\to0\Rightarrow\Delta S_e\to0$(3법칙)→이동률 0; config·vib 는 $T\to0$ 에서도 상수 $\Delta S^0$(고전 격자 근사, 양자 보정 범위 밖). **정합.** [확정](식 미분)+[미검증](다온도 실측 plot 미수행 = 피팅 예고).

### C-5. ★ g(E_F,x) MIT-logistic 게이트 — 모델 가정의 교재급 정당화 재검

**[현 Ch1 진술]** eq:ggate $g(E_F,x)=g_\max[1-\sigma((x-x_\mathrm{MIT})/\Delta x_\mathrm{MIT})]$, 초기값 $g_\max=13$·$x_\mathrm{MIT}=0.85$·$\Delta x_\mathrm{MIT}=0.05$. eq:dSegate 가 게이트를 eq:dSe 에 대입한 닫힌식. L1047-1063 가 네 정당화(anchor·천이중심·폭·자기일관성).

**[정련 — 게이트의 세 구성요소 신뢰 등급 분리(허위 정밀 금지)]** sec:lco-Se(L970-979)가 이미 "함수형(tier A)·anchor 한 점(tier A)·연속 곡선(부재 G2)" 3분리를 갖췄다. 교재급 정련 = 이 등급 분리를 *게이트 파라미터별로* 다시 매핑:

| 게이트 요소 | 물리 근거 | 신뢰 등급 | 피팅 지위 |
|---|---|---|---|
| 함수형 $S_e=\frac{\pi^2}3 k_B^2 T g$ | Sommerfeld 표준(C-3-b) | **tier A** | 고정(유도) |
| $g_\max=13$ e/eV | $\mathrm{CoO_2}$ metal 측정 [motohashi2009] | **tier A 단일점** | 초기값 고정, 도핑 소폭 |
| $x_\mathrm{MIT}\approx0.85$ | MIT 2상역 0.75-0.94 중앙 [menetrier1999,reimers1992] | tier A→B(중앙 추정) | 피팅 |
| $\Delta x_\mathrm{MIT}\approx0.05$ | 2상역 폭 0.19↔logistic $\pm2\Delta x$; 결함 분산 | **tier B-C** | 피팅(결함 의존) |
| 연속 곡선 $g(E_F,x)$ | 1차 문헌 부재 (G2) | **근거 미발견** | logistic 가정→피팅 |

핵심 정련 두 가지: **(가) 왜 step 이 아니라 logistic** — 실 시료의 산소 결손·양이온 무질서가 MIT 발현 조성을 *분산*시키므로 0폭 step 은 비물리($\partial g/\partial x$ 가 델타 스파이크). logistic 의 유한 폭이 결함 분산을 *폭 하나*로 흡수(L1054-1059). **(나) 자기일관성** — eq:ggate 의 logistic 이 sec:dist 의 점유 분포 eq:fermifn 와 *같은 함수형* → 전자 띠가 열리는 천이를 Fermi-함수형 게이트로 적는 것은 전도 전자 점유가 Fermi-Dirac(eq:fd)인 것과 *한 언어*(L1060-1062). 이 "게이트 = 점유 분포의 자연 귀결" 논증이 게이트를 임의 곡선맞춤에서 구별하는 핵이다.

**[정련 제안 — eq:dSegate 의 종 항등식 다리 강화]** eq:dSegate 유도는 $\sigma'(z)=\sigma(z)[1-\sigma(z)]$ 종 항등식(eq:belliden 과 *같은 것*)·연쇄율 $\partial\sigma/\partial x=\sigma'/\Delta x_\mathrm{MIT}$ 를 씀(L1031-1034). 이는 흑연 평형 peak 의 종(eq:belliden)과 *동일 항등식*이라, "전자항 골의 모양 = 흑연 peak 종과 같은 logistic 미분 종"임을 명시하면 교재 통일성이 완성된다 — 곧 **$\Delta S_e(x)$ 골은 $g(E_F,x)$ 게이트의 logistic 미분이고, 그 미분 종은 eq:eqpeak 의 평형 peak 종과 같은 $\sigma(1-\sigma)$**. 한 항등식이 흑연 peak·LCO 전자항 골을 동시에 닫는다.

**[적대검산 C-5]** 부호 — eq:dSegate leading $-$: $\partial g/\partial x=-\frac{g_\max}{\Delta x_\mathrm{MIT}}\sigma(1-\sigma)<0$(삽입 기준 감소) → $\Delta S_e<0$(정합 C-3-c). 차원 — $g_\max/\Delta x_\mathrm{MIT}$[e/eV/(무차원 x)]·$\frac{\pi^2}3 k_B^2 T$ → eV→J 환산 후 자리당 [J/K], $N_A$ 곱 몰당(정합). 극한 — $x=x_\mathrm{MIT}\Rightarrow\sigma=\frac12\Rightarrow\sigma(1-\sigma)=\frac14$ 최대(골 가장 깊음); $|x-x_\mathrm{MIT}|\gg\Delta x_\mathrm{MIT}\Rightarrow\sigma(1-\sigma)\to0$ 지수 소멸(T1 국소화). step 극한 $\Delta x_\mathrm{MIT}\to0\Rightarrow$ 델타 스파이크(비물리, 결함 분산 미수용 → logistic 정당). **정합.** [확정](식·항등식)+[tier 병기](파라미터 등급).

### C-6. LCO 정련 종합 — 무결성 체크리스트

| 정련 항 | 물리 무결 | 유도 완결 | 비약 | 부호 | 차원 | 극한 |
|---|---|---|---|---|---|---|
| C-1 타당성 3전제 | ✓ | ✓ | 0 | ✓($f=-σ_d$) | ✓ | ✓(Ω→0 환원) |
| C-2 세 봉우리 | ✓ | ✓ | 0 | ✓(Ω↑→gap↑) | ✓(C/V) | ✓(w→0 면적보존) |
| C-3-a 유도 재검 | ✓ | ✓ | 0(b→c 다리 C-3-b 보완) | — | — | — |
| C-3-b Sommerfeld 다리 | ✓ | ✓ | 0 | ✓(C_e>0) | ✓(J/K) | ✓(T→0) |
| C-3-c 부호 5고리 | ✓ | ✓ | 0 | ✓(삽입 음수 일관) | ✓ | ✓(x_MIT 골) |
| C-3-d 부호 박스 | ✓ | ✓ | 0 | ✓(7고리 PASS) | ✓ | ✓ |
| C-3-e 단위 다리 | ✓ | ✓ | 0 | ✓(N_A>0) | ✓(혼합차원 R k_B) | ✓(N_A 누락 경고) |
| C-3-f 가법성 2층 | ✓ | ✓ | 0("선도차수" 보강) | ✓(총 부호 불변) | ✓ | ✓(Δx 밖 소멸) |
| C-4 T-선형성 | ✓ | ✓ | 0 | ✓(이동률 음기울기) | ✓(V/K) | ✓(T→0) |
| C-5 게이트 정당화 | ✓ | ✓ | 0 | ✓(leading −) | ✓ | ✓(step 비물리) |

→ **LCO 정련 10항 전부 물리 무결·유도 완결·비약 0·적대검산(부호/차원/극한) 통과.** 신규 *식*은 도입하지 않음(전부 기존 eq:dSe~eq:dSegate 의 정련·다리·검산 박스). 코드 구현은 P4 plug-in 예고(sec:lco-code (ii)).

---

## §D. 드래프트 종합·정정·tier 요약

### D-1. 산출 3건 요약
- **§A coverage 매트릭스**: N0→N9 17 step + equilibrium = 18 코드 step 전부 Ch1 식 1:1 충족, 12 closed-form 0 누락. **누락 3건**(equilibrium T 스칼라·해상도 의존·resolver 사다리 — 코드 *거동* 설명 결손, §B 보완). **과잉-A 9건**(LCO plug-in, 후속 예고 정당), **과잉-B 0건**. 死코드·docstring 2건 = Ch1 의 올바른 비대응.
- **§B 다리 보완**: 본문 유도 사슬 끊김 0[확정](대표 3건 검증). 보완은 *코드 거동 설명* 다리 3건(B-1·B-2·B-3) 초안. 어투·식번호 tex 양식.
- **§C LCO 정련(중점)**: 타당성 3전제(C-1)·세 봉우리(C-2)·전자 엔트로피 6항(C-3-a~f)·T-선형성(C-4)·게이트 정당화(C-5)·종합 체크리스트(C-6). 신규 식 0, 다리·검산 박스 신설 제안(C-3-b Sommerfeld 적분 출처·C-3-d 부호 박스·C-3-e 단위 혼합차원·C-3-f 선도차수). 전 10항 적대검산 통과.

### D-2. 추정 근거 명시 (4-tier 분류)
- **[확정]**(코드·식 직접): coverage 18 step·12 식·누락 3·死코드·docstring 정확성·유도 사슬 끊김 0·부호 5/7고리·단위 항등식·T-선형 식미분. 근거 = P1 §1-§4 줄근거 + tex 식 라벨 전수 grep.
- **[근거 미발견]**: $g(E_F,x)$ 연속 곡선(갭 G2, 1차 문헌 부재 → logistic 가정); inter-particle $\eta$ 분포 형상(ORIGIN §2(c), dahn1995 는 intra-particle, tier C).
- **[추정]**(설계 의도): C-1 자리-등가 한계(order-disorder 비등가, 근거=monoclinic 초격자); C-3-f 교차항 크기(직교성 고차 보정, 근거=MIT 결합); A-3 과잉-A 정당성(P1 §2-E·Open Issues 의 "후속 develop" 선언).
- **[미검증]**(수치 미실행): C-4 다온도 이동률 plot(피팅 예고); C-2 LCO 봉우리 절대 위치(tier A→B 초기값, 피팅 override).

### D-3. master 통합 시 주의 (범위 밖이라 제안만)
- 본 드래프트는 *식 신설 0* — 전부 기존 식의 정련·다리·검산. master 가 신규 verifybox(C-3-d) 식번호 배정 시 sec:signcheck S/R 양식과 충돌 점검.
- §B 다리 3건은 "버그"가 아니라 "코드 거동 설명"으로 삽입해야 함(P1 도 보고만, 코드 정정 X — P4 후보).
- LCO 절은 전부 과잉-A(후속 plug-in 예고) — Ch1 헤더·P1 Open Issues 의 "흑연 전용·LCO 후속" 선언과 충돌 없이 정련 깊이만 강화.

*드래프트: O1(작업 sub) | 입력 전문 정독(tex 1847줄·P1 result·broadening 설계·ORIGIN_VERDICT) | 산출 = supplement 드래프트(문건·코드 수정 X) | 물리 적대검산 전 항 부호·차원·극한 통과*
