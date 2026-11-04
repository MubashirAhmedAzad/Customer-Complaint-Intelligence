"""
scratch/record_walkthrough_2min.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Automated high-energy browser agent that navigates http://localhost:8501,
deeply exercises all functions in app.py and Complaint Clustering,
continuously scrolls up/down, and records a 2-minute (120s) video walkthrough.
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

def smooth_scroll(page, total_distance, steps=10, step_delay=0.06):
    """Smooth human scroll wheel motion without idle lag."""
    step = total_distance / steps
    for _ in range(steps):
        page.mouse.wheel(0, step)
        time.sleep(step_delay)

def inject_visual_cursor(page):
    """Inject a visible glowing cursor that turns green on click."""
    cursor_script = """
    (() => {
        if (window.__custom_cursor_installed) return;
        window.__custom_cursor_installed = true;
        const box = document.createElement('div');
        box.id = 'human-agent-cursor';
        box.style.position = 'fixed';
        box.style.width = '18px';
        box.style.height = '18px';
        box.style.borderRadius = '50%';
        box.style.backgroundColor = 'rgba(239, 68, 68, 0.9)';
        box.style.border = '2px solid white';
        box.style.boxShadow = '0 0 10px rgba(239, 68, 68, 0.7), 0 2px 4px rgba(0,0,0,0.4)';
        box.style.pointerEvents = 'none';
        box.style.zIndex = '9999999';
        box.style.transition = 'transform 0.12s ease-out, background-color 0.15s';
        box.style.transform = 'translate(-50%, -50%)';
        document.body.appendChild(box);

        document.addEventListener('mousemove', e => {
            box.style.left = e.clientX + 'px';
            box.style.top = e.clientY + 'px';
        });
        document.addEventListener('mousedown', () => {
            box.style.backgroundColor = 'rgba(16, 185, 129, 0.95)';
            box.style.transform = 'translate(-50%, -50%) scale(1.5)';
        });
        document.addEventListener('mouseup', () => {
            box.style.backgroundColor = 'rgba(239, 68, 68, 0.9)';
            box.style.transform = 'translate(-50%, -50%) scale(1.0)';
        });
    })();
    """
    try:
        page.evaluate(cursor_script)
    except Exception:
        pass

def human_click(page, locator, name="element", wait_after=0.3):
    """Move cursor to element and click briskly."""
    inject_visual_cursor(page)
    try:
        box = locator.bounding_box()
        if box:
            page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=5)
            time.sleep(0.1)
            page.mouse.down()
            time.sleep(0.08)
            page.mouse.up()
        else:
            locator.click(timeout=3000)
    except Exception:
        try:
            locator.click(timeout=3000)
        except Exception:
            pass
    time.sleep(wait_after)

def human_type(page, locator, text, delay=0.015):
    """Fast natural typing without awkward pauses."""
    inject_visual_cursor(page)
    try:
        box = locator.bounding_box()
        if box:
            page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=4)
            time.sleep(0.08)
        locator.click()
        locator.fill("")
        for ch in text:
            locator.type(ch, delay=delay * 1000)
    except Exception:
        pass
    time.sleep(0.2)

def wait_ready(page, max_wait=8):
    """Wait for Streamlit to finish executing."""
    try:
        page.wait_for_selector("[data-testid='stStatusWidget']", state="hidden", timeout=max_wait * 1000)
    except Exception:
        pass
    time.sleep(0.4)

def nav_to_page(page, link_text, fallback_path=""):
    """Navigate via sidebar link or direct URL."""
    try:
        link = page.locator(f"a:has-text('{link_text}')").first
        if link.is_visible():
            human_click(page, link, f"Sidebar: {link_text}", wait_after=0.3)
            wait_ready(page, max_wait=5)
            inject_visual_cursor(page)
            return
    except Exception:
        pass
    if fallback_path:
        page.goto(f"http://localhost:8501/{fallback_path}", wait_until="networkidle", timeout=15000)
    wait_ready(page, max_wait=5)
    inject_visual_cursor(page)


def main():
    print("=" * 80)
    print(" [START] SCREEN RECORDING AGENT: 2-MINUTE ACTIVE WALKTHROUGH")
    print(f" Target URL: http://localhost:8501")
    print(f" Target Duration: Exactly ~120s (2.0 minutes)")
    print(f" Focus: Full function utilization on Home and Clustering pages")
    print("=" * 80)

    start_total_time = time.perf_counter()

    with sync_playwright() as p:
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
        # 1. Page 0: Home Portal (app.py) (~22s)
        # Deep test: Type custom narrative in text_area, click Analyze, inspect
        # predictions, then change template selectbox and re-analyze!
        # -------------------------------------------------------------------
        print("\n[SCENE 1/9] Active Test: Home Portal (app.py)...")
        page.goto("http://localhost:8501", timeout=30000)
        try:
            page.wait_for_selector("textarea", timeout=15000)
        except Exception:
            pass
        inject_visual_cursor(page)
        time.sleep(0.5)

        # Scroll down through KPI cards to live sandbox
        print("  -> Scrolling through overview KPIs to Live Sandbox...")
        smooth_scroll(page, 450, steps=8)
        time.sleep(0.4)

        # FUNCTION TEST 1: Type custom narrative directly in text area
        text_area = page.locator("textarea").first
        if text_area.is_visible():
            print("  -> FUNCTION: Typing custom narrative into Customer Complaint Narrative text area...")
            custom_complaint = (
                "I was charged an unexpected overdraft fee and monthly penalty on my checking account "
                "even though my direct deposit cleared yesterday morning."
            )
            human_type(page, text_area, custom_complaint, delay=0.015)
            time.sleep(0.3)

        # Click 'Analyze Complaint'
        analyze_btn = page.locator("button:has-text('Analyze Complaint')").first
        if analyze_btn.is_visible():
            print("  -> FUNCTION: Clicking 'Analyze Complaint' for custom narrative...")
            human_click(page, analyze_btn, "Analyze Button")
            wait_ready(page, max_wait=6)

        # Scroll down through predictions
        print("  -> Scrolling down to inspect Issue, Sub-Issue, and Sentiment cards...")
        smooth_scroll(page, 400, steps=8)
        time.sleep(0.8)

        # FUNCTION TEST 2: Select a pre-filled complaint template from dropdown
        print("  -> FUNCTION: Choosing pre-filled template from dropdown...")
        smooth_scroll(page, -350, steps=7)
        selectbox = page.locator("[data-testid='stSelectbox']").first
        if selectbox.is_visible():
            human_click(page, selectbox, "Selectbox")
            time.sleep(0.3)
            # Choose template 5 (Someone opened unauthorized account...)
            opts = page.locator("[role='option']").all()
            if len(opts) > 5:
                human_click(page, opts[5], "Option 5: Unauthorized Account")
            elif len(opts) > 1:
                human_click(page, opts[1], "Option 1")
            time.sleep(0.4)

            # Re-click Analyze Complaint
            if analyze_btn.is_visible():
                print("  -> Re-analyzing with new template...")
                human_click(page, analyze_btn, "Analyze Button 2")
                wait_ready(page, max_wait=5)
                smooth_scroll(page, 450, steps=8)
                time.sleep(0.6)

        smooth_scroll(page, -700, steps=10)


        # -------------------------------------------------------------------
        # 2. Page 1: Executive Dashboard (~11s)
        # -------------------------------------------------------------------
        print("\n[SCENE 2/9] Active Test: Page 1 Executive Dashboard...")
        nav_to_page(page, "Dashboard", "Dashboard")
        smooth_scroll(page, 400, steps=8)
        time.sleep(0.4)

        # Test search filter
        search_input = page.locator("input[type='text']").first
        if search_input.is_visible():
            print("  -> Testing complaints table search filter...")
            human_type(page, search_input, "unauthorized charge", delay=0.015)
            wait_ready(page, max_wait=3)
            smooth_scroll(page, 350, steps=6)
            time.sleep(0.4)
            human_type(page, search_input, "", delay=0.01)
            wait_ready(page, max_wait=2)

        smooth_scroll(page, -800, steps=9)


        # -------------------------------------------------------------------
        # 3. Page 2: Complaint Classification (~12s)
        # -------------------------------------------------------------------
        print("\n[SCENE 3/9] Active Test: Page 2 Complaint Classification...")
        nav_to_page(page, "Complaint Classification", "Complaint_Classification")

        # Quick Test sample pill
        btn_sample = page.locator("button:has-text('Duplicate Charge')").first
        if btn_sample.is_visible():
            print("  -> Clicking Quick Test pill: Duplicate Charge...")
            human_click(page, btn_sample, "Sample 1")
            time.sleep(0.3)

        classify_btn = page.locator("button:has-text('Classify Narrative')").first
        if classify_btn.is_visible():
            human_click(page, classify_btn, "Classify")
            wait_ready(page, max_wait=5)

        print("  -> Scrolling through hierarchical predictions & probability chart...")
        smooth_scroll(page, 450, steps=8)
        time.sleep(0.6)
        smooth_scroll(page, -450, steps=8)


        # -------------------------------------------------------------------
        # 4. Page 3: Sentiment Analysis (~11s)
        # -------------------------------------------------------------------
        print("\n[SCENE 4/9] Active Test: Page 3 Sentiment Analysis...")
        nav_to_page(page, "Sentiment Analysis", "Sentiment_Analysis")

        btn_neg = page.locator("button:has-text('Frustrated / Negative')").first
        if btn_neg.is_visible():
            human_click(page, btn_neg, "Frustrated sample")

        eval_btn = page.locator("button:has-text('Evaluate Sentiment')").first
        if eval_btn.is_visible():
            human_click(page, eval_btn, "Evaluate button")
            wait_ready(page, max_wait=5)

        print("  -> Scrolling emotion gauge & continuous score...")
        smooth_scroll(page, 400, steps=7)
        time.sleep(0.5)
        smooth_scroll(page, -400, steps=7)


        # -------------------------------------------------------------------
        # 5. Page 4: Complaint Clustering (~24s)
        # Deep test: Hover over 2D UMAP scatter points to show tooltips,
        # sort/inspect dataframe, open Cluster Inspector dropdown, select
        # Cluster 1, inspect verbatim cards, then select Cluster 2!
        # -------------------------------------------------------------------
        print("\n[SCENE 5/9] Active Test: Page 4 Complaint Clustering...")
        nav_to_page(page, "Complaint Clustering", "Complaint_Clustering")
        try:
            page.wait_for_selector(".js-plotly-plot", timeout=10000)
        except Exception:
            pass

        # Scroll to 2D UMAP plot
        print("  -> FUNCTION: Interacting with 2D UMAP scatter plot...")
        smooth_scroll(page, 350, steps=7)
        time.sleep(0.4)

        # Hover over UMAP scatter points to trigger interactive tooltips
        plotly_canvas = page.locator(".js-plotly-plot").first
        if plotly_canvas.is_visible():
            box = plotly_canvas.bounding_box()
            if box:
                # Hover point 1 (center-left)
                page.mouse.move(box["x"] + box["width"] * 0.45, box["y"] + box["height"] * 0.45, steps=5)
                time.sleep(0.4)
                # Hover point 2 (center-right)
                page.mouse.move(box["x"] + box["width"] * 0.65, box["y"] + box["height"] * 0.55, steps=5)
                time.sleep(0.4)
                # Hover point 3 (upper-center)
                page.mouse.move(box["x"] + box["width"] * 0.52, box["y"] + box["height"] * 0.35, steps=5)
                time.sleep(0.4)

        # Scroll to Discovered Clusters Table
        print("  -> Scrolling to Discovered Cluster Profiles & Keywords dataframe...")
        smooth_scroll(page, 450, steps=8)
        time.sleep(0.5)

        # FUNCTION: Cluster Inspector dropdown selection #1
        cluster_sb = page.locator("[data-testid='stSelectbox']").first
        if cluster_sb.is_visible():
            print("  -> FUNCTION: Opening Cluster Inspector dropdown and selecting Cluster 1...")
            human_click(page, cluster_sb, "Cluster Dropdown")
            time.sleep(0.4)
            opts = page.locator("[role='option']").all()
            if len(opts) > 1:
                human_click(page, opts[1], "Option: Cluster 1")
                wait_ready(page, max_wait=4)

        # Scroll through verbatim complaint cards for Cluster 1
        print("  -> Scrolling through 4 representative verbatim complaint cards...")
        smooth_scroll(page, 400, steps=8)
        time.sleep(0.8)

        # FUNCTION: Cluster Inspector dropdown selection #2
        if cluster_sb.is_visible():
            print("  -> FUNCTION: Selecting second Cluster (Cluster 2) from dropdown...")
            smooth_scroll(page, -350, steps=6)
            human_click(page, cluster_sb, "Cluster Dropdown 2")
            time.sleep(0.4)
            opts = page.locator("[role='option']").all()
            if len(opts) > 2:
                human_click(page, opts[2], "Option: Cluster 2")
                wait_ready(page, max_wait=4)
                smooth_scroll(page, 400, steps=7)
                time.sleep(0.8)

        smooth_scroll(page, -900, steps=10)


        # -------------------------------------------------------------------
        # 6. Page 5: Root-Cause Analysis (~11s)
        # -------------------------------------------------------------------
        print("\n[SCENE 6/9] Active Test: Page 5 Root-Cause Analysis...")
        nav_to_page(page, "Root-Cause Analysis", "Root_Cause_Analysis")
        smooth_scroll(page, 350, steps=7)

        # Select report dropdown
        rca_sel = page.locator("[data-testid='stSelectbox']").first
        if rca_sel.is_visible():
            print("  -> Selecting pattern report #1 from dropdown...")
            human_click(page, rca_sel, "RCA selectbox")
            time.sleep(0.3)
            opts_r = page.locator("[role='option']").all()
            if len(opts_r) > 1:
                human_click(page, opts_r[1], "Report 1")
                wait_ready(page, max_wait=4)

        print("  -> Scrolling through Gemini hypothesis & cited evidence...")
        smooth_scroll(page, 450, steps=8)
        time.sleep(0.6)
        smooth_scroll(page, -800, steps=9)


        # -------------------------------------------------------------------
        # 7. Page 6: Trend Analytics (~10s)
        # -------------------------------------------------------------------
        print("\n[SCENE 7/9] Active Test: Page 6 Trend Analytics...")
        nav_to_page(page, "Trend Analytics", "Trend_Analytics")
        print("  -> Scrolling longitudinal charts, Sunburst, & product splits...")
        smooth_scroll(page, 500, steps=8)
        time.sleep(0.4)
        smooth_scroll(page, 500, steps=8)
        time.sleep(0.4)
        smooth_scroll(page, -1000, steps=9)


        # -------------------------------------------------------------------
        # 8. Page 7: AI Assistant (RAG) (~14s)
        # -------------------------------------------------------------------
        print("\n[SCENE 8/9] Active Test: Page 7 AI Assistant (RAG)...")
        nav_to_page(page, "AI Assistant", "AI_Assistant")

        pill1 = page.locator("button:has-text('Which product has the most complaints?')").first
        if pill1.is_visible():
            print("  -> Clicking sample question pill #0: 'Which product has the most complaints?'...")
            human_click(page, pill1, "Question Pill 1")
            wait_ready(page, max_wait=12)

        print("  -> Scrolling down to read Gemini cited response...")
        smooth_scroll(page, 350, steps=7)
        time.sleep(0.8)
        smooth_scroll(page, -350, steps=7)


        # -------------------------------------------------------------------
        # 9. Page 8: Model Evaluation (~9s)
        # -------------------------------------------------------------------
        print("\n[SCENE 9/9] Active Test: Page 8 Model Evaluation...")
        nav_to_page(page, "Model Evaluation", "Model_Evaluation")
        print("  -> Scrolling through benchmark evaluation scorecards across all models...")
        smooth_scroll(page, 450, steps=8)
        time.sleep(0.4)
        smooth_scroll(page, 450, steps=8)
        time.sleep(0.4)
        smooth_scroll(page, -900, steps=9)


        # -------------------------------------------------------------------
        # Precise Pacing for exactly 120s (2 minutes)
        # -------------------------------------------------------------------
        elapsed = time.perf_counter() - start_total_time
        remaining = 120 - elapsed
        if remaining > 0:
            print(f"\n[PACING] Remaining time for exactly 2 minutes: {remaining:.1f}s. Returning Home for final fluid showcase...")
            nav_to_page(page, "Home", "")
            time.sleep(0.5)
            sub_passes = int(remaining // 3)
            for _ in range(max(1, sub_passes)):
                smooth_scroll(page, 300, steps=7)
                time.sleep(0.4)
                smooth_scroll(page, -300, steps=7)
                time.sleep(0.4)
            rem_after = 120 - (time.perf_counter() - start_total_time)
            if rem_after > 0:
                time.sleep(rem_after)

        print("\n[FINALIZING] Closing browser context and finalizing 2-minute video recording...")
        page.close()
        context.close()
        browser.close()

    total_time = time.perf_counter() - start_total_time
    print(f"\n[DONE] Walkthrough recording completed in {total_time:.1f}s ({total_time/60:.2f} mins)!")

    # Find the latest recorded video and rename it
    video_files = list(RECORDINGS_DIR.glob("*.webm"))
    if video_files:
        latest_video = max(video_files, key=lambda f: f.stat().st_mtime)
        final_video_name = RECORDINGS_DIR / "customer_complaint_classifier_2min_walkthrough.webm"
        if latest_video != final_video_name:
            if final_video_name.exists():
                try:
                    final_video_name.unlink()
                except Exception:
                    pass
            latest_video.rename(final_video_name)
        video_size_mb = final_video_name.stat().st_size / (1024 * 1024)
        print("=" * 80)
        print(f" [SUCCESS] 2-MINUTE SCREEN RECORDING SAVED!")
        print(f" File: {final_video_name}")
        print(f" Size: {video_size_mb:.2f} MB")
        print(f" Duration: {total_time/60:.2f} minutes ({total_time:.1f}s)")
        print("=" * 80)


if __name__ == "__main__":
    main()

