# v12 Round-Trip 검증 보고 (2026-07-01)

> 대상: `Anode_Fit_v12.py` (v11_final 기반, use_w_eff 경로 제거본)
> 실행 환경: Python 3.12 / NumPy 2.x / SciPy — Windows

## 제거 항목 확인

| 항목 | 제거 여부 |
|------|-----------|
| `func_w_eff` 함수 | ✓ 삭제 |
| `use_w_eff` 생성자 인자 | ✓ 삭제 |
| `w_eff_floor_frac` 생성자 인자 | ✓ 삭제 |
| `self.use_w_eff` 속성 | ✓ 삭제 |
| `self.w_eff_floor_frac` 속성 | ✓ 삭제 |
| `_width()` 내 use_w_eff 분기 | ✓ 삭제 (func_w 직접 반환만) |
| `__main__` 내 `use_w_eff=False` | ✓ 삭제 |
| `use_dH_eff` / 기타 로직 | 불변 |

## (a) 단일 LiC₆ 전이 평형 peak — 면적 보존

| 항목 | 값 | 판정 |
|------|-----|------|
| 면적 (∫dQ/dV·dV) | **0.4951** | Q=0.5 보존 ✓ |
| FWHM | **42.3 mV** | 종모양 (35~55 mV 범위) ✓ |
| 유한성 | True | ✓ |

## (b) full dQ/dV (4전이 + 동역학 꼬리)

| 항목 | 값 | 판정 |
|------|-----|------|
| 유한성 | True | ✓ |
| max dQ/dV | 7.350 | 정상 범위 ✓ |
| 종모양 구조 | 4 peak 뚜렷 | ✓ |

## (c) v11 기본(use_w_eff=False) vs v12 거동 동일

| 비교 항목 | max_diff | 판정 |
|-----------|---------|------|
| equilibrium() | **0.00e+00** | 완전 동일 ✓ |
| dqdv() 방전 0.2C | **0.00e+00** | 완전 동일 ✓ |

v12는 v11의 `use_w_eff=False` 경로(정상 경로)만 남긴 것이므로 출력 차이 = 정확히 0.

## (d) v12 __main__ 독립 실행

- 반환 코드: 0 (예외 없음)
- `overall OK: True` 출력 확인
- guard 7/7, per-tr override isolation: True

## 결론

- 실행 완료: ✓
- 면적 보존: ✓ (0.4951 ≈ Q=0.5)
- 종모양: ✓ (FWHM 42.3 mV)
- v11_base vs v12 차이: 정확히 0
- use_w_eff 기계장치 전부 제거: ✓
- 불확실 사항: 없음 (정수치 검증 모두 통과)
