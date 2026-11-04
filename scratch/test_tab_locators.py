from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:8501/Complaint_Classification', wait_until='networkidle')
    page.wait_for_timeout(3000)
    
    print("Page title:", page.title())
    tab_locator = page.locator('[role="tab"]')
    print("Role tab count:", tab_locator.count())
    for i in range(tab_locator.count()):
        el = tab_locator.nth(i)
        print(f"Tab {i}: {el.inner_text()!r}")
        
    browser.close()

