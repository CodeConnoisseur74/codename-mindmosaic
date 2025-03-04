from decouple import config

# 🔹 Detect if running on Fly.io (checks if "FLY_DATABASE_URL" exists)
FLY_DATABASE_URL = config('FLY_DATABASE_URL', default=None)

# 🔹 Database connection setup
if FLY_DATABASE_URL:
    DATABASE_URL = FLY_DATABASE_URL  # ✅ Use Fly.io database in production
else:
    DATABASE_URL = config(
        'DATABASE_URL',
        default='postgresql://postgres:bobby11@localhost:5432/codename-mindmosaic',
    )  # ✅ Default to local database for development

# 🔹 Other settings
HOST = config('HOST', default='https://codename-mindmosaic.fly.dev')
PORT = config('PORT', default='443')
SECRET_KEY = config('SECRET_KEY', default='your-secret-key')
MARVIN_OPENAI_API_KEY = config('MARVIN_OPENAI_API_KEY', default='')
ACCESS_TOKEN_EXPIRE_MINUTES = config(
    'ACCESS_TOKEN_EXPIRE_MINUTES', default=30, cast=int
)
