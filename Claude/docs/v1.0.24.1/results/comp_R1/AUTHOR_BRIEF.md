# AUTHOR_BRIEF — v1.0.24 R1 문건 저작 (9창 경쟁 저작)

## 0. 너의 역할 (4-세션 모델 고지)
너는 v1.0.24 R1 의 **작업(저작) sub** 다. master(총괄)+작업+검수+검토 4-세션 분업 중 작업 sub.
- **경계**: 너는 **초안만 작성**한다. 실제 문건 파일(`ch*_v1.0.24.tex`, `_sections/*.tex`) 편집 금지·git 금지·commit 금지. 네 결과는 **너 전용 폴더에만** 쓴다.
- **범위 밖 자의 작업 금지**: 새 표준·새 파일(지정 외)·메모리 X. 발견은 네 초안 말미 `NOTES` 에 기록만.
- **허위 attribution 금지**: 네 저작을 "사용자/master 작업"으로 표기 X.
- commit 권한은 master.

## 1. 임무
아래 **3개 신규 LaTeX 소절**을 각각 초안 저작한다. 물리는 §3 시드에 확정돼 있다 — 너는 이를 **교과서 register(전제부터 친절)+리뷰 깊이**로 자기완결 소절로 저작한다.
1. **[GR-2L]** 흑연 stage-2L / XRD 5-feature staging 소절 (ch1 흑연, `ch1_sec05_width` 뒤에 붙을 신규 subsection).
2. **[SI-FR]** Si-host 정칙용액(Frumkin, Ω<2RT 고용체) 커널 소절 (ch3 Si, `ch3v22_sec02_cases` 인접 신규 subsection).
3. **[LCO-Ω]** LCO per-peak Ω(정칙용액 커널) + 전자항 on/off 토글 소절 (ch2 LCO, `ch1_sec13_lcohys`·`ch1_sec15_lcoelec`·`ch1_sec16_lcopeak` 정합 신규 subsection).

