from decouple import config

# Fly.io
DATABASE_URL = config('DATABASE_URL', default=None)

HOST = config('HOST', default='https://codename-mindmosaic.fly.dev')

PORT = config('PORT', default='443')

SECRET_KEY = config('SECRET_KEY', default='SECRET_KEY')

MARVIN_OPENAI_API_KEY = config('MARVIN_OPENAI_API_KEY', default='')

ACCESS_TOKEN_EXPIRE_MINUTES = config(
    'ACCESS_TOKEN_EXPIRE_MINUTES', default=30, cast=int
)
