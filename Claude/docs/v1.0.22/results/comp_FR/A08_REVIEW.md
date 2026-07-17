# A08_REVIEW — §7 두-상 broadening (`ch1_sec07_broadening.tex`) 심층 검토 (FR-A08)

> 대상: `/home/user/Project_Anode_Fit/Claude/docs/v1.0.22/_sections/ch1_sec07_broadening.tex` (전문 정독)
> 참조 원문 확인(read-only): `ch1_sec05_width.tex`(§5 폭·이중지위·폴백), `ch1_sec06_eqpeak.tex`(eq:eqpeak·eq:belliden), `ch1_sec04_hys.tex`(eq:Veq·eq:spinodal·eq:dUhys), `ch1_sec08_lag.tex`(L_V∝|I|), `ch1_sec09_tail.tex`(eq:lag=단측 지수 커널 합성곱), `ch1_sec10_sum.tex`(tab:staging·w 폴백), `ch1_sec01_n0n1.tex`(fig:staging), `ch1_sec11_lcointro.tex`(tier 각주 원본), `ch1_graphite_v1.0.22.tex`(빌드·xr), `ch1v22_bib.tex`, `results/V1022_REFERENCE_LEDGER.md`(V1 원장·v1.0.21 승계).
> 규율: 보고 전용 — 소스 무수정·git 무조작·`Codex/` 미접근. bgbox 증축분(CLT box·tier 각주)의 제거 용이 독립성 유지 전제로만 제안. GS-1/GS-2(Ch3 Si 정직 공백)는 본 절 무관 — 메움 제안 없음.
> 상태: **작성 중 조기 저장본** — 수치 재검증(§V)·문헌 서치(§S) 완료 후 최종 확정. (완료 시 이 줄 갱신)

---

## 발견 표 (BRIEF 양식)

*(진행 중 — 아래 등급별 절에 축적, 최종 표는 본 절에 통합)*

| ID | 파일:행 | 유형 | 등급 | 현행(축자) | 제안(완성 LaTeX) | 근거 |
|---|---|---|---|---|---|---|
| (작성 중) | | | | | | |

---

## H 등급 (논리/물리 오류·오귀속)

### A08-H1 — keybox 가 본문의 이중계산 금지 규정과 자기모순: "셋을 한꺼번에 흡수하는 것이 현상학적 자유 피팅 폭"
- 파일:행 = `ch1_sec07_broadening.tex:309`
- 유형 = 논리(수식↔산문 불일치·자기모순)
- 현행(축자, 301–310행 keybox 중):
```
③ \emph{입자 앙상블}의 집합 통계역학 --- 평형 층(Dreyer 순차 전환이 \emph{plateau 구조}를
만듦)과 broadening 층(그 평형 델타를 펴는 \emph{apparent-U $=U_j+\eta$} 의 입자간 $\eta$ 산포 $\rho(U_\app)$)으로 갈리며,
forward 평균 $\int\rho(U_\app)\,(\dd Q/\dd V)^\mathrm{single}\,\dd U_\app$(식~\eqref{eq:ensavg}; $\rho\!\to\!\delta$ 면
평형 중심 $U_j$ 의 단일 델타로 환원; 흑연-특정 구조 무질서 \emph{근거}는 흑연 두-상 한정 --- LCO 는 일반
$\eta$ 산포로만, 본문 ③). 셋을 한꺼번에 흡수하는 것이 \emph{현상학적 자유 피팅 폭}이며 ---
```
- 문제: 본문(120–123행)은 "식~\eqref{eq:ensavg} 가 담는 것은 ②$\otimes$③뿐", "두-상 \emph{총} broadening 은 $w_j(\text{②}\otimes\text{③})+L_V(\text{①})$ 로 묶인다(①의 전류 몫을 $w_j$ 가 다시 흡수하면 **이중계산**)"으로 ①을 $w_j$ 에서 명시 배제했고, 식~\eqref{eq:widthbudget}(157–164행)도 대칭 폭(②③)과 비대칭 꼬리 길이(①=$L_{V,j}$)를 별도 축으로 분리했다. 절 도입(8–9행)에서 "현상학적 자유 피팅 폭"= $w_j$ 로 정의되므로, keybox 의 "셋을 한꺼번에 흡수"는 $w_j$ 가 ①까지 흡수한다는 뜻이 되어 **본문 규정과 정면 모순**(keybox 자체 안에서도 ① 을 "$L_V$" 담당으로 이미 적어 두 문장이 충돌).
- 제안(대체 LaTeX — keybox 해당 문장만):
```latex
②$\otimes$③ 을 한꺼번에 흡수하는 것이 \emph{현상학적 자유 피팅 폭} $w_j$ 이고, ① 은 별도 축
$L_{V,j}$ 가 담당한다(①의 전류 몫을 $w_j$ 가 다시 흡수하면 이중계산 --- 식~\eqref{eq:widthbudget}) ---
```
  (뒤따르는 "\emph{분포하는 것은 $\eta$...}" 문장은 그대로 접속.)
