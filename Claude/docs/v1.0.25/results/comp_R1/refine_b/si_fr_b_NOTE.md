# si_fr_b.tex — refine_b NOTE (Phase-② competition-cherrypick)

**Target refined:** `../../_sections/ch3v22_sec02b_sifr.tex` (라이브 파일 — **미변경**).
**Output:** `si_fr_b.tex` (비파괴 개선 사본). 원본과 **모든 boxed 식·라벨·cite 동일**, 산문만 명확화.
**Scope discipline:** refine_b/ 밖 어떤 파일도 read-only 로만 접근, 수정 없음.

---

## 개선 방향별 변경 (direction → 무엇을·왜)

### D1. 넓은 폭의 출처 = 다중도 n_j (Ω<2RT 아님) 일관화
문제 방향: "Ω<2RT 가 peak 을 넓게 만든다"는 인상 차단. 실제 물리 = 넓은 폭은 폭 다중도
`n_j>1` (`w_j=n_jRT/F`), 인력 `Ω>0` 는 오히려 폭을 **좁힘** (`w_eff=(RT/F)(1−Ω/2RT)`).
Ω<2RT 는 단일상 **가드**일 뿐.

- **(a)** eq:sifr-width 정규화 값 `[1.45,2.74,1.09]` 을 "정의상 폭 다중도 n_j (w_j=n_jRT/F,
  eq:wbase)"로 명시하고, 넓은 폭의 출처가 **Ω 아니라 n_j** 임을 못박음. 단일상 판정은 폭의
  *크기*가 아니라 *유한-대-델타 대조*가 가른다고 축 분리.
- **(b)** 커널 유도 말미에 "eq:sifr-kernel 의 열척도는 n_j=1 기준이고 넓은 갤러리 폭은 이를
  다중도로 키운 w_j=n_jRT/F(eq:wbase); Ω 는 그 위 날카로움만 바꿈" 한 문장 추가 → n_j 의 자리를 조기 확정.
- **signbox (ii)(iii)+맺음**: (ii) `Ω=0` 폭 `RT/F` 는 "열척도 기준 n_j=1; 넓은 갤러리는 n_jRT/F"
  로 주석. 맺음문을 "Ω 는 **날카로움만** 조율, 넓은 폭 출처는 n_j; Ω<2RT 는 넓히는 손잡이가 아니라
  단일상 가드이고 경계 Ω→2RT⁻ 는 오히려 **좁힘**"으로 강화.
- **(c)** "폭의 출처(정밀)" 단락을 airtight 재작성: 관측 정규화값 = *(유효) 다중도*; 인력 Ω>0 는
  `(1−Ω/2RT)` 축소(§width 첫째 지위와 동일)로 좁히므로 **바탕 n_j 는 관측값 이상** → "≳1 넓이를
  지는 것은 어느 경우에도 Ω 가 아니라 n_j". Ω<2RT = 단일상 가드(넓힘 손잡이 아님, 경계는 좁힘) 재확인.
- **적대 (1)(3)·keybox**: (1)에 "유한 폭의 *크기*는 n_j 가 정하지 Ω 아님" 반절 추가. (3)의
  "**폭 조율**" 표현을 "**날카로움(peakedness)** 자유도"로 교체(+"모양 손잡이이지 넓은 폭 출처 아님,
  넓은 폭=n_j, 인력 Ω>0 는 좁힘"). keybox 에 "넓은 폭=n_j, Ω 는 날카로움만; 인력 Ω>0 는 넓히지 않고 좁힘".

수치 확인: `w_eff/(RT/F)=1−Ω/2RT` → Ω=+0.9RT ⇒ 0.55(좁아짐), Ω=−0.8RT ⇒ 1.40(넓어짐). Ω>0 좁힘 확정.

### D2. 단일 Frumkin 종은 θ=½ 대칭 — 비대칭은 envelope 에서만
문제 방향: "단일 Frumkin 종이 그 자체로 비대칭"이라는 문장이 없도록 차단.

- **(c)** 에 대칭 근거 추가: "분모의 θ(1−θ) 우함수성(θ=½)과 V(θ)−U° 의 기함수성 때문에 각 단일
  종은 중심 V=U° 에 **대칭이라 그 자체로는 비대칭이 될 수 없고**, 케이스별 비대칭은 **오직** 폭이
  다른 여러 종의 envelope 에서만 온다."
- **적대 (3)** 원문("단일 종 θ=½ 대칭, 비대칭은 envelope")을 "그 자체로는 **결코 비대칭이 아니며**
  … **오직** … envelope **에서만**"으로 강화. logistic 도 "대칭 종" 명시.
- **keybox** 한 줄 추가로 3중 커버.

수치 검증: Frumkin peak 을 V 축에서 U° 대칭 검사 → max rel-diff ~1e-16 (기계정밀), 정점 θ=½·
높이 QF/(4RT−2Ω) 확인. 대칭 주장은 asserted 아니라 유도·검증됨.

### D3. Honest-limit airtight
- **(i)** Ω_Si 를 "물리가 확정 = 단일상(Ω<2RT)뿐; 시드는 그 안에서 인력 쪽 `0.2RT≲Ω<2RT`(바닥
  δ-물리캡, 천장 단일상 문턱), 점값은 피팅 위임"으로 부호·범위·비-점식별을 명료화 ((c)의 인력 Ω>0 과 정합).
  물리가 sign 을 강제한다고 과장하지 않고 "시드 선택"으로 정직 표기.
