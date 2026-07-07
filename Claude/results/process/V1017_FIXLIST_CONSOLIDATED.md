# V1.0.17 통합 fix-list (9종 체리피킹 → master 체리픽·적대검증)

> 리뷰어(sonnet) 산출을 master(opus)가 체리픽·적대검증한 **적용 확정 목록**. 상태: ⏳수집중. 판정 = 적용/보존/기각/범위밖.
> 원칙: 물리·수식·수치·식별자 불변. 코드참조는 구현대응표/appendix 만. seed 기각·전제붕괴는 근거 명시(허위 X).

## Appendix (CR8 완료 — register/버전/구조)
| 항목 | 판정 | 조치 |
|---|---|---|
| A1 L37 `버전 1.0.15 초안` | **적용(필수)** | → `버전 1.0.17 초안` (렌더링 현행 선언) |
| A2 L2 `v1.0.14 Step 7` 소스주석 | **보존(override)** | 역사적 작성 스탬프(3개 버전 불변) — 버전 안 올림. 모호성 해소 위해 `초안, v1.0.14 Step 7` → `초안; 최초 작성 v1.0.14 계획 Step 7` [선택 보강]만 |
| A4 L453 "섞임" 절제목 | **기각** | 전제붕괴 — L453=`\toprule`(표 명령), "섞임" 포함 절제목 0건. "섞임 몫"=본문 f(ξ) 일관 용어. 조치 불요 |
| A6 numverif 버전태그 | 범위밖 | Ch2 L895 소관(appendix 0건). 유지 |
| A7 "(초안)" 레벨 L26/L35 | 확인·유지 | 결정과 정합, 무변경 |
| A8 "구현 대응표" 절 | 범위밖 | Ch1 L3349 소관. 유지 |
| A9 Ch1 date 방침 | 흡수 | appendix date=버전만(달력 없음) → A1로 자동 정합 |
| register(코드/구현) | clean | appendix 코드참조 0건 |

→ **Appendix 순 편집: A1(필수) + A2 소스주석 명료화(선택). CR9(물리·단위) 대기 중 — A3·A5 추가 예정.**

## Ch2 (CR7 완료 — 박스·용어·버전)
| 항목 | 판정 | 조치 |
|---|---|---|
| **NEW L36 pdftitle·L38 lhead `(v1.0.16)`** | **적용(필수)** | → `(v1.0.17)`. 매 페이지 렌더링 노출(P1 .tex 누락분) |
| C7 용어 L450·L645·L647·L708 축약 "가역열/비가역열" | **적용(경미)** | → "가역 발열/비가역 발열"(지배형 25회+). L646-651 keybox 내 3형태 혼재 |
| C5 L646-651 "혼동 금지" 박스 keybox | **적용(경미)** | → warnbox(동류 경고 L315-331·L614-621도 warnbox, \label 없음) |
| C6 L43 derbox 정의만·0회 사용 | **적용(경미)** | **삭제**(L43 제거). 최소변경 채택(repurpose는 srcbox 내용 이동 위험 — 회피) |
| NEW L1-2 소스헤더 `release 1.0.16` | 적용(선택) | → `release 1.0.17; 계보 1.0.16 승계`(현행 release 스탬프라 갱신 타당, A2와 성격 다름) |
| C5[3] srcbox 2용도 이질(문헌 vs 내부 numverif) | 보류(선택) | 라벨 변경 위험 — register 정련 범위 밖, 유지 |
| C7 "재가역열"·"기억 방출"·"메모리" | 기각(근거 미발견) | Ch2 grep 0건 — SEED 전제 미성립, 조치 불요 |

## 참고문헌 저자 보충 (조회팀 CrossRef raw JSON — Ch2 C3)
**⚠ DOI 정정 2건(P4 master 자체 재확인 후 적용)**: occupation2019 `...135634`(404)→`10.1016/j.electacta.2019.134774` · hysteresis2018 `...05.060`(오배정=Milcarek fuel cell)→`10.1016/j.jpowsour.2018.05.052`.
저자 7건(bibitem 앞에 삽입):
- occupation2019 → `M. P. Mercer, M. Otero, M. Ferrer-Huerta, A. Sigal, D. E. Barraco, H. E. Hoster, E. P. M. Leiva,`
- chemmater2015 → `S. Konar, U. Häussermann, G. Svensson,` (CrossRef 오탈자 "Häusserman"→정정 Häussermann)
- jpcc2021 → `J. Haruyama, S. Takagi, K. Shimoda, I. Watanabe, K. Sodeyama, T. Ikeshoji, M. Otani,`
- msmr_partI → `T. R. Garrick, B. J. Koch, M. Choi, X. Du, A. M. Adeyinka, J. A. Staser, S.-Y. Choe,`
- msmr_partII → `A. Paul, K. Wolfe, M. W. Verbrugge, B. J. Koch, J. S. Lowe, J. Trembly, J. A. Staser, T. R. Garrick,`
- standardised2024 → `A. Hales, J. Bulman,`
- hysteresis2018 → `I. Zilberman, A. Rheinfeld, A. Jossen,`

