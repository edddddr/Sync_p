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
- `GET /api/places/`
- `POST /api/places/`
- `GET /api/places/trending/`
- `GET /api/posts/`
- `POST /api/posts/`
- `GET /api/posts/explore/`
- `POST /api/posts/{id}/like/`
- `POST /api/posts/{id}/unlike/`
- `GET /api/posts/{id}/comments/`
- `POST /api/posts/{id}/comments/`
- `POST /api/posts/{id}/bookmark/`
- `POST /api/posts/{id}/unbookmark/`
- `GET /api/comments/`
- `POST /api/comments/`
- `GET /api/bookmarks/`
- `POST /api/bookmarks/`
- `GET /api/ratings/`
- `POST /api/ratings/`

## Place/Post Flow

1. Create a place with name, category, address/city/country, latitude, and longitude.
2. Create a post with an image, caption, optional tags, and `place_id`.
3. Browse public posts through `/api/posts/explore/`.
4. Like, comment on, bookmark, and rate places around shared posts.