- 근거: 같은 파일 120–123행·157–164행·§도입 8–9행과의 정합; §5 `sec:width-w` 296–305행("broadening 이 정하는 현상학적 자유 피팅 폭"=w_j)과의 정합.

*(이하 등급별 발견 — 작성 진행 중)*

## M 등급 (의미·이해 실질 개선)

- A08-M1 (bgbox CLT — Lindeberg 조건의 gloss 가 Feller(무지배) 조건과 혼동) — 상세 작성 예정
- A08-M2 (bgbox CLT — "분산 가법의 CLT 재유도" 귀속 오류: 가법은 독립성만으로 성립, CLT 는 형상만 공급) — 상세 작성 예정
- A08-M3 (fig:widthbudget 캡션 "치수선 길이로 직접 대비" — σ 치수선은 2σ 스팬, L_V 치수선은 1·L_V 로 2배 눈금 불일치) — 상세 작성 예정
- A08-M4 (scope(ii) "분포는 폭을 넓힐 뿐 평형 중심 U_j 를 옮기지 않는다" — 관측 peak 중심은 η̄ 만큼 이동 가능, U_j(파라미터) 불변과 구분 필요) — 상세 작성 예정
- A08-M5 (② 내재 폭의 기작 한 걸음 — binodal 접속의 단상 가지 몫을 한 봉우리로 읽을 때의 유효 폭임을 명시) — 상세 작성 예정

## L 등급 (문체·표시)

- A08-L1 ("약 10%" 수치 정밀도 — 수치 재검증 후 확정) — 진행 중
- A08-L2 (① "본 장이 이미 모델로 담은 출처" — 선형 독자에겐 §8·§9 가 후행) — 상세 작성 예정
- A08-L3 ("비-크기·비-사이즈" 중복 표현) — 상세 작성 예정
- A08-L4 (FWHM ≈91 mV(본문) vs 90.5 mV(fig:logistic 캡션) 표시 자리수 어긋남) — 상세 작성 예정

## 검증 로그 (§V — 재계산·재유도)

*(진행 중 — Python 수치 검증 결과 기입 예정)*

- [수기 검증 완료] logistic FWHM $=2\ln(3+2\sqrt2)\,w\approx3.5255\,w$ ✓ (u²−6u+1=0, u=3−2√2 재유도)
- [수기 검증 완료] logistic 분산 $\pi^2w^2/3$, $\sigma_\mathrm{int}=\pi w/\sqrt3=1.8138\,w$ ✓ (그림 1.81 ✓)
- [수기 검증 완료] $\sigma_\eta=1.25\sigma_\mathrm{int}$ ⇒ $\sigma_\mathrm{sym}=\sigma_\mathrm{int}\sqrt{1+1.25^2}=1.6008\,\sigma_\mathrm{int}=2.9035\,w$ ✓ (그림 2.90 ✓); 유효 scale $1.6008\,w\approx1.6w_j$ ✓
- [수기 검증 완료] Gibbs–Thomson: $\Delta U(1\,\mu m;\gamma=1)=2\cdot3.6\times10^{-5}/(96485\times10^{-6})=0.746$ mV ✓ (≈0.75); $\delta U_\mathrm{PSD}(3/15\,\mu m)=0.199$ mV ✓ (≈0.20); γ=5 ⇒ 0.995 mV ✓ (≈1.0); r=30 nm ⇒ 24.9 mV ✓ (≈25); 0.746/25.68=2.9% ✓ (<3% 주장 성립)
- [수기 검증 완료] $V_m$: 6×12.011/2.26=31.89 cm³/mol ✓ (≈31.9); ×1.13≈36.0 ✓
- [수기 검증 완료] τ(5μm)=r²/D: D=4×10⁻¹⁰ ⇒ 625 s ≈ 6×10²; D=10⁻¹¹ ⇒ 2.5×10⁴ s ✓
- [수기 검증 완료] 지수꼬리 분산 가법: eq:lag ⇒ peak shape = (dξ_eq/dV) ⊛ Exp(L_V) (정확 합성곱, §9 eq:tail-limit-start 재유도) ⇒ Var += L_V², 평균이동 +σ_d L_V ✓
- [수기 검증 완료] tab:staging Ω 초기값(6000/8000/10000/13000) 모두 > 2RT=4957.6 J/mol ✓ ("네 전이 모두 문턱" 주장 성립)
- [수기 검증 완료] 폴백 폭 0.014/0.012 V ⇒ 유효 다중도 n=wF/RT=0.545/0.467 (<1) — ② 문단 주장과 정합 ✓
- [ ] fig:widthbudget stage2/3/4 좌표의 수치 합성곱 재현 — Python 예정
- [ ] "지름길 peak 약 10% 높다" 정밀값 — Python 예정

## 서치 절 (§S — 하이쿠 서브에이전트 위임 결과)

*(진행 중 — doi 실검증분만 후보 표로 통합 예정)*

## 무발견 축 (검토했으나 문제 없음)

*(최종 정리 시 확정)*

## 4-tier 분류

*(최종 정리 시 확정)*
