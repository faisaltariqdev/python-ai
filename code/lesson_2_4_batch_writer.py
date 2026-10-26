"""Lesson 2.4: Write a menu description for every priced item in one run."""

from langchain.chat_models import init_chat_model

products = {
    "Chocolate Cake": 1500,
    "Cupcake": 250,
    "Brownie": 300,
    "Donut": 200,
    "Old Stock": 0,
}

# Create the model once. Making it inside the loop would reload it for every item.
model = init_chat_model(
    "llama3.2:1b",
    model_provider="ollama",
    temperature=0.2,
)

menu = []
total_tokens = 0
total_seconds = 0

for name, price in products.items():
    # A zero price is not for sale, so skip it before any AI call.
    if price == 0:
        print(f"Skipping {name.lower()} (no price)")
        continue

    response = model.invoke([
        {
            "role": "system",
            "content": "You write bakery menu text. Reply with one sentence only.",
        },
        {
            "role": "user",
            "content": f"Describe {name}, which costs {price} PKR, in one sentence.",
        },
    ])

    menu.append({
        "item": name,
        "price": price,
        "text": response.text.strip(),
    })
    total_tokens += response.usage_metadata["total_tokens"]
    total_seconds += response.response_metadata["total_duration"] / 1_000_000_000

print("=" * 50)
for number, item in enumerate(menu, start=1):
    print(f"{number}. {item['item']} ({item['price']} PKR)")
    print(f"   {item['text']}")
print("=" * 50)
print(f"{len(menu)} descriptions, {total_tokens} tokens, {total_seconds:.1f} seconds")