# v7-11 D-PEAK 정정 (2026-06-30)

> `PHASE7_FINAL_RESULT.md`(v7 종합)은 v7-11 을 최종으로 보고했으나, 이후 **v8 런의 G-derive 렌즈가 v7-11 의 유도 서술 오류(D-PEAK)를 적발**. 결과 문건 보호상 RESULT 는 덮지 않고 본 정정 노트로 기록하며, 산출물 `v7-11.tex` 는 정정한다(사용자 지시 "7-11 정정하자", 2026-06-30).

## 무엇이 틀렸나 (§sec:tail, eq:peakshape 직후)
틀린 서술: "$L_V$ 가 작으면 $\xi_\mathrm{lag}\to$ 한 칸 뒤처진 $\xi_\eq$ 라 식~\eqref{eq:peakshape} 가 미분 $\dd\xi_\eq/\dd V$ 의 종으로 환원된다 — 곧 평형 peak 로 돌아간다."
- **수학적으로 거짓**: 점화식 $\xi_{\mathrm{lag},i}=\rho\xi_{\mathrm{lag},i-1}+(1-\rho)\xi_{\eq,i}$, $\rho=e^{-\Delta_\mathrm{grid}/L_V}$ 에서 $L_V\to0\Rightarrow\rho\to0\Rightarrow\xi_\mathrm{lag}\to\xi_\eq$(같은 칸)이라 $(\xi_\eq-\xi_\mathrm{lag})/L_V\to0/0\to0$(종 아님).
- 매끈한 종 환원은 **반대 극한 $L_V\gg\Delta_\mathrm{grid}$**($\rho\to1$).
- 작은 $L_V$ 평형 회복은 매끈한 극한이 아니라 **코드의 이산 분기 스위치**(`eq:branch`, $L_V<\nu\Delta_\mathrm{grid}$)가 담당 — 문턱서 두 분기 진폭이 정확히 같지 않아 작은 불연속이 있을 수 있는 수치 안정용 모드 전환.

## 정정 (v7-11.tex)
위 거짓 서술을 삭제하고 올바른 두-극한 + 분기 스위치 + 문턱 불연속(정직) 기술로 교체. 결과 박스(eq:peakshape·eq:branch)·부호·코드 정합·다른 문장은 불변. 빌드 3-pass 0-error·17p 재확인.

## 비고
- 동일 결함이 v8 초본 8/9 에 상속됐고(v8 KNOWN_DEFECTS D-PEAK), v8-11 은 처음부터 정정 반영.
- 이 정정 자체가 **경쟁·체리픽 방법의 효용 사례**: v7 의 1패스 검토가 통과시킨 유도 오류를 v8 의 더 깊은 G-derive 렌즈가 적발 → v7 로 소급 정정.
