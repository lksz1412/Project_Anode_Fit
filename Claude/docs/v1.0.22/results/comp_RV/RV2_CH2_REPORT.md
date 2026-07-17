# RV2 — 신 Chapter 2 (LCO 양극) 선행 검수 보고

- 검수 창: **RV2 (Opus) — v1.0.22 신 Chapter 2 LCO 전담**
- 성격: **보고 전용** (파일 수정·git·Codex 접근 없음)
- 대상 마스터: `/home/user/Project_Anode_Fit/Claude/docs/v1.0.22/ch2_lco_v1.0.22.tex`
- 정독 소스(전량): `ch2v22_sec00_intro` · `ch2v22_notation` · `_sections/ch1_sec11_lcointro` ~ `ch1_sec17_msmr` · `ch2v22_bib`
- xr 대상(Chapter 1) 실확인 소스: `ch1_graphite_v1.0.22.tex` + `_sections/ch1_sec01~10`, `ch1_graphite_v1.0.22.aux/.log`
- 검증 방법: (1) 빌드 로그 undefined-ref 스캔, (2) ch1.aux `\newlabel` 대조로 xr 해소 확인, (3) 골격식 원본(ch1) 대 LCO 대입형(ch2) 1:1 대조, (4) 전 수치 재계산, (5) 서지 대조.

> 표기: 파일은 `_sections/` 기준 상대명으로 적되, 절대경로는 `/home/user/Project_Anode_Fit/Claude/docs/v1.0.22/_sections/<파일>`.
> 주의: 섹션 파일명은 `ch1_sec11~17` 이나 **내용은 Chapter 2(LCO)** 다(v1.0.21 이력 — 파일명 불변, 조립만 재편).

---

## 0. 총괄 한 줄

**구조적 결함(H) 없음.** xr 전건 해소·흑연 골격식 전건 일치·전자 엔트로피 유도의 부호사슬과 산술 전건 정확·4개 인용 다리 서지 정확. 발견은 **내부 척도 병치/티어 표기의 정합 이슈(M) 3건 + 경미 개선 후보(L) 6건**에 국한.

---

## 1. 발견별 상세

### RV2-01 (M) — 골 깊이(−46 J/(mol·K))와 적분 방출(1.1 k_B/atom)의 오해 유발 병치
- 파일:행 — `ch1_sec12_lcocenter.tex:102-103` (verifybox)
- 분류 — 척도 혼동 / §15 자체 가드 위반
- 현행 인용 — "전자항은 MIT 게이트의 x-국소 골로, **창 중심에서 몰당 ≈−46 J/(mol K)(게이트 적분 방출 ≈1.1 k_B/atom, §15)**, 창 밖에서 ≈0 이다."
- 문제 — `−46 J/(mol·K)` 는 **게이트 미분 골 깊이**(1/Δx≈20 증폭 포함, = 5.5 k_B/atom)이고, `1.1 k_B/atom` 은 **적분 방출(=완전 metal 끝점 S_e)** 로 **서로 다른 양**이다. 두 수를 괄호 병치하면 `−46 J/(mol K) ≈ 1.1 k_B/atom` 로 읽혀 **5배 오등치**가 된다. 정작 §15(`ch1_sec15_lcoelec.tex:296-303`, "세 양의 구분")는 "세 수치는 서로 다른 양이므로 한자리에 섞지 않는다 … 골 깊이가 부분몰 차보다 큰 것은 1/Δx≈20 증폭 때문"이라 **바로 이 병치를 금지**한다. 하류 계산(+80−46≈+34)에서 −46 을 골 깊이로 쓰는 것은 정확하므로 결함은 괄호 주석에 국한.
- 제안 — 괄호를 "(이 골 깊이는 §15 게이트에서 오며, 그 전 구간 적분 방출은 별개 양 ≈1.1 k_B/atom)" 처럼 **별개 양임을 명시**하거나 제거. (수정은 저자 몫 — 보고만)

