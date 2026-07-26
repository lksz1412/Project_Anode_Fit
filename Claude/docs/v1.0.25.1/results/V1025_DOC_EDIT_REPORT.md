# V1025_DOC_EDIT_REPORT — 문건(LaTeX) 국소 수정 집행 보고

> 집행: **마스터 세션(Opus 5.0) 직접** — 2026-07-26.
> 사용자 지시 "물리·화학 논리를 건드리는 문건 작업은 Opus 5.0, 나머지는 Opus 4.8" 에 따라
> **T1~T12(물리·화학 서술)** 는 마스터가 직접 편집했고, **T13(데이터 addendum)·T14(버전 문자열)** 은
> Opus 4.8 서브세션이 수행했다(그 보고 = `V1025_T13_T14_REPORT.md`·`V1025_DATA_ADDENDUM.md`).
> 지시서 = `V1025_DOC_CASCADE_TODO.md`, 계획서 = `plans/2026-07-26-v1025-surgical-skew-consistency-plan.md`.

---

## 0. 요약

| 항목 | 값 |
|---|---|
| 편집 파일 | `_sections/*.tex` **15** (마스터) + 마스터 `.tex` **3** + `ARCHIVE_NOTE.md` (4.8 서브) |
| 줄 변화 | `_sections` 합 **+262줄**(삭제 문장 1 · 나머지 전부 추가) — 최종 실측값 |
| 신규 `\label` | **3** — `eq:skewpeak` · `eq:skewapex` · `eq:gr2l-fwhm` (전부 Ch1) |
| 삭제 `\label` | **0** (4 마스터 전건 대조) |
| `\boxed` 식 | 38 → **39** (+1 = `eq:skewpeak`; 삭제 0) |
| 구조 검사 | `STRUCTURE_CHECK: PASS` (라벨 중복 0 · 미해소 ref 0 · cite-undef 0 · env 짝 오류 0) |
| 엄격 검사 | `STRICT CHECK: ALL PASS` (장별 xr 참조 · `$` 패리티 · 중괄호 · 라벨 회귀) |
| doc↔code 감사 | **30건 전건 PASS** |
| 실제 LaTeX 빌드 | ★**미수행** — 이 PC 에 TeX 배포판 부재(§5 한계) |

---

## 1. T1~T12 항목별 판정

### T1 — §6 skew peak 식 신설 ✅ 완료
- **파일**: `_sections/ch1_sec06_eqpeak.tex` (+38), `_sections/ch1_sec05_width.tex` (+8)
- **위치**: `eq:eqpeak` 의 "세 양" 읽기 문단 **직후**, 배경 상자(`bgbox`) **직전**에 삽입. `eq:eqpeak` 은 한 글자도
  수정하지 않았다.
- **신규 식 2개**:
  - `eq:skewpeak`(boxed): $(\dd Q/\dd V)^\eq_j=Q_j(\alpha_j/w_j)[\xi_{\eq,j}]^{\alpha_j}(1-\xi_{\eq,j})$
  - `eq:skewapex`: $V^\ast_j-U_j^{\,d}=\sigma_dw_j\ln\alpha_j$, 높이 $=(Q_j/w_j)[\alpha_j/(\alpha_j+1)]^{\alpha_j+1}$
- **표기 결정(중요)**: TODO 초안은 logistic 을 $\sigma$ 로 적었으나, 본 문건에서 $\sigma_d$ 는 **방향 부호**다
  (`eq:xieq`). 기호 충돌을 피하려고 새 그리스 문자를 도입하지 않고 **기존 $\xi_{\eq,j}$ 를 밑으로 하는 거듭제곱**
  $\xi^{(\alpha)}_{\eq,j}\equiv[\xi_{\eq,j}]^{\alpha_j}$ 로 적었다. 코드의 `sig`/`ksi=sig**alpha` 와 1:1.
