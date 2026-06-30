# A3 Adversarial Review — v4-10 (Build + Citation + Style + Completeness)
> Reviewer role: adversarial A3 (인용·빌드·문체·완결성 회의자). 반증 시도. 파일 수정 금지.
> 대상: `Claude/results/ch2v4/v4-10/v4-10.tex` (737줄). Ground truth: `v4-00_spine/REVIEW_RISK_PATTERNS.md`.

---

## 1. 인용 정확성 표 (Citation Accuracy)

| bibitem key | 저자 | 저널·권·페이지 | 연도 | DOI | 판정 |
|---|---|---|---|---|---|
| bernardi1985 | Bernardi, Pawlikowski, Newman | JES 132(1) 5–12 | 1985 | 10.1149/1.2113792 | PASS (ground truth CONFIRMED) |
| newman | Newman & Thomas-Alyea | 교과서 3rd ed., Wiley | 2004 | ISBN | PASS |
| huggins2009 | **R. A.** Huggins | Springer 교과서 | 2009 | ISBN | PASS — R.A. Huggins(2009) 정확. M.L. Huggins 아님. |
| bazant2013 | Bazant | Acc.Chem.Res 46(5) 1144–1160 | 2013 | 10.1021/ar300145c | PASS (ground truth CONFIRMED) |
| reynier2003 | Reynier, Yazami, Fultz | J.Power Sources 119–121 850 | 2003 | 10.1016/S0378-7753(03)00285-4 | PASS (ground truth CONFIRMED) |
| allart2018 | Allart et al. | JES 165(2) A380 | 2018 | 10.1149/2.1251802jes | PASS (ground truth CONFIRMED) |
| occupation2019 | (저자 미기재) | Electrochimica Acta | 2019 | 10.1016/j.electacta.2019.135634 | PASS DOI — 저자·페이지 미기재(abstract tier 라벨 있음) |
| **chemmater2015** | (저자 미기재) | Chem.Mater. 27 | 2015 | 10.1021/acs.chemmater.5b00235 | **상세 아래** |
| jpcc2021 | (저자 미기재) | J.Phys.Chem.C 125(51) | 2021 | 10.1021/acs.jpcc.1c08992 | **상세 아래** |
| msmr_partI | (저자 미기재) | JES 2024 | 2024 | 10.1149/1945-7111/ad1d27 | PASS (ground truth CONFIRMED) |
| msmr_partII | (저자 미기재) | JES 2024 | 2024 | 10.1149/1945-7111/ad70d9 | PASS (ground truth CONFIRMED) |
| standardised2024 | (저자 미기재) | JES 2024 | 2024 | 10.1149/1945-7111/ad4918 | PASS (ground truth CONFIRMED — 전셀 값 라벨 명시됨) |
| hysteresis2018 | (저자 미기재) | J.Power Sources 2018 | 2018 | 10.1016/j.jpowsour.2018.05.060 | PASS (ground truth CONFIRMED) |
| numverif2026 | 본 연구 내부 자료 | 내부 | 2026 | 없음 | PASS — 내부 자료 명시 |

### chemmater2015 상세 판정

- **DOI 실재**: YES — CrossRef 확인, 실존 논문.
- **실제 제목**: "Intercalation Compounds from LiH and Graphite: Relative Stability of Metastable Stages and Thermodynamic Stability of Dilute Stage I_d" (Konar, Häusserman, Svensson, Chem.Mater. 27(7), 2015)
- **v4-10 기재 제목**: "Intercalation Compounds from LiH and Graphite: Relative Stability of Metastable Stages\ldots" — 부제(" and Thermodynamic Stability of Dilute Stage I_d") 누락, `\ldots` 처리
- **내용 정당성**: 본문 인용 맥락(line 340–342): LiC₆ -13.9, LiC₁₂ -24.8 kJ/mol Li 형성 엔탈피 calorimetry. 논문 주제(LiH-graphite 삽입화합물 안정성)와 내용 도메인 정합 — 그러나 이 특정 수치는 LiH 루트 형성 엔탈피이고, 흑연+Li 금속 기준 형성 엔탈피와의 기준계 차이 주의(본문이 이미 "기준 차이" 주의를 달고 있음).
- **fabrication 판정**: **NOT fabricated** — DOI 실존, 제목 일치(축약 처리), 내용 도메인 정합. 체리픽이 "유효 DOI"로 주장한 것이 맞음. 저자·호수·페이지 미기재는 abstract tier 관행으로 허용 범위.
- **잔여 위험**: 구체적 수치(-13.9/-24.8)의 기준계(LiH vs Li 금속 기준)를 full-text 없이 확정 불가 — 본문의 "직접 등치 불가·미분 환산 필요" 경고로 이미 방어됨(line 341-342).

### jpcc2021 상세 판정

- **DOI 실재**: YES — CrossRef 확인(J.Phys.Chem.C 125(51) pp.27891–27900, 2021, Haruyama et al. 7저자).
- **제목 내 "Calculations"**: **존재함** — 실제 제목 "Thermodynamic Analysis of Li-Intercalated Graphite by First-Principles Calculations with Vibrational and Configurational Contributions". v4-10 기재 제목과 **완전 일치**.
- **ground truth 경고(★title "Calculations" 누락 주의)**: v4-10 은 "Calculations" 포함하고 있으므로 위험 이미 회피됨. **PASS**.
- **판정**: fabrication 없음.

---

## 2. 빌드 상태 (xelatex 2-pass)

