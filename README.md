# Smart BI

Smart BI is a full-stack BI dashboard app with:
- A Vue 3 + Vite frontend
- A Flask + Pandas + LangChain backend
- CSV upload, auto chart generation, prompt-based chart generation, and data Q&A

## Features

- CSV Upload and Profiling: Upload CSV files and automatically extract schema, column types, and data preview.
- Auto Dashboard Generation: Instantly generate KPI cards and multiple chart types from detected numeric and categorical fields.
- Prompt-Based Chart Creation: Create custom visualizations with natural-language prompts.
- Data Q&A Assistant: Ask questions about uploaded data and get natural-language answers.
- Interactive BI UI: Drag-and-arrange dashboard widgets with responsive chart rendering.
- Export-Friendly Reports: Capture and export dashboard snapshots for sharing.
- Frontend and Backend Separation: Vue frontend communicates with Flask APIs for scalable full-stack development.
- CORS-Enabled API Layer: Ready for local frontend-backend integration during development.

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

- Frontend API base uses `VITE_API_BASE_URL` with a localhost fallback in `frontend/src/components/Dashboard.vue`.
- CORS is enabled in the backend via `flask-cors`.
- Uploaded CSV files are stored in a temporary folder and dataset metadata is kept in memory.
- `GROQ_API_KEY` is read from environment variables in `backend/GroqService.py`.

## Free Render Deployment (No Blueprint)

Use two separate manual services on Render free tier.

Backend (Web Service):

- Runtime: Python
- Branch: `feature/docker-deployment` (or your main branch)
- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
- Environment Variables:
  - `GROQ_API_KEY=<your_real_key>`
  - `PYTHON_VERSION=3.11.0`

Frontend (Static Site):

- Branch: `feature/docker-deployment` (or your main branch)
- Root Directory: `frontend`
- Build Command: `npm install && npm run build`
- Publish Directory: `dist`
- Environment Variables:
  - `VITE_API_BASE_URL=<your_backend_render_url>`

Static site rewrite rule:

- Source: `/*`
- Destination: `/index.html`

Fallback if Root Directory is not available in your Render UI:

- Backend Build Command: `pip install -r backend/requirements.txt`
- Backend Start Command: `gunicorn --chdir backend app:app --bind 0.0.0.0:$PORT`
- Frontend Build Command: `cd frontend && npm install && npm run build`
- Frontend Publish Directory: `frontend/dist`

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
