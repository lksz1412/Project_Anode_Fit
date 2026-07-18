# AUD_REPORT_v23 — 코드↔문건 정합 적대적 검수 (v1.0.22 + v1.0.23, 5창)

> P5 마감. 사용자 요청 = 양 버전 빡세게 재검수(코드↔문건 상관관계 중점). 5창 병렬(general-purpose)·독립 재유도·게이트 실행.
> 판정 요약: **치명 0. 물리·수식·코드·게이트·서지 견고.** 중대 2건(부록 E 수치 증거 문장 과장/오귀속) = **수정 완료**. 나머지 경미/제안 = 수정 또는 accepted(근거 명시).

## 0. 버전 parity (AUD-5 독립 검증 + 마스터 확인)

v1.0.23 = v1.0.22 + {부록 E, 코드 3함수(_causal_memory_ratio·transfer_apparent_from_equilibrium·_lag_ratio_geff)+플래그+dqdv elif, §8 포인터 1문장, bib 3종}. **그 외 공유 본문·코드 byte-identical**:
- py diff = 위 추가분 + 버전문자열뿐. **공유 함수 본문 로직 변경 0**(AUD-5 diff).
- _sections: 벗어난 파일 정확히 3개(ch1_appE 신규·ch1_sec08_lag 포인터·ch1v22_bib 3종). 47개 공유 섹션 **sha256 동일**.
- 경험적: G1 v1.0.23 vs v1.0.19 `np.array_equal=True max|d|=0.0`; G-E2 ratio ON==OFF array_equal.
→ **공유부 검수 결과는 두 버전 모두에 적용.** parity 순수 additive 확정.

## 1. 창별 판정

| 창 | 범위 | 판정 | 치명 | 중대 | 경미/제안 |
|---|---|---|---|---|---|
| AUD-1 | 흑연 커브사슬 §0–10 ↔ 코드 | 정합 | 0 | 0 | 3(경미2·제안1) |
| AUD-2 | Part T 열특성 ↔ 코드 | 정합 | 0 | 0 | 2(경미1·제안1) |
| AUD-3 | LCO+Si/블렌드 ↔ 코드 | 정합 | 0 | 0 | 3(경미1·제안2) |
| AUD-4 | **부록 E ↔ ratio/transfer 코드**(신규·최고강도) | 중대→수정후 정합 | 0 | 2 | 5(경미2·제안3) |
| AUD-5 | 검수7항+parity+서지 | 정합 | 0 | 0 | 4(경미2·제안2) |

## 2. 핵심 정합 확인 (독립 재유도·수치 재현)

- **식↔코드 1:1 EXACT** (AUD-1): eq:vn/Uj/dUhys/Ubranch/wbase/xieq/eqpeak/chid/Lqfull/LV/dHeff/lag/reversal/sum + Acut/peakshape/tail-limit — 부호·계수·지수·분모 전건 일치. 인과기억 점화식 = eq:lag 해석적분과 완전 동일 증명.
- **g_eff 독립 재유도** (AUD-4): `∂ln L_V/∂ξ = −2χ_d(Ω/RT)` 를 §8 eq:kuniv·dHeff 에서 독립 유도 → eq:sc-true·코드 L_loc·g_eff 부호·계수·(1−ξ) 방향 **전부 일치**. 충전 거울대칭이 진행률 규약(s=σ_d·χ→1−χ)으로 자동 처리됨까지 확인. **양방향 정확.**
- **G2 열특성 회귀값 독립 재계산** (AUD-2, 게이트 미의존): U_oc(0.25)=74.35mV·complete −0.204·simple −0.134·config −0.070·ΔS=−19.7·Q̇_rev/I=+60.8 — 문건 명기값 재현. solve_U_oc=eq:implicit·vib Einstein bit-exact·Sommerfeld S_e 정합.
- **블렌드/LCO** (AUD-3, 수치 검산): C-052 f_Si 환산·R6-G1 bit-exact·eq:lco-sigmaslot/decomp/ggate·func_dSe_molar −45.7 J/mol/K — 전건 일치. **"0~30% 실측 커버" 과장 없음**(문건이 [0,20]연속+30단일점+(20,30)보간으로 정직 한정·GS-2 경고).
- **서지 무날조** (AUD-4·AUD-5, 원문·웹 대조): lee2017jcp DOI 10.1063/1.5000882·제목 원문 일치. lee2011/son2013 실재(son2013 실 DOI 10.1063/1.4802584 웹확인)·미확보분 "원문 대조 확정" 정직 유보. **dangling 라벨 0**(코드 인용 59/59 정의됨).
- **검수 7항** (AUD-5): 전항 PASS(V_n 위계·전하보존 중심식·순환의존 4분류·ref 5항·전달식·명칭).
- **게이트 실행 재현** (AUD-4): G-E1 max|x1−x0|=0·G-E2 array_equal·전달함수 수학·정직 프레임(계산절감 철회) 확인.

