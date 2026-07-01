# v1.0.10 인계 무결성 대검수 — S2 (KNOWN_DEFECTS 정정 보존)

> 역할: 검수자 S2. 초점 = v8 KNOWN_DEFECTS(D-PEAK·D-PEAK2·D-VEQ·D-DHEFF·D-WEFF·D-UBR)가 v8-11→v9→v10→v1.0.10 에 정정된 형태로 인계·보존됐는가. 검수 의견만 — 코드/문건 수정 0.
> 정독: `results/builds/v8/v8-00_spine/KNOWN_DEFECTS.md`(SPEC) · `old/Ch1_v8/v8-11.tex`(체리픽 반영본) · `old/Ch1_v9/graphite_ica_ch1_v9.tex` · `old/Ch1_v10/graphite_ica_ch1_v10.tex` · `docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex`(현행) · `docs/v1.0.10/Anode_Fit_v1.0.10.py`(코드) · `results/builds/v9/v9-00_spine/FIX_LIST_v911.md` · `results/builds/ch1v10/v10-00_spine/FIX_LIST_v1011.md` · `results/builds/ch1v10/review1/R2_weff_preservation.md` · `results/builds/ch1v10/v10-00_spine/review2/A2_adv_weff_preserve.md` · `docs/v1.0.10/V1010_PROBLEM_REPORT.md` · `docs/v1.0.10/HANDOVER_v1.0.11.md`. 계획서 `Claude/plans/2026-07-06-v1010-handover-integrity-inspection-plan.md` 전문 정독.

## 방법
D-PEAK/D-PEAK2/D-VEQ/D-DHEFF/D-WEFF/D-UBR 각각에 대해 (1) KNOWN_DEFECTS.md 의 정확한 처방 재확인 (2) v8-11(체리픽 반영본)에 처방이 실제 반영됐는지 확인 (3) v9→v10→v1.0.10 각 단계에서 라인-레벨 diff(PowerShell `Compare-Object`) + grep 교차확인으로 byte 보존 여부 실측. 추가로 코드(`Anode_Fit_v1.0.10.py`)와 tex 서술의 정합성, 그리고 기존 adversarial review 문건(R2/A2)의 독립 확인 결과와 교차대조.

---

## 항목별 판정

### [무결] D-PEAK (eq:peakshape, "종 환원" 오류 → 정정)
- **위치(SPEC)**: `results/builds/v8/v8-00_spine/KNOWN_DEFECTS.md` L5-10.
- **위치(현행)**: `docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex` L1553-1593(§peak 모양, eq:peakshape·eq:branch).
- **확인**: v8-11.tex L922-962 의 정정 문단("이 매끈한 차분이 미분 dξ_eq/dV 로 수렴하는 극한은 오히려 L_V≫Δ_grid … 반대로 L_V 가 작아지는 평형 회복은 이 매끈한 차분의 극한이 아니라 코드의 분기 스위치가 담당")이 v1.0.10 L1557-1593 에 **완전 동일**하게 존재. PowerShell `Compare-Object` 로 v9/v10/v1.0.10 세 버전의 해당 블록(`\subsection{peak 모양` ~ `sub-grid 지연의 수치 불안정을 피하기` 구간)을 라인 단위 비교 = **0 diff 전 구간**(v8-11==v9, v9==v10, v10==v1.0.10 모두 정확 일치, 문자열 `-eq` 비교도 True). "L_V 작으면 종으로 환원"이라는 v7-11 원 오류 문장은 v1.0.10 어디에도 없음(grep 0건) — 오히려 L1906 에 "``L_V 작으면 식이 종으로 환원''이라는 서술은 거짓(반증 가능 회귀…)"으로 **반증 문구로 명문화**돼 있음.
- **코드 정합**: `Anode_Fit_v1.0.10.py` L481-499 의 `if lag_len_V < min_lag_grid_steps*grid_step: peak_shape = ksi_eq*(1-ksi_eq)/w; else: peak_shape=(ksi_eq-occ_lagged)/lag_len_V` 가 tex eq:branch 서술과 정확히 대응(이산 스위치, 매끈한 극한 아님).
- **판정**: 정정 완전 보존. v9→v10→v1.0.10 3단계 전부 무손상.
- **렌즈**: G-derive(수학적 정확성 회복) + 이력 대조(v8-11 체리픽 기준과 byte 일치).