- ★**초안에 없던 물리 정정 2건을 반영**(수치 재확인 후):
  1. TODO 초안은 "면적·중심 정의 불변"이라고만 했으나, $\alpha\ne1$ 이면 **정점이 전이 중심에서
     $\sigma_dw_j\ln\alpha_j$ 만큼 밀린다**($w\approx25.7$ mV, $\alpha=2$ → $+17.8$ mV). 중심 $U_j^{\,d}$ 의
     *정의*는 불변이지만 **정점에서 직접 읽을 수 없다** — 이 사실을 `eq:skewapex` 로 명시했다.
     (§6 기존 본문의 "위치 $=$ 중심 $U_j^{\,d}$" 는 $\alpha=1$ 한정이 되므로 그 한정을 밝혔다.)
  2. $\alpha$ 는 **순수 비대칭 손잡이가 아니다** — 반높이 폭이 $\alpha=0.5/1/2/4$ 에서 $4.45/3.53/3.02/2.74\,w$
     로 함께 좁아진다. 따라서 $w_j$($n_j$)와도 축퇴하며, 이 사실이 T3 가드의 근거가 된다.
  3. 아래 `bgbox` 의 감수율 **유도 서식**($\mathrm{var}_j=M_j\theta_j(1-\theta_j)$ 독립-자리 분산)은
     $\alpha=1$ 기준임을 밝혔다($\xi=\sigma^\alpha$ 재모수화는 독립-자리 분산 형태를 보존하지 않으므로).
- **연계**: `sec:width-w` 끝에 "폭과 형상 지수의 분업" 단락 추가 — 폭식 `eq:wbase` 는 불변이고 비대칭은 진행률
  좌표 재모수화에서 온다는 것, 그리고 $\alpha$–$n_j$ 축퇴.
- **자산 앵커**: `% 자산(v1.0.25 C1): [V1025-C1-A …] [V1025-C1-B …]` 2줄 추가. 기존 `% 자산:` 행의
  집계(265개)를 흔들지 않도록 `% 자산(…):` 괄호 형식을 썼다(기존 `% 자산(v1.0.22 SM2):` 선례와 동일).

### T2 — §7 broadening 에 α 추가 축 ✅ 완료
- **파일**: `_sections/ch1_sec07_broadening.tex` (+18)
- **위치 결정**: TODO 는 ① 문단 끝을 지목했으나, ①②③ 열거 사이에 끼우면 "첫째–둘째–셋째" 서사가 끊긴다.
  세 출처와 폭 예산(그림 `fig:widthbudget`)이 **모두 끝난 뒤**, `sec:broadening-scope` 직전에 넣었다.
  번호 ①②③ 는 불변이고 α 는 "(추가 축)" 으로 별도 단락이다.
- **내용**: ① 만 비대칭원이고 ②③ 합성은 좌우 대칭 전제라는 점 → α 는 ② 와 같은 부류(평형 잔여)이면서 좌우를
  가르는 **네 번째 축**. **교란**: ① 과 α 는 정점 이동 방향까지 겹친다(그림의 ① 도 오른쪽으로 민다,
  α>1 도 $+\sigma_dw\ln\alpha$). **분리**: 율속 스윕만이 가른다(① 만 $\propto|I|$). 다율속 없이 α 로 얻은
  비대칭을 "평형 비대칭의 측정"으로 읽지 말라는 정직 단서 포함.

### T3 — §18 식별 가드 ✅ 완료 (초안보다 확장)
- **파일**: `_sections/ch1_sec18_inputs.tex` (+22), `warnbox` 신설
- TODO 초안은 α·$L_V$·gallery **3** 손잡이였는데, T1 에서 α 가 폭도 바꾼다는 것이 확인되어 **$w_j$($n_j$)를
  더한 4 손잡이 축퇴**로 적었다. 각 손잡이가 무엇을 움직이는지 한 줄씩, 권장 스코프(α 열면 $L_V$ 동결 ·
  gallery 세분과 동시 자유화 지양 · α 와 $n_j$ 중 하나만), 원리적 분리(율속 스윕만 ②를 가름 / (1)(3)(4)는
  단일 곡선으로 비유일 → 다온도·다율속 또는 XRD 필요), 그리고 "이 손잡이 값은 곡선 표현 파라미터이지
  상 개수·상 성격의 측정이 아니다".

### T4 — §5b $w_\eff$ "연속화" 정정 ✅ 완료 (초안보다 정량 강화)
- **파일**: `_sections/ch1_sec05b_gr2L.tex` (+39)
- **삭제**: "$w_\eff\to0$ 으로 좁아져 두-상 델타로 수렴한다 --- 이 한 식으로 연속화된다" (계획서 C5 지정).
- **대체**: (i) 중심 **높이** $Q/(4w_\eff)$ 는 **모든 $\lambda$ 에서 정확**한 항등임을 명시.
  (ii) 반높이 폭의 **닫힌형을 유도해 신규 식 `eq:gr2l-fwhm`** 로 넣었다 ---
  $\mathrm{FWHM}=(4RT/F)\,\mathrm{artanh}\,x-(2\Omega/F)x$, $x=\sqrt{\lambda/(1+\lambda)}$, 점근
  $(16/3)(RT/F)\lambda^{3/2}$. (TODO 초안은 "$\lambda^{3/2}$ 스케일" 이라는 서술만 요구했으나 닫힌형을
  주는 편이 사용 가능해서 식으로 승격.)
  (iii) $w_\eff$ 를 폭으로 읽으면 $\approx0.66/\sqrt\lambda$ 배 과대 — $\lambda=10^{-2}/10^{-3}/5\times10^{-4}$
  에서 $6.6/21/30$ 배.
  (iv) 판정자가 $\Omega=2RT$ 를 넘는 순간 평형 등온선은 Maxwell 공존평탄으로 **불연속** 전환이므로
  "연속 보간이 아니다".
