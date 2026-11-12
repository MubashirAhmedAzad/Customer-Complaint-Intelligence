from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto('http://localhost:8501/Complaint_Classification', wait_until='networkidle')
    page.wait_for_timeout(2000)

    # Click tab 1 (Batch CSV)
    batch_tab = page.locator('[role="tab"]').nth(1)
    batch_tab.click()
    page.wait_for_timeout(1000)

    # Set file input
    file_input = page.locator('input[type="file"]').first
    file_input.set_input_files(r'C:\Users\mubas\PROJECTS\ML Project\Customer-Complaint-Root-Cause-Classifier-and-RAG-Intelligence-Engine\data\batch_test_complaints_100mb.csv')
    
    # Wait 8 seconds and screenshot
    page.wait_for_timeout(8000)
    page.screenshot(path='scratch/upload_debug.png')
    
    # Print all text on page
    print(page.locator('body').inner_text()[:1000])
    browser.close()

