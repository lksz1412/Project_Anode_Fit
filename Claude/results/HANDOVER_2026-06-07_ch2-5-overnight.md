# HANDOVER — Ch2~5 야간 자율 초안 (2026-06-07)

## Chain 헤더 (거슬러 올라갈 위치)
- 본 handover ← (Ch1 작업: F 교과서화 + G §8~10 이해보완, 동일 세션 연속 — 별도 handover 없이 본 문서가 Ch1 완료 후 Ch2~5 진입 기록)
- 상위 트랙 인계: `Claude/results/Archive_oldtrack/HANDOVER_RB_2026-06-02b.md`(구-track rb-rebuild) — 구-track Ch1~5 는 archive 로 이동, 신규 트랙으로 재작성 중.

## 1. 본 세션 지시 (전문, 생략 없이)
사용자: "지금 작업한 내용과, 형식 그리고 작업방법을 그대로 따와서 챕터2~5를 밤새 진행한다. 현재 새벽 2시30분이므로 나는 자러가니 니가 최대한 현재 챕터1과 정합성이 있도록 초안 작성을 해놓길 바란다. 당연히 작업은 계획서 → 절 별로 작업 → 문제 없을 때까지 검수 → 앞 절과의 관계 검토 → (끝까지 반복) → 저장 → 커밋,푸쉬 같은 형식을 지켜야하는건 동일한데, 이제 챕터 2부터는 이전 챕터까지도 함께 검토를 진행해야한다."
- 즉 Ch1(확정본) 의 \*내용 방식·형식·register·작업방법\* 그대로 Ch2~5 초안, Ch1 최대 정합, Ch2부터 \*이전 챕터까지 함께 검토\*.

## 2. 수행 결과 (chapter 별 상태)
프로젝트 P1: Ch2=발열, Ch3=반응속도론, Ch4=통합 상태방정식, Ch5=히스테리시스.
계획서: `Claude/plans/2026-06-07-ch2-5-rebuild-consistent-with-ch1-plan.md`(챕터 H).
구-track 물리 source: `Claude/work/oldtrack_src/graphite_ica_ch[2-5]_rebuilt.tex`(zip 백업서 추출, 물리 \*재료\*).

| Ch | 파일 | 줄/p | 빌드 | Codex 검수 | 상태 |
|---|---|---|---|---|---|
| **2 발열** | `graphite_ica_ch2.tex` | 589·12p | GREEN | \*완료\*(8 MAJOR+MINOR) → \*핵심 5건 수정\* | **검수+1차정정** |
| **3 반응속도론** | `graphite_ica_ch3.tex` | 762·16p | GREEN | \*미실시\* | **초안(빌드 clean)** |
| **4 통합 상태방정식** | `graphite_ica_ch4.tex` | 841·16p | GREEN | \*미실시\* | **초안(빌드 clean)** |
| **5 히스테리시스** | `graphite_ica_ch5.tex` | 838·16p | GREEN | \*미실시\* | **초안(빌드 clean)** |

- Ch2 = Claude 직접 작성(exemplar). Ch3~5 = 병렬 subagent 가 Ch1·Ch2 exemplar + 구-track 물리로 port(엄격 표기/register 규칙). 4개 전부 독립 컴파일 GREEN(0 err/undefined ref·cite/overfull; 잔존 경고는 한글 italic 폰트 fallback — Ch1 과 동일 무해).
- 커밋·푸쉬 완료(버전마다, origin/rb-rebuild-2026-05-30): `310310a`(Ch2)·`5a0fffe`(Ch3-5 초안)·`ed80de2`(Ch2 정정). [[feedback_anode_fit_auto_commit_push]] 적용.
- 표기 정합 맵 일관 적용: $s_{\phi,j}{\to}s$·$Q_{j,\tot}{\to}Q_j$·$\chi_j{\to}\chi$·$V_{n,\app}{\to}V_\app$·$V_{n,\drive}{\to}V_\drive$·$\Delta S_{\rxn,j}{\to}\Delta S_j$. $Q_p\cdot\Theta$ 미사용(Ch1 형식). linkbox→inheritbox, \AL/BOUNDED/CHARTER/AL원장절 → 박스 흡수. "질문./물리./(무비약)" 라벨 0. 각 챕터 inherit 절(C1~C6/C7)로 Ch1(·앞 챕터) 기준식 수령.

## 3. 미완료 항목 (다음 세션 우선순위)

