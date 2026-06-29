# Ch2 v3 — 검토 요약 (교수님 면담용 1–2p)

## 한 줄
흑연 음극 $dQ/dV$(Chapter 1)의 평형 전위 $U_j(T)$ 에서, **가역(엔트로피) 발열**을 1차 문헌 근거 위에 끌어낸 Chapter 2 초안(v3).

## 무엇을 했나
Chapter 1 은 흑연 staging 전이별 평형 중심 $U_j(T)=(-\Delta H_{\rxn,j}+T\,\Delta S_{\rxn,j})/F$ 를 가졌다.
이를 온도로 미분하면 $\partial U_j/\partial T=\Delta S_{\rxn,j}/F$ — 곧 **각 전이의 엔트로피 계수가 그 반응
엔트로피**다. Bernardi 에너지 수지에서 가역 발열은 $\dot Q_\rev=-I\,T\,\partial U/\partial T$ 이므로,
$$\text{다온도 } dQ/dV \;\to\; U_j(T)\;\to\;\Delta S_{\rxn,j}\;\to\;\dot Q_\rev$$
의 사슬이 선다. 이 사슬을 광범위 문헌(Bernardi 1985, Newman 교과서, Reynier/Yazami 2003, Allart 2018,
MSMR 2024, calorimetry, 히스 2018)으로 근거화하고 초안을 작성했다.

## 핵심 결과 (검증된 것)
1. **부호 규약 확정**(다출처 일치): $\Delta S=+nF\,\partial U/\partial T$, $\dot Q_\rev=-I\,T\,\partial U/\partial T$.
2. ★**Chapter 1 의 엔트로피 값이 문헌과 정량 일치**: Ch1 의 전이별 $\Delta S_{\rxn,j}$
   ($+29\to0\to-5\to-16$ J\,mol$^{-1}$K$^{-1}$)가 측정된 흑연 엔트로피 프로파일(Allart 2018)의
   양 끝($+29$@저-$x$, $-16$@$x>0.5$)과 정확히 대응 — Chapter 1 의 입력이 임의값이 아님을 뒷받침.
3. **가역 발열의 부호 교대**: 저-$x$ 양$\Delta S$(방전 발열)↔고-$x$ 음$\Delta S$(흡열), stage 2$\to$1
   ($x\approx0.5$)의 큰 음$\Delta S$ 가 두드러진 신호.
4. **두 엔트로피 구분**: 가역 발열엔 \emph{반응} 엔트로피 $\Delta S_{\rxn}$ 만 들어가며, Chapter 1 동역학
   꼬리의 \emph{활성화} 엔트로피 $\Delta S_a$ 와 별개(혼동 금지).

## 정직한 공백·질문 (교수님 의견 구함)
- ★**핵심 기여 지점**: 문헌은 대부분 $OCV(T)$ 직접 측정 또는 MSMR 로 엔트로피 계수를 얻는다. 우리는
  Chapter 1 의 \emph{전 전이 $dQ/dV$ 모델을 다온도로 동시 피팅}해 peak 이동에서 전이별 $\partial U_j/\partial T$
  를 뽑으려 한다 — 직접 선례가 약한 신규 각. **이 경로가 타당한지, 정확도/식별성에 함정은 없는지** 의견을
  구합니다.
- $dQ/dV \to$ 부분몰 $\Delta S/\Delta H$ 의 가장 근접 prototype(Electrochim. Acta 2019)은 dilute 한계($x<0.1$)
  이고 원문(유료) 미확보 — 고-$x$ 적용·모델 식 확장이 과제.
- 히스테리시스 하 "가역" $\partial U/\partial T$ 의 경로의존 불확실도 정량.
- 형성 엔탈피(calorimetry)↔전이별 반응 엔탈피 환산.

## 다음
교수님 검토 후 — (i) prototype 식 확보·확장, (ii) 실데이터 다온도 $dQ/dV$ round-trip 으로 추정 정확도 실증,
(iii) Chapter 1+2 의 v9 통합(가역/비가역 발열을 한 인과 사슬로).

## 산출물 위치
- 초안: `Claude/docs/graphite_ica_ch2_v3.tex` (5p, xelatex 0-error).
- 조사 근거: `Claude/research/CH2_v3/`(범위·출처·추출카드·Ch1 정합·종합·갭).
