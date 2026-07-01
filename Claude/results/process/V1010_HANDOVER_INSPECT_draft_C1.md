# V1010_HANDOVER_INSPECT draft C1

역할: C1 / cross-version 물리 손실 검수.  
판정 범위: `results/research/radius/DOCS_say_about_distribution.md` + `old/_archive/{graphite_ica_ch1_Fable_v3,graphite_ica_ch1_Opus_v4,graphite_ica_ch1_Opus_v5}.tex` 대 `docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex`.  
주의: bell/종모양 자체는 결함으로 보지 않았다. radius/size는 회의적으로 보되, `입자 크기 -> 평형 U_j`와 `입자 크기/구조 -> 동역학 장벽 G`를 분리했다.

## 확인 범위

- base 프롬프트 `handover_inspect_base.txt`: 전문 확인. 핵심 SPEC = v3/v4/v5의 `rho_G` 배리어 분포, 두 broadening, 현상학적 `w`, forward-only, v1.0.10 부재 여부를 정당 컷 vs 손실로 판정.
- 계획서 `Claude/plans/2026-07-06-v1010-handover-integrity-inspection-plan.md`: 전문 확인. 핵심 SPEC = v10에서 broadening 복원, `w_eff` 완전 제거, size 전면 배제, `apparent-U=U_j+eta`, forward-only.
- `DOCS_say_about_distribution.md`: 1-28행 직접 확인. v3/v4/v5는 명시적 분포 골격을 갖고, 연구 결론상 `rho_G(G)`는 올바른 동역학 채널, `rho_G` 역산 금지는 R1 결론과 일치한다고 정리됨(5-15, 19-28행).
- 보조 전문 검독: v3 1-2588행, v4 1-2912행, v5 1-1883행. 주요 근거 구간은 직접 재확인했다.
- v1.0.10 직접 대조 구간: release note 1-60행, `w` 이중지위 716-743행, broadening 1220-1352행, caption 1380-1390행, tail/Lq 1408-1505행, D-PEAK 1528-1591 및 1898-1907행, 입력표/코드 대응 1768-1806 및 1838-1845행. `rho_G|sigma_G|KWW|stretched|superpose|장벽 분포` 검색 결과는 release comment의 KWW 제거 언급 46행 외 본문 모델 근거 없음.

## 문제 발견

### [HIGH] `rho_G(G)` 동역학 장벽분포와 저온 stretched-tail 진단이 v1.0.10 본문에서 손실됨

위치:
- 현행: `docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex` 1244-1248행은 유한율속 꼬리를 단일 `L_V` 기작으로 설명하고, 1415-1496행은 전이당 스칼라 `L_q/L_V` 평가로 닫는다. 1788-1790행 입력표에도 `dH_a`, `dS_a`, `dVdq_qa`, `L_V`만 있고 `rho_G/sigma_G` 또는 분포 적분 입력이 없다. 1843행은 broadening 설명이 “모델 항 0”임을 명시한다.
- SPEC: v3 1605-1650행, v4 1611-1656행, v5 1116-1140행은 `rho_G(G)`를 활성화 장벽의 용량분율 밀도로 두고, `sigma_{ln L}=sigma_G/RT`, `int rho_G(G) ... dG`, `rho_G -> delta` 환원, stretched/KWW 꼬리, 역산 금지, forward model 대조를 한 세트로 둔다.
- SPEC 보조: `DOCS_say_about_distribution.md` 11-14행 및 24-26행은 이 `rho_G` 배리어 분포가 “크기가 들어오는 올바른 동역학 채널”이고, R2가 `tau propto r^2`/크기-동역학 맵을 채운다고 정리한다.

무엇이 인계 안 됐나:
- v1.0.10은 `apparent-U = U_j + eta`의 `rho(U_app)` 앙상블 broadening은 복원했다(1275-1297, 1326-1333, 1342-1351행). 그러나 이것은 2상 peak의 겉보기 중심 분포 설명이고, v3/v4/v5의 꼬리 길이 분포 `rho_G(G)`가 주던 저온 증폭 `sigma_G/RT`, 반로그 현 아래 처짐, KWW/stretched tail, `beta(T)` 반증 규칙은 남아 있지 않다.
- 현행 1291-1292행은 `eq:ensavg`가 ② 내재폭과 ③ 앙상블 `eta` 산포만 담고 ① 유한율속 skew는 대칭 합성곱이 아니라고 분리한다. 따라서 `rho(U_app)` 복원으로 `rho_G(G)` 꼬리분포 손실을 refute할 수 없다.

왜 문제인가:
- G-derive: v1.0.10은 “유한율속 꼬리”를 Eyring 단일 장벽 + 전이당 `L_V`로 유도하지만, 과거 버전의 “같은 전극 안에서 장벽 분포가 꼬리 길이 분포를 만든다”는 2차 물리층이 빠져 있다. 저온에서 꼬리가 왜 단순 지수보다 늘어지는지의 전개가 축약된다.
- G-follow: 독자는 `eta` 분포와 `L_V` 꼬리를 읽고도, 반로그 tail curvature가 보이면 무엇을 켜고 무엇을 역산하지 말아야 하는지 알 수 없다. v5 1647행의 “꼬리가 반로그 현 아래로 처짐 -> rho_G 분포 넓음 -> 분포 적분 켜기” 진단이 사라졌다.

