# RB Ledger — Ch1 rebuilt Phase R1 (근사 닫힌 피팅식 자급 + §7~9 무생략 봉합)

- 일자: 2026-06-01
- 대상: `Claude/docs/graphite_ica_ch1_rebuilt.tex`
- 계획서: `Claude/plans/2026-06-01-ch1-rebuilt-fitting-closure-plan.md`
- 근거 감사: `Claude/results/AUDIT_CH1_REBUILT_ADVERSARIAL.md` (F절 H1~H8)
- 사용자 결정: ① "Ch1에서 근사 닫힌식까지" ② "챕터 6은 없앨 수도 있다" ③ "계획 한 번 + 업무는 쪼개서"
- cumulative steps: 40~49

## 수정 결과표 (H1~H8 — 모두 CLOSED)

| # | 등급 | 봉합 방식 | 위치(식/라벨) | 상태 |
|---|---|---|---|---|
| H1 | CRIT | $A_{0,j}=(Q_{j,\tot}/Q_p)a_j$ 구체식 부여(용량분율×접근성, L무관 상수) | eq:A0_def | CLOSED |
| H2 | HIGH | 동역학 잔차 $r_j(q_a)$ 를 $A_0$ 에서 분리해 별도 인자로(역산금지 자가당착 해소) | eq:kernel_integral 본문 | CLOSED |
| H3 | HIGH | $\sum_{j=1}^{N_p}$ 복구 + 두 다중성(이산 전이/연속 $\rho_{G,j}$) 분리 명시 | eq:kernel_integral, eq:volterra, §8 진입 박스 | CLOSED |
| H4 | HIGH | $\Theta,\Theta_\eq,\Theta_\mathrm{init},\Theta_\mathrm{tail}$ 를 §8 진입부에 정의 | eq:theta_family | CLOSED |
| H5 | MED | $g$ = barrier $G$ 의 한 실현값·적분 더미(단위 J/mol) 첫 사용 명시 | §7 line 428 | CLOSED |
| H6 | HIGH(결정) | **Ch1 근사 닫힌식(frozen-target KWW)** 신설 → 단독 fit 가능 | eq:kww, eq:kww_params | CLOSED |
| H7 | MED-HIGH | ~~shoulder/far-tail 분리~~ → **§5(line354) 수정은 §≤6 보호 위반이라 원복**. 원문(정직 BOUNDED) 유지. 추가 명료화는 별도 reviewed step. | §5 Marcus bound(원복) | **DEFERRED(원복)** |
| H8 | MED | 피팅 기본=eq:kww(frozen forward), 정확=eq:volterra(self-consistent), 1차근사 관계 못박음 | §8 "어느 식을 피팅에" + boundbox | CLOSED |

## ⚠ 정정 (사용자 6-1 지시 반영)
- §1~6은 완성도 높음 → **수정·요약 금지, 보완만**. R1의 H7 편집이 §5(line354)를 수정 → **원복 완료**.
- H7은 현재 **UNRESOLVED**(원문 정직 표기 유지). 추가 명료화는 §≤6 보완 또는 §7+ 처리로 별도 reviewed step.
- 나머지 H1·H3·H4·H5·H6·H8 = §7~9(작업 구역) 내 → 유지, retroactive 10점 검수 대상.
- 향후 step별 순차 + 매 step 10점 검수(plan §6) 적용.

## 근사 닫힌식 (Ch1 deliverable)
$$\frac{d\Theta_\text{tail}}{dq}\approx\sum_j A_{0,j}r_j(q_a)\frac{\beta_j}{\tau_j}\Big(\frac{q-q_{a,j}}{\tau_j}\Big)^{\beta_j-1}e^{-((q-q_{a,j})/\tau_j)^{\beta_j}}$$
$\tau_j=L_0e^{(G_{0,j}-\chi_j\mathcal A_j)/RT}$, $\beta_j=\beta(\sigma_{G,j}/RT)$. 정규 배리어→log-normal $L$→KWW(근사). $\sigma_G\to0$ 면 단일지수 환원(해석적 무결성 점검 명시).

