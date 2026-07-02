# V1.0.13 CODE_MAP — 문건↔코드 양방향 매핑 (P1.1 S4)

> 역할: 감사/초기화 sub(파일 수정 없음, 표만). 입력 전문 정독: `Anode_Fit_v1.0.13.py`(860줄, 1-860 head→tail),
> `graphite_ica_ch1_v1.0.13.tex`(2230줄, 1-2230 head→tail), `graphite_ica_ch2_v1.0.13.tex`(731줄, 1-731 head→tail),
> 승계 기반 `FABLE_AUDIT_03_code_fitness.md` + `FABLE_REAUDIT_C6_note.md`(v1.0.11 시점 24-boxed 매핑). 줄번호는
> 전부 실측(Read/Grep, cat -n 기준) — 문서 재인용 아님.
>
> **v1.0.13 실측 boxed 총 30개** = Ch1 23개(grep 확인, v1.0.11의 17 + LCO 신설 다수) + Ch2 7개(불변).
> `tab:inputs`(ch1 L2193-2226)가 생성자 인자 전수를 식 라벨과 함께 표로 제공 — 과거 감사가 "코드-only"로
> 의심했던 다수 항목(`grid_pad_lo/hi`,`n_work_min`,`min_lag_grid_steps`,`v_span_floor`,`seed_T/I/Q_cell`,
> `z_cut`,`A_cap_RT`,`use_dH_eff`,`chi_split`)이 v1.0.13 에서는 **전부 표에 명문화**되어 orphan(b) 후보에서 제외됨.

---

## A. Ch1 결과박스(boxed) 23개 — 문건→코드

