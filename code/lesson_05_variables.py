"""Lesson 1.5: AI model profile card with a cost estimate."""

# The client's own model settings, so the cost uses their price.
model_name = "llama3.2"
context_window = 128000
price_per_1k = 0.5
runs_locally = True

print("--- AI Model Profile Card ---")
print(f"Model: {model_name} {type(model_name)}")
print(f"Context window: {context_window} tokens {type(context_window)}")
print(f"Price per 1K tokens: {price_per_1k} PKR {type(price_per_1k)}")
print(f"Runs locally: {runs_locally} {type(runs_locally)}")

# input() returns text, so int() is required before the maths.
tokens = int(input("Tokens per chat: "))
estimated_cost = round((tokens / 1000) * price_per_1k, 2)

print(f"Tokens per chat: {tokens}")
print(f"Estimated cost: {estimated_cost} PKR")