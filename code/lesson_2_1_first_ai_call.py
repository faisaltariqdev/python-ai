"""Lesson 2.1: Ask a local AI model to explain a topic."""

import time

from langchain.chat_models import init_chat_model

# A low temperature keeps a tutor's answer steady instead of creative.
model = init_chat_model(
    "llama3.2:1b",
    model_provider="ollama",
    temperature=0.2,
)

topic = input("Topic: ").strip()
level = input("Level (beginner or expert): ").strip()

# The system message sets the role, the student's level, and how long the answer may be.
response = model.invoke([
    {
        "role": "system",
        "content": f"You are a friendly tutor. Explain for a {level}. Answer in 3 short lines.",
    },
    {"role": "user", "content": topic},
])

seconds = response.response_metadata["total_duration"] / 1_000_000_000
total_tokens = response.usage_metadata["total_tokens"]

print("=" * 40)
print(response.text)
print("=" * 40)
print(f"{total_tokens} tokens in {seconds:.1f} seconds")