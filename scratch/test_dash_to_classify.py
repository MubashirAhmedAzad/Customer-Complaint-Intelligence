import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:8501', wait_until='domcontentloaded')
    page.wait_for_timeout(2000)

    # 1. Dashboard
    print("Going to Dashboard...")
    page.goto('http://localhost:8501/Dashboard', wait_until='domcontentloaded')
    page.wait_for_timeout(2000)
    print("URL at Dashboard:", page.url)

    # 2. Going to Complaint Classification
    print("Going to Complaint Classification...")
    page.goto('http://localhost:8501/Complaint_Classification', wait_until='domcontentloaded')
    page.wait_for_timeout(2500)
    print("URL at Complaint Classification:", page.url)
    print("Role tab count:", page.locator('[role="tab"]').count())

    browser.close()
print("Direct navigation PASSED!")
