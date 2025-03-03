# 📚 Study Plan AI

This is a FastAPI + MarvinAI + Streamlit project that allows users to create Study plans based on their chosen subject matter

### 🤖 AI-Powered Study Plan Schedule

This app uses Marvin AI to generate Study Plam recommendations.

How It Works:
1. The user saves
2. The backend sends this data to the AI recommendation system.
3. The AI suggests ... based on .....

## 🎯 Installation & Setup

1. Clone the Repository:
   ```bash
   git clone https://github.com/CodeConnoisseur74/codename-mindmosaic

   cd codename-mindmosaic
   ```
2. Set Up Backend (FastAPI):
  Ensure you have Python installed, then create a virtual environment:
    ```bash
    uv venv
    ```
    Install dependencies:
    ```bash
      uv sync
    ```
    Set up environment variables:
    ```bash
      cp .env.example .env
    ```
    Then edit .env with your API keys and database settings.

    Run database migrations:
    ```bash
    alembic upgrade head
    ```
    Start the FastAPI server:
    ```bash
      uvicorn app.main:app --reload
    ```
3. Set Up Frontend (Streamlit):
    This will be in a separate concurrent terminal.
    Navigate to the frontend directory and install dependencies:
    ```bash
    cd frontend
    uv sync
    ```
    Run the Streamlit app:
    ```bash
      streamlit run app.py
    ```


## 🛠️ Tech Stack
- Backend: [FastAPI](https://fastapi.tiangolo.com), [PostgreSQL](https://www.postgresql.org), [Alembic (for migrations)](https://pypi.org/project/alembic/)
- Frontend: [Streamlit](https://streamlit.io), [Marvin AI (for recommendations)](https://www.askmarvin.ai)
- Deployment: [Fly.io (backend)](https://fly.io), [Streamlit Cloud (frontend)](https://streamlit.io/cloud)

To deploy updates:
- For backend:
  ```bash
  flyctl deploy
  ```
- For frontend if linked to Streamlit cloud:
  ```bash
  git push origin main
  ```

## 🔥 Future Features

- 📅 Calander
- 🏆 Challenges & goals
- 📝 Contributing


## 📄 License

This project is licensed under the MIT License.

## Acknowledgements

- [PyBites PDM Program](https://pybit.es/catalogue/the-pdm-program/)
- [FastAPI Documentation](https://fastapi.tiangolo.com)

---
Feel free to suggest any improvements or share your feedback by logging an issue against this repo!
