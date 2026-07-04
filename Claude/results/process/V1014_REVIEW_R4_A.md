# V1.0.14 P4.1 R4 검수 — 검수자 A (참조 무결 렌즈)

- 대상: `Claude/docs/v1.0.14/graphite_ica_ch1_v1.0.14.tex`(3235줄, 전문 정독) · `graphite_ica_ch2_v1.0.14.tex`(783줄, 전문 정독) · `appendix_phase_separation.tex`(486줄, 전문 정독). 3파일 모두 offset/limit 분할로 head→tail 전 구간 커버(중간 추정 없음 — ch1 은 최초 3062줄 청크 이후 tail 172줄을 추가로 재정독해 3235줄 전체 확인, appendix 는 441→486줄 실측 재확인 후 442–486 추가 정독).
- 렌즈: 참조 무결 — R1~R3 대규모 정정 이후의 여파 전수. 방법 = (1) 전문 통독 1회 (2) `\label`/`\ref`/`\eqref` 전수 추출 후 라벨-참조 집합 대조(PowerShell 정규식 스크립트, 3파일 개별) (3) 지정 라벨 10종 개별 문맥 검증 (4) 상대위치·전방약속 어휘(다음 절/앞 절/바로 아래/가 닫는다/가 다룬다) grep 전수 및 실제 절 순서 대조 (5) ch1↔ch2 평문 교차참조("Chapter 2 의 식 (eq:xxx)") 전수 대조 (6) 배경 컨텍스트로 `V1014_EXECUTION_LEDGER.md`·`V1014_REVIEW_R1~R3_*.md` 확인 — R1-R3 가 실제로 무엇을 정정했는지 확인해 "여파" 점검 대상을 좁힘. 파일 수정 없음(보고서만 신규 작성).
- 표기: 심각도 CRIT/HIGH/MED/LOW. 원문 인용 + 줄번호 병기.

---

## 검사 범주별 수행 내역 및 근거

### ① eqref/ref 라벨-내용 정합 (지정 10 라벨 포함)

전 라벨(ch1 175개·ch2 38개·appendix 30개)과 전 참조(ch1 157개·ch2 35개·appendix 16개)를 정규식으로 추출해 대조. **댕글링 참조(라벨 없는 곳을 가리키는 \ref/\eqref) = 0건, 3파일 전체**(PowerShell 스크립트 출력, 아래 재현 가능).

지정 10 라벨 개별 문맥 검증(라벨 정의 내용 vs 모든 참조처의 서술 내용 대조):

| 라벨 | 정의 위치 | 참조처 수 | 정합 판정 |
|---|---|---|---|
| `eq:branch` | ch1 L1878 (평형/꼬리 이산 분기) | 1851(선행 캡션 forward-ref)·1870·1944·3046·3057·3144 | PASS — 전 참조처가 "이산 분기 스위치" 개념과 정확히 일치 |
| `eq:center` | ch1 L1142 (분기 중심 배열 대입형, `eq:Ubranch`의 배열-브로드캐스트 특수형) | 1144·1251·2933 | PASS — `eq:Ubranch`(L1128, 스칼라 shift 정의)와 별개 목적(배열 U_j 에 대표-T 스칼라 shift 를 더하는 구현형)으로 명확히 구분되어 있고 모든 참조가 이 구분을 따름 |
| `sec:eqpeak` | ch1 L1386 (N6, 평형 peak) | 502·1197·2018·2654·3076 | PASS — L2654 "흑연 §sec:eqpeak 의 출발점인 전하 보존식은..."이 실제로 sec:eqpeak (a)단계(L1391 전하보존식)와 축자 일치 |
| `sec:lco-hys` | ch1 L2259 (LCO order-disorder/MIT 정규용액) | 595·2094·2103·2348·2414·2435·2705·2710·2791 | PASS — 특히 L594-595 Part 0 의 forward 약속("Ω_j^cat 은 표 밖 — 피팅 배정 전제, §sec:lco-hys")이 L2286-2290 "표~tab:lco-staging 는 Ω_j^cat 수치 열을 싣지 않으며... 미배정 시 Ω=0" 로 정확히 이행됨 |
| `sec:appendix-code` | ch1 L3066 (구현 대응표, "부록 B") | 267·1008·1794·2921·2944·2950 | PASS — 최초 3062줄 청크 정독 시 라벨을 못 보고 "orphan 아닌가" 의심했으나 재정독으로 L3066 존재 확인(3235줄 전체 재확인 완료, 오검출 자체 정정) |
| `eq:widthbudget` | ch1 L1521 (broadening 분산 예산) | 1526·1558(캡션) | PASS |
| `eq:psdconv` | ch1 L1577 (PSD 합성곱 보편형) | 1612 | PASS — "일반형~eqref{eq:psdconv} 의 반경 의존이 커널에서 소거되어" 서술이 L1571-1613 수치논증과 일치 |
| `eq:gibbsthomson` | ch1 L1583 (Gibbs-Thomson 이동) | 1645(키박스) | PASS |
| `eq:sm-epstilde` | ch1 L468 | 550 | PASS |
| `eq:sm-sint` | ch1 L513 (단일자리 vib 엔트로피 원형) | 516 + **ch2 평문 교차참조**("Chapter 2 의 vibrational 엔트로피 사슬의 단일 자리 원형") | PASS — ch2 `eq:Svib_mode`(L384-386) `S_vib,k=k_B[(1+n_k)ln(1+n_k)-n_k ln n_k]` 가 ch1 L517 이 예고한 식과 글자 그대로 일치 |

