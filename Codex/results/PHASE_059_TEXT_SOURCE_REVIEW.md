# Phase 059 Step 33.2 — v1.0.14–v1.0.18.2 text source 전문 검독

정본일: 2026-07-28

범위:

- source paths: 117
- content-addressed unique blobs: 93
- unique text blobs: 63
- unique text lines: 36,641
- contiguous review chunks: 158
- versions: v1.0.14, v1.0.15, v1.0.16, v1.0.17,
  v1.0.18.1, v1.0.18.2

권위 경계:

- 이 결과는 frozen v1.0.14–v1.0.18.2 source를 읽었다는
  coverage gate다.
- 문건의 `PASS`, `완료`, `물리 오류 0`, 내부 round trip,
  그림 생성과 외부 reviewer 판정은 그대로 과학적 권위로 승계하지
  않았다.
- 물리·코드·시험·artifact의 최종 disposition은 Step 33.3 이후
  독립 유도, 실행 probe, PDF/image 검독과 1차 문헌 검증을 거쳐
  확정한다.

## 1. 전문 검독 방법

`PHASE_059_V1014_V1018_2_AUDIT_QUEUE.json`의 각 text record에 대해
다음을 수행했다.

1. representative path의 현재 bytes가 queue의 Git blob SHA와 같은지
   확인했다.
2. UTF-8 decode, byte size, line count와 EOF를 확인했다.
3. queue가 동결한 1–300, 301–600 형식의 연속 chunk가 1행부터 EOF까지
   공백·중복 없이 덮는지 확인했다.
4. v1.0.14의 새 source는 전문을 직접 읽었다.
5. copy-forward 계열은 직전판 전문과 exact text diff를 함께 읽어,
   동일 줄은 직전판의 검독을 계승하고 모든 추가·삭제·변경 줄을
   다시 읽었다. 파일명이 달라도 내용이 같은 경우에는 blob SHA
   동일성으로만 중복을 제거했다.
6. handover나 closing의 요약은 source 전문을 대신하는 근거로 쓰지
   않고, 사용자 의도와 당시 자기보고를 복구하는 별도 evidence로만
   읽었다.

역할별 coverage:

| 역할 | unique text blobs | lines | 판정 |
|---|---:|---:|---|
| theory | 17 | 28,876 | COMPLETE |
| production code | 4 | 3,704 | COMPLETE |
| tests | 12 | 1,254 | COMPLETE |
| demos | 18 | 2,118 | COMPLETE |
| fitting guides | 3 | 339 | COMPLETE |
| result/handover/closing | 8 | 301 | COMPLETE |
| supporting roadmap | 1 | 49 | COMPLETE |
| 합계 | 63 | 36,641 | COMPLETE |

PDF 18개, image 10개와 NPZ 2개는 text coverage에 섞지 않았다.
그것들은 각각 Phase 059 Steps 34.5와 35에서 독립 검독한다.

## 2. 사용자가 원한 작성 방향의 source 내 복구

`CLOSING_v1.0.15.md:9–31,47–51,76–92,101–105`는 다음 원칙을
명시한다.

- 우선순위는 교과서 register, 논문 깊이의 전문성, 수식 주도다.
- 수식을 따라가면 물리·화학 논리를 대부분 복구할 수 있도록
  비약 없는 유도를 제공한다.
- 이론 본문의 렌더링 텍스트에는 작업 단계, 구현 함수명과
  자기보고를 넣지 않는다. 구현 추적은 결과 문건·주석·통제된
  대응 절의 역할이다.
- code-first가 아니라 theory-first이며, 문건·코드는 같은 물리
  계약을 공유해야 한다.
- 대상 base 문건과 코드를 전문 정독한 뒤 작업한다.
- 실제 측정 전위점에서 직접 계산하며 인공 작업 격자와
  재보간을 제거한다.
- 폭의 다온도 확장은 상수 \(n\), per-temperature 진단,
  two-phase의 상수 \(w\), 필요한 경우에만 최소 선형 \(n(T)\)
  순서로 올린다.