부가(CR5[11]): L888-894 7건은 vol/issue/page 도 부분 누락 → 저자 조회분에 확보된 서지요소 함께 보강(occupation vol 324·chemmater 27(7) 2566-2575·jpcc 125(51) 27891-27900·msmr_partI 171(2)·msmr_partII 171(10)·standardised 171(5) art 050535). 확보 못한 요소는 무리 보충 X.

## Ch2 추가 (CR5·CR6 — register·서지·수식주도)
| 항목 | 판정 | 조치 |
|---|---|---|
| C1 L756 코드(Anode_Fit_v1.0.16) | 적용(필수) | → "모델이 산출하는 값과 일치한다"(식별자 소거) |
| C2 L800 "코드 entropy_coefficient" | 적용(필수) | "코드"→"모델의"(\texttt{} 보존) |
| C3 L888-894 저자 7 + DOI 2정정 | 적용(필수) | 위 조회분 |
| C4 맺음(L866-878) payoff 미요약 | 적용(경미, 필수→하향) | L877-878 앞 1문장(계산예제 round-trip<0.001μV/K + tab:qrev 부호교대 + 방법론 출구) — CR6 문안 |
| NEW "계산용 종합식(use-this)" 무 label(L734) | 적용(경미) | `\begin{equation}\label{eq:complete}` 부여 + 3곳 \eqref(L520·786·859) |
| NEW L732 "(use-this)" 영어 라벨 | 적용(선택) | → 한글("계산용 종합식(실전용)") |
| NEW L895 "PASS" | 적용(경미) | → "확인"(CI 어휘 제거) |
| L36 pdftitle·L38 lhead·L1-2 헤더·L895 코드 v1.0.16 | 적용(필수 L36/38·선택 나머지) | → v1.0.17(매칭코드·현행. L895 코드=매칭이라 bump) |

## Appendix 추가 (CR9 — 물리·단위·수식주도; 물리 전건 재유도 무결)
| 항목 | 판정 | 조치 |
|---|---|---|
| A3 L473 broadening 참조 | 적용(경미) | → "§1.7(broadening 절)" **리터럴**(독립컴파일 위해 \ref 금지, CR9 확인) |
| A5 L430 κ·L437 M 단위 | 적용(선택) | f 기준 명시 1문장(L429-430: eq:app-fxi 몰당→몰부피 v_m 나눈 부피밀도[J/m³]) + κ[J/m]·M 단위. master 차원 재검 후 |
| NEW L400-402 γ[J/m²] 옆 v_m·Δg_v 무단위 | 적용(선택) | v_m[m³/mol]·Δg_v[J/m³] 병기 |
| NEW L98 N_A(아보가드로) vs L192 N_A(A종수) 폰트만 구분 | 적용(선택) | L192 각주(아보가드로 무관) |
| NEW §app:kinetics 두 소절 (a-d) 구조 이탈 | 적용(경미) | nucleation/spindecomp 박스 라벨 또는 축약 명시 |
| NEW L252 "(c) 중간식"이 표 지칭 | 적용(선택) | → "(c) 분류표" |

## Ch1 (CR3·CR4 — 기호·완결·표; CR1 register·CR2 수식주도 대기)
| 항목 | 판정 | 조치 |
|---|---|---|
| #4 q(T) 분배함수 | 적용(경미) | → **q_int**(ζ는 L2742 선점 — CR3가 충돌 차단). L474/476/480/481/482/492/495/499/503/505/524/562/1440/3487 |
| #5 N3 그룹 순서(CR3·CR4 중복확인) | 적용(경미) | 마스터표 N3 5행을 N2와 N4/N5 사이로 |
| #7 T_c → T_{c,j} | 적용(경미) | L663·L671 |
| #8 z 4중용(CR3 4번째 발굴 L1316) | 적용(선택) | L1316 각주(국소 logistic 인자, 배위수/전하수 z와 무관) |
| #9 ω_0→ω_i(→ω_k) 다리(SEED ω_j는 오기) | 적용(선택) | L484·L554 전환 다리 1구절씩 |
| #10 T_rep + NEW T_{c,j} 마스터표 누락 | 적용(선택) | 표에 2행 추가 |
| #19 사전/매핑 | 적용(선택) | "사전"→"대응표" L2388·2436·3130(dict 은유 제거) |
| NEW s(ζ) Fermi 핵 vs s(고정부호) 충돌 | 적용(경미) | L2742-2757 s(ζ)→h(ζ) 국소 |
| NEW §sm-lattice N=∑n_k vs n 표류 | 적용(경미) | L580~ n→N |
| #15 fig:widthbudget "1.6w_j 지름길" 본문無 | 적용(경미) | 본문 1문장 도입 또는 캡션 가정형 완화 |
| #17 기억/메모리 혼용 | 적용(경미) | L1976·1993-1994·2053·2146 "메모리"→"기억" |
| #24 signcheck-R 판정열 ✓ 부재 | 적용(선택) | ✓열 추가 또는 S표도 산문 통일 |
| #25 tab:inputs·nodecode \begin{table} | 적용(선택) | longtable 통일 |
| #26 tab:staging vs lco-staging 서식 | 적용(경미) | 폰트·arraystretch 통일 |
| NEW 마스터 기호표(L236-278) caption/label 無 | 적용(경미) | \caption+\label{tab:notation} 추가(상호참조 가능화) |