refute:
- “v10 의도는 코드 차원 증가 없이 현상학적 `w`에 흡수”라는 반론은 일부 맞다. 현행 1334-1338행은 PSD convolution 모델을 넣지 않는다고 못박는다.
- 그러나 v3/v4/v5의 `rho_G`는 PSD convolution만이 아니라 장벽/동역학 꼬리분포의 forward-only 설명과 진단이다. `DOCS_say_about_distribution.md`도 `rho_G`를 R2 동역학 분산의 정식화로 보며(24행), 단순 radius 평형분포와 구분한다. 그러므로 “size 전면 배제”만으로 `rho_G` 전체 삭제를 정당화하기 어렵다.

렌즈: cross-version 물리 손실, G-derive, G-follow.

가장 약한 지점:
- v1.0.10 1310-1338행이 “설명만 복원, 코드 모델 항 0, dimension 증가 없음”을 명시하므로, 만약 v1.0.10의 승인 범위가 “두-상 `apparent-U` broadening만 복원하고 kinetic barrier distribution은 후속장으로 보류”였다는 별도 기록이 있으면 이 항목은 HIGH에서 MED로 내려간다. 이번 C1 범위에서 그런 명시적 보류 근거는 발견하지 못했다.

## 정당 컷 / 무결 영역

### [PASS] bell/종모양은 의도된 물리이며 결함 아님

현행 1226-1237행은 연속 고용체 전이는 원래 logistic bell이고, 2상 전이만 평형 delta가 broadening으로 bell이 된다고 구분한다. 1342-1351행과 1380-1389행은 세 broadening 출처와 `eta` 분포/forward-only/size 배제를 함께 둔다. 따라서 bell 자체를 “구조 결함”으로 적발하면 오적발이다.

### [PASS] 두 broadening과 현상학적 `w` 지위는 v3/v4/v5보다 정교하게 보존됨

SPEC v3 2077-2088행, v4 2083-2095행, v5 1435행의 “입자 분포 broadening + 동역학 꼬리, 2상 `w`는 현상학적 피팅 폭”은 현행 728-743행 및 1244-1307행에 유지된다. 현행은 더 나아가 평형 `U_j` 분포가 아니라 `eta`/`U_app` 분포라고 정정한다(1275-1285, 1300-1306행). 이는 손실이 아니라 개선이다.

### [PASS] `w_eff`/isotherm-slope narrowing 제거는 정당 컷

SPEC v3 839-868행, v4 845-875행, v5 607-638행은 `w_eff = RT/F(1-Omega/2RT)`식의 등온선 중심기울기 좁힘을 갖는다. 그러나 계획서와 현행 release note는 `D-WEFF` 정정 및 `w_eff` 완전 제거를 명시한다(현행 19-20, 32-33행). 현행 725-726행도 상호작용으로 폭을 인위로 좁히는 별도 항을 두지 않는다고 한다. 이는 v10 SPEC의 정정 이행으로 보고, cross-version 손실로 보지 않는다.

### [PASS] D-PEAK 계열 정정은 유지됨

현행 1528-1591행 및 1901-1906행은 `L_V >> Delta_grid`에서만 `peak_shape=(xi_eq-xi_lag)/L_V`가 미분 커널로 수렴하고, `L_V -> 0` 평형 회복은 식의 극한이 아니라 `eq:branch` 스위치가 담당한다고 명시한다. base SPEC의 bell 오적발 주의와 일치한다.

## 버전 전환별 인계 판정

- v3/v4/v5 -> v8: `rho_G` 배리어 분포, 두 broadening, `w` 지위 중 일부가 제거되어 후퇴. 특히 `rho_G` 꼬리분포와 stretched-tail 진단 손실.
- v8 -> v9: v8 흑연 구조 보존 + LCO 전자엔트로피 추가. C1 초점의 `rho_G` 손실은 복구되지 않은 것으로 판정.
- v9 -> v10: broadening 복원은 실질 개선. `apparent-U=U_j+eta`, forward-only, size 배제, `w_eff` 제거는 정정으로 판정. 단 `rho_G(G)` 동역학 장벽분포의 온도 의존 꼬리 진단은 완전 복원되지 않음.
- v10 -> v1.0.10: v10-11 broadening 설명은 v1.0.10에 대체로 보존. 신규 bell/코드 회귀 결함은 C1 범위에서 발견하지 못함. 다만 위 `rho_G` 손실은 v1.0.10까지 미해소.

## 5줄 요약

1. 초점: v3/v4/v5의 분포/broadening 물리가 v1.0.10에서 정당 컷인지 손실인지 대조.
2. 인계 결함 수: HIGH 1건(`rho_G(G)` 동역학 장벽분포 및 `sigma_G/RT` stretched-tail 진단 손실).
3. 최중대: `rho(U_app)` 복원은 충분하지만, `rho_G(G)` 꼬리 길이 분포까지 대체하지 못한다.
4. 두 축 판정: G-derive/G-follow 모두 이 한 지점에서 약화. 나머지 broadening, `w` 이중지위, D-PEAK, bell 물리는 보존/개선.
5. 오적발 자기표시: bell은 결함 아님. radius 평형분포 배제와 `w_eff` 제거는 정당 컷으로 보았다.
