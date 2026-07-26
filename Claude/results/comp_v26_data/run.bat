@echo off
chcp 65001 >nul
cd /d "D:\Projects\Project_Anode_Fit\Claude\results\comp_v26_data"
echo ============================================================
echo  1) 평형 데이터 다운로드 시도 (GITT+hold; 이미 있으면 스킵)
echo ============================================================
powershell -ExecutionPolicy Bypass -File ".\dl_sintef.ps1"
echo.
echo ============================================================
echo  2) 분석 - 로컬 기존 데이터(gr/si/sigr)로도 3종 결과 보장
echo ============================================================
python ".\analyze_sintef.py"
echo.
echo ============================================================
echo  완료. 결과 이미지: out\graphite_dqdv.png / silicon_dqdv.png / blend_dqdv.png
echo         요약: out\summary.json
echo ============================================================
pause
