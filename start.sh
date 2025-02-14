#!/bin/bash

# Run the FastAPI application
uv run fastapi dev api/main.py &

# Run the Streamlit application
uv run streamlit run app.py
