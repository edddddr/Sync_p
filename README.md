# SyncP

SyncP is a social discovery platform for sharing and discovering real places through posts, photos, ratings, and community activity.

## Local Development

1. Review `.env` and adjust values if needed.
2. Start the stack:

```bash
docker compose up --build
```

3. Open the API:

```text
http://localhost:8000/api/
```

4. Open API docs:

```text
http://localhost:8000/api/docs/
```

## First Backend Endpoints

- `GET /api/health/`
- `POST /api/auth/register/`
- `POST /api/auth/token/`
- `POST /api/auth/token/refresh/`
- `POST /api/auth/logout/`
- `GET /api/auth/me/`
- `PATCH /api/auth/me/`
- `GET /api/users/`
- `POST /api/users/{id}/follow/`
- `POST /api/users/{id}/unfollow/`

