"""
scratch/record_walkthrough.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Automated browser agent that navigates http://localhost:8501,
simulates realistic human interactions across all 9 pages,
and records a complete 5-minute video walkthrough.
"""

import os
import sys
import time
from pathlib import Path

# Safe UTF-8 output for Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
RECORDINGS_DIR = _PROJECT_ROOT / "recordings"
RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)

from playwright.sync_api import sync_playwright

def human_scroll(page, distance=400, steps=4, delay=0.4):
    """Scroll smoothly like a human reader."""
    step_dist = distance // steps
    for _ in range(steps):
        page.mouse.wheel(0, step_dist)
        time.sleep(delay)

def inject_visual_cursor(page):
    """Inject a visible red mouse pointer so viewer can see user clicks in video."""
    cursor_script = """
    (() => {
        if (window.__custom_cursor_installed) return;
        window.__custom_cursor_installed = true;
        const box = document.createElement('div');
        box.id = 'human-agent-cursor';
        box.style.position = 'fixed';
        box.style.width = '20px';
        box.style.height = '20px';
        box.style.borderRadius = '50%';
        box.style.backgroundColor = 'rgba(255, 68, 68, 0.75)';
        box.style.border = '2px solid white';
        box.style.boxShadow = '0 0 8px rgba(0,0,0,0.4)';
        box.style.pointerEvents = 'none';
        box.style.zIndex = '999999';
        box.style.transition = 'transform 0.15s ease-out, background-color 0.2s';
        box.style.transform = 'translate(-50%, -50%)';
        document.body.appendChild(box);

        document.addEventListener('mousemove', e => {
            box.style.left = e.clientX + 'px';
            box.style.top = e.clientY + 'px';
        });
        document.addEventListener('mousedown', () => {
            box.style.backgroundColor = 'rgba(34, 197, 94, 0.9)';
            box.style.transform = 'translate(-50%, -50%) scale(1.4)';
        });
        document.addEventListener('mouseup', () => {
            box.style.backgroundColor = 'rgba(255, 68, 68, 0.75)';
            box.style.transform = 'translate(-50%, -50%) scale(1.0)';
        });
    })();
    """
    try:
        page.evaluate(cursor_script)
    except Exception:
        pass

def human_click(page, locator_or_element, name="element"):
    """Move mouse to element and click smoothly."""
    inject_visual_cursor(page)
    box = locator_or_element.bounding_box()
    if box:
        # Move smoothly to center of element
        target_x = box["x"] + box["width"] / 2
        target_y = box["y"] + box["height"] / 2
        page.mouse.move(target_x, target_y, steps=10)
        time.sleep(0.3)
        page.mouse.down()
        time.sleep(0.12)
        page.mouse.up()
    else:
        locator_or_element.click()
    time.sleep(0.6)

def human_type(page, locator, text, delay=0.035):
    """Type character-by-character like a human."""
    inject_visual_cursor(page)
    box = locator.bounding_box()
    if box:
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=6)
        time.sleep(0.2)
    locator.click()
    time.sleep(0.3)
    locator.fill("")
    for ch in text:
        locator.type(ch, delay=delay * 1000)
    time.sleep(0.5)

def wait_for_streamlit_ready(page, timeout=30):
    """Wait until Streamlit finishes processing/running."""
    try:
        # Streamlit shows stStatusWidget or running indicator when executing
        page.wait_for_selector("[data-testid='stStatusWidget']", state="hidden", timeout=timeout*1000)
    except Exception:
        pass
    time.sleep(1.0)


