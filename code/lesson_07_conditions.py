"""Lesson 1.7: Route each task to a model and estimate the cost."""

# Clean the task so " Code " and "PRIVATE" still match the router.
task = input("Task (code / private / chat): ").strip().lower()
tokens = int(input("Estimated tokens: "))

# Private data stays on the laptop, so that route costs nothing.
if task == "code":
    model = "claude (cloud, strong at code)"
    price_per_1k = 0.8
elif task == "private":
    model = "llama3.2 (local, Ollama)"
    price_per_1k = 0
else:
    model = "gemini (cloud, cheap chat)"
    price_per_1k = 0.2

if tokens > 4000:
    print("Warning: long request, consider shortening it.")
else:
    print("Length is fine.")

cost = (tokens / 1000) * price_per_1k
print(f"Chosen model: {model}")
print(f"Estimated cost: {cost:.2f} PKR")