"""Lesson 2.5: Reusable AI skills for a bakery marketing toolkit."""

from langchain.chat_models import init_chat_model

# Both models are created once. Skills only choose which one to call.
precise = init_chat_model("llama3.2:1b", model_provider="ollama", temperature=0.2)
creative = init_chat_model("llama3.2:1b", model_provider="ollama", temperature=0.9)


def ask_ai(prompt: str, system: str = "You are a helpful assistant.", creative_mode: bool = False) -> str:
    """Send one prompt and return the model's text."""
    chosen = creative if creative_mode else precise
    response = chosen.invoke([
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ])
    return response.text.strip()


def estimate_tokens(text: str) -> int:
    """Estimate tokens from characters, without calling the AI."""
    return round(len(text) / 4)


assert estimate_tokens("abcd") == 1
assert estimate_tokens("abcdefgh") == 2


def summarize(text: str) -> str:
    """Shorten a note into one sentence."""
    return ask_ai(text, system="Summarize this in one short sentence.")


def translate(text: str, language: str = "Urdu") -> str:
    """Translate text. Urdu is used when no language is given."""
    return ask_ai(
        f"Translate this into {language}: {text}",
        system="You are a translator. Return only the translation.",
    )


def reply_to_review(review: str) -> str:
    """Write a polite reply to a customer review."""
    return ask_ai(
        review,
        system="You reply to bakery reviews in 2 short lines. Be polite.",
        creative_mode=True,
    )


usage = {"summarize": 0, "translate": 0, "reply": 0}

print("Sweet Crumbs AI Toolkit. Commands: /summarize, /translate, /reply, bye")

while True:
    command = input("Command: ").strip().lower()

    if command == "bye":
        break
    elif command == "/summarize":
        text = input("Text to summarize: ").strip()
        print(f"AI: {summarize(text)}")
        usage["summarize"] += 1
    elif command == "/translate":
        text = input("Text to translate: ").strip()
        language = input("Language (Enter for Urdu): ").strip()
        # An empty Enter keeps the default, so the skill still translates to Urdu.
        if language == "":
            answer = translate(text)
        else:
            answer = translate(text, language)
        print(f"AI: {answer}")
        usage["translate"] += 1
    elif command == "/reply":
        review = input("Customer review: ").strip()
        print(f"AI: {reply_to_review(review)}")
        print(f"    (review was about {estimate_tokens(review)} tokens)")
        usage["reply"] += 1
    else:
        print("Unknown command. Try /summarize, /translate, /reply or bye.")

print("Skills used today:")
for skill, count in usage.items():
    print(f"  {skill}: {count}")