# Phase 057AY — v1.0.24 snapshot·v1.0.25.2 kernel report 관찰

정본일: 2026-07-28
세부 Step: 19.9B
범위: 2 unique documents, 246 physical lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `Claude/docs/v1.0.24.1/results/snapshot_v1024_R0.json`
- `Claude/docs/v1.0.25.2/results/KERNEL_COMPARISON_REPORT_v1025_2.html`

두 파일을 첫 byte부터 EOF까지 검독했다. HTML의 9개 embedded
PNG는 base64 validation, PNG signature·크기·hash 확인 후
전부 렌더해 육안 검사했다. 표 9행은 저장된
`summary_versions.json`과 field별 대조했다. 이 검증은 저장
산출물 내부 정합성 검사이며 fit 재실행은 아니다.

## Whole-file Verification

### v1.0.24 R0 snapshot

- bytes: 37
- physical lines: 1
- SHA-256:
  `d620fc7c67b9448d8a372d77d2738bfcc0e645499e791bdfb5039cabb12da636`
- complete content:
  `snapshot -> ch1_graphite_v1.0.24.tex`
- target exists:
  `Claude/docs/v1.0.24.1/ch1_graphite_v1.0.24.tex`
- target SHA-256:
  `4194958ee9774bdbd617955fe78fc02b0ebb5ab537129b594b2fe75e4c9877c3`

### v1.0.25.2 kernel report

- bytes: 1,858,103
- physical lines: 245
- LF count: 244; final line은 LF 없이 종료
- SHA-256:
  `5bca08e0f94d37a1f8512d71c30e09d788648ba83007082397eb2fdcbe8a6e26`
- table: header 9 cells, data 9행 모두 9 cells
- embedded images: 9 valid PNG, 모두 2,015×702 pixels
- HTML table vs stored summary: 9/9 rows exact match
- embedded image vs external PNG: 9/9 byte hash exact match
- `Claude/results/comp_v26_data/KERNEL_COMPARISON_REPORT.html`과
  v1.0.25.2 배치본은 byte-identical

| 그림 | decoded bytes | SHA-256 |
|---|---:|---|
| graphite regsol-4 | 125,353 | `2fc6239f75c8bc0d7d25f84469841867e88f5d1d659d8e938972144153b2baeb` |
| graphite logistic-7 | 124,058 | `49b5b497f41fb66088f599710ed369f595305f0019a204c5a1117229141fe392` |
| graphite skew-logistic-7 | 131,580 | `d3a96f129e1e3b765a25430ac804c526047cdbffa310b9f4d98961f6f8c8f908` |
| silicon regsol-4 | 190,873 | `99f09d3ba7c071117388a5b7aad4d2d41626de951bca2d69a75944a74d001e88` |
| silicon logistic-7 | 179,759 | `69c4ca78ec14020c0804784da5806139938036d0dd4ba423b9dc2c34f5aa79fe` |
| silicon skew-logistic-7 | 190,796 | `490252633df439722400b9c257149ac93759a1f61e2868dea8098aabc93f900f` |
| blend regsol-8 | 141,289 | `39e01b771da1ac62563f2dc0bf17d3fdbda63f8eea318c35abc4876fbab728d7` |
| blend logistic-14 | 143,386 | `3ad6d1165482d3bdc1aaa47a90e6557085b48d5a8cf1d5d0471fce9bb6271106` |
| blend skew-logistic-14 | 153,050 | `a573fda2b042e873c9b22d0422e10923b64b260c6811e126478dab8c98f4ba1b` |

## Provisional Findings

### INTENT-PROV-0395 — `.json` snapshot은 JSON도 snapshot도 아니다

R0 file은 JSON parser가 첫 문자에서 실패하는 plain-text
pointer 한 줄이다. target path만 있고 target blob, commit,
size, line count, timestamp, schema가 없다.

판정:

- R0의 “snapshot”이라는 명칭은 `MISLABELED_POINTER`.
- 현재 target이 존재하고 v1.0.24와 v1.0.24.1 사본이 같은
  hash라는 사실만 확인된다.
- future snapshot manifest는 valid JSON과 content-addressed
  blob/commit을 가져야 하며 parser validation을 gate로 둔다.

### INTENT-PROV-0396 — kernel report의 표·그림은 저장 산출물과 내부적으로 일치한다

