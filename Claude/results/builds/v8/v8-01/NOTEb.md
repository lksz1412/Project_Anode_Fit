# NOTEb — v8-01b.tex 보완 기록

## 보완 사항 (v8-01 → v8-01b)

### [CRIT-1] staging 표 U값 정정 · 7컬럼 전체 교체
- **원본 오류**: tab:staging에 U=0.120/0.090/0.075 (3열 단순표)
- **정본**: GRAPHITE_STAGING_LIT / v7-11 tab:staging 기준
  - 4→3: U=0.210, dH=-11700, dS=+29.0, Q=0.10, Ω=6000, dHa=48000, dVdq=0.30
  - 3→2L: U=0.140, dH=-13500, dS=0.0, Q=0.12, Ω=8000, dHa=46000, dVdq=0.30
  - 2L→2: U=0.120, dH=-13100, dS=-5.0, Q=0.25, Ω=10000, dHa=44000, dVdq=0.30
  - 2→1: U=0.085, dH=-13000, dS=-16.0, Q=0.50, Ω=13000, dHa=40000, dVdq=0.30
- 7컬럼(U/dH/dS/Q/Ω/dHa/dVdq_qa) 전체 표로 교체, renewcommand arraystretch 적용

### [CRIT-2] eq:vn 중복 라벨 해소
- N1 절 261행: `\label{eq:vn}` — 원 권위 라벨 유지
- N9 절(구 865행): `\label{eq:vn}` → `\label{eq:vnN9}` 으로 변경
- N9 절 문장을 "N1에서 유도한 식~\eqref{eq:vn} 참조"로 수정해 박스 중복 제거
- nodemap 표 N0 행의 `\eqref{eq:vn}` 참조는 N1 유도식을 올바르게 가리켜 그대로 유지

### [ansatz] eq:Ubranch 현상학적 매개변수화 명시
- 분기 중심 식 앞에 "ansatz(현상학적 매개변수화)"임을 명시
- γ_j의 지위를 열역학 이론값이 아닌 피팅 매개변수로 설명하는 문단 추가
- ΔU_hys가 spinodal 상한으로 물리적 스케일을 고정함을 명기

### [유도 보강] eq:dHeff의 χ_d 계수 중간식
- derivebox에 방전/충전 꼬리 극한별 중간식 추가:
  - 방전 ξ→1: (1-2ξ)→-1, 보정=-χΩ → dH_a^eff=dH_a-χΩ
  - 충전 ξ→0: (1-2ξ)→+1, 보정=-(1-χ)Ω → dH_a^eff=dH_a-(1-χ)Ω
  - 두 경우를 χ_d로 통합하는 과정을 명시

### [self-test] 새 회귀 자가검증 절 추가
- R1: U_j(T) 손계산 → 0.08529V (목표 0.085V, 편차<0.1mV)
- R2: w_j 손계산 → 0.02569V
- R3: spinodal u_j → 0.7865 (Ω>2RT 조건 확인)
- R4: ΔU_hys → 0.1053V (artanh 경로 포함)
- R5: ΔH_a^eff → 33500 J/mol (방전·충전 χ=0.5 대칭 확인)
- R6: D-PEAK 이산 분기 확인 — |I|→0 극한에서도 분기 중심이 U_j^d로 고정되어 "종 환원" 거짓 극한 회피

## 빌드 결과
- xelatex 2-pass 완료
- PDF 생성: v8-01b.pdf (333349 bytes)
- 치명 error(^!): 0건
- 비치명 경고: "Infinite glue shrinkage" (longtable+setspace 조합 기인, 출력 무해)
- 기타 경고: Font shape undefined (UnBatang italic — kotex 환경 정상), hyperref Token warning (한글 섹션 제목 정상)

## 강점 유지 확인
- D-PEAK 거짓 극한 회피: 이산 분기 처리 eq:Ubranch / eq:center 수정 없이 보존
- 절 순서 N0→N9, 결과 박스, 그림 5+3개, 부호 8항 검산 전부 그대로
