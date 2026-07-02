# V1012 P4.3 review C2r — union map v10

- ID: C2r
- 대상: `Claude/results/process/V1012_P43_map_v10.md`
- 금지 준수: tex/코드/통합본 수정 없음. 본 검수 파일 1개만 작성.
- 실제 확인: base prompt 전문 1-11행, map v10 1-677행, Ch1/Ch2 v1.0.12 line count(1964/755) 및 삽입·라벨 관련 구간, FABLE_REAUDIT_C4_note 1-68행, draft군 MSMR/H-2/config/방향 슬롯 관련 대조.

## 판정 요약

**판정: FAIL-BLOCKER(조건부).** center/hys/peak/H-2의 대수·차원·극한 검산은 대부분 정합하지만, 편입 직전 supplement로는 아래 3곳이 막는다. 특히 §4 config 부호는 map 자신이 원자적 결합을 인정하면서도 finalizer 체크리스트에서 별도 10차로 미루고 있어, 그대로 편입하면 같은 절 안에 정반대 부호가 병존한다.

## Findings

### [HIGH/BLOCKER] §4 `eq:lco-configsplit`와 원문 L1728-1729 역부호를 원자적으로 처리하지 않으면 절 내부가 즉시 모순

- 위치: map L363-L370, L401-L407, L417-L420, L619, L655; Ch1 원문 L1728-L1729; Ch2 원문 L237-L243, L678-L679.
- 무엇이 문제인가: map §4(c)는 삽입 기준 config 내부항을 `+R\ln[\xi/(1-\xi)]`로 신설한다. 그러나 finalizer 체크리스트는 L1728-L1729 원문 `R\ln[(1-\xi)/\xi]`를 F-1 판정 전까지 유지하라고 한다. 그러면 `eq:lco-configsplit` 바로 뒤 bullet이 같은 물리항을 반대 부호로 설명한다.
- 재유도 근거: `S_config=-R[theta ln theta+(1-theta)ln(1-theta)]`에서 `dS/dtheta=-R ln[theta/(1-theta)]`, `theta=1-xi`이므로 삽입 기준 부분몰항은 `+R ln[xi/(1-xi)]`다. 희박 극한 `xi -> 1`에서도 삽입 가능한 빈 자리 수가 커져 `+infty`가 맞다. Ch2 L237-L243 및 revheat L678-L679도 같은 부호다.
- 수정안: §4 블록 편입은 F-1 정정과 반드시 같은 원자적 변경으로 묶는다. F-1을 10차 이후로 미룰 경우, §4(c)의 `eq:lco-configsplit`도 함께 보류하거나 역부호 bullet과 충돌하지 않는 중립 문장으로 낮춰야 한다.

### [HIGH] §5 MSMR 대응의 `f=-\sigma_d`는 map 내부의 `theta/x_j` 및 `xi=1-theta` 정의와 부호가 맞지 않음

- 위치: map L437-L447, L453-L467, L474-L480, L641; Ch1 `eq:xieq` L787; 코드 주석 L619, L645.
- 무엇이 문제인가: map은 `theta_j^{MSMR}=x_j/X_j`를 리튬화 점유율로 두고, `xi_j^{MSMR}=1-x_j/X_j`를 여집합으로 정의한다. 그러면 Ch1의 `xi_eq=1/(1+exp[-sigma_d(V-U)/w])`에 맞는 것은 `f=+sigma_d`다. map은 점유형 지수 `+f(...)`를 Ch1의 여집합 지수 `-sigma_d(...)`와 직접 맞대어 `f=-sigma_d`를 얻는데, 이는 `theta_MSMR`를 `xi_Ch1`에 대응시킨 것이다.
- 독립 재유도:
  - `theta_MSMR=1/(1+exp[f a])`
  - `xi_MSMR=1-theta_MSMR=1/(1+exp[-f a])`
  - `xi_Ch1=1/(1+exp[-sigma_d a])`
  - 따라서 `xi_MSMR == xi_Ch1`이면 `f=sigma_d`; `f=-sigma_d`이면 `xi_MSMR=1/(1+exp[+sigma_d a])=theta_Ch1`가 된다.
