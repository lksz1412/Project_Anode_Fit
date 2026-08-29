# Phase 064 Step 65 Literature Authority Result

정본일: 2026-08-29

Status: `PASS_PENDING_PERSISTENCE_WITH_GROUND_NOT_FOUND`

Gate: `PASS_P064_STEP65_LITERATURE_BOUNDED_GNF`

Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`

Expected parent: `fd8e192f031bb302933d925ceb9ba599a7975837`

Expected subject: `audit(phase064): bound v1023 literature authority`

Postcommit persistence terminal: `PASS_P064_STEP65_PERSISTENCE`

Phase ceiling after this Step: `CONDITIONAL_P064`

## 1. 결론

Step 65는 JCP 147 적용 논문과 Ref. 6의 원문 권위를 닫았고 Ref. 7은 정확한 서지 identity와 DOI까지 확인했지만 원문 raw bytes를 합법 경로에서 확보하지 못했다. 따라서 다음을 구분한다.

- JCP 147: local AIP Version of Record (VOR) `10/10`쪽 전문 검독 완료.
- Ref. 6: AIP 공식 CDN VOR `4/4`쪽 전문 검독 완료.
- Ref. 7: official bibliographic metadata identity만 확인, original full-text method-content authority는 `GROUND_NOT_FOUND`.
- 오래된 Ref. 7 DOI `10.1063/1.4802005`: 다른 논문으로 확정되어 Ref. 7에 사용 금지.

따라서 JCP 147 Eq. 32→33→34→35–38→39의 적용 논리는 원문에서 확인됐고, ratio/reference substitution의 원 유도는 Ref. 6 Eqs. 9–13 범위에서 직접 확인됐다. 단 Eq. 32는 Eqs. 19–20의 critical orientation-averaging approximations에서 유도된 체계 안의 적분방정식이며 원 문제에 대한 무조건 exact 식이 아니다. Ref. 7의 확장 유도는 원문 미확보이므로 기존 v1.0.23 annotation을 원문 확인 완료로 취급할 수 없다. 본 Step의 PASS는 문헌 경계와 GNF routing이 닫혔다는 뜻이지 Phase 064의 무조건 PASS가 아니다.

## 2. 복구 및 저장소 경계

- active branch: `codex/anode-fit-v1025_2-canonical-completion`.
- Step 64 containing commit: `fd8e192f031bb302933d925ceb9ba599a7975837`.
- Step 64 subject: `audit(phase064): freeze v1023 source process topology`.
- Step 64 persistence: Python 3.12와 3.14 모두 `PASS_P064_STEP64_PERSISTENCE`.
- frozen v1.0.23 baseline: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`.
- protected branch local/tracking/live: `fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71`.
- main tracking/live: `4069cb36a8a52b1b88c29d68aa54dcbe915b1618`.
- `Claude/**` tracked/staged/untracked mutation: `0/0/0`.
- 외부 논문 원문은 저장소 밖 disposable temporary directory에서만 읽었고 Git 추적 대상으로 추가하지 않았다.

## 3. 실제 원천과 전문 검독 범위

### 3.1 JCP 147 적용 논문

- path: `Claude/JCP_147(14)_144111_(2017) - Effects of external electric field.pdf`.
- Git blob: `4fbe2b91b2b3f62cea76feb4272b1e3275dab986`.
- raw SHA-256: `47c7c415093bf5e3ee78215d6efa9141e4cd574e74e206cd9e3e863c5da85bd9`.
- bytes/pages: `2,075,558 / 10`.
- PDF 1.4, unencrypted.
- controller: Poppler 150 dpi render, `10/10`쪽 원해상도 시각 재검독.
- independent reader Kierkegaard: Poppler 180 dpi render, `10/10`쪽 시각 검독.
- render failure, blank page, clipping, overlap, broken equation glyph: `0/0/0/0/0`.
- Poppler의 Symbol/ArialUnicode display-font warning은 있었으나 PDF page image에서 실제 glyph 누락은 발견하지 못했다.

보조 extract `Claude/jcp_extract.txt`는 `69,524` bytes, `725` physical lines, blob `2588ac5da0e9ce4c25141f302a1e33e460ff7966`, raw SHA-256 `cfd8e9f86c2e7937fc648971d455a6a1cd2fb4da4cc5ced48b50f5826f11e6e9`다. 이 파일은 strict UTF-8이 아니며 ISO-8859-1-compatible high bytes와 수식 glyph 손실이 있으므로 위치·prose cross-check에만 사용했다. 수식 판독은 PDF 원문을 우선했다.

