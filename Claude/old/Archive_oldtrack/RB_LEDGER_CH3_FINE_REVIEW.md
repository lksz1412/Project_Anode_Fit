# RB_LEDGER_CH3_FINE_REVIEW — Ch3 절별(fine) 적대검수 + 정정 Result (2026-06-02 자율)

> §절마다 1 agent(13 병렬, 9렌즈). 파일 `Claude/docs/graphite_ica_ch3_rebuilt.tex`. Ch3=반응속도론 Level B. 거친 3렌즈가 놓친 keystone 순환·식별성 미입증 다수 적발.

## 적발 결함 (정정 대상 CRITICAL/HIGH/주요 MED)

### CRITICAL
- **C1 [655–671 §ident] ΔH‡·ΔS‡ 부재 + Eyring/Arrhenius 혼선**: 절 표제는 "활성화 ΔH‡·ΔS‡ 다온도 제약"인데 본문은 lumped Arrhenius E_{ν,j} 만 사용, ΔH‡·ΔS‡ 미등장. 175행 Eyring prefactor ν=(k_BT/h)κ 의 k_BT/h \*선형 T 인자\*가 660행 순수 Arrhenius E_{ν,j} 에 은닉 → 다온도 fit 으로 얻는 E 가 ΔH‡도 ΔS‡도 아닌 혼합량. G-usable(다온도가 무엇을 분리하나) 미실현. → **Eyring 1차 분해 box 신설**: ln(ν_j^±/T)=ln(k_B/h)+ΔS_j^{±‡}/R−ΔH_j^{±‡}/(RT); "ln(r/T) vs 1/T 직선 기울기=−ΔH‡/R, 절편=ΔS‡/R+ln(k_B/h)+ln a" + E_{ν,j}≈ΔH‡+RT 보정 1줄 + 공선형 쌍 명시({ν,a} 곱만 식별·{E_ν,ΔH_a} 합만). 기호표 ΔH‡·ΔS‡·E_{ν,j} 등재.

### HIGH
- **H1 [171 §inherit] k_j^phys=r^++r^- 무조건 정의**: 이 항등은 detailed-balance split(Level A) 한정인데 기호표가 일반 정의로 제시. → "Level A mobility(detailed-balance split 하; §sec:ch3_split)" 한정 + 일반 r^±서는 합≠mobility 1구.
- **H2 [226·233 §potentials] η_j 이중정의**: eq:ch3_Aj 가 η_j≡𝒜_j/(n^eff F)=s_φ[V_drive−U_j](중심 U_j)로 재정의 — 상속 L6 η_j=V_drive−V_eq,j(국소 평형)와 충돌(같은 기호 2정의). → 식(5) 둘째식 좌변을 별개 기호 η̃_j(또는 η_{𝒜,j}, affinity 전위정규화·중심 U_j 기준)로 바꾸고 기호표 등재 + 233–236 관계 재진술. s_φ(229)가 L4 logistic s_φ 와 동일물임 1줄.
- **H3 [310–354 §consistency] keystone 순환(★기존 HIGH 미해소)**: (a) 327행 "split이 detailed balance 자동 만족"=동어반복(split을 ξ_eq로 정의했으니), keystone 닫힘조건(평형서 r^+/r^- 가 ξ_j-무관, 즉 C_j(ξ_j,T)의 ξ_j-의존 소거)이 식·범위로 미명시. (b) 351–354 ξ_ss→ξ_eq 환원이 split 재대입(순환). → 닫힘조건 BOUNDED box 신설 + ξ_ss=ξ_eq 를 \*split-free\*로: 일반 ξ_ss=r^+/(r^++r^-)에 eq:ch3_db(r^+/r^-=ξ_eq/(1−ξ_eq)) 직접 대입 → ξ_ss=ξ_eq, split은 이를 달성하는 한 표현(사후 확인)으로 강등.
- **H4 [457·462 §levelB]**: 457 verifybox 대입 체인(odds→reciprocal→exp) 3항등 1줄 압축(무비약 미달) → 한 줄 전개. 462–467 (ii) "ratio ξ_j-무관"의 ξ_j(동적)와 ξ_eq(평형 target, V_n 함수) 미구분 → "무관 대상은 현재 ξ_j; ratio의 ξ_eq(=V_n)-의존은 detailed balance 가 요구" 1줄.
- **H5 [484·488 §limiter]**: 484 "r^+→min 병목으로 포화" 거짓(reciprocal 합은 조화합, min 아님) → "r^+→∞ 면 r_obs^+→(나머지 병목 조화합); 한 병목 지배 시 최소 병목 근사". 488–491 "기본형 대칭 병목"이 실제 식 부재 + eq:ch3_split(병목 없는 Level A) 오인용 + 478↔489 forward-only 위상 역전 → 기본형 대칭 병목식 1/k_obs^phys=1/k_phys+1/k_lim(L3, ratio 보존) 명시 + 466 오인용 정정 + 478을 "(강구동 branch용) forward-only template"로 한정.
- **H6 [527·503 §bv]**: 527 R_ct=∂η/∂I 정의에 역수+면적 환산(∂I/∂η=A_eff·j_0 F/RT → 역수) 1줄 명시. 503·548 "α_n=β_j 같은 계열" 오류 — BV anodic=(1−α_n), Level B forward=β_j 라 \*상보\* → "α_n=1−β_j (anodic 측 대응; 동일 값 아닌 상보 관계)" + 184 기호표 α_n 정의(cathodic; anodic=1−α_n) 명시.
- **H7 [568 §genaff] 𝒜_resid 비폐쇄**: 𝒜_resid≡𝒜_n−Fη_n 은 항등이라 임의 분배 허용(double-counting 차단 식 아님). → U_n operational 정의 고정("U_n≡측정 OCV at I→0, reference 고정") + "주어진 U_n 정의에 대해 𝒜_resid는 그 reference 제외 항만; staging∈U_n 이면 ∂𝒜_resid/∂(staging μ)=0" 귀속 불변식.
- **H8 [592·599 §current] ΣI_j≤|I| 부호 무증명**: I_j=Q_jtot dξ_j/dt 부호·I_bg^prog≥0 미증명이라 부등호 뒤집힐 수 있음. → "방전 정전류·s_φ=+1 단일방향 가정 하 모든 dξ_j/dt≥0 → I_j≥0; I_bg^prog=(∂Q_bg/∂V_n)(dV_n/dt) 부호 평가 후 비음수 영역서 ΣI_j=|I|−I_bg^prog≤|I| 성립" 보조정리.
- **H9 [609·614 §Rn] 5항 분해 부호·비식별**: LHS s_I|I|R_n signed, RHS 5 η 부호·측정경로 미정(η_ct 만 식). → "각 η_•,n≥0(s_I 공통부호 흡수); 본 분해는 T×|I|×f 다채널 분리 전제, 단일 I-V서는 η_ct 만 식별" BOUNDED + η_ohm/conc/film 분리신호(current-interrupt/relaxation/EIS) 1열.
- **H10 [648·636 §crate] 𝓕 인수 누락 + 표↔식 비대응**: 𝓕 인수에 w_j(T)·(ξ_eq,j−ξ_j) 누락, 𝒜_j·R_n·V_drive 종속 평탄나열, 표 5요소↔식 6인수 불일치. → 인수에 w_j·lag 추가 + 종속(co-linear) 각주 + 표에 "수식 위치" 열로 1:1 정렬 + tail/broadening 차원 분리(L∝|I| 정합).