**refute 시도**: `eq:center` 를 `eq:Ubranch` 의 불필요한 중복 라벨로 의심(같은 물리량 재정의?) → L1134-1136 "전이당 필요한 것은 상수인 분기 shift 뿐이므로... 배열 중심 U_j 에 더한다"를 재정독해 배열 브로드캐스트 구현 세부를 별도로 코드화하는 목적임을 확인, 중복 아님 — 반증 실패(생존).

### ② 상대 위치 참조("다음 절/다음 소절/바로 아래/앞 절") 전수 검증

ch1 16건 + ch2 1건 + appendix 1건, 전건 grep 후 실제 다음 절/소절과 대조:

- ch1 L308 "바로 다음 절 Part 0" → 실제 다음 `\section`=sec:sm-found(P0). 일치.
- ch1 L1420 "다음 절(§sec:lag; 그 전에 아래 소절이 두-상 폭의 지위를 먼저 닫는다)" — **가장 정밀한 사례**: 문자 그대로의 다음 `\section` 은 sec:lag 이지만 그 사이에 sec:broadening 서브섹션이 끼어 있음을 저자가 명시적으로 선점 인지하고 괄호로 정정해 둠 — 재배치 이후에도 정합.
- ch1 L1991 "다음 절부터... Part II 를 건다" → 실제 다음 섹션 = sec:lco-intro(Part II 표제). 일치.
- ch1 L2517 "다음 소절 §sec:lco-gate 가 닫는다" → 실제 다음 서브서브섹션 = sec:lco-gate. 일치.
- ch2 L501 "다음 절 파생 B" → 실제 다음 `\subsection` = ssec 파생 B(L555). 일치(단, 같은 문장 안의 "수치 검증의 대상"은 사실 같은 서브섹션 내 후속 srcbox(L503-527)를 가리켜 문장 하나에 forward-subsection과 same-subsection 참조가 섞여 있음 — 물리적으로 오류는 아니나 문장 하나에서 두 시점을 겸하는 서술은 LOW 수준 가독성 이슈로 기록).
- appendix L391 "앞 절까지의 논의는 '어디가 평형인가'만 답했고" → 실제 선행 5절(mixfe·chord·binodal·spinodal·maxwell) 전부 평형 위치만 다룸, 동역학은 이 절(app:kinetics)이 처음. 일치.

**16+1+1건 중 CRIT/HIGH 급 어긋남 0건.** 유일한 관찰은 ch2 L501 의 겸용 서술(LOW, 아래 요약표).

### ③ 전방 약속("§X 가 다룬다/닫는다") - 이행 대조

ch1 3건 + ch2 1건 grep 매칭, 전건 이행 확인:

