# REVIEW1 — v8-09 (Codex) 적대 검수

> 검수 sub (리뷰 전용·수정/커밋 X). 대상 `v8-09/v8-09.tex` (1190행 전문 정독, ~500행 4청크).
> 기준 정독: `Anode_Fit_v11_final.py`(706줄)·`v11_flowchart.md`·`AUTHOR_BRIEF_v8.md`·`KNOWN_DEFECTS.md`(전수).
> 렌즈: ①G-derive ②배치 보존 ③부호 8항 v11 1:1 ④G-follow·G-usable·완결성 ⑤그림.

---

## 1. 확정 결함 (Confirmed)

### C1 — ★D-PEAK 미수정 (CRITICAL, 수학적 오류·v7-11 상속)
KNOWN_DEFECTS §D-PEAK 가 "삭제하라" 지목한 문장이 **그대로 잔존**.
- 행 919–920: "$L_V$ 가 작으면 $\xi_\mathrm{lag}\to$ 한 칸 뒤처진 $\xi_\eq$ 라, 식~\eqref{eq:peakshape} 가 이산 미분 $\to\dd\xi_\eq/\dd V$ 의 종으로 환원된다."
- **틀림**: $L_V\to0\Rightarrow\rho=e^{-\Delta_{grid}/L_V}\to0\Rightarrow\xi_{lag}\to\xi_{eq}$(같은 칸)$\Rightarrow(\xi_{eq}-\xi_{lag})/L_V\to 0/0$, 종 아님. $\to d\xi_{eq}/dV$ 환원은 **반대 극한 $L_V\gg\Delta_{grid}$**($\rho\to1$)에서만 성립.
- 완화 정황: 행 920–929 가 eq:branch 스위치($L_V<\nu\Delta_{grid}\Rightarrow\xi_{eq}(1-\xi_{eq})/w$)를 명시. 그러나 KNOWN_DEFECTS 요구 (a)(연속 정당화는 $L_V\gtrsim\Delta_{grid}$) (b)(작은 $L_V$ 평형 회복은 스위치로) 중 (b)만 충족, (a)의 *틀린 매끈 극한 서술 삭제*는 미이행 — 스위치 문장과 틀린 환원 문장이 **공존**(자기모순). 9종 공유 ★ 결함을 v8-09 가 잡지 못함.

### C2 — D-WEFF 중간식 누락 (G-derive)
행 543–548: eq:weff $w^\eff=(RT/F)(1-\Omega/2RT)$ 를 "상호작용이 종을 좁히는 옵션 유효 폭은" 한 줄 뒤 박스로 점프. KNOWN_DEFECTS 가 요구한 중심기울기 다리($sF\,dV/d\xi|_{1/2}=4Fw$, 이상 $4RT\leftrightarrow$일반 $4Fw^\eff$) **부재**. 브리프 §3 "한 줄 점프 금지" 위반.

### C3 — fig 곡선 데이터 중복 의심 (그림, MEDIUM)
fig:reversal (행 956–969) 의 방전 평형종(densely dotted)과 fig:logistic 미분 종은 별개지만, fig:reversal (a)(b)의 점선 평형종 좌표쌍이 동일(행 956=967) — 의도된 동일 평형종이라 결함 아님. 단 KNOWN_DEFECTS 가 v8-04 서 지적한 "fig:hysloop 와 byte 동일 중복"은 v8-09 fig:hysloop(행 489)이 독자 좌표라 **해당 없음(양호)**.

### C4 — 미사용 매크로 (LOW, 완결성)
preamble 행 51–55 의 `\dis`/`\chg`/`\hys`/`\rep` 중 `\work`(행 54) 정의됐으나 본문은 $V_\work$ 로 다수 사용 — OK. 단 `\app`,`\cell`,`\eff`,`\eq`,`\bg`,`\rxn` 전부 사용 확인. 실질 미사용 0(양호). **철회**.

---

## 2. KNOWN_DEFECTS 보유표 (전수)

| 결함 | 요구 | v8-09 상태 | 판정 |
|---|---|---|---|
| ★D-PEAK | "작은 $L_V$ 종 환원" 삭제 + (a)(b) | 틀린 문장 행919–920 잔존; (b)스위치만 | **보유(미수정)** |
| D-VEQ | eq:Veq 다리 forward-defer 제거 | §3(행370–410)서 g(ξ)→g′→V_eq 직접 유도, 순환 없음 | 해소 |
| D-DHEFF | $\chi_d$ 계수 중간식 | 행769–783 eq:barrier_split 중간식 명시 | 해소 |
| D-WEFF | 중심기울기 $4Fw$ 다리 | 행544 점프, 다리 없음 | **보유** |
| D-UBR | ansatz→현상학 매개변수화 명시 | 행459 "실측 분기 중심을 방향별 한 자유도로" 명시 | 해소 |
| D-VN(minor) | 이항 중간식 | 행263–269 자명 이항, 부호 검산 동반 | 해소(자명) |
| fig 식번호 오기/라벨 | overshoot 라벨·번호 | fig:hysloop(행482)이 대체, \ref 정합 | 해소 |
| eyring/bazant/dreyer 미인용 | 인용 | 행1182–1184 3건 모두 등재(단 본문 \cite 호출은 dahn/ohzuku/bloom/dubarry만 — eyring/bazant/dreyer 미참조 LOW) | 부분 |

