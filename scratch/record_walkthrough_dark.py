"""
scratch/record_walkthrough_dark.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Automated relaxed human browser agent in DARK THEME:
- Enforces dark theme across the entire application
- Slower, smooth, elegant human mouse glide and natural typing
- Holds 3 seconds on every page for clear visual absorption
- Fully scrolls each page from top to bottom
- Exercises all functions on Home, Clustering, and all analytical pages
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

def smooth_scroll(page, total_distance, steps=14, step_delay=0.08):
    """Slower, smooth, fluid human scroll wheel motion."""
    step = total_distance / steps
    for _ in range(steps):
        page.mouse.wheel(0, step)
        time.sleep(step_delay)

def inject_visual_cursor(page):
    """Inject a visible glowing cyan/amber cursor optimized for dark theme."""
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
        box.style.backgroundColor = 'rgba(56, 189, 248, 0.9)'; /* Electric cyan */
        box.style.border = '2px solid white';
        box.style.boxShadow = '0 0 12px rgba(56, 189, 248, 0.8), 0 0 4px rgba(0,0,0,0.8)';
        box.style.pointerEvents = 'none';
        box.style.zIndex = '9999999';
        box.style.transition = 'transform 0.18s ease-out, background-color 0.2s';
        box.style.transform = 'translate(-50%, -50%)';
        document.body.appendChild(box);

        document.addEventListener('mousemove', e => {
            box.style.left = e.clientX + 'px';
            box.style.top = e.clientY + 'px';
        });
        document.addEventListener('mousedown', () => {
            box.style.backgroundColor = 'rgba(245, 158, 11, 0.95)'; /* Warm amber on click */
            box.style.transform = 'translate(-50%, -50%) scale(1.6)';
        });
        document.addEventListener('mouseup', () => {
            box.style.backgroundColor = 'rgba(56, 189, 248, 0.9)';
            box.style.transform = 'translate(-50%, -50%) scale(1.0)';
        });
    })();
    """
    try:
        page.evaluate(cursor_script)
    except Exception:
        pass

def human_click(page, locator, name="element", wait_after=0.6):
    """Slow, deliberate human cursor movement and click."""
    inject_visual_cursor(page)
    try:
        box = locator.bounding_box()
        if box:
            # Slower, smooth glide with 12 steps
            page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=12)
            time.sleep(0.25)
            page.mouse.down()
            time.sleep(0.12)
            page.mouse.up()
        else:
            locator.click(timeout=4000)
    except Exception:
        try:
            locator.click(timeout=4000)
        except Exception:
            pass
    time.sleep(wait_after)

def human_type(page, locator, text, delay=0.035):
    """Slower, natural typing with visible progression."""
    inject_visual_cursor(page)
    try:
        box = locator.bounding_box()
        if box:
            page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=10)
            time.sleep(0.2)
        locator.click()
        locator.fill("")
        for ch in text:
            locator.type(ch, delay=delay * 1000)
    except Exception:
        pass
    time.sleep(0.4)

def wait_ready(page, max_wait=10):
    """Wait for Streamlit to finish executing without stalling."""
    try:
        page.wait_for_selector("[data-testid='stStatusWidget']", state="hidden", timeout=max_wait * 1000)
    except Exception:
        pass
    time.sleep(0.6)

def nav_to_page(page, link_text, fallback_path=""):
    """Navigate via sidebar link or direct URL."""
    try:
        link = page.locator(f"a:has-text('{link_text}')").first
        if link.is_visible():
            human_click(page, link, f"Sidebar: {link_text}", wait_after=0.5)
            wait_ready(page, max_wait=6)
            inject_visual_cursor(page)
            return
    except Exception:
        pass
    if fallback_path:
        page.goto(f"http://localhost:8501/{fallback_path}", wait_until="networkidle", timeout=20000)
    wait_ready(page, max_wait=6)
    inject_visual_cursor(page)