- ch1 L630 "spinodal 의 닫힌 근과... 히스테리시스 gap 은 §sec:hys 가 닫는다" → sec:hys 가 `eq:spinodal`(L1038)·`eq:dUhys`(L1107) 실제로 유도·박스화. 이행 확인.
- ch1 L2164 "★같은 logistic... 박스는 §sec:lco-code 가 닫는다" → sec:lco-code L2841-2854 에 "함수형 동형≠물리량 동일" 가드와 `eq:lco-msmrpeak` 박스 실재. 이행 확인.
- ch1 L2517 (③과 중복 표기, 위 ②에서 확인).
- ch2 L181 "두 층위 구분... 파생 C(§ssec:weff)와 파생 A 전제 명시(§ssec:overlap)가 다룬다" → ssec:weff(L570-599)·ssec:overlap 의 "★전제 명시" srcbox(L518-526) 둘 다 실재하며 정확히 그 내용(현상학적 자유 폭 지위·T-의존 함수형 확정은 후속 과제)을 다룸. 이행 확인.

**전방 약속 4건 중 미이행 0건.**

### ④ ch1↔ch2 교차 참조("그 문건 식 (eq:xxx)") 전수 대조

ch1→ch2 평문 참조 4건, ch2→ch1 평문 참조(수식 지시) 2건 — 전수 대조(라벨이 다른 파일에 있어 `\eqref` 매크로 대신 의도적으로 평문 "(eq:xxx)"를 쓰는 설계, 두 파일 모두 독립 컴파일 보존 목적과 일치):

| 참조 방향 | 위치 | 대상 | 정합 |
|---|---|---|---|
| ch1→ch2 | L451 "(eq:Z1)" | ch2 `eq:Z1`(L129, Ξ_1=1+e^{-β(ε0-μ)}) | PASS(기호 Ξ_1 통일까지 ch2 L142 가 재확인) |
| ch1→ch2 | L746 "(eq:muV)" | ch2 `eq:muV`(L152-154, μ=μ0-sF(V-Uj)) | PASS |
| ch1→ch2 | L873 "(eq:Vxi)" | ch2 `eq:Vxi`(L188-190) | PASS |
| ch1→ch2 | L1341 "(eq:logistic)" | ch2 `eq:logistic`(L165-168) | PASS(부호까지 동일 — s=+1 대입 시 축약형 일치 직접 확인) |
| ch2→ch1 | L603 "Chapter 1 eq:Ubranch 의 γ_jh_η,j=1 특수형" | ch1 `eq:Ubranch`(L1128) | PASS — γ=h_η=1 대입 시 축약식이 ch2 L602-604 형과 정확히 일치 |
| ch2→ch1 | L714 "Chapter 1 eq:xieq 에서 σ_d→s=+1·U_j(분기無)" | ch1 `eq:xieq`(L1245) | PASS — 치환 결과가 ch2 자신의 `eq:logistic` 과 일치 |
| ch2→ch1(부가) | L473 "Chapter 1 의 g_j(ξ)(그 문건 eq:gxi)" | ch1 `eq:gxi`(L615) | PASS |

**7건 전건 PASS.** 부가로 문헌 인용 위상 확인 — ch2 bibitem `msmr_partI`(JES, DOI ad1d27)과 ch1 bibitem `msmr2024`(ECS Advances "Part I", DOI ad7d1c)는 서로 다른 논문이며, ch2 자신이 각주로 이를 이미 명시 구분(L775) — R3 C-F2 정정 사항이 정확히 반영되어 있음(회귀 확인, 신규 결함 아님).

### ⑤ fig:/tab: 참조-float 배치 정합, orphan 확인

3파일 전수 라벨/참조 대조 스크립트 결과:

- **ch1**: fig 17개·tab 8개 전부 ≥1회 참조됨. orphan 0.
- **ch2**: fig 2개(`occ_config`·`blend`)·tab 2개(`ds`·`limits`) 전부 참조됨. orphan 0.
- **appendix_phase_separation.tex**: fig 2개 중 `fig:app-tangent`(L317)는 참조 2건(L222·352)이나, **`fig:app-phasediag`(L353)는 본문 어디에서도 `\ref`되지 않음 — orphan 확정.**

#### [MED] appendix_phase_separation.tex L320-354 — `fig:app-phasediag`(상평형도) 고아 그림