## 2. 필독 (저작 전 — 표기·라벨·스타일 정합)
`/home/user/Project_Anode_Fit/Claude/docs/v1.0.24/` 하위:
- `results/REFLECT_SEED_TABLE.md` — **확정 물리·값·서지**(최우선).
- 흑연: `_sections/ch1_sec05_width.tex`(폭·두-상·Ω 규약·라벨), `_sections/ch1_sec06_eqpeak.tex`(평형 peak 식).
- Si: `_sections/ch3v22_sec02_cases.tex`, `_sections/ch3v22_sec03_blend.tex`, `_sections/ch3v22_notation.tex`.
- LCO: `_sections/ch1_sec13_lcohys.tex`(정칙용액 Ω·질서 — #7 정정 대상 문구 여기), `_sections/ch1_sec15_lcoelec.tex`(전자 엔트로피 ΔS_e), `_sections/ch1_sec16_lcopeak.tex`.
- 표기 계승: 각 장 notation 파일. 기존 기호(V_n·V_{n,app}·ξ_j·w_j·Ω·U_j·ΔS_rxn·Q_j·C_bg)·라벨 prefix(eq:·ssec:) **그대로 계승**. 신규 라벨은 장 관행 따라 새 이름(중복 금지).

## 3. 각 소절 내용 사양 (시드 기반)
### [GR-2L] 흑연 stage-2L·XRD 5-feature
- XRD 확정 staging(Dahn 1991): dilute 1′↔4·**4↔3 고용체 shoulder(Ω<2RT)**·3↔2L·2L↔2·2↔1 (두-상 4 + 고용체 1).
- **판정자**: Ω>2RT ⇒ miscibility gap ⇒ near-delta(XRD 공존)·Ω<2RT ⇒ 고용체 shoulder(새 상 아님). μ(θ)=μ°+RT ln[θ/(1−θ)]+Ω(1−2θ), dμ/dθ|½=4RT−2Ω 유도 포함.
- **stage-2L 온도 분리**: 2L=엔트로피 안정화 상(>~10℃). 3↔2L·2L↔2 의 ΔS 차 Δ(ΔS)≈29 J/mol/K → ∂U/∂T=ΔS_rxn/F 로 분리 0.30 mV/℃·병합~10℃·45℃ 2피크/25℃ 병합. 실측 검증(Δ=29 재현 0.271 mV/℃).
- 서지(실재): Dahn PRB44,9170(1991)·Schmitt 2022(탈리튬 2L)·Reynier JPS119-121,850(2003).
- 기존 4전이가 이미 두-상 4에 대응함을 명기(폐기: 전이 6+는 XRD 미지원 curve-fitting).

### [SI-FR] Si-host 정칙용액(Frumkin Ω<2RT)
- a-Si = **단일상 고용체**(sharp 두-상 아님) — 폭/(RT/F)≳1 실측(흑연 두-상 ≪0.12와 대조, ~20-50×).
- Frumkin 단일상 peak: `dQ/dV = Q·F / |RT/(θ(1−θ)) − 2Ω|`, Ω<2RT. Ω→2RT서 sharpen·발산, Ω<0서 broaden. 유도 포함(V(θ)=U°−(RT/F)ln[θ/(1−θ)]−(Ω/F)(1−2θ), dQ/dV=Q/(F·|dV/dθ|)).
- Si-host = 소수 broad gallery(연속 고용체 이산화). 유일 두-상 = c-Li₁₅Si₄(1차 심리튬 ~50-60mV plateau, 순환 a-Si엔 부재).
- 서지: Chevrier-Dahn JES156,A454(2009)·Artrith JCP148,241711(2018)·Verbrugge JES164,E3243(2017).
- 블렌드 가산중첩(§3.5) 유효(공통 전위): Tu-Dao-Verbrugge-Koch JES171,050520(2024) "clearly a superposition".

### [LCO-Ω] LCO per-peak Ω + 전자항 토글
- LCO dQ/dV = 흑연과 동일 MSMR. feature별 상 성격 다름: 3.70V(O2)/3.90V(O3) 두-상 sharp(Ω>2RT)·x½ order-disorder broad. per-peak Ω(정칙용액 커널)로 포착.
- **#7 정정**: `ch1_sec13_lcohys` 의 "Ω>2RT ⇔ x½ 질서상 안정" → **"Ω_j^cat = 전이당 진행좌표의 유효 평균장 축약(미시 질서구조 아님)·config 엔트로피는 별도 슬롯 분리"** 명확화(물리 유지·문구만). 혼동가드 계승.
- **전자항 토글**: ΔS_e(MIT, ~−45.7 J/mol/K)는 **T_ref 동결로 상온 커브에 무영향**(dH 흡수)·**∂U/∂T(가역열)에만 작용**. 코드에 `include_electronic_entropy` 플래그(기본 OFF=커브·ON=∂U/∂T). "커브 산출엔 불필요·다온도 엔트로피에서만 선택 활성" 명기. 실측: LCO plain MSMR R²=0.944≈흑연 0.940(전자항 무관).

## 4. 출력 (너 전용 폴더에만)
`/home/user/Project_Anode_Fit/Claude/docs/v1.0.24/results/comp_R1/W<번호>/` 에:
- `gr_2L.tex` · `si_fr.tex` · `lco_omega.tex` — 3개 소절 LaTeX(각 `\subsection{...}\label{ssec:...}` 로 시작, 자기완결).
- `NOTES.md` — 저작 근거(읽은 파일·행), 가정, 불확실점.
LaTeX 규율: 기존 preamble 매크로만 사용(신규 패키지 X)·boxed 최종식 1개 이상·식마다 라벨·서지는 `\cite{key}`(신규 key 는 NOTES에 서지 명기, 본문 임의 bibitem 금지)·한글 교과서 register.

## 5. 공통 규칙 (위반 시 기각)
- 시드표 값 임의 변경 X·무근거 수치 X(4-tier: 확정/근거미발견/추정/미검증).
- 기존 라벨·기호·식 재정의 X(계승). 신규만 새 라벨.
- 물리 골격 불변: 전하보존 중심식·V_n 구분·MSMR 동형 유지.
- 분량: 각 소절 **논리 깊이 리뷰급·전제부터 전개**. 복붙·skim 금지.
