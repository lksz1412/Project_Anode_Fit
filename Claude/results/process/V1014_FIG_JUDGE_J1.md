# V1.0.14 P5.1 이미지 경연 심사 보고 — J1 (Fable) / T1–T4 초벌 채점

- 심사일: 2026-07-04. 대상: T1 `fig:spine` · T2 `fig:staging` · T3 `fig:hysloop` · T4 `fig:barrier`, 각 9안 (sonnet1–3, opus1–3, codex1–3).
- 기준선: `Claude/docs/v1.0.14/graphite_ica_ch1_v1.0.14.tex` 의 현행 블록 (T1 L158–191, T2 L272–305, T3 L1147–1173, T4 L1255–1289) — 이보다 나아야 교체 가치.
- 채점 3축 (각 0–10, 무가중 합산): **물리** (좌표 표본 검산·식/기호/부호 본문 일치·정보 소실 없음) / **전달** (한눈 물리·라벨 교차/과밀) / **정합** (현행 용어·영어 ASCII 내부 텍스트·회색조·"좌표는 식 그대로의 수치 평가" 캡션 관례 유지 가능성). **물리 <7 = 총점 무관 탈락(DQ)**.

## 검산 방법 (공통)

- 곡선 좌표는 **독립 재계산**으로 표본 검산 (후보당 최소 2점, 실제 2–5점). 필요 시 동봉 `T{n}_calc.py` 실행·대조 (opus1/T2, opus3/T2, codex1/T1 은 calc.py 가 결함의 직접 증거).
- T1 (flow diagram, 곡선 없음)은 각 노드의 결과식·식번호 태그를 본문 박스식 (eq:vn L910, eq:Uj L992, eq:Ubranch L1127, eq:xieq L1246, eq:branch L1879–1886 (ν=2), eq:dHeff, eq:sum) 과 전수 대조. 인용 라벨 18종 전부 본문에 실재함을 확인 (tab:nodemap 포함).
- T3 공통 검증치: y=ln[ξ/(1−ξ)]+4(1−2ξ), spinodal ξ_s^∓=0.1464/0.8536 에서 y=±1.06568, gap=2.13137 RT/F=54.8 mV @298.15 K — 이 값 대비 각 안의 수치를 대조.
- 최종 추천 8건은 `_skeleton.tex` 로 xelatex 컴파일 재확인 → **전건 0-err PASS** (sonnet2/T1, opus2/T1, sonnet1/T2, opus2/T2, opus2/T3, sonnet1/T3, opus2/T4, codex2/T4).

---

## T1 — fig:spine (계산 진행 spine)

| 안 | 물리 | 전달 | 정합 | 총점 | 근거 1줄 |
|---|---|---|---|---|---|
| sonnet1 | 9 | 7 | 6 | 22 | 식·분기(N7 뒤, L_V<νΔ_grid) 전부 정확하나 식번호가 literal `[eq:vn]` 문자열 — 인쇄본 독자는 해석 불능인데 캡션은 "식 번호"라 주장 |
| **sonnet2** | 9 | 8 | 9 | **26** | \eqref 실번호 해석·라벨 전수 정확·3계조 시각 위계·branch select 명시; 두 경로 병렬 후 선택 구도만 실행순서를 살짝 흐림 |
| sonnet3 | 7 | 8 | 6 | 21 | 분기 판정을 N7 앞에 배치 — L_V 를 계산(N7) 전에 검사하는 인과 오류; 캡션에 T1_calc.py(경연 아티팩트) 참조 |
| opus1 | 7 | 7 | 7 | 21 | N3 식에서 h_η 누락(현행 그림 보유 정보 소실); 평형종=방향불변/꼬리=방향의존 lane 주석은 가치 큼 |
| **opus2** | 8 | 8 | 7 | **23** | 화살표마다 산출량(σ_d,|I|→V_n→U_j→U_j^d→w_j→ξ_eq→L_V) 표기 = 브리프의 "산출량" 요구 직격, mode switch 위치(N7 뒤) 정확; 단 N2 태그 [eq:center] 는 eq:Uj 의 오기 + literal 태그 |
| opus3 | 5 | 7 | 8 | 20 **DQ** | N1 에 eq:n0map(정답 eq:vn)·N2 에 eq:center(정답 eq:Uj) 오태그 2건 + 분기를 N5 직후 배치(인과 오류) |
| codex1 | 6 | 6 | 7 | 19 **DQ** | N8 에서 꼬리 식·charge reversal 소실; 미니 logistic inset(w=1/3, ×0.8 스케일)은 수식 일치하나 동봉 calc.py(w=0.5)와 불일치 — 검증가능성 파손 |
| codex2 | 6 | 6 | 6 | 18 **DQ** | N2/N3/N4 결과식 탈락(현행 정보 소실)+reversal 소실; inset bell 은 ξ(1−ξ)×8.8 정확 일치; 캡션에 T2 아티팩트 참조·격자 배경 노이즈 |
| codex3 | 8 | 4 | 6 | 18 | 현행 사슬·식 전부 보존(안전)하나 개선이 좌우 라벨 상자 2개뿐 — 식번호·분기·반복 화살표 전무, 보조 dashed 화살표 의미 불명 |