페이지 대응은 PDF `1→extract 1–9`, `2→10–69`, `3→70–173`, `4→174–274`, `5→275–388`, `6→389–468`, `7→469–530`, `8→531–614`, `9→615–686`, `10→687–725`다.

### 3.2 Ref. 6 원문

- DOI: `10.1063/1.3565476`.
- official VOR: `https://aipp.silverchair-cdn.com/aipp/content_public/journal/jcp/134/12/10.1063_1.3565476/4/121102_1_online.pdf`.
- raw SHA-256: `c0f2dbefa26731581235da28477f19f07f81f1e897523f6144e272f6b0959460`.
- bytes/pages: `258,112 / 4`.
- HTTP `200`, media type `application/pdf`, PDF 1.3, unencrypted.
- controller: Poppler 180 dpi render, `4/4`쪽 시각 검독.
- independent reader Leibniz: VOR PDF `4/4`쪽 및 official full HTML `1–974` lines 검독.
- render failure, blank page, clipping, overlap, broken equation glyph: `0/0/0/0/0`.
- 접근 시점에 AIP 공식 CDN에서 무료 원문 다운로드가 가능했으나 Crossref/OpenAlex에 명시적 reuse license는 없고 PDF는 AIP copyright를 표시한다. `full-text access`와 `open reuse license`를 합치지 않는다.

Ref. 6에서 직접 확인한 method chain은 다음과 같다.

1. Eq. 9: transformed propagator에 대한 Fredholm 제2종 적분방정식.
2. Eq. 10: 통상적 반복 급수이며 큰 Laplace variable에서 발산할 수 있는 경로.
3. Eq. 11: 미지 propagator 자체를 곱해 ratio가 나타나도록 다시 쓴 exact identity.
4. Eq. 12: 아직 exact인 renormalized equation; 미지 propagator ratio를 유지.
5. Eq. 12 다음 문단: 미지 ratio를 적절한 근사 propagator의 ratio로 치환.
6. Eq. 13: 그 치환으로 얻은 근사 propagator. 작은 Laplace variable 극한에서 exact하고, 더 높은 차수 reference를 쓰면 개선 가능한 구조.

이 확인은 Ref. 6의 시간/Laplace-domain interacting-pair propagator 문제에 한정된다. JCP 147의 steady-state survival-probability 문제나 graphite voltage-domain Volterra 문제와 literal identity를 만들지 않는다.

### 3.3 Ref. 7 원문

- DOI: `10.1063/1.4802584`.
- AIP, Crossref, PubMed가 title/authors/journal/volume/issue/article number/DOI를 일치 확인했다.
- AIP article은 `Available to Purchase`로 표시했다.
- AIP official PDF route는 CLI에서 HTTP `403` 또는 article-minimal HTML로 귀결됐다.
- SNU S-Space, POSTECH OASIS와 Ewha Pure는 metadata-only였고 PDF/bitstream을 제공하지 않았다.
- OpenAlex는 `oa_status=closed`, repository full text 없음으로 보고했다.
- raw PDF/accepted manuscript SHA-256, page count와 1–EOF/전 페이지 검독: `GROUND_NOT_FOUND`.

PubMed abstract는 discovery cross-check로 열람했지만 이번 machine evidence에는 PubMed response bytes와 bounded abstract slice를 결속하지 않았다. 따라서 Ref. 7의 허용 권위는 official bibliographic metadata identity뿐이며, abstract claim도 equation-level method-content authority도 아니다. JCP 147의 인용 또는 Ref. 6의 원문도 Ref. 7 원문의 대체물이 아니다.

## 4. 서지 판정

### 4.1 JCP 147

Kyusup Lee, Seonghoon Lee, Cheol Ho Choi, Sangyoub Lee, “Effects of external electric field and anisotropic long-range reactivity on charge separation probability,” *The Journal of Chemical Physics* 147(14), 144111 (2017), DOI `10.1063/1.5000882`.

Local VOR, DOI resolver, AIP/Crossref metadata의 identity가 일치한다.

### 4.2 Ref. 6

