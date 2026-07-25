# refine_b — `lco_omega_b.tex` 개선 노트 (ch1_sec16b_lcoomega Phase-② 정련)

대상 원본: `Claude/docs/v1.0.24/_sections/ch1_sec16b_lcoomega.tex` (비파괴 — 원본 무수정)
산출 사본: `results/comp_R1/refine_b/lco_omega_b.tex`

방침: 5개 boxed/식 라벨과 물리는 불변, 약한 방향(1~4)만 조인다. 값·문턱·회귀 수치 전부 보존.

---

## 변경 사항 (방향별 · why)

### 방향 1 — per-peak Frumkin 커널의 Ω→0 환원을 명시·자기정합화 (핵심 수정)
- **문제**: 커널 식(`eq:lcoomega-kernel`)의 Ω→0 극한이 `... /w_j` 로 적혀 있어, 분모
  `|RT/(ξ(1−ξ))−2Ω|` 와 `eq:lco-eqpeak` 의 폭 `w_j=n_jRT/F` 사이의 관계가 모호(w_j 충돌).
  극한식은 `ξ_{eq,j}` 를, 박스는 `ξ_j` 를 써 좌표 표기도 어긋났다.
- **수정** (박스 내부는 byte-identical 보존, 박스 **밖** arrow-limit + 후속 산문만 교체):
  - 극한 타깃을 `Q_j^cat·ξ_{eq,j}(1−ξ_{eq,j})/w_j^{eq},  w_j^{eq}≡RT/F` 로 명시.
  - 새 산문에서 (i) 박스의 `ξ_j` = 전위 V 의 평형 진행률 `ξ_{eq,j}(V)`(음함수 `V=V_{eq,j}` 근,
    `eq:lco-Veq`)임을 못박아 극한식과 **같은 한 좌표**로 통일 → `ξ`-`θ` 혼선 원천 차단
    ("새 기호 θ 를 들이지 않는다" 문장 명시).
  - (ii) 분모 = 자유에너지 곡률 `∂²g/∂ξ²`[J/mol](`eq:lco-gpp`), 그 역수×F = dξ/dV.
    Ω→0 에서 `dξ_{eq,j}/dV=Fξ(1−ξ)/RT` → **이상용액 Nernst 폭 `w_j^{eq}=RT/F`**, 이는
    현상학 폭 `w_j=n_jRT/F` 의 **n_j=1 지점**임을 명시 → `w_j` vs 분모 충돌 해소.
  - (iii) Ω→0 이면 히스 gap 소멸(`ΔU^{hys}=0`, `eq:lco-dUhys`) → 분기 중심 `U_j^{d}=U_j`
    → `ξ_{eq,j}` 는 중심 `U_j`·폭 `RT/F` 의 순 로지스틱 → `eq:lco-eqpeak` **이상 핵과 정확히
    일치** → "Ω 미지정=0 은 eq:lco-eqpeak 경로로 bit-exact 폴백" 을 도출로 뒷받침.
  - (iv) **폭 슬롯 이중계산 방지**: `w_j^{eq}=RT/F`(열역학 이상)와 두-상 측 관측 폭
    `w_j=n_jRT/F`(현상학, `sec:lco-peak` "폭의 지위")를 별도 층으로 분리 — 커널의 두-상 델타가
    관측 폭을 `w_j` 로 넘긴다고 명시.
- **why**: "cleanly reduces / no notational clash" 요구 충족. 물리(커널 자체)는 그대로, 환원의
  논리적 사슬만 노출.

### 방향 2 — 토글 기본값을 전 구간 OFF(사양)로 정합
- **문제**: 헤더 주석(원본 4~6행)이 `코드 기본 = include_electronic_entropy=True … OFF 는 옵션`
  이라 본문(기본 False)과 **정반대** — 유일한 "default ON" 잔재.
- **수정**: 헤더 주석을 `★토글 기본값 = include_electronic_entropy=False (OFF; 사용자 사양
  "커브 구할 땐 빼고"·브리프 "기본 OFF")` 로 교체. 상온 커브 = 토글 무관 전자항 무영향
  (`U(T_ref)` 불변, ΔH^eff 재기준) 명시, `True(옵션)=v1.0.19/v1.0.23 상시-ON 재현, G1 은 이 ON
  경로로 bit-exact 검증` 로 프레임. 본문·박스·keybox·asset 은 이미 기본 False 라 그대로 유지.
- **회귀**: "default True/ON" 잔재 스캔 0건. 기본 False/OFF 진술 6곳 일관.

