# V1.0.19 Ch2 — 10종 검수 UNION 결함 목록 (이전본 v1.0.18.2 Ch2 vs 신본, master 삼각검증·직접판정)

> C-P3 산출. 10창(W1~W9 콘텐츠+regression / W10 Fable 전체 물리 적대검산) → master union·중복제거·삼각검증. C-P4에서 Fable(작성 세션 이어서)이 수정. **doc-leads: 코드-불일치는 결함 아님.**

## ★ 종합 판정
- **물리 골격**: CENTRAL 18식·비자명 유도 11·수치 전항을 W4(Opus)·W10(Fable) 독립 재유도/재산출 재현 → **핵심 무결**. **단 CU-1(신규 문장 부호 오류 1건, master 확인)** 은 수정 필요.
- **regression(자산 유실)**: **0** — 133 자산 전건 보존. **narrowing 금지(C-2/3/87) 오히려 강화**·**구본 오류 2건 신본이 수정**(eq:weighted↔eq:complete 오인용·본문 entropy_coefficient register 위반).
- 결함 = CU-1(HIGH 물리) + CU-2~7(MEDIUM) + LOW. 물리 골격 무관 다수.

## master 직접 검증 CONFIRMED
- CU-1: Ch2 §2.1 L44-45 "−k_B ln q(T)"(자유에너지 미분) ↔ 엔트로피 s_int=−∂f/∂T=+k_B ln q(T) 선도(Ch1 L158-162). **부호 반전 확정**(+C-52 고온극한 T↑증가와 모순).
- CU-2: §2.1 L60 "−N_A sF(V−U_j)/N_A" 자리당/몰 혼재·μ⁰ 상쇄 미표시(W1·W10 2창).
- CU-3: 본문 평문 "식 eq:sm-epstilde/eq:Se"(Ch1 라벨명 인쇄) 실재.

---

## CU-1 [HIGH·물리 부호] `ch2_sec01_partition.tex` §ssec:site L44-45 (W1-1)
신규 문장 "그 내부 자유도의 온도 미분 **$-\kB\ln q(T)$** 의 $T$-의존이, 곧 vibrational 엔트로피 몫의 단일 자리 원형이다" — 부호 반전. vib 엔트로피 원형은 **s_int=−∂f_int/∂T=k_B ∂(T ln q)/∂T = +k_B ln q(T) 선도**(Ch1 §2 eq:sm-epstilde 계열). Ch2는 자유에너지 미분(∂f/∂T=−k_B ln q…)을 "엔트로피 원형"이라 오기. 같은 챕터 고온극한 S_vib→R[1+ln(T/θ_E)](C-52, T↑ 증가)와 **모순**(−k_B ln q는 T↑ 감소). 이전본(L146-147)은 명시식 없어 오류 없었음(신본 고유). → **정정**: "$-\kB\ln q(T)$" → 엔트로피 형태 "$+\kB\ln q(T)$"(또는 Ch1 s_int=k_B ∂(T ln q)/∂T 전체 인용해 반쪽 표시 오해 제거). 물리 = 엔트로피(자유에너지 미분의 음).

## CU-2 [MEDIUM·유도비약/표기] `ch2_sec01_partition.tex` §ssec:logistic L60 (W1-2 + W10-2, 2창 corroborate)
중간식 "지수의 분자가 $-N_A sF(V-U_j)/N_A=-sF(V-U_j)$ 꼴로" — 자리당(ε₀−μ/N_A, 분모 k_BT)과 몰(N_Aε₀−μ=μ⁰−μ=sF(V−U_j), 분모 RT)을 한 분수에 혼재 + μ⁰ 상쇄(N_Aε₀−μ에서 μ⁰이 소거되는 실질 단계) 미표시. 결과 (V−U_j)/w는 정확. 이전본은 이 문장 없이 boxed 직행. → **정정**: 이 중간식을 (a)삭제해 boxed 직행(이전본대로), 또는 (b)"분자·분모를 N_A배 하면 N_Aε₀−μ=μ⁰−μ=sF(V−U_j), 분모 RT"로 자리당/몰 짝과 μ⁰ 상쇄를 명시.

## CU-3 [MEDIUM·표기] 본문 평문 Ch1 라벨명 인쇄 (W3-1·W9 관련, chapter-wide)
Ch2가 Ch1 식을 참조할 때 "(식 eq:sm-epstilde)"·"식 eq:Se"처럼 **Ch1 내부 라벨명을 평문으로 박아** 최종 PDF에 "eq:sm-epstilde" 등 내부 jargon이 인쇄됨(별도 컴파일이라 \eqref 불가·undef 회피용으로 평문화). 이전본은 절 이름만("Chapter 1 의 전자 엔트로피 절") 써 안전. 여러 절(sec00/01/03/05/08). → **정정**: 평문 "식 eq:XXX" (Ch1 참조)를 **서술형**("Chapter 1 §N의 <식 설명>")으로 일괄 교체(Ch1 절번호+식 내용). Ch2 자체 식 참조 `\eqref{}`는 그대로.

