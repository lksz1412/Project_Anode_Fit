# R7-F2 검증 노트 — Si 케이스 3계열 dQ/dV 개형 비교 그림 초안

- 산출: `results/comp_R7/F2_si_cases.tex` (라벨 제안 `fig:si-cases-shape`, 자산 앵커 `[V22-R7-F2]`)
- 규율: 초안 전용(`_sections/` 미수정)·git 미실행·`Codex/` 미접촉. 수치 창작 금지·"확인 필요" 값 사용 금지.
- 스타일 준거: `fig:svibid`(`_sections/ch2_sec04_einstein.tex`)·`fig:staging`(`_sections/ch1_sec01_n0n1.tex`)
  및 동일 R7 가족 `results/comp_R7/F1_blend_family.tex` — 흑백(선종+명도)·`\scriptsize`/`\tiny`·실계산 좌표 관행.

---

## 1. 실행 커맨드 (좌표 재현)

모듈명에 점(`.`)이 있어 `import` 대신 `importlib` 경로 로드. 작업 디렉토리 = `docs/v1.0.22/`.

```python
import importlib.util, warnings, numpy as np
spec = importlib.util.spec_from_file_location("anodefit", "Anode_Fit_v1.0.22.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

f_Si, T = 0.5, 298.15
V = np.linspace(0.08, 0.66, 1161)          # 0.0005 V 격자
for case in ("elemental", "siox", "sic"):
    with warnings.catch_warnings(record=True) as wl:
        warnings.simplefilter("always")
        model = m.BlendedAnodeDQDV(f_Si, si_case=case, Cbg=0.05)
        gr, si = model.host_contributions(V, T)   # si = Si-host 기여(배경 제외 평형 종)
    imax = int(np.argmax(si))
    print(case, "Q_Si=%.4f" % model.Q_Si, "peak V*=%.4f h=%.4f" % (V[imax], si[imax]),
          "warn=%d" % len(wl))
```

- 전체 계산 스크립트 사본: (세션 스크래치패드) `compute_F2.py` — 케이스 셋·wt% 환산·성분 전이·좌표 샘플·우세영역 표를 모두 출력.
- 그림 곡선 좌표 = 위 `si` 배열을 `V ∈ [0.12/0.135/0.150, 0.585/0.600/0.570]` 구간에서 `step 0.015 V`로 표본(케이스별 29–32점, `plot[smooth]`).

### 케이스 셋(코드 `SI_CASE_SETS`, tier-C 시연 = §3.2 `tab:si-cases`)
| case | 전이 (U[V], w[V], Q_raw) | q_Si[mAh/g] (tier-A) | 공백(`SI_CASE_GAPS`) |
|---|---|---|---|
| elemental | (0.30, 0.060, 0.60), (0.45, 0.050, 0.40) | 1000 (limthongkul2003) | 없음 |
| siox | (0.30, 0.090, 1.00) | 1710 (zhang_sio2018) | **평균전위 U·히스 절대 mV (확인 필요)** |
| sic | (0.30, 0.050, 0.50), (0.42, 0.050, 0.50) | 3117 (andersen_sic2019) | 없음 |

`f_Si=0.5` 공통 → `si_scale = 0.97·f_Si/(1−f_Si) = 0.97` (세 케이스 `Q_si0=1.00` 동일) →
**세 케이스 총 Si 용량 `Q_Si = 0.97 Q_cell` 동일 = 면적 동일** → 순수 개형 비교.
케이스별 wt% 대응(같은 f_Si, 서로 다른 q_Si): elemental 27.1 · siox 17.9 · sic 10.7 wt% (모두 §3.3 0–30 wt% 스윕 밴드 내).

---

## 2. 좌표 수기 대조 (독립 로지스틱 재계산 vs 플롯값)

평형 종 `dQ/dV = Σ_j Q_j^Si·ξ(1−ξ)/w_j`, `ξ = 1/(1+e^{−(V−U)/w})` (방전 s=+1, `func_ksi_eq`).
독립 손계산이 플롯 좌표와 **소수 3자리까지 완전 일치**:

| 케이스 | 점 | 손계산 | 플롯값 | 비고 |
|---|---|---|---|---|
| sic | V=0.360 (peak) | 3.451 | 3.451 | 두 전이 0.30·0.42 중점 |
| sic | V=0.300 | 3.165 | 3.165 | |
| elemental | V=0.330 (peak) | 2.871 | 2.871 | 평탄역 정점 |
| elemental | V=0.495 | 1.943 | 1.943 | 깊은-탈리튬 어깨 |
| siox | V=0.300 (peak) | 2.694 | 2.694 | = Q/(4w)=0.97/0.36 |
| siox | V=0.180 | 1.779 | 1.779 | 넓은 저전위 꼬리 |

피크 요약: **sic 3.451 @0.360 (최고·최협) > elemental 2.871 @0.335 (평탄) > siox 2.694 @0.300 (최광·대칭)**.
동일 면적에서 폭이 좁을수록 피크가 높다(sic w=0.050×2, siox w=0.090). 우세(최대) 케이스 by 구간:
`V≤0.24 → siox`(최광), `0.28≤V≤0.40 → sic`(최고), `V≥0.46 → elemental`(둘째 전이 0.45 V 어깨) —
세 케이스가 각기 다른 전위 구간을 점유해 겹침에도 흑백에서 판독 가능.

---

## 3. SiOₓ "확인 필요" 공백 처리 — **방안 (b) 채택** (사유 기록)

과제 지시: siox 절대 전위·히스는 §3.2 각주 c·f "확인 필요" 공백(코드 경고). (a) siox 제외 2케이스 / (b) 상대
형상만 보이며 배너·캡션에 placeholder 명시 — **정직한 쪽 택일**.

**채택 = (b).** 사유:
1. 그림 목표가 "3계열 비교"라 siox 제외(a)는 목적 훼손. siox 의 **개형**(폭 0.090 V 단일 연속 hump, 이산
   상전이 없음)은 `kitada_sio2019`(tier-A) 의 정성 실측 서명이라 **실재 정보**다 — 숨기는 것이 오히려 비정직.
2. 공백인 것은 오직 **가로(절대 전위) 위치** 하나. 세 케이스 U 는 모두 tier-C 시연이지만, elemental/sic 은
   tier-A/B 전위 범위(0.2–0.5 V·~0.4 V)에 앵커됐고 siox 만 앵커 자체가 공백이다. 이 차이를 **표식으로 노출**.
3. 코드 계약과 정합: `BlendedAnodeDQDV(0.5, 'siox')` 는 placeholder 사용 시 경고를 발생(§4) — 그림도 같은 정직
   규율(placeholder 는 쓰되 명시).

**3중(+선종) 표식으로 오독 차단:**
- 배너(상단): "SiO$_x$: 절대 위치 = placeholder (확인 필요 — §3.2 각주 c·f); 개형(폭·대칭)만 유효".
- 범례: "SiO$_x$ (위치 placeholder)".
- 선종: **회색 점선**(`black!58, densely dotted`) — 두 실측 앵커 케이스(굵은 실선 sic·파선 elemental)와 대비되는
  "잠정" 시각 신호.
- 캡션 정직 표식 (i): 절대 전위·히스 공백·placeholder 경고·"개형만 유효" 명기.

→ siox 의 **세로 개형(폭·대칭)은 유효 비교**, **가로 위치는 무의미(placeholder)** 임이 명백. 수치 창작 없음.

---

## 4. siox placeholder 경고 로그 (실행 캡처)

`f_Si>0 & si_case='siox'` 생성 시 코드가 실제로 발생시킨 경고(원문):

```
UserWarning: [BlendedAnodeDQDV] si_case='siox' 은(는) 확인 필요 공백 보유:
  평균 전위 U_avg (절대 mV 미확보 — 표 각주 c); 히스테리시스 절대 mV (미확보 — 표 각주 f)
  — 시연 placeholder 사용 중(신뢰값 아님, 피팅 override 전제).
```

elemental·sic 은 경고 0건(공백 미사용). 그림은 이 경고의 내용을 배너·캡션으로 그대로 계승.

---

## 5. §3.2 서술과의 대응 및 **정직 표식(캡션 (i)–(iii))**