**순위**: sonnet2 > opus2 > sonnet1 > sonnet3 ≈ opus1 > opus3(DQ) > codex1(DQ) > codex2(DQ) ≈ codex3.

**추천 top-2**
1. **sonnet2** — 유일하게 "식번호 실해석(\eqref) + 정확 라벨 매핑 + 분기 명시 + 시각 위계" 4박자가 결함 없이 갖춰짐. 남은 결함: N6/N78 병렬-후-선택 구도가 "조건 만족 시 꼬리를 평가하지 않는다"는 본문(L1878)의 실행 순서와 미묘하게 다름.
2. **opus2** — 산출량-온-화살표는 9안 중 최고의 정보 설계. 편입 시 필수 교정 2건: N2 태그 [eq:center]→eq:Uj, literal `[eq:*]` 문자열→\eqref.
- **합성 제안**: sonnet2 골격에 opus2 의 화살표 산출량 주석을 이식하고, 분기를 opus2 식(N7 뒤 mode switch)으로 배선하면 인과·정보량 모두 최상.
- **현행 유지?** 아니오 — 현행은 식번호·분기·반복 표기가 전무, top-2 가 명백 우위.

---

## T2 — fig:staging (갤러리 채움 ↔ 전이 전위)

| 안 | 물리 | 전달 | 정합 | 총점 | 근거 1줄 |
|---|---|---|---|---|---|
| **sonnet1** | 10 | 8 | 9 | **27** | 하단 4곡선 = eq:eqpeak×tab:staging 초기값의 진짜 수치 평가(표본 전점 재계산 일치: 4→3 z=0.1→1.2469, 2→1 V=0.086→10.399), 진축척 V축, 범례 무충돌을 좌표로 검증해 둠; 상하 대응이 전이명뿐 |
| sonnet2 | 7 | 7 | 8 | 22 | Li 점입자+2L jitter(액체상 구분)는 참신·정직하나 0.38pt 점은 인쇄 시 소실 위험, peak 텐트가 등폭·등고 schematic |
| **sonnet3** | 9 | 9 | 7 | **25** | 진축척 축+실 bell(전 높이 0.1536 균일 스케일·값 재계산 일치)+상단 칸→하단 실위치 점선 leader("pitch≠true spacing" 주석) = 브리프 요구 직격; 캡션의 T2_calc.py 참조·"중첩=eq:sum 시각화" 경미 과장 |
| opus1 | 2 | 8 | 5 | 15 **DQ** | calc.py 가 `Q=[1,1,1,1] # schematic amplitude` 로 그린 합산 곡선을 캡션은 "Q_j 공식, 좌표는 식 그대로의 수치 평가"라 주장 — **허위 검증가능성 문구** + peak 높이비 왜곡(진짜는 2→1 이 10.4 로 압도, 그림은 2L→2 가 최고) |
| **opus2** | 8 | 9 | 9 | **26** | bell glyph 위치·상대폭 정확(xscale=9.17w 전 비율 검증), 정점 균일화를 캡션에 정직 고지, U/w/Q 데이터 카드+dropline; 범주축이라 0.140/0.120 의 20 mV 근접은 안 보임 |
| opus3 | 6 | 8 | 7 | 21 **DQ** | 선형 V축+slanted leader 는 좋으나 glyph 높이=0.4+1.8Q(affine, calc.py 확인)인데 캡션은 "Q_j 에 비례" — 허위 정량 주장 |
| codex1 | 6 | 7 | 6 | 19 **DQ** | 축 선형(44.1/V) ✓ 이나 marker 가 문서에 없는 Gaussian·전이 무관 등폭 등고 — "식 그대로" 관례 위반 |
| codex2 | 4 | 5 | 6 | 15 **DQ** | 하단축 방향 역전으로 0.210 V(4→3) guide 가 stage 1 열 쪽에 도달(적극 오도)+3점 텐트를 "logistic 미분 종 수치 평가"라 주장(등폭·값 불일치) |
| codex3 | 8 | 6 | 7 | 21 | 허위 없음·패턴 보존이나 peak 시각화 자체가 없고(문장 라벨뿐) 범주 간격에 수치 라벨; \code{T2_calc.py} 캡션 참조 |

