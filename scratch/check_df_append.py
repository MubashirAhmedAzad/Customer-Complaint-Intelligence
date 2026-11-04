import json
import glob
import re

for p in sorted(glob.glob('notebooks/*.ipynb')):
    with open(p, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    for i, c in enumerate(nb['cells']):
        if c['cell_type'] == 'code':
            src = ''.join(c['source'])
            # match df.append or dataframe.append
            if re.search(r'\b\w+_?df\.append\(', src) or re.search(r'\bdf\.append\(', src):
                print(f"File {p} Cell {i}: found df.append")
                for line in src.splitlines():
                    if '.append(' in line:
                        print("  ", line.strip())

