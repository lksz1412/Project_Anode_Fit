# Phase 059 v1.0.17 문건·인용 감사

정본일: 2026-07-28

판정: `CONDITIONAL_P059_V1017_BIBLIOGRAPHIC_CORRECTIONS_AND_REGISTER_CLEANUP_PASS_BUT_CITATION_SCOPE_THEORY_BODY_AND_SCIENTIFIC_AUTHORITY_FAIL`

## 결론

v1.0.17은 생산 물리나 알고리즘을 바꾼 판이 아니다. 생산 코드와
golden은 byte-identical이다. plot, LCO heat demo와 regression
harness는 버전/절대경로 문자열만 바뀌었고 계산 논리와 assertion은
같다. 따라서 이 판의 정당한 지위는 doc-only register·서지 정련이다.

두 잘못된 DOI를 바로잡은 것은 분명한 개선이다.
`occupation2019`는 134774가 맞고, `hysteresis2018`은
`2018.05.052`가 맞다. 그러나 서지 완결과 주장-인용 정합은 아직
닫히지 않았다.

## 인용 범위 판정

- Konar et al. 2015는 LiH/graphite 고온 합성, PXRD/Raman과 staged
  phase 안정성 논문이지 본 문건 주석이 말하는 형성 엔탈피
  calorimetry 논문이 아니다.
- Garrick et al. MSMR Part I은 가역 entropy coefficient와 gallery
  분해를 다룬다. 이를 Eyring activation entropy가 가역열에 들어가지
  않는다는 문장의 직접 근거로 쓰는 것은 인용 위치가 맞지 않는다.
- Paul et al. Part II는 MCMB graphite 다온도 MSMR 추정을 지지하지만
  이 저장소의 4-transition 기본값을 검증하지 않는다.
- Hales--Bulman은 full-cell 유효 entropy coefficient 추출 방법을
  지지할 뿐, 본 문건의 graphite \(+60.8\) mW/A 수치를 검증하지 않는다.
- Haruyama et al.은 graphite의 vibrational/configurational free-energy
  기여를 직접 다루므로 해당 범위에는 적합하다.
- Zilberman et al.은 temperature-path-dependent OCP hysteresis와
  entropy 측정 불확실성을 직접 지지한다.

MSMR Part I/II에는 article number 023502/103505가 빠졌고 Part II
제목도 원제와 정확히 같지 않다. hysteresis 논문은 DOI는 고쳤으나
179--184쪽이 빠졌다.

## 문건 경계

제목과 여러 본문 표현에서 `코드`를 `계산` 또는 `모델`로 바꾼 방향은
사용자 제약에 맞다. 하지만 지정된 구현 대응 부록 밖에 구현 언어가
여전히 남는다. Chapter 2에는 `entropy_coefficient`가 본문에 있고,
내부 `Anode_Fit_v1.0.17` 계산이 참고문헌 항목으로 들어가 있다.
그러므로 theory-only body gate는 아직 FAIL이다.

## 권위

v1.0.17이 새로 확보한 것은 서지 오류 정정과 표현 개선이지 graphite,
LCO, Si 또는 doped high-voltage LCO의 외부 데이터 적합성 검증이
아니다. handover의 “리뷰 완전 반영”, “완결”은 작업 절차의 자기
보고로만 보존하며 과학적 완결 권위로 승격하지 않는다.

## 다음 단계

Step 38.2에서 v1.0.18.1이 v1.0.17의 물리 무변경 이월판인지
theory/code/test/PDF 전 축에서 판정한다.

원본 `Claude/`, `main`은 수정하지 않았다.
