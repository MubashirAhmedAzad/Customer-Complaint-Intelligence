import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.rag.vector_store import get_or_create_collection

col = get_or_create_collection()
where_clause = {
    "$and": [
        {"company": {"$eq": "Cedar Ridge Bank"}},
        {"product": {"$eq": "Credit card"}}
    ]
}
res = col.query(query_texts=["duplicate charge"], n_results=2, where=where_clause)
print("SUCCESS! Documents found:", len(res["documents"][0]))
for doc, meta in zip(res["documents"][0], res["metadatas"][0]):
    print("Meta:", meta)
