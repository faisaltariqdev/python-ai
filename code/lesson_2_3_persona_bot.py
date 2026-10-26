"""Lesson 2.3: A bakery bot that answers from real facts and can change style."""

from langchain.chat_models import init_chat_model

# One dictionary controls the model, so the name and memory size are not buried in the loop.
config = {
    "model": "llama3.2:1b",
    "temperature": 0.2,
    "memory_size": 8,
}

facts = {
    "name": "Sweet Crumbs bakery",
    "city": "Lahore",
    "hours": "9 am to 10 pm, every day",
    "location": "Main Boulevard, Lahore",
    "delivery": "free over 3,000 PKR",
    "prices": {
        "cupcake": 250,
        "cake": 1500,
        "brownie": 300,
    },
}

personas = {
    "friendly": "warm and cheerful, uses simple words",
    "formal": "polite and professional, uses complete sentences",
    "sales": "excited, always suggests one extra item to buy",
}

def build_system(style):
    price_text = ", ".join(
        f"{item} {price} PKR" for item, price in facts["prices"].items()
    )
    return (
        f"You are the assistant of {facts['name']} in {facts['city']}. "
        f"Style: {style}. Hours: {facts['hours']}. Location: {facts['location']}. "
        f"Prices: {price_text}. Delivery: {facts['delivery']}. "
        "Only use these facts. If you do not know, say you do not know. "
        "Answer in 2 short lines."
    )

model = init_chat_model(
    config["model"],
    model_provider="ollama",
    temperature=config["temperature"],
)

messages = [{"role": "system", "content": build_system(personas["friendly"])}]

print("Bot ready. Commands: /persona friendly|formal|sales, /price <item>, bye")

while True:
    text = input("You: ").strip()
    lowered = text.lower()

    if lowered == "bye":
        print("Bot: Goodbye!")
        break
    elif lowered.startswith("/persona"):
        # .get() returns the friendly style when the name is missing, so pirate never crashes.
        chosen = lowered.split(maxsplit=1)[1] if " " in lowered else ""
        style = personas.get(chosen, personas["friendly"])
        messages[0]["content"] = build_system(style)
        print(f"Bot: Style changed to: {style}")
    elif lowered.startswith("/price"):
        # Prices come from the dictionary, not the model, so the bot cannot invent a number.
        item = lowered.split(maxsplit=1)[1] if " " in lowered else ""
        price = facts["prices"].get(item)
        if price is None:
            print(f"Bot: Sorry, {item} is not on our menu.")
        else:
            print(f"Bot: {item.title()} costs {price} PKR.")
    elif text == "":
        print("Bot: Please type a question.")
    else:
        messages.append({"role": "user", "content": text})
        messages = [messages[0]] + messages[1:][-config["memory_size"] :]
        response = model.invoke(messages)
        messages.append({"role": "assistant", "content": response.text})
        print(f"Bot: {response.text}")