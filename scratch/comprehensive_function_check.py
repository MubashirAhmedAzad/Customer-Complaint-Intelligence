import sys
import traceback
from pathlib import Path

# Add project root to sys.path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

print("==================================================")
print("COMPREHENSIVE BACKEND & FUNCTION HEALTH CHECK")
print("==================================================")

errors = []

# 1. Data Pipeline
print("\n[1/7] Testing Data Pipeline (load, clean, validate)...")
try:
    from src.data.load_data import load_complaints
    from src.data.clean_data import clean_complaints
    from src.data.validate_data import validate_dataset

    df_raw = load_complaints()
    print(f"  ✓ load_complaints: {df_raw.shape[0]} rows, {df_raw.shape[1]} columns loaded")
    
    df_clean = clean_complaints(df_raw)
    print(f"  ✓ clean_complaints: {df_clean.shape[0]} rows cleaned")
    
    is_valid = validate_dataset(df_clean)
    print(f"  ✓ validate_dataset: schema verified valid = {is_valid}")
except Exception as e:
    print(f"  ✗ Data pipeline failed: {e}")
    traceback.print_exc()
    errors.append(("Data Pipeline", str(e)))

# 2. Executive Analytics & KPIs
print("\n[2/7] Testing Analytics & KPI Computation...")
try:
    from src.analytics.complaint_statistics import (
        compute_executive_kpis,
        compute_company_benchmarks,
        compute_product_hierarchy,
        compute_state_statistics,
        compute_channel_efficiency,
    )

    kpis = compute_executive_kpis(df_clean)
    print(f"  ✓ compute_executive_kpis: Total={kpis['total_complaints']}, Resolution Rate={kpis['resolution_rate_pct']}%, Negative Sentiment={kpis['negative_sentiment_pct']}%")

    benchmarks = compute_company_benchmarks(df_clean)
    print(f"  ✓ compute_company_benchmarks: {benchmarks.shape[0]} institutions ranked (top: {benchmarks['company'].iloc[0]})")

    hierarchy = compute_product_hierarchy(df_clean)
    print(f"  ✓ compute_product_hierarchy: {hierarchy.shape[0]} product branches computed")

    states = compute_state_statistics(df_clean)
    print(f"  ✓ compute_state_statistics: {states.shape[0]} states computed (top state: {states['state'].iloc[0]})")

    channels = compute_channel_efficiency(df_clean)
    print(f"  ✓ compute_channel_efficiency: {channels.shape[0]} submission channels analyzed")
except Exception as e:
    print(f"  ✗ Analytics failed: {e}")
    traceback.print_exc()
    errors.append(("Analytics", str(e)))

# 3. Hierarchical Classification (Issue + Sub-issue)
print("\n[3/7] Testing Hierarchical Classification Pipeline...")
try:
    from src.classification.predict import predict_hierarchical, predict_issue, predict_sub_issue

    sample_narrative = "I was charged an unexpected monthly maintenance fee of $25 on my checking account without any advance disclosure."
    issue_pred = predict_issue(sample_narrative)
    print(f"  ✓ predict_issue: '{issue_pred['predicted_issue']}' (confidence: {issue_pred['confidence']:.2%})")

    sub_issue_pred = predict_sub_issue(sample_narrative, issue_pred['predicted_issue'])
    print(f"  ✓ predict_sub_issue: '{sub_issue_pred['predicted_sub_issue']}' (confidence: {sub_issue_pred['confidence']:.2%})")

    hierarchical_pred = predict_hierarchical(sample_narrative)
    print(f"  ✓ predict_hierarchical: successfully coordinated issue + sub-issue")
except Exception as e:
    print(f"  ✗ Classification failed: {e}")
    traceback.print_exc()
    errors.append(("Classification", str(e)))