### [무결] D-PEAK2 (eq:branch 문턱 ν=2 진폭 불연속 정직 기술)
- **위치(SPEC)**: KNOWN_DEFECTS.md L24-30.
- **위치(현행)**: v1.0.10.tex L1589-1593.
- **확인**: 처방 3요소 — (a) "이산 모드 스위치"(매끈한 handoff 아님) (b) "문턱에서 작은 불연속 가능"의 정직 기술 (c) "eq-분기가 인수"(꼬리식 자체 극한 아님) — 전부 v1.0.10 L1589-1593 에 원문 그대로("이 전환은 매끈한 handoff 가 아니라 이산 모드 스위치임에 주의한다 — 문턱 L_V=νΔ_grid 에서 꼬리 분기의 진폭과 평형 종의 진폭(∝1/w)이 정확히 같게 맞춰져 있지 않아 작은 불연속이 생길 수 있다"). "매끈한 handoff"로 호도하는 표현은 문서 전체에 0건(해당 위치 1건만 존재하며 그마저 "아니라"로 부정).
- **회귀 self-test 보존**: v1.0.10.tex L1901-1906 의 "R8: 꼬리 극한의 방향(D-PEAK 회귀)" — KNOWN_DEFECTS 의 D-PEAK 항목을 **명시적으로 "회귀 가드"로 라벨링**한 falsifiable 수치 self-test 가 그대로 존재("반증 가능 회귀: 두 극한의 ρ 부호를 뒤집으면 깨짐"). 이는 v1.0.10 작성자가 D-PEAK 정정을 능동적으로 인지·보호하고 있다는 강한 정황증거.
- **판정**: 정정 완전 보존 + 능동적 회귀 가드까지 유지.
- **렌즈**: G-derive + G-follow(정직한 불연속 기술이 독자 오해 방지) + 이력 대조.

### [무결] D-VEQ (eq:Veq → §5 forward-defer 순환 → inline 정당화)
- **위치(SPEC)**: KNOWN_DEFECTS.md L13.
- **위치(현행)**: v1.0.10.tex L584-638(§gap 의 닫힌 꼴 ~ §방향별 분기 중심).
- **확인**: v8-11.tex L461-462 에 평형조건 `μ=μ^0-sF(V-U)` 로부터 `g_j'(ξ)=sF(V_eq-U_j)` 를 **그 자리에서 inline 유도**(처방 "inline 1줄" 반영, §5 forward-defer 제거). PowerShell 라인 비교(`\subsection{gap 의 닫힌 꼴` 시작 58줄 블록) = v8-11/v9/v10/v1.0.10 전부 **diff 0**.
- **판정**: 정정 완전 보존, 4단계 무손상.
- **렌즈**: G-derive(순환 논리 제거) + 이력 대조.

### [무결] D-DHEFF (eq:dHeff, χ_d·Ω 흡수 중간식 추가)
- **위치(SPEC)**: KNOWN_DEFECTS.md L14.
- **위치(현행)**: v1.0.10.tex L1450-1456.
- **확인**: v8-11.tex L820-822 에 처방된 중간식 "꼬리 구동력 A_j=sF(V-U_j)-Ω_j(1-2ξ_j)에서 상호작용 몫 -Ω(1-2ξ)가 깊은 꼬리에서 상수 +Ω로 가고, 이것이 활성화 엔탈피에 흡수되어 유효값이 된다"가 정확히 존재(처방된 `r^+=k_0e^{-(ΔH_a-TΔS_a-χ_d A)/RT}` 형태의 물리적 정당화 문단). PowerShell 라인 비교(`textbf{(d) 유효 장벽` 기준 12줄 블록) = v8-11/v9/v10/v1.0.10 **diff 0**.
- **판정**: 정정 완전 보존.
- **렌즈**: G-derive(누락 중간식 복원) + 이력 대조.