| 문건 항목(라벨·줄) | 코드 대응(함수/분기/줄) | 방향 | 지위 | 처분·비고 |
|---|---|---|---|---|
| eq:vn (box L379, label L380) | `dqdv` 분극: `V_n = V_in - sigma_d*I_abs*self.Rn` (L431) | 문건→코드 | 1:1 구현 | 변경 없음 |
| eq:Uj (box L459, label L460) | `func_U_j` (L79-80) `(-dH_rxn+T*dS_rxn)/F` | 문건→코드 | 1:1 구현 | v1.0.11과 동일 |
| eq:lco-dUdT (box L523-527, label L528) | 흑연과 같은 `func_U_j` 재사용(LCO는 `LCOCathodeDQDV._effective_dS_rxn` L666-682 seam 경유 `dS_rxn` 만 치환) | 문건→코드 | 1:1 구현(파라미터 치환) | "같은 함수, 값만 cat" 주장이 코드로 확인됨(새 함수 無) |
| eq:dUhys (box L683-685, label L686) | `func_dU_hys` (L134-141) | 문건→코드 | 1:1 구현 | Ω≤2RT→0 분기 포함 |
| eq:Ubranch (box L703, label L704) | `func_U_branch` (L144-149) | 문건→코드 | 1:1 구현 | h_eta 인자화 확인 |
| eq:lco-dUhys (box L823-830, label L831) | `func_dU_hys` 재사용(LCO 전이에 호출) | 문건→코드 | **1:1 구현(구조)·비활성(데이터)** | `LCO_MSMR_LIT`(L625-642) 3건 모두 `'Omega'` 키 미배정→`tr.get('Omega',0.0)`=0→`gamma`도 미배정→분기 비활성. 코드 경로는 열려있으나 현재 시연 데이터셋에서 수치적으로 발현 안 됨(tex L781-785가 이를 명시) |
| eq:lco-Ubranch (box L834-836, label L837) | `func_U_branch` 재사용 | 문건→코드 | 1:1 구현(구조)·비활성(데이터) | 상동 |
| eq:lco-mit (box L890-893, label L894) | 구조적 분리 자체: `func_dU_hys`(Ω만 인자)와 `_effective_dS_rxn`(전자항, Ω 무관)가 코드상 별개 함수/경로 | 문건→코드 | 1:1 구현(구조 분리 검증) | "두 몫이 다른 슬롯" 주장 = 코드에서 Ω와 ΔS_e가 물리적으로 다른 인자·다른 함수로 실증 |
| eq:xieq (box L983, label L984) | `func_ksi_eq` (L95-98), z≥0/z<0 오버플로 분기 | 문건→코드 | 1:1 구현 | `np.where` 분기 수학적 동치 |
| eq:dSe (box L1222-1223, label L1224) | `func_dSe_molar` 내부 (자리당→몰당 전) | 문건→코드 | 유도 중간식 | 코드는 몰당 최종형(eq:dSegate)만 직접 평가 |
| eq:U1T2 (box L1270, label L1271) | **미대응** — `_effective_dS_rxn`(L666-682)은 T_ref 동결 상수 오프셋만 사용 | 문건→코드 | **미구현 과제** | 코드·문건 양측 명시 선언(docstring L670-676 "P4 미구현, 다온도 round-trip 과제"). eq:lco-U1V(비boxed, 아래 C절)가 코드가 실제 쓰는 동결 근사형 |
| eq:ggate (box L1284-1285, label L1286) | `func_dSe_molar` 내부 σ(1-σ) 게이트 항(암묵 folded) | 문건→코드 | 1:1 구현(folded) | g(E_F,x) 자체를 별도 반환하지 않고 dSegate 닫힌식에 흡수 — 정합이나 중간값 미노출 |
| eq:dSegate (box L1297-1300, label L1301) | `func_dSe_molar` (L171-186) 전체 | 문건→코드 | 1:1 구현 | 3중 단위가드(leading −·÷e_V·몰당 R·k_B) 코드·문건 일치, 실측 −45.655 vs 문건 −45.7~−46 |
| eq:eqpeak (box L1402-1404, label L1405) | `equilibrium` (L388) / `dqdv` 평형분기 (L487) `ksi_eq*(1-ksi_eq)/w` | 문건→코드 | 1:1 구현 | 면적보존 실측(과거 감사 ratio 1.00000) |
| eq:lco-eqpeak (box L1465-1468, label L1469) | `equilibrium`/`dqdv` 동일 코드, `LCO_MSMR_LIT` 3전이 통과 | 문건→코드 | 1:1 구현(코드 일반화로 자동 충족) | 새 함수 불요 — MSMR 동형 주장(§sec:lco-code)이 "구조 변경 0"을 코드로 실증 |
| eq:Lq (box L1688, label L1689) | `_resolve_lag_length` 내 A 산출 (L354) | 문건→코드 | 1:1 구현 | `min(z_cut*n_safe*R*T, A_cap*R*T)` |
| eq:dHeff (box L1731, label L1732) | `func_dH_a_eff` (L153-156) | 문건→코드 | 1:1 구현 | `use_dH_eff` 토글로 on/off (L264, L321-322) |
| eq:LV (box L1761, label L1762) | `_resolve_lag_length` 반환 (L370) `abs(dVdq_qa)*L_q` | 문건→코드 | 1:1 구현 | |
| eq:peakshape (box L1846, label L1847) | `dqdv` (L498) `(ksi_eq - occ_lagged)/lag_len_V` | 문건→코드 | 1:1 구현 | |
| eq:sum (box L1934-1936, label L1937) | `dqdv` 누적(L500) + `np.interp`(L502) | 문건→코드 | 1:1 구현 | |
| eq:lco-decomp (box L2017-2019, label L2020) | `LCOCathodeDQDV._effective_dS_rxn` (L666-682) | 문건→코드 | 1:1 구현(부분 folded) | config+vib는 `LCO_MSMR_LIT`의 `dS_rxn` 리터럴 숫자에 이미 합산되어 들어감(코드가 3항을 분리 변수로 갖지 않음) — elec 항만 명시 가산(`func_dSe_molar` 호출) |
| eq:lco-msmrpeak (box L2120-2123, label L2124) | — (등가성 증명, 별도 코드 불요) | 문건→코드 | 유도 전용(등가성 증명) | MSMR θ(1-θ)/ω ≡ Ch1 ξ(1-ξ)/w — eq:lco-eqpeak/eq:eqpeak 로 이미 구현된 식과 대수적으로 같음을 보이는 절 |
| eq:lco-plugin (box L2175-2178, label L2179) | **부분 구현**: `func_U_branch`→`func_ksi_eq`→`equilibrium`/`dqdv` 단은 구현, 첫 화살표(x→ΔS_e,1(V,T), eq:lco-SeV/eq:lco-xmap)는 미구현 | 문건→코드 | 부분 구현 | 사슬 5단 중 뒤 3단(U_1^d→ξ_eq,1→peak)만 코드 실행 경로, 앞 2단(x 좌표매핑→ΔS_e(V,T))은 `x_center` 고정 스칼라로 대체(아래 B/미구현 참조) |

---

## B. Ch2 결과박스(boxed) 7개 — 문건→코드

