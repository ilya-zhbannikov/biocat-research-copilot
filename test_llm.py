from llm import summarize_literature

summary = summarize_literature(
    "CTHRC1 pulmonary fibrosis",
    """
PMID: 123456

CTHRC1 promotes extracellular matrix
remodeling and fibrosis.
"""
)

print(summary)