### [무결, 단 관련 구조 변경 병존] D-WEFF (eq:weff, 4RT↔4Fw^eff 다리 중간식)
- **위치(SPEC)**: KNOWN_DEFECTS.md L15.
- **위치(v8-11/v9)**: v8-11.tex L576-580, v9.tex L~671-695.
- **확인 (파생 유도 품질 관점)**: v8-11.tex L576-577 에 처방된 중간식이 정확히 존재 — "비단조 등온선의 중심 기울기를 이상 logistic 의 중심 기울기와 같다고 둔 데서 온다 — sF dV_eq/dξ|_{1/2}=4RT-2Ω_j 와 4Fw^eff_j 를 같다고 풀면(s 부호는 양변 공통이라 상쇄)". D-WEFF 처방("이상 4RT↔일반 4Fw^eff 다리")이 정확히 이 문장. v9 까지 이 형태로 보존 확인(grep L577 대응 라인 존재).
- **★구조적 후속 변경(별개 사안, SPEC 문건상 정당)**: v9→v10 전환에서 **eq:weff·func_w_eff·use_w_eff·w_eff_floor_frac 전체가 삭제**됨(v10.tex 헤더 L11: "w_eff 제거(eq:weff·func_w_eff·use_w_eff·w_eff_floor_frac 자취 0)"). 이는 `results/builds/ch1v10/v10-00_spine/FIX_LIST_v1011.md` A2 "w_eff 잔존 0"·`review1/R2_weff_preservation.md`·`review2/A2_adv_weff_preserve.md` 세 독립 adversarial 문건이 **의도된 삭제로 3중 확인**한 사항(v10-06 이 "w_eff 완전제거 + 보존 PASS"로 최종 체리픽 채택). SPEC(base 프롬프트 L9: "w_eff 완전제거")과 정확히 일치 — **결함 아님, 의도된 설계 변경**.
- **판정 구분**: D-WEFF 의 *원 결함*(유도 중간식 누락)은 v8-11 에서 이미 정정됐고 그 정정판이 v9 까지 온전 보존. 이후 v9→v10 에서 w_eff **자체가 통째로 제거**되어 이 유도 문단도 함께 사라졌으나, 이는 KNOWN_DEFECTS 재발이 아니라 SPEC 이 명시한 후속 리팩터(narrowing 폐기·apparent-U 재정초)의 자연스러운 결과. v1.0.10 에서 D-WEFF 관련 잔존물 = 0(정상, 설계대로).
- **렌즈**: G-derive(원 결함은 정정됨) + 이력 대조(구조 변경은 SPEC 인가 사항, 훼손 아님).

### [무결, 처방 대비 완화형이나 취지 충족] D-UBR (eq:Ubranch, ansatz 정직 라벨링)
- **위치(SPEC)**: KNOWN_DEFECTS.md L16 — "eq:Ubranch 는 ansatz(γ·h_η 도입이 유도 아님) → spinodal 한계 ±½ΔU_hys 위 현상학적 매개변수화로 명시(유도 가장)하거나 γ 보간 인자 명시."
- **위치(현행)**: v1.0.10.tex L625-638.
- **확인**: v8-11.tex L501-517(=v1.0.10.tex L625-643, PowerShell 라인 비교 4버전 diff 0)에서 γ_j 는 "분기 축소 인자"(표기 notation, KNOWN_DEFECTS.md 처방과 정확히 일치하는 "γ 보간 인자 명시" 옵션 채택)로 명시되고, 본문은 "이 대칭 위에서 실측 분기 중심을 방향별 한 자유도로 적으면(축소 인자 γ_j 와 부분 cycle 인자 h_{η,j} 를 곱해)"라고 **γ·h_η 를 유도된 필연식이 아니라 "실측 분기 중심을 표현하는 자유도"로 명시적으로 낮춰 기술**. `ansatz`/`현상학적 매개변수화`라는 verbatim 단어 자체는 v8-11에도 없음(grep 0건) — 처방의 두 옵션 중 "γ 보간 인자 명시" 쪽으로 이행된 것으로 판단.
- **판정**: 처방 정신(유도 가장 금지·γ 를 자유도/보간 인자로 정직 표기)은 충족. verbatim "ansatz" 단어 부재는 v8-11 자체의 선택이며 v1.0.10 에서 추가로 훼손된 바 없음(4버전 byte 동일) — **인계 무결**(원 처방 대비 표현 강도는 약하나 이는 v8-11 저작 시점의 결정이지 v9→v10→v1.0.10 인계 과정의 손실이 아님).
- **렌즈**: G-follow(독자가 γ 를 유도값으로 오인할 위험 감소) + 이력 대조.

---

## 앞선 10차 문제검수와의 교차검증 (오적발 여부 재검)

`docs/v1.0.10/V1010_PROBLEM_REPORT.md`·`HANDOVER_v1.0.11.md` 정독 결과, 10차 재검이 실제로 기각한 오적발 목록은 **"논리 점핑 6건(C1·C2·C3·C5·S3-02·S3-07)·면적 3건(G1)·E2·E3·z_cut(S3-08)"** 이며, 이 중 **D-PEAK/D-PEAK2 를 지칭하는 항목은 없음**. 유일한 CRIT 로 확정된 R1("폭 모델 구조 결함 — 두-상 near-delta 생성 불가·4 staging 병합")은 **별개 사안**(w=nRT/F 보편 적용이 두-상 전이에 sub-thermal 폭을 요구하는 문제)으로, peak_shape 유도의 수학적 오류(D-PEAK)나 branch 문턱 불연속(D-PEAK2)과는 무관하다. 즉 **base 프롬프트가 우려한 "앞선 10차가 D-PEAK류를 오적발로 기각"한 사실은 문서상 확인되지 않음** — 10차는 애초에 D-PEAK/D-PEAK2 를 결함 후보로 다루지 않았고(이미 정정 완료 상태로 간주해 대상에서 제외), 대신 R1(폭 구조)이라는 별개의 새 CRIT 를 확정했다. 따라서 "오적발 기각" 프레이밍 자체가 부정확 — **재검 결과 = 기각된 적이 없으며, 정정 상태는 실측으로도 그대로 보존 확인됨**.