Sangyoub Lee, Chang Yun Son, Jaeyoung Sung, Song-Ho Chong, “Communication: Propagator for diffusive dynamics of an interacting molecular pair,” *The Journal of Chemical Physics* 134(12), 121102 (2011), DOI `10.1063/1.3565476`.

JCP 147 printed reference list는 title과 DOI 없이 abbreviated citation만 제공한다. Title/DOI는 AIP VOR, Crossref와 PubMed에서 독립 확인했다.

### 4.3 Ref. 7

Chang Yun Son, Jaehoon Kim, Ji-Hyun Kim, Jun Soo Kim, Sangyoub Lee, “An accurate expression for the rates of diffusion-influenced bimolecular reactions with long-range reactivity,” *The Journal of Chemical Physics* 138(16), 164123 (2013), DOI `10.1063/1.4802584`.

JCP 147 printed reference list, adopted bibliography, AIP/Crossref/PubMed identity가 일치한다. 단, method-content original full-text authority는 미확보다.

### 4.4 잘못된 DOI 음성 대조

DOI `10.1063/1.4802005`는 Elisa Frezza, Alberta Ferrarini, Hima Bindu Kolli, Achille Giacometti, Giorgio Cinacchi의 “The isotropic-to-nematic phase transition in hard helices: Theory and simulation,” *J. Chem. Phys.* 138(16), 164906 (2013)로 해석된다. Ref. 7의 title, authors와 article number 어느 것도 맞지 않으므로 `REJECT_AS_REF7_DOI`다.

## 5. JCP 147 Eqs. 19–20 및 32–39 원문 판정

Eqs. 19–20은 printed page `144111-3`, PDF page `4`에 있고 Eqs. 32–39는 printed page `144111-4`, PDF page `5`에 있다. Eqs. 19–20의 critical approximation 문맥은 extract `223–241`, context-locator SHA-256 `d56658f43a8751f0a367441f5eeb05988b38aa9a51450c0190d3a3d29da4c6f0`에 결속한다. 이 근사들은 orientation dependence가 크지 않을 때 방향별 survival probability를 orientation average로 치환하며, Eq. 32는 이 근사계에서 유도된다.

`jcp_extract.txt`는 두 column을 같은 physical line에 섞어 놓으므로 extract hash는 `context_locator_sha256`이며 독립 수식 slice가 아니다. 식별 가능한 수식별 증거는 local VOR raw SHA-256, PDF page, 300 dpi Poppler 26.05.0 RGB crop bbox/pixel box와 raw pixel SHA-256으로 별도 결속했다. ASCII semantic projection hash는 감사 재현용이며 원문 수식 glyph의 hash로 표시하지 않는다.

| Equation | Extract context | PDF bbox points | 300 dpi RGB crop SHA-256 | 역할 |
|---|---:|---|---|---|
| 32 | 277–299 | `[44,76,289,156]` | `9b4bbf896f7d25f30a1ba465942582ee3baf9b002990c5edd8caf97f1fda2a08` | Eqs. 19–20 근사계 내부의 방향 평균 ultimate survival Fredholm 제2종 방정식 |
| 33 | 299–325 | `[44,195,289,265]` | `250261fbd54b8ef41aae5cffc5458dd766a18bcda6b4da55e33df75f1b4c1af3` | Eq. 32 내부의 형식적으로 exact한 inverse 재배열; 미지 ratio가 남음 |
| 34 | 321–340 | `[95,390,289,409]` | `93a60a6ea82c6953ae8be893a80bebe7164f2da8f7521ee43bd551f0ea700924` | 미지 ratio를 contracted delta-sink reference ratio로 치환하는 근사 closure |
| 35 | 339–351 | `[64,468,289,500]` | `e67bd01b9ddcd9648e66e6dbd0ed10488ad6552f3d6a1f708a6d1c62ca54a52b` | actual long-range sink와 contact delta sink의 Boltzmann-weighted integrated reactivity 일치 |
| 36 | 351–359 | `[44,524,289,553]` | `26299e3e157ff4edea2481586d9581cb8765c47bac5d4b20e52babd923fea2da` | Eq. 35에서 orientation-dependent contact reactivity를 풂 |
| 37 | 359–371 | `[44,592,289,630]` | `bee5dcb83848b11197bd0620458656eb27bcc41352d9b11df91e4189f9e26b43` | delta-sink 해를 사용한 reference ratio |
| 38 | 371–378 | `[44,660,289,695]` | `63946340028fd9d4dac21dd6f8853aa536a0291923b02e2c774fba3a90771978` | contracted reactivity 정의 |
| 39 | 277–300 | `[305,76,551,138]` | `2c08f7a419fc83fcd1475519e98db2a91d27096fe03706d71fff1397e18a6b7f` | Eq. 37/38 ratio를 넣은 최종 근사 survival probability |

