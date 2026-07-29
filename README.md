## Problem
Biologists often spend hours searching PubMed to interpret RNA-seq results.

## Solution
BioCAT Research Copilot automates literature retrieval and biological interpretation.

## Architecture
User Query -> PubMed -> Abstract Retrieval -> Llama 3.2 -> Summary


## How to install and use
git clone https://github.com/ilya-zhbannikov/biocat-research-copilot.git

cd biocat-research-copilot

pip install -r requirements.txt

cp .env.example .env
source venv/bin/activate

Open a new Terminal window and run Ollama server by executing  "ollama serve"

Then (in original Terminal window):
streamlit run app.py
