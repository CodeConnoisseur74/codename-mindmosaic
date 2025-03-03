from decouple import config

# Load environment variables from .env
HOST = config('HOST', default='https://codename-mindmosaic.fly.dev')
PORT = config('PORT', default='443')
DATABASE_URL = config('DATABASE_URL')  # This should be in .env
SECRET_KEY = config('SECRET_KEY')  # Load secret keys safely

# OpenAI API Key (if used)
MARVIN_OPENAI_API_KEY = config('MARVIN_OPENAI_API_KEY', default='')

# Other settings (optional)
ACCESS_TOKEN_EXPIRE_MINUTES = config(
    'ACCESS_TOKEN_EXPIRE_MINUTES', default=30, cast=int
)
