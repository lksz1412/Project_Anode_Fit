# V1.0.14 P2.2 Step 12 — 코드-측 eq 참조 보강 (Anode_Fit_v1.0.14.py)

- 대상: `D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.14\Anode_Fit_v1.0.14.py` (899 lines, 전문 정독 완료: head→tail 2-pass, offset 0-718 / 719-900)
- 근거 문건: `D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.14\graphite_ica_ch1_v1.0.14.tex` (+ ch2, 동일 폴더) — 모든 대상 eq 라벨을 `\label{eq:...}` grep 으로 원문 대조 후 추가(추측 삽입 없음).
- 방침: 문건→코드 단방향 참조. **누락분만 채움**, 기존 eq 참조·주석·코드 로직은 삭제·변경 없음(추가만).
- 수정 = 주석·docstring 텍스트만. 실행 코드(로직·시그니처·상수·공백)는 git diff 로 대조 확인 — 변경 라인은 전부 `#`/`"""` 텍스트 추가뿐.

## 커버리지 표

| 함수/메서드 | 기존 참조 | 추가 참조 | 비고 |
|---|---|---|---|
| `func_w` (원형보존 블록) | 없음(파일 헤더에만 간접 언급) | eq:wbase | 함수 첫 줄에 주석 삽입(func_U_j_hys 선례와 동일 패턴), 반환식 불변 |
| `func_U_j` (원형보존 블록) | 없음 | eq:Uj | 상동 |
| `func_ksi_eq` (원형보존 블록) | 없음 | eq:xieq | 상동 |
| `func_L_q` (원형보존 블록) | 없음 | eq:Lqfull | 상동 |
| `_causal_lowpass` (원형보존 블록) | 없음 | eq:lowpass (+ 호출부 eq:reversal 안내) | 상동 |
| `func_U_j_hys` (원형보존 블록, orphan) | 없음 | **[미배정]** | 사용자 제공 매핑 표에 미포함(현재 미호출 orphan). func_dU_hys/func_U_branch 와 동등물리라는 기존 서술은 있으나 eq 라벨(eq:dUhys/eq:Ubranch)은 그 두 활성 함수 쪽에 이미 있어, 범위 밖으로 보고 건드리지 않음 |
| `func_dU_hys` | eq:dUhys | (유지) | 이미 충족 |
| `func_U_branch` | eq:Ubranch | (유지) | 이미 충족 |
| `func_dH_a_eff` | eq:dHeff | (유지) | 이미 충족 |
| `func_chi_d` | eq:chid | (유지) | 이미 충족 |
| `_chi_and_dH_eff` | eq:chid·eq:dHeff | (유지) | 이미 충족 |
| `_n_factor` | 없음 | eq:wbase | docstring 1건 추가 |
| `_width` | 없음 | eq:wbase | docstring 1건 추가 |
| `_resolve_lag_length` (L_V) | eq:LV(docstring) | (유지) | 이미 충족 |
| `_resolve_lag_length` (컷 affinity A) | 없음(서술만) | eq:Acut | 인라인 주석 1건 추가 |
| `equilibrium` (평형 peak) | eq:eqpeak | (유지) | 이미 충족 |
| `dqdv` 헤더(분극·합산) | eq:vn·eq:sum | (유지) | 이미 충족 |
| `dqdv` 작업 격자 | 없음 | eq:vwork | 인라인 주석 1건 추가 |
| `dqdv` 분기 스위치(min_lag_grid_steps) | eq:eqpeak(평형쪽만) | eq:branch | 스위치 조건 자체에 주석 1건 추가 |
| `dqdv` 방향 반전(꼬리) | eq:memory | eq:reversal | 인라인 주석에 추가 |
| `dqdv` peak_shape(꼬리) | eq:peakshape | (유지) | 이미 충족 |
| `dqdv` 역보간(np.interp) | 없음 | eq:sum | 인라인 주석 1건 추가("합산·역보간" 중 후자) |
| `curve` (facade 환산) | 없음 | eq:n0map | docstring 1건 추가 |
| `func_dSe_molar` | eq:dSegate | eq:dSemolar·eq:ggate | docstring 1건 추가(몰당 환산+게이트 대입형 — 코드가 실제 구현하는 정확형) |
| `_effective_dS_rxn` (LCOCathodeDQDV override) | eq:U1T2(하단) | eq:lco-decomp | docstring 1건 추가 |
| `entropy_coefficient` | eq:weighted·eq:dxidT | eq:lco-dUdT | docstring 1건 추가(LCO 개별 전이 ∂U/∂T 관계식) |
| LCO σ_d 슬롯(`_delith_is_discharge` 등 4곳) | eq:lco-sigmaslot | (유지) | 이미 충분히 참조됨, 추가 불필요 |
| `GRAPHITE_STAGING_LIT` / `LCO_MSMR_LIT` 데이터 블록 | 개별 주석(dH_rxn/dS_rxn 도출 근거) | (변경 없음) | 함수가 아닌 데이터 dict — 매핑 표 대상 외, 기존 주석으로 충분 |

## Coverage 선언

- 사용자 제공 매핑 목록 20개 항목 중 19개 확인·처리(이미 충족 10건 + 신규 추가 9건[아래 "신규 추가 함수 수" 참고] + 미배정 1건).
- 실제 신규 코드 삽입 지점 = **16곳**(원형보존 블록 5 + `_n_factor`/`_width` 2 + `_resolve_lag_length` Acut 1 + `dqdv` 내부 4[vwork·branch·reversal·interp/sum] + `curve` 1 + `func_dSe_molar` 1 + LCO `_effective_dS_rxn` 1 + `entropy_coefficient` 1).
- [미배정] 1건: `func_U_j_hys` — 매핑 표 미포함, orphan 함수라 범위 판단상 보류(불확실 시 미수정 원칙 적용).
- eq 라벨 전수는 `graphite_ica_ch1_v1.0.14.tex`/`ch2` 의 `\label{eq:...}` grep 원문 대조로 검증 완료(가상 라벨 삽입 없음). `func_dSe_molar` 건은 기존 `eq:dSegate`(자리당 닫힌형)와 신규 `eq:dSemolar·eq:ggate`(코드가 실제 계산하는 몰당+게이트 대입형)가 물리적으로 구분되는 별개 라벨임을 tex 원문(line 2438/2489-2490 vs 2506)으로 확인 후 추가.

## 회귀 결과

- `python test_regression_graphite.py` (cwd=`D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.14`) → **PASS** (`=== GRAPHITE 0-DIFF: PASS ✓ ===`, 12/12 OK 항목 + AREA check 정상).
- 추가로 모듈 자체 `if __name__ == "__main__"` 셀프테스트도 실행 확인: `guards fired: 7/7`, `per-tr override isolation: True`, `>>> overall OK: True`.
- `git diff` 로 전체 변경분 라인 단위 재확인 — 16곳 전부 `#` 주석 또는 `"""` docstring 텍스트 추가뿐, 코드 로직·시그니처·상수·공백 구조 변경 0건.
