# REVIEW_B — v7-10 적대 재검수 (검수 sub B)

대상: `v7-10.tex` (879줄, 16p PDF) — v7-06b 베이스 + 체리픽 graft(tab:inputs·6단계 재현 박스).
기준: `v7-00_spine/AUTHOR_BRIEF.md` · `v7-00_spine/Anode_Fit_v11_final.py` 전문 정독.
검수 렌즈: G-follow · G-usable · 그림 6개 · 형식/이음새 · 시각(PDF 16p 전 페이지 렌더 판독).
방식: refute mandate — 한 번에 OK 거부, 가장 약한 3곳 강제 적발, 빈 통과 금지.

---

## 1. 확정 결함 {심각도 · 행 · 내용}

### D1 (HIGH · G-usable/G-follow) — `w_j=n_jRT/F` 기본 폭이 라벨 없는 식이고, 3곳이 잘못된 eq:weff 를 참조
- **현상**: 평형 peak 의 분모인 **기본 폭** `w_j=n_jRT/F` 는 본문에서 **번호 없는 산문(L435)** 으로만 등장한다. 유일한 `\label{eq:weff}` 는 식 (1.11) = *옵션* 유효폭 `w^eff=(RT/F)(1−Ω/2RT)` 에 붙어 있다(L438–441, aux 확인: eq:weff={1.11}).
- **잘못된 참조 3곳**:
  - `tab:inputs` L753: `\code{w} 또는 \code{n} ... 폭 $w_j=n_jRT/F$ (\eqref{eq:weff})` → 기본 폭을 설명하며 *옵션* 식 (1.11) 을 가리킴.
  - `tab:nodemap` L810: `N4 & $w_j=n_jRT/F$ ($w^\eff$) & \eqref{eq:weff}` → 동일.
  - `keybox` 6단계 재현 박스 L785: `폭 $w_j$(\eqref{eq:weff})` → 동일.
- **영향(G-usable)**: 6단계 재현 박스 step (3) 을 그대로 따르는 독자는 "폭 = eq:weff" 를 보고 *기본값 w=nRT/F* 대신 *옵션 narrowing w^eff* 를 쓰게 된다. 코드 기본은 `use_w_eff=False`(L224·`_width` L283–288 → `func_w`)라 곡선이 어긋난다. **이 문건만으로 v11 곡선 재현 시 폭이 틀어지는 직접 함정.**
- **권고(v7-11)**: 기본 폭 `w_j=n_jRT/F` 를 번호식(예 eq:wbase)으로 승격하고, 위 3곳 참조를 eq:wbase 로 교정. tab:inputs/nodemap 의 `w` 행은 (eq:wbase) + 옵션은 (eq:weff) 로 분리 표기.

### D2 (HIGH · G-follow) — L_q "forward 극한" 진술이 eq:Lqfull 의 `1/(1+e^{−A/RT})` 분모를 만들어내지 못함(비약)
- **현상**: L536 은 `k_j ≃ k0·exp[−(ΔG_a−χA)/RT]` 를 "**forward 극한**"으로 선언한 뒤 곧장 eq:Lqfull(L575) 로 간다. 그러나 eq:Lqfull 에는 **추가 분모** `1/(1+e^{−A/RT})` 가 있다(코드 `func_L_q` L96 `− log(1+exp(−A/RT))` 와 정합 — *결과식은 맞다*).
- **결함**: 순수 forward `k_j` 만으로는 `1+e^{−A/RT}` 항이 나오지 않는다. 이 분모는 net BV(정−역) 형태에서만 나온다. L536→eq:Lqfull 사이에 그 다리(net rate / 역방향 항)가 빠져 학부생이 따라갈 수 없다. AUTHOR_BRIEF §4 "산문-only 유도단계는 명시 중간식으로 승격" 위반.
- **권고**: `k_j` 를 net 형(정−역 또는 forward×(1−역/정))으로 한 줄 중간식 추가 → `1+e^{−A/RT}` 가 어디서 오는지 명시. 또는 "forward 극한" 문구를 정정.

### D3 (HIGH · 시각/형식) — 마지막 페이지 헤더 "16/15"(LastPage 1쪽 오류) + tab:nodemap 16p 로 분리
- **현상**: PDF 실제 16p 인데 우상단 헤더가 마지막 장에서 **"16/15"** 로 찍힌다(p16 렌더·pdftotext 둘 다 확인). `\pageref{LastPage}` 가 15 로 굳었다. 로그에 `LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right.` 가 남아 있고 **2-pass 로 수렴 안 됨** — tab:nodemap 이 15→16p 로 넘치면서 페이지 수가 1 늘어 LastPage 가 어긋났다.
- **권고**: xelatex 3-pass(또는 latexmk) 로 재빌드해 LastPage 수렴. 더불어 tab:nodemap 을 p15 안에 들어오게 `[t]`/`[h]` 배치 조정 검토(현재 14→15→16 로 표가 페이지를 가른다).

### D4 (MEDIUM · G-follow) — eq:eqcond 두 등식 연결 미유도
- L306–307: `μ_Li(θ_eq)=μ⁰−sF(V−U)` 와 `ΔG_j=−sFU_j` 를 나란히 선언만 하고, 두 등식의 연결(왜 ΔG=−sFU 인가)을 산문 괄호("U는 비배치 몫 자유에너지의 전위 환산")로만 처리. Nernst 관계가 assertion. 평형 중심 절의 출발 식이라 G-follow 부담.
- **권고**: μ 균형 → ΔG=−sFU 한 줄 중간식(또는 짧은 도출) 보강.

