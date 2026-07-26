# comp_v26_data — regsol 재검증 (v1.0.26 A/B 두 버전의 근거)

> v1.0.25 가 삭제한 regsol(정칙용액 두-상 커널)을 되살릴지 판정하기 위한 실측 작업 폴더.
> **결과 문서는 여기가 아니라** [`Claude/docs/v1.0.26A-regsol/`](../../docs/v1.0.26A-regsol/README.md) ·
> [`Claude/docs/v1.0.26B-gallery/`](../../docs/v1.0.26B-gallery/README.md) 에 있다.

## 무엇을 물었나

1. regsol 은 **물리 전이 4 개**로 **gallery 7 개로의 분화**를 스스로 모사하는가? → **아니다**(ΔBIC +844.5)
2. regsol 을 되살릴 근거가 있는가? → **적합도로는 없다.** 단 흑연 Ω≈2RT 는 문헌 앵커와 맞는다.

## 파일 (현행)

| 파일 | 역할 |
|---|---|
| `bdd_dqdv.py` | 사용자 BDD `99_Backend` 방식 dQ/dV 이식 — dMSMCD 다중창 중앙값 미분 + 웨이블릿 denoise + savgol 앙상블 |
| `regsol_kernel.py` | ★regsol / skew-regsol 커널 — 조성격자 ripple 제거판(혼화갭 닫힌형 + 밀도⊛FFT합성곱) |
| `test_skew_regsol_v2.py` | 커널 4 종 정의 + 데이터 로더(등장성회귀 → 균일 V 격자 재빈닝) + 동일 N 비교 |
| `test_gallery_vs_regsol.py` | ★전이 수 스윕(N=3~8) + gallery 근축퇴 검출 → `out_v3/` |
| `build_two_versions.py` | 버전 A(regsol) · B(gallery) 피팅 → `out_versions/` |
| `make_version_docs.py` | 위 결과를 `docs/v1.0.26*/README.md` 로 굽는다(수치 전사 오류 0) |
| `MULTI_DATASET_REVIEW.md` | 다각 데이터·소재별 물리 문헌 검토 |
| `HANDOVER_regsol_investigation.md` | 착수 시점 인계문서(서비스 장애로 실행 차단됐던 기록) |
| `dl_sintef.ps1` · `analyze_sintef.py` · `run.bat` | GITT/hold **평형** 데이터 확보 파이프라인 — **미실행(잔여 과제)** |

## ⚠️ 폐기 (실행하지 말 것)

| 파일 | 폐기 사유 |
|---|---|
| `test_skew_regsol.py` · `out_skew/` | 결함 3 건 — ① `np.gradient` 로 1 µV 양자화 V 를 미분해 dQ/dV 가 **10¹²** 로 발산 ② 비대칭을 δL≠δR 조각폭으로 구현(v1.0.25 실제 채택분은 α 지수형) ③ skew 커널 정규화 4×·2× 오류로 면적=Q 파괴. 게다가 피팅 예외를 삼켜 4 종 전부 실패했는데 빈 JSON 만 남겼다. |
| `regsol_decision.html` · `../regsol_test/` | 위 폐기분 기반 |

## 재현

```bash
python -X utf8 test_gallery_vs_regsol.py   # 전이 수 스윕
python -X utf8 build_two_versions.py       # 두 버전 피팅
python -X utf8 make_version_docs.py        # docs 문서 생성
```

필요 패키지: `numpy` `scipy` `pandas` `matplotlib` `PyWavelets`.
원자료: `../comp_v24/sintef_data/` (SINTEF Zenodo 20086298, CC-BY-4.0).

## 잔여 (다음 세션)

- **★평형 데이터 재검** — 현 판정은 전부 plain p-OCV(비평형) 위에서 나왔다. `dl_sintef.ps1` 로
  GITT / p-OCV+hold 를 받아 재실행해야 확정된다. 특히 흑연 0.104 V 피크의 FWHM ≲ 1 mV
  (RT/F 의 1/25)가 진짜 두-상인지 비평형 인공물인지는 평형 데이터로만 갈린다.
- 신규 CSV 리포 영구보존(v1.0.25 N6) · 파라미터 불확실도(bootstrap) 미산출.
