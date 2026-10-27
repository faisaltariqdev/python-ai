"""Lesson 2.8: Bakery agent that checks prices, tracks orders and places orders."""

import json

from langchain.chat_models import init_chat_model
from langchain.tools import tool
from pydantic import ValidationError

MAX_STEPS = 5  # stop the loop if the model keeps calling tools and never answers

PRICES = {"chocolate cake": 1500, "cupcake": 250, "brownie": 300}
ORDERS = {"A101": "baking", "A102": "out for delivery", "A103": "delivered"}


@tool(parse_docstring=True)
def get_price(item: str) -> str:
    """Get the price of one bakery item.

    Args:
        item: The item name, for example "cupcake".
    """
    name = item.lower().strip()
    if name in PRICES:
        return f"{name} costs {PRICES[name]} PKR"
    return f"{item} is not on the menu. Menu: {', '.join(PRICES)}"


@tool(parse_docstring=True)
def order_status(order_id: str) -> str:
    """Check the delivery status of an existing order.

    Args:
        order_id: The order number, for example "A101".
    """
    key = order_id.upper().strip()
    if key not in ORDERS:
        return f"Order {order_id} not found"
    return f"Order {key} is {ORDERS[key]}"


@tool(parse_docstring=True)
def place_order(item: str, quantity: int, customer: str) -> str:
    """Place a new order. Only use this when the customer clearly asks to order.

    Args:
        item: The item name, for example "cupcake".
        quantity: How many, for example 2.
        customer: The customer's name.
    """
    name = item.lower().strip()
    if name not in PRICES:
        return f"{item} is not on the menu"
    total = PRICES[name] * int(quantity)  # Python does the maths, not the AI

    # Money leaves the shop only after a person types yes.
    answer = input(f"  [approve] {quantity} x {name} for {customer} = {total} PKR. Place it? (yes/no) ")
    if answer.strip().lower() != "yes":
        return "The owner did not approve this order"

    order_id = f"A{101 + len(ORDERS)}"
    ORDERS[order_id] = "received"
    with open("agent_orders.json", "a", encoding="utf-8") as file:
        file.write(json.dumps({
            "id": order_id,
            "item": name,
            "quantity": int(quantity),
            "customer": customer,
            "total": total,
        }) + "\n")
    return f"Order {order_id} placed: {quantity} x {name}, total {total} PKR"


TOOLS = {"get_price": get_price, "order_status": order_status, "place_order": place_order}

model = init_chat_model("llama3.2:1b", model_provider="ollama", temperature=0)
model_with_tools = model.bind_tools(list(TOOLS.values()))

messages = [{
    "role": "system",
    "content": (
        "You are the Sweet Crumbs bakery agent. Use the tools for prices, order status and new orders. "
        "Never guess prices or statuses. Answer in 2 short lines."
    ),
}]

print("Sweet Crumbs Agent: ask about prices, orders, or place an order. Type 'bye' to exit.")

while True:
    text = input("You: ").strip()
    if text.lower() == "bye":
        break
    if text == "":
        continue
    messages.append({"role": "user", "content": text})

    # Keep calling tools until the model writes an answer, or MAX_STEPS runs out.
    for step in range(MAX_STEPS):
        response = model_with_tools.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            print(f"Agent: {response.text}")
            break

        for call in response.tool_calls:
            name = call["name"]
            args = call["args"]
            if name not in TOOLS:
                result = f"Unknown tool: {name}"
            else:
                try:
                    result = TOOLS[name].invoke(args)
                except ValidationError:
                    result = f"Tool error: wrong arguments {args}. Check the tool's Args."
            print(f"  [tool] {name}({args}) -> {result}")
            messages.append({"role": "tool", "content": result, "tool_call_id": call["id"]})
    else:
        print("Agent: Sorry, I could not finish that. A human will help you.")