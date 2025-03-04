from decouple import config

# Load environment mode (defaults to 'local' if not specified)
ENVIRONMENT = config('ENVIRONMENT', default='local')

# ✅ Use Fly.io database in production, otherwise use local database
DATABASE_URL = (
    config('FLY_DATABASE_URL')
    if ENVIRONMENT == 'production'
    else config('DATABASE_URL')
)

# ✅ Other configurations
HOST = config('HOST', default='https://codename-mindmosaic.fly.dev')
PORT = config('PORT', default='443')
SECRET_KEY = config('SECRET_KEY')
MARVIN_OPENAI_API_KEY = config('MARVIN_OPENAI_API_KEY', default='')
ACCESS_TOKEN_EXPIRE_MINUTES = config(
    'ACCESS_TOKEN_EXPIRE_MINUTES', default=30, cast=int
)
