# F1_NOTE — R7-F1 그림 초안 산출 로그 · 설계 근거

- **대상 그림**: 블렌드 `f_Si`(wt% 스윕) 가족 dQ/dV 곡선 (2패널)
- **산출물**: `results/comp_R7/F1_blend_family.tex` (그림 블록 초안)
- **라벨 제안**: `fig:blend-family` / **자산 앵커 제안**: `[V22-R7-F1]`
- **규율 준수**: 초안 전용 — `_sections/` 미수정 · git 미사용 · `Codex/` 미접근. 본 NOTE·tex 는 `results/comp_R7/` 에만 생성.
- **날짜**: 2026-07-18 (v1.0.22 R7)

---

## 1. 실행 커맨드 (좌표 실계산)

좌표는 손계산이 아니라 **문서 코드 `Anode_Fit_v1.0.22.py` 를 실제 import·실행**해 뽑았다. 모듈 파일명에 점(`.`)이 있어 `importlib` 로 로드한다.

```python
import importlib.util, numpy as np
PYPATH = "/home/user/Project_Anode_Fit/Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py"
spec = importlib.util.spec_from_file_location("anodefit", PYPATH)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
B = m.BlendedAnodeDQDV

T = 298.15
for wt in [0.0, 0.10, 0.20, 0.30]:
    b = B.from_wt(wt, si_case='elemental')       # Cbg 기본 0.0
    y_total = np.asarray(b.equilibrium(Vgrid, T)) / b.Q      # 패널 (a): 총 dQ/dV / Q
    _, si   = b.host_contributions(Vgrid, T)
    y_si    = np.asarray(si) / b.Q                            # 패널 (b): Si host 몫 / Q
```

- 사용 진입점: `BlendedAnodeDQDV.from_wt(m_Si, si_case='elemental')` → 생성자 기본 `Cbg=0.0`.
- 평가식: `equilibrium(V, 298.15)` = eq:blend-dqdv 의 `|I|→0` 평형 종 `Σ_host Σ_j Q_j^host ξ_eq,j^host (1−ξ_eq,j^host)/w_j^host` (배경 `C_bg=0`).
- 케이스 `elemental` → 전이 셋 `SI_ELEMENTAL_LIT = [{U:0.300, w:0.060, Q:0.60}, {U:0.450, w:0.050, Q:0.40}]`, 비용량 `q_Si=1000 mAh/g`.
- 흑연 host = `GRAPHITE_STAGING_LIT` (staging 4전이 `U=0.210/0.140/0.120/0.085`, `n=1` → 폭 `w=RT/F≈25.7 mV`).
- 스크립트 원본: `scratchpad/extract_F1.py` (좌표 덤프), `scratchpad/verify2.py` (교차검증). 그림 컴파일 검증: `scratchpad/test_compile.tex` (xelatex 2패스, `common_preamble_v1022` 사용, 2페이지 정상 출력, Overfull 0).

---

## 2. wt% ↔ f_Si 환산 (C-052) — 코드 vs 손계산 대조

환산식 `f_Si = m·q_Si / [m·q_Si + (1−m)·q_gr]`, `q_Si=1000` (elemental, tier-A limthongkul2003), `q_gr=372`.

| m_Si (wt%) | f_Si (코드) | f_Si (손계산) | Q_gr | Q_Si | Q=Q_gr+Q_Si |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0  | 0.000000 | 0.000000 | 0.9700 | 0.0000 | 0.9700 |
| 10 | 0.229991 | 0.229991 | 0.9700 | 0.2897 | 1.2597 |
| 20 | 0.401929 | 0.401929 | 0.9700 | 0.6519 | 1.6219 |
| 30 | 0.535332 | 0.535332 | 0.9700 | 1.1175 | 2.0875 |

- **일치**: 코드 = 손계산 (부동소수점까지). §3.3 각주의 "0–30 wt% ≈ f_Si 0–0.7" 범위 진술과 정합 (elemental 에서 30 wt% → 0.535).
- **주의(코드 규약)**: 흑연 절대 용량 `Q_gr=0.97`(= staging Q 합 0.10+0.12+0.25+0.50)은 **f_Si 무관 불변**, Si 는 `Q_Si=[f_Si/(1−f_Si)]·Q_gr` 로 절대 스케일. 총 `Q=Q_gr/(1−f_Si)`.

---

## 3. 좌표 검증 (피크 위치·높이 수기 대조)

### 3-A. 알려진 값과의 교차검증 (독립 대조점)

