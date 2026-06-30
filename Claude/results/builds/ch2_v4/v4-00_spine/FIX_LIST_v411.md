# Ch2 v4-11 — adversarial 재검수 fix-list (v4-10 → v4-11)

> A1/A2/A3 결함 누적. master 삼각검증 후 v4-11 정정. v4-10 = 견고(4대 부호 반증 실패).

## A1 분포·부호 ✅ (CRIT 0)
- ★4대 부호(config `+R ln[ξ/(1-ξ)]`·exo/endo·w_eff `w(1-Ω/2RT)`·μ(V)/단위다리) 전부 견고. 역수·역매핑 0.
- **A1-H1 (HIGH)**: vib(BE eq:Svib_mode)·elec(Sommerfeld S_e, line 372-374) 두 항이 "분포→엔트로피" 중간대수 생략·라벨 후 결과 직착(공식·부호는 교과서 정확). → 간단 중간대수 1-2줄 추가 *또는* Ch1 v9 §전자엔트로피 전개 명시 참조(Ch2 는 *확장*이므로 참조 적절).
- **A1-L1 (LOW)**: line 680 "선두차수까지다" — 42_numerical 이 겹침 포함 175점 abs-err=0 입증한 걸 과소진술 → "중심 근사(단순식); 완전식은 config 포함 0.000 일치" 로 다듬기.
- (별도) 내 스파인 doc `41_statmech_spine.md` line27 역수 표기 — v4-10 미상속이나 doc 일관성 위해 확인·정정(소스 정합).

## A2 섞임·범위 ✅ (CRIT 0)
- A 겹침·w_eff·극한·범위(하프셀 CLEAN)·Bernardi 전부 견고(독립 재현 확인).
- **A2-D1 (HIGH)**: line 680 "현재는 선두차수까지다" = §A·§B "완전식=FD 부동소수점 일치" 와 자기모순(강겹침 테스트 max|FD−완전식|=0.00001). "선두차수"는 단순식 수식어인데 완전식 한계로 오이월 → **삭제·재서술**. (A1-L1 과 동일.)

## A3 인용·빌드·문체 ✅ (CRIT 0)
- ★**chemmater2015 = 정당 인용**(DOI 10.1021/acs.chemmater.5b00235·Konar 2015 Chem.Mater.27(7)·실존·도메인 정합). 미제거 옳음. jpcc2021 "Calculations" 포함. **fabrication 0**.
- **문체 PASS**(한계·갭·맺음 전부 완결 문장·전보체 0). 빌드 0-error·overfull 1(4.57pt<20).
- **A3-D1 (MED)**: ★TikZ 3 그림 node 텍스트에 **한글 포함**(영어 ASCII 위반) → 영어로 교체.
- **A3-D2 (MED)**: line 386 "파생 I" **dangling**(문서 내 미정의 — 설계 doc 포인터 누출) → 제거 or 문맥 표현으로.

## ★v4-11 정정 종합 (전부 제시/조판·물리 무변)
1. A1-H1: vib(BE)·elec(Sommerfeld) 중간대수 1-2줄 추가 or Ch1 v9 전개 참조(Ch2=확장).
2. A2-D1/A1-L1: line 680 "선두차수까지다" 삭제·재서술(단순식 중심 근사 / 완전식 0.000 일치).
3. A3-D1: TikZ 3그림 한글 node → 영어 ASCII.
4. A3-D2: line 386 "파생 I" dangling 제거.
5. 불변: config·w_eff·exo/endo·범위·인용 전부.

## 정정 원칙
base=v4-10 복사→v4-11, HIGH 정정(vib/elec 중간대수 or Ch1 참조)+가능 LOW, 부호·w_eff·config 불변, 정식 10회 후 xelatex 0-error.