## CU-4 [MEDIUM·register/라벨충돌] `ch2_sec03_vibel.tex` L55/L58-59 (W9-1)
Ch2 자체 `\label{eq:Se}`(자기 유도 박스)가 **Ch1 §15 `\label{eq:Se}`와 라벨명 충돌**(별도 컴파일이라 빌드 OK나 동일 이름). L58 Ch1 eq:Se 평문 언급 직후 L59 Ch2 로컬 eq:Se를 \eqref → 한 문장에 같은 이름 다른 객체. 부록 A 함정표(9종)에도 이 충돌만 누락. → **정정**: Ch2 로컬 라벨 개명(예 `eq:Se-ch2`)로 분리(물리 동일성은 서술 유지) + 부록 A에 eq:Se 충돌 행 추가(또는 최소 L58-59 분리 각주). CU-3와 함께 처리.

## CU-5 [MEDIUM·수식주도] `ch2_sec07_revheat.tex` L11-13 (W6-1)
신규 문장 "총 발열률은 …엔트로피 항의 **합(sum)**"이 eq:qrev underbrace(raw항 IT∂U_oc/∂T를 Q̇_rev로 라벨)와 부호 긴장 — 라벨 문자대입 시 Q̇=Q̇_irr−Q̇_rev(차)로 읽히나 boxed 정의 Q̇_rev=−IT∂U_oc/∂T 대입해야 합. boxed(물리)는 정확·이전본 동일. → **정정**: underbrace를 부호 포함 "$-\underbrace{IT\partial U_{oc}/\partial T}_{...}$" 재배치(또는 라벨을 −IT∂U_oc/∂T에), 또는 "합"을 "부호 포함 결합"으로 완화.

## CU-6 [LOW-MED·구조] §2.6 마무리 ↔ §2.7 개시 이중 전환 (W6-2)
§2.6 마무리 "이제 …가역 발열로 환산할 차례다" + §2.7 개시 "이제 …가역 발열로 닫는다" — 같은 전환 연속 2회(둘 다 신규 다리). → §2.6 마무리는 국소 정리로, 예고는 §2.7 개시 전담.

## CU-7 [MEDIUM·부록 재수록 원칙] `ch2_appA_traps.tex` "θ vs ξ" 행 (W8-1)
"흔한 오류(둘을 뒤섞어 발산 부호 ±∞ 반대로 읽음)"가 지정 근거 절(§2.1 ssec:logistic, θ/ξ 정의만)에 **없음** — Fable이 본문 조각 합성한 신규 주장(부록 "순수 재수록" 원칙 자기모순) + 근거열 부정확. → **정정**: (a)근거열 `ssec:sconfig`/`ssec:dvdt`로 정정 + 그 본문에 "θ/ξ 혼동 시 발산 부호 반전" 문장 실제 추가, 또는 (b)"흔한 오류"를 본문 실재 서술로 좁힘.

## LOW (선택·경미)
- **CU-8** [LOW] §2.2 warnbox "Ch1 §14 같은 골격"(W2-1): Ch1 §14(config/vib/elec 3슬롯) vs Ch2(ΔS⁰_j+config+δ잔차) 대응 과일반화 → "config 중심/분포 분리에 한정" 한정어.
- **CU-9** [LOW] §2.3.3 말미 "다음 절"(W3-2): 단수 모호(§2.4 vib/§2.5 겹침) → 두 절 명시.
- **CU-10** [LOW] §2.5.2 "단순식과 완전식"(W5-1): eq:weighted(파생A 결과)에 "파생 A" 표식 없음 → 제목 표식.
- **CU-11** [LOW] 두-상 전이 특정 vs 초기 Ω(W10-1): Ch1 초기 Ω(6000~13000)이 전부 2RT≈4957 초과 → "초기값 Ω 기준 전 전이 임계 초과·두-상 특정은 실측 plateau/staging 문헌 기준(Ch1 A-106 post-fit)" 한 줄 한정.
- (선택) W4-9 진폭 R 고정 한정·W4-10 곡률 정밀 — 이전본 계승, 저자 재량.

## 무수정(확인)
- W7-1/W7-2 tab:qrev·tab:worked 표시 반올림 — 이전본 계승·무해.
- W5-2/W5-3(파생B 2단·config n_j)·W4-11/W4-12(문체·점근 라벨) — 정합, 결함 아님.
- 구본 오류 2건(eq:weighted 오인용·entropy_coefficient register)은 신본이 이미 수정 = 개선.
