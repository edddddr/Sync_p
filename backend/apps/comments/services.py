from __future__ import annotations

from apps.comments.models import Comment
from apps.posts.models import Post
from apps.users.models import User


def create_comment(*, author: User, post: Post, body: str) -> Comment:
    comment = Comment(author=author, post=post, body=body)
    comment.full_clean()
    comment.save()
    return comment


def update_comment(*, comment: Comment, body: str) -> Comment:
    comment.body = body
    comment.full_clean()
    comment.save(update_fields=["body", "updated_at"])
    return comment
