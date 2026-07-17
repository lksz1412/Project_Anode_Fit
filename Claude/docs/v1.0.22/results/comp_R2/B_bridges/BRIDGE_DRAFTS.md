# BRIDGE_DRAFTS — 인용 다리(흑연분) 초안 색인 (v1.0.22 R2 · O-B)

> 초안 전용. 각 다리 = `br_<키>.tex` 스니펫(본문 삽입용 LaTeX, `srcbox` 컨테이너, 우리 기호 서술 · 논문 기호는 대응표에서만). 삽입 시 마스터가 diff 1:1 로그로 집행.
> 3요소(마스터플랜 §7): ①변수 대응표/등치 중간식 1~3개 ②논문 방법 요지 1문장 ③가정 차 1문장 — 전건 완비.
> 컨테이너 = `srcbox`(preamble `\newtheorem*{srcbox}{문헌 근거}`) — 기존 §2.7 등에서 인용 근거 노트로 쓰던 관행 따름. 신규 등치식 라벨 = `eq:br-<키>-<n>`(제안, 현재 bazant 1건만).

## 다리 8건 색인

| # | 스니펫 | 키 | 삽입 파일:행(앵커) | 우리 식(라벨) | 논문 식/결과 | 행수 | 원문검증 |
|---|---|---|---|---|---|---|---|
| 1 | `br_bazant2013.tex` | bazant2013 | ch1_sec05_width.tex : eq:bv 블록(17–21) 직후, 22행 앞 | eq:bv·eq:db | 식[7][26][27][29] | 38 | **완료**(arXiv:1208.1587 HTML) |
| 2 | `br_dreyer.tex` | dreyer2010/2011 | ch1_sec07_broadening.tex : (iii-a) 문단(68–74) 직후, 76행 앞 | eq:Veq·eq:spinodal·eq:dUhys | 다입자 결과(구조) | 36 | 방법 검증 · **식 ★확인 필요** |
| 3 | `br_mckinnon1983.tex` | mckinnon1983 | ch1_sec02a_part0.tex : 156–161 직후, verifybox(162) 앞 | eq:sm-bare·eq:Veq | 격자기체 등온선(표준형) | 34 | 방법 검증 · **식 ★확인 필요**(단행본 장) |
| 4 | `br_weppner_huggins1977.tex` | weppner_huggins1977 | ch1_sec01_n0n1.tex : 측정원리 bgbox(204–218) 직후, 219행 앞 | eq:vn | GITT 준평형 OCV | 31 | 방법 검증 · D식 ★확인 필요(불요) |
| 5 | `br_baek_pilon2022.tex` | baek_pilon2022 | ch1_sec01_n0n1.tex : #4 스니펫과 인접(그 뒤) | ∂U_oc/∂T=ΔS/F | entropic potential 해석지도 | 30 | 방법 검증(제목/주제) · 유도식 없음 |
| 6 | `br_bernardi1985.tex` | bernardi1985 | ch2_sec07_revheat.tex : 두 전제 문단(22–25) 직후, 27행 앞 | eq:qrev | 일반 에너지 수지(항 대응) | 31 | 방법 검증 · **식번호 ★확인 필요** |
| 7 | `br_allart2018.tex` | allart2018 | ch2_sec09_method.tex : procedurebox(10–29) 직후, 31행 앞 | ΔS⁰_j=F dU_j/dT | 전극 분리 ΔS(x) 실측 | 29 | 방법 검증(제목) · 유도식 없음 |
| 8 | `br_reynier2003.tex` | reynier2003 | ch2_sec03_vibel.tex : jpcc2021 문장(33) 직후, 35행 앞 | eq:Svib_mode | 실측 ΔS(x) "second contribution" | 19 | 방법 검증(제목) · 유도식 없음 |

총 248행. 삽입 위치 8곳 전건 파일:행·앵커 문장 명기.

## 다리별 3요소 요지(스니펫 상세는 각 .tex)

