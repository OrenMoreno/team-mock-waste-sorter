from pathlib import Path
from collections import Counter
labels_dir = Path('dataset/train/labels')
class_counts = Counter()
for f in labels_dir.glob('*.txt'):
    for line in f.read_text().splitlines():
        if line.strip():
            class_counts[int(line.split()[0])] += 1
names = {0:'plastic', 1:'metal_can', 2:'paper_cardboard', 3:'other'}
print('Label distribution:')
for cls_id, count in sorted(class_counts.items()):
    label = names.get(cls_id, 'STILL BROKEN')
    print(f'  Class {cls_id} ({label}): {count} instances')
