# V1010_HANDOVER_INSPECT draft C3

- 검수자: C3
- 역할/SPEC: 두 축 holistic + G-follow/G-usable + radius 회의. v1.0.10이 두 최우선 축(물리논리 전개 비약 0, 교과서 follow)을 각 AUTHOR_BRIEF 요구 대비 유지하는지 검수. 그래프는 apparent-U/eta 의도 물리 기준이며 bell은 정상. radius 연구는 회의적 참조이지 확정 근거가 아님.
- 출력 성격: 검수 의견만. 코드/문건 수정 없음.

## 0. 직접 확인 범위

base prompt `C:/Users/lksz1/AppData/Local/Temp/claude/d--Projects/f45f576c-1efc-4f50-8591-1f84bb7d7f39/scratchpad/handover_inspect_base.txt` 전문과 계획서 `Claude/plans/2026-07-06-v1010-handover-integrity-inspection-plan.md` 전문을 먼저 읽었다.

현재 대상은 `Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py` 1-851, `Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex` 1-1937, `Claude/docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex` 1-750을 전 범위로 확인했다. Ch1 긴 출력 중 누락 의심 구간은 1267-1275, 1701-1766을 좁혀 재확인했다.

SPEC/기록으로는 v8/v9/ch1v10/ch2_v4 AUTHOR_BRIEF와 FIX_LIST, `PHASE_CH1v10_RESULT.md`, radius/w_eff handover와 radius verdict 계열, `broadening_w_design.md`, `CODE_w_check.md`를 확인했다. 구버전 대조는 `old/Ch1_v9`, `old/Ch1_v10`, `old/Ch2_v4`, `results/code/Anode_Fit_v11_final.py`의 필요한 구간과 전자 엔트로피 section hash를 직접 계산해 확인했다.

## 1. 문제 발견 우선 결론

### F1. Ch1 전자 엔트로피 절은 현재 v1.0.10에서 byte-preserved가 아니다

판정: 인계 무결성 결함. 물리식이 곧바로 틀렸다는 뜻은 아니지만, 기록의 "byte-identical/unchanged" 주장과 현재 산출물이 맞지 않는다.

근거:

- 기록 `Claude/results/builds/ch1v10/PHASE_CH1v10_RESULT.md:20`은 전자 엔트로피 절을 byte-identical로 보존한 항목으로 기록한다.
- 구 Ch1 v9 전자 엔트로피 절은 `Claude/old/Ch1_v9/graphite_ica_ch1_v9.tex:885-1068`, 구 Ch1 v10 전자 엔트로피 절은 `Claude/old/Ch1_v10/graphite_ica_ch1_v10.tex:914-1097`이며, 직접 SHA-256 계산 결과 둘 다 `ED246D9DF24A38E06618AB748BF1F612C5EFB020C9AE2E412BE603381AFB8E53`이었다.
- 현재 v1.0.10 전자 엔트로피 절은 `Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex:933-1167`이고 직접 SHA-256 계산 결과 `2488E68FB80B9F6FBD0B37420B79C04C3FC1883A2BF2BD29D23D07C533FA70D3`였다. 줄 수도 184줄에서 235줄로 늘었다.
- 실제 추가/변경 흔적은 직접 엔트로피 경로 `Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex:979-992`, eV->J 환산 보강 `:1029-1038`, T^2 누적계수 `:1054-1066` 등이다.

refute/downgrade:

- 이 항목은 "전자 엔트로피 물리 자체가 붕괴"가 아니다. 현재 절은 Fermi-Dirac 출발 `:953-964`, Sommerfeld 가정 `:965-978`, 몰당 변환 `:1018-1028`, 부호 규약 `:1039-1047`을 더 자세히 적고 있어 G-derive를 강화한 부분도 있다.
- 따라서 CRIT가 아니라 "인계 기록과 산출물 불일치"다. 다만 base/plan이 인계 무결성을 요구하므로 통과 처리할 수 없다.

### F2. 전자항 크기 설명은 G-follow 관점에서 아직 가장 위험한 혼동 지점이다

판정: G-follow/G-usable 결함 후보. current text 안에 구분 문단이 존재하므로 물리 모순으로 단정하지는 않지만, 독자가 AUTHOR_BRIEF의 `0.18 k_B/atom ~= 1.5 J/(mol K)` 요구와 현재 `-46 J/(mol K)` gate depth를 같은 물리량으로 읽을 위험이 남는다.

