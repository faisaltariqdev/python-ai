"""Lesson 2.2: A tutor that remembers the chat, then forgets on /reset."""

from langchain.chat_models import init_chat_model

model = init_chat_model(
    "llama3.2:1b",
    model_provider="ollama",
    temperature=0.2,
)

# Index 0 stays forever, so /reset and trimming never delete the tutor's role.
messages = [
    {
        "role": "system",
        "content": "You are a friendly tutor. Answer in 2 short lines.",
    }
]

print("Tutor: Ask me anything. Commands: /reset, /count, bye")

while True:
    text = input("You: ").strip()

    if text.lower() == "bye":
        print("Tutor: Goodbye!")
        break
    elif text.lower() == "/reset":
        # Drop the chat and keep only the system message.
        messages = [messages[0]]
        print("Tutor: Memory cleared.")
    elif text.lower() == "/count":
        print(f"Tutor: {len(messages)} messages in memory.")
    elif text == "":
        print("Tutor: Please type a question.")
    else:
        messages.append({"role": "user", "content": text})
        # System message plus the last 8 messages, so a long chat stays cheap.
        messages = [messages[0]] + messages[1:][-8:]

        response = model.invoke(messages)
        messages.append({"role": "assistant", "content": response.text})

        print(f"Tutor: {response.text}")
        print(f"(tokens sent: {response.usage_metadata['input_tokens']})")