| 문건 항목(라벨·줄) | 코드 대응(함수/분기/줄) | 방향 | 지위 | 처분·비고 |
|---|---|---|---|---|
| 서두 사슬 박스 (비labeled, L99) `Z→⟨n⟩→S→∂U/∂T→q_rev` | `func_ksi_eq`→`entropy_coefficient`→`reversible_heat` 전체 파이프라인 | 문건→코드 | 개념도(코드 대응 불요) | 5개 화살표가 각각 아래 항목에 대응 |
| eq:logistic (box L152-153, label L154) | `func_ksi_eq` (동일 함수, Ch1 eq:xieq 재확인) | 문건→코드 | 1:1 구현(중복 확인) | Ch2가 통계역학 기원을 재유도할 뿐 코드는 Ch1과 공유 |
| eq:Sconfig (box L226-227, label L228) | **미대응(직접)** — 절댓값 S_config 자체는 코드에 없음 | 문건→코드 | 유도 중간식 | 도함수형(eq:dSconfig, 비boxed)만 `entropy_coefficient`의 `config` 항으로 구현(L574) |
| eq:weighted "단순식" (box L484-486, label L487) | **미대응(단독)** — 코드는 이 식을 거치지 않고 바로 완전식 구현 | 문건→코드 | 유도 중간식(디딤돌) | 중심값-only 근사이며 코드는 처음부터 config 항 포함 완전식만 계산 |
| use-this 완전식 (비labeled box, L699-701) | `entropy_coefficient` (L545-579) 전체, 특히 L572-578 | 문건→코드 | 1:1 구현 | `num=Qg*(dS_eff/F+config)`, `den=Qg` — 독립 재구현 대조 실측 diff 1.08e-19(과거 감사) |
| eq:hys_rev (box L605-606, label L607) | `entropy_coefficient`가 히스 분기 미분 U_j(shift 없음) 사용 (L564-568) | 문건→코드 | **동결 근사(자동 근사)** | 분기별 평균을 직접 계산하지 않고 평형 중심 U_j로 근사 — docstring(L552-556)이 "γ 대칭 전제, 비대칭 분기별 ∂U/∂T 미구현" 명시 |
| eq:qrev (box L672, label L673) | `reversible_heat` (L581-589) `-I*T*entropy_coefficient(...)` | 문건→코드 | 1:1 구현 | T 한 번(T² 아님) 확인, 과거 감사 실측 diff 0 |

---

## C. 비-boxed 이지만 명시적 코드 대응 식 (선별)

문건이 `\boxed{}`로 강조하지 않았으나 본문에서 `\code{...}` 로 코드 식별자를 직접 지목하는 식들 — orphan 판정에서 제외.

| 문건 항목 | 코드 대응 | 지위 |
|---|---|---|
| eq:vwork (L390-394) 작업격자 | `dqdv` L438 `V_work=np.linspace(...)`, `grid_pad_lo/hi`·`n_work_min` (생성자 L250-251, 269) | 1:1 구현 — tab:inputs L2218에 재확인 |
| eq:branch (L1857-1863) 꼬리/평형 전환 | `dqdv` L485 `if lag_len_V < self.min_lag_grid_steps*grid_step` | 1:1 구현 — ν=2, tab:inputs L2219 |
| eq:reversal (L1879-1885) 충전 격자역전 | `dqdv` L493-496 `ksi_arr[::-1]` | 1:1 구현 |
| eq:center (L713-719) 분기중심 선택 | `dqdv` L467-473 `if gamma!=0 and Omega>0: center=U_j+hys_shift else U_j` | 1:1 구현 |
| eq:lowpass (L1803-1808) 이산 저역통과 | `_causal_lowpass` (L111-129) | 1:1 구현 |
| eq:Acut (L1708-1711) A 상한 | `_resolve_lag_length` L352-354 | 1:1 구현, `z_cut`/`A_cap_RT` per-tr override 포함 |
| eq:chid (L1721-1725) | `func_chi_d` (L159-164) + `chi_split` 주입(L247, L263, L310-313) | 1:1 구현 |
| eq:lco-xmap (L2138) x=x(ξ_eq,1(V)) | **미구현** — `LCOCathodeDQDV._effective_dS_rxn`은 `tr['x_center']` 고정 스칼라 사용 (L679-681) | 미구현 과제(문건·코드 양측 명시 tier-C 라벨) |
| eq:lco-SeV (L2147-2152) ΔS_e(V,T) | **미구현(V-종속형)** — 코드는 `func_dSe_molar(x_center, T_ref, ...)` 로 T_ref 1회 평가 후 상수 오프셋 (L680-681) | 동결 근사 — V-격자 위 실시간 평가 아님 |
| eq:lco-U1V (L2158-2162) U_1(V,T) 적분형의 동결 근사 | `_effective_dS_rxn`(L666-682) 전체 로직 | 1:1 구현(동결 근사형) | 코드가 실제로 쓰는 식은 eq:U1T2(완전 T² 적분)이 아니라 이 동결 근사형 — 문건이 코드의 실제 근사를 스스로 명문화(L2164-2168) |

