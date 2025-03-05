from decouple import config

# 🔹 Detect if running on Fly.io (checks if "FLY_APP_NAME" exists)
IS_PRODUCTION = config('FLY_APP_NAME', default=None) is not None

# 🔹 Set database URL based on environment
if IS_PRODUCTION:
    DATABASE_URL = config('DATABASE_URL')  # ✅ Use Fly.io database
    HOST = 'https://codename-mindmosaic.fly.dev'
    PORT = 443
else:
    DATABASE_URL = config(
        'DATABASE_URL', default='LOCAL_DATABSE_URL'
    )  # ✅ Default to local database
    HOST = 'http://127.0.0.1'
    PORT = 8080

# 🔹 Ensure PORT is an integer (since environment variables are strings)
PORT = int(PORT)

# 🔹 Other settings
SECRET_KEY = config('SECRET_KEY', default='your-secret-key')
MARVIN_OPENAI_API_KEY = config('MARVIN_OPENAI_API_KEY', default='')
ACCESS_TOKEN_EXPIRE_MINUTES = config(
    'ACCESS_TOKEN_EXPIRE_MINUTES', default=30, cast=int
)
