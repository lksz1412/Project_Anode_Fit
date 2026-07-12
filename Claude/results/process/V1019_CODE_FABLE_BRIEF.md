# Fable 브리핑 — 코드 개정(실현) v1.0.19 (doc-leads·문건→코드)

> 너(Fable)는 Anode_Fit **코드를 v1.0.19 문건(Ch1+Ch2)에 맞춰 개정(실현)**한다. **문건이 권위(authoritative)·코드가 그것을 실현**한다(doc-leads). 기존 코드는 물리가 이미 v1.0.19와 대체로 일치(문건이 물리 보존)하므로 **전면 재작성이 아니라 정합 개정**이다.

## 0. 원칙 (★코드 소유권·doc-leads)
- **사용자 원형 보존(불가침)**: 사용자 작성 함수·식별자·시그니처·정수/문자열 코드·데이터(`func_w`·`func_U_j`·`func_ksi_eq`·`func_L_q`·`func_U_branch`·`GRAPHITE_STAGING_LIT`·`LCO_MSMR_LIT` 등) **그대로**. 대소문자·명명 절대 변경 금지. 로직 임의 재작성 금지.
- **doc-leads**: v1.0.19 Ch1+Ch2 문건이 spec. 코드가 그 물리·수치를 **재현**해야 한다. 문건↔코드 불일치 시 **코드를 문건에 맞춘다**(단, 사용자 원형 로직은 보존 — 불일치가 진짜 물리 갭이면 최소 수정, 아니면 주석/버전/참조 정합만).
- **개정 = 정합**(전면 재작성 X): (a)버전/계보/근거문건/날짜 헤더 갱신 (b)docstring의 문건 절·식 참조를 v1.0.19 구조로 (c)검증에서 드러난 실제 doc↔code 갭만 최소 수정. 물리 로직은 이미 맞으면 건드리지 말 것.

## 1. 개정 대상 (헤더·참조 = 확정 / 물리 = 검증 delta 따라)
- **버전 헤더**(L3·L7): "release 버전 = **1.0.16**" → **1.0.19**. 계보에 1.0.17·1.0.18.1·1.0.18.2·1.0.19 추가(1.0.17=register 정련·1.0.18.2=제안1 vib Einstein·1.0.19=Ch1+Ch2 전면 재작성 정합). 날짜 갱신.
- **근거 문건**(L38): "graphite_ica_ch1_v1.0.16.tex(+ch2)" → **v1.0.19**.
- **파일명**: `Anode_Fit_v1.0.18.2.py` → **`Anode_Fit_v1.0.19.py`**(matched — master가 git mv 후 너는 내용 개정; 또는 네가 새 파일로 저장). 위치 `docs/v1.0.19/`.
- **docstring 문건 참조**: 코드가 인용하는 Ch1 식 라벨(eq:vn·eq:Uj·eq:dUhys·eq:Ubranch·eq:wbase·eq:xieq·eq:eqpeak·eq:chid·eq:Lqfull·eq:LV·eq:memory·eq:reversal·eq:sum·eq:lco-*·eq:dSegate·eq:U1T2·eq:qrev·eq:complete·eq:dxidT·eq:weighted·eq:hys_rev 등)은 **v1.0.19에서 보존됨(그대로 유효)**. 단 **Ch2 자체 eq:Se는 v1.0.19에서 `eq:Se-ch2`로 개명**됨 — 코드가 Ch2 eq:Se를 인용하면 갱신(Ch1 §15 eq:Se 인용이면 불변). 절 번호 인용(예 "Ch1 §N")이 있으면 v1.0.19 구조(Part0=Ch1 §2·U_j=§3·히스=§4·폭=§5·broadening=§7·전자엔트로피=§15·MSMR=§17 / Ch2 §2.1 분배함수·§2.4 vib Einstein·§2.7 가역발열·§2.8 종합식)로 정정.
- **물리 갭**(검증 delta): 아래 §2 검증 결과가 "재현 불가/불일치"로 지목한 항목만 최소 수정(doc→code). 없으면 물리 무변경.

