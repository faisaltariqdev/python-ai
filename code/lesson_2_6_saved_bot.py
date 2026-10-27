"""Lesson 2.6: A bakery bot that loads facts from a file and saves the chat."""

import json
from pathlib import Path

import httpx
import ollama
from langchain.chat_models import init_chat_model

FOLDER = Path(__file__).parent
FAQ_PATH = FOLDER / "faq.json"
HISTORY_PATH = FOLDER / "chat_history.json"
LOG_PATH = FOLDER / "errors.log"


def log_error(message: str) -> None:
    """Append one error line so a crash can be checked later."""
    with LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(message + "\n")


def save_history(history: list) -> None:
    """Write the chat as readable JSON after every turn."""
    with HISTORY_PATH.open("w", encoding="utf-8") as file:
        json.dump(history, file, indent=2, ensure_ascii=False)


# The owner edits faq.json, so a price change does not need a code change.
try:
    with FAQ_PATH.open(encoding="utf-8") as file:
        facts = json.load(file)
except FileNotFoundError:
    print("faq.json is missing. Add it next to this script and run again.")
    raise SystemExit(1)

price_text = ", ".join(f"{item} {price} PKR" for item, price in facts["prices"].items())
system = (
    f"You are the assistant of {facts['name']} in {facts['city']}. "
    f"Hours: {facts['hours']}. Location: {facts['location']}. "
    f"Delivery: {facts['delivery']}. Prices: {price_text}. "
    "Only use these facts. Answer in 2 short lines."
)

# A damaged history file must start fresh instead of showing a traceback.
history = []
if HISTORY_PATH.exists():
    try:
        with HISTORY_PATH.open(encoding="utf-8") as file:
            loaded = json.load(file)
        if isinstance(loaded, list):
            history = loaded
            print(f"Loaded {len(history)} old messages.")
        else:
            raise json.JSONDecodeError("not a list", "", 0)
    except json.JSONDecodeError:
        print("History file was damaged. Starting a fresh chat.")
        history = []

model = init_chat_model("llama3.2:1b", model_provider="ollama", temperature=0.2)
messages = [{"role": "system", "content": system}, *history]

print("Sweet Crumbs Bot: Ask me anything. Commands: /reset, bye")

while True:
    text = input("You: ").strip()

    if text.lower() == "bye":
        save_history(messages[1:])
        print("Bot: Goodbye! Your chat is saved.")
        break
    elif text.lower() == "/reset":
        messages = [messages[0]]
        save_history([])
        print("Bot: Memory cleared.")
        continue
    elif text == "":
        print("Bot: Please type a question.")
        continue

    messages.append({"role": "user", "content": text})
    try:
        response = model.invoke(messages)
    except httpx.ConnectError:
        # The question never got an answer, so take it back out of the saved chat.
        messages.pop()
        log_error("ConnectError: Ollama app is not running.")
        print("Bot: I am offline right now. Please open the Ollama app and try again.")
        continue
    except ollama.ResponseError as error:
        messages.pop()
        log_error(f"ResponseError: {error}")
        print("Bot: The model could not answer. Check the model name and try again.")
        continue

    messages.append({"role": "assistant", "content": response.text.strip()})
    save_history(messages[1:])
    print(f"Bot: {response.text.strip()}")