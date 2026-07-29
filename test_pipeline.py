# test_pipeline.py

from pubmed import (
    query_pubmed,
    papers_to_text
)

from llm import (
    summarize_literature
)

query = "CTHRC1 pulmonary fibrosis"

papers = query_pubmed(
    query,
    max_results=5
)

literature = papers_to_text(
    papers
)

summary = summarize_literature(
    query,
    literature
)

print(summary)