## 2. 검증 delta (K-P0 Sonnet 독립 검증 결과)
**물리·수치 7항목 전부 정합**(코드 헬퍼 조합으로 재현): entropy_coefficient 완전식 −0.2039/단순식 −0.1340/config −0.0700·worked U_oc 74.35/Q̇_rev +60.81/ΔS −19.68·tab:qrev 5점(−0.307/−0.204/−0.089/+0.044/+0.218 mV/K·+91.5/+60.8/+26.6/−13.2/−64.9)·round-trip diff 0.000011µV/K·vib −3.74/0/+3.70/+9.14 µV/K·고온극한 수렴·**회귀 13/13 bit-exact(골든)**·tab:ds. → **물리 로직 무변경**(이미 정합).

**★ doc↔code API 갭 2건 = 개정 대상(순수 additive, 기존 함수·시그니처 불변)**:
- **(a) x̄→U_oc eq:implicit 솔버 부재(핵심·G-usable)**: Ch2 부록 B.1·§2.8(C-106 계산순서)이 **"코드가 전하보존 음함수 $\sum_j Q_j\,\xi_{eq,j}(U_{oc},T)=Q\bar x$(eq:implicit)를 풀어 $U_{oc}(\bar x,T)$를 얻고, 그로부터 $\partial U_{oc}/\partial T$·$\dot Q_{rev}$를 낸다"**를 구현 타깃으로 명시하나, 코드엔 x̄→U_oc 솔버·x̄ 진입점이 **없음**(현 `entropy_coefficient(V_n,T)`·`reversible_heat(V_n,T)`는 전위 V_n만 입력). → **추가**: (i) **eq:implicit 솔버**(기존 `func_ksi_eq`+전하보존 `Σ Q_j ξ_j=Q x̄`, U_oc 단조라 이분법/brentq — 신규 물리 없음, 기존 헬퍼 재사용) (ii) **x̄ 진입점 메서드**(x̄, T → U_oc, ∂U_oc/∂T, Q̇_rev). 기존 V_n 기반 메서드는 **그대로 보존**(additive 병행).
- **(b) 완전식/단순식 분리 출력 부재**: `entropy_coefficient`가 완전식(config 포함)만 반환. Ch2는 완전식(−0.204) vs 단순식(중심값만 −0.134)·config 몫(−0.070) 구분. → 단순식·config 몫을 꺼낼 수 있게(옵션 kwarg 예 `return_terms=True` 또는 companion). **기존 기본 반환(완전식) 불변.**

이 2건이 **문건 계산 파이프라인(x̄→가역발열)을 코드가 직접 실현(G-usable)** 하게 함. **물리는 이미 정합이므로 기존 함수 로직 무변경 — 순수 additive 신규 진입점만.** 검증 script(scratchpad `verify_v1019.py`)가 이분법 x̄→U_oc·config 분리를 이미 외부 재구성했으니 참고(그 로직을 코드 내부 메서드로 승격).

## 3. 필수 유지 (회귀·자기검증)
- **회귀 bit-exact**: θ_E·n(T) 미지정 시 골든(`golden_graphite_ref.npz`)과 완전 동일. __main__(L840) self-test `overall OK: True` 유지.
- **문건 수치 재현**: U(298) 0.085 등·dU_hys 86.7mV·entropy_coefficient −0.204·tab:qrev 5점·vib −3.74/+3.70/+9.14·round-trip <0.001µV/K.
- **PEP8·타입힌트**는 기존 코드 스타일에 맞춰(전면 리포맷 X — 원형 보존 우선). 개정 후 `PYTHONIOENCODING=utf-8 python Anode_Fit_v1.0.19.py` 실행해 self-test 통과 보고.

## 4. 자료 경로
- 코드: `docs/v1.0.19/Anode_Fit_v1.0.18.2.py`(개정 원본).
- 문건 spec: `docs/v1.0.19/_sections/ch1_*.tex`·`ch2_*.tex`(특히 부록 B 구현 대응·요구명세). Ch1 부록B(구현 대응표)·Ch2 부록B(코드 요구명세) = 코드가 만족할 기준.
- 자산: `V1019_ASSET_CHECKLIST.md`(Ch1)·`V1019_CH2_ASSET_CHECKLIST.md`(Ch2).
