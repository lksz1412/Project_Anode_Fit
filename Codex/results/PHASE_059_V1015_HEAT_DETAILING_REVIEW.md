# Phase 059 v1.0.15 Ch2 heat 상세화 독립 판정

정본일: 2026-07-28

판정: `CONDITIONAL_P059_V1015_HEAT_WORKED_EXAMPLE_NUMERICALLY_CLOSED_BUT_NO_NEW_HEAT_PHYSICS_AND_SIGN_API_BOUNDARY_REMAINS`

## 결론

v1.0.15 Ch2의 핵심 추가분은 새 열물리 구현이 아니라 기존
상수-\(n\), \(w=nRT/F\) 식의 worked explanation이다. Ch2 exact
diff는 +99/-7
행이고, 생산 코드의 `func_U_j`, graphite/LCO entropy seam,
`entropy_coefficient`, `reversible_heat`, `irreversible_heat` 실행
AST는 v1.0.14와 전부 동일하다.

추가 예제의 대수와 수치는 보존한다. \(\bar x=0.25\),
\(T=298.15\) K에서 독립 계산은
\(U_{oc}=74.351\) mV,
\(\partial U/\partial T=-0.203946\)
mV/K, \(\Delta S=-19.678\)
J mol\(^-1\) K\(^-1\),
\(\dot Q_{rev}/I=60.806\) mV를 낸다.
해석 가중식, 생산 함수와 \(T\pm3\) K 음함수 유한차분은 최대
9.681e-11
V/K 안에서 일치한다.

## 새 물리와 설명의 경계

- 새로 추가된 실제 물리 내용은 진동 엔트로피의 고전극한 흡수와
  준양자 잔여 \(T\)-의존에 대한 caveat다. oscillator spectrum이나
  잔여항은 식·코드에 추가되지 않았다.
- 완전식의 config 항은 상수 \(n\)인 열적 폭 \(w=nRT/F\)를 선택한
  결과다. 폭을 \(T\)-동결하면 그 항은 사라지고 중심값 가중식으로
  돌아간다. 따라서 두-상 흑연의 물성 사실이 아니라 다온도
  round-trip으로 선택해야 할 model branch다.
- 표와 round-trip은 demonstration prior에 대한 내부 자기일관성이다.
  흑연 calorimetry 또는 다온도 실험 피팅의 외부 검증이 아니다.

## quantity·reference·sign

문건이 선언한 graphite-vs-Li 하프셀 범위 안에서는 같은 quantity를
사용한다. \(\bar x\)는 탈리튬화 분율이고,
\(F\,\partial U_{oc}/\partial T\)는 해당 Li-reference half-cell
반응 엔트로피이며, \(I>0\)은 하프셀 방전/graphite lithiation
전류다. 이 좌표에서는
\(\dot Q_{rev}=-I T\,\partial U_{oc}/\partial T\)가 예제와
생산 함수에서 일치한다.

그러나 curve API의 `direction="discharge"`는 graphite
delithiation을 뜻한다. 문건과 docstring이 두 discharge 라벨의 반대
화학 방향을 공개했지만 `reversible_heat(..., I)`는 이 반응 좌표를
타입이나 state로 강제하지 않는다. full-cell 방전으로 옮길 때
\(U_{cell}=U_{cat}-U_{an}\)이므로 graphite 몫은
\(+I_{cell}T\,\partial U_{an}/\partial T\)이고, 총열은 cathode
계수까지 있어야 한다. graphite-only 표를 full-cell 총열로 읽으면
안 된다.

v1.0.14 LCO 감사의 reference, DOS gate, 조성 의존과 \(T^2\) 곡률
blocker는 heat AST가 동일하므로 하나도 수리되지 않았다.

## 인용 권위와 본문 경계

Hales–Bulman 2024(DOI `10.1149/1945-7111/ad4918`)는 full-cell entropy
coefficient의 표준 potentiometric 추출법을 지지한다. 이 문헌은
현재 4-transition graphite prior의 \(+60.8\) mW/A 부호·규모를
실험 검증하지 않는다. 따라서 해당 문장의 “calorimetry 관측과
정합”은 구체적 외부 검증 주장으로는 기각한다.

또한 새 worked section은 생산 코드와 함수명을 직접 두 번 언급한다.
사용자의 “이론 문건 본문은 물리·화학만, 코드 언급은 통제 절에만”
제약을 통과하지 못한다. 최종 이론 정본에서는 독립 수치 검산으로
서술하고 코드명은 제거해야 한다.

## 다음 단계

Step 37.4에서 v1.0.16의 \(n(T)=n_0+n_1(T-T_{ref})\)를 microscopic
물리가 아닌 empirical width law와 분리하고,
\(\partial w/\partial T=(R/F)(n+Tn')\), entropy propagation,
positivity와 parameter correlation을 검산한다.

원본 `Claude/`, `main`은 수정하지 않았다.
