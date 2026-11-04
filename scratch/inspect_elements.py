from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:8501', wait_until='networkidle')
    print("=== APP.PY ELEMENTS ===")
    print("Text area:", page.locator("textarea").count())
    print("Buttons:", [b.inner_text() for b in page.locator("button").all() if b.inner_text().strip()])
    print("Selectboxes:", page.locator("[data-testid='stSelectbox']").count())
    
    page.goto('http://localhost:8501/Complaint_Clustering', wait_until='networkidle')
    print("\n=== CLUSTERING PAGE ELEMENTS ===")
    print("Plotly charts:", page.locator(".js-plotly-plot").count())
    print("Selectboxes:", page.locator("[data-testid='stSelectbox']").count())
    print("Dataframes:", page.locator("[data-testid='stDataFrame']").count())
    print("Buttons:", [b.inner_text() for b in page.locator("button").all() if b.inner_text().strip()])
    
    # Try opening selectbox
    sb = page.locator("[data-testid='stSelectbox']").first
    sb.click()
    page.wait_for_timeout(1000)
    opts = page.locator("[role='option']").all()
    print("Options in selectbox:", len(opts), [o.inner_text() for o in opts[:3]])
    
    browser.close()

