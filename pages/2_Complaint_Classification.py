"""
Streamlit Page: Complaint Classification (Issue & Sub-Issue)

Real-time hierarchical text classification and batch CSV categorization using
trained TF-IDF + Logistic Regression / Linear SVM models.
"""

import sys
from pathlib import Path

# Resolve project root and ensure it is on sys.path
_PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import streamlit as st
import pandas as pd
import plotly.express as px

from src.classification.predict import (
    predict_issue,
    predict_sub_issue,
    predict_hierarchical,
    predict_issues_batch,
    predict_sub_issues_batch,
)

st.set_page_config(page_title="Complaint Classification", page_icon="🏷️", layout="wide")

st.title("🏷️ Automated Complaint Issue & Sub-Issue Classifier")
st.caption("Two-tier hierarchical NLP classification model mapping customer narratives to 21 Issues and 38 Sub-Issues.")


# ---------------------------------------------------------------------------
# Navigation Tabs
# ---------------------------------------------------------------------------

tab_single, tab_batch = st.tabs(["⚡ Single Complaint Classification", "📁 Batch CSV File Processing"])


# ---------------------------------------------------------------------------
# TAB 1: Single Complaint Classification
# ---------------------------------------------------------------------------

with tab_single:
    st.subheader("Classify Real-Time Narrative")

    # Sample prompt buttons with session state persistence
    st.markdown("##### Quick Test Examples:")
    samples = {
        "Duplicate Charge": "I am concerned because I was charged twice for one transaction on my credit card statement since my last payment.",
        "Account Locked": "My mobile banking app is locked and I cannot access my savings account to pay urgent bills.",
        "Overdraft Fee": "I was assessed an unexpected overdraft fee even though my balance was positive at the time of purchase.",
        "Debt Collection": "Debt collector keeps calling repeatedly at my workplace after I told them I do not owe anything.",
        "Payoff Delay": "I requested a payoff quote for my vehicle lease but customer service has delayed sending the documentation.",
    }

    if "classify_input_text" not in st.session_state:
        st.session_state["classify_input_text"] = ""

    def set_classify_sample(sample_text: str):
        st.session_state["classify_input_text"] = sample_text

    cols = st.columns(len(samples))
    for i, (name, text) in enumerate(samples.items()):
        cols[i].button(
            name,
            key=f"sbtn_{i}",
            on_click=set_classify_sample,
            args=(text,),
            use_container_width=True,
        )

    input_text = st.text_area(
        "Enter customer complaint narrative:",
        key="classify_input_text",
        height=130,
        placeholder="Type or paste unstructured customer complaint text here...",
    )

    if st.button("Classify Narrative", type="primary"):
        if input_text.strip():
            with st.spinner("Classifying complaint..."):
                h_res = predict_hierarchical(input_text)
                issue_detail = predict_issue(input_text)

                st.markdown("---")
                st.subheader("Prediction Results")

                col_res1, col_res2, col_res3 = st.columns([2, 2, 1])

                with col_res1:
                    with st.container(border=True):
                        st.markdown("##### Primary Issue Category (Tier 1)")
                        st.subheader(h_res["issue"])
                        st.progress(max(0.0, min(1.0, float(h_res["issue_confidence"]))))
                        st.caption(f"Model Confidence: {h_res['issue_confidence']:.2%}")

                with col_res2:
                    with st.container(border=True):
                        st.markdown("##### Granular Sub-Issue (Tier 2)")
                        st.subheader(h_res["sub_issue"])
                        st.progress(max(0.0, min(1.0, float(h_res["sub_issue_confidence"]))))
                        st.caption(f"Model Confidence: {h_res['sub_issue_confidence']:.2%}")

                with col_res3:
                    with st.container(border=True):
                        st.markdown("##### Taxonomy Consistency")
                        if h_res["is_hierarchically_consistent"]:
                            st.success("Hierarchically Valid")
                            st.caption("Sub-issue strictly matches parent category.")
                        else:
                            st.warning("Taxonomy Constrained")
                            st.caption(f"Mapped from raw prediction: {h_res['raw_sub_issue']}")

                # Probabilities breakdown chart
                if issue_detail.get("all_probabilities"):
                    probs = issue_detail["all_probabilities"]
                    top_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)[:5]
                    prob_df = pd.DataFrame(top_probs, columns=["Issue", "Probability"])

                    st.markdown("##### Top 5 Issue Probability Distribution")
                    fig_prob = px.bar(
                        prob_df,
                        x="Probability",
                        y="Issue",
                        orientation="h",
                        color="Probability",
                        color_continuous_scale="Blues",
                        range_x=[0, 1.0],
                        height=260,
                    )
                    fig_prob.update_layout(yaxis=dict(autorange="reversed"), margin=dict(l=20, r=20, t=10, b=20))
                    st.plotly_chart(fig_prob)
        else:
            st.warning("Please enter text to classify.")