### D5 (MEDIUM · G-follow) — eq:xieq logistic 유도 3단계 점프
- L447–452: "점유비=Boltzmann 비 `e^{A/RT}` (detailed balance) → 진행률로 풀면 logistic" 으로 직행. 빠진 단계: (a) `ξ/(1−ξ)=e^{A/RT}` → `ξ=1/(1+e^{−A/RT})` 대수, (b) `A/RT=sF(V−U)/RT` 를 `σ_d(V−U)/w_j`(w=RT/F) 로 환산하는 단계. 가장 물리 적재된 평형식인데 세 단계가 산문 뒤로 숨음.
- **권고**: `ξ/(1−ξ)=e^{A/RT}` 와 `A/RT=σ_d(V−U)/w_j` 두 중간식 명시.

### D6 (LOW · 형식) — Overfull \hbox 4건(L188, L197, L297-staging longtable; L777-780 prose; L381-386)
- L197 17.3pt, L777-780 22.6pt 가 가장 크다. PDF 판독상 longtable·tab 본문이 margin 밖으로 **육안 침범은 안 보임**(115·150dpi 렌더 확인)이라 치명은 아니나, L777-780(전체 인자 표 뒤 산문)·L188/197(notation longtable 셀) 줄바꿈 미세 조정 권고. `\emergencystretch` 이미 2em 인데 잔존.

---

## 2. 가장 약한 3곳 (refute 집중)

1. **D1 — 기본 폭 라벨 부재 + 3중 오참조** (가장 약함). G-usable 닫힘을 깨는 유일한 "재현 시 곡선이 틀어지는" 함정. 6단계 박스가 graft 의 핵심 셀링포인트인데 그 안의 참조가 옵션식을 가리킨다.
2. **D2 — L_q forward-극한 비약**. 결과식은 코드와 정합하나 유도가 닫히지 않아 "이 문건만으로 따라간다"가 깨지는 가장 큰 G-follow 구멍. 동역학 절(graft 인접)이라 이음새 점검에서도 약점.
3. **D5 — logistic 유도 점프** + **D4 eqcond**. 평형 골격 두 출발식이 둘 다 assertion-heavy. 묶어서 한 라운드 보강 가치.

---

## 3. 혼란 유발 그림 유무 (그림 6개 판정)

| 그림 | 라벨 | 신규 TikZ | ASCII 전용 | 본문 \ref | 식 정합 | 혼란? |
|------|------|-----------|-----------|-----------|---------|-------|
| spine | fig:spine | O | O | O(서론) | N0–N9 순서 정합 | **무** — 명료, per-tr loop 점선 상자 양호 |
| staging | fig:staging | O | O | O(§1) | 4전이 U 정합 | **무** — 갤러리 채움·양방향 화살표 명료 |
| hysloop | fig:hysloop | O | O | O(§1.4) | ξ_s^±=0.146/0.854(Ω=4RT) 좌표 정확, dis 좌상/chg 우하 방향 정합 | **무** |
| logistic | fig:logistic | O | O | O(§1.5) | S-curve + 벨(max ¼ @z=0) 정합 | **무** |
| reversal | fig:reversal | O | O | O(§1.8) | (a)dis→高V (b)chg→低V 거울, 점선=평형종 정합 | **무** |

**혼란 유발 그림 0개.** 6개 모두 신규 TikZ·렌더 ASCII 전용(소스 한글 주석은 무해)·본문 \ref 사용(orphan 0)·식과 좌표 정합. 기존 v5/v6 그림 문제(이해 저해) 재발 없음. 그림은 합격.
(주의: figure 환경은 5개. spine/staging/hysloop/logistic/reversal — AUTHOR_BRIEF "6개" 언급은 task 측 표현이며 실제 본문은 5개 figure + 3개 table. 5개 모두 양호.)

---

## 4. G-usable 닫힘 여부

**부분 닫힘 — D1 으로 1곳 새는 닫힘.** tab:staging(4전이 초기값)·tab:inputs(전 인자·기본값)·tab:nodemap(노드↔식↔코드)·6단계 박스가 구조적으로 완비돼 있고, eq:Lqfull·eq:Acut·eq:chid·eq:dHeff·eq:reversal 모두 코드 식별자와 1:1 정합(func_L_q·min(z_cut·n·RT,A_cap·RT)·func_chi_d·func_dH_a_eff·`[::-1]` 역전 전수 대조 통과). **단 D1(폭 기본식 오참조)** 때문에 6단계 박스를 글자 그대로 따르면 폭이 옵션식으로 흐를 위험 — 이 한 곳을 막으면 닫힘 완성.

---

## 5. v7-11 보완 권고 (우선순위)

1. **[HIGH] D1**: `w_j=n_jRT/F` 번호식 승격 + tab:inputs/tab:nodemap/keybox 3곳 참조 교정.
2. **[HIGH] D2**: L_q net-rate 중간식 추가(`1+e^{−A/RT}` 출처 명시) 또는 "forward 극한" 문구 정정.
3. **[HIGH] D3**: 3-pass 재빌드 → "16/15" 헤더 수렴 + tab:nodemap 페이지 분리 완화.
4. **[MED] D4·D5**: eqcond(ΔG=−sFU)·xieq(logistic 대수+w 환산) 중간식 1줄씩 보강.
5. **[LOW] D6**: L777-780·L197 overfull 줄바꿈 미세 조정.

부호 사슬 8/8 정합·코드 1:1 대응·그림 5/5 무혼란은 확정. 핵심 구멍은 **D1(재현 함정)·D2(유도 비약)·D3(헤더/페이지)** 3건.
