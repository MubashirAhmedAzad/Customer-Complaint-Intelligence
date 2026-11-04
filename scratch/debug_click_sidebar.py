import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:8501', wait_until='networkidle')
    page.wait_for_timeout(2000)

    # Click Dashboard
    print("Clicking Dashboard...")
    page.locator('[data-testid="stSidebarNav"] a:has-text("Dashboard")').first.click()
    page.wait_for_timeout(3000)
    print("URL after Dashboard:", page.url)

    # Click Complaint Classification
    print("Clicking Complaint Classification...")
    link = page.locator('[data-testid="stSidebarNav"] a:has-text("Complaint Classification")').first
    print("Link visible:", link.is_visible())
    link.click()
    page.wait_for_timeout(4000)
    print("URL after Complaint Classification:", page.url)
    print("Tabs count:", page.locator('[role="tab"]').count())

    browser.close()

