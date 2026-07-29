# test_ollama.py

import ollama

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "What is CTHRC1?"
        }
    ]
)

print(
    response["message"]["content"]
)