```
320: \begin{figure}[t]
...
348: \caption{대칭 정규 용액의 상평형 그림(신규 그림 --- 좌표는 식~\eqref{eq:app-binodal}·%
349: \eqref{eq:app-spinodal} 그대로의 수치 평가). ...}
353: \label{fig:app-phasediag}
```

이 그림(binodal `T/T_c=2(1-2ξ)/ln[(1-ξ)/ξ]` 곡선과 spinodal `T/T_c=4ξ(1-ξ)` 곡선을 겹친 상평형도)은 §app:binodal(L206-223, binodal 식 유도)과 §app:spinodal(L239-250, spinodal 식 유도) 두 절 어디의 본문에서도 `\ref{fig:app-phasediag}`로 호출되지 않는다. 유일하게 그림 자신의 캡션(L352)이 **앞** 그림 `fig:app-tangent` 를 역참조할 뿐, 정작 `fig:app-phasediag` 자신을 가리키는 산문은 3파일 전체에 0건이다(스크립트 확인, `app-phasediag` grep 결과 = `\label` 정의 1건뿐).

**"R1~R3 여파" 근거 강화**: `V1014_EXECUTION_LEDGER.md` R2 진행 로그(2026-07-04 P4.1 R2)에 "⑪[LOW C-F1] 부록 A.2 상평형도 binodal 좌표 4점(+거울 4점) 마지막 자리 정정(0.4265/0.9692/0.9865/0.9967)"이 명시되어 있다 — 이는 정확히 이 그림(appendix 두 번째 그림 = "상평형도")의 좌표 정밀도를 R2 에서 실제로 손본 이력이다. 즉 이 그림은 R1-R3 동안 활발히 수정 대상이었음에도, 정작 "본문에서 이 그림을 가리키는 문장이 있는가"라는 참조-무결 축은 R1(통독)·R2(유도 재검산)·R3(용어/어투/레퍼런스-출처) 어느 렌즈에도 포함되지 않아 그대로 남은 것으로 판단된다 — 빈 통과가 아니라 실제 이력 대조로 뒷받침된 신규 발견.

**정정 제안**: §app:binodal 박스(L206-215) 직후 또는 §app:spinodal (c) 절(L252-266, 세 영역 표 직후)에 "이 binodal·spinodal 곡선을 T/T_c-ξ 평면에 겹쳐 그리면 그림~\ref{fig:app-phasediag} 이 된다" 류의 1문장 삽입.

**refute 시도**: "`fig:app-tangent` 바로 다음에 배치되어 있어 독자가 자연히 이어서 볼 것"이라는 반론을 검토했으나, 두 그림 모두 `[t]` 배치 지정(페이지 상단 부동)이라 실제 컴파일 시 서로 다른 페이지로 분리될 수 있고, 본 프로젝트 자신이 ch1 개정이력(L34, "A3: fig:broadening 본문 \ref 추가(orphan 해소)")에서 "그림은 근접 배치만으로 충분하지 않고 본문 \ref 이 있어야 해소된 것으로 간주"하는 선례를 이미 세워 두었다 — 반증 실패, 결함 생존.

### ⑥ 부록 A 표의 근거 식 열 — R1~R3 정정 후 유효성

`V1014_EXECUTION_LEDGER.md` 확인 결과 "부록 A" = ch1 자체의 `\appendix` 절(`sec:signcheck`, "부호 사슬 검산표" — Step 10 에서 §1.13 을 이관, `\appendix` 명령으로 section 문자 A 부여)이며, "부록 B" = `sec:appendix-code`. (참고: `appendix_phase_separation.tex` 도 자체 표제가 "Appendix A" 이나 이는 별도 독립 초안 문서이고 ch1 은 이를 전혀 참조하지 않음 — 두 "Appendix A" 명칭이 서로 다른 문서에 공존하는 점은 혼동 소지가 있으나 어느 쪽도 상대를 잘못 지시하지 않으므로 CRIT/HIGH 는 아님, LOW 로 기록.)

`tab:signcheck-S`(S1-S8, "근거 식" 열)와 `tab:signcheck-R`(R1-R6, "근거 식" 열) 전 14행을, 각 행이 인용하는 `eqref` 대상의 **현재** 정의·부호와 대조 및 R1-R6 수치 재계산으로 검증:

