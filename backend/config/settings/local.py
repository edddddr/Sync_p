from __future__ import annotations

from decouple import config

from .base import *  # noqa: F403

DEBUG = config("DJANGO_DEBUG", default=True, cast=bool)

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
