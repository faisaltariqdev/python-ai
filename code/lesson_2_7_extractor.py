"""Lesson 2.7: Turn messy WhatsApp messages into checked orders."""

import json
from pathlib import Path

from langchain.chat_models import init_chat_model

PRICES = {
    "chocolate cake": 1500,
    "cupcake": 250,
    "brownie": 300,
}

ORDER_SCHEMA = {
    "type": "object",
    "properties": {
        "customer": {"type": "string"},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "quantity": {"type": "integer"},
                },
                "required": ["name", "quantity"],
            },
        },
        "address": {"type": "string"},
    },
    "required": ["customer", "items", "address"],
}

# Temperature 0 and a schema keep the same message in the same JSON shape.
extractor = init_chat_model(
    "llama3.2:1b",
    model_provider="ollama",
    temperature=0,
    format=ORDER_SCHEMA,
)

SYSTEM = (
    "Extract the bakery order from the WhatsApp message. "
    f"Item names must be one of: {', '.join(PRICES)}. "
    "If the customer name or address is not in the message, use an empty string. "
    "If it is not an order, return an empty items list. Never invent details."
)

messages_in = [
    "3 brownies please, Sara, DHA phase 5",
    "Salam! 2 cupcakes aur 1 chocolate cake chahiye. Ali, house 12 Gulberg",
    "1 pizza and 2 brownies, Bilal, Model Town",
    "hi do you deliver to Johar Town?",
    "bhai 1 brownie bhej dena, Hina, Johar Town",
]

saved = []
total_value = 0
check_count = 0

for message in messages_in:
    print(f"\nMessage: {message}")
    response = extractor.invoke([
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": message},
    ])

    # The model can still add extra words, so bad JSON must not crash the loop.
    try:
        order = json.loads(response.text)
    except json.JSONDecodeError:
        print("  CHECK: reply was not valid JSON")
        check_count += 1
        continue

    customer = str(order.get("customer", "")).strip()
    address = str(order.get("address", "")).strip()
    raw_items = order.get("items", [])
    if not isinstance(raw_items, list) or raw_items == []:
        print("  Not an order: needs a human reply.")
        continue

    if customer and customer.lower() not in message.lower():
        print(f"  CHECK: '{customer}' is not in the message")
        check_count += 1
        customer = ""

    checked_items = []
    order_total = 0
    for item in raw_items:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "")).strip().lower()
        try:
            quantity = int(item.get("quantity", 0))
        except (TypeError, ValueError):
            quantity = 0
        if quantity < 1:
            continue
        # Off-menu items are flagged and never given a price.
        if name not in PRICES:
            print(f"  CHECK: '{name}' is not on the menu")
            check_count += 1
            continue
        line_total = PRICES[name] * quantity
        order_total += line_total
        checked_items.append({"name": name, "quantity": quantity, "line_total": line_total})
        print(f"  {quantity} x {name} = {line_total} PKR")

    if checked_items == []:
        print("  Not an order: needs a human reply.")
        continue

    print(f"  Customer: {customer}, Address: {address}")
    print(f"  Total: {order_total} PKR")
    saved.append({
        "customer": customer,
        "address": address,
        "items": checked_items,
        "total": order_total,
    })
    total_value += order_total

out_path = Path(__file__).parent / "orders.json"
with out_path.open("w", encoding="utf-8") as file:
    json.dump(saved, file, indent=2, ensure_ascii=False)

print("\n" + "=" * 50)
print(f"Orders found: {len(saved)} | Total value: {total_value:,} PKR | Checks: {check_count}")
print(f"Saved {len(saved)} orders to orders.json")