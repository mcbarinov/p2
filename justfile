dev:
    uv run fastapi dev main.py

tunnel:
    cloudflared tunnel --url localhost:8000