### MED (정정 권장)
- M1 [154·159 §inherit] n^eff: L4 의 \equiv 를 "w_j 만 전달; n^eff 정의는 §neff 1회"로, 159 n^eff→n_j^eff 첨자.
- M2 [280 §db] 분모 r^-(1−ξ_eq): r^->0 경계 명시(곱형 db 로 ξ_eq=1 닫기) + 0<ξ_eq<1 열린구간.
- M3 [288 §db] db_width box 에 (s_φ=+1 방전 기본형) 단서 + "평형점에서 성립, 비평형 ln(r^+/r^-)=C_j+𝒜_j/RT 는 §levelB" forward-ref.
- M4 [423 §levelB] 기울기 정합 전 "U_j·w_j·n_eff 는 V_n-무의존(T 함수)" 전제.
- M5 [530 §bv] 차원검산 자문자답 오기 삭제, Ω 직진.
- M6 [639 §crate] C-rate 귀속 순위 단언(1차=1/|I| 체류, 강구동 율속=k_lim/r_curr, k_act 아님).
- M7 [330 §consistency] keybox "Ch1 keystone k_j=r^++r^-" dangling → "Ch1 §X 유도 결과 입력(L2 적층)" + 기본형 η_drive=0 전제.

### LOW (기록)
- 175 κ^± 정의, 374 a_j^± 인자, 434 n_eff w_j=RT/F 단위, 705 AL 매핑 K2/K3 중복, 763 이월 "분리 vs 닫힘" 한정, 687 transmit 입도.

### 통과 확인(빈통과 아님)
- DOI 귀속 클린: onsager1931 DOI(10.1103/PhysRev.37.405) 가 degrootmazur(book)에 오귀속 0(AL-30·35 정확). 구 Ch6 참조 잔존 0(Ch1 부록 B 재지정). AL-30~39 10개 전수·중복 0. 핵심 식 부호·차원(R_ct=Ω, n^eff=RT/Fw_j, barrier lowering ∓, β+(1−β)=1) 산술 정합.

## 정정·빌드·커밋 (완료)
- 정정 적용: **CRITICAL 1(C1) + HIGH 10(H1~H10) + MED 7(M1~M7)**. 기존 줄 BOUNDED/box/인자 추가·부호/기호 교정 위주(식 재유도 0, 식별자 보존). LOW 기록·미적용.
- 검증(master 독립): xelatex 2-pass GREEN(`!` 0, undefined ref/cite 0, dup 0, 20p). 핵심 정정 실텍스트 확인 — C1 Eyring box(733 `eq:ch3_eyring` + 176 ΔH‡ 기호표)·H2 η̃_j(231 box·187 기호표·243 `\tilde\eta_j-\eta_j=w_j\ln[...]` 이중정의 해소)·H3 keystone(344 "평형서 r^+/r^- ξ_j-무관 closure" + 382 split-free 사후확인)·H6 α_n=1−β_j 상보(189·544·590).
- tex **834→915줄**(+81). 신규 라벨 eq:ch3_eyring·eq:ch3_mobility_limiter. 커밋·push(main+rb-rebuild).
