# NOTE_q3o2 — v1.0.21 Q3 (Eyring TST 분배함수 유도) 경쟁 초안 q3o2

> 독립·무통신 창. `results/comp_Q3_tst/` 의 다른 draft·NOTE 미열람.
> 산출: `draft_q3o2.tex`(78행, content 66행) + 본 NOTE. 문서 원본 무수정.
> 반영은 v1.0.21 — 본 창은 초안만.

---

## 1. 형식 판단 — bgbox 채택 (근거 기록, 태스크 요구)

**결론: 인라인 (a)~(d) 소단락이 아니라 `bgbox`(배경 박스) 자족 블록으로 작성.**

근거 세 가지:

1. **본문 흐름 비간섭.** §5.1 `sec:width-logistic` 본문은 이미 자체 (a)출발(Eyring)→(b)연산(비→detailed balance)→(c)중간식(정지점 logit)의 사슬로 짜여 있고(현행 line 13~42), 그 흐름은 `k_0`·`ΔS_a` 의 미시 기원 없이도 정지점→logistic 으로 완결된다. 배경 유도를 인라인 (a)~(d) 소단락으로 넣으면 **같은 소절 안에 (a)~(d) 사슬이 둘** 겹쳐 라벨·헤더가 충돌한다. rubric D2'·A3(orphan 0) 위반 위험.
2. **rubric D2' 자족 블록 정의에 정확히 부합.** "본문 흐름에서 분리 가능한 배경 지식 전용, 자족 블록(본문이 박스 없이도 읽히고 박스는 어디로 옮겨도 성립)." TST `k_BT/h`·`ΔS_a` 미시 기원이 바로 이 성격이다.
3. **동형 선례.** 같은 Chapter 1 Part 0 §2.2(`ch1_sec02a_part0.tex` line171~205)가 구조적으로 동일한 배경 통계역학(페르미온·보손 양자통계)을 `bgbox` 로 처리한다. 이 선례를 따라 렌더·어조 정합.

`DIRECTION_STATMECH_REPORT.md` 후보(ii) 배치 제안도 **1순위 = §5.1 `eyring1935` 인용 직후 `bgbox`** 로 동일 결론(단, 그 판단은 창이 독립 정독 후 재확인한 것).