| 항목 | 결과 |
|---|---|
| 컴파일 에러 (!) | 0 |
| undefined reference/citation (2nd pass) | 0 |
| multiply-defined label | 0 |
| Overfull \hbox > 20pt | **0** (유일 Overfull: 4.57pt @ lines 687–689, 임계 20pt 미달) |
| 출력 | v4-10.pdf 13 pages 생성 |
| 결론 | **빌드 PASS** (재실행 권고 경고만 — cross-ref 정상 수렴) |

---

## 3. 위험 6 — 텔레그래프 문체 (한계·갭·맺음 절)

### 한계·갭 절 (lines 678–684)
각 항목이 완결 문장(finite verb 있음): "확정해야 한다", "제시한다", "확보하지 못했다", "다뤘다", "명시했다". **PASS — 완결 문장**.

### 맺음 절 (lines 709–716)
모든 문장 finite verb 있음: "세웠다", "보였고", "세웠다", "만든다", "닫았다", "검산하고", "확정했다", "재배열하는 열이다". **PASS — 완결 문장**.

### 기타 한계 관련 서술
항목별 산문체 완결. 텔레그래프 문체(괄호 보충 명사구로 끝, finite verb 없음) **미발견**.

---

## 4. 완결성·Orphan 점검

### 라벨 정의 vs 참조 (전수 대조)

정의된 주요 라벨: `sec:partition`, `ssec:logistic`, `ssec:BW`, `sec:config`, `sec:vibel`, `ssec:elec`, `sec:mixing`, `ssec:overlap`, `ssec:weff`, `ssec:hys`, `sec:limits`, `sec:revheat`, `fig:occ_config`, `fig:blend`, `fig:weff`, `tab:ds`, `tab:limits`, `eq:Z1`–`eq:qrev` 등 43개.

모든 `\ref{}·\eqref{}` 대상이 문서 내 정의됨 — **undefined ref 0 (2nd pass 확인)**.

### ★ DEFECT — "파생 I" 미정의 참조 (line 386)

```tex
유지된다(파생 I 의 예외, \S\ref{sec:limits}).
```

문서에는 파생 A, B, C, D 만 존재. "파생 I"는 어떤 section·subsection·keybox·warnbox에도 정의되지 않은 **dangling 텍스트 포인터**. `\S\ref{sec:limits}` 는 정상이나, "파생 I" 라는 이름 자체가 orphan. 심각도: MED (논리 흐름 혼란, 독자 오인 위험).

### 그림 TikZ 내 한글

3개 TikZ 환경 전부에서 `\node` 텍스트에 한글 포함:
- `fig:occ_config` (lines 264, 275, 279): "(a) 점유 분포 = Ch1 logistic", "최대 $\ln 2$...", "(b) configurational 엔트로피"
- `fig:blend` (lines 478, 490, 495): "탈리튬화 진행", "겹침 영역: 연속 블렌드", "계단(틀림)"
- `fig:weff` (lines 550, 560, 561): "(임계)", "균질 고용체", "상분리"

요구 조건: "그림 TikZ 영어 ASCII(한글 0)". **모든 그림 위반** — 심각도: MED (요구 조건 불이행, PDF 출력은 kotex 덕분에 현재 정상이나 규약 위반).

### 흐름 완결성 (분포→섞임→가역열)
사슬 $Z \to \langle n\rangle \to S \to \partial U_\oc/\partial T \to \dot Q_\rev$ 이 서문 boxed식에서 선언되고 각 절이 순서대로 전개·닫힘. 각 파생(A–D)이 뒤 참조 포함. **흐름 완결 PASS**.

---

## 5. 결함 요약표

| 식별자 | 위치 | 심각도 | 내용 | 정정 방향 |
|---|---|---|---|---|
| D1-TIKZ-KO | lines 264,275,279,478,490,495,550,560,561 | **MED** | TikZ node 내 한글 — 영어 ASCII 요건 위반 | 모든 TikZ 라벨을 영어 ASCII로 교체(caption에 한글 설명 이전) |
| D2-DANGLING-PAESAENG-I | line 386 | **MED** | "파생 I" — 문서 어디에도 정의 없는 dangling 포인터 | "파생 I" → 실제 해당 절(예: \S\ref{ssec:elec}) 참조 또는 삭제 |
| D3-CHEMMATER-TITLE | line 727 | **LOW** | chemmater2015 제목 부제 누락(\ldots 처리). fabrication 아님, abstract tier 허용 범위. | 필요 시 전체 제목 기재(Konar et al.) |

---

## 6. 가장 약한 1곳 (weakest point)

**D2 — line 386 "파생 I" dangling** 이 논리 무결성 관점 최약. "파생 I 의 예외"가 무엇인지 독자가 추적 불가. D1(TikZ 한글)은 규약 위반이나 시각적으로는 정상 렌더링되므로 논리 파괴 없음. D2는 텍스트 자체가 근거 없는 포인터.

---

## 결론 (10줄 이내)

1. **fabrication**: chemmater2015 — NOT fabricated (DOI 실존, Konar et al. 2015, 제목 정합, 내용 도메인 정합). jpcc2021 — PASS ("Calculations" 포함 확인). 전 bibitem fabrication 0.
2. **문체(위험 6)**: 한계·갭·맺음 절 전부 완결 문장. 텔레그래프 문체 미발견. PASS.
3. **빌드**: 2-pass 0 error, 0 undefined ref, 0 multiply-defined. Overfull 4.57pt only (< 20pt). PASS.
4. **Orphan/완결성**: "파생 I" (line 386) dangling — 문서 내 미정의 포인터 (MED). TikZ 3개 환경 한글 라벨 — 규약 위반 (MED). 논리 흐름(Z→열) 완결.
5. **가장 약한 곳**: line 386 "파생 I" dangling reference.
