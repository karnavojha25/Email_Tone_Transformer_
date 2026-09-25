# Email Tone Transformer

A small web app that rewrites emails in a different tone (Professional, Friendly,
Formal, Casual, Assertive, Apologetic, Persuasive, Concise) using the OpenAI API,
while preserving the original meaning and details.

## How it works

1. Paste an email and pick a target tone.
2. The app sends it to OpenAI's chat completions API with a system prompt that
   instructs the model to preserve facts/intent and only change tone/phrasing.
3. The rewritten email is displayed back to you.

Your OpenAI API key is submitted per-request and is never stored or logged by
the server.

## Local setup

```bash
pip install -r requirements.txt
python app.py
```

Visit http://localhost:5000

Optionally copy `.env.example` to `.env` and set `OPENAI_API_KEY` so you don't
have to paste a key each time locally (do not commit `.env`).

## Deployment (Render)

1. Push this repo to GitHub.
2. On render.com: New -> Web Service -> connect the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Deploy on the Free tier. Render gives you a public URL.

## Tech stack

- Python, Flask
- OpenAI API (`gpt-4o-mini` by default)
- Deployed on Render

## Notes

- No email content or API keys are stored server-side.
- This is a demo project; for production use you'd add rate limiting and
  server-side key management instead of asking visitors for their own key.
