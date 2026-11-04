import os
import sys
import time
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
RECORDINGS_DIR = ROOT / "recordings"
RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)
TEMP_VIDEO_DIR = RECORDINGS_DIR / "temp_video_100mb"
FINAL_VIDEO_PATH = RECORDINGS_DIR / "customer_complaint_classifier_walkthrough_100mb.webm"
DATASET_PATH = str(ROOT / "data" / "batch_test_complaints_100mb.csv")

PAGE_URLS = {
    "app": "http://localhost:8501/",
    "Dashboard": "http://localhost:8501/Dashboard",
    "Complaint Classification": "http://localhost:8501/Complaint_Classification",
    "Sentiment Analysis": "http://localhost:8501/Sentiment_Analysis",
    "Complaint Clustering": "http://localhost:8501/Complaint_Clustering",
    "Root Cause Analysis": "http://localhost:8501/Root_Cause_Analysis",
    "Trend Analytics": "http://localhost:8501/Trend_Analytics",
    "AI Assistant": "http://localhost:8501/AI_Assistant",
    "Model Evaluation": "http://localhost:8501/Model_Evaluation",
}

if TEMP_VIDEO_DIR.exists():
    shutil.rmtree(TEMP_VIDEO_DIR)
TEMP_VIDEO_DIR.mkdir(parents=True, exist_ok=True)

print(f"Dataset path: {DATASET_PATH}")
print(f"Target video path: {FINAL_VIDEO_PATH}")

