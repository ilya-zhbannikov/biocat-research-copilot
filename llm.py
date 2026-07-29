# llm.py
from dotenv import load_dotenv
from openai import OpenAI
import os
import ollama

load_dotenv()

client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)


def summarize_literature(
    query,
    literature_text
):

    prompt = f"""
You are a senior computational biologist.

Question:
{query}

Literature:
{literature_text}

Identify:

1. Shared biological themes
2. Relevant cell types
3. Key pathways
4. Disease mechanisms
5. Controversies
6. Future directions

Cite PMIDs.
"""

    #response = client.chat.completions.create(
    #    model="gpt-4.1",
    #    messages=[
    #        {
    #            "role": "user",
    #            "content": prompt
    #        }
    #    ],
    #    temperature=0.2
    #)

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    #return (
    #    response
    #    .choices[0]
    #    .message
    #    .content
    #)
    
    return response["message"]["content"]
