import json
import sys
import traceback
from pathlib import Path

# Add project root to sys.path
_PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_PROJECT_ROOT))

nb_path = _PROJECT_ROOT / "notebooks" / "01_data_exploration.ipynb"
with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

global_scope = {}
local_scope = {}

print("Testing notebook cells execution...")
for idx, cell in enumerate(nb.get("cells", [])):
    if cell.get("cell_type") != "code":
        continue
    source = "".join(cell.get("source", []))
    if not source.strip():
        continue
    # Filter out magic commands like %matplotlib inline, etc.
    clean_lines = []
    for line in source.splitlines():
        if line.strip().startswith("%") or line.strip().startswith("!"):
            continue
        clean_lines.append(line)
    code = "\n".join(clean_lines)
    if not code.strip():
        continue

    try:
        exec(code, global_scope, local_scope)
        global_scope.update(local_scope)
        # print(f"Cell {idx} passed")
    except Exception as e:
        print(f"\n==========================================")
        print(f"FAILED AT CELL {idx}")
        print(f"==========================================")
        print("Source:")
        print(source)
        print("\nException:")
        traceback.print_exc()
        break
else:
    print("\nAll cells in 01_data_exploration.ipynb executed successfully!")