## Ch.6 약결합 (결정: 미정 → 보수적)
- 적재 포인터(§8 닫기·§9 S5·deliverable·헤더주석·KWW앞 박스) → "수치 구현(별도 후속; 잠정 Ch6)" 중립 표기.
- 전달절(line ~671) 및 roadmap/parenthetical "(Ch.6)" 일부(L85,97,182,409,481,491) = **보존**(사용자 무선호 → 전달절 보존 원칙).

## 검증 (실행)
- xelatex 2-pass: exit 0 / exit 0
- undefined reference·citation: **0**
- LaTeX error: **0**, 중복 라벨: **0**, overfull hbox: 5(경미, 기존수준)
- 새 라벨 4개(A0_def/theta_family/kww/kww_params) 단일정의·참조정합(eqref 10회)
- 차원: $A_{0,j}$ 무차원, $A_{L,j}^{prob}$ 밀도, $\tau_j$=q 단위 — 정합
- PDF: graphite_ica_ch1_rebuilt.pdf (347 KB) 갱신

## P3 7항목 (재평가)
1. V_n 일가 구분: 영향 없음 PASS
2. 전하 보존 중심식: eq:A0_def 가 Q_{j,tot}/Q_p 를 전하보존서 도출로 명시 — 강화 PASS
3. 순환의존 dependency graph: **미작성(G1, 다음 phase)** — 보류
4. 순환 4분류: **미작성(G2, 다음 phase)** — 보류
5. ref.6,7 4항목 sub-section: 본 phase 범위 외 — 미해당
6. Ch1↔Ch2~5 전달 정합: 전달절 보존, kernel 구조 변경이 ver.N 전달식과 충돌 없음(점검 필요 → C2 차기)
7. ver.N vs Chapter 명칭: 혼동 없음 PASS

## Retroactive 10점 검수 (§7~9 batch — step 50)
batch로 들어간 H1·H3·H4·H5·H6·H8을 plan §6 10점 체크리스트로 재검수:
1. 앞 정합성: Θ 일가가 §4 logistic($\xi_{\eq,j}$)·§3 전하보존($Q_{j,\tot}$)과 정합 — PASS
2. §≤6 불변: H7 §5 수정 원복 후 §1~6 본문 무변경(diff 확인) — PASS
3. 컨벤션: 기존 $q_a,\rho_G,Q_p,Q_{j,\tot}$ 보존; 전이별은 $j$ 첨자로 확장 — PASS
4. 논리 전개: 두 다중성(이산 $\sum_j$/연속 $\int dL$) 분리, KWW가 식21에서 frozen-target로 따라옴 — PASS
5. 차원: $A_{0,j}$무차원, $A_{L,j}^{prob}$밀도, $\tau_j$=q단위 — PASS
6. 정의 선행: **FAIL→FIX** — $q_{a,j}$(§6 $q_a$의 전이별), $\rho_{G,j}$(§7 $\rho_G$의 전이별) 깨끗이 정의; $r_j(q_a)\to r_j(q_{a,j})$ 전 식 일관화(eq:kernel_integral·eq:kww·single-mode)
7. 라벨: 중복 0, 신규 4개 정합 — PASS
8. 빌드: 2-pass exit0, ref/cite 0, error 0 — PASS
9. BOUNDED: KWW β 사상·frozen-target 근사 정직 표기 — PASS
10. P3: 2 PASS강화 / 3·4 보류(G1·G2) — 부분

**검수 발견·수정**: I-1($q_{a,j}$ 정의·$r_j$ 첨자 불일치), I-2($\rho_{G,j}$ 명시) → step 50에서 봉합, 재빌드 0/0.

## Next Step (step 51~)
- G1/G2(순환 의존성 dependency graph + 4분류 박스) — P3-3·4 FAIL 해소
- C2: Ch1 kernel 구조 변경(Σ_j·eq:kww)이 Ch2~5 전달식과 정합하는지 교차검증
- C3/GS-3: 본문 AL-# ↔ RB_AL_MASTER 일치
- Ch6 제거 확정 시 전달절(line ~671) 재배치