| §3.2 서술 | 그림 개형 | 정직 주석 |
|---|---|---|
| 원소 Si 두-상 평탄역(ssec:si-elemental) | elemental 파선 0.30–0.42 V 평정 + 어깨 | 정합 |
| SiOₓ 비정질 연속·이산 상전이 없음(ssec:si-siox) | siox 회색점선 단일 연속 hump(최광) | 정합(형상); 위치=placeholder |
| Si–C 평균 탈리튬 ~0.4 V(ssec:si-sic) | sic 실선 0.30·0.42 감싼 평정부 | 정합 |

**demo 와 §3.2 전 서술 간 간극(캡션에 명시):**
- (ii) 원소 Si 날카로운 **Li₁₅Si₄ 결정화(~50 mV)** 특징은 §3.2 서술엔 있으나 **리튬화 feature** 이고, demo
  전이 셋은 **탈리튬(방전) 경사 대표값**(코드 주석 명기)이라 그림에 없음 — 날카로운 피크를 만들지 **않음**(창작 X).
- (iii) §3.2 표제 "피크 분리"는 블렌드에서 **Si 대 흑연** 피크 분리(`eq:blend-dqdv`, Si 10 wt% `naboka_sic2021`)를
  뜻하지 Si-**내부** 두 피크가 아니며, sic demo 두 전이(w=0.050, 간격 0.120 V)는 이 폭에서 **겹쳐 평정부**(완전
  분리 아님). → 그림은 "분리 피크"가 아니라 "겹친 평정부"로 정직 표기.

이 세 간극을 캡션 "정직 표식 (i)–(iii)"으로 노출 — P3 검수 및 "확인 필요/창작 금지" 규율 준수.

---

## 6. 삽입 위치 제안

- **1순위: §3.2 `ssec:si-sic`(Si–C 소절) 직후, `ssec:si-thermal`(열특성) 앞.**
  세 케이스 개형 서술(elemental·siox·sic)이 막 끝난 자리라 3계열 비교 그림이 가장 자연스럽고, `tab:si-cases`·
  `ssec:si-elemental~sic` 참조가 근접. `\input{results/comp_R7/F2_si_cases}` 또는 블록 붙여넣기.
- **허용 대안: §3.2 말미(`srcbox` 데이터 등급 요약 뒤).** `[t]` 플로트라 배치는 페이지 상단으로 뜨므로 실질 동일.
  **§3.2 말미 권장 여부 → 가능하나 1순위(ssec:si-sic 직후)를 더 권장** (개형 3소절과 그림의 인접성 우선).
- 참고: 캡션이 `eq:blend-dqdv`(§3.3)·`naboka_sic2021`·`andersen_sic2019` 를 전방 참조 — 셋 다 동일 컴파일
  단위(`ch3_si_v1.0.22`)에 존재해 다중 패스에서 해소됨(전방 참조 정상).

---

## 7. 컴파일 확인

- 엔진: xelatex(kotex·D2Coding) — `common_preamble_v1022.tex` + 본 그림만으로 standalone 컴파일 **성공(1p)**.
- 잔여 경고는 전부 예상 범위: (a) standalone 미해소 상호참조(`eq:blend-dqdv`·`tab:si-cases`·`ssec:si-*`·인용
  키) → ch3 본문 삽입 시 해소, (b) 한글 italic 폰트 fallback(`\emph` 한글 — 기존 `fig:svibid` 캡션과 동일 관행).
- TikZ 라이브러리: `arrows.meta`(Latex 화살촉) — 프리앰블 기로드. 신규 패키지 요구 없음.

## 8. 미해결/추가 후보 (실제 수정 안 함 — 보고만)

- SiOₓ 절대 전위·히스 mV 확정 시 배너·placeholder 선종 제거하고 실측 위치로 이동 가능(현재는 공백 유지).
- 블렌드 전체 곡선(흑연 staging + Si) 위 Si-흑연 피크 분리를 보이려면 `equilibrium()` 전체(F1 계열)와 결합한
  별도 패널이 필요 — 본 그림은 케이스 간 Si 개형 비교에 집중(흑연은 세 케이스 공통이라 비교정보 없음)해 Si-host
  단독으로 한정. (추가 후보)
