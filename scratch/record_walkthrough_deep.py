"""
scratch/record_walkthrough_deep.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Comprehensive Dark Theme Walkthrough Agent:
- Dark Theme (#0e1117)
- Relaxed, smooth human-paced pointer movements (12 steps) & natural typing
- 3-second hold at the top of every page
- Full-page scrolling (top to bottom and back)
- Full feature coverage:
  * Home Portal: custom narrative typing, Analyze button, 3 prediction cards, dropdown template change, re-analyze
  * Dashboard: full scroll, search filter
  * Classification: Quick test button, Classify narrative, probability chart
  * Sentiment: Negative and Positive sample evaluations, gauge & score
  * Clustering: UMAP scatter hover tooltips, keyword table, Cluster 1 selection & 4 verbatim cards, Cluster 2 selection
  * Root Cause: Pattern report 1, Gemini hypothesis & cited evidence
  * Trend Analytics: ALL 4 TABS CLICKED & SCROLLED (Temporal, Product Sunburst, Institutional Benchmarks, Channels & Geography)
  * AI Assistant: Sidebar filters (Company & Product), 3 conversations (2 pills + 1 custom typed query), citation expander
  * Model Evaluation: ALL 4 TABS CLICKED & SCROLLED (Issue, Sub-Issue, Sentiment, Methodological Caveats)
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

def smooth_scroll(page, total_distance, steps=14, step_delay=0.07):
    """Slow, fluid human scroll wheel motion."""
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

def human_click(page, locator, name="element", wait_after=0.5):
    """Slow, deliberate human cursor movement and click."""
    inject_visual_cursor(page)
    try:
        box = locator.bounding_box()
        if box:
            page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=10)
            time.sleep(0.2)
            page.mouse.down()
            time.sleep(0.1)
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
    """Natural typing with visible progression."""
    inject_visual_cursor(page)
    try:
        box = locator.bounding_box()
        if box:
            page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=8)
            time.sleep(0.15)
        locator.click()
        locator.fill("")
        for ch in text:
            locator.type(ch, delay=delay * 1000)
    except Exception:
        pass
    time.sleep(0.3)

def wait_ready(page, max_wait=10):
    """Wait for Streamlit to finish executing without stalling."""
    try:
        page.wait_for_selector("[data-testid='stStatusWidget']", state="hidden", timeout=max_wait * 1000)
    except Exception:
        pass
    time.sleep(0.5)

def nav_to_page(page, link_text, fallback_path=""):
    """Navigate via sidebar link or direct URL."""
    try:
        link = page.locator(f"a:has-text('{link_text}')").first
        if link.is_visible():
            human_click(page, link, f"Sidebar: {link_text}", wait_after=0.4)
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
    print(" [START] SCREEN RECORDING AGENT: COMPREHENSIVE DARK THEME WALKTHROUGH")
    print(f" Target URL: http://localhost:8501")
    print(f" Theme: Dark Mode (Pure #0e1117)")
    print(f" Coverage: All 9 pages + Trend Analytics Tabs + AI Assistant Filters & 3 Qs + Model Eval Tabs")
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
        # Hold 3s, custom narrative typing, Analyze button, prediction cards,
        # template selectbox change, re-analyze, full scroll!
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

        smooth_scroll(page, 450, steps=12)
        time.sleep(0.8)

        # Custom narrative typing in text area
        text_area = page.locator("textarea").first
        if text_area.is_visible():
            print("  -> FUNCTION: Typing custom narrative into Customer Complaint Narrative text area...")
            custom_complaint = (
                "I was charged an unexpected overdraft fee and monthly penalty on my checking account "
                "even though my direct deposit cleared yesterday morning."
            )
            human_type(page, text_area, custom_complaint, delay=0.035)
            time.sleep(0.4)

        analyze_btn = page.locator("button:has-text('Analyze Complaint')").first
        if analyze_btn.is_visible():
            print("  -> FUNCTION: Clicking 'Analyze Complaint'...")
            human_click(page, analyze_btn, "Analyze Button")
            wait_ready(page, max_wait=8)

        print("  -> Scrolling fully to view Issue, Sub-Issue, Sentiment prediction cards & guide...")
        smooth_scroll(page, 550, steps=12)
        time.sleep(2.0)
        smooth_scroll(page, 400, steps=10) # reach bottom
        time.sleep(1.0)
        smooth_scroll(page, -600, steps=12)
        time.sleep(0.6)

        # Template dropdown change
        print("  -> FUNCTION: Choosing pre-filled template from dropdown...")
        selectbox = page.locator("[data-testid='stSelectbox']").first
        if selectbox.is_visible():
            human_click(page, selectbox, "Selectbox")
            time.sleep(0.4)
            opts = page.locator("[role='option']").all()
            if len(opts) > 5:
                human_click(page, opts[5], "Option 5: Unauthorized Account")
            elif len(opts) > 1:
                human_click(page, opts[1], "Option 1")
            time.sleep(0.5)

            if analyze_btn.is_visible():
                print("  -> Re-analyzing with new template...")
                human_click(page, analyze_btn, "Analyze Button 2")
                wait_ready(page, max_wait=6)
                smooth_scroll(page, 450, steps=10)
                time.sleep(1.5)

        smooth_scroll(page, -800, steps=12)
        time.sleep(0.8)


        # -------------------------------------------------------------------
        # 2. Page 1: Executive Dashboard
        # Hold 3s, full scroll, search filter
        # -------------------------------------------------------------------
        print("\n[PAGE 1/8] Executive Dashboard...")
        nav_to_page(page, "Dashboard", "Dashboard")
        print("  -> Holding 3 seconds to review executive summary cards...")
        time.sleep(3.0)

        smooth_scroll(page, 500, steps=12)
        time.sleep(1.0)
        smooth_scroll(page, 500, steps=12)
        time.sleep(1.0)

        search_input = page.locator("input[type='text']").first
        if search_input.is_visible():
            print("  -> Testing complaint search filter...")
            human_type(page, search_input, "unauthorized charge", delay=0.035)
            wait_ready(page, max_wait=4)
            time.sleep(1.2)
            human_type(page, search_input, "", delay=0.02)
            wait_ready(page, max_wait=3)

        smooth_scroll(page, -1000, steps=14)
        time.sleep(0.8)


        # -------------------------------------------------------------------
        # 3. Page 2: Complaint Classification
        # Hold 3s, Quick Test button, Classify narrative, probability chart
        # -------------------------------------------------------------------
        print("\n[PAGE 2/8] Complaint Classification...")
        nav_to_page(page, "Complaint Classification", "Complaint_Classification")
        print("  -> Holding 3 seconds at top...")
        time.sleep(3.0)

        btn_sample = page.locator("button:has-text('Duplicate Charge')").first
        if btn_sample.is_visible():
            print("  -> Testing Quick Test pill: Duplicate Charge...")
            human_click(page, btn_sample, "Sample 1")
            time.sleep(0.4)

        classify_btn = page.locator("button:has-text('Classify Narrative')").first
        if classify_btn.is_visible():
            human_click(page, classify_btn, "Classify")
            wait_ready(page, max_wait=6)

        print("  -> Full scroll through hierarchical predictions & probability charts...")
        smooth_scroll(page, 550, steps=12)
        time.sleep(1.5)
        smooth_scroll(page, 450, steps=10)
        time.sleep(1.0)
        smooth_scroll(page, -1000, steps=14)
        time.sleep(0.8)


        # -------------------------------------------------------------------
        # 4. Page 3: Sentiment Analysis
        # Hold 3s, Frustrated sample, Evaluate, full scroll, Satisfied sample
        # -------------------------------------------------------------------
        print("\n[PAGE 3/8] Sentiment Analysis...")
        nav_to_page(page, "Sentiment Analysis", "Sentiment_Analysis")
        print("  -> Holding 3 seconds at top...")
        time.sleep(3.0)

        btn_neg = page.locator("button:has-text('Frustrated / Negative')").first
        if btn_neg.is_visible():
            human_click(page, btn_neg, "Frustrated sample")
            time.sleep(0.4)

        eval_btn = page.locator("button:has-text('Evaluate Sentiment')").first
        if eval_btn.is_visible():
            human_click(page, eval_btn, "Evaluate button")
            wait_ready(page, max_wait=6)

        print("  -> Full scroll through emotion gauge & confidence metrics...")
        smooth_scroll(page, 500, steps=12)
        time.sleep(1.5)
        smooth_scroll(page, -500, steps=12)
        time.sleep(0.8)


        # -------------------------------------------------------------------
        # 5. Page 4: Complaint Clustering
        # Hold 3s, UMAP scatter hover tooltips, keyword table, Cluster 1
        # selection & verbatim cards, Cluster 2 selection
        # -------------------------------------------------------------------
        print("\n[PAGE 4/8] Complaint Clustering...")
        nav_to_page(page, "Complaint Clustering", "Complaint_Clustering")
        try:
            page.wait_for_selector(".js-plotly-plot", timeout=12000)
        except Exception:
            pass

        print("  -> Holding 3 seconds to review clustering KPIs...")
        time.sleep(3.0)

        smooth_scroll(page, 400, steps=10)
        time.sleep(0.8)

        plotly_canvas = page.locator(".js-plotly-plot").first
        if plotly_canvas.is_visible():
            box = plotly_canvas.bounding_box()
            if box:
                print("  -> FUNCTION: Gliding cursor over UMAP scatter points to display interactive tooltips...")
                page.mouse.move(box["x"] + box["width"] * 0.42, box["y"] + box["height"] * 0.45, steps=8)
                time.sleep(0.6)
                page.mouse.move(box["x"] + box["width"] * 0.62, box["y"] + box["height"] * 0.52, steps=8)
                time.sleep(0.6)
                page.mouse.move(box["x"] + box["width"] * 0.50, box["y"] + box["height"] * 0.32, steps=8)
                time.sleep(0.6)

        print("  -> Scrolling to Discovered Cluster Profiles & Keywords dataframe...")
        smooth_scroll(page, 450, steps=10)
        time.sleep(1.0)

        cluster_sb = page.locator("[data-testid='stSelectbox']").first
        if cluster_sb.is_visible():
            print("  -> FUNCTION: Opening Cluster Inspector dropdown and selecting Cluster 1...")
            human_click(page, cluster_sb, "Cluster Dropdown")
            time.sleep(0.5)
            opts = page.locator("[role='option']").all()
            if len(opts) > 1:
                human_click(page, opts[1], "Option: Cluster 1")
                wait_ready(page, max_wait=5)

        print("  -> Scrolling fully through 4 representative verbatim complaints for Cluster 1...")
        smooth_scroll(page, 500, steps=12)
        time.sleep(1.8)
        smooth_scroll(page, 450, steps=10)
        time.sleep(1.0)

        smooth_scroll(page, -600, steps=12)
        time.sleep(0.6)
        if cluster_sb.is_visible():
            print("  -> FUNCTION: Selecting second Cluster (Cluster 2) from dropdown...")
            human_click(page, cluster_sb, "Cluster Dropdown 2")
            time.sleep(0.5)
            opts = page.locator("[role='option']").all()
            if len(opts) > 2:
                human_click(page, opts[2], "Option: Cluster 2")
                wait_ready(page, max_wait=5)
                smooth_scroll(page, 500, steps=10)
                time.sleep(1.5)

        smooth_scroll(page, -1200, steps=14)
        time.sleep(0.8)


        # -------------------------------------------------------------------
        # 6. Page 5: Root-Cause Analysis
        # Hold 3s, select report 1, Gemini hypothesis & cited evidence
        # -------------------------------------------------------------------
        print("\n[PAGE 5/8] Root-Cause Analysis...")
        nav_to_page(page, "Root-Cause Analysis", "Root_Cause_Analysis")
        print("  -> Holding 3 seconds at top...")
        time.sleep(3.0)

        rca_sel = page.locator("[data-testid='stSelectbox']").first
        if rca_sel.is_visible():
            print("  -> Selecting pattern report #1 from dropdown...")
            human_click(page, rca_sel, "RCA selectbox")
            time.sleep(0.4)
            opts_r = page.locator("[role='option']").all()
            if len(opts_r) > 1:
                human_click(page, opts_r[1], "Report 1")
                wait_ready(page, max_wait=5)

        print("  -> Full scroll through Gemini root-cause hypothesis & verbatim evidence citations...")
        smooth_scroll(page, 550, steps=12)
        time.sleep(1.8)
        smooth_scroll(page, 450, steps=10)
        time.sleep(1.2)
        smooth_scroll(page, -1000, steps=14)
        time.sleep(0.8)


        # -------------------------------------------------------------------
        # 7. Page 6: Trend Analytics
        # Hold 3s, EXPLORE ALL 4 TABS:
        # Tab 1: Temporal Trends & Velocity
        # Tab 2: Product & Taxonomy Breakdown (Sunburst + Category ranking)
        # Tab 3: Institutional Benchmarks (Comparisons bar + Performance scorecard)
        # Tab 4: Channels & Geography (Channel efficiency + Top 10 States bar)
        # -------------------------------------------------------------------
        print("\n[PAGE 6/8] Trend Analytics - Deep Exploration Across All 4 Tabs...")
        nav_to_page(page, "Trend Analytics", "Trend_Analytics")
        print("  -> Holding 3 seconds at top...")
        time.sleep(3.0)

        trend_tabs = page.locator("[role='tab']").all()
        print(f"  -> Found {len(trend_tabs)} analytical tabs on Trend Analytics!")

        # TAB 1: Temporal Trends & Velocity (already active)
        print("  -> [TAB 1/4] Reviewing Temporal Trends & Velocity...")
        smooth_scroll(page, 450, steps=10)
        time.sleep(1.2)
        smooth_scroll(page, 450, steps=10)
        time.sleep(1.2)
        smooth_scroll(page, -900, steps=12)
        time.sleep(0.6)

        # TAB 2: Product & Taxonomy Breakdown
        if len(trend_tabs) > 1:
            print("  -> [TAB 2/4] Clicking 'Product & Taxonomy Breakdown' Tab...")
            human_click(page, trend_tabs[1], "Tab 2: Product & Taxonomy Breakdown")
            time.sleep(1.0)
            print("  -> Scrolling through Hierarchical Product Sunburst & Category Ranking Table...")
            smooth_scroll(page, 450, steps=10)
            time.sleep(1.8)
            smooth_scroll(page, 450, steps=10)
            time.sleep(1.5)
            smooth_scroll(page, -900, steps=12)
            time.sleep(0.6)

        # TAB 3: Institutional Benchmarks
        if len(trend_tabs) > 2:
            print("  -> [TAB 3/4] Clicking 'Institutional Benchmarks' Tab...")
            human_click(page, trend_tabs[2], "Tab 3: Institutional Benchmarks")
            time.sleep(1.0)
            print("  -> Scrolling through Financial Institution Comparisons Bar & Scorecard Table...")
            smooth_scroll(page, 450, steps=10)
            time.sleep(1.8)
            smooth_scroll(page, 450, steps=10)
            time.sleep(1.5)
            smooth_scroll(page, -900, steps=12)
            time.sleep(0.6)

        # TAB 4: Channels & Geography
        if len(trend_tabs) > 3:
            print("  -> [TAB 4/4] Clicking 'Channels & Geography' Tab...")
            human_click(page, trend_tabs[3], "Tab 4: Channels & Geography")
            time.sleep(1.0)
            print("  -> Scrolling through Channel Resolution Efficiency & Top 10 States Charts...")
            smooth_scroll(page, 450, steps=10)
            time.sleep(1.8)
            smooth_scroll(page, 450, steps=10)
            time.sleep(1.5)
            smooth_scroll(page, -900, steps=12)
            time.sleep(0.8)


        # -------------------------------------------------------------------
        # 8. Page 7: AI Assistant (RAG)
        # Hold 3s, USE SIDEBAR FILTERS (Company & Product),
        # 2-3 CONVERSATIONS:
        # Conversation 1: Sample pill 0 (Which product has the most complaints?)
        # Conversation 2: Sample pill 1 (What are common billing dispute issues?)
        # Conversation 3: Type custom question in chat input (Show complaints related to duplicate charges)
        # Expand citation card to read verbatim snippet!
        # -------------------------------------------------------------------
        print("\n[PAGE 7/8] AI Assistant (RAG) - Multi-Turn Conversation & Sidebar Filters...")
        nav_to_page(page, "AI Assistant", "AI_Assistant")
        print("  -> Holding 3 seconds at chat header...")
        time.sleep(3.0)

        # FUNCTION: Use Retrieval Filters in Sidebar
        print("  -> FUNCTION: Interacting with Sidebar Retrieval Filters...")
        sidebar_company = page.locator("[data-testid='stSidebar'] [data-testid='stSelectbox']").first
        if sidebar_company.is_visible():
            human_click(page, sidebar_company, "Sidebar Company Filter")
            time.sleep(0.4)
            opts_c = page.locator("[role='option']").all()
            if len(opts_c) > 2:
                human_click(page, opts_c[2], "Filter: Cedar Ridge Bank")
                wait_ready(page, max_wait=4)

        sidebar_product = page.locator("[data-testid='stSidebar'] [data-testid='stSelectbox']").nth(1)
        if sidebar_product.is_visible():
            human_click(page, sidebar_product, "Sidebar Product Filter")
            time.sleep(0.4)
            opts_p = page.locator("[role='option']").all()
            if len(opts_p) > 1:
                human_click(page, opts_p[1], "Filter: Credit card")
                wait_ready(page, max_wait=4)

        # CONVERSATION 1: Click Sample Question Pill 0
        print("  -> [CONVERSATION 1/3] Asking Question Pill #0: 'Which product has the most complaints?'...")
        pill1 = page.locator("button:has-text('Which product has the most complaints?')").first
        if pill1.is_visible():
            human_click(page, pill1, "Question Pill 1")
            wait_ready(page, max_wait=16)

        print("  -> Reading Gemini answer 1 and citations...")
        smooth_scroll(page, 400, steps=10)
        time.sleep(2.0)
        smooth_scroll(page, -400, steps=10)
        time.sleep(0.6)

        # CONVERSATION 2: Click Sample Question Pill 1
        print("  -> [CONVERSATION 2/3] Asking Question Pill #1: 'What are common billing dispute issues?'...")
        pill2 = page.locator("button:has-text('What are common billing dispute issues?')").first
        if pill2.is_visible():
            human_click(page, pill2, "Question Pill 2")
            wait_ready(page, max_wait=16)

        print("  -> Reading Gemini answer 2...")
        smooth_scroll(page, 450, steps=10)
        time.sleep(2.0)
        smooth_scroll(page, -450, steps=10)
        time.sleep(0.6)

        # CONVERSATION 3: Type custom question into chat input
        print("  -> [CONVERSATION 3/3] Typing custom natural-language question into chat input...")
        chat_input = page.locator("textarea[placeholder*='Ask a question']").first
        if chat_input.is_visible():
            human_type(page, chat_input, "Show complaints related to duplicate charges on credit cards.", delay=0.035)
            time.sleep(0.4)
            page.keyboard.press("Enter")
            print("  -> Awaiting synthesized assistant response with citations...")
            wait_ready(page, max_wait=20)

        # Scroll to inspect response and expand citation
        print("  -> Scrolling to view answer 3 and expanding citation card...")
        smooth_scroll(page, 550, steps=12)
        time.sleep(1.5)
        citation_expander = page.locator("[data-testid='stExpander'] summary").first
        if citation_expander.is_visible():
            human_click(page, citation_expander, "Expand Citation Record")
            time.sleep(1.5)
            smooth_scroll(page, 300, steps=8)
            time.sleep(1.5)

        smooth_scroll(page, -900, steps=14)
        time.sleep(0.8)


        # -------------------------------------------------------------------
        # 9. Page 8: Model Evaluation
        # Hold 3s, EXPLORE ALL 4 TABS:
        # Tab 1: Module 2: Issue Classifier (21 classes)
        # Tab 2: Module 3: Sub-Issue Classifier (38 classes + bar chart)
        # Tab 3: Module 4: Sentiment Model (3 classes)
        # Tab 4: Methodological Caveats (Scientific transparency, synthetic limitations)
        # -------------------------------------------------------------------
        print("\n[PAGE 8/8] Model Evaluation - Deep Exploration Across All 4 Tabs...")
        nav_to_page(page, "Model Evaluation", "Model_Evaluation")
        print("  -> Holding 3 seconds at benchmark scorecard header...")
        time.sleep(3.0)

        eval_tabs = page.locator("[role='tab']").all()
        print(f"  -> Found {len(eval_tabs)} evaluation tabs on Model Evaluation!")

        # TAB 1: Module 2: Issue Classifier
        print("  -> [TAB 1/4] Reviewing Module 2: Issue Classifier Scorecard...")
        smooth_scroll(page, 450, steps=10)
        time.sleep(1.5)
        smooth_scroll(page, -450, steps=10)
        time.sleep(0.6)

        # TAB 2: Module 3: Sub-Issue Classifier
        if len(eval_tabs) > 1:
            print("  -> [TAB 2/4] Clicking 'Module 3: Sub-Issue Classifier' Tab...")
            human_click(page, eval_tabs[1], "Tab 2: Sub-Issue Classifier")
            time.sleep(1.0)
            print("  -> Scrolling through Sub-Issue Benchmark Table & Macro F1 Bar Chart...")
            smooth_scroll(page, 450, steps=10)
            time.sleep(1.8)
            smooth_scroll(page, 450, steps=10)
            time.sleep(1.5)
            smooth_scroll(page, -900, steps=12)
            time.sleep(0.6)

        # TAB 3: Module 4: Sentiment Model
        if len(eval_tabs) > 2:
            print("  -> [TAB 3/4] Clicking 'Module 4: Sentiment Model' Tab...")
            human_click(page, eval_tabs[2], "Tab 3: Sentiment Model")
            time.sleep(1.0)
            print("  -> Reviewing 3-Class Sentiment Scorecard & Performance Metrics...")
            smooth_scroll(page, 450, steps=10)
            time.sleep(1.8)
            smooth_scroll(page, -450, steps=10)
            time.sleep(0.6)

        # TAB 4: Methodological Caveats
        if len(eval_tabs) > 3:
            print("  -> [TAB 4/4] Clicking 'Methodological Caveats' Tab...")
            human_click(page, eval_tabs[3], "Tab 4: Methodological Caveats")
            time.sleep(1.0)
            print("  -> Scrolling fully through Scientific Transparency, GroupSplit, & Hypothesis Guidelines...")
            smooth_scroll(page, 500, steps=12)
            time.sleep(2.0)
            smooth_scroll(page, 500, steps=12)
            time.sleep(1.8)
            smooth_scroll(page, -1000, steps=14)
            time.sleep(0.8)


        # Final showcase returning Home
        print("\n[CONCLUSION] Returning Home for final visual wrap-up...")
        nav_to_page(page, "Home", "")
        time.sleep(2.0)
        smooth_scroll(page, 350, steps=10)
        time.sleep(1.5)
        smooth_scroll(page, -350, steps=10)
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
        final_video_name = RECORDINGS_DIR / "customer_complaint_classifier_complete_walkthrough.webm"
        if latest_video != final_video_name:
            if final_video_name.exists():
                try:
                    final_video_name.unlink()
                except Exception:
                    pass
            latest_video.rename(final_video_name)
        video_size_mb = final_video_name.stat().st_size / (1024 * 1024)
        print("=" * 80)
        print(f" [SUCCESS] COMPREHENSIVE DARK THEME SCREEN RECORDING SAVED!")
        print(f" File: {final_video_name}")
        print(f" Size: {video_size_mb:.2f} MB")
        print(f" Duration: {total_time/60:.2f} minutes ({total_time:.1f}s)")
        print("=" * 80)


if __name__ == "__main__":
    main()

