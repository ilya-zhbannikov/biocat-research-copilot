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
7. Highlight what is not represented in literature


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
    # Use tool calling and gemma4:latest:
    #response = ollama.chat( model=model_name, messages=messages, tools=[{ 'type': 'function', 'function': { 'name': 'web_search', 'description': 'Search the web for real-time live information', 'parameters': { 'type': 'object', 'properties': { 'query': {'type': 'string', 'description': 'The search query string'}, }, 'required': ['query'], }, }, }] )
    
    
    response = ollama.chat(
        model="gemma4",
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
