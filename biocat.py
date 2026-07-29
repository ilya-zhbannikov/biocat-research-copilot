# biocat.py
#
# This file should contain functions that operate on:
# * DE gene lists
# * RNA-seq results
# * pathway results
# * spatial marker genes

def genes_to_query(
    genes
):
    """
    Convert a list of genes into a PubMed query.
    """

    genes = [
        g.strip()
        for g in genes
        if g.strip()
    ]

    return " OR ".join(genes)


def build_pubmed_query(
    genes,
    disease=None
):
    """
    Build PubMed query from gene list.
    """

    gene_query = " OR ".join(genes)

    if disease:
        return f"({gene_query}) AND {disease}"

    return gene_query