---

## D. Orphan (a) — 문건O · 코드X (미구현, 지위 라벨 포함)

| 문건 항목 | 지위 | 근거 |
|---|---|---|
| eq:U1T2 (L1270) 전자항 T² 곡률 | **미구현 과제** — 동결 근사(eq:lco-U1V)로 대체 | 코드 docstring L670-676, tex L2164-2168 양측 명시 |
| eq:lco-xmap (L2138) 좌표매핑 x=x(ξ_eq,1(V)) | **동결 근사(tier-C)** — `x_center` 고정 스칼라 | tex L331-335(tab:lco-staging 캡션), L2053-2058(★Ch2/P4 예고) 명시 |
| eq:hys_branch (L600, Ch2) 분기별 ∂U/∂T | **동결 근사(자동)** — 평형 중심 U_j 사용으로 근사 | 코드 docstring L552-556 "Ch2 범위 밖 선언, 후속 과제" |
| eq:ensavg (L1554-1559, Ch1) 앙상블 ρ(U_app) 합성곱 broadening | **미구현 과제(forward-only 명시 배제)** — 코드는 단일 유효입자+L_V 구조 유지 | tex L1602-1615 (iii) "다입자 기계장치는 모델에 넣지 않는다" 명문 |
| procedurebox (Ch2 L726-738) S_0^j 다온도 round-trip 식별 절차(1-5단계) | **미구현(스코프 밖)** — Optuna 등 외부 피팅 스크립트 영역, forward 모델 자체는 이 절차를 실행하지 않음 | Anode_Fit_v1.0.13.py 는 forward 모델만; 피팅 루프 없음(파일 전체 확인) |
| eq:lco-dUhys/eq:lco-Ubranch (Ch1) | **구조 구현·수치 비활성** — 위 A절 참조(LCO_MSMR_LIT에 Omega 미배정) | LCO_MSMR_LIT dict 3건 전수 확인(L625-642): `'Omega'` 키 없음 |
| LCO_MSMR_LIT 전자항 배정 (x_MIT=0.50, 중간 T2-dict) | **시연값 tier-C placeholder** — 물리 anchor(T1 MIT~3.90V·x_MIT≈0.85)와 불일치, round-trip 재정렬 선언 | tex L331-335 명시, 코드 L630-637 데이터와 정확히 대조됨(불일치 확인, 결함 아님) |
| q_irr 3분해 (I²R+Iη_ct+Iη_diff) | **양측 일관 lumped-only** — boxed 식 자체가 Ch2에 없음(orphan 아닌 "정직한 부재") | 코드 docstring L594-597, tex L714-724 한계 섹션(5) |

---

## E. Orphan (b) — 코드O · 문건X (문건 미서술)