### 1. bazant2013 → eq:bv (§5) — [원문 검증완료]
- ① χ/(1−χ) ↔ α_c=α/α_a=1−α(식[27]) · 𝒜_j=sF(V_n−U_j) ↔ neη=Δμ(식[26]) · k₀e^(−ΔG_a/RT) ↔ I₀/ne(식[29]) · r⁺/r⁻=e^(𝒜/RT) ↔ η=0서 I=0. 등치식 eq:br-bazant2013-1: 𝒜_j/RT = e·s(V_n−U_j)/k_BT ↔ neη/k_BT.
- ② 알짜 속도를 전이상태 excess μ 기준 지수차(식[7])로 적고 η=Δμ/ne 특수화 후 α 비대칭 분할 → 일반화 BV(식[27]).
- ③ 원 I₀(식[29])는 활동도계수 γ·γ‡ 로 전치인자 조성의존 / 우리는 조성무관 k₀e^(−ΔG_a/RT) 로 흡수(조성의존은 𝒜_j·logistic 만).

### 2. dreyer2010/2011 → eq:dUhys + (iii-a) (§4/§7)
- ① 비단조 V_eq,j(eq:Veq) ↔ 비단조 단일입자 μ · ξ_s^±(eq:spinodal) ↔ 준안정 가지 한계 · ΔU_j^hys(eq:dUhys) ↔ 영전류 잔존 갈림 · (iii-a) 공통전위 순차전환 ↔ 겉보기 평형.
- ② 다입자가 빠른 교환으로 공통 μ 공유 시, 비단조 등온선 위 순차 전환으로 겉보기 평형 평탄역 + 준안정 가지 갈림(히스).
- ③ 원 골격=공통 μ·size-blind·단일입자 등온선이 유일 원천 / 본문은 apparent-U=U_j+η 이질성(iii-b)을 별도 층으로, U_j=입자무관 상수, gap=spinodal 상한(eq:dUhys)으로 닫음.
- ★확인 필요: 원 논문 정확 닫힌식·식번호 미확인(방법=초록/본문 구조 검증) → 대응은 결과 구조 수준, 논문 식 재현 안 함.

### 3. mckinnon1983 → eq:sm-bare + eq:Veq (§2 Part 0)
- ① ⟨n⟩⁰(eq:sm-bare) ↔ 삽입분율 x · (RT/sF)ln[ξ/(1−ξ)] ↔ (kT/e)ln[x/(1−x)] · U_j ↔ E₀ · (Ω_j/sF)(1−2ξ) ↔ 평균장 상호작용 · Ω_j>2RT ↔ 1차 전이 임계.
- ② 삽입 자리를 격자기체로 보고 대정준(Langmuir형) 평형으로 등온선을 닫고, 평균장 상호작용이 임계 넘으면 1차 전이(전위 계단).
- ③ 원 원형=점유 0/1 만(내부자유도 없음) / 본문은 q(T)(eq:partfn)로 유효 자리에너지 온도이동 + 규칙용액 Ω_j spinodal 문턱 명시.
- ★확인 필요: 단행본 장(pp.235–304) 웹 원문 미확보 → 장내 식번호 미확인. 표준형 대응으로 제시.

### 4. weppner_huggins1977 → eq:vn (§1 bgbox)
- ① 목표 U_oc(x̄) ↔ 펄스후 완화 정지전위 · σ_d|I|R_n(eq:vn) ↔ 대기완화로 제거되는 IR·과전압 · 저율 연속곡선 ↔ 펄스-완화 이산점열.
- ② 정전류 펄스로 조성 한 걸음 옮긴 뒤 완화 정지전위를 읽어 준평형 OCV 점열(펄스중 √t 의존서 D 추출).
- ③ GITT=완전완화로 분극 0 / eq:vn=저율 연속곡선서 상수-저항 R_n 근사(R_n 조성·전류 의존 무시) — 연속 근사판.
- ★확인 필요(불요): D의 √t 식 정확형 미확인이나 본 다리는 U_oc 측정 대응이 핵이라 D식 불요.