- ★**자기 정정 1건**: 초고에 "점근식은 $\lambda\le0.05$ 에서 $1\%$ 이내" 라고 적었는데 doc↔code 감사에서
  실측 $2.97\%$ 로 **FAIL** 이 떴다. 실측값으로 교체 —
  과대율 $\lambda=0.01{:}0.6\%$ · $0.02{:}1.2\%$ · $0.05{:}3.0\%$ · $0.5{:}27\%$, 따라서
  "$\lambda\gtrsim0.02$ 에서는 닫힌형을 쓴다". 재감사 후 PASS.

### T5 — Part T warnbox 를 두-상 폭 한정으로 ✅ 완료
- **파일**: `_sections/ch2_sec05_mixing.tex` (+10)
- 기존 warnbox 의 "쓰지 않는다(재도입 금지)" 를 **삭제하지 않고**, 대상을 "\emph{두-상 봉우리의 폭}" 으로
  좁혔다. 이어 "조준 좁힘(v1.0.25)" 단락으로 **단상 중심 높이 지표 용법은 허용 / 폭 읽기는 여전히 금지 /
  두-상까지의 연속 보간도 금지** 두 가지를 분리 명시. `[C-2]` 자산 행에 조준 변경 병기.

### T6 — Ch3 §3.2b "오직 envelope" 완화 ✅ 완료 + 파생 결함 1건 정정
- **파일**: `_sections/ch3v22_sec02b_sifr.tex` (+36 중 해당분)
- 두 곳(본문 (c) · 세 확인 (3))을 "envelope **또는** skew 지수 $\alpha_j$(상호 대안 · 동시 자유화 시 축퇴)"
  로 완화. 헤더 주석 개선방향 (2) 에 완화 이력 병기(원래 서술이 왜 그렇게 강했는지 보존).
- ★**TODO 에 없던 결함 발견·정정**: 같은 파일 (c) 대목이
  `$w_\mathrm{eff}=(RT/F)(1-\Omega/2RT)<RT/F$` 를 **폭으로** 읽고 있었다 — T4/T5 가 금지한 바로 그 오독이다.
  좁힘의 **방향**은 유지하고 **크기**를 $\lambda$ 로 읽지 말라는 정량 주의를 삽입(높이는 정확 ·
  FWHM 은 $\lambda^{3/2}$, Ch1 `eq:gr2l-fwhm` 참조).
- ★**문장 삭제 1건**(본 버전의 유일한 삭제): 세 확인 (3) 끝의
  "커널 분기가 이 $\Omega$(모양) 자유도 하나를 열되, 미지정 시 로지스틱 폴백으로 bit-exact 회수돼…" —
  **커널 분기가 삭제되어 사실이 아니게 되었으므로** 제거하고, 그 역할을 실제로 담는 것이 $\alpha_j$ 와
  gallery 세분임을 밝혔다. (D-D 의 additive 원칙에 대한 의도적 예외 — 근거 = 거짓 서술 존치 불가.)

### T7 — Ch3 sifr 지위: **코드 삭제** 반영 ✅ 완료
- **파일**: 같은 파일, 절 도입부에 `warnbox` 신설 + (v)·`keybox` 정화
- 사용자 결정(DG-1(b) 삭제)에 맞춰 TODO 의 "강등·코드 존치" 문구를 **"해석적 기록 — 미채택·코드 미구현"**
  으로 바꿔 썼다. 담은 내용: 유도는 유효 물리 / 이득이 전이 수 가정에 종속(+0.97 → −0.53 %p 역전) /
  gallery·α 가 더 적은 가정으로 같은 개형 / 커널 계통 = 로지스틱 단일계 /
  **$\Omega$ 파라미터 지위는 불변**(히스 gap·$\Delta H_a^\eff$·§7 상성격 판정 — 삭제된 것은 커널뿐) /
  재도입 시 새 게이트 필요.