---

## 무결 영역 정독 근거 (추가)
- `results/builds/v9/v9-00_spine/FIX_LIST_v911.md` L12: "흑연 byte-동일(diff 제거 0)" — v8-11→v9 전환에서 흑연 섹션(D-PEAK 포함 영역) 전체가 무손상임을 별도 fix-list 가 자체 확인.
- `results/builds/ch1v10/v10-00_spine/review2/A2_adv_weff_preserve.md` L36: "N7·N8·N9(lag/tail/sum) byte-identical(offset +157 후 diff 0)" — N8 이 정확히 peak_shape/eq:reversal 을 다루는 node(§sec:tail, D-PEAK/D-PEAK2 소재)이며, v9→v10-10 adversarial review 가 독립적으로 동일 결론(무손상) 도달.
- 코드 `docs/v1.0.10/Anode_Fit_v1.0.10.py` L466-499: branch-switch 로직이 KNOWN_DEFECTS.md 가 지목한 "코드 L466–479"(v8-11 기준 줄번호 대응)와 동일 구조로 존재 — 문서 서술과 코드 구현의 정합성도 확인.

---

## 가장 약한 1곳
**D-UBR** — KNOWN_DEFECTS.md 가 제시한 두 처방("현상학적 매개변수화 명시" 또는 "γ 보간 인자 명시") 중 verbatim "ansatz"/"현상학적"이라는 명시적 단어 없이 완화된 형태("분기 축소 인자"·"실측 분기 중심을 … 한 자유도로 적으면")로만 이행됐다. 물리적으로는 처방 취지(유도 가장 금지)를 충족하나, 향후 검수자가 이 절을 KNOWN_DEFECTS 원문과 글자 그대로 대조하면 "완전 이행"이라 단정하기보다 "완화 이행"으로 기록해두는 편이 v1.0.11 인계에 더 정직하다. 결함이라기보다 **표현 강도의 미세 gap** — CRIT/HIGH 아님, NOTE 급.

## 버전전환별 인계 판정
| 전환 | D-PEAK | D-PEAK2 | D-VEQ | D-DHEFF | D-WEFF(유도) | D-UBR |
|---|---|---|---|---|---|---|
| v7-11→v8-11(체리픽) | 정정 도입 | 정정 도입 | 정정 도입 | 정정 도입 | 정정 도입 | 완화 정정 도입 |
| v8-11→v9 | 보존 | 보존 | 보존 | 보존 | 보존 | 보존 |
| v9→v10 | 보존 | 보존 | 보존 | 보존 | (w_eff 자체 삭제, SPEC 인가) | 보존 |
| v10→v1.0.10 | 보존 | 보존 | 보존 | 보존 | 해당없음(이미 부재) | 보존 |

## 5줄 요약
- **초점**: v8 KNOWN_DEFECTS(D-PEAK·D-PEAK2·D-VEQ·D-DHEFF·D-WEFF·D-UBR) 6종의 v9→v10→v1.0.10 인계 보존 여부.
- **인계 결함 수**: 0건(CRIT/HIGH/MED 전부 무결). D-UBR 1건만 NOTE 급 표현 완화(결함 아님).
- **최중대 발견**: peak_shape/eq:branch 절(D-PEAK/D-PEAK2 소재) 전체가 v8-11→v9→v10→v1.0.10 **4버전 라인단위 diff 0** — 가장 취약할 수 있었던 영역이 오히려 가장 견고. R8 "D-PEAK 회귀" self-test 까지 명문 보존.
- **두 축 유지 판정**: G-derive(유도 완결성)·G-follow(교과서 follow-ability) 둘 다 이 6종에 한해 v1.0.10 까지 저하 없음. w_eff 삭제는 두 축 저하가 아니라 SPEC 이 지시한 정당한 구조 변경.
- **오적발 자기표시**: base 프롬프트가 전제한 "10차가 D-PEAK류를 오적발로 기각"은 문서 근거로 확인 안 됨 — 10차의 오적발 목록(논리점핑 6·면적 3·E2·E3·z_cut)과 유일 CRIT(R1 폭구조)는 D-PEAK 계열과 무관한 별개 사안이었음. 이 재프레이밍 자체가 이번 S2 검수의 핵심 정정.
