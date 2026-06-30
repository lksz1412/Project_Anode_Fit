# R3 — 가역열 부호(exo/endo) + Bernardi + 챕터 충실도 (검토1, 검수 sub)

> 대상 9종(v4-01..09). Ground truth: REVIEW_RISK_PATTERNS ★위험3, 41_statmech_spine.md, base_ch2_v3.tex(Bernardi).
> 판정식: $\dot Q_\rev=-IT\,\partial U/\partial T=-(IT/F)\Delta S$. 방전 $I>0$. **$\Delta S>0$(희박/저-x) → $\dot Q_\rev<0$ = 흡열(endo)**. **$\Delta S<0$(만충/stage 2→1) → $\dot Q_\rev>0$ = 발열(exo)**.

---

## (a) 9종 exo/endo PASS/FAIL · 챕터 충실도 랭킹

### exo/endo PASS/FAIL (★위험3)

| 빌드 | exo/endo | 근거(줄) | 판정 |
|---|---|---|---|
| **v4-01** | **PASS** | L565–566·578–579: ΔS>0 희박→흡열, ΔS<0 stage2→1→발열, stage4→3 방전흡열·stage2→1 방전발열 (전부 정합) | ✅ |
| **v4-02** | **FAIL (CRITICAL)** | L637–644: "ΔS>0(저-x)→$\dot Q_\rev>0$ 발열", L642 "저-x ΔS>0→방전 발열", L643–644 "stage2→1 ΔS<0→강한 흡열" — **전면 역매핑**. L638 "ΔS<0→$\dot Q_\rev<0$" 대수 자체도 틀림($-(IT/F)\cdot$음=양) | ❌ |
| **v4-03** | **PASS** | L615–617·686: ∂U/∂T>0 방전→$\dot Q_\rev<0$ 흡열, 저-x(ΔS>0) 방전흡열·고-x(ΔS<0) 방전발열. fig caption 도 정합 | ✅ |
| **v4-04** | **FAIL (CRITICAL)** | L777 일반문은 OK이나 L799 "희박서 +(방전 **발열**), 만충서 −(방전 **흡열**)", L800–801 "stage2→1 큰 음 ΔS→가역 **흡열**" — ★위험3 명시 line777/799 결함 실재. 자식 reviewer 도 적발 | ❌ |
| **v4-05** | **FAIL (CRITICAL)** | L654–655 "저-x config 양 발산→방전 $\dot Q_\rev>0$ 발열", "고-x→흡열으로 돈다", L656–657 "stage2→1 음 ΔS→가역 **흡열**" — 양방향 역. (챕터 구조는 우수하나 부호 inverted) | ❌ |
| **v4-06** | **FAIL (CRITICAL)** | L769–770 "저-x 양⇒방전 $\dot Q_\rev>0$ 발열, 고-x 음⇒흡열", L370–372 "고-x 음 baseline→흡열 신호", L770–772 "stage2→1 음 ΔS→calorimetry 가역 **흡열** 정합" — 일관 역매핑 | ❌ |
| **v4-07** | **PASS** | L104–105·595–596: 방전 ∂U/∂T>0→$\dot Q_\rev<0$ 흡열, 충전 부호 반전 명시. ξ=de-lith·config=$+R\ln[\xi/(1-\xi)]$(L639–640) 정합. per-stage exo/endo 라벨은 *안전하게 절제* | ✅ |
| **v4-08** | **PASS(절제)** | L404·628–631: 일반 규칙만(∂U/∂T 부호로 가역열 부호 반전·전류반전). 위험한 per-stage 라벨 미주장. stage표는 ΔS 부호만(595–598). 단 ★위험7 w_eff 역수형(L624) 잔존 — **R1/R2 영역** | ✅(exo/endo 한정) |
| **v4-09** | **PASS(절제)** | L86–92·404–406: 일반 규칙 정확. ξ→0 만충/ξ→1 희박→±∞(L256–257, ★위험1 정합). stage표(595–598) ΔS 부호만, exo/endo 미주장 | ✅ |

**PASS 5 (01·03·07·08·09) / FAIL 4 (02·04·05·06, 전부 CRITICAL 역매핑).** FAIL 4종은 동일 결함 클래스 = "희박 +ΔS→방전 발열" 역(정답=흡열). Opus 3종(04·05·06)이 전원 FAIL, Sonnet/Codex 가 더 안전.

### Bernardi 틀 보존·재서술 (가역/비가역 분리)
9종 전부 $\dot Q=I(U-V)-IT\,\partial U/\partial T$ 골격·$\dot Q_\rev$ box·$\Delta S=+F\,\partial U/\partial T$ 규약 보존(v3 정합, 부호규약 통일문 유지). **봉합(가역열=분포 재배열 열) 재서술**: v4-04(Part7 전용 절)·v4-05·v4-06(distbox)·v4-09(맺음)이 명시 우수. v4-07·08 은 간결하나 정확. Bernardi 보존 = 9종 PASS, 차등은 *재서술 깊이*만.

