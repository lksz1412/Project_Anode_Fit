# 재수정 계획서 — Chapter 1 (구현본 보완: 겹침 확장·staging 그림·수식 일관·χ 설명 등)

**Date**: 2026-06-03 · **Author**: Claude · **상태**: 재수정 계획. **GO 대기 — 본 turn 에 tex 수정 X.**
**대상**: `Claude/docs/graphite_ica_ch1.tex` (구현 완료·4렌즈 결함검증 통과, 747줄 GREEN). 본 계획은 그 위에
사용자 재수정 7항목을 반영한다.
**원칙**: 발췌패치로 전후 깨뜨리지 않는다 — 각 항목 적용 후 \*전 문서 재빌드 + 줄별 영향 검증\*. 분량 제한 없음
(문제 없는 논리·유도면 책 분량도 무방).

---

## §0. 사용자 재수정 항목 (verbatim 요지)

1. **□ 렌더 에러**: 6p eq(9) 이후 리튬 산화환원식의 빈자리 기호가 네모로 깨짐 → 수정.
2. **χ/(1−χ) 설명 부재**: 정반응 계수 χ, 역반응 (1−χ), 합=1 의 \*근원\*을 이해 못함 → 본문에 유도 추가.
3. **추가 보완 필요 느낌**: 많이 좋아졌으나 조금 더 보완.
4. **"다음 장으로" 절 불필요**: 로드맵은 작업자(Claude)만 보유, 문서엔 불요 → 제거.
5. **수식 배정 기준**: inline(줄글) vs numbered(정식 식)의 기준이 뭔가 → 기준 정립·일관 적용.
6. **흑연 staging 도입부 + 그림**: Ch1 초기에 상전이 간략 요약 + 가장 잘 설명한 이미지 배치(지금은 교과서 감
   잡기용; 논문화 시 교체 가능).
7. **★ 다중 피크 겹침 케이스 확장**: C-rate 커지면 피크 겹침 → OCV/저율 정보로 \{U_j,w_j,Q_j\} 고정 후, 현재
   식을 확장해 \*겹쳐진 피크들의 합산 정보\*를 구할 수 있을 만큼 \*다루는 대상 케이스 확장\* 확보.

## §0bis. χ/(1−χ) 합=1 의 근원 (사용자 질문 답 — 본문에 들어갈 핵심)

전달 계수 $\chi$ = 전이상태의 \*반응 좌표상 분율 위치\*(0=반응물 쪽, 1=생성물 쪽, ½=가운데). 구동력
$\mathcal A_j$ 가 두 우물의 상대 높이를 기울이면, \*같은 한 점\*인 전이상태가 그 분율만큼($\chi\mathcal A_j$)
따라 내려가 — \*forward 장벽은 $\chi\mathcal A_j$ 내려가고 backward 장벽은 $(1-\chi)\mathcal A_j$ 올라간다.\*
\textbf{합이 1인 이유 = detailed balance}: 정/역 속도 비 $r^+/r^-=e^{[\chi+(1-\chi)]\mathcal A_j/RT}=e^{\mathcal A_j/RT}$
가 자유에너지 차의 Boltzmann 인자와 같으려면 두 계수 합이 \*정확히 1\* 이어야 한다(아니면 평형 상수가 열역학
구동력과 어긋나 detailed balance 위반). 즉 χ 는 자유 파라미터지만 "χ·(1−χ) 합=1"은 \*두 방향이 같은 전이상태를
공유\*함의 대수적 귀결이며, eq:db 에서 χ 상쇄·평형 target 불변을 보장하는 바로 그 조건이다.

## §1. 수식 배정 기준 (Notation policy — 정립·적용)

\textbf{기준(정립)}: 식이 (i) 다른 곳에서 \eqref 로 \*참조\*되거나, (ii) \*핵심 결과\*(boxed)이거나, (iii) \*다단
유도의 명시 단계\*이면 \textbf{numbered display}. (iv) 즉시 쓰고 마는 \*단순 중간 표현\*은 \textbf{inline}. 박스
안 식은 줄기 밖이라 inline 유지(규약 정합).
\textbf{현황}: 본문은 이미 이 기준에 거의 부합(numbered 30개 모두 참조·핵심·다단). \textbf{유일 불일치}: L500
`\xi_{\sstat,j}=\xi_{\eq,j}` (detailed balance 증명의 \*결론\*, L503 이 "정확히 일치"로 참조하는 load-bearing
결과)가 `equation*` 무번호 → \textbf{numbered 승격(label `eq:sseq`)}. (L327 logistic 도함수 항등식은 선택적
승격 후보.) 강등 권장 0.

## §2. ★ 다중 전이 겹침 확장 (가장 큰 보완 — 신규 절)