---

## 3. 강점 3 / 약점 3

**강점**
1. D-VEQ·D-DHEFF·D-UBR 3개 v8-04 자체결함을 단계적 유도로 해소 — artanh gap(행426–436)·barrier_split(행769–783)·spinodal 대칭(행451–457) 사슬 완결.
2. 부호 8항 v11 1:1 정합(§부호검산 S1–S8 + falsifiable R1–R4 수치): $V_n=V_\app-\sigma_d|I|R_n$·$\xi_\eq$ 부호·$\chi_d$ 충전 $1-\chi$·격자역전 모두 코드(L412/L459/L477/func_chi_d)와 일치. dU_hys=86.7 mV 수치 회귀 박스(행1162)가 코드 self-test(L648)와 동일량.
3. G-usable 우수 — tab:staging·tab:inputs·tab:nodemap + 6단계 재현 keybox(행1091)로 "문건만으로 곡선 재현" 실증성 확보. 그림 6개(spine/staging/hysloop/logistic/memorykernel/reversal) ASCII-English·\ref 정합.

**약점**
1. ★D-PEAK(C1) 미수정 — 최우선 ★ 결함을 잡지 못함(틀린 환원 문장 잔존+스위치 문장과 모순).
2. D-WEFF(C2) 중간식 점프 — 브리프 핵심 "한 줄 점프 금지" 위반 1건.
3. eyring/bazant/dreyer 참고문헌 등재했으나 본문 \cite 미호출(orphan bib 3건, LOW).

## 4. 차원 점수 (합 / 35)

| 차원 | 점수/5 | 근거 |
|---|---|---|
| G-derive(유도 완결) | 3 | D-VEQ/DHEFF/UBR 해소 우수, 그러나 D-PEAK 틀린서술+D-WEFF 점프 잔존 |
| 배치 보존(v7-11) | 5 | 절순서 N0→N9·결과박스·식별자·표 그대로, 유도만 추가 |
| 부호 8항 v11 1:1 | 5 | S1–S8 전건 + R1–R4 수치 회귀, 코드 라인 정합 |
| G-follow(따라가짐) | 4 | 절 도입/마무리 다리 양호, D-WEFF 한 곳 끊김 |
| G-usable(사용성) | 5 | 3표+6단계 keybox+노드맵, 재현 실증 |
| 완결성(orphan) | 4 | 그림 \ref 정합, 단 bib 3건 본문 미참조 |
| 그림(6개) | 4 | 신규 5+개선, ASCII-English·혼란 없음; 중복 의심 무 |
| **합** | **30 / 35** | |

## 5. 부호 8항 (v11 1:1)

| # | 항 | v8-09 | v11 코드 | 정합 |
|---|---|---|---|---|
| 1 | $U_j=(-\Delta H+T\Delta S)/F$, $\Delta G=-FU$ | eq:Uj(행344)·S1 | func_U_j L69 | O |
| 2 | $\xi_\eq=$logistic$[\sigma_d(V-U)/w]$ 방전 V↑→ξ↑ | eq:xieq(행584)·S2 | func_ksi_eq L86 | O |
| 3 | $d\xi/dV$ peak 양수·방향불변 | eq:eqpeak(행664)·S3 | L468/L370 | O |
| 4 | $\Delta U_\hys\ge0$/$\Omega\le2RT\to0$/분기 $\pm\tfrac12\sigma_d$ | eq:dUhys(행439)·S4 | func_dU_hys L123, U_branch L138 | O |
| 5 | $\chi_d$ 충전 $1-\chi$·$\Delta H_a^\eff=\Delta H_a-\chi_d\Omega$ | eq:chid(행757)·eq:dHeff(행783)·S5 | func_chi_d L160, func_dH_a_eff L152 | O |
| 6 | $\partial\ln L_q/\partial V$ 컷상수 운영0(부등식=동기) | 행827–832·S6·R4 | A=min(...) L335 동결 | O |
| 7 | 꼬리 충전 격자역전·충전 dQ/dV 방전 거울(양수) | eq:reversal(행935)·S7 | L477 [::-1]…[::-1] | O |
| 8 | $V_n=V_\app-\sigma_d|I|R_n$ 방전 측정>평형 | eq:vn(행264)·S8 | L412 | O |

부호 8/8 정합. (단 8항 *부호*는 무결, 결함은 G-derive 영역의 D-PEAK·D-WEFF.)

---
**총평**: 30/35. 배치보존·부호·사용성 만점, 유도해소 3건 우수하나 ★D-PEAK 미수정(CRITICAL)·D-WEFF 점프가 G-derive 감점. 체리픽 채택 시 C1·C2 반드시 보정 필요.