Eq. 32는 Eqs. 19–20 approximation을 전제로 한 source integral equation이다. Eq. 33은 그 Eq. 32 내부에서 exact rearrangement이지만 Eq. 34가 approximate substitution이므로 Eq. 39는 근사식이다. “formally exact”를 원 문제 전체나 Eq. 39까지 확장하지 않는다.

## 6. 적용 조건과 열화 조건

JCP 147 printed `144111-5`, extract `398–411`, raw slice SHA-256 `a31e6008b0862eda58ad5072c18b18af7f0f6e093a7eb30340ef5853c067390b`에서 저자가 명시한 세 조건은 다음과 같다.

1. anisotropic external electric field가 너무 크지 않을 것.
2. Onsager distance `r_c`가 initial separation `r`보다 클 것.
3. contact inherent reactivity `kappa`가 작을 것.

Eq. 34의 직접 열화 조건은 printed `144111-4`, extract `380–388`, raw slice SHA-256 `9d3c57ad152aa5ca9db8389f8fda03bd467353e5e29e05b979d60315b6a70aca`: reaction zone이 매우 넓어지면 reference-ratio 근사의 정확도가 나빠진다.

수치 비교에서 보고된 stronger anisotropy/field, smaller `r_c`, larger inherent reactivity, larger initial separation에 따른 정확도 저하는 위 조건의 결과 관찰로 분리한다. Eq. 65 단순 sink model의 large-parameter 비물리 거동은 모델 결함이며 Eq. 34 broad-zone 열화와 동일 항목으로 합치지 않는다.

## 7. Adopted bibliography와 stale ledger 경계

- `Claude/docs/v1.0.23/_sections/ch1v22_bib.tex` lines 45–47은 JCP 147/Ref. 6/Ref. 7의 title과 DOI identity를 정확히 적는다.
- line 46의 Ref. 6 원 유도 annotation은 이번 VOR full read로 method-content support를 얻었다.
- line 47의 Ref. 7 확장 유도 annotation은 metadata/abstract 수준만 확인됐으므로 original full-text verified로 승격할 수 없다.
- JCP 147 reference list extract lines `711–714`는 Ref. 6/7 abbreviated identity만 제공하며 title/DOI는 없다.
- `V1023_REFERENCE_LEDGER.md`는 v1.0.22 inherited partial ledger이며 adopted bibliography inventory가 아니다.
- 과거 dossier의 `10.1063/1.4802005`는 음성 대조에서 폐기된다.

## 8. Result-first Human Evidence

아래 strict JSON block은 builder의 self-report가 아니다. controller와 독립 readers의 실제 원문 검독, 공식 metadata/access route 조사와 보수적 authority 판정을 builder가 기계 artifact로 변환하는 입력이다.