근거:

- v9 AUTHOR_BRIEF는 LCO 전자 엔트로피 anchor를 `0.18 k_B/atom ≈ 1.5 J/mol/K`로 둔다(`Claude/results/builds/v9/v9-00_spine/AUTHOR_BRIEF.md:34`). v9 FIX_LIST도 같은 크기 보존을 요구한다(`Claude/results/builds/v9/v9-00_spine/FIX_LIST_v911.md:14`).
- 현재 Ch1 앞쪽 설명은 전자항을 "몰당 |Delta S_e| ≈ 1.5 J/(mol K) 규모의 소수 음의 보정"이라고 한다(`Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex:501-505`).
- 같은 현재 절 후반은 세 양을 구분하며, 부분몰 차 `0.18 k_B/atom`과 별도로 gate 미분 골 깊이가 중심에서 `≈ -46 J/(mol K)`라고 한다(`Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex:1123-1130`).
- code plug-in 설명은 forward 슬롯에 몰당 `N_A partial S_e/partial x`를 더한다고 한다(`Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex:1757-1761`). 이 경로는 `-46` gate-depth 식과 연결되므로, 앞쪽의 "전자항은 1.5 J 규모" 문장이 별도 척도라는 사실을 못 본 독자는 같은 전자항 안의 수치 충돌로 읽을 수 있다.

refute/downgrade:

- 현재 문서가 이 차이를 완전히 무시한 것은 아니다. `Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex:1123-1130`은 절대량, 부분몰 anchor, gate 골 깊이를 다른 척도로 명시한다.
- 그러므로 "부호/단위 물리 오류 확정"은 아니다. 하지만 두 축 중 "교과서 follow" 기준에서는 가장 약하지 않은 위험이다. 앞쪽 대표 설명 `:501-505`가 후반의 gate-depth 구분을 선행 참조하지 않아 인계자가 실수하기 쉽다.

### F3. LCO code 기본값은 AUTHOR_BRIEF 물리 anchor와 직접 맞지 않아 G-usable 위험이 있다

판정: G-usable 결함 후보. 현재 코드가 스스로 placeholder라고 라벨링하므로 숨은 결함은 아니지만, v1.0.10 사용자가 `LCO_MSMR_LIT`를 그대로 물리 기준값으로 쓰면 AUTHOR_BRIEF 요구와 어긋난다.

근거:

- v9 AUTHOR_BRIEF는 LCO T1 MIT를 약 3.90 V, `x_MIT≈0.85`, T2 약 4.05 V, T3 약 4.17-4.20 V로 요구한다(`Claude/results/builds/v9/v9-00_spine/AUTHOR_BRIEF.md:31-34`). 또한 같은 class를 LCO에 parameter substitution + electronic plug-in으로 일반화하라는 요구가 있다(`:40`).
- 현재 code `LCO_MSMR_LIT`는 `U=3.930`, `U=3.880`, `U=4.050` 세 항이고, electronic 항은 두 번째 항의 `x_center=0.50`, `x_MIT=0.50`에 붙어 있다(`Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py:623-634`). T3 약 4.17 anchor도 기본 list에는 없다.
- 현재 Ch1 표 주변은 이 문제를 알고 있으며 code 값이 tier-C placeholder이고 round-trip fitting 전 초기값이라고 명시한다(`Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex:321-329`). code도 같은 라벨을 둔다(`Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py:621-622`).

refute/downgrade:

- placeholder 라벨이 명시되어 있어 "문서가 물리 기준값이라고 속인다"는 문제는 아니다.
- 그러나 base SPEC가 `G-usable`까지 요구하고 `docs/v1.0.10/Anode_Fit_v1.0.10.py`를 대상에 포함하므로, 이 상태는 사용자가 바로 import해서 쓰는 code default의 위험으로 남는다. 최소한 v1.0.10 handover에서는 "LCO code default는 물리 anchor가 아니라 시연 placeholder"를 실패 방지 조건으로 크게 남겨야 한다.

### F4. code 헤더에 제거된 `w_eff` 공식 잔재가 남아 있다

판정: 가장 약한 1곳. live code 결함은 아니고 문서/헤더 무결성 잡음이다.

근거:

