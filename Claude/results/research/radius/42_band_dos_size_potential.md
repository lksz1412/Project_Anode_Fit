# 42 — 전자구조(밴드/DOS)가 삽입 전위를 정하는가 + 입자/결정자 크기의 영향

> 축 I 조사 카드. 학술 조사 sub 작성. 배정 축(전자구조 채널 + 크기 의존)만 다룸 —
> 종합·최종 verdict·타 축 카드는 master 전담.
> tier 표기: **확정**(1차 문헌 본문/식 확인) / **abstract-확정**(초록·DB 메타만, 본문 미열람) /
> **추정+계산근거**(직접 계산) / **근거미발견**.
> 본 조사는 web search + 일부 WebFetch 기반. 본문 전문(full-text) 열람 여부를 카드 `정독범위`에 명시.

---

## 소절 1 — 삽입 전극 전위의 전자(밴드 채움) 몫: DOS가 전위·dQ/dV 형상을 정하는가

### 1.1 기본 분해: V = (μ_Li⁺ + μ_e⁻)/F

삽입 전극의 전위는 삽입된 Li **원자**의 화학퍼텐셜로 결정되며, 이는 이온 몫과 전자 몫으로 분해된다:

```
E = μ_Li / F = (μ_Li⁺ + μ_e⁻) / F          ... (식 A)
```

여기서 μ_e⁻ = host 내 전자의 화학퍼텐셜 = **Fermi level** (E_F). 즉 Li 한 개를 더 넣으면
(i) Li⁺ 이온이 격자 가스(lattice gas) 자리에 들어가며 배열 엔트로피·이온-이온 상호작용 몫을 바꾸고,
(ii) 전자 한 개가 host의 전도띠를 채우며 **E_F 를 g(E_F) 의 역수만큼 끌어올린다**.
(출처: Lithium Inventory "Thermodynamics of intercalation materials"; 본문에 식 A 와 "The chemical potential of the electron is equivalent to the Fermi level" 명시.)

### 1.2 전자 몫 = quantum/chemical capacitance = 1/g(E_F)

전자 채움 몫의 전위 기울기는 전자 DOS 의 역수다:

```
∂μ_e⁻/∂n = 1 / g(E_F)        (n = 전자 밀도)
C_Q = e² g(E_F)              (quantum capacitance)        ... (식 B)
```

DOS 가 낮으면(g 작음) 전자 한 개 추가에 E_F 가 크게 움직여 **전위가 가파르게 변하고**(dV/dx 큼 → dQ/dV peak 낮고 넓음),
DOS 가 높으면 E_F 가 거의 안 움직여 **전위 평탄**(dV/dx 작음 → dQ/dV peak 높고 뾰족).
이 틀에서 **dQ/dV(=dx/dμ × 상수) 자체를 "전기화학 DOS"로 읽을 수 있다.**
(출처: graphene quantum capacitance 문헌 일반식 C_Q = e² dn/dE; arXiv:1001.4690 Drӧscher et al., graphene 에서 C_Q ∝ DOS 가 Dirac point 부근 선형, 실측 DOS ≈ 1×10¹⁷ m⁻²eV⁻¹.)

### 1.3 ★graphite 직접 선례 — Dahn et al. PRB 45, 3773 (1992)

본 축에서 **가장 강한 1차 선례**. 흑연·붕소치환 흑연 Li_x(C₁₋zBz)₆ 의 OCV 를 Li 농도 x 의 함수로 측정 →
작은 x 영역에서 화학퍼텐셜(=전위)의 변화가 **흑연의 1전자 준위 DOS g(E) 로 예측**된다는 것을 보임.
rigid-band 모델에서 측정 **dx/dμ vs μ** 곡선이 경험적 tight-binding DOS 계산과 잘 일치.
즉 **"OCV(dQ/dV) 측정 = 흑연 전자 DOS 측정"** 이 실험적으로 성립한 사례.
- LiC₆ / LiC₁₂ 의 E_F DOS = 0.25 / 0.12 (eV·C atom)⁻¹, 순수 흑연 ≈ 0 (semimetal). Li 2s 전자가 C π-band 로 이동해 E_F 가 高DOS 영역으로 올라가며 금속화.
- ★단, 여기서 DOS 를 바꾸는 변수는 **붕소 치환(화학적 도핑)** 이지 입자 크기가 아니다 → 소절 2 의 핵심 갈림.

