from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:8501', wait_until='networkidle')
    page.wait_for_timeout(2000)
    print("Initial URL:", page.url)
    
    # List all links in sidebar
    links = page.locator('[data-testid="stSidebarNav"] a').all()
    print(f"Found {len(links)} sidebar links:")
    for l in links:
        print(" -", l.inner_text().strip(), "href:", l.get_attribute("href"))
    
    # Try navigating directly to URL
    page.goto('http://localhost:8501/Complaint_Classification', wait_until='networkidle')
    page.wait_for_timeout(2500)
    print("After direct goto URL:", page.url)
    tabs = page.locator('button[data-baseweb="tab"]').all()
    print("Found tabs after direct goto:", len(tabs))
    for i, t in enumerate(tabs):
        print(f"Tab {i}: text={t.inner_text()!r}")
    
    browser.close()
