"""Lesson 1.4: Build a ready-to-use AI prompt from business details."""

# Ask first so the prompt is about this client's real business, not a generic one.
name = input("Your name: ")
business = input("Business type: ")
problem = input("Biggest problem: ")

print(f"Welcome, {name}!")
print("--- Your AI Prompt ---")

# An f-string keeps the client's words inside one prompt we can send to a model later.
prompt = f"Suggest 3 AI solutions for a {business} that struggles with {problem}."
print(prompt)