<!-- P064_STEP65_HUMAN_EVIDENCE_BEGIN -->
```json
{
  "access_date": "2026-08-29",
  "authority_ceiling": "CONDITIONAL_P064_REF7_ORIGINAL_FULL_TEXT_GROUND_NOT_FOUND",
  "bibliography_sources": {
    "adopted_bibliography": {"path": "Claude/docs/v1.0.23/_sections/ch1v22_bib.tex", "blob_sha1": "3f7d417962fb5fced5b420d5e081b2dcabc901d0", "raw_sha256": "d0dd060fd635dd9fe1c32c872357d4ce85f106866cf8c378906067f85c5fc9d1", "line_interval": [45, 47], "raw_slice_sha256": "88f02551a06f7d2fdb7d700606b8f96c15c2dfdccb5220ff0ed46a98ceb2c7ef"},
    "jcp147_reference_list": {"path": "Claude/jcp_extract.txt", "line_interval": [711, 714], "ref6_slice_sha256": "69d9a62c07726d929ff95702a65560192d1123b713573485836887239c481219", "ref7_slice_sha256": "9b58deba54b319508ae7c95b20e449a2bd4c9a797dad1a52600a8190cc5b3726"}
  },
  "conflicts": [
    {"id": "P064-LIT-CONFLICT-001", "candidate_ref7_doi": "10.1063/1.4802005", "disposition": "REJECT_AS_REF7_DOI", "actual_article_number": "164906", "actual_title": "The isotropic-to-nematic phase transition in hard helices: Theory and simulation", "authoritative_routes": ["https://doi.org/10.1063/1.4802005", "https://pubs.aip.org/aip/jcp/article/138/16/164906/71301/The-isotropic-to-nematic-phase-transition-in-hard", "https://api.crossref.org/works/10.1063%2F1.4802005"]}
  ],
  "equations": [
    {"equation": "32", "pdf_page": 5, "printed_page": "144111-4", "context_interval": [277, 299], "context_locator_sha256": "ab26cc49eab8969516378a38fb4b95772947aeb97e60b8334d4c917d136716fe", "pdf_bbox_points": [44, 76, 289, 156], "pixel_box_300dpi": [183, 316, 1205, 650], "crop_width": 1022, "crop_height": 334, "crop_mode": "RGB", "crop_raw_pixel_sha256": "9b4bbf896f7d25f30a1ba465942582ee3baf9b002990c5edd8caf97f1fda2a08", "semantic_projection": "EQ32|upstream=EQ19_EQ20_orientation_average_approximation|unknown=Wbar_u(r)|operator=fredholm_second_kind|domains=sigma_to_r+r_to_infinity|kernel=chi*radial_sink*boltzmann_weight", "semantic_projection_sha256": "7a8f428a1754e8c34d8e00461ba81c3041164291df7f94eaf15e008e0b591941", "operation": "EXACT_WITHIN_EQ19_EQ20_APPROXIMATED_SYSTEM"},
    {"equation": "33", "pdf_page": 5, "printed_page": "144111-4", "context_interval": [299, 325], "context_locator_sha256": "e6ca93fa04645e684e3169c4159c78664a67271ee4212612cfb8564b3e1e18f4", "pdf_bbox_points": [44, 195, 289, 265], "pixel_box_300dpi": [183, 812, 1205, 1105], "crop_width": 1022, "crop_height": 293, "crop_mode": "RGB", "crop_raw_pixel_sha256": "250261fbd54b8ef41aae5cffc5458dd766a18bcda6b4da55e33df75f1b4c1af3", "semantic_projection": "EQ33|operation=algebraic_rearrangement_of_EQ32_within_EQ19_EQ20_approximated_system|form=inverse_one_plus_two_ratio_integrals|unknown_ratio=Wbar_u(r1)/Wbar_u(r)", "semantic_projection_sha256": "6154097a54b55d4986f75506d94d201bb0bb115511010baebef3036c8fdf2694", "operation": "FORMALLY_EXACT_REARRANGEMENT_WITHIN_EQ32"},
    {"equation": "34", "pdf_page": 5, "printed_page": "144111-4", "context_interval": [321, 340], "context_locator_sha256": "662ed8054ff5c9fa600b03448dad03d7e131965429d182097eb94c006ba50d8e", "pdf_bbox_points": [95, 390, 289, 409], "pixel_box_300dpi": [395, 1625, 1205, 1705], "crop_width": 810, "crop_height": 80, "crop_mode": "RGB", "crop_raw_pixel_sha256": "93a60a6ea82c6953ae8be893a80bebe7164f2da8f7521ee43bd551f0ea700924", "semantic_projection": "EQ34|closure=replace_unknown_ratio|from=Wbar_u(r1)/Wbar_u(r)|to=Wbar_delta_u(r1)/Wbar_delta_u(r)", "semantic_projection_sha256": "b00bae5cbf79cc55c98c756607999df69379ea53c5cb66e72d06057db07b0ab6", "operation": "REFERENCE_RATIO_APPROXIMATION"},
    {"equation": "35", "pdf_page": 5, "printed_page": "144111-4", "context_interval": [339, 351], "context_locator_sha256": "80ee9beb12075836b0d321f9a465c2cd7c9edf5b0c81af8e06b35bfef1ced722", "pdf_bbox_points": [64, 468, 289, 500], "pixel_box_300dpi": [266, 1950, 1205, 2084], "crop_width": 939, "crop_height": 134, "crop_mode": "RGB", "crop_raw_pixel_sha256": "e67bd01b9ddcd9648e66e6dbd0ed10488ad6552f3d6a1f708a6d1c62ca54a52b", "semantic_projection": "EQ35|definition=equal_boltzmann_weighted_integrated_reactivity|contact_sink=delta(r-sigma)*kappa(mu)/(4*pi*sigma^2)|long_range_sink=S_R(r,mu)", "semantic_projection_sha256": "edb4ab6f329c9e3d91e51ff1175f10a389b0a1c7032a6d72603cc2f93df0f510", "operation": "CONTRACTED_REACTIVITY_MATCH"},
    {"equation": "36", "pdf_page": 5, "printed_page": "144111-4", "context_interval": [351, 359], "context_locator_sha256": "c28c7e8fe442b5cb39ad7798c1d56362e816a0cdc408c1273904aea5583192fb", "pdf_bbox_points": [44, 524, 289, 553], "pixel_box_300dpi": [183, 2183, 1205, 2305], "crop_width": 1022, "crop_height": 122, "crop_mode": "RGB", "crop_raw_pixel_sha256": "26299e3e157ff4edea2481586d9581cb8765c47bac5d4b20e52babd923fea2da", "semantic_projection": "EQ36|solves=EQ35_for_kappa(mu)|integral=4*pi*exp(U1(sigma))*integral_0_infinity[r^2*S_R(r,mu)*exp(-U1(r))dr]", "semantic_projection_sha256": "7e2435e0601ec7644f528b942f856046c516c83fd3d5e5d842c69987f60c948d", "operation": "DERIVED_CONTACT_REACTIVITY"},
    {"equation": "37", "pdf_page": 5, "printed_page": "144111-4", "context_interval": [359, 371], "context_locator_sha256": "73966d067e87b847197bff2a443c7d3bba1690bc4a2b754401ce182d51018708", "pdf_bbox_points": [44, 592, 289, 630], "pixel_box_300dpi": [183, 2466, 1205, 2625], "crop_width": 1022, "crop_height": 159, "crop_mode": "RGB", "crop_raw_pixel_sha256": "bee5dcb83848b11197bd0620458656eb27bcc41352d9b11df91e4189f9e26b43", "semantic_projection": "EQ37|approximation=EQ34_with_EQ25|ratio=delta_sink_survival_ratio|parameters=kappa(mu),D,sigma,chi", "semantic_projection_sha256": "224fe0d58fcdfa611a8d5d36f79d3667971671465db7904437af2d14c892a056", "operation": "REFERENCE_RATIO_EVALUATION"},
    {"equation": "38", "pdf_page": 5, "printed_page": "144111-4", "context_interval": [371, 378], "context_locator_sha256": "00efd93d95945d8f9813479b39e7dc00223b6c7ded44eac3b8c4d8a67929122c", "pdf_bbox_points": [44, 660, 289, 695], "pixel_box_300dpi": [183, 2750, 1205, 2896], "crop_width": 1022, "crop_height": 146, "crop_mode": "RGB", "crop_raw_pixel_sha256": "63946340028fd9d4dac21dd6f8853aa536a0291923b02e2c774fba3a90771978", "semantic_projection": "EQ38|definition=Lambda_rx|integral=4*pi*exp(U1(sigma))*integral_0_infinity[r^2*exp(-U1(r))*angular_average(exp(K*r*mu)*S_R(r,mu))dr]", "semantic_projection_sha256": "2c34839ea0f6ab76386ed21c8c4fc76ca68acf5f17dc5cf1f5e544da9721d83b", "operation": "CONTRACTED_REACTIVITY_DEFINITION"},
    {"equation": "39", "pdf_page": 5, "printed_page": "144111-4", "context_interval": [277, 300], "context_locator_sha256": "65eb943abec1e527efa27e8e692632702fd5bff722dae7e7a75df0920c10ae85", "pdf_bbox_points": [305, 76, 551, 138], "pixel_box_300dpi": [1270, 316, 2296, 575], "crop_width": 1026, "crop_height": 259, "crop_mode": "RGB", "crop_raw_pixel_sha256": "2c08f7a419fc83fcd1475519e98db2a91d27096fe03706d71fff1397e18a6b7f", "semantic_projection": "EQ39|result=approximate_orientation_averaged_ultimate_survival|form=inverse_one_plus_two_radial_integrals|uses=chi,Lambda,EQ37_ratio", "semantic_projection_sha256": "12909edebe442070b6a16a5372ae0f13db350c5b1957086671f2787ea320b807", "operation": "APPROXIMATE_CLOSED_EXPRESSION"}
  ],
  "evidence_date": "2026-08-29",
  "evidence_id": "P064-HUMAN-LITERATURE-STEP65-001",
  "jcp147_upstream_approximations": {"equations": ["19", "20"], "pdf_page": 4, "printed_page": "144111-3", "context_interval": [223, 241], "context_locator_sha256": "d56658f43a8751f0a367441f5eeb05988b38aa9a51450c0190d3a3d29da4c6f0", "claim": "direction-resolved survival probabilities are replaced by their orientation average when angular dependence is weak", "downstream_equations": ["21", "22", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39"]},
  "jcp147_conditions": [
    {"id": "JCP147-COND-1", "claim": "anisotropic external electric field is not too large", "pdf_page": 6, "printed_page": "144111-5", "extract_interval": [398, 411]},
    {"id": "JCP147-COND-2", "claim": "Onsager distance r_c is large compared with initial separation r", "pdf_page": 6, "printed_page": "144111-5", "extract_interval": [398, 411]},
    {"id": "JCP147-COND-3", "claim": "contact inherent reactivity kappa is small", "pdf_page": 6, "printed_page": "144111-5", "extract_interval": [398, 411]}
  ],
  "jcp147_degradation": {"id": "JCP147-DEGRADE-1", "claim": "Eq. 34 reference-ratio accuracy worsens when the reaction zone becomes very broad", "pdf_page": 5, "printed_page": "144111-4", "extract_interval": [380, 388], "raw_slice_sha256": "9d3c57ad152aa5ca9db8389f8fda03bd467353e5e29e05b979d60315b6a70aca"},
  "readers": [
    {"reader": "controller", "scope": "JCP147 PDF 10/10; Ref6 official VOR 4/4; official metadata/access routes; integration"},
    {"reader": "Kierkegaard", "scope": "JCP147 PDF 10/10 and extract 1-725"},
    {"reader": "Leibniz", "scope": "Ref6 VOR PDF 4/4, full HTML 1-974 and lawful acquisition routes"},
    {"reader": "Singer", "scope": "Ref7 official metadata, lawful acquisition routes and wrong-DOI negative control"}
  ],
  "sources": [
    {"source_id": "JCP147", "title": "Effects of external electric field and anisotropic long-range reactivity on charge separation probability", "authors": ["Kyusup Lee", "Seonghoon Lee", "Cheol Ho Choi", "Sangyoub Lee"], "journal": "The Journal of Chemical Physics", "volume": "147", "issue": "14", "article_number": "144111", "year": 2017, "doi": "10.1063/1.5000882", "original_full_text_status": "FULL_TEXT_READ", "authority_tier": "PRIMARY_VOR_FULL_TEXT", "raw_sha256": "47c7c415093bf5e3ee78215d6efa9141e4cd574e74e206cd9e3e863c5da85bd9", "bytes": 2075558, "pages": 10, "pages_read": 10, "license_status": "AIP_COPYRIGHT_NO_OPEN_REUSE_LICENSE_ASSERTED", "access_url": "local Git blob plus https://doi.org/10.1063/1.5000882"},
    {"source_id": "REF6", "title": "Communication: Propagator for diffusive dynamics of an interacting molecular pair", "authors": ["Sangyoub Lee", "Chang Yun Son", "Jaeyoung Sung", "Song-Ho Chong"], "journal": "The Journal of Chemical Physics", "volume": "134", "issue": "12", "article_number": "121102", "year": 2011, "doi": "10.1063/1.3565476", "original_full_text_status": "FULL_TEXT_READ", "authority_tier": "PRIMARY_VOR_FULL_TEXT", "raw_sha256": "c0f2dbefa26731581235da28477f19f07f81f1e897523f6144e272f6b0959460", "bytes": 258112, "pages": 4, "pages_read": 4, "license_status": "AIP_COPYRIGHT_REUSE_LICENSE_NOT_LOCATED", "access_url": "https://aipp.silverchair-cdn.com/aipp/content_public/journal/jcp/134/12/10.1063_1.3565476/4/121102_1_online.pdf"},
    {"source_id": "REF7", "title": "An accurate expression for the rates of diffusion-influenced bimolecular reactions with long-range reactivity", "authors": ["Chang Yun Son", "Jaehoon Kim", "Ji-Hyun Kim", "Jun Soo Kim", "Sangyoub Lee"], "journal": "The Journal of Chemical Physics", "volume": "138", "issue": "16", "article_number": "164123", "year": 2013, "doi": "10.1063/1.4802584", "original_full_text_status": "GROUND_NOT_FOUND", "authority_tier": "OFFICIAL_BIBLIOGRAPHIC_METADATA_ONLY", "raw_sha256": null, "bytes": null, "pages": null, "pages_read": 0, "license_status": "CROSSREF_LICENSE_NULL_AIP_PURCHASE_ROUTE", "access_url": "https://pubs.aip.org/aip/jcp/article/138/16/164123/71188/An-accurate-expression-for-the-rates-of-diffusion"}
  ],
  "source_mutation_count": 0
}
```
<!-- P064_STEP65_HUMAN_EVIDENCE_END -->

