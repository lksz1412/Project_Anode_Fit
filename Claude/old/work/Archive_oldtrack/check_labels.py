import re, glob
from collections import defaultdict

base = r'd:/Projects/Project_Anode_Fit/Claude/docs'
labels = defaultdict(list)
for ch in range(1, 7):
    fn = f'{base}/graphite_ica_ch{ch}_rebuilt.tex'
    txt = open(fn, encoding='utf-8').read()
    for m in re.finditer(r'\\label\{([^}]+)\}', txt):
        labels[m.group(1)].append(ch)

dups = {k: v for k, v in labels.items() if len(set(v)) > 1}
print('total unique label keys:', len(labels))
total_label_occurrences = sum(len(v) for v in labels.values())
print('total label occurrences:', total_label_occurrences)
print('cross-chapter duplicate label keys:', len(dups))
for k, v in sorted(dups.items()):
    print('  DUP', k, '->', v)

# also list Ch1 non-prefixed labels (potential collision class)
ch1 = [k for k, v in labels.items() if 1 in v]
nonpref = [k for k in ch1 if not re.match(r'(eq|sec|tab|fig):ch\d', k)]
print('\nCh1 labels not using chN prefix (count={}):'.format(len(nonpref)))
for k in sorted(nonpref):
    print('   ', k)
