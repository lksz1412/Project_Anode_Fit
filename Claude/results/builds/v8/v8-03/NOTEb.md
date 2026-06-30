# v8-03b 보완 노트 (2026-06-29)

## 산출물
- `v8-03b.tex` — v8-03 증분 보완판 (원본 v8-03.tex 불변)
- `v8-03b.pdf` — xelatex 2-pass, 0 error

---

## 보완 5개 요약

### (1) D-PEAK 정정 — eq:branch 스위치 역할 명시 (N8 절)
**오류**: "L_V 가 작으면 종으로 환원"이라는 설명이 'L_V→0 ⇒ peak→0'으로 읽힐 여지.
**정정**: L_V→0은 peak를 0으로 만들지 않는다. 매끄러운 평형 환원은 연속적으로 일어난다.
eq:branch 스위치의 실제 역할은 **수치 불안정 방지** — 분모 L_V ≈ 0일 때 평형 종으로 대체.
관련 수정: (a) N8 절 본문 재서술 + 이탤릭 명시, (b) verifybox R3 정정 주석 추가.

### (2) D-VEQ — eq:Veq 앞 sF(V_eq−U)=g'(ξ) 다리 추가 (N3 절)
eq:Veq 직전에 eq:gder(g'(ξ) = RT ln[ξ/(1−ξ)] + Ω(1−2ξ)) 추가,
평형 조건 sF(V_eq−U)=g'(ξ) 경유 inline 유도 → eq:Veq forward-defer 제거.

### (3) D-DHEFF — χ_d 계수 중간식 보강 (N7 절)
χ_d 정의(eq:chid) 뒤, eq:dHeff 앞에:
방전 꼬리(ξ→1)와 충전 꼬리(ξ→0)에서 A_j가 동일 극한으로 수렴함을 보이고,
Ω_j가 전진 장벽을 χ_d·Ω_j 낮춘다는 BEP 상수 몫 흡수 과정 명시.
χ=0.5 대칭·비대칭 꼬리 폭 효과 설명 추가.

### (4) D-WEFF — 중심기울기 4Fw 다리 추가 (N4/N5 절)
eq:weff 앞 서술을 개조: g''(ξ)|_{ξ=1/2} = 4RT−2Ω 로부터 이상 중심기울기가
(4RT−2Ω)/RT 배로 줄어 등가 폭 w_eff = (RT/F)(1−Ω/2RT) 가 된다는 유도 다리 추가.
spinodal 문턱 u_j→0 정합도 명시.

### (5) orphan fig:logistic·fig:reversal 본문 \ref 보강
- **fig:logistic**: signbox 뒤에 "그림~\ref{fig:logistic} 이 ξ_eq(z) logistic…" 문장 삽입.
- **fig:reversal**: eq:reversal 설명 뒤에 "그림~\ref{fig:reversal} 이 방전과 충전의 꼬리 방향을…" 문장 삽입.

---

## 부호 8항 재확인 (S1–S8)
v8-03 원본의 S1–S8 전건이 v8-03b 수정 후에도 유지됨:
- S3 (peak 양수) + S7 (충전 거울·양수): D-PEAK 정정으로 혼동 없이 강화됨.
- 나머지 S1·S2·S4·S5·S6·S8: 변경 없음. 전건 정합 ✓

## 새 회귀 self-test
기존 R1–R4 유지. R3 표현 개선: "L_V→0 ⇒ eq:branch 스위치가 평형 종 선택, peak≠0 정정" 명시.

## build
xelatex 2-pass (kotex), pass1 errors=0, pass2 errors=0.