- `eq:sifr-kernel`·`eq:sifr-blend` **식·라벨·boxed 전부 보존**(문건 자산 삭제 금지).
- (v) binodal 구성 서술에 "재구현 시의 명세로 읽되 현행 코드 거동으로 읽지 말 것" 추가.
- `keybox` 의 "$\Omega{=}0$ 로지스틱 폴백(bit-exact)" → "로지스틱 회수"(코드 계약 표현 제거) + 지위 한 줄.

### T8 — 부록 B 코드맵 ✅ 완료
- **파일**: `_sections/ch1_appB_codemap.tex` (+29)
- `tab:symcode`: `$\alpha_j$`(키 `alpha`·`_alpha_factor`) · `$\xi^{(\alpha)}_{\eq,j}$`(`func_dxi_eq(...)[1]`) ·
  `$R,F$`(레거시 기본 ↔ `R_SI`/`F_SI`/`use_si_constants()`) 3행 추가.
- `tab:inputs`: `alpha` 행(기본 부재$=1.0$·tier C·축퇴 경고 G-α4).
- `tab:nodecode`: N6 을 `peak_shape = dxi_eq` 로 갱신(구 인라인과 α=1 에서 부동소수점 동일) ·
  N8 에 `_causal_pad` 사양(5·$L_V$ · 간격 $\le L_V/20$ · 4000점 · 동결·ratio 양 경로).
- 부록 도입부에 "v1.0.25 갱신 요지" 단락 — 추가 4항(전부 additive·미지정 시 bit-exact) 대비 **삭제 1항**
  (regsol 커널 3심볼 + `'kernel'` 분기)을 명시하고, 파일명 유지 규약(DG-2)을 적었다.
- **주의**: `longtable` 본문 안 `\footnote` 는 취약하므로 각주로 쓰지 않고 셀 텍스트로 흡수했다
  (컴파일 불가 환경에서 위험을 만들지 않기 위함).

### T9 — 인과 pad 각주 ✅ 완료
- **파일**: `_sections/ch1_sec09_tail.tex` (+8), `_sections/ch1_appE_selfconsistent.tex` (+5)
- §9: `eq:lag` 규격화 검산 직후 "임의의 평가점 $V$ 마다 그 점 하나의 적분으로 닫힌다" 에 각주 —
  "점별"은 **출력**이 점별이라는 뜻이고 하한은 $-\infty$ 인 이력 적분이므로 격자 시작점 이전 과거가
  누락된다 → 진행방향 과거로 $5L_V$ pad(간격 $\le L_V/20$·상한 4000점) 후 원 격자만 절단.
- ★**수치 정정 1건**: 초고에 "종전 최대 $100\%$ → pad 후 $\le0.005\%$" 라고 적었는데, 게이트 G-창의 **실측**은
  같은 물리점의 세 시작점 상대 산포 **$74.3\%$ → $0.02\%$** 였다. 게이트 실측값으로 교체하고
  pad 길이의 커널 잔여 $e^{-5}\approx0.7\%$ 가 잔차 하한을 준다는 점을 덧붙였다.
- 부록 E: ratio 경로도 **같은** pad 를 쓴다는 것 + **한쪽만 pad 하면 동결극한 정확 회수가 깨진다**는 실제
  경험(동결 경로만 pad 했을 때 자기일관 게이트 동결 회수 실패 → ratio 경로에도 넣어 $\lVert r_1-r_0\rVert=0$
  복구)을 기록.

### T10 — $C_\bg$ 창-국소 상수 근사 ✅ 완료
- **파일**: `_sections/ch1_sec10_sum.tex` (+17 중 해당분)
- `eq:sum` 직후 단락: 상수 $C_\bg$ 는 전역 사실이 아니라 **피팅 창 안에서만** 쓰는 근사 / 실측(4셀·2프로토콜)
  에서 $0.3$–$0.9$ V 단조 감쇠(창 평균의 $\sim$230 %, 셀 간 일치 → 잡음 아님) / 창 넓히면 광폭 종 1개 필요 /
  **그 이득은 조건부**(흑연 단독 투입은 악화, skew α 동반 시에만 개선) / 세 조건(창 명시·창 밖 외삽 금지·
  창 확장 시 α 동반 검토) / 배경의 물리적 출처 분해는 범위 밖.

### T11 — 상수 opt-in 표시값 각주 ✅ 완료
- **파일**: `_sections/ch1_sec10_sum.tex`(각주), `_sections/ch2_sec08_synthesis.tex` (+7),
  `_sections/ch2_appB_codemap.tex` (+2)
