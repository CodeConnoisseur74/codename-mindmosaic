from decouple import config

# 🔹 Detect if running on Fly.io (checks if "FLY_APP_NAME" exists)
IS_PRODUCTION = config('FLY_APP_NAME', default=None) is not None

# 🔹 Always get DATABASE_URL from the environment (set in Fly.io or .env)
DATABASE_URL = config('DATABASE_URL')

# 🔹 Set API host based on environment
if IS_PRODUCTION:
    HOST = 'https://codename-mindmosaic.fly.dev'
    PORT = 443
else:
    HOST = 'http://127.0.0.1'
    PORT = 8080

# 🔹 Ensure PORT is an integer
PORT = int(PORT)

# 🔹 Other settings
SECRET_KEY = config('SECRET_KEY', default='your-secret-key')
MARVIN_OPENAI_API_KEY = config('MARVIN_OPENAI_API_KEY', default='')
ACCESS_TOKEN_EXPIRE_MINUTES = config(
    'ACCESS_TOKEN_EXPIRE_MINUTES', default=30, cast=int
)
