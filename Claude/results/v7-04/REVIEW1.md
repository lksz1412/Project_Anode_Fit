# REVIEW1 — v7-04.tex 적대 검수 (검수 sub, v7-04)

> 대상 `v7-04.tex` (627행) 전문 정독(1–392 / 393–627 2청크 head→tail).
> 판정 기준 = `Anode_Fit_v11_final.py`(707행) · `v11_flowchart.md` · `AUTHOR_BRIEF.md` 전문 대조.
> refute mandate: 각 부호 항을 v11 코드로 재유도·반례 시도. 빈 통과 금지.

---

## 1. 확정 결함 {심각도 · 행 · 틀림 · 옳은 형}

확정 CRIT = 0, HIGH = 0. 아래는 MEDIUM/LOW (차단 아님, 개선 권고).

| # | 심각도 | 행 | 틀림 | 옳은 형 |
|---|---|---|---|---|
| D1 | MEDIUM | L607, L338, 표 L600-603 | GRAPHITE_STAGING_LIT 네 전이는 dict 에 `'w'` 키(0.020/0.016/0.014/0.012)를 **모두** 가진다. `_width`(코드 L285-288)의 w^eff 게이트는 `tr.get('w') is None` 일 때만 발화하므로, 이 문헌 데이터셋에서는 `use_w_eff=True` 라도 w^eff 가 **절대 적용되지 않는다**. 본문(L338)은 "w 직접 지정이 없을 때만"으로 게이트는 맞게 적었으나, 곧이어 표(L607)에서 "'w'…는 'n' 이 있으면 쓰이지 않는 하위호환 폴백"이라고만 해, w^eff 게이트가 'w' 키 존재로 막힌다는 사실(=문헌셋엔 w^eff 무효)을 독자가 놓친다. G-usable 재현자가 use_w_eff 를 켜도 좁힘이 안 일어나 혼란. | 표 주석에 "단, 'w' 키가 있으면 `_width` 의 w^eff 분기도 막혀(코드 L286 `tr.get('w') is None`), 이 데이터셋에선 use_w_eff 가 무효 — w^eff 를 쓰려면 'w' 키를 비우고 'n'·'Omega' 만 둘 것" 한 줄 추가. |
| D2 | LOW | L444, L610 | 컷 affinity 를 "$\mathcal A=\min(z_{\mathrm{cut}}\,|n|\,RT,\dots)$"로 적었는데, 코드 L335 는 `z_cut * n_safe * R * T` 이고 `n_safe = abs(n_j)`. 즉 `|n|` 표기는 코드와 일치(✓)이나, 식 L446 `eq:affcut` 박스 본체는 "$z_{\mathrm{cut}}\,|n|$" 가 아니라 "$z_{\mathrm{cut}}\,|n|\,RT$"로 본문(L444)과 박스(L446)에서 `|n|` vs `n` 표기가 미세 혼용(박스 L446 은 `|n|`, G-usable 요약 L610 은 `nRT` 로 절댓값 빠짐). 물리 동일하나 표기 일관성 결함. | L610 의 "$\mathcal A=\min(z_{\mathrm{cut}}nRT,\dots)$"를 "$z_{\mathrm{cut}}|n|RT$"로 통일(코드 `abs` 반영). |
| D3 | LOW | L470 | "함수 func_L_q 자체는 I≤0 에서 −∞(미정의)를 반환" — 코드 L92-93 은 `if I<=0: return -np.inf`. 맞음(✓). 다만 그 직후 `_resolve_lag_length` 는 L323 에서 `I<=0` 를 먼저 걸러 0.0 반환하므로 func_L_q 의 −inf 경로는 정상 진행에선 도달 안 함 — 본문은 "재현 코드는 이 컷을 둬야 한다"로 바르게 경고하나, dqdv 본류에선 L_q 의 −inf 가 L347 `if not np.isfinite(L_q): return 0.0` 으로도 2중 차단됨을 안 짚어 재현자가 컷 위치를 오해할 여지. | "코드는 `_resolve_lag_length` 입구(L323 I≤0)와 L_q 비유한 체크(L347) 두 곳에서 차단한다" 보강. |