- S1-S8: 전 8행이 인용하는 `eq:Uj`·`eq:xieq`·`eq:eqpeak`·`eq:dUhys`·`eq:Ubranch`·`eq:chid`·`eq:dHeff`·`eq:Lqfull`·`eq:LV`·`eq:reversal`·`eq:vn` 의 현재 정의와 표의 명제 문구가 전부 일치.
- R1 재계산: T=298.15K, Ω=12000 J/mol → 2RT/Ω=0.4131 → u=√0.5869=0.7661 → ΔU_hys=(2/F)[Ωu−2RT·artanh(u)]=(2/96485)[9193.2−4957.6×1.0107]=86.7mV — **표기값(86.7mV)과 독립 재계산이 정확히 일치**.
- R6 재계산: F×0.83mV/K=96485×0.00083=80.08 J/(mol·K)≈+80 (표기값과 일치), 30K×80/96485=24.9mV≈+25mV(표기값과 일치). 아울러 R6 은 본문 §sec:lco-center verifybox(L2238-2257)의 수치와 상호 참조되어 있으며(캡션 L3022 "본문 §sec:lco-center verifybox 와 동일 수치") 두 곳 수치 완전 동일 확인.
- R2·R3·R4·R5: 정성 극한(u→0, |I|→0, 컷 상수 동결) 전부 해당 식의 현재 형태와 정합.

**"근거 식" 열 14행 전건 현재 방정식 내용과 수치 재계산 양쪽에서 PASS.** R1-R3 정정(주로 어투·PSD 수치·spinodal 부록 정밀화)이 이 표의 물리 내용 자체를 건드리지 않았음을 확인(EXECUTION_LEDGER 로그에도 이 표를 겨냥한 수정 이력 없음 — Step 10 에서 "label sec:signcheck 보존→기존 참조 무결"로 표 자체가 이관 시 그대로 보존됐다고 명시).

---

## 요약

| # | 위치 | 내용 | 심각도 |
|---|---|---|---|
| A5-1 | `appendix_phase_separation.tex` L320-354 (`fig:app-phasediag`) | 상평형도 그림이 본문 어디에서도 `\ref` 되지 않는 고아 그림 — R2 에서 좌표 정밀도까지 손본 그림인데도 참조 미삽입 | **MED** |
| A2-1 | ch2 L501 | "다음 절 파생 B" 서술이 실제로는 다음 서브섹션(파생 B)과 같은 서브섹션 내 후속 내용(수치검증 srcbox) 두 시점을 한 문장에 겸용 — 오류는 아니나 가독성 저하 | LOW |
| A6-1 | ch1 부록 A(`sec:signcheck`) vs `appendix_phase_separation.tex`("Appendix A") | 두 문서가 각각 "Appendix A"를 자칭하나 서로 참조하지 않아 실질적 충돌은 없음(명명 혼동 소지만 존재) | LOW |

**범주별 수행 내역 요약(0-근거 포함)**: ① 라벨-참조 전수 대조 — 댕글링 참조 0건(스크립트 재현 가능), 지정 10 라벨 전건 PASS. ② 상대위치 참조 18건 전수 대조 — 어긋남 0건(LOW 1건은 어긋남이 아니라 겸용 서술). ③ 전방 약속 4건 — 미이행 0건. ④ 장간 교차참조 7건(ch1→ch2 4·ch2→ch1 3) — 불일치 0건. ⑤ fig/tab orphan — ch1·ch2 는 0건, appendix 에서 1건 발견(A5-1, 본 보고서 핵심 발견). ⑥ 부록 A 표 근거식 14행 — 방정식 내용 대조 + 수치 재계산(R1·R6) 양쪽 PASS, 무효화 0건.

**가장 약한 1곳**: A5-1(`fig:app-phasediag` 고아 그림). CRIT/HIGH 급 참조 파손은 발견되지 않았으나, 본 렌즈가 명시적으로 요구한 "참조 없는 그림·표 = orphan 0" 기준을 3파일 중 유일하게 위반하는 사례이자, EXECUTION_LEDGER 로그로 "R2 에서 실제로 수정 대상이었던 그림"임이 확인되어 "R1~R3 대규모 정정의 여파" 조사 목적에 정확히 부합하는 신규 결함이다.