R², BIC, peak/valley RMSE, background, N, parameter count의
9개 table row가 `summary_versions.json`과 일치한다. 9개
embedded figure도 외부 PNG와 byte-identical하다.

판정:

- 보고서를 옮기는 과정에서 수치나 그림이 바뀌지는 않았다는
  `ARTIFACT_CONSISTENCY`는 통과한다.
- 이는 raw data→전처리→optimizer→metric의 독립 재현이나
  물리 해석의 타당성을 보증하지 않는다.

### INTENT-PROV-0397 — 현재 BIC는 강한 순위 신호지만 정식 model evidence로 쓸 수 없다

참조된 fit script는
`n log(RSS/n) + k log(n)`을 사용한다. 그런데 fit target은
isotonic regression, voltage rebinning, Savitzky–Golay
ensemble을 거친 dQ/dV다. 인접 residual은 독립 동일분산
Gaussian이라고 보기 어렵고, raw point count 744/528/1,280을
그대로 effective sample size로 쓰면 BIC 차이를 과대평가할 수
있다.

판정:

- reported BIC ordering은 `PRESERVE_AS_CALIBRATION_SIGNAL`.
- covariance-aware likelihood, effective degrees of freedom,
  extraction uncertainty, held-out predictive score 없이
  Bayes evidence나 기작 선택으로 해석하는 것은 `REJECT`.
- bootstrap은 cell/protocol 단위와 preprocessing까지 포함해야
  한다.

### INTENT-PROV-0398 — A 대 B 비교는 kernel만의 비교가 아니다

A는 graphite/Si 4개, blend 8개 transition을 쓰고 B·C는
각각 7개와 14개를 쓴다. BIC가 parameter count 벌점을 주더라도
kernel family와 basis resolution이 동시에 바뀐다.

판정:

- “regsol 4개가 gallery 7개를 대체하지 못했다”는 특정
  approximation test로는 보존한다.
- “regular-solution physics가 틀렸다” 또는 “kernel 효과가
  이만큼이다”라는 일반 결론은 이 비교로 식별되지 않는다.
- 같은 parent transition, 같은 heterogeneity representation,
  같은 data hierarchy에서 nested/controlled comparison을
  새로 설계한다.

### INTENT-PROV-0399 — C의 우세는 α의 물리적 식별을 뜻하지 않는다

보고서는 graphite α 7개 중 5개가 upper bound 8 근처에
포화했다고 스스로 밝힌다. 저장 파라미터에는 graphite width
lower bound, blend width upper bound, silicon α 양쪽 bound와
극소 capacity component 등 추가 boundary/degeneracy 신호가
있다. optimizer success, active mask, gradient, Hessian
conditioning, 각 restart 결과, covariance는 저장하지 않았다.

또한 blend에서는 B→C 때 BIC와 valley RMSE는 좋아지지만
peak RMSE는 0.438→0.459로 악화된다. “세 소재 전부 우세”는
BIC에 한정해야 한다.

판정:

- skew basis의 in-sample 표현력은 `EMPIRICAL_SIGNAL`.
- α와 각 component의 U·w·Q를 물리량·상·gallery로 읽는 것은
  `REJECT_AS_NONIDENTIFIED`.
- skew transformation은 area만 보존할 뿐 parent center,
  variance/susceptibility, entropy를 자동 보존하지 않으므로
  thermodynamic kernel에 직접 삽입하지 않는다.

### INTENT-PROV-0400 — 보고서의 protocol 설명은 같은 계보의 검증 기록과 충돌한다

HTML은 세 파일을 모두 “완화 구간 없는 pOCV(C/50)”라고
기술한다. 그러나 v1.0.25 검증은 다음처럼 정정했다.

- `gr.csv`: `gr_A`, `p-ocv`
- `si.csv`: `si_Dhold`, `p-ocvhold`
- `sigr.csv`: source key·protocol 미확정

또 graphite p-ocv와 p-ocvhold 비교 파일은 서로 다른 specimen
UUID다. 따라서 report의 “같은 모델로 protocol만 바꾼 대조”와
잔차를 비평형에 귀속한 문장은 통제된 인과 대조가 아니다.

판정:

- protocol label과 “세 파일 모두” 주장은 `CORRECT_REQUIRED`.
- hold dataset에서 fit이 높았다는 관찰만 보존한다.
- protocol effect, cell effect, preprocessing effect를 분리하지
  않은 비평형 귀속은 `REJECT_AS_UNCONTROLLED`.

