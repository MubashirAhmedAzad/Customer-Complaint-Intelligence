"""
scratch/record_walkthrough_3min.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Automated high-energy browser agent that navigates http://localhost:8501,
actively exercises every feature on every page, continuously scrolls up/down,
and records an active, non-idle 3-minute video walkthrough.
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

def smooth_scroll(page, total_distance, steps=12, step_delay=0.07):
    """Smooth, fluid human scroll wheel motion without idle lag."""
    step = total_distance / steps
    for _ in range(steps):
        page.mouse.wheel(0, step)
        time.sleep(step_delay)

def inject_visual_cursor(page):
    """Inject a visible red/green glowing pointer with click animations."""
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
        box.style.backgroundColor = 'rgba(239, 68, 68, 0.85)';
        box.style.border = '2px solid white';
        box.style.boxShadow = '0 0 10px rgba(239, 68, 68, 0.6), 0 2px 4px rgba(0,0,0,0.4)';
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
            box.style.backgroundColor = 'rgba(239, 68, 68, 0.85)';
            box.style.transform = 'translate(-50%, -50%) scale(1.0)';
        });
    })();
    """
    try:
        page.evaluate(cursor_script)
    except Exception:
        pass

def human_click(page, locator, name="element", wait_after=0.4):
    """Glide cursor to element and click briskly."""
    inject_visual_cursor(page)
    try:
        box = locator.bounding_box()
        if box:
            page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=6)
            time.sleep(0.12)
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

def human_type(page, locator, text, delay=0.02):
    """Fast natural typing without awkward pauses."""
    inject_visual_cursor(page)
    try:
        box = locator.bounding_box()
        if box:
            page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=5)
            time.sleep(0.1)
        locator.click()
        locator.fill("")
        for ch in text:
            locator.type(ch, delay=delay * 1000)
    except Exception:
        pass
    time.sleep(0.3)

def wait_ready(page, max_wait=10):
    """Briefly wait for Streamlit to finish executing without stalling."""
    try:
        page.wait_for_selector("[data-testid='stStatusWidget']", state="hidden", timeout=max_wait * 1000)
    except Exception:
        pass
    time.sleep(0.5)