## 9. 확정·미결·근거 미발견

### 확정

- JCP 147과 Ref. 6의 bibliographic identity와 original full-text method content.
- JCP 147 Eqs. 32–39의 page/equation chain, exact vs approximate operation boundary.
- JCP 147이 명시한 세 applicability condition과 broad reaction-zone degradation condition.
- Ref. 7의 official bibliographic metadata identity `10.1063/1.4802584`.
- `10.1063/1.4802005`는 unrelated paper.

### 미결

- Ref. 7 original full-text equation-level method chain.
- Ref. 7이 Ref. 6의 ratio/reference method를 정확히 어떤 kernel, boundary와 approximation order로 확장하는지.
- graphite voltage-domain Volterra closure에 대한 적용은 Step 66의 독립 재유도 전까지 미승인.

### 근거 미발견

- Ref. 7의 합법 공개 VOR 또는 accepted manuscript raw bytes.
- Ref. 7의 명시적 open reuse license.
- JCP 147/Ref. 6/Ref. 7 방법이 graphite algebraic charge-balance root에 직접 적용된다는 primary-source evidence.

## 10. OPEN acquisition owner

| Item | Status | Owner | Acceptance criterion | Target |
|---|---|---|---|---|
| Ref. 7 original | `OPEN_GROUND_NOT_FOUND` | Phase 064 Step 65 literature acquisition owner, carry to Step 69.1 | DOI `10.1063/1.4802584`에 명시적으로 결속된 AIP VOR 또는 lawful author/institutional accepted manuscript; access/reuse condition; raw SHA-256; page count; 1–EOF와 전 페이지 시각 검독 | Phase 064 Step 69.1 and final Step 69.2 ceiling |

