"""Config, requirements, and coverage audit."""
import os, glob

print('=== Config & Environment Check ===')
env_exists = os.path.exists('.env')
env_example = os.path.exists('.env.example')
gitignore_content = open('.gitignore').read() if os.path.exists('.gitignore') else ''
print(f'.env file        : {"EXISTS" if env_exists else "MISSING - create from .env.example"}')
print(f'.env.example     : {"EXISTS" if env_example else "MISSING"}')
print(f'.gitignore venv  : {"OK" if "venv" in gitignore_content else "MISSING - venv not ignored!"}')
print(f'.gitignore .env  : {"OK" if ".env" in gitignore_content else "MISSING - .env not ignored!"}')

print()
print('=== requirements.txt ===')
with open('requirements.txt') as f:
    reqs = [l.strip() for l in f if l.strip() and not l.startswith('#')]
print(f'Total requirements: {len(reqs)}')
for r in reqs:
    print(f'  {r}')

print()
print('=== Test Coverage Check ===')
src_modules = set()
for f in glob.glob('src/**/*.py', recursive=True):
    base = os.path.basename(f)
    if base != '__init__.py':
        src_modules.add(base.replace('.py', ''))

test_modules = set()
for f in glob.glob('tests/test_*.py'):
    with open(f) as tf:
        content = tf.read()
    for m in src_modules:
        if m in content:
            test_modules.add(m)

untested = src_modules - test_modules
print(f'Source modules  : {len(src_modules)}')
print(f'Covered in tests: {len(test_modules)}')
print(f'NOT tested ({len(untested)}):')
for m in sorted(untested):
    print(f'  - {m}')

print()
print('=== Clustering Agent eval() - Security Risk ===')
with open('src/agents/clustering_agent.py') as f:
    lines = f.readlines()
for i, line in enumerate(lines, 1):
    if 'eval(' in line:
        print(f'  Line {i}: {line.strip()}')