def run_recording():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--start-maximized",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--force-dark-mode",
            ]
        )
        
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            record_video_dir=str(TEMP_VIDEO_DIR),
            record_video_size={"width": 1440, "height": 900},
            color_scheme="dark",
        )
        page = context.new_page()

        # Inject glowing cursor styling and visual click effects
        def inject_cursor():
            try:
                page.evaluate("""() => {
                    if (document.getElementById('virtual-cursor')) return;
                    const cursor = document.createElement('div');
                    cursor.id = 'virtual-cursor';
                    cursor.style.position = 'fixed';
                    cursor.style.width = '20px';
                    cursor.style.height = '20px';
                    cursor.style.borderRadius = '50%';
                    cursor.style.backgroundColor = 'rgba(0, 229, 255, 0.75)';
                    cursor.style.border = '2px solid #ffffff';
                    cursor.style.boxShadow = '0 0 14px rgba(0, 229, 255, 0.9), 0 0 4px #000000';
                    cursor.style.pointerEvents = 'none';
                    cursor.style.zIndex = '9999999';
                    cursor.style.transition = 'transform 0.08s ease-out, background-color 0.15s ease';
                    cursor.style.transform = 'translate(-50%, -50%)';
                    cursor.style.left = '720px';
                    cursor.style.top = '450px';
                    document.body.appendChild(cursor);

                    window.updateVirtualCursor = (x, y) => {
                        cursor.style.left = x + 'px';
                        cursor.style.top = y + 'px';
                    };

                    window.clickVirtualCursor = () => {
                        cursor.style.transform = 'translate(-50%, -50%) scale(0.65)';
                        cursor.style.backgroundColor = '#ffab00';
                        const ripple = document.createElement('div');
                        ripple.style.position = 'fixed';
                        ripple.style.borderRadius = '50%';
                        ripple.style.border = '2px solid rgba(255, 171, 0, 0.8)';
                        ripple.style.width = '14px';
                        ripple.style.height = '14px';
                        ripple.style.left = cursor.style.left;
                        ripple.style.top = cursor.style.top;
                        ripple.style.transform = 'translate(-50%, -50%)';
                        ripple.style.pointerEvents = 'none';
                        ripple.style.zIndex = '9999998';
                        ripple.style.transition = 'all 0.4s ease-out';
                        document.body.appendChild(ripple);
                        setTimeout(() => {
                            ripple.style.width = '55px';
                            ripple.style.height = '55px';
                            ripple.style.opacity = '0';
                        }, 10);
                        setTimeout(() => ripple.remove(), 450);
                        setTimeout(() => {
                            cursor.style.transform = 'translate(-50%, -50%) scale(1.0)';
                            cursor.style.backgroundColor = 'rgba(0, 229, 255, 0.75)';
                        }, 180);
                    };
                }""")
            except Exception:
                pass

        curr_x, curr_y = 720, 450

        def glide_to(x, y, steps=10, delay=0.015):
            nonlocal curr_x, curr_y
            for i in range(1, steps + 1):
                nx = curr_x + (x - curr_x) * (i / steps)
                ny = curr_y + (y - curr_y) * (i / steps)
                try:
                    page.evaluate(f"window.updateVirtualCursor({nx}, {ny})")
                except Exception:
                    pass
                time.sleep(delay)
            curr_x, curr_y = x, y

        def human_click(target):
            try:
                if isinstance(target, str):
                    el = page.locator(target).first
                    el.wait_for(state="visible", timeout=12000)
                    box = el.bounding_box()
                    if box:
                        glide_to(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                        try:
                            page.evaluate("window.clickVirtualCursor()")
                        except Exception:
                            pass
                        el.click()
                else:
                    target.wait_for(state="visible", timeout=12000)
                    box = target.bounding_box()
                    if box:
                        glide_to(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                        try:
                            page.evaluate("window.clickVirtualCursor()")
                        except Exception:
                            pass
                        target.click()
            except Exception as e:
                print(f"Warning on click: {e}")
            time.sleep(0.4)

        def smooth_scroll(distance, steps=8, delay=0.15):
            chunk = distance / steps
            for _ in range(steps):
                page.mouse.wheel(0, chunk)
                time.sleep(delay)

        def hold(seconds=3.0):
            intervals = int(seconds / 0.5)
            for _ in range(intervals):
                glide_to(curr_x + 6, curr_y - 4, steps=4, delay=0.02)
                time.sleep(0.2)
                glide_to(curr_x - 6, curr_y + 4, steps=4, delay=0.02)
                time.sleep(0.2)

        def click_sidebar_page(page_name):
            print(f"\n>>> Navigating to sidebar page: {page_name}")
            link = page.locator(f'[data-testid="stSidebarNav"] a:has-text("{page_name}")').first
            if link.is_visible():
                box = link.bounding_box()
                if box:
                    glide_to(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                    try:
                        page.evaluate("window.clickVirtualCursor()")
                    except Exception:
                        pass
                    time.sleep(0.3)
            
            target_url = PAGE_URLS.get(page_name, f"http://localhost:8501/{page_name.replace(' ', '_')}")
            page.goto(target_url, wait_until="domcontentloaded")
            time.sleep(2.0)
            inject_cursor()

        # ==============================================================
        # START NAVIGATION & HUMAN WALKTHROUGH
        # ==============================================================
        print("\nLoading Streamlit home page...")
        page.goto("http://localhost:8501", wait_until="domcontentloaded")
        time.sleep(2.0)
        inject_cursor()

        # --- PAGE 1: app.py (Home) ---
        print("\n--- [Page 1/9] app.py (Home & Architecture Overview) ---")
        glide_to(550, 220)
        time.sleep(0.5)
        smooth_scroll(450, steps=6, delay=0.15)
        smooth_scroll(500, steps=6, delay=0.15)
        hold(3.0)

        # --- PAGE 2: 1_Dashboard.py ---
        print("\n--- [Page 2/9] 1_Dashboard.py (Executive Portfolio Dashboard) ---")
        click_sidebar_page("Dashboard")
        glide_to(350, 180) # KPI cards
        time.sleep(0.5)
        smooth_scroll(450, steps=6, delay=0.15) # Charts row 1
        time.sleep(0.8)
        smooth_scroll(550, steps=6, delay=0.15) # Charts row 2
        time.sleep(0.8)
        smooth_scroll(500, steps=6, delay=0.15) # Records table

        search_box = page.locator('input[aria-label*="Filter complaints"]').first
        if search_box.is_visible():
            human_click(search_box)
            search_box.fill("overdraft")
            time.sleep(1.2)
        hold(3.0)

        # --- PAGE 3: 2_Complaint_Classification.py (WITH 100MB DATASET UPLOAD) ---
        print("\n--- [Page 3/9] 2_Complaint_Classification.py ---")
        click_sidebar_page("Complaint Classification")
        
        # Step 3a: Single Complaint Classification
        print("  Testing Tab 0: Single Complaint Classification...")
        tab_single = page.locator('[role="tab"]').nth(0)
        tab_single.wait_for(state="visible", timeout=25000)
        human_click(tab_single)
        time.sleep(0.5)

        dup_btn = page.locator('button:has-text("Duplicate Charge")').first
        if dup_btn.is_visible():
            human_click(dup_btn)
            time.sleep(0.8)

        classify_btn = page.locator('button:has-text("Classify Narrative")').first
        if classify_btn.is_visible():
            human_click(classify_btn)
            print("  Waiting for single classification results...")
            page.get_by_text("Primary Issue Category").wait_for(state="visible", timeout=20000)
            time.sleep(1.0)
            smooth_scroll(400, steps=6, delay=0.15)
            hold(3.0)

        smooth_scroll(-400, steps=5, delay=0.12)
        time.sleep(0.5)

        # Step 3b: Batch CSV File Processing & 100MB File Upload
        print("  Testing Tab 1: Batch CSV File Processing (100MB Dataset Upload)...")
        tab_batch = page.locator('[role="tab"]').nth(1)
        human_click(tab_batch)
        time.sleep(1.0)

        file_input = page.locator('input[type="file"]').first
        print(f"  Uploading 100MB CSV dataset: {DATASET_PATH}")
        file_input.set_input_files(DATASET_PATH)
        print("  Waiting for Streamlit to parse 100MB dataset (276,000 records)...")
        loaded_el = page.get_by_text("Loaded file with")
        loaded_el.wait_for(state="visible", timeout=60000)
        print("  100MB dataset loaded successfully into session state!")
        time.sleep(1.5)

        # Click Run Bulk Classification button
        bulk_btn = page.locator('button:has-text("Run Bulk Classification")').first
        if bulk_btn.is_visible():
            print("  Clicking Run Bulk Classification button...")
            human_click(bulk_btn)
            print("  Categorizing 276,000 records across hierarchical models...")
            complete_el = page.get_by_text("Bulk classification complete!")
            complete_el.wait_for(state="visible", timeout=90000)
            print("  Bulk classification completed with 100% success!")
            time.sleep(1.5)
            smooth_scroll(500, steps=6, delay=0.15)
            hold(3.5)

        # --- PAGE 4: 3_Sentiment_Analysis.py ---
        print("\n--- [Page 4/9] 3_Sentiment_Analysis.py ---")
        click_sidebar_page("Sentiment Analysis")
        sent_sample = page.locator('button:has-text("Frustrated / Negative")').first
        if sent_sample.is_visible():
            human_click(sent_sample)
            time.sleep(0.5)
        
        analyze_btn = page.locator('button:has-text("Analyze Sentiment")').first
        if analyze_btn.is_visible():
            human_click(analyze_btn)
            time.sleep(1.5)
            smooth_scroll(400, steps=5, delay=0.15)
            smooth_scroll(450, steps=5, delay=0.15)
            hold(3.0)

        # --- PAGE 5: 4_Complaint_Clustering.py ---
        print("\n--- [Page 5/9] 4_Complaint_Clustering.py ---")
        click_sidebar_page("Complaint Clustering")
        glide_to(650, 420, steps=12, delay=0.02)
        time.sleep(0.8)
        glide_to(750, 480, steps=10, delay=0.02)
        time.sleep(0.8)
        smooth_scroll(500, steps=6, delay=0.15)
        time.sleep(0.8)
        smooth_scroll(500, steps=6, delay=0.15)

        cluster_box = page.locator('div[data-baseweb="select"]').first
        if cluster_box.is_visible():
            human_click(cluster_box)
            time.sleep(0.5)
            opt = page.locator('li[role="option"]').nth(2)
            if opt.is_visible():
                human_click(opt)
                time.sleep(1.0)
        smooth_scroll(400, steps=5, delay=0.15)
        hold(3.0)

        # --- PAGE 6: 5_Root_Cause_Analysis.py ---
        print("\n--- [Page 6/9] 5_Root_Cause_Analysis.py ---")
        click_sidebar_page("Root Cause Analysis")
        smooth_scroll(300, steps=5, delay=0.15)
        
        pat_box = page.locator('div[data-baseweb="select"]').first
        if pat_box.is_visible():
            human_click(pat_box)
            time.sleep(0.5)
            pat_opt = page.locator('li[role="option"]').nth(1)
            if pat_opt.is_visible():
                human_click(pat_opt)
                time.sleep(1.0)
        smooth_scroll(500, steps=6, delay=0.15)
        smooth_scroll(450, steps=6, delay=0.15)
        hold(3.0)

        # --- PAGE 7: 6_Trend_Analytics.py ---
        print("\n--- [Page 7/9] 6_Trend_Analytics.py ---")
        click_sidebar_page("Trend Analytics")
        
        trend_tab_count = page.locator('[role="tab"]').count()
        for i in range(trend_tab_count):
            ttab = page.locator('[role="tab"]').nth(i)
            human_click(ttab)
            time.sleep(1.2)
            smooth_scroll(350, steps=5, delay=0.15)
            time.sleep(0.8)
            smooth_scroll(-350, steps=4, delay=0.12)
        hold(3.0)

        # --- PAGE 8: 7_AI_Assistant.py ---
        print("\n--- [Page 8/9] 7_AI_Assistant.py ---")
        click_sidebar_page("AI Assistant")

        print("  Applying retrieval filters in sidebar...")
        comp_select = page.locator('[data-testid="stSidebar"] div[data-baseweb="select"]').first
        if comp_select.is_visible():
            human_click(comp_select)
            time.sleep(0.4)
            c_opt = page.locator('li[role="option"]:has-text("Cedar Ridge Bank")').first
            if c_opt.is_visible():
                human_click(c_opt)
                time.sleep(0.8)

        prompt_btn = page.locator('button:has-text("Credit Card Disputes")').first
        if not prompt_btn.is_visible():
            prompt_btn = page.locator('button:has-text("Fees & Charges")').first
        if prompt_btn.is_visible():
            human_click(prompt_btn)
            print("  Waiting for AI Assistant response generation & citation cards...")
            time.sleep(4.0)
            smooth_scroll(450, steps=6, delay=0.15)
            hold(3.0)

        # --- PAGE 9: 8_Model_Evaluation.py ---
        print("\n--- [Page 9/9] 8_Model_Evaluation.py ---")
        click_sidebar_page("Model Evaluation")

        eval_tab_count = page.locator('[role="tab"]').count()
        for i in range(eval_tab_count):
            etab = page.locator('[role="tab"]').nth(i)
            human_click(etab)
            time.sleep(1.0)
            smooth_scroll(300, steps=4, delay=0.15)
            time.sleep(0.8)
            smooth_scroll(-300, steps=4, delay=0.12)
        hold(3.0)

        print("\nWalkthrough completed across all 9 pages! Finalizing video...")
        context.close()
        browser.close()

    video_files = list(TEMP_VIDEO_DIR.glob("*.webm"))
    if video_files:
        src_video = video_files[0]
        if FINAL_VIDEO_PATH.exists():
            FINAL_VIDEO_PATH.unlink()
        shutil.move(str(src_video), str(FINAL_VIDEO_PATH))
        shutil.rmtree(TEMP_VIDEO_DIR)
        final_size_mb = FINAL_VIDEO_PATH.stat().st_size / (1024 * 1024)
        print(f"\n=======================================================")
        print(f"VIDEO SAVED SUCCESSFULLY!")
        print(f"Destination: {FINAL_VIDEO_PATH}")
        print(f"File Size: {final_size_mb:.2f} MB")
        print(f"=======================================================")
    else:
        print("ERROR: No video file found in temp directory.")

if __name__ == "__main__":
    run_recording()