### INTENT-PROV-0401 — fitted Ω/RT로 “흑연은 두-상”을 확정한 논리는 성립하지 않는다

`[1.916, 2.027, 2.472, 2.604]`는 비교에서 진 A-regsol
fit의 parameters다. 한 값은 threshold 2 아래이고, 나머지도
boundary uncertainty·transition correspondence·temperature
transfer가 평가되지 않았다. 이 값을 winning C basis나
독립 XRD phase assignment로 이전할 수 없다.

판정:

- regular-solution free energy와 Ω/RT threshold 자체는
  `THEORY_CANDIDATE`.
- 이 fit이 “흑연은 두-상이되 marginal”을 입증했다는 문장은
  `REJECT_AS_OVERCLAIM`.
- phase identity는 diffraction/thermodynamics와
  multi-temperature equilibrium data가 결정하며 curve basis
  component가 결정하지 않는다.

### INTENT-PROV-0402 — report가 제안한 “상 구조와 곡선 표현 분리”는 살리되 단절 모델은 버린다

“transition 수는 phase 수가 아니며 gallery 세분은 곡선 표현
해상도”라는 경고는 현재 사용자 방향과 맞는다. 그러나
“theory=regsol, fitting=unrelated skew logistic”으로 병치하면
문건과 코드가 같은 물리를 공유하지 못한다.

판정:

- physical parent transition과 sub-resolution shape basis를
  구분하는 원칙은 `PRESERVE_AND_STRENGTHEN`.
- shape는 parent free energy에 연결된 heterogeneity/strain/
  composition distribution 또는 명시적 observation model로
  유도한다.
- kinetics와 protocol response는 같은 latent equilibrium
  state 위의 별도 layer로 둔다.

### INTENT-PROV-0403 — 이 비교는 사용자의 최종 validation 범위를 거의 다루지 않는다

데이터는 graphite, silicon, graphite+Si의 single-temperature,
single-rate half-cell curves다. high-voltage doped LCO,
temperature sweep, current sweep, electrode-potential-dependent
barrier, independent cells, out-of-sample prediction은 없다.

판정:

- 현재 report는 room-temperature curve-basis calibration
  artifact다.
- 사용자 연구의 핵심인 저온·정전류 peak lowering/broadening과
  T–I–U dependent barrier를 검증한 것으로 인용하지 않는다.
- doped LCO와 graphite/Si/blend의 multi-condition public-data
  validation을 새 acceptance gate로 둔다.

### INTENT-PROV-0404 — 생성 report는 publication artifact로 재생성이 필요하다

파일에는 doctype, `html`, `head`, `body` tag가 없고 title/style
다음에 fragment가 바로 온다. embedded plots의 한글이 생성
환경의 font 부재로 네모 glyph로 렌더되어 있다. 각 component
curve는 background를 반복 가산해 표시하므로 caption만으로는
분해 합 규약도 명료하지 않다.

판정:

- 수치 보존 여부와 별개로 `REGENERATE_REQUIRED`.
- final report는 schema-valid document, font embedding,
  accessible captions, raw/model/residual/component definition을
  명시해야 한다.

## Direction Recovered

1. machine artifact는 확장자가 아니라 parseability와 content
   address로 검증한다.
2. internal report consistency와 scientific validity를 분리한다.
3. BIC/R²는 correlated processed dQ/dV에 맞는 likelihood와
   holdout 없이는 기작 판정으로 쓰지 않는다.
4. protocol·cell·preprocessing confounding을 제거한다.
5. parent phase, within-parent heterogeneity, kinetics,
   observation을 연결된 계층 모델로 만든다.
6. curve-fit parameter를 phase constant나 activation barrier로
   이전하지 않는다.
7. final acceptance에는 doped high-voltage LCO와 다온도·다전류
   공개 데이터가 필수다.

## Coverage Status

- 이 batch의 2문건, 246행은 `READ`.
- Phase 057 intent queue는 271/271문건,
  57,795/57,795행 전량 `READ`.
- v1.0.24.1–v1.0.25.2 queue는 41/41문건,
  8,923/8,923행 전량 `READ`.

## Next

Step 19.10:
queue–coverage path, blob, physical extent, EOF, contiguous range,
duplicate representative, status count, idempotence를 독립
검증해 읽기 누락이 0인지 판정한다. 이 gate 전에는 Phase 057을
`PASS`로 올리지 않는다.