### 5. baek_pilon2022 → 엔트로피계수 판독틀 (§1 bgbox / Part T)
- ① ∂U_oc/∂T=ΔS/F ↔ entropic potential ∂U/∂T · 단상폭/두-상 broadening/SOC 부호교대 ↔ 고용체/두-상/유형별 서명.
- ② entropic potential ∂U/∂T 부호·모양을 상전이 유형(고용체·질서화·두-상)별 열역학 서명으로 갈라 읽는 해석 지도.
- ③ 측정 해석 리뷰(tier B)라 미시 모형 비규정 / 본문은 유형 분류만 판독틀로, 부호·크기는 세 분포 합 + 1차문헌(reynier2003·allart2018) 병기로 확정.

### 6. bernardi1985 → eq:qrev (§2.7)
- ① I(U_oc−V) ↔ 반응 비가역 · −IT∂U_oc/∂T ↔ 반응 가역 엔트로피 · (소거) ↔ 혼합엔탈피 · (소거) ↔ 상변화 항.
- ② 셀 에너지 보존서 반응(가역+소산)·상변화·혼합·joule 을 모두 담은 일반 에너지 수지.
- ③ 원 수지는 혼합·상변화 항 명시 / eq:qrev는 준평형 저율(혼합 소거)·staging 열 U_oc 흡수(상변화 소거)로 두 항만(고율 잔여 부활) — 현행 22–25행과 취지 동일(★중복 주의: RISK 참조).

### 7. allart2018 → ΔS⁰_j 검증 (§2.9)
- ① ΔS⁰_j=F dU_j/dT ↔ 흑연 전극 몫 ΔS(x) 실측 · 회귀 U_j(T) 기울기 ↔ 평형곡선 U(x) 온도의존 · tab:ds ↔ ΔS(x) 부호·규모.
- ② 흑연 하프셀 평형곡선 + 온도계단 전위차 엔트로피곡선을 전위차 분석으로 함께 얻어 전극 몫 ΔS(x) 조성 분해.
- ③ Allart=조성연속 전극몫 실측 / tab:ds=전이별 봉우리 중심 표준값(내부 x-의존은 eq:single_config config 항 자동) → 중심값 부호·규모 수준 대조(점대점 아님).

### 8. reynier2003 → eq:Svib_mode 음 baseline (§2.3)
- ① S_vib(eq:Svib_mode) 포논 BE ↔ Reynier 측정 ΔS(x) 의 vib "second contribution" · ΔS_vib=∂S_vib/∂x 고-x 음 baseline ↔ 둘째 몫.
- ② 흑연 삽입 엔트로피·엔탈피를 온도의존 전위 측정으로 실측하고 ΔS(x)를 config 발산 + vib 음 baseline 으로 분해 해석.
- ③ Reynier=부호·추세 정성 분해(tier B) / 본문은 vib 를 포논 BE서 제일원리적으로 세워(eq:Svib_mode) 폭 안 T-무관 중심흡수 — 부호·스케일 앵커로만, 모드별 정량은 jpcc2021 소관.

## "확인 필요" 집계
- **원문 식 재현 관련 ★확인 필요 = 3건**: dreyer(정확 닫힌식·식번호) · mckinnon1983(단행본 장내 식번호) · bernardi1985(정확 식번호). 세 건 모두 **방법 요지(②)는 검증**됐고, 논문 식을 재현하지 않고 결과/항 대응 수준으로 제시(규칙 준수).
- 부수 ★확인 필요(다리 불요) = 1건: weppner_huggins1977 의 D √t 식(본 다리는 U_oc 측정 대응이라 D식 미사용).
- 검증 완료 = 1건: bazant2013(arXiv HTML 식[7][26][27][29] 대조).
- 유도식 없는 서술/량 대응 다리(★확인 필요 비해당) = 3건: baek_pilon2022·allart2018·reynier2003(논문 식 미재현, 방법=제목/주제로 검증).