**박스 제목 형식:** part0 bgbox 실사용형(`\textbf{제목 ---}` 인라인)을 따름. `\newtheorem*{bgbox}{배경}` 는 `[...]` 옵션 인자도 지원하나(rubric D2' 예시), 같은 파일군의 렌더 선례가 인라인 `\textbf` 이므로 그것으로 통일.

---

## 2. 전 식 자체 재유도 검산 (태스크 "모든 식 자체 재유도 검산 기록")

수치 검산은 `python3`(sympy 부재 → math 모듈, 기계정밀도 rel.err 확인). 아래 ✓ 는 해석적 + 수치 병행 확인.

### (b) eq:tst-nu — `k_BT/h` 의 보편성 (δ·m* 상쇄)
- 통과 빈도 × 병진 분배함수:
  `(⟨v⟩/δ)·q∥ = [(k_BT/2πm*)^{1/2}/δ]·[(2πm*k_BT)^{1/2}δ/h]`
- 근호 안 결합: `(k_BT/2πm*)·(2πm*k_BT) = (k_BT)²` → 근호 `= k_BT` → `/h`.
- **δ 와 m* 가 완전 상쇄**, 결과 `= k_BT/h` (온도만의 함수).
- 수치: 임의 (δ,m*) 두 조 모두 `(v/δ)q∥ = 6.212438e12 s⁻¹ = k_BT/h`, rel.err 1.6e-16. ✓
- 물리 읽기: `k_0` 는 특정 진동수가 아니라 장벽 통과의 **보편 빈도** — 현행 "시도 빈도" 한 마디에 근거 부여.

### (c) eq:tst-rate — 분배함수 비 → ΔG_a
- `k = (k_BT/h)(q‡/q_R)e^{-ΔE_0/RT}`.
- `(q‡/q_R) = e^{+ln(q‡/q_R)}` 를 지수로 합침:
  `= (k_BT/h)e^{ln(q‡/q_R) - ΔE_0/RT} = (k_BT/h)e^{-[ΔE_0 - RT ln(q‡/q_R)]/RT} = (k_BT/h)e^{-ΔG_a/RT}`,
  `ΔG_a ≡ ΔE_0 - RT ln(q‡/q_R)`.
- 몰당 환산: `k_B→R`, `ΔE_0` 는 몰당 에너지.
- 수치: `(q‡/q_R)e^{-ΔE_0/RT}` 와 `e^{-ΔG_a/RT}` rel.err 4.3e-15. ✓

### (d) eq:tst-arr — Eyring 형 + ΔS_a 식별
- `ΔG_a = ΔH_a - TΔS_a` 대입:
  `e^{-ΔG_a/RT} = e^{-(ΔH_a - TΔS_a)/RT} = e^{ΔS_a/R}e^{-ΔH_a/RT}`.
- 따라서 `k = (k_BT/h)e^{ΔS_a/R}e^{-ΔH_a/RT}`.
- T-선형(엔트로피) 항 대응: `-TΔS_a = -RT ln(q‡/q_R)` ⟹ `ΔS_a = R ln(q‡/q_R)` (반응좌표 제외 reduced 비).
- 수치: 좌·우변 rel.err 4.3e-15; `q‡<q_R ⟹ ΔS_a<0` 부호 확인. ✓

### 접속 — eq:sm-sint 동일 언어 (Part 0)
- 엄밀 열역학 엔트로피: `ΔS_a = -∂ΔG_a/∂T = -∂/∂T[ΔE_0 - RT ln(q‡/q_R)]`
  `= R ln(q‡/q_R) + RT ∂ln(q‡/q_R)/∂T = R ∂[T ln(q‡/q_R)]/∂T`.
- Part 0: `s_int = k_B ∂(T ln q)/∂T` (eq:sm-sint).
- **동일 연산자** `∂(T ln q)/∂T` 를 활성화 비 `q‡/q_R` 에 적용(자리당 `k_B` → 몰당 `R`). 박스의 `R ln(q‡/q_R)` 는 그 **선행 항**(비의 잔여 T-의존을 ΔH_a 로 넘긴 표준 읽기). ✓ 해석적 확인.

### 차원·고전 극한 검산 (verifybox)
- 차원: `[k_BT/h] = J/(J·s) = s⁻¹`(빈도), `q‡/q_R·ΔS_a/R·ΔH_a/RT` 무차원 → `k` 속도 차원, `eq:kuniv` 의 `k_j` 와 정합. ✓
- 원형(Arrhenius) 회수: `q‡=q_R ⟹ ΔS_a=0 ⟹ ΔG_a=ΔH_a ⟹ k=(k_BT/h)e^{-ΔH_a/RT}` = 본문 (a) 의 `k≃k_0 e^{-ΔG_a/RT}`. **현행 §10(sec:sum) 기본값 `ΔS_a=0` 이 정확히 이 경우** — 회수 지점이 문서 기본값에 착지. ✓

---

## 3. 가드 준수 (태스크 "기존 기호 정의 충돌 금지" + 보고서 필수 가드)

| 가드 | 처리 |
|---|---|
| **ΔS_a(활성화·속도) vs ΔS_rxn(반응·평형)** | verifybox 에 오독방지 가드(rubric A2 허용형): "공유하는 것은 '엔트로피=분배함수 로그' 언어뿐이고, ΔS_a 는 안장점 기준 활성화량(속도)·ΔS_rxn 은 생성물 기준 반응량(평형)". `tab:notation` 분리 등재 참조. |
| **ΔG_a 기호 충돌** | 별도 `ΔG‡` 신설 안 함. 문서 기존 `ΔG_a` 를 그대로 써 `ΔG_a = ΔE_0 - RT ln(q‡/q_R) = ΔH_a - TΔS_a` 로 **강화**(관례 표기 `ΔG‡` 는 1회 괄호 병기). |
| **q(T)(Part0 내부 분배함수) vs q=Q/Q_cell(용량 좌표)** | 박스는 `q‡·q_R·q(T)`(모두 내부/분배함수 q)만 사용, 용량 좌표 미접촉. eq:partfn 각주의 기존 가드와 일관. |
| **χ·𝒜·k_j 정의 불변** | 박스에서 재정의 없음. eq:tst-arr 의 `k` 를 `eq:kuniv` 의 `k_j` 와 차원·정합으로만 연결. χ(장벽 분율)는 미사용. |
| **k_BT/h 도출 한정** | "반응좌표 모드를 자유 1D 병진으로 본 표준 TST, 변분 TST·터널링 범위 밖" 1문장 명시(보고서 필수 가드). |
| **새 물리 주장 금지** | 기존 `k_0`·`ΔS_a` 의 근거 보강만. 결과식 eq:bv·eq:kuniv·eq:Lqfull **불변**. |

§8 = 사용 / 여기 = 기원 프레이밍: 박스 말미 "§8 이 ΔS_a 를 L_q 로 쓰는 자리라면(eq:Lqfull), 이 박스는 그 기원" 명시 + B 문장이 §8.4 에서 후방 참조.

---

## 4. 인벤토리 (라벨·인용·참조)

- **신규 라벨(eq:tst-\* 계열, 충돌 없음 — 전 `_sections` grep 결과 eq:tst 부재):**
  `eq:tst-nu`(k_BT/h 상쇄) · `eq:tst-rate`(분배함수 비→ΔG_a) · `eq:tst-arr`(boxed Eyring+ΔS_a).
- **인용(전 4종 원장 V1 등재 확인):** `eyring1935`·`glasstone1941`·`laidlerking1983`(박스 개시) · `mcquarrie1976`(eq:tst-rate). `V1020_REFERENCE_LEDGER.md` row37·38 에 glasstone1941·laidlerking1983 = V1 등재("v1.0.21 Q3 TST" 사유), eyring1935·mcquarrie1976 = 기존 V1.
- **참조한 기존 라벨(존재 확인):** eq:bv·eq:kuniv·eq:partfn·eq:sm-sint·eq:Lqfull·tab:notation·sec:width-logistic·sec:center·sec:sum·sec:lag — 전부 현행 문서에 실재.
- **삽입점:**
  - A(bgbox) → `ch1_sec05_width.tex` line15 `\cite{eyring1935}` 문장 직후(다음 "구동력 𝒜_j..." 문장 앞).
  - B(1문장) → `ch1_sec08_lag.tex` §8.4 `sec:lag-LV`, eq:Lqfull(line103) 직후.

---

## 5. 컴파일 검증

`ch1_preamble.tex` + 외부 라벨 스텁 래퍼로 `xelatex -halt-on-error` 컴파일 →
**exit 0, PDF 생성, 미정의 제어열 0, math/구문 오류 0.** (bgbox·verifybox·equation×3·boxed×1 환경 짝 정합, 중괄호 87/87 균형.)

---

## 6. P3 검수 7항 관련 (해당 항목만)

- 1항(V_n 계열 구분): 박스는 `k_0`·`ΔS_a` 배경으로 V_n 계열 미접촉 → 무영향.
- 6항(Ch1 기준식 ↔ Ch2~5 충돌): 결과식 불변이라 전달식 정합 무변.
- 7항(ver.N ↔ Chapter 명칭): 박스에 ver 표기 부재 → 혼동 없음.
- rubric B1·B3·B4(D7 정통 선행): (a)출발→(b)연산→(c)중간식→(d)boxed + verifybox(극한≥2·부호·원형회수). 정통 TST = 원형, Part0 접속 = 확장 동기, ΔS_a=R ln(q‡/q_R) = 식별, q‡=q_R Arrhenius = 회수. 충족.

---

## 7. 추가 후보 (실제 수정 안 함 — 보고만, P5 규약)

- `tab:notation` 에 `q^\ddagger`·`q_R`·`ΔE_0`·`m^*`·`δ` 정식 등재는 v1.0.21 반영 시 집행 항목(본 초안은 박스-국소 정의로 자족 처리). 등재하면 rubric B5 완전 충족.
- `laidlerking1983` 은 리뷰(tier B 성격) — 반영 시 tier 각주 부착 여부는 사용자/집행 판단.
