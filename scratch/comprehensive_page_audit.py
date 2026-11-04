import sys
import traceback
from pathlib import Path
from streamlit.testing.v1 import AppTest

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent

def test_page(rel_path):
    abs_path = str(ROOT_DIR / rel_path)
    print(f"\n--- Testing: {rel_path} ---")
    try:
        at = AppTest.from_file(abs_path, default_timeout=45)
        at.run()
        if at.exception:
            print(f"[FAIL] {len(at.exception)} exceptions on initial render:")
            for exc in at.exception:
                print("  Exception:", exc.value)
            return False, at.exception
        else:
            print(f"[PASS] Rendered successfully with 0 exceptions.")
            return True, []
    except Exception as e:
        print(f"[CRASH] Failed to run AppTest on {rel_path}: {e}")
        traceback.print_exc()
        return False, [str(e)]

pages = [
    "app.py",
    "pages/1_Overview.py",
    "pages/2_EDA_Explorer.py",
    "pages/3_Narrative_Analysis.py",
    "pages/4_Complaint_Clustering.py",
    "pages/5_Root_Cause_Analysis.py",
    "pages/6_Trend_Analytics.py",
    "pages/7_AI_Assistant.py",
    "pages/8_Model_Evaluation.py"
]

results = {}
for p in pages:
    success, excs = test_page(p)
    results[p] = (success, excs)

print("\n================ SUMMARY ================")
all_pass = True
for p, (success, excs) in results.items():
    status = "OK" if success else f"FAIL ({len(excs)} errors)"
    if not success:
        all_pass = False
    print(f"{p:<35}: {status}")

if all_pass:
    print("\nALL 9 STREAMLIT PAGES PASSED INITIAL RENDER WITHOUT ANY ERRORS!")
else:
    print("\nSOME PAGES HAD ERRORS.")