## 11. 검증 결과

- result-first evidence block: saved before machine artifacts.
- builder normal/repeated deterministic reconstruction: `PASS`, `2/2`.
- Python 3.12/3.14 artifact and exact-staged precommit validator: `PASS` in both runtimes.
- named negative controls: `PASS`, `54/54` in both runtimes.
- strict JSON duplicate/nonfinite/truncation controls: `PASS`, `5/5` in both runtimes.
- equation-crop independent rerender/hash controls: `PASS`, `8/8` in both runtimes.
- exact-eight staged/Git boundary: `PASS`; 계획에 고정한 8개 경로 외 staged path 없음.
- independent scientific-source review: `PASS`, final `P0/P1/P2 = 0/0/0`; initial Eq. 32 upstream-approximation, equation-locator wording, Ref. 7 provenance findings were corrected and rechecked.
- independent validator/adversarial review: `PASS`, final `P0/P1/P2 = 0/0/0`; bibliography provenance false-pass and malformed-scalar paths were corrected and reproduced as controlled rejects.
- independent lineage/record review: `PASS`, `P0/P1/P2 = 0/0/0` on the reviewed lineage set; final exact-eight staged-boundary recheck는 precommit gate로 결속됨.
- postcommit persistence: `PENDING_AT_PRECOMMIT_BY_DESIGN`.

## 12. 다음 단계 조건

`PASS_P064_STEP65_PERSISTENCE` 뒤 Step 66으로 진입한다. Step 66은 JCP 147과 Ref. 6에서 확인된 ratio/reference logic을 출발점으로 Fredholm과 voltage-domain Volterra를 별개로 재유도해야 한다. Ref. 7 원문 부재는 숨기지 않고 `CONDITIONAL_P064` ceiling과 OPEN owner로 유지한다.