**순위**: sonnet1 > opus2 > sonnet3 > sonnet2 > codex3 > opus3(DQ) > codex1(DQ) > opus1(DQ) ≈ codex2(DQ).

**추천 top-2**
1. **sonnet1** — 유일하게 "진짜 축척 + 진짜 식 평가 + 검증가능성 문구 그대로 유지 가능"을 전부 충족. 남은 결함: 상단 칸→하단 peak 연결선 부재(전이명 대응뿐), stage 2L 비율 표기 "(1:2L)" 어색.
2. **opus2** — 단일 패널 준정량 대안으로 가장 깔끔·정직. 남은 결함: 범주축이라 실전위 간격 정보 없음.
- **합성 제안**: sonnet1 골격 + **sonnet3 의 점선 leader(칸 경계→실축 위치) 및 "schematic pitch ≠ true spacing" 주석** 이식이 최상 조합.
- **현행 유지?** 아니오 — 현행은 하단 전위축 자체가 없어 브리프 요구 미충족.

---

## T3 — fig:hysloop (비단조 V_eq·과주행·spinodal gap)

| 안 | 물리 | 전달 | 정합 | 총점 | 근거 1줄 |
|---|---|---|---|---|---|
| **sonnet1** | 10 | 9 | 9 | **28** | 전 표본 재계산 일치+Maxwell 선(γ→0 plateau)+gap 실수치 "≈54.8 mV"(재계산 54.76 mV 일치)+방향 화살표 정확 |
| sonnet2 | 8 | 7 | 7 | 22 | 캡션이 ξ_s^+ 를 "극대"로 오기(본문·자기 그림과 모순), Maxwell·ΔU 라벨이 우측 x≈1.0–1.1 에 동시 밀집, T3_calc.py 캡션 참조 |
| sonnet3 | 5 | 9 | 7 | 21 **DQ** | Ω-가족(2.4205/5.2445, 극값 0.1212/2.0001 재계산 일치)은 9안 중 최고 콘텐츠이나 **충전 과주행 화살표가 역방향**(ξ_s^+ 가 아니라 ξ=0.98 쪽으로) — 브리프의 핵심 요구(방향 명확화) 정면 위반·자기 캡션과 모순 |
| opus1 | 10 | 8 | 9 | 27 | thin 전곡선+bold 경로 위계·metastable 주석·방향 정확; gap 실수치 없음 |
| **opus2** | 9 | 9 | 10 | **28** | g″<0 불안정 띠(fig:doublewell 와 접속)+spinodal 좌표 readout+±1.066 y눈금+gap=2.131RT/F, 캡션에 평가식 자체 명기(검증가능성 최상); 현행의 in-plot γ→0 주석은 캡션으로 이동(경미) |
| opus3 | 10 | 7 | 9 | 26 | 3기준선(Maxwell+spinodal 2)·방향 정확하나 white-fill Maxwell 라벨이 ξ≈0.45–0.49 곡선 구간을 가림 |
| codex1 | 10 | 7 | 9 | 26 | 수치 전점 일치·충/방 선종 구분·gap 2.1314RT/F; "Maxwell line y=0" 라벨이 x-tick 0.5 라벨과 충돌, 동일 곡선 2중 묘화 잡티 |
| codex2 | 10 | 6 | 7 | 23 | 수치 정확·±1.066 눈금이나 Maxwell 라벨이 곡선 통과 대역(ξ≈0.44–0.49)에 걸침+전면 격자 배경, T3_calc.py 캡션 참조 |
| codex3 | 9 | 7 | 7 | 23 | 현행+가이드+양방향 화살표는 성실하나 in-figure ΔU_j^hys 기호를 "spinodal gap" 텍스트로 대체(기호 연결 소실)+Maxwell 라벨-tick 충돌+\code 캡션 참조 |