### (A) Ch2 잔여 Codex 정정 — \*부분 수정, 나머지 미반영\*
Codex Ch2 검수(8 MAJOR) 중 \*수정 완료\*: C4 k_act/k_eff 구분·$\dot{\mathcal Q}_{\rev,j}$ rename(q 충돌)·서론 ΔS_j conflation·열 kernel 1/L(per-time↔per-capacity)·"novel" 제거.
\*미반영(다음 세션)\*:
- **B4**: `eq:ch2_consistency` boxed 등호가 boundbox 의 부분조건과 어긋남 → 가정(등온·준정적·단일 우세 transition 또는 $D_q$ 정규화)을 식 display 안에 명시하거나 reaction-entropy 성분만 투영.
- **B6**: $\dot{\mathcal Q}_{\irr}=|I|\eta$ 축약 시 background·ohmic 전류 처리 명시(현재 $\eta\ge0$ 전제만).
- **B7**: `eq:ch2_sigma`·`eq:ch2_qirrkin_ext` 의 bare $k_j$ → $k_j^{\eff}$(또는 활성화 지배 한정 명시).
- **C1**: $I_j$·$s^{\conv}$·$h_\bg$ 가 정의 전 사용(first-use 인라인 정의 추가). $\dd q_{\irr,\kin,j}$ 의 소문자 q(열) → $\mathcal Q$ 로 rename(잔여 q 충돌).
- **A1**: C3 의 $k_j^{\eff}$ 사용을 Ch1 $k_j$(=$r^++r^-$) 의 압축임을 한 줄 명시.

### (B) Ch3·Ch4·Ch5 — \*deep Codex 물리·정합 검수 미실시\* (최우선)
초안은 빌드 clean 이나 \*물리 정확성·Ch1 정합·이전 챕터 정합\*은 Claude/Codex 깊은 검수를 \*안 거침\*. subagent 가 Ch2 를 exemplar 로 썼으므로 \*Ch2 와 같은 결함이 전파됐을 가능성\* 높음(특히 k_eff/k_act 구분, q 기호 충돌, prose conflation). 각 챕터:
1. Codex foreground 적대 검수(Ch2 검수 프롬프트 양식 재사용) — A.Ch1정합 B.물리정확 C.무비약 D.register E.\*이전 챕터 정합\*(Ch3↔Ch2, Ch4↔Ch1-3, Ch5↔Ch1-4 의 inherit 식 ↔ 앞 챕터 실제 식·전달항목 교차매핑).
2. 판정(타당/오바/구라) → 수정 → 재검수 문제 0까지 → 커밋.
3. subagent 보고의 의심점 확인: Ch5 의 $\Pi_j$(Ch2 가역열 표기와 대조)·reynier/bazant 인용 위치 / Ch3 의 $\chi\equiv\beta_j$ 조건부 동일물 / Ch4 의 bernardi1985 서지.

#### Ch3 Codex 검수 결과 (실시 완료 — 정정 fix-list)
빠른 register MINOR \*수정 완료\*: 서론 수사의문문→평서·"무비약으로" 메타 태그 제거.
\*미반영 MAJOR(다음 세션, 정밀 물리 수정)\*:
- **A3(MAJOR)**: Ch3 가 $\mathcal A_j=s\,n_j^{\eff}F(V_\drive-U_j)$ 로 \*Ch1 의 $\mathcal A_j=sF(V_\drive-U_j)$ 재정의\*. → Ch1 $\mathcal A_j$ 유지하고 일반화는 \*별도 기호\*($\mathcal A_j^{\mathrm{gen}}$ 등)로, 또는 controlled generalization 명시.
- **B3(MAJOR)**: $\beta_j\equiv\chi$ 를 "대칭 Marcus 극한"에서만 동일물이라 했으나, Ch1 $\chi$ 는 BV/BEP \*전달계수\*(대칭 Marcus 는 $\chi=1/2$ 특수값). → "$\beta_j$ 는 같은 전달계수 규약 하 Ch1 $\chi$ 와 동일; 대칭 Marcus 가 유일 조건 아님"으로.
- **B3/B4(MAJOR)**: $\alpha_n=1-\beta_j$ 라 했다가 뒤에서 $\beta_j(=\alpha)$ — 불일치. → $\beta_j$ 또는 $\alpha_n=1-\beta_j$ 일관, $\beta_j\ne\alpha_n$.
- **B5/C(MAJOR)**: $C_j(\xi_j,T)$ 인데 $a_j^\pm(\xi_j,V_n,T)$ 라 $V_n$ 의존 가능 → $n_j^{\eff}=RT/(Fw_j)$ 기울기 유도는 $C_j$ 의 $V_n$ 무관 전제 필요. → $C_j(\xi_j,V_n,T)$ 로 정의 후 partition 가정 명시하고 box.
- **E(MAJOR)**: Ch2 가 넘긴 $\eta_j$ \*메커니즘 분해\*($\eta_\kin+\eta_\ohm+\eta_\conc$)를 Ch3 가 apparent $R_n$ 분해만 하고 닫지 않음. → $\eta_j$ 메커니즘 분해 표 추가(apparent $R_n$ shift 와 분리).
- **MINOR**: C4 가 $k_{j,\mathrm{act}}\simeq k_0 e^{-(\Delta G_a-\chi\mathcal A_j)/RT}$($\mathcal A_j\gtrsim RT$) 형 미재현(Ch2 와 동일 k_eff/k_act) · 미인덱스 $\theta$(→$\theta_j$) · `eq:ch3_drive` overfull 위험(aligned 분할).

