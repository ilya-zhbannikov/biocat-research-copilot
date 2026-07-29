# test_pubmed.py

from pubmed import query_pubmed

papers = query_pubmed(
    "CTHRC1 pulmonary fibrosis",
    max_results=3
)

for p in papers:
    print()
    print(p["pmid"])
    print(p["title"])
