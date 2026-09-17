# First 15 Minutes

1. Install Docker Engine + Compose on the host.
2. Clone the repository.
3. Enter `35_RUNTIME/`.
4. Copy `.env.example` to `.env`.
5. Start `docker compose up --build`.
6. Open `http://localhost:8080/`.
7. Click **Create demo incident**.
8. Call `curl http://localhost:8080/api/v1/incidents`.
9. Stop with `docker compose down`.

To remove local data too:

```bash
docker compose down -v
```

The `-v` flag deletes the local PostgreSQL and Redis volumes.