### 소절 1 판정
DOS 가 전위를 정하는 정도 = **확정적으로 유의**. 전위의 전자 몫(식 A 의 μ_e⁻)은 1/g(E_F)
로 직접 dV/dx 에 들어가며, 흑연에서 OCV→DOS 역산이 PRB(1992)로 실증됨.
**사용자 "dQ/dV = 일종의 DOS" 틀은 1차 문헌으로 지지됨.** 다만 이는 *크기*가 아니라 *어떤 변수가 DOS를 바꾸느냐*의 문제로 넘어간다(소절 2).

---

## 소절 2 — ★입자/결정자 *크기*가 DOS·밴드 폭·전위를 바꾸는가, 어느 스케일에서

### 2.1 양자 가둠의 에너지 스케일 (직접 계산, tier=추정+계산근거)

탄소 sp² 계의 측면 가둠(lateral confinement) 밴드 폭/gap 두 가지 추정:

**(a) 경험적 AGNR 스케일링** Eg(eV) ≈ a / W(nm), a ≈ 1~2 eV·nm
(캘리브레이션: 6-aGNR W≈0.6nm Eg=1.69 eV → a≈1.0; 15-aGNR W≈1.7nm Eg=1.03 eV → a≈1.75. 출처: Merino-Díez et al. ACS Nano 2018, PMC5789393, 측정 gap 6/9/12/15-aGNR = 1.69/1.35/1.13/1.03 eV; Son-Cohen-Louie PRL 97,216803(2006) Eg ∝ 1/W.)

| W (그래핀 도메인 측방 폭) | Eg ≈ 1 eV·nm/W | Eg ≈ 1.7 eV·nm/W |
|---|---|---|
| 0.6 nm | ~1670 meV | ~2830 meV |
| 2 nm | ~500 meV | ~850 meV |
| 5 nm | ~200 meV | ~340 meV |
| 10 nm | ~100 meV | ~170 meV |
| 50 nm | ~20 meV | ~34 meV |
| 1000 nm (1 µm) | ~1 meV | ~1.7 meV |
| 5 µm (실제 흑연 입자경) | ~0.2 meV | ~0.34 meV |

**(b) 유효질량 입자-in-box** ΔE = ħ²π²/(2m*L²), m*≈m_e:
L=2nm→94 meV, L=5nm→15 meV, L=10nm→3.8 meV, L=100nm→0.038 meV, L=1µm→3.8×10⁻⁴ meV.
(흑연 운반자 유효질량은 m_e보다 작거나 Dirac형이라 실제론 더 큰 ΔE도 가능 — (a)가 보수적 상한.)

→ **두 방법 모두 수렴**: 수 mV~수십 mV 의 전위 shift 를 내려면 측방 가둠 크기 **L ≈ 5~50 nm** 가 필요.
L ≳ 수백 nm 면 가둠 효과는 **sub-meV → 사실상 0**.

### 2.2 ★어느 "크기"가 관건인가 — 입자경 vs 면내 결정자 크기 La

결정적 구분: Li 는 흑연의 **그래핀 면 사이**에 들어가고, 전자 채움도 면내 π-band 에서 일어난다.
따라서 양자 가둠의 관련 길이는 **입자 직경(µm)이 아니라 면내 결정 coherence 길이 La**(그래핀 도메인 크기)다.

실제 흑연 음극의 결정자 크기(특허/재료 스펙 종합, abstract-확정):
- **La (면내, 110 방향)**: 흔히 ~80 Å(8 nm) ~ 1000 Å(100 nm) **이상**, 양질 흑연은 더 큼(수백 nm~µm). (출처: graphite 음극 재료 특허 다수, "La (110) 800~50 Å 이상 바람직")
- **Lc (c축, 002)**: 일반 흑연 40~100 nm, 우수재 100 nm 이상(1000~100000 Å). 천연흑연 입자경 D50 ≈ 5~20 µm.
- 대비: hard carbon 의 그래핀 시트는 "수 nm 이상 자라지 않음" → 그쪽은 가둠 유의할 수 있으나 그건 흑연이 아니다.

**판정**: 마이크론 흑연의 면내 도메인 La 는 보통 ≳ 수십 nm~수백 nm 이므로,
2.1 표에서 양자 가둠 전위 shift 는 **≲ 1 meV** — staging peak(수십~수백 mV 영역, peak 간격 수십 mV)에 비해 **무시 가능**.
순수 흑연은 또한 semimetal(E_F DOS≈0)이라 가둠 gap 이 열려도 그 자체가 staging plateau 구조(LiCₓ 상전이 기반)를 만드는 주체가 아니다.

