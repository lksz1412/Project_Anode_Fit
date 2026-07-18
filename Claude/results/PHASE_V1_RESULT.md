# Phase V1 — 공개 반쪽셀 데이터 조사·확보 Result

## Summary
흑연·LCO·흑연+Si 반쪽셀 dQ/dV 검증을 위한 공개 실측 데이터를 조사·확보했다. **흑연·흑연+Si**는 Zenodo 20086298(pseudo-OCV ~C/50, 상온, 다수 셀)이 강한 앵커로 확보. **LCO 반쪽셀**은 공개 실험 데이터 부재(전부 풀셀·상용) — 계획서의 화학 3종 중 LCO 는 공개데이터 경로가 막힘을 확정 기록. 아울러 공개데이터는 **상온·저율(C/50)** 로 한정 → 검증 매트릭스의 **다온도(15/35/45°C)·율①(0.05/0.1/0.2C)** 축은 공개데이터로 테스트 불가(사내 회사데이터 필요)임을 확정.

## Step Range
Cumulative **5–7** (V0 1–4 이어).

## Inputs
- 계획서 §Phase V1(공개데이터 조사 설계).
- 병렬 리서치 2창(흑연 반쪽셀 / LCO 반쪽셀 공개데이터 서베이) 결과.
- Zenodo record 20086298 파일 목록(metadata.csv, 95 파일).

## Files Created
- `results/comp_v24/PUBLIC_DATA_SURVEY.md`(조사 요약: 확보처·부재 확정·한계).
- 스크래치: `zenodo_gr/`(metadata.csv, gr_pocv_1d5628.parquet, gr_pocv_4ccc47.parquet) — 임시(비커밋 원자료).

## Files Updated
- (없음)

## Read Coverage
- Zenodo 20086298 metadata.csv 전수 스캔(95 파일 → p-ocv/graphite/SiGr 분류).
- 리서치 2창 보고 전문.

## Execution Evidence
- **흑연/블렌드**: Zenodo 20086298 = 흑연 및 Si-흑연 반쪽셀 pseudo-OCV(~C/50) parquet 다수. 컬럼 `Test Time/s, Current/A, Voltage/V, Step Index, Cumulative Capacity/Ah`. 상온.
- **LCO**: 공개 실험 반쪽셀(vs Li) dQ/dV 원자료 **부재** 확정 — 검색된 LCO 데이터셋은 전부 풀셀 사이클/상용 셀. (계산적 OCV 형상은 Materials Project 경로 가능하나 실측 아님.)
- **온도·율 축**: Zenodo 20086298 은 상온·C/50 단일 조건 → (율−GITT)=①·4온도=T의존 축은 공개데이터에 없음.

## Validation
| 게이트(V1) | 판정 | 근거 |
|---|---|---|
| 흑연 공개데이터 확보 | PASS | Zenodo 20086298 pseudo-OCV 2셀 다운로드·로드 성공 |
| LCO 공개데이터 확보 | **FAIL(확정)** | 공개 실험 반쪽셀 부재 — 풀셀만 존재 |
| 검증 매트릭스 커버리지 | PARTIAL | 공개데이터=상온·C/50만 → ②③(평형)만 테스트 가능·①·T 축 사내 필요 |

## Gate
**PASS(부분).** 흑연·블렌드 공개데이터로 평형 브로드닝(②③) 검증 진입 가능(→V2). LCO·율①·다온도는 커버리지 공백으로 **명시 기록**(사용자 결정 대상 — 아래 추가 후보).

## Confirmed Non-Changes
- 코드·문건 무수정(조사 phase). v1.0.23 불가침. 원자료 원본 미변조.

## 추가 후보 (실행 X — 사용자 결정 대상)
1. **LCO 공개데이터 공백**: (a) Materials Project/계산 OCV 로 *형상만* 정성 점검, (b) 사내 회사데이터로 이관(반출 불가 → 스크립트만 사내 실행), (c) LCO 검증 보류. → 기본안 = (a) 형상 점검 + (b) 스크립트 준비.
2. **율①·다온도 축**: 공개데이터 부재 → 검증 스크립트를 완성해 **사내 실행 패키지**로 납품(GITT/0.05/0.1/0.2C × 15/23/35/45°C).
