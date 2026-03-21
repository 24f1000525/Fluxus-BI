# Smart BI

Smart BI is a full-stack BI dashboard app with:
- A Vue 3 + Vite frontend
- A Flask + Pandas + LangChain backend
- CSV upload, auto chart generation, prompt-based chart generation, and data Q&A

## Project Structure

```text
backend/
  app.py
  GroqService.py
  requirements.txt
frontend/
  src/
  package.json
```

## Prerequisites

- Python 3.10+ (recommended: 3.11 or newer)
- Node.js 18+
- npm

## Backend Setup (Windows PowerShell)

From the project root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install langchain-groq
```

Run backend:

```powershell
cd backend
.\.venv\Scripts\python.exe app.py
```

Backend runs on: `http://localhost:5000`

## Frontend Setup

```powershell
cd frontend
npm install
npm run dev
```

Frontend runs on: `http://localhost:3000`

## API Endpoints

Base URL: `http://localhost:5000`

- `POST /upload`
  - Form field: `file` (CSV)
  - Returns: `doc_id`, `schema`, `auto_charts`, `dataset_subset`

- `POST /generate-chart`
  - JSON body:
    - `doc_id` (string)
    - `prompt` (string)
  - Returns: ECharts chart config

- `POST /query`
  - JSON body:
    - `doc_id` (string)
    - `question` (string)
  - Returns: natural-language answer from the dataset

## Notes

- Frontend API base is set to `http://localhost:5000` in `frontend/src/components/Dashboard.vue`.
- CORS is enabled in the backend via `flask-cors`.
- Uploaded CSV files are stored in a temporary folder and dataset metadata is kept in memory.
- Current backend code sets `GROQ_API_KEY` directly in `backend/app.py`. For production, use environment variables instead of hardcoding secrets.

## Run Both Services

Use two terminals:

Terminal 1 (backend):

```powershell
cd backend
.\.venv\Scripts\python.exe app.py
```

Terminal 2 (frontend):

```powershell
cd frontend
npm run dev
```

Open `http://localhost:3000` in your browser.
