# -*- coding: utf-8 -*-
"""comment_gate.py — 단정형 코드 주석 식번호 게이트.
graphite_ica_model.py 주석의 하드코딩 (1.x) 가 현재 .aux 의 식번호와 다르면 exit 1.
(V.T R5·V.U R3 에서 중간식 삽입 때마다 주석 번호가 stale 해진 사고의 재발 방지 —
새 식이 추가되어 번호가 밀리면 이 게이트가 즉시 FAIL 한다.)"""
import io, re, sys

import sys as _sv
_ver = _sv.argv[1] if len(_sv.argv) > 1 else 'v2'
AUX = rf'D:\Projects\Project_Anode_Fit\Claude\docs\graphite_ica_ch1_Fable_{_ver}.aux'
PY = r'D:\Projects\Project_Anode_Fit\Claude\results\V2_E_codeexample\graphite_ica_model.py'

aux = io.open(AUX, encoding='utf-8', errors='replace').read()
nums = dict(re.findall(r'newlabel\{eq:([A-Za-z]+)\}\{\{(1\.\d+)\}', aux))
py = io.open(PY, encoding='utf-8').read()

CHECKS = [
    '"""({hysdU}) spinodal 상한 gap',
    '"""({hyscenter}) 분기 중심',
    '"""({logistic}) 의 꼴',
    '"""({lnLq}) — M3',
    '"""({hysmaster}) 양방향 통합식',
    '# ({vapp})',
    '# ({cbg})',
    '# ({affinity}) 방향형',
    '# ({chisum}) 합-1',
    '# ({hysmaster}) 종',
    '# ({hysmaster}) 꼬리',
    '({simplefit}) 종 항만',
    '... ({LqV})',
    '... ({ydef})·({arrhenius})',
    '... ({hysobsgap})',
]
bad = [t for t in CHECKS if t.format(**nums) not in py]
import sys as _s
try:
    _s.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
print(f"comment gate: {len(CHECKS)-len(bad)}/{len(CHECKS)} ok" + (f" -- STALE: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
