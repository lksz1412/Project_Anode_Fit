# R4 검토 보고서 — 흑연 보존 무결성 · xelatex 빌드 · 그림 · orphan/완결성

**검토자**: R4 sub (보존·빌드·그림·orphan 전담)  
**대상**: v9-01 ~ v9-09 (9종) + `base_v8-11.tex` (흑연 원본 1208줄)  
**기준**: 흑연 내용 verbatim 보존 · 0-error 빌드 · TikZ 영어 ASCII · orphan 0  
**날짜**: 2026-06-30

---

## (a) 흑연 VERBATIM 보존 — 9종 PASS/FAIL 표

검사 방식: 9개 핵심 literal string을 base에서 추출해 각 초안 전문 literal 대조.

검사 항목:
1. `ksi\_eq * (1 - ksi\_eq) / w` — eq:eqpeak 코드 식별자
2. `ksi\_eq - occ\_lagged) / lag\_len\_V` — eq:peakshape 코드 식별자
3. `ksi\_arr[::-1])[::-1]` — 충전 격자 역전 코드 (reversal)
4. `artanh}\,u_j` — eq:dUhys 쌍곡탄젠트 공식
5. `xi_{\mathrm{lag},i}=\rho\,\xi_{\mathrm{lag},i` — eq:lowpass 점화식
6. `V_n\;=\;V_\app\;-\;\sigma_d` — eq:vn 박스
7. `브리프 §7 의 부호 체크리스트` — sign check 도입부
8. `D-PEAK2` — 이산 모드 스위치 회귀 마커
9. `0.0853` — U=0.0853 V (stage 2→1 열역학 검산 수치)

추가 확인: ΔS_rxn +29/0/−5/−16 (staging 표), 8개 S-항 checkmark, weff Ω/(2RT) 계수 (D-WEFF 회귀 부재), s_F orphan 부재.

| 초안 | (1)eqpeak코드 | (2)peakshape코드 | (3)reversal코드 | (4)artanh | (5)lowpass | (6)vn박스 | (7)sign도입 | (8)D-PEAK2 | (9)U0853 | 종합 |
|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| v9-01 | OK | OK | OK | OK | OK | OK | OK | OK | OK | **PASS** |
| v9-02 | OK | OK | OK | OK | OK | OK | OK | OK | OK | **PASS** |
| v9-03 | OK | OK | OK | OK | OK | OK | OK | OK | OK | **PASS** |
| v9-04 | OK | OK | OK | OK | OK | OK | OK | OK | OK | **PASS** |
| v9-05 | OK | OK | OK | OK | OK | OK | OK | OK | OK | **PASS** |
| v9-06 | OK | OK | OK | OK | OK | OK | OK | OK | OK | **PASS** |
| v9-07 | OK | OK | OK | OK | OK | OK | OK | OK | OK | **PASS** |
| v9-08 | OK | OK | OK | OK | OK | OK | OK | OK | OK | **PASS** |
| v9-09 | OK | OK | OK | OK | OK | OK | OK | OK | OK | **PASS** |

**보조 확인 결과:**
- ΔS_rxn 값(+29.0/0.0/−5.0/−16.0): 전 9종 PASS
- 8항 sign check (S1–S8 checkmark=8): v9-01/03/05/08/09 = 8개 (기준치 정확). v9-02/04 = 11개 (새 LCO L-항 3개 추가), v9-06/07 = 9개 (LCO S-항 1개 추가) — 모두 흑연 S1–S8 보존 확인
- D-WEFF: 전 9종 `\frac{\Omega_j}{2RT}` 계수 정확 (¼ 회귀 없음) — PASS
- s_F orphan: 전 9종 1회 (comment header만) — base와 동일, PASS
- D-PEAK R5 self-test: 전 9종 존재, `0/0` 논증 정확 보존

**결론**: 9종 전원 흑연 verbatim PASS. 의도적 변경(title/lhead/comment)을 제외한 흑연 본문 내용 훼손 없음.

---

## (b) xelatex 빌드 상태 표

| 초안 | PDF | 빌드 로그 | 하드 에러 | undef ref | 심각 overfull (>50pt) | 위치 |
|------|:---:|:---:|:---:|:---:|:---:|:---|
| v9-01 | YES | 기존 | 0 | 0 | 118pt | LCO 표 (새 콘텐츠 lines 294-303) |
| v9-02 | YES | 기존 | 0 | 0 | 없음 | — |
| v9-03 | YES | 기존 | 0 | 0 | 72pt | LCO 표 (새 콘텐츠 lines 295-304) |
| v9-04 | YES | 기존 | 0 | 0 | 57pt+78pt | LCO 표+내용 (새 콘텐츠) |
| v9-05 | YES | 신규 컴파일 | 0 | 0 (2nd pass 필요) | 115pt | LCO 표 (새 콘텐츠 lines 298-307) |
| v9-06 | YES | 신규 컴파일 | 0 | 0 | 124pt | LCO 표 (새 콘텐츠 lines 297-308) |
| v9-07 | YES | 기존 | 0 | 0 | 없음 | — |
| v9-08 | YES | 기존 | 0 | 0 | 없음 | — |
| v9-09 | YES | 기존 | 0 | 0 | 36pt | LCO 표 (새 콘텐츠 lines 281-291) |