def main():
    print("=" * 80)
    print(" [START] SCREEN RECORDING AGENT: 5-MINUTE HUMAN WALKTHROUGH")
    print(f" Target URL: http://localhost:8501")
    print(f" Output Directory: {RECORDINGS_DIR}")
    print("=" * 80)

    start_total_time = time.perf_counter()

    with sync_playwright() as p:
        # Launch Chromium with realistic viewport
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            record_video_dir=str(RECORDINGS_DIR),
            record_video_size={"width": 1440, "height": 900}
        )

        page = context.new_page()

        # -------------------------------------------------------------------
        # 1. Page 0: Home Portal (app.py) (~35 seconds)
        # -------------------------------------------------------------------
        print("\n[SCENE 1/9] Visiting Home Page (app.py)...")
        page.goto("http://localhost:8501", wait_until="networkidle", timeout=45000)
        time.sleep(2)
        inject_visual_cursor(page)

        # Overview reading pause
        print("  -> Viewing executive portfolio header & KPI metric cards...")
        time.sleep(3)
        human_scroll(page, distance=350, steps=5, delay=0.5)
        time.sleep(3)

        # Select a complaint template
        print("  -> Selecting sample narrative template from dropdown...")
        selectbox_container = page.locator("[data-testid='stSelectbox']").first
        if selectbox_container.is_visible():
            human_click(page, selectbox_container, "Selectbox")
            time.sleep(1)
            # Choose second option
            option = page.locator("li[role='option']").nth(1)
            if option.is_visible():
                human_click(page, option, "Option: Duplicate Charge")
            time.sleep(2)

        # Scroll to narrative text area
        human_scroll(page, distance=300, steps=4, delay=0.4)
        time.sleep(2)

        # Click 'Analyze Complaint'
        analyze_btn = page.locator("button:has-text('Analyze Complaint')").first
        if analyze_btn.is_visible():
            print("  -> Clicking 'Analyze Complaint'...")
            human_click(page, analyze_btn, "Analyze Button")
            wait_for_streamlit_ready(page)
            time.sleep(3)

        # Scroll down to inspect predictions & confidence breakdown
        print("  -> Inspecting prediction cards and model confidence scores...")
        human_scroll(page, distance=450, steps=5, delay=0.6)
        time.sleep(4)
        human_scroll(page, distance=-500, steps=4, delay=0.4) # scroll back up
        time.sleep(2)


        # -------------------------------------------------------------------
        # 2. Page 1: Executive Dashboard (~35 seconds)
        # -------------------------------------------------------------------
        print("\n[SCENE 2/9] Navigating to Page 1: Executive Dashboard...")
        dash_link = page.locator("a:has-text('Dashboard')").first
        if dash_link.is_visible():
            human_click(page, dash_link, "Sidebar: Dashboard")
            wait_for_streamlit_ready(page)
            time.sleep(3)
            inject_visual_cursor(page)

            print("  -> Reviewing KPI cards and portfolio charts...")
            time.sleep(3)
            human_scroll(page, distance=400, steps=5, delay=0.6)
            time.sleep(4)
            human_scroll(page, distance=500, steps=5, delay=0.6)
            time.sleep(3)

            # Test search box
            print("  -> Interacting with complaint search filter...")
            search_input = page.locator("input[type='text']").first
            if search_input.is_visible():
                human_type(page, search_input, "unauthorized transaction")
                wait_for_streamlit_ready(page)
                time.sleep(4)
                # Clear search to show full table again
                human_type(page, search_input, "")
                wait_for_streamlit_ready(page)
                time.sleep(2)

            human_scroll(page, distance=-700, steps=4, delay=0.4)
            time.sleep(2)


        # -------------------------------------------------------------------
        # 3. Page 2: Complaint Classification (~35 seconds)
        # -------------------------------------------------------------------
        print("\n[SCENE 3/9] Navigating to Page 2: Complaint Classification...")
        classify_link = page.locator("a:has-text('Complaint Classification')").first
        if classify_link.is_visible():
            human_click(page, classify_link, "Sidebar: Classification")
            wait_for_streamlit_ready(page)
            time.sleep(3)
            inject_visual_cursor(page)

            print("  -> Testing Quick Test sample pills...")
            # Click quick sample button 0 (Duplicate Charge)
            btn_sample1 = page.locator("button:has-text('Duplicate Charge')").first
            if btn_sample1.is_visible():
                human_click(page, btn_sample1, "Quick Sample: Duplicate Charge")
                time.sleep(2)

            # Click 'Classify Narrative'
            classify_btn = page.locator("button:has-text('Classify Narrative')").first
            if classify_btn.is_visible():
                print("  -> Clicking 'Classify Narrative'...")
                human_click(page, classify_btn, "Classify Narrative")
                wait_for_streamlit_ready(page)
                time.sleep(3)

            # Inspect predictions & scroll down to probability distribution
            print("  -> Inspecting hierarchical classification results...")
            human_scroll(page, distance=400, steps=5, delay=0.6)
            time.sleep(4)
            human_scroll(page, distance=400, steps=4, delay=0.5)
            time.sleep(3)

            # Try another sample button: Late Fee Dispute
            btn_sample2 = page.locator("button:has-text('Late Fee Dispute')").first
            if btn_sample2.is_visible():
                print("  -> Testing second sample: 'Late Fee Dispute'...")
                human_scroll(page, distance=-700, steps=4, delay=0.4)
                time.sleep(1)
                human_click(page, btn_sample2, "Quick Sample: Late Fee")
                time.sleep(1.5)
                human_click(page, classify_btn, "Classify Narrative 2")
                wait_for_streamlit_ready(page)
                time.sleep(4)


        # -------------------------------------------------------------------
        # 4. Page 3: Sentiment Analysis (~30 seconds)
        # -------------------------------------------------------------------
        print("\n[SCENE 4/9] Navigating to Page 3: Sentiment Analysis...")
        sentiment_link = page.locator("a:has-text('Sentiment Analysis')").first
        if sentiment_link.is_visible():
            human_click(page, sentiment_link, "Sidebar: Sentiment")
            wait_for_streamlit_ready(page)
            time.sleep(3)
            inject_visual_cursor(page)

            print("  -> Testing Frustrated / Negative sample...")
            btn_neg = page.locator("button:has-text('Frustrated / Negative')").first
            if btn_neg.is_visible():
                human_click(page, btn_neg, "Frustrated / Negative")
                time.sleep(2)

            eval_btn = page.locator("button:has-text('Evaluate Sentiment')").first
            if eval_btn.is_visible():
                human_click(page, eval_btn, "Evaluate Sentiment")
                wait_for_streamlit_ready(page)
                time.sleep(4)

            print("  -> Reviewing emotion score metric & confidence gauge...")
            human_scroll(page, distance=350, steps=4, delay=0.5)
            time.sleep(3)

            # Now test Positive sample
            btn_pos = page.locator("button:has-text('Satisfied / Positive')").first
            if btn_pos.is_visible():
                print("  -> Testing Satisfied / Positive sample...")
                human_scroll(page, distance=-350, steps=3, delay=0.4)
                human_click(page, btn_pos, "Satisfied / Positive")
                time.sleep(1.5)
                human_click(page, eval_btn, "Evaluate Positive Sentiment")
                wait_for_streamlit_ready(page)
                time.sleep(4)


        # -------------------------------------------------------------------
        # 5. Page 4: Complaint Clustering (~35 seconds)
        # -------------------------------------------------------------------
        print("\n[SCENE 5/9] Navigating to Page 4: Complaint Clustering...")
        cluster_link = page.locator("a:has-text('Complaint Clustering')").first
        if cluster_link.is_visible():
            human_click(page, cluster_link, "Sidebar: Clustering")
            wait_for_streamlit_ready(page)
            time.sleep(3)
            inject_visual_cursor(page)

            print("  -> Reviewing UMAP density visualization & theme KPIs...")
            time.sleep(3)
            human_scroll(page, distance=450, steps=5, delay=0.6)
            time.sleep(4)
            human_scroll(page, distance=450, steps=5, delay=0.6)
            time.sleep(4)

            # Deep dive inspector selectbox
            print("  -> Interacting with Cluster Deep Dive dropdown...")
            cluster_select = page.locator("[data-testid='stSelectbox']").first
            if cluster_select.is_visible():
                human_click(page, cluster_select, "Cluster Selectbox")
                time.sleep(1)
                opt2 = page.locator("li[role='option']").nth(2)
                if opt2.is_visible():
                    human_click(page, opt2, "Option: Cluster 2")
                    wait_for_streamlit_ready(page)
                    time.sleep(3)

            # Inspect verbatim complaint cards
            print("  -> Reading verbatim complaint evidence cards...")
            human_scroll(page, distance=350, steps=4, delay=0.5)
            time.sleep(4)


        # -------------------------------------------------------------------
        # 6. Page 5: Root-Cause Analysis (~35 seconds)
        # -------------------------------------------------------------------
        print("\n[SCENE 6/9] Navigating to Page 5: Root-Cause Analysis...")
        rca_link = page.locator("a:has-text('Root-Cause Analysis')").first
        if rca_link.is_visible():
            human_click(page, rca_link, "Sidebar: Root Cause")
            wait_for_streamlit_ready(page)
            time.sleep(3)
            inject_visual_cursor(page)

            print("  -> Examining anomaly spikes and investigation reports...")
            time.sleep(3)
            human_scroll(page, distance=400, steps=5, delay=0.6)
            time.sleep(4)

            # Switch to another investigation report
            report_select = page.locator("[data-testid='stSelectbox']").first
            if report_select.is_visible():
                print("  -> Selecting pattern report #1 from dropdown...")
                human_click(page, report_select, "Report Dropdown")
                time.sleep(1)
                opt1 = page.locator("li[role='option']").nth(1)
                if opt1.is_visible():
                    human_click(page, opt1, "Report Option 1")
                    wait_for_streamlit_ready(page)
                    time.sleep(3)

            # Read Gemini hypothesis & evidence
            print("  -> Reviewing Gemini Root-Cause hypothesis and cited records...")
            human_scroll(page, distance=450, steps=5, delay=0.6)
            time.sleep(5)
            human_scroll(page, distance=-400, steps=3, delay=0.4)
            time.sleep(2)


        # -------------------------------------------------------------------
        # 7. Page 6: Trend Analytics (~30 seconds)
        # -------------------------------------------------------------------
        print("\n[SCENE 7/9] Navigating to Page 6: Trend Analytics...")
        trend_link = page.locator("a:has-text('Trend Analytics')").first
        if trend_link.is_visible():
            human_click(page, trend_link, "Sidebar: Trend Analytics")
            wait_for_streamlit_ready(page)
            time.sleep(3)
            inject_visual_cursor(page)

            print("  -> Exploring longitudinal time-series & product distributions...")
            time.sleep(3)
            human_scroll(page, distance=450, steps=5, delay=0.6)
            time.sleep(4)
            human_scroll(page, distance=500, steps=5, delay=0.6)
            time.sleep(4)
            human_scroll(page, distance=450, steps=5, delay=0.6)
            time.sleep(3)
            human_scroll(page, distance=-800, steps=4, delay=0.4)
            time.sleep(2)


        # -------------------------------------------------------------------
        # 8. Page 7: AI Assistant (RAG) (~40 seconds)
        # -------------------------------------------------------------------
        print("\n[SCENE 8/9] Navigating to Page 7: AI Assistant (RAG)...")
        rag_link = page.locator("a:has-text('AI Assistant')").first
        if rag_link.is_visible():
            human_click(page, rag_link, "Sidebar: AI Assistant")
            wait_for_streamlit_ready(page)
            time.sleep(3)
            inject_visual_cursor(page)

            print("  -> Clicking sample question pill #0: 'Which product has the most complaints?'...")
            q_pill = page.locator("button:has-text('Which product has the most complaints?')").first
            if q_pill.is_visible():
                human_click(page, q_pill, "Question Pill")
                print("  -> Awaiting Gemini RAG synthesis...")
                wait_for_streamlit_ready(page, timeout=40)
                time.sleep(5)

            # Scroll down to read cited response
            print("  -> Reading Gemini assistant answer and cited records...")
            human_scroll(page, distance=350, steps=4, delay=0.5)
            time.sleep(5)

            # Test interactive chat input
            chat_input = page.locator("textarea[placeholder*='Ask a question']").first
            if chat_input.is_visible():
                print("  -> User types custom question into chat input...")
                human_type(page, chat_input, "What are common billing dispute issues?", delay=0.04)
                time.sleep(1)
                page.keyboard.press("Enter")
                print("  -> Awaiting assistant response...")
                wait_for_streamlit_ready(page, timeout=40)
                time.sleep(5)
                human_scroll(page, distance=400, steps=4, delay=0.5)
                time.sleep(4)


        # -------------------------------------------------------------------
        # 9. Page 8: Model Evaluation (~30 seconds)
        # -------------------------------------------------------------------
        print("\n[SCENE 9/9] Navigating to Page 8: Model Evaluation...")
        eval_link = page.locator("a:has-text('Model Evaluation')").first
        if eval_link.is_visible():
            human_click(page, eval_link, "Sidebar: Model Evaluation")
            wait_for_streamlit_ready(page)
            time.sleep(3)
            inject_visual_cursor(page)

            print("  -> Reviewing machine learning benchmark comparison scorecards...")
            time.sleep(3)
            human_scroll(page, distance=400, steps=5, delay=0.6)
            time.sleep(4)
            human_scroll(page, distance=450, steps=5, delay=0.6)
            time.sleep(4)
            human_scroll(page, distance=-500, steps=4, delay=0.4)
            time.sleep(3)

        # Ensure total duration approaches 5 minutes (300s)
        elapsed = time.perf_counter() - start_total_time
        remaining = 300 - elapsed
        if remaining > 0:
            print(f"\n[PACING] Remaining duration to reach 5 minutes: {remaining:.1f}s. Performing closing review on Home...")
            page.goto("http://localhost:8501", wait_until="networkidle")
            time.sleep(3)
            human_scroll(page, distance=350, steps=4, delay=0.6)
            time.sleep(max(1.0, remaining - 5))
            human_scroll(page, distance=-350, steps=4, delay=0.6)
            time.sleep(2)

        # Close page & context to finalize video writing
        print("\n[FINALIZING] Closing browser context to encode and save video recording...")
        video_path = page.video.path()
        page.close()
        context.close()
        browser.close()

    total_time = time.perf_counter() - start_total_time
    print(f"\n[DONE] Walkthrough recording completed in {total_time:.1f}s ({total_time/60:.2f} mins)!")

    # Find the recorded video file and rename it
    video_files = list(RECORDINGS_DIR.glob("*.webm"))
    if video_files:
        # Sort by modification time to get the latest
        latest_video = max(video_files, key=lambda f: f.stat().st_mtime)
        final_video_name = RECORDINGS_DIR / "customer_complaint_classifier_5min_walkthrough.webm"
        if latest_video != final_video_name:
            if final_video_name.exists():
                try:
                    final_video_name.unlink()
                except Exception:
                    pass
            latest_video.rename(final_video_name)
        video_size_mb = final_video_name.stat().st_size / (1024 * 1024)
        print("=" * 80)
        print(f" [SUCCESS] SCREEN RECORDING SAVED SUCCESSFULLY!")
        print(f" File: {final_video_name}")
        print(f" Size: {video_size_mb:.2f} MB")
        print(f" Duration: ~{total_time/60:.1f} minutes")
        print("=" * 80)
    else:
        print("[WARNING] Video file not found in recordings dir.")


if __name__ == "__main__":
    main()

