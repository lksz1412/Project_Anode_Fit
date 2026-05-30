# PHASE_DIAG — 사용자 PhD Refs 6/7 Dossier (P3-5 의무 5항목 완성)

**근거 문서**: 사용자 논문 *JCP* **147**(14), 144111 (2017), "Effects of external electric field and anisotropic long-range reactivity on charge separation probability" (Kyusup Lee, Seonghoon Lee, Cheol Ho Choi, Sangyoub Lee). — **임시 열람 후 삭제(2026-05-29), GitHub 미업로드. 본 dossier는 텍스트 추출 결과만 보존.**
**용도**: 합류 Ch1 §closure 및 Ch6 가속 후보의 grounding (plan §6.10, P3-5).
**일자**: 2026-05-29

---

## (a) 서지 — refs [6], [7] 확정
2017 논문 본문에서 인용된 ref. 번호 기준 (논문 참고문헌 목록 확인):
- **[6]** S. Lee, C. Y. Son, J. Sung, S. Chong, *J. Chem. Phys.* **134**, 121102 (2011). (= 프로젝트 `lee2011`)
- **[7]** C. Y. Son, J. Kim, J.-H. Kim, J. S. Kim, S. Lee, *J. Chem. Phys.* **138**, 164123 (2013). (= 프로젝트 `son2013`)

## (b) 사용자 논문 내 사용 위치 (page · paragraph)
- **Sec. I (Introduction), p.144111-1, 우단 2번째 문단**: "In this work, we employ the **recently proposed solution method⁶,⁷ for Fredholm integral equations of the second kind** to treat the effects of external electric field and anisotropic long-range reactivity…". → Refs 6/7 의 역할 = **Fredholm 2종 적분방정식 해법**.
- **Sec. II (Theory), p.144111-4, Eq. (32) 직후**: "This type of integral equations is called the **Fredholm integral equation of the second kind**. An efficient solution method for this type… was proposed by us in **Refs. 6 and 7**." → 방법 도입 지점.
- 적용: Eq. (32) → (33)[formal exact] → (34)[ratio approximation] → (39)[closed-form], 그리고 Sec. III 전체에서 δ-sink·anisotropic·long-range case 에 사용.

## (c) 원 방법론의 수학적 구조 (ratio-substitution closure)
미지 함수 = `W̄u(r)` (ultimate survival/ separation probability, 변수 = 상대 반경 `r∈[σ,∞)`).
1. **Fredholm 2종 적분방정식** [Eq. (32)] — 미지 `W̄u` 가 적분 안에 선형으로 등장:
   `W̄u(r) = 1 − (χ(σ/r)/Dσ)∫_σ^r dr₁ [r₁²Λ(r₁)/e^{U₁(r₁)}] W̄u(r₁) − (1/Dσ)∫_r^∞ dr₁ χ(σ/r₁)[r₁²Λ(r₁)/e^{U₁(r₁)}] W̄u(r₁)`.
2. **형식적 厳密해 (ratio form)** [Eq. (33)] — `W̄u(r)` 를 적분 밖으로 묶어, 적분 안에는 **비(ratio) `W̄u(r₁)/W̄u(r)`** 만 남김:
   `W̄u(r) = [ 1 + (χ(σ/r)/Dσ)∫_σ^r … (W̄u(r₁)/W̄u(r)) + (1/Dσ)∫_r^∞ … (W̄u(r₁)/W̄u(r)) ]^{-1}`.
3. **★ratio-substitution (핵심 근사)** [Eq. (34)]: 미지 비를 **해석적으로 풀리는 reference 해의 비**로 치환:
   `W̄u(r₁)/W̄u(r) ≈ W̄uδ(r₁)/W̄uδ(r)`, 여기서 `W̄uδ` = δ-function reaction sink(contact reactivity) 의 ultimate survival probability(닫힌 형태, Eq. (25),(37),(38)).
4. → **closed-form 근사 해석식** [Eq. (39)], 모든 parameter 영역에서 정확하다고 주장.
- **자기 명시 유효범위 (Eq. (34) 직후, p.144111-5)**: "the accuracy of the approximation given by Eq. (34) **gets worse when the reaction zone becomes very broad**." → **ratio ansatz 는 kernel/reaction zone 이 넓을수록 부정확.** (단, 전자전달 sink 는 지수 감쇠·단거리라 대개 양호하다고 논증.)