\textbf{목표}: 단일 전이 $j$ 로 좁혔던 §2~6 을 \*$N_p$ 전이 합산\*으로 복원해, 고율서 겹치는 peak 들의 \*합산
형상\*을 OCV-anchored 로 예측한다.
\textbf{재사용 자산(신규 유도 최소)}: eq:charge(이미 $\sum_j Q_j\xi_j$), \textbf{eq:dQdV(이미 $C_\bg+\sum_j Q_j
\dd\xi_j/\dd V_n$ 총합 전개 존재)}, eq:closed(단일 $j$ 종합식), 식별 S1(OCV 로 $\{U_j,w_j,Q_j\}$ 고정).
\textbf{신규 절 spec(§ 신설, 약 30~50줄; 위치 = §종합 뒤 또는 §반증 앞)}:
1. \textbf{총합식 본문 승격}: $\dd Q/\dd V_n=C_\bg+\sum_{j=1}^{N_p}Q_j\,\dd\xi_j/\dd V_n$ 를 본문식으로 박고, 각 $j$
   항이 eq:closed 의 (평형 rise $-$ 지연 꼬리) 구조임을 전개. (현재 §7 boundbox "선형 중첩" 한 줄을 절로 승격.)
2. \textbf{겹침 식별 부등식(신규 1~2식)}: 인접 $j,j{+}1$ 이 겹치는 조건을 정량화 — 평형 분리 한계
   $|U_{j+1}-U_j|\lesssim\Delta V_{1/2}=3.53\,w_j$(eq:eqpeak 재사용) + 동역학 꼬리 겹침 $L_{V,j}\gtrsim
   |U_{j+1}-U_j|$(eq:tail 재사용). 저율 분리 → 고율 융합 전이를 이 부등식으로.
