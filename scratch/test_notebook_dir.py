import json
import os
import sys
import traceback
from pathlib import Path

# Change working dir to notebooks/ as VS Code Jupyter does by default
os.chdir(Path("notebooks").resolve())
sys.path.insert(0, str(Path("..").resolve()))

with open("01_data_exploration.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

global_scope = {}

print("Running cells from notebooks/ directory...")
for idx, cell in enumerate(nb["cells"]):
    if cell["cell_type"] != "code":
        continue
    source = "".join(cell["source"])
    clean_lines = [l for l in source.splitlines() if not l.strip().startswith(("%", "!"))]
    code = "\n".join(clean_lines)
    if not code.strip():
        continue
    # Mock plt.show and fig.show to avoid blocking
    code = code.replace("plt.show()", "pass").replace("fig.show()", "pass")
    try:
        exec(code, global_scope)
    except Exception as e:
        print(f"\nFAILED IN CELL {idx} (running from notebooks/):")
        print("Source:")
        print(source[:300])
        print("Exception:")
        traceback.print_exc()
        break
else:
    print("ALL CELLS PASSED when run from notebooks/ directory!")

