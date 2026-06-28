# NOTEb.md — v7-05b 보완 로그 (v7-05 → v7-05b)

> v7-05.tex(원본 보존) 을 v7-05b.tex 로 복사해 **미세 보완 3건**만 가한 로그.
> 원본 v7-05.tex / NOTE.md / REVIEW1.md 미수정(REVIEW1.md 는 지시대로 미열람).
> 빌드: `xelatex -interaction=nonstopmode` 2-pass, **에러 0**, v7-05b.pdf **18쪽**.

## 1. Read Coverage (이번 보완 라운드)
- `v7-05.tex` 전문 1–752행 정독(2 페이지 분할).
- `v7-00_spine/Anode_Fit_v11_final.py`: L400–444(분극 V_n·작업격자·전이루프 진입), L307–361(`_resolve_lag_length`·컷 affinity A=min(...)·`equilibrium`). 분극·컷상수 부호 정본 확인.
- `v7-00_spine/v11_flowchart.md` 전문 1–90행, `AUTHOR_BRIEF.md` 전문 1–76행 정독.
- REVIEW1.md **미열람**(지시).

## 2. 보완 3건 (방향성만 받음, 구현은 자율)

### 보완 1 — N1 분극 물리 서술의 식·코드 정합 (브리프 task #1)
- **쟁점**: 작업지시문은 "초본의 분극 물리 서술이 eq:vn 및 flowchart 와 반대 방향"이라 보고, 서술을 식에 맞추라 지시.
- **독립 적대 물리검산**(서브에이전트, 도구 무): 흑연 음극은 셀 방전에서 **탈리튬화=산화**되는 전극 → anodic 과전압 **양수**(η=V_app−V_eq>0) → 방전 시 측정 V_app 가 평형 V_eq 보다 **위**. eq:vn(V_n=V_app−|I|R_n, 방전 σ_d=+1 → V_n<V_app)과 **합치**.
- **결론**: 초본의 기존 서술(`방전은 측정 전위를 내부보다 올림`, 235·240행)은 **이미 식·코드와 일치하는 (A)** 였음. flowchart 의 괄호 문구(`방전 시 관측 V 가 평형보다 낮게 읽힘`)가 오히려 식과 반대. 즉 task #1 이 지목한 "반대 방향"은 본 .tex 초본이 아니라 flowchart 괄호였음.
- **조치**(★ feedback_execute_explicit_choice·식 무결 보존): 초본을 (B)로 뒤집으면 물리·eq:vn 양쪽과 어긋나 도리어 task #1 의 "식과 일치" 요구를 위반. 따라서 **올바른 (A) 서술을 유지하되, 식과의 일치가 자명하도록 명시 강화** —
  - 235행: 흑연 음극=방전 시 산화 전극 → η=V_app−V_eq>0 정의를 본문에 삽입, "방전은 측정을 평형보다 위로, 충전은 아래로" 를 과전압 부호로 못박음.
  - 240행: 검산을 `V_n=V_app−|I|R_n<V_app`(방전)·`V_n=V_app+|I|R_n>V_app`(충전)로 식 그대로 전개, "η>0 과 합치" 명시.
- **식·박스(eq:vn) 자체는 불변**(브리프 "식 자체 무결" 준수).

### 보완 2 — ∂lnL_q/∂V 박스 과단정 회피 (브리프 task #2)
- N7 boundbox(560행) 재작성: 𝒜 는 **운영상** 컷 상수(eq:Acut, `A=min(z_cut·n·RT, A_cap·RT)`, 코드 L335, V_n 무의존)임을 못박음 → 코드가 실제 평가하는 **운영 미분 ∂lnL_q/∂V_n=0**(꼬리 길이 전이당 상수).
- ★부호 체크리스트 6번의 `∂lnL_q/∂V<0` 은 𝒜 를 달리는 affinity 로 볼 때의 **모델 정합 동기 부등식**이지 운영 미분 음수 주장이 아님을 분리 명시.