3. \textbf{OCV-anchored 분해/예측 절차(enumerate)}: (S$_1'$) 저율 OCV 로 $j$별 $\{U_j,w_j,Q_j\}$ 고정 →
   (S$_2'$) 각 $j$ 의 logistic 상승부 + 지수 꼬리(eq:simplefit)를 고율 파라미터$\{\Delta H_a,\chi\}$로 생성 →
   (S$_3'$) $\sum_j$ forward 합산 → (S$_4'$) 융합 데이터와 대조. \*역산 아님(forward 예측; 비유일성 정책 L597 정합)\*.
4. \textbf{분리 한계 명시}: peak 융합 시 $j$별 면적 분리는 OCV anchor 없이 불가(공선형; L656 논리 확장).
\textbf{신규 유도 = 부등식 1~2개 + 절차}; 핵심 식은 재사용.

## §3. 흑연 staging 도입부 + TikZ schematic (교과서 감)

\textbf{위치}: 서(序)의 관찰 quote 직후 ~ "전개의 뼈대" 앞. \textbf{박스}: `\newtheorem*{stagebox}{흑연 staging 배경}`
신설(배경이라 keybox 와 구분). \textbf{요약 내용(3~5줄)}: stage $4\to3\to2\mathrm L\to2\to1$ 구조·조성
(LiC$_{72}$/LiC$_{36}$/LiC$_{18}$/LiC$_{12}$/LiC$_6$ 근사)·각 전이가 dQ/dV peak $j$ 를 만든다·인접 융합으로
$N_p\approx3\sim4$. \textbf{그림(TikZ 자체 제작 — 저작권 회피)}: preamble 에 `\usepackage{tikz}`. 좌 패널=stage
모식(흑연 층 사이 Li 채움 패턴 5단 + stage·조성 라벨), 우 패널=대응 모식 dQ/dV vs $V$ 에 peak $j$ 배치 + 비대칭
꼬리 1개(저온 긴 꼬리 예고), 화살표로 stage↔peak 연결. \textbf{캡션}: "모식도(정량 스케일 아님; 정량은 본문 식);
논문화 시 실측 그림으로 교체". (그림은 배경 — 본문 줄기 무관, L12 규약 정합.)

## §4. χ/(1−χ) 설명 추가

\textbf{위치}: eq:bv(L490) 직후, "평형은 그대로" 문단 \*앞\* 새 문단 3~5줄. \textbf{내용}: §0bis 의 detailed-balance
유도(전이상태 분율 위치 χ → forward $-\chi\mathcal A$·backward $+(1-\chi)\mathcal A$ → 합=1 강제). cite 기존
`evanspolanyi1938`,`bardfaulkner` 재사용. 박스 아닌 본문(L504 "평형 target 불변"의 직접 근거).

## §5. "다음 장으로" 절 제거

L717~726(구분주석·`\section*`·`\addcontentsline`·본문) 전체 삭제. 직전 §반증(falsify, L715 결론적 톤)이
자연스러운 끝. dangling 0 확인(이 절엔 label 없음, 내부 \eqref 는 절과 함께 소멸). 목차 자동 갱신.

## §6. □ 렌더 에러 수정

L278 `\mathrm{Li}^++e^-+\square\rightleftharpoons\mathrm{Li}_{(\text{graphite})}` 의 `\square`(폰트 누락) →
`[\,]`(빈자리 표준, 폰트 비의존) 또는 host 명시 `\mathrm{C_6}`(LiC$_6$ 생성 엄밀형). 권고: `[\,]`(최소수정).
문서 내 `\square` 유일 1곳.

## §7. 기타 완성도 보완 (우선순위순; 선별 적용)

- [높음] 단일 삽입반응식 ↔ stage-$j$ 전이 연결 단서 1문장(L276~283: "각 stage 전이를 유효 삽입반응으로 본
  coarse-grained 표현"). χ vs 전기화학 표준 α 표기 1구절(L153 또는 483: "통상 α; 본 장 χ").
- [중간] 검산 verifybox 균형(eq:arrhenius 에 "절편 $=\Delta S_a/R$" 차원검산 1박스). 대표 수치 예시 1~2개(1C·상온
  에서 $L_{q,j}$·높이 $Q_j/4w_j$).
- [낮음] $\Omega_j\!>\!2RT$ 상분리(miscibility gap) 단서 1~2줄(flagbox 확장; 논문 reviewer 예상 질문). $s_I$
  부호 정합 재확인(L633 표 "$+s_I|I|R_n$" = 방전 시 apparent 상승).

## Phase Range (재수정 실행 순서)

| Phase | 작업 | Step | 비고 |
|---|---|---|---|
| RR.1 | 국소 편집: □(§6)·"다음장" 제거(§5)·수식 승격(§1)·χ 설명(§4) | 1–4 | 저위험, 빌드 확인 |
| RR.2 | 다중 전이 겹침 신규 절(§2) | 5–8 | 신규 유도 일부, 핵심 |
| RR.3 | staging 박스 + TikZ 그림(§3) + preamble tikz | 9–11 | 그림 제작 |
| RR.4 | 기타 보완(§7) 선별 + 전 문서 재빌드 + 줄별 영향 검증 | 12–15 | 정합 |
| RR.5 | 적대검증(물리·무비약·정합) + 수정 + Decision Gate | 16–18 | 결함 0 확인 |

## Non-goals
- 자기참조 Volterra·closure·solver(부록/이후). 그림을 \*외부 저작권 이미지\* 복사(TikZ 자체 제작). 단일전이 식의
  물리 재유도(이미 검증 통과 — 겹침은 \*합산 확장\*이지 재유도 아님). Workflow 도구(Agent only).

## Test Plan (게이트)
- **G-build**: 매 Phase 후 전 문서 재빌드 GREEN(`!`0·undefined 0·dup 0), □ 렌더 정상.
- **G-coherence(★ 발췌패치 금지)**: 각 편집 후 \*전후 문맥\* 줄별 영향 확인(dangling·중복·모순 0). 겹침 절이
  단일전이 §2~6 과 정합(Σ_j 복원이 기존 단일 j 결과의 합).
- **G-overlap**: 겹침 절이 총합식·식별순서·비유일성 정책과 정합; 부등식이 검산됨; 역산 금지 일관.
- **G-eqpolicy**: §1 기준으로 inline/numbered 일관(L500 승격 반영).
- **G-noleap·G-undergrad·G-ground·G-nostep·G-jindex**: 기존 게이트 유지(추가분도 무비약·grounded·$\xi_j$ 일관).
- **G-figure**: TikZ 그림 빌드 정상·캡션에 "모식도·교체 가능" 명기.

## Decisions Required (평문, 무응답 시 권고값)
- **D-겹침 위치**: 다중 전이 겹침을 \*독립 신규 절\*로(§종합 뒤). 권고: 그대로.
- **D-그림**: 지금은 \*TikZ 자체 제작 schematic\*(저작권 안전, 교과서 감), 논문화 시 실측 교체. 권고: 그대로.
  (외부 특정 이미지를 원하시면 출처 주시면 캡션 인용으로.)
- **D-□ 교체**: `[\,]`(최소수정) vs `\mathrm{C_6}`(화학 엄밀). 권고: `[\,]`.
- **D-기타 범위**: §7 [높음]·[중간]까지 적용, [낮음]은 선택. 권고: [높음]+[중간] 적용.

## Correction History
| 일자 | 변경 |
|---|---|
| 2026-06-03 (RR v1) | 구현본 결함검증 통과 후, 사용자 재수정 7항목 반영: □ 수정·χ 합=1 설명·"다음장" 제거·수식 배정 기준 정립(L500 승격)·staging 도입부+TikZ·\textbf{다중 전이 겹침 확장(OCV-anchored 합산/예측)}·기타 완성도. 발췌패치 금지(전 문서 재빌드·줄별 정합). |
