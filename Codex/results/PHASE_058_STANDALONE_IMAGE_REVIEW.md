# Phase 058 standalone image 원해상도 감사

정본일: 2026-07-28
범위: v1.0.10–v1.0.13의 unique standalone PNG 8개
기계 근거:
`Codex/results/PHASE_058_STANDALONE_IMAGE_AUDIT.json`

## 절차와 범위

8개 PNG를 축소 contact sheet가 아니라 저장된 원해상도로 각각 열어
axis, unit, legend, temperature/current condition, sign/direction,
peak morphology와 glyph를 시각 검독했다. 동시에 PNG·generator의
SHA-256, 크기, mode, content bounding box와 pairwise pixel 관계를
기계 기록했다.

8/8 파일과 대응 generator가 존재했고, 8개는 모두 서로 다른 blob이며
비어 있지 않았다. 이 검사는 저장 그림의 전달 상태와 그림이 실제로
보이는 주장을 처분하는 단계다. 그림을 만들었다는 사실을 외부 실험
검증으로 세지 않는다.

## 파일별 판정

### v1.0.10 sample test

`Claude/docs/v1.0.10/figs/Anode_Fit_v1.0.10_sample_test.png`

- 축과 범례는 읽을 수 있다.
- fitted \(n=0.12\)는 네 staging peak를 분리하지만, 이는 fitting
  flexibility의 예시이지 \(n=0.12\)의 물리 유도 또는 물성 검증이
  아니다.
- LCO 0.02 C, 0.05 C, 0.2 C 곡선은 거의 겹친다. 전류 증가에 따른
  peak-height 감소와 broadening의 증거가 아니다.
- `physical anchor`와 `code tier-C demo`를 한 그림에 표시하지만,
  anchor라는 범례 자체가 독립 실험 근거를 제공하지 않는다.
- LCO의 `discharge` 표기는 v1.0.13에서 고친 delithiation mapping과
  맞지 않는 이전 방향 표기다.

### v1.0.10 P4 LCO/heat validation

`Claude/docs/v1.0.10/figs/P4_lco_heat_validation.png`

- graphite rate 곡선은 주로 전압 이동으로 보이며 명료한 peak-height
  저하·폭 증가를 입증하지 않는다.
- LCO rate 곡선은 사실상 겹친다.
- reversible-heat panel은 graphite의 약 0–0.34 V 구간과 LCO의
  약 3.75–4.15 V 구간을 한 가로축에 놓아 가운데 큰 빈 구간이 생긴다.
  수치 부호를 볼 수는 있으나 직접적인 전극 간 형태 비교에는 부적합하다.
- LCO `discharge` 방향 표기는 이후 v1.0.13의 수정과 맞지 않는다.

### v1.0.10 P5 graph suite

`Claude/docs/v1.0.10/figs/P5_graph_suite.png`

- 여러 제목과 범례의 한글이 사각형 tofu glyph로 깨져 있다.
- V2 round-trip은 같은 구현에서 계산한 정방향·역방향 관계의 내부
  항등 확인이다. 독립 열역학 검증이 아니다.
- V5는 저온에서 더 높고 좁은 평형 peak를 보인다. 사용자가 관측한
  유한전류·저온 조건의 peak 저하와 broadening을 설명하는 그림이 아니다.
- V7은 \(T^2\) 전자항을 향후 항목으로 남긴 상태다.
- V9의 면적비 0.9790은 그림에 출력될 뿐 test tolerance로 gate되지
  않는다.
- V1 LCO 방향 표기는 이후 수정 전 convention이다.

### v1.0.10 dQ/dV overview

`Claude/docs/v1.0.10/figs/anode_fit_v1_0_10_dqdv.png`

- 축과 곡선은 읽을 수 있다.
- panel 3 제목은 `kinetic tail + hysteresis`라고 하지만 저장 default에서
  해당 항들이 실질적으로 활성화되지 않는다. 보이는 작은 차이를
  kinetics+hysteresis의 검증으로 읽으면 안 된다.
- 온도 panel은 저온에서 높고 좁아지는 평형 경향을 보이며 사용자의
  핵심 유한전류 관측과 반대 방향이다.
- 표시된 약 0.47의 유한 창 면적은 전체 capacity conservation gate가
  아니다.

### v1.0.12 sample test

`Claude/docs/v1.0.12/sample_test_v1012.png`

- 축, 단위와 범례는 읽을 수 있고 dQ/dV 정규화를
  `[Q_cell/V]`로 더 명확히 표시한다.
- LCO rate 곡선은 여전히 거의 겹친다.
- LCO `discharge` 방향 표기는 v1.0.12 guide가 인정한 facade 문제와
  일치하며, 실제 전극 반응 방향 증거로 사용할 수 없다.
