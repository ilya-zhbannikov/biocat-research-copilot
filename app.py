import streamlit as st
import gseapy as gp
import ollama
import pandas as pd

# Title
col1, col2 = st.columns([1, 6])
with col1:
    st.image("assets/biocat_logo1.png", width=80)
with col2:
    st.markdown("""
# BioCAT Research Copilot: AI-powered literature discovery and omics interpretation

Built with: PubMed, Ollama Gemma4, and Streamlit
""")





from pubmed import (
    query_pubmed,
    papers_to_text
)

from llm import (
    summarize_literature
)

st.set_page_config(
    page_title="BioCAT Research Copilot",
    layout="wide"
)

examples = [
    "CTHRC1 pulmonary fibrosis",
    "POSTN fibrosis",
    "COL1A1 ECM remodeling",
    "TGFB1 fibroblast activation",
    "MUC5B interstitial lung disease"
]

selected_query = st.selectbox(
    "Example Queries",
    examples
)

query = st.text_input(
    "Or enter your own query",
    value = selected_query
)

n_papers = st.slider(
    "Number of papers",
    min_value=1,
    max_value=20,
    value=5
)




with st.sidebar:
    st.image("assets/biocat_logo1.png", width=120)
    st.title("BioCAT Research Copilot")
    st.markdown("""
### Roadmap

- [x] PubMed Search
- [x] LLM Summary
- [x] Differential Expression Upload
- [x] Pathway Analysis
- [ ] Spatial Transcriptomics Support
- [ ] FCAP Integration
""")


#tab1, tab2, tab3 = st.tabs([
#    "📚 Literature Search",
#    "🧬 DE Interpretation",
#    "ℹ️ About"
#])

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📚 Literature",
    "🧬 DE Analysis",
    "🧪 Pathways",
    "🗺️ Spatial",
    "🏥 FCAP",
    "ℹ️ About"
])


with tab1:
    if st.button("Run Search"):
        with st.spinner("Searching PubMed..."):
            papers = query_pubmed(query, max_results=n_papers)
            literature = papers_to_text(papers)
        
        with st.spinner("Generating summary..."):
            summary = summarize_literature(
                query,
                literature
            )
            
        st.subheader("Summary")
        st.write(summary)
        st.subheader("Retrieved Papers")
        
        for paper in papers:
            with st.expander( f"📄 PMID {paper['pmid']}"):
                st.markdown(f"### {paper['title']}")
                st.write(paper['abstract'])
        
        ### Metrics 
        col1, col2, col3 = st.columns(3)
        col1.metric("Papers Retrieved",len(papers))
        col2.metric("PMIDs",len(set([p["pmid"] for p in papers])))
        col3.metric("Model", "gemma4")
        
        st.download_button(
            "Download Summary",
            summary,
            "summary.txt"
        )

with tab2:
    st.header("Differential Expression Analysis")

    uploaded_file = st.file_uploader(
        "Upload DE Results",
        type=["csv"]
    )

    top_genes = []
    if uploaded_file:

        df = pd.read_csv(uploaded_file)

        st.dataframe(df.head())
        # Extract top genes
        top_genes = (df.sort_values("logFC", ascending=False).head(10)["gene"].tolist())
        st.write(top_genes)
        # Create a literature query
        query = (" OR ".join(top_genes))
        # Leading genes:
        top_genes_str = ", ".join(top_genes)
    
with tab3:
    st.header("Pathway Analysis")
    
    if top_genes :
        enr = gp.enrichr(gene_list=top_genes, gene_sets="KEGG_2021_Human", outdir=None)
        pathway_df = enr.results
        top_pathways = pathway_df.sort_values("Adjusted P-value").head(10)
    
        st.dataframe(top_pathways[["Term", "Adjusted P-value", "Odds Ratio"]])
    
        pathway_text = ""
        for _, row in top_pathways.iterrows():
            pathway_text += f"""
            Pathway: {row['Term']}
            Adjusted P-value: {row['Adjusted P-value']}
            Odds Ratio: {row['Odds Ratio']}
        
            """
        
        # Send this to Ollama:
        prompt = f"""
        You are an expert computaitonal biologist
        
        Top DE genes:
        
        {top_genes_str}
        
        The following pathways are significantly enriched (top enriched pathways):
        
        {pathway_text}
    
        Generate:
        
        1. Main biological theme (biological interpretation)
        2. Relevant cell types (cell type hypothesis)
        3. Disease relevance
        4. Potential mechanisms (mechanistic explanation)
        5. Suggested follow-up analyses
        6. Manuscript-ready paragraph
        
        Be concise and scientific
        """
        
        # Generate response:
        response = ollama.chat(model="gemma4", messages=[{"role": "user", "content": prompt}])
        interpretation = response["message"]["content"]
        
        st.subheader("AI Pathway Interpretation")
        st.markdown(interpretation)

with tab4:

    st.header("🗺️ Spatial Transcriptomics Support")

    st.markdown("""
    Upload ROI or cluster marker genes and generate
    pathway analysis and AI-assisted spatial interpretation.
    """)

    uploaded_file = st.file_uploader(
        "Upload ROI Marker Genes",
        type=["csv"],
        key="spatial"
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.subheader("Input Data")

        st.dataframe(df.head())

        #gene_column = st.selectbox("Gene Column",df.columns)
        
        cluster_id = st.selectbox("Select Cluster", sorted(df["cluster"].unique()))
        
        marker_genes = (
            df[df["cluster"] == cluster_id]["gene"]
            .dropna()
            .unique()
            .tolist()
        )

        #marker_genes = (
        #    df[gene_column]
        #    .dropna()
        #    .unique()
        #    .tolist()
        #)

        st.subheader("Marker Genes")

        st.write(marker_genes[:20])

        if st.button("🧬 Analyze Spatial Region"):

            with st.spinner("Running pathway analysis..."):

                enr = gp.enrichr(
                    gene_list=marker_genes,
                    gene_sets=[
                        "GO_Biological_Process_2023",
                        "KEGG_2021_Human"
                    ],
                    organism="human",
                    outdir=None
                )

                pathway_df = (
                    enr.results
                    .sort_values(
                        "Adjusted P-value"
                    )
                    .head(10)
                )

            st.subheader("Top Pathways")

            st.dataframe(
                pathway_df[
                    [
                        "Term",
                        "Adjusted P-value",
                        "Odds Ratio"
                    ]
                ]
            )

            pathway_text = ""

            for _, row in pathway_df.iterrows():

                pathway_text += f"""
Pathway:
{row['Term']}

Adjusted p-value:
{row['Adjusted P-value']}

"""

            spatial_prompt = f"""
You are an expert spatial transcriptomics scientist.

Marker genes:

{", ".join(marker_genes[:30])}

Enriched pathways:

{pathway_text}

Generate:

1. Likely cell type
2. Biological state
3. Disease relevance
4. Spatial niche interpretation
5. Suggested downstream analyses

Assume marker genes come from a spatial
transcriptomics ROI.
"""

            response = ollama.chat(
                model="gemma4", # model="llama3.2",
                messages=[
                    {
                        "role": "user",
                        "content": spatial_prompt
                    }
                ]
            )

            interpretation = (
                response["message"]["content"]
            )

            st.subheader(
                "🤖 AI Spatial Interpretation"
            )

            st.markdown(
                interpretation
            )

with tab6:
    st.header("About")

    st.markdown("""
    BioCAT Research Copilot

    - PubMed Retrieval
    - Local LLM (Gemma 4.0)
    - AI-assisted interpretation
    """)



