import json
from pathlib import Path

nb_path = Path("notebooks/01_data_exploration.ipynb")
with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

print(f"Total cells: {len(nb.get('cells', []))}")
errors_found = 0
for idx, cell in enumerate(nb.get("cells", [])):
    cell_type = cell.get("cell_type")
    source = "".join(cell.get("source", []))
    outputs = cell.get("outputs", [])
    for out in outputs:
        if out.get("output_type") == "error":
            errors_found += 1
            print(f"\n--- ERROR IN CELL {idx} ({cell_type}) ---")
            print("Source:")
            print(source[:200])
            print("Error:")
            print(f"{out.get('ename')}: {out.get('evalue')}")
            print("Traceback:")
            for tb in out.get("traceback", []):
                print(tb)

if errors_found == 0:
    print("No error outputs recorded in notebook cells. Inspecting cell code for potential issues...")