- \(n(T)\)를 채택하면
  \(\partial w/\partial T=(R/F)[n(T)+Tn'(T)]\)를 가역열에도
  같은 파라미터로 전파한다.
- 계획, 세부 step, 결과와 ledger를 남기고 자주 commit하여
  compaction 뒤에도 source evidence로 복구한다.

v1.0.17 Ch1은 본문의 “코드 진행”, “현재 코드”, “구현 사전”
표현을 “계산 진행”, “현재 모델”, “대응표”로 바꾸고 구현 대응을
별도 절에 집중시키는 방향으로 정련했다. 이 변화는 사용자의 문건
경계에 맞는 계보 자산이다. 다만 물리 closure를 추가한 변화로
계수하지 않는다.

## 3. version별 source 변화

### 3.1 v1.0.14

v1.0.14는 v1.0.13의 생산 물리 경로를 대체하기보다 문건의
통계역학 유도, LCO 서술, 폭의 지위와 별도 phase-separation
appendix를 정련했다.

appendix는 regular-solution binodal/spinodal, common tangent,
Maxwell construction, nucleation과 Cahn–Hilliard를 독립적으로
전개한다. 그러나 appendix 스스로 production bell closure와
독립인 후속 물리로 남으므로, 존재만으로 two-phase kernel의
정당화가 닫히지 않는다.

appendix v1.0.14–v1.0.16에는 molar free-energy density를
공간 적분하는 차원 혼용이 있었고, v1.0.17이 \(f\)를 volumetric
free-energy density, \(\kappa\)를 J/m, mobility를
\(\mathrm{m^5\,J^{-1}\,s^{-1}}\)로 명시해 차원을 수리했다.

### 3.2 v1.0.15

production code는 인공 균일 작업 격자, resampling과 inverse
interpolation을 제거하고 입력 전위점을 정렬한 뒤 각 구간에서
\(\xi_\mathrm{eq}\)의 선형 변화를 가정하여 지수 기억 커널을
해석적으로 적분한다
(`Anode_Fit_v1.0.15.py:104–154,402–504`).

연속 커널의 정규화와 \(L_V\to0\) 유도 자체는 상수 파라미터 아래
정합하다. 하지만 source 수준에서 다음 계약은 아직 닫히지 않았다.

- history는 시간 좌표가 아니라 정렬된 전위 좌표로 재구성된다.
  따라서 비단조 또는 동일 전위 재방문 trajectory를 표현하지 못한다.
- 첫 점을 평형으로 놓는 초기조건은 관측창 밖의 과거가 충분히
  평형이었다는 경계 가정이다.
- 유한 전위창과 미해상 \(L_V\) guard는 이론의 무한 과거 적분과
  별개인 수치 계약이다.

### 3.3 v1.0.16

선형 \(n(T)=n+n_{T1}(T-T_\mathrm{ref})\)와
\(\partial w/\partial T=(R/F)[n(T)+Tn_{T1}]\)가 code와 Ch1/Ch2에
추가됐다 (`Anode_Fit_v1.0.16.py:294–337`).

대수적 미분은 맞지만 다음을 최종 물리로 승격할 수 없다.

- \(n(T)\)는 미시적 상전이 모형에서 유도된 양이 아니라
  다온도 residual을 줄이기 위한 최소 empirical 확장이다.
- \(n\), \(n_{T1}\), 중심 엔트로피, vibrational/electronic
  온도항 사이의 식별 가능성 검증이 없다.
- `_n_factor`는 `n`과 `w`가 모두 없을 때 \(n=1\)을 반환하지만
  `_dwdT`는 같은 default 경로를 \(0\)으로 처리한다. public
  transition contract 안에서 폭과 폭 미분의 default 의미가
  일치하지 않는다.

### 3.4 v1.0.17과 v1.0.18.1

v1.0.16, v1.0.17과 v1.0.18.1의 production code는 같은 blob이다.
따라서 두 후속판은 새 executable physics가 아니다.

v1.0.17은 theory-only 본문 경계를 정돈했고, v1.0.18.1은 검산
box, 기호 충돌 해소와 표 pagination을 정련했다. 이들은 유용한
교재 편집 자산이지만 독립 물리 검증으로 계수하지 않는다.

### 3.5 v1.0.18.2

Einstein vibrational correction가 optional transition key
`theta_E`로 추가됐다
(`Anode_Fit_v1.0.18.2.py:341–390,662`).

source 수식을 직접 미분한 결과 다음은 내부적으로 맞다.

- 단일 조화 oscillator의 \(S_\mathrm{vib}(T)\)
- 기준온도에서 \(\Delta U_\mathrm{vib}=0\)이 되도록 한
  reference subtraction
- 그 voltage correction의 온도 미분과 entropy correction의
  round trip

그러나 insertion reaction의 vibrational entropy는 일반적으로
product와 reactant phonon spectrum의 차이와 mode multiplicity를
요구한다. 단일 \(\theta_E\), unit amplitude와 고정 부호만으로는
그 반응량을 정의하지 못한다. shipped transition defaults에는
`theta_E`가 없어서 기능은 기본 경로에서 비활성이다. 따라서
ROADMAP의 “구현·검증 완료”는 additive capability의 내부 정합
완료로만 읽고, 물질별 물리 검증 완료로 읽지 않는다.

## 4. 문건 내부에서 발견된 핵심 미해결 계약

### 4.1 two-phase 폭과 configurational entropy

Ch1은 two-phase peak의 잔여 폭 \(w_j\)를 apparent transition
potential의 현상론적 분포라고 명시한다
(`graphite_ica_ch1_v1.0.18.2.tex:1590–1610,1849–1861`).

반면 Ch2는 같은 \(w=nRT/F\)를 이상 격자기체의 분포 폭으로
미분해 peak 내부 configurational entropy로 해석한다. 같은
수치 서식을 공유한다는 사실만으로 두 물리 의미가 같아지지
않는다. 따라서 two-phase 전이에 Ch2의 config 항을 그대로
적용하는 것은 문건 내부의 미해결 모순이다.

### 4.2 local barrier와 실제 production lag

문건의 연구 동기는 온도, 전류와 전극 전위에 따라 상전이
활성화 장벽이 달라지는 것이다. 그러나 production path는
affinity를
\(\min(z_\mathrm{cut}nRT,A_\mathrm{cap}RT)\)로 전이당 고정하고,
깊은-tail 상호작용을 \(\Delta H_a-\chi_d\Omega\)로 흡수한다.
따라서 설명된 local electrode-potential dependence는 실제
평가에서 사라진다.

또한 Eyring \(k_BT/h\) prefactor와 기본 activation parameters가
만드는 \(L_V\)는 일반적인 데이터 간격에서 매우 작다. 실제
가시적 broadening fit은 독립 `L_V` override에 의존하는데,
그 override는 전류와 분리되어 \(I\to0\) 평형 환원을 보장하지
않는다.

### 4.3 LCO 이론과 code

Ch1은 LCO의 MIT gate, composition-dependent electronic entropy,
\(T^2\) center shift와 도핑에 따른 \(\Omega\), 폭과 중심의
분리 슬롯을 전개한다. 그러나 production code는 electronic
entropy를 `x_center`와 \(T_\mathrm{ref}\)에서 평가한 상수
offset으로 동결한다. 문건의 \(V\)-dependent composition gate와
온도 곡률을 구현하지 않는다.

더구나 \(U_1(V,T)\)를 composition gate로 만들면 logistic
인자 안의 중심이 \(V\)에 의존하는 implicit problem이 된다.
그 경우 단순 \(\xi(1-\xi)/w\) 미분식에는
\(\mathrm dU_1/\mathrm dV\) chain rule이 추가되어야 한다.
문건과 code 어느 쪽도 이 고리를 닫지 않는다.

code의 LCO demo 값 3.930/3.880/4.050 V는 theory 표의
약 3.90/4.05/4.17 V anchor와 일치하지 않는다. 문건은 이를
tier-C demo로 고백하지만 round-trip fit이나 공개 데이터
검증은 없다.

고전압 약 4.55 V O3→H1-3는 문건이 명시적으로 범위 밖으로
둔다 (`graphite_ica_ch1_v1.0.18.2.tex:2331–2362`). 사용자가
요구한 도핑 고전압 LCO 데이터 설명은 이 계보에서 달성되지
않았다.

## 5. test와 demo의 실제 coverage

v1.0.14의 test/demo 전문과 이후판의 exact diff를 읽었다.
v1.0.15–v1.0.18.2에서 이 파일들의 계산·assertion 로직은 바뀌지
않고 version string, import path와 output path만 바뀐다.

따라서 다음 새 기능은 동반 test가 없다.

- v1.0.15 pointwise memory의 유한창, 초기조건, traversal와
  nonmonotonic history
- v1.0.16 \(n(T)\), positivity, default derivative와 parameter
  identifiability
- v1.0.18.2 Einstein low/high-temperature limit, reaction-spectrum
  interpretation와 multi-mode amplitude

`sample_test`와 graph suite의 다수 판정은 console report와
finite check이지 physics assertion이 아니다. version-local
golden NPZ에 대한 bit-exact 검사는 해당 golden이 어떤 기준으로
capture됐는지와 독립이지 않다. 특히 deliberate rebaseline은
새 architecture가 옳다는 과학적 검증이 아니라 새 출력을
고정하는 회귀 장치일 수 있다.

## 6. Step 33.2 판정

`PASS_P059_TEXT_COVERAGE`

이 PASS가 뜻하는 것은 다음뿐이다.

- 63/63 unique text blobs와 36,641/36,641 lines를 SHA·EOF가
  고정된 source로 전문 검독했다.
- copy-forward와 실제 변경을 분리했다.
- 사용자의 문건 경계와 작업 규율을 source에서 복구했다.
- 후속 claim/code/test matrix에 넣을 모순과 evidence debt를
  선별했다.

이 PASS는 v1.0.14–v1.0.18.2의 물리적 타당성, 공개 데이터 fit,
PDF 품질, golden 재현이나 최종 계보 승인을 뜻하지 않는다.

다음 단계는 Step 33.3이다. 17 theory blob의 section, equation,
label, definition와 bibliography index를 만들고 v1.0.13→14 및
각 후속판 exact source diff를 content-addressed evidence로 저장한다.
