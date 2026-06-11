# -*- coding: utf-8 -*-
"""build_gate.py — 단정형 빌드 게이트. err/Overfull/undef 가 0 이 아니면
exit 1 (V.P P.R3·V.T T.4 에서 echo 비단정 게이트가 overfull 커밋을 통과시킨
사고의 재발 방지)."""
import io, sys, re
log = io.open(r'D:\Projects\Project_Anode_Fit\Claude\docs\graphite_ica_ch1_Fable_v2.log',
              encoding='utf-8', errors='replace').read()
err = len(re.findall(r'^!', log, re.M))
of = log.count('Overfull')
undef = len(re.findall(r'Reference.*undefined', log))
pages = re.search(r'Output written.*\((\d+) pages', log)
print(f"gate err={err} overfull={of} undef={undef} pages={pages.group(1) if pages else '?'}")
sys.exit(0 if (err == 0 and of == 0 and undef == 0) else 1)