### RV2-02 (M) — Reynier 척도 수치(4.2 / 9.0 k_B/atom)의 tier·원전 확인 flag 누락
- 파일:행 — `ch1_sec14_lcodecomp.tex:117-118` (srcbox), 대조 `:124`
- 분류 — 원전 대조 / tier 병기 누락
- 현행 인용 — "척도는 O3 상 내 변화 최대 ≈4.2 k_B/atom, 전 구간 최대 ≈9.0 k_B/atom 이다." / (동 srcbox) "(본문 §15 의 O3 부분몰 ≈0.18 k_B/atom 수치는 원 초록에 미명기 — **★확인 필요**)."
- 문제 — 같은 srcbox 안에서 `0.18 k_B/atom` 은 "원 초록 미명기 ★확인 필요" 로 flag 됐는데, 그보다 앞서 나온 `4.2`·`9.0 k_B/atom`(역시 Reynier 원전 정량 주장)은 **아무 tier·hedge 없이 단정**된다. 표기 비대칭이며, 세 수치(0.18/4.2/9.0)가 20배 이상 벌어져(0.18=부분몰 차, 4.2=O3 내 변화 최대, 9.0=전 구간 최대) **서로 다른 양임을 명시하지 않으면 상호 검산으로 오용될 소지**.
- 제안 — 4.2·9.0 에도 `0.18` 과 동격의 "원전 재확인" flag 병기 + 세 양(부분몰 차 vs 변화 최대)의 종류 차 한 줄. 원문(Reynier PRB 70, 174304) 대조는 본 창에서 불가 → Tier 4.

### RV2-03 (M) — charge-order config ΔS 셀 "배정 tier C" vs 캡션·각주 "값·배정 tier C" 표기 불일치
- 파일:행 — `ch1_sec11_lcointro.tex:72-73` (표 tab:lco-staging 본문 셀), 대조 캡션 `:65` 및 `ch1_sec13_lcohys.tex:168-171`(각주), `ch1_sec14_lcodecomp.tex:137`
- 분류 — tier 표기 정합(축 4)
- 현행 인용 — 표 본문 T2: "config 주도(≈0.47 J/(mol K); **배정 tier C**)", T3: "config(≈1.49 …; **배정 tier C**)" / 캡션: "config ΔS **수치**(0.47/1.49)는 원전 재확인 중이라 tier C 유지" / 각주: "**값도 배정도** tier C 다".
- 문제 — R4m 정정으로 이 ΔS 값의 1차 원전(종전 귀속 motohashi2009)이 원전 아님이 확인되어 **값과 배정 양쪽**이 tier C 로 강등됐다. 캡션·각주·sec14 는 "값·배정 both C" 로 정정됐으나 **표 본문 셀만 "배정 tier C"** 로 남아, 셀만 보면 "값은 확정, 배정만 C" 로 오독 가능(=R4m 이전 상태 잔재).
- 제안 — 표 셀을 "값·배정 tier C" 로 통일(캡션/각주와 일치). 보고만.

### RV2-04 (L) — MIT-logistic 게이트 절연체 끝점(x=1) 잔차와 산문 "창 밖 ≈0" 의 근사성
- 파일:행 — `ch1_sec15_lcoelec.tex:317`(그림 g 잔차 ≈5%), `:320`(파선 |ΔS_e| 좌단 0.244 vs 봉우리 1.350 ≈18%), `:330`(캡션), 대조 `ch1_sec14_lcodecomp.tex:48,65`("창 밖 ≈0")
- 분류 — 모델 근사 정직성
- 문제 — logistic 게이트는 x=1(절연체)에서 g≈5% g_max, |ΔS_e|≈18% 봉우리 잔차를 남긴다(그림엔 **정직히** 도시). 다만 산문의 "게이트 골, 창 밖 ≈0" 은 **금속측(x≲0.7)엔 정확**하나 절연 끝점(x=1, 3Δx)엔 18% 잔차라 근사. 물리적으로 x=1 은 g(E_F)=0 이어야 하므로 미소 비물리 잔차. tier-C 피팅 범위 내이고 그림이 값을 드러내므로 경미.
- 제안 — "창 밖(특히 금속측) ≈0, 절연 끝점엔 게이트 꼬리 잔차 존재(피팅 흡수)" 로 한정. 보고만.

