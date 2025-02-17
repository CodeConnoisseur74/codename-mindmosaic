#!/bin/bash

#!/bin/sh
/app/wait-for-it.sh database:5432 -- echo "Database is up"
# Start your application
exec exec fastapi dev api/main.py


# Run the FastAPI application
uv run fastapi dev api/main.py

# Run the Streamlit application
# uv run streamlit run app.py