- §10 예제의 $w=RT/F=25.693$ mV 가 **CODATA-2018 값**임을 밝히고, 구현 기본(레거시)은 $25.6912$ mV(표시
  $25.691$) 이며 CODATA 는 `use_si_constants()` opt-in 이라는 것, 즉시 교체가 골든 bit-exact 계약과 양립하지
  않는다는 이유를 각주로.
- Part T worked example: $U_\oc(\bar x{=}0.25)$ 를 "$74.4$ mV(raw $74.35$ mV)" 로 병기 + 각주 —
  레거시 raw $74.3511$ / SI $74.3497$($-1.4\,\mu$V $=2\times10^{-5}$ 상대차, 물리적 무의미) 인데 하필
  $74.35$ 반올림 절벽에 걸려 `.1f` 표시가 $74.4\to74.3$ 으로 뒤집힘. 나머지 회귀 기준
  ($-0.204/-0.134/-0.070$ mV/K, $+60.8$ mV)은 두 상수계에서 표시 자리까지 동일(G-SI).
- 부록 B.2 회귀 기준표의 $U_\oc$ 행에 "정합 판정은 **raw 값**으로" 명기.

### T12 — 해상도 사다리에 Si 7-gallery + gallery≠상 ✅ 완료
- **파일**: `_sections/ch1_sec05b_gr2L.tex`, `_sections/ch3v22_sec02_cases.tex` (+11)
- Ch1 사다리: 기존 \{4-전이(기본)·5-feature XRD·6-gallery MSMR\} 에 **7-gallery(Si, opt-in)** 을 더하고,
  그 근거를 실측으로 적었다 — 프로토콜 의존(hold 엔 $0.433/0.456$ V 두 feature, p-ocv 엔 부재) ·
  흑연 검출 봉우리 수 문턱 따라 $3\to4\to5$ · 고해상 적합의 중심 $U$ 는 새 위치가 아니라 기존 세 위치
  ($\approx105/141/227$ mV)에 $\Delta U<12$ mV 근축퇴 쌍 = MSMR 6-gallery 관용과 동일 양상.
  결론: **사다리를 올려도 상은 늘지 않는다**(XRD staging 4 · 물리 두-상 2 불변, 판정은 §7 소관) ·
  gallery 세분과 α 는 상호 대안(동시 자유화 시 축퇴) · **봉우리 수를 상 수의 증거로 제시하지 말 것**.
- Ch3 원소 Si 절: 프로토콜 의존 feature 단락 신설(같은 취지) + 7-gallery opt-in 병존 · 기본 케이스 셋 무변경.

---

## 2. 마스터 반결 — 지시서에 없던 판단 3건

1. **T1 표기**: logistic 을 $\sigma$ 로 적지 않았다(문건의 $\sigma_d$ = 방향 부호와 충돌). 새 문자 도입
   없이 $\xi^{(\alpha)}_{\eq,j}=[\xi_{\eq,j}]^{\alpha_j}$ 로 적었다.
2. **T2 삽입 위치**: ① 문단 뒤가 아니라 세 출처·폭 예산 종료 후. 열거 서사 보존이 이유.
3. **`par:skewpeak` 라벨 미생성**: `\paragraph*`(비번호) 뒤의 `\label` 은 직전 카운터에 붙어 오독을 낳는데
   참조처도 없다. `eq:skewpeak` 만 만들었다. → 신규 라벨은 계획서의 1개가 아니라 **3개**
   (`eq:skewpeak`·`eq:skewapex`·`eq:gr2l-fwhm`)이고, 뒤 둘은 T1/T4 의 정량 정정에 필요해서 승격한 것이다.

### ★ 미해결로 남긴 물리 판단 1건 (사용자 확인 요청)
**"흑연 물리 두-상의 개수"** 표기가 문건 계열 안에서 이미 엇갈려 있고, v1.0.25 에서도 통일하지 않았다.
- `results/comp_v24/GRAPHITE_STAGING_XRD.md` §1 결론 = "XRD 확정 **두-상 4개**(1′↔4 · 3↔2L · 2L↔2 · 2↔1),
  4↔3 만 고용체" — 근거는 Dahn PRB **44**, 9170(1991) 초록 verbatim("모든 전이가 공존, stage 4→3 만 예외").
- 챕터 §7(`sec:broadening-class`, 문건 내 **권위**) = 물리 두-상은 **2개**(2L→2 $=$ LiC₁₂ · 2→1 $=$ LiC₆)이고
  dilute 1′→4 · 4→3 · **3→2L 은 연속 고용체** — 근거는 DFT(Persson 2010: stage 1/2 두-상만 재현) +
  2↔1 plateau 의 $\partial U/\partial T\approx0$ 열역학 서명(Reynier).
