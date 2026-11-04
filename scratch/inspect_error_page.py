import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:8501/Complaint_Classification', wait_until='domcontentloaded')
    
    print("Waiting for page elements to mount...")
    tab = page.locator('[role="tab"]').first
    tab.wait_for(state="visible", timeout=25000)
    print("Mounted! Role tab count:", page.locator('[role="tab"]').count())
    print("Body text snippet:\n", page.locator('body').inner_text()[:400])
    browser.close()