| 검증 항목 | 코드 출력 | 기대값(출처) | 판정 |
|:---|:---:|:---:|:---:|
| f_Si=0 총 raw dQ/dV @ V=0.085 | **6.9023** | 6.902 (fig:sumcurve §sum-worked 끝-대-끝 예제) | ✅ 일치 |
| 흑연 2→1 단독 전이 raw 피크 | **4.8655** | Q/(4w)=0.50/(4·0.025691)=4.8655 | ✅ 일치 |
| f_Si=0 블렌드 vs 흑연 단독 equilibrium | max\|diff\|=**0.0** | bit-exact (eq:blend-limit / eq:si-code-bitexact) | ✅ 일치 |
| (dQ/dV)/Q 면적 ∫dV (전 V역) | **1.00000** (네 곡선 전부) | 규약상 →1 (Q/Q) | ✅ 일치 |
| host 면적 분해: gr / si | 1−f_Si / f_Si (정확) | 정의상 | ✅ 일치 |

### 3-B. 그림에 실린 피크 (정규화 (dQ/dV)/Q [1/V])

**패널 (a) 흑연 겹침 envelope 피크** (V≈0.10, staging 4전이가 298 K 에서 겹쳐 단일 envelope 이 됨 — fig:sumcurve 와 동일 거동. "흑연 2→1 단독"의 4.865 는 개별 전이값이고, 관측 곡선은 겹침 envelope 이라 더 높다):

| m_Si | envelope 피크 V | 높이 [1/V] | = 7.526 × (1−f_Si)? |
|:---:|:---:|:---:|:---:|
| 0  | 0.100 | 7.526 | 7.526×1.000=7.526 ✅ |
| 10 | 0.101 | 5.874 | 7.526×0.770=5.795 (≈; envelope 는 Si 꼬리 미소 가산) |
| 20 | 0.101 | 4.639 | 7.526×0.598=4.501 (≈) |
| 30 | 0.102 | 3.682 | 7.526×0.465=3.499 (≈) |

→ **흑연 축소가 대체로 (1−f_Si) 스케일**(총용량 정규화의 직접 귀결). envelope 은 Si 저전위 꼬리를 조금 얹어 순수 (1−f_Si) 보다 약간 높다 — 물리적으로 옳음(겹침).

**패널 (b) Si host 기여 피크** (V≈0.335, Si 두 전이 0.30·0.45 겹침 envelope):

| m_Si | Si envelope 피크 V | 높이 [1/V] |
|:---:|:---:|:---:|
| 10 | 0.339 | 0.681 |
| 20 | 0.339 | 1.190 |
| 30 | 0.339 | 1.585 |

- 개별 Si 전이 해석 피크 `Q_j/(4w_j)`(raw)와도 대조 완료: 예 m_Si=30% 전이1 `Q=0.6705, w=0.060 → 2.794 raw → /Q=1.338`; envelope(1.585)은 전이1·2 겹침이라 단독보다 높음 — 정합.
- **성장 = f_Si 정비례** (Si host 몫 면적 = f_Si): 0.681/1.190/1.585 는 대략 0.230/0.402/0.535 비율을 따름(피크는 겹침으로 약간 편차).

### 3-C. 정성 서명 (그림이 보여야 하는 것)
- (a) f_Si=0 실선이 **최상단 기준선**, wt% 증가로 흑연 envelope **축소**, Si 기여 **성장**, `V_n≈0.26 V` 부근 **순서 역전**(crossover). ✅ 렌더 확인.
- (b) Si 몫이 0(0 wt%, 부재)→1.585 로 단조 성장. ✅ 렌더 확인.

---

## 4. 그림 설계 근거

1. **스타일**: `_sections/ch2_sec04_einstein.tex` `fig:svibid`(2패널) · `ch1_sec10_sum.tex` `fig:sumcurve`(dQ/dV) 의 시각 언어 준수 — **순수 tikz**(pgfplots 아님; `common_preamble` 는 tikz+arrows.meta 만 로드, 관행 확인), 흑백, `\scriptsize`(축)·`\tiny`(범례·주석), `\draw ... plot[smooth] coordinates {...}` 인라인 좌표, 수동 범례, 캡션에 "좌표=식 그대로 수치 평가" 명시.
2. **흑백 구분**: 4곡선을 색이 아니라 **선종+명도**로 — 0 wt%=very thick 실선 / 10=thick densely dashed / 20=densely dashdotted (black!75) / 30=densely dotted (black!58). (fig:sumcurve 의 실선·파선·점선 관행과 정합.)
3. **정규화 선택 (핵심 설계 결정)**: y = **(dQ/dV)/Q**, Q=총용량, **곡선 아래 면적=1**. 근거 = 과제 요구 "흑연 peak 축소·Si 기여 성장 한눈에". 코드 규약상 흑연 절대 Q 는 불변(§2 주의)이라 **raw 로는 흑연 peak 이 안 줄어든다**. 총용량 정규화해야 흑연 몫이 (1−f_Si) 로 줄고 Si 몫이 f_Si 로 커지는 **가족 재분배**가 드러난다(면적=1 검증으로 규약 확정, §3-A). 이 변환은 실계산 좌표에 대한 **명시적·검증된 정규화**이지 수치 창작이 아니다.
4. **2패널 정당화**: 정규화 후 흑연 envelope(피크 7.5)이 Si 기여(넓고 낮음)를 y축에서 압도 → (a) 전체 창(가족 전모+crossover) + (b) Si host 몫만 확대(코드 `host_contributions` 의 Si 반환, = eq:blend-dqdv 의 Si 이중합). fig:svibid 가 2패널로 서로 다른 두 양을 보인 것과 동형.
5. **캡션 정직 규율**: (i) 좌표=`BlendedAnodeDQDV.from_wt`·`equilibrium`(eq:blend-dqdv, `|I|→0`)·elemental·298.15 K·C_bg=0 실계산 명시. (ii) 정규화 규약(면적=1) 명시. (iii) wt%↔f_Si 환산·q_Si 병기. (iv) **tier 명시**: 전이 중심·폭 = tier-C 시연값(원소 Si 0.2–0.5 V 범위 obrovac_chevrier2014 tier-B 안), q_Si=1000 = tier-A. (v) `elemental` 케이스는 "확인 필요" 공백 0건(SiOx 절대전위 공백 미사용).