### 보완 3 — §8 부호 체크리스트 전건 재확인 + ★새 부호 회귀 self-test
- 신규 §(`sec:signregression`) + 표(`tab:signregression`, 9행): 방전 σ_d=+1 기준 식별자별 "입력 변화⇒출력 부호" 단언 + 충전 거울 + 코드 식별자 1:1.
- 코드 `__main__` self-test(평형 peak 양수·|I|→0 방충 일치·ΔU_hys|_{Ω=2RT}=0)를 **식 수준 부호 회귀**로 확장. 169행·732행에 표 참조 추가.

## 3. ★부호 체크리스트 8전건 재확인 결과 (PASS)
| # | 항목 | 식 라벨 | 결과 |
|---|------|---------|------|
| 1 | U_j=(−ΔH+TΔS)/F, ΔH<0→중심↑ | eq:Uj | PASS (verifybox 0.085 V) |
| 2 | ξ_eq=logistic[σ_d(V_n−U)/w], 방전 V↑→ξ↑ | eq:logistic | PASS |
| 3 | dξ/dV=σ_d·ξ(1−ξ)/w → peak 양수 | eq:dxidV | PASS (σ_d²=1) |
| 4 | ΔU_hys≥0, Ω≤2RT→0, 분기 ±½σ_d | eq:hysdU/hyscenter | PASS |
| 5 | χ_d 방전χ/충전1−χ, ΔH_a^eff=ΔH_a−χ_dΩ | eq:chid/dHeff | PASS |
| 6 | ∂lnL_q/∂V: 운영 0·동기 부등식<0 | eq:lnLq/Acut | PASS (보완2로 명료화) |
| 7 | 꼬리 충전 격자 역전, 충전=방전 거울 | eq:reversal | PASS |
| 8 | 분극 V_n=V_app−σ_d|I|R_n | eq:vn | PASS (보완1로 서술 정합) |
- 핵심 사슬(방전 V↑→탈리튬화↑→평형 peak 양수, 충전=거울) 전건 유지. **결함 0**.

## 4. 자체 검수 (가변-청크·렌즈)
- 구조·spine 정합: N0–N9 절 순서·라벨 불변, 신규 §은 N9 말미(합산 직후)라 spine 비파괴. PASS.
- 물리·부호 적대검산: 독립 서브에이전트 1차 + master 삼각검증(과전압 정의·eq:vn 부호·컷 상수성). PASS.
- G-follow/G-usable: 보완 모두 기존 식 사슬 내 인라인 참조만(orphan 0), 신규 표는 기존 라벨만 인용. PASS.
- 시각(PDF): 5·13·14·16·17쪽 렌더 확인 — 신규 표 마진 내 정렬, overfull hbox **0**, undefined ref/cite **0**.
- 직전 수정 새 결함: 235/240/560/신규표 상호 부호 일관(η>0 ↔ V_n<V_app ↔ 표 9행) 재검. PASS.

## 5. 그림·표 목록 (이번 추가)
- `tab:signregression`(신규, p.17): 부호 회귀 self-test 9행. 위치 = N9 닫힌식·재현성표 뒤, 도착 앞(부호 사슬 마무리로 자연 위치). 기존 그림·표 불변.

## 6. Decision Queue
- **DQ-b1 (정보 보고)**: `v11_flowchart.md` L88 괄호 `방전 시 관측 V 가 평형보다 낮게 읽힘`은 eq:vn(V_n=V_app−|I|R_n) 및 물리(anodic 과전압 양수)와 **반대**. flowchart 가 master 권위 원본이라 본 작업 sub 는 **미수정**(경계 준수). master 가 spine 정정 여부 판단 요망. v7-05b 본문은 식·코드에 맞는 올바른 방향으로 적었음.

## 7. 빌드 결과
- `xelatex -interaction=nonstopmode v7-05b.tex` ×2(pass1 17쪽→pass2 18쪽, ref 수렴).
- **에러 0 · undefined ref 0 · undefined cite 0 · overfull hbox 0**. 산출: `v7-05b.pdf`(18쪽, 359 KB).