- 현재 code 헤더는 구현식 목록에서 `w = nRT/F`와 함께 "옵션 `w^eff = (RT/F)(1-Omega/2RT)`"를 적는다(`Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py:37-44`).
- 같은 파일 앞부분은 `use_w_eff` 경로 제거를 v1.0.10 변경으로 명시한다(`Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py:4-7`).
- 실제 폭 계산은 `_n_factor`가 `n` 우선, `w` fallback, 없으면 1.0을 반환하고(`Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py:294-300`), `_width`는 `func_w(T, self._n_factor(tr))`만 쓴다(`:303-306`). 즉 live `use_w_eff` branch는 없다.

refute/downgrade:

- 이 항목은 graphite bell이나 w_eff runtime bug 재발이 아니다. 제거 의도와 실제 code path는 맞다.
- 다만 인계 검수 기준에서는 헤더 한 줄이 나중 작업자에게 `w_eff` 복원을 유도할 수 있는 약한 오염이다.

## 2. Refute / 오적발 방지

### R1. graphite bell-shaped peak는 결함이 아니다

- 현재 code header는 graphite bell shape와 area-preserving dQ/dV가 정상이라고 적는다(`Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py:8-11`).
- current Ch1은 solid-solution transition은 원래 bell이고, only LiC12/LiC6 two-phase near-delta가 apparent distribution broadening 대상이라고 분리한다(`Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex:1226-1237`).
- broadening은 `U_app=U_j+eta`, `U_j=const`, `rho(U_app)` forward average로 정리되어 있다(`Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex:1275-1297`). 이는 v10 FIX_LIST의 apparent-U/eta correction 요구와 맞는다(`Claude/results/builds/ch1v10/v10-00_spine/FIX_LIST_v1011.md:5-12`).
- 따라서 bell 자체를 "분포가 잘못 들어갔다"거나 "radius를 못 넣었다"는 이유로 잡는 것은 오적발이다.

### R2. radius 연구는 회의적 참조로만 사용해야 하며, current Ch1은 그 경계를 대체로 지킨다

- radius verdict는 "사용자 직감 일부는 맞지만 U_j=radius는 invalid, inverse ill-posed, kinetic이 dominate"라고 한다(`Claude/results/research/radius/RADIUS_VERDICT.md:10`, `:27-36`).
- handover도 "radius를 equilibrium U handle로 재도입하지 말 것", "GITT ≠ true equilibrium", "inverse ill-posed"를 경고한다(`Claude/results/process/HANDOVER_2026-06-30_radius-dqdv-distribution-and-w-eff-bug.md:58-63`).
- current Ch1은 size/radius/PSD convolution을 하지 않는 목록에 넣고, Dahn 사례를 capacity-limit illustration으로만 둔다(`Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex:1314-1325`). forward-only/no inversion 경계도 둔다(`:1326-1331`, `:1350-1351`).
- 그러므로 radius를 확정근거로 삼아 current broadening을 부정할 수 없다.

### R3. Ch2의 `w_eff` 제거는 current defect가 아니라 later SPEC supersession이다

- Ch2 v4 AUTHOR_BRIEF/FIX_LIST에는 `w_eff=w(1-Omega/2RT)` 요구가 남아 있다(`Claude/results/builds/ch2_v4/v4-00_spine/AUTHOR_BRIEF.md:18`, `Claude/results/builds/ch2_v4/v4-00_spine/FIX_LIST_v411.md:21-24`).
- 그러나 ch1v10 AUTHOR_BRIEF는 v10 목표에 `w_eff` complete removal을 넣는다(`Claude/results/builds/ch1v10/v10-00_spine/AUTHOR_BRIEF.md:13-16`), FIX_LIST도 `w_eff` zero를 요구한다(`Claude/results/builds/ch1v10/v10-00_spine/FIX_LIST_v1011.md:24-28`).
- current Ch2 header는 v4-11 기반에서 `w_eff` 축소식을 제거하고 Ch1 broadening으로 교체했다고 명시한다(`Claude/docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex:8-13`). 본문도 effective-width shrink를 반대방향 문제로 설명하고 fitted phenomenological width로 둔다(`:539-568`, `:668-684`).
- 따라서 "Ch2가 v4 brief의 w_eff를 따르지 않는다"는 사실은 맞지만, current v1.0.10 산출물 결함이라기보다 SPEC 계층/인계 문구 정리가 필요한 기록 staleness다.

### R4. Ch2의 통계열역학 follow 축은 대체로 유지된다