### 챕터 충실도 랭킹 (분포 전개=챕터 본체·서사 다리·분량 자연결과)
1. **v4-05**(720L) — warnbox 범위가드+6코너 극한+세 분포 distbox, 절도입/마무리 다리 충실. (단 exo/endo FAIL)
2. **v4-04**(872L) — Part1–7 명시 골격·수치검증(0.000 mV/K)·부분몰 절. (config-sign+exo/endo CRITICAL)
3. **v4-06**(820L) — Ch1↔Ch2 분업 명문(L94–96)·distbox 통일렌즈. (exo/endo FAIL)
4. **v4-07**(744L) — 사슬 box·다온도 workflow·정직 범위절. **부호 clean**
5. **v4-03**(810L) — 도입→분포→config→vib/el→겹침→가역열 서사. **부호 clean**
6. **v4-02**(791L) — 분포 전개 충실하나 exo/endo CRITICAL
7. **v4-01**(775L) — 사슬 명확·부호 clean, 다리 다소 짧음
8. **v4-09**(651L) — 영문혼용 많고 prose 밀도 낮으나 정확
9. **v4-08**(451L) — **최단·챕터급 미달**(절 도입/마무리 다리 부족, "한 절+" 수준에 근접)

---

## (b) 흐름·봉합 best 초안 · 체리픽 추천

- **exo/endo 맞은 초안 best = v4-07**: 방전 ∂U/∂T>0→흡열·충전 반전 명시(L104,595–596), ξ=de-lith·config=$+R\ln[\xi/(1-\xi)]$ 정합, 이중계산 B 명시, 위험한 per-stage 라벨 절제(역매핑 0). v4-03 도 per-stage 까지 **맞게** 적은 유일 PASS 라 *서술 payoff* 는 더 큼.
- **챕터 충실도·봉합 서사 best 골격 = v4-05/v4-04**(범위 warnbox·세 분포 distbox·Part 골격·다리)이나 **둘 다 exo/endo CRITICAL**.
- **Ch1↔Ch2 봉합 best 문장 = v4-06 L94–96**("Ch1=평형 모양 / Ch2=같은 분포의 엔트로피·온도·가역열, 재유도 X").
- **★체리픽 추천**: **base = v4-07**(부호 clean·정직 범위·이중계산 B). 여기에 **(1) v4-05/04 의 챕터 골격(범위 warnbox·세 분포 distbox·극한 6코너)** 이식, **(2) v4-03 의 *정확한* per-stage exo/endo 문단**(저-x 방전흡열·고-x 방전발열) 채택, **(3) v4-06 L94–96 봉합 문장** 삽입. **단 FAIL 4종(02·04·05·06)에서 exo/endo 문단은 절대 이식 금지**(부호 오염원).

---

## (c) 결함표

| # | 빌드 | 위치 | 심각도 | 결함 | 정정 |
|---|---|---|---|---|---|
| 1 | v4-02 | L637–644 | CRITICAL | exo/endo 전면 역매핑+L638 대수 오류 | ΔS>0→흡열, ΔS<0(stage2→1)→발열 |
| 2 | v4-04 | L799–801 | CRITICAL | "희박 +→방전 발열, 만충 −→흡열, stage2→1→흡열" 역(★위험3 명시) | 희박→방전 흡열, stage2→1→발열 |
| 3 | v4-05 | L654–657 | CRITICAL | "저-x→발열, 고-x→흡열, stage2→1 음ΔS→흡열" 역 | 부호 전면 반전 |
| 4 | v4-06 | L369–372,769–772 | CRITICAL | "저-x→발열·고-x→흡열·stage2→1→흡열" 역 | 부호 전면 반전 |
| 5 | v4-08 | L451 전체 | HIGH | 최단(451L)·챕터급 다리 미달(절 도입/마무리 빈약) | 도입·마무리 다리 보강 또는 base 부적격 |
| 6 | v4-08 | L624 | CRITICAL(교차) | w_eff=w/[1−Ω/2RT] 역수형(★위험7) — **R1/R2 영역, cross-note** | w_eff=w(1−Ω/2RT) |
| 7 | v4-09 | 본문 다수 | MED | 영문/한글 혼용 과다·prose 밀도 낮음(챕터 문체 약화) | 한글 prose 정리 |
| 8 | v4-04 | (config-sign 473/605/793) | CRITICAL(교차) | config 부호 결함 — **R1 영역, cross-note**. exo/endo FAIL 과 동반 → base 부적격 강화 | — |

**메타**: exo/endo 위험3 은 Opus 3종(04·05·06)에 집중 + v4-02. 부호 PASS 5종 중 *per-stage 까지 맞게 서술* = v4-01·v4-03·(v4-07 은 절제). 체리픽 base 는 v4-07, exo/endo 서술은 v4-03, 챕터 골격은 v4-05 에서 *부호만 정정해* 이식.