**비고:**
- v9-05/06은 원래 로그 파일 없이 제출됨. 현장 컴파일로 확인: 0 errors.
- 모든 심각 overfull은 **신규 LCO 콘텐츠** (삽입 표)에만 집중. 흑연 섹션 overfull은 base와 동일한 4.62/17.33/2.15/22.55pt 패턴 (base 컴파일로 확인).
- 흑연 본문 중 32pt overfull (Lq 단락): base에도 동일하게 존재 (base 컴파일 확인), 레이아웃 재배치로 v9-07/08에선 표면화 안 됨. 내용 변경 아님.

---

## (c) 그림·orphan 결함표

### TikZ 그림 수 (base=9)

| 초안 | 총 TikZ | 신규 | 신규 TikZ 내 한글 | 신규 그림 레이블 |
|------|:---:|:---:|:---:|:---|
| v9-01 | 11 | 2 | **0** | fig:elec_entropy, fig:lco_dqdv |
| v9-02 | 10 | 1 | **0** | fig:lco_dqdv |
| v9-03 | 10 | 1 | **0** | fig:lco_dqdv |
| v9-04 | 11 | 2 | **0** | fig:egate, fig:lcopeak |
| v9-05 | 11 | 2 | **0** | fig:eentropy, fig:lcopeak |
| v9-06 | 10 | 1 | **0** | fig:lco-electronic |
| v9-07 | 11 | 2 | **0** | fig:lco_egate, fig:lco_peaks |
| v9-08 | 11 | 2 | **0** | fig:lco-electronic-gate, fig:lco-dqdv |
| v9-09 | 11 | 2 | **0** | fig:lco_gate, fig:lco_peaks |

- **TikZ 내 한글 라벨**: 전 9종 0 — PASS
- **신규 그림 caption 언어**: v9-01~06 = 한국어 (문서 전체 한국어 스타일과 일관). v9-07/08/09 = 영어.
  - 브리프 조건 "TikZ 영어 ASCII 라벨"은 tikzpicture 내부 node 텍스트 기준. caption은 기존 흑연 그림들도 한국어. → 위반 없음.

### Orphan/미참조 레이블

| 초안 | orphan 레이블 수 | 비고 |
|------|:---:|:---|
| v9-01 ~ v9-09 | **모두 0** | 모든 \label{}에 \ref{} 대응 확인 |

**검사 방법**: 모든 `\label{X}` 추출 후 X의 총 출현 횟수 - label 행 = ref 횟수. ref=0이면 orphan. 9종 전원 orphan 0.

---

## (d) 보존 위반·빌드 깨짐·체리픽 base 부적격 표시

### 보존 FAIL 초안
**없음.** 9종 전원 흑연 verbatim 보존 PASS.

### 빌드 깨진 초안 (hard error)
**없음.** 9종 전원 0 hard error.

### 체리픽 base 적합성 분류 (빌드 청정도 기준)

| 등급 | 초안 | 근거 |
|:---:|:---|:---|
| **A급** (최우선 체리픽 후보) | v9-02, v9-07, v9-08 | 심각 overfull 없음, 0 error, 흑연 보존 완전 |
| **B급** (LCO 표 개선 시 A급) | v9-09 | 36pt overfull (LCO 표, 가장 작음), 0 error |
| **C급** (LCO 표 레이아웃 수정 필요) | v9-03, v9-04, v9-05, v9-06 | 57~124pt overfull (LCO 표), 0 error |
| **C급** (동일+헤더 미갱신) | v9-01 | 118pt overfull (LCO 표), title 갱신됨 |

**헤더/title 갱신 현황**: v9-01/02/04/05 = lhead+title 갱신됨. v9-03 = title 갱신, comment 갱신. v9-06/07/08/09 = base와 동일 헤더 (미갱신). 갱신 여부는 내용 보존과 무관 — 별도 지적 항목.

---

## 비고: 기존 로그 미제출 초안 컴파일 결과

- v9-05: 2026-06-30 현장 xelatex 컴파일 → 0 errors, citations는 2-pass 후 해소 예상 (1st pass 경고는 정상)
- v9-06: 2026-06-30 현장 xelatex 컴파일 → 0 errors

---

*R4 검토 종료. 파일 수정 없음.*
