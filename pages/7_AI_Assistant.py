"""
Streamlit Page: RAG-Based AI Assistant

Interactive natural language assistant for querying complaint records,
combining exact analytical statistics with semantic vector search and citations.
"""

import os
import sys
from pathlib import Path

# Resolve project root and ensure it is on sys.path
_PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import streamlit as st
import pandas as pd

from config.labels import PRODUCT_LABELS, ISSUE_LABELS
from src.rag.rag_pipeline import query_rag_assistant

st.set_page_config(page_title="AI Assistant", page_icon="💬", layout="wide")

st.title("💬 Customer Complaint AI Assistant (RAG)")
st.markdown(
    """
    **Evidence-Backed Natural Language Question Answering**  
    Ask natural-language questions about financial complaint records. The assistant routes
    analytical queries to an **Exact Statistical Engine** (Pandas) and exploratory queries to
    a **Semantic Vector Search Engine** (ChromaDB), citing specific complaint IDs.
    """
)

# Sidebar: Filters & Configuration
st.sidebar.header("🎯 Retrieval Filters")
filter_company = st.sidebar.selectbox("Filter by Company:", ["All Companies", "Blue Mesa Servicing", "Cedar Ridge Bank", "Harborline Credit", "Maple Street Card Services", "Northstar Financial Services", "Pioneer Lending Group", "Riverbend Consumer Finance", "Summit Path Payments"])
filter_product = st.sidebar.selectbox("Filter by Product:", ["All Products"] + PRODUCT_LABELS)

where_filter = {}
if filter_company != "All Companies":
    where_filter["company"] = filter_company
if filter_product != "All Products":
    where_filter["product"] = filter_product
where_filter = where_filter if where_filter else None

# Sidebar: LLM Configuration & Temporary API Key Input
st.sidebar.markdown("---")
st.sidebar.header("⚡ LLM Configuration")
from src.utils.gemini_client import (
    is_gemini_configured,
    get_gemini_api_key,
    validate_gemini_api_key,
)
from config.settings import LLM_MODEL_NAME

api_key_input = st.sidebar.text_input(
    "🔑 Enter Gemini API Key:",
    value=st.session_state.get("custom_gemini_api_key", ""),
    type="password",
    placeholder="AIzaSy...",
    help="Enter your Google Gemini API key to activate live LLM synthesis for this session.",
    key="gemini_key_input_box",
)

cleaned_key = api_key_input.strip()

if not cleaned_key:
    # Key was cleared or left empty -> Disconnect immediately!
    st.session_state["custom_gemini_api_key"] = ""
    st.session_state.pop("_validated_key_tuple", None)
    if "GEMINI_API_KEY" in os.environ:
        os.environ.pop("GEMINI_API_KEY", None)
    st.sidebar.info(
        f"🟡 **Offline Engine Active**\nModel target: `{LLM_MODEL_NAME}`\n\n"
        "Enter your Gemini API key in the box above to activate live AI generation."
    )
else:
    # Key is present -> Validate with Google Gemini
    cached_val = st.session_state.get("_validated_key_tuple")
    if not cached_val or cached_val[0] != cleaned_key:
        with st.sidebar.status("Verifying API key...", expanded=False):
            is_valid, err_msg = validate_gemini_api_key(cleaned_key)
            st.session_state["_validated_key_tuple"] = (cleaned_key, is_valid, err_msg)
    else:
        _, is_valid, err_msg = cached_val

    if is_valid:
        st.session_state["custom_gemini_api_key"] = cleaned_key
        os.environ["GEMINI_API_KEY"] = cleaned_key
        st.sidebar.success(f"🟢 **Google Gemini Connected**\nModel: `{LLM_MODEL_NAME}`")
    else:
        st.session_state["custom_gemini_api_key"] = ""
        if "GEMINI_API_KEY" in os.environ:
            os.environ.pop("GEMINI_API_KEY", None)
        st.sidebar.error(f"🔴 **Invalid API Key**\n{err_msg}")
        st.sidebar.caption("Get a free key at [Google AI Studio](https://aistudio.google.com/app/apikey).")

# Initialize session state chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {
            "role": "assistant",
            "content": (
                "Hello! I am your AI Compliance & Complaint Investigation Assistant.\n\n"
                "You can ask me questions such as:\n"
                "- *Which product has the most complaints?*\n"
                "- *What are common billing dispute issues?*\n"
                "- *Show complaints related to duplicate charges.* \n"
                "- *Which companies have the most unresolved complaints?*"
            ),
            "cited_ids": [],
            "query_type": "System",
        }
    ]

# Sample question pills
st.markdown("##### 💡 Example Questions (Click to Ask):")
sample_queries = [
    "Which product has the most complaints?",
    "What are common billing dispute issues?",
    "Which companies have the most unresolved complaints?",
    "Show complaints related to duplicate charges on credit cards.",
]

cols = st.columns(len(sample_queries))
clicked_query = None
for i, q in enumerate(sample_queries):
    if cols[i].button(q, key=f"sample_{i}", use_container_width=True):
        clicked_query = q

# Render chat history
for msg in st.session_state["chat_history"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("cited_ids"):
            st.caption(f"📑 Cited Records: {', '.join([f'`{cid}`' for cid in msg['cited_ids']])}")

# User input processing
user_input = st.chat_input("Ask a question about customer complaint records...")
active_query = clicked_query if clicked_query else user_input

if active_query:
    # Append user question
    st.session_state["chat_history"].append({"role": "user", "content": active_query})
    with st.chat_message("user"):
        st.markdown(active_query)

    # Process query
    with st.chat_message("assistant"):
        with st.spinner("Retrieving evidence & synthesizing answer..."):
            res = query_rag_assistant(
                query=active_query,
                n_results=4,
                metadata_filter=where_filter,
            )

            # Display query type badge
            qbadge = res.get("query_type", "Search")
            st.caption(f"🔍 Query Router: `{qbadge}`")

            # Display synthesized answer
            st.markdown(res["answer"])

            # Display citations card
            cited = res.get("cited_complaints", [])
            if cited:
                st.markdown("---")
                st.markdown("##### 📑 Retrieved Complaint Citations")
                for r in res.get("source_records", []):
                    cid = r.get("complaint_id")
                    meta = r.get("metadata", {})
                    sim = r.get("similarity_score", 0.0)
                    with st.expander(f"Record [{cid}] — {meta.get('company')} | {meta.get('issue')} ({meta.get('sub_issue')}) — Relevance: {sim:.1%}"):
                        st.write(r.get("document"))

            # Save to chat history
            st.session_state["chat_history"].append({
                "role": "assistant",
                "content": res["answer"],
                "cited_ids": cited,
                "query_type": qbadge,
            })