### RV2-05 (L) — 3-전이 시연값(3.93/3.88/4.05 V)의 비단조·표 anchor 상이
- 파일:행 — `ch1_sec11_lcointro.tex:57-60`(캡션 ★시연값), `ch1_sec15_lcoelec.tex:342-343`(worked), `ch1_sec17_msmr` 연계
- 분류 — 데모 표기 혼동 소지
- 문제 — 시연 세트는 T2(3.88)가 T1(3.93)보다 **낮은 비단조** 배열이고 표 물리 anchor(3.90/4.05/4.17 오름차순)와 다르다. 캡션이 "전이 구성·순서가 표와 다른 데모 — 구조 대응이지 1:1 값 대응 아님, tier-C" 로 **명시 가드**하므로 결함은 아니나, 값만 훑는 독자에 혼동 소지.
- 제안 — 필요 시 시연값도 오름차순으로. 보고만.

### RV2-06 (L) — g_max 단위 표기 혼재("e/eV/atom" vs "states/(eV·Co)")
- 파일:행 — `ch1_sec15_lcoelec.tex:164,238,243,326`("e/eV/atom") vs `:343`("states/(eV·Co)")
- 분류 — 단위 표기 일관성
- 문제 — LixCoO2 에서 per-atom(=per-Co)로 동의이나 "atom" 이 전 원자/Co 를 가르지 않아 느슨. 1.1 k_B/atom 검산이 per-Co 전제라 표기 통일이 안전.
- 제안 — "states/(eV·Co)" 로 통일하거나 "atom = Co 자리" 각주. 보고만.

### RV2-07 (L) — gap 공식 3회 반복(경미 중복)
- 파일:행 — `ch1_sec13_lcohys.tex:77-93`(일반 박스 eq:lco-dUhys/Ubranch), `:116-123`(T2/T3 재기입), `:182-186`(T1 재기입)
- 분류 — 서술 중복
- 문제 — 박스가 이미 j∈J_LCO 전체를 담는데 T2/T3·T1 블록이 u_j·ΔU^hys·U^d 를 재인쇄. 교육적 인스턴스화이나 "추가 텀만/중복 없음" 관점에선 잉여. 모순은 없음.
- 제안 — T2/T3·T1 블록은 "박스에 j=2,3 / j=1 대입" 한 줄로 축약 가능. 보고만.

### RV2-08 (L) — `swiderska2019` label multiply-defined 빌드 경고
- 파일:행 — `ch2_lco_v1.0.22.log:905`; 원인 `ch2v22_bib.tex:16` + ch1 bib 공통 키 + xr import
- 분류 — 빌드 위생
- 문제 — 장 자기완결(D22) 의도의 공통 키 중복 수록 + xr import 로 `swiderska2019`·`LastPage` multiply-defined 경고 발생(로그 :905/:908/:1785). **undefined 는 0건**이라 참조 무결성엔 무해하나 경고 잔존.
- 제안 — 의도적이면 그대로 두되 change-log 에 "예상 경고" 로 기록. 보고만.

### RV2-09 (L) — 섹션 파일명(ch1_sec11~17)이 Chapter 2 내용 보유
- 파일:행 — `ch2_lco_v1.0.22.tex:22-28` (`\input{_sections/ch1_sec11_lcointro}` …)
- 분류 — 유지보수 함정(P3-7 인접)
- 문제 — 파일명 접두 `ch1_` 은 v1.0.21 이력(당시 LCO=구 Ch1 Part II)이고 현재 Chapter 2 로 조립. 렌더 문서엔 "Chapter 2/§2.x" 로 무해하나, 유지보수자가 파일명만 보고 Ch1 로 오인할 함정.
- 제안 — 주석/README 에 "ch1_sec11~17 = Chapter 2 LCO 소스" 매핑 명기(이미 마스터 상단 주석 일부 존재). 보고만.

---

## 2. 확정 검증(Tier 1) — 이상 없음 항목

