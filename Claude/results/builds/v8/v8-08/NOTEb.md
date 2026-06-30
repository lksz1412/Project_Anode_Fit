# v8-08b 보완 기록

## Read Coverage

- `Claude/results/v8-08/v8-08.tex`: 1-1180행 전문 확인.
- `Claude/results/v7-00_spine/Anode_Fit_v11_final.py`: 1-706행 전문 확인.
- `Claude/results/v7-11/v7-11.tex`: 1-889행 전문 확인.
- `Claude/results/v8-00_spine/AUTHOR_BRIEF_v8.md`: 1-63행 전문 확인.
- `Claude/results/v8-08/REVIEW1.md`: 사용자 지시대로 읽기 대상에서 제외.

## 수정 요약

- [D-PEAK] `v8-08b.tex` 908-922행 부근:
  - 기존의 "작은 `L_V`에서 저역통과가 한 격자 뒤의 평형 목표가 되어 logistic 미분 종으로 환원" 서술을 제거.
  - `rho=exp(-Delta_grid/L_V)` 이므로 `L_V << Delta_grid` 에서 `rho -> 0`, `xi_lag -> xi_eq`, 꼬리식 `(xi_eq-xi_lag)/L_V` 는 수치적으로 0에 가까워짐을 명시.
  - `L_V >> Delta_grid` (`rho -> 1`) 에서 매끈한 bell 환원이 해상되고, 작은 `L_V`의 수치적 평형 복귀는 `eq:branch` 명시 스위치가 담당한다고 정정.

- [D-VEQ] `v8-08b.tex` 431-440행 부근:
  - 평형 전위식을 번호식 `eq:Veq` 로 고정.
  - 직후에 `sF(V_eq,j(xi)-U_j)=g_j'(xi)=RT ln[xi/(1-xi)] + Omega_j(1-2xi)` 다리 식을 inline 삽입.

- [D-WEFF] `v8-08b.tex` 559-568행 부근:
  - `w_eff` 결과식 앞에 `g_j''(xi)=RT/[xi(1-xi)]-2Omega_j`, `g_j''(1/2)=4RT-2Omega_j` 중간식을 추가.
  - 중심 inverse-logistic 기울기 `sF dV/dxi|_{1/2}=4F w_j^eff` 와 `4F w_j^eff=4RT-2Omega_j` 를 거쳐 `w_j^eff=(RT/F)(1-Omega_j/(2RT))` 로 닫히게 보강.

## 부호 8항 재확인

- S1 `U_j(T)=(-Delta H+T Delta S)/F`, `Delta G=-FU`: 통과.
- S2 `xi_eq=logistic[sigma_d(V-U)/w]`, 방전 `V up -> xi up`: 통과.
- S3 `d xi/dV = sigma_d xi(1-xi)/w`, peak 양수/방향 불변: 통과.
- S4 `Delta U_hys >= 0`, `Omega <= 2RT -> 0`, 분기 중심 `+- 1/2 sigma_d`: 통과.
- S5 `chi_d`: 방전 `chi`, 충전 `1-chi`; `Delta H_a^eff=Delta H_a-chi_d Omega`: 통과.
- S6 `partial ln L_q / partial V`: 코드 실현은 컷 상수라 0, 부등식은 컷 규칙 동기: 통과.
- S7 꼬리 충전 격자 역전, 충전 `dQ/dV` 방전 거울 및 양수: 통과.
- S8 분극 `V_n=V_app-sigma_d |I| R_n`: 통과.

## Self-Test

- 검색 self-test:
  - `eq:Veq`, `sF(...)=g_j'(xi)`, `4F w_j^eff`, `L_V << Delta_grid`, `rho -> 0`, `eq:branch`, `매끈한 bell 환원` 존재 확인.
  - 기존 오서술 `한 격자 뒤`는 `v8-08b.tex`에서 미검출.

- `Anode_Fit_v11_final.py` 자체 실행:
  - 명령: `PYTHONDONTWRITEBYTECODE=1 python Claude/results/v7-00_spine/Anode_Fit_v11_final.py`
  - 결과: `>>> overall OK: True`.
  - 확인 포함: hysteresis split `+86.9 mV` vs 기대 `+86.7 mV`, `Omega=2RT -> dU_hys=0`, `gamma=0, |I| -> 0` 방전/충전 차 `5.107e-15`, guard `7/7`, per-transition override isolation `True`.

- 추가 수치 self-test:
  - 결과: `SIGN8_AND_BRANCH_SELFTEST=PASS`.
  - `small_LV_tail_formula_max=0.000e+00`: 작은 `L_V`에서 꼬리식 자체는 0으로 무너짐 확인.
  - `small_LV_branch_vs_equilibrium_maxdiff=1.086e-04`: 코드의 `eq:branch` 평형 분기 결과가 직접 `equilibrium()`과 보간 오차 수준으로 일치.
  - `hys_dU_mV=86.686`.
  - direct `L_V=0.02` tail 방향: discharge peak `0.133644`, charge peak `0.106336`, 양수 유지.

## 컴파일 상태

- `xelatex` 설치 확인: `C:\Users\lksz1\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe`.
- 임시 출력 디렉터리에서 `xelatex -halt-on-error -interaction=batchmode` 2-pass 실행.
- 결과: `PASS1_EXIT=0`, `PASS2_EXIT=0`, `PDF_EXISTS=True`, `LOG_BANG_COUNT=0`, `LOG_FATAL_COUNT=0`.
- 최종 산출 폴더에는 사용자 지시 `지정 두 파일만 생성`을 지키기 위해 PDF/aux/log/toc/out을 새로 남기지 않았다. PDF 생성 여부는 임시 디렉터리에서 확인 후 임시 파일을 정리했다.
- MiKTeX가 콘솔에 사용자 로그 권한 및 업데이트 확인 경고를 출력했으나, LaTeX 로그 기준 fatal/LaTeX error는 0개였다.
