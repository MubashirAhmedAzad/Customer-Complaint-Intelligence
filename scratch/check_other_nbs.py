import json
import glob

for p in sorted(glob.glob('notebooks/*.ipynb')):
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'resample("M")' in content or "resample('M')" in content:
        print(f"Found resample('M') in {p}")
    if 'append(' in content and 'df.' in content:
        print(f"Potential df.append in {p}")