## 3. 중대 findings → 수정 완료 (부록 E 수치 증거 문장)

물리 오류 아님 — **커밋 안 된 scratchpad 스크립트 수치를 커밋 스크립트로 오귀속/과장**. 커밋·재현 가능 수치로 정정.

| ID | 위치 | 문제 | 마스터 검산 | 수정 |
|---|---|---|---|---|
| **AUD-4 F-1** | appE derivbox | "p1_ratio_check.py: g=0 서 ~10⁻⁸" — 실제 그 커밋 스크립트는 **정확히 0** 산출(~1e-8은 scratchpad RK4 산물) | p1_ratio_check.py 실행: g=0 → err_0=err_1=**0.0** 확인 | "‖r₁−r₀‖=0(기계정확·항등환원)+ε 반감 시 err₀→½·err₁→¼" 로 정정(진값이 더 강한 증거) |
| **AUD-4 F-2** | appE E.5 | "FFT ~10⁻⁹ 기계정밀" — 커밋 게이트 G-E4 실측은 **3.96e-6**(1e-9는 FFT 왕복 자기정합 artifact) | G-E4 실행: rel RMS **3.96e-6** 확인 | "커밋 게이트 G-E4: 전달함수가 동결 인과합성곱을 rel RMS 3.96×10⁻⁶ 로 재현" 로 정정 |

## 4. 경미/제안 → 수정 또는 accepted

**수정 완료(v1.0.23):**
- AUD-4 F-3(warnbox "3–10×"→**"2–10×"** 정직 하한) · F-4("일치한다"→**"정합한다(계수 ~1.5 내)"**+커밋 수치) · F-6(E.1 **충전 거울대칭 1문장 추가**) · F-7(G-E4 허용오차 5e-3→**1e-4** 회귀감지력↑).
- AUD-1 F-1(appB 코드파일명 v1.0.21→**v1.0.23**·코드헤더 release 버전 1.0.21→**1.0.23**·test_gates_v1021→**v1023**) — stale 버전 라벨 정정(P0 클론 누락분).
- AUD-3 F-1(코드 f_Si 라벨 "0.7"→**"0.8"**[sic 0.78 명기]) — 자기 기본케이스 과소표기 정정.

**Accepted(수정 안 함 — 근거):**
- **AUD-2 F-1**(mixing.tex "해석 상한 0.21" vs shipping 그리드 0.227): **마스터 검산 = 결함 아님.** 원출처 `42_numerical_verification.md`(V∈[0.03,0.35] 2만점)가 config 범위 [−0.210,+0.139]·최대 ±0.21 로 정의 → 문건이 충실히 인용+"z_j 로그 발산·스팬 의존" 명시 hedge. AUD-2의 0.227은 다른 그리드(x̄∈[0.05,0.95]) 끝점값으로 그 hedge가 이미 커버. 공유 본문 parity 보존 위해 무수정.
- AUD-4 F-5(G-E3 자기참조 Picard): 순환이나 vacuous 아니고 docstring 정직 공시·O(ε²) 독립검증은 p1_ratio_check.py 에 존재. 유지.
- AUD-1 F-2("원문 그대로" N2 축약)·F-3(tab:symcode 배치)·AUD-3 F-2(phantom appendix)·F-3(LCO Ω 미배정 정직표기)·AUD-2 F-2(LCO S_e 동결 라벨)·AUD-5 F-1(V_{n,·} 하첨자 미사용·물리구분 보존)·F-2(순환의존 분산표시)·F-3(Ref번호 유보)·F-4(버전bump 투명): 전부 결함 아닌 관찰 또는 정직 표기됨.

## 5. 수정 후 재검증

- ch1 3-pass 재빌드: **err0·undef0·87p**.
- 기존 게이트: **G1 bit-exact=True(max|d|=0.0)**·G2/G3/n(T)/R6 exit0 (수정=주석·문자열이라 로직 무영향).
- 신 게이트: G-E1~E5 **5/5 PASS**(G-E4 tightened 1e-4 서 3.96e-6 통과).

## 6. 결론

**양 버전 코드↔문건 상관관계 = 견고(치명 0).** 물리·수식·코드·게이트·서지·parity·검수7항 전부 정합. 신규 부록 E 의 수치 증거 2문장 과장은 커밋·재현 수치로 정정 완료(밑바탕 주장은 참). 잔여는 전부 정직 표기된 관찰. **v1.0.23 병합 준비 완료.**

<!-- 자산(AUD_REPORT): [AU-01 5창 치명0·물리수식코드 EXACT] [AU-02 parity 순수additive 독립확인] [AU-03 g_eff 독립재유도 양방향 정확] [AU-04 G2/블렌드/서지/검수7항 정합] [AU-05 중대2=수치증거 과장→커밋수치로 정정] [AU-06 AUD-2 F-1 결함아님 마스터검산] [AU-07 stale버전라벨 정정] [AU-08 수정후 GREEN·G1 bit-exact·신게이트5/5] -->
