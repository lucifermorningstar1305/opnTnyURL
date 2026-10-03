# opnTnyURL

opnTnyURL is a **self-hostable** simple URL shortener.

## Self-host

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd opntnyurl
```

### 2. Create the environment file

```bash
cp .env.example .env
```

Update `.env` with your own values.

### 3. Start the application

```bash
docker compose up -d
```

Check the containers:

```bash
docker compose ps
```

Check logs:

```bash
docker compose logs -f
```

## Run locally

### Backend

```bash
cd backend
uv sync
uv run alembic upgrade head
uv run fastapi dev app/app.py --host 0.0.0.0 --port 8080
```

### Frontend

In another terminal:

```bash
cd frontend
uv sync
uv run streamlit run app.py
```

The backend runs on:

```text
http://localhost:8080
```

The frontend runs on:

```text
http://localhost:8501
```

## License

MIT