# ---------------------------------------------------------------------------
# TAB 2: Batch CSV Processing
# ---------------------------------------------------------------------------

with tab_batch:
    st.subheader("Bulk Complaint Classification")
    st.markdown("Upload a CSV file containing an unstructured narrative column to categorize records in bulk.")

    uploaded_file = st.file_uploader("Upload CSV file:", type=["csv"])

    if uploaded_file is not None:
        try:
            batch_df = pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            batch_df = pd.read_csv(uploaded_file, encoding="latin1")
        st.write(f"Loaded file with {len(batch_df):,} rows and columns: {list(batch_df.columns)}")

        # Select narrative column
        narr_candidates = [c for c in batch_df.columns if ("narrative" in c.lower() or "text" in c.lower() or "desc" in c.lower()) and "id" not in c.lower()] or [c for c in batch_df.columns if "complaint" in c.lower() and "id" not in c.lower()]
        default_col = narr_candidates[0] if narr_candidates else batch_df.columns[0]
        text_column = st.selectbox("Select Complaint Text Column:", batch_df.columns, index=batch_df.columns.get_loc(default_col))

        run_clicked = st.button("🚀 Run Bulk Classification", type="primary")

        if run_clicked:
            with st.spinner(f"Categorizing {len(batch_df):,} records..."):
                texts = batch_df[text_column].astype(str).tolist()

                issue_preds = predict_issues_batch(texts)
                sub_preds = predict_sub_issues_batch(texts)

                batch_df["predicted_issue"] = issue_preds["predicted_issue"]
                batch_df["issue_confidence"] = issue_preds["confidence"].round(3)
                batch_df["predicted_sub_issue"] = sub_preds["predicted_sub_issue"]
                batch_df["sub_issue_confidence"] = sub_preds["confidence"].round(3)

                st.session_state["batch_results_df"] = batch_df
                st.session_state["batch_file_name"] = uploaded_file.name

        # Render analytics and results if available in session
        if "batch_results_df" in st.session_state and st.session_state["batch_results_df"] is not None:
            res_df = st.session_state["batch_results_df"]
            fname = st.session_state.get("batch_file_name", "test_dataset.csv")

            st.success(f"✅ Bulk classification complete for {len(res_df):,} records from `{fname}`!")

            # Quick Actions: Set as Active Dataset & Download
            col_apply, col_dl = st.columns([1, 1])
            with col_apply:
                if st.button("📊 Set as Active Application Dataset", use_container_width=True):
                    clean_df = res_df.copy()
                    if "complaint_narrative" not in clean_df.columns and text_column in clean_df.columns:
                        clean_df["complaint_narrative"] = clean_df[text_column]
                    if "issue" not in clean_df.columns and "predicted_issue" in clean_df.columns:
                        clean_df["issue"] = clean_df["predicted_issue"]
                    if "sub_issue" not in clean_df.columns and "predicted_sub_issue" in clean_df.columns:
                        clean_df["sub_issue"] = clean_df["predicted_sub_issue"]
                    if "resolution_status" not in clean_df.columns:
                        clean_df["resolution_status"] = "In review"
                    if "sentiment_label" not in clean_df.columns:
                        clean_df["sentiment_label"] = "Negative"
                    if "company" not in clean_df.columns:
                        clean_df["company"] = "Sample Institution"
                    if "product" not in clean_df.columns:
                        clean_df["product"] = "Credit card"
                    if "date_received" not in clean_df.columns:
                        clean_df["date_received"] = pd.Timestamp.now()
                    if "channel" not in clean_df.columns:
                        clean_df["channel"] = "Web"
                    if "complaint_id" not in clean_df.columns:
                        clean_df["complaint_id"] = [f"TEST-{i+1:05d}" for i in range(len(clean_df))]

                    st.session_state["custom_test_df"] = clean_df
                    st.session_state["custom_test_name"] = fname
                    st.session_state["active_custom_df"] = clean_df
                    st.session_state["active_dataset_name"] = fname
                    st.session_state["selected_dataset_option"] = f"🧪 Test Data: {fname} ({len(clean_df):,} records)"
                    for pk in ["main", "dashboard", "classification", "sentiment", "clustering", "root_cause", "trend_analytics", "ai_assistant", "model_eval"]:
                        st.session_state[f"dataset_selector_{pk}"] = st.session_state["selected_dataset_option"]
                    st.toast("Active dataset updated across all pages!", icon="🚀")
                    st.success("🎉 Test dataset is now active across all application pages! Use the **Active Dataset dropdown** at the top of any page to switch between datasets.")

            with col_dl:
                csv_bytes = res_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download Categorized CSV",
                    data=csv_bytes,
                    file_name="categorized_complaints.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

            # Summary KPI Cards
            st.markdown("---")
            st.markdown("### 📈 Test Dataset Prediction Summary")
            m1, m2, m3, m4 = st.columns(4)
            avg_conf = res_df["issue_confidence"].mean() if "issue_confidence" in res_df.columns else 0.0
            high_conf_pct = (res_df["issue_confidence"] >= 0.75).mean() * 100 if "issue_confidence" in res_df.columns else 0.0
            flagged_cnt = (res_df["issue_confidence"] < 0.60).sum() if "issue_confidence" in res_df.columns else 0

            m1.metric("Total Records", f"{len(res_df):,}")
            m2.metric("Avg Issue Confidence", f"{avg_conf:.1%}")
            m3.metric("High Confidence (≥75%)", f"{high_conf_pct:.1f}%")
            m4.metric("Flagged for Audit (<60%)", f"{flagged_cnt:,}", delta="Needs Review" if flagged_cnt > 0 else "All Confident", delta_color="inverse")

            # Analytical Visualizations
            cg1, cg2 = st.columns(2)
            with cg1:
                st.markdown("##### Top 10 Predicted Issue Categories")
                top_issues = res_df["predicted_issue"].value_counts().head(10).reset_index()
                top_issues.columns = ["Issue", "Count"]
                fig_top_issues = px.bar(
                    top_issues,
                    x="Count",
                    y="Issue",
                    orientation="h",
                    color="Count",
                    color_continuous_scale="Viridis",
                    height=350,
                )
                fig_top_issues.update_layout(yaxis=dict(autorange="reversed"), margin=dict(l=10, r=10, t=20, b=20))
                st.plotly_chart(fig_top_issues, use_container_width=True)

            with cg2:
                st.markdown("##### Prediction Confidence Distribution")
                fig_conf = px.histogram(
                    res_df,
                    x="issue_confidence",
                    nbins=20,
                    color_discrete_sequence=["#3498db"],
                    labels={"issue_confidence": "Confidence Score"},
                    height=350,
                )
                fig_conf.add_vline(x=0.60, line_dash="dash", line_color="red", annotation_text="60% Threshold")
                fig_conf.update_layout(margin=dict(l=10, r=10, t=20, b=20))
                st.plotly_chart(fig_conf, use_container_width=True)

            # Table Browser
            st.markdown("##### 📑 Classified Records Preview")
            st.dataframe(res_df.head(50), use_container_width=True, height=350)

