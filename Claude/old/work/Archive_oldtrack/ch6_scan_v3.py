# -*- coding: utf-8 -*-
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'd:/Projects/Project_Anode_Fit/Claude/docs'
full = open(f'{BASE}/graphite_ica_full_rebuilt.tex', encoding='utf-8').read()

print('=== All "Chapter 6 / Ch.6 / Ch6" occurrences in merged full doc ===')
hits = list(re.finditer(r'Chapter[~ ]?6|Ch\.?[~ ]?6', full))
print('count:', len(hits))
for m in hits:
    ctx = full[max(0, m.start() - 50):m.start() + 40].replace('\n', ' ')
    print('  >>', ctx)

print()
print('=== sec:ch6_ label count (Ch1 Appendix B labels — legitimate) ===')
print('sec:ch6_ labels:', len(re.findall(r'sec:ch6_', full)))

# Distinguish legitimate (구 Chapter 6 / preamble comment / Ch6 해체) from any body
# claim of a separate "Chapter 6" section.
print()
print('=== \\section{Chapter ...} headers in merged doc ===')
for m in re.finditer(r'\\section\{Chapter[^}]*\}', full):
    print('  >>', m.group(0)[:80])