#### Ch4 Codex 검수 결과 (실시 완료 — fix-list)
\*수정 완료\*: "(피팅 X)"→"피팅 대상 아님"·$q_{\rev,j}$→$\dot{\mathcal Q}_{\rev,j}$(q 충돌).
\*미반영(다음 세션)\*:
- **A/E(MAJOR) 𝒜_j 일반형**: Ch4 가 $\mathcal A_j=sF(V_\drive-U_j)$(Ch1 이상형)만 계승, Ch3 일반형 $\mathcal A_j=s\,n_j^{\eff}F(V_\drive-U_j)$ 미반영(L121 C4·L217·L220·L399). → \*\*cross-chapter 해법(아래 §𝒜)\*\*.
- **B4(MAJOR)**: `eq:ch4_qrev_micro`($s I_j\Pi_j$)가 Ch2 boxed Bernardi $\dot{\mathcal Q}_{\rev,j}=T\Delta S_j I_j/(sF)=I_j\Pi_j$(Ch2 L293-300)와 명시 연결·reaction/activation entropy 분리 출처 미연결. → Ch2 식 명시 참조 추가.
- **B5(MAJOR/SUSPECT)**: 전기-열 coupling 순서서 $\dd\xi_{\eq,j}/\dd t$ 안에 $(\partial\xi_{\eq}/\partial T)(\dd T/\dd t)$ 가 $\dd T/\dd t$ 결정(L733) 전에 쓰임 = same-step 순환(Ch2 L480-492 회피 패턴과 불일치). → implicit DAE 명시 / predictor / 순서 재배치.
- **MINOR**: `eq:ch4_affinity_eta` $s$ 일반화 박스(방전 한정, $s$ 는 Ch5 이월 명시) · $R_{\transp,n}$ 미정의 기호 → 기호표 추가 · L313 "이 절이 본 장의 핵심이다" rhetorical 제거.

#### Ch5 Codex 검수 결과 (실시 완료 — fix-list, \*가장 많은 HIGH\*)
\*미반영(다음 세션, 정밀 물리)\*:
- **B-1(HIGH) 충전 logistic 부호**: Ch5 가 충전서 logistic 지수 부호 반전을 "유도"라 주장하나, Ch1 좌표 $\xi_j=1-\theta_j$ 유지하면 평형 logistic 은 충·방전 모두 단조증가 → 부호 반전은 \*좌표변환 없이는 가정\*. → 충전 진행 좌표 $\zeta_j=1-\xi_j$ 도입해 명시 유도, 또는 "규약 선택"으로 수위 낮춤(L247-259·257). \*\*Ch1 정합의 핵심\*\*.
- **B-2(HIGH) 두 평형**: Ch5 가 branch 평형 $\xi_{\eq,j}^b$ 와 metastable $\xi_{\tar,j}^b$ 둘 도입. Ch1 은 detailed-balance 진평형 $\xi_{\eq,j}$ \*하나\*. → $\xi_{\eq,j}$=진평형 예약, $\xi_{\tar,j}^b$=metastable target 전용.
- **A/B-3(HIGH) η 에 부호 삽입**: $\eta_j^b=s_{\phi,j}^b[V_\drive-V_{\eq,j}^b]$ 재정의 — Ch2/Ch4 는 η 에 부호 안 넣고 affinity 에서 처리(이중 부호 충돌). + L477/487 $\eta_{\prog}^\chg$ 부호 모순(>0 then <0). → $\eta_j^b=V_\drive-V_{\eq,j}^b$(무부호), 부호는 $I_j$/affinity 로; signed 진행력은 별도 명명.
- **B-6(HIGH) full-cell η_loss 부호**: `eq:ch5_fullcell` 정의부와 L595-596 닫힘의 $(\Delta V_{n,\pol}-\Delta V_{p,\pol})$ 부호 순서 불일치. → 부호 정합.
- **B-4(MED)**: 방전 단독 극한 환원이 $\dd Q_\bg=0$ 조건 요구 — Ch1 보존식은 $Q_\bg$ 포함이라 조건 없이 환원돼야. → 기준 상수 조정.
- **MED/SUSPECT**: $n_j^{\eff,b}$ 일관(기저 $n^{\eff}$ 혼용 L271-275) · $R_{n,\pol}^b\equiv R_n^b+R_\ct^b$ 이중계산 위험 · $U_j^b$ 반응방향 부호($-1/(s^bF)\partial G^b/\partial n$) · $\Delta S_j^b=s^b F\partial U_j^b/\partial T$ 명시 · hysteresis center/$h_j$ 완화는 \*ansatz\* 명시.
- **정상 확인**: $\Pi_j$(Ch2 정합)·$\chi$(Ch1 전달계수)·$Q_j$(구-track 잔재 0)·$q_\stt$(Ch1 q 와 구분).

