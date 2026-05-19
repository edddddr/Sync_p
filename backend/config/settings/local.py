from __future__ import annotations

from .base import *  # noqa: F403
from decouple import config

DEBUG = config("DJANGO_DEBUG", default=True, cast=bool)

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