**순위**: opus2 ≈ sonnet1 (동점 28) > opus1 > opus3 ≈ codex1 > codex2 ≈ codex3 > sonnet2 > sonnet3(DQ).

**추천 top-2**
1. **opus2** — 브리프 3요구(방향 화살표·Maxwell 수평선·gap 상한 주석)에 더해 불안정 띠로 fig:doublewell 와 시각 연결, 캡션 내 평가식 명기. 남은 결함: γ→0 주석이 그림 안에 없음.
2. **sonnet1** — in-figure 실수치(≈54.8 mV)와 γ→0 주석이 그림 안에 있어 자립성이 가장 높음.
- **합성 제안**: opus2 골격 + sonnet1 의 "≈54.8 mV"·"γ→0: both collapse to y=0" in-plot 주석. sonnet3 의 Ω-가족 곡선은 **충전 화살표 좌표 순서만 뒤집으면** 3자 합성의 최상 요소로 재활용 가치 있음.
- **현행 유지?** 아니오 — 현행엔 Maxwell 선·gap 수치·spinodal 강조가 없음.

---

## T4 — fig:barrier (Eyring 장벽 — 평형 vs 구동)

| 안 | 물리 | 전달 | 정합 | 총점 | 근거 1줄 |
|---|---|---|---|---|---|
| sonnet1 | 9 | 8 | 9 | 26 | 폐형 quartic G₀=0.1+0.9(1−u²)²+구간선형 h(x) 전 표본 일치(0.69/1.29/0.60 정합); 단 χ 브래킷이 기하상 50:50 구간에 0.35:0.65 라벨(위치-라벨 비정합) |
| sonnet2 | 8 | 8 | 6 | 22 | 5앵커는 eq:bv 로 정확·"보간은 물리식 아님" 정직 고지이나 x=0.5 에서 driven>equilibrium 보간 artifact, 캡션에 T4_calc.py 2회 참조, "식 그대로" 문구 유지 불가형 |
| sonnet3 | 8 | 8 | 7 | 23 | raised-cosine 공개 보간·**TS 를 χ 분할점에 실제 배치한 유일한 안**(기하 정합); (b)에 평형 점선 오버레이 부재 = 현행 보유 정보 소실 |
| opus1 | 9 | 9 | 8 | 26 | cos²+선형 tilt(h(ts)=½=χ 자기정합)·공식 캡션 명기·peak↓χ𝒜 연결 화살표; ΔH_a^eff 주석이 그림·캡션 모두 부재(브리프 요구) |
| **opus2** | 10 | 9 | 9 | **28** | sin² 폐형 공식 캡션 명기+전 수치 라벨(ΔG_a=0.90, 0.65/1.15/χ𝒜=0.25/𝒜=0.50 전부 재계산 일치)+ΔH_a^eff in-figure+χ·(1−χ)→detailed balance 연결 문장; "이중 포물선" 용어만 느슨(실제 raised-cosine) |
| opus3 | 8 | 6 | 6 | 20 | 단일 패널 겹침 재해석은 흥미로우나 평형 ΔG_a 브래킷 소실(정보 소실)+rev 라벨이 점선 곡선과 교차 위험+**node 내부에 한글 "식~" (ASCII 규칙 위반)** |
| codex1 | 9 | 7 | 7 | 23 | quartic+tilt(A=0.7) 전점 일치하나 A 브래킷이 driven 곡선 관통, ΔH_a^eff 부재, 캡션에 공식 없음("Python 수치 평가"만) |
| **codex2** | 10 | 8 | 8 | **26** | quartic 공식을 캡션에 그대로 명기(G₀=0.10+0.90(x−1)²(x−5)²/16, 𝒜=0.35 정합 전점 일치)+ΔH_a^eff in-figure; fwd 라벨이 점선 곡선과 graze, T4_calc.py 캡션 참조 |
| codex3 | 9 | 7 | 6 | 22 | 현행 좌표가 cos² 임을 정확 재구성하고 rev/𝒜/χA 를 보강(성실)하나 ΔH_a^eff 부재+A 브래킷 곡선 관통+\code 캡션 참조 |