- **(ii)** 폭 `[1.45,2.74,1.09]` 에 **tier-B** 라벨을 명시(§(a)와 일치)하고 "n_j 의 관측 추정일 뿐
  Ω 의 문헌값 아님"으로 D1 과 교차 강화.
- **(v)** "Ω>2RT 는 단일상 가드 Ω<2RT 를 넘겨 커널 유효범위 밖 → 현상학 broadening(§width 둘째 지위)"
  로 가드-경계 연결 문구 보강(차원 정합 검산은 원문 유지).
- **c-Li₁₅Si₄**(유일 두-상, 1차 한정, 순환 a-Si 부재)는 (c)·keybox 에 원문 그대로 보존·검증.

### D4. 강점 보존 (변경 없음)
- boxed **eq:sifr-kernel**, eq:sifr-V, eq:sifr-dVdtheta, eq:sifr-blend, eq:sifr-width →
  **5식 전부 byte-identical**.
- **Ω→0 로지스틱 폴백(bit-exact)** 문장 보존(적대 3 의 "미지정 시 bit-exact 회수"도 유지).
- **블렌드 가산중첩 box**(eq:sifr-blend, 공통-μ, tu_blend2024·verbrugge_lisi2016) 보존.
- **ω-형 verbrugge2017 대응**(honest-limit iv) 보존.

---

## Self regression-check

| 항목 | 결과 |
|---|---|
| 원본 5식 byte 동일 (eq:sifr-width/V/dVdtheta/kernel/blend) | ✅ IDENTICAL (5/5) |
| `\begin`/`\end` 매칭 (equation 5/5, signbox·warnbox·keybox 1/1) | ✅ |
| 중괄호 균형 (`\{`,`\}` 제외) | ✅ 227/227 |
| `\boxed` 개수 (kernel + blend) | ✅ 2 |
| inline `$` 개수 짝수 | ✅ 342 |
| 정의 라벨 = 자체 것뿐 (ssec:si-fr + eq:sifr-*) | ✅ 6개, 신규 발명 라벨 무 |
| 참조 ref 존재성 | ✅ 전부 존재 |
| 원본 대비 **추가 ref** | `eq:wbase` 1개만 (ch1_sec05_width.tex:269 존재 확인) |
| 원본 대비 ref 삭제 / cite 추가·삭제 | ✅ 없음 (cite 7개 원본과 동일; 신규 발명 cite 무) |
| 물리 변경 여부 | ❌ 없음 — boxed 식 불변, 산문 명확화만 |
| Direction-1 위반 문장(Ω<2RT→wide) | ✅ 0 (다수 문장이 명시적으로 부정; 넓은 폭=n_j) |
| Direction-2 위반 문장(단일 종 비대칭) | ✅ 0 (§c·적대3·keybox 3중으로 단일 종 대칭 명시) |
| refine_b/ 밖 파일 수정 | ✅ 없음 (라이브 원본 미변경) |

참조 ref 전체(존재 확인): eq:eqpeak, eq:xieq, eq:wbase, eq:lco-Veq(원본 계승),
eq:sifr-{width,V,dVdtheta,kernel,blend}(자체), sec:{si-cases,width,si-blend},
ssec:{si-fr,si-blend-gs2}, tab:si-cases, fig:si-cases-shape, eq:blend-dqdv.
cite 전체: chevrier_dahn2009, artrith2018, obrovac_christensen2004, ogata_nmr2014,
tu_blend2024, verbrugge_lisi2016, verbrugge2017 (artrith2018·verbrugge2017 은 ch3v22_bib 등재 확인).