### 방향 3 — #7 정정 airtight 보강 (물리 불변)
- 박스 `eq:lcoomega-hash7` 는 byte-identical 보존.
- 산문 보강: (a) "식·값·슬롯 그대로, **읽기(문구)만** 정확화(물리 불변)" 을 문두에 명시,
  (b) `eq:br-vanderven1998-1` **원식(값·구조) 불수정** — "⟺ 질서상 안정" 읽기만 "유효 좌표 볼록성
  상실 = 두-상 문턱" 으로 재독한다고 못박음, (c) config `ΔS`[J/(mol·K)] 와 Ω[J/mol] 의 **차원
  직교** 를 명시하고 charge-order ΔS(값·배정 tier C)를 "→Ω" 로 직접 연결하지 않음 재확인,
  (d) `sec:lco-hys-od` 혼동 가드 "계승"("새 물리가 아니다") 명시.
- 원본의 `(식 …부근)` 을 정확 참조 `(식~\eqref{eq:br-vanderven1998-1})` 로 조임.

### 방향 4 — O3-LCO 온도 의존 tier/미검증 플래그 강화 (나머지 유지)
- warnbox (i) 에 `(tier 없음 --- round-trip 미확정)` 을 추가해 "미검증" 을 tier 언어로 승격.
- 적대 3문 블록 유지(값 불변). Q3 에 `eq:br-vanderven1998-1 원식 불변` 을 한 구절 덧대 방향 3 과
  정합. warnbox (ii)(iii)(iv) 및 R²=0.944≈0.940 진술 3곳 전부 보존.

### 방향 5 — 기존 강점 보존
- `eq:lcoomega-Tref`(ΔH^eff T_ref 동결 유도) · `eq:lcoomega-toggle`(boxed 토글) ·
  `eq:lcoomega-hash7`(#7 박스) = **full-env byte-identical**. `eq:lcoomega-kernel` 은 박스+2계도함수
  부분 byte-identical(극한 tail 만 변경). keybox 첫 문장에 Ω→0 폴백 한 구절만 추가.

---

## Self regression-check

- **refs exist**: 추가·유지 참조 전수 확인.
  - 신규 인용(전부 **내부**, ch2 LCO 마스터가 `\input` 하는 섹션): `eq:lco-Veq`(sec13),
    `eq:lco-dUhys`(sec13), `eq:lco-gpp`(sec13), `eq:lco-eqpeak`(sec16), `sec:lco-peak`(sec16).
  - **외부(\externaldocument{ch1_graphite}) 참조는 원본과 동일한 3개뿐**: `eq:Uj`,
    `eq:gr2l-disc`, `ssec:gr-2L` (각 1회) — 새 외부참조 **0건**. `sec:revheat` 는 원본 기존
    참조 그대로(1회, 미증설).
  - 기타 유지 참조(`eq:dSegate eq:U1T2 eq:lco-decomp eq:lco-dope eq:lco-gxi eq:lco-spinodal
    eq:br-vanderven1998-1 sec:lco-hys sec:lco-hys-od sec:lco-electronic sec:lco-Se
    tab:lco-staging`) 모두 문서 내 정의 존재.
- **default reads OFF**: 헤더/본문/박스/keybox/asset 전 구간 "기본 False=OFF" 일관, "default
  True/ON·OFF 는 옵션" 잔재 grep 0건.
- **braces balanced**: `{`=`}`=246 (주석 제외, `\{`/`\}` 무시). 환경쌍 equation 4/4·cases 1/1·
  warnbox 1/1·keybox 1/1. `\boxed` 3개(kernel·hash7·toggle; Tref 는 원본대로 비-boxed).
- **physics unchanged**: 3 boxed + `eq:lcoomega-Tref` full-env byte-identical(스크립트 대조).
  물리 불변 토큰 보존 — `R^2=0.944`(=4)·`0.940`(=4)·`2RT`(=8)·골깊이 `45.7`·`G1`·`v1.0.19/23`
  개수·값 원본과 동일. 커널의 유일 변경은 박스 **밖** Ω→0 극한 표기(w_j→w_j^{eq}=RT/F)로,
  값이 아닌 표기 명시화.
- **labels**: 자체 라벨 5개(`ssec:lco-omega`·`eq:lcoomega-{kernel,hash7,Tref,toggle}`) 보존, 신규
  라벨 0.
- **범위**: `refine_b/` 밖 파일 무수정(원본 포함). 사본만 생성.

## 미결/판단 유보 (본 정련이 확정하지 않은 것 — 추가 후보)
- `w_j^{eq}` 는 본 소절에서 도입한 표기(라벨 아님). 원한다면 상위 표기표에 등재 검토 = 추가 후보.
- Ω→0 환원의 "bit-exact 폴백" 은 문서 논리(코드가 Ω 미지정 시 eq:lco-eqpeak 경로)를 서술로
  명시한 것 — 구현 대조(코드 게이트)는 R2 소관으로 남김(원본 취지 유지).