### 소절 2 판정
입자/결정자 크기의 양자효과는 **L ≈ 5~50 nm 이하에서만** 수~수십 mV 급으로 유의.
실제 마이크론 흑연(면내 도메인 La ≳ 수십 nm)에서는 **무시 가능(sub-meV)**.
**사용자 "작은 입자에서 밴드 폭이 가늘어져 U 분포를 만든다" 가설은, *흑연 입자경(µm) 분포*로는 성립하기 어렵다** —
µm 크기 차이가 만드는 가둠 ΔE 차이는 sub-meV. 단 **면내 도메인 La 가 진짜 nm급(나노결정 탄소·고결함 흑연)인 분획**이 있으면 그 분획에 한해 수 mV급 기여 가능(열린 문제).

---

## 소절 3 — 선례: 크기→전자구조→삽입전위 shift 직접 보고 문헌

- **DOS→전위 직접 매핑(크기 아님)**: Dahn et al. PRB 45,3773(1992) — 화학 도핑(B)으로 DOS/E_F 변화 → OCV 변화. **크기 변수는 아님.** (소절1.3)
- **크기→밴드 직접(전위는 아님)**: Son-Cohen-Louie PRL 97,216803(2006); Merino-Díez ACS Nano 12,4538(2018, PMC5789393) — GNR 폭→gap. **전기화학 전위로 연결한 본문은 미발견.**
- **입자경(µm)→삽입전위 shift 를 *전자구조 채널*로 귀속한 1차 문헌**: **근거미발견.**
  문헌의 입자경·결정자 의존 전위/용량 변화는 대부분 (i) 표면적·SEI, (ii) 동역학(확산거리, GITT로 사라짐), (iii) 결정성/결함·d002 격자 — 즉 **열역학적 전자구조 채널이 아닌 다른 채널**로 설명됨.
  → 사용자가 찾는 "평형에서도 남는 전자구조 기원 U 분포(입자경 기원)"를 흑연에서 직접 보인 선례는 **이번 조사 범위에서 발견 못 함**(부재 명시).

---

## 카드 (schema: 주장 | 근거 | 지배식/정량 | 흑연 적용성 | 타당/한계 | 가설 지지/반박 | 정독범위 | tier)

| # | 주장 | 근거(저자·연도·DOI) | 지배식/정량값 | 흑연/탄소 적용성 | 타당/한계 | 밴드가설 지지/반박 | 정독범위 | tier |
|---|---|---|---|---|---|---|---|---|
| C1 | 삽입 전위 = 이온+전자 화학퍼텐셜, 전자 몫 = Fermi level | Lithium Inventory, Thermodynamics of intercalation (교육자료, primary 식 인용); 일반 열역학 | E=(μ_Li⁺+μ_e⁻)/F, μ_e⁻=E_F | 직접 적용 | 표준식, 견고 | **지지(전제)** | 본문 발췌 열람 | 확정 |
| C2 | 전자 몫 dV/dx = 1/g(E_F); dQ/dV ~ 전기화학 DOS | quantum capacitance 일반식; Drӧscher et al. 2010 arXiv:1001.4690 | C_Q=e²g(E_F); dx/dμ∝g(E) | 직접 | 견고. 단 전체 dQ/dV엔 이온 엔트로피·상전이 몫도 합산됨 | **지지** | 초록+발췌 | abstract-확정 |
| C3 | ★흑연 OCV(dx/dμ) 측정 = 흑연 전자 DOS 측정 (실증) | Dahn, Reimers, Sleigh, Tiedje, PRB 45,3773(1992), doi:10.1103/PhysRevB.45.3773 | 작은 x: dx/dμ vs μ ≈ tight-binding DOS; LiC₆/LiC₁₂ g(E_F)=0.25/0.12 (eV·C)⁻¹ | **직접(흑연 그 자체)** | 강력. DOS 변경 변수=B 도핑(화학), 크기 아님 | **지지(틀)·크기엔 중립** | 초록·DB 메타 확정, 본문 PDF 접속실패 | abstract-확정 |
| C4 | 양자 가둠 ΔE: 수~수십 mV shift엔 L≈5~50nm 필요 | Son-Cohen-Louie PRL 97,216803(2006) doi:10.1103/PhysRevLett.97.216803; Merino-Díez ACS Nano 12,4538(2018) doi:10.1021/acsnano.7b06765 (PMC5789393) + 직접계산 | Eg≈(1~2 eV·nm)/W; ΔE=ħ²π²/2m*L². L=10nm→~100meV, 50nm→~20meV, 1µm→~1meV | 탄소 sp² 직접 | gap 데이터는 GNR(에지효과 포함)·상한; 입자-box 보수적 | 부분지지(스케일 한정) | gap값 본문열람(PMC5789393), 계산 직접 | 확정 + 추정+계산근거 |
| C5 | ★마이크론 흑연 입자경(µm) 양자효과는 무시(sub-meV) | 위 계산 + 흑연 결정자 스펙(La≳수십nm~µm, 음극 특허 스펙) | µm·면내 La≳100nm → ΔE≲1meV ≪ staging 수십mV | 직접 | La 가 진짜 nm급인 나노결정 분획은 예외 | **반박(입자경 µm 기준)** | 스펙 초록 발췌, 계산 직접 | 추정+계산근거 |
| C6 | 입자경(µm)→전위 shift 를 전자구조로 귀속한 흑연 선례 | — | — | — | 문헌은 표면/SEI·동역학·결함으로 설명 | 가설의 *입자경 채널* 미지지 | 검색 다수, 해당 보고 없음 | 근거미발견 |
| C7 | 순수 흑연 semimetal(E_F DOS≈0), Li 채움이 금속화; 밴드는 rigid-band서 벗어남 | 흑연 LIC 전자구조 다수; "Electronic properties of various stages of Li-GIC"; 흑연 staging arXiv:2006.12055 | LiC₆/LiC₁₂ g(E_F)=0.25/0.12 (eV·C)⁻¹; ARPES: 밴드 비균일 이동(rigid-band 위배) | 직접 | DOS 단순 rigid-band 한계 | 틀엔 지지·단순화 경고 | 초록·발췌 | abstract-확정 |

