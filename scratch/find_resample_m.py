import glob

for f in sorted(glob.glob('notebooks/*.ipynb') + glob.glob('src/**/*.py', recursive=True) + glob.glob('pages/*.py')):
    with open(f, 'r', encoding='utf-8') as fh:
        lines = fh.readlines()
    for idx, line in enumerate(lines):
        if 'resample(' in line and ('"M"' in line or "'M'" in line):
            print(f"{f}:{idx+1}: {line.strip()}")