| 코드 항목 | 위치 | 지위·비고 |
|---|---|---|
| `_finite`/`_finite_pos`/`_finite_nonneg` 가드 3종 + 전 호출부의 `ValueError` fail-fast 패턴 | L190-211, 생성자·`dqdv`·`_resolve_lag_length` 전역 삽입 | **코드 전용** — tab:inputs가 각 인자의 "기본값·역할"은 표로 주지만, 입력 검증 메커니즘(유한성·양수·비음수 가드, 예외 타입) 자체는 물리식이 아니라 순수 엔지니어링 관행이라 문건 서술 대상이 아님(정상) |
| `_build_seed_L_V` 메서드의 구현 메커니즘(대표 방전조건에서 1회 `_resolve_lag_length` 선호출) | L285-292 | **코드 전용** — `seed_T/I/Q_cell` *파라미터*는 tab:inputs L2221에 있으나, 그 파라미터를 소비하는 메서드의 내부 로직·주석에 적힌 유래("원본 List에 문자열 키 대입 TypeError 버그를 seed_L_V 리스트로 우회") L273-278는 코드 유지보수 이력이라 문건 대상 아님 |
| `curve()` facade의 방향 문자열 별칭 전수 (`"dis"`,`"d"`,`"+"`,`"+1"`,`"1"`,`"sigma+"` / `"chg"`,`"c"`,`"-"`,`"-1"`,`"sigma-"`) | `_direction_to_sigma` L606-613 | **코드 전용(경미)** — 문건은 "discharge/d/dis/+ 또는 charge/c/chg/−" 정도의 대표 예만 제시(L199-205), 코드는 이보다 별칭이 많음. 물리 무관, 문서화 갭 정도 |
| `__main__` self-test 스위트 전체 (guard 7종 점검·`chi_split` 주입 A/B 비교·히스테리시스 분기 dis/chg peak 분리·꼬리 방향역전 데모·극한 reduction 체크·per-transition override 격리 회귀테스트) | L725-861 | **코드 전용(당연)** — 코드 품질/회귀 게이트일 뿐 물리 서술 대상이 아님. 다만 이 스위트가 위 boxed 식들(S1-S8 부호사슬 등)을 실행 검증하는 유일한 코드 경로이므로 완전한 orphan은 아니고 "검증 인프라"로 분류 |
| `func_U_j_hys` (L83-92, "사용자 원형 보존") | 모듈 최상단 | **부분 orphan — 원형 보존·활성 경로 미호출** — eq:dUhys+eq:Ubranch 원형과 문건 대응은 있으나(주석 L36 명시), 실제 `equilibrium`/`dqdv`는 이를 호출하지 않고 분리된 `func_dU_hys`+`func_U_branch`(L134-149)를 쓴다. 문건 근거는 있으나 dead code 성격 — orphan(b)이라기보다 "중복/미사용" 메모 |
| `LCOCathodeDQDV` 클래스가 상속만으로 `equilibrium`/`dqdv`/`curve`/`entropy_coefficient`/`reversible_heat`/`irreversible_heat` 6개 메서드를 재정의 없이 그대로 물려받는 사실 자체 | L645-682 | **코드 전용(구조적 사실)** — "구조 변경 0"이라는 문건 주장(sec:lco-code)의 실증이나, "6개 메서드가 override 없이 상속된다"는 사실을 문건이 나열하지는 않음(요약 서술만). 실질은 orphan이 아니라 근거 보강 |

---

## 요약

- **문건→코드 boxed 매핑**: Ch1 23 + Ch2 7 = **30건**, 전부 코드 대응 확인(1:1 구현 22 / 구조구현·데이터비활성 2 / 동결근사 1 / 유도전용·등가증명 2 / 부분구현 1 / 미구현 1[eq:U1T2] — 세부는 A·B절).
- **Orphan (a) 문건-만**: **7건** — eq:U1T2(T² 곡률)·eq:lco-xmap(좌표매핑)·eq:hys_branch(분기별 ∂U/∂T)·eq:ensavg(앙상블 convolution)·procedurebox(피팅 절차)·eq:lco-dUhys/Ubranch(LCO 데이터 비활성)·LCO_MSMR_LIT tier-C 배정불일치. 전부 문건·코드 양측 명시 선언(미서술 누락 아님).
- **Orphan (b) 코드-만**: **6건** — `_finite*` 가드·`_build_seed_L_V` 내부 메커니즘·`curve()` 방향별칭 전수·`__main__` self-test 스위트·`func_U_j_hys`(미사용 원형)·LCOCathodeDQDV 상속 사실. 전부 물리 무관(엔지니어링/테스트/문서화 갭)이며 근거 없는 창작(진짜 orphan)은 0건.

### 핵심 발견 5건
1. v1.0.13 `tab:inputs`(ch1 L2193-2226)가 생성자 인자 전수를 문서화해, v1.0.11 감사 때 "코드-only 후보"였던 `grid_pad_lo/hi`·`n_work_min`·`min_lag_grid_steps`·`v_span_floor`·`seed_T/I/Q_cell`가 전부 orphan(b)에서 **제외**됨 — 과거 우려가 이번 버전에서 해소.
2. LCO 히스테리시스 박스(eq:lco-dUhys/eq:lco-Ubranch)는 코드 경로가 구조적으로 완비돼 있으나 `LCO_MSMR_LIT`에 `Omega`가 아예 없어 **수치적으로 죽어있다** — "구현됨"과 "발현됨"을 분리해야 할 사례.
3. eq:lco-plugin(5단 forward 사슬)은 **부분 구현**이다 — 뒤 3단(U^d→ξ_eq→peak)은 실행되지만 앞 2단(x 좌표매핑→V-종속 ΔS_e)은 `x_center` 고정 스칼라로 대체돼 있다.
4. `func_U_j_hys`(사용자 원형 보존 코드)는 문건 근거가 있음에도 활성 실행경로에서 호출되지 않는 **중복 dead code** — orphan 분류가 아니라 코드 정리 후보로 별도 기록해야 함.
5. 진짜 의미의 "근거 없는 창작"(코드가 있는데 문건이 전혀 언급조차 안 하는 신물리)은 **0건** — orphan(b) 6건 전부 엔지니어링/테스트 인프라이거나 문서화 완결성 경미 갭.
