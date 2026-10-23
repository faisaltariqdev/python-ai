"""Lesson 1.6: Clean a messy question before it becomes an AI prompt."""

# Customers paste extra spaces and random capitals, so clean the text before the model sees it.
name = input("Your name: ").strip().title()
question = input("Your question: ").strip().capitalize()

characters = len(question)
estimated_tokens = round(characters / 4)
# .lower() makes the check ignore PYTHON, Python, or python.
mentions_python = "python" in question.lower()

print("=" * 40)
print(f"Cleaned question: {question}")
print(f"Characters: {characters}, about {estimated_tokens} tokens")
print(f"Mentions Python: {mentions_python}")
print("=" * 40)

# Slice to 150 characters so a very long question cannot blow the prompt size.
prompt = f"""You are a friendly Python tutor.
Greet {name} by name and answer in 3 short lines.
Question: {question[:150]}"""
print(prompt)