- **판단**: 어느 쪽도 내부 모순은 아니다(챕터는 "$\Omega$ 문턱이 확정하지 않는다 → §7 위임" 으로 자기일관).
  그러나 **두 문서가 다른 수를 말하는 것은 사실**이고, 이는 **v1.0.24 부터의 선행 불일치**이지 v1.0.25 가
  만든 것이 아니다. 통일하려면 Dahn 1991 **본문**(초록 아님)의 공존역 판정과 피팅된 $\Omega_j$ 를 함께 봐야
  하므로 이번 국소 수정 범위를 넘는다 → **미해결로 등재**(`V1025_DATA_ADDENDUM.md` M4 와 동일 항목).
  v1.0.25 의 신규 서술은 전부 §7(2개) 기준으로 적었다 — 챕터 내부 정합은 유지된다.

---

## 3. 실행한 검증 (원문 출력)

### 3.1 구조 검사 — `results/tools_check_structure.py check`
```
=== ch1_graphite_v1.0.24.tex (34 files) ===
labels: 266 (dup: 0) []
refs: 1112 (unresolved: 0) []
cites: 139 keys, bibitems: 44 (cite-undef: [], bib-uncited: [])
env pairing errors: 0
asset anchors: 265 tags, unique 265
math env blocks: 146 (boxed: 39)
=== ch2_lco_v1.0.24.tex (13 files) ===
labels: 82 (dup: 0) []   refs: 355 (unresolved: 0) []   env pairing errors: 0   boxed: 16
=== ch3_si_v1.0.24.tex (11 files) ===
labels: 44 (dup: 0) []   refs: 201 (unresolved: 0) []   env pairing errors: 0   boxed: 4
=== appendix_phase_separation.tex (1 files) ===
labels: 30 (dup: 0) []   refs: 41 (unresolved: 0) []    env pairing errors: 0   boxed: 3
STRUCTURE_CHECK: PASS
```
편집 전 baseline 도 PASS 였다(라벨 263 · ref 1064 · boxed 38).

### 3.2 엄격 검사 — `scratchpad/patch/tex_strict_check.py`
이 도구는 위 검사가 **못 잡는 것**을 잡는다. 특히 [A]: 위 도구는 미해소 ref 를 **전 마스터 라벨 합집합**으로
판정하므로 "ch1 이 xr 없이 ch3 라벨을 참조" 하는 실제 빌드 오류를 통과시킨다. [A] 는 각 master 를
**자기 라벨 ∪ 자기가 `\externaldocument` 한 master 의 라벨** 로만 판정한다.
```
[A] 장별 참조 해소 (xr 경로만 허용 — 라벨 합집합 금지)
  ch1_graphite_v1.0.24.tex  refs= 1112  xr=[ch2_lco_v1.0.24.tex]                            미해소=0
  ch2_lco_v1.0.24.tex       refs=  355  xr=[ch1_graphite_v1.0.24.tex]                       미해소=0
  ch3_si_v1.0.24.tex        refs=  201  xr=[ch1_graphite_v1.0.24.tex,ch2_lco_v1.0.24.tex]   미해소=0
  appendix_phase_separation.tex refs= 41  xr=[-]                                            미해소=0

[B~D] 편집 파일 14종 — $ 패리티 불변 · 중괄호 depth=0 초과닫힘=0 · 미확인 매크로 전건 표준(langle/ell/
      textwidth/arabic/roman/resizebox/hbar/…) 또는 tikz 국소(xx/yy/lab/px/py) = 내 편집이 도입한 것 0

[E] 라벨 회귀
  ch1: +['eq:gr2l-fwhm','eq:skewapex','eq:skewpeak']  -[]      ch2: +[] -[]   ch3: +[] -[]   부록: +[] -[]

>>> STRICT CHECK: ALL PASS
```
※ [B] 의 `$` 검사는 **절대 패리티가 아니라 v1.0.24.1 대비 패리티 불변**을 본다 —
`ch1_sec05_width.tex`(617)·`ch1_sec07_broadening.tex`(599)는 **원본에서 이미** 홀수로 세어지는데(tikz 노드·
`\code` 인자 안의 `$` 때문에 생기는 순진한 카운터의 위양성) 원본은 정상 빌드된다. 따라서 판정 기준은
"내 편집이 패리티를 바꾸지 않았는가" 이고, 14종 전건 불변이다.

