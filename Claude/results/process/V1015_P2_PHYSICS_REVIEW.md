# V1015 P2 — Fable 물리 논리 6종 검토 보고 (2026-07-05)

> 마스터 = `../../plans/2026-07-05-v1015-code-doc-sync-master-plan.md`(rev.2) P2(Steps 5–8). 스킬 §4.1 검증-전용 모드 + §4 교차합의 triage. **대상 = Ch1(3445줄)·Ch2(794줄) 물리·화학 논리**(격자 퇴출로 교체될 §N1/§N8/eq:branch/ν/부록 A R5 제외 — P3 소관). **원칙 = 기본 무수정·보고만. 수정 여부는 박사님 결정(Decision Gate).**

## 방법
- **6종 독립 검토**(Agent, 무통신, 다른 세션): Opus 3(R-O1·R-O2·R-O3) + Codex 3(R-C2·R-C3b·R-C1b). Fable 불가 → master 판정 = Opus. Codex 3 중 2건은 async job으로 재기동(foreground). 전원 Ch1·Ch2 전문 정독(Read Coverage missing 0 자기선언).
- **교차합의 triage**: ≥2종 공통 = 진짜 문제 가능성 높음(채택 후보) / 1종 단독 = master(Opus) 정밀 재검(원문 재정독·재유도)으로 진위 확정.

## 총평
**세 Opus 전원 "확정 CRIT/HIGH 물리 결함 0"** — 부호 8/8·히스 gap Taylor 극한(부호 함정 회피 포함)·Sommerfeld 전자엔트로피 2경로 교차검증·detailed balance·spinodal·config 부분몰·Ch1↔Ch2 정합(ξ=1−θ)·가역열 부호·Kirchhoff 일관성을 재유도·재산출로 전건 통과. 수치(86.7 mV·2.131 RT/F·−46 J/mol·K·1.1 k_B/atom 등) 전부 자립 재계산 일치. **박사님 평가("근접 정답 수준")가 6종 독립 검증으로 확증됨.** 아래는 그 위의 미세 갭.

---

## Tier 1 — 확정 물리 오류 (1건, master 재유도 확정)

**[P2-1 | LOW | Ch1 L2684–2685 (eq:Se 유효경계 서술) | Sommerfeld 전자 엔트로피 보정항 오귀속]**
- **문건 서술**: "동결 g≈g(E_F) 의 정확형은 보정항 **∝ g′(E_F)·(k_BT)² (Mott 항)**, 상대 크기 O[(k_BT/E_F)²]를 포함하나 … 무시할 수준."
- **오류(master 재유도 확정)**: $S_e=k_B\int g(E)\,s(\zeta)\,dE$, $\zeta=(E{-}E_F)/k_BT$, 엔트로피 핵 $s(\zeta)$ **짝함수**. $g$ 를 Taylor 전개하면 $g'(E_F)$ 항은 $\int\zeta\,s(\zeta)\,d\zeta=0$(홀×짝)으로 **패리티 상쇄** → 첫 보정은 $\tfrac12 g''(E_F)(k_BT)^3\!\int\zeta^2 s\,d\zeta$ = **O(T³)**, 즉 $g''(k_BT)^3$. $g'(k_BT)^2$ "Mott 항"은 thermopower·전도도(또는 fixed-N μ(T) 이동) 소관이지 엔트로피의 선도 보정이 아니다.
- **영향**: 무시가능 결론(k_BT/E_F~0.03)은 유효(보정은 여전히 작음)·모델 수치 불변. **explanatory prose의 항 귀속만 오류** → LOW.
- **발견**: R-C1b(Codex 단독). **Opus 3종은 선도항·2경로 교차검증은 검산했으나 이 "유효경계" 보정항 귀속은 미검. 다모델(Codex) 검토가 잡은 실질 사례.**
- **권고 수정(박사님 결정)**: "∝ g′(E_F)(k_BT)²(Mott 항)" → "선도 보정은 $g''(E_F)(k_BT)^3$(g′ 항은 엔트로피 핵 패리티로 상쇄); 상대 크기는 여전히 O[(k_BT/E_F)²] 급으로 무시가능" 로 1–2문장 정정.

---

## Tier 2 — 확정 문서 완결성·서술 갭 (≥2종 공통, 물리 오류 아님, 3건)

**[P2-2 | MED | Ch2 use-this 박스 L717–732 + "측정급 비선형" L522 ↔ srcbox L525–535 | 3종 공통(R-O1·R-C2·R-O3)]**
- 가역열 완전식 config 항 $(n_jR/F)\ln[\xi_j/(1-\xi_j)]$이 **지배 전이인 흑연 two-phase(LiC₁₂·LiC₆)**에 적용됨. 발산형 solid-solution config는 two-phase plateau의 진짜 가역 엔트로피가 아니고(plateau 평형은 $\partial U/\partial T=\Delta S_\rxn/F$·발산항 0), 그 기여는 폭이 $T$-동결이면 뒤집힌다(~0.3 mV/K).
- ★**doc가 이미 caveat 보유**: srcbox(L525–535)가 "완전식 일치는 해석 미분 사슬의 자기일관성 검증이지 two-phase 폭이 실제 $n_jRT/F$ 스케일한다는 실측 검증 아님; 실측 $w_j$ 가 $T$-동결이면 우열 뒤집힘" 을 명시. **문제 = 그 caveat이 use-this 조작 박스(L717–732)·"측정급 비선형 자동생성"(L522–523) 결론에 전파되지 않아, 지배 two-phase 전이에 대해 미검증 전제 위에 강한 결론이 얹힘.**
- **권고**: srcbox caveat을 use-this 박스에 1문장 전파 + "측정급 비선형 자동생성" 을 "모델 내 자기일관 산출(two-phase 폭 $T$-의존은 round-trip 확정 대상)" 로 완화.