## Ch1 register (CR1 — SEED 8 확인 + 신규 15; "슬롯" 유지)
| 항목 | 판정 | 조치 |
|---|---|---|
| #1 L105 date | 적용(필수) | `\date{\normalsize 버전 1.0.17}`(코드괄호 삭제·버전 bump) |
| #2 L221 "코드 규격화" | 적용(필수) | →"정규화" |
| #3 L230 "(★최우선 결함 클래스)" | 적용(필수) | 삭제(SEED 인용 "결합"은 오사, 실제 "결함") |
| #12 L921 "(코드 진행 N1--N9)" | 적용(필수) | →"(N1--N9)" |
| #13 L982 "코드 입력" | 적용(필수) | →"입력" |
| #14 L1606 "현재 코드의 staging" | 적용(필수) | →"현재 모델의" |
| #18 L2934 "forward 코드는" | 적용(필수) | →"이 일반화는" |
| #23 L3304 "구현 self-test 와 같은 양의 수기 재산출" | 적용(필수) | CR1 재구성: "R1--R3 은 독립 수기 재산출로 동일 양을 재확인한 것"(중복 회피) |
| **NEW L76/103/156 "코드 진행을 따라가는"·L78 헤더 "코드 진행"** | **적용(필수·최대노출)** | →"계산 진행"(본문 L138-142 이미 "계산"·매페이지 헤더·챕터제목). ★HANDOVER 최우선 명기 |
| NEW L212·L3223 "진입점" | 적용(필수) | →"출발점"/"계산은"(부록 실제 \code{curve} 진입점과 충돌) |
| NEW L1436·L2997 "식·코드 경로" | 적용(필수) | →"식·모델 경로" |
| NEW L2327 "MIT dict"·L2695 "전이 dict" | 적용(필수) | →"MIT 전이"/"전이 파라미터 집합" |
| NEW L2330 "현 구현은" | 적용(필수) | →"현행 모델은"(L3175 정합) |
| NEW L2803 "(★최우선 결함 클래스)" 2차 | 적용(필수) | 삭제(SEED#3 놓친 사본) |
| NEW L3072 "구현식은" | 적용(필수) | →"닫힌식은"(대상 eq:lco-xmap=수식) |
| NEW L1926 "토글 옵션"·L3226 "구현대응(진입점·함수이름)" | 적용(경미) | →"적용하지 않으면"/"구현 대응표는" |
| NEW L76/78 등 렌더링 "(v1.0.16)" | 적용(필수) | →"(v1.0.17)"(pdftitle·헤더·표지 전수 grep) |
| NEW "슬롯" 30+회 | **유지** | 전역 채택 용어 — 과잉수정 회피(CR1 판단) |
| changelog메타·방어어투 | clean | %주석만·정상 교과서 장치 |

## Ch1 수식-주도 (CR2 — SEED 6 확인·정정)
| 항목 | 판정 | 조치 |
|---|---|---|
| #6 (b)+(c) 병합 | 적용(선택, **정정**) | 실제 1곳 L893-895만(L370-452는 정상분리 — SEED "2곳" 오지목). 단락구분 또는 "(b)(c)" 복합라벨 |
| #11 "극한 검산" 5곳 평문 | 적용(선택) | verifybox 감쌈(정의된 derivbox/verifybox 활성화 — L432·519·605·669·912) |
| #16 L1914 "(d) 유효 장벽" | 적용(경미) | →"(d) 박스 --- 유효 장벽."(L1922 실제 \boxed, 23/24 통계) |
| #20 L2672-2678 eq:lco-mit underbrace | 적용(경미) | config+vib+전자 합 명시 또는 라벨 "전자(신규 항)"(직전 산문 정합) |
| #21 L3039 (d) 박스 라벨 누락 | 적용(필수) | "(d) 박스 --- 슬롯 분해식." 추가 |
| #22 G1/G3 미태깅 | 적용(경미) | G3=L2681 부근·G1=round-trip 가드 L3072-3077(CR2 위치 보정) |
| NEW L1017-1018·L1159-1165 (b)(c)·(d)순서 | 적용(선택) | 복합라벨·박스前 (d) 라벨 |

→ **CR2 부산물**: Ch1 derivbox(L85)도 0회 사용 — #11에서 verifybox/derivbox 활성화로 동시 해소.



