import glob

for f in sorted(glob.glob('notebooks/*.ipynb') + glob.glob('src/**/*.py', recursive=True) + glob.glob('pages/*.py')):
    with open(f, 'r', encoding='utf-8') as fh:
        text = fh.read()
    if 'resample' in text:
        for idx, line in enumerate(text.splitlines()):
            if 'resample' in line:
                print(f"{f}:{idx+1}: {line.strip()}")

