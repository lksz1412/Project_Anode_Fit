# v1.0.10 인계 무결성 대검수 계획 — 기록 기반 9종 union + 10차 재검 → v1.0.11

> 사용자 지시(2026-07-02): 이전 문제검수가 **버전 이력·계획서·FIX_LIST를 참조하지 않고** 현재 문건만 봐서 오판(bell을 "구조 결함"으로). 이력이 "이전 버전 문제→개선 의도→달성→우수구조 유지"의 **기준 명세(SPEC)**. 이걸 정독해 v1.0.10이 인계를 제대로 받았는지 대조. ★두 최우선 축 = (축1) 물리·화학 논리 전개과정까지 비약 없이 이론적 무결한 식 · (축2) 학부지식만으로 타전공 석박사 따라오는 교과서성. v8~v10은 이 두 축 필수 + 코드 불요 TMI만 덜기가 목표였다.

## 재구성된 의도 궤적 (SPEC — 기록 정독 확정)
- **v3/v4/v5**: broadening/분포 물리 보유(ρ_G 배리어 분포·두 broadening·현상학적 w·forward-only).
- **v7-11→v8**: 유도 복원(G-derive) 목표였으나 broadening/분포 **제거(후퇴)**. KNOWN_DEFECTS: ★D-PEAK(peak_shape→dξ/dV 극한 오류→branch-switch 정정 필요)·D-VEQ·D-DHEFF·D-WEFF·D-UBR·D-PEAK2(문턱 불연속 정직기술).
- **v8→v9**: v8-11 흑연 보존 + LCO 전자엔트로피 추가(Sommerfeld·MIT 게이트·ΔS_e<0·가법 직교성·x_MIT≈0.85·T1 3.90/T2 4.05/T3 4.17). v9-11 fix F1-F8.
- **v9→v10**(6-30 핸드오버 [과제 V8-1] 이행): v9 전부 보존 + **broadening 복원** — 전이별(dilute·4L↔3L=SS / LiC₁₂·LiC₆ 2개만 two-phase, 코드 Ω 초기값 전부>2RT=거친추정) · 3기작(①L_V 비대칭꼬리 ②내재 RT/F ③집합 다입자 통계역학=Dreyer plateau + **apparent-U=U_j+η 앙상블 분포, U_j 중심=입자무관 상수·분포는 η=과전압/국소환경 비-크기**·forward 통계평균·ρ→δ·역산X) · **w 이중지위**(단상 Ω<2RT=nRT/F 평형예측 / 두-상=현상학적 자유 피팅폭) · **w_eff 완전제거** · **사이즈 전면 배제**(τ∝r²·반경→U_j·PSD 배제 경고만). v10-11 CRIT D1=apparent-U/η 재정초. **전자엔트로피 절 byte-identical**(SHA 검증)·34p·0-error.
- **Ch2 v3→v4**: 통계열역학 챕터(분배함수→점유분포→config/vib/elec 엔트로피·섞임 A/C/D/I·가역열). C=w_eff=w(1−Ω/2RT) 섞임항(단상 V-폭).
- **코드 v11_final**: 6-30 CODE_w_check 실측 = 기본(w=12-20mV·use_w_eff=False) **정상 종 FWHM 42mV·면적보존**. use_w_eff는 버그(면적 위반).

## 검수 초점 (인계 무결성 = 두 축 + 이력 대조)
각 버전 전환마다: (1) 이전 문제 무엇 (2) 이번 개선 의도 무엇 (3) 실제 개선됐나 (4) ★이전 우수 구조·물리 보존됐나 (5) v1.0.10까지 인계됐나. + 두 축(논리 전개 비약0·교과서 follow) 유지 여부.

## ★핵심 검증 쟁점
1. **broadening 복원 보존**: v10의 broadening 절(3기작·apparent-U=U_j+η 중심상수·w 이중지위·forward-only·사이즈배제·D1 apparent-U)이 v1.0.10에 **온전·정확**한가? 제 P2 교과서화가 훼손/축약?
2. **KNOWN_DEFECTS 정정 보존**: v8 D-PEAK(branch-switch·문턱 불연속 정직기술)·D-VEQ·D-DHEFF·D-WEFF·D-UBR가 v1.0.10에 정정된 형태로 있나? (내 10차가 D-PEAK류를 오적발로 기각한 게 맞나 재검.)
3. **전자엔트로피 byte 보존**: v10이 byte-identical 유지한 전자엔트로피 절을 P2/P5가 깨뜨렸나?
4. **★코드 회귀**: v11_final(42mV 정상)→v1.0.10('n':1.0로 w inert→90mV 병합) 회귀인가? use_w_eff 제거·w 이중지위 코드정합.
5. **두 축 degradation**: v10 대비 v1.0.10의 유도 완결성(G-derive)·follow-ability 저하?
6. **cross-version 손실**: v3/v4/v5 물리 중 v1.0.10 부재 = 정당 컷 vs 손실.
7. **FIX_LIST 이행**: FIX_LIST_v911·v1011·v411 각 항목이 실제 반영·보존?

## 방법 (기록 SPEC 기반)
- **검수 1-9 = 9 에이전트(3 Sonnet-5·3 Opus·3 Codex)** 각 초점(위 쟁점 분산) + 두 축 렌즈. 기록을 SPEC로 대조. 그래프는 apparent-U 물리 기준 판독(bell=정상). **단점 union**(체리픽 X). refute·가장약한1곳·빈통과금지.
- **검수 10 = 진짜 문제 재검**(별세션): 진짜 인계 결함 vs 오적발 vs 강등. ★내 이전 R1 "구조 결함" 오판 여부 포함 재검.
- 산출: 보고 문건(인계 무결성) + v1.0.11 핸드오버 갱신(R1 재framing 반영).

## Sonnet 슬롯 = Sonnet 5 (신규)
`model: "sonnet"` → Sonnet 5. 이전 검수 Sonnet 항목을 Sonnet 5로 갱신 적용.

## 주의
- v1.0.10 코드/문건 수정 0(진단만). 검수=별세션·commit master. 추정 금지(기록 줄·코드·실측). radius 회의적. 원본 불가침.
