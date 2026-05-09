FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir fastapi uvicorn[standard] sqlalchemy pydantic pydantic-settings openai python-multipart pypdf Pillow python-jose[cryptography] httpx

COPY . .

RUN mkdir -p data

EXPOSE ${PORT:-8002}

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8002}"]
