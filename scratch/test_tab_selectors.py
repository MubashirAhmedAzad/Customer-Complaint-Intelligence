from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:8501/Trend_Analytics', wait_until='networkidle')
    trend_tabs = page.locator("[role='tab']").all()
    print("Trend tabs:", [t.inner_text().strip() for t in trend_tabs])
    
    # Click Tab 2
    if len(trend_tabs) > 1:
        trend_tabs[1].click()
        page.wait_for_timeout(1000)
        print("Clicked Tab 2! Sunburst chart visible:", page.locator(".js-plotly-plot").count())
        
    page.goto('http://localhost:8501/Model_Evaluation', wait_until='networkidle')
    eval_tabs = page.locator("[role='tab']").all()
    print("\nEval tabs:", [t.inner_text().strip() for t in eval_tabs])
    
    browser.close()

