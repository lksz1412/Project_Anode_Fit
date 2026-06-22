# v6 작업물 10회 가변-청크 검수 (사용자 지시)

> 대상 = v6 문건(graphite_ica_ch1_Opus_v6.tex) + Task A(BD Anode_Fit 코드 플로우차트 코멘트)+코드검토. 방법론 §3: 매 라운드 청크·렌즈 전환, 수렴=연속 2R 0확정결함. 이전 V6 "수렴" 미신뢰·fresh.

## Wave 1 (R1–R5) — 완료
| R | 청크 / 렌즈 | 확정 결함(수정) |
|---|---|---|
| R1 | 절별 / 물리·화학·수리 적대 재유도(SymPy+수치) | 0 (17절 박스식·verifybox 전수 PASS, 최약 3곳 기각) |
| R2 | 식별 / G-follow·의존 정합 | 0 CRITICAL (sub 과장 2건=j첨자·s_I "orphan"은 §1.1 정의됨, master 기각) |
| R3 | 전체 통독 / 완결성·orphan·흐름도순 | 0 break (절순서 흐름도 정확 일치, orphan·dangling 0) |
| R4 | 도메인 그룹 / 기호·부호·정의역 | **1 확정** — σ_d 작용처 열거 불완전(코드 A_d의 σ_d 누락) |
| R5 | 라인/페이지 / 시각 렌더 41p | 0 (잘림·겹침·overfull·셀오버플로 0) |

### 수정 3건 (master 삼각 후 직접)
1. σ_d 작용처(R4 확정) — "세 작용처(분극·분기중심·꼬리방향)" → 동역학 L_q 평가 시 꼬리 구동력 정렬 $\mathcal A_j^d=\sigma_d F(V_{a,j}-U_j^d)\ge0$ 추가(코드 A_d 와 정합).
2. master→hysobsgap forward(R3) — eq:hysobsgap 참조에 "(§hyspol 에서 유도)" signpost(재배열 master↔hyspol swap 유발).
3. L1268 오타 — `\end{equation}(전이대` 공백 누락 → 개행.

### 삼각 기각(빈 통과 방지·과잉수정 방지)
- binodal/gprime 번호역행(R2 #1): eq:binodal(L704)이 RT ln+Ω 닫힌 꼴을 명시해 G-follow 자족, "아래 식"은 naming → soft, 비수정.
- regsol peak 3중진술(R3 #1): thermo 기원(접선=평탄전위) vs charge 관측(dQ/dV) = 점진 정교화, 모순 아님.
- sec:inputs U^d 직렬화(R3 #3): L107 roadmap("상분리·분기중심 regsol--hys")과 이미 정합.
- charge 서로소·gprime V_n표기·b_j cross-ref·w_j 이중의미·j첨자: v5 내재·산문 받침, 비수정(과잉수정 경계).

빌드 0/0/0 41p · listing↔aux OK · 97식.

## Wave 2 (R6–R8) — 완료
| R | 청크 / 렌즈 | 확정 결함(수정) |
|---|---|---|
| R6 | v5↔v6 절별 / 내용 보존 감사(완성도≥v5) | 0 (v6 ≥ v5 YES, 누락·왜곡·중복 0, 정보 순증) |
| R7 | Task A 코드+코멘트 / 코드↔코멘트↔검토 정합 | **2 확정**(W2 [F] affinity 4RT·dead branch 미명시 / 검토 line번호 stale) |
| R8 | 인용 / 인용-사실 호응 | 1 의심(D-H 원전 1969 누락, McKinnon 리뷰만) |

### 수정 (master 직접)
1. **D-H 원전 추가(R8)** — `daumas1969`(C. R. Acad. Sci. C 268,373,1969) bibitem 신설 + L438 도메인 모델 명시처에 `\cite{daumas1969,mckinnon1983}` 병기. bibitem 19→20, undefined 0.
2. **[F] 코멘트(R7 W2)** — 플로우차트 [F]에 "A=전이당 대표 affinity(_resolve_lag_length 4RT 상수)" 명시 + "A<3RT 보정은 직접 affinity 입력 시만 발동, 4RT 경로엔 dead branch" 단서. (BD 코드, 디스크.)
3. **검토 line번호(R7)** — H1/H2/M2 의 stale line 번호(코멘트 추가로 ~46줄 이동)를 함수 기준(`_resolve_lag_length`·`dqdv` 등)으로 갱신 + dead branch 명시. (BD 검토 문서.)

### 삼각 기각/판정
- R7 W1((1.82) eq:total): v4/v5 에 실재(합산식)·코드 v4 번호와 정합 → R7이 코드만 보고 과플래그, 정확. 비수정.
- R7 W3(equilibrium() docstring (1.94)): 사용자 원 코드 docstring — 코멘트 추가 범위 밖, 비수정(보고만).
- R6 master signpost "(§hyspol 에서 유도)": R3 요청 추가분, R6은 약간 무겁다 보나 정확·비차단 → 유지.

빌드 0/0/0 41p · undefined 0 · 20 bibitem.