#### §𝒜 — 𝒜_j cross-chapter 해법 (Ch1/3/4/5 일관, \*반드시 한 번에\*)
detailed balance($\ln(r^+/r^-)=\mathcal A_j/RT$)가 logistic logit $(V_n-U_j)/w_j$ 와 \*모든 $V_n$\*에서 같으려면 $\mathcal A_j=(RT/w_j)(V_n-U_j)=s\,n_j^{\eff}F(V_n-U_j)$, $n_j^{\eff}=RT/(Fw_j)$. \*\*즉 일반형 $\mathcal A_j=s\,n_j^{\eff}F(V_\drive-U_j)$ 가 옳고, Ch1 의 $sF$ 는 이상($w_j=RT/F$, $n^{\eff}=1$) 특수형.\*\* → Ch3(보유, reconcile box)·Ch4(미반영)·Ch5(branch $n^{\eff,b}$) \*모두 일반형으로 통일\*하고, "Ch1 $sF$=이상 특수형" 한 줄 reconcile 을 각 챕터 inherit 에 둔다. Codex Ch3-A3(재정의 우려)는 이 reconcile 로 해소(일반형이 물리적으로 옳음).

### (C) 통합·교차 (그 다음)
- 4개 챕터 inherit 식이 \*서로\* 일치하는지 횡단(Ch2 가 넘긴 전달항목 ↔ Ch3 inherit, …). 병렬 작성이라 drift 가능 — 교차 reconcile.
- master 문서(\\include) 또는 cross-file \eqref 연결은 추후(현재 의미 인용).
- 충전 branch 부호 $s$(Ch1 방전 +1) ↔ $s^b$(Ch5 충전 −1) 확장 일관 재확인.

## 4. 다음 세션 주의
- \*\*[[feedback_full_file_read_required]]\*\*: Ch3~5 검수 시 전문 정독(subagent 산출이라 더 엄격). [[feedback_multiagent_review_chunking]]: 분량 있으면 절별 청킹.
- \*\*Ch2 가 exemplar\*\* — Ch2 의 확정 표기·박스·register 가 Ch3~5 정합 기준. Ch2 잔여 정정(A)을 먼저 끝내고 그 기준으로 Ch3~5 검수.
- \*\*표기 충돌\*\*: 소문자 q(용량좌표, Ch1)는 \*열 기호로 재사용 금지\* — 열은 $\mathcal Q$/$\dot{\mathcal Q}$. Ch3~5 도 점검.
- \*\*k_j 계열\*\*: Ch1 = $k_j$(완화율, eq:keff Eyring), $k_j^{\eff}$(직렬 1/k_eff=1/k_act+1/k_lim). 혼용 주의.
- 구-track 의 \AL/CHARTER/AL원장/BOUNDED/GS-4 메타는 Ch1 에 없음 → 박스 흡수(가정원장 별도 절 X). Ch3~5 도 동일.
- 커밋·푸쉬는 버전마다 자동([[feedback_anode_fit_auto_commit_push]]). Codex 는 \*foreground(`--wait`)\*로만(백그라운드 시 턴 끊김·hung 사례 있었음).
- `Claude/work/oldtrack_src/` 는 구-track 물리 \*재료\*(읽기). 원본 Ch1·구-track 수정 금지.

## 5. 산출물 위치
- 신규 챕터: `Claude/docs/graphite_ica_ch{2,3,4,5}.tex`(+`.pdf`).
- 계획서: `Claude/plans/2026-06-07-ch2-5-rebuild-consistent-with-ch1-plan.md`.
- Ch1 확정본: `Claude/docs/graphite_ica_ch1.tex`(952줄·20p, F·G 완료) — 기준.