- 수정안: `x_j/X_j`가 리튬화 조성이라는 현재 정의를 유지한다면 `eq:lco-msmrmap`의 방향 대응은 `f \leftrightarrow \sigma_d`로 재심해야 한다. 반대로 `f=-sigma_d`를 보존하려면 `x_j/X_j`가 Ch1의 `xi`가 아니라 반대 방향 점유형이라는 한정과 peak 절대값만 동형이라는 제한을 명시하고, “진행 방향이 일관되게 맞춰진다”는 문장은 삭제/수정해야 한다.
- draft 대조: F1/O2/C2_s3도 이 부호를 계승했다. 이는 체리픽 누락이 아니라 여러 draft가 공유한 blind spot이다. F1의 MSMR 귀속 정정(F1 draft L497-L500 상당)을 §8로 미룬 것도 본문 §5의 부호 해석을 더 취약하게 만든다.

### [HIGH/GATE] F-2 방향 슬롯은 “10차 후 별도 커밋” 후보가 아니라 LCO 편입 게이트임

- 위치: map L621-L630, L660; Ch1 L203-L208, L309-L315, L1893-L1898; 코드 L619-L620, L648-L649.
- 무엇이 문제인가: Ch1 원문은 `sigma_d=+1`을 방전으로 정의하지만, 동시에 signcheck에서는 `sigma_d=+1`일 때 `V up -> xi up`, 즉 탈리튬화 진행을 기준 명제로 둔다. LCO 원문 L310-L315는 방전=리튬화, 충전=탈리튬화라고 명시한다. 따라서 LCO에 셀 라벨 그대로 `sigma_d`를 넣으면 branch/tail/polarization의 물리 방향이 어긋난다는 F-2 지적은 선택적 개선이 아니라 적용 규칙의 전제다.
- 삽입 정합 근거: map 본문 §2/§3/§5는 F-2 본문을 제외해 “중립”이라고 하지만, 실제 식들은 계속 `sigma_d`를 입력으로 받는다. 코드 주석도 현재 LCO에서 방전 `sigma_d=+1`을 리튬화로 쓰며 “뒤집지 않는다”고 되어 있어, 문서 편입 뒤 P4 구현 경로가 곧바로 같은 모순을 밟는다.
- 수정안: F-2를 §8 후속 후보가 아니라 LCO supplement 편입 gate로 승격한다. 최소한 finalizer 체크리스트에 “LCO 호출 시 `sigma_d`는 셀 라벨이 아니라 탈리튬화 여부 기준으로 공급해야 하며, 이 한정 없이는 §2/§3/§5 적용 금지”를 넣어야 한다.

## 물리 소당성 루프

- §1 center: `Delta G=-FU`, `Delta G=Delta H-TDelta S`로부터 `U=(-Delta H+TDelta S)/F`, `dU/dT=Delta S/F`는 부호·차원 PASS. `+0.83 mV/K -> +80.08 J/(mol K)` 수치 PASS. 다온도 전자항 적분 한정도 `eq:U1T2`와 정합.
- §2 hys: spinodal `u=sqrt(1-2RT/Omega)`, gap `2/F[Omega u-2RT artanh u]`, `Omega -> 2RT+`에서 `8RT/(3F)u^3` PASS. `2RT@298.15K=4957.9 J/mol` PASS.
- §3 peak: `d xi/dz=xi(1-xi)`, `|d xi/dV|=xi(1-xi)/w`, 높이 `Q/4w`, 면적 `Q` PASS. 다만 방향 슬롯 한정은 위 F-2 gate에 종속.
- §4 decomp: 분배함수 가법성 자체는 PASS. config 내부항 부호는 수식상 `+R ln[xi/(1-xi)]`가 맞으므로 F-1 원자 결합 없이는 FAIL.
- §5 code/MSMR: 전자항 수치 `-(pi^2/3)R(kBT/eV)(13/0.05)/4=-45.68 J/(mol K)` 및 `46/F*30K=14.3 mV` PASS. MSMR `f` 대응은 FAIL.
- §6 H-2: keybox의 단상 한정, 두-상 폭의 값/함수형 분리, srcbox 조건부 검증 문안은 C4 note의 구조적 모순을 대체로 줄인다. 단, 이 항도 실제 코드의 `w_j(T)=n_jRT/F` 고정 함수형과 “현상학적 자유 폭”의 의미를 계속 분리해 읽어야 한다.

