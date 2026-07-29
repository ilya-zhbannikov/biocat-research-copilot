# pubmed.py
#
# This module handles:
# * PubMed search
# * Abstract retrieval
# * Formatting results
# * Saving papers (optional)
#

import os
from Bio import Entrez
from dotenv import load_dotenv

load_dotenv()

Entrez.email = os.getenv(
    "PUBMED_EMAIL",
    "ilya.zhbannikov@duke.edu"
)


def search_pubmed(
    query: str,
    max_results: int = 10
):
    """
    Search PubMed and return PMIDs.
    """

    handle = Entrez.esearch(
        db="pubmed",
        term=query,
        retmax=max_results
    )

    results = Entrez.read(handle)

    handle.close()

    return results["IdList"]


def fetch_pubmed_details(pmids):
    """
    Retrieve title + abstract for a list of PMIDs.
    """

    if not pmids:
        return []

    handle = Entrez.efetch(
        db="pubmed",
        id=",".join(pmids),
        rettype="abstract",
        retmode="xml"
    )

    records = Entrez.read(handle)

    handle.close()

    papers = []

    for article in records["PubmedArticle"]:

        try:

            citation = article["MedlineCitation"]

            pmid = str(citation["PMID"])

            title = citation["Article"][
                "ArticleTitle"
            ]

            abstract = ""

            if (
                "Abstract"
                in citation["Article"]
            ):

                abstract_text = citation[
                    "Article"
                ]["Abstract"][
                    "AbstractText"
                ]

                abstract = " ".join(
                    [
                        str(x)
                        for x in abstract_text
                    ]
                )

            papers.append(
                {
                    "pmid": pmid,
                    "title": str(title),
                    "abstract": abstract
                }
            )

        except Exception as e:

            print(
                f"Error parsing article: {e}"
            )

    return papers


def query_pubmed(
    query,
    max_results=10
):
    """
    Search + retrieve papers.
    """

    pmids = search_pubmed(
        query,
        max_results
    )

    papers = fetch_pubmed_details(
        pmids
    )

    return papers


def papers_to_text(
    papers
):
    """
    Convert papers into an LLM-friendly string.
    """

    text = ""

    for i, paper in enumerate(
        papers,
        start=1
    ):

        text += f"""
PAPER {i}

PMID: {paper['pmid']}

TITLE:
{paper['title']}

ABSTRACT:
{paper['abstract']}

---------------------------------------
"""

    return text