---

## 5. 정직 규율 체크 (과제 4항)

- ✅ **SiOx 공백 미사용**: `si_case='elemental'` 만 사용. `SI_CASE_GAPS['elemental']=[]` (공백 0). SiOx 절대 평균전위·히스 절대 mV 같은 "확인 필요" 값은 그림에 일절 등장 안 함.
- ✅ **수치 창작 없음**: 모든 좌표는 코드 실행 출력. 정규화(÷Q)만 적용(면적=1 로 독립 검증). 손으로 지어낸 점 없음.
- ✅ **시연값 tier 캡션 명시**: 전이 개형 tier-C, q_Si tier-A 를 캡션+본 NOTE 에 기록.
- ✅ **bit-exact / 알려진값 교차검증**: §3-A 5건 전부 통과(특히 f_Si=0 bit-exact, worked-example 6.902, 단독전이 4.8655).

---

## 6. 삽입 위치 제안

**1순위 — §3.3 `eq:blend-dqdv` 부근** (`ch3v22_sec03_blend.tex`, `\begin{keybox}` 공통-μ 앵커 직후):
- 근거: 그림이 바로 그 식(eq:blend-dqdv)의 `|I|→0` 평형 종을 wt% 스윕으로 실체화. keybox 가 "관측 dQ/dV = 두 host 기여의 배경 위 선형 합"을 선언한 직후 그 선형 합의 가족 곡선을 보여주면 서술→그림 흐름이 자연스럽다. §3.3 이 이미 언급한 "저-Si 블렌드에서 Si·흑연 피크 부분 분리"(naboka_sic2021)의 시각 대응이 패널 (b).
- 유의: 그림은 **평형 층**(GS-2 이전)의 곡선이다. `ssec:si-blend-gs2` 의 warnbox(1차 근사·비가산 경고)보다 **앞**에 두어 "평형 골격의 곡선"으로 읽히게 하는 편이 안전(warnbox 뒤에 두면 "율속 실측"으로 오인 위험). → keybox 직후, `\subsection{정직 공백 GS-2 ...}` 앞이 최적.

**2순위 — §3.5 코드 절** (`ch3v22_sec05_code.tex`):
- 근거: 그림이 코드 산출물(`from_wt`·`equilibrium`·`host_contributions`)의 직접 시연이라 코드 절 예시로도 적합. `f_Si=0 bit-exact` 게이트의 시각 증거로 쓸 수 있음.
- 단점: §3.3 중심식과 그림 사이 거리가 멀어져 "식→곡선" 즉시성이 약함.

**권고**: 1순위(§3.3 keybox 직후). 캡션의 `\ref{fig:sumcurve}`·`\eqref{eq:blend-limit}` 참조가 이미 §3.3 문맥과 연결됨.

---

## 7. 추가 후보 (실제 수정 안 함 — 보고만)

- **온도 가족**: 현재 298.15 K 단일. fig:sumcurve 처럼 268/328 K 를 겹쳐 "Si 대 흑연 엔트로피 서명 차"(§3.2 ssec:si-thermal, Si `∂U/∂T` 평탄 vs 흑연 peak)를 한 장 더로 보일 수 있음 — 별도 그림(F2 후보).
- **raw(비정규화) 보조 패널**: "흑연 절대 불변, Si 절대 성장"의 코드 규약을 그대로 보이는 raw 곡선을 부록/각주 그림으로. 단 과제 요구("흑연 축소")는 정규화판이 충족하므로 본 그림은 정규화 유지.
- **piecewise host 전환 표식**: GS-2(비가산·구간별 우세 host 전환)를 점선 화살표로 표기 — 단 이는 평형 곡선이 아니므로 warnbox 소관, 본 평형 그림에는 미포함(정직 경계 유지).
- **Si_case 비교**: elemental vs sic(q_Si=3117) 의 f_Si 위치 차. 단 sic 도입 시 케이스 혼선 위험 — 본 그림은 elemental 단일로 한정(과제 지시).
```