### 3.3 doc↔code 1:1 감사 — `scratchpad/patch/doc_code_audit.py` (**30/30 PASS**)
문건 v1.0.25 에 새로 쓴 **모든** 수치·거동 주장을 코드로 재현했다. 주요 항목:

| 문건 주장 | 코드 재현 |
|---|---|
| `eq:skewpeak` 의 α=1 이 `eq:eqpeak` 를 부동소수점까지 회수 | `array_equal(func_dxi_eq(α=1), ksi(1−ksi)/w) = True` |
| `func_dxi_eq(...)[1]` $=[\xi_\eq]^\alpha$ | `== sigma**2` (bit 동일) |
| 면적은 α 무관 $=Q$ | α=0.25/0.5/1/2/4 → 0.999–1.000 |
| `eq:skewapex` 정점 이동 $=\sigma_dw\ln\alpha$ | α=0.25/0.5/1: 측정 $-35.6156/-17.8078/0.0000$ vs 예측 동일 |
| `eq:skewapex` 높이 $=(Q/w)[\alpha/(\alpha+1)]^{\alpha+1}$ | 상대오차 $<10^{-9}$ (5개 α 전건) |
| 정점은 $\xi_\eq=\alpha/(\alpha+1)$ | |diff|$<10^{-4}$ |
| 반높이 폭 $4.45/3.53/3.02/2.74\,w$ | 실측 $4.453/3.525/3.015/2.740$ |
| 좌우 반폭비 $0.80/1.00/1.18/1.30$ | 실측 $0.796/1.000/1.175/1.303$ |
| α=2 → 정점 $+17.8$ mV | $w\ln2=17.808$ mV |
| α 를 네 경로가 공유 | equilibrium/dqdv/solve_U_oc 전부 변화(entropy_coefficient 는 해당 점에서 0) |
| pad $=5L_V$ · 간격 $\le L_V/20$ · 4000점 · 잔여 $e^{-5}\approx0.7\%$ | `_LAG_PAD_NLV=5.0` · `lag_length/20.0` · `_LAG_PAD_MAXPTS=4000` · $0.674\%$ |
| pad 가 동결·ratio 양 경로 | `_causal_pad(V_prog` 호출 3회 |
| 기본 레거시 $R{=}8.314\cdot F{=}96485.0$ / `R_SI`·`F_SI` CODATA | 일치 |
| 레거시 $RT/F=25.6912$ / SI $25.6926$ mV | 일치 |
| $U_\oc$ raw $74.3511\to74.3497$, `.1f` $74.4\to74.3$ | 일치($-1.42\,\mu$V) |
| regsol 심볼 3종 부재 · `tr.get('kernel')` 0회 | 일치 |
| legacy `'kernel':'regsol'` dict $=$ 로지스틱 `array_equal` | True |
| $\Omega$ 코드 존치(`func_dU_hys`·`func_dH_a_eff`) | 존재 |
| `SI_MSMR7_LIT` 7전이·0.433/0.456·순수 로지스틱 | 일치 |
| `eq:gr2l-fwhm` 점근 과대율 $0.6/1.2/3.0\%$($\lambda{=}0.01/0.02/0.05$), $27\%$($0.5$) | 일치 |
| $w_\eff$ 폭 오독 배수 $6.6/21/30$ | 실측 $6.6/20.9/29.6$ |
| 단상 중심 높이 $=Q/(4w_\eff)$ 전 $\lambda$ 정확 | 항등 확인 |

### 3.4 코드 게이트 (문건이 인용하는 게이트 이름·결과)
```
test_gates_v1024.py                G1 PASS (module max|d|=0.0e+00, golden max|d|=0.0e+00, bit-exact=True)
                                   G2 PASS | G3 PASS | n(T) PASS | R6-G1/G2/G3/coverage PASS
test_gates_v1024_reflect.py        ALL PASS (4/4)   ← G-R3 = "regsol 삭제 확인" 으로 재작성
test_gates_v1024_selfconsistent.py ALL PASS (5/5)
test_gates_v1025.py                ALL PASS (8/8)   G-α1~4 · G-창 · G-극단 · G-SI · G-si7
python Anode_Fit_v1.0.24.py        >>> overall OK: True
```

### 3.5 줄바꿈·인코딩 무결
편집 14 + 3 + 코드/게이트 전건 **순수 CRLF**(bare LF 0) · BOM 0 — `scratchpad/patch/editstat.py` 대조.

---

## 4. 원본 불가침 확인
`docs/v1.0.24.1/` · `docs/v1.0.24/` **무변경** — LF-sha256 앞 16 `f230f59bb10bcc49`(두 폴더 동일),
`Claude/results/comp_v24/` 기존 파일도 무수정(T13 은 신규 addendum 방식).

