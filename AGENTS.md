# SyncP Agent Notes

SyncP is a modular monolith for a social discovery platform focused on real places shared by real people.

## Architecture Rules

- Keep the backend as one Django project with separate domain apps.
- Use service modules for business rules that do not belong in serializers or views.
- Keep DRF views thin and permission-aware.
- Prefer database constraints for uniqueness and integrity.
- Do not introduce microservices during the MVP.
- Use PostgreSQL and Redis through Docker Compose for local development.

## Backend Apps

- `users`
- `posts`
- `places`
- `comments`
- `ratings`
- `bookmarks`
- `notifications`