**부호 8항 — 확정 결함 0.** 8항 전건이 v11 과 1:1 정합(아래 §5).

---

## 2. 강점 3 · 약점 3

### 강점
- **S1. 부호 사슬 8항 완전 정합 + 코드 1:1 추적성.** §8 8항을 각 절 verifybox·codebox 에서 v11 행번호와 함께 재확인하고, 맺음 L613 에서 8건을 한 번에 봉인. 스폿체크한 line 참조(L412/L419/L420/L430/L68/L438/L440/L123/L133/L448-454/L64/L141/L283/L84/L459/L354/L370/L468/L307/L335/L346/L90/L155/L149/L100/L474-477/L479/L481/L483/L535) **전부 정확** — 단 하나의 행 오기도 없음. 회사 배포·피팅 근거 문건으로서 신뢰 1급.
- **S2. 척추 N0→N9 순서·노드 커버 완전.** 절 9개(N0=§1 … N9=§9)가 flowchart 노드와 정확히 대응, N3(히스)를 N2 뒤 "구조 선언"으로 배치한 것도 brief §3-6("방전 메인·히스는 분기 위상")과 정합. 노드 누락 0.
- **S3. G-usable 재현 절(§9.4, L609-610) 자족.** 6단계 진행 + 수치 상수 기본값(z_cut=4.357, A_cap=4, m=2.0, pad=0.15, n_min=2048, floor_frac=0.05, χ=0.5, ΔS_a=0)까지 닫아, 표(GRAPHITE_STAGING_LIT)와 합쳐 "이 문건만으로 곡선 재현" 요건 충족. 두 환원 극한(|I|→0, γ=0/Ω≤2RT)을 검산으로 봉인.

### 약점 (가장 약한 1 = W1)
- **★W1 (가장 약한 1곳). w^eff 의 실효적 무효(D1).** 본문은 w^eff 식(eq:weff)을 정식 유도하고 "use_w_eff 켤 때만"이라 적었으나, 정작 본 장이 싣는 유일한 데이터셋(GRAPHITE_STAGING_LIT)에서는 'w' 키 존재로 w^eff 게이트가 막혀 **한 번도 발화하지 않는다**. 재현자가 use_w_eff=True 로 좁힘을 기대하면 코드와 결과가 어긋난다. eq:weff 가 본 장에서 "결과식이 N4 에 물리는" orphan-경계에 가까운 유일 지점 — 게이트-데이터 상호작용을 한 줄로 닫아야 완결. (수정 비용 1줄, §1 D1 참조.)
- **W2. 표기 미세 혼용(D2).** `|n|` vs `n`, affinity 절댓값 표기가 본문·박스·요약에서 통일 안 됨. 물리 무해하나 수식-주도 문건의 형식 1급 기준에선 결함.
- **W3. equilibrium vs dqdv 의 |I|→0 불일치 단서가 분산.** L394·L613 에서 "equilibrium 은 분기 미반영(U_j 중심), dqdv 의 |I|→0 은 U_j^d 중심 → γ>0 이면 ±½γΔU_hys 차"를 바르게 짚었으나, §6 본문(L388)에서 "코드의 equilibrium 메서드가 이 합이다"라고 먼저 단정한 뒤 L394 에서 단서를 다는 순서라, 빠른 독자는 두 메서드 완전 일치로 오독할 위험(단서가 뒤에 옴). 순서상 도입에서 "단 분기 한정"을 선치하면 깔끔.

---

## 3. 차원 점수 (6차원 × 5점 = /30)