축 1·2 (물리·수학 정합, "추가 텀만" xr 수신)에서 **직접 검증되어 이상 없는** 항목:

**A. xr(외부 참조) 무결성 — 전건 해소**
- `ch2_lco_v1.0.22.log:901` "IMPORTING LABELS FROM ch1_graphite_v1.0.22.aux", **undefined reference 0건**.
- ch1.aux `\newlabel` 대조: `eq:Uj, eq:Ujmid, eq:dUhys, eq:Ubranch, eq:sum, eq:xieq, eq:wbase, eq:spinodal, eq:gpp, eq:Veq, eq:hyssub, eq:hysdiff, eq:hyssym, eq:sm-mc-balance, eq:eqcond, eq:gxi, eq:mu, eq:fermifn, eq:belliden, eq:complete, eq:reversal, eq:vn, eq:n0map, eq:eqpeak, eq:eqbalance, eq:gibbsdef, eq:logisticsolve, tab:staging` — **전부 각 1회 정의(해소)**.

**B. 흑연 골격식 ↔ LCO 대입형 1:1 일치**
| Chapter 1 원식 | Chapter 2 LCO 대입형 | 판정 |
|---|---|---|
| `eq:Uj` U_j=(−ΔH+TΔS)/F, ∂U/∂T=ΔS/F | `eq:lco-dUdT`(cat 상첨자) | 부호까지 일치 |
| `eq:spinodal` ξ_s±=½(1±u), u=√(1−2RT/Ω) | `eq:lco-spinodal` | 일치 |
| `eq:dUhys` ΔU=(2/F)[Ωu−2RT·artanh u] | `eq:lco-dUhys`(+ Ω≤2RT→0 분기) | 일치 |
| `eq:Ubranch` U^d=U+½σ_d h_η γ ΔU^hys | `eq:lco-Ubranch` | 일치 |
| `eq:hyssym` ½[V(ξ_s⁻)+V(ξ_s⁺)]=U | sec13 대칭평균 | 일치 |
| `eq:xieq` ξ=1/(1+exp[−σ_d(V−U^d)/w]) | `eq:lco-eqpeak` ξ_eq,j | 일치 |
| `eq:wbase` w=n_j RT/F | sec13·sec16 | 일치 |
| `eq:belliden` dξ/dz=ξ(1−ξ) | `eq:lco-belliden` | 일치 |
| `eq:eqpeak` (dQ/dV)_j=Q_j ξ(1−ξ)/w | `eq:lco-eqpeak`·`eq:lco-msmrpeak` | 일치 |
| `eq:sum` dQ/dV=C_bg+Σ Q_j[…] | `eq:lco-charge` | 일치 |
| Taylor 극한 (8RT/3F)u³ (ch1:114) | `eq:lco-dope` | 일치(부호까지) |

**C. 흑연 anchor 재현** — ch1 `tab:staging`(sec10:40) stage 2→1: ΔH=−13000, ΔS=−16.0 J/(mol·K), Q=0.50, Ω=13000. → U(298.15)=(13000−298.15×16)/96485=**0.0853 V**. ch2 가 반복 인용하는 "흑연 2→1 삽입 ΔS=−16, U≈0.085 V" **정확 일치**.

**D. 2상/고용체 분류 충실 인용** — ch1 sec07(:14-21): 고용체=(dilute→stage4, 4→3, 3→2L), 2상(Ω>2RT)=**2L→2(LiC12)·2→1(LiC6)**. ch2 `ch1_sec13_lcohys.tex:28-33` 가 **동일 분류를 충실 수신**(초기 Ω 열은 전건 >2RT 이나 "피팅 후 유지 두 개뿐" 으로 정확 서술).

