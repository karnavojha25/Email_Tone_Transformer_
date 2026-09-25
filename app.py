import os
from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TONES = [
    "Professional",
    "Friendly",
    "Formal",
    "Casual",
    "Assertive",
    "Apologetic",
    "Persuasive",
    "Concise",
]

SYSTEM_PROMPT = (
    "You are an expert email editor. Rewrite the user's email in the requested tone "
    "while preserving all factual details, names, dates, and the original intent. "
    "Do not add new information or invent details that were not in the original email. "
    "Do not add a subject line unless one was already present. "
    "Output ONLY the rewritten email text, with no explanation, preamble, or quotation marks."
)


def rewrite_email(original_text: str, tone: str, api_key: str, model: str = "gpt-4o-mini") -> str:
    if not api_key:
        raise ValueError("OpenAI API key is required.")
    if not original_text.strip():
        raise ValueError("Email text cannot be empty.")

    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

    user_prompt = (
        f"Rewrite the following email in a {tone.lower()} tone:\n\n---\n{original_text}\n---"
    )

    response = client.chat.completions.create(
        model="gemini-3.6-flash",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=800,
    )

    return response.choices[0].message.content.strip()


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        tones=TONES,
        result=None,
        error=None,
        original="",
        selected_tone=TONES[0],
    )


@app.route("/transform", methods=["POST"])
def transform():
    original_text = request.form.get("email_text", "")
    tone = request.form.get("tone", TONES[0])
    api_key = request.form.get("api_key", "").strip() or os.environ.get("GEMINI_API_KEY", "")

    error = None
    result = None

    try:
        result = rewrite_email(original_text, tone, api_key)
    except Exception as e:
        error = str(e)

    return render_template(
        "index.html",
        tones=TONES,
        result=result,
        error=error,
        original=original_text,
        selected_tone=tone,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