# 4. Sentiment Analysis
print("\n[4/7] Testing Sentiment Analysis Model...")
try:
    from src.sentiment.sentiment_analyzer import predict_sentiment

    sample_sentiment = predict_sentiment(sample_narrative)
    print(f"  ✓ predict_sentiment: '{sample_sentiment['predicted_sentiment']}' (score: {sample_sentiment.get('sentiment_score', 0):.2f}, confidence: {sample_sentiment.get('confidence', 0):.2%})")
except Exception as e:
    print(f"  ✗ Sentiment analysis failed: {e}")
    traceback.print_exc()
    errors.append(("Sentiment Analysis", str(e)))

# 5. Clustering Artifacts & Datasets
print("\n[5/7] Testing Clustering Datasets & Artifacts...")
try:
    import pandas as pd
    cluster_csv = ROOT / "reports" / "sample_clustered_complaints.csv"
    topics_csv = ROOT / "reports" / "cluster_topics.csv"

    if cluster_csv.exists() and topics_csv.exists():
        cdf = pd.read_csv(cluster_csv)
        tdf = pd.read_csv(topics_csv)
        print(f"  ✓ sample_clustered_complaints.csv: {cdf.shape[0]} records, clusters: {cdf['cluster_id'].unique().tolist()}")
        print(f"  ✓ cluster_topics.csv: {tdf.shape[0]} cluster topics with top keywords")
    else:
        raise FileNotFoundError(f"Missing cluster files: cluster_csv exists={cluster_csv.exists()}, topics_csv exists={topics_csv.exists()}")
except Exception as e:
    print(f"  ✗ Clustering failed: {e}")
    traceback.print_exc()
    errors.append(("Clustering", str(e)))

# 6. RAG & Vector Store (ChromaDB + Where Filters)
print("\n[6/7] Testing RAG Vector Store & ChromaDB Multi-Filter Queries...")
try:
    from src.rag.vector_store import search_vector_store

    # Test 1: plain search
    res1 = search_vector_store("disputed unauthorized charge", n_results=3)
    print(f"  ✓ search_vector_store (unfiltered): returned {len(res1)} matches")

    # Test 2: single-attribute filter
    res2 = search_vector_store("checking account overdraft", n_results=3, where_filter={"product": "Checking or savings account"})
    print(f"  ✓ search_vector_store (single filter): returned {len(res2)} matches")

    # Test 3: multi-attribute filter (The exact fix we applied!)
    res3 = search_vector_store("late fee interest rate", n_results=3, where_filter={"company": "Cedar Ridge Bank", "product": "Credit card"})
    print(f"  ✓ search_vector_store (multi filter $and): returned {len(res3)} matches with zero errors")
except Exception as e:
    print(f"  ✗ Vector Store failed: {e}")
    traceback.print_exc()
    errors.append(("Vector Store", str(e)))

# 7. Model Evaluation Scorecards
print("\n[7/7] Testing Model Evaluation Data...")
try:
    # Ensure classification & sentiment models load without errors
    from src.classification.predict import load_issue_model, load_sub_issue_model
    from src.sentiment.sentiment_analyzer import load_sentiment_model

    im, iv, il = load_issue_model()
    print(f"  ✓ load_issue_model: loaded {len(il.classes_)} issue classes")

    sm, sv, sl = load_sub_issue_model()
    print(f"  ✓ load_sub_issue_model: loaded {len(sl.classes_)} sub-issue classes")

    sent_m, sent_v, sent_l = load_sentiment_model()
    print(f"  ✓ load_sentiment_model: loaded {len(sent_l.classes_)} sentiment classes")
except Exception as e:
    print(f"  ✗ Model evaluation failed: {e}")
    traceback.print_exc()
    errors.append(("Model Evaluation", str(e)))

print("\n==================================================")
if not errors:
    print("ALL CORE MODULES & FUNCTIONS PASSED WITH ZERO ERRORS! (100% HEALTHY)")
else:
    print(f"TESTS FINISHED WITH {len(errors)} ERROR(S):")
    for component, err in errors:
        print(f"  - {component}: {err}")
print("==================================================")
