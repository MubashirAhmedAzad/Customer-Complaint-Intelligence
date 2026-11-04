from playwright.sync_api import sync_playwright

pages = [
    "",
    "Dashboard",
    "Complaint_Classification",
    "Sentiment_Analysis",
    "Complaint_Clustering",
    "Root_Cause_Analysis",
    "Trend_Analytics",
    "AI_Assistant",
    "Model_Evaluation",
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    for p_name in pages:
        url = f"http://localhost:8501/{p_name}"
        page.goto(url, wait_until="networkidle", timeout=20000)
        page.wait_for_timeout(1000)
        
        # Check for error elements
        exceptions = page.locator("[data-testid='stException']").all()
        errors = page.locator("[data-testid='stNotification'][data-test-script='error']").all()
        error_alerts = page.locator(".stAlert:has-text('Error'), .stAlert:has-text('Exception')").all()
        
        print(f"Page: {url} -> Exceptions: {len(exceptions)}, Errors: {len(errors)}, Alerts: {len(error_alerts)}")
        for e in exceptions:
            print("  Exception text:", e.inner_text()[:150])
        for a in error_alerts:
            print("  Alert text:", a.inner_text()[:150])
            
    browser.close()