## 삽입·라벨 정합

- Ch1/Ch2 실측 줄수: Ch1 1964, Ch2 755. map L5의 1964/755가 현재 파일 기준 맞다. base prompt 괄호의 1965/756과는 1줄 차이.
- 기존 `eq:lco-*` 정의는 Ch1 L487 `eq:lco-dUdT`, L1723 `eq:lco-decomp` 2개뿐임을 확인.
- `eq:lco-dUdT` 참조 6곳, 교체 후 잔존 5곳이라는 map 판단은 정합.
- `eq:lco-decomp` 참조 9곳이라는 map 판단은 정합.
- `eq:msmr` 정의/참조 위치도 map 판단과 정합.
- 신설 라벨 충돌 자체는 발견하지 못했다. 문제는 라벨이 아니라 §4 부호 원자성 및 §5 방향 대응이다.

## G-derive/follow 판정

- G-derive는 center/hys/peak/H-2에서 대체로 PASS다.
- FAIL 지점은 MSMR이다. “정규화 -> 여집합 -> Ch1 xi” 사슬을 쓴다고 선언했지만 실제 부호 비교는 점유형을 여집합형에 직접 맞댄다. 학부 수준 logistic 보수관계에서 드러나는 부호 flip이므로 전보체가 아니라 실제 수학 결함으로 본다.

## 가장 약한 1곳

가장 약한 1곳은 **§5 MSMR `f=-sigma_d` 대응(map L459-L467)**이다. 이유는 (1) map 내부에서 `theta=x_j/X_j`, `xi=1-theta`를 이미 정의해 반증이 한 줄로 가능하고, (2) F1/O2/C계열이 모두 같은 대응을 계승해 독립 draft 수렴으로 방어되지 않으며, (3) 코드 주석까지 같은 부호를 물고 있어 후속 P4 구현으로 전파될 가능성이 크기 때문이다.

## 물리 불변 계약 판정

**위반/조건부 FAIL.** 결과식·수치 대부분은 보존됐지만, `sigma_d` 방향 계약과 MSMR 점유/진행률 대응이 불변 계약을 깨뜨린다. §4도 F-1을 원자적으로 함께 채택하지 않으면 같은 config 항을 두 부호로 동시에 싣게 되어 물리 불변 계약 위반이다.

## 5줄 요약

1. 빈 통과 아님: §4 config 부호 원자성, §5 MSMR `f` 대응, F-2 방향 슬롯 gate를 BLOCKER/HIGH로 적발.
2. center/hys/peak/H-2의 핵심 대수·차원·수치 검산은 대부분 PASS다.
3. 신설 라벨 충돌은 발견하지 못했지만, 라벨 안전성과 물리 안전성은 별개다.
4. 오적발 가능성: MSMR 외부 원 논문 표기는 별도 실측하지 않았으나, 본 적발은 map 내부 `theta/xi` 정의와 Ch1 `eq:xieq`만으로 성립한다.
5. 편입 권고: §4는 F-1과 원자 결합, §5 MSMR 부호 재심, F-2는 후속 후보가 아니라 LCO 적용 gate로 승격한 뒤 재검수.