def nav_to_page(page, link_text, fallback_path=""):
    """Navigate via sidebar or fallback URL."""
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
    print(" [START] SCREEN RECORDING AGENT: ACTIVE 3-MINUTE ACTION WALKTHROUGH")
    print(f" Target URL: http://localhost:8501")
    print(f" Target Duration: ~180s (3.0 minutes) with continuous active scrolling")
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
        # 1. Page 0: Home Portal (app.py) (~19s)
        # -------------------------------------------------------------------
        print("\n[SCENE 1/9] Active Test: Home Portal (app.py)...")
        page.goto("http://localhost:8501", wait_until="networkidle", timeout=20000)
        inject_visual_cursor(page)
        time.sleep(1.0)

        # Active scroll down to see overview
        smooth_scroll(page, 350, steps=8)
        time.sleep(0.5)

        # Select template
        print("  -> Selecting sample template...")
        selectbox = page.locator("[data-testid='stSelectbox']").first
        if selectbox.is_visible():
            human_click(page, selectbox, "Selectbox")
            time.sleep(0.4)
            opt = page.locator("li[role='option']").nth(1)
            if opt.is_visible():
                human_click(page, opt, "Option: Duplicate Charge")
                time.sleep(0.5)

        # Click Analyze
        analyze_btn = page.locator("button:has-text('Analyze Complaint')").first
        if analyze_btn.is_visible():
            print("  -> Clicking Analyze...")
            human_click(page, analyze_btn, "Analyze Button")
            wait_ready(page, max_wait=6)

        # Active scrolling through prediction cards & confidence breakdown
        print("  -> Scrolling through prediction cards and confidence...")
        smooth_scroll(page, 450, steps=10)
        time.sleep(0.8)
        smooth_scroll(page, 350, steps=8)
        time.sleep(0.8)
        smooth_scroll(page, -800, steps=12) # scroll back to top
        time.sleep(0.5)


        # -------------------------------------------------------------------
        # 2. Page 1: Executive Dashboard (~20s)
        # -------------------------------------------------------------------
        print("\n[SCENE 2/9] Active Test: Page 1 Executive Dashboard...")
        nav_to_page(page, "Dashboard", "Dashboard")
        time.sleep(0.8)

        # Scroll down through KPI cards & charts
        print("  -> Scrolling through KPI cards, volume chart, & distributions...")
        smooth_scroll(page, 400, steps=8)
        time.sleep(0.8)
        smooth_scroll(page, 450, steps=8)
        time.sleep(0.8)

        # Type into search filter
        print("  -> Testing complaint table search filter...")
        search_input = page.locator("input[type='text']").first
        if search_input.is_visible():
            human_type(page, search_input, "unauthorized charge", delay=0.02)
            wait_ready(page, max_wait=3)
            time.sleep(0.8)
            smooth_scroll(page, 300, steps=6)
            time.sleep(0.8)
            # Clear search
            human_type(page, search_input, "", delay=0.01)
            wait_ready(page, max_wait=3)

        smooth_scroll(page, -900, steps=12)
        time.sleep(0.5)


        # -------------------------------------------------------------------
        # 3. Page 2: Complaint Classification (~22s)
        # -------------------------------------------------------------------
        print("\n[SCENE 3/9] Active Test: Page 2 Complaint Classification...")
        nav_to_page(page, "Complaint Classification", "Complaint_Classification")
        time.sleep(0.8)

        # Click Sample 1
        print("  -> Testing Quick Test: Duplicate Charge...")
        btn1 = page.locator("button:has-text('Duplicate Charge')").first
        if btn1.is_visible():
            human_click(page, btn1, "Sample 1")
            time.sleep(0.4)

        classify_btn = page.locator("button:has-text('Classify Narrative')").first
        if classify_btn.is_visible():
            human_click(page, classify_btn, "Classify 1")
            wait_ready(page, max_wait=5)

        # Active scroll through predictions and distribution chart
        print("  -> Scrolling through hierarchical predictions and probability distribution...")
        smooth_scroll(page, 450, steps=9)
        time.sleep(0.8)
        smooth_scroll(page, 350, steps=7)
        time.sleep(0.8)
        smooth_scroll(page, -800, steps=10)

        # Click Sample 2
        print("  -> Testing Quick Test: Identity Theft...")
        btn2 = page.locator("button:has-text('Identity Theft')").first
        if btn2.is_visible():
            human_click(page, btn2, "Sample 2")
            time.sleep(0.3)
            if classify_btn.is_visible():
                human_click(page, classify_btn, "Classify 2")
                wait_ready(page, max_wait=5)
                smooth_scroll(page, 400, steps=8)
                time.sleep(0.8)
                smooth_scroll(page, -400, steps=8)


        # -------------------------------------------------------------------
        # 4. Page 3: Sentiment Analysis (~20s)
        # -------------------------------------------------------------------
        print("\n[SCENE 4/9] Active Test: Page 3 Sentiment Analysis...")
        nav_to_page(page, "Sentiment Analysis", "Sentiment_Analysis")
        time.sleep(0.8)

        # Negative sample
        print("  -> Testing Frustrated / Negative sample...")
        btn_neg = page.locator("button:has-text('Frustrated / Negative')").first
        if btn_neg.is_visible():
            human_click(page, btn_neg, "Frustrated sample")
            time.sleep(0.3)

        eval_btn = page.locator("button:has-text('Evaluate Sentiment')").first
        if eval_btn.is_visible():
            human_click(page, eval_btn, "Evaluate button")
            wait_ready(page, max_wait=5)

        print("  -> Scrolling through emotion score gauge & probability breakdown...")
        smooth_scroll(page, 400, steps=8)
        time.sleep(0.8)
        smooth_scroll(page, -400, steps=8)

        # Positive sample
        print("  -> Testing Satisfied / Positive sample...")
        btn_pos = page.locator("button:has-text('Satisfied / Positive')").first
        if btn_pos.is_visible():
            human_click(page, btn_pos, "Satisfied sample")
            time.sleep(0.3)
            if eval_btn.is_visible():
                human_click(page, eval_btn, "Evaluate button 2")
                wait_ready(page, max_wait=5)
                smooth_scroll(page, 350, steps=7)
                time.sleep(0.8)
                smooth_scroll(page, -350, steps=7)


        # -------------------------------------------------------------------
        # 5. Page 4: Complaint Clustering (~20s)
        # -------------------------------------------------------------------
        print("\n[SCENE 5/9] Active Test: Page 4 Complaint Clustering...")
        nav_to_page(page, "Complaint Clustering", "Complaint_Clustering")
        time.sleep(0.8)

        print("  -> Scrolling through 37 discovered themes & UMAP projection...")
        smooth_scroll(page, 450, steps=9)
        time.sleep(0.8)
        smooth_scroll(page, 450, steps=9)
        time.sleep(0.8)

        # Select Cluster from dropdown
        print("  -> Interacting with Cluster deep dive selector...")
        cluster_sel = page.locator("[data-testid='stSelectbox']").first
        if cluster_sel.is_visible():
            human_click(page, cluster_sel, "Cluster selectbox")
            time.sleep(0.3)
            opt_c = page.locator("li[role='option']").nth(2)
            if opt_c.is_visible():
                human_click(page, opt_c, "Cluster 2")
                wait_ready(page, max_wait=4)

        print("  -> Scrolling through representative verbatim complaint cards...")
        smooth_scroll(page, 400, steps=8)
        time.sleep(0.8)
        smooth_scroll(page, -1000, steps=12)
        time.sleep(0.4)


        # -------------------------------------------------------------------
        # 6. Page 5: Root-Cause Analysis (~20s)
        # -------------------------------------------------------------------
        print("\n[SCENE 6/9] Active Test: Page 5 Root-Cause Analysis...")
        nav_to_page(page, "Root-Cause Analysis", "Root_Cause_Analysis")
        time.sleep(0.8)

        print("  -> Scrolling through anomaly spikes & investigation cards...")
        smooth_scroll(page, 350, steps=8)
        time.sleep(0.8)

        # Select report dropdown
        rca_sel = page.locator("[data-testid='stSelectbox']").first
        if rca_sel.is_visible():
            print("  -> Selecting pattern report #1 from dropdown...")
            human_click(page, rca_sel, "RCA selectbox")
            time.sleep(0.3)
            opt_r = page.locator("li[role='option']").nth(1)
            if opt_r.is_visible():
                human_click(page, opt_r, "Report 1")
                wait_ready(page, max_wait=4)

        print("  -> Scrolling through Gemini hypothesis & cited evidence...")
        smooth_scroll(page, 450, steps=9)
        time.sleep(0.8)
        smooth_scroll(page, 450, steps=9)
        time.sleep(0.8)
        smooth_scroll(page, -900, steps=12)
        time.sleep(0.4)


        # -------------------------------------------------------------------
        # 7. Page 6: Trend Analytics (~18s)
        # -------------------------------------------------------------------
        print("\n[SCENE 7/9] Active Test: Page 6 Trend Analytics...")
        nav_to_page(page, "Trend Analytics", "Trend_Analytics")
        time.sleep(0.8)

        print("  -> Actively scrolling longitudinal charts, Sunburst, & product splits...")
        smooth_scroll(page, 450, steps=9)
        time.sleep(0.8)
        smooth_scroll(page, 500, steps=9)
        time.sleep(0.8)
        smooth_scroll(page, 450, steps=8)
        time.sleep(0.8)
        smooth_scroll(page, -1100, steps=12)
        time.sleep(0.4)


        # -------------------------------------------------------------------
        # 8. Page 7: AI Assistant (RAG) (~24s)
        # -------------------------------------------------------------------
        print("\n[SCENE 8/9] Active Test: Page 7 AI Assistant (RAG)...")
        nav_to_page(page, "AI Assistant", "AI_Assistant")
        time.sleep(0.8)

        # Click question pill 1
        print("  -> Clicking sample question pill #0: 'Which product has the most complaints?'...")
        pill1 = page.locator("button:has-text('Which product has the most complaints?')").first
        if pill1.is_visible():
            human_click(page, pill1, "Question Pill 1")
            print("  -> Waiting for Gemini RAG response...")
            wait_ready(page, max_wait=18)

        print("  -> Scrolling down to read Gemini cited answer...")
        smooth_scroll(page, 400, steps=8)
        time.sleep(1.0)

        # Click question pill 2
        print("  -> Clicking sample question pill #1: 'What are common billing dispute issues?'...")
        pill2 = page.locator("button:has-text('What are common billing dispute issues?')").first
        if pill2.is_visible():
            smooth_scroll(page, -350, steps=7)
            human_click(page, pill2, "Question Pill 2")
            print("  -> Waiting for second response...")
            wait_ready(page, max_wait=18)
            smooth_scroll(page, 450, steps=9)
            time.sleep(1.0)


        # -------------------------------------------------------------------
        # 9. Page 8: Model Evaluation (~17s)
        # -------------------------------------------------------------------
        print("\n[SCENE 9/9] Active Test: Page 8 Model Evaluation...")
        nav_to_page(page, "Model Evaluation", "Model_Evaluation")
        time.sleep(0.8)

        print("  -> Scrolling through benchmark evaluation scorecards across all models...")
        smooth_scroll(page, 400, steps=8)
        time.sleep(0.8)
        smooth_scroll(page, 450, steps=9)
        time.sleep(0.8)
        smooth_scroll(page, 400, steps=8)
        time.sleep(0.8)
        smooth_scroll(page, -1000, steps=12)
        time.sleep(0.4)


        # -------------------------------------------------------------------
        # Precise Pacing to achieve ~180s (3 minutes)
        # -------------------------------------------------------------------
        elapsed = time.perf_counter() - start_total_time
        remaining = 180 - elapsed
        if remaining > 0:
            print(f"\n[PACING] Remaining time for exactly 3 minutes: {remaining:.1f}s. Returning Home for final fluid showcase...")
            nav_to_page(page, "Home", "")
            time.sleep(0.8)
            sub_passes = int(remaining // 4)
            for _ in range(max(1, sub_passes)):
                smooth_scroll(page, 350, steps=8)
                time.sleep(0.5)
                smooth_scroll(page, -350, steps=8)
                time.sleep(0.5)
            # Final micro-sleep to align with 180s
            rem_after = 180 - (time.perf_counter() - start_total_time)
            if rem_after > 0:
                time.sleep(rem_after)

        print("\n[FINALIZING] Closing browser context and finalizing 3-minute video recording...")
        page.close()
        context.close()
        browser.close()

    total_time = time.perf_counter() - start_total_time
    print(f"\n[DONE] Walkthrough recording completed in {total_time:.1f}s ({total_time/60:.2f} mins)!")

    # Find the latest recorded video and rename it
    video_files = list(RECORDINGS_DIR.glob("*.webm"))
    if video_files:
        latest_video = max(video_files, key=lambda f: f.stat().st_mtime)
        final_video_name = RECORDINGS_DIR / "customer_complaint_classifier_3min_walkthrough.webm"
        if latest_video != final_video_name:
            if final_video_name.exists():
                try:
                    final_video_name.unlink()
                except Exception:
                    pass
            latest_video.rename(final_video_name)
        video_size_mb = final_video_name.stat().st_size / (1024 * 1024)
        print("=" * 80)
        print(f" [SUCCESS] ACTIVE 3-MINUTE SCREEN RECORDING SAVED!")
        print(f" File: {final_video_name}")
        print(f" Size: {video_size_mb:.2f} MB")
        print(f" Duration: {total_time/60:.2f} minutes ({total_time:.1f}s)")
        print("=" * 80)


if __name__ == "__main__":
    main()

