# V1024 EXECUTION LEDGER (12-col)

> v1.0.24 = 반쪽셀 dQ/dV 생성기 완성도 검증·보정. 계획서 = `plans/2026-07-18-v1024-completeness-validation-plan.md`.
> 대상 화학: LCO·흑연·흑연+Si(전부 v1.0.23 보유). 순서 흑연→LCO→블렌드. 검증 매트릭스 = GITT/0.05/0.1/0.2C × 15/23/35/45°C.
> 운용 = Opus 마스터+진단·저작 / 조사(공개데이터)=병렬 리서치 에이전트.

| Phase | Planned | Actual | Block | Purpose | Status | Plan | Result | Artifacts | Validation | Gate | Next |
|---|---:|---:|---|---|---|---|---|---|---|---|---:|
| V0 | 1-4 | 1-4 | setup | 검증설계·조건↔출처 매핑·코드 T/I/V 구현범위 확인 | PASS | 계획서 §Phase V0 | results/PHASE_V0_RESULT.md | (코드 확인) | 매트릭스·매핑·코드 T/I/V 확정: I→func_L_q(∝\|I\|)·T→func_w(nRT/F)+func_L_q(Arrhenius)+n(T)·σ_η(③)=코드 미예측(w_j 흡수) | PASS_V0 | 5 |
| V1 | 5-8 | 5-7 | data | 공개데이터 조사(흑연/LCO 반쪽셀·GITT/저율·다온도) | PASS(부분) | 계획서 §Phase V1 | results/PHASE_V1_RESULT.md | PUBLIC_DATA_SURVEY.md·zenodo_gr(2셀) | 흑연/블렌드=Zenodo 20086298 확보·LCO=공개부재(풀셀만)·공개=상온C/50만(율①·T축 사내필요) | PASS_V1(LCO공백·T/율공백 명시) | 8 |
| V2 | 9-12 | 8-12 | 흑연평형 | 흑연 near-eq(pOCV C/50) 브로드닝②③ 검증+M제거 근거(평형) | PASS | 계획서 §Phase V2 | results/PHASE_V2_RESULT.md | gr_fit.png·gr_dva_Mremoval.png·v24_graphite_fit.py·gr_fit_result.json | 실측 두-상 FWHM 3.5–4mV=0.14–0.16·RT/F(near-delta,§7정합)·출하 equilibrium() 피팅 R²=0.95(2셀)·높이 209/90.6≈real 201/98·default(w=RT/F)~20×과대·FIT dV/dQ(M無)가 real골 재현 | PASS_V2(기본값현실성=CONDITIONAL·율①/T=미검증) | 13 |
| V2b | 13-15 | 13-15 | 블렌드평형 | 흑연+Si 블렌드 합성식(§3.5) 검증(2조성 저/고Si) | PASS | 계획서 §Phase V2 | results/PHASE_V2B_RESULT.md | blend_fit.png·v24_blend_fit.py·blend_fit_result.json | blend=gr+si 가산 R²=0.94–0.98·흑연 host 위치불변(0.10/0.14/0.225=순수흑연)·Si 0.29–0.46V 함량의존·f_Si(고Si) fit0.776≈metadata0.75 | PASS_V2b(저Si f_Si축퇴=CONDITIONAL·율①/T=미검증) | 16 |
| V2c | 16-22 | 16-22 | 확장·양극·각짐 | 10셀 다중화학+NMC양극(⚠LCO대리)+각짐규명+MSMR정체+개선방향 | PASS | 계획서 §Phase V2 | results/PHASE_V2C_RESULT.md | multi_fit.png·cathode_fit.png·gr_angular_diag.png·IMPROVEMENT_DIRECTIONS.md | 순수Si R²=0.998·흑연피크 전조성 불변·NMC양극 R²=0.99·각짐=격자아티팩트(모델 해석적매끈)·문건식=MSMR 정확동형(w=ωRT/F)·개선 랭크(전이4→6·비대칭폭·정칙용액) | PASS_V2c(저Si축퇴·NMC≠LCO·B_c2저품질) | 23 |
| V3 | 23-25 | 23-25 | 유한율속① | 율속시리즈(Zenodo 20323533) ① 브로드닝·분극 검증 | PASS(정성) | 계획서 §Phase V3 | results/PHASE_V3_RESULT.md | rate_broadening.png·v24_rate_broadening.py | ①브로드닝: 높이191→3(20×I)·~10mA washout / 분극: 피크 20mV/mA 선형R²=0.86(V_n=V−|I|Rn) / 정량L_V∝|I|=DEFER(상용SiOx confound→dqdv()피팅) | PASS_V3(정성·반정량·정량이월) | 26 |