| 차원 | 점수 | 근거 |
|---|---|---|
| 척추 정합(N0→N9 순서·노드) | 5/5 | 절-노드 1:1, 누락 0, 히스 분기 위상 배치 정합 |
| 부호 사슬(8항 적대검산) | 5/5 | 8항 전건 v11 재유도 정합, 반례 시도 실패(=결함 없음) |
| G-follow(따라가짐·비약) | 4/5 | logistic 을 속도식 정지점에서 유도(L341-352)·spinodal 제곱근 정의역까지 전개 양호. detailed balance "χ 약분"(L347)은 한 줄로 빠른 편(학부생엔 1단계 더 필요) |
| G-usable(재현·STAGING 정합) | 4/5 | §9.4 자족하나 W1(w^eff 무효) 미봉합으로 −1 |
| 완결성(orphan)·그림(\ref·영어전용·도움) | 5/5 | 그림 5개 전부 신규 TikZ·내부 ASCII·\ref 연결(fig:staging/hysbranch/bell/tail/sum)·앞식 동기·뒤본문 사용. orphan 0 |
| 형식(수식주도·전보체·절 다리) | 4/5 | 절 도입/마무리 다리 의무 이행·수식 주도 양호. D2 표기 혼용·괄호 보충 일부(L181·L607 장문 괄호)로 −1 |
| **합** | **27/30** | |

---

## 4. 부호 8항 PASS/FAIL + 근거 (v11 대조)

| 항 | 판정 | 근거(tex ↔ v11) |
|---|---|---|
| 1. U_j(T)=(−ΔH+TΔS)/F, ΔG=−FU | **PASS** | tex eq:Uj L234 ↔ 코드 L69 `(-dH_rxn+T*dS_rxn)/F`. 발열(ΔH<0)→U_j>0, 흑연 0.08-0.21V 정합. 수치 0.0853/0.2109 재계산 일치. |
| 2. ξ_eq=logistic[σ_d(V−U)/w], 방전 V↑→ξ↑ | **PASS** | tex eq:logistic L349 ↔ 코드 L86 `z=s*(V_n-U)/func_w`. σ_d=+1, V>U→ξ→1 ✓. |
| 3. dξ/dV=σ_d ξ(1−ξ)/w → peak 양수(방향 불변) | **PASS** | tex eq:dxidV L376 + eq:eqpeak L381(σ_d 없음) ↔ 코드 L468 `ksi_eq*(1-ksi_eq)/w`(σ_d 없음). ξ(1−ξ)>0·1/w>0. |
| 4. ΔU_hys≥0, Ω≤2RT→0, 분기 ±½σ_d | **PASS** | tex eq:dUhys L275·eq:Ubranch L284 ↔ 코드 func_dU_hys L127-130(Ω≤2RT→0.0)·func_U_branch L138 `+0.5*sigma_d*h_eta*gamma*dU`. 임계 소멸 ∝(T_c−T)^{3/2} 유도 정확. |
| 5. χ_d(방전 χ/충전 1−χ), ΔH_a^eff=ΔH_a−χ_dΩ | **PASS** | tex eq:chid L454·eq:dHeff L459 ↔ 코드 func_chi_d L160 `chi if sigma_d>=0 else 1-chi`·func_dH_a_eff L152 `dH_a-chi_d*Omega`. |
| 6. ∂lnL_q/∂V<0 (V↑→장벽↓→꼬리↓) | **PASS** | tex L441/L473 `−χ_d σ_d F/RT≤0(σ_d=+1)` ↔ 코드 L96 `... − x*A/RT`, A=σ_d F(V−U): V↑→A↑→−x·A/RT↓→L_q↓. affinity 연속 의존을 컷서 동결한다는 단서도 정확(L473). |
| 7. 충전 격자 역전 ξ[::-1]…[::-1], 충전=방전 거울·양수 | **PASS** | tex eq:reversal L504 ↔ 코드 L477 `_causal_lowpass(ksi_arr[::-1],...)[::-1]`. 인과성("진행 방향의 과거") 설명 정합. |
| 8. V_n=V_app−σ_d|I|R_n | **PASS** | tex eq:vn L195 ↔ 코드 L412 `V_in - sigma_d*I_abs*self.Rn`. 방전 V_app>V_n 물리 정합. |

**부호 8항: 8 PASS / 0 FAIL.**

추가 확인: 컷 affinity 부호 버그 회피(σ_d 를 min 밖에, 크기만 min 안에) — tex L449 가 코드 L330-331 주석("s 를 min 밖에 두면 충전서 음수 상한 되던 원본 버그 정정")과 정합. ✓
