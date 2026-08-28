import ollama

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "Explain what an AI agent is in very simple words."
        }
    ]
)

print(response["message"]["content"])
