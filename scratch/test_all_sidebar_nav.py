import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

pages = [
    "app",
    "Dashboard",
    "Complaint Classification",
    "Sentiment Analysis",
    "Complaint Clustering",
    "Root Cause Analysis",
    "Trend Analytics",
    "AI Assistant",
    "Model Evaluation"
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:8501', wait_until='domcontentloaded')
    page.wait_for_timeout(2000)

    for pname in pages:
        print(f"\nClicking sidebar: {pname}...")
        link = page.locator(f'[data-testid="stSidebarNav"] a:has-text("{pname}")').first
        if not link.is_visible():
            link = page.locator(f'a:has-text("{pname}")').first
        link.click()
        page.wait_for_timeout(2000)
        print(f"  -> Current URL: {page.url}, Page title: {page.title()!r}")
        if pname == "Complaint Classification":
            print("  -> Tabs count:", page.locator('[role="tab"]').count())

    browser.close()
print("\nAll 9 pages navigation test PASSED successfully!")

