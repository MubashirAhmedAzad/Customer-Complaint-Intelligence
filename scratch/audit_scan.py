"""Static audit scan for deprecated patterns, hardcoded paths, and syntax errors."""
import ast, glob, re

issues = []

files = (
    glob.glob('src/**/*.py', recursive=True) +
    glob.glob('pages/*.py') +
    glob.glob('tests/*.py') +
    ['app.py', 'config/settings.py']
)

deprecated_patterns = [
    (r'use_container_width', 'DEPRECATED: Streamlit use_container_width (remove after 2025-12-31, use width=)'),
    (r'st\.experimental_', 'DEPRECATED: st.experimental_ API'),
    (r"resample\([\"']M[\"']\)", 'DEPRECATED: pandas resample("M") — use "ME"'),
    (r'DataFrame\.append\(|df\.append\(', 'DEPRECATED: DataFrame.append() — use pd.concat()'),
    (r'\.iteritems\(\)', 'DEPRECATED: iteritems() — use .items()'),
    (r'customer-complaint-root-cause-classifier1', 'OLD PATH: stale folder name reference'),
    (r'GEMINI_API_KEY\s*=\s*["\'][A-Za-z0-9_-]{10,}', 'SECURITY: Possible hardcoded API key'),
    (r'eval\(', 'SECURITY: eval() usage'),
    (r'except:\s*$|except\s+Exception\s*:\s*pass', 'SMELL: Bare except or silent pass'),
]

for fpath in sorted(files):
    try:
        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
        for lineno, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('#'):
                continue
            for pattern, msg in deprecated_patterns:
                if re.search(pattern, line):
                    issues.append((fpath, lineno, msg, stripped[:120]))
        try:
            ast.parse(''.join(lines))
        except SyntaxError as e:
            issues.append((fpath, e.lineno, f'SYNTAX ERROR: {e.msg}', ''))
    except FileNotFoundError:
        pass
    except Exception as e:
        issues.append((fpath, 0, f'READ ERROR: {e}', ''))

if issues:
    print(f'\nTotal issues found: {len(issues)}\n')
    current_file = None
    for fpath, lineno, msg, code in issues:
        if fpath != current_file:
            print(f'\n=== {fpath} ===')
            current_file = fpath
        print(f'  Line {lineno:4d}: {msg}')
        if code:
            print(f'            >> {code}')
else:
    print('No deprecated patterns or syntax errors found.')