- current Ch2는 Z -> occupancy -> entropy -> dU/dT -> q_rev의 분포 체인을 먼저 선언한다(`Claude/docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex:89-100`).
- 단일자리 partition function과 logistic occupancy를 유도한다(`:119-164`), configurational partial entropy를 전개한다(`:221-244`), vib/electronic 분포와 Sommerfeld bridge를 설명한다(`:353-409`), overlap/mixing closed form과 finite-difference validation을 둔다(`:430-482`).
- 최종 "use-this" 식과 한계도 있다(`:668-697`).
- 따라서 Ch2는 `w_eff` SPEC staleness를 제외하면 두 축의 큰 붕괴는 보이지 않는다.

### R5. D-PEAK small-L 오류는 current Ch1에서 재발하지 않았다

- v8 KNOWN_DEFECTS는 small L에서 peak가 0으로 가야 하며 large-L derivative limit와 branch discontinuity를 구분하라고 요구한다(`Claude/results/builds/v8/v8-00_spine/KNOWN_DEFECTS.md:5-10`, `:24-30`).
- current Ch1은 small-L branch와 large-L derivative limit를 분리한다(`Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex:1564-1593`).
- self-test도 "small L returns bell"을 명시적으로 반박하고 large-L derivative limit만 검증한다(`Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex:1901-1906`).

## 3. 두 최우선 축별 종합 판정

### 축 1: 물리논리 전개 비약 0

대체로 유지. Broadening은 apparent-U/eta 기준으로 정정되어 있고, `U_j`를 radius/particle-size distribution으로 오인하는 길은 차단되어 있다. `w_eff` runtime path도 제거되어 있다.

남은 물리논리 위험은 전자항 magnitude trail이다. current 문서가 세 척도를 구분해 refute 장치를 두지만, 앞쪽의 "전자항은 1.5 J 규모" 문장과 후반의 "-46 J gate depth"가 같은 `Delta S_e` 문맥 안에 있어 인계자가 단위/미분/부분몰 anchor를 다시 섞을 수 있다.

### 축 2: 교과서 follow / G-follow / G-usable

Ch1/Ch2의 큰 derivation ladder는 유지된다. v8의 G-derive/G-follow 요구, v9 LCO 전자 엔트로피 요구, ch1v10 broadening 요구는 대부분 본문 구조로 살아 있다.

하지만 G-usable 기준에서는 세 가지 약점이 남는다.

1. 전자 엔트로피 절이 byte-identical이라는 기록은 현재 산출물과 다르다.
2. LCO code default가 AUTHOR_BRIEF의 physical anchor가 아니라 placeholder인 점이 code 사용자에게 위험하다.
3. code header의 `w_eff` 잔재와 Ch2 v4 SPEC의 `w_eff` staleness는 current v1.0.10의 의도와 충돌하는 약한 인계 잡음이다.

## 4. Union / Refute 요약

문제로 남길 항목:

- F1: Ch1 전자 엔트로피 절 byte-preservation 기록 불일치.
- F2: 전자항 `1.5 J` anchor와 `-46 J` gate-depth 설명의 followability 위험.
- F3: `LCO_MSMR_LIT` placeholder default의 G-usable 위험.
- F4: code header `w_eff` 잔재. 가장 약한 1곳.

반박/오적발 항목:

- graphite bell-shaped peak는 정상이다.
- radius는 회의적 참조이며 broadening의 확정 반증이 아니다.
- current Ch2의 `w_eff` 제거는 later v10 SPEC에 맞는 변화다.
- Ch2 distribution/entropy/q_rev follow ladder는 유지된다.
- D-PEAK small-L defect는 current Ch1에서 재발하지 않았다.

## 5. 5-line 결론

1. v1.0.10은 graphite broadening의 핵심 의도(apparent-U/eta, bell 정상, forward-only, no-radius-inversion)를 대체로 유지한다.
2. `w_eff` live code 제거도 유지되어 runtime 재발은 보이지 않는다.
3. 그러나 Ch1 전자 엔트로피 절은 기록상 byte-identical이라고 보기 어렵고, 직접 hash로 current가 구 v9/v10과 다름을 확인했다.
4. 전자항 수치 설명(`1.5 J` anchor vs `-46 J` gate depth)과 LCO code placeholder default는 G-follow/G-usable 관점의 주요 약점이다.
5. 가장 약한 1곳은 code header의 `w_eff` 잔재이며, 이는 live bug가 아니라 인계 잡음이다.