**E. 전자 엔트로피 유도·산술 전건 검증**(sec15)
- Sommerfeld: C_e=S_e=(π²/3)k_B²T g(E_F) — 표준. 자리당 S_e=3.29×0.0259 eV×13/eV=**1.10 k_B/atom** ✓.
- 부호 사슬: 삽입 x↑→metal→insulator→∂g/∂x<0→ΔS_e<0(삽입 기준), 탈리튬화 방출 |ΔS_e|>0 — 흑연 음의 ΔS_rxn 슬롯과 동일 좌표, 전건 정합. `eq:dSegate` 선두 음부호 유도 정확.
- 단위: N_A k_B²=R k_B ✓; N_A 누락 시 ~10²³ 배, e_V 곱셈 오류 시 1/e_V²≈**4×10³⁷** 배 ✓.
- 몰당 골 깊이: −(π²/3)R(k_BT/e_V)(g_max/Δx)·¼ = 3.29×8.314×0.02585×(13/0.05)×0.25 = **−46.0 J/(mol·K)** ✓ (sec15:301, worked −45.7).
- worked: ΔS_rxn,1^eff=+6.0−45.7=−39.7 J/(mol·K) → /F=**−0.411 mV/K** ✓; 게이트 on/off 관측계수 +0.160→−0.128 mV/K 부호 반전 서술 일관.
- T² 누적계수 ½ 인자: ∫_Tref^T a_e T'dT'=½a_e(T²−Tref²) → `eq:U1T2` U_1(T)=U_1(Tref)+(ΔS_0/F)(T−Tref)+(a_e/2F)(T²−Tref²) ✓.
- 2RT@298.15=2×8.314×298.15=**4957.5≈4958 J/mol** ✓ (sec13:28).

**F. 4개 인용 다리(srcbox) 서지·구조 정확**(축 1 핵심 — R3 신규분)
- sec13 `vanderven1998`(PRB 58, 2975, 1998) — 제일원리 클러스터 전개 상 안정성, x=½ 질서상·저-x staging. 서지·주장 정확. 대응표(Ω_j^cat↔ECI 평균장 축약)·방법요지·**가정 차(다 ECI+명시 바닥상태 vs 단일 평균장 쌍)** 구비.
- sec14 `reynier2004`(PRB 70, 174304, 2004) — 리튬화 엔트로피 config/vib(INS)/elec 삼분해. 측정식 ΔS=F dU_oc/dT 등치 정확. 단, 척도 수치는 RV2-02 참조.
- sec15 `marianetti2004`(Nat. Mater. 3, 627, 2004) — 불순물 준위 Mott 전이, x≳0.95 절연/x≲0.75 금속. 게이트 중심 0.85±2×0.05=0.75~0.95 경계 대응 정확(`eq:br-marianetti2004-1`). bgbox 의 밴드 vs Mott 절연체 구분·"host t2g 는 밴드절연, Mott 는 불순물 띠 소관" 물리 정확.
- sec17 MSMR 계보: `msmr_origin2017`(Verbrugge, JES 164, E3243 — 제목에 MSMR 없음 명시)·`bakerverbrugge2018`(명명 원전)·`msmr2024`. **f=+σ_d 유도**(계수비교 f/ω=σ_d/w, 폭 슬롯 대응 하 유일해)와 가드("함수형 동형≠물리량 동일; occupation↔progress 교차 시 f=−σ_d") 정확.

---

## 3. 4-tier 요약 (보고 정책)

**Tier 1 — 확정(문서·빌드·원전 대조로 직접 검증)**
- OK: 위 §2-A~F 전건(xr 무결·골격식 일치·anchor 재현·2상 분류·전자항 산술·다리 서지).
- 확정 불일치(문서만으로 성립): **RV2-01**(−46 vs 1.1 병치, §15 가드 위반), **RV2-03**(표 셀 tier 표기 stale).

**Tier 2 — 강한 의심(저자/원전 확인 요)**
- **RV2-02**(4.2/9.0 k_B/atom tier flag 누락 — 0.18 과 비대칭), **RV2-04**(절연 끝점 게이트 잔차 vs "창 밖 ≈0").

**Tier 3 — 개선 후보(수정 말 것, 보고만)**
- **RV2-05**(시연값 비단조), **RV2-06**(단위 표기), **RV2-07**(gap 3회 중복), **RV2-08**(multiply-defined 경고), **RV2-09**(파일명 함정).