**순위**: opus2 > sonnet1 ≈ opus1 ≈ codex2 (26 동점) > sonnet3 ≈ codex1 > sonnet2 ≈ codex3 > opus3.

**추천 top-2**
1. **opus2** — 물리 결함 0 + 브리프 3요구(매끄러운 폐형 개형·χ·(1−χ) 분할·ΔH_a^eff 주석) 유일 완비 + 전 수치 라벨. 남은 결함: reverse 가이드가 점선 (a) 곡선과 1회 교차, "이중 포물선"→"raised-cosine" 용어 교정 권.
2. **codex2** — 물리 10 동급, 캡션 공식 명기·ΔH_a^eff 완비. 편입 시 캡션의 T4_calc.py 문구 삭제 필요.
- **합성 제안**: opus2 골격 그대로. χ≠½ 일반성까지 보이려면 sonnet3 의 "TS=χ 분할점" 기하(하단 χ:1−χ 치수선 포함)를 (b)에 이식.
- **현행 유지?** 아니오 — 현행은 역장벽 크기·χ 분할·ΔH_a^eff 주석이 없고 (b) 곡선이 비공개 스플라인.

---

## 부기 (공통 관찰)

1. **캡션의 경연 아티팩트 참조 금지 필요**: sonnet3(T1·T2·T3), sonnet2(T3·T4), codex2(T2·T3·T4), codex3(T1–T4) 등이 캡션에 `T{n}_calc.py` 를 인용 — 본문 편입 시 존재하지 않는 파일 참조가 되므로 편입 전 일괄 삭제/치환해야 함 (tex 주석 내 참조는 무방).
2. **calc.py↔tex 불일치 2건**: codex1/T1 (logistic w 상이), opus1/T2 (Q_j=1 schematic 인데 캡션은 정식 주장) — 후자는 허위 문구라 탈락 사유.
3. 라벨 18종(eq:n0map·eq:vn·eq:Uj·eq:dUhys·eq:Ubranch·eq:center·eq:wbase·eq:xieq·eq:eqpeak·eq:branch·eq:LV·eq:Acut·eq:chid·eq:dHeff·eq:peakshape·eq:reversal·eq:sum·tab:nodemap) 본문 실재 확인 완료. `\code` 매크로·tikz 라이브러리 5종은 본문·스켈레톤 동일 — 추천안 8건 xelatex 0-err.
