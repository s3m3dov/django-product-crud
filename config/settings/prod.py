from .base import *

X_FRAME_OPTIONS = "DENY"
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_REDIRECT_EXEMPT = []
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', True)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', True)
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', True)

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": env.db("DATABASE_URL", default="postgres:///django"),
}