## (d) 변수 매핑 (논문 → graphite dQ/dV 문제, (A) §closure)
| 논문 (2017) | graphite (합류 Ch1) | 비고 |
|---|---|---|
| 미지 `W̄u(r)` (survival prob.) | `Θ(q)` (effective phase progress) | self-referential 미지 함수 |
| 변수 `r` (radial, `[σ,∞)`) | `q` (charge/진행 좌표) | independent variable |
| reference 해 `W̄uδ(r)` (δ-sink contact) | `Θ^simple(q)` (single-mode `δ(L−L_0)` kernel) | 해석적으로 풀리는 baseline |
| ratio `W̄u(r₁)/W̄u(r) ≈ W̄uδ(r₁)/W̄uδ(r)` | `Θ(q')/Θ(q) ≈ Θ^simple(q')/Θ^simple(q)` | ★구조적 1:1 일치 ((A) `eq:closed_pre`,`eq:closed`) |
| kernel `χ(z)`, `Λ(r)` (diffusion+Coulomb+field) | spectrum kernel `𝒦(q,q')`, `A_L(L)` (barrier→length) | kernel mapping (검증 대상 F1) |
| closed-form Eq. (39) | (A) `eq:closed` `Θ_A(q)` | instantiated closed-form |

## (e) ★ 그대로 가져오면 안 되는 물리적 가정 차이 (load-bearing, M1/DQ-v3-2)
1. **Fredholm(고정 구간·정상상태) vs Volterra(인과·시간상한)** — 논문의 `r`-적분은 **고정 경계** `[σ,∞)`, **ultimate(정상상태) 확률**(시간 없음). graphite 의 self-consistent 식 `Θ(q)=Θ_0+∫_0^q 𝒦(q,q')[Θ_eq−Θ]dq'` 은 **상한이 현재 `q` 인 Volterra(인과 memory)**. → 방법 적용 전 graphite 를 **Fredholm 으로 환원**해야 하며, 그 조건은 (i) moving target 동결 `dΘ_eq/dq≈0`(post-peak), (ii) kernel decay length ≪ window. 이 환원의 붕괴는 **측정(ε, M1)** 으로 다루고 주장하지 않는다 ((A) "단계 0"). 
2. **★ratio ansatz 의 broad-kernel 열화 = stretched-tail 영역과 정면 충돌** — 논문 자체 경고(Eq. 34 직후): reaction zone 이 넓으면 부정확. graphite 에서 "넓은 kernel" = **넓은 relaxation-length spectrum = 바로 stretched tail(저온·관심 영역)**. 즉 **closure 가 가장 필요한 영역에서 가장 부정확할 수 있다.** → Plan B(g-grid direct numerical, Ch6 `eq:ch6_grid_average`)를 **validator/reference 로 필수 유지**, ε 를 운용 T·rate 영역에서 측정해 승격(M5). 단독 채택 금지.
3. **추가 비선형 결합** — 논문은 `W̄u` 에 **선형**(ratio 로 대수화). graphite 는 `Θ↔V_n` 이 charge balance(`eq:charge_balance`)로 **추가 결합(비선형)**. → graphite 가 더 강결합. ratio-substitution 은 `Θ` 자기참조 적분에만 적용하고, `V_n` 결합은 별도 root(Ch6 dynamic root)로 처리.
4. **solvable baseline 존재 확인** — 논문은 δ-sink closed form `W̄uδ`(Eq. 25) 가 이미 있음. graphite 는 single-mode `δ(L−L_0)` kernel 이 그 역할(`eq:single_kernel`); 이 baseline 이 실제로 닫히는지(F2: δ baseline 환원)가 승격 조건.

## 합류 반영 (G-series 지시)
- **Ch1 §closure**: ratio-substitution 을 **Plan A(검증 tier)** 로 명시, (c) 구조 + (d) 매핑 + (e) 차이를 본문/각주에 기록(P3-5 충족). Plan B(g-grid) = core/validator.
- **Ch6**: F1–F5(kernel mapping·δ baseline·Neumann 수렴·ε·fallback) gate 유지; 특히 (e)-2 broad-kernel 열화를 **stretched-tail 영역에서 ε 측정**으로 강제.
- **DQ-v3-2 갱신**: "Volterra→Fredholm 적용성" = (e)-1,2 로 구체화. 데이터·수치 검증 전까지 Plan A 는 candidate.