**Tier 4 — 범위 밖/미확인(본 창에서 대조 불가 — 1차 원문 PDF 필요)**
- 원전 정량값의 1차 원문 직접 대조: `reynier2004` 의 0.18/4.2/9.0 k_B/atom, `motohashi2009` 의 g_max=13 e/eV/atom, `swiderska2019` 의 +0.83 mV/K. 문서 내 tier 병기(각 tier A/B/C)는 정합하나 **수치 자체의 원문 실측 여부**는 미검(→ RV2-02 와 연동, 원문 확인 시 해소).

---

## 4. 프로젝트 검수 7항목(P3) 점검

1. **V_n/V_app/V_drive/V_OCV 구분** — 통과. sec11:101 V_app>V_n(분극), sec15 U_oc, U_j(중심)/V(전위점) 구분 일관. 혼용 없음.
2. **전하 보존식이 내부 전위 결정 중심식** — 통과. sec15 worked(:357)가 `eq:sm-mc-balance` 음함수를 풀어 U_oc 획득(OCV 직독 회귀 아님), sec16 이 전하 보존식에서 출발.
3. **순환 의존성(ξ_j·Q_bg·dQ/dV·dV/dQ) 발생처 표시** — 통과. sec17(c):154-158 이 "eq:lco-xmap↔ξ_eq,1↔U_1 고정점 구조" 로 발생 식·변수 명시.
4. **순환 의존성 4분류 진단** — 통과. "동결 근사는 순환 없음, 정밀형은 1회 갱신(수치)" = **수치해법 필요** 분류로 진단, 되먹임 이동 ≈14 mV≲w_1 상한 제시.
5. **ref 방법론 도입 4항목(서지/위치/수학구조/변수매핑/가정차)** — 통과(ch2 자체 4개 다리에 적용). 각 srcbox 가 정확 서지+대응표(변수매핑)+방법요지+**가정 차** 구비(§2-F).
6. **Ch1 기준식 ↔ Ch2 전달식 무충돌** — 통과. §2-B 표 전건 일치, 모순 0건.
7. **ver.N vs Chapter N 명칭 비혼동** — 통과(본문). 절 라벨 N0'~N9'(흑연 N-번호+프라임) 사용, "Chapter 1 골격" 인용 일관. **단 파일명 ch1_sec11~17 잔재는 RV2-09 로 별도 보고**.

---

## 5. 총평

신 Chapter 2(LCO)는 **"같은 골격, 추가 텀만" 설계 의도를 구조적으로 충실히 구현**한다. (i) 흑연 골격식 11종이 xr 로 정확히 수신되어 부호까지 1:1 대입형으로 재현되고, (ii) 유일한 신규 물리인 전자 엔트로피 항(MIT-logistic 게이트)의 유도가 Sommerfeld 표준결과에서 부호사슬·단위환산·T² 곡률까지 **전 수치 재계산 검증을 통과**하며, (iii) R3 신규 4개 인용 다리는 서지가 정확하고 "가정 차" 를 빠짐없이 분리 기록해 **함수형 동형과 물리량 동일을 혼동하지 않는 가드**를 일관되게 유지한다. R4m 정정분(config ΔS tier C 강등·원전 재확인 각주)도 대체로 반영됐다.

발견은 **High(구조 결함) 0건**이며, Medium 3건은 모두 **척도·tier 표기의 국소 정합**(RV2-01 골 깊이/적분 방출 병치, RV2-02 Reynier 척도 flag 비대칭, RV2-03 표 셀 tier stale)으로, 물리 결론·수치 결과에는 전파되지 않는다. 특히 RV2-01 은 §15 가 스스로 세운 "세 양의 구분" 가드를 §12 verifybox 가 국소 위반한 사례라 **우선 정합 대상**으로 권고한다. Tier 4(원전 정량값 1차 대조)는 본 검수 창의 범위 밖으로, `_local_only/` 원문 PDF 확보 시 RV2-02 와 함께 해소 가능.

*(수정·git·Codex 접근 없이 보고만 수행. 이상.)*