## 4-A. 마감 검수에서 나온 후속 처리 (본 보고서 1차 작성 이후)

`MERGE_READINESS_v25.md` 를 쓴 4.8 서브세션이 본 보고서 1차판(mtime 02:06)과 실제 파일 상태를 대조해
**세 건**을 지적했고, 전부 처리했다. 지적이 옳았고 유용했으므로 그대로 남긴다.

| # | 지적 | 처리 |
|---|---|---|
| 1 | 본 보고서 1차판 이후에도 마스터가 `_sections` 를 계속 수정했고(자체검수 라운드), 그래서 **줄 수 합계와 정적 검사 실행 시점이 어긋난다** | ★**정적 검사·doc↔code 감사 전건 재실행**(최종 결과 = §3 에 반영: `STRUCTURE_CHECK PASS` · `STRICT ALL PASS` · doc↔code **30/30**) + 줄 수 **+250 → +262**(15파일) 로 갱신. 라벨(+3/−0)·`\boxed`(+1)·삭제 라벨 0 은 전 시점 불변 |
| 2 | 계획서 G0 이 요구한 **`G-금지` 게이트가 미구현**이라 "연속화 재사용 금지"·"두-상 폭 한정 재도입 금지" 가 기계 검증 없이 유지됨 | ★**구현 완료** — `test_gates_v1025.py` 에 `gate_forbidden()` 추가(규칙 4종: C5-a 연속화 문구 · C5-b `w_eff` 를 폭으로 읽는 서술[어순 양방향] · C5-c `w_eff(Ω)` 축소식 · C6 regsol 을 채택 경로로 서술). 금지를 \emph{서술}하는 문장은 면제 패턴으로 통과. **게이트 8종 → 9종, 9/9 PASS**. 공허하지 않음을 `results/tools_gate_forbidden_selftest.py`(음성 5/5 탐지 · 면제 4/4 통과)로 별도 증빙 |
| 3 | 지시서 T9 가 지목한 `ch1_sec08_lag.tex` 와 T10 이 지목한 §6 이 **미편집**(각주를 §9·§10 한 곳에 집약했었다) | ★**보완** — `ch1_sec08_lag.tex` 끝에 "$L_{V,j}$ 가 `eq:lag` 에 들어갈 때 하한 $-\infty$ 가 pad 를 요구한다 → 규약은 §9 각주" 포인터 3줄, `ch1_sec06_eqpeak.tex` 배경 제외 항에 "$C_\bg$ 상수는 창-국소 근사(§10 명기)" 1줄. 중복 서술 대신 **포인터**로 둔 것은 의도이며, 이제 지시된 파일 전건에 진입점이 있다 |

부수적으로, 검증 도구 4종을 스크래치에서 **리포로 이관**하고 경로를 리포 상대(`__file__` 기준)로 고쳐
재현 가능하게 했다 — `results/tools_tex_strict_check.py` · `tools_doc_code_audit.py` ·
`tools_gate_forbidden_selftest.py` (기존 `tools_check_structure.py` 와 같은 자리). `tools_tex_strict_check.py`
의 baseline 은 외부 스냅샷 파일 대신 `docs/v1.0.24.1/` 원본에서 즉석 수집하도록 바꿨다(의존 제거).

## 5. 한계 — 잔여 게이트 (★빌드 해소됨)
- ~~실제 LaTeX 빌드 미수행~~ → ★**해소(2026-07-26)**: MiKTeX 25.12(XeLaTeX 4.16)를 설치해 3장을 빌드했다
  — **오류 0 · Reference/Citation undefined 0** · 원본 v1.0.24.1 과 경고 프로파일 완전 동일(상세 =
  `MERGE_READINESS_v25.md` §0-A). §4-A 에서 빌드에서 처음 검증된다고 했던 세 곳((i) `ch1_sec18_inputs.tex`
  warnbox 안 enumerate, (ii) `ch1_appB_codemap.tex` longtable 셀 긴 서술, (iii) 신규 `\footnote` 배치) **전부
  정상 조판·오류 0**. 신설 식 페이지(ch1 p37 `eq:gr2l-fwhm`·p41 `eq:skewpeak`·`eq:skewapex`)를 PNG 렌더로
  시각 확인 완료.
- **미해결 물리 판단 1건** = §2 의 "흑연 물리 두-상 4 vs 2"(사용자 확인 요청) — 비-차단, 유일하게 남은 항목.
