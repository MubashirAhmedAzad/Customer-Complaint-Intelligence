import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = str(ROOT / "data" / "batch_test_complaints_100mb.csv")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:8501/Complaint_Classification', wait_until='domcontentloaded')

    print("Waiting for page mount...")
    tab_batch = page.locator('[role="tab"]').nth(1)
    tab_batch.wait_for(state="visible", timeout=25000)
    print("Mounted! Clicking Batch CSV tab...")
    tab_batch.click()
    page.wait_for_timeout(1000)

    print(f"Uploading 100MB dataset ({DATASET_PATH})...")
    file_input = page.locator('input[type="file"]').first
    file_input.set_input_files(DATASET_PATH)

    print("Waiting for file loaded confirmation with page.get_by_text()...")
    loaded_el = page.get_by_text("Loaded file with")
    loaded_el.wait_for(state="visible", timeout=60000)
    print("Found 'Loaded file with' successfully! Text:", loaded_el.inner_text()[:60])

    # Click Run button
    btn = page.locator('button:has-text("Run Bulk Classification")').first
    btn.click()
    print("Clicked Run Bulk Classification! Waiting for completion...")
    complete_el = page.get_by_text("Bulk classification complete!")
    complete_el.wait_for(state="visible", timeout=90000)
    print("SUCCESS: Bulk classification completed!")

    # Check download button
    dl_btn = page.locator('button:has-text("Download Categorized CSV")').first
    print("Download button visible:", dl_btn.is_visible())

    browser.close()
print("All batch tests passed with 100% success!")
