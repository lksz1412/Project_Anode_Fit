import re
from collections import defaultdict

base = r'd:/Projects/Project_Anode_Fit/Claude/docs'
# map label -> defining chapter
label_ch = {}
for ch in range(1, 7):
    txt = open(f'{base}/graphite_ica_ch{ch}_rebuilt.tex', encoding='utf-8').read()
    for m in re.finditer(r'\\label\{([^}]+)\}', txt):
        label_ch[m.group(1)] = ch

# find all \ref / \eqref / \pageref usages and their chapter
crosses = []
unresolved = []
for ch in range(1, 7):
    txt = open(f'{base}/graphite_ica_ch{ch}_rebuilt.tex', encoding='utf-8').read()
    for m in re.finditer(r'\\(?:eqref|ref|pageref|autoref)\{([^}]+)\}', txt):
        key = m.group(1)
        if key == 'LastPage':
            continue
        if key not in label_ch:
            unresolved.append((ch, key))
        elif label_ch[key] != ch:
            crosses.append((ch, key, label_ch[key]))

print('cross-chapter \\ref/\\eqref usages (ref in chA to label defined in chB):', len(crosses))
for ch, key, dch in crosses:
    print(f'  Ch{ch} refs {key} (defined in Ch{dch})')
print('\nunresolved \\ref/\\eqref (label not defined in ANY chapter):', len(unresolved))
for ch, key in unresolved:
    print(f'  Ch{ch} refs UNDEFINED {key}')
