# HANDOVER — v1.0.14 완주 세션 (2026-07-04)

> **Chain**: v1.0.10 문제점 대검수(9종+10차) → 인계 무결성 대검수+LCO 수식-주도 검수(`v1.0.10/HANDOVER_v1.0.11.md`) → v1.0.12 Fable 재검 5대 지시 완주(`process/V1012_EXECUTION_LEDGER.md`, 커밋 ea4c169) → v1.0.13 통계역학-first 재구조화 완주(`v1.0.13/HANDOVER_v1.0.13.md`, 커밋 5995d64) → **본 핸드오버(v1.0.14, 기준 커밋 bea6571~)**. 이 리스트만으로 역추적 가능.

## 1. 본 세션 지시(요지 — 전문은 플랜 rev.2 §Summary)
1. 사용자 피드백 8건: F-A 어투(교과서·메이저 저널급 — "양자역학 불요" 류 금지) / F-B eq1.8 엄밀 유도(사전 설명 후 납득 — Hill Ch.7, "간결보다 면밀" GO) / F-C spinodal 사전지식 부록(별도 문건, 편입은 검토 후) / F-D §1.7 식·이미지 보강 / F-E PSD 보편식 도입 후 수치 유도로 배제 / F-F 코드 연계 = 단방향(문건 내 변수명 금지) / F-G 레퍼런스 DOI / F-H §1.13 → appendix 표.
2. 방식: 방법론·큰 틀 동일(지침·과거 플랜 준수)·문건 절별 루핑(체리픽 없음)·이미지만 9안(S3/O3/C3) 경연·토큰 절약(기계 작업 Sonnet·판단 Fable).
3. GO: "물리·화학 이론 전개 시 문제 발견되면 수정하면서 가는 것 필수(최우선 물리>비약>수식-주도). 반영해서 작업 진행하자."

## 2. 본 세션 작업 요약
- P1.1 증판+감사 2종(어투 79·코드 언급 83)+판정 → P2.1 물리 3건(Hill 유도·PSD 배제·spinodal 부록 초안) → P2.2 재배치(부록 A/B·§1.7 폭 예산) → P3.1 어투 루핑(수식 해시 무손실 검증) → P3.2 레퍼런스(신규 bibitem 5·park2021 정정 — 전건 Crossref 검증) → P4.1 검수 R1~R7(누적 ~98건 정정·수렴 종결) → P5.1 경연(72안→8승자 편입+master 캡션 검증 정정 4건) → P6.1 마감.
- 상세·결정 근거 = `Claude/results/V1014_RESULT.md`(11항목) + `Claude/results/process/V1014_EXECUTION_LEDGER.md`(정본).

## 3. 미완료·사용자 검토 대기
- **①spinodal 부록**(`appendix_phase_separation.pdf`, 8p) — 편입/폐기 결정 대기(본문 §1.2·§1.5 연결 문장은 편입 확정 시 삽입).
- **②경연 편입 그림 8종** — 물리·좌표·컴파일 검증 완료, 미감(취향) 확인만 대기(원본 복원은 `results/process/fig_contest/_replaced_originals.tex`).
- 이월(실데이터 단계): 다온도 T² 동결 해제·LCO Ω^cat/dH_a 배정·ν≳10 상향 재베이스라인·x-매핑 순환 수치 확인(v1.0.13 승계) + Motohashi g_max=13·ml2024·[A2]–[A5] 원문 직접 재확인.

## 4. 다음 세션 주의
- **부호 함정 3종 가드 유지**(문서·코드·가이드에 깔려 있음 — 지우지 말 것): ①σ_d 슬롯=탈리튬화(LCO 충전↦+1, `curve(direction=+1)` 처방 금지) ②Bernardi "방전(I>0)"=흑연 리튬화 ③MSMR f=+σ_d.
- **py 원형 보존 구역**(L74 헤더 "1바이트도 변조 X") — 주석 추가도 금지(이번 세션에 침범분 원복 이력 있음).
- 회귀 = `python test_regression_graphite.py`(무인자 verify) 13/13 이 게이트. capture 는 골든 덮어씀.
- v1.0.14 원본은 이제 동결 관례(개정은 v1.0.15) — 결과 문건 정정은 Addendum 패턴.
- FITTING_GUIDE 의 수치(문턱 70–74 kJ/mol 등)는 코드 재검산 기준값 — 코드 기본값(z_cut·A_cap·dVdq_qa 등) 변경 시 함께 갱신 필요.
- Codex 연동: rescue 서브에이전트 Bash stdout 결함 시 companion CLI 직접 구동(`task --write --fresh`, 폴더 선생성) 레시피가 이 세션에서 확립됨.