---

## 이 축 요약

**(1) DOS 가 전위를 정하는 정도** — 강함·확정. 삽입 전위의 전자 몫 μ_e⁻ = Fermi level 이고
그 기울기 dV/dx 는 1/g(E_F)(quantum capacitance) 다. **흑연에서 OCV(dx/dμ)→전자 DOS 역산이 Dahn et al. PRB 45,3773(1992)로 실증**됐다.
사용자의 "dQ/dV = 일종의 전기화학 DOS" 틀은 1차 문헌으로 **지지**된다(단 전체 dQ/dV 엔 이온 배열엔트로피·상전이 plateau 몫이 합산됨 — DOS 가 유일 인자는 아님).

**(2) 입자/결정자 크기의 양자효과 스케일** — 측방 가둠 크기 **L ≈ 5~50 nm 에서만** 수~수십 mV 급.
경험식 Eg≈(1~2 eV·nm)/W 와 유효질량 box 가 일치 수렴. L ≳ 수백 nm 면 sub-meV.

**(3) 마이크론 흑연 적용성 판정** — **부정적**. Li 삽입·전자채움의 관련 가둠 길이는 입자경(µm)이 아니라
**면내 도메인 La**이고, 실제 흑연 La 는 보통 수십 nm~µm 라 양자 가둠 ΔE ≲ 1 meV — staging peak 간격(수십 mV)에 **무시 가능**.
따라서 **"흑연 입자경(µm) 분포 → 밴드 폭 차이 → U 분포"** 라는 사용자 가설은 *입자경(µm) 채널로는 성립하기 어렵다*.
(주의: 가설의 물리적 *방향*—작은 결정자에서 DOS narrowing—자체는 옳다. 다만 그 효과가 켜지는 크기 스케일이 흑연 입자경보다 1~3 자릿수 작다.)

**(4) 열린 문제**
- 면내 도메인 La 가 진짜 nm급인 분획(나노결정성/고결함 흑연, edge-rich 입자)이 시료에 섞여 있으면, 그 분획에 한해 수 mV급 전자구조 기여가 가능 — 입자경이 아니라 **결정자/도메인 크기 분포**로 가설을 재정식화하면 살아날 여지.
- Dahn(1992)는 DOS 변경을 *화학 도핑(B)*으로 했다. *크기*로 DOS 를 바꿔 OCV shift 를 본 흑연 선례는 이번 조사서 **근거미발견**.
- 순수 흑연 semimetal·rigid-band 위배(ARPES) 때문에, "작은 입자 DOS narrowing"의 정량 예측엔 단순 rigid-band 가 아닌 stage-별 실제 밴드 계산이 필요.

**가장 강한 DOI**: **Dahn, Reimers, Sleigh, Tiedje, Phys. Rev. B 45, 3773 (1992), doi:10.1103/PhysRevB.45.3773** —
흑연 OCV→전자 DOS 직접 매핑의 keystone(틀 지지). 크기 스케일 근거는 doi:10.1103/PhysRevLett.97.216803 (Son-Cohen-Louie 2006) + doi:10.1021/acsnano.7b06765 (Merino-Díez 2018).
