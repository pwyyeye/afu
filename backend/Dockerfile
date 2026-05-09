FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir fastapi uvicorn[standard] sqlalchemy pydantic pydantic-settings openai python-multipart pypdf Pillow python-jose[cryptography] httpx

COPY . .

RUN mkdir -p data

EXPOSE 8002

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