**[P2-3 | LOW–MED | Ch1 verifybox L2458–2465 | 2종 공통(R-O2·R-O3)]**
- "$\Delta S^{cat}_\rxn\approx+80$ = config+vib+elec **세 성분의 합**" 이라 규정 후 곧바로 "$+80-46\approx+34$" 로 전자항 −46 을 **다시 차감** → 자기모순 라벨(+80이 elec 포함이면 이중차감, config+vib 기저면 "세 성분 합" 거짓). 부호 sanity 박스라 모델 결과식엔 전파 안 됨.
- **권고**: "$+80$ 은 MIT 창 **밖** 대표 SOC 기준 config+vib(elec≈0)" 로 1구절 못박아 이중차감 오독 제거. 결론(전자항이 총부호 못 뒤집음) 방향은 옳음.

**[P2-4 | LOW–MED | Ch1 §sec:lco-Se·Ch2 §vibel | 2종 공통(R-O1·R-O3)]**
- "config·vib 는 상수 $\Delta S$, 전자만 $\propto T$ → $U\propto T^2$ 곡률이 전자 신호" 의 식별이 **vib 부분몰 엔트로피의 엄밀 $T$-무관**을 전제하나, 이는 고전(고온) 극한 $k_BT\gg\hbar\omega$ 에서만. LiCoO₂ 포논 수백 K → 300 K 준양자, 잔여 $T$-의존이 작지만 0 아님(config 부분몰은 fixed-x 에서 엄밀 $T$-무관이 맞음 — vib만 근사).
- **권고**: vib $T$-무관이 고전 극한 근사임을 1문장 명시(Ch2 §5 코너 각주와 동급 한정). 다온도 곡률 피팅 시 vib 잔여 $T$-계수가 전자 $a_e$ 에 소량 섞일 수 있음.

## Tier 3 — 공개된 불확실 (advisory, 은닉 결함 아님, 1건)

**[P2-5 | LOW/불확실 | Ch1 §sec:lco-Se·gate | 2종(R-O1·R-O2), 둘 다 공개 인지]**
- 전자엔트로피 $-46$ J/(mol·K)=$-5.5\,k_B$/atom(게이트 골)·$g{=}13$ e/eV/atom → $S_e{\sim}1.1\,k_B$/atom(자유전자 $\sim$30배)은 큰 값이고 MIT 중심에서 Sommerfeld 동결-$g$ 가 가장 취약. **단, doc(L2689–2698)가 이미 tier 분리 명시**(함수형 tier-A·단일 anchor tier-A·연속 곡선 tier-C 갭 G2·round-trip 위임). → **은닉 아님·조치 불요**. round-trip 단계에서 $g_{\max}{=}13$ 단위(원자당 vs 화학식당) 재확인 권고만.

## Tier 4 — 단독 재검 결과 (오적발 필터)

| 원발견 | master 재검 판정 |
|---|---|
| **R-C3b-1** (major, 히스 분기 가역열 ∂_TΔU_hys 항 생략) | **LOW 강등** — eq:hys_branch 단일분기식이 분기-홀수항 $\tfrac12\sigma_d\partial_T\Delta U_\hys$ 생략은 맞으나, 가역열은 **분기 평균**이라 이 항 상쇄(doc eq:hys_rev·keybox가 유도·gap=비가역 분리 명시). 비대칭 분기 ∂U/∂T는 "범위 밖" 선언. 물리 결과 오류 아님·eq:hys_branch 완결성 소폭. |
| **R-C1b-2** (V-의존 전자 plug-in vs peak 미분) | **현행 정합·P4 advisory** — doc(L3102–3103)가 freeze(ΔS_e·조성 $x{=}x_\mathrm{center}$ $V$-무관 동결) 명시 → eq:lco-eqpeak $\xi(1-\xi)/w$ 옳음. 단 **정밀형(비동결) 구현 시 peak 미분에 $(1-\partial U/\partial V)$ chain-rule 필요** — P4 전자항 정밀형 착수 시 반영. |
| **R-O2-2** (ΔS⁰=+29 dilute 끝점을 중심값) | **기각** — R-O3 명시 반증. doc가 "+29 끝점은 config 겹침 구간 대표값" hedge·전 표 "초기값·피팅 override" 선언. 나머지 3전이 창 내부라 무해. |

---

## 종합
- **확정 물리 오류 = 1건(P2-1, LOW, Sommerfeld 보정항 오귀속)** — 유일한 물리 content 정정.
- **문서 완결성·서술 갭 = 3건(P2-2 MED·P2-3·P2-4 LOW–MED)** — 전부 1–2문장 caveat/명시 추가급, 물리 로직 무변경.
- **공개 불확실 1건(P2-5)·단독 기각/강등 3건.**
- **박사님 결정 필요(Decision Gate)**: 위 P2-1~P2-4 를 수정할지(권고: 4건 모두 저위험 국소 수정 — P2-1 실오류·P2-2~4 완결성) / P2-5·단독 3건은 무조치. **기본값 = 무수정 원칙이라 박사님 승인 시에만 P3 착수 중 반영.**
