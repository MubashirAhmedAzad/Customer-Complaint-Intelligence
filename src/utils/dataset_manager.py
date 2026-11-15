"""
Dataset Manager Utility Module

Provides a compact dropdown selector to switch between the default training dataset
and any uploaded test dataset across all Streamlit pages, with automatic schema
sanitization to prevent missing-column KeyErrors.
"""

import streamlit as st
import pandas as pd
from typing import Optional, Tuple


def ensure_dataset_schema(df: pd.DataFrame) -> pd.DataFrame:
    """
    Guarantees standard CFPB columns exist on any uploaded/custom test DataFrame
    so that downstream analytics, charts, and KPI calculators run without KeyErrors.
    """
    if df is None or df.empty:
        return df

    clean_df = df.copy()

    # Narrative column
    if "complaint_narrative" not in clean_df.columns:
        narr_candidates = [
            c for c in clean_df.columns
            if ("narrative" in c.lower() or "text" in c.lower() or "desc" in c.lower()) and "id" not in c.lower()
        ] or [c for c in clean_df.columns if "complaint" in c.lower() and "id" not in c.lower()]
        clean_df["complaint_narrative"] = clean_df[narr_candidates[0]] if narr_candidates else "Customer complaint record."

    # ID
    if "complaint_id" not in clean_df.columns:
        clean_df["complaint_id"] = [f"TEST-{i+1:05d}" for i in range(len(clean_df))]

    # Date received
    if "date_received" not in clean_df.columns:
        clean_df["date_received"] = pd.Timestamp.now()
    else:
        clean_df["date_received"] = pd.to_datetime(clean_df["date_received"], errors="coerce").fillna(pd.Timestamp.now())

    # Product & Sub-Product
    if "product" not in clean_df.columns:
        clean_df["product"] = "Credit card"
    if "sub_product" not in clean_df.columns:
        clean_df["sub_product"] = clean_df["product"]

    # Issue & Sub-Issue
    if "issue" not in clean_df.columns:
        if "predicted_issue" in clean_df.columns:
            clean_df["issue"] = clean_df["predicted_issue"]
        else:
            clean_df["issue"] = "Managing an account"

    if "sub_issue" not in clean_df.columns:
        if "predicted_sub_issue" in clean_df.columns:
            clean_df["sub_issue"] = clean_df["predicted_sub_issue"]
        else:
            clean_df["sub_issue"] = "Deposits and withdrawals"

    # Company, Channel, State
    if "company" not in clean_df.columns:
        clean_df["company"] = "Sample Financial Corp"
    if "channel" not in clean_df.columns:
        clean_df["channel"] = "Web"
    if "state" not in clean_df.columns:
        clean_df["state"] = "NY"

    # Sentiment & Resolution
    if "sentiment_label" not in clean_df.columns:
        clean_df["sentiment_label"] = "Negative"
    if "resolution_status" not in clean_df.columns:
        clean_df["resolution_status"] = "In review"

    return clean_df


def render_dataset_dropdown(page_key: str = "main") -> Tuple[Optional[pd.DataFrame], bool, str]:
    """
    Renders a compact dropdown menu inplace of the info banner.
    Allows user to switch between Default Training Dataset and Uploaded Test Dataset.

    Returns:
        (df_or_none, is_test_active, dataset_label)
    """
    # Check if a custom test dataset has been loaded in session
    test_df = st.session_state.get("custom_test_df")
    if test_df is None and "active_custom_df" in st.session_state and st.session_state["active_custom_df"] is not None:
        test_df = st.session_state["active_custom_df"]
        test_df = ensure_dataset_schema(test_df)
        st.session_state["custom_test_df"] = test_df
        st.session_state["custom_test_name"] = st.session_state.get("active_dataset_name", "Uploaded Test Dataset")

    if test_df is not None:
        test_name = st.session_state.get("custom_test_name", "Uploaded Test Dataset")
        opt_test = f"🧪 Test Data: {test_name} ({len(test_df):,} records)"
        opt_default = "📊 Default Training Data (100,000 records)"
        options = [opt_test, opt_default]

        # Initialize or validate selection
        if "selected_dataset_option" not in st.session_state or st.session_state["selected_dataset_option"] not in options:
            st.session_state["selected_dataset_option"] = opt_test

        current_idx = options.index(st.session_state["selected_dataset_option"])

        col_label, col_drop = st.columns([1, 4])
        with col_label:
            st.markdown("<p style='margin-top: 6px; font-weight: 600; color: #a0aec0;'>📂 Active Dataset:</p>", unsafe_allow_html=True)
        with col_drop:
            widget_key = f"dataset_selector_{page_key}"
            if widget_key in st.session_state and st.session_state[widget_key] != st.session_state["selected_dataset_option"]:
                st.session_state[widget_key] = st.session_state["selected_dataset_option"]

            selected = st.selectbox(
                "Active Dataset Selection",
                options=options,
                index=current_idx,
                key=widget_key,
                label_visibility="collapsed",
            )
            if selected != st.session_state["selected_dataset_option"]:
                st.session_state["selected_dataset_option"] = selected
                for pk in ["main", "dashboard", "classification", "sentiment", "clustering", "root_cause", "trend_analytics", "ai_assistant", "model_eval"]:
                    st.session_state[f"dataset_selector_{pk}"] = selected
                st.rerun()

        st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)

        if st.session_state["selected_dataset_option"] == opt_test:
            sanitized_test_df = ensure_dataset_schema(test_df)
            st.session_state["active_custom_df"] = sanitized_test_df
            st.session_state["custom_test_df"] = sanitized_test_df
            st.session_state["active_dataset_name"] = test_name
            return sanitized_test_df, True, test_name
        else:
            # Default dataset selected; temporarily disable active_custom_df for downstream engines
            st.session_state["active_custom_df"] = None
            return None, False, "Default Training Dataset"

    return None, False, "Default Training Dataset"
