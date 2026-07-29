# debug_env.py

from dotenv import load_dotenv
import os

load_dotenv()

print(
    "OPENAI:",
    os.getenv("OPENAI_API_KEY")
)

print(
    "EMAIL:",
    os.getenv("PUBMED_EMAIL")
)