def main():
    print("=" * 80)
    print(" [START] SCREEN RECORDING AGENT: DARK THEME RELAXED WALKTHROUGH")
    print(f" Target URL: http://localhost:8501")
    print(f" Theme: Dark Mode (Pure #0e1117)")
    print(f" Pace: Deliberate, smooth movements, 3-second hold on every page, full scrolls")
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
            color_scheme="dark",
            viewport={"width": 1440, "height": 900},
            record_video_dir=str(RECORDINGS_DIR),
            record_video_size={"width": 1440, "height": 900}
        )

        page = context.new_page()

        # -------------------------------------------------------------------
        # 1. Page 0: Home Portal (app.py)
        # Hold 3s, type custom narrative in text area, click Analyze,
        # inspect predictions, change template, re-analyze, full scroll!
        # -------------------------------------------------------------------
        print("\n[PAGE 0/8] Home Portal (app.py) - Dark Mode...")
        page.goto("http://localhost:8501", timeout=35000)
        try:
            page.wait_for_selector("textarea", timeout=20000)
        except Exception:
            pass
        inject_visual_cursor(page)

        print("  -> Holding 3 seconds at top for overview absorption...")
        time.sleep(3.0)

        # Smooth scroll down through overview to sandbox
        print("  -> Smooth scrolling through executive KPIs down to sandbox...")
        smooth_scroll(page, 450, steps=14)
        time.sleep(1.0)

        # FUNCTION: Type custom complaint narrative directly into text area
        text_area = page.locator("textarea").first
        if text_area.is_visible():
            print("  -> FUNCTION: Typing custom narrative into text area...")
            custom_complaint = (
                "I was charged an unexpected overdraft fee and monthly penalty on my checking account "
                "even though my direct deposit cleared yesterday morning."
            )
            human_type(page, text_area, custom_complaint, delay=0.035)
            time.sleep(0.5)

        # Click Analyze Complaint
        analyze_btn = page.locator("button:has-text('Analyze Complaint')").first
        if analyze_btn.is_visible():
            print("  -> FUNCTION: Clicking 'Analyze Complaint'...")
            human_click(page, analyze_btn, "Analyze Button")
            wait_ready(page, max_wait=8)

        # Full scroll down to view predictions and entire page
        print("  -> Scrolling fully to view Issue, Sub-Issue, Sentiment cards & navigation guide...")
        smooth_scroll(page, 550, steps=14)
        time.sleep(2.5)
        smooth_scroll(page, 400, steps=12) # reach bottom
        time.sleep(1.5)

        # Scroll back up to sandbox
        smooth_scroll(page, -600, steps=14)
        time.sleep(0.8)

        # FUNCTION: Choose template from dropdown
        print("  -> FUNCTION: Selecting pre-filled complaint template from dropdown...")
        selectbox = page.locator("[data-testid='stSelectbox']").first
        if selectbox.is_visible():
            human_click(page, selectbox, "Selectbox")
            time.sleep(0.5)
            opts = page.locator("[role='option']").all()
            if len(opts) > 5:
                human_click(page, opts[5], "Option 5: Unauthorized Account")
            elif len(opts) > 1:
                human_click(page, opts[1], "Option 1")
            time.sleep(0.6)

            if analyze_btn.is_visible():
                print("  -> Re-analyzing with selected template...")
                human_click(page, analyze_btn, "Analyze Button 2")
                wait_ready(page, max_wait=6)
                smooth_scroll(page, 450, steps=12)
                time.sleep(2.0)

        # Scroll back to top
        smooth_scroll(page, -800, steps=14)
        time.sleep(1.0)


        # -------------------------------------------------------------------
        # 2. Page 1: Executive Dashboard
        # Hold 3s, full scroll down to bottom, search filter, full scroll back
        # -------------------------------------------------------------------
        print("\n[PAGE 1/8] Executive Dashboard...")
        nav_to_page(page, "Dashboard", "Dashboard")
        print("  -> Holding 3 seconds to review executive summary cards...")
        time.sleep(3.0)

        # Full scroll through charts & data
        print("  -> Scrolling fully down through all charts and tables...")
        smooth_scroll(page, 500, steps=14)
        time.sleep(1.2)
        smooth_scroll(page, 500, steps=14)
        time.sleep(1.2)

        # Test search filter
        search_input = page.locator("input[type='text']").first
        if search_input.is_visible():
            print("  -> Testing complaint search filter...")
            human_type(page, search_input, "unauthorized charge", delay=0.035)
            wait_ready(page, max_wait=4)
            time.sleep(1.5)
            human_type(page, search_input, "", delay=0.02)
            wait_ready(page, max_wait=3)

        smooth_scroll(page, -1000, steps=16)
        time.sleep(1.0)


        # -------------------------------------------------------------------
        # 3. Page 2: Complaint Classification
        # Hold 3s, test Quick Test buttons, classify, full scroll
        # -------------------------------------------------------------------
        print("\n[PAGE 2/8] Complaint Classification...")
        nav_to_page(page, "Complaint Classification", "Complaint_Classification")
        print("  -> Holding 3 seconds at top...")
        time.sleep(3.0)

        btn_sample = page.locator("button:has-text('Duplicate Charge')").first
        if btn_sample.is_visible():
            print("  -> Testing Quick Test pill: Duplicate Charge...")
            human_click(page, btn_sample, "Sample 1")
            time.sleep(0.5)

        classify_btn = page.locator("button:has-text('Classify Narrative')").first
        if classify_btn.is_visible():
            print("  -> Clicking 'Classify Narrative'...")
            human_click(page, classify_btn, "Classify")
            wait_ready(page, max_wait=6)

        print("  -> Full scroll through hierarchical predictions & probability charts...")
        smooth_scroll(page, 550, steps=14)
        time.sleep(2.0)
        smooth_scroll(page, 450, steps=12) # Reach bottom
        time.sleep(1.5)
        smooth_scroll(page, -1000, steps=16)
        time.sleep(1.0)


        # -------------------------------------------------------------------
        # 4. Page 3: Sentiment Analysis
        # Hold 3s, negative sample, evaluate, full scroll, positive sample
        # -------------------------------------------------------------------
        print("\n[PAGE 3/8] Sentiment Analysis...")
        nav_to_page(page, "Sentiment Analysis", "Sentiment_Analysis")
        print("  -> Holding 3 seconds at top...")
        time.sleep(3.0)

        btn_neg = page.locator("button:has-text('Frustrated / Negative')").first
        if btn_neg.is_visible():
            human_click(page, btn_neg, "Frustrated sample")
            time.sleep(0.5)

        eval_btn = page.locator("button:has-text('Evaluate Sentiment')").first
        if eval_btn.is_visible():
            human_click(page, eval_btn, "Evaluate button")
            wait_ready(page, max_wait=6)

        print("  -> Full scroll through emotion gauge & confidence metrics...")
        smooth_scroll(page, 500, steps=14)
        time.sleep(2.0)
        smooth_scroll(page, -500, steps=14)
        time.sleep(1.0)


        # -------------------------------------------------------------------
        # 5. Page 4: Complaint Clustering
        # Hold 3s, hover over UMAP points, keyword dataframe, select Cluster 1,
        # inspect 4 verbatim cards, select Cluster 2, inspect updated cards!
        # -------------------------------------------------------------------
        print("\n[PAGE 4/8] Complaint Clustering...")
        nav_to_page(page, "Complaint Clustering", "Complaint_Clustering")
        try:
            page.wait_for_selector(".js-plotly-plot", timeout=12000)
        except Exception:
            pass

        print("  -> Holding 3 seconds to review clustering KPIs...")
        time.sleep(3.0)

        # Smooth scroll to 2D UMAP scatter
        smooth_scroll(page, 400, steps=12)
        time.sleep(1.0)

        # FUNCTION: Hover over multiple UMAP data clusters to show interactive tooltips
        plotly_canvas = page.locator(".js-plotly-plot").first
        if plotly_canvas.is_visible():
            box = plotly_canvas.bounding_box()
            if box:
                print("  -> FUNCTION: Gliding cursor over UMAP scatter points to display interactive tooltips...")
                # Point 1
                page.mouse.move(box["x"] + box["width"] * 0.42, box["y"] + box["height"] * 0.45, steps=10)
                time.sleep(0.7)
                # Point 2
                page.mouse.move(box["x"] + box["width"] * 0.62, box["y"] + box["height"] * 0.52, steps=10)
                time.sleep(0.7)
                # Point 3
                page.mouse.move(box["x"] + box["width"] * 0.50, box["y"] + box["height"] * 0.32, steps=10)
                time.sleep(0.7)

        # Scroll down to topic keywords table
        print("  -> Scrolling to Discovered Cluster Profiles & Keywords dataframe...")
        smooth_scroll(page, 450, steps=12)
        time.sleep(1.2)

        # FUNCTION: Cluster Inspector dropdown selection #1
        cluster_sb = page.locator("[data-testid='stSelectbox']").first
        if cluster_sb.is_visible():
            print("  -> FUNCTION: Opening Cluster Inspector dropdown and selecting Cluster 1...")
            human_click(page, cluster_sb, "Cluster Dropdown")
            time.sleep(0.6)
            opts = page.locator("[role='option']").all()
            if len(opts) > 1:
                human_click(page, opts[1], "Option: Cluster 1")
                wait_ready(page, max_wait=5)

        # Scroll fully through 4 verbatim complaint cards
        print("  -> Scrolling fully through 4 representative verbatim complaints for Cluster 1...")
        smooth_scroll(page, 500, steps=14)
        time.sleep(2.0)
        smooth_scroll(page, 450, steps=12) # reach bottom
        time.sleep(1.5)

        # Scroll back to dropdown and select Cluster 2
        smooth_scroll(page, -600, steps=14)
        time.sleep(0.8)
        if cluster_sb.is_visible():
            print("  -> FUNCTION: Selecting second Cluster (Cluster 2) from dropdown...")
            human_click(page, cluster_sb, "Cluster Dropdown 2")
            time.sleep(0.6)
            opts = page.locator("[role='option']").all()
            if len(opts) > 2:
                human_click(page, opts[2], "Option: Cluster 2")
                wait_ready(page, max_wait=5)
                smooth_scroll(page, 500, steps=12)
                time.sleep(2.0)

        smooth_scroll(page, -1200, steps=16)
        time.sleep(1.0)


        # -------------------------------------------------------------------
        # 6. Page 5: Root-Cause Analysis
        # Hold 3s, select report 1, Gemini hypothesis, cited evidence, full scroll
        # -------------------------------------------------------------------
        print("\n[PAGE 5/8] Root-Cause Analysis...")
        nav_to_page(page, "Root-Cause Analysis", "Root_Cause_Analysis")
        print("  -> Holding 3 seconds at top...")
        time.sleep(3.0)

        # Select report dropdown
        rca_sel = page.locator("[data-testid='stSelectbox']").first
        if rca_sel.is_visible():
            print("  -> Selecting pattern report #1 from dropdown...")
            human_click(page, rca_sel, "RCA selectbox")
            time.sleep(0.5)
            opts_r = page.locator("[role='option']").all()
            if len(opts_r) > 1:
                human_click(page, opts_r[1], "Report 1")
                wait_ready(page, max_wait=5)

        print("  -> Full scroll through Gemini root-cause hypothesis & verbatim evidence citations...")
        smooth_scroll(page, 550, steps=14)
        time.sleep(2.0)
        smooth_scroll(page, 450, steps=12) # bottom
        time.sleep(1.5)
        smooth_scroll(page, -1000, steps=16)
        time.sleep(1.0)


        # -------------------------------------------------------------------
        # 7. Page 6: Trend Analytics
        # Hold 3s, full scroll longitudinal charts, Sunburst hierarchy
        # -------------------------------------------------------------------
        print("\n[PAGE 6/8] Trend Analytics...")
        nav_to_page(page, "Trend Analytics", "Trend_Analytics")
        print("  -> Holding 3 seconds at top...")
        time.sleep(3.0)

        print("  -> Full scroll through longitudinal trajectories, Sunburst, & channel splits...")
        smooth_scroll(page, 550, steps=14)
        time.sleep(1.5)
        smooth_scroll(page, 550, steps=14)
        time.sleep(1.5)
        smooth_scroll(page, 450, steps=12)
        time.sleep(1.5)
        smooth_scroll(page, -1500, steps=18)
        time.sleep(1.0)


        # -------------------------------------------------------------------
        # 8. Page 7: AI Assistant (RAG)
        # Hold 3s, click sample question pill, await Gemini response, full scroll
        # -------------------------------------------------------------------
        print("\n[PAGE 7/8] AI Assistant (RAG)...")
        nav_to_page(page, "AI Assistant", "AI_Assistant")
        print("  -> Holding 3 seconds at top...")
        time.sleep(3.0)

        pill1 = page.locator("button:has-text('Which product has the most complaints?')").first
        if pill1.is_visible():
            print("  -> Clicking sample question pill #0: 'Which product has the most complaints?'...")
            human_click(page, pill1, "Question Pill 1")
            wait_ready(page, max_wait=16)

        print("  -> Full scroll down to read Gemini cited response and metadata...")
        smooth_scroll(page, 450, steps=14)
        time.sleep(2.5)
        smooth_scroll(page, -450, steps=14)
        time.sleep(1.0)


        # -------------------------------------------------------------------
        # 9. Page 8: Model Evaluation
        # Hold 3s, full scroll through all benchmark tables
        # -------------------------------------------------------------------
        print("\n[PAGE 8/8] Model Evaluation...")
        nav_to_page(page, "Model Evaluation", "Model_Evaluation")
        print("  -> Holding 3 seconds at top...")
        time.sleep(3.0)

        print("  -> Full scroll through supervised benchmark comparison scorecards...")
        smooth_scroll(page, 500, steps=14)
        time.sleep(1.5)
        smooth_scroll(page, 500, steps=14)
        time.sleep(1.5)
        smooth_scroll(page, -1000, steps=16)
        time.sleep(1.5)

        # Final showcase returning Home
        print("\n[CONCLUSION] Returning Home for final visual wrap-up...")
        nav_to_page(page, "Home", "")
        time.sleep(2.0)
        smooth_scroll(page, 350, steps=12)
        time.sleep(2.0)
        smooth_scroll(page, -350, steps=12)
        time.sleep(1.0)

        print("\n[FINALIZING] Closing browser context and encoding final video...")
        page.close()
        context.close()
        browser.close()

    total_time = time.perf_counter() - start_total_time
    print(f"\n[DONE] Walkthrough recording completed in {total_time:.1f}s ({total_time/60:.2f} mins)!")

    # Find the latest recorded video and rename it
    video_files = list(RECORDINGS_DIR.glob("*.webm"))
    if video_files:
        latest_video = max(video_files, key=lambda f: f.stat().st_mtime)
        final_video_name = RECORDINGS_DIR / "customer_complaint_classifier_dark_theme_walkthrough.webm"
        if latest_video != final_video_name:
            if final_video_name.exists():
                try:
                    final_video_name.unlink()
                except Exception:
                    pass
            latest_video.rename(final_video_name)
        video_size_mb = final_video_name.stat().st_size / (1024 * 1024)
        print("=" * 80)
        print(f" [SUCCESS] DARK THEME SCREEN RECORDING SAVED!")
        print(f" File: {final_video_name}")
        print(f" Size: {video_size_mb:.2f} MB")
        print(f" Duration: {total_time/60:.2f} minutes ({total_time:.1f}s)")
        print("=" * 80)


if __name__ == "__main__":
    main()