- \(x_\mathrm{MIT}=0.50\) code/demo curve와 0.85 physical-anchor
  curve의 병치는 두 값 중 어느 것도 외부 데이터로 검증하지 않는다.

### v1.0.13 P4 LCO/heat validation

`Claude/docs/v1.0.13/figs/P4_lco_heat_validation.png`

- LCO 방향 표기는 `charge = delithiation, s=+1`로 수정됐다.
- LCO rate 곡선은 수정 뒤에도 거의 겹쳐 finite-current broadening을
  보여 주지 않는다.
- panel (c)의 긴 제목이 오른쪽에서 잘려 저장됐다. raster 바깥 edge가
  아니라 subplot/title 배치 안에서 생긴 시각 truncation이므로 단순
  outer-edge 검사로는 잡히지 않는다.
- 서로 멀리 떨어진 graphite/LCO voltage domain을 한 축에 놓은
  reversible-heat panel의 비교 한계가 유지된다.

### v1.0.13 graph suite

`Claude/docs/v1.0.13/figs/graph_suite_v1013.png`

- v1.0.10 P5와 달리 한글 glyph가 정상 렌더된다.
- V1은 같은 delithiation 방향을 graphite half-cell `dis`와
  LCO half-cell `chg`로 구분해 표시한다.
- V2는 여전히 같은 구현의 round-trip identity이고, V9의 0.9790
  면적비는 출력값일 뿐 자동 gate가 아니다.
- V5는 저온에서 더 높고 좁은 평형 peak를 재현한다. 유한전류에서
  저온 peak가 낮아지고 넓어진다는 사용자의 관측은 닫지 못한다.
- V7 제목은 \(T^2\) 항 미구현을 명시한다.

### v1.0.13 sample test

`Claude/docs/v1.0.13/sample_test_v1013.png`

- 축, 단위, 범례와 glyph는 읽을 수 있다.
- LCO 세 rate curve는 거의 겹쳐 전류 의존 peak 저하·broadening을
  검증하지 않는다.
- 같은 v1.0.13의 P4/graph suite가 \(s=+1\) LCO delithiation을
  `charge`로 표시하는 반면 이 그림 범례는 세 곡선을 모두
  `discharge`로 표시한다. 버전 내부 방향 표기가 일관되지 않다.
- reversible-heat 제목의 `cell discharge; graphite: lithiation`은
  full-cell 반응 방향과 half-cell 이름을 혼합한 표기다. public heat
  convention과 electrode-curve convention을 분리하지 않으면 부호를
  오독할 수 있다.
- \(n=0.12\)와 두 MIT 위치의 병치는 여전히 parameter illustration이며
  public experiment와의 fitting validation이 아니다.

## 공통 과학 판정

8개 그림은 모두 저장된 model-generated output이다. raw public
experiment, 측정 protocol, 오차막대, replicate, parameter covariance,
residual 또는 holdout prediction overlay가 없다. 따라서 다음을
입증하지 않는다.

1. 도핑 고전압 LCO의 4.5 V 이상 안정화 또는 phase/oxygen-redox physics
2. Si 단독·graphite/Si blend의 반응·팽창·hysteresis
3. 전류 증가와 저온에서 관측된 dQ/dV peak 저하·broadening
4. 전위·온도·반응 진행도에 따른 전이 barrier의 독립 식별
5. 특정 fitted transition을 graphite/LCO 물리상으로 식별하는 것

graphite의 전류 효과는 주로 \(R_n I\) 이동으로 보이고, default LCO는
rate-invariant다. 온도 그림은 평형 kernel의 저온 고폭·협폭 경향만
보여 준다. 사용자의 출발 관측을 설명하려면 평형 kernel과 별도로
finite-current nonequilibrium population/phase-boundary transport와
measurement protocol을 닫아야 한다.

## Step 28.2 판정

8/8 standalone image의 원해상도 검독과 generator 연결을 완료했다.
판정은 `VISUAL_COMPLETE_SCIENTIFIC_VALIDATION_ABSENT`다.

확인된 전달 결함은 v1.0.10 P5의 한글 tofu와 v1.0.13 P4 panel (c)
제목 truncation이다. 더 중요한 과학 결함은 rate/temperature figure가
사용자의 핵심 현상을 검증하지 않고, LCO 방향 표기가 version 간·
v1.0.13 내부에서도 일관되지 않다는 점이다.

다음 Step 28.3에서 각 PDF/image의 저장 commit과 generator/source
commit을 연결하고, 격리 재실행 산출물과 hash를 대조해 stale artifact
여부를 확정한다.
