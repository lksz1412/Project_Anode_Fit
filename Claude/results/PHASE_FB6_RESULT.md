# Phase FB6 — F-01 §1.1.4 배경 압축 + F-08 LCO장 서두 재균형 Result

## Summary
국소 내용 조정. **F-01**: §1.1.4(sec:pointwise)의 측정-원리 배경 2박스(bgbox 14줄 + srcbox 27줄 = 41줄)가 foundational 절을 과점 → 인용·표 보존하며 산문 압축(~20줄, ~50%↓, ch1 98→97쪽). **F-08**: LCO장(ch2_lco) 서두가 "같은 골격/같은 식" 공유점을 선도 → 흑연과 \emph{갈라지는} 세 축($\sigma_d$ 재배선·order--disorder/MIT·전자 엔트로피 항)을 선도로 재배열, 공유 골격은 1개 절로 격하. 장 제목도 "같은 골격, 추가되는 텀만" → 세 차이 축으로 개작. 물리·식번호·label 정의 불변.

## Step Range
cumulative **FB step 36–39**.

## Inputs
- `_sections/ch1_sec01_n0n1.tex`(§1.1.4 = sec:pointwise; bgbox·srcbox).
- `_sections/ch2v22_sec00_intro.tex`(LCO장 서두 단락).
- `ch2_lco_v1.0.24.tex`(장 제목 `\title`).
- 결정: D4(§1.1.4 배경 박스 압축 — 삭제 아님) · F-08 사용자 지시(공유점 최대 생략·$\sigma_d$/차이/추가 중점).

## Files Created
- 없음.

## Files Updated
- `ch1_sec01_n0n1.tex`: **F-01** (1) bgbox "측정 원리 배경" 14줄 → 7줄(3-대응 색인: $U_\oc$↔GITT·$\partial U/\partial T$↔전위차엔트로피법·가역발열↔등온열량; 인용 4종 보존·"모델 식은 측정 무관" 가드 유지·Part T 방법론 절 포인터). (2) srcbox "다리" 27줄 → 15줄(GITT 대응표 보존·"방법 요지/가정 차" 산문 12줄→5줄 압축; 인용 5종 보존).
- `ch2v22_sec00_intro.tex`: **F-08** 서두 단락 재작성 — 선도를 흑연 공유점에서 \emph{차이 세 축}((i) $\sigma_d$ 방향 재배선[양극 방전=리튬화, 흑연과 부호 반대] (ii) order--disorder/MIT 2상역 (iii) 흑연에 없는 전자 엔트로피 항 $\Delta S_e$)으로 이동. 공유 곡선 골격은 "이미 닫혔으므로 재유도 없이 식 번호만 인용" 1절로 격하.
- `ch2_lco_v1.0.24.tex`: **F-08** 장 제목 부제 "같은 골격, 추가되는 텀만: 파라미터 교체와 전자 엔트로피" → "방향 재배선$\cdot$order--disorder$\cdot$전자 엔트로피 항"(공유점 선도 제거·차이 축 선도).

## Read Coverage
- 전문 정독: §1.1.4 전체(191–255)·LCO장 서두(ch2v22_sec00_intro 전문)·장 제목.
- 렌더 확인: §1.1.4(p10, 압축 박스 가독)·LCO 제목/서두(ch2 p1, 차이 선도 확인).
- 인용 보존 grep: §1.1.4 = weppner_huggins1977·reynier2003·swiderska2019·baek_pilon2022·allart2018 전부 존치.

## Execution Evidence
```
F-01: §1.1.4 배경 41줄→~20줄(bgbox 14→7·srcbox 27→15). 인용 5종 전부 보존. ch1 98→97쪽(1쪽 절감)
F-08: LCO 서두 단락+장 제목 차이-선도 재배열. σ_d/order-disorder/전자항 foregrounded, 공유 골격 격하
빌드(3챕터): ch1 0-err/97p · ch2 0-err/30p · ch3 0-err/21p · undefined ref/cite 0
invariant: \label 정의 제거 0 · 식번호 불변 · cite/eqref 키(§1.1.4 5인용·eq:vn) 보존
압축 부수: 낙오 \ref 포인터 4개(sec:width·sec:broadening·sec:lco-hys-od·ssec:qrevtab) — 삭제된 판독지도 대상-열거 문장 소속, 대상 label 존치·타처 참조·빌드 0-undef
```

## Validation (게이트별)
- **F-01 §1.1.4 압축** — PASS(배경 박스 ~50%↓, 인용·GITT 대응표 보존, D4 준수[삭제 아닌 압축], 1쪽 절감, 렌더 가독).
- **F-08 LCO 서두 재균형** — PASS(서두 단락+장 제목 모두 차이 축[σ_d·order-disorder·전자항] 선도, 공유점 격하; 렌더 확인).
- **빌드 GREEN** — PASS(97/30/21·undefined ref/cite 0).
- **물리·식번호·label 정의 불변** — PASS(label 정의 제거 0, 식번호 불변).

## Gate
**PASS_FB6_CONTENT** (§1.1.4 배경 압축[인용 보존] + LCO 서두 차이-선도 재균형 + 빌드 GREEN + label 정의 불변).

## Confirmed Non-Changes
- 코드 `.py` 무변경(sha256 f230f59b). 식번호·`\label` 정의·물리 내용 불변.
- §1.1.4 핵심 산문(점별 평가 원칙)·keybox(두 전위)·GITT 대응표 보존 — 압축은 배경 박스 \emph{산문 verbosity} 한정.

## 추가 후보 (실제 미수정 — flag)
- **LCO장 §2.1 도입 소절 제목**(§2.1.1 "전극-중립 골격 --- 전극 무관 요소"·§2.1.3 "MSMR 대응 개관 --- 같은 logistic, 같은 부호 규약")은 공유-골격 측면을 다루는 절이라 제목이 내용과 정합(전극-중립 골격 확립은 재사용 방식의 필수 토대). F-08 서두 프레이밍(단락·제목)은 차이-선도로 완료했으나, 도입 소절 제목까지 공유점 표현을 더 줄일지는 사용자 판단(내용 왜곡 위험 있어 미개작).
- **페이지수 변동**: ch1 98→97(§1.1.4 압축). FB7 MERGE_READINESS/HANDOVER/INDEX 페이지수(98→97) 갱신 필요